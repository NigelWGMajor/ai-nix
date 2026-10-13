---
name: now
description: Triage the team's recent Jira and GitHub activity (default window 3 weeks) into a prioritized CSV, a Findings.md and an interactive HTML dashboard, kept as a rolling weekly record (this week, last week, the week before) and compared with the two earlier weeks. Use when the user invokes now, or asks what needs attention across Pod 12 and core-team work since a date or over the last N weeks. Do not use for single-ticket investigation (use dg-jira-investigate) or code review. Read-only against Jira and GitHub; writes only to the output base.
---

# NOW: recent-activity triage with weekly baselines

> **Quick help:** if invoked with `?` as the only parameter, summarize the usage below and stop.

Usage: `/now [window] [notes]`. `window` is a duration such as `3w`, `21d`, `4w` (default `3w` = 21 days). Anything else is a note that narrows or steers the triage. Run it as often as you like: each run replaces this week's triage, and the earlier weeks stay as baselines.

Team, scope, GitHub handles and the roadmap-epic list live in [config.md](config.md). Read it first and follow it; if the user corrects something, update the file.

## 1. Decide where results go

The record lives in `<output-base>/triage/`:
| Folder | Holds |
|---|---|
| `current/` | This week's triage, replaced by each run |
| `last-week/`, `prior-week/` | The final state of the previous week and the week before; the baselines |
| `previous-run/` | `current` as it was before the last replacement ("since my last run") |
| `history.csv` | One row per finished week (counts and hours), so trends outlive the three slots |
| `.next/` | The run in progress; it becomes `current` only at `commit` |
Weeks start on the roll day (config.md, default Monday); weekend runs belong to the week that is ending. Files are matched to weeks by the `Week start` line in their `00-control.md`, not by folder name, so a skipped week leaves a gap rather than mislabelled data.
Run:

```text
python <skill-dir>/scripts/now_run.py plan --window-days <N> [--roll-day <mon..sun>]
```

It prints JSON:

- `mode`: `refresh` (this week already has a `current`; this run replaces it) or `new-week` (the first run of a new week; `commit` will roll the slots).
- `baselines`: `last-week` and `prior-week`, each with a `path`, or null. These are resolved by week, so they are right even before the roll has happened. `gaps` lists missing ones.
- `week_start`, `window_start`, `next` (the work folder), `previous_run_source` (set on a refresh).
- `min_window_days` and `window_ok`: comparing with the prior week needs a window that reaches back to the start of that week. If `window_ok` is false, widen the window (otherwise items that merely aged out show as `dropped`) or warn the user.
- `recovered`: what was put back after an interrupted commit; mention it if non-empty. `error` is non-null if a slot is dated after this week; stop and report it.

Tell the user the mode, the week, and which baselines exist (and which are missing) before writing anything. If there is no baseline, say there is nothing to compare against. Then run `begin`, which prepares an empty `.next` (discarding leftovers from a run that stopped early) and prints its path. Nothing is rolled or replaced until `commit`, so a run that stops (for example Jira needs re-authentication) leaves the record untouched.



## 2. Gather (read-only)

Window start is `window_start` from the plan. Do not mutate Jira, GitHub, Git state, or the repo.

1. **Jira** via `mcp__plugin_jira-integration_atlassian__*` (load with ToolSearch). Two JQL searches, with comments and issuelinks expanded:
   - Pod 12: `cf[11300] = "<Pod 12 team id>"` (see config.md) and `updated >= <window_start>`. The field is a Team: matching on the name ("Pod 12", `~` or `=`) returns nothing.
   - Outside pod: owned or reported by a core-team member, `updated >= <window_start>`, minus what the first search returned.
   - Add tickets named by in-scope PRs that neither search found.
   If Jira is unreachable, present the OAuth URL and stop (see memory: Jira authentication workflow).
2. **GitHub** with read-only `gh pr list/view` against `degreed/Degreed` and `degreed/fe-workspace`: PRs by each known handle and PRs whose title or branch names an in-scope PD key. Capture state, draft, review decision, mergeable state, CI status, reviewers, updated date. Include PRs merged or closed within the window. Keep the mergeable state: write it into `pr_state` as `mergeable:CONFLICTING` (or `MERGEABLE`) so the dashboard's conflicts lane works.
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
| `pr_state` | For PRs: `<state>/<draft or ready>/ci:<pass or FAILING or mixed>/mergeable:<MERGEABLE or CONFLICTING>`. For tickets: the states of related PRs |

Judgement guidance:
- Priority 1 means something is blocked on Nick, a customer or support deadline exists, a PR stalls on conflicts/failing CI/no reviewer, or a review requested changes.
- Closed or resolved items with no open question are 4. Open items with no activity needing a decision are 3.
- A merged PR whose ticket is still open, or a ticket whose fix PR merged, is `verify-close`.
- Cross-check PRs against their tickets: a ticket status that disagrees with its PR is itself a finding.

**Reuse earlier judgement.** Read the `triage.csv` of the file this run replaces (`previous_run_source`, on a refresh) or else the `last-week` baseline. For an item whose `status`, `last_updated` and `pr_state` are unchanged, carry forward its priority, action and reasoning unless new evidence says otherwise. Re-triage items that changed. This keeps the comparison meaningful: a priority change should reflect a real change, not re-rolled judgement.

