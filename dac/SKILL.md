---
name: dac
description: Coordinate complex Jira-backed feature or project delivery through a divide-and-conquer workflow. Use when Codex or Claude needs to align on a parent outcome, investigate Jira and code evidence, resolve shared decisions, partition work into dependency-aware portions, route each ready portion to Spec Kit, another skill, a direct implementation agent, or a human, and reconcile results through pull-request integration. Maintain resumable, human-readable Markdown while keeping Jira as the management view and requiring explicit approval for local, code, Git, Jira, and remote mutations.
---

# Divide-and-Conquer Delivery

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the coordination workflow.

## Objective

Coordinate a large outcome without requiring any participant to hold the whole implementation in context. Keep shared intent, decisions, dependencies, Jira visibility, and integration at the parent level. Give each executor a bounded portion envelope and require a normalized result.

Treat Jira and repository artifacts as evidence that may disagree. Treat approved DAC artifacts as the coordination record, child specifications as portion-local detail, code and tests as observed behavior, and Jira as the management view.

## Folder Convention

**DAC internal artifacts** live under `.dac/<workstream>/` in the repository root and should be excluded from version control (typically via global gitignore):

- All coordination files: `00-control.md`, `01-mission.md`, `02-evidence.md`, `03-decisions.md`, `04-portion-plan.md`, `05-jira-plan.md`, `06-integration-plan.md`
- Portion envelopes: `portions/P-001.md`, `portions/P-002.md`, etc.
- Result records: `results/P-001-result.md`, etc.
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
3. **Jira** - Jira organization reviewed and approved
4. **Execute** - Portions routed and executing
5. **Integrate** - PRs merged, convergence complete

## Start or resume

**Show progress indicator first.**

1. Confirm the repository root, branch, HEAD, and worktree state without changing them.
2. Identify the parent Jira issue or stable workstream ID. Do not guess among plausible parents.
3. Discover available Jira, repository, GitHub, Spec Kit, and skill capabilities. For Jira access, use the Atlassian MCP server tools (prefixed `mcp__atlassian__`). Verify the server is available by attempting a lightweight call. If the server is unreachable or returns a connection error, advise the user:

   > Could you try restarting the MCP server? You can either:
   > 1. Run `! /mcp` in this prompt to check MCP server status
   > 2. Use `curl` with your MCP credentials to access the Atlassian API directly
4. Look for `.dac/<workstream>/00-control.md`.
   - If it exists, read it first and resume its recorded next action.
   - If it does not, align on the intended outcome in conversation and request W1 approval.
5. After W1 approval, initialize the workspace:

```bash
python <skill-dir>/scripts/dac.py init --workstream ABC-123 --repo-root . --title "Outcome"
```

Read [references/artifact-contract.md](references/artifact-contract.md) before initializing, approving, resuming, or validating a workspace.

Read [references/jira-integration.md](references/jira-integration.md) for Jira field discovery, acceptance criteria formatting, and the Jira organization review step.

Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols used in DAC artifacts. Its current assignments override any symbols hardcoded in templates or other reference files. Use its shared output-spine and evidence-status palettes when composing workspace artifacts and completion reports.

## Coordinate the workstream

### 1. Align and investigate

Produce and approve, in order:

1. `01-mission.md`: outcome, users, success criteria, scope, non-goals, and constraints.
2. `02-evidence.md`: relevant Jira graph, current repository behavior, tests, contracts, discrepancies, and confidence.
3. `03-decisions.md`: shared clarifications, alternatives, decisions, owners, and deferrals.

Resolve decisions that could alter portion boundaries or shared contracts before partitioning. Preserve later discoveries as new or superseding decisions; never rewrite history silently.

### 2. Partition by outcomes

Produce `04-portion-plan.md`. Prefer portions that are independently understandable, testable, reviewable, and suitable for one Jira child and one PR.

Each portion must have:

- one coherent outcome and explicit non-goals
- traceability to parent success criteria
- stable inputs, outputs, and compatibility obligations
- explicit dependencies and downstream consumers
- a bounded change surface and test obligation
- a proposed executor route
- an escalation boundary

Prefer vertical slices. Create a foundation portion only for a genuinely shared contract, additive schema, compatibility adapter, migration, or reusable capability. Reject cycles, hidden blockers, unsafe parallel file overlap, and partitions that merely mirror architecture layers.

### 3. Review Jira organization (MANDATORY)

**ALWAYS pause after portion plan approval to review Jira structure,** regardless of complexity:

Present the proposed Jira organization:

| Portion | Proposed Jira | Type | Parent | Rationale |
|---------|--------------|------|--------|-----------|
| P-001   | ...          | ...  | ...    | ...       |

**Jira child issue requirements:**
- **Always create child issues as Stories** (never subtasks) for better tracking
- **Copy parent labels** to all child issues
- **Copy parent team field** to all child issues
- Link children to parent with "Created By" relationship

**Questions to ask:**
- Should we reuse existing issues or create new ones?
- What work is in DAC scope vs. handled separately?
- Are there additional labels needed for specific portions?

