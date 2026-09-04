# DAC Portion Necessity, Reuse, and Security Review

## Purpose

Prevent a proposed portion from creating duplicate services, classes, abstractions, workflows, or security mechanisms when the codebase already has a suitable capability or established way to extend one. The review is deliberately performed before Jira allocation and executor handoff, when changing course is inexpensive.

This is not a request to preserve an existing design at all costs. It distinguishes a justified new capability from speculative or redundant implementation, and makes the rationale reviewable.

## When to use this standard

Complete the review for every active proposed portion after drafting `04-portion-plan.md` and before its content approval. Repeat it when evidence, a parent decision, or the proposed portion boundary changes materially.

Use this standard with repository-local architecture, ownership, authorization, security, database, and testing guidance. More specific repository or team rules take precedence.

## Evidence discovery

For each portion:

1. State the parent mission criterion and the observable outcome the portion must contribute.
2. Inspect the repository's local guidance and the relevant code, tests, contracts, configuration, and history.
3. Use the Codebase Knowledge Graph for structural discovery of relevant symbols, callers, consumers, and extension points; verify material graph findings against the checked-out source.
4. Record the existing capability, its symbol or path, and the evidence that it is or is not suitable.
5. Identify the established methodology that governs the change, such as an existing service pattern, repository, migration framework, authorization path, API convention, or test approach.
6. Identify the existing authorization and security boundary, including the enforcement point, caller or principal context, failure behavior, and relevant tests. Do not design a parallel path or bypass without an explicit parent decision and evidence-based justification.

Text search is appropriate for literals, configuration, documentation, and gaps in graph coverage. Do not infer an implementation or security boundary from names or folder proximity alone.

## Required per-portion record

The **Portion necessity, reuse, and security review** table in `04-portion-plan.md` must contain one row for every active proposed portion.

| Field | Required content |
|---|---|
| Mission criterion | The parent criterion the portion covers. |
| Existing capability or extension point inspected | Exact service, class, module, query, API, schema object, test helper, or `none found after inspection`. |
| Intended action | `reuse`, `extend`, `new`, `discovery`, or `remove/defer`. |
| Established methodology or pattern | The concrete local approach the change will follow. |
| Authorization/security approach | Existing enforcement point, principal context, failure behavior, and required test evidence; or an explicit parent decision for a justified change. |
| Evidence | Repository-relative paths, symbols, tests, documentation, or other observed sources. |
| Necessity rationale | Why the selected action is the smallest path that satisfies the criterion. |
| Gate status | `ready`, `revise`, `discovery`, `decision`, or `remove/defer`. |

## Decision rules

### Reuse or extend

Choose `reuse` or `extend` when an existing capability can satisfy the required outcome without violating its contract, ownership boundary, or authorization/security protocol. Name the extension point and preserve its established patterns, tests, failure behavior, and compatibility obligations.

### New capability

Choose `new` only when the review shows that existing capabilities and approved extension points cannot meet the requirement. The rationale must name what was inspected and why reuse or extension is insufficient. It must also name the new capability's owner, coherent responsibility, contract boundary, the local pattern it will follow, and how it participates in established authorization and security controls.

Do not justify a new service, class, or security mechanism solely by a desire for cleaner partitioning, a convenient name, anticipated future flexibility, or an unverified assumption about the current codebase.

### Discovery or revise

Choose `discovery` or `revise` when the relevant code, contract, owner, established methodology, or authorization/security boundary is unknown, inaccessible, or contradictory. Choose `decision` when evidence supports multiple reasonable paths with a material tradeoff. The portion must not become an implementation handoff until the missing evidence is resolved or a parent decision explicitly accepts the risk.

### Automatic planning corrections

With W1 authority, DAC must automatically correct a flagrant planning defect when direct repository evidence establishes the correction and it does not change an approved mission criterion, non-goal, or parent decision. Examples include replacing a duplicate net-new service with the evidenced extension point, removing a portion whose outcome is already fully covered, or recording the existing authorization/security protocol that the portion must use.

Record the evidence, before-and-after action, and affected portion in `04-portion-plan.md` and the control change log. Do not silently change source, tests, Jira, branches, remote state, or an approved parent decision.

### Decision required

Ask the user one consequential question before progressing when the evidence leaves multiple reasonable paths or a material tradeoff. This includes competing extension points, unclear ownership, incompatible consumers, uncertain migration or rollout effects, ambiguous authorization behavior, or a choice to deliberately diverge from established methodology. Record the alternatives, evidence, and the needed decision; do not promote the portion to an implementation handoff while the decision remains open.

### Remove or defer

Choose `remove/defer` when the portion does not make a demonstrated contribution to a mission criterion, duplicates a capability without a justified divergence, bypasses established security protocol, or represents optional improvement rather than required scope. Record any future trigger that would make reconsideration appropriate.

## Gate exit criteria

`04-portion-plan.md` may be approved only when every active proposed portion has a `ready` review status and the table contains evidence sufficient for a reviewer to locate the capability, methodology, and security approach relied upon. The coordinator must:

- revise portions that duplicate existing capability, use an unsupported abstraction, or bypass an established authorization/security path;
- automatically correct flagrant, evidence-proven planning defects under W1 authority and record the correction;
- route unresolved facts to a bounded `discovery` outcome or a parent decision; and
- ask the user one consequential question for material ambiguity rather than silently selecting a path;
- keep the existing capability's owner, security obligations, and compatibility obligations visible in the portion envelope; and
- keep net-new capability as the exception that is explained, not the default that is assumed.

This gate is evidence and planning only. It neither authorizes implementation nor replaces code review, testing, security review, or integration validation.

