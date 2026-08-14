#!/usr/bin/env python3
"""Convert a Marp-compatible Markdown slideshow to a self-contained interactive HTML file.

Supports:
- Keyboard/click slide navigation (arrows, space, escape)
- Mermaid diagram rendering via CDN
- Speaker notes panel (toggle with S key)
- Dark theme
- Images (relative paths preserved)
- Slide counter and progress bar
- Overview mode (toggle with O key)
- Print-friendly layout (Ctrl+P)
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import textwrap
from pathlib import Path

import yaml


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (metadata, remaining body)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}, text
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except Exception:
        meta = {}
    return meta, text[match.end():]


def parse_frontmatter_simple(text: str) -> tuple[dict, str]:
    """Fallback parser when PyYAML is not available."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip().strip('"').strip("'")
            val = val.strip().strip('"').strip("'")
            if val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            meta[key] = val
    return meta, text[match.end():]


def split_slides(body: str) -> list[str]:
    """Split the body into slides on --- separators."""
    parts = re.split(r"\n---\s*\n", body)
    return [p.strip() for p in parts if p.strip()]


def extract_speaker_notes(slide_md: str) -> tuple[str, str]:
    """Extract speaker notes from HTML comments, return (content, notes)."""
    notes_parts = []
    def replacer(m):
        text = m.group(1).strip()
        if text.lower().startswith("speaker notes:"):
            text = text[len("speaker notes:"):].strip()
        elif text.lower().startswith("speaker notes\n"):
            text = text[len("speaker notes"):].strip()
        notes_parts.append(text)
        return ""

    content = re.sub(
        r"<!--\s*[Ss]peaker\s+[Nn]otes\s*:?\s*(.*?)-->",
        replacer,
        slide_md,
        flags=re.DOTALL,
    )
    # Remove non-speaker HTML comments that are directives (like _class)
    directives = re.findall(r"<!--\s*(_class:\s*\S+)\s*-->", content)
    content = re.sub(r"<!--\s*_class:\s*\S+\s*-->", "", content)
    # Strip stray <script> tags that may exist in the source markdown
    content = re.sub(r"<script[^>]*>.*?</script>", "", content, flags=re.DOTALL)
    return content.strip(), "\n\n".join(notes_parts), directives


