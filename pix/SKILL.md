---
name: pix
description: Transform a markdown document (typically output from Kit, Lit, or Nix) into a Marp-compatible markdown slideshow with progressive disclosure, narrative arc, and visual anchoring. Use when the user invokes pix, asks to turn a document into a presentation or slideshow, or wants slide-ready material from an existing analysis. Do not use for ordinary document editing, code review, or formatting tasks unless the user explicitly asks to use pix. Explicit invocation overrides task-shape exclusions but never authorizes mutation of the source document.
---

# PIX Slideshow Generator

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the slideshow workflow.

Turn a technical document into a visual, frame-by-frame Markdown slideshow using a five-stage cycle:

`Survey -> Storyboard -> Compose -> Polish -> Deliver`

Produce a presentation that communicates the source's key messages through progressive disclosure, visual anchoring, and narrative pacing. The slideshow must stand alone as a presentation artifact while remaining traceable to its source.

## Standalone contract

- Contain the entire method in this package.
- Never require, invoke, or read RECIPE, LIT, KIT, NIX, their phase skills, their caches, or their outputs at runtime.
- Do not require subagents, mentor agents, special slash commands, or model routing.
- Use available workspace tools and repository guidance without depending on a particular tool name.
- Treat the source document as read-only. Never modify, move, or delete it.
- Create a durable slideshow for Standard and Extended decks. A Short deck may be returned in the conversation when the user explicitly requests chat-only output.

## Begin or resume

Determine whether the request identifies an existing PIX instance. If a `.data/pix-*` directory exists under the workspace root:

1. Read its `00-control.md` first.
2. Ask the user whether to **resume** the prior slideshow or **start a new instance**.
3. If resuming, verify that the source document still exists, continue from the recorded next safe action, and do not repeat completed stages.
4. If more than one instance is plausible, list them and ask which to use.

## Resolve the source

Apply this precedence:

1. Use an explicit document path or pasted content as the source.
2. When pointed at a `.data/<skill>-*` instance directory, use its `Findings.md` as the source.
3. When pointed at a directory containing a single prominent markdown document, use it.
4. With no clear source, ask one concise question. Do not guess.

Accept Markdown documents as primary input. Accept other text formats when the content is parseable, but warn that fidelity may be reduced. Do not fetch external URLs unless explicitly authorized.

Record the resolved source path and its provenance in `00-control.md`.

## Capture external references

Before building the slideshow, ensure that any external sources referenced by the source document are available locally as stable markdown snapshots.

### Gather links

Ask the user whether any Atlassian pages (Confluence, Jira), web documents, or other external links referenced in the source document should be captured for slide content or speaker notes. Accept URLs from the prompt, from the user's response, or discovered inside the source document.

### Check Atlassian MCP availability

Before fetching any Jira or Confluence content, verify the Atlassian MCP server is available by attempting a lightweight call using the `mcp__atlassian__*` tools. If the server is unreachable or returns a connection error, stop and advise the user:

> Could you try restarting the MCP server? You can either:
> 1. Run `! /mcp` in this prompt to check MCP server status
> 2. Use `curl` with your MCP credentials to access the Atlassian API directly

### Check for an existing `./md` folder

If a `./md` directory already exists under the resolved workspace root:

1. List every file in it with its frontmatter `source` and `captured` fields.
2. For each existing capture, ask the user whether to **keep** the current snapshot, **re-capture** it (fetch again and overwrite), or **remove** it from scope.
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

Once captures are complete, treat the `./md` snapshots as the working copies when drawing on external content for slides or speaker notes. Cite them by their local path rather than the original URL, but preserve the original URL in frontmatter for traceability. Note the capture date as a freshness limitation in `00-control.md`.

## Choose depth

