# ⏱️ NOW recent-activity triage

| Capability           | Support | Alternative |
| -------------------- | ------- | ----------- |
| Workspace-aware      | ❌      | nix         |
| Repo-aware           | ❌      | wiz         |
| Jira-aware           | ✔️      |             |
| Layered              | ❌      |             |
| Distilled            | ✔️      |             |
| Stateful             | ✔️      |             |
| Safe output folder   | ✔️      |             |
| Needs write approval | ✔️      |             |

| Compatible skills |             |
| ----------------- | ----------- |
| Preprocessors     | —           |
| Postprocessors    | act, pix    |

## What it does

NOW triages the team's recent Jira and GitHub activity (default window 3 weeks) into a prioritized `triage.csv` and a `Findings.md`, then compares them with last week and the week before. It is read-only against Jira and GitHub and writes only to the output base (`TOOLING_OUTPUT_PATH`, otherwise `C:\.data\now`). Team, scope, handles and roadmap epics come from `now/config.md`.

Output lives in `<output-base>\triage\`: `current` (this week), `last-week`, `prior-week`, `previous-run`, and `history.csv` (one row per finished week). Each slot holds `triage.csv` (one row per Jira issue or PR, priority `P|B-1..4`, `needs_nick` flag), `comparison-last-week.csv` and `comparison-prior-week.csv` where baselines exist, `Findings.md`, `00-control.md`, and an interactive dashboard (`index.html` with `data.js` and `data.json`, opens from `file://`, with a "Compare with" menu). Not for single-ticket investigation or code review.

Run it as often as needed: each run replaces `current`. On the first run of a new week (Monday by default) `current` becomes `last-week`, `last-week` becomes `prior-week`, and a new `current` starts, so you can see week-to-week progress and, over a two-week sprint, progress since the week before last. Nothing rolls until a run finishes, so a failed run changes nothing. Usage: `/now [window] [notes]`, for example `/now 3w`.
