---
name: val
description: Evaluate the effectiveness of a solution by designing test strategies, generating test data and test cases, creating test plans, and assessing coverage. Use when asked to validate an implementation, design a test approach, generate test data, create a test plan, or assess whether a solution meets its acceptance criteria. Do not use for implementing the solution itself, code review, or general exploration — use cop for code review and nix or wiz for exploration.
---

# VAL Validation Design

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the validation workflow.
## `new` fresh-run override

When `new` is a standalone invocation keyword (for example, `/nix new <topic>`), start a fresh run. The ordinary word `new` within a topic or other prose does not enable this mode. This reset applies only to prior skill-run artifacts: continue to inspect the existing codebase, user-supplied material, and authoritative systems normally.

Do not inspect, resume, or reuse a prior `.data/` or `.dac/` run. After resolving the exact workspace folder this run would otherwise write into or update, if that folder already exists, first rename it in the same parent using the first unused alphabetic suffix: `<name>-a`, `<name>-b`, ..., `<name>-z`, then `<name>-aa`, and so on. Never overwrite, merge, or archive unrelated folders or folders used solely as read-only inputs. If the fresh run creates a distinct new destination or is read-only, do not rename anything.

The archive move needs the same local-write approval as writing the destination. Report the old and archive paths, then continue as though that run never existed. `new` does not authorize source changes, Git mutations, tests, deployment, Jira, or other remote actions.

## Output location

Resolve `TOOLING_OUTPUT_PATH` before locating or creating durable output. When set, an absolute value is the output base; a value beginning `./` or `.\\` is relative to the resolved repository root (or current folder when no repository is available); reject other relative forms. All standard run paths below are relative to `<output-base>`; do not append a further `.data` segment. When unset, the output base is `<workspace-root>/.data`.

Evaluate whether a solution actually does what it should through structured validation design:

`Scope -> Design -> Generate -> Execute -> Assess`

Produce test strategies, test cases, test data, and coverage assessments that prove a solution works — or reveal where it doesn't. Where cop reviews code quality and wiz reviews intent alignment, val answers "does this actually work?"

## Standalone contract

- Contain the entire method in this package.
- Never require, invoke, or read RECIPE, LIT, KIT, NIX, WIZ, their phase skills, their caches, or their outputs at runtime.
- Do not require subagents, mentor agents, special slash commands, or model routing.
- Use available workspace tools and repository guidance without depending on a particular tool name.
- Default Quick work to a response in the conversation. Create a durable workspace document for Standard and Deep work unless the user explicitly requests chat-only output.
- Generating test code requires explicit user approval. Proposing test cases does not authorize writing them.

## Load validation guidance

At the start of every validation:

1. Enumerate every Markdown file directly under `references/`.
2. Read each file completely before designing validation.
3. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Its current assignments override any symbols hardcoded in templates, output contracts, or other reference files.
4. Read [references/prefactoring-development-guidance.md](references/prefactoring-development-guidance.md) and apply its testing guidance when designing validation strategies.
5. Use [references/jira-integration.md](references/jira-integration.md) to interpret Jira fields and acceptance criteria when the validation target originates from a ticket.
6. Also read repository-local instructions such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, test conventions, and existing test infrastructure documentation.

## Begin or resume

Determine whether the request identifies an existing VAL instance. If an `<output-base>/val-*` directory exists:

1. Read its `00-control.md` first.
2. Ask the user whether to **resume** the prior validation or **start a new instance**.
3. If resuming, verify that the target implementation still matches, continue from the recorded next safe action, and do not repeat completed stages or re-execute already-run tests.
4. If more than one instance is plausible, list them and ask which to use.

## Resolve the validation target

Apply this precedence:

1. **Explicit target**: a named implementation, feature, fix, migration, or API to validate.
2. **Ticket reference**: Jira issue or PR with acceptance criteria to validate against.
3. **Recent change**: the current branch diff or uncommitted work as the target.
4. **Pre-implementation**: a design or spec to create a validation strategy for, before code is written.
5. With no clear target, ask one concise question. Do not guess at what needs validation.

Record the resolved target and its provenance in `00-control.md`.

## Capture external references

