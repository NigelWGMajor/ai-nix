---
name: wiz
description: Review work in progress against its intended outcome by opening an explicit Jira ticket or pull request through available Atlassian, GitHub, or repository integrations, or by deriving the work item and change set from the current Git branch. Use when asked to review a ticket implementation, pull request, branch, diff, or unfinished change and produce an evidence-based Markdown assessment organized as intent, evidence, discovered relationships, ideation, implementation, and realization. Apply bundled development guidance, stay within task scope, cite documents and code lines where feasible, distinguish facts from inference, calibrate severity and confidence, and note strengths as well as concerns.
---

# WIZ Work-in-Progress Review

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the review workflow.
## `new` fresh-run override

When `new` is a standalone invocation keyword (for example, `/nix new <topic>`), start a fresh run. The ordinary word `new` within a topic or other prose does not enable this mode. This reset applies only to prior skill-run artifacts: continue to inspect the existing codebase, user-supplied material, and authoritative systems normally.

Do not inspect, resume, or reuse a prior `.data/` or `.dac/` run. After resolving the exact workspace folder this run would otherwise write into or update, if that folder already exists, first rename it in the same parent using the first unused alphabetic suffix: `<name>-a`, `<name>-b`, ..., `<name>-z`, then `<name>-aa`, and so on. Never overwrite, merge, or archive unrelated folders or folders used solely as read-only inputs. If the fresh run creates a distinct new destination or is read-only, do not rename anything.

The archive move needs the same local-write approval as writing the destination. Report the old and archive paths, then continue as though that run never existed. `new` does not authorize source changes, Git mutations, tests, deployment, Jira, or other remote actions.

## Output location

Resolve `TOOLING_OUTPUT_PATH` before locating or creating durable output. When set, an absolute value is the output base; a value beginning `./` or `.\\` is relative to the resolved repository root (or current folder when no repository is available); reject other relative forms. All standard run paths below are relative to `<output-base>`; do not append a further `.data` segment. When unset, the output base is `<workspace-root>/.data`.

Review the change that is actually in progress against the work it is meant to accomplish. Build a traceable, evidence-grounded assessment from intent through realization using six analytical layers:

`Intent -> Evidence -> Relationships -> Ideation -> Implementation -> Realization`

Produce deeply analyzed findings with traceable ID chains (F-01 -> I-01 -> A-01), calibrated seriousness and confidence, and concrete next actions. Where NIX provides quick discovery of where action is needed, WIZ follows up with the rigorous depth to act on it.

## Standalone contract

- Contain the entire method in this package.
- Never require, invoke, or read RECIPE, LIT, KIT, NIX, their phase skills, their caches, or their outputs at runtime.
- Do not require subagents, mentor agents, special slash commands, or model routing.
- Use available workspace tools and repository guidance without depending on a particular tool name.
- Default Quick work to a response in the conversation. Create a durable workspace document for Standard and Deep work unless the user explicitly requests chat-only output.
- Remain read-only unless the user separately and explicitly asks for a mutation. Treat "open a ticket" or "open a pull request" as fetch/read, not create, edit, comment, approve, or merge.

## Load review guidance

At the start of every review:

1. Enumerate every Markdown file directly under `references/`.
2. Read each file completely before judging the change.
3. Apply only the guidance relevant to the target and its demonstrated relationships. Do not import unrelated process requirements into the review.
4. Also read repository-local instructions such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, ownership rules, and more specific guidance in the affected directories.

Always include [references/prefactoring-development-guidance.md](references/prefactoring-development-guidance.md). Use [references/jira-integration.md](references/jira-integration.md) to interpret Jira fields and conventions where applicable; its Jira-writing procedures do not authorize remote changes.

If guidance conflicts, follow the user's current instructions first, then applicable repository or organizational requirements, then the work item's approved contract, then this skill's bundled guidance. Call out a material conflict instead of silently choosing.

## Begin or resume

Determine whether the request identifies an existing WIZ instance. If an `<output-base>/wiz-*` directory exists:

