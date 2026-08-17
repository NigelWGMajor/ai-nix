---
name: act
description: Extract concise, focused information from analysis output or raw material and shape it for a specific action — a Jira ticket description, an executive summary, a Slack message, a task list, a handoff note, or a decision brief. Use when you need to turn findings into movement. Do not use for the analysis itself — use nix, wiz, lit, kit, fix, or val for that, then act to extract the actionable artifact.
---

# ACT Action Extraction

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the extraction workflow.

Transform analysis, findings, or raw information into a concise artifact shaped for a specific action:

`Intake -> Distill -> Shape -> Deliver`

Act is the last-mile skill. It takes the output of any other skill (or raw material) and produces exactly the artifact needed to move work forward — nothing more, nothing less.

## Standalone contract

- Contain the entire method in this package.
- Never require, invoke, or read RECIPE, LIT, KIT, NIX, WIZ, their phase skills, their caches, or their outputs at runtime.
- Do not require subagents, mentor agents, special slash commands, or model routing.
- Always produce output in the conversation. Act does not create `.data/` instances — its value is immediacy, not durability. If the user wants to save the output, they can copy it or ask for a file.
- Do not perform the underlying analysis. If the source material is insufficient, recommend the appropriate analysis skill first.
- Read-only: do not create Jira tickets, send messages, or push content to external systems unless the user separately authorizes that specific action.

## Load formatting guidance

At the start of every extraction:

1. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Use its palettes when the target format benefits from visual markers.
2. Use [references/jira-integration.md](references/jira-integration.md) when the target format is a Jira ticket — apply its field conventions, acceptance criteria formatting, and ADF structure.
3. Read repository-local instructions when the target artifact lives in the repository (e.g., PR descriptions, commit messages).

## Resolve the source and target

Identify two things:

1. **Source material**: what to extract from. One of:
   - Output from another skill (a Findings.md, a wiz review, a fix diagnosis, a nix analysis).
   - A `.data/<skill>-*` instance directory — use its `Findings.md`.
   - Raw material supplied in the prompt (pasted text, URLs, conversation context).
   - The current workspace state (branch, diff, recent commits).

2. **Target format**: what to produce. One of:
   - **Ticket**: Jira issue description with summary, description, acceptance criteria, and labels.
   - **Summary**: executive summary for a non-technical audience (email, Slack, status update).
   - **Task list**: ordered, actionable items with owners, targets, and completion criteria.
   - **Handoff**: concise briefing for someone picking up the work.
   - **Decision brief**: options, criteria, recommendation, and tradeoffs for a decision-maker.
   - **PR description**: title, summary, test plan, and reviewer guidance.
   - **Message**: focused communication for a specific audience and channel.
   - **Custom**: user-specified format.

If either is ambiguous, ask one concise question. Do not guess at the target format.

## Run the four-stage extraction

### 1. Intake

Understand the source material:

- Read the source completely before extracting.
- Identify the central conclusion, key findings, open questions, and recommended actions.
- Note the evidence basis and confidence levels from the source.
- Identify the audience for the target artifact — what do they need to know and what can be omitted?

### 2. Distill

Extract only what the target audience needs:

- Strip analysis scaffolding, methodology notes, and evidence chains that served the analysis but not the action.
- Preserve critical context that would be lost without it.
- Preserve uncertainty — do not polish qualified findings into confident assertions.
- Keep source traceability: if the artifact references a finding, the reader should be able to trace it back.
- When the source uses opaque identifiers (work item IDs, requirement codes, phase numbers), define them in the artifact or link to the parent document's definitions.
- Rank information by action value, not by source order or volume.

### 3. Shape

Format for the target medium:

**Ticket format:**
- Summary: one line, action-oriented, under 80 characters.
- Description: problem, context, proposed approach, and scope.
- Acceptance criteria: testable, specific, and complete.
- Labels, components, and priority when inferrable from the source.

**Summary format:**
- Lead with the conclusion or status.
- One paragraph of context.
- Key risks or decisions needed.
- Recommended next action.

**Task list format:**
- Ordered by dependency, then priority.
- Each item: action verb, target, completion criterion.
- Flag items that require decisions or external input.
- Flag items that block other items.

**Handoff format:**
- Current state: what's done, what's in progress, what's blocked.
- Key decisions already made and their rationale.
- Open questions and who can answer them.
- Immediate next action with stopping condition.

**Decision brief format:**
- Decision needed: one sentence.
- Options with tradeoffs (table or bullets).
- Recommendation with rationale.
- Deadline or consequence of delay.

**PR description format:**
- Title: short, descriptive, under 70 characters.
- Summary: what changed and why (not how).
- Test plan: what was validated and how.
- Reviewer notes: what to focus on, what's intentionally left out.

**Message format:**
- Match the channel's conventions (Slack = concise, email = structured).
- Lead with the ask or news.
- Provide only enough context for the reader to act.

### 4. Deliver

Present the artifact:

- Return the shaped artifact in the conversation, ready to copy.
- If the target is a Jira ticket, format with clear field labels so it can be pasted into Jira.
- If multiple artifacts were requested, separate them clearly.
- State what was omitted and why, so the user can judge completeness.
- If the source material was insufficient for a confident extraction, say so and recommend the analysis skill that would fill the gap.

## Evidence and attribution

- When the source used evidence classifications (Observed, Claimed, Inferred, Unknown), preserve the classification for consequential claims in the target artifact.
- When the source used finding IDs (F-01, KIT-001, H-01), reference them in the artifact so the reader can trace back.
- Do not elevate uncertain findings to confident assertions during extraction. If the source said "plausible but unverified," the ticket should not say "confirmed."

## Quality check

Before returning the artifact, verify:

- The artifact serves the stated target format and audience.
- The central message matches the source's actual conclusion.
- Uncertainty and limitations from the source are preserved, not polished away.
- The artifact is self-contained — the reader should not need to read the source to act on it.
- The artifact is concise — every sentence earns its place.
- Source-originated identifiers are defined or linked to their definitions in the parent document.
- No action was taken (no ticket created, no message sent, no code changed) without explicit authorization.
