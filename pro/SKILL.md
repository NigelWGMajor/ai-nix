---
name: pro
description: Reconstruct an oversized pull request into small, dependency-ordered, discipline-specific child PRs. Use when the current branch has an existing PR that is hard to review because previously separate work was integrated into one parent branch.
---

# Pull Requests Open

Quick help: if invoked with ? as the only parameter, explain the source-PR, reconstructed-parent, and child-PR workflow. Do not inspect a branch or create output.

/pro reduces review cognitive load after integration has made a branch too broad. It treats the current branch and its PR as read-only evidence, proposes a reviewable reconstruction, then - only after explicit approval - creates child branches and PRs that merge into a newly reconstructed parent.

It is not a general PR review, a replacement for early delivery planning, or a way to rewrite an existing remote PR in place. Use /wiz or /gap for review; use /dac before implementation when a workstream needs delivery coordination and Jira allocation.

## Core model

Resolve the current branch's exact PR and actual target. Do not assume the target is main.

The source branch remains unchanged. Create a reconstructed parent from the resolved target branch. Create every child branch from that reconstructed parent and merge every child PR back to it. The final reconstructed-parent PR targets the original PR target.

~~~text
<original target> -> <reconstructed parent> -> <child portion branches>
<original target> <- final parent PR        <- child PRs

<original broad branch and PR> = read-only source of intent and changes
~~~

Do not use the original broad branch as a child-PR base: it already contains the proposed child changes, so child PRs would be empty or misleading. After all intended child PRs merge, the reconstructed parent must have equivalent behavior and tree contents to the source branch, except for explicitly approved corrections.

## Authority

Start with read-only inspection.

| Class | Scope | Default |
|---|---|---|
| R0 | Read local Git state, code, tests, PR/Jira metadata, and indexes | allowed |
| W1 | Write a named local /pro plan | explicit scoped approval |
| V2 | Run builds, tests, generators, or equivalence checks | explicit approval |
| C3 | Create branches, worktrees, commits, or source changes | explicit approval |
| R4 | Push branches; create, edit, close, or merge PRs; mutate Jira or other remote systems | separate explicit approval |

Content approval does not authorize C3, V2, or R4. Preserve unrelated worktree changes. Never force-push, rebase, close, or modify the source branch or its PR unless the user separately asks and grants R4 approval.

## Inspect the source

When invoked on a branch:

1. Confirm repository root, current branch, HEAD, worktree status, remotes, and merge base.
2. Resolve the PR whose head is the current branch. Establish repository identity, PR URL/number, actual head and base, provider state, linked ticket(s), description, acceptance criteria, checks, reviewers, and merge strategy. If no matching or more than one plausible PR exists, stop and ask for the exact PR or branch; do not guess.
3. Compare the source branch to the resolved target. Inventory commits, changed files, tests, generated artifacts, migrations, configuration, public contracts, deployment concerns, and current behavior.
4. Use repository instructions, tests, and the Codebase Knowledge Graph to identify existing extension points and consumers. Treat graph evidence as applying only to a verified matching checkout.
5. Record unavailable or conflicting local/remote evidence as Unknown. Local ancestry proves containment only; it never proves a remote PR exists, its base, or that it merged.
When the reconstruction may involve a client, service, or prototype boundary, read [references/codebase-scope.md](references/codebase-scope.md) before partitioning the change.


The source PR description and linked ticket express intent, but are not proof that the implemented diff meets them. Resolve material contradictions before proposing a split.

## Propose a reconstruction

Partition by expertise boundary first: SQL/schema/data migration, data layer/backend/API, frontend/UI, infrastructure/configuration, and independently reviewable tests or documentation. Then split within a discipline by coherent outcome - not merely by file extension.

Create a foundation portion only for a shared additive contract, migration, compatibility adapter, or reusable capability. A data-layer or API portion may depend on an earlier schema/contract portion. Do not propose portions that create cycles, conceal shared ownership, duplicate a contract, or require unsafe file overlap.

