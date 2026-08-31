#!/usr/bin/env python3
"""Manage local Markdown state for a DAC delivery workstream.

This helper intentionally operates only inside a selected .dac workspace. It
does not invoke Jira, Spec Kit, other skills, Git, tests, builds, deployment,
or network tools.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ALLOWED_STATUSES = {
    "not_started",
    "drafting",
    "proposed",
    "approved",
    "executing",
    "blocked",
    "pr_open",
    "integrated",
    "complete",
    "superseded",
}

SOLO_STATUSES = {
    "assessed",
    "adopted",
    "executing",
    "blocked",
    "pr_open",
    "integrated",
    "complete",
    "superseded",
}

SOLO_TRANSITIONS = {
    "assessed": {"adopted", "superseded"},
    "adopted": {"executing", "blocked", "superseded"},
    "executing": {"blocked", "pr_open", "complete", "superseded"},
    "blocked": {"executing", "superseded"},
    "pr_open": {"blocked", "integrated", "superseded"},
    "integrated": {"complete"},
    "complete": set(),
    "superseded": set(),
}

REQUIRED_FILES = [
    "00-control.md",
    "01-mission.md",
    "02-evidence.md",
    "03-decisions.md",
    "04-portion-plan.md",
    "05-jira-plan.md",
    "06-integration-plan.md",
]

TERMINAL_DEPENDENCY_STATUSES = {"integrated", "complete"}

PORTION_TRANSITIONS = {
    "proposed": {"superseded"},
    "approved": {"executing", "blocked", "superseded"},
    "executing": {"blocked", "pr_open", "complete", "superseded"},
    "blocked": {"approved", "superseded"},
    "pr_open": {"blocked", "integrated", "superseded"},
    "integrated": {"complete"},
    "complete": set(),
    "superseded": set(),
}

EXECUTOR_PATTERN = re.compile(
    r"(?:speckit|direct|discovery|human|skill:[a-z0-9][a-z0-9-]{0,62})"
)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def validate_identifier(value: str, label: str) -> str:
    normalized = value.strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", normalized):
        raise ValueError(
            f"{label} must begin with a letter and contain only letters, digits, "
            f"underscores, or hyphens; received {value!r}."
        )
    return normalized


def validate_executor(value: str) -> str:
    normalized = value.strip().lower()
    if not EXECUTOR_PATTERN.fullmatch(normalized):
        raise ValueError(
            "Executor must be speckit, direct, discovery, human, or skill:<name>."
        )
    return normalized


def frontmatter_bounds(text: str) -> Tuple[int, int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Markdown file does not begin with YAML frontmatter.")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("YAML frontmatter is not closed with '---'.") from exc
    return 0, end


def parse_frontmatter(text: str) -> Dict[str, str]:
    lines = text.splitlines()
    _, end = frontmatter_bounds(text)
    result: Dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def update_frontmatter(text: str, updates: Dict[str, str]) -> str:
    lines = text.splitlines()
    _, end = frontmatter_bounds(text)
    seen = set()
    for index in range(1, end):
        if ":" not in lines[index]:
            continue
        key = lines[index].split(":", 1)[0].strip()
        if key in updates:
            lines[index] = f"{key}: {updates[key]}"
            seen.add(key)
    missing = [key for key in updates if key not in seen]
    if missing:
        lines[end:end] = [f"{key}: {updates[key]}" for key in missing]
    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + suffix


def append_before_marker(text: str, marker: str, row: str) -> str:
    if marker not in text:
        raise ValueError(f"Required marker {marker!r} was not found.")
    return text.replace(marker, f"{row}\n{marker}", 1)


def ensure_workspace(path: Path) -> Path:
    workspace = path.expanduser().resolve()
    if not workspace.is_dir():
        raise ValueError(f"Workspace does not exist: {workspace}")
    if not (workspace / "00-control.md").is_file():
        raise ValueError(f"Not a DAC workspace; missing {workspace / '00-control.md'}")
    return workspace


def safe_member(workspace: Path, relative: str, must_exist: bool = True) -> Path:
    candidate = (workspace / relative).resolve()
    if candidate != workspace and workspace not in candidate.parents:
        raise ValueError("Artifact path escapes the workspace.")
    if must_exist and not candidate.is_file():
        raise ValueError(f"Artifact does not exist: {relative}")
    return candidate


def render_tree(source_root: Path, destination_root: Path, values: Dict[str, str]) -> None:
    for source in sorted(source_root.rglob("*")):
        relative = source.relative_to(source_root)
        destination = destination_root / relative
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        if source.name.endswith("-template.md"):
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        content = source.read_text(encoding="utf-8")
        for token, value in values.items():
            content = content.replace("{{" + token + "}}", value)
        destination.write_text(content, encoding="utf-8")


def update_control_timestamp(workspace: Path, timestamp: str) -> None:
    path = workspace / "00-control.md"
    text = update_frontmatter(path.read_text(encoding="utf-8"), {"last_updated": timestamp})
    path.write_text(text, encoding="utf-8")


def log_control(
    workspace: Path,
    timestamp: str,
    actor: str,
    artifact: str,
    action_class: str,
    scope: str,
    notes: str,
) -> None:
    path = workspace / "00-control.md"
    text = path.read_text(encoding="utf-8")
    row = "| {timestamp} | {actor} | {artifact} | {action_class} | {scope} | {notes} |".format(
        timestamp=escape_cell(timestamp),
        actor=escape_cell(actor),
        artifact=escape_cell(artifact),
        action_class=escape_cell(action_class),
        scope=escape_cell(scope),
        notes=escape_cell(notes or "-"),
    )
    text = update_frontmatter(text, {"last_updated": timestamp})
    text = append_before_marker(text, "<!-- GATE_LOG -->", row)
    path.write_text(text, encoding="utf-8")


def dependency_ids(value: str) -> List[str]:
    if not value or value.strip() in {"-", "none", "None"}:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def portion_records(workspace: Path) -> Dict[str, Tuple[Path, Dict[str, str]]]:
    records: Dict[str, Tuple[Path, Dict[str, str]]] = {}
    for path in sorted((workspace / "portions").glob("*.md")):
        if path.name.endswith("-template.md"):
            continue
        data = parse_frontmatter(path.read_text(encoding="utf-8"))
        portion_id = data.get("portion_id", "")
        if portion_id:
            records[portion_id] = (path, data)
    return records


def solo_records(workspace: Path) -> Dict[str, Tuple[Path, Dict[str, str]]]:
    """Return solo ticket records keyed by ticket_id."""
    records: Dict[str, Tuple[Path, Dict[str, str]]] = {}
    solo_dir = workspace / "solo"
    if not solo_dir.exists():
        return records
    for path in sorted(solo_dir.glob("*.md")):
        if path.name.endswith("-template.md"):
            continue
        data = parse_frontmatter(path.read_text(encoding="utf-8"))
        ticket_id = data.get("ticket_id", "")
        if ticket_id:
            records[ticket_id] = (path, data)
    return records


def readiness(
    portion_id: str, records: Dict[str, Tuple[Path, Dict[str, str]]]
) -> Tuple[bool, List[str]]:
    _, data = records[portion_id]
    reasons: List[str] = []
    if data.get("status") != "approved":
        reasons.append(f"status is {data.get('status', '?')}, not approved")
    for dependency in dependency_ids(data.get("depends_on", "")):
        if dependency not in records:
            reasons.append(f"dependency {dependency} is missing")
            continue
        dependency_status = records[dependency][1].get("status", "?")
        if dependency_status not in TERMINAL_DEPENDENCY_STATUSES:
            reasons.append(f"dependency {dependency} is {dependency_status}")
    return not reasons, reasons


def find_cycle(graph: Dict[str, List[str]]) -> List[str]:
    visiting = set()
    visited = set()
    stack: List[str] = []

    def visit(node: str) -> List[str]:
        if node in visiting:
            start = stack.index(node)
            return stack[start:] + [node]
        if node in visited:
            return []
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                cycle = visit(dependency)
                if cycle:
                    return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return []

    for node in graph:
        cycle = visit(node)
        if cycle:
            return cycle
    return []


def artifact_rows(workspace: Path) -> Iterable[Tuple[str, str, str, str]]:
    for path in sorted(workspace.rglob("*.md")):
        if path.name.endswith("-template.md"):
            continue
        relative = str(path.relative_to(workspace))
        try:
            data = parse_frontmatter(path.read_text(encoding="utf-8"))
            yield (
                relative,
                data.get("stage", "?"),
                data.get("status", "?"),
                data.get("last_updated", "?"),
            )
        except ValueError as exc:
            yield (relative, "?", "invalid", str(exc))


def command_init(args: argparse.Namespace) -> int:
    workstream = validate_identifier(args.workstream, "Workstream")
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.is_dir():
        raise ValueError(f"Repository root is not a directory: {repo_root}")
    workspace = repo_root / args.workspace_dir / workstream
    if workspace.exists():
        raise ValueError(f"Workspace already exists: {workspace}. Resume it instead.")

    template_root = Path(__file__).resolve().parent.parent / "assets" / "workspace-templates"
    if not template_root.is_dir():
        raise ValueError(f"Bundled templates are missing: {template_root}")

    timestamp = now_iso()
    jira_reference = (
        f"[{workstream}]({args.jira_url.strip()})"
        if args.jira_url and args.jira_url.strip()
        else f"`{workstream}`"
    )
    values = {
        "WORKSTREAM_ID": workstream,
        "TITLE": args.title.strip() or workstream,
        "NOW": timestamp,
        "REPO_ROOT": str(repo_root),
        "JIRA_REFERENCE": jira_reference,
    }

    workspace.mkdir(parents=True, exist_ok=False)
    try:
        render_tree(template_root, workspace, values)
    except Exception:
        shutil.rmtree(workspace, ignore_errors=True)
        raise

    print(workspace)
    print("Initialized DAC Markdown artifacts only.")
    print(f"Read first: {workspace / '00-control.md'}")
    return 0


def command_status(args: argparse.Namespace) -> int:
    workspace = ensure_workspace(Path(args.workspace))
    rows = list(artifact_rows(workspace))
    widths = [len("Artifact"), len("Stage"), len("Status"), len("Last updated")]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    header = ("Artifact", "Stage", "Status", "Last updated")
    print("  ".join(value.ljust(widths[index]) for index, value in enumerate(header)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)))
    return 0


def command_validate(args: argparse.Namespace) -> int:
    workspace = ensure_workspace(Path(args.workspace))
    errors: List[str] = []
    expected_workstream = ""

    for relative in REQUIRED_FILES:
        path = workspace / relative
        if not path.is_file():
            errors.append(f"Missing required file: {relative}")

    for path in sorted(workspace.rglob("*.md")):
        if path.name.endswith("-template.md"):
            continue
        relative = str(path.relative_to(workspace))
        text = path.read_text(encoding="utf-8")
        if re.search(r"{{[A-Z0-9_]+}}", text):
            errors.append(f"Unresolved template token in {relative}")
        try:
            data = parse_frontmatter(text)
        except ValueError as exc:
            errors.append(f"Invalid frontmatter in {relative}: {exc}")
            continue
        for key in ("artifact", "workstream", "stage", "status", "last_updated", "inputs"):
            if not data.get(key):
                errors.append(f"Missing frontmatter key {key!r} in {relative}")
        if data.get("status") not in ALLOWED_STATUSES:
            errors.append(f"Invalid status {data.get('status')!r} in {relative}")
        if relative == "00-control.md":
            expected_workstream = data.get("workstream", "")
        elif expected_workstream and data.get("workstream") != expected_workstream:
            errors.append(
                f"Workstream mismatch in {relative}: {data.get('workstream')!r} "
                f"!= {expected_workstream!r}"
            )

    for directory in (workspace / "portions", workspace / "results", workspace / "reviews"):
        if not directory.is_dir():
            errors.append(f"Missing required directory: {directory.relative_to(workspace)}")

    marker_checks = {
        "00-control.md": "<!-- GATE_LOG -->",
        "03-decisions.md": "<!-- DECISION_LOG -->",
    }
    for relative, marker in marker_checks.items():
        path = workspace / relative
        if path.is_file() and marker not in path.read_text(encoding="utf-8"):
            errors.append(f"Missing marker {marker} in {relative}")

    records = portion_records(workspace)
    graph: Dict[str, List[str]] = {}
    for portion_id, (path, data) in records.items():
        if path.stem != portion_id:
            errors.append(f"Portion filename {path.name} does not match ID {portion_id}")
        if not EXECUTOR_PATTERN.fullmatch(data.get("executor", "")):
            errors.append(f"Invalid executor in portions/{path.name}: {data.get('executor')!r}")
        graph[portion_id] = dependency_ids(data.get("depends_on", ""))
        for dependency in graph[portion_id]:
            if dependency == portion_id:
                errors.append(f"Portion {portion_id} depends on itself")
            elif dependency not in records:
                errors.append(f"Portion {portion_id} has missing dependency {dependency}")

    cycle = find_cycle(graph)
    if cycle:
        errors.append("Portion dependency cycle: " + " -> ".join(cycle))

    for path in sorted((workspace / "results").glob("*.md")):
        if path.name.endswith("-template.md"):
            continue
        try:
            data = parse_frontmatter(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        portion_id = data.get("portion_id", "")
        if portion_id not in records:
            errors.append(f"Result {path.name} refers to missing portion {portion_id!r}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validation passed: {workspace}")
    return 0


def command_approve(args: argparse.Namespace) -> int:
    workspace = ensure_workspace(Path(args.workspace))
    path = safe_member(workspace, args.artifact)
    text = path.read_text(encoding="utf-8")
    data = parse_frontmatter(text)
    if data.get("status") != "proposed":
        raise ValueError(
            f"Content approval requires status 'proposed'; {args.artifact} is "
            f"{data.get('status')!r}."
        )
    if "<!-- APPROVAL_LOG -->" not in text:
        raise ValueError(f"Artifact has no approval log: {args.artifact}")

    timestamp = now_iso()
    notes = args.notes.strip() if args.notes else "-"
    row = "| {timestamp} | {by} | {scope} | {notes} |".format(
        timestamp=escape_cell(timestamp),
        by=escape_cell(args.by),
        scope=escape_cell(args.scope),
        notes=escape_cell(notes),
    )
    text = update_frontmatter(text, {"status": "approved", "last_updated": timestamp})
    text = append_before_marker(text, "<!-- APPROVAL_LOG -->", row)
    path.write_text(text, encoding="utf-8")
    log_control(
        workspace,
        timestamp,
        args.by,
        args.artifact,
        "content",
        args.scope,
        notes,
    )
    print(f"Recorded content approval for {args.artifact}")
    print("This does not authorize execution, Git, Jira, PR, or remote actions.")
    return 0


def command_decision(args: argparse.Namespace) -> int:
    workspace = ensure_workspace(Path(args.workspace))
    decision_id = validate_identifier(args.id, "Decision ID")
    path = workspace / "03-decisions.md"
    text = path.read_text(encoding="utf-8")
    if re.search(rf"^\|\s*{re.escape(decision_id)}\s*\|", text, flags=re.MULTILINE):
        raise ValueError(f"Decision ID already exists: {decision_id}")
    timestamp = now_iso()
    decided_at = f"{timestamp} by {args.by}" if args.status in {"decided", "superseded"} else "-"
    row = "| {id} | {question} | {alternatives} | {recommendation} | {owner} | {status} | {outcome} | {rationale} | {evidence} | {decided_at} |".format(
        id=escape_cell(decision_id),
        question=escape_cell(args.question),
        alternatives=escape_cell(args.alternatives or "-"),
        recommendation=escape_cell(args.recommendation or "-"),
        owner=escape_cell(args.owner or args.by),
        status=escape_cell(args.status),
        outcome=escape_cell(args.outcome or "-"),
        rationale=escape_cell(args.rationale or "-"),
        evidence=escape_cell(args.evidence or "-"),
        decided_at=escape_cell(decided_at),
    )
    data = parse_frontmatter(text)
    updates = {"last_updated": timestamp}
    if data.get("status") == "not_started":
        updates["status"] = "drafting"
    text = update_frontmatter(text, updates)
    text = append_before_marker(text, "<!-- DECISION_LOG -->", row)
    path.write_text(text, encoding="utf-8")
    update_control_timestamp(workspace, timestamp)
    print(f"Recorded decision {decision_id} with status {args.status}")
    return 0


def command_portion_create(args: argparse.Namespace) -> int:
    workspace = ensure_workspace(Path(args.workspace))
    portion_id = validate_identifier(args.id, "Portion ID")
    executor = validate_executor(args.executor)
    dependencies = [validate_identifier(item, "Dependency ID") for item in dependency_ids(args.depends_on)]
    destination = safe_member(workspace, f"portions/{portion_id}.md", must_exist=False)
    if destination.exists():
        raise ValueError(f"Portion already exists: {portion_id}")
    template = Path(__file__).resolve().parent.parent / "assets" / "workspace-templates" / "portions" / "portion-template.md"
    if not template.is_file():
        raise ValueError(f"Portion template is missing: {template}")
    content = template.read_text(encoding="utf-8")
    control_data = parse_frontmatter((workspace / "00-control.md").read_text(encoding="utf-8"))
    values = {
        "WORKSTREAM_ID": control_data.get("workstream", ""),
        "PORTION_ID": portion_id,
        "PORTION_TITLE": args.title.strip() or portion_id,
        "DEPENDS_ON": ",".join(dependencies) if dependencies else "-",
        "EXECUTOR": executor,
        "PORTION_JIRA": args.jira.strip() or "-",
        "SPEC_DIRECTORY": args.spec_dir.strip() or "-",
        "NOW": now_iso(),
    }
    for token, value in values.items():
        content = content.replace("{{" + token + "}}", value)
    destination.write_text(content, encoding="utf-8")
    update_control_timestamp(workspace, values["NOW"])
    print(destination)
    print("Created a proposed portion envelope. Complete and approve it before dispatch.")
    return 0


def command_ready(args: argparse.Namespace) -> int:
    workspace = ensure_workspace(Path(args.workspace))
    records = portion_records(workspace)
    ready_ids = []
    blocked_rows = []
    settled_rows = []
    for portion_id in sorted(records):
        status = records[portion_id][1].get("status", "?")
        if status in TERMINAL_DEPENDENCY_STATUSES or status == "superseded":
            if args.all:
                settled_rows.append((portion_id, status))
            continue
        is_ready, reasons = readiness(portion_id, records)
        if is_ready:
            ready_ids.append(portion_id)
        elif args.all:
            blocked_rows.append((portion_id, "; ".join(reasons)))
    if ready_ids:
        print("Planning-ready portions:")
        for portion_id in ready_ids:
            data = records[portion_id][1]
            print(f"- {portion_id}: executor={data.get('executor', '?')} jira={data.get('jira', '-')}")
    else:
        print("No portions are planning-ready.")
    if blocked_rows:
        print("Not ready:")
        for portion_id, reason in blocked_rows:
            print(f"- {portion_id}: {reason}")
    if settled_rows:
        print("Settled:")
        for portion_id, status in settled_rows:
            print(f"- {portion_id}: {status}")
    print("Readiness does not authorize implementation or remote actions.")
    return 0


def command_transition(args: argparse.Namespace) -> int:
    workspace = ensure_workspace(Path(args.workspace))
    portion_id = validate_identifier(args.portion, "Portion ID")
    path = safe_member(workspace, f"portions/{portion_id}.md")
    text = path.read_text(encoding="utf-8")
    data = parse_frontmatter(text)
    current = data.get("status", "")
    target = args.to
    allowed = PORTION_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise ValueError(f"Invalid portion transition: {current!r} -> {target!r}")
    if target == "executing" and current == "approved":
        records = portion_records(workspace)
        is_ready, reasons = readiness(portion_id, records)
        if not is_ready:
            raise ValueError("Portion is not ready: " + "; ".join(reasons))
    timestamp = now_iso()
    row = "| {timestamp} | {current} | {target} | {actor} | {reason} |".format(
        timestamp=escape_cell(timestamp),
        current=escape_cell(current),
        target=escape_cell(target),
        actor=escape_cell(args.by),
        reason=escape_cell(args.reason or "-"),
    )
    text = update_frontmatter(text, {"status": target, "last_updated": timestamp})
    text = append_before_marker(text, "<!-- STATE_LOG -->", row)
    path.write_text(text, encoding="utf-8")
    update_control_timestamp(workspace, timestamp)
    print(f"Transitioned {portion_id}: {current} -> {target}")
    if target == "executing":
        print("State transition does not itself grant C3 or V2 authority.")
    return 0


def command_result_create(args: argparse.Namespace) -> int:
    workspace = ensure_workspace(Path(args.workspace))
    portion_id = validate_identifier(args.portion, "Portion ID")
    portion_path = safe_member(workspace, f"portions/{portion_id}.md")
    portion_data = parse_frontmatter(portion_path.read_text(encoding="utf-8"))
    destination = safe_member(workspace, f"results/{portion_id}.md", must_exist=False)
    if destination.exists():
        raise ValueError(f"Result already exists: {destination}")
    template = Path(__file__).resolve().parent.parent / "assets" / "workspace-templates" / "results" / "result-template.md"
    if not template.is_file():
        raise ValueError(f"Result template is missing: {template}")
    content = template.read_text(encoding="utf-8")
    control_data = parse_frontmatter((workspace / "00-control.md").read_text(encoding="utf-8"))
    values = {
        "WORKSTREAM_ID": control_data.get("workstream", ""),
        "PORTION_ID": portion_id,
        "EXECUTOR": portion_data.get("executor", "unknown"),
        "NOW": now_iso(),
    }
    for token, value in values.items():
        content = content.replace("{{" + token + "}}", value)
    destination.write_text(content, encoding="utf-8")
    update_control_timestamp(workspace, values["NOW"])
    print(destination)
    return 0
def _git(*cmd: str) -> Tuple[int, str]:
    result = subprocess.run(
        ["git"] + list(cmd), capture_output=True, text=True
    )
    return result.returncode, result.stdout.strip()
def _discover_branch(jira: str) -> str:
    if not jira:
        return ""
    ticket_match = re.search(r"[A-Za-z]+-(\d+)", jira)
    if not ticket_match:
        return ""
    ticket_num = ticket_match.group(1)
    rc, out = _git("branch", "--list", f"*{ticket_num}*")
    if rc != 0 or not out:
        return ""
    candidates = [b.strip().lstrip("* +") for b in out.splitlines() if b.strip()]
    if len(candidates) == 1:
        return candidates[0]
    return ""
def command_solo_adopt(args: argparse.Namespace) -> int:
    """Adopt an existing Jira ticket into solo management."""
    workspace = ensure_workspace(Path(args.workspace))
    ticket_id = validate_identifier(args.ticket_id, "Ticket ID")

    # Ensure solo directory exists
    solo_dir = workspace / "solo"
    solo_dir.mkdir(exist_ok=True)

    destination = safe_member(workspace, f"solo/{ticket_id}.md", must_exist=False)
    if destination.exists():
        raise ValueError(f"Solo ticket already exists: {ticket_id}")

    template = Path(__file__).resolve().parent.parent / "assets" / "workspace-templates" / "solo" / "solo-template.md"
    if not template.is_file():
        raise ValueError(f"Solo template is missing: {template}")

    content = template.read_text(encoding="utf-8")
    timestamp = now_iso()

    # Get workstream from control
    control_data = parse_frontmatter((workspace / "00-control.md").read_text(encoding="utf-8"))
    workstream = control_data.get("workstream", "")

    # Construct branch name
    branch_name = args.branch or f"feature/{ticket_id}-{args.title.lower().replace(' ', '-')[:40]}"

    values = {
        "WORKSTREAM_ID": workstream,
        "TICKET_ID": ticket_id,
        "TITLE": args.title.strip() or ticket_id,
        "OUTCOME": args.outcome.strip() if args.outcome else "To be defined",
        "ACCEPTANCE_CRITERIA": args.ac.strip() if args.ac else "- [ ] To be defined",
        "STATUS": "adopted",
        "EXECUTOR": args.executor or "direct",
        "JIRA_URL": args.jira_url.strip() if args.jira_url else f"https://jira.example.com/browse/{ticket_id}",
        "BRANCH": branch_name,
        "BASE_BRANCH": args.base_branch or "main",
        "NOW": timestamp,
        "SOURCE": "adopted from existing Jira ticket",
    }

    for token, value in values.items():
        content = content.replace("{{" + token + "}}", value)

    destination.write_text(content, encoding="utf-8")
    update_control_timestamp(workspace, timestamp)

    print(destination)
    print(f"Adopted solo ticket {ticket_id}")
    print("Next steps:")
    print(f"1. Review and refine {destination.relative_to(workspace)}")
    print(f"2. Ensure Jira ticket has proper acceptance criteria")
    print(f"3. Create branch: git checkout -b {branch_name}")
    return 0


def command_solo_create(args: argparse.Namespace) -> int:
    """Create a new solo ticket (Jira creation would happen outside this script)."""
    workspace = ensure_workspace(Path(args.workspace))
    ticket_id = args.ticket_id.strip()

    if not ticket_id:
        print("Note: This command creates the DAC envelope.")
        print("Create the Jira ticket first, then call with --ticket-id")
        return 1

    ticket_id = validate_identifier(ticket_id, "Ticket ID")

    # Ensure solo directory exists
    solo_dir = workspace / "solo"
    solo_dir.mkdir(exist_ok=True)

    destination = safe_member(workspace, f"solo/{ticket_id}.md", must_exist=False)
    if destination.exists():
        raise ValueError(f"Solo ticket already exists: {ticket_id}")

    template = Path(__file__).resolve().parent.parent / "assets" / "workspace-templates" / "solo" / "solo-template.md"
    if not template.is_file():
        raise ValueError(f"Solo template is missing: {template}")

    content = template.read_text(encoding="utf-8")
    timestamp = now_iso()

    # Get workstream from control
    control_data = parse_frontmatter((workspace / "00-control.md").read_text(encoding="utf-8"))
    workstream = control_data.get("workstream", "")

    # Construct branch name
    branch_name = args.branch or f"feature/{ticket_id}-{args.title.lower().replace(' ', '-')[:40]}"

    values = {
        "WORKSTREAM_ID": workstream,
        "TICKET_ID": ticket_id,
        "TITLE": args.title.strip() or ticket_id,
        "OUTCOME": args.outcome.strip() if args.outcome else "To be defined",
        "ACCEPTANCE_CRITERIA": args.ac.strip() if args.ac else "- [ ] To be defined",
        "STATUS": "adopted",
        "EXECUTOR": args.executor or "direct",
        "JIRA_URL": args.jira_url.strip() if args.jira_url else f"https://jira.example.com/browse/{ticket_id}",
        "BRANCH": branch_name,
        "BASE_BRANCH": args.base_branch or "main",
        "NOW": timestamp,
        "SOURCE": "created as new solo ticket",
    }

    for token, value in values.items():
        content = content.replace("{{" + token + "}}", value)

    destination.write_text(content, encoding="utf-8")
    update_control_timestamp(workspace, timestamp)

    print(destination)
    print(f"Created solo ticket envelope for {ticket_id}")
    print("Next steps:")
    print(f"1. Review and complete {destination.relative_to(workspace)}")
    print(f"2. Create branch: git checkout -b {branch_name}")
    return 0


def command_solo_status(args: argparse.Namespace) -> int:
    """Show status of solo tickets."""
    workspace = ensure_workspace(Path(args.workspace))
    records = solo_records(workspace)

    if not records:
        print("No solo tickets found.")
        return 0

    print(f"Solo tickets in {workspace.name}:")
    print()

    headers = ("Ticket", "Status", "Branch", "Executor", "Last Updated")
    widths = [len(h) for h in headers]

    rows = []
    for ticket_id in sorted(records):
        _, data = records[ticket_id]
        row = (
            ticket_id,
            data.get("status", "?"),
            data.get("branch", "-"),
            data.get("executor", "?"),
            data.get("last_updated", "?"),
        )
        rows.append(row)
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(val))

    print("  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print("  ".join(val.ljust(widths[i]) for i, val in enumerate(row)))

    return 0


def command_solo_transition(args: argparse.Namespace) -> int:
    """Record a state transition for a solo ticket."""
    workspace = ensure_workspace(Path(args.workspace))
    ticket_id = validate_identifier(args.ticket_id, "Ticket ID")
    path = safe_member(workspace, f"solo/{ticket_id}.md")
    text = path.read_text(encoding="utf-8")
    data = parse_frontmatter(text)
    current = data.get("status", "")
    target = args.to

    allowed = SOLO_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise ValueError(f"Invalid solo ticket transition: {current!r} -> {target!r}")

    timestamp = now_iso()
    row = "| {timestamp} | {current} | {target} | {actor} | {reason} |".format(
        timestamp=escape_cell(timestamp),
        current=escape_cell(current),
        target=escape_cell(target),
        actor=escape_cell(args.by),
        reason=escape_cell(args.reason or "-"),
    )
    text = update_frontmatter(text, {"status": target, "last_updated": timestamp})
    text = append_before_marker(text, "<!-- STATE_LOG -->", row)
    path.write_text(text, encoding="utf-8")
    update_control_timestamp(workspace, timestamp)

    print(f"Transitioned {ticket_id}: {current} -> {target}")
    return 0


def command_sync(args: argparse.Namespace) -> int:
    workspace = ensure_workspace(Path(args.workspace))
    portion_recs = portion_records(workspace)
    solo_recs = solo_records(workspace)
    parent_branch = args.parent_branch
    if not parent_branch:
        rc, out = _git("rev-parse", "--abbrev-ref", "HEAD")
        if rc != 0:
            raise ValueError("Could not determine current branch. Use --parent-branch.")
        parent_branch = out
    rc, _ = _git("rev-parse", "--verify", parent_branch)
    if rc != 0:
        raise ValueError(f"Parent branch not found: {parent_branch}")

    rows: List[Tuple[str, ...]] = []
    merge_cmds: List[str] = []
    push_branches: List[str] = []

    # Process portions
    for portion_id in sorted(portion_recs):
        _, data = portion_recs[portion_id]
        status = data.get("status", "?")
        branch = data.get("branch", "") or _discover_branch(data.get("jira", ""))
        type_label = "P"

        if not branch:
            rows.append((f"{type_label}:{portion_id}", status, "(no branch)", "-", "-", "-", ""))
            continue
        rc, _ = _git("rev-parse", "--verify", branch)
        if rc != 0:
            rows.append((f"{type_label}:{portion_id}", status, branch, "-", "-", "-", "not found"))
            continue
        _, behind_s = _git("rev-list", "--count", f"{branch}..{parent_branch}")
        _, ahead_s = _git("rev-list", "--count", f"{parent_branch}..{branch}")
        behind = int(behind_s) if behind_s.isdigit() else -1
        ahead = int(ahead_s) if ahead_s.isdigit() else -1
        _, local_sha = _git("rev-parse", branch)
        rc_r, remote_sha = _git("rev-parse", f"origin/{branch}")
        if rc_r != 0:
            remote_status = "no remote"
        elif local_sha == remote_sha:
            remote_status = "in sync"
        else:
            _, la_s = _git("rev-list", "--count", f"origin/{branch}..{branch}")
            _, lb_s = _git("rev-list", "--count", f"{branch}..origin/{branch}")
            la = int(la_s) if la_s.isdigit() else 0
            lb = int(lb_s) if lb_s.isdigit() else 0
            if la > 0 and lb > 0:
                remote_status = f"diverged (+{la}/-{lb})"
            elif la > 0:
                remote_status = f"unpushed (+{la})"
            else:
                remote_status = f"behind remote (-{lb})"
        active = status not in {"integrated", "complete", "superseded"}
        note = ""
        if behind > 0 and active:
            merge_cmds.append(
                f"git checkout {branch} && git merge {parent_branch} --no-edit"
            )
            note = "MERGE PARENT"
        elif behind > 0:
            note = "stale (merged/done)"
        if "unpushed" in remote_status and active:
            push_branches.append(branch)
            note = f"{note}, PUSH" if note else "PUSH"
        rows.append((
            f"{type_label}:{portion_id}", status, branch,
            str(behind), str(ahead), remote_status, note,
        ))

    # Process solo tickets
    for ticket_id in sorted(solo_recs):
        _, data = solo_recs[ticket_id]
        status = data.get("status", "?")
        branch = data.get("branch", "") or _discover_branch(ticket_id)
        type_label = "S"

        if not branch:
            rows.append((f"{type_label}:{ticket_id}", status, "(no branch)", "-", "-", "-", ""))
            continue
        rc, _ = _git("rev-parse", "--verify", branch)
        if rc != 0:
            rows.append((f"{type_label}:{ticket_id}", status, branch, "-", "-", "-", "not found"))
            continue
        _, behind_s = _git("rev-list", "--count", f"{branch}..{parent_branch}")
        _, ahead_s = _git("rev-list", "--count", f"{parent_branch}..{branch}")
        behind = int(behind_s) if behind_s.isdigit() else -1
        ahead = int(ahead_s) if ahead_s.isdigit() else -1
        _, local_sha = _git("rev-parse", branch)
        rc_r, remote_sha = _git("rev-parse", f"origin/{branch}")
        if rc_r != 0:
            remote_status = "no remote"
        elif local_sha == remote_sha:
            remote_status = "in sync"
        else:
            _, la_s = _git("rev-list", "--count", f"origin/{branch}..{branch}")
            _, lb_s = _git("rev-list", "--count", f"{branch}..origin/{branch}")
            la = int(la_s) if la_s.isdigit() else 0
            lb = int(lb_s) if lb_s.isdigit() else 0
            if la > 0 and lb > 0:
                remote_status = f"diverged (+{la}/-{lb})"
            elif la > 0:
                remote_status = f"unpushed (+{la})"
            else:
                remote_status = f"behind remote (-{lb})"
        active = status not in {"integrated", "complete", "superseded"}
        note = ""
        if behind > 0 and active:
            merge_cmds.append(
                f"git checkout {branch} && git merge {parent_branch} --no-edit"
            )
            note = "MERGE PARENT"
        elif behind > 0:
            note = "stale (merged/done)"
        if "unpushed" in remote_status and active:
            push_branches.append(branch)
            note = f"{note}, PUSH" if note else "PUSH"
        rows.append((
            f"{type_label}:{ticket_id}", status, branch,
            str(behind), str(ahead), remote_status, note,
        ))

    headers = ("Item", "Status", "Branch", "Behind", "Ahead", "Remote", "Action")
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(val))
    print(f"Parent branch: {parent_branch}")
    print(f"Legend: P:portion S:solo")
    print()
    print("  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print("  ".join(val.ljust(widths[i]) for i, val in enumerate(row)))
    if merge_cmds or push_branches:
        print()
        print("Suggested actions:")
        for cmd in merge_cmds:
            print(f"  {cmd}")
        if push_branches:
            print(f"  git push origin {' '.join(push_branches)}")
    else:
        print()
        print("All active branches are in sync.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage DAC Markdown artifacts without executing delivery work."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init", help="Initialize a .dac workspace")
    init_parser.add_argument("--workstream", required=True)
    init_parser.add_argument("--repo-root", default=".")
    init_parser.add_argument("--workspace-dir", default=".dac")
    init_parser.add_argument("--title", default="")
    init_parser.add_argument("--jira-url", default="")
    init_parser.set_defaults(func=command_init)

    status_parser = commands.add_parser("status", help="Show artifact states")
    status_parser.add_argument("--workspace", required=True)
    status_parser.set_defaults(func=command_status)

    validate_parser = commands.add_parser("validate", help="Validate workspace structure")
    validate_parser.add_argument("--workspace", required=True)
    validate_parser.set_defaults(func=command_validate)

    approve_parser = commands.add_parser("approve", help="Record content approval")
    approve_parser.add_argument("--workspace", required=True)
    approve_parser.add_argument("--artifact", required=True)
    approve_parser.add_argument("--by", required=True)
    approve_parser.add_argument("--scope", required=True)
    approve_parser.add_argument("--notes", default="")
    approve_parser.set_defaults(func=command_approve)

    decision_parser = commands.add_parser("decision", help="Append a parent decision")
    decision_parser.add_argument("--workspace", required=True)
    decision_parser.add_argument("--id", required=True)
    decision_parser.add_argument("--question", required=True)
    decision_parser.add_argument("--outcome", default="")
    decision_parser.add_argument("--by", required=True)
    decision_parser.add_argument("--owner", default="")
    decision_parser.add_argument("--alternatives", default="")
    decision_parser.add_argument("--recommendation", default="")
    decision_parser.add_argument("--rationale", default="")
    decision_parser.add_argument("--evidence", default="")
    decision_parser.add_argument(
        "--status", choices=("decided", "deferred", "superseded"), default="decided"
    )
    decision_parser.set_defaults(func=command_decision)

    portion_parser = commands.add_parser("portion", help="Manage portion envelopes")
    portion_commands = portion_parser.add_subparsers(dest="portion_command", required=True)
    portion_create = portion_commands.add_parser("create", help="Create a proposed portion")
    portion_create.add_argument("--workspace", required=True)
    portion_create.add_argument("--id", required=True)
    portion_create.add_argument("--title", required=True)
    portion_create.add_argument("--executor", required=True)
    portion_create.add_argument("--depends-on", default="")
    portion_create.add_argument("--jira", default="")
    portion_create.add_argument("--spec-dir", default="")
    portion_create.set_defaults(func=command_portion_create)

    ready_parser = commands.add_parser("ready", help="Derive dependency-ready portions")
    ready_parser.add_argument("--workspace", required=True)
    ready_parser.add_argument("--all", action="store_true", help="Also explain non-ready portions")
    ready_parser.set_defaults(func=command_ready)

    transition_parser = commands.add_parser("transition", help="Record a portion state transition")
    transition_parser.add_argument("--workspace", required=True)
    transition_parser.add_argument("--portion", required=True)
    transition_parser.add_argument("--to", required=True, choices=sorted(ALLOWED_STATUSES))
    transition_parser.add_argument("--by", default="coordinator")
    transition_parser.add_argument("--reason", default="")
    transition_parser.set_defaults(func=command_transition)
    sync_parser = commands.add_parser(
        "sync", help="Report git sync status of portion branches vs parent"
    )
    sync_parser.add_argument("--workspace", required=True)
    sync_parser.add_argument(
        "--parent-branch", default="",
        help="Parent integration branch (default: current branch)",
    )
    sync_parser.set_defaults(func=command_sync)

    result_parser = commands.add_parser("result", help="Manage normalized results")
    result_commands = result_parser.add_subparsers(dest="result_command", required=True)
    result_create = result_commands.add_parser("create", help="Create a result for a portion")
    result_create.add_argument("--workspace", required=True)
    result_create.add_argument("--portion", required=True)
    result_create.set_defaults(func=command_result_create)

    # Solo ticket management
    solo_parser = commands.add_parser("solo", help="Manage solo tickets")
    solo_commands = solo_parser.add_subparsers(dest="solo_command", required=True)

    solo_adopt = solo_commands.add_parser("adopt", help="Adopt an existing Jira ticket")
    solo_adopt.add_argument("--workspace", required=True)
    solo_adopt.add_argument("--ticket-id", required=True)
    solo_adopt.add_argument("--title", required=True)
    solo_adopt.add_argument("--outcome", default="")
    solo_adopt.add_argument("--ac", default="", help="Acceptance criteria")
    solo_adopt.add_argument("--executor", default="direct")
    solo_adopt.add_argument("--jira-url", default="")
    solo_adopt.add_argument("--branch", default="")
    solo_adopt.add_argument("--base-branch", default="main")
    solo_adopt.set_defaults(func=command_solo_adopt)

    solo_create = solo_commands.add_parser("create", help="Create a new solo ticket envelope")
    solo_create.add_argument("--workspace", required=True)
    solo_create.add_argument("--ticket-id", required=True)
    solo_create.add_argument("--title", required=True)
    solo_create.add_argument("--outcome", default="")
    solo_create.add_argument("--ac", default="", help="Acceptance criteria")
    solo_create.add_argument("--executor", default="direct")
    solo_create.add_argument("--jira-url", default="")
    solo_create.add_argument("--branch", default="")
    solo_create.add_argument("--base-branch", default="main")
    solo_create.set_defaults(func=command_solo_create)

    solo_status = solo_commands.add_parser("status", help="Show solo ticket status")
    solo_status.add_argument("--workspace", required=True)
    solo_status.set_defaults(func=command_solo_status)

    solo_transition = solo_commands.add_parser("transition", help="Transition solo ticket state")
    solo_transition.add_argument("--workspace", required=True)
    solo_transition.add_argument("--ticket-id", required=True)
    solo_transition.add_argument("--to", required=True, choices=sorted(SOLO_STATUSES))
    solo_transition.add_argument("--by", default="coordinator")
    solo_transition.add_argument("--reason", default="")
    solo_transition.set_defaults(func=command_solo_transition)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