1. Read its `00-control.md` first.
2. Ask the user whether to **resume** the prior review or **start a new instance**.
3. If resuming, verify that the target ticket/PR/branch still matches, continue from the recorded next safe action, and do not repeat completed layers.
4. If more than one instance is plausible, list them and ask which to use.

## Resolve the review target

Use this precedence:

1. **Explicit Jira issue:** Fetch it using the Atlassian MCP server tools (prefixed `mcp__atlassian__`). If the MCP server is unavailable, advise the user to run `! /mcp` to check status or use `curl` with their MCP credentials. Read the summary, description, acceptance criteria, status, relevant comments or documents, parent/epic, children, and one hop of issue links. Follow deeper links only when they materially constrain scope, behavior, compatibility, rollout, or validation.
2. **Explicit pull request:** Fetch it with the connector matching its host. Read the title, description, target and source refs, commits, changed files and diff, checks, unresolved review context, and linked work items. Fetch linked Jira issues through the Atlassian MCP server when a key or link is present.
3. **Current branch:** Inspect the repository root, branch, HEAD, status, upstream/default branch, recent history, and the merge-base diff. Keep committed, staged, unstaged, and untracked work distinct. Extract a Jira key only from clear evidence such as a conventional branch name, commit, or PR link; never choose among ambiguous keys.

Prefer an explicit user target over inferred context. When both a ticket and PR are available, use the ticket as intent evidence and the PR/diff as implementation evidence.

If no unique target or comparison base can be established, stop and ask for the Jira key, PR, or intended base branch. State what was checked. Do not manufacture a scope from nearby repository activity.

For implementation review:

- Read [references/codebase-scope.md](references/codebase-scope.md) before treating the reviewed repository as the complete change surface.
- **Detect multi-repository workspace**: If codebase-memory-mcp is available, call `mcp__codebase-memory-mcp__list_projects` to discover all indexed projects. For feature reviews (UI surfaces, APIs, product features), automatically search across ALL related projects (e.g., both backend and frontend repos) without requiring explicit instruction. Document each project searched in evidence.


## Capture external references

Before deep analysis, ensure that all external sources are available locally as stable markdown snapshots.

### Gather links

Ask the user whether any Atlassian pages (Confluence, Jira tickets, epics), pull requests, design documents, or other external links should be captured for the review. Accept URLs from the prompt, from the user's response, or discovered inside ticket descriptions and PR bodies.

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

1. **Fetch the full content.**
   - **Confluence pages:** Fetch via the REST API v1 with `?expand=body.storage,version,space,ancestors`. The response's `body.storage.value` is Confluence storage-format HTML, which preserves code blocks, macros, and structured content that higher-level rendering APIs may strip. Save the raw JSON response to a temporary file for the conversion step.
   - **Web pages:** Use WebFetch or curl. Prefer fetching the raw or printer-friendly version when available.
   - **Jira issues:** Use the Atlassian MCP tools or the REST API with fields expanded.

