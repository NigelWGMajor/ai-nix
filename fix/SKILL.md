---
name: fix
description: Diagnose a symptom, bug, error, or unexpected behavior through multi-path hypothesis triage. Use when something is broken, failing, or behaving unexpectedly and the cause is not immediately obvious. Generates competing hypotheses, gathers evidence for and against each, eliminates systematically, and proposes a fix with risk assessment. The output can be passed to act for ticket creation or directly to implementation. Do not use for feature design, code review, or general exploration — use nix, wiz, or cop for those.
---

# FIX Triage and Diagnosis

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the triage workflow.
## `new` fresh-run override

When `new` is a standalone invocation keyword (for example, `/nix new <topic>`), start a fresh run. The ordinary word `new` within a topic or other prose does not enable this mode. This reset applies only to prior skill-run artifacts: continue to inspect the existing codebase, user-supplied material, and authoritative systems normally.

Do not inspect, resume, or reuse a prior `.data/` or `.dac/` run. After resolving the exact workspace folder this run would otherwise write into or update, if that folder already exists, first rename it in the same parent using the first unused alphabetic suffix: `<name>-a`, `<name>-b`, ..., `<name>-z`, then `<name>-aa`, and so on. Never overwrite, merge, or archive unrelated folders or folders used solely as read-only inputs. If the fresh run creates a distinct new destination or is read-only, do not rename anything.

The archive move needs the same local-write approval as writing the destination. Report the old and archive paths, then continue as though that run never existed. `new` does not authorize source changes, Git mutations, tests, deployment, Jira, or other remote actions.

Trace a symptom to its root cause through structured multi-path triage:

`Capture -> Hypothesize -> Investigate -> Narrow -> Diagnose -> Prescribe`

Form competing hypotheses, test them against evidence in parallel, eliminate systematically, and converge on a confirmed root cause with a proposed fix. Where nix explores outward from a subject, fix narrows inward from a symptom.

## Standalone contract

- Contain the entire method in this package.
- Never require, invoke, or read RECIPE, LIT, KIT, NIX, WIZ, their phase skills, their caches, or their outputs at runtime.
- Do not require subagents, mentor agents, special slash commands, or model routing.
- Use available workspace tools and repository guidance without depending on a particular tool name.
- Default Quick work to a response in the conversation. Create a durable workspace document for Standard and Deep work unless the user explicitly requests chat-only output.
- Remain read-only unless the user separately and explicitly asks for a mutation. Proposing a fix does not authorize implementing it.

## Load diagnostic guidance

At the start of every triage:

1. Enumerate every Markdown file directly under `references/`.
2. Read each file completely before beginning investigation.
3. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Its current assignments override any symbols hardcoded in templates, output contracts, or other reference files.
4. Read [references/prefactoring-development-guidance.md](references/prefactoring-development-guidance.md) and apply relevant design and testing guidance when diagnosing code failures.
5. Use [references/jira-integration.md](references/jira-integration.md) to interpret Jira fields and conventions when the symptom originates from a ticket.
6. Also read repository-local instructions such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and more specific guidance in the affected directories.

## Begin or resume

Determine whether the request identifies an existing FIX instance. If an `<output-base>/fix-*` directory exists:

1. Read its `00-control.md` first.
2. Ask the user whether to **resume** the prior triage or **start a new instance**.
3. If resuming, verify that the symptom context still applies, continue from the recorded next safe action, and do not repeat completed stages or re-eliminated hypotheses.
4. If more than one instance is plausible, list them and ask which to use.

## Resolve the symptom

Apply this precedence:

1. **Explicit symptom**: error message, stack trace, failing test, log excerpt, user report, or incident description supplied in the prompt.
2. **Ticket reference**: Jira issue, GitHub issue, or incident report describing the problem. Fetch and read it.
3. **Current state**: failing test suite, broken build, or unexpected behavior observable in the workspace.
4. With no clear symptom, ask one concise question. Do not guess at what is broken.

Record the resolved symptom and its provenance in `00-control.md`.
For code investigation, read [references/codebase-scope.md](references/codebase-scope.md) before assuming the active checkout contains the complete diagnostic surface.


## Capture external references

Before deep investigation, ensure that all external sources are available locally as stable markdown snapshots.

### Gather links

