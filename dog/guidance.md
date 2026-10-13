# 🐕 DOG Degreed in Datadog

| Capability           | Support | Alternative |
| -------------------- | ------- | ----------- |
| Workspace-aware      | ❌      | nix         |
| Repo-aware           | ❌      | wiz         |
| Jira-aware           | ❌      | now         |
| Layered              | ❌      |             |
| Distilled            | ✔️      |             |
| Stateful             | ❌      |             |
| Safe output folder   | ❌      |             |
| Needs write approval | ❌      |             |

| Compatible skills |             |
| ----------------- | ----------- |
| Preprocessors     | —           |
| Postprocessors    | fix, act    |

## What it does

DOG carries the Degreed-specific conventions for querying Datadog application logs and custom metrics (environments, `source` components, `@seid` service environments) so runtime questions in staging, beta, or production can be answered accurately. Use it for "is this happening in prod?", "did my change take effect?", and "why is X failing in staging?". It also covers confirming a commit has deployed to staging (top-of-hour pipeline, `az` CLI) and verifying a fix across all `source` components. For customer questions it asks which region first, and it cannot query the `org_directory` / `service_environments` reference tables, so it asks you to look up the `seid`. Scope: application logs and custom metrics only, not traces or infrastructure. It is read-only and creates no files.