For every proposed portion, include:

- concise title, PR description, outcome, in-scope work, and non-goals;
- acceptance criteria as a Markdown checklist, including validation;
- discipline and suggested reviewer audience;
- source commits/files/hunks used as evidence;
- dependencies, downstream consumers, merge order, and compatibility state;
- expected change surface, unavoidable overlap, and risk;
- branch name and PR base; and
- a statement of why the portion is independently reviewable.

Present this table before any mutation:

| Portion | Discipline | Outcome | Depends on | Branch | PR base | Review audience | Compatibility / validation |
|---|---|---|---|---|---|---|---|
| P-001 | SQL | Additive schema contract | - | pro/...-schema | reconstructed parent | database | additive migration; schema validation |
| P-002 | Backend | Consume new contract | P-001 | pro/...-data-layer | reconstructed parent | backend | compatible before/after P-001; unit tests |

Also present the dependency diagram and exact child merge order; original target, source branch/PR, and reconstructed-parent name; mapping of each source acceptance criterion to portions; options to keep, combine same-discipline portions, split further, defer a safe residual, or stop; and an equivalence plan that names behavioral checks and every allowed divergence.

Do not create Jira issues by default. If requested, preview each Story description and acceptance criteria first, then require separately scoped R4 approval.

## Materialize only after approval

After plan approval, ask for exact authority before acting: C3 for local reconstruction, V2 for validation, and R4 for every remote push and PR payload.

1. Create the reconstructed parent from the recorded original target, using an explicit name such as pro/<source>-reconstructed.
2. Create every portion branch from that parent - never from a sibling or the source branch.
3. Reapply only the portion's bounded change from the source. Use source commits as evidence, not indivisible transfer units: selective cherry-picks, patch extraction, or clean reimplementation are acceptable when a commit mixes concerns.
4. When a child needs an already merged dependency, merge the updated reconstructed parent into the active child branch. Do not rebase a published child branch.
5. Verify each child diff against its current parent: it must not contain sibling-owned work. Run approved validation, record deviations, then create the child PR to the reconstructed parent.
6. Give each PR its approved description, acceptance criteria, dependency note, test evidence, and named reviewer discipline.

Do not call a child integrated merely because a local parent contains its commit. Independently verify the remote PR head, base, lifecycle, and merge state.

## Convergence gate

Before proposing the final parent PR:

- all required child PRs are remotely verified merged into the reconstructed parent;
- every source acceptance criterion has coverage and evidence;
- the reconstructed parent tree matches the source branch, or every difference appears in the approved divergence register;
- migration, contract, rollout, rollback, authorization, and cleanup order remain safe;
- validation passed, or every unrun or failed check is plainly reported; and
- the source PR has not drifted materially since inspection. Reinspect and replan if it has.

Only after this gate and separate R4 approval, create one final PR from the reconstructed parent to the recorded original target. Closing, superseding, or annotating the source PR is a separate remote action requiring explicit approval.

## Output and quality gate

Keep the plan in conversation unless W1 is granted. Resolve TOOLING_OUTPUT_PATH first: an absolute value is the output base, ./ or .\\ is relative to the repository root, and when unset use the repository's .data folder. With W1 approval, create a collision-safe pro-YY-MM-DD-letter-context folder under that output base containing 00-control.md, 01-source-evidence.md, 02-repartition-plan.md, 03-pr-payloads.md, and 04-convergence.md.

Before returning a proposal or completion report, confirm:

- [ ] Source PR and actual target are observed, or clearly marked Unknown.
- [ ] Every portion has one coherent outcome, reviewer discipline, acceptance criteria, and validation obligation.
- [ ] Dependencies are directional and acyclic; no child is based on a sibling.
- [ ] The reconstructed parent, every child PR base, and final PR target are explicit.
- [ ] Source intent is traced to portions and final equivalence is defined.
- [ ] No local or remote mutation exceeded granted authority.
