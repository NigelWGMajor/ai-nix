# DAC Intent Brief and Traceability Check

## Purpose

Catch a misconstrued mission before it is partitioned. A portion plan can pass every per-portion check (see [portion-sanity-review.md](portion-sanity-review.md)) and still be wrong if the shared understanding of the outcome is wrong. The two lightweight steps below bracket the partition: the **intent and strategy brief** confirms the mission before `04-portion-plan.md` is drafted, and the **traceability check** confirms the draft plan stays inside that confirmed intent.

The methods are adapted from VET and COP (requirement register, assumption audit, scope control, pattern fit). Neither step invokes `/vet`: VET is anchored to a Git branch, PR, and comments, none of which exist at partition time.

## Intent and strategy brief

Produce after `01-mission.md`, `02-evidence.md`, and `03-decisions.md` are drafted and before any portion is proposed. Keep it to roughly 10-15 lines; it is a confirmation aid, not a second mission document.

| Element | Content |
|---|---|
| Outcome, restated | The outcome in the coordinator's own words, not copied from Jira. |
| Non-goals | What this work will explicitly not touch, including adjacent cleanup or refactoring that is tempting but out of scope. |
| Patterns and extension points | The existing capabilities and conventions expected to be followed, each with an evidence path or symbol. State `none found after inspection` rather than leaving it blank. |
| Strategy shape | The approach at the level of `reuse`/`extend`/`new` per area, for example "extend X; one additive SQL migration; no new service". No portion boundaries yet. |
| Assumptions and overreach risks | Assumptions that, if wrong, would change the strategy; places where the plan could grow beyond the ask. |
| Open questions | At most one or two questions where intent is ambiguous. |

Apply these COP passes while drafting: requirement alignment and scope control; assumption audit (no invented structure, schema, or contract); simplicity and pattern fit.

Present the brief in chat and record it under **Intent and strategy brief** in `01-mission.md`. The user confirms or corrects it. Record the confirmation in the mission approval record, and record any correction that changes scope or strategy as a decision in `03-decisions.md`. Do not draft `04-portion-plan.md` until the brief is confirmed.

### Re-confirmation

A confirmed brief is not re-asked on resume merely because time passed. Reopen it only through the existing drift rules: a parent decision or acceptance criterion changed, or Jira or the target branch changed materially. Record the change as a new or superseding decision, mark the brief `superseded`, and present the revised brief.

### Preview mode

The blanket W1 approval for preview does not cover this step. Preview pauses once for brief confirmation, because a wrong intent wastes the entire run. After confirmation, preview continues without further pauses.

## Traceability check

Run automatically after drafting `04-portion-plan.md`, alongside the necessity, reuse, and security review and before content approval. It is lightweight: record the matrix, surface only the flags, and do not ask the user anything unless a flag cannot be resolved from evidence.

| Direction | Question | Flag |
|---|---|---|
| Forward | Does every mission success criterion map to a portion or integration check? | `gap` |
| Reverse | Does every active portion trace to a mission criterion and to the confirmed brief's strategy? | `overreach` |
| Non-goals | Does any portion touch a stated non-goal? | `overreach` |
| Pattern fit | Does every portion follow the patterns named in the brief, or state why it deviates? | `deviation` |

Record the result in the **Traceability and overreach check** table in `04-portion-plan.md`.

- With W1 authority, correct a flag directly when evidence establishes the correction and the confirmed brief is unchanged (for example, remove a portion that traces to no criterion). Record the correction in the portion plan and control change log.
- A flag that would require changing the confirmed brief is a drift event. Route it to the parent decision register and the user rather than editing the brief silently.
- `04-portion-plan.md` may be approved only when no `gap`, `overreach`, or `deviation` flag is open.

This check is planning evidence only. It neither authorizes implementation nor replaces code review or integration validation.

## Part plan check (one level down)

The same pattern repeats inside a portion. Portions are split by dependency and deployment sequencing; **parts** (`P-003-a`, `P-003-b`, ...) are split by workload and responsibility, and usually map to one commit. Cross-cutting decisions are made at the brief and portion level, so a part needs only the decisions that pertain to it.

Draft the part plan when the portion starts: after the executor is routed and before any C3 work. Record it in the portion envelope's **Part plan** table and show that table to the user. A portion with one part is a single row; do not add ceremony.

Each part needs:

| Element | Content |
|---|---|
| Purpose | One responsibility, in a sentence. |
| Traces to | The portion strategy and mission criterion it serves. |
| Change surface | Files or components touched, within the portion's change surface. |
| Resume and review guidance | Where to pick up if interrupted, what the user should review, and links to the relevant DAC files, spec directory, or commit. |

Run the lightweight check automatically and surface only flags:

- Every part traces to the portion outcome and the confirmed strategy (`overreach` otherwise); the parts together cover the portion's acceptance criteria (`gap` otherwise).
- Every part follows the pattern named for the portion, or states why it deviates (`deviation`). Reuse and security approach are inherited from the portion review and are not repeated.
- No part leaves the portion's change surface or touches a stated non-goal.
- Parts are ordered and run strictly in sequence. Do not propose parallel parts.
- A part sized beyond roughly one commit of work is split.

A flag that would contradict the portion plan is an escalation to the portion level, not a local edit. One content approval covers the whole part plan; C3 approval for the portion covers its parts, so do not prompt per part.

### Spec Kit routing

A `speckit` route keeps its own specify-through-converge cycle. The parts still exist: they give the user the map of what needs resumption or review, and name the stage or task group each part corresponds to. Spec Kit's detail must stay within the parts' purposes; a contradiction is a portion-level escalation.
