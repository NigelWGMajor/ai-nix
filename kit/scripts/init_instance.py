#!/usr/bin/env python3
"""Create a collision-safe KIT review instance from read-only local evidence."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run_git(repo: Path, *args: str, check: bool = True) -> tuple[int, str, str]:
    command = ["git", "-C", str(repo), *args]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    if check and result.returncode != 0:
        detail = stderr or stdout or f"exit code {result.returncode}"
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result.returncode, stdout, stderr


def resolve_repo(start: Path) -> Path:
    start = start.expanduser().resolve()
    code, stdout, stderr = run_git(start, "rev-parse", "--show-toplevel", check=False)
    if code != 0 or not stdout:
        raise RuntimeError(f"not a Git repository: {start} ({stderr or 'no root found'})")
    return Path(stdout).resolve()


def alphabetic_suffix(index: int) -> str:
    if index < 0:
        raise ValueError("suffix index must be non-negative")
    value = index + 1
    result = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(ord("a") + remainder) + result
    return result


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def ensure_ignored_output(repo: Path, output_root: Path) -> None:
    if not is_within(output_root, repo):
        return
    relative = output_root.relative_to(repo).as_posix()
    probe = f"{relative.rstrip('/')}/kit-ignore-probe" if relative != "." else "kit-ignore-probe"
    code, _, _ = run_git(
        repo,
        "check-ignore",
        "--quiet",
        "--no-index",
        "--",
        probe,
        check=False,
    )
    if code != 0:
        raise RuntimeError(
            f"refusing unignored in-repository output path: {output_root}; "
            "choose an ignored path or pass --output-root outside the repository"
        )


def git_facts(repo: Path, base: str | None) -> dict[str, str]:
    _, head, _ = run_git(repo, "rev-parse", "HEAD")
    branch_code, branch, _ = run_git(
        repo, "symbolic-ref", "--quiet", "--short", "HEAD", check=False
    )
    if branch_code != 0 or not branch:
        branch = "(detached HEAD)"

    upstream_code, upstream, _ = run_git(
        repo,
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{upstream}",
        check=False,
    )
    if upstream_code != 0 or not upstream:
        upstream = "(none or unresolved)"

    _, status, _ = run_git(repo, "status", "--short", "--branch", "--untracked-files=all")
    _, porcelain, _ = run_git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    _, unstaged_stat, _ = run_git(repo, "diff", "--stat")
    _, staged_stat, _ = run_git(repo, "diff", "--cached", "--stat")
    _, recent, _ = run_git(
        repo,
        "log",
        "-n",
        "12",
        "--date=iso-strict",
        "--pretty=format:%h%x09%ad%x09%s",
    )

    base_commit = "(unresolved)"
    merge_base = "(unresolved)"
    base_diff_stat = "(not available)"
    if base:
        base_code, resolved, _ = run_git(
            repo, "rev-parse", "--verify", f"{base}^{{commit}}", check=False
        )
        if base_code == 0 and resolved:
            base_commit = resolved
            merge_code, merged, _ = run_git(
                repo, "merge-base", "HEAD", resolved, check=False
            )
            if merge_code == 0 and merged:
                merge_base = merged
                _, base_diff_stat, _ = run_git(repo, "diff", "--stat", f"{merged}...HEAD")

    return {
        "repository": str(repo),
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "dirty": "yes" if porcelain else "no",
        "status": status or "(clean)",
        "unstaged_stat": unstaged_stat or "(none)",
        "staged_stat": staged_stat or "(none)",
        "recent": recent or "(no commits)",
        "base_ref": base or "(unresolved)",
        "base_commit": base_commit,
        "merge_base": merge_base,
        "base_diff_stat": base_diff_stat or "(none)",
    }


def resolve_feature(
    repo: Path, branch: str, explicit: Path | None
) -> tuple[Path | None, list[Path]]:
    specs_root = repo / "specs"
    candidates = (
        sorted((item for item in specs_root.iterdir() if item.is_dir()), key=lambda p: p.name)
        if specs_root.is_dir()
        else []
    )

    if explicit:
        feature = explicit.expanduser()
        if not feature.is_absolute():
            feature = repo / feature
        feature = feature.resolve()
        if not feature.is_dir():
            raise NotADirectoryError(f"feature directory does not exist: {feature}")
        if not is_within(feature, repo):
            raise ValueError(f"feature directory must be inside the repository: {feature}")
        return feature, candidates

    if branch != "(detached HEAD)":
        branch_leaf = branch.replace("\\", "/").rsplit("/", 1)[-1]
        matches = [item for item in candidates if item.name == branch_leaf]
        if len(matches) == 1:
            return matches[0].resolve(), candidates
    return None, candidates


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def role_for(repo: Path, path: Path) -> str:
    relative = path.relative_to(repo).as_posix()
    name = path.name.lower()
    parts = {part.lower() for part in path.parts}
    if relative == ".specify/memory/constitution.md":
        return "Constitution"
    if name == "spec.md":
        return "Feature specification"
    if name == "plan.md":
        return "Implementation plan"
    if name == "tasks.md":
        return "Task roadmap"
    if name == "research.md":
        return "Research and decisions"
    if name == "data-model.md":
        return "Data model"
    if name == "quickstart.md":
        return "Validation quickstart"
    if name == "roadmap.md":
        return "Feature roadmap"
    if relative == "ROADMAP.md":
        return "Repository roadmap"
    if "contracts" in parts:
        return "Contract"
    if "checklists" in parts:
        return "Requirements checklist"
    if relative.startswith(".specify/"):
        return "Spec Kit configuration"
    return "Custom feature artifact"


def artifact_paths(repo: Path, feature: Path | None) -> list[Path]:
    paths: set[Path] = set()
    project_artifacts = [
        repo / ".specify" / "memory" / "constitution.md",
        repo / ".specify" / "extensions.yml",
        repo / ".specify" / "preset.yml",
        repo / ".specify" / "presets.yml",
        repo / ".specify" / "preset-catalogs.yml",
        repo / "ROADMAP.md",
    ]
    paths.update(path.resolve() for path in project_artifacts if path.is_file())
    if feature:
        paths.update(path.resolve() for path in feature.rglob("*") if path.is_file())
    return sorted(paths, key=lambda path: path.relative_to(repo).as_posix())


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def inventory_text(
    repo: Path, feature: Path | None, candidates: list[Path]
) -> str:
    selected = feature.relative_to(repo).as_posix() if feature else "Unresolved"
    candidate_text = ", ".join(path.relative_to(repo).as_posix() for path in candidates) or "None found"
    lines = [
        "# Spec Kit inventory",
        "",
        "## Feature resolution",
        "",
        f"- Selected feature: `{selected}`",
        f"- Candidate directories: {candidate_text}",
        "- Selection rule: explicit path or exact current-branch-leaf match only.",
        "",
        "## Artifact fingerprints",
        "",
        "| Path | Role | Bytes | Modified UTC | SHA-256 |",
        "| --- | --- | ---: | --- | --- |",
    ]
    artifacts = artifact_paths(repo, feature)
    if not artifacts:
        lines.append("| (none inventoried) | Unknown | 0 | Unknown | Unknown |")
    for path in artifacts:
        stat = path.stat()
        modified = dt.datetime.fromtimestamp(stat.st_mtime, tz=dt.timezone.utc).isoformat()
        relative = path.relative_to(repo).as_posix()
        lines.append(
            f"| `{md_cell(relative)}` | {md_cell(role_for(repo, path))} | "
            f"{stat.st_size} | {modified} | `{sha256(path)}` |"
        )
    lines.extend(
        [
            "",
            "## Missing, optional, or custom artifacts",
            "",
            "Classify absence only after inspecting the installed Spec Kit version, presets, extensions, and feature applicability.",
        ]
    )
    return "\n".join(lines)


def control_text(
    created: str,
    mode: str,
    purpose: str,
    facts: dict[str, str],
    feature: Path | None,
    repo: Path,
    previous: Path | None,
) -> str:
    feature_text = feature.relative_to(repo).as_posix() if feature else "Unresolved"
    previous_text = str(previous) if previous else "Not applicable"
    return f"""
