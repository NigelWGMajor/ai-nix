"""Convert Confluence storage-format HTML to Markdown with full code-block preservation.

Usage: python convert_confluence.py <input.json> <output.md>

Reads a JSON file from the Confluence REST API v1 (body.storage expansion)
and produces a Markdown file with YAML frontmatter.
"""

import json
import re
import sys
import html as html_mod
from pathlib import Path


def extract_cdata(text: str) -> str:
    """Extract text from CDATA wrapper if present."""
    text = text.strip()
    if text.startswith("<![CDATA["):
        text = text[9:]
    if text.endswith("]]>"):
        text = text[:-3]
    return text


def process_code_macros(storage_html: str) -> str:
    """Replace ac:structured-macro code/noformat blocks with markdown fences BEFORE
    the general HTML-to-markdown pass, so they aren't lost."""

    def replace_code_macro(match):
        block = match.group(0)

        # Determine language
        lang_match = re.search(
            r'<ac:parameter\s+ac:name="language">([^<]+)</ac:parameter>',
            block,
        )
        lang = lang_match.group(1).strip() if lang_match else ""

        # Determine title
        title_match = re.search(
            r'<ac:parameter\s+ac:name="title">([^<]+)</ac:parameter>',
            block,
        )
        title = title_match.group(1).strip() if title_match else ""

        # Extract the actual content from plain-text-body
        ptb_match = re.search(
            r"<ac:plain-text-body>(.*?)</ac:plain-text-body>", block, re.DOTALL
        )
        if ptb_match:
            content = extract_cdata(ptb_match.group(1))
        else:
            content = ""

        # Build markdown
        parts = []
        if title:
            parts.append(f"**{title}**")
        parts.append(f"```{lang}")
        parts.append(content)
        parts.append("```")
        return "\n".join(parts)

    # Replace code and noformat macros
    result = re.sub(
        r'<ac:structured-macro[^>]*ac:name="(?:code|noformat)"[^>]*>.*?</ac:structured-macro>',
        replace_code_macro,
        storage_html,
        flags=re.DOTALL,
    )
    return result


def process_info_macros(storage_html: str) -> str:
    """Convert info/note/warning/tip macros to blockquotes."""

    def replace_info_macro(match):
        macro_type = match.group(1)
        block = match.group(0)

        rtb_match = re.search(
            r"<ac:rich-text-body>(.*?)</ac:rich-text-body>", block, re.DOTALL
        )
        if rtb_match:
            content = rtb_match.group(1).strip()
        else:
            content = ""

        prefix_map = {
            "info": "ℹ️ Info",
            "note": "📝 Note",
            "warning": "⚠️ Warning",
            "tip": "💡 Tip",
        }
        prefix = prefix_map.get(macro_type, macro_type.title())
        return f"\n> **{prefix}:** {content}\n"

    result = re.sub(
        r'<ac:structured-macro[^>]*ac:name="(info|note|warning|tip)"[^>]*>.*?</ac:structured-macro>',
        replace_info_macro,
        storage_html,
        flags=re.DOTALL,
    )
    return result


def process_panel_macros(storage_html: str) -> str:
    """Convert panel macros to blockquotes."""

    def replace_panel(match):
        block = match.group(0)

        title_match = re.search(
            r'<ac:parameter\s+ac:name="title">([^<]+)</ac:parameter>', block
        )
        title = title_match.group(1).strip() if title_match else ""

        rtb_match = re.search(
            r"<ac:rich-text-body>(.*?)</ac:rich-text-body>", block, re.DOTALL
        )
        content = rtb_match.group(1).strip() if rtb_match else ""

        parts = []
        if title:
            parts.append(f"> **{title}**")
        parts.append(f"> {content}")
        return "\n".join(parts)

    result = re.sub(
        r'<ac:structured-macro[^>]*ac:name="panel"[^>]*>.*?</ac:structured-macro>',
        replace_panel,
        storage_html,
        flags=re.DOTALL,
    )
    return result


