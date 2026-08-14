---
name: lit
description: Transform one or more dense technical documents into a professional, layered, evidence-linked explanation with progressive disclosure, terminology reconciliation, source assessment, useful diagrams, and resumable analysis artifacts. Use when asked to clarify or synthesize document collections, build orientation or implementation guides, reconcile overlapping or contradictory sources, create decision-support documentation, or resume an existing LIT analysis instance. Do not use solely for an ordinary short summary, copyediting, mechanical reformatting, unsupported content generation, or code or pull-request review unless document synthesis is the primary task. An explicit request to use lit overrides these exclusions.
---

# Layered Information Transformation

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the analysis workflow.

Turn complex source material into an auditable guide that supports rapid orientation and progressively deeper understanding. Preserve nuance and a precise route back to the original evidence.

## Operating principles

- Treat source documents as read-only.
- Keep the source boundary explicit; do not add unrelated research unless the user authorizes it or requested research from the outset.
- Distinguish source-stated facts from interpretation, synthesis, inference, recommendation, assumption, and unknowns.
- Do not silently reconcile disagreement. Resolve it with explicit evidence and criteria or preserve it as an open question.
- Normalize terminology only when useful. Retain source-specific aliases and meaningful distinctions.
- Let comprehension dependencies, natural subject boundaries, and cognitive load determine sequence and density.
- Write for the reader's decision or activity, not merely to mirror source order or length.
- Use diagrams and graphical symbols only when they materially improve comprehension.
- Store generated work in a dedicated `.data` instance and never add it to source control.
- Use [references/jira-integration.md](references/jira-integration.md) to interpret Jira fields and conventions when the corpus includes Jira or Atlassian sources.

## Begin or resume

Determine whether the request identifies an existing LIT instance. If it does:

1. Read `00-control.md` and `01-evidence.md` first.
2. Verify that referenced local sources still exist and identify material changes where feasible.
3. Continue from the recorded next safe action rather than repeating completed analysis.
4. Ask which instance to use if more than one is plausible; do not guess.

For new work, determine:

1. The intended audience. Default to technically informed decision-makers.
2. The question, decision, or activity the result must support.
3. The source corpus and its boundaries.
4. Which sources are primary, supplementary, normative, historical, or explanatory.
5. The desired depth and any time or length limit. Default to an orientation plus detailed reference.
6. The current workspace and suitable persistence location.

Ask concise questions only when an answer could materially change scope, interpretation, organization, or conclusions. Otherwise proceed with a bounded assumption and record it in `00-control.md`.

## Capture external references

Before deep analysis, ensure that all external sources are available locally as stable markdown snapshots.

### Gather links

Ask the user whether any Atlassian pages (Confluence, Jira), web documents, API references, or other external links should be included in the corpus. Accept URLs from the prompt, from the user's response, or discovered inside supplied documents.

### Check for an existing `./md` folder

If a `./md` directory already exists under the resolved workspace root:

1. List every file in it with its frontmatter `source` and `captured` fields.
2. For each existing capture, ask the user whether to **keep** the current snapshot, **re-capture** it (fetch again and overwrite), or **remove** it from the corpus.
3. Accept new URLs to add alongside the retained captures.

If no `./md` directory exists, create it when the first external reference is confirmed.

### Capture process

For each confirmed URL:

1. Fetch the content and convert it to clean Markdown.
2. Write it to `./md/<slugified-title>.md` with YAML frontmatter:

```yaml
---
source: "<original URL>"
captured: "<YYYY-MM-DD>"
title: "<page or issue title>"
type: "<confluence | jira-issue | jira-epic | web | api-doc | other>"
---
```

3. Preserve the document's semantic structure (headings, lists, tables, code blocks). Strip navigation chrome, sidebars, and boilerplate.
4. For Jira issues, include key fields (summary, status, type, assignee, labels, description, and acceptance criteria) as structured frontmatter or a leading metadata table.
5. For Confluence pages, preserve the page hierarchy context (space, parent page) in frontmatter when available.

### Use captured documents

Once captures are complete, treat the `./md` snapshots as the working copies for all subsequent analysis. Cite them by their local path rather than the original URL, but preserve the original URL in frontmatter for traceability. Note the capture date as a freshness limitation in `01-evidence.md`.

## Create the analysis instance

Prefer the supplied initializer because it creates a collision-safe directory and the standard artifacts:

```text
python <skill-directory>/scripts/init_instance.py --workspace <workspace-root> --purpose "<purpose>" --audience "<audience>"
```

The initializer creates `.data/lit-YY-MM-DD-<suffix>` under the resolved workspace root using the next available lowercase alphabetic suffix. It creates `.data` if needed and never overwrites an existing instance. Pass the resolved workspace root explicitly; never use an existing ancestor `.data` directory as a workspace marker. When the environment cannot execute Python, reproduce the same structure manually without reusing an existing directory.