- **Short**: 5-10 slides. Key takeaways and one or two anchor visuals. Suited for a quick briefing or elevator pitch.
- **Standard**: 10-25 slides. Balanced narrative with section breaks, visuals, and speaker notes. Default for most documents.
- **Extended**: 25-50 slides. Detailed coverage with rich visuals, step-by-step builds, and comprehensive speaker notes. Use for training material or deep-dive presentations.

Never inflate a small source into an Extended deck. Never compress a document with many interacting concepts into a Short deck. Match the deck depth to the source's complexity and the audience's needs.

## Create the slideshow instance

For Standard or Extended work, initialize a durable instance before substantial analysis:

```text
python <skill-directory>/scripts/init_instance.py --workspace <workspace-root> --source "<source-path>" --title "<title>" --audience "<audience>" --depth <short|standard|extended>
```

The initializer creates the next collision-safe `.data/pix-YY-MM-DD-<suffix>` directory under the resolved workspace root. It creates `.data` when needed, never overwrites an existing instance, and copies the slideshow template to `Findings.md`. Pass the resolved workspace root explicitly; never use an existing ancestor `.data` directory as a workspace marker.

Maintain:

- `00-control.md`: identity, source, scope, stage, progress, assumptions, questions, and next safe action.
- `01-source-map.md`: source structure, key messages, existing visuals inventory, and content classification.
- `02-storyboard.md`: slide sequence plan, narrative arc, visual assignments, and generation notes.
- `Findings.md`: the Marp-compatible slideshow.

Checkpoint `00-control.md` after each meaningful stage and before stopping. If the user explicitly requests chat-only output, do not create an instance. For Short work, create an instance only when the user asks to save the result.

## Run the five-stage cycle

### 1. Survey

Read and map the source document before planning any slides:

- Identify the document's purpose, audience, central message, and scope.
- Map the document's structure: sections, headings, hierarchy, and logical flow.
- Inventory existing visuals: Mermaid diagrams, images, code blocks, tables, and ASCII art.
- Classify content by presentation value: essential (must appear), supporting (include if space permits), reference-only (omit or compress).
- Note the document's evidence classifications, terminology, and source citations when present.
- Identify the natural narrative arc: what must the audience understand first, what builds on what.

Record the source map in `01-source-map.md`. Do not skip this stage for Standard or Extended decks.

### 2. Storyboard

Plan the slide sequence before drafting any content:

- Define the narrative arc: opening hook, context, core concepts, detailed exploration, synthesis, and call to action.
- Assign each slide a type: Title, Section, Content, Diagram, Code, Comparison, Summary, or Action.
- Map source sections to slides, noting which content to include, compress, or omit.
- Identify visual opportunities: where a new Mermaid diagram, comparison table, or visual metaphor would communicate better than prose.
- Plan which existing visuals to reuse, adapt, or split across slides.
- Estimate slide count and verify it fits the chosen depth.
- Note speaker note needs for slides that require presenter context beyond the visible content.

Record the storyboard in `02-storyboard.md`. Include the planned slide sequence as a numbered list with types and brief content descriptions.

### 3. Compose

Draft each slide following the storyboard:

- Write one idea per slide. If a slide tries to say two things, split it.
- Lead each content slide with a clear heading that communicates the slide's point, not just its topic.
- Use bullet points sparingly and keep them parallel in structure.
- Place visuals (Mermaid diagrams, code blocks, tables) as the focal point of their slide, not as an afterthought.
- Reuse source Mermaid diagrams verbatim when they fit a single slide. Simplify or split diagrams that are too dense for slide format.
- Generate new Mermaid diagrams for relationships, flows, hierarchies, or comparisons that the source explains in prose but would benefit from visual treatment on a slide.
- Add speaker notes (HTML comments below the slide separator) for context, delivery cues, or source attribution.
- Keep text concise: aim for no more than 6 lines of body text per slide, excluding code blocks and diagrams.
- Preserve source evidence classifications and citations in speaker notes when traceability matters.

### 4. Polish

Refine the slideshow for presentation quality:

