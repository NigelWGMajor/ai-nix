---
name: now
description: Triage the team's recent Jira and GitHub activity (default window 2 weeks) into a prioritized CSV plus a Findings.md, and compare it with the prior triage. Use when the user invokes now, or asks what needs attention across Pod 12 and core-team work since a date or over the last N weeks. Do not use for single-ticket investigation (use dg-jira-investigate) or code review. Read-only against Jira and GitHub; writes only to the output base.
---

# NOW: recent-activity triage with prior comparison

> **Quick help:** if invoked with `?` as the only parameter, summarize the usage below and stop.

Usage: `/now [window] [notes]`. `window` is a duration such as `2w`, `10d`, `3w` (default `2w` = 14 days). Anything else is a note that narrows or steers the triage.

Team, scope, GitHub handles and the roadmap-epic list live in [config.md](config.md). Read it first and follow it; if the user corrects something, update the file.

## 1. Decide where results go

Run:

```text
python <skill-dir>/scripts/now_run.py plan --window-days <N>
```

It prints JSON. The rule it applies: if the latest existing result set is **less than one window old**, this run **overwrites** it and the comparison is against the result set before that. Otherwise the latest result set becomes the **prior** and this run gets a new instance.

| `mode` | Meaning | Prior for comparison |
|---|---|---|
| `new` | Latest result set is at least one window old (or none exists) | `latest` |
| `overwrite` | Latest result set is less than one window old | the one before `latest`, may be null |

Tell the user which mode applies and why (latest instance, its age, the window) before writing anything. In `overwrite` mode, name the instance that will be replaced. Then run `begin`:

```text
now_run.py begin [--overwrite <overwrite_target>] [--context-suffix "<short title>"]
```

`begin` creates `<output-base>/now-YY-MM-DD-<suffix>[-<context>]`, or renames the overwritten instance to today's date. It prints the instance path. Do not ask for a context suffix unless the user offered one.

## 2. Gather (read-only)

Window start is `window_start` from the plan. Do not mutate Jira, GitHub, Git state, or the repo.

1. **Jira** via `mcp__plugin_jira-integration_atlassian__*` (load with ToolSearch). Two JQL searches, with comments and issuelinks expanded:
   - Pod 12: `cf[11300]` matches Pod 12 and `updated >= <window_start>`.
   - Outside pod: owned or reported by a core-team member, `updated >= <window_start>`, minus what the first search returned.
   - Add tickets named by in-scope PRs that neither search found.
   If Jira is unreachable, present the OAuth URL and stop (see memory: Jira authentication workflow).
2. **GitHub** with read-only `gh pr list/view` against `degreed/Degreed` and `degreed/fe-workspace`: PRs by each known handle and PRs whose title or branch names an in-scope PD key. Capture state, draft, review decision, mergeable state, CI status, reviewers, updated date. Include PRs merged or closed within the window.
3. Infer roadmap epics: walk each item's `parent` chain up to 5 levels (fetch ancestors not already returned). An ancestor of type Epic or Initiative counts as a roadmap epic when a team member in config is its assignee or reporter, or it is in Pod 12. Record the epic key in `roadmap_epic`.

Record the handles you lack, truncated comments, and anything else you could not see; these become Limits.

## 3. Triage

Produce one row per Jira issue or PR in `triage.csv`, with exactly the columns below (the comparison depends on them). Write it as UTF-8 with BOM, sorted by priority number, then P before B, then key.

`item_type, key, url, title, issue_type, status, owner, reporter, scope, parent, roadmap_epic, jira_priority, track, priority, action_type, est_hours, triage_reason, initial_steps, last_updated, last_activity, linked_items, related_prs, pr_state, needs_nick`

