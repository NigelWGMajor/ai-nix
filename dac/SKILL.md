---
name: dac
description: Coordinate complex Jira-backed feature or project delivery through a divide-and-conquer workflow. Use when Codex or Claude needs to align on a parent outcome, investigate Jira and code evidence, resolve shared decisions, partition work into dependency-aware portions, route each ready portion to Spec Kit, another skill, a direct implementation agent, or a human, and reconcile results through pull-request integration. Maintain resumable, human-readable Markdown while keeping Jira as the management view and requiring explicit approval for local, code, Git, Jira, and remote mutations.
---

# Divide-and-Conquer Delivery

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the coordination workflow.
## `new` fresh-run override

When `new` is a standalone invocation keyword (for example, `/nix new <topic>`), start a fresh run. The ordinary word `new` within a topic or other prose does not enable this mode. This reset applies only to prior skill-run artifacts: continue to inspect the existing codebase, user-supplied material, and authoritative systems normally.

Do not inspect, resume, or reuse a prior `.data/` or `.dac/` run. After resolving the exact workspace folder this run would otherwise write into or update, if that folder already exists, first rename it in the same parent using the first unused alphabetic suffix: `<name>-a`, `<name>-b`, ..., `<name>-z`, then `<name>-aa`, and so on. Never overwrite, merge, or archive unrelated folders or folders used solely as read-only inputs. If the fresh run creates a distinct new destination or is read-only, do not rename anything.

The archive move needs the same local-write approval as writing the destination. Report the old and archive paths, then continue as though that run never existed. `new` does not authorize source changes, Git mutations, tests, deployment, Jira, or other remote actions.

## Output location

Resolve `TOOLING_OUTPUT_PATH` before locating or creating a DAC workspace. When set, an absolute value is the output base; a value beginning `./` or `.\\` is relative to the repository root; reject other relative forms. All `.dac/` paths below mean `<output-base>/.dac/`; when unset, retain the repository-root default. An explicit `--workspace-dir` remains an override.

## Objective

Coordinate a large outcome without requiring any participant to hold the whole implementation in context. Keep shared intent, decisions, dependencies, Jira visibility, and integration at the parent level. Give each executor a bounded portion envelope and require a normalized result.

Treat Jira and repository artifacts as evidence that may disagree. Treat approved DAC artifacts as the coordination record, child specifications as portion-local detail, code and tests as observed behavior, and Jira as the management view.

## Folder Convention

**DAC internal artifacts** live under `.dac/<workstream>/` in the repository root and should be excluded from version control (typically via global gitignore):

- All coordination files: `00-control.md`, `01-mission.md`, `02-evidence.md`, `03-decisions.md`, `04-portion-plan.md`, `05-jira-plan.md`, `06-integration-plan.md`
- Portion envelopes: `portions/P-001.md`, `portions/P-002.md`, etc.
- Result records: `results/P-001.md`, etc.
- Helper state and logs

**Deliverable artifacts** (e.g., Spec Kit specifications, design documents, generated code) belong in the repository under their normal locations and should be committed:

- Spec Kit features: typically under a `features/` or `.speckit/` directory per project convention
- Documentation: `docs/` or project-specific documentation directories
- Generated or scaffold code: standard source tree locations

The `.dac/` directory is a coordination workspace, not a deliverable. Only the implementation artifacts it orchestrates become part of the repository history.

## Authority

Remain read-only until the user approves a mutation class. Never infer execution authority from approval of content.

| Class | Scope | Default |
|---|---|---|
| R0 | Read Jira, documentation, repository files, Git metadata, PRs, and indexes | allowed |
| W1 | Write the named `.dac/<workstream>/` workspace or explicitly allocated specification directories | explicit scoped approval |
| V2 | Run tests, builds, generators, dependency resolution, or commands with ephemeral output | explicit command or validation-scope approval |
| C3 | Change source, tests, configuration, schemas, fixtures, branches, worktrees, commits, or other Git state | explicit portion-specific approval |
| R4 | Create or update Jira items, push, open or edit PRs, merge, deploy, or mutate any remote system | separate exact-action approval |

Preserve pre-existing changes. Do not let a child executor change shared Jira hierarchy, parent decisions, or sibling scope. Route those changes back through the coordinator.