def process_expand_macros(storage_html: str) -> str:
    """Convert expand macros to <details> blocks."""

    def replace_expand(match):
        block = match.group(0)

        title_match = re.search(
            r'<ac:parameter\s+ac:name="title">([^<]+)</ac:parameter>', block
        )
        if not title_match:
            # Some expand macros use first parameter without name
            title_match = re.search(
                r"<ac:parameter[^>]*>([^<]+)</ac:parameter>", block
            )
        title = title_match.group(1).strip() if title_match else "Details"

        rtb_match = re.search(
            r"<ac:rich-text-body>(.*?)</ac:rich-text-body>", block, re.DOTALL
        )
        content = rtb_match.group(1).strip() if rtb_match else ""

        return f"\n<details>\n<summary>{title}</summary>\n\n{content}\n\n</details>\n"

    result = re.sub(
        r'<ac:structured-macro[^>]*ac:name="expand"[^>]*>.*?</ac:structured-macro>',
        replace_expand,
        storage_html,
        flags=re.DOTALL,
    )
    return result


def process_images(storage_html: str) -> str:
    """Convert ac:image to markdown image placeholders."""

    def replace_image(match):
        block = match.group(0)
        alt_match = re.search(r'ac:alt="([^"]*)"', block)
        filename_match = re.search(r'ri:filename="([^"]*)"', block)

        alt = alt_match.group(1) if alt_match else ""
        filename = filename_match.group(1) if filename_match else ""

        label = alt or filename or "image"
        return f"<!-- [image: {label}] -->"

    result = re.sub(r"<ac:image[^>]*>.*?</ac:image>", replace_image, storage_html, flags=re.DOTALL)
    result = re.sub(r"<ac:image[^/]*/\s*>", lambda m: "<!-- [image] -->", result)
    return result


def process_emoticons(storage_html: str) -> str:
    """Convert Confluence emoticons to unicode equivalents."""
    emoticon_map = {
        "smile": "😊",
        "sad": "😢",
        "tongue": "😛",
        "biggrin": "😄",
        "wink": "😉",
        "thumbs-up": "👍",
        "thumbs-down": "👎",
        "information": "ℹ️",
        "tick": "✅",
        "cross": "❌",
        "warning": "⚠️",
        "plus": "➕",
        "minus": "➖",
        "question": "❓",
        "light-on": "💡",
        "light-off": "💡",
        "yellow-star": "⭐",
        "red-star": "⭐",
        "green-star": "⭐",
        "blue-star": "⭐",
    }

    def replace_emoticon(match):
        name = match.group(1)
        return emoticon_map.get(name, f"[:{name}:]")

    result = re.sub(
        r'<ac:emoticon\s+ac:name="([^"]+)"\s*/>', replace_emoticon, storage_html
    )
    return result


def strip_remaining_ac_tags(html_text: str) -> str:
    """Remove any remaining ac: tags that weren't handled, preserving their text content."""
    # Remove breakoutMode and other layout macros entirely (they're structural, not content)
    html_text = re.sub(
        r'<ac:structured-macro[^>]*ac:name="(?:breakoutMode|layoutSection|layoutCell|layout)"[^>]*>.*?</ac:structured-macro>',
        lambda m: re.sub(r"<[^>]+>", "", m.group(0)),
        html_text,
        flags=re.DOTALL,
    )
    # Strip remaining ac: open/close tags but keep content
    html_text = re.sub(r"</?ac:[^>]+>", "", html_text)
    html_text = re.sub(r"</?ri:[^>]+>", "", html_text)
    return html_text