2. **Convert to clean Markdown with code-block preservation.**

   **For Confluence pages, use the bundled converter script:**

   ```text
   python <skill-directory>/scripts/convert_confluence.py <raw-response.json> <workspace>/md/<slugified-title>.md
   ```

   The converter handles all Confluence storage-format elements that standard HTML-to-markdown tools lose — code macros (`ac:structured-macro`), noformat blocks, panels, admonitions, expand/collapse sections, images, and emoticons. It:
   - Extracts code content from `<ac:plain-text-body>` CDATA children before general HTML conversion (the step that tools universally miss).
   - Converts `<ol>` to numbered lists and `<ul>` to bullet lists, with nested list support and proper handling of `<p>` tags inside `<li>` elements.
   - Writes YAML frontmatter with source URL, capture date, title, type, space, parent page, and version.
   - Verifies output: counts source macros vs output code fences, detects empty code blocks, and appends a `## Capture gaps` section if any content was lost.
   - Prints a verification summary showing macro counts, fence counts, and gap status.

   After running the converter, check its summary output. If it reports empty fences or fewer output fences than source macros, investigate before proceeding.

   **For non-Confluence sources**, or when the converter is unavailable, convert manually. Handle these Confluence elements explicitly — they are the most common sources of lost content:

   | Confluence HTML element | Contains | Markdown conversion |
   |---|---|---|
   | `<ac:structured-macro ac:name="code">` | Source code with optional language and title | Fenced code block with language identifier; preserve title as a comment or preceding bold line |
   | `<ac:structured-macro ac:name="noformat">` | Preformatted text (commands, output, config) | Fenced code block (no language) |
   | `<ac:structured-macro ac:name="panel">` | Callout/info panels with body content | Blockquote with panel title as bold first line |
   | `<ac:structured-macro ac:name="info\|note\|warning\|tip">` | Admonition content | Blockquote prefixed with admonition type |
   | `<ac:structured-macro ac:name="expand">` | Collapsible sections | `<details>/<summary>` or a subsection |
   | `<pre>` | Inline preformatted text | Fenced code block |
   | `<ac:plain-text-body>` or `<ac:rich-text-body>` | The actual body content inside macros | Extract the text content; do not discard |
   | `<ac:image>` | Embedded images (no text equivalent) | `<!-- [image: alt-text or filename] -->` placeholder noting the image exists |

   The actual text content inside code and noformat macros lives within a `<ac:plain-text-body>` CDATA child. Extract its text verbatim — do not skip it because it is wrapped in CDATA or nested inside a macro element.

   When using any other conversion library or tool, verify its output against the raw HTML for every code fence in the result. Libraries commonly strip `<ac:structured-macro>` elements entirely because they do not recognize them as standard HTML.

3. **Write the result** (if not already written by the converter) to `./md/<slugified-title>.md` with YAML frontmatter:

   ```yaml
   ---
   source: "<original URL>"
   captured: "<YYYY-MM-DD>"
   title: "<page or issue title>"
   type: "<confluence | jira-issue | jira-epic | web | api-doc | pull-request | other>"
   ---
   ```

4. **Preserve** the document's semantic structure (headings, lists, tables, code blocks). Strip navigation chrome, sidebars, and boilerplate.

5. **Verify capture completeness.** After writing the file (whether by converter or manually), scan it for empty or placeholder content blocks (blank code fences, empty table cells that clearly held content, stub sections). If any are found:
   - First, re-examine the raw fetched content (HTML or API response) to determine whether the content was present in the source but lost during conversion. If so, fix the conversion and rewrite the file.
   - If the source itself contained no content (the block was genuinely empty on the page), or the content is an image/attachment with no text equivalent, append a `## Capture gaps` section at the end of the captured file listing each empty block with its heading context, the reason (e.g., "embedded image", "empty on source page"), and a note about whether re-fetching could recover it.

6. For Jira issues, include key fields (summary, status, type, assignee, labels, description, and acceptance criteria) as structured frontmatter or a leading metadata table.
7. For Confluence pages, preserve the page hierarchy context (space, parent page) in frontmatter when available.

### Use captured documents

Once captures are complete, treat the `./md` snapshots as the working copies for all subsequent analysis. Cite them by their local path rather than the original URL, but preserve the original URL in frontmatter for traceability. Note the capture date as a freshness limitation in `01-evidence.md`.

## Choose depth

- **Quick**: use for a narrow, well-scoped ticket with few changed files. Produce a concise review in the conversation covering all six layers. Omit instance creation unless the user asks to save the result.
- **Standard**: use by default. Produce a durable review document with all six layers visible, traceable finding chains, and an evidence index.
- **Deep**: use when the user asks for thorough analysis or the target has several interacting systems, broad surface area, security implications, or contested design decisions. Increase tracing depth, explore more scope extensions, and apply multi-pass evidence gathering.

Never inflate a small fix into a deep audit. Never compress a security-sensitive or architecturally consequential change into a quick pass.

## Create the review instance

For Standard or Deep work, initialize a durable review instance before substantial exploration.
Immediately before creating its folder, ask the user: `Optional folder context suffix (for example, a short title)? Leave blank to omit it.` Use the response under the shared output-location naming rule.

