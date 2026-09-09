---
artifact: solo
workstream: {{WORKSTREAM_ID}}
title: {{SOLO_ID}} - {{TITLE}}
solo_id: {{SOLO_ID}}
ticket_id: {{TICKET_ID}}
stage: solo
status: {{STATUS}}
last_updated: {{NOW}}
inputs: -
executor: {{EXECUTOR}}
jira: {{TICKET_ID}}
jira_url: {{JIRA_URL}}
branch: {{BRANCH}}
base_branch: {{BASE_BRANCH}}
---

<!-- Template note: symbols are examples from references/visual-language.md.
     Always read visual-language.md and use its current assignments. -->

# {{WORKSTREAM_LABEL}} — {{SOLO_ID}}: {{TITLE}} ({{TICKET_ID}})

## 💭 Outcome and boundaries

- Outcome: {{OUTCOME}}
- Included:
- Excluded:
- Jira: [{{TICKET_ID}}]({{JIRA_URL}})

## 📋 Acceptance Criteria

{{ACCEPTANCE_CRITERIA}}

## 🎯 Scope

### What's In
- 

### What's Out
- 

## ⚖️ Decisions and Assumptions

- Key decisions:
- Assumptions:
- Escalation conditions:

## 🧭 Execution approach

- Executor: {{EXECUTOR}}
- Base branch: {{BASE_BRANCH}}
- Working branch: {{BRANCH}}
- Branch status: not_created

## 🟰 Change and authority envelope

- Expected files, components, or systems:
- Explicit exclusions:
- W1 scope: .dac/{{WORKSTREAM_ID}}/solo/
- Proposed C3 scope:
- V2 validation scope:
- R4 actions: Jira updates, PR creation, merge

## 📋 Test obligations

- Unit tests:
- Integration tests:
- Manual verification:
- Failure cases:

## 🎬 Adoption/Creation record

- Workstream: {{WORKSTREAM_ID}}
- Jira last verified: {{NOW}}
- Repository last verified: {{NOW}}
- Adopted/created at: {{NOW}}
- Source: {{SOURCE}}

## Approval record

| Timestamp | Approver | Scope | Notes |
|---|---|---|---|
<!-- APPROVAL_LOG -->

## State log

| Timestamp | Previous | New | Actor | Evidence or reason |
|---|---|---|---|---|
| {{NOW}} | - | {{STATUS}} | system | {{SOURCE}} |
<!-- STATE_LOG -->
