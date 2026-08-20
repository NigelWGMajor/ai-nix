#!/usr/bin/env python3
"""Create a collision-safe, durable TUT tutorial instance."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path


def find_workspace(start: Path) -> Path:
    """Return the nearest ancestor that looks like a workspace."""
    start = start.expanduser().resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start


def alphabetic_suffix(index: int) -> str:
    """Convert zero-based indexes to a, b, ..., z, aa, ab, ... ."""
    if index < 0:
        raise ValueError("suffix index must be non-negative")
    value = index + 1
    result = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(ord("a") + remainder) + result
    return result


def slugify(text: str) -> str:
    """Convert text to a lowercase hyphenated slug suitable for filenames."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    text = text.strip("-")
    return text[:80]


def single_line(value: str) -> str:
    return " ".join(value.splitlines()).strip()


def write_text(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def control_text(
    created: str,
    topic: str,
    audience: str,
    outcome: str,
    depth: str,
    output_filename: str,
) -> str:
    return f"""
# TUT control

## Identity

- Status: initialized
- Created: {created}
- Topic: {topic}
- Audience: {audience}
- Outcome: {outcome}
- Depth: {depth.title()}
- Final document: `{output_filename}`

## Scope and evidence boundary

- Included: To be resolved from the request and workspace.
- Excluded: To be determined.
- External research: Not included unless requested or required by the topic.
- Mutation boundary: Read-only except this TUT instance.

## Current stage

Scope — ask clarifying questions.

## Completed work

- Created the tutorial instance and standard artifacts.

## Assumptions and open questions

- Record only assumptions that could materially affect the tutorial content or structure.

## Next safe action

Ask the user clarifying questions to frame the tutorial scope, audience, and outcome.
"""


EVIDENCE = """
# TUT evidence map

## Boundary and freshness

- Topic boundary:
- External evidence boundary:
- Freshness limitations:

## Material sources and references

| ID | Source or reference | Role | What it establishes | Limitation |
| --- | --- | --- | --- | --- |
| R001 | To be inspected | Unknown | | Unknown |

## Gaps and limitations

- Missing information:
- Platform or version constraints:
"""


OUTLINE = """
# TUT tutorial outline

## Prerequisites

- Tools:
- Access:
- Prior knowledge:

## Step sequence

1. [Step title] — [purpose]
2. [Step title] — [purpose]

## Diagram plan

- Overview diagram: [type and purpose]
- Detail diagram: [type and purpose, if Comprehensive]

## Verification checkpoints

- After step 1: [check]
- After step 2: [check]

## Troubleshooting plan (Comprehensive only)

- Common failure 1: [symptom and likely cause]
"""


def allocate_instance(data_dir: Path, date_value: str) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    for index in range(26 * 27):
        candidate = data_dir / f"tut-{date_value}-{alphabetic_suffix(index)}"
        try:
            candidate.mkdir()
            return candidate
        except FileExistsError:
            continue
    raise RuntimeError("could not allocate an available TUT instance suffix")


def build_output_filename(slug: str | None, topic: str, part: str | None) -> str:
    """Build the descriptive output filename from slug/topic and optional part."""
    effective_slug = slug if slug else slugify(topic)
    if not effective_slug:
        effective_slug = "tutorial"
    name = f"tutorial-{effective_slug}"
    if part:
        name += f"-part-{part}"
    return f"{name}.md"


def create_instance(
    workspace: Path,
    date_value: str,
    topic: str,
    audience: str,
    outcome: str,
    depth: str,
    slug: str | None = None,
    part: str | None = None,
) -> Path:
    template = Path(__file__).resolve().parents[1] / "assets" / "findings-template.md"
    if not template.is_file():
        raise FileNotFoundError(f"findings template not found: {template}")

    output_filename = build_output_filename(slug, topic, part)
    instance = allocate_instance(workspace / ".data", date_value)
    created = dt.datetime.now(tz=dt.timezone.utc).isoformat()
    try:
        write_text(
            instance / "00-control.md",
            control_text(created, topic, audience, outcome, depth, output_filename),
        )
        write_text(instance / "01-evidence.md", EVIDENCE)
        write_text(instance / "02-outline.md", OUTLINE)
        shutil.copyfile(template, instance / output_filename)
    except Exception:
        shutil.rmtree(instance, ignore_errors=True)
        raise
    return instance


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the next .data/tut-YY-MM-DD-<suffix> tutorial instance."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        help="Workspace root. Defaults to the nearest Git root, otherwise the current directory.",
    )
    parser.add_argument(
        "--date",
        default=dt.date.today().strftime("%y-%m-%d"),
        help="Instance date in YY-MM-DD format (default: today).",
    )
    parser.add_argument("--topic", default="Tutorial topic")
    parser.add_argument("--audience", default="Technically informed readers.")
    parser.add_argument("--outcome", default="Complete the described task independently.")
    parser.add_argument("--depth", choices=("brief", "standard", "comprehensive"), default="standard")
    parser.add_argument(
        "--slug",
        default=None,
        help="Filename slug for the output file. Derived from --topic when omitted.",
    )
    parser.add_argument(
        "--part",
        default=None,
        help="Part suffix for multi-part tutorials (e.g., a, b). Appended as -part-<value>.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if not re.fullmatch(r"\d{2}-\d{2}-\d{2}", args.date):
            raise ValueError("date must use the exact YY-MM-DD format")
        dt.datetime.strptime(args.date, "%y-%m-%d")
        workspace = (
            args.workspace.expanduser().resolve()
            if args.workspace
            else find_workspace(Path.cwd())
        )
        if not workspace.is_dir():
            raise NotADirectoryError(f"workspace is not a directory: {workspace}")
        instance = create_instance(
            workspace=workspace,
            date_value=args.date,
            topic=single_line(args.topic),
            audience=single_line(args.audience),
            outcome=single_line(args.outcome),
            depth=args.depth,
            slug=args.slug,
            part=args.part,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(instance)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
