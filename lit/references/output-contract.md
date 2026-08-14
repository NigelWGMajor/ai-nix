# LIT output contract

Use this contract when designing, drafting, and validating the reader-facing synthesis. Adapt the exact sections to the corpus and audience, but preserve the evidence, navigation, and source-integrity requirements.

## Contents

- [Reader contract](#reader-contract)
- [Output spine](#output-spine)
- [Evidence and citations](#evidence-and-citations)
- [Terminology](#terminology)
- [Conflicts and uncertainty](#conflicts-and-uncertainty)
- [Source assessment](#source-assessment)
- [Findings and decisions](#findings-and-decisions)
- [Visual presentation](#visual-presentation)
- [Next steps](#next-steps)
- [Evidence index](#evidence-index)
- [Quality gate](#quality-gate)

## Reader contract

State the shared reader contract near the beginning:

- Purpose or question.
- Audience and intended use.
- Scope and material exclusions.
- Evidence boundary, including corpus cutoff and research authorization.
- Status and freshness.
- Material limitations that affect the whole document.

Make the overall information architecture visible early. A reader should understand the shape of the subject and know where to go next without reading linearly from beginning to end.

## Output spine

Use the shared output spine from `documentation-standard.md` with these LIT sections:

1. **Title and reader contract**: identify purpose, audience/use, scope, evidence boundary, status/freshness, and material limitations.
2. **Orientation**: explain the domain, central mental model, important conclusion or uncertainty, and next reading path.
3. **At a glance**: compare three or more important dimensions compactly.
4. **Content map**: include when the document has more than three substantial reading paths.
5. **Foundations**: define dependent concepts and reconcile terminology.
6. **Relationships and evidence**: explain source relationships, boundaries, dependencies, sequences, state changes, or hierarchies.
7. **Detailed analysis**: organize depth along natural subject boundaries and comprehension dependencies.
8. **Findings and decisions**: present implications, decisions, conflicts, gaps, assumptions, and open questions.
9. **Next steps**: give the next reading, decision, validation, or action with a stopping condition.
10. **Evidence index**: account for every consulted source and its role.

Do not force empty sections. Combine adjacent concerns when separation would create fragments. Avoid single-item sections, repetitive summaries, decorative callouts, and walls of text.

## Evidence and citations

Link central claims to the closest available evidence. Prefer, in descending precision:

1. A stable anchor or heading.
2. A page or numbered section.
3. A line reference.
4. A file-level link when nothing more precise is possible.

Use relative links for local sources when the final document will remain in a stable workspace relationship. Preserve a usable source ID such as `S004` even when a direct link is unavailable.

Distinguish these evidence roles wherever context does not make them unmistakable:

- **Source-stated fact**: quote minimally or paraphrase faithfully and cite it.
- **Interpretation**: cite the source being interpreted and state that it is an interpretation.
- **Cross-source synthesis**: cite all sources that materially support the synthesis.
- **Inference**: identify it explicitly and show the evidence and reasoning boundary.
- **Recommendation**: state the goal, evidence, tradeoff, and uncertainty behind it.
- **Assumption**: state why it was needed and what would invalidate it.
- **Unknown**: state the missing information and likely consequence.

Never use citation density to imply certainty. A claim may remain uncertain even when several dependent or low-authority sources repeat it.

## Terminology

Choose canonical terminology for the synthesis when doing so improves comprehension. Record source-specific aliases and explain meaningful differences.

Do not merge terms merely because they look similar. Preserve distinctions in scope, lifecycle, ownership, or technical meaning. Include a compact glossary or mapping table when more than a few aliases occur.

## Conflicts and uncertainty

Do not flatten contradictions into smooth prose. For each material conflict:

1. State the competing claims.
2. Identify their supporting sources.
3. Compare authority, date, version, scope, and applicability.
4. Explain any resolution and its basis.
5. Otherwise preserve the conflict as an open question and state its impact.

Separate missing evidence from conflicting evidence. Separate an unknown answer from a low-confidence inference. Give consequential uncertainty more prominence than minor documentary gaps.

## Source assessment

Assess dimensions separately and briefly:

| Dimension | Question | Example values |
| --- | --- | --- |
| Currency | How well does the source align with the relevant current version or time? | Current, aging, superseded, unknown |
| Authority | Why can this source speak for the subject? | Normative, official, expert, derivative, informal, unknown |
| Relevance | How directly does it address the synthesis purpose? | Direct, supporting, contextual, peripheral |
| Completeness | How much of its claimed scope is present and usable? | Complete, partial, fragmentary, unknown |
| Decision value | How much could it affect the target decision or activity? | High, medium, low, unknown |
| Interpretation confidence | How confident is this synthesis in its reading of the source? | High, medium, low, unknown |

Explain the evidence for material assessments. Do not calculate or imply a single composite quality score. Perceived value depends on the current purpose and is not an intrinsic property of a source.

## Findings and decisions

Connect the synthesis to the reader's decision or activity. For each material finding or decision, state:

- The conclusion, implication, or choice.
- Its source basis and evidence role.
- Why it matters.
- The material tradeoff, uncertainty, or limitation.
- The decision owner or resolution path when applicable.

Keep conflicts, gaps, assumptions, and open questions in this section. Preserve viable alternatives when the corpus does not justify one definitive answer.

## Visual presentation

Use a table for repeated field comparisons, a flow or timeline for sequence, a tree for hierarchy, and a diagram for relationships that are difficult to explain linearly.

Use Mermaid only when supported by the target renderer. Keep node labels concise, avoid unexplained abbreviations, and follow every diagram with a short textual interpretation. The prose must preserve the essential meaning if the diagram does not render.

Use headings at consistent depths. Keep paragraphs focused. Adjust density according to cognitive load: introduce difficult abstractions before applying them, and place optional detail after the reader has a stable mental model.

Read `visual-language.md` before adding symbols. Use only its palette and never make a symbol the sole carrier of meaning. The visual-language reference is authoritative; its current symbol assignments override any symbols appearing in templates or examples elsewhere in this package.

## Next steps

End with the most useful next reading, decision, validation, or action. Name its purpose, target, expected evidence, and stopping condition. Do not use generic advice such as “continue investigating.”

Separate safe reading or validation from actions that require user choice, external coordination, or mutation approval.

## Evidence index

Include every source consulted, including unavailable or superseded sources that affected the analysis. For each source, provide:

- Stable source ID and title.
- Link or exact location.
- Role in the corpus.
- Relationship to other sources where material.
- Currency and decision-value marker plus textual explanation.
- Important limitations.

Use a tree when sources form a meaningful hierarchy, such as a specification with appendices or a primary guide with clarification notes. Do not invent hierarchy from mere filename proximity.

## Quality gate

Before completion, verify all of the following:

- [ ] Purpose, audience, decision context, and corpus boundary are explicit.
- [ ] Status, freshness, and material limitations are visible near the beginning.
- [ ] The shared output spine is present, with optional sections omitted only when they add no value.
- [ ] Central claims are traceable or explicitly labeled as derived or unknown.
- [ ] Source-stated facts, interpretations, synthesis, inferences, recommendations, assumptions, and unknowns are not misleadingly blended.
- [ ] Terminology is consistent and meaningful aliases are preserved.
- [ ] Material contradictions are resolved transparently or retained visibly.
- [ ] Important gaps and limitations state their likely effect.
- [ ] The overview agrees with the detailed sections.
- [ ] The organization follows comprehension dependencies rather than source order by default.
- [ ] Heading depth, pacing, links, and navigation are consistent.
- [ ] Diagrams materially improve understanding and have prose interpretations.
- [ ] Symbols come from the configured palette and are used sparingly.
- [ ] Every consulted source appears in the evidence index.
- [ ] Source assessments remain separate and have an explained basis.
- [ ] Each major section earns its cognitive cost.
- [ ] The original source documents remain unchanged.
- [ ] Persistence artifacts are sufficient to resume or audit the work.
