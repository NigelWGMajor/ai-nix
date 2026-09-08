#!/usr/bin/env python3
"""Create a collision-safe, resumable LIT analysis instance."""

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
    result = ""
    value = index + 1
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(ord("a") + remainder) + result
    return result


def write_text(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def control_text(purpose: str, audience: str) -> str:
    return f"""
# LIT control

## Identity

- Status: initialized
- Purpose: {purpose}
- Audience: {audience}
- Final document: `Findings.md`

## Corpus boundary

- Included: To be inventoried.
- Excluded: To be determined.
- Research authorization: Source corpus only unless explicitly expanded by the user.

## Current phase

Source orientation and inventory.

## Completed work

- Created the analysis instance and standard artifacts.

## Assumptions

- Default output is professional Markdown in US English.
- Default depth is orientation plus detailed reference.

## Open questions

- Confirm the target decision or activity if it is not explicit in the request.
- Confirm any material corpus ambiguity.

## Next safe action

Inventory the supplied sources in `01-evidence.md` without modifying them.
"""


EVIDENCE = """
# Source inventory

## Corpus boundary

- Included:
- Excluded:
- Unavailable or missing:

## Sources

| ID | Source and location | Role | Version or date | Scope and authority | Availability | Currency | Relevance | Completeness | Decision value | Interpretation confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S001 | To be inventoried | To be classified | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | |

## Relationships

Record normative, supplementary, superseding, derivative, or hierarchical source relationships here.
"""


ANALYSIS = """
# Analysis

## Essential concepts and claims

## Terminology and aliases

## Relationships, flows, and boundaries

## Agreements and conflicts

## Interpretations, synthesis, and inferences

## Implications and recommendations

## Assumptions, gaps, and unknowns
"""


STRUCTURE = """
# Proposed structure

## Reader journey

## Comprehension dependencies

## Section plan

## Planned diagrams and visual aids

List only visuals that materially improve comprehension and note the relationship each one explains.
"""


def create_instance(
    workspace: Path,
    date_value: str,
    purpose: str,
    audience: str,
) -> Path:
    template = Path(__file__).resolve().parents[1] / "assets" / "findings-template.md"
    if not template.is_file():
        raise FileNotFoundError(f"findings template not found: {template}")

    data_dir = resolve_output_base(workspace) / ".data"
    data_dir.mkdir(parents=True, exist_ok=True)

    instance_dir = None
    for index in range(26 * 27):
        candidate = data_dir / f"lit-{date_value}-{alphabetic_suffix(index)}"
        try:
            candidate.mkdir()
        except FileExistsError:
            continue
        instance_dir = candidate
        break

    if instance_dir is None:
        raise RuntimeError("could not allocate an available LIT instance suffix")

    write_text(instance_dir / "00-control.md", control_text(purpose, audience))
    write_text(instance_dir / "01-evidence.md", EVIDENCE)
    write_text(instance_dir / "02-analysis.md", ANALYSIS)
    write_text(instance_dir / "03-structure.md", STRUCTURE)

    shutil.copyfile(template, instance_dir / "Findings.md")
    return instance_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the next .data/lit-YY-MM-DD-<suffix> analysis instance."
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
    parser.add_argument("--purpose", default="To be confirmed.")
    parser.add_argument("--audience", default="Technically informed decision-makers.")
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
            purpose=args.purpose,
            audience=args.audience,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(instance)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