### Resolve the workspace root

Use the initialization script which automatically resolves the workspace root:

```bash
python <skill-directory>/scripts/init_instance.py \
  --workspace <workspace-root> \
  --target "<ticket-or-pr>" \
  --base "<base-ref>" \
  --depth <quick|standard|deep>
```

The script resolves workspace root in this order:
1. Explicit `--workspace` argument (if provided)
2. VSCode workspace via MCP tool (if available)
3. Repository root via git: `git rev-parse --show-toplevel`
4. Current folder (when there is no repository or configured workspace root)

The workspace root is the repository root (containing `.git`), NOT the terminal's current working directory.

If the Python script is unavailable, manually create the instance as `<output-base>/wiz-YY-MM-DD-<suffix>`, using the next available lowercase alphabetic suffix. Create the output base when needed. Never overwrite an existing instance or modify `.gitignore`.

Maintain:

- `00-control.md`: identity, target, scope, depth, progress, assumptions, questions, and next safe action.
- `01-evidence.md`: material sources, entry points, roles, freshness, and limitations.
- `02-analysis.md`: findings, relationships, ideation, and implementation chains.
- `Findings.md`: professional reader-facing review.

Checkpoint `00-control.md` after each meaningful layer and before stopping. If the user explicitly requests chat-only output, do not create an instance. For Quick work, create an instance only when the user asks to save the result.

## Establish the scope envelope

Write a short scope contract before reviewing details:

- Intended user or system outcome.
- Acceptance criteria and explicit non-goals.
- Target branch/base and included change states.
- Affected surfaces named by the ticket or diff.
- Material unknowns and inaccessible evidence.

Review the changed code plus only the adjacent code needed to understand contracts, callers, consumers, state, data flow, tests, configuration, migration, security, and rollout effects.

Do not report unrelated cleanup or pre-existing defects. Extend beyond the immediate diff only when a demonstrated relationship could affect correctness, security, privacy, data integrity, compatibility, deployment, rollback, or the stated acceptance criteria. Label each extension **Scope extension** and give the evidence-based reason.

## Maintain evidence discipline

Classify material claims:

- **Observed**: directly inspected in code, output, or tool results.
- **Claimed**: asserted by documentation, ticket, comment, PR, or another narrative source.
- **Inferred**: derived from evidence; state the reasoning boundary.
- **Unknown**: missing, conflicting, inaccessible, or outside scope.

Cite repository evidence as `path/to/file.ext:line` or `path/to/file.ext:start-end`. Use Markdown links when the renderer supports stable line anchors. Cite symbols in addition to lines when that makes the evidence easier to relocate. Never cite a line, test result, relationship, or requirement that was not inspected. State when evidence is inaccessible, stale, generated, or graph-derived but not directly verified.

Prefer repository-aware graph tools for symbol discovery, call paths, dependencies, and impact analysis when available. Verify material graph claims against the current checked-out files because indexes may be stale. Use text search for literals, configuration, documentation, and gaps in graph coverage.

Do not claim tests or checks passed unless their results were observed. Distinguish **passed**, **failed**, **blocked**, and **not run**.

Record good decisions with the same specificity used for concerns. Note clear intent, cohesive boundaries, appropriate abstractions, readable tests, safe compatibility handling, explicit failures, limited scope, or other strengths only when evidence supports them.

## Run the six-layer review

### 1. Intent

Establish the scope and contract for the review:

- Intended user or system outcome.
- Acceptance criteria and explicit non-goals.
- Target branch/base and included change states.
- Affected surfaces named by the ticket or diff.
- Material unknowns and inaccessible evidence.
- Ambiguities or conflicts that prevent a confident judgment.
- Links to the primary ticket, PR, and governing documents.

### 2. Evidence

Gather and classify all material observations:

