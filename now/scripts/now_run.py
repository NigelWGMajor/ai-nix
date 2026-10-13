#!/usr/bin/env python3
"""Instance rotation and prior/current comparison for the NOW skill.

Subcommands:
  plan     Decide whether this run overwrites the latest instance or starts a new one.
  begin    Create (or re-date) the instance folder chosen by `plan`.
  compare  Diff two triage CSVs and write comparison.csv plus a Markdown summary.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

PREFIX = "now"
CSV_NAME = "triage.csv"
CONTROL = "00-control.md"
NAME_RE = re.compile(rf"^{PREFIX}-(\d\d)-(\d\d)-(\d\d)-([a-z]+)(?:-.+)?$")
RUN_DATE_RE = re.compile(r"^- Run date:\s*(\d{4}-\d\d-\d\d)", re.MULTILINE)

COLUMNS = [
    "item_type", "key", "url", "title", "issue_type", "status", "owner", "reporter",
    "scope", "parent", "roadmap_epic", "jira_priority", "track", "priority",
    "action_type", "est_hours", "triage_reason", "initial_steps", "last_updated",
    "last_activity", "linked_items", "related_prs", "pr_state", "needs_nick",
]


def output_base() -> Path:
    configured = os.environ.get("TOOLING_OUTPUT_PATH", "").strip()
    if configured and Path(configured).is_absolute():
        return Path(configured).resolve()
    return Path("C:/.data/now") if sys.platform == "win32" else Path.home() / ".local/share/claude-skills/now"


def folder_date(p: Path) -> dt.date | None:
    m = NAME_RE.match(p.name)
    return dt.date(2000 + int(m[1]), int(m[2]), int(m[3])) if m else None


def run_date(p: Path) -> dt.date | None:
    """Prefer the recorded run date; fall back to the folder name."""
    control = p / CONTROL
    if control.exists():
        m = RUN_DATE_RE.search(control.read_text(encoding="utf-8"))
        if m:
            return dt.date.fromisoformat(m[1])
    return folder_date(p)


def instances(base: Path) -> list[Path]:
    """Existing NOW instances that hold results, oldest first."""
    found = [p for p in base.glob(f"{PREFIX}-*") if p.is_dir() and NAME_RE.match(p.name) and (p / CSV_NAME).exists()]
    return sorted(found, key=lambda p: (run_date(p) or dt.date.min, p.name))


def next_suffix(base: Path, day: dt.date) -> str:
    stem = f"{PREFIX}-{day:%y-%m-%d}-"
    used = {m[4] for p in base.glob(stem + "*") if (m := NAME_RE.match(p.name))}
    for n in range(26 * 27):
        s = chr(97 + n) if n < 26 else chr(97 + n // 26 - 1) + chr(97 + n % 26)
        if s not in used:
            return s
    raise RuntimeError("suffix space exhausted")


def cmd_plan(a: argparse.Namespace) -> int:
    base = output_base()
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    found = instances(base)
    latest = found[-1] if found else None
    age = (today - run_date(latest)).days if latest and run_date(latest) else None
    # The latest result set is replaced when it is closer to today than one window.
    overwrite = latest is not None and age is not None and age < a.window_days
    prior = (found[-2] if len(found) > 1 else None) if overwrite else latest
    plan = {
        "today": today.isoformat(),
        "window_days": a.window_days,
        "window_start": (today - dt.timedelta(days=a.window_days)).isoformat(),
        "output_base": str(base),
        "mode": "overwrite" if overwrite else "new",
        "latest": str(latest) if latest else None,
        "latest_age_days": age,
        "overwrite_target": str(latest) if overwrite else None,
        "prior": str(prior) if prior else None,
        "prior_run_date": run_date(prior).isoformat() if prior else None,
    }
    print(json.dumps(plan, indent=2))
    return 0


def cmd_begin(a: argparse.Namespace) -> int:
    base = output_base()
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    context = re.sub(r"[^a-z0-9]+", "-", (a.context_suffix or "").lower()).strip("-")
    tail = f"-{context}" if context else ""
    if a.overwrite:
        target = Path(a.overwrite).resolve()
        if target.parent != base.resolve() or not NAME_RE.match(target.name):
            print(f"refusing to re-date {target}: not a NOW instance under {base}", file=sys.stderr)
            return 2
        dest = base / f"{PREFIX}-{today:%y-%m-%d}-{next_suffix(base, today)}{tail}"
        if folder_date(target) == today:
            dest = target
        else:
            target.rename(dest)
    else:
        dest = base / f"{PREFIX}-{today:%y-%m-%d}-{next_suffix(base, today)}{tail}"
        dest.mkdir(parents=True)
    print(dest)
    return 0


def read_csv(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"{path}: missing columns {missing}")
        return {r["key"]: r for r in reader}


def hours(rows: dict[str, dict[str, str]]) -> float:
    return sum(float(r["est_hours"] or 0) for r in rows.values() if r["needs_nick"] == "Y")


def cmd_compare(a: argparse.Namespace) -> int:
    cur_dir, prior_dir = Path(a.current), Path(a.prior)
    cur, prior = read_csv(cur_dir / CSV_NAME), read_csv(prior_dir / CSV_NAME)
    out: list[dict[str, str]] = []

    def rec(key: str, change: str, p: dict | None, c: dict | None, detail: str = "") -> None:
        src = c or p or {}
        out.append({
            "key": key, "change": change, "title": src.get("title", ""), "url": src.get("url", ""),
            "prior_priority": (p or {}).get("priority", ""), "current_priority": (c or {}).get("priority", ""),
            "prior_status": (p or {}).get("status", ""), "current_status": (c or {}).get("status", ""),
            "prior_owner": (p or {}).get("owner", ""), "current_owner": (c or {}).get("owner", ""),
            "detail": detail,
        })

    unchanged = 0
    for key, c in cur.items():
        p = prior.get(key)
        if p is None:
            rec(key, "new", None, c)
            continue
        diffs = [(f, "status-changed") for f in ("status",) if p[f] != c[f]]
        if p["priority"] != c["priority"]:
            diffs.append(("priority", "priority-changed"))
        if p["owner"] != c["owner"]:
            diffs.append(("owner", "owner-changed"))
        if p["pr_state"] != c["pr_state"]:
            diffs.append(("pr_state", "review-state-changed"))
        if not diffs:
            unchanged += 1
            continue
        for field, label in diffs:
            rec(key, label, p, c, f"{field}: {p[field]} -> {c[field]}")
    for key, p in prior.items():
        if key not in cur:
            # Absence is ambiguous: finished, reassigned, or simply outside the current window.
            rec(key, "dropped", p, None, "not in current results (resolved, out of scope, or outside window)")

    order = {"new": 0, "priority-changed": 1, "status-changed": 2, "review-state-changed": 3, "owner-changed": 4, "dropped": 5}
    out.sort(key=lambda r: (order[r["change"]], r["key"]))
    cols = ["key", "change", "title", "url", "prior_priority", "current_priority", "prior_status",
            "current_status", "prior_owner", "current_owner", "detail"]
    with (cur_dir / "comparison.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    counts: dict[str, int] = {}
    for r in out:
        counts[r["change"]] = counts.get(r["change"], 0) + 1
    ph, ch = hours(prior), hours(cur)
    lines = [
        f"Prior: `{prior_dir.name}` ({len(prior)} rows) vs current: `{cur_dir.name}` ({len(cur)} rows).",
        "",
        "| Change | Count |", "|---|---|",
        *[f"| {k} | {counts[k]} |" for k in order if k in counts],
        f"| unchanged | {unchanged} |",
        "",
        f"Hours needing you directly: {ph:.2f} -> {ch:.2f} ({ch - ph:+.2f}).",
        "",
        "Full list: [comparison.csv](comparison.csv). `dropped` means absent from the current results, "
        "which can mean finished, reassigned, or outside the window.",
    ]
    print("\n".join(lines))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--window-days", type=int, default=14)
    p.add_argument("--today")
    p.set_defaults(fn=cmd_plan)
    b = sub.add_parser("begin")
    b.add_argument("--overwrite", help="existing instance to replace (re-dated to today)")
    b.add_argument("--context-suffix")
    b.add_argument("--today")
    b.set_defaults(fn=cmd_begin)
    c = sub.add_parser("compare")
    c.add_argument("--current", required=True)
    c.add_argument("--prior", required=True)
    c.set_defaults(fn=cmd_compare)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
