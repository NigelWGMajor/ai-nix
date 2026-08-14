#!/usr/bin/env python3
"""Create a collision-safe, durable PIX slideshow instance."""

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


def single_line(value: str) -> str:
    return " ".join(value.splitlines()).strip()


def write_text(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def control_text(
    created: str,
    source: str,
    title: str,
    audience: str,
    depth: str,
) -> str:
    return f"""
# PIX control

## Identity

- Status: initialized
- Created: {created}
- Source document: {source}
- Slideshow title: {title}
- Audience: {audience}
- Depth: {depth.title()}
- Final document: `Findings.md`

## Scope

- Included: To be resolved from the source document.
- Excluded: To be determined during Survey.
- Mutation boundary: Read-only except this PIX instance. Source document is never modified.

## Current stage

Survey — read and map the source document.

## Completed work

- Created the slideshow instance and standard artifacts.

## Assumptions

- Output format is Marp-compatible Markdown.
- Mermaid diagrams use dark theme initialization.
- Slides target a screen or projector presentation context.

## Open questions

- Confirm the target audience if it differs from the source document's audience.
- Confirm any material scope constraints.

## Next safe action

Read the source document and build the source map in `01-source-map.md`.
"""


SOURCE_MAP = """
# Source map

## Source document

- Path:
- Purpose:
- Audience:
- Central message:
- Structure: [section count, heading depth, approximate length]

## Section inventory

| # | Heading | Level | Approx size | Content classification | Key visuals | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | To be mapped | | | | | |

## Existing visuals inventory

| # | Type | Location (heading or line) | Node/row count | Slide fit | Reuse plan |
| --- | --- | --- | --- | --- | --- |
| V001 | To be inventoried | | | | |

## Content classification

- **Essential** (must appear on slides):
- **Supporting** (include if space permits):
- **Reference-only** (omit or compress):

## Terminology and concepts requiring definition

| Term | Source definition | Slide treatment |
| --- | --- | --- |
| To be identified | | |

## Narrative entry points

- Natural opening hook:
- Key climactic moment:
- Natural closing action:
"""


STORYBOARD = """
# Storyboard

## Narrative arc

- **Hook:**
- **Context:**
- **Rising complexity:**
- **Climax (key insight):**
- **Denouement (implications):**
- **Action:**

## Planned slide sequence

| # | Type | Heading | Content summary | Source section | Visual plan |
| --- | --- | --- | --- | --- | --- |
| 1 | Title | To be determined | | | |
| 2 | Content | Why this matters | | | |
| 3 | Diagram | Mental model | | | |

## Visual generation plan

| # | Type | Purpose | Source basis | New or reused |
| --- | --- | --- | --- | --- |
| D001 | To be planned | | | |

## Slide count estimate

- Depth: [Short | Standard | Extended]
- Target range: [N-M slides]
- Current plan: [N slides]

## Pacing notes

- Section breaks planned at:
- Transition notes:
"""


def allocate_instance(data_dir: Path, date_value: str) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    for index in range(26 * 27):
        candidate = data_dir / f"pix-{date_value}-{alphabetic_suffix(index)}"
        try:
            candidate.mkdir()
            return candidate
        except FileExistsError:
            continue
    raise RuntimeError("could not allocate an available PIX instance suffix")


def create_instance(
    workspace: Path,
    date_value: str,
    source: str,
    title: str,
    audience: str,
    depth: str,
) -> Path:
    template = Path(__file__).resolve().parents[1] / "assets" / "findings-template.md"
    if not template.is_file():
        raise FileNotFoundError(f"findings template not found: {template}")

    instance = allocate_instance(workspace / ".data", date_value)
    created = dt.datetime.now(tz=dt.timezone.utc).isoformat()
    try:
        write_text(
            instance / "00-control.md",
            control_text(created, source, title, audience, depth),
        )
        write_text(instance / "01-source-map.md", SOURCE_MAP)
        write_text(instance / "02-storyboard.md", STORYBOARD)
        shutil.copyfile(template, instance / "Findings.md")
    except Exception:
        shutil.rmtree(instance, ignore_errors=True)
        raise
    return instance


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the next .data/pix-YY-MM-DD-<suffix> slideshow instance."
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
    parser.add_argument("--source", default="To be specified.")
    parser.add_argument("--title", default="Untitled Presentation")
    parser.add_argument("--audience", default="Technical audience.")
    parser.add_argument("--depth", choices=("short", "standard", "extended"), default="standard")
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
            source=single_line(args.source),
            title=single_line(args.title),
            audience=single_line(args.audience),
            depth=args.depth,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(instance)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