def md_to_html(md: str, mermaid_collector: list | None = None) -> str:
    """Minimal Markdown to HTML conversion for slide content."""
    if mermaid_collector is None:
        mermaid_collector = []
    lines = md.split("\n")
    result = []
    in_code = False
    in_mermaid = False
    in_list = False
    in_table = False
    code_lang = ""
    code_lines = []
    table_rows = []
    list_items = []

    def flush_list():
        nonlocal in_list, list_items
        if list_items:
            ordered = list_items[0][0]
            tag = "ol" if ordered else "ul"
            items_html = "".join(f"<li>{item}</li>" for _, item in list_items)
            result.append(f"<{tag}>{items_html}</{tag}>")
            list_items = []
            in_list = False

    def flush_table():
        nonlocal in_table, table_rows
        if table_rows:
            header = table_rows[0]
            body = [r for r in table_rows[1:] if not re.match(r"^\s*\|[-\s:|]+\|\s*$", "|".join(r))]
            html_parts = ['<div class="table-wrapper"><table>']
            html_parts.append("<thead><tr>")
            for cell in header:
                html_parts.append(f"<th>{inline_format(cell.strip())}</th>")
            html_parts.append("</tr></thead>")
            if body:
                html_parts.append("<tbody>")
                for row in body:
                    html_parts.append("<tr>")
                    for cell in row:
                        html_parts.append(f"<td>{inline_format(cell.strip())}</td>")
                    html_parts.append("</tr>")
                html_parts.append("</tbody>")
            html_parts.append("</table></div>")
            result.append("".join(html_parts))
            table_rows = []
            in_table = False

    def inline_format(text: str) -> str:
        """Apply inline formatting: bold, italic, code, links, images."""
        # Images
        text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" />', text)
        # Links
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
        # Bold
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
        # Italic
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
        # Inline code
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        return text

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code fences
        fence_match = re.match(r"^```(\w*)", line)
        if fence_match and not in_code:
            flush_list()
            flush_table()
            code_lang = fence_match.group(1).lower()
            in_code = True
            in_mermaid = code_lang == "mermaid"
            code_lines = []
            i += 1
            continue
        if in_code and line.strip() == "```":
            if in_mermaid:
                mermaid_src = "\n".join(code_lines)
                mermaid_src = re.sub(r"<script[^>]*>.*?</script>", "", mermaid_src, flags=re.DOTALL)
                mermaid_src = re.sub(r"^\s*%%\{init:.*?\}%%\s*$", "", mermaid_src, flags=re.MULTILINE).strip()
                # Store index, collect source later via mermaid_collector
                idx = len(mermaid_collector)
                mermaid_collector.append(mermaid_src)
                result.append(f'<div class="mermaid-diagram" data-mermaid-index="{idx}"></div>')
            else:
                escaped = html.escape("\n".join(code_lines))
                lang_class = f' class="language-{code_lang}"' if code_lang else ""
                result.append(f"<pre><code{lang_class}>{escaped}</code></pre>")
            in_code = False
            in_mermaid = False
            code_lines = []
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Table rows
        if re.match(r"^\s*\|.*\|\s*$", line):
            flush_list()
            stripped = line.strip()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # Skip separator rows
            if re.match(r"^\s*\|[-\s:|]+\|\s*$", stripped):
                i += 1
                continue
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            i += 1
            continue
        else:
            flush_table()

        # Headings
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            flush_list()
            level = len(heading_match.group(1))
            text = inline_format(heading_match.group(2))
            result.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # Unordered list
        ul_match = re.match(r"^(\s*)[*\-+]\s+(.+)$", line)
        if ul_match:
            flush_table()
            if not in_list:
                in_list = True
            list_items.append((False, inline_format(ul_match.group(2))))
            i += 1
            continue

        # Ordered list
        ol_match = re.match(r"^(\s*)\d+\.\s+(.+)$", line)
        if ol_match:
            flush_table()
            if not in_list:
                in_list = True
            list_items.append((True, inline_format(ol_match.group(2))))
            i += 1
            continue

        flush_list()

        # Horizontal rule
        if re.match(r"^[-*_]{3,}\s*$", line):
            result.append("<hr />")
            i += 1
            continue

        # Blank line
        if not line.strip():
            i += 1
            continue

        # Paragraph
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6}\s|```|[*\-+]\s|\d+\.\s|\|)", lines[i]):
            para_lines.append(lines[i])
            i += 1
        result.append(f"<p>{inline_format(' '.join(para_lines))}</p>")

    flush_list()
    flush_table()
    return "\n".join(result)


def build_slide_html(content: str, notes: str, directives: list, index: int, total: int, mermaid_collector: list) -> str:
    """Build HTML for a single slide."""
    css_class = ""
    for d in directives:
        m = re.match(r"_class:\s*(\S+)", d)
        if m:
            css_class = m.group(1)

    slide_class = f"slide {css_class}".strip()
    content_html = md_to_html(content, mermaid_collector)

    notes_html = ""
    if notes:
        notes_html = f'<div class="speaker-notes">{md_to_html(notes)}</div>'

    return f'<div class="{slide_class}" data-slide="{index}">\n<div class="slide-content">\n{content_html}\n</div>\n{notes_html}\n</div>'


HTML_TEMPLATE = textwrap.dedent("""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<style>
:root {{
  --bg: #1e1e2e;
  --bg-slide: #24243a;
  --fg: #e0e0e8;
  --fg-dim: #a0a0b0;
  --accent: #7aa2f7;
  --accent-dim: #3d5a9a;
  --green: #9ece6a;
  --orange: #e0af68;
  --red: #f7768e;
  --code-bg: #1a1b26;
  --border: #414168;
  --notes-bg: #1a1a2e;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

html, body {{
  height: 100%;
  background: var(--bg);
  color: var(--fg);
  font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
  overflow: hidden;
}}

/* Slide container */
.deck {{
  position: relative;
  width: 100%;
  height: 100%;
}}

.slide {{
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  display: none;
  flex-direction: column;
  justify-content: center;
  padding: 60px 80px;
  background: var(--bg-slide);
  overflow-y: auto;
}}

.slide.active {{
  display: flex;
}}

.slide-content {{
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}}

/* Lead / section break slides */
.slide.lead {{
  text-align: center;
  justify-content: center;
}}

.slide.lead h1 {{
  font-size: 2.8em;
  margin-bottom: 0.3em;
}}

.slide.lead p {{
  font-size: 1.4em;
  color: var(--fg-dim);
}}

/* Typography */
h1 {{
  font-size: 2.2em;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 0.4em;
  line-height: 1.2;
}}

h2 {{
  font-size: 1.7em;
  font-weight: 600;
  color: var(--accent);
  margin-bottom: 0.5em;
  line-height: 1.3;
  border-bottom: 2px solid var(--accent-dim);
  padding-bottom: 0.2em;
}}

h3 {{
  font-size: 1.3em;
  font-weight: 600;
  color: var(--fg);
  margin-bottom: 0.4em;
}}

p {{
  font-size: 1.15em;
  line-height: 1.6;
  margin-bottom: 0.6em;
  color: var(--fg);
}}

strong {{ color: var(--orange); font-weight: 700; }}

em {{ color: var(--fg-dim); font-style: italic; }}

a {{ color: var(--accent); text-decoration: underline; }}

/* Lists */
ul, ol {{
  padding-left: 1.8em;
  margin-bottom: 0.6em;
}}

li {{
  font-size: 1.15em;
  line-height: 1.7;
  margin-bottom: 0.3em;
  color: var(--fg);
}}

/* Code */
code {{
  background: var(--code-bg);
  padding: 0.15em 0.4em;
  border-radius: 4px;
  font-family: 'Cascadia Code', 'Fira Code', 'JetBrains Mono', 'Consolas', monospace;
  font-size: 0.9em;
  color: var(--green);
}}

pre {{
  background: var(--code-bg);
  padding: 1em 1.2em;
  border-radius: 8px;
  border: 1px solid var(--border);
  overflow-x: auto;
  margin: 0.8em 0;
}}

pre code {{
  background: none;
  padding: 0;
  font-size: 0.85em;
  line-height: 1.5;
  color: var(--fg);
}}

/* Tables */
.table-wrapper {{
  overflow-x: auto;
  margin: 0.8em 0;
}}

table {{
  border-collapse: collapse;
  width: 100%;
  font-size: 1em;
}}

th {{
  background: var(--accent-dim);
  color: #fff;
  font-weight: 600;
  padding: 0.6em 1em;
  text-align: left;
  border: 1px solid var(--border);
}}

td {{
  padding: 0.5em 1em;
  border: 1px solid var(--border);
  color: var(--fg);
}}

tr:nth-child(even) td {{
  background: rgba(255,255,255,0.03);
}}

/* Images */
img {{
  max-width: 90%;
  max-height: 60vh;
  display: block;
  margin: 1em auto;
  border-radius: 6px;
}}

hr {{
  border: none;
  border-top: 1px solid var(--border);
  margin: 1em 0;
}}

/* Mermaid */
.mermaid-diagram {{
  background: transparent;
  text-align: center;
  padding: 0.5em 0;
  margin: 0.8em 0;
}}

.mermaid-diagram svg {{
  max-width: 100%;
  height: auto;
}}

/* Navigation bar */
.nav-bar {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 44px;
  background: rgba(20, 20, 36, 0.95);
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  z-index: 100;
  backdrop-filter: blur(8px);
}}

.nav-bar .slide-counter {{
  color: var(--fg-dim);
  font-size: 0.9em;
  font-variant-numeric: tabular-nums;
}}

.progress-bar {{
  position: fixed;
  bottom: 44px;
  left: 0;
  height: 3px;
  background: var(--accent);
  transition: width 0.3s ease;
  z-index: 100;
}}

.nav-bar .controls {{
  display: flex;
  gap: 8px;
}}

.nav-bar button {{
  background: transparent;
  border: 1px solid var(--border);
  color: var(--fg-dim);
  padding: 4px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85em;
}}

.nav-bar button:hover {{
  background: var(--accent-dim);
  color: #fff;
}}

.nav-bar button.active {{
  background: var(--accent-dim);
  color: #fff;
  border-color: var(--accent);
}}

/* Header / footer */
.slide-header {{
  position: absolute;
  top: 16px;
  left: 30px;
  right: 30px;
  font-size: 0.8em;
  color: var(--fg-dim);
  opacity: 0.7;
}}

.slide-footer {{
  position: absolute;
  bottom: 54px;
  left: 30px;
  right: 30px;
  font-size: 0.75em;
  color: var(--fg-dim);
  opacity: 0.5;
  text-align: right;
}}

/* Speaker notes panel */
.notes-panel {{
  position: fixed;
  bottom: 44px;
  left: 0;
  right: 0;
  max-height: 30vh;
  background: var(--notes-bg);
  border-top: 2px solid var(--accent);
  padding: 16px 24px;
  overflow-y: auto;
  display: none;
  z-index: 90;
  font-size: 0.95em;
  line-height: 1.5;
  color: var(--fg-dim);
}}

.notes-panel.visible {{
  display: block;
}}

.notes-panel h3 {{
  color: var(--accent);
  font-size: 0.85em;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.5em;
}}

.speaker-notes {{
  display: none;
}}

/* Overview mode */
.deck.overview {{
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 20px;
  overflow-y: auto;
}}

.deck.overview .slide {{
  position: relative;
  display: flex !important;
  width: 280px;
  height: 180px;
  padding: 16px 20px;
  border-radius: 8px;
  border: 2px solid var(--border);
  cursor: pointer;
  flex-shrink: 0;
  overflow: hidden;
  font-size: 0.45em;
}}

.deck.overview .slide.active {{
  border-color: var(--accent);
  box-shadow: 0 0 12px rgba(122, 162, 247, 0.3);
}}

.deck.overview .slide:hover {{
  border-color: var(--accent-dim);
}}

.deck.overview .slide-header,
.deck.overview .slide-footer {{
  display: none;
}}

/* Print */
@media print {{
  .nav-bar, .progress-bar, .notes-panel {{ display: none !important; }}
  .slide {{
    position: relative !important;
    display: flex !important;
    page-break-after: always;
    height: 100vh;
    border-bottom: 1px solid #ccc;
  }}
  .slide-header, .slide-footer {{ display: none; }}
}}

/* Responsive */
@media (max-width: 768px) {{
  .slide {{ padding: 30px 24px; }}
  h1 {{ font-size: 1.6em; }}
  h2 {{ font-size: 1.3em; }}
  p, li {{ font-size: 1em; }}
}}
</style>
</head>
<body>

<div class="deck" id="deck">
{header_el}
{slides_html}
{footer_el}
</div>

<div class="notes-panel" id="notesPanel">
  <h3>Speaker Notes</h3>
  <div id="notesContent"></div>
</div>

<div class="progress-bar" id="progressBar"></div>

<div class="nav-bar">
  <span class="slide-counter" id="slideCounter">1 / 1</span>
  <div class="controls">
    <button onclick="prevSlide()" title="Previous (←)">&#9664; Prev</button>
    <button onclick="nextSlide()" title="Next (→)">Next &#9654;</button>
    <button id="notesBtn" onclick="toggleNotes()" title="Speaker notes (S)">Notes</button>
    <button id="overviewBtn" onclick="toggleOverview()" title="Overview (O)">Grid</button>
  </div>
</div>

<script id="mermaid-sources" type="application/json">{mermaid_json}</script>

<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({{
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {{
    primaryColor: '#3d5a9a',
    primaryTextColor: '#e0e0e8',
    primaryBorderColor: '#7aa2f7',
    lineColor: '#7aa2f7',
    secondaryColor: '#24243a',
    tertiaryColor: '#1e1e2e',
    fontSize: '14px',
  }}
}});
const sources = JSON.parse(document.getElementById('mermaid-sources').textContent);
const targets = document.querySelectorAll('.mermaid-diagram');
for (const el of targets) {{
  const idx = parseInt(el.dataset.mermaidIndex, 10);
  try {{
    const {{ svg }} = await mermaid.render('mermaid-svg-' + idx, sources[idx]);
    el.innerHTML = svg;
  }} catch (e) {{
    el.innerHTML = '<pre style="color:#f7768e;">Mermaid render error: ' + e.message + '</pre>';
  }}
}}
</script>

<script>
(function() {{
  const slides = document.querySelectorAll('.slide');
  const counter = document.getElementById('slideCounter');
  const progressBar = document.getElementById('progressBar');
  const notesPanel = document.getElementById('notesPanel');
  const notesContent = document.getElementById('notesContent');
  const notesBtn = document.getElementById('notesBtn');
  const overviewBtn = document.getElementById('overviewBtn');
  const deck = document.getElementById('deck');
  let current = 0;
  let showNotes = false;
  let overviewMode = false;

  const speakerNotes = {notes_json};

  function goTo(n) {{
    if (n < 0 || n >= slides.length) return;
    slides[current].classList.remove('active');
    current = n;
    slides[current].classList.add('active');
    counter.textContent = (current + 1) + ' / ' + slides.length;
    progressBar.style.width = ((current + 1) / slides.length * 100) + '%';
    if (showNotes) {{
      notesContent.innerHTML = speakerNotes[current] || '<em>No notes for this slide.</em>';
    }}
  }}

  window.nextSlide = function() {{
    if (overviewMode) return;
    goTo(current + 1);
  }};

  window.prevSlide = function() {{
    if (overviewMode) return;
    goTo(current - 1);
  }};

  window.toggleNotes = function() {{
    showNotes = !showNotes;
    notesPanel.classList.toggle('visible', showNotes);
    notesBtn.classList.toggle('active', showNotes);
    if (showNotes) {{
      notesContent.innerHTML = speakerNotes[current] || '<em>No notes for this slide.</em>';
    }}
  }};

  window.toggleOverview = function() {{
    overviewMode = !overviewMode;
    deck.classList.toggle('overview', overviewMode);
    overviewBtn.classList.toggle('active', overviewMode);
    if (!overviewMode) {{
      goTo(current);
    }}
  }};

  // Keyboard navigation
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'ArrowRight' || e.key === ' ') {{
      e.preventDefault();
      if (overviewMode) return;
      nextSlide();
    }} else if (e.key === 'ArrowLeft') {{
      e.preventDefault();
      if (overviewMode) return;
      prevSlide();
    }} else if (e.key === 'Home') {{
      e.preventDefault();
      goTo(0);
    }} else if (e.key === 'End') {{
      e.preventDefault();
      goTo(slides.length - 1);
    }} else if (e.key === 's' || e.key === 'S') {{
      toggleNotes();
    }} else if (e.key === 'o' || e.key === 'O') {{
      toggleOverview();
    }} else if (e.key === 'Escape') {{
      if (overviewMode) toggleOverview();
      if (showNotes) toggleNotes();
    }} else if (e.key === 'f' || e.key === 'F') {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen();
      }} else {{
        document.exitFullscreen();
      }}
    }}
  }});

  // Click on slide in overview to jump
  slides.forEach(function(slide, i) {{
    slide.addEventListener('click', function() {{
      if (overviewMode) {{
        toggleOverview();
        goTo(i);
      }}
    }});
  }});

  // Touch support
  let touchStartX = 0;
  document.addEventListener('touchstart', function(e) {{
    touchStartX = e.changedTouches[0].clientX;
  }});
  document.addEventListener('touchend', function(e) {{
    const diff = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(diff) > 50) {{
      if (diff < 0) nextSlide();
      else prevSlide();
    }}
  }});

  // Initialize
  goTo(0);
}})();
</script>
</body>
</html>
""")


def generate_html(input_path: Path, output_path: Path | None = None) -> Path:
    """Convert a Marp markdown file to an interactive HTML slideshow."""
    text = input_path.read_text(encoding="utf-8")

    # Parse frontmatter
    try:
        meta, body = parse_frontmatter(text)
    except Exception:
        meta, body = parse_frontmatter_simple(text)

    title = meta.get("header", meta.get("title", input_path.stem))
    header_text = meta.get("header", "")
    footer_text = meta.get("footer", "")

    # Split into slides
    raw_slides = split_slides(body)

    slides_html_parts = []
    all_notes = []
    mermaid_sources = []

    for i, slide_md in enumerate(raw_slides):
        content, notes, directives = extract_speaker_notes(slide_md)
        slide_html = build_slide_html(content, notes, directives, i, len(raw_slides), mermaid_sources)
        slides_html_parts.append(slide_html)
        all_notes.append(md_to_html(notes) if notes else "")

    # Build header/footer elements
    header_el = ""
    if header_text:
        header_el = f'<div class="slide-header">{html.escape(str(header_text))}</div>'
    footer_el = ""
    if footer_text:
        footer_el = f'<div class="slide-footer">{html.escape(str(footer_text))}</div>'

    import json
    notes_json = json.dumps(all_notes)
    mermaid_json = json.dumps(mermaid_sources)

    final_html = HTML_TEMPLATE.format(
        title=html.escape(str(title)),
        header_el=header_el,
        slides_html="\n".join(slides_html_parts),
        footer_el=footer_el,
        notes_json=notes_json,
        mermaid_json=mermaid_json,
    )

    if output_path is None:
        output_path = input_path.with_suffix(".html")

    output_path.write_text(final_html, encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert Marp Markdown slideshow to interactive HTML."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to the Marp-compatible Markdown file (e.g. Findings.md).",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output HTML file path. Defaults to <input>.html.",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"error: input file not found: {args.input}", file=sys.stderr)
        return 1

    try:
        out = generate_html(args.input, args.output)
        print(out)
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