## Progress Indicator

**Display at start and end of every interaction:**

```
DAC Progress: [●] Align → [ ] Partition → [ ] Jira → [ ] Execute → [ ] Integrate
```

Status indicators:
- `[●]` Current phase
- `[✓]` Completed phase
- `[ ]` Future phase

Major phases:
1. **Align** - Mission, Evidence, Decisions approved
2. **Partition** - Portion plan approved
3. **Jira** - Jira allocation strategy decided and approved by user
4. **Execute** - Portions routed and executing
5. **Integrate** - PRs merged, convergence complete


## Start or resume

**Show progress indicator first.**

1. Confirm the repository root, branch, HEAD, and worktree state without changing them.
2. Identify the parent Jira issue or stable workstream ID. The normal form is `PD-######`; do not guess among plausible parents. Accept another key only when the user explicitly supplies that exact alternative key in the prompt.
   - An explicitly supplied suffixed folder such as `PD-123456-b` is an exact workspace selector. Treat `.dac/PD-123456-b/` as the current workspace and resume its control file; do not normalize it to `PD-123456` or scan sibling suffixes.
3. Discover available Jira, repository, GitHub, Spec Kit, and skill capabilities.
For Jira access, use the available Atlassian plugin or MCP capability. Verify it with a lightweight read before relying on Jira evidence.
For repository code discovery, prefer the available Codebase Knowledge Graph MCP; fall back to text search only when graph results are insufficient.

   > Could you try restarting the MCP server? You can either:
   > 1. Run `! /mcp` in this prompt to check MCP server status
   > 2. Use `curl` with your MCP credentials to access the Atlassian API directly
4. Look for `.dac/<workstream>/00-control.md`.
   - With `new`, do not read the existing control file. Once W1 is approved, archive that exact `.dac/<workstream>/` folder under the fresh-run rule before initialization, then start at Align as though it had not existed.
   - For automatic discovery, only consider directories whose name exactly matches the parent-ticket form `PD-######` (case-insensitive). Ignore every other folder under `.dac/`, including legacy, scratch, and similarly named directories.
   - If the user explicitly supplied a non-PD key, do not scan non-PD folders; check only the exact `.dac/<explicit-key>/00-control.md` path.
   - If that exact suffixed folder exists, resume it even when its internal `workstream` value remains the unsuffixed Jira key. Initialize a suffixed key only when the user actually intends a distinct new workstream.
   - If it exists, read it first and resume its recorded next action.
   - If it does not, align on the intended outcome in conversation and request W1 approval.
5. After W1 approval, initialize the workspace:

```bash
python <skill-dir>/scripts/dac.py init --workstream PD-123456 --repo-root . --title "Outcome"
```

For a genuinely new explicitly supplied non-PD workstream, add `--allow-non-pd` to `dac.py init`. Do not initialize an existing archived suffix; resume that exact folder instead.

Read [references/artifact-contract.md](references/artifact-contract.md) before initializing, approving, resuming, or validating a workspace.

Read [references/jira-integration.md](references/jira-integration.md) for Jira field discovery, acceptance criteria formatting, and the Jira allocation decision step.

Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols used in DAC artifacts. Its current assignments override any symbols hardcoded in templates or other reference files. Use its shared output-spine and evidence-status palettes when composing workspace artifacts and completion reports.

## Preview mode

When the user invokes DAC with `preview` on the prompt line (e.g. `/dac preview PD-123456`), the entire run is confined to `.dac/` workspace writes (W1 only). No code changes (C3), no Jira or remote writes (R4), no builds or tests (V2). Because of this safety boundary:

**Request blanket W1 approval once at the start** and then proceed through Align and Partition without pausing for per-artifact write permission. The user should only need to confirm once ("approve W1 for `.dac/<workstream>/`") and then see results, not a series of permission prompts.