Assume `.data` is excluded when the workspace is a Git repository. Never modify `.gitignore`. Never add instance artifacts or the final document to source control.

Maintain these files:

- `00-control.md`: purpose, audience, boundary, phase, progress, assumptions, questions, and next safe action.
- `01-evidence.md`: stable source IDs, locations, roles, versions, scope, authority, availability, and explained assessments.
- `02-analysis.md`: concepts, terminology, evidence, relationships, conflicts, inferences, and gaps.
- `03-structure.md`: reader journey, comprehension dependencies, section plan, and planned visuals.
- `Findings.md`: professional reader-facing result.

Checkpoint `00-control.md` after each meaningful phase and before stopping. Keep interim notes compact but sufficient for another session to resume.

## Inventory the corpus

Build the inventory before synthesizing a large or multi-document corpus. Assign stable IDs such as `S001`, `S002`, and `S003`. Record, when known:

- Exact location and access status.
- Role in the corpus.
- Title, owner or publisher, version, and date.
- Scope and applicability.
- Authority and relationship to other sources.
- Currency, relevance, completeness, decision value, and confidence in interpretation.

Keep these dimensions separate and explain assessments briefly. Never turn them into one vague quality score.

For inaccessible or missing sources, record the limitation and its likely effect. Do not invent their content. For changed sources on resumption, record what changed or that the extent is unknown.

## Analyze the material

Analyze sources in manageable passes when the corpus is large. Preserve source IDs and precise evidence locations throughout.

Extract and relate:

- Essential concepts and claims.
- Terminology, aliases, and collisions.
- Dependencies, sequences, boundaries, hierarchies, and flows.
- Agreement, ambiguity, and contradiction.
- Differences in authority, currency, scope, and applicability.
- Missing evidence and unanswered questions.
- Implications for decisions, production, testing, deployment, or other relevant lifecycle concerns.

Classify important statements as one of:

- **Source-stated fact**: directly supported by a cited source.
- **Interpretation**: an explanation of source meaning.
- **Cross-source synthesis**: a conclusion formed by combining cited sources.
- **Inference**: a reasoned conclusion not stated directly.
- **Recommendation**: proposed action or choice.
- **Assumption**: a provisional premise used to proceed.
- **Unknown**: unresolved or unsupported.

Use explicit labels wherever a reader might otherwise mistake derived material for source fact. For conflicts, compare authority, scope, date, version, and applicability. Document the basis for any resolution.

## Design the reader journey

Organize according to what the audience must understand first. Use a progression such as `concepts -> sources -> relationships -> inferences -> production -> testing -> deployment` only when it fits the material.

Reveal the information architecture near the beginning. Support both scanning and progressive disclosure. Give each subject space proportional to importance, consequence, conceptual difficulty, and decision value rather than source volume.

Before drafting the final document:

1. Read [references/documentation-standard.md](references/documentation-standard.md) and apply its shared document, link, visual, handoff, and workspace-storage rules.
2. Read [references/output-contract.md](references/output-contract.md) and follow its LIT-specific structure, evidence, source-assessment, and quality rules.
3. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Its current assignments override any symbols hardcoded in templates, output contracts, or other reference files. Use only its configured symbols.
4. Copy and adapt [assets/findings-template.md](assets/findings-template.md) rather than treating it as a mandatory rigid outline. Replace any template symbols with the current assignments from visual-language.md.
5. Record the proposed structure and comprehension dependencies in `03-structure.md`.

Preserve the shared output spine and keep LIT-specific source synthesis inside its mapped sections.

Use Mermaid where supported only for a relationship that is materially easier to understand visually. Provide a short prose interpretation so the document remains useful without rendered diagrams.

## Draft and validate

Write polished Markdown in US English unless the user requests another convention. Prefer precise relative links with headings, anchors, pages, sections, or line references. Link central claims as closely as the source format permits.

Use the shared quality gate in [references/documentation-standard.md](references/documentation-standard.md) and the LIT-specific gate in [references/output-contract.md](references/output-contract.md). In addition, verify:

- The executive view agrees with the detailed analysis.
- Every consulted source appears in the evidence index.
- Conflicts, assumptions, and unknowns remain visible.
- Terminology and aliases are consistent.
- Diagrams and symbols add meaning and remain understandable in text.
- The persistence files accurately describe completed work and the final state.
- Original source documents remain unchanged.
- No generated artifact is staged or otherwise added to source control.

Set the control status to `complete` only after the result passes the quality gate. Report the output path, corpus limitations, unresolved questions, and material assumptions to the user.

## Self-improvement signals

After real use, note recurring friction in `00-control.md`, such as missed trigger language, unclear evidence labels, insufficient checkpoint state, an awkward template section, or a missing visual role. Recommend a narrowly scoped skill adjustment rather than silently editing the installed skill during analysis.