Ask the user whether any Atlassian pages (Confluence, Jira tickets), incident reports, monitoring dashboards, log excerpts, or other external links should be captured for the triage. Accept URLs from the prompt, from the user's response, or discovered inside error messages and ticket descriptions.

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
   type: "<confluence | jira-issue | incident | monitoring | log | web | other>"
   ---
   ```

4. **Preserve** the document's semantic structure (headings, lists, tables, code blocks). Strip navigation chrome, sidebars, and boilerplate.

5. **Verify capture completeness.** After writing the file (whether by converter or manually), scan it for empty or placeholder content blocks (blank code fences, empty table cells that clearly held content, stub sections). If any are found:
   - First, re-examine the raw fetched content (HTML or API response) to determine whether the content was present in the source but lost during conversion. If so, fix the conversion and rewrite the file.
   - If the source itself contained no content (the block was genuinely empty on the page), or the content is an image/attachment with no text equivalent, append a `## Capture gaps` section at the end of the captured file listing each empty block with its heading context, the reason (e.g., "embedded image", "empty on source page"), and a note about whether re-fetching could recover it.

6. For Jira issues, include key fields (summary, status, type, assignee, labels, description, and acceptance criteria) as structured frontmatter or a leading metadata table.
7. For Confluence pages, preserve the page hierarchy context (space, parent page) in frontmatter when available.

### Use captured documents

Once captures are complete, treat the `./md` snapshots as the working copies for all subsequent investigation. Cite them by their local path. Note the capture date as a freshness limitation in evidence records.

## Choose depth

- **Quick**: use for a single obvious failure with a clear error message. Produce a concise diagnosis in the conversation. Omit instance creation unless the user asks to save the result.
- **Standard**: use by default. Multi-path triage with hypothesis tracking, evidence tables, and a durable diagnosis document.
- **Deep**: use for complex cross-system failures, intermittent issues, or symptoms with multiple plausible causes across service boundaries. Broader investigation, more hypotheses, environment reproduction steps.

Never inflate a simple error into a deep investigation. Never compress a cross-system failure into a quick diagnosis.

## Create the triage instance

For Standard or Deep work, initialize a durable triage instance before substantial investigation.
Immediately before creating its folder, ask the user: `Optional folder context suffix (for example, a short title)? Leave blank to omit it.` Use the response under the shared output-location naming rule.

### Resolve the workspace root

Before creating the instance, use the initialization script which automatically resolves the workspace root:

```bash
python <skill-directory>/scripts/init_instance.py \
  --workspace <workspace-root> \
  --symptom "<symptom-description>" \
  --depth <quick|standard|deep>
```

The script resolves workspace root in this order:
1. Explicit `--workspace` argument (if provided)
2. VSCode workspace via MCP tool (if available)
3. Repository root via git: `git rev-parse --show-toplevel`
4. OS-specific fallback: `C:\.data` (Windows), `~/Library/Application Support/claude-skills` (macOS/Linux)

The workspace root is the repository root (containing `.git`), NOT the terminal's current working directory.

**Trunk workspace preference:** when multiple workspace roots are available (e.g. a multi-root VS Code workspace), check each for a `trunk` folder. If exactly one workspace root contains a `trunk` folder, use that root when resolving the output base regardless of which root the current file or working directory belongs to.

If the Python script is unavailable, manually create the instance as `<output-base>/fix-YY-MM-DD-<suffix>`, using the next available lowercase alphabetic suffix. Create the output base when needed. Never overwrite an existing instance or modify `.gitignore`.

Maintain:

- `00-control.md`: identity, symptom, scope, depth, hypotheses, progress, and next safe action.
- `01-evidence.md`: material sources, observations, reproduction steps, and limitations.
- `02-triage.md`: hypothesis register, evidence for/against, elimination log, and diagnosis.
- `Findings.md`: professional reader-facing diagnosis report.

Checkpoint `00-control.md` after each meaningful stage and before stopping. For Quick work, create an instance only when the user asks to save the result.

## Maintain evidence discipline

Classify material claims:

- **Observed**: directly inspected in code, output, logs, or tool results.
- **Claimed**: asserted by documentation, ticket, error message, or another narrative source.
- **Inferred**: derived from evidence; state the reasoning boundary.
- **Unknown**: missing, conflicting, inaccessible, or outside scope.

Cite repository evidence as `path/to/file.ext:line` or `path/to/file.ext:start-end`. Never claim a test passed or failed unless the result was observed. State when evidence is inaccessible or stale.

## Run the six-stage triage

### 1. Capture

Document the symptom precisely before forming hypotheses:

