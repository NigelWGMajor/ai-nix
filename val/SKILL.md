---
name: val
description: Evaluate the effectiveness of a solution by designing test strategies, generating test data and test cases, creating test plans, and assessing coverage. Use when asked to validate an implementation, design a test approach, generate test data, create a test plan, or assess whether a solution meets its acceptance criteria. Do not use for implementing the solution itself, code review, or general exploration — use cop for code review and nix or wiz for exploration.
---

# VAL Validation Design

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the validation workflow.

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

Determine whether the request identifies an existing VAL instance. If a `.data/val-*` directory exists under the workspace root:

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

1. Fetch the content and convert it to clean Markdown.
2. Write it to `./md/<slugified-title>.md` with YAML frontmatter:

```yaml
---
source: "<original URL>"
captured: "<YYYY-MM-DD>"
title: "<page or issue title>"
type: "<confluence | jira-issue | api-spec | test-report | web | other>"
---
```

3. Preserve the document's semantic structure. Strip navigation chrome, sidebars, and boilerplate.

### Use captured documents

Once captures are complete, treat the `./md` snapshots as the working copies for all subsequent analysis. Cite them by their local path. Note the capture date as a freshness limitation in evidence records.

## Choose depth

- **Quick**: use for a narrow, well-specified feature with clear acceptance criteria. Produce a concise test plan in the conversation.
- **Standard**: use by default. Comprehensive test strategy with test cases, coverage matrix, and generated test data.
- **Deep**: use for high-risk changes, security-sensitive features, data migrations, or multi-system integrations. Decision tables, boundary analysis, failure injection scenarios, and generated fixtures.

Never inflate a simple validation into a deep test suite design. Never compress a security-sensitive change into a quick checklist.

## Create the validation instance

For Standard or Deep work, initialize a durable validation instance before substantial design:

Create the instance as `.data/val-YY-MM-DD-<suffix>` under the resolved workspace root, using the next available lowercase alphabetic suffix. Create `.data` when needed. Never overwrite an existing instance or modify `.gitignore`.

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