- **Multi-project discovery**: When multiple indexed projects are detected (via list_projects), search each relevant project systematically. For product features, this typically means both backend (APIs, database) and frontend (UI components, routes) projects. Use graph search, code search, glob, and grep across all projects to ensure comprehensive coverage.
- **Strengths** (G-XX): good decisions with specific evidence.
- **Concerns** (F-XX): each with seriousness, confidence, evidence class, citations, and impact on the stated intent.
- **Evidence gaps**: missing or inaccessible evidence and why it matters.

Trace the smallest useful path from entry point to observable outcome across all relevant projects. Inspect relevant tests and contracts. Compare intended names, inputs, outputs, invariants, errors, side effects, transaction behavior, idempotency, compatibility, and validation with the implementation. When searching multiple projects, document evidence from each project separately in the evidence map.

### 3. Discovered relationships

Map the relationships that affect correctness, security, or completion:

- Callers, consumers, contracts, state, data flow, test coverage, deployment, and issue dependencies.
- Use relationship IDs (R-XX) and link them to the findings they affect.
- Label scope extensions explicitly with the evidence-based reason.

### 4. Ideation

Propose directions and alternatives for each concern:

- Link each idea (I-XX) to the finding it addresses (I-01 -> F-01).
- State the recommended direction, viable alternatives, tradeoffs, and confidence.
- Keep optional ideas visibly separate from changes required to meet intent.

### 5. Implementation

Define the smallest concrete change for each recommendation:

- Link each action (A-XX) to the idea it implements (A-01 -> I-01).
- Name likely files, symbols, tests, and compatibility or rollback considerations.
- Do not imply that a recommendation has already been implemented.

### 6. Realization

Assess the overall state:

- Acceptance criteria: met, partially met, not met, or unable to verify — with evidence.
- Tests and checks: passed, failed, blocked, or not run — naming what was observed.
- Remaining risks and focused follow-ups.
- Positive summary of what the work already accomplishes well.

## Apply paired self-checks

Replace external review with one lightweight internal pass:

- **Intent <-> Realization**: Does the realization assessment answer every acceptance criterion from the intent? Are there criteria that could not be verified?
- **Evidence <-> Ideation**: Are recommendations grounded in observed evidence? Did evidence gathering miss a source needed to evaluate an idea?
- **Relationships <-> Implementation**: Do proposed changes account for all discovered callers, consumers, and dependencies?

Correct material failures before answering. Do not narrate the self-check unless it reveals a limitation the reviewer should know.

## Compose the output

Before drafting a Standard or Deep review:

1. Read [references/documentation-standard.md](references/documentation-standard.md) and apply its shared document, link, visual, handoff, and workspace-storage rules.
2. Read [references/output-contract.md](references/output-contract.md) for WIZ-specific six-layer presentation rules.
3. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Its current assignments override any symbols hardcoded in templates, output contracts, or other reference files.
4. Adapt [assets/findings-template.md](assets/findings-template.md) to the target; do not force empty sections. Replace any template symbols with the current assignments from visual-language.md.

For Quick output, follow the same evidence and visual rules without loading or reproducing a large template unnecessarily.

For Standard and Deep output, preserve the shared output spine while keeping all six WIZ layers visible through the mapped headings in the output contract.

Lead with the overall assessment and orientation, then make the six-layer reasoning trace easy to scan. Write Standard and Deep output to `Findings.md` in the initialized instance and return only the concise handoff described by the shared standard. Use professional Markdown, consistent headings, restrained symbols, and precise links. Keep raw discovery details out of the main narrative unless they change the conclusion.

## Complete the review

Apply the shared quality gate in [references/documentation-standard.md](references/documentation-standard.md) and the WIZ-specific gate in [references/output-contract.md](references/output-contract.md). Report:

- The overall assessment.
- The scope and important evidence limits.
- The most serious concerns and notable strengths.
- The most useful next action.

## Self-improvement signals

After real use, record recurring friction in `00-control.md`, such as a missed scope-extension pattern, an evidence gap that needed a new graph query, an overly rigid finding template, or a guidance section that produced false positives. Recommend a narrow skill adjustment rather than silently editing the installed skill during a review.
