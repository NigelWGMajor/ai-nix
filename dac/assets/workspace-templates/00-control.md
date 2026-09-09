---
artifact: control
workstream: {{WORKSTREAM_ID}}
workspace_label: {{WORKSTREAM_LABEL}}
context_suffix: {{CONTEXT_SUFFIX}}
master_branch: -
target_branch: -
stage: control
status: drafting
last_updated: {{NOW}}
inputs: Jira {{WORKSTREAM_ID}}, repository {{REPO_ROOT}}
---

<!-- Template note: symbols are examples from references/visual-language.md.
     Always read visual-language.md and use its current assignments. -->

# {{WORKSTREAM_LABEL}} DAC Control: {{TITLE}}

## 💭 Resume here

- Current phase: alignment
- Current status: drafting
- Read next: `01-mission.md`
- Next action: align on the parent mission
- Required authority: R0; request W1 before editing this workspace

## 🧭 Repository and Jira context

| Field | Value |
|---|---|
| Repository | `{{REPO_ROOT}}` |
| Parent Jira | {{JIRA_REFERENCE}} |
| Branch | To verify |
| HEAD | To verify |
| Worktree | To verify |
| Last verified | {{NOW}} |

## 🔗 Parent artifacts

| Artifact | Purpose | Status |
|---|---|---|
| [Mission](01-mission.md) | Outcome, scope, success | not_started |
| [Evidence](02-evidence.md) | Jira and repository truth | not_started |
| [Decisions](03-decisions.md) | Shared choices and deferrals | not_started |
| [Portion plan](04-portion-plan.md) | Partition and dependency graph | not_started |
| [Jira plan](05-jira-plan.md) | Management hierarchy and writes | not_started |
| [Integration plan](06-integration-plan.md) | PR, merge, rollout, rollback | not_started |
| [Portions](portions/) | Executor-neutral handoffs | not_started |
| [Results](results/) | Normalized executor returns | not_started |
| [Reviews](reviews/) | Parent integration evidence | not_started |

## 🟰 Open gates

| Gate | Content or action | Class | Exact scope | Status | Owner |
|---|---|---|---|---|---|
| GATE-001 | Parent mission | content | `01-mission.md` | open | decision maker |
| GATE-002 | Portion necessity, reuse, and security review | content | `04-portion-plan.md` review; one row per active proposed portion | open | coordinator |

## ⚖️ Open decisions

See `03-decisions.md`.

| ID | Summary | Owner | Needed by | Status |
|---|---|---|---|---|
| - | None recorded | - | - | - |

## 📋 Approval and action log

| Timestamp | Approver | Artifact or action | Class | Scope | Notes |
|---|---|---|---|---|---|
<!-- GATE_LOG -->

## 📚 Change log

| Timestamp | Change | Evidence |
|---|---|---|
| {{NOW}} | Workspace initialized | DAC helper |

## Branch switch registry

| Timestamp | Source | Target | Stash marker | State | Notes |
|---|---|---|---|---|---|
<!-- SWITCH_LOG -->