**Preview MUST write workspace artifacts.** Always initialize the `.dac/<workstream>/` workspace and write the full set of artifacts (00-control through 06-integration-plan). Never substitute inline display for file creation — the artifacts are the deliverable of a preview, not a summary in chat. If the workspace was previously cleaned up or does not exist, initialize it fresh.
Run the full Align and Partition phases, then write a non-binding, asynchronous allocation review to `05-jira-plan.md` and display the same table. The review must separate SQL, frontend (FE), and backend (BE) work; split large portions further at natural outcome or contract boundaries; and show optional same-discipline groupings.
### Recursive hierarchy visibility
When preview starts from an Epic, inspect its reachable Jira hierarchy and the local `.dac/` workspaces for every discovered ticket key. A Story that already has `.dac/<story-key>/00-control.md` is a master Story with a nested DAC workspace: recursively include its portions and any Jira children or linked split work that the available evidence establishes. Continue until no further nested workspace or Jira child is found.
`05-jira-plan.md` must begin its planning content with both navigators, before the allocation table:
1. **DAC portion hierarchy** — an indented tree covering the complete nested portion/workspace structure.
2. **Jira ticket hierarchy** — an indented tree covering the corresponding Epic → Story → descendant-ticket structure.
Each navigator node must include its Jira key or DAC portion ID and a concise status. Every master Story node in both trees must be a relative Markdown link to that Story's detail block later in the same plan (for example, `[PD-123457 — Search foundation](#pd-123457-search-foundation)`). Give each detail block that exact explicit HTML anchor immediately before its heading, so the tree links remain stable. Follow the two trees with a **Master Story details** section containing one detail block for every discovered master Story, in hierarchy order. Each block must state its parent, local workspace path, portion IDs/statuses, known Jira descendants, dependencies, and any unknown or conflicting evidence. The summary shown to the user must include the same two trees and the master-Story links.
Keep the traversal read-only: do not infer unobserved relationships from folder names alone, do not follow a node more than once, and mark cycles, duplicate references, inaccessible workspaces, and unknown Jira relationships explicitly. This is a planning artifact only: do not construct a final Jira creation payload, request R4 approval, or create tickets. Then **stop**.

```
DAC Preview complete: [✓] Align → [✓] Partition → [●] Jira (proposed) → [ ] Execute → [ ] Integrate

Preview stops here. The partition and asynchronous Jira allocation review are ready for review.
All artifacts are in .dac/<workstream>/ — no code, Jira, or remote changes were made.
To proceed with ticket creation, run `/dac` again to resume from the Jira approval step.
```

Do not prompt for Jira approval, create tickets, or advance past the proposal. On resumption, read and present the saved allocation table for confirmation before regenerating it. Regenerate only if the user asks to repartition, select a different grouping, or new evidence changes the portion boundary. The workspace artifacts (mission, evidence, decisions, portion plan, and the proposed Jira plan) are written and available for review, but no R4 actions are taken.

## Coordinate the workstream

### 1. Align and investigate

Produce and approve, in order:

1. `01-mission.md`: outcome, users, success criteria, scope, non-goals, and constraints.
2. `02-evidence.md`: relevant Jira graph, current repository behavior, tests, contracts, discrepancies, and confidence.
3. `03-decisions.md`: shared clarifications, alternatives, decisions, owners, and deferrals.

Resolve decisions that could alter portion boundaries or shared contracts before partitioning. Preserve later discoveries as new or superseding decisions; never rewrite history silently.

### 2. Partition by outcomes

Produce `04-portion-plan.md`. Prefer portions that are independently understandable, testable, reviewable, and suitable for one PR each.

Each portion must have:

- one coherent outcome and explicit non-goals
- traceability to parent success criteria
- stable inputs, outputs, and compatibility obligations
- explicit dependencies and downstream consumers
- a bounded change surface and test obligation
- a proposed executor route
- an escalation boundary

**Split by expertise domain by default.** When work spans distinct expertise boundaries — SQL/database, Elasticsearch/search, backend/API, frontend/UI — create separate portions for each domain even if the changes are small. This ensures each portion can be routed to an appropriate executor and reviewed by domain experts. Only combine cross-domain work into a single portion when the changes are so tightly coupled that splitting would create circular dependencies.

Prefer vertical slices within a domain. Create a foundation portion only for a genuinely shared contract, additive schema, compatibility adapter, migration, or reusable capability. Reject cycles, hidden blockers, unsafe parallel file overlap, and partitions that merely mirror architecture layers.

### 2a. Mandatory per-portion necessity, reuse, and security review

Before requesting approval for `04-portion-plan.md` or moving to Jira allocation, read [references/portion-sanity-review.md](references/portion-sanity-review.md) and complete its review for **every active proposed portion**.

