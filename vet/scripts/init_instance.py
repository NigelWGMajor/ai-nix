#!/usr/bin/env python3
"""Create a collision-safe, resumable VET review instance."""

from __future__ import annotations

import argparse
import os
import re
import shutil
from datetime import date
from pathlib import Path


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return result[:48] or "review"


def output_base(workspace: Path) -> Path:
    configured = os.environ.get("TOOLING_OUTPUT_PATH", "").strip()
    if not configured:
        return workspace / ".data"
    candidate = Path(configured)
    if candidate.is_absolute():
        return candidate
    if configured.startswith("./") or configured.startswith(".\\"):
        return (workspace / configured[2:]).resolve()
    raise ValueError("TOOLING_OUTPUT_PATH must be absolute or start with './' or '.\\\\'")


def suffix(index: int) -> str:
    chars: list[str] = []
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        chars.append(chr(ord("a") + remainder))
    return "".join(reversed(chars))


def next_instance(base: Path, context: str | None) -> Path:
    stem = f"vet-{date.today():%y-%m-%d}"
    context_suffix = f"-{slug(context)}" if context else ""
    for index in range(26 * 27):
        candidate = base / f"{stem}-{suffix(index)}{context_suffix}"
        if not candidate.exists():
            return candidate
    raise RuntimeError("could not allocate a VET instance name")


CONTROL = """# VET review control

## Identity

- Repository root: {workspace}
- Branch: {branch}
- HEAD: {head}
- Comparison base: {base}
- Depth: {depth}
- Created: {today}
- Final document: `Findings.md`

## Remote snapshot

| Source | Stable ID | Updated/fingerprint | Observed at | Status |
| --- | --- | --- | --- | --- |
| Pull request | [resolve] | [resolve] | [resolve] | [unknown/current] |
| Ticket | [resolve] | [resolve] | [resolve] | [unknown/current] |
| Comment | [resolve] | [resolve] | [resolve] | [active/resolved/changed] |

## Scope and evidence boundary

- Intended outcome: [record after target resolution]
- Included change states: [committed/staged/unstaged/untracked]
- Repository boundary: [primary and relevant ROOT_FE/ROOT_BE]
- Material limitations: [record]

## Progress

| Area | Status | Evidence/result |
| --- | --- | --- |
| Branch and comparison basis | ⚪ Not started | |
| PR and ticket snapshot | ⚪ Not started | |
| Requirements | ⚪ Not started | |
| Code and contract review | ⚪ Not started | |
| Active comment dispositions | ⚪ Not started | |
| Action queue | ⚪ Not started | |

## Assumptions and questions

- [Only assumptions that could materially change a disposition or action.]

## Action state

- No local or remote action has been authorized or performed.

## Next safe action

Resolve the exact branch, comparison basis, and remote PR/ticket snapshot; then update `01-evidence.md`.
"""

EVIDENCE = """# VET evidence map

## Boundary and freshness

| Repository/source | Role | Direct or derived | Freshness | Limitation |
| --- | --- | --- | --- | --- |
| [primary checkout] | WIP source of truth | Direct | [HEAD/time] | |
| [ROOT_FE/ROOT_BE] | Complementary source | Direct/Not inspected | [HEAD/time] | |
| [codebase graph] | Relationship mapping | Derived | [index status] | May omit WIP |
| [PR/Jira] | Intent and review context | Claimed/remote observed | [time] | Does not prove code |

## Material evidence

| ID | Source | What it establishes | Class | Notes |
| --- | --- | --- | --- | --- |
| E-001 | [path:line or remote link] | | Observed/Claimed/Inferred/Unknown | |

## Gaps and limitations

- [Gap, consequence, and smallest next check.]
"""

REVIEW = """# VET working review

## Requirement register

| Requirement | Coverage | Evidence | Finding/action |
| --- | --- | --- | --- |
| REQ-01 | Not verifiable | | |

## Active comment register

| ID | Source/stable ID | Summary | Assessment | Disposition | Response | Action | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-001 | | | | not verifiable | R-001 | | |

## Findings and strengths

| ID | Type | Seriousness | Confidence | Evidence | Recommendation |
| --- | --- | --- | --- | --- | --- |
| F-001 | [finding/strength] | | | | |

## Validation

| Status | Check | Purpose | Evidence/limitation |
| --- | --- | --- | --- |
| Not run | | | |
"""

ACTIONS = """# VET action queue

> Actions are recommendations only until the user explicitly authorizes the selected IDs.

| ID | Status | Type | Scope | Depends on | Validation | Stop when | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A-001 | ⚪ Not started | corrective/restorative/response | | | | | |

## Response drafts

| ID | Comment | Draft | Publication state | Freshness check |
| --- | --- | --- | --- | --- |
| R-001 | C-001 | | Draft only | Required before publication |

## Idempotency record

- Reuse the action or response ID when its source, scope, and intent are unchanged.
- Record posted remote IDs and content fingerprints here; do not publish a matching response twice.
"""


def write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--depth", choices=("quick", "standard", "deep"), required=True)
    parser.add_argument("--context-suffix")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    if not workspace.is_dir():
        raise ValueError(f"workspace does not exist: {workspace}")

    base = output_base(workspace)
    base.mkdir(parents=True, exist_ok=True)
    instance = next_instance(base, args.context_suffix)
    instance.mkdir()

    values = {
        "workspace": workspace,
        "branch": args.branch,
        "head": args.head,
        "base": args.base,
        "depth": args.depth,
        "today": date.today().isoformat(),
    }
    template = Path(__file__).resolve().parents[1] / "assets" / "findings-template.md"
    if not template.is_file():
        raise FileNotFoundError(f"findings template not found: {template}")

    write(instance / "00-control.md", CONTROL.format(**values))
    write(instance / "01-evidence.md", EVIDENCE)
    write(instance / "02-review.md", REVIEW)
    write(instance / "03-action-queue.md", ACTIONS)
    shutil.copyfile(template, instance / "Findings.md")
    print(instance)


if __name__ == "__main__":
    main()
