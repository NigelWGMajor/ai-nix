# KIT output contract

Use this contract to produce a professional, evidence-backed project-recovery report. The report must re-educate a reader quickly while preserving enough precision to resume safely.

## Contents

- [KIT output contract](#kit-output-contract)
  - [Contents](#contents)
  - [Reader contract](#reader-contract)
  - [Output spine](#output-spine)
  - [Progress and traceability](#progress-and-traceability)
  - [Findings and decisions](#findings-and-decisions)
    - [Severity](#severity)
    - [Confidence](#confidence)
    - [Evidence class](#evidence-class)
  - [Resume comparison](#resume-comparison)
  - [Validation](#validation)
  - [Next steps](#next-steps)
  - [Evidence index](#evidence-index)
  - [Quality gate](#quality-gate)

## Reader contract

State the shared reader contract near the beginning:

- Purpose or recovery question.
- Audience and intended use.
- Scope and exclusions.
- Evidence boundary.
- Status and freshness.
- Material limitations that affect the whole report.

Also state the KIT-specific identity:

- Repository, branch, exact HEAD, review time, feature directory, and review mode.
- Intended base and merge base, or that either remains unresolved.
- Whether the worktree is clean, staged, unstaged, or contains untracked work.
- Whether remote state was refreshed; default to “not refreshed” unless observed otherwise.
- Previous KIT instance in Resume mode.

The first page or screen should answer:

1. What is this project trying to accomplish?
2. Where is it in the Spec Kit lifecycle?
3. What is genuinely complete?
4. What is in progress, blocked, stale, or unknown?
5. What could invalidate the current understanding?
6. What is the safest next action?

## Output spine

Use the shared output spine from `documentation-standard.md` with these KIT sections:

1. **Title and reader contract**: shared contract plus review mode and prior instance.
2. **Orientation**: project purpose, current position, dominant uncertainty, and safest next action.
3. **At a glance**: repository identity, lifecycle, worktree, implementation, validation, integration, uncertainty, and next action.
4. **Content map**: include when the report has more than three substantial reading paths.
5. **Foundations**: problem, users, outcomes, scope, architecture, decisions, and vocabulary.
6. **Relationships and evidence**: lifecycle, progress, traceability, coverage gaps, and Resume delta when applicable.
7. **Findings and decisions**: contradictions, risks, strengths, open decisions, and external blockers.
8. **Validation**: what was checked, against which state, and with what result.
9. **Next steps**: ordered, dependency-aware actions and stopping conditions.
10. **Evidence index**: source artifacts, code areas, commands, and external read-only context used.

Do not bury a dirty worktree, ambiguous base, failed validation, or high-confidence contradiction below implementation detail.

## Progress and traceability

Use these status labels consistently:

| Status | Meaning |
| --- | --- |
| Verified complete | Appropriate implementation and validation evidence satisfy the intended outcome. |
| Implemented, validation incomplete | Implementation exists, but acceptance evidence is missing or insufficient. |
| In progress | Coherent partial implementation or active uncommitted work exists. |
| Claimed only | A tracking artifact asserts completion without corroborating implementation evidence. |
| Not started | Planned work has no material implementation evidence. |
| Blocked | A named dependency or external condition prevents progress. |
| Contradicted or stale | Source artifacts and current evidence materially disagree. |
| Unknown | Evidence is missing, inaccessible, ambiguous, or outside the approved scope. |

For each material story, requirement, phase, or task group, show:

- Stable requirement or story identifier when available.
- Intended outcome.
- Design and task coverage.
- Implementation evidence with paths or symbols.
- Validation evidence and exact result.
- Status, evidence class, and confidence.
- Remaining work or decision.

Prefer separate compact tables by story or phase over one unreadably wide matrix. Link to detailed evidence instead of duplicating large diffs or logs.

## Findings and decisions

Assign stable IDs such as `KIT-001`. Each finding must contain:

- Concise title.
- Severity.
- Confidence.
- Evidence class.
- Observed evidence with precise locations.
- Why it matters to completion, correctness, resumption, integration, or delivery.
- Concrete next step.

### Severity

| Severity | Meaning |
| --- | --- |
| Critical | Continuing could cause severe loss, corruption, security exposure, or a fundamentally invalid implementation direction. |
| High | A material requirement, integration boundary, or recovery assumption is wrong or unproven and likely blocks responsible completion. |
| Medium | A meaningful gap, inconsistency, or validation weakness should be addressed but does not invalidate the whole effort. |
| Low | A bounded maintainability, clarity, or process weakness with limited immediate impact. |
| Note | Useful observation, strength, or improvement idea that is not a defect. |

### Confidence

| Confidence | Meaning |
| --- | --- |
| High | Direct, consistent evidence strongly supports the conclusion. |
| Medium | Evidence supports the conclusion but has a material gap or interpretive step. |
| Low | The concern is plausible but evidence is incomplete, stale, or ambiguous. |

### Evidence class

- **Observed**: directly present in inspected artifacts, Git state, code, or command output.
- **Claimed**: asserted by a task, commit, PR, or narrative source.
- **Inferred**: derived from observed facts; state the reasoning.
- **Unknown**: not available or not responsibly derivable.

Do not inflate severity because confidence is low, or lower severity merely because evidence is incomplete. State both dimensions.

Include strengths that reduce recovery risk, such as clean story boundaries, accurate tasks, focused tests, reversible design decisions, or a well-contained dirty worktree. Keep unresolved decisions and external blockers in this section so the action plan does not conceal its prerequisites.

## Source identifiers and shorthand

  When sources use opaque identifiers (work item IDs like F1/E2, requirement codes like REQ-PM-001,
  phase numbers, or internal acronyms) and those identifiers appear in the synthesis:

  1. **Define before use.** Provide a reference table that maps each identifier to its full description
     before using it in running text. Place this table in Foundations or at the start of the section
     that introduces the identifiers.
  2. **Link to origin.** Each identifier's first definition must include a relative link to the
     source location where it is defined (heading, line, or section).
  3. **Stand-alone readability.** A reader encountering any identifier in the document must be able
     to resolve its meaning without leaving the document. The reference table satisfies this;
     bare identifiers in prose without a prior definition do not.
  4. **Derivative documents.** When a derivative artifact (Actions, slideshow, handoff) uses
     identifiers from the parent Findings, it must include a header note linking back to the
     parent's reference table and to the original source.

## Resume comparison

In Resume mode, include a delta from the prior KIT instance:

| Dimension                     | Previous snapshot | Current evidence | Meaning |
| ----------------------------- | ----------------- | ---------------- | ------- |
| Repository/branch             |                   |                  |         |
| HEAD/base/merge base          |                   |                  |         |
| Worktree state                |                   |                  |         |
| Spec Kit artifacts and hashes |                   |                  |         |
| Requirements or scope         |                   |                  |         |
| Implementation progress       |                   |                  |         |
| Validation                    |                   |                  |         |
| Findings and blockers         |                   |                  |         |
| Recommended next action       |                   |                  |         |

Distinguish observed change from an inability to compare. If the current repository or feature does not match the prior snapshot, stop rather than manufacture a delta.

Do not rewrite the historical KIT instance. Create a new instance and link the previous one.

## Validation

For every executed command or manual check, record:

- Timestamp.
- Exact command or procedure.
- Purpose and mapped requirement/risk.
- HEAD and whether uncommitted changes were present.
- Environment and prerequisites.
- Exit result and concise outcome.
- New worktree artifacts or state changes.
- Limitations.

Group validation outcomes as Passed, Failed, Partial, Blocked, or Not run. Never turn “command unavailable,” “database unavailable,” “tests not selected,” or “existing log claims green” into a pass.

## Next steps

Provide a dependency-aware sequence, normally three to seven actions. For each action include:

- Desired outcome.
- Why it comes next.
- Prerequisite or unresolved decision.
- Target files, component, task IDs, or requirement IDs.
- Suggested validation.
- Stopping condition or checkpoint.

Make the first action executable without rereading the entire report. If a decision blocks implementation, make decision resolution the first action rather than proposing speculative code.

Separate:

- Safe next action.
- Work that requires user choice.
- Work that requires external coordination or access.
- Work that requires Git, Spec Kit, Jira, PR, or remote mutation approval.

## Evidence index

Include a compact index of every material source that shaped the report:

| ID   | Source                                                      | Role                | Snapshot or freshness limitation          |
| ---- | ----------------------------------------------------------- | ------------------- | ----------------------------------------- |
| E001 | Artifact, code area, Git command, test output, PR, or issue | What it establishes | Time, commit, access, or confidence limit |

Prefer precise links in the body. Use the index for audit and navigation rather than duplicating large evidence excerpts.

## Visual presentation

Read `visual-language.md` before adding symbols. Use only its defined roles and never make a symbol the sole carrier of meaning. The visual-language reference is authoritative; its current symbol assignments override any symbols appearing in templates or examples elsewhere in this package.

## Quality gate

- [ ] Repository, branch, HEAD, worktree, feature, and base facts were freshly resolved.
- [ ] Purpose, audience/use, scope, evidence boundary, status/freshness, and material limitations are visible near the beginning.
- [ ] The shared output spine is present, with optional sections omitted only when they add no value.
- [ ] Remote-freshness limits are explicit.
- [ ] Applicable repository guidance and Spec Kit customization were inspected.
- [ ] Intent, scope, stories, requirements, design, tasks, implementation, validation, and integration were reconciled.
- [ ] Task checkboxes were treated as claims until corroborated.
- [ ] Every material requirement or story has a status and evidence trail, or an explicit unknown.
- [ ] Dirty, staged, unstaged, untracked, detached, local-only, and ambiguous-base risks are visible where applicable.
- [ ] Findings separate severity, confidence, and evidence class.
- [ ] Facts, claims, inference, and unknowns are not misleadingly blended.
- [ ] Missing optional artifacts were not mislabeled as defects.
- [ ] Validation is tied to the exact reviewed state; omissions and generated artifacts are disclosed.
- [ ] Resume mode compares against, but does not overwrite, the prior snapshot.
- [ ] Symbols come from the configured `visual-language.md` palette and remain restrained.
- [ ] Strengths and sound implementation decisions are recorded.
- [ ] The `Next steps` plan is ordered, bounded, and immediately actionable.
- [ ] No source, Git, Spec Kit, issue, PR, or remote mutation occurred without explicit authorization.
- [ ] `00-control.md` contains the next safe action and sufficient state for another session.
- [ ] Source-originated identifiers (work item IDs, requirement codes, phase numbers) are defined in a reference table before first use, with links to their source location.
- [ ] Derivative artifacts link back to the parent document's identifier definitions.