| Column | Rule |
|---|---|
| `key` | Jira key, or `be#NNNN` / `fe#NNNN` for PRs |
| `scope` | `pod12`, `related-outside-pod`, or `team-pr` |
| `track`, `priority` | `P` if a roadmap epic was inferred in step 2, else `B`; priority is `<track>-<1..4>` |
| `action_type` | `decide`, `review`, `unblock`, `verify-close`, `respond`, `acknowledge` |
| `est_hours` | Time for the first action, not to finish the work. A judgement, say so |
| `triage_reason`, `initial_steps` | Why it has that priority; what to do first |
| `last_activity` | Last comment (author, date, text truncated to 160 characters) or `review: <decision>` for PRs |
| `needs_nick` | `Y` if Nick owns or authored it, or priority number is 1 |

Judgement guidance:
- Priority 1 means something is blocked on Nick, a customer or support deadline exists, a PR stalls on conflicts/failing CI/no reviewer, or a review requested changes.
- Closed or resolved items with no open question are 4. Open items with no activity needing a decision are 3.
- A merged PR whose ticket is still open, or a ticket whose fix PR merged, is `verify-close`.
- Cross-check PRs against their tickets: a ticket status that disagrees with its PR is itself a finding.

**Reuse the prior triage.** When `prior` exists, read its `triage.csv`. For an item whose `status`, `last_updated` and `pr_state` are unchanged, carry forward its priority, action and reasoning unless new evidence says otherwise. Re-triage items that changed. This keeps the comparison meaningful: a priority change should reflect a real change, not re-rolled judgement.

Write the rows with a short Python script using `csv.DictWriter` and `encoding="utf-8-sig"`. Keep the script out of the instance and out of the repo.

## 4. Compare

If `prior` is non-null:

```text
now_run.py compare --current <instance> --prior <prior>
```

It validates both CSVs against the column list, writes `comparison.csv` into the instance, and prints a Markdown summary (new, priority-changed, status-changed, review-state-changed, owner-changed, dropped, unchanged, and the delta in hours needing Nick). Read `comparison.csv` and interpret it for the reader: the three or four changes that matter most, not the whole table. A `dropped` row is ambiguous (finished, reassigned, or outside the window); check the few that matter before calling them resolved.

If `prior` is null, say there is nothing to compare against and omit the section.

## 5. Write the instance

Files in the instance folder:

| File | Content |
|---|---|
| `triage.csv` | The rows from step 3 |
| `comparison.csv` | From step 4, when a prior exists |
| `Findings.md` | Reader-facing summary, below |
| `00-control.md` | Control record, below |

`00-control.md` must begin with these lines (the script reads `Run date`):

```markdown
# 00-control

- Run date: YYYY-MM-DD
- Window: YYYY-MM-DD to YYYY-MM-DD (N days)
- Mode: new | overwrite (replaced <old instance name>)
- Prior: <instance name or none>
- Rows: <count>
```

Then list the user decisions in force (from config), open assumptions, and the next safe action.

`Findings.md` follows the structure of the 2026-10-13 triage:

1. Title: `Recent triage: <scope>, <window_start> to <today>`, and a link to the CSV with row count.
2. **Answer:** how many P-1 and B-1 items, the hours needing Nick directly, and the two or three places they cluster, each with the concrete blocker. Plain sentences, no jargon.
3. **Since the prior triage** (only when a prior exists): the summary table from `compare`, then the changes that matter. Say what got better, what got worse, and what is new.
4. **Method and assumptions:** a short table (team, Jira scope, PR scope, track, number, estimates). Flag the roadmap-epic list and estimates as judgement.
5. **Limits:** missing handles, comment truncation, staleness of CI and review state (state the date read), related issues missed by owner/reporter matching, uncommitted working-tree changes relevant to an item.
6. **CSV columns:** the table from step 3.
7. **Next step:** one concrete action, naming the first item.

Return to the user only a short handoff: the answer, whether the run was `new` or `overwrite`, the instance path, and the open assumptions that need their correction.

## Guardrails

- Read-only against Jira, GitHub, Git, and the repo. Never transition tickets, comment, or push.
- Write only under the output base (`TOOLING_OUTPUT_PATH`, otherwise `C:\.data\now`). The only deletion-like action is the `overwrite` re-dating, which is the specified behaviour; announce it first.
- Do not copy the prior run's per-ticket judgements for items that changed; do not invent priorities for items you could not read.
- Do not read or depend on other skills at runtime.
