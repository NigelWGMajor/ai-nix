# Executor Routing

## Route at readiness

Select an executor when a portion becomes dependency-ready. Record the route and rationale in the envelope. Reconsider it when prerequisite work changes complexity or risk.

| Route | Use when | Required completion evidence |
|---|---|---|
| `speckit` | behavior or design needs an independent specification cycle | spec, plan, tasks, analysis, convergence, tests, PR |
| `skill:<name>` | an installed specialist skill matches the bounded outcome | skill-native artifacts plus normalized DAC result |
| `direct` | behavior is small, clear, and locally testable | diff, tests, review, PR or deliverable |
| `discovery` | uncertainty prevents a safe decision or partition | evidence, recommendation, exit decision, proposed follow-up |
| `human` | work is organizational, manual, privileged, or intentionally assigned | owner-confirmed deliverable and evidence |

Do not create a general executor framework. Support a small explicit routing vocabulary and use the shared handoff and result contracts.

## Handoff packet

Pass:

1. portion identity and Jira mapping
2. outcome, scope, and non-goals
3. acceptance criteria and parent traceability
4. locked decisions and delegated local decisions
5. upstream contracts and dependency evidence
6. downstream obligations
7. allowed and excluded change surface
8. test, compatibility, rollout, and rollback obligations
9. base revision and drift checks
10. current action authority and escalation rules

Exclude unrelated sibling detail and parent history. Link to evidence instead of copying it.

## Spec Kit adapter

Use the envelope as the bounded input to the child feature specification. Allocate its directory before dispatch and link the directory to the portion in both directions.

Run the child cycle independently:

```text
specify -> clarify -> plan -> checklist -> tasks -> analyze
        -> implementation approval -> implement -> converge -> PR
```

Let Spec Kit decide portion-local technical detail within delegated freedom. A contradiction with the envelope is a parent escalation, not a local clarification.

Avoid shared active-feature state during concurrency. Prefer a separate worktree for each executing portion and explicitly select its feature directory when the installed Spec Kit integration supports that capability. Keep Git creation and remote actions under DAC C3 and R4 gates.

## Skill adapter

Invoke only an available skill whose declared purpose matches the portion. Give it the envelope as the user-level objective plus the minimum linked evidence. Follow that skill's instructions, but retain DAC authority and escalation boundaries.

If the skill cannot produce the full normalized result, have the coordinator translate its output. Do not require specialist skills to know DAC internals.

## Direct adapter

Use a direct implementation prompt only when acceptance criteria, target behavior, repository surface, and tests are sufficiently clear. Require the executor to inspect local instructions, show a pre-change summary, remain within C3 scope, validate proportionately, and return a result.

## Discovery adapter

State one blocking question, a bounded investigation surface, a time or evidence limit, and the decision the result must enable. Discovery does not authorize implementation. Convert the result into parent evidence or a decision before repartitioning.

## Human adapter

Name the owner, deliverable, due or review condition, dependency effect, evidence expected, and coordinator follow-up. Do not mark human work complete based only on elapsed time or an unverified status message.

## Escalation classes

- **Local:** stays within envelope; record in child artifacts.
- **Parent:** changes intent, acceptance, priority, or shared design; pause and decide centrally.
- **Contract:** changes an upstream or downstream interface; block affected portions and revise the graph.
- **New scope:** create or explicitly approve a new portion.
- **Authority:** requires operations beyond the current grant; stop and request the exact class and scope.
