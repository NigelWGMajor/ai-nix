# DAC Artifact Contract

## Purpose

Keep the workstream understandable and resumable without hidden conversation history. Use Markdown as the human interface and simple YAML frontmatter as the helper interface.

## Workspace

```text
.dac/<workstream>/
  00-control.md
  01-mission.md
  02-evidence.md
  03-decisions.md
  04-portion-plan.md
  05-jira-plan.md
  06-integration-plan.md
  portions/
    portion-template.md
    P-001.md
  results/
    result-template.md
    P-001.md
  reviews/
    integration-review-template.md
```

`00-control.md` is the only required resume entrypoint. The coordinator alone updates shared registers. Executors write their own assigned artifacts or return a result for ingestion.

## Frontmatter

Use scalar values only:

```yaml
---
artifact: portion
workstream: ABC-123
portion_id: P-001
stage: portions
status: proposed
last_updated: 2026-07-31T12:00:00-05:00
inputs: 01-mission.md,03-decisions.md,04-portion-plan.md
depends_on: P-000
executor: speckit
jira: ABC-124
spec_directory: specs/021-abc-124-contract
---
```

Allowed statuses are `not_started`, `drafting`, `proposed`, `approved`, `executing`, `blocked`, `pr_open`, `integrated`, `complete`, and `superseded`.

`approved` means the content is accepted. It does not grant C3 or R4 authority. Readiness is derived: a portion is ready when it is `approved` and each dependency is `integrated` or `complete`.

## Stable identity

Never recycle a portion or decision ID. Use `P-001`, `P-002`, and `DEC-001`. If scope changes materially, supersede the old item and create a new one. Allocate Jira keys, Spec Kit directories, branch names, and PR identifiers centrally before concurrent execution.

## Title-line identity

Every generated DAC artifact must start its first Markdown title line with the parent Jira ticket, for example `# PD-123456 — Evidence and Current Behavior`. This includes parent artifacts, portion envelopes, results, solo-ticket envelopes and results, and integration reviews. The parent key is the workspace workstream value; never substitute a child Jira ticket for it.

## Sources of truth

| Concern | Authority |
|---|---|
| organizational commitment, ownership, visible status | Jira |
| parent mission, decisions, dependencies, authority, integration | `.dac/<workstream>/` |
| portion boundary and delegated freedom | `portions/<id>.md` |
| portion-local requirements and plan | routed executor artifacts |
| observed behavior | code, tests, and runtime evidence |
| review and integration | PR/CI plus DAC results and reviews |

When sources disagree, record the discrepancy and obtain a decision. Do not silently choose the most convenient source.

## Evidence and revisions

Reference Jira keys and canonical URLs, repository-relative paths and symbols, commits, PRs, documents, exact commands, observed results, and timestamps. Distinguish fact, inference, assumption, and unknown.

Prefer concise relative Markdown links for evidence:

- Bookmark: `[🔖 Description](relative/path.md#heading)`.
- File: `[🔗 Description](relative/path.md)`.
- Jira ticket: `[🎟️ ABC-123](url)`.
- Pull request: `[🔀 PR #123](url)`.
- Other external source: `[🔗 Description](url)`.

## Visual presentation

Use symbols only from `visual-language.md`, at most one leading symbol per heading, and never as the sole carrier of meaning. The visual-language reference is authoritative; its current symbol assignments override any symbols in templates.

A handoff records the parent decision IDs, upstream contracts, Jira verification time, base branch, and base commit it relied upon. Recheck volatile facts before execution and integration.

## Approval semantics

A content approval accepts an artifact as input to later reasoning. An action approval names the class, exact files or systems, constraints, approver, and timestamp. Spec Kit or another skill cannot broaden the coordinator's approval.

Record the user's actual approval wording when practical. A general positive response does not authorize code, Git, Jira, PR, test, or deployment actions.

## State transitions

Normal portion flow:

```text
proposed -> approved -> executing -> pr_open -> integrated
                         |             |
                         +-> complete  +-> blocked
                         +-> blocked
```

Use `complete` for portions with no PR integration requirement. After resolving a blocker, return the portion to `approved`, recheck readiness and authority, and then move it to `executing`. Any active state may be superseded through an explicit decision.

## Result ingestion

A result is evidence, not automatic acceptance. The coordinator verifies it against the envelope and records:

- executor and run identity
- base and resulting revision
- changed surface
- requirement and test trace
- deviation and escalation disclosures
- PR or deliverable state
- downstream effects

Only the coordinator changes the central portion state and dependency graph.
