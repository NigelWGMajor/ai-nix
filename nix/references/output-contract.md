# NIX output contract

Use this contract for Standard and Deep NIX analyses. Adapt the exact sections to the subject while preserving the six-stage method, evidence integrity, visual restraint, and actionable ending.

## Contents

- [Reader contract](#reader-contract)
- [Output spine](#output-spine)
- [Six-stage presentation](#six-stage-presentation)
- [Evidence and confidence](#evidence-and-confidence)
- [Findings and decisions](#findings-and-decisions)
- [Visual presentation](#visual-presentation)
- [Evidence index](#evidence-index)
- [Quality gate](#quality-gate)

## Reader contract

State, explicitly or through unmistakable context:

- Purpose or question.
- Audience and intended use.
- Scope and material exclusions.
- Evidence boundary.
- Status and freshness.
- Material limitations that affect the whole document.
- Depth: Compact, Standard, or Deep.
- Important assumptions that affect the conclusion.

Do not make the reader reconstruct the question from discovery notes. Lead with the central explanation or conclusion, then show how the six stages support it.

## Output spine

Use the shared output spine from `documentation-standard.md` and preserve these NIX mappings:

| Shared role | NIX section |
| --- | --- |
| Title and reader contract | Title block |
| Orientation | Orientation |
| At a glance | At a glance, when three or more dimensions help |
| Content map | Content map, when the document has more than three substantial sections |
| Foundations | Reflect |
| Relationships and evidence | Explore and Connect |
| Detailed analysis | Imagine |
| Findings and decisions | Produce |
| Validation | Proposed or executed checks, when material |
| Next steps | Empower |
| Evidence index | Evidence index |

Begin Orientation with a short answer to:

1. What is this subject?
2. Why does it matter in the current context?
3. What is the dominant mental model?
4. What is the most consequential finding, uncertainty, or decision?
5. Where should the reader go next?

Use the common section names in the NIX stage qualifiers, such as `Produce - findings and decisions` and `Empower - next steps`. Omit optional sections when they would add no value.

## Six-stage presentation

Make all stages visible for Standard and Deep output. Keep each stage focused on its distinct job.

### Reflect

Show the trigger, core question, scope, constraints, assumptions, and sufficient exit condition. Avoid turning Reflect into a paraphrase of the entire prompt.

### Explore

Summarize the evidence landscape: authoritative sources, entry points, existing patterns, available tools, contradictions, and gaps. Prefer a small source map over a long inventory.

### Connect

Present the system model: boundaries, hierarchy, ownership, dependencies, flows, state changes, sources of truth, consumers, and failure propagation. Use the smallest visual that materially reduces explanation cost.

### Imagine

Present only grounded interpretations, alternatives, counterfactuals, or implications. For real choices, compare options using consistent criteria. For pure explanation, emphasize hidden assumptions, likely evolution, and what would change the model.

### Produce

Deliver the coherent answer: central concepts, conclusions, reconciled terminology, prioritized findings, or recommendation. This should be the section a returning reader can use as the durable mental model.

### Empower

Explain how to use, navigate, test, challenge, or extend the understanding. Provide the best next reading or action, its purpose, expected evidence, and stopping condition.

Do not repeat the same statement in every stage. Let stages accumulate understanding:

`frame -> evidence -> relationships -> possibilities -> synthesis -> use`

## Evidence and confidence

Use these labels when provenance is not obvious:

| Class    | Meaning                                             | Required treatment                                  |
| -------- | --------------------------------------------------- | --------------------------------------------------- |
| Observed | Directly inspected evidence                         | Cite the artifact, output, or source precisely.     |
| Claimed  | Assertion by a narrative source                     | Identify who or what makes the claim.               |
| Inferred | Conclusion derived from evidence                    | State the reasoning boundary and relevant evidence. |
| Unknown  | Missing, conflicting, inaccessible, or out of scope | State impact and what could resolve it.             |

Use confidence only when it improves interpretation:

- **High**: direct, consistent evidence strongly supports the conclusion.
- **Medium**: evidence supports the conclusion with a material gap or interpretive step.
- **Low**: plausible but based on incomplete, stale, or ambiguous evidence.

Do not equate source quantity with independent corroboration. Do not hide disagreement in polished synthesis.

## Findings and decisions

In Produce, state for each material finding:

- What was observed or inferred.
- Supporting evidence.
- Why it matters.
- Confidence and material limitation when useful.
- What should happen next, if anything.

For options, compare the same criteria across each alternative. Common criteria include scope fit, complexity, reversibility, maintainability, performance, usability, delivery risk, and future flexibility.

Make a recommendation only when the user needs a decision or one follows naturally from the analysis. State the criteria and tradeoffs. Preserve viable alternatives instead of presenting preference as fact.

Include strengths and coherent design choices when they materially help understanding. Keep open decisions in Produce; put the actionable sequence in Empower.

## Visual presentation

Use a visualization when it makes an important relationship easier to understand than prose.

| Relationship                               | Preferred form   |
| ------------------------------------------ | ---------------- |
| Repeated dimensions or exact mappings      | Table            |
| Hierarchy, ownership, or nesting           | Tree             |
| Sequence, lifecycle, or state change       | Flow or timeline |
| Several interacting components or branches | Mermaid diagram  |
| One simple fact or relationship            | Prose            |

For Mermaid:

- Use it only when supported by the target renderer.
- Keep nodes and edges few enough to scan.
- Label the meaning of important edges.
- Avoid unexplained abbreviations.
- Follow the diagram with a short prose interpretation.
- Preserve the essential meaning if the diagram does not render.

Read `visual-language.md` before adding symbols. Use only its defined roles. The visual-language reference is authoritative; its current symbol assignments override any symbols appearing in templates or examples elsewhere in this package.

## Evidence index

For Standard and Deep output, include a compact index of material sources:

| ID   | Source                                                       | Role                | Evidence class or limitation                         |
| ---- | ------------------------------------------------------------ | ------------------- | ---------------------------------------------------- |
| E001 | Precise local path, symbol, heading, command output, or link | What it establishes | Observed, claimed, freshness, access, or scope limit |

Include only consulted sources that materially shaped the answer. Prefer precise links in the body and use the index as an audit/navigation aid, not a bibliography dump.

## Quality gate

- [ ] The subject, question, scope, and evidence boundary are explicit.
- [ ] Status, freshness, and material limitations are visible near the beginning.
- [ ] The opening gives the central answer or mental model.
- [ ] The shared output spine is present, with optional sections omitted only when they add no value.
- [ ] Reflect identifies assumptions and does not confuse symptoms with the core question.
- [ ] Explore identifies authoritative evidence, gaps, and diminishing-return boundaries.
- [ ] Connect explains material relationships, dependencies, flows, and impact.
- [ ] Imagine remains grounded and does not invent forced alternatives.
- [ ] Produce synthesizes rather than repeats discovery notes.
- [ ] Empower provides a concrete way to use, validate, or extend the understanding.
- [ ] Paired self-checks expose missing dependencies, unsupported possibilities, and unusable conclusions.
- [ ] Observed, claimed, inferred, and unknown material are not misleadingly blended.
- [ ] Local links and source references are as precise as practical.
- [ ] Visuals materially improve comprehension and have textual interpretation.
- [ ] Symbols come from the configured palette and remain restrained.
- [ ] Recommendations disclose criteria and tradeoffs.
- [ ] Important strengths, conflicts, risks, and unknowns remain visible.
- [ ] The response is proportionate to the user's requested depth.
- [ ] No workspace or external mutation occurred without explicit authorization.