Use repository instructions, code, tests, and the Codebase Knowledge Graph to establish the existing capability, extension point, established methodology, and authorization/security path relevant to each portion. Record the result in the **Portion necessity, reuse, and security review** section of `04-portion-plan.md`, including the requirement covered, evidence links, intended action (`reuse`, `extend`, `new`, `discovery`, or `remove/defer`), security approach, and gate status.

- Do not propose a new service, class, abstraction, contract, schema, pipeline, or authorization mechanism merely because it makes the portion description convenient. First establish that no suitable existing capability or approved extension point can meet the need.
- Treat a missing, inaccessible, or ambiguous source of truth as `discovery` or `revise`, not as justification for net-new implementation or a security bypass.
- A `new` action needs a concise necessity case: the existing capabilities inspected, why reuse or extension is insufficient, the owner and boundary of the new capability, the established pattern it follows, and its authorization/security obligations.
- A portion may proceed to content approval only when its review status is `ready`, or it has been explicitly removed or deferred. Resolve `revise`, `discovery`, and `decision` outcomes through evidence or a parent decision before allocating Jira work or creating an implementation envelope.
- With W1 authority, automatically correct a flagrant planning defect only when direct evidence establishes the correction and it preserves the approved mission: revise a `new` action to `reuse` or `extend`, remove a redundant portion, or name the established authorization/security path. Record the evidence and correction in the portion plan and control change log.
- When reasonable alternatives remain, such as competing extension points, unclear ownership, compatibility consequences, or ambiguous authorization behavior, do not choose silently. Record the alternatives and ask the user one consequential question before proceeding.

### 3. Jira allocation decision (MANDATORY)

**ALWAYS pause after portion plan approval to decide Jira ticket allocation.** A preview may propose non-binding allocation alternatives, but it must not create Jira issues, construct a final creation payload, or request R4 approval. A final mapping and any Jira action require the user's explicit confirmation and approval.

#### Present the allocation context

Summarize enough information for the user to make an informed decision:

| Portion | Outcome | Complexity | Dependencies | Change surface |
|---------|---------|------------|--------------|----------------|
| P-001   | ...     | ...        | ...          | ...            |

Include:
- Total number of portions and their dependency structure
- Whether portions touch overlapping or disjoint files/systems
- Estimated scope of each portion (small fix vs. substantial feature)
- Any existing Jira children or related tickets already in the hierarchy

#### Propose ticket allocation

Start from one proposed Story per portion. SQL, FE, and BE portions must always be separate because they use different review pipelines. Split a large portion into additional portions at natural outcome, contract, or independently testable change boundaries before suggesting Jira groupings. Do not group portions across those discipline boundaries.

Present and persist this exact table in `05-jira-plan.md`:

| Portion | Proposed Jira Issue | Type | Master | Dependencies | Status | Description | Suggested Grouping |
|---------|---------------------|------|--------|--------------|--------|-------------|--------------------|
| P-001 | New Story | Story | PD-123456 | - | proposed | Add SQL migration | A — combine with P-002 (same SQL review pipeline) |
| P-002 | New Story | Story | PD-123456 | P-001 | proposed | Add SQL data backfill | A — combine with P-001 (same SQL review pipeline) |
| P-003 | New Story | Story | PD-123456 | P-001 | proposed | Add backend API | — |

Each letter is a candidate grouping: portions bearing the same letter would share one Jira Story if selected. A dash means no grouping is suggested. The `Description` must be brief but sufficient for an asynchronous reviewer to understand the proposed ticket boundary.

The user may then:

- **Use portions** — keep one Jira Story per portion.
- **Accept suggested groupings** — confirm one or more lettered groupings.
- **Split more** — name the portion to split; revise `04-portion-plan.md`, then regenerate the table.
- **Parent-only** — track all portions under the master ticket with no new Stories.

Wait for the user to decide before proceeding.
**Respect the user's selection exactly.** When the user chooses an allocation option, implement exactly what they chose. Do not substitute your recommendation after they have made their selection. If you believe the choice has issues, raise them explicitly before proceeding — never silently override a stated preference.

#### After the user chooses

