#!/usr/bin/env python3
"""Create a collision-safe, durable NIX analysis instance."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import sys
from pathlib import Path


def get_fallback_path() -> Path:
    """Return OS-specific fallback path when no git repository is found."""
    if sys.platform == 'win32':
        return Path('C:/.data')
    elif sys.platform == 'darwin':
        return Path.home() / 'Library' / 'Application Support' / 'claude-skills'
    else:
        return Path.home() / '.local' / 'share' / 'claude-skills'


def call_mcp_tool(tool_name: str) -> dict | None:
    """Try to call MCP tool for workspace root resolution."""
    return None  # Placeholder for MCP integration


def find_workspace(start: Path) -> Path:
    """Return the nearest ancestor that looks like a workspace."""
    # 1. Try MCP tool if available
    try:
        mcp_result = call_mcp_tool('vscode-workspace.get_workspace_root')
        if mcp_result and mcp_result.get('workspaceRoot'):
            return Path(mcp_result['workspaceRoot'])
    except Exception:
        pass  # MCP not available, continue to git detection

    # 2. Try git from current location
    start = start.expanduser().resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate

    # 3. Fallback to OS-specific data directory
    return get_fallback_path()


def resolve_output_base(workspace: Path) -> Path:
    """Resolve TOOLING_OUTPUT_PATH, defaulting to the legacy .data directory."""
    configured = os.environ.get("TOOLING_OUTPUT_PATH", ".data").strip() or ".data"
    if configured == ".data":
        return (workspace / ".data").resolve()
    candidate = Path(configured).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    if configured.startswith(("./", ".\\")):
        return (workspace / candidate).resolve()
    raise ValueError("TOOLING_OUTPUT_PATH must be absolute or start with './' or '.\\'")


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
    subject: str,
    question: str,
    audience: str,
    depth: str,
) -> str:
    return f"""
# NIX control

## Identity

- Status: initialized
- Created: {created}
- Subject: {subject}
- Question: {question}
- Audience/use: {audience}
- Depth: {depth.title()}
- Final document: `Findings.md`

## Scope and evidence boundary

- Included: To be resolved from the request and workspace.
- Excluded: To be determined.
- External research: Not included unless requested or required by the subject.
- Mutation boundary: Read-only except this NIX instance.

## Current stage

Reflect and resolve the subject.

## Completed work

- Created the analysis instance and standard artifacts.

## Assumptions and open questions

- Record only assumptions that could materially affect the model or conclusion.
- Resolve any ambiguity that would change the subject or workspace boundary.

## Next safe action

Frame the core question and inventory the material evidence in `01-evidence.md`.
"""


EVIDENCE = """
# NIX evidence map

## Boundary and freshness

- Workspace or subject boundary:
- External evidence boundary:
- Freshness limitations:

## Material sources and entry points

| ID | Source or entry point | Role | What it establishes | Evidence class or limitation |
| --- | --- | --- | --- | --- |
| E001 | To be inspected | Unknown | | Unknown |

## Conflicts, gaps, and diminishing-return boundary

- Conflicts:
- Missing evidence:
- Exploration stopping condition:
"""


ANALYSIS = """
# NIX working analysis

## Reflect

## Explore

## Connect

## Imagine

## Produce

## Empower

## Material findings, assumptions, conflicts, and unknowns
"""


def allocate_instance(data_dir: Path, date_value: str) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    for index in range(26 * 27):
        candidate = data_dir / f"nix-{date_value}-{alphabetic_suffix(index)}"
        try:
            candidate.mkdir()
            return candidate
        except FileExistsError:
            continue
    raise RuntimeError("could not allocate an available NIX instance suffix")


def create_instance(
    workspace: Path,
    date_value: str,
    subject: str,
    question: str,
    audience: str,
    depth: str,
) -> Path:
    template = Path(__file__).resolve().parents[1] / "assets" / "findings-template.md"
    if not template.is_file():
        raise FileNotFoundError(f"findings template not found: {template}")

    instance = allocate_instance(resolve_output_base(workspace), date_value)
    created = dt.datetime.now(tz=dt.timezone.utc).isoformat()
    try:
        write_text(
            instance / "00-control.md",
            control_text(created, subject, question, audience, depth),
        )
        write_text(instance / "01-evidence.md", EVIDENCE)
        write_text(instance / "02-analysis.md", ANALYSIS)
        shutil.copyfile(template, instance / "Findings.md")
    except Exception:
        shutil.rmtree(instance, ignore_errors=True)
        raise
    return instance


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the next <output-base>/nix-YY-MM-DD-<suffix> analysis instance."
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
    parser.add_argument("--subject", default="Current workspace")
    parser.add_argument("--question", default="Build a usable mental model of the subject.")
    parser.add_argument("--audience", default="Technically informed readers.")
    parser.add_argument("--depth", choices=("compact", "standard", "deep"), default="standard")
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
            subject=single_line(args.subject),
            question=single_line(args.question),
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
