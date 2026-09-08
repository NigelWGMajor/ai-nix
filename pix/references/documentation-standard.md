# PIX documentation standard

Use this baseline for slideshow output produced by PIX. Adapts the shared LIT/KIT/NIX documentation conventions for slide-based presentation artifacts while preserving instance management and evidence integrity.

## Durable output and workspace storage

- Treat a slideshow as a durable artifact, not terminal-only output.
- Use a chat-only response only when the user explicitly requests it or the skill classifies the work as Short and the user permits chat-only output.
- Resolve the workspace root in this order: an explicit user-supplied workspace root, the configured workspace root that contains the source, the repository root, then the current working directory.
- Resolve one **output base** before locating or creating a run:
  1. If `TOOLING_OUTPUT_PATH` is set, use its absolute value directly. A value beginning `./` or `.\` is relative to the resolved workspace root (or current folder when no repository is available).
  2. Otherwise use `<workspace-root>/.data`.
- The output base already names the output directory. Never append another `.data` segment to it.
- Store a new run under `<output-base>/pix-YY-MM-DD-<suffix>/`, where the suffix is lowercase alphabetic: `a` through `z`, then `aa`, `ab`, and so on.
- Allocate the first unused suffix. Never overwrite, merge into, or silently reuse an existing instance.
- Create the output base when needed. Never modify `.gitignore` automatically and never stage, commit, or publish generated artifacts.
- Keep working notes and control artifacts in the instance, but always name the reader-facing deliverable `Findings.md`.
- When the user supplies an explicit output path, honor it. Retain an instance in the workspace when the skill requires resumability, and record the relationship between the instance and the requested deliverable.

## Slideshow structure

A PIX slideshow follows Marp-compatible Markdown conventions:

### Frontmatter

Every slideshow begins with YAML frontmatter:

```yaml
---
marp: true
theme: default
paginate: true
header: "[Short title or logo]"
footer: "Source: [source document name]"
---
```

### Slide separators

Use `---` on its own line, surrounded by blank lines, as the slide boundary. No other separator syntax.

### Slide types

| Type | Purpose | Heading level | Visual expectation |
| --- | --- | --- | --- |
| Title | Opening slide with presentation title, subtitle, audience, and date | `#` | Minimal text, strong focal point |
| Section | Marks a new major topic within the narrative | `#` or `##` with `<!-- _class: lead -->` | Topic name and one-line context |
| Content | Communicates one idea with text and optional visual | `##` | 3-6 lines of body text maximum |
| Diagram | Centers a Mermaid diagram or image as the focal point | `##` | Diagram plus 1-2 lines of interpretation |
| Code | Shows a code example or configuration | `##` | Code block plus 1-2 lines of context |
| Comparison | Contrasts options, approaches, or states | `##` | Table or side-by-side layout |
| Summary | Recaps key points at a section or deck boundary | `##` | Bulleted takeaways, 3-5 items |
| Action | Closes the deck with next steps or call to action | `##` | Concrete actions, not generic advice |

### Speaker notes

Place speaker notes as HTML comments at the end of each slide, before the next separator:

```markdown
<!-- Speaker notes: Context for the presenter. Source attribution, delivery cues, or background that does not belong on the visible slide. -->
```

Speaker notes should contain:
- Source attribution when the slide draws from a specific section.
- Delivery context or talking points.
- Evidence classifications when traceability matters.
- Transition cues to the next slide.

## Source attribution and evidence

- Record the source document path in the slideshow footer and in `00-control.md`.
- Preserve source evidence classifications (Observed, Claimed, Inferred, Unknown) in speaker notes when the source uses them.
- Do not add source IDs or citation markers to visible slide content unless the audience expects academic rigor.
- When reusing a source's Mermaid diagram, note the original location in a speaker note.
- When generating a new diagram from source prose, note the source section in a speaker note.

## Visual presentation on slides

- One idea per slide. If a slide communicates two distinct concepts, split it.
- Lead with the conclusion or key point, then support it. Do not build to a reveal unless the narrative arc specifically requires it.
- Keep body text to 3-6 visible lines per slide (excluding code blocks and diagrams).
- Use bullet points sparingly and keep them grammatically parallel.
- Tables: maximum 5 rows and 4 columns per slide.
- Code blocks: show only essential lines, 15 lines maximum. Use comments for omissions.
- Mermaid diagrams: maximum 12 nodes per slide. Use `%%{init: {'theme':'dark'}}%%` immediately after the fence.
- Images: use descriptive alt text. Size with Marp width directives when needed.
- Prefer one visual per slide. Two visuals compete for attention.
- Use symbols only from the skill's `visual-language.md` reference, sparingly, and only when they aid scanning. The visual-language reference is the authoritative source; when any other file uses a different symbol for the same role, the visual-language assignment wins.

## Final handoff

Return a concise chat summary that names:

- The slideshow paths (`Findings.md` for Marp source, `Findings.html` for interactive presentation).
- The source document and its scope.
- Slide count and depth level.
- Material content omitted or compressed from the source.
- Interactive HTML keyboard shortcuts: arrows/space to navigate, S for speaker notes, O for overview, F for fullscreen.
- Note: HTML file requires internet for Mermaid CDN. For offline use, the Marp markdown source is also provided.
- Any limitation a presenter should be aware of.

Do not paste the full slideshow into the conversation unless the user requests it.

## Shared quality gate

- [ ] The output is a durable Marp-compatible Markdown file when required by this standard.
- [ ] The instance path uses `<output-base>/pix-YY-MM-DD-<suffix>` and did not overwrite existing work.
- [ ] The slideshow begins with valid Marp YAML frontmatter.
- [ ] Slide separators are `---` on their own line, surrounded by blank lines.
- [ ] The opening orients the audience within the first 3 slides.
- [ ] Each slide communicates one idea.
- [ ] Visuals materially improve understanding and render correctly in Marp.
- [ ] Mermaid diagrams use the dark theme initializer and have 12 or fewer nodes.
- [ ] Speaker notes provide source attribution and presenter context.
- [ ] The closing provides actionable next steps.
- [ ] The source document was not modified.
- [ ] Generated artifacts remain outside source control.
- [ ] The final chat handoff includes the output path and does not substitute for the slideshow.
- [ ] Opaque identifiers from sources (codes, IDs, shorthand) are defined before first use and linked to their origin.