- **If Parent-only:** Record the decision in `05-jira-plan.md` with strategy `none`. Skip Jira child creation, but complete and obtain content approval for a **trivial** `06-integration-plan.md` before materializing portion envelopes. The trivial plan records the direct branch/PR path, validation, rollout/rollback, and parent-ticket traceability; it must not be omitted.
- **If Use portions or Accept suggested groupings:** update the saved table to the chosen mapping, then present the proposed Jira organization for approval. For each proposed ticket, include the acceptance criteria as a markdown checklist exactly as they will appear in the Jira ticket:

| Portion | Proposed Jira | Type | Parent | Rationale |
|---------|--------------|------|--------|-----------|
| P-001   | ...          | ...  | ...    | ...       |

**P-001 — Acceptance Criteria:**
- [ ] First criterion derived from parent success criteria
- [ ] Second criterion specific to this portion's outcome
- [ ] Relevant test or validation obligation

**P-002 — Acceptance Criteria:**
- [ ] ...

Present every ticket's acceptance criteria in this checklist format so the user can review them in context before any Jira writes. These same checklists are written verbatim into `05-jira-plan.md` and into the Jira acceptance criteria field when tickets are created.

**Standalone Jira-preview requirement:** When a Jira preview refers to a DAC decision, include the decision ID, a brief plain-language summary of what was decided, and its implementation effect in that preview. Do not rely on a reader having access to `03-decisions.md` or conversation history. Example: `DEC-003 — Use additive schema migration; deploy the schema before API changes.`

**Jira child issue requirements (when creating):**
- **Always create child issues as Stories** (never subtasks) for better tracking
- Treat the issue being split as the **split-from issue**.
- Copy the split-from issue's native **Parent** field to every new Story. This usually places the new Stories under the same upstream Epic; never set the split-from issue itself as their native parent.
- Copy the split-from issue's **labels** and **team** fields to every new Story.
- Link each new Story back to the split-from issue with the **Created By** relationship.

**Additional questions to resolve:**
- Should we reuse existing issues or create new ones?
- What work is in DAC scope vs. handled separately?
- Are there additional labels needed for specific portions?

After Jira allocation strategy and specific actions are approved, produce:

- `05-jira-plan.md` for the proposed parent, child issues, links, ownership, exact remote actions, and acceptance criteria field discovery.
- `06-integration-plan.md` for branches or worktrees, PR bases, merge order, compatibility states, rollout, and rollback.
**Branching strategy — explicitly recorded integration topology:**
Before implementation, record the target branch, parent integration branch (when child Stories exist), every child branch and PR base, and any direct-PR path in `06-integration-plan.md`. Never default or infer a PR base as `main`: the approved target may be a release branch, an existing parent branch, or another integration branch.

When DAC splits a master Jira issue into child Stories, create the parent integration branch from the recorded target branch. Create every child portion branch from that parent branch; open each child PR back to the parent branch; then open one parent PR from the parent branch to the recorded target branch after the intended child PRs have merged. Record the exact branch names and PR bases in `06-integration-plan.md` before implementation.

Treat that topology as a planned contract, not evidence that it happened. Before reporting, accepting, or completing integration, read the **PR topology verification** section in [references/quality-and-integration.md](references/quality-and-integration.md). Resolve the repository, the child PR's actual head and base, and the remote PR state independently. Do not infer any of those facts from a ticket, branch name, workspace folder, or the expected DAC topology.
```text
<recorded target branch> -> parent integration branch -> child portion branches
<recorded target branch> <- parent PR                 <- child PRs
```

- Never branch a child portion from a sibling portion branch. Dependencies govern child-PR merge order within the parent integration branch.
- Merge the updated parent integration branch into an active child branch when it needs the newly integrated child work; do not rebase published child branches.
- For work with no child Stories, use one branch from and one PR back to the recorded target branch.
- **Worktrees are optional:** use them for editing convenience when working on multiple portions simultaneously, not for code isolation. For a single checkout, use the tracked DAC switch workflow rather than direct `git stash` / `git checkout`.
- **Never switch away from uncommitted work directly:** commit it, or use `/dac switch` after C3 approval so DAC creates and records a named stash. Never remove a worktree with uncommitted work.

Content approval does not authorize Jira or GitHub writes. Require R4 approval, execute only the approved payload, then read back and record the actual result.