# KIT control

## Identity

- Status: initialized
- Mode: {mode}
- Created: {created}
- Purpose: {purpose}
- Repository: `{repo}`
- Branch: `{facts['branch']}`
- HEAD: `{facts['head']}`
- Base ref: `{facts['base_ref']}`
- Merge base: `{facts['merge_base']}`
- Feature directory: `{feature_text}`
- Previous KIT instance: `{previous_text}`
- Final document: `Findings.md`

## Scope and boundaries

- Review boundary: Selected Spec Kit feature and material integration surfaces.
- Mutation boundary: Read-only except this KIT instance and approved validation artifacts.
- Remote freshness: No fetch was performed by the initializer.

## Current phase

Repository and Spec Kit artifact orientation.

## Completed audit layers

- Captured local Git snapshot.
- Fingerprinted discovered Spec Kit artifacts.

## Assumptions and open questions

- Confirm the intended base if unresolved.
- Confirm the feature directory if unresolved.
- Record any external issue or pull-request context separately.

## Next safe action

Read applicable repository guidance, then reconcile constitution, spec, plan, tasks, implementation, and validation evidence.
"""


def repository_snapshot_text(created: str, facts: dict[str, str]) -> str:
    return f"""
# Repository snapshot

Captured: {created}

## Identity

| Fact | Value |
| --- | --- |
| Repository | `{facts['repository']}` |
| Branch | `{facts['branch']}` |
| HEAD | `{facts['head']}` |
| Upstream | `{facts['upstream']}` |
| Dirty | {facts['dirty']} |
| Intended base ref | `{facts['base_ref']}` |
| Resolved base commit | `{facts['base_commit']}` |
| Merge base | `{facts['merge_base']}` |
| Remote refresh | Not performed |

## Status

```text
{facts['status']}
```

## Unstaged diff stat

```text
{facts['unstaged_stat']}
```

## Staged diff stat

```text
{facts['staged_stat']}
```

## Base-to-HEAD diff stat

```text
{facts['base_diff_stat']}
```

## Recent commits

