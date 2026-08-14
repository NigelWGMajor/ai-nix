# PIX output contract

Use this contract for Standard and Extended PIX slideshows. Adapt the exact slide sequence to the source document while preserving the narrative arc, visual anchoring, source traceability, and presentation quality.

## Contents

- [Source contract](#source-contract)
- [Slide architecture](#slide-architecture)
- [Five-stage presentation](#five-stage-presentation)
- [Narrative arc](#narrative-arc)
- [Visual generation rules](#visual-generation-rules)
- [Mermaid on slides](#mermaid-on-slides)
- [Source reuse rules](#source-reuse-rules)
- [Speaker notes contract](#speaker-notes-contract)
- [Pacing and density](#pacing-and-density)
- [Quality gate](#quality-gate)

## Source contract

State in the slideshow's title slide and in `00-control.md`:

- Source document and its path.
- Source purpose and audience (inherited from the document).
- Slideshow audience (may differ from the source audience).
- Scope: what the slideshow covers and what it omits.
- Depth level: Short, Standard, or Extended.
- Material limitations that affect the presentation.

Do not make the presenter reconstruct the source's purpose. The title slide and first content slides must orient the audience to the subject, why it matters, and the shape of what follows.

## Slide architecture

### Deck structure

A Standard or Extended deck follows this structural template. Adapt it to the source; do not force empty sections.

| Position | Slide type | Purpose | Required |
| --- | --- | --- | --- |
| 1 | Title | Presentation title, subtitle, audience, date | Yes |
| 2-3 | Content | Context and motivation — why this matters | Yes |
| 4 | Content or Diagram | Mental model or architecture overview | Yes for Standard+ |
| 5-N | Section + Content + Diagram + Code + Comparison | Body: progressive exploration of the subject | Yes |
| N+1 | Summary | Key takeaways | Yes for Standard+ |
| N+2 | Action | Next steps or call to action | Yes |

### Short deck structure

| Position | Slide type | Purpose |
| --- | --- | --- |
| 1 | Title | Title and context in one slide |
| 2-3 | Content or Diagram | The essential concepts |
| 4-8 | Content | Key details and relationships |
| 9-10 | Summary + Action | Takeaways and next step |

## Five-stage presentation

The five PIX stages govern how the slideshow is built, not how it is presented. The audience sees a narrative, not a process.

### Survey

Map the source before planning slides. Record in `01-source-map.md`:

- Document purpose, audience, and central message.
- Section-by-section structure with heading levels and approximate size.
- Inventory of existing visuals: Mermaid diagrams (with node count), images, code blocks, tables.
- Content classification: essential, supporting, or reference-only.
- Key terminology and concepts that need definition on slides.
- Natural narrative entry points and climactic moments.

### Storyboard

Plan the slide sequence before drafting. Record in `02-storyboard.md`:

- Numbered slide list with type, heading, and content summary.
- Source section mapping: which source sections feed each slide.
- Visual plan: which existing visuals to reuse, which to adapt, which to generate new.
- Narrative arc annotation: hook, context, rising complexity, climax (key insight), denouement (implications), action.
- Estimated slide count and depth verification.

### Compose

Draft slides following the storyboard. Apply:

- One idea per slide rule.
- Visual anchoring: prefer a visual focal point (diagram, code, table) over text-only slides when the content supports it.
- Progressive disclosure: introduce concepts before using them in relationships.
- Parallel structure in bullet lists.
- Concise headings that state the slide's point, not just its topic.

### Polish

Refine for presentation quality:

- Narrative flow between slides.
- Visual consistency (heading levels, diagram themes, code language tags).
- Density balance (no scrolling slides, no empty slides).
- Speaker note completeness.
- Marp compatibility verification.

### Deliver

Finalize and hand off:

- Write completed slideshow to `Findings.md`.
- Update `00-control.md` to complete status.
- Return handoff summary.

## Narrative arc

Every deck, regardless of depth, follows a narrative arc:

1. **Hook** (slide 1-2): Why should the audience care? State the problem, question, or opportunity.
2. **Context** (slides 2-4): What does the audience need to know first? Establish the mental model.
3. **Rising complexity** (slides 5-N): Build understanding progressively. Each slide adds one layer. Use section breaks at natural topic boundaries.
4. **Climax** (1-2 slides): The key insight, finding, or decision. This is what the audience should remember.
5. **Denouement** (1-3 slides): Implications, tradeoffs, and open questions.
6. **Action** (final slide): What should the audience do next?

For documents that are primarily reference material (like implementation guides), replace the climax with a "key patterns" summary and the denouement with "gotchas and exceptions."

## Visual generation rules

Generate new visuals when the source explains a relationship, flow, hierarchy, or comparison in prose that would be more effective as a diagram on a slide. Do not generate visuals merely to fill space.

### When to generate

| Source content | Generate | Type |
| --- | --- | --- |
| A process or workflow described in numbered steps | Yes | Mermaid flowchart |
| A hierarchy or containment relationship | Yes | Mermaid flowchart (TD) |
| A sequence of events or state changes | Yes | Mermaid sequence or state diagram |
| A comparison of 2-4 options with consistent criteria | Consider | Table (often better than a diagram) |
| A single fact or definition | No | Prose is sufficient |
| A list of items without relationships | No | Bullets are sufficient |

### When to reuse from source

- Reuse a source Mermaid diagram verbatim when it has 12 or fewer nodes and communicates one relationship.
- Simplify a source diagram when it exceeds 12 nodes by focusing on the most important path or splitting it across slides.
- Adapt a source table into a comparison slide when it fits within the 5-row, 4-column limit.
- Reference source images by path when the slideshow will be presented from the same workspace.

### When to split

- A source diagram with 13-20 nodes: split into two slides at a natural boundary. Show the overview on one slide and the detail on the next.
- A source diagram with 20+ nodes: summarize the top-level structure on one slide and show subsections on subsequent slides as needed.
- A source table with 6+ rows: show the most important rows on one slide and the remainder on a continuation slide or omit reference-only rows.

## Mermaid on slides

- Always include `%%{init: {'theme':'dark'}}%%` as the first line after the mermaid fence.
- Maximum 12 nodes per diagram on a single slide.
- Use concise node labels (2-4 words). Move detail to speaker notes.
- Label edges that carry meaning. Omit labels on obvious relationships.
- Use subgraphs only when containment is the point of the diagram.
- Prefer `flowchart TD` for hierarchies and `flowchart LR` for processes.
- Follow each diagram with 1-2 lines of prose interpretation on the same slide.

## Source reuse rules

When the source document contains Mermaid diagrams, images, code blocks, or tables:

1. **Assess fit**: Does the visual communicate effectively at slide scale (limited space, large font)?
2. **Reuse verbatim** when it fits within slide constraints and communicates one idea.
3. **Adapt** when the visual is too dense: simplify labels, remove secondary paths, or extract one subgraph.
4. **Split** when the visual covers two ideas: put each on its own slide.
5. **Replace** when the visual format is wrong for slides: convert a wide table to a vertical comparison, or a dense flowchart to a simplified overview.
6. **Attribute** the source location in a speaker note.

Never silently modify the source document's visuals. Work on copies.

## Speaker notes contract

Every content, diagram, and code slide should have speaker notes. Speaker notes serve three purposes:

1. **Presenter context**: What to say about this slide beyond what is visible.
2. **Source attribution**: Which section of the source document this slide draws from.
3. **Transition cue**: How to bridge to the next slide.

Format:

```markdown
<!-- Speaker notes:
[Talking points for this slide.]
Source: [section or heading in the source document]
Transition: [how this connects to the next slide]
-->
```

Title slides, section break slides, and summary slides may omit speaker notes when the visible content is self-explanatory.

## Pacing and density

### Slide-per-minute rule

Estimate 1-2 minutes per slide for Standard decks. A 20-slide deck should support a 20-40 minute presentation.

### Density guidelines

| Depth | Slides | Visual ratio | Speaker note depth |
| --- | --- | --- | --- |
| Short | 5-10 | 1 visual per 3 slides | Minimal or none |
| Standard | 10-25 | 1 visual per 2-3 slides | Source attribution + talking points |
| Extended | 25-50 | 1 visual per 2 slides | Full context, delivery cues, transitions |

### Section breaks

Insert a section break slide before each new major topic. A section break provides:
- The section name.
- A one-line context statement.
- Optional: a visual showing where this section fits in the overall narrative.

## Visual symbols

Read `visual-language.md` before adding symbols to slides or speaker notes. Use only its defined roles. The visual-language reference is authoritative; its current symbol assignments override any symbols appearing in templates or examples elsewhere in this package.

## Quality gate

- [ ] The source document, audience, scope, and depth are explicit in the title slide and `00-control.md`.
- [ ] The slideshow begins with valid Marp YAML frontmatter (`marp: true`).
- [ ] The narrative arc is present: hook, context, rising complexity, climax, denouement, action.
- [ ] The audience is oriented within the first 3 slides.
- [ ] Each slide communicates one idea.
- [ ] Headings state the slide's point, not just its topic.
- [ ] Visible text stays within 3-6 lines per content slide.
- [ ] Mermaid diagrams use dark theme initialization and have 12 or fewer nodes.
- [ ] Tables fit within 5 rows and 4 columns per slide.
- [ ] Code blocks show only essential lines, 15 lines maximum.
- [ ] Existing source visuals are reused, adapted, or attributed rather than silently discarded.
- [ ] New visuals are generated only where prose relationships benefit from visual treatment.
- [ ] Speaker notes provide source attribution and presenter context on content slides.
- [ ] Section breaks appear at major topic transitions.
- [ ] The closing slide provides a concrete next step, not generic advice.
- [ ] The slideshow is self-sufficient: a presenter can deliver it using only the slides and speaker notes.
- [ ] Survey <-> Compose: all essential source content is represented.
- [ ] Storyboard <-> Polish: the final order matches the planned narrative arc.
- [ ] Symbols come from the configured `visual-language.md` palette and are used sparingly.
- [ ] The source document was not modified.
- [ ] No generated artifact is staged or added to source control.
