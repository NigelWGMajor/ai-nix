---
artifact: portion-plan
workstream: {{WORKSTREAM_ID}}
stage: partition
status: not_started
last_updated: {{NOW}}
inputs: 01-mission.md,02-evidence.md,03-decisions.md
---

<!-- Template note: symbols are examples from references/visual-language.md.
     Always read visual-language.md and use its current assignments. -->

# {{WORKSTREAM_LABEL}} — Portion and Dependency Plan

## 💭 Partition strategy

- Boundary principle:
- Shared contracts:
- Critical path:
- Safe parallel lanes:

## 🔗 Portions

| Portion | Outcome | Covers | Depends on | Points | Sizing rationale or split review | Executor candidate | Change surface | Status |
|---|---|---|---|---|---|---|---|---|
| P-001 | To determine | M-001 | - | unestimated | Estimate before Jira allocation; justify any 8+ portion | speckit/direct/skill/discovery/human | To determine | proposed |

## 🧭 Portion necessity, reuse, and security review

Complete this review for every active proposed portion before approving this plan. Read the DAC skill's `references/portion-sanity-review.md`.

| Portion | Mission criterion | Existing capability or extension point inspected | Intended action | Established methodology or pattern | Authorization/security approach | Evidence | Necessity rationale | Gate status |
|---|---|---|---|---|---|---|---|---|
| P-001 | M-001 | To determine | reuse/extend/new/discovery/remove-defer | To determine | To determine | To determine | To determine | revise |

## Dependency graph

```text
P-001
  -> P-002
```

## 🟰 Coverage

| Mission criterion | Portion or integration check | Gap |
|---|---|---|
| M-001 | P-001 | none/to determine |

## Parallelization and conflict analysis

| Lane | Portions | Why safe | Shared files or state | Coordination point |
|---|---|---|---|---|
| A | To determine | - | - | - |

## ⚠️ Rejected partitions

Record layer-based, overly coupled, too-small, or unsafe alternatives and why they were rejected.

## Approval record

| Timestamp | Approver | Scope | Notes |
|---|---|---|---|
<!-- APPROVAL_LOG -->
