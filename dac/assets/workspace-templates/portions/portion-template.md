---
artifact: portion
workstream: {{WORKSTREAM_ID}}
portion_id: {{PORTION_ID}}
stage: portions
status: proposed
last_updated: {{NOW}}
inputs: 01-mission.md,03-decisions.md,04-portion-plan.md,06-integration-plan.md
depends_on: {{DEPENDS_ON}}
executor: {{EXECUTOR}}
jira: {{PORTION_JIRA}}
spec_directory: {{SPEC_DIRECTORY}}
---

<!-- Template note: symbols are examples from references/visual-language.md.
     Always read visual-language.md and use its current assignments. -->

# {{PORTION_ID}}: {{PORTION_TITLE}}

## 💭 Outcome and boundaries

- Outcome:
- Included:
- Excluded:
- Parent criteria:
- Jira: {{PORTION_JIRA}}

## 🔗 Dependency contract

- Required predecessors: {{DEPENDS_ON}}
- Inputs and versions:
- Outputs promised to downstream portions:
- Compatibility obligations:

## ⚖️ Decisions

- Locked parent decisions:
- Decisions delegated locally:
- Assumptions permitted:
- Escalation conditions:

## 🧭 Execution route

- Executor: {{EXECUTOR}}
- Routing rationale:
- Spec directory: {{SPEC_DIRECTORY}}
- Base branch and commit:
- Isolation or worktree:

## 🟰 Change and authority envelope

- Expected files, components, or systems:
- Explicit exclusions:
- W1 scope:
- Proposed C3 scope:
- V2 validation scope:
- R4 actions reserved for coordinator:

## 📋 Acceptance and validation

| Criterion | Parent source | Proof required | Status |
|---|---|---|---|
| To determine | M-001/Jira/DEC-001 | test, review, or deliverable | not_started |

## ⚠️ Test, rollout, and rollback obligations

- Tests and test data:
- Failure cases:
- Observability:
- Rollout:
- Rollback:

## 🎬 Handoff record

- Parent revision:
- Jira last verified:
- Repository last verified:
- Dispatched to:
- Dispatched at:

## Approval record

| Timestamp | Approver | Scope | Notes |
|---|---|---|---|
<!-- APPROVAL_LOG -->

## State log

| Timestamp | Previous | New | Actor | Evidence or reason |
|---|---|---|---|---|
<!-- STATE_LOG -->