**Simple case example:** "Both PRs under ABC-123, no new tickets needed"
**Complex case example:** "Create 4 Story issues linked to parent ABC-123, inheriting labels and team"

After Jira structure approved, produce:

- `05-jira-plan.md` for the proposed parent, child issues, links, ownership, exact remote actions, and acceptance criteria field discovery.
- `06-integration-plan.md` for branches or worktrees, PR bases, merge order, compatibility states, rollout, and rollback.
**Branching strategy — parallel by default:**
Every portion branches independently from the target branch (usually `main`). Dependencies govern **merge order**, not branch parentage. Never stack a portion branch on a sibling's PR branch unless there is a verified compile-time dependency between them (one portion's code imports or references the other's new symbols and will not build without them).
- **Test the assumption:** before stacking, confirm the downstream portion actually fails to build on `main` alone. SQL stored procedures, configuration, and runtime contracts are deployment-order dependencies, not code dependencies — they do not justify stacking.
- **Merge gates, not branch gates:** record which portions must merge first in the integration plan table. The PR can be opened and reviewed in parallel; only the merge is sequenced.
- **Worktrees are optional:** use them for editing convenience when working on multiple portions simultaneously, not for code isolation. Since all branches are independent, `git stash` / `git checkout` is sufficient for single-directory workflows.
- **Always commit before switching:** never leave portion work as uncommitted changes in a worktree. Uncommitted work is lost if the worktree branch is switched or the worktree is removed.

Content approval does not authorize Jira or GitHub writes. Require R4 approval, execute only the approved payload, then read back and record the actual result.

**When creating Jira issues:**
- Always create child issues as **Story** type (never subtasks)
- Copy **labels** from parent to all children
- Copy **team field** from parent to all children
- Link children to parent with "is part of" relationship type
- Include acceptance criteria in the dedicated custom field (NOT in description)
- Copy the **parent** from the parent issue to the child issues
- See [references/jira-integration.md](references/jira-integration.md) for field discovery, ADF format, and common mistakes

### 4. Materialize portion envelopes

Create a portion only after the partition is approved:

```bash
python <skill-dir>/scripts/dac.py portion create \
  --workspace .dac/ABC-123 \
  --id P-001 \
  --title "Add compatibility contract" \
  --executor speckit \
  --jira ABC-124
```

Use `--depends-on P-001,P-002` when needed. Approve the completed envelope as content before routing it. A portion becomes planning-ready only when its envelope is approved and every dependency is `integrated` or `complete`:

```bash
python <skill-dir>/scripts/dac.py ready --workspace .dac/ABC-123
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

- outcome: completed, blocked, failed, or superseded
- artifact, branch, commit, and PR references when applicable
- files or systems changed
- acceptance criteria and test evidence
- deviations, assumptions, discoveries, and contract effects
- residual work and downstream recommendations

Create a result artifact and have the coordinator update shared state. Child executors must not write the parent registry concurrently.

### 7. Integrate and converge

Before accepting a portion result, verify its envelope, approvals, actual diff or output, tests, compatibility, and escalation disclosures. Mark a portion `integrated` only after its required PR or deliverable is accepted. Recalculate the ready set and update Jira only with R4 approval.

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

## Helper boundaries

The bundled helper manages Markdown under one `.dac` workspace. It can initialize, validate, record approvals and decisions, create portions and results, derive readiness, and record permitted state transitions. It never invokes Jira, Spec Kit, another skill, Git, tests, builds, deployment, or network tools.

```bash
python <skill-dir>/scripts/dac.py status --workspace .dac/ABC-123
python <skill-dir>/scripts/dac.py validate --workspace .dac/ABC-123
python <skill-dir>/scripts/dac.py approve --workspace .dac/ABC-123 --artifact 01-mission.md --by "Name" --scope "Mission and success criteria"
python <skill-dir>/scripts/dac.py decision --workspace .dac/ABC-123 --id DEC-001 --question "Question" --outcome "Decision" --by "Name"
python <skill-dir>/scripts/dac.py transition --workspace .dac/ABC-123 --portion P-001 --to executing
python <skill-dir>/scripts/dac.py result create --workspace .dac/ABC-123 --portion P-001
```

## Completion response

**Show progress indicator:**
```
DAC Progress: [✓] Align → [✓] Partition → [✓] Jira → [✓] Execute → [●] Integrate
```

Produce a completion summary using symbols from `visual-language.md`. Report the parent outcome, completed and deferred portions, executor and Jira mapping, dependency and PR sequence, decisions, tests, integration evidence, rollout and rollback, remaining risks, and the resume path under `.dac/<workstream>/`.

Use the shared evidence link conventions from `artifact-contract.md` for Jira tickets, PRs, and file references.

## Getting Help

Type `/dac-help` at any time for:
- Guidance on current phase
- When to partition vs. keep simple
- Jira strategy recommendations
- Troubleshooting stuck portions
- How to resume after interruption