Before deep analysis, ensure that all external sources are available locally as stable markdown snapshots.

### Gather links

Ask the user whether any Atlassian pages (Confluence, Jira tickets), API specs, test reports, monitoring data, or other external links should be captured for the validation design. Accept URLs from the prompt, from the user's response, or discovered inside ticket descriptions and specifications.

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
   type: "<confluence | jira-issue | api-spec | test-report | web | other>"
   ---
   ```

4. **Preserve** the document's semantic structure (headings, lists, tables, code blocks). Strip navigation chrome, sidebars, and boilerplate.

5. **Verify capture completeness.** After writing the file (whether by converter or manually), scan it for empty or placeholder content blocks (blank code fences, empty table cells that clearly held content, stub sections). If any are found:
   - First, re-examine the raw fetched content (HTML or API response) to determine whether the content was present in the source but lost during conversion. If so, fix the conversion and rewrite the file.
   - If the source itself contained no content (the block was genuinely empty on the page), or the content is an image/attachment with no text equivalent, append a `## Capture gaps` section at the end of the captured file listing each empty block with its heading context, the reason (e.g., "embedded image", "empty on source page"), and a note about whether re-fetching could recover it.

6. For Jira issues, include key fields (summary, status, type, assignee, labels, description, and acceptance criteria) as structured frontmatter or a leading metadata table.
7. For Confluence pages, preserve the page hierarchy context (space, parent page) in frontmatter when available.

### Use captured documents

Once captures are complete, treat the `./md` snapshots as the working copies for all subsequent analysis. Cite them by their local path. Note the capture date as a freshness limitation in evidence records.

## Choose depth

- **Quick**: use for a narrow, well-specified feature with clear acceptance criteria. Produce a concise test plan in the conversation.
- **Standard**: use by default. Comprehensive test strategy with test cases, coverage matrix, and generated test data.
- **Deep**: use for high-risk changes, security-sensitive features, data migrations, or multi-system integrations. Decision tables, boundary analysis, failure injection scenarios, and generated fixtures.

Never inflate a simple validation into a deep test suite design. Never compress a security-sensitive change into a quick checklist.

## Create the validation instance

For Standard or Deep work, initialize a durable validation instance before substantial design.

### Resolve the workspace root

Before creating the instance, use the initialization script which automatically resolves the workspace root:

```bash
python <skill-directory>/scripts/init_instance.py \
  --workspace <workspace-root> \
  --target "<target-description>" \
  --criteria "<acceptance-criteria>" \
  --depth <standard|deep>
```

The script resolves workspace root in this order:
1. Explicit `--workspace` argument (if provided)
2. VSCode workspace via MCP tool (if available)
3. Repository root via git: `git rev-parse --show-toplevel`
4. OS-specific fallback: `C:\.data` (Windows), `~/Library/Application Support/claude-skills` (macOS/Linux)

The workspace root is the repository root (containing `.git`), NOT the terminal's current working directory.

**Trunk workspace preference:** when multiple workspace roots are available (e.g. a multi-root VS Code workspace), check each for a `trunk` folder. If exactly one workspace root contains a `trunk` folder, use that root when resolving the output base regardless of which root the current file or working directory belongs to.

If the Python script is unavailable, manually create the instance as `<output-base>/val-YY-MM-DD-<suffix>`, using the next available lowercase alphabetic suffix. Create the output base when needed. Never overwrite an existing instance or modify `.gitignore`.

Maintain:

- `00-control.md`: identity, target, scope, depth, progress, and next safe action.
- `01-evidence.md`: requirements, acceptance criteria, existing tests, and infrastructure.
- `02-strategy.md`: test strategy, coverage matrix, risk areas, and test case register.
- `Findings.md`: professional reader-facing validation plan and results.

Checkpoint `00-control.md` after each meaningful stage and before stopping.

## Maintain evidence discipline

Classify material claims:

- **Observed**: directly inspected in code, test output, or tool results.
- **Claimed**: asserted by documentation, ticket, or specification.
- **Inferred**: derived from evidence; state the reasoning boundary.
- **Unknown**: missing, conflicting, inaccessible, or outside scope.

