#!/usr/bin/env python3
"""Render the DAC introduction Markdown to one self-contained HTML file.

Standard library only. Handles the Markdown subset the introduction uses:
headings, paragraphs, bullet and numbered lists, tables, fenced code, bold,
italic, and inline code. A ```mermaid fence becomes a live diagram loaded from
a CDN; offline, the diagram stays visible as readable source.

Output goes to the output base, never the skill folder:
  TOOLING_OUTPUT_PATH absolute            -> that folder
  TOOLING_OUTPUT_PATH starting ./ or .\\   -> relative to the repository root
  unset                                    -> <repository-root>/.data
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
from pathlib import Path

OUTPUT_NAME = "dac-introduction.html"
MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"

CSS = """
:root { color-scheme: dark; }
body { background:#0f1419; color:#d8dee9; font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif;
       margin:0; }
main { max-width:900px; margin:0 auto; padding:2rem 1.25rem 4rem; }
h1 { font-size:2rem; border-bottom:1px solid #2e3a46; padding-bottom:.4rem; }
h2 { font-size:1.4rem; margin-top:2.2rem; color:#9ecbff; }
a { color:#9ecbff; }
code { background:#1b2430; padding:.1rem .35rem; border-radius:4px; font-size:.92em; }
pre { background:#1b2430; padding:1rem; border-radius:6px; overflow:auto; }
pre code { background:none; padding:0; }
pre.mermaid { background:#141b23; text-align:center; color:#9aa7b4; }
table { border-collapse:collapse; margin:1rem 0; width:100%; }
th, td { border:1px solid #2e3a46; padding:.5rem .7rem; text-align:left; vertical-align:top; }
th { background:#1b2430; }
li { margin:.25rem 0; }
"""


def inline(text: str) -> str:
    """Escape and format inline Markdown. Code spans are protected first."""
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        s = html.escape(part)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", s)
        out.append(s)
    return "".join(out)


def split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def is_table_sep(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$", line))


def convert(md: str) -> tuple[str, str]:
    """Return (title, body_html)."""
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    title = "DAC Introduction"
    paragraph: list[str] = []
    i = 0

    def flush_paragraph() -> None:
        if paragraph:
            out.append("<p>" + inline(" ".join(s.strip() for s in paragraph)) + "</p>")
            paragraph.clear()

    while i < len(lines):
        line = lines[i]

        fence = re.match(r"^```\s*(\w*)\s*$", line)
        if fence:
            flush_paragraph()
            lang = fence.group(1).lower()
            block: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            body = html.escape("\n".join(block))
            if lang == "mermaid":
                out.append(f'<pre class="mermaid">{body}</pre>')
            else:
                out.append(f"<pre><code>{body}</code></pre>")
            continue

        heading = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            if level == 1 and title == "DAC Introduction":
                title = re.sub(r"[`*]", "", heading.group(2))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        if "|" in line and i + 1 < len(lines) and is_table_sep(lines[i + 1]):
            flush_paragraph()
            header = split_row(line)
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in header)
                       + "</tr></thead><tbody>")
            for row in rows:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
            out.append("</tbody></table>")
            continue

        item = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if item:
            flush_paragraph()
            ordered = item.group(2)[0].isdigit()
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>")
            while i < len(lines):
                m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                if not m or m.group(2)[0].isdigit() != ordered:
                    break
                text = m.group(3)
                i += 1
                while i < len(lines) and lines[i].strip() and not re.match(
                    r"^(\s*)([-*]|\d+\.)\s+", lines[i]
                ) and not lines[i].startswith(("#", "```", "|")):
                    text += " " + lines[i].strip()
                    i += 1
                out.append(f"<li>{inline(text)}</li>")
            out.append(f"</{tag}>")
            continue

        if not line.strip():
            flush_paragraph()
        else:
            paragraph.append(line)
        i += 1

    flush_paragraph()
    return title, "\n".join(out)


def page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<main>
{body}
</main>
<script type="module">
// If the CDN is unreachable the import fails and the diagram stays visible as source.
import mermaid from '{MERMAID_CDN}';
mermaid.initialize({{ startOnLoad: false, theme: 'dark' }});
await mermaid.run({{ querySelector: 'pre.mermaid' }});
</script>
</body>
</html>
"""


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return start


def resolve_output_base(repo_root: Path, override: str | None) -> Path:
    raw = override if override is not None else os.environ.get("TOOLING_OUTPUT_PATH", "")
    raw = raw.strip()
    if not raw:
        return repo_root / ".data"
    if raw.startswith(("./", ".\\")):
        return (repo_root / raw).resolve()
    path = Path(raw)
    if path.is_absolute():
        return path
    raise ValueError(f"Reject relative output path {raw!r}: use an absolute path or one starting ./ or .\\")


def main() -> int:
    default_source = Path(__file__).resolve().parent.parent / "introduction.md"
    parser = argparse.ArgumentParser(description="Render the DAC introduction to HTML.")
    parser.add_argument("--source", type=Path, default=default_source, help="Markdown file to render")
    parser.add_argument("--repo-root", type=Path, default=None, help="Repository root (default: from cwd)")
    parser.add_argument("--output-base", default=None, help="Override TOOLING_OUTPUT_PATH")
    args = parser.parse_args()

    if not args.source.is_file():
        print(f"error: source not found: {args.source}", file=sys.stderr)
        return 1
    try:
        repo_root = (args.repo_root or find_repo_root(Path.cwd())).resolve()
        base = resolve_output_base(repo_root, args.output_base)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    title, body = convert(args.source.read_text(encoding="utf-8"))
    base.mkdir(parents=True, exist_ok=True)
    destination = base / OUTPUT_NAME
    destination.write_text(page(title, body), encoding="utf-8")
    print(destination)
    print(destination.resolve().as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
