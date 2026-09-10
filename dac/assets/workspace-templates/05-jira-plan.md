---
artifact: jira-plan
workstream: {{WORKSTREAM_ID}}
stage: jira
status: not_started
last_updated: {{NOW}}
inputs: 01-mission.md,03-decisions.md,04-portion-plan.md
---

<!-- Template note: symbols are examples from references/visual-language.md.
     Always read visual-language.md and use its current assignments. -->

# {{WORKSTREAM_LABEL}} — Jira Visibility Plan

<!-- In an Epic-rooted preview, replace these placeholders with the complete observed recursive
     hierarchy before the allocation strategy. Every nested master Story with a local
     .dac/<ticket-key>/00-control.md workspace must appear in both trees and link to its detail
     heading below. Preserve unknowns, inaccessible workspaces, repeated references, and cycles
     explicitly; do not infer Jira relationships from a folder name alone. -->
## DAC portion hierarchy
```text
{{WORKSTREAM_ID}} — parent outcome
└── To determine from observed Jira and DAC workspace evidence
```
## Jira ticket hierarchy
```text
{{WORKSTREAM_ID}} — parent outcome
└── To determine from observed Jira evidence
```
## Master Story details
<!-- One block per discovered nested master Story, in hierarchy order. Use an explicit anchor
     immediately before the H3 heading as the target of both tree links, e.g.:
     <a id="pd-123457-search-foundation"></a>
     ### PD-123457 — Search foundation
     - Parent: PD-123456
     - Local workspace: `.dac/PD-123457/`
     - Portions: P-001 (complete), P-002 (planned)
     - Jira descendants: PD-123458
     - Dependencies: …
     - Evidence gaps or conflicts: … -->
No nested master Story discovered yet.
## Allocation strategy

<!-- Preview may record a non-binding review. Final strategy: none | per-portion | suggested-grouping | custom -->
**Strategy:** To determine
**Rationale:** To determine

**Review state:** not_started / proposed / awaiting_confirmation / confirmed

<!-- In preview, persist the proposed table and reuse it on resumption. Regenerate only after a
     user-requested repartition/grouping change or material evidence drift. SQL, FE, and BE must
     remain separate; lettered Suggested Grouping values may join only same-discipline portions.
     Use Fibonacci points. Carry a single portion's points to its ticket; for a grouping, total
     constituent portions and round up to the next Fibonacci value. Explain every 8+ split signal. -->

## 🔗 Hierarchy

| Portion | Proposed Jira Issue | Portion Points | Ticket Points | Type | Master | Dependencies | Status | Description | Suggested Grouping |
|---|---|---|---|---|---|---|---|---|---|
| P-001 | New Story | unestimated | unestimated | Story | {{WORKSTREAM_ID}} | - | proposed | To determine | — |

## Story-point field

- Field ID or name: To determine through Jira field discovery
- Ticket-point source: Portion estimate / grouped-total rounded up to Fibonacci
- 8+ sizing review: To determine

## 🎬 Proposed remote actions

| Action | Target | Exact fields or links | Expected result | R4 approval |
|---|---|---|---|---|
| To determine | - | - | - | required |

## ✔️ Executed actions and read-back

| Timestamp | Actor | Action | Result | Verified state |
|---|---|---|---|---|
| - | - | None | - | - |

## Management reporting

- Parent status meaning:
- Child status mapping:
- Blocker visibility:
- PR and release links:

## Approval record

| Timestamp | Approver | Scope | Notes |
|---|---|---|---|
<!-- APPROVAL_LOG -->
