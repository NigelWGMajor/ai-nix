# Shared visual language

Use this file as the single editable source of truth for symbols in LIT, KIT, NIX, and PIX output. Each skill package contains its own copy so it remains standalone.
Update in ./nix/references and keep the four copies in sync using the `ps` deploy script.

Symbols support scanning and semantic consistency. They are never decoration or the sole carrier of meaning.

## Rules

- Typically use at most one leading symbol in a heading (unless the first is a highlight).
- Pair every symbol with explicit text.
- Only usewhen such is aiding comprehension, ordering, filtering.
- Use the shared output-spine symbols for equivalent sections across all three skills.
- Use the NIX stage symbols only for NIX's six-stage method.
- Never use a verification symbol for a claim, inference, proposal, or unexecuted check.
- In a hierarchy, prefix each displayed state with its configured state symbol where that state aids scanning; retain the state name as text.
- Keep symbol density restrained and use consistently within one document to aid readability.

## Highlighting

| Role           | Symbol | Usage rule                                       |
| -------------- | ------ | ------------------------------------------------ |
| Key Point      | 📌     | Draw attention to a critical point to understand |
| Call to action | 🎬     | Item needing attention                           |
| Bandaid        | 🩹     | Workaround or tenporary fix                      |


## Shared output-spine palette

| Role                       | Symbol | Meaning                                                 | Usage rule                                                        |
| -------------------------- | ------ | ------------------------------------------------------- | ----------------------------------------------------------------- |
| Orientation                | 💭     | Rapid reader orientation                                | Use for the opening mental model and current position.            |
| Foundations                | 🧭     | Required context or vocabulary                          | Use for concepts that later sections depend on.                   |
| Relationships and evidence | 🔗     | Flows, boundaries, dependencies, or traceability        | Use for the system or source model.                               |
| Detailed analysis          | 💡     | Skill-specific examination, ideation                    | Use when analysis needs a distinct section beyond relationships.  |
| Findings and decisions     | 🟰     | Conclusions, strengths, risks, tradeoffs, and decisions | Use for the main synthesis or assessment.                         |
| Validation                 | 📋     | Executed or proposed checks                             | Clearly distinguish executed checks from proposed checks.         |
| Next steps                 | 🎬     | Actionable continuation                                 | State target, purpose, expected evidence, and stopping condition. |
| Evidence index             | 📚     | Source and evidence navigation                          | Use for the final evidence map, not every citation.               |

## NIX stage palette

| Stage   | Symbol | Shared role                | Meaning                                                           |
| ------- | ------ | -------------------------- | ----------------------------------------------------------------- |
| Reflect | 💭     | Foundations                | Frame the question, scope, constraints, and assumptions.          |
| Explore | 🧭     | Relationships and evidence | Establish the evidence landscape and gaps.                        |
| Connect | 🔗     | Relationships and evidence | Build the system model and explain impact.                        |
| Imagine | 💡     | Detailed analysis          | Explore grounded implications, alternatives, and counterfactuals. |
| Produce | 🚧     | Findings and decisions     | Synthesize the durable explanation and conclusions.               |
| Empower | 🎁     | Next steps                 | Enable navigation, verification, and action.                      |

##  Evidence and status palette

| Role            | Symbol | Meaning                                     | Usage rule                                          |
| --------------- | ------ | ------------------------------------------- | --------------------------------------------------- |
| Observed        | 🔎     | Directly inspected evidence                 | Pair with a precise source location when practical. |
| Verified        | ✔️     | Corroborated result                         | State the validation or corroboration.              |
| Inference       | 🟰     | Derived conclusion                          | State the evidence and reasoning boundary.          |
| Will not do     | ✖️     | Omitted, deprecated, invalid                |                                                     |
| Unknown         | ❓     | Missing, ambiguous, or conflicting evidence | State impact and what could resolve it.             |
| Conflict        | 💥     | Material disagreement                       | Identify the competing evidence or interpretations. |
| Risk or warning | ⚠️     | Consequential uncertainty or caveat         | Use sparingly and state the consequence.            |
| Decision        | ⚖️     | Choice or decision gate                     | State criteria, owner, or current status.           |
| Current         | 🟢     | Apparently current source or state          | State the basis for currency.                       |
| Pending         | 🟡     | Ready or proposed                           |                                                     |
| Needed          | 🔴     | Missing, Needed, Queued                     |                                                     |
| Deferred        | ⏸️     | deferred, awaiting resources                |                                                     |
| Blocked         | ⛔     | Blocked, No access                          |                                                     |
| Aging           | 🔵     | Possibly outdated source or state           | State why staleness is plausible.                   |
| Superseded      | ⚫     | Replaced or deprecated source or state      | Identify the replacement when known.                |

## Hierarchy state palette

| State       | Symbol | Meaning                                  | Usage rule                                                        |
| ----------- | ------ | ---------------------------------------- | ----------------------------------------------------------------- |
| Done        | ✔️     | Completed and verified work or outcome   | Use only when completion has been validated.                      |
| In progress | 🚧     | Work is actively underway                | Pair with the current owner, activity, or next checkpoint.       |
| Planned     | 📌     | Accepted future work                     | Use for committed work that has not started; state the next step. |
| Blocked     | ⛔     | Work cannot proceed                      | State the blocker and what would unblock it.                      |
| Deferred    | ⏸️     | Intentionally paused or postponed work   | State the reason and the condition for resumption.                |
| Not started | ⚪     | Identified work with no active commitment | Use sparingly; distinguish it from planned work.                  |

For example: `✔️ Done`, `🚧 In progress`, `⛔ Blocked`. Use these symbols in hierarchy labels, tree nodes, and status summaries when they improve state scanning; do not use them as decoration or without the state text.

## Mermaid diagrams

- Use Mermaid only when it makes a material relationship easier to understand.
- Add `%%{init: {'theme':'dark'}}%%` immediately after the ```mermaid fence.
- Prefer top-down flowcharts unless the relationship is intrinsically narrow.
- Keep diagrams to roughly six to twenty elements; split larger diagrams at natural boundaries.
- Label important relationships and avoid unexplained abbreviations.
- Follow every diagram with a prose interpretation.
- For class or entity relationships, consider separating relationship and composition views when one diagram would be too dense.