def html_to_markdown(html_text: str) -> str:
    """Convert cleaned HTML (after macro processing) to Markdown."""
    text = html_text

    # Headings
    for level in range(6, 0, -1):
        text = re.sub(
            rf"<h{level}[^>]*>(.*?)</h{level}>",
            lambda m, l=level: f"\n{'#' * l} {m.group(1).strip()}\n",
            text,
            flags=re.DOTALL,
        )

    # Bold
    text = re.sub(r"<(?:strong|b)>(.*?)</(?:strong|b)>", r"**\1**", text, flags=re.DOTALL)
    # Italic
    text = re.sub(r"<(?:em|i)>(.*?)</(?:em|i)>", r"*\1*", text, flags=re.DOTALL)
    # Inline code
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)
    # Strikethrough
    text = re.sub(r"<(?:del|s)>(.*?)</(?:del|s)>", r"~~\1~~", text, flags=re.DOTALL)
    # Underline (no markdown equivalent, just strip)
    text = re.sub(r"</?u>", "", text)

    # Links
    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r"[\2](\1)", text, flags=re.DOTALL)

    # Pre blocks (that weren't already converted via macro processing)
    text = re.sub(
        r"<pre[^>]*>(.*?)</pre>",
        lambda m: f"\n```\n{html_mod.unescape(m.group(1).strip())}\n```\n",
        text,
        flags=re.DOTALL,
    )

    # Tables
    def convert_table(match):
        table_html = match.group(0)
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, re.DOTALL)
        if not rows:
            return ""

        md_rows = []
        for i, row in enumerate(rows):
            cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.DOTALL)
            cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
            md_rows.append("| " + " | ".join(cells) + " |")
            if i == 0:
                md_rows.append("| " + " | ".join(["---"] * len(cells)) + " |")

        return "\n" + "\n".join(md_rows) + "\n"

    text = re.sub(r"<table[^>]*>.*?</table>", convert_table, text, flags=re.DOTALL)

    # Lists — process inside-out to handle nesting correctly.
    # First, inline <p> tags inside <li> so they don't inject newlines.
    def _inline_p_in_li(text):
        """Strip <p> wrappers inside <li> elements to keep content on one line."""
        def strip_p_in_li(m):
            li_content = m.group(1)
            li_content = re.sub(r"<p[^>]*>(.*?)</p>", r"\1", li_content, flags=re.DOTALL)
            return f"<li>{li_content.strip()}</li>"
        return re.sub(r"<li[^>]*>(.*?)</li>", strip_p_in_li, text, flags=re.DOTALL)

    text = _inline_p_in_li(text)

    def convert_list(match):
        tag = match.group(1)  # "ul" or "ol"
        inner = match.group(2)
        is_ordered = tag == "ol"

        items = re.findall(r"<li[^>]*>(.*?)</li>", inner, re.DOTALL)
        lines = []
        for idx, item in enumerate(items):
            content = item.strip()
            prefix = f"{idx + 1}. " if is_ordered else "- "
            lines.append(f"{prefix}{content}")
        return "\n" + "\n".join(lines) + "\n"

    # Process innermost lists first (up to 5 nesting levels)
    for _ in range(5):
        prev = text
        text = re.sub(
            r"<(ul|ol)[^>]*>((?:(?!<(?:ul|ol)[^>]*>).)*?)</\1>",
            convert_list,
            text,
            flags=re.DOTALL,
        )
        if text == prev:
            break

    # Task lists (inline tasks outside of normal lists)
    text = re.sub(
        r'<li[^>]*data-inline-task-id="[^"]*"[^>]*>(.*?)</li>',
        lambda m: f"- [ ] {re.sub(r'<p[^>]*>(.*?)</p>', r'\\1', m.group(1), flags=re.DOTALL).strip()}",
        text,
        flags=re.DOTALL,
    )

    # Blockquotes
    text = re.sub(
        r"<blockquote[^>]*>(.*?)</blockquote>",
        lambda m: "\n> " + m.group(1).strip() + "\n",
        text,
        flags=re.DOTALL,
    )

    # Horizontal rule
    text = re.sub(r"<hr\s*/?>", "\n---\n", text)

    # Line breaks
    text = re.sub(r"<br\s*/?>", "\n", text)

    # Paragraphs (only remaining <p> tags not already handled inside lists)
    text = re.sub(r"<p[^>]*>(.*?)</p>", r"\n\1\n", text, flags=re.DOTALL)

    # Divs and spans (strip, keep content)
    text = re.sub(r"</?(?:div|span)[^>]*>", "", text)

    # Strip any remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Unescape HTML entities
    text = html_mod.unescape(text)

    # Fix code fences glued to preceding text (from code blocks inside list items)
    text = re.sub(r"([^\n])```", r"\1\n```", text)

    # Clean up excessive blank lines
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    return text.strip()