**When creating Jira issues:**
- Always create child issues as **Story** type (never subtasks)
- Copy the split-from issue's native **Parent**, **labels**, and **team** fields to every Story.
- Link each Story to the split-from issue with the **Created By** relationship. Do not use an `is part of` link and do not make the split-from issue the Story's native parent.
- Include acceptance criteria in the dedicated custom field (NOT in description)
- See [references/jira-integration.md](references/jira-integration.md) for field discovery, ADF format, and common mistakes

### 4. Materialize portion envelopes

Create a portion only after the partition is approved:

```bash
python <skill-dir>/scripts/dac.py portion create \
  --workspace .dac/PD-123456 \
  --id P-001 \
  --title "Add compatibility contract" \
  --executor speckit \
  --jira ABC-124
```

Use `--depends-on P-001,P-002` when needed. Approve the completed envelope as content before routing it. A portion becomes planning-ready only when its envelope is approved and every dependency is `integrated` or `complete`:

```bash
python <skill-dir>/scripts/dac.py ready --workspace .dac/PD-123456
```

Read [references/executor-routing.md](references/executor-routing.md) before dispatching a portion.

### 5. Route the ready portion

Choose the executor at dispatch time:

| Condition | Route |
|---|---|
| meaningful ambiguity, risk, or cross-component design | `speckit` |
| specialized repeatable workflow has a matching skill | `skill:<name>` |
| small, well-understood implementation | `direct` |
| uncertainty blocks design | `discovery` |
| organizational or manual work | `human` |

Pass only the portion envelope, named parent decisions and contracts, relevant repository evidence, and current authority. Do not load sibling implementation detail unless a declared contract requires it.

For Spec Kit, allocate a unique feature directory centrally and use the envelope as the input to its specify/clarify/plan/tasks/analyze/implement/converge cycle. Keep concurrent runs in separate worktrees and select the feature directory explicitly when supported.

For another skill, treat the envelope as the prompt contract. Let the target skill govern its specialist workflow, but do not let it broaden authority or edit parent coordination state.

### 6. Ingest a normalized result

Every executor must return the same minimum result:

- outcome: completed, blocked, or superseded. Record a failed execution attempt as `blocked`, with its cause, retry condition, and required escalation.
- artifact, branch, commit, and PR references when applicable
- files or systems changed
- acceptance criteria and test evidence
- deviations, assumptions, discoveries, and contract effects
- residual work and downstream recommendations

Create a result artifact and have the coordinator update shared state. Child executors must not write the parent registry concurrently.

### 7. Integrate and converge