Cite repository evidence as `path/to/file.ext:line`. Never claim a test passed or failed unless the result was observed. Distinguish existing coverage from proposed coverage.

## Run the five-stage cycle

### 1. Scope

Define what needs validation:

- What is the solution and what problem does it solve?
- What are the explicit acceptance criteria? (from ticket, spec, or user)
- What are the implicit quality requirements? (performance, security, compatibility, data integrity)
- What existing tests already cover parts of this?
- What test infrastructure is available? (frameworks, fixtures, test databases, CI)
- What are the highest-risk areas — where is a failure most likely or most costly?

### 2. Design

Create the test strategy:

- Use test case IDs: T-01, T-02, T-03, etc.
- Choose the right test level for each scenario: unit, contract, integration, end-to-end, manual.
- Map acceptance criteria to test cases in a coverage matrix.
- Apply boundary analysis: what are the edge values, limits, and transitions?
- Apply decision tables for complex conditional logic.
- Design negative tests: what should be rejected, fail gracefully, or remain unchanged?
- Design regression tests: what existing behavior must survive the change?
- Identify risks not covered by tests (timing, concurrency, external dependencies, data volume).

### 3. Generate

Produce concrete test artifacts:

- **Test cases**: for each T-XX, specify input, setup, action, expected output, and cleanup.
- **Test data**: generate realistic, representative data that covers normal, boundary, and error cases.
- **Test fixtures**: seed data, mock configurations, or environment setup needed to run the tests.
- **Decision tables**: for complex logic, generate the full input/output matrix.

Format test data as the project's test infrastructure expects (SQL inserts, JSON fixtures, CSV, factory builders, etc.). Match existing test conventions in the repository.

Do not write test code unless explicitly authorized. Present generated artifacts as proposed content.

### 4. Execute

Run or propose running the validation:

- If authorized and safe, execute focused tests and record results.
- Record each test execution: command, environment, HEAD, result, and any generated artifacts.
- Distinguish **passed**, **failed**, **blocked**, **skipped**, and **not run**.
- For tests that cannot be run locally (integration, E2E, production), specify the execution environment and prerequisites.
- Do not claim a test passed unless the result was observed.

Obtain approval before installing dependencies, using network access, touching databases, or running broad test suites.

### 5. Assess

Evaluate the validation results:

- Coverage: which acceptance criteria are covered, partially covered, or uncovered?
- Confidence: how much does the validation prove? What could still fail?
- Gaps: what risks are not validated? What would a comprehensive validation require?
- Existing test quality: are current tests meaningful or do they test trivialities?
- Recommendations: what tests should be added to the codebase permanently?

## Apply paired self-checks

- **Scope <-> Assess**: Does the assessment cover every acceptance criterion identified in Scope? Are there criteria that could not be validated?
- **Design <-> Execute**: Were all designed test cases attempted or explicitly deferred? Did execution reveal test design gaps?
- **Generate <-> Assess**: Is the generated test data representative enough to support the assessment's confidence level?

Correct material failures before answering. Do not narrate the self-check unless it reveals a limitation the user should know.

## Compose the output

Before drafting a Standard or Deep report:

1. Read [references/documentation-standard.md](references/documentation-standard.md) and apply its shared document, link, visual, handoff, and workspace-storage rules.
2. Read [references/output-contract.md](references/output-contract.md) for VAL-specific validation presentation rules.
3. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Its current assignments override any symbols hardcoded in templates, output contracts, or other reference files.
4. Adapt [assets/findings-template.md](assets/findings-template.md) to the target; do not force empty sections. Replace any template symbols with the current assignments from visual-language.md.

Lead with the coverage assessment and confidence level, then make the test strategy easy to scan. Write Standard and Deep output to `Findings.md` in the initialized instance and return only the concise handoff.

## Complete the validation

Report:

- Coverage level and confidence assessment.
- Test cases designed and their results (if executed).
- Gaps and uncovered risks.
- Recommended permanent test additions.
- Material unknowns or limitations.

## Self-improvement signals

After real use, record recurring friction in `00-control.md`, such as a missed test pattern, insufficient test data generation, or a validation stage that needed access to unavailable infrastructure. Recommend a narrow skill adjustment rather than silently editing the installed skill during validation.
