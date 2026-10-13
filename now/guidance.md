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

NOW triages the team's recent Jira and GitHub activity (default window 2 weeks) into a prioritized `triage.csv` and a `Findings.md`, then compares them with the prior triage. It is read-only against Jira and GitHub and writes only to the output base (`TOOLING_OUTPUT_PATH`, otherwise `C:\.data\now`). Team, scope, handles and roadmap epics come from `now/config.md`.

Output per instance (`now-YY-MM-DD-<suffix>`): `triage.csv` (one row per Jira issue or PR, priority `P|B-1..4`, `needs_nick` flag), `comparison.csv` (when a prior exists), `Findings.md`, and `00-control.md`. Not for single-ticket investigation or code review.

A result set less than one window old is overwritten (re-dated); an older one becomes the prior for comparison. Usage: `/now [window] [notes]`, for example `/now 3w`.
