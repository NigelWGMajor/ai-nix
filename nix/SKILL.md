---
name: nix
description: Explain or analyze the current workspace, an explicitly supplied path or artifact set, or a subject described in the prompt through a lightweight six-stage Reflect, Explore, Connect, Imagine, Produce, and Empower cycle. Use when the user invokes nix, asks for broad workspace orientation, wants a coherent explanation of an unfamiliar system or topic, needs relationships and implications mapped, or wants evidence-grounded options and actionable understanding. Do not trigger merely because a request concerns the Nix language, NixOS, or the Nix package manager; do not use for direct implementation, bug fixing, pull-request review, or a narrowly factual lookup unless the user explicitly asks to use nix. Explicit invocation overrides task-shape exclusions but never authorizes mutation.
---

# NIX Workspace Analysis

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the analysis workflow.

Turn a workspace or supplied subject into a professional, evidence-grounded explanation using one compact reasoning cycle:

`Reflect -> Explore -> Connect -> Imagine -> Produce -> Empower`

Build a usable mental model, not an inventory dump. Keep the analysis lightweight, visually navigable, and proportionate to the request.

## Standalone contract

- Contain the entire method in this package.
- Never require, invoke, or read RECIPE, LIT, KIT, their phase skills, their caches, or their outputs at runtime.
- Do not require subagents, mentor agents, special slash commands, or model routing.
- Use available workspace tools and repository guidance without depending on a particular tool name.
- Default Compact work to a response in the conversation. Create a durable workspace document for Standard and Deep work unless the user explicitly requests chat-only output.
- Treat explanation and analysis as read-only. “Produce” means produce the explanation, not modify the subject.
- Use [references/jira-integration.md](references/jira-integration.md) to interpret Jira fields and conventions when the subject includes Jira or Atlassian sources.

## Begin or resume

Determine whether the request identifies an existing NIX instance. If a `.data/nix-*` directory exists under the workspace root:

1. Read its `00-control.md` first.
2. Ask the user whether to **resume** the prior analysis or **start a new instance**.
3. If resuming, verify that referenced sources still exist, continue from the recorded next safe action, and do not repeat completed stages.
4. If more than one instance is plausible, list them and ask which to use.

## Resolve the subject

Apply this precedence:

1. Use explicit prompt parameters as the analysis goal and scope.
2. Treat supplied paths, files, URLs, issue identifiers, or pasted material as named evidence or subjects.
3. With no parameters, analyze the current workspace, starting from the active working directory and configured workspace roots.

Do not require a Git repository. When Git exists, record branch, HEAD, and dirty-state facts only when they materially affect the explanation. Do not fetch or mutate Git state.

For a broad workspace request:

- Read applicable agent or repository guidance first.
- Identify the workspace boundary before exploring deeply.
- Prefer the repository's configured structural discovery facilities; fall back to ordinary file and text discovery when necessary.
- Include source, documentation, configuration, tests, build/deploy definitions, data contracts, and history only in proportion to the question.

If multiple roots or subjects are equally plausible and choosing one would materially change the answer, ask one concise question. Otherwise use the active directory or most explicit subject and state the assumption.

Do not silently add unrelated internet research. Use external sources when the request asks for them, the subject inherently requires current external facts, or local evidence explicitly depends on them. State the local and external evidence boundaries.

## Capture external references

Before deep analysis, ensure that all external sources are available locally as stable markdown snapshots.

### Gather links

Ask the user whether any Atlassian pages (Confluence, Jira), web documents, API references, or other external links should be included in the analysis. Accept URLs from the prompt, from the user's response, or discovered inside supplied documents.

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

Once captures are complete, treat the `./md` snapshots as the working copies for all subsequent analysis. Cite them by their local path rather than the original URL, but preserve the original URL in frontmatter for traceability. Note the capture date as a freshness limitation in evidence records.

## Choose depth

- **Compact**: use for a narrow subject. Give each stage one focused paragraph or combine adjacent stages when their distinction would add no value.
- **Standard**: use by default. Make all six stages visible and keep the report skimmable.
- **Deep**: use when the user asks for thorough analysis or the subject has several interacting systems, decisions, or evidence conflicts.

Never inflate a small question into a workspace-wide audit. Never compress a consequential ambiguity into an unsupported summary.

## Create the analysis instance

For Standard or Deep work, initialize a durable analysis instance before substantial exploration:

```text
python <skill-directory>/scripts/init_instance.py --workspace <workspace-root> --subject "<subject>" --question "<question>" --audience "<audience>" --depth <standard|deep>
```

The initializer creates the next collision-safe `.data/nix-YY-MM-DD-<suffix>` directory under the resolved workspace root. It creates `.data` when needed, never overwrites an existing instance, and copies the reader-facing template to `Findings.md`. Pass the resolved workspace root explicitly; never use an existing ancestor `.data` directory as a workspace marker.

Maintain:

- `00-control.md`: identity, purpose, scope, phase, progress, assumptions, questions, and next safe action.
- `01-evidence.md`: material sources, entry points, roles, freshness, and limitations.
- `02-analysis.md`: concepts, relationships, flows, findings, implications, and unresolved questions.
- `Findings.md`: professional reader-facing explanation.

Checkpoint `00-control.md` after each meaningful stage and before stopping. If the user explicitly requests chat-only output, do not create an instance. For Compact work, create an instance only when the user asks to save the result.

## Maintain evidence discipline

Classify material statements when a reader could mistake interpretation for fact:

- **Observed**: directly inspected in workspace artifacts, command output, or supplied sources.
- **Claimed**: asserted by documentation, comments, issues, commits, or another narrative source.
- **Inferred**: derived from evidence; state the reasoning boundary.
- **Unknown**: unavailable, ambiguous, conflicting, or outside scope.

Use high, medium, or low confidence only when confidence materially helps the reader. Cite local files, symbols, headings, pages, lines, or source links as precisely as practical. Do not imply that repeated claims are independently corroborated.

## Run the six-stage cycle

### 1. Reflect

Frame the analysis before gathering detail:

- Identify the trigger, question, audience, and desired use of the answer.
- State the core subject in one or two sentences.
- Separate symptoms, prompts, or surface structure from the underlying question.
- Define what is in scope, out of scope, and sufficient for this run.
- Surface constraints, assumptions, and the exit criterion.

Do not block on minor omissions. Use a bounded assumption and label it unless a missing answer would change the scope or conclusion materially.

### 2. Explore

Build the evidence landscape:

- Locate authoritative sources and likely entry points.
- Inspect existing concepts, components, conventions, tests, interfaces, tools, and history relevant to the subject.
- Distinguish sources of truth from derived, generated, stale, or narrative material.
- Note contradictions, missing evidence, and areas where exploration is yielding diminishing returns.

Prefer targeted retrieval over broad dumping. Retain stable evidence locations and compact findings rather than filling the final response with raw source content.

### 3. Connect

Turn the evidence into a system model:

- Map hierarchy, ownership, boundaries, dependencies, call or data flows, state transitions, and lifecycle stages.
- Identify sources of truth, persistence, caches, integration points, consumers, and reverse dependencies where relevant.
- Explain how the important pieces cooperate and what can break when one changes.
- Show discovered relationships that are not obvious from any single source.

Choose the smallest useful visualization: a table for repeated comparisons, a tree for hierarchy, a flow or timeline for sequence, or Mermaid for a relationship that is difficult to express linearly. Always interpret the visual in prose.

### 4. Imagine

Explore meaning and possibility without leaving the evidence behind:

- Generate alternative interpretations, designs, explanations, or futures only when the subject contains a real choice or uncertainty.
- Consider simple through sophisticated options, important counterfactuals, edge cases, failure modes, and non-functional qualities.
- Evaluate maintainability, usability, performance, flexibility, and operational consequences when relevant.
- State which possibility is best supported and what evidence or decision could change it.

For a pure explanatory request, focus Imagine on implications, likely evolution, hidden assumptions, and useful counterfactuals rather than forcing artificial solution options.

### 5. Produce

Synthesize the answer the user actually needs:

- Present the central mental model and key conclusions.
- Reconcile terminology while preserving meaningful distinctions.
- Rank findings, options, or implications by decision value rather than source volume.
- Resolve evidence conflicts transparently or retain them as open questions.
- Make recommendations only when criteria and tradeoffs are explicit.

Do not write code, edit files, or execute a proposed change merely because the cycle reaches Produce. A separate user request is required for mutation.

### 6. Empower

Make the understanding usable:

- Explain how to navigate the subject or verify the model.
- Identify the best next place to read, inspect, decide, or validate.
- Provide examples, checkpoints, or success criteria when useful.
- Separate safe next steps, user decisions, external dependencies, and actions requiring mutation approval.
- Make the first next step immediately actionable.

Avoid generic “continue investigating” advice. Name the target, purpose, expected evidence, and stopping condition.

## Apply paired self-checks

Replace RECIPE-style mentor agents with one lightweight internal pass:

- **Reflect <-> Connect**: Does the system model answer the framed question without losing a material dependency or expanding scope accidentally?
- **Explore <-> Imagine**: Are possibilities grounded in observed evidence, and did exploration miss a source needed to evaluate them?
- **Produce <-> Empower**: Is the synthesis accurate and complete enough to use, and do the next steps expose rather than hide uncertainty?

Correct material failures before answering. Do not narrate the self-check unless it reveals a limitation the user should know.

## Compose the output

Before drafting a Standard or Deep response:

1. Read [references/documentation-standard.md](references/documentation-standard.md) and apply its shared document, link, visual, handoff, and workspace-storage rules.
2. Read [references/output-contract.md](references/output-contract.md) for NIX-specific six-stage presentation rules.
3. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Its current assignments override any symbols hardcoded in templates, output contracts, or other reference files.
4. Adapt [assets/findings-template.md](assets/findings-template.md) to the subject; do not force empty sections. Replace any template symbols with the current assignments from visual-language.md.

For Compact output, follow the same evidence and visual rules without loading or reproducing a large template unnecessarily.

For Standard and Deep output, preserve the shared output spine while keeping all six NIX stages visible through the mapped headings in the output contract.

Lead with the answer and orientation, then make the six-stage reasoning trace easy to scan. Write Standard and Deep output to `Findings.md` in the initialized instance and return only the concise handoff described by the shared standard. Use professional Markdown, consistent headings, restrained symbols, and precise links. Keep raw discovery details out of the main narrative unless they change the conclusion.

If the user supplies an explicit output path, honor it and record that path in `00-control.md`. Never overwrite an existing directory, never modify `.gitignore`, and disclose the reader-facing output path.

## Complete the analysis

Apply the shared quality gate in [references/documentation-standard.md](references/documentation-standard.md) and the NIX-specific gate in [references/output-contract.md](references/output-contract.md). Report:

- The central explanation or conclusion.
- The scope and important evidence limits.
- Material unknowns or conflicts.
- The most useful next action.

Recommend a narrow NIX improvement after real use only when recurring friction reveals a missing trigger, stage guardrail, visual role, or output pattern. Do not silently modify the installed skill during an analysis.
