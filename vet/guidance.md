# 🩺 VET branch readiness review

| Capability | Support | Alternative |
| --- | --- | --- |
| Branch-aware | ✔️ | wiz |
| PR and Jira comment-aware | ✔️ | wiz |
| Critical comment dispositions | ✔️ | cop |
| Cross-repository evidence | ✔️ | nix |
| Resumable action queue | ✔️ | act |
| Safe output folder | ✔️ | |
| Needs write approval | ✔️ | |

## What it does

VET checks whether the current Git branch addresses its requirements and every active PR or related-ticket comment. It treats direct code as the WIP source of truth, verifies complementary frontend/backend evidence when relevant, and produces a resumable review with comment dispositions, response drafts, and dependency-ordered corrective or restorative actions.

**Use `/vet`** when a branch has a pull request or Jira discussion and you need a rigorous readiness assessment before deciding what to change or reply to.

**Typical route:** `/map -> /vet -> /act`

- `/map` is useful first when the branch or workspace needs orientation.
- `/vet` is the focused readiness and comment-response review.
- `/act` can turn an approved VET action queue into a ticket, handoff, or concise update.

VET stays read-only until you explicitly authorize selected `A-###` corrective/restorative actions or `R-###` remote responses.
