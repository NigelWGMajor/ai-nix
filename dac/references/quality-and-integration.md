# Partition, Result, and Integration Quality

## Partition review

Approve a partition only when:

- every parent success criterion is covered
- each portion has one coherent outcome and testable boundary
- dependencies are directional, necessary, and acyclic
- shared contracts are assigned to a clear owner
- cross-cutting security, privacy, observability, migration, rollout, and cleanup work is assigned
- proposed parallel work has low file and state overlap
- intermediate repository and deployment states remain safe
- deferred work has a safe boundary, owner, and revisit trigger

Prefer one portion, one executor package, and one PR. When the chosen Jira allocation strategy includes child tickets, prefer one Jira child per portion. Split further when a portion cannot fit comfortably in one focused reasoning and implementation cycle.

## Result review

Compare the result with the approved envelope:

- behavior and non-goals
- requirement and decision traceability
- actual change surface
- error and compatibility behavior
- security and privacy boundaries
- tests and deterministic test data
- migration, deployment, monitoring, and rollback
- deviations, assumptions, and unreported sibling effects
- repository status and unrelated changes

Treat missing evidence as unknown, not passed. A successful executor run is not proof of acceptance.

## PR integration

Prefer backward-compatible foundations before consumers. Wait for a predecessor to merge when practical. Use a shallow explicit PR stack only when waiting would materially harm delivery and intermediate checks remain meaningful.

Before opening a PR, verify the intended base, dependency state, approved C3 surface, current diff, tests, and result artifact. Before merging, verify required reviews, CI, contract compatibility, deployment order, and rollback.

After integration, record the merge reference and read back Jira or PR state when updated. Recalculate readiness; do not start downstream work from an unverified status assumption.

## Parent convergence

Complete the workstream only when:

1. every required mission criterion maps to integrated evidence
2. every approved decision is honored or superseded
3. every required portion is integrated or explicitly deferred
4. cross-portion and end-to-end behavior is tested or clearly marked not run
5. Jira, portion, commit, and PR references reconcile
6. deployment, monitoring, rollback, and ownership are actionable
7. residual work is represented as new portions or Jira follow-ups

If convergence finds a gap, add a proposed residual portion. Do not weaken the mission or edit completed evidence to manufacture completion.
