# Shared documentation standard

Use this baseline for reader-facing Markdown produced by LIT, KIT, NIX, WIZ, COP, FIX, and VAL. Each skill package contains its own copy so it remains standalone. Keep copies byte-for-byte identical when this standard changes; PIX has its own slide-adapted version.

## Durable output and workspace storage

- Treat a professional analysis, synthesis, recovery review, or handoff as a durable document, not terminal-only output.
- Use a chat-only response only when the user explicitly requests it or the skill classifies the work as Compact and its own contract permits chat-only output.
- Resolve the workspace root in this order:
  1. An explicit user-supplied workspace root from the prompt
  2. The repository root via MCP tool `vscode-workspace.get_workspace_root` if available
  3. The repository root via `git rev-parse --show-toplevel` from the current directory
  4. OS-specific fallback: `C:\.data` (Windows), `~/Library/Application Support/claude-skills` (macOS), or `~/.local/share/claude-skills` (Linux)
- Resolve one **output base** before locating or creating a run:
  1. If `TOOLING_OUTPUT_PATH` is set, use its absolute value directly. A value beginning `./` or `.\` is relative to the resolved workspace root (or current folder when no repository is available).
  2. Otherwise use `<workspace-root>/.data`.
- The output base already names the output directory. Never append another `.data` segment to it.
- Store a new run under `<output-base>/<skill>-YY-MM-DD-<suffix>/`, where `<skill>` is the skill prefix (`lit`, `kit`, `nix`, `wiz`, `cop`, `fix`, `val`) and the suffix is lowercase alphabetic: `a` through `z`, then `aa`, `ab`, and so on.
- Allocate the first unused suffix. Never overwrite, merge into, or silently reuse an existing instance.
- Create the output base when needed. Never modify `.gitignore` automatically and never stage, commit, or publish generated artifacts.
- Follow stricter skill-specific safety rules. In particular, honor any requirement to refuse an unignored in-repository output path.
- Keep working notes and control artifacts in the instance, but always name the reader-facing deliverable `Findings.md`. - EXCEPTION: TUT names its output artifacts tutorial-a.md.
- When the user supplies an explicit output path, honor it. Retain an instance in the workspace when the skill requires resumability, and record the relationship between the instance and the requested deliverable.

## Reader-facing structure

Lead with the answer and orientation. Use this shared output spine, omitting only sections marked optional when they would add no value:

| Order | Common section | Purpose | Requirement |
| ---: | --- | --- | --- |
| 1 | Title and reader contract | State purpose or question, audience/use, scope, evidence boundary, status or freshness, and material limitations. | Required |
| 2 | Orientation | Explain what the subject is, why it matters, the dominant mental model, the most consequential conclusion or uncertainty, and where to go next. | Required |
| 3 | At a glance | Compare three or more status or understanding dimensions compactly. | Optional |
| 4 | Content map | Expose natural reading paths when the document has more than three substantial sections. | Optional |
| 5 | Foundations | Define concepts, vocabulary, scope, and context that later sections depend on. | Required when the body depends on specialized context |
| 6 | Relationships and evidence | Explain flows, boundaries, dependencies, lifecycle, traceability, or source relationships. | Required |
| 7 | Detailed analysis | Hold skill-specific analysis that does not fit the shared sections cleanly. | Optional |
| 8 | Findings and decisions | Connect the evidence to conclusions, strengths, risks, tradeoffs, choices, and unresolved decisions. | Required |
| 9 | Validation | Distinguish executed checks, existing evidence, proposed checks, and limitations. | Required when validation is material |
| 10 | Next steps | Give the next reading, decision, validation, or action with its target, purpose, expected evidence, and stopping condition. | Required |
| 11 | Evidence index | List material sources and their roles. | Required for Standard or Deep work |

Use the common section names when their roles apply. A skill may prefix its method name or stage, such as `Produce - findings and decisions`, but should preserve the shared role in the heading. Keep skill-specific subsections inside this spine rather than inventing a parallel reader journey.

Do not force empty sections, repeat the same conclusion under several headings, or create a section for one minor item.

## Evidence and links

- Distinguish direct evidence from claims, interpretation, synthesis, inference, recommendation, assumption, and unknowns whenever the reader could confuse them.
- Put evidence links close to consequential statements. Prefer a heading or anchor, then a page or numbered section, then a line, then a file-level link.
- Prefer concise relative Markdown links for local workspace evidence:
  - Bookmark: `[🔖 Description](relative/path.md#heading)`.
  - File: `[🔗 Description](relative/path.md)`.
  - Jira ticket: `[🎟️ ABC-123](url)`.
  - Pull request: `[🔀 PR #123](url)`.
  - Other external source: `[🔗 Description](url)`.
- Preserve meaningful disagreements and missing evidence. Do not polish uncertainty into apparent fact.
- State freshness and access limits explicitly. Repetition by dependent sources is not independent corroboration.

## Visual presentation

- Use professional Markdown, consistent heading depth, focused paragraphs, and compact tables.
- Use a table for repeated dimensions, a tree for hierarchy, a flow or timeline for sequence, and Mermaid for several interacting components or branches.
- Pad Markdown tables so their source remains readable.
- Include a readable Mermaid or ASCII diagram proactively when a material relationship, flow, or lifecycle is harder to understand in prose alone.
- Keep diagrams small, label important relationships, avoid unexplained abbreviations, and interpret every diagram in prose so the document remains useful when it does not render.
- Prefer roughly six to twenty diagram elements; split larger diagrams at natural boundaries.
- Use symbols only from the skill's `visual-language.md` reference, at most one leading symbol per heading, and never as the sole carrier of meaning. The visual-language reference is the authoritative source; when any other file uses a different symbol for the same role, the visual-language assignment wins.
- Prefer precise prose over decorative callouts, icon density, wide matrices, raw discovery dumps, and long unbroken sections.

## Final handoff

Return a concise chat summary that names:

- The reader-facing document path.
- The central conclusion or current status.
- Material evidence or validation limitations.
- The most useful next action.

Do not paste the full durable document into the conversation unless the user requests it.

## Shared quality gate

- [ ] The output is a durable Markdown document when required by this standard and the skill-specific contract.
- [ ] The instance path uses `<output-base>/<skill>-YY-MM-DD-<suffix>` and did not overwrite existing work.
- [ ] Purpose, audience/use, scope, evidence boundary, and material limitations are visible near the beginning.
- [ ] The opening leads with the central answer or mental model.
- [ ] Equivalent sections follow the shared output spine and retain the common role in their headings.
- [ ] The structure follows comprehension dependencies rather than discovery order.
- [ ] Consequential statements are linked or explicitly labeled by evidence role.
- [ ] Conflicts, assumptions, risks, and unknowns remain visible.
- [ ] Visuals materially improve understanding, work in Mermaid or ASCII as appropriate, and have prose interpretation.
- [ ] Local links are precise, concise, and relative where practical.
- [ ] The ending provides an actionable next step and stopping condition.
- [ ] Generated artifacts remain outside source control.
- [ ] The final chat handoff includes the output path and does not substitute for the document.
- [ ] Opaque identifiers from sources (codes, IDs, shorthand) are defined before first use and linked to their origin.