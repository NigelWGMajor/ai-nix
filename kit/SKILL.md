---
name: kit
description: Reconstruct, sanity-check, and preserve the full status of a partially implemented Spec Kit project or feature branch. Use when asked to review a Spec Kit-generated branch, prepare work to be shelved or paused, resume an interrupted project, determine what is truly complete, compare spec/plan/tasks with implementation and tests, identify drift or risk, or produce an evidence-backed next-action plan. Do not use for implementing the remaining work, mutating Spec Kit artifacts, changing Git state, or ordinary code review without a project-recovery objective. An explicit request to use kit overrides these exclusions but not its mutation boundaries.
---

# KIT Project Recovery

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the review workflow.

Rebuild the project's mental model and establish an evidence-backed status that a person or agent can safely resume. Audit the in-scope feature from intent through implementation and validation without trusting stale narrative, task checkboxes, or branch names on their own.

## Operating boundaries

- Stay read-only except for the dedicated KIT output instance and ordinary temporary artifacts from approved validation.
- Treat “shelve” as pause-and-document, not permission to run `git stash`, switch branches, commit, reset, clean, rebase, merge, fetch, pull, or push.
- Never edit specs, plans, tasks, checklists, code, tests, Jira, pull requests, or remote state unless the user separately authorizes that mutation.
- Do not switch away from a dirty checkout. Capture the dirty state and continue the review in place when safe.
- Do not claim remote freshness from local tracking refs. State when no fetch occurred.
- Follow repository guidance before inspecting or validating. Prefer the repository's structural code-discovery facilities when available.
- Keep the audit bounded to the selected Spec Kit feature and material integration surfaces. “Full” means full traceability for that scope, not an unrelated whole-repository audit.
- Separate observed evidence, source claims, inference, and unknowns. Calibrate severity and confidence independently.

## Select the mode

Use one of three modes:

1. **Review**: perform a fresh full-status audit of the current feature branch.
2. **Snapshot**: perform the same audit and optimize the final report as a pause or handoff package.
3. **Resume**: read a previous KIT instance, re-resolve current facts, explain drift since that snapshot, and produce a refreshed reorientation and next-action plan.

If the request says “shelve,” default to Snapshot. If it says “resume,” require a uniquely identifiable prior KIT instance. Ask rather than guessing among multiple plausible instances.

## Resolve the exact target

Before trusting any prior context, re-resolve:

- Repository root.
- Current branch and exact HEAD.
- Staged, unstaged, and untracked state.
- Upstream and the freshness limits of tracking information.
- Intended base branch and merge base, when it can be established from explicit user input, pull-request metadata, or unambiguous local evidence.
- Spec Kit feature directory.
- Applicable repository instructions.
- Previous KIT instance in Resume mode.

Do not assume `main`, infer a feature directory from a loose name similarity, or reuse a target from an earlier conversation after the branch or HEAD changes. An exact branch-leaf-to-feature-directory match is acceptable evidence; otherwise present candidates and ask if the choice materially affects the audit.

Stop and explain the mismatch when a prior KIT instance names a different repository, feature, or branch and no explicit relationship makes the transition safe.

## Capture external references

Before deep analysis, ensure that all external sources are available locally as stable markdown snapshots.

### Gather links

Ask the user whether any Atlassian pages (Confluence, Jira tickets, epics), pull requests, web documents, or other external links should be included in the review. Accept URLs from the prompt, from the user's response, or discovered inside Spec Kit artifacts and repository metadata.

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
type: "<confluence | jira-issue | jira-epic | web | api-doc | pull-request | other>"
---
```

3. Preserve the document's semantic structure (headings, lists, tables, code blocks). Strip navigation chrome, sidebars, and boilerplate.
4. For Jira issues, include key fields (summary, status, type, assignee, labels, description, and acceptance criteria) as structured frontmatter or a leading metadata table.
5. For Confluence pages, preserve the page hierarchy context (space, parent page) in frontmatter when available.

### Use captured documents

Once captures are complete, treat the `./md` snapshots as the working copies for all subsequent analysis. Cite them by their local path rather than the original URL, but preserve the original URL in frontmatter for traceability. Note the capture date as a freshness limitation in `02-evidence.md`.

## Initialize the KIT instance

Prefer the supplied initializer after resolving the target:

```text
python <skill-directory>/scripts/init_instance.py --workspace <workspace-root> --repo <repo> --mode <review|snapshot|resume> --feature-dir <feature-dir> --base <base-ref> [--previous <kit-instance>]
```

The initializer captures a read-only local Git snapshot, hashes known Spec Kit artifacts, and creates the next collision-safe `.data/kit-YY-MM-DD-<suffix>` directory under the resolved workspace root. Pass the resolved workspace root explicitly; do not substitute the repository root when the workspace root differs. It refuses to write inside an unignored repository path. Use `--output-root` to select an approved location outside the repository when necessary. Never modify `.gitignore` automatically.

Maintain:

- `00-control.md`: identity, mode, target, scope, progress, assumptions, open questions, and next safe action.
- `01-repository-snapshot.md`: exact local Git facts, status, diffs, and recent commits.
- `02-evidence.md`: known artifacts, hashes, roles, and candidate feature directories.
- `03-analysis.md`: requirement/story-to-design-to-task-to-code-to-validation mapping.
- `04-validation.md`: validation ledger with commands, environment, results, and limitations.
- `Findings.md`: professional reader-facing recovery report.

Checkpoint `00-control.md` after each audit layer and before stopping. Do not mark it complete until the status report passes the quality gate.

## Reconstruct intent and design

Read [references/spec-kit-evidence.md](references/spec-kit-evidence.md) before evaluating artifacts. Respect the installed project's version, presets, extensions, and templates instead of assuming every current upstream artifact exists.

Use [references/jira-integration.md](references/jira-integration.md) to interpret Jira fields and conventions when the project has Jira-linked tickets or acceptance criteria. Use [references/prefactoring-development-guidance.md](references/prefactoring-development-guidance.md) when assessing implementation quality against design intent.

Establish the evidence chain:

`constitution -> specification -> clarification/checklists -> plan/research/design/contracts -> tasks -> implementation -> validation -> integration -> next action`

Identify:

- The problem, intended users, outcomes, scope, exclusions, user stories, requirements, and acceptance scenarios.
- Constitution gates and project-specific principles.
- Technical decisions, rationale, rejected alternatives, data model, contracts, and quickstart scenarios.
- Task phases, dependencies, parallel markers, file targets, and declared completion.
- Optional roadmap or spec-of-specs relationships.

Record missing, contradictory, stale, or customized artifacts. Absence is not automatically a defect when an artifact is optional or inapplicable.

## Determine actual implementation status

Do not equate a checked task with completed work or an unchecked task with absent work. For each in-scope requirement, story, phase, or material task, compare:

1. The source claim in `tasks.md` or other tracking artifact.
2. Relevant commits and current worktree changes against the resolved base.
3. Concrete code, configuration, schema, migration, contract, or documentation evidence.
4. Tests, quickstart results, build output, or other acceptance evidence.
5. Integration state such as commits, upstream, or pull-request evidence when available.

Assign a status:

- **Verified complete**: appropriate implementation and validation evidence satisfy the stated outcome.
- **Implemented, validation incomplete**: implementation exists but acceptance evidence is missing or insufficient.
- **In progress**: coherent partial implementation or active uncommitted work exists.
- **Claimed only**: an artifact marks completion without corroborating implementation evidence.
- **Not started**: planned work has no material implementation evidence.
- **Blocked**: a stated dependency or external condition prevents progress.
- **Contradicted or stale**: artifacts and current evidence materially disagree.
- **Unknown**: available evidence cannot support a responsible classification.

Use code discovery proportionate to the feature. Trace important entry points and downstream effects, but do not perform an unbounded architecture review.

## Sanity-check the project

Apply the audit in [references/spec-kit-evidence.md](references/spec-kit-evidence.md). At minimum, test for:

- Constitution, spec, plan, task, and implementation consistency.
- Requirement and user-story coverage by design and tasks.
- Task dependency and ordering coherence.
- Plan or contract drift in the implementation.
- Acceptance and edge-case coverage.
- Stale task checkboxes or orphan implementation.
- Missing migrations, configuration, observability, security, failure handling, or rollout work where relevant.
- Quickstart and validation commands that no longer match the project.
- Dirty worktree risk, detached HEAD, ambiguous base, missing upstream, and local-only commits.
- Material gaps between “feature complete,” “tests green,” “integrated,” and “ready to merge or deploy.”

If an installed `speckit.analyze` capability is available and can be guaranteed read-only, its cross-artifact analysis may supplement the audit. Do not run `speckit.converge`: current Spec Kit behavior can append tasks. Do not run `speckit.implement`, task generation, clarification, checklist generation, or other mutating workflows during a read-only KIT review.

## Validate responsibly

Inspect existing test evidence before running commands. Run focused, safe local validation when it is a normal part of the requested sanity check and repository guidance supports it. Obtain approval before installing dependencies, using network access, touching databases or external services, launching long or broad test suites, or causing material working-tree changes.

Capture Git status before and after validation so generated artifacts are not mistaken for pre-existing project work. Record each command, timestamp, environment or prerequisite, exact result, and the HEAD tested. Report “not run” with the reason instead of implying success.

## Produce the recovery report

Before drafting:

1. Read [references/documentation-standard.md](references/documentation-standard.md) and apply its shared document, link, visual, handoff, and workspace-storage rules.
2. Read [references/output-contract.md](references/output-contract.md) for KIT-specific recovery and traceability rules.
3. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Its current assignments override any symbols hardcoded in templates, output contracts, or other reference files.
4. Adapt [assets/findings-template.md](assets/findings-template.md) to the feature. Replace any template symbols with the current assignments from visual-language.md.

Preserve the shared output spine and keep KIT-specific recovery detail inside its mapped sections.

Lead with reorientation: what the project is, why it exists, where it is in the lifecycle, what is genuinely complete, what remains uncertain, and the safest next action. Include strengths as well as concerns.

In Resume mode, compare the previous snapshot with current repository, branch, HEAD, worktree, artifacts, findings, validation, and next action. Preserve historical facts rather than rewriting the prior instance.

Use stable finding IDs such as `KIT-001`. State severity, confidence, evidence class, impact, and a concrete next step. Keep facts distinct from inference.

End with a `Next steps` section containing an ordered resume plan. Make the first action immediately executable by naming its prerequisite, target file or component, validation expectation, and stopping condition.

## Complete the review

Apply the shared quality gate in [references/documentation-standard.md](references/documentation-standard.md) and the KIT-specific gate in [references/output-contract.md](references/output-contract.md). Update `00-control.md` with:

- Final status.
- Completed audit layers.
- Validation performed and omitted.
- Unresolved decisions and blockers.
- Exact next safe action.

Report the KIT instance path, repository/branch/HEAD reviewed, source and remote-freshness limitations, validation outcome, highest-priority concerns, and next action to the user.

## Self-improvement signals

After real use, record recurring friction such as a missed custom artifact, unreliable feature-directory resolution, an overly wide traceability table, a validation command that needs a guardrail, or a resume comparison that required manual reconstruction. Recommend a narrow skill or script adjustment rather than silently changing the installed skill during a project review.
