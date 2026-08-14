<!-- Template note: symbols in this template are examples drawn from references/visual-language.md.
     Always read visual-language.md before generating output and use its current symbol assignments.
     If visual-language.md has been updated since this template was last edited, its symbols take precedence. -->

# Work-in-progress review: [ticket, PR, or branch]

> **Purpose/question:** [What this review assesses and enables]
>
> **Audience/use:** [Who needs this assessment and why]
>
> **Scope:** [Target ticket/PR/branch, included change states, affected surfaces]
>
> **Evidence boundary:** [What was inspected, what was inaccessible, remote-refresh status]
>
> **Status/freshness:** [Review timestamp, exact HEAD, worktree state]
>
> **Material limitations:** [Constraints that affect the whole review]
>
> **Depth:** [Quick, Standard, or Deep]
>
> **Overall assessment:** [One concise, calibrated conclusion]

## 💭 Intent - orientation

[Explain what the work is trying to accomplish, why it matters, the dominant concern or strength, and the safest next action.]

### At a glance

| Dimension              | Current status                | Evidence/confidence           |
| ---------------------- | ----------------------------- | ----------------------------- |
| Target                 | [Ticket/PR/branch identity]   | [Freshly resolved]            |
| Intended outcome       | [What the work delivers]      | [Ticket/PR evidence]          |
| Implementation state   | [Summary]                     | [Evidence class]              |
| Most serious concern   | [Finding or none]             | [Seriousness and confidence]  |
| Notable strength       | [Strength or none]            | [Evidence]                    |
| Validation state       | [Passed/failed/partial/not run] | [Scope]                     |
| Best next step         | [Action]                      | [Prerequisite]                |

### 🧭 Scope envelope

- **Intended outcome:** [User or system outcome from the ticket/PR]
- **Acceptance criteria:** [Explicit criteria from the ticket]
- **Non-goals:** [Explicit exclusions]
- **Target/base:** [Branch, base, and change states included]
- **Affected surfaces:** [Named by ticket or diff]
- **Constraints:** [Technical, business, access, or evidence constraints]
- **Assumptions:** [Material bounded assumptions]

## 🔗 Evidence - relationships and evidence

### 🔎 Strengths

- **G-01 - [Title]** — [Observed evidence with links/lines. State what makes this a good decision and why it matters.]

### Concerns

- **F-01 - [Title]**
  - **Seriousness:** [Critical | High | Medium | Low | Note]
  - **Confidence:** [High | Medium | Low]
  - **Evidence class:** [Observed | Claimed | Inferred | Unknown]
  - **Evidence:** [Specific citations with path:line]
  - **Impact:** [Effect on the stated intent]

### Evidence gaps

- [Missing or inaccessible evidence and why it matters]

### Discovered relationships

- **R-01 -> F-01:** [Caller, consumer, contract, state, data, test, deployment, or issue relationship and its evidence]
- **Scope extension:** [Only when justified, with evidence-based reason]

## 💡 Ideation - detailed analysis

- **I-01 -> F-01:** [Recommended direction, viable alternatives, tradeoffs, and confidence]
- Keep optional ideas visibly separate from changes required to meet intent.

## 🟰 Findings - findings and decisions

[Synthesize the overall picture: what is genuinely complete, what needs work, what decisions remain open.]

### Material findings

| ID   | Finding                    | Seriousness | Confidence | Impact                     |
| ---- | -------------------------- | ----------- | ---------- | -------------------------- |
| F-01 | [Concise finding]          | [Level]     | [Level]    | [Effect on intent]         |

### Open decisions

| Decision              | Owner/input needed | Impact if unresolved       | Safe interim state         |
| --------------------- | ------------------ | -------------------------- | -------------------------- |
| [Decision]            | [Who decides]      | [Consequence]              | [What to do meanwhile]     |

## 📋 Realization - validation

- **Acceptance criteria:** [Met | Partially met | Not met | Unable to verify], with evidence
- **Tests/checks:** [Passed | Failed | Blocked | Not run], naming what was observed

| Result                                                   | Check                  | Purpose                      | Evidence or limitation          |
| -------------------------------------------------------- | ---------------------- | ---------------------------- | ------------------------------- |
| [Passed, failed, partial, blocked, proposed, or not run] | [Command or procedure] | [Question, finding, or risk] | [Observed result or limitation] |

## 🎬 Implementation - next steps

1. **A-01 -> I-01: [Action]**
   - Outcome: [What this establishes or fixes]
   - Target: [Files, symbols, tests, or components]
   - Compatibility: [Rollback or compatibility considerations]
   - Validation: [Focused check]
   - Stop when: [Checkpoint]

### Remaining risks and follow-ups

- [Remaining risks and focused follow-ups beyond immediate actions]
- [Positive summary of what the work already accomplishes well]

## 📚 Evidence index

| ID   | Source                                           | Role                  | Evidence class or limitation                   |
| ---- | ------------------------------------------------ | --------------------- | ---------------------------------------------- |
| E001 | [Precise path, symbol, heading, output, or link] | [What it establishes] | [Observed, claimed, freshness, or scope limit] |
