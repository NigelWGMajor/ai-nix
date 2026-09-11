---
name: pro
description: Reconstruct an oversized pull request into small, dependency-ordered, discipline-specific child PRs. Use when the current branch has an existing PR that is hard to review because previously separate work was integrated into one parent branch.
---

# Pull Requests Open

Quick help: if invoked with ? as the only parameter, explain the source-PR, feature-master, and child-PR workflow. Do not inspect a branch or create output. With no parameters, first detect whether the current branch belongs to one recorded Pro reconstruction; when it does, show its branch switch list instead of treating the current branch as a new source PR.

/pro reduces review cognitive load after integration has made a branch too broad. It treats the current branch and its PR as read-only evidence, proposes a reviewable reconstruction, then - only after explicit approval - creates child branches and PRs that merge into a newly created feature-master integration branch.

It is not a general PR review, a replacement for early delivery planning, or a way to rewrite an existing remote PR in place. Use /wiz or /gap for review; use /dac before implementation when a workstream needs delivery coordination and Jira allocation.

## Core model

Resolve the current branch's exact PR and actual target. Do not assume the target is main.

The source branch remains unchanged. Create a feature-master branch from the resolved target branch. When that target is `main`, the feature-master is the new feature/integration branch branched from `main`. Create every child branch from feature-master and merge every child PR back to feature-master; child PRs must never target `main` directly. The final feature-master PR targets the original PR target.

~~~text
<original target> -> <feature-master> -> <child portion branches>
<original target> <- final feature-master PR  <- child PRs

<original broad branch and PR> = read-only source of intent and changes
~~~

Do not use the original broad branch as a child-PR base: it already contains the proposed child changes, so child PRs would be empty or misleading. After all intended child PRs merge, feature-master must have equivalent behavior and tree contents to the source branch, except for explicitly approved corrections.

## Authority

Start with read-only inspection.

| Class | Scope | Default |
|---|---|---|
| R0 | Read local Git state, code, tests, PR/Jira metadata, and indexes | allowed |
| W1 | Write a named local /pro plan | explicit scoped approval |
| V2 | Run builds, tests, generators, or equivalence checks | explicit approval |
| C3 | Create branches, worktrees, commits, or source changes | explicit approval |
| R4 | Push branches; create, edit, comment on, close, or merge PRs; mutate Jira or other remote systems | separate explicit approval |

Content approval does not authorize C3, V2, or R4. Preserve unrelated worktree changes. Never force-push, rebase, close, or modify the source branch or its PR unless the user separately asks and grants R4 approval.
## Output location and Pro environment