```text
{facts['recent']}
```
"""


TRACEABILITY = """
# Traceability

Use separate compact tables by story or phase when the feature is large.

| Requirement/story | Intended outcome | Design evidence | Task evidence | Implementation evidence | Validation evidence | Status | Evidence class and confidence | Remaining work |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| To be mapped | | | | | | Unknown | Unknown | |

## Orphan or contradictory evidence

Record tasks without requirements, implementation without tasks, stale paths, and conflicting artifacts here.
"""


VALIDATION = """
# Validation ledger

Record the pre-validation and post-validation worktree state. Do not infer success from an existing command or log.

| Timestamp | Result | Command or check | Purpose | HEAD/worktree context | Environment | Important output or limitation |
| --- | --- | --- | --- | --- | --- | --- |
| Not run | Not run | None yet | Validation scope not yet selected | Captured in `01-repository-snapshot.md` | Unknown | |
"""


def allocate_instance(output_root: Path, date_value: str) -> Path:
    output_root.mkdir(parents=True, exist_ok=True)
    for index in range(26 * 27):
        candidate = output_root / f"kit-{date_value}-{alphabetic_suffix(index)}"
        try:
            candidate.mkdir()
            return candidate
        except FileExistsError:
            continue
    raise RuntimeError("could not allocate an available KIT instance suffix")


def create_instance(
    repo: Path,
    output_root: Path,
    date_value: str,
    mode: str,
    purpose: str,
    facts: dict[str, str],
    feature: Path | None,
    candidates: list[Path],
    previous: Path | None,
) -> Path:
    template = Path(__file__).resolve().parents[1] / "assets" / "findings-template.md"
    if not template.is_file():
        raise FileNotFoundError(f"status template not found: {template}")

    instance = allocate_instance(output_root, date_value)
    created = dt.datetime.now(tz=dt.timezone.utc).isoformat()
    try:
        (instance / "00-control.md").write_text(
            control_text(created, mode, purpose, facts, feature, repo, previous).strip() + "\n",
            encoding="utf-8",
        )
        (instance / "01-repository-snapshot.md").write_text(
            repository_snapshot_text(created, facts).strip() + "\n", encoding="utf-8"
        )
        (instance / "02-evidence.md").write_text(
            inventory_text(repo, feature, candidates).strip() + "\n", encoding="utf-8"
        )
        (instance / "03-analysis.md").write_text(
            TRACEABILITY.strip() + "\n", encoding="utf-8"
        )
        (instance / "04-validation.md").write_text(
            VALIDATION.strip() + "\n", encoding="utf-8"
        )
        shutil.copyfile(template, instance / "Findings.md")
    except Exception:
        shutil.rmtree(instance, ignore_errors=True)
        raise
    return instance


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a read-only local snapshot and KIT recovery-review instance."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Path inside the Git repository.")
    parser.add_argument(
        "--workspace",
        type=Path,
        help="Workspace root for .data output. Defaults to the resolved repository root.",
    )
    parser.add_argument("--mode", choices=("review", "snapshot", "resume"), default="review")
    parser.add_argument("--feature-dir", type=Path, help="Explicit feature directory, absolute or repository-relative.")
    parser.add_argument("--base", help="Intended local base ref. No fetch is performed.")
    parser.add_argument("--previous", type=Path, help="Previous KIT instance; required in resume mode.")
    parser.add_argument(
        "--output-root",
        type=Path,
        help="Explicit output parent. Defaults to <workspace>/.data.",
    )
    parser.add_argument("--purpose", default="Reconstruct and sanity-check project status.")
    parser.add_argument("--date", default=dt.date.today().strftime("%y-%m-%d"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if not re.fullmatch(r"\d{2}-\d{2}-\d{2}", args.date):
            raise ValueError("date must use the exact YY-MM-DD format")
        dt.datetime.strptime(args.date, "%y-%m-%d")
        if args.mode == "resume" and not args.previous:
            raise ValueError("--previous is required in resume mode")
        if args.mode != "resume" and args.previous:
            raise ValueError("--previous is only valid in resume mode")

        repo = resolve_repo(args.repo)
        facts = git_facts(repo, args.base)
        feature, candidates = resolve_feature(repo, facts["branch"], args.feature_dir)

        previous = None
        if args.previous:
            previous = args.previous.expanduser().resolve()
            required = [previous / "00-control.md", previous / "Findings.md"]
            if not previous.is_dir() or not all(path.is_file() for path in required):
                raise ValueError(f"previous KIT instance is incomplete or missing: {previous}")

        workspace = args.workspace.expanduser().resolve() if args.workspace else repo
        if not workspace.is_dir():
            raise NotADirectoryError(f"workspace is not a directory: {workspace}")
        output_root = (
            args.output_root.expanduser().resolve()
            if args.output_root
            else (workspace / ".data").resolve()
        )
        ensure_ignored_output(repo, output_root)
        instance = create_instance(
            repo=repo,
            output_root=output_root,
            date_value=args.date,
            mode=args.mode,
            purpose=args.purpose,
            facts=facts,
            feature=feature,
            candidates=candidates,
            previous=previous,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(instance)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
