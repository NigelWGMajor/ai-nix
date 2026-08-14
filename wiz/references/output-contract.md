# WIZ output contract

Use this contract for Standard and Deep WIZ reviews. Adapt the exact sections to the target while preserving the six-layer method, evidence integrity, traceable finding chains, and actionable ending.

## Contents

- [Reader contract](#reader-contract)
- [Output spine](#output-spine)
- [Six-layer review method](#six-layer-review-method)
- [Finding identification](#finding-identification)
- [Seriousness and confidence](#seriousness-and-confidence)
- [Evidence and citations](#evidence-and-citations)
- [Visual presentation](#visual-presentation)
- [Evidence index](#evidence-index)
- [Quality gate](#quality-gate)

## Reader contract

State the shared reader contract near the beginning:

- Purpose or review question.
- Audience and intended use.
- Scope: target ticket, PR, or branch and included change states.
- Evidence boundary: what was inspected and what was inaccessible.
- Status and freshness: review timestamp, HEAD, worktree state, remote-refresh status.
- Material limitations that affect the whole review.
- Depth: Quick, Standard, or Deep.

Also state the WIZ-specific identity:

- Repository, branch, exact HEAD.
- Jira ticket, PR URL, or branch target.
- Intended base branch and comparison state.
- Whether the worktree is clean, staged, unstaged, or untracked.

The first page or screen should answer:

1. What is this work trying to accomplish?
2. What is the overall assessment?
3. What are the most serious concerns?
4. What is genuinely well done?
5. What is the safest next action?

## Output spine

Use the shared output spine from `documentation-standard.md` with these WIZ mappings:

| Shared role                | WIZ section                          |
| -------------------------- | ------------------------------------ |
| Title and reader contract  | Title block with full reader contract |
| Orientation                | Intent - scope and orientation       |
| At a glance                | At a glance - findings summary       |
| Foundations                | Intent - scope envelope              |
| Relationships and evidence | Evidence + Discovered relationships  |
| Detailed analysis          | Ideation                             |
| Findings and decisions     | Findings - concerns and strengths    |
| Validation                 | Realization                          |
| Next steps                 | Implementation + follow-ups          |
| Evidence index             | Evidence index                       |

Preserve the shared role in each heading. Use qualified headings such as `Evidence - relationships and evidence` and `Ideation - detailed analysis`. Omit optional sections when they would add no value.

## Six-layer review method

WIZ reviews use six analytical layers. Each layer adds depth; finding IDs chain forward so reasoning is traceable from evidence to action.

### Intent

Establish the scope and contract for the review:

- Intended user or system outcome.
- Acceptance criteria and explicit non-goals.
- Target branch/base and included change states.
- Affected surfaces named by the ticket or diff.
- Material unknowns and inaccessible evidence.
- Ambiguities or conflicts that prevent a confident judgment.

### Evidence

Gather and classify all material observations:

- **Strengths** (G-XX): good decisions, clean boundaries, readable tests, appropriate abstractions, safe handling.
- **Concerns** (F-XX): defects, risks, gaps, or weaknesses with seriousness, confidence, evidence class, and impact.
- **Evidence gaps**: missing or inaccessible evidence and why it matters.

### Discovered relationships

Trace the relationships that affect correctness, security, or completion:

- Callers, consumers, contracts, state, data flow, test coverage, deployment, and issue dependencies.
- Label each extension beyond the immediate diff as **Scope extension** with the evidence-based reason.
- Use relationship IDs (R-XX) and link them to the findings they affect.

### Ideation

Propose directions and alternatives for each concern:

- Link each idea (I-XX) to the finding it addresses (I-01 -> F-01).
- State the recommended direction, viable alternatives, tradeoffs, and confidence.
- Keep optional ideas visibly separate from changes required to meet intent.

### Implementation

Define the smallest concrete change for each recommendation:

- Link each action (A-XX) to the idea it implements (A-01 -> I-01).
- Name likely files, symbols, tests, and compatibility or rollback considerations.
- Do not imply that a recommendation has already been implemented.

### Realization

Assess the overall state:

- Acceptance criteria met, partially met, not met, or unable to verify — with evidence.
- Tests and checks: passed, failed, blocked, or not run — naming what was observed.
- Remaining risks and focused follow-ups.
- Positive summary of what the work already accomplishes well.

## Finding identification

Use stable IDs that chain across layers:

| Layer   | Prefix | Example | Links to        |
| ------- | ------ | ------- | --------------- |
| Strength | G-XX  | G-01    | —               |
| Concern  | F-XX  | F-01    | —               |
| Relationship | R-XX | R-01 | F-XX or G-XX   |
| Idea     | I-XX  | I-01    | F-XX            |
| Action   | A-XX  | A-01    | I-XX            |

Carry IDs forward so a reader can trace from evidence (F-01) through analysis (I-01 -> F-01) to action (A-01 -> I-01). This chain is WIZ's primary depth advantage over NIX.

## Seriousness and confidence

Give each concern both a seriousness level and a confidence level.

### Seriousness

| Level    | Meaning                                                                                               |
| -------- | ----------------------------------------------------------------------------------------------------- |
| Critical | Credible risk of severe security/privacy harm, irreversible data loss, or a release-blocking failure. |
| High     | Likely failure of a core requirement, material regression, or serious operability problem.             |
| Medium   | Meaningful defect or gap that should be addressed but is not release-critical.                         |
| Low      | Bounded improvement with limited immediate impact.                                                    |
| Note     | Question, observation, or optional idea without a demonstrated defect.                                |

### Confidence

| Level  | Meaning                                                                |
| ------ | ---------------------------------------------------------------------- |
| High   | Directly supported by current code, contract, or observed behavior.    |
| Medium | Supported by multiple clues but missing one verification step.         |
| Low    | Plausible and worth checking, with important evidence missing.         |

Do not inflate seriousness to make a review look useful. Present low-confidence concerns as validation questions, not facts. If there are no substantiated blockers, say so.

## Evidence and citations

Classify material claims:

| Class    | Meaning                                              | Required treatment                                 |
| -------- | ---------------------------------------------------- | -------------------------------------------------- |
| Observed | Directly inspected in code, output, or tool results  | Cite the artifact, output, or source precisely.    |
| Claimed  | Assertion by documentation, ticket, comment, or PR   | Identify who or what makes the claim.              |
| Inferred | Conclusion derived from evidence                     | State the reasoning boundary and relevant evidence.|
| Unknown  | Missing, conflicting, inaccessible, or out of scope  | State impact and what could resolve it.            |

Cite repository evidence as `path/to/file.ext:line` or `path/to/file.ext:start-end`. Use Markdown links when the renderer supports stable line anchors. Cite symbols in addition to lines when that makes the evidence easier to relocate.

Do not claim tests or checks passed unless their results were observed. Distinguish passed, failed, blocked, and not run.

Record good decisions with the same specificity used for concerns.

## Visual presentation

Use a visualization when it makes an important relationship easier to understand than prose.

| Relationship                               | Preferred form   |
| ------------------------------------------ | ---------------- |
| Repeated dimensions or exact mappings      | Table            |
| Hierarchy, ownership, or nesting           | Tree             |
| Sequence, lifecycle, or state change       | Flow or timeline |
| Several interacting components or branches | Mermaid diagram  |
| One simple fact or relationship            | Prose            |

Read `visual-language.md` before adding symbols. Use only its defined roles. The visual-language reference is authoritative; its current symbol assignments override any symbols appearing in templates or examples elsewhere in this package.

## Evidence index

For Standard and Deep reviews, include a compact index of material sources:

| ID   | Source                                                       | Role                | Evidence class or limitation                         |
| ---- | ------------------------------------------------------------ | ------------------- | ---------------------------------------------------- |
| E001 | Precise local path, symbol, heading, command output, or link | What it establishes | Observed, claimed, freshness, access, or scope limit |

Include Jira tickets, PRs, documents, code areas, and command output that materially shaped the review. Prefer precise links in the body and use the index as an audit/navigation aid.

## Quality gate

- [ ] Purpose, audience/use, scope, evidence boundary, status/freshness, and material limitations are visible near the beginning.
- [ ] Repository, branch, HEAD, worktree, and target ticket/PR facts were freshly resolved.
- [ ] The opening gives the overall assessment and most consequential finding.
- [ ] The shared output spine is present, with optional sections omitted only when they add no value.
- [ ] Every concern has seriousness, confidence, evidence class, evidence citations, and impact.
- [ ] Finding IDs chain correctly across layers (F-XX -> I-XX -> A-XX).
- [ ] Observed, claimed, inferred, and unknown material are not misleadingly blended.
- [ ] Scope extensions are labeled and justified by demonstrated relationships.
- [ ] Strengths are recorded with the same specificity as concerns.
- [ ] Test and check status is accurate: passed, failed, blocked, or not run.
- [ ] Symbols come from the configured `visual-language.md` palette and remain restrained.
- [ ] Local links and source references are as precise as practical.
- [ ] The ending provides a concrete next action with stopping condition.
- [ ] No remote or local mutation was performed merely to complete the review.
- [ ] The response is proportionate to the user's requested depth.
