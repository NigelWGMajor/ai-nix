#!/usr/bin/env python3
"""Create a collision-safe, durable FIX triage instance."""

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
        pass

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
    symptom: str,
    depth: str,
) -> str:
    return f"""
# FIX control

## Identity

- Status: initialized
- Created: {created}
- Symptom: {symptom}
- Depth: {depth.title()}
- Final document: `Findings.md`

## Scope and evidence boundary

- Included: To be resolved from the symptom and workspace.
- Excluded: To be determined.
- External research: Not included unless required by the symptom.
- Mutation boundary: Read-only except this FIX instance.

## Hypotheses

To be formed after capturing the symptom precisely.

## Current stage

Capture - document the symptom precisely before forming hypotheses.

## Completed work

- Created the triage instance and standard artifacts.

## Next safe action

Capture the symptom: what is the observable failure, when does it occur, where does it manifest?
"""


EVIDENCE = """
# FIX evidence map

## Symptom

Document the observable failure before investigation.

## Evidence

| ID | Source or observation | Role | Supports/contradicts | Assessment |
| --- | --- | --- | --- | --- |
| E-01 | To be gathered | Unknown | | Unknown |

## Hypothesis evaluation

| Hypothesis | Evidence For | Evidence Against | Status |
| --- | --- | --- | --- |
| H-01 | | | Active |
"""


TRIAGE = """
# FIX triage trace

## Hypothesis register

| ID | Hypothesis | Status | Confidence |
| --- | --- | --- | --- |

## Narrowing analysis

## Root cause

## Causal chain

## Contributing factors
"""


def allocate_instance(data_dir: Path, date_value: str) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    for index in range(26 * 27):
        candidate = data_dir / f"fix-{date_value}-{alphabetic_suffix(index)}"
        try:
            candidate.mkdir()
            return candidate
        except FileExistsError:
            continue
    raise RuntimeError("could not allocate an available FIX instance suffix")


def create_instance(
    workspace: Path,
    date_value: str,
    symptom: str,
    depth: str,
) -> Path:
    template = Path(__file__).resolve().parents[1] / "assets" / "findings-template.md"
    if not template.is_file():
        raise FileNotFoundError(f"findings template not found: {template}")

    instance = allocate_instance(resolve_output_base(workspace) / ".data", date_value)
    created = dt.datetime.now(tz=dt.timezone.utc).isoformat()
    try:
        write_text(
            instance / "00-control.md",
            control_text(created, symptom, depth),
        )
        write_text(instance / "01-evidence.md", EVIDENCE)
        write_text(instance / "02-triage.md", TRIAGE)
        shutil.copyfile(template, instance / "Findings.md")
    except Exception:
        shutil.rmtree(instance, ignore_errors=True)
        raise
    return instance


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the next .data/fix-YY-MM-DD-<suffix> triage instance."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        help="Workspace root. Defaults to the nearest Git root, otherwise the fallback path.",
    )
    parser.add_argument(
        "--date",
        default=dt.date.today().strftime("%y-%m-%d"),
        help="Instance date in YY-MM-DD format (default: today).",
    )
    parser.add_argument("--symptom", default="Symptom to be diagnosed")
    parser.add_argument("--depth", choices=("quick", "standard", "deep"), default="standard")
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
            symptom=single_line(args.symptom),
            depth=args.depth,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(instance)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