def convert(json_path: str, output_path: str):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "Untitled")
    version = data.get("version", {}).get("number", "?")
    space = data.get("space", {}).get("key", "?")
    source_url = data.get("_links", {}).get("base", "https://degreedjira.atlassian.net/wiki") + \
                 data.get("_links", {}).get("webui", "")

    ancestors = data.get("ancestors", [])
    parent = ancestors[-1].get("title", "") if ancestors else ""

    storage_html = data.get("body", {}).get("storage", {}).get("value", "")

    if not storage_html:
        print("ERROR: No body.storage.value found in JSON", file=sys.stderr)
        sys.exit(1)

    # Count macros before processing for verification
    code_count_before = len(
        re.findall(r'<ac:structured-macro[^>]*ac:name="(?:code|noformat)"', storage_html)
    )
    ptb_count_before = len(
        re.findall(r"<ac:plain-text-body>", storage_html)
    )

    # Step 1: Process macros (BEFORE general HTML conversion)
    processed = process_code_macros(storage_html)
    processed = process_info_macros(processed)
    processed = process_panel_macros(processed)
    processed = process_expand_macros(processed)
    processed = process_images(processed)
    processed = process_emoticons(processed)
    processed = strip_remaining_ac_tags(processed)

    # Step 2: Convert remaining HTML to markdown
    markdown = html_to_markdown(processed)

    # Step 3: Count code fences in output for verification
    code_fences = re.findall(r"^```", markdown, re.MULTILINE)
    fence_pairs = len(code_fences) // 2

    # Step 4: Check for empty code fences
    empty_fences = re.findall(r"```[^\n]*\n\s*\n?```", markdown)
    capture_gaps = []
    if empty_fences:
        for i, fence in enumerate(empty_fences):
            # Find surrounding context
            pos = markdown.find(fence)
            context_start = max(0, pos - 200)
            context = markdown[context_start:pos].strip().split("\n")
            heading = next(
                (line for line in reversed(context) if line.startswith("#")),
                "(no heading context)",
            )
            capture_gaps.append(
                f"- Empty code block near: {heading.strip()} — content may be an image or genuinely empty on source page"
            )

    # Build frontmatter
    from datetime import date
    frontmatter = f"""---
source: "{source_url}"
captured: "{date.today().isoformat()}"
title: "{title}"
type: "confluence"
space: "{space}"
parent: "{parent}"
version: {version}
---"""

    # Build output
    output = frontmatter + "\n\n" + markdown

    # Append capture gaps section if any
    if capture_gaps:
        output += "\n\n## Capture gaps\n\n"
        output += "\n".join(capture_gaps)
        output += "\n"

    # Write
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    # Report
    print(f"Converted: {title}")
    print(f"  Source macros: {code_count_before} code/noformat, {ptb_count_before} plain-text-body")
    print(f"  Output fences: {fence_pairs} code blocks")
    print(f"  Empty fences: {len(empty_fences)}")
    if capture_gaps:
        print(f"  Capture gaps: {len(capture_gaps)} (see ## Capture gaps in output)")
    else:
        print("  Capture gaps: none")
    print(f"  Output: {output_path} ({Path(output_path).stat().st_size} bytes)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.json> <output.md>", file=sys.stderr)
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
