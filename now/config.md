# NOW configuration

Seeded from the 2026-10-13 triage (`nix-26-10-13-a-recent-triage`). Edit this file to change who and what NOW covers; the skill reads it on every run.

## Team

| Person | Role | GitHub | Notes |
|---|---|---|---|
| Nick Major | You | `NigelWGMajor` | Items they own set `needs_nick = Y` |
| Alex Ribeiro | Core | `alexr-degreed` | |
| Vedant Koditkar | Core | `KoditkarVedant` | |
| Ryan Haber | Core | unknown | PRs only found when the title names an in-scope PD key |
| Tim Scott | Frontend | unknown | Same limitation |
| Sheldon Nathan | Adjacent | `sheldon-degreed` | Covered for comments on team work and for their own PRs |

## Scope

- **Jira, in pod:** Pod 12 issues (`customfield_11300`) updated since the window start.
- **Jira, outside pod:** issues owned or reported by a core-team member (Nick, Alex, Vedant, Ryan, Tim) updated since the window start, plus any ticket named by an in-scope PR.
- **PRs:** `degreed/Degreed` and `degreed/fe-workspace`. Include PRs by the GitHub handles above, and any PR whose title or branch names an in-scope PD key. Read-only `gh`.
- Jira cloudId: `151636d7-9099-4803-a108-4f053f36c9fe`.

## Roadmap epics (the P track)

Epics are inferred from the team, not listed here. An item is `P-x` when its parent chain (up to 5 levels) reaches an Epic or Initiative that is assigned to or reported by a team member above, or that is in Pod 12. Everything else is `B-x`.

For reference, the 2026-10-13 run found PD-112369 (Nick's epic), PD-129388 (ReBAC, Ryan) and PD-112104 (initiative). Treat these as an expected result to sanity-check against, not an input.

## Priority numbers

1 = act today, 2 = this week, 3 = this sprint, 4 = FYI or acknowledge.

Background (`B`) work becomes `B-1` only with a customer, support, or blocking-dependency deadline.
