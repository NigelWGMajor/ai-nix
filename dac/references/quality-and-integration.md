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

Before DAC plans or creates branches, record the integration target in `06-integration-plan.md`; it is the branch the final parent PR (or a direct unpartitioned PR) targets. Never assume that target is `main`, and never substitute a repository default branch for the recorded target.

When DAC creates child Stories, create a parent integration branch from the recorded target, branch every child from that parent branch, and target every child PR back to the parent branch. Merge the parent branch to the recorded target only through its final parent PR. Do not stack a child branch on a sibling branch; use child-PR merge order and merge the updated parent into active child branches when needed. For a single unpartitioned work item, branch from and target the recorded target directly.
## PR topology verification
The planned DAC hierarchy and the observed Git/PR hierarchy are separate evidence. Re-resolve all volatile facts immediately before a status report, portion acceptance, or parent convergence. Record the observation time and source when these facts matter.
For each relevant PR, establish all of the following:
- **Repository identity:** the local Git root and its configured remote URL, plus the remote repository/project returned by the PR provider. Do not assume that a nested DAC workspace, a checkout directory, or a branch prefix identifies the parent repository.
- **Actual PR topology:** PR number/URL, head repository and branch, base repository and branch, and the expected DAC role (`child` or `master`). The base branch is authoritative for the integration target; it may differ from the planned topology and must be reported as a discrepancy.
- **Remote PR lifecycle:** provider-reported state, `mergedAt`/equivalent merge timestamp, and merge commit when available. `closed` is not `merged`; a missing PR, inaccessible provider, or ambiguous response is `unknown`, not merged.
- **Local ancestry:** only after resolving the exact refs, report `git merge-base --is-ancestor <child-commit-or-merge-commit> <base-ref>` or equivalent as a local containment observation. Name both refs. This evidence cannot establish that a remote PR exists, its base, or its merge state, and it cannot substitute for remote verification.
Status language must preserve the hierarchy:

| Observed evidence | Permitted statement | Not permitted |
|---|---|---|
| Child PR is remotely merged into the parent branch; parent has no verified merge into its recorded target | `P-001 is integrated into <parent-branch>; the parent PR to <target-branch> is not verified as merged.` | `P-001 is merged into <target-branch>.` |
| Child commit is contained in a local parent branch but not in the recorded target; remote PR state is unavailable | `Local ancestry shows <parent-branch> contains P-001; local <target-branch> does not. Remote child-PR state is unknown.` | `P-001 is merged`, `P-001 is direct-to-<target-branch>`, or `P-001 has no parent branch.` |
| PR is remotely merged into its declared base | `<PR> is merged into <base-repository>:<base-branch>.` | Claiming it reached a different ancestor branch without separately verifying that branch's PR/merge. |
| PR is open, closed-unmerged, missing, inaccessible, or has conflicting base evidence | State the exact observed state and block the corresponding integration conclusion. | Inferring completion from Jira status, commit containment, or a branch name. |
If planned topology conflicts with observed topology, record the discrepancy in the result/integration evidence and use the observed facts in status language. Pause parent convergence when the intended child or parent merge cannot be verified; ask for access or direction instead of simplifying the hierarchy. A parent workstream reaches its recorded target only when its final parent PR (or the explicitly recorded direct PR for an unpartitioned work item) is remotely verified merged into that resolved target repository and branch.
When Jira allocation is parent-only, `06-integration-plan.md` is still required and must be approved as content before portion envelopes are created. Mark it `trivial` and record the direct branch/PR path, parent-ticket traceability, required validation, rollout, and rollback; do not bypass the integration record because no child Stories exist.

Before opening a PR, verify the intended base, dependency state, approved C3 surface, current diff, tests, and result artifact. Before accepting a merge result, complete PR topology verification as well as verifying required reviews, CI, contract compatibility, deployment order, and rollback.

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
