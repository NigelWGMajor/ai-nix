---
artifact: integration-plan
workstream: {{WORKSTREAM_ID}}
stage: integration-plan
status: not_started
last_updated: {{NOW}}
inputs: 03-decisions.md,04-portion-plan.md,05-jira-plan.md
---

<!-- Template note: symbols are examples from references/visual-language.md.
     Always read visual-language.md and use its current assignments. -->

# {{WORKSTREAM_ID}} — PR and Integration Plan

## 💭 Strategy

- Plan classification: full / trivial
- Target branch:
- Contract-first ordering:
- Worktree or branch isolation:
- Compatibility window:

<!-- For a parent-only Jira strategy, use a trivial plan: one branch from main, one PR to main,
     parent-ticket traceability, required validation, and rollout/rollback. Do not omit this artifact. -->

## 🔗 Portion integration

| Portion | Jira | Base | Depends on | PR | Tests | Merge order | Status |
|---|---|---|---|---|---|---|---|
| P-001 | - | target branch | - | planned | To determine | 1 | proposed |

## Integration graph

```text
P-001 / PR-001
  -> P-002 / PR-002
```

## 📋 End-to-end verification

| Parent criterion or risk | Verification | Required portions | Owner |
|---|---|---|---|
| M-001 | To determine | P-001 | - |

## ⚠️ Rollout and rollback

- Deployment order:
- Flags, configuration, schema, or migration:
- Monitoring and success signals:
- Rollback trigger and method:
- Data recovery limitations:

## Remote boundary

Approval of this artifact does not authorize branches, commits, pushes, PRs, merges, deployments, or Jira changes.

## Approval record

| Timestamp | Approver | Scope | Notes |
|---|---|---|---|
<!-- APPROVAL_LOG -->