Write the rows with a short Python script using `csv.DictWriter` and `encoding="utf-8-sig"`, into the `.next` folder. Keep the script out of `.next` and out of the repo.

## 4. Compare

For each baseline in the plan that exists, compare `.next` with it:

```text
now_run.py compare --current <next> --baseline <baseline path> --label last-week
now_run.py compare --current <next> --baseline <baseline path> --label prior-week
```

Each validates both CSVs against the column list, writes `comparison-<label>.csv` into `.next`, and prints a Markdown summary (new, priority-changed, status-changed, review-state-changed, owner-changed, dropped, unchanged, and the delta in hours needing Nick). It states how many weeks apart the two files are and warns when the windows differ. Pass any warning on to the reader: it means some `new` and `dropped` rows are window effects. Read each comparison CSV and interpret it for the reader: the three or four changes that matter most, not the whole table. A `dropped` row is ambiguous (finished, reassigned, or outside the window); check the few that matter before calling them resolved.

`last-week` answers "what moved this week"; `prior-week` answers "what moved over the sprint". Both are measured from the end of those weeks, not from the same weekday. If a baseline is missing, say there is nothing to compare against for it and omit that section.

## 5. Write the run and commit

Files in `.next`:

| File | Content |
|---|---|
| `triage.csv` | The rows from step 3 |
| `comparison-last-week.csv`, `comparison-prior-week.csv` | From step 4, for each baseline that exists |
| `Findings.md` | Reader-facing summary, below |
| `00-control.md` | Control record, below |
| `index.html`, `data.js`, `data.json` | Interactive dashboard, from `render` below |
Once `triage.csv` and `00-control.md` exist, render the dashboard:
```text
now_run.py render --instance <next> --baseline last-week=<path> --baseline prior-week=<path> [--previous-run <previous_run_source>]
```
Pass each baseline that exists, and `--previous-run` on a refresh. It builds `data.json` from `triage.csv`, bundles `data.js`, and copies `templates/dashboard.html` to `index.html`. The page opens from `file://` with no server: summary tiles, a "needs you" queue, PR health lanes, epic roll-ups, filters, a window selector defaulting to the run's window, CSV export, and a **Compare with** menu (last week, prior week, previous run) that recomputes NEW / CHANGED / resolved against the chosen baseline. Each item has one stand-in activity event from `last_updated` and `last_activity`.

`00-control.md` must begin with these lines (the script reads `Run date`, `Week start` and the window):

```markdown
# 00-control

- Run date: YYYY-MM-DD
- Week start: <week_start from the plan>
- Window: YYYY-MM-DD to YYYY-MM-DD (N days)
- Mode: refresh | new-week
- Baselines: last-week <week or missing>; prior-week <week or missing>
- Rows: <count>
```

The `(N days)` text is read by `compare` to check that the two windows match, so keep that form.
Then list the user decisions in force (from config), open assumptions, and the next safe action.

`Findings.md` follows the structure of the 2026-10-13 triage:

1. Title: `Recent triage: <scope>, <window_start> to <today>`, and a link to the CSV with row count.
2. **Answer:** how many P-1 and B-1 items, the hours needing Nick directly, and the two or three places they cluster, each with the concrete blocker. Plain sentences, no jargon. Take every count from `now_run.py summary --instance <next>` rather than counting by hand.
3. **Since last week and since the prior week** (only for baselines that exist): the summary table from each `compare`, then the changes that matter. Say what got better, what got worse, and what is new. Mention `history.csv` trends when it has rows.
4. **Method and assumptions:** a short table (team, Jira scope, PR scope, track, number, estimates). Flag the roadmap-epic list and estimates as judgement.
5. **Limits:** missing handles, comment truncation, staleness of CI and review state (state the date read), related issues missed by owner/reporter matching, uncommitted working-tree changes relevant to an item.
6. **CSV columns:** the table from step 3.
7. **Next step:** one concrete action, naming the first item.

When the files are written, **commit**:
```text
now_run.py commit [--roll-day <mon..sun>]
```
On a refresh it keeps the file being replaced as `previous-run` and swaps `.next` in as `current`. On a new week it records the finished week in `history.csv`, moves `current` to `last-week` and `last-week` to `prior-week` (by week id; a skipped week leaves a gap and anything older than two weeks is dropped), and makes `.next` the new `current`. Commit only after every file above is written and Jira and GitHub were read successfully; if a run stops earlier, do not commit.
Return to the user only a short handoff: the answer, the mode (`refresh` or `new-week`), the path to `current\index.html`, which baselines were used or missing, and the open assumptions that need their correction.

## Guardrails

- Read-only against Jira, GitHub, Git, and the repo. Never transition tickets, comment, or push.
- Write only under the output base (`TOOLING_OUTPUT_PATH`, otherwise `C:\.data\now`), inside `triage/`. The only deletion-like actions are the specified ones: replacing `current` on a refresh, and dropping the slot that ages out on a new week. Announce them first. Never modify `last-week`, `prior-week` or `history.csv` by hand.
- Every run re-gathers from Jira and GitHub; never copy another file's data into a new run.
- Do not copy the baseline's per-ticket judgements for items that changed; do not invent priorities for items you could not read.
- Do not read or depend on other skills at runtime.
