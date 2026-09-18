# VET output contract

Use this contract for Standard and Deep VET reviews. Preserve the disposition chain, comment accountability, evidence integrity, and actionable ending; omit empty sections rather than inventing content.

## Reader contract

A returning reader must be able to answer:

1. What exact branch, comparison basis, PR, tickets, and comment snapshot were reviewed?
2. Which requirements are met, unmet, or not verifiable?
3. What happened to every active PR or related-ticket comment?
4. What recommendation or response is justified by which evidence?
5. Which action can be safely launched next, and what proves it is complete?

## Output spine

| Section | Required content |
| --- | --- |
| 💭 Overview | Readiness verdict, scope, freshness, top concern, and next decision. |
| 🧭 Scope and requirements | Target, base, requirements, non-goals, repositories, and evidence limits. |
| 🔗 Evidence and relationships | Branch/PR/ticket map, source index, strengths, and verified contracts. |
| 💡 Comment dispositions | One row per active comment with critical assessment and response draft. |
| 🟰 Findings and decisions | Requirement coverage and concerns with severity and confidence. |
| 📋 Validation | Observed, failed, blocked, and proposed checks; never imply proposed checks ran. |
| 🎬 Action queue | Dependency-ordered corrective or restorative actions, response publication choices, and stop conditions. |

## Stable identifiers and links

- Use `E-###` for evidence, `C-###` for active comments, `F-###` for findings, `R-###` for recommended responses, and `A-###` for action items.
- Keep IDs stable when resuming the same branch/PR snapshot. Link the chain explicitly, for example: `C-03 -> F-02 -> R-03 -> A-02`.
- Every comment disposition must be one of **accept**, **partly accept**, **clarify**, **decline**, **superseded**, or **not verifiable**. A blank or implicit disposition is not allowed.
- Every active comment must have a recommended response. For **accept** or **partly accept**, the response links to an action; for **clarify**, it asks a precise question; for **decline** or **superseded**, it gives concise evidence-based reasoning.
- Do not call a comment resolved just because a response is drafted. Resolution is a remote state and must be freshly observed.

## Seriousness and confidence

Use **Critical**, **High**, **Medium**, **Low**, or **Note** for seriousness and **High**, **Medium**, or **Low** for confidence. Severity reflects impact if true; confidence reflects the evidence quality. Label claims **Observed**, **Claimed**, **Inferred**, or **Unknown**.

## Diagrams

Use the smallest useful visual. A branch/PR/ticket relationship diagram is useful when two or more repositories, tickets, or cross-surface dependencies affect the verdict. An action-dependency diagram is useful when three or more actions have ordering constraints. Cite the source of every edge in prose immediately after the diagram.

## Quality gate

- [ ] The overview precedes detail and names the next interactive decision.
- [ ] The evidence boundary separates current working-tree evidence from graph-derived mapping and remote observations.
- [ ] Every requirement has an explicit coverage state.
- [ ] Every active comment appears once in the register, has a disposition and response draft, and is linked to evidence.
- [ ] Every recommendation is either linked to a finding or clearly marked optional.
- [ ] Action items identify scope, owner/input, validation, status, and stopping condition.
- [ ] All proposed remote changes remain drafts until the user explicitly authorizes their selected IDs.