- Verify the narrative arc flows naturally from slide to slide. Add transition phrases or bridging slides where the jump between topics is too abrupt.
- Check visual consistency: heading levels, bullet style, diagram theme settings, and code block language tags.
- Ensure all Mermaid diagrams use `%%{init: {'theme':'dark'}}%%` for consistent rendering.
- Verify slide density: no slide should require scrolling or have so little content that it feels empty.
- Check that the opening slides orient the audience within 3 slides.
- Verify the closing slides provide a clear takeaway and actionable next step.
- Remove decorative content that does not aid comprehension.
- Ensure the slideshow is self-sufficient: a presenter unfamiliar with the source document should be able to deliver it using only the slides and speaker notes.

### 5. Deliver

Finalize and hand off:

- Write the completed slideshow to `Findings.md` in the initialized instance.
- Verify Marp frontmatter is present and correct.
- Update `00-control.md` with final status, slide count, and any material limitations.
- Return the concise handoff: output path, slide count, source document, key limitations, and suggested presentation tool.

## Apply paired self-checks

Replace external review with one lightweight internal pass:

- **Survey <-> Compose**: Does each slide trace to a source section? Did Survey miss content that Compose needed? Is any essential content from the source map absent from the slides?
- **Storyboard <-> Polish**: Does the final slide order match the planned narrative arc? Is pacing consistent with the storyboard's intent?
- **Compose <-> Deliver**: Is the slideshow self-sufficient for presentation? Would a presenter find the speaker notes adequate?

Correct material failures before delivering. Do not narrate the self-check unless it reveals a limitation the presenter should know.

## Compose the output

Before drafting a Standard or Extended slideshow:

1. Read [references/documentation-standard.md](references/documentation-standard.md) and apply its slideshow structure, instance management, and visual rules.
2. Read [references/output-contract.md](references/output-contract.md) for PIX-specific slide architecture and generation rules.
3. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Its current assignments override any symbols hardcoded in templates, output contracts, or other reference files.
4. Adapt [assets/findings-template.md](assets/findings-template.md) to the source; do not force empty slide types. Replace any template symbols with the current assignments from visual-language.md.

For Short output, follow the same visual rules without loading or reproducing a large template unnecessarily.

Write the slideshow in Marp-compatible Markdown:

- YAML frontmatter with `marp: true`, theme, and pagination settings.
- `---` as slide separators on their own line.
- Directives via HTML comments (`<!-- _class: ... -->`) for slide-level styling.
- Speaker notes via HTML comments (`<!-- Speaker notes: ... -->`).

## Slideshow format rules

- Use `---` (three hyphens on a blank line) as the sole slide separator.
- Begin with YAML frontmatter: `marp: true`, `theme: default`, `paginate: true`.
- Use level-1 headings (`#`) only on title slides. Use level-2 (`##`) for content slide headings.
- Keep one blank line before and after every slide separator.
- Place speaker notes as the last element before the next separator: `<!-- Speaker notes: ... -->`.
- For Mermaid diagrams on slides, keep them under 12 nodes to remain legible at presentation scale.
- For code blocks, show only the essential lines. Use comments to indicate omissions.
- For tables, limit to 5 rows and 4 columns per slide. Split larger tables across slides.
- For images, use standard Markdown image syntax with descriptive alt text.

## Complete the slideshow

Apply the quality gate in [references/documentation-standard.md](references/documentation-standard.md) and the PIX-specific gate in [references/output-contract.md](references/output-contract.md). Report:

- The slideshow output path.
- The source document and its scope.
- Slide count and depth level.
- Material content omitted or compressed.
- Suggested presentation tool (Marp CLI, VS Code Marp extension, or compatible renderer).

Recommend a narrow PIX improvement after real use only when recurring friction reveals a missing slide type, visual rule, or storyboard pattern. Do not silently modify the installed skill during slideshow generation.