Resolve `TOOLING_OUTPUT_PATH` before locating or creating durable Pro state. When set, it is the priority output boundary: an absolute value is the output base; a value beginning `./` or `.\` is relative to the resolved repository root; reject other relative forms. No inferred or explicitly requested output location may escape that base; ask the user to reconcile any conflict. When unset, use `<repository-root>/.data`. The output base already names the output directory: never append another `.data` segment, and never write Pro artifacts beside source code, a PR checkout, or a child branch.

A W1-approved Pro instance is the evidence source for a Pro environment. Store it as a collision-safe `<output-base>/pro-YY-MM-DD-<suffix>[-<context>]/` directory and retain these files:

- `00-control.md` — repository root, source branch and PR, recorded target branch, feature-master branch, current phase, branch switch table, and links to the other records;
- `01-source-evidence.md` — read-only source PR and diff evidence;
- `02-repartition-plan.md` — approved portions, dependencies, ownership, and merge order;
- `03-pr-payloads.md` — each child ID, branch, explicit base, approved PR payload, and observed remote status; and
- `04-convergence.md` — equivalence register, validation evidence, and final-parent gate.

Use explicit labels such as `Pro reconstruction`, `feature_master_branch`, `source_branch`, `target_branch`, `P-001`, `branch`, `base`, and `status`. Other skills may use only this recorded evidence to recognize the hierarchy; a similarly named branch is not Pro evidence.

## Resume and fast branch switching

With no parameters, resolve the repository root and output base, then look for Pro instances whose recorded repository root matches and whose source, feature-master, or child branch matches the current branch. If exactly one instance matches:

1. **Fetch current PR status** for all recorded child PRs and the parent PR (if created). Use `gh pr view` or an equivalent read-only integration; if it is unavailable, mark the remote state Unknown.
2. **Show status report** with clickable links:
```markdown
**Pro Reconstruction Status**: <instance-name>
**Child PRs** (targeting `<feature-master>`):
- [#XXXXX](url) P-001 <title> — ✅ MERGED
- [#XXXXX](url) P-002 <title> — ⬜ OPEN
- [#XXXXX](url) P-003 <title> — 🔶 APPROVED (not merged)
...
**Parent PR** (targeting `<original-target>`):
- ⬜ Not created yet
  OR
- [#XXXXX](url) <title> — ⬜ OPEN
**Progress**: 2 of 6 child PRs merged
```
3. **Offer parent PR creation** if any child PR has merged AND parent PR doesn't exist:
   > "Some child PRs have merged. Create parent PR from feature-master → <target>? (requires R4 approval)"
   If approved, create the parent PR with:
   - Approved parent PR description from `03-pr-payloads.md`
   - Add cross-reference comment listing all child PRs (same format as child PR comments)
4. Show the compact keyboard-selectable branch list: `A` for the recorded target, `B` for feature-master, then `C...` for child branches in dependency order. Mark the current branch.
Listing and status report are R0. Switching requires one C3 approval for the selected target. Creating parent PR requires separate R4 approval. Refuse to switch a dirty worktree without an explicitly approved preservation action; never discard work, force a checkout, or infer a stash policy. When the feature-master or a child is newly created, record it in the same Pro instance before returning, so subsequent no-parameter runs can resume and switch quickly.

If no instance matches, proceed with ordinary source-PR inspection. If several instances match, show their paths, feature-master branches, and recorded phases and ask the user to choose one; do not scan or merge them.

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
| P-001 | SQL | Additive schema contract | - | pro/...-schema | feature-master (`pro/<source>-feature-master`) | database | additive migration; schema validation |
| P-002 | Backend | Consume new contract | P-001 | pro/...-data-layer | feature-master (`pro/<source>-feature-master`) | backend | compatible before/after P-001; unit tests |

Also present the dependency diagram and exact child merge order; original target, source branch/PR, and feature-master name; mapping of each source acceptance criterion to portions; options to keep, combine same-discipline portions, split further, defer a safe residual, or stop; and an equivalence plan that names behavioral checks and every allowed divergence.

Do not create Jira issues by default. If requested, preview each Story description and acceptance criteria first, then require separately scoped R4 approval.

## Materialize only after approval

After plan approval, request authority in consolidated classes rather than serial confirmations. One W1 request covers creating and maintaining the named Pro instance and all five planning records. One C3 request covers the approved local reconstruction as a unit: create feature-master and child branches, apply the bounded changes, record resulting local branch/commit evidence, and switch to feature-master. One V2 request covers the named validation and equivalence checks. R4 approval for child PR creation should include cross-linking: creating all child PRs and adding cross-reference comments to each. Keep each remote payload under separately scoped R4 approval. Ask another question only for a material decision or new authority outside the approved scope.

1. Create feature-master directly from the recorded original target, using an explicit name such as `pro/<source>-feature-master`. When the original target is `main`, this is the new branched-from-`main` feature/integration parent. Record the branch, then switch the active checkout to it before creating children.
2. Create every portion branch from feature-master - never from a sibling or the source branch. Record every branch and its explicit feature-master base in `00-control.md` and `03-pr-payloads.md`.
3. Reapply only the portion's bounded change from the source. Use source commits as evidence, not indivisible transfer units: selective cherry-picks, patch extraction, or clean reimplementation are acceptable when a commit mixes concerns.
4. When a child needs an already merged dependency, merge the updated feature-master into the active child branch. Do not rebase a published child branch.
5. Verify each child diff against feature-master: it must not contain sibling-owned work. Run approved validation, record deviations, then create the child PR with feature-master as its explicit base. Never target the original target, including `main`, directly.
6. Give each PR its approved description, acceptance criteria, dependency note, test evidence, and named reviewer discipline.
7. After all child PRs are created, add a cross-reference comment to each PR listing all sibling PRs with clickable links. Do not include status: it will become stale over the PR's lifetime.
Use this format:
```markdown
This PR is part of a set of related PRs which share a common feature-master branch.
**Child PRs** (all targeting `<feature-master-branch>`):
- [#XXXXX](url) P-001 <title>
- [#XXXXX](url) P-002 <title>
- [#XXXXX](url) P-003 <title>
...
**Parent PR**: Offer creation after at least one child PR merges to feature-master.
```
This cross-linking requires one R4 approval covering all comment posts.

Do not call a child integrated merely because local feature-master contains its commit. Independently verify the remote PR head, base, lifecycle, and merge state.

## Convergence gate

Before creating the parent PR, at least one required child PR must be remotely verified merged into feature-master. If any readiness condition below is unmet, the parent PR may be created only in draft form:

- every required child PR is remotely verified merged into feature-master before the parent PR is proposed as ready for review;
- every source acceptance criterion has coverage and evidence;
- the feature-master tree matches the source branch, or every difference appears in the approved divergence register;
- migration, contract, rollout, rollback, authorization, and cleanup order remain safe;
- validation passed, or every unrun or failed check is plainly reported; and
- the source PR has not drifted materially since inspection. Reinspect and replan if it has.

Only after R4 approval, create the parent PR from feature-master to the recorded original target, and add a cross-reference comment listing each child PR's observed final status:
```markdown
This PR integrates all child PRs from the Pro reconstruction.
**Child PRs** (targeting `<feature-master-branch>`):
- [#XXXXX](url) P-001 <title> — ✅ MERGED
- [#XXXXX](url) P-002 <title> — ⬜ OPEN
- [#XXXXX](url) P-003 <title> — ❓ UNKNOWN
...
**Source PR**: [#XXXXX](url) (read-only source; any supersession action needs separate approval)
```
Closing, superseding, or annotating the source PR is a separate remote action requiring explicit approval.

## Output and quality gate

Keep the plan in conversation unless W1 is granted. Use the Output location and Pro environment contract above. Derive an optional context suffix from an unambiguous user-supplied title; otherwise omit it. Do not ask a separate suffix question before the consolidated W1 request.

Before returning a proposal or completion report, confirm:

- [ ] Source PR and actual target are observed, or clearly marked Unknown.
- [ ] Every portion has one coherent outcome, reviewer discipline, acceptance criteria, and validation obligation.
- [ ] Dependencies are directional and acyclic; no child is based on a sibling.
- [ ] Feature-master, every child PR base, and final PR target are explicit.
- [ ] Source intent is traced to portions and final equivalence is defined.
- [ ] The W1 Pro instance is under `TOOLING_OUTPUT_PATH` (or its documented fallback), and its switch table records every created branch and base.
- [ ] After feature-master creation, the active checkout is feature-master unless a dirty-worktree safeguard prevented the switch and that limitation is recorded.
- [ ] No local or remote mutation exceeded granted authority.