Before accepting a portion result, verify its envelope, approvals, actual diff or output, tests, compatibility, and escalation disclosures. For a portion with a PR requirement, mark it `integrated` only after [PR topology verification](references/quality-and-integration.md#pr-topology-verification) establishes that the actual child PR was merged into its intended base. Local branch ancestry can support a narrowly labelled containment observation, but never proves a remote PR merge. Recalculate the ready set and update Jira only with R4 approval.

After all required portions are integrated or explicitly deferred, perform parent convergence. Check mission coverage, decision compliance, cross-portion behavior, integration tests, Jira and PR traceability, deployment order, monitoring, rollback, and remaining ownership. Add residual portions instead of weakening acceptance criteria.

Read [references/quality-and-integration.md](references/quality-and-integration.md) before approving a partition, accepting a result, or completing the parent.

## Drift and escalation

Pause the affected portion when:

- a parent decision or acceptance criterion changes
- an upstream contract differs from the envelope
- Jira or the target branch changed materially since handoff
- implementation requires sibling-owned files or broader authority
- a new dependency, migration, security, or rollout concern appears

Classify the discovery as local, parent-level, contract-changing, or new scope. Handle local discoveries inside the child. Route all others to the parent decision register, mark affected portions stale or blocked, and reapprove their envelopes before continuing.

## Branch sync
Use the `sync` subcommand to check whether child portion branches are up to date with the parent integration branch. This is useful after merging child PRs into the parent, after updating the parent from its recorded target branch, or when resuming work after time away.
```bash
python <skill-dir>/scripts/dac.py sync --workspace .dac/PD-123456
python <skill-dir>/scripts/dac.py sync --workspace .dac/PD-123456 --parent-branch <parent-integration-branch>
```
The sync report shows each portion's branch status:
- **Behind** — commits on the parent not yet in the portion branch (needs merge)
- **Ahead** — portion-specific commits not yet in parent (expected for active PRs)
- **Remote** — whether the local branch is pushed to origin
- **Action** — `MERGE PARENT` if the portion branch is behind, `PUSH` if unpushed
Branch discovery is automatic: the helper matches portion Jira ticket numbers to local branch names. You can also add a `branch` field to portion frontmatter for explicit mapping.
Sync is read-only (R0). To act on suggestions, ask `/dac` to merge the parent into portion branches (requires C3 approval) and push (requires R4 approval).

## Tracked branch switching

`/dac switch` provides a safe context switch in a single checkout. The coordinator must obtain C3 approval before any switch that changes the active branch or creates/restores a stash. Running it without a target is R0 and lists choices; an asterisk marks a target with DAC-recorded stashed work.

Before first use, record the branch names approved in `06-integration-plan.md` and configure the helper under W1:

```bash
python <skill-dir>/scripts/dac.py switch --workspace .dac/PD-123456 configure \
  --master-branch <parent-integration-branch> --target-branch <recorded-target-branch>
```

After C3 approval, use:

```bash
python <skill-dir>/scripts/dac.py switch --workspace .dac/PD-123456       # list A, B, C..., and the recorded target
python <skill-dir>/scripts/dac.py switch --workspace .dac/PD-123456 A     # first listed target
python <skill-dir>/scripts/dac.py switch --workspace .dac/PD-123456 B     # second listed target
python <skill-dir>/scripts/dac.py switch --workspace .dac/PD-123456 <recorded-target-branch>
```

If the current checkout is dirty, the helper creates an include-untracked named stash, records its marker in `00-control.md`, then switches. When returning to a target with DAC-recorded WIP, it applies and drops that exact named stash. If restoration conflicts, it retains the stash, records `restore_conflict`, and stops without resolving the conflict. Do not use direct Git stash/switch commands for DAC-managed context switching.
## Helper boundaries

The bundled helper manages Markdown under one `.dac` workspace. It can initialize, validate, record approvals and decisions, create portions and results, derive readiness, record permitted state transitions, and report git sync status of portion branches. Except for `sync` (Git read-only) and `switch` (a C3-gated tracked branch/stash operation), it never invokes Jira, Spec Kit, another skill, Git, tests, builds, deployment, or network tools.

```bash
python <skill-dir>/scripts/dac.py status --workspace .dac/PD-123456
python <skill-dir>/scripts/dac.py validate --workspace .dac/PD-123456
python <skill-dir>/scripts/dac.py approve --workspace .dac/PD-123456 --artifact 01-mission.md --by "Name" --scope "Mission and success criteria"
python <skill-dir>/scripts/dac.py decision --workspace .dac/PD-123456 --id DEC-001 --question "Question" --outcome "Decision" --by "Name"
python <skill-dir>/scripts/dac.py transition --workspace .dac/PD-123456 --portion P-001 --to executing
python <skill-dir>/scripts/dac.py result create --workspace .dac/PD-123456 --portion P-001
python <skill-dir>/scripts/dac.py sync --workspace .dac/PD-123456
python <skill-dir>/scripts/dac.py switch --workspace .dac/PD-123456
```

## Completion response

**Show progress indicator:**
```
DAC Progress: [✓] Align → [✓] Partition → [✓] Jira → [✓] Execute → [●] Integrate
```

Produce a completion summary using symbols from `visual-language.md`. Report the parent outcome, completed and deferred portions, executor and Jira mapping, dependency and PR sequence, decisions, tests, integration evidence, rollout and rollback, remaining risks, and the resume path under `.dac/<workstream>/`.

Use the shared evidence link conventions from `artifact-contract.md` for Jira tickets, PRs, and file references.

## Solo Ticket Management

DAC can manage individual tickets that are outside the current workstream's Jira scope. Solo tickets live alongside portions in the `.dac/<workstream>/` workspace and use local IDs `S-001`, `S-002`, etc.; their real Jira key, Jira parent, team, labels, and base branch remain independent of the master workstream.

### When to use solo tickets

- Add existing work demands to DAC management without creating artificial parent Epic
- Ensure proper acceptance criteria on standalone tickets
- Track branch sync status for individual tickets
- Maintain structured work records for tickets with common workstream ancestor
- Bridge between informal work and full DAC coordination

### Solo ticket folder structure

```
.dac/<workstream>/
  solo/
    S-001.md             # Solo ticket envelope; stores its separate Jira key
    S-002.md
  results/
    S-001-result.md     # Solo ticket results
```

### Solo commands

#### Adopt an existing ticket

```bash
python <skill-dir>/scripts/dac.py solo adopt \
  --workspace .dac/PD-123456 \
  --ticket-id PD-123457 \
  --title "Fix authentication bug" \
  --outcome "Users can log in reliably" \
  --ac "- [ ] Login succeeds for valid credentials\n- [ ] Error message for invalid credentials" \
  --executor direct \
  --jira-url "https://jira.example.com/browse/PD-123457" \
  --branch "feature/PD-123457-auth-fix"
```

This creates a solo envelope such as `.dac/PD-123456/solo/S-001.md` with:
- Work scope and acceptance criteria
- Branch tracking
- Status: `adopted`
- Authority model (W1, C3, V2, R4)

#### Create a new solo ticket

```bash
python <skill-dir>/scripts/dac.py solo create \
  --workspace .dac/PD-123456 \
  --ticket-id PD-123458 \
  --title "Add request logging" \
  --outcome "All API requests are logged" \
  --executor direct \
  --base-branch <approved-base-branch>
```

**Note:** Jira ticket creation happens outside this script (via Atlassian MCP tools). This command creates the DAC envelope after the ticket exists.

#### Check solo ticket status

```bash
python <skill-dir>/scripts/dac.py solo status --workspace .dac/PD-123456
```

Shows all solo tickets with their status, branch, executor, and last update.

#### Transition and record a solo ticket

```bash
python <skill-dir>/scripts/dac.py solo transition \
  --workspace .dac/PD-123456 \
  --solo S-001 \
  --to executing \
  --by "Developer Name" \
  --reason "Starting implementation"
```

Valid transitions:
- `assessed` → `adopted`, `superseded`
- `adopted` → `executing`, `blocked`, `superseded`
- `executing` → `blocked`, `pr_open`, `complete`, `superseded`
- `blocked` → `executing`, `superseded`
- `pr_open` → `blocked`, `integrated`, `superseded`
- `integrated` → `complete`

Create its normalized result with:

```bash
python <skill-dir>/scripts/dac.py solo result --workspace .dac/PD-123456 --solo S-001
```

#### Branch sync for solo tickets

The `sync` command includes solo tickets:

```bash
python <skill-dir>/scripts/dac.py sync --workspace .dac/PD-123456
```

Output shows both portions (P:) and solo tickets (S:). Solo rows compare to the solo ticket's own base branch, not the master integration branch:
```
Legend: P:portion S:solo

Item         Status      Branch                  Behind  Ahead  Remote      Action
P-001      executing     feature/P-001-api       0       3      unpushed    PUSH
S-001      executing     feature/PD-123456-auth  2       1      in sync     MERGE PARENT
```

### Solo ticket workflow

1. **Adopt or create** - Bring the external ticket into DAC as the next `S-###`; retain its independent Jira parent, team, labels, and base branch
2. **Review envelope** - Ensure acceptance criteria, scope, test obligations clear
3. **Create branch** - Follow branch naming from envelope
4. **Execute** - Implement with authority model (W1, C3, V2, R4)
5. **Track progress** - Use `transition` to update status
6. **Sync branch** - Keep up to date with that solo ticket's configured base branch
7. **Record result** - Create result artifact on completion

### Promoting solo tickets to portions

When a solo ticket grows into part of a larger initiative, you can:

1. Create or identify the parent Epic/Feature
2. Initialize DAC coordination for the parent
3. Convert the solo envelope to a portion envelope
4. Add to portion plan and integration plan
5. Remove from `solo/` directory

This preserves the work and audit trail while integrating into full DAC coordination.

## Getting Help

Type `/dac-help` at any time for:
- Guidance on current phase
- When to partition vs. keep simple
- Jira strategy recommendations
- Troubleshooting stuck portions
- How to resume after interruption
- Solo ticket vs. portion decision