- What is the observable failure? (error message, wrong output, crash, hang, data corruption)
- When does it occur? (always, intermittently, after a specific change, under load)
- Where does it manifest? (which component, endpoint, test, environment)
- Who reported it and what is the impact?
- What changed recently? (commits, deployments, configuration, dependencies, data)
- What has already been tried?

Record reproduction steps when available. Distinguish the symptom from its interpreted cause.

### 2. Hypothesize

Generate competing hypotheses for the root cause:

- Use hypothesis IDs: H-01, H-02, H-03, etc.
- Each hypothesis must be a specific, testable claim about the cause.
- Order by prior probability (most likely first) based on the symptom and recent changes.
- Include at least one non-obvious hypothesis — the first guess is often wrong.
- For each, state what evidence would confirm it and what evidence would eliminate it.

Do not commit to a single hypothesis. The value of fix is maintaining multiple paths until evidence forces convergence.

### 3. Investigate

Gather evidence for and against each hypothesis:

- Trace the execution path from entry point to the point of failure.
- Inspect the code at the failure site and its immediate dependencies.
- Check recent changes (git log, diff) to the affected area.
- Inspect relevant tests — do they cover this path? Do they pass?
- Check configuration, environment, data state, and external dependencies.
- Look for related issues, known bugs, or similar past failures.

Record each piece of evidence with its hypothesis link (supports H-01, contradicts H-02, neutral).

### 4. Narrow

Systematically eliminate hypotheses:

- For each hypothesis, weigh the evidence for and against.
- Eliminate hypotheses contradicted by strong evidence. Record why.
- Merge hypotheses that turn out to be aspects of the same cause.
- If all hypotheses are eliminated, return to Hypothesize with new information.
- If multiple hypotheses survive, identify the distinguishing test for each.

The elimination log is a key output — it prevents revisiting dead ends.

### 5. Diagnose

Confirm the root cause:

- State the confirmed or most-supported root cause with evidence.
- Explain the causal chain from root cause to observed symptom.
- Identify contributing factors (conditions that made the bug possible but are not the root cause).
- State confidence: High (confirmed by reproduction or code proof), Medium (strong evidence but not reproduced), Low (best available hypothesis).
- Note what remains unknown.

### 6. Prescribe

Propose a fix with risk assessment:

- Describe the minimal change that addresses the root cause.
- Identify the files, symbols, and components to change.
- Assess risk: what could the fix break? What are the rollback options?
- Define validation: how to confirm the fix works (specific test, reproduction scenario, expected output).
- Suggest preventive measures: what test or guard would have caught this earlier?
- If the fix is complex, recommend creating a ticket (via `/act`) rather than implementing immediately.

Do not implement the fix. Proposing is not permission to change code.

## Apply paired self-checks

- **Capture <-> Diagnose**: Does the diagnosis explain all aspects of the captured symptom? Are there symptom details the diagnosis cannot account for?
- **Hypothesize <-> Narrow**: Were all plausible hypotheses considered? Was any eliminated on insufficient evidence?
- **Investigate <-> Prescribe**: Does the proposed fix address the confirmed root cause without introducing the conditions for a related failure?

Correct material failures before answering. Do not narrate the self-check unless it reveals a limitation the user should know.

## Compose the output

Before drafting a Standard or Deep report:

1. Read [references/documentation-standard.md](references/documentation-standard.md) and apply its shared document, link, visual, handoff, and workspace-storage rules.
2. Read [references/output-contract.md](references/output-contract.md) for FIX-specific triage presentation rules.
3. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Its current assignments override any symbols hardcoded in templates, output contracts, or other reference files.
4. Adapt [assets/findings-template.md](assets/findings-template.md) to the symptom; do not force empty sections. Replace any template symbols with the current assignments from visual-language.md.

For Quick output, follow the same evidence and visual rules without loading or reproducing a large template unnecessarily.

Lead with the diagnosis and proposed fix, then make the triage trace easy to scan. Write Standard and Deep output to `Findings.md` in the initialized instance and return only the concise handoff described by the shared standard.

## Complete the triage

Report:

- The confirmed or most-supported root cause.
- Confidence level and evidence limitations.
- The proposed fix and its risk.
- The recommended validation approach.
- Material unknowns or alternative causes that could not be eliminated.

## Self-improvement signals

After real use, record recurring friction in `00-control.md`, such as a missed hypothesis pattern, an evidence source that needed a new tool, or a triage stage that was too broad. Recommend a narrow skill adjustment rather than silently editing the installed skill during a triage.
