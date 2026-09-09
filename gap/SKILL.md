---
name: gap
description: Apply COP-style skeptical review to one branch or an evidence-backed DAC branch hierarchy, then produce per-branch verdicts and a cross-branch integration roll-up. Use when reviewing a branch in isolation or when related branches, portions, or parent integration need a combined review.
---

# GAP Hierarchical Review

> **Quick help:** If invoked with `?` as the only parameter, explain the supported single-branch and DAC-hierarchy inputs. Do not begin a review.

GAP is an independent, read-only reviewer for branch relationships. It uses COP as its per-branch review engine, but adds an evidence-backed hierarchy and an integration-level verdict. It does not replace DAC coordination, create a Jira plan, switch branches, make commits, or create nested COP instances.

## Select the review scope

- `/gap` reviews the current branch as one node.
- `/gap <exact-branch>` reviews that exact local branch as one node.
- `/gap <path-to-.dac-workspace>` reviews the recorded DAC hierarchy rooted at that workspace.
- When the user supplies a DAC workstream plus a request for hierarchy, first resolve its exact `.dac/<workspace-label>/00-control.md`; ask one question if more than one matching workspace is plausible.

Do not scan sibling branches or `.dac` workspaces merely because their names look related. A supplied suffixed workspace label is an exact selector. A branch without evidenced relation remains a separate single-branch review.

## Authority and output

Read Git metadata, recorded DAC artifacts, local branch refs, code, tests, and available read-only integrations under R0. Do not switch branches or run tests merely to inspect them. Request the same explicit approval that COP requires before a build, test, generator, source edit, Git mutation, Jira action, or remote action.

For a Standard or Deep review, ask immediately before creating output: `Optional folder context suffix (for example, a short title)? Leave blank to omit it.` With W1 approval, write a collision-safe `<output-base>/gap-YY-MM-DD-<letter>-<context>/` instance containing `00-control.md`, `01-hierarchy.md`, `02-branch-reviews.md`, and `Findings.md`. A Quick review stays in chat unless the user asks to save it.

## Establish the branch hierarchy

Read the current COP contract and every file in `../cop/references/` before making COP-derived findings. Also read repository-local instructions and, for DAC mode, the selected workspace's `00-control.md`, portions, solo envelopes, results, and integration plan.
For branch code review, read [references/codebase-scope.md](references/codebase-scope.md) before treating a branch checkout as the complete implementation boundary.


Build the tree only from observed evidence:

1. Record the selected workspace label and its parent Jira workstream separately.
2. Read `target_branch` and `master_branch` from `00-control.md`.
3. Add portion branches only from recorded envelope or result metadata. Their expected base is the recorded master branch.
4. Add solo branches only from their recorded `branch` and `base_branch` metadata.
5. Recurse into another DAC workspace only when the current artifacts explicitly link to that exact workspace or the user names it.

Use local Git refs to verify that a named branch exists and to obtain its merge base or diff. Local ancestry can establish containment only; it does not prove a pull request, a remote base, or merge status. Never fall back silently to `main`. Mark a missing base, missing branch, cycle, duplicate node, inaccessible workspace, or undocumented relationship as **Unknown** and keep it visible in the output.

Show the observed tree before reviewing it. Use this shape, adapting labels and status to the evidence:

```text
Target branch (recorded: release/2026.09)
└── Parent integration (recorded: feature/PD-123456)
    ├── P-001 — branch feature/PD-123456-schema
    ├── P-002 — branch feature/PD-123456-api
    └── S-001 — branch feature/PD-654321-hotfix (base: release/2026.09)
```

## Review each branch with COP

Review the baseline before its descendants, then recurse in dependency-aware order. For every accessible branch, apply all eight COP passes: requirement alignment, assumption audit, schema and contract verification, simplicity review, failure analysis, implementation risk, reality check, and alternative analysis.

Compare the branch to its recorded base when that base is available. When no base is recorded or available, inspect the branch as a bounded snapshot and label the diff basis **Unknown** rather than inventing a relationship. Use the Codebase Knowledge Graph only for the current checked-out tree or another verified matching checkout; inspect branch contents directly before applying graph-derived claims to another ref.

Record one compact node review containing:

| Field | Required content |
| --- | --- |
| Node | DAC local ID or exact branch name |
| Base and evidence | Recorded base, local ref status, and comparison boundary |
| COP verdict | Yes, Yes with changes, No, or Unable to verify |
| Findings | Severity, confidence, and evidence links for material concerns and strengths |
| Contract effects | Upstream inputs, downstream consumers, and changed shared contracts |
| Coverage | COP passes completed, gaps, and validation evidence |

Do not inflate duplicated inherited concerns. State the first affected node, then reference it from descendants unless the descendant introduces a distinct failure mode.

## Synthesize the hierarchy

Keep branch-local and hierarchy-level conclusions separate.

1. **Branch-local findings:** concerns owned by one implementation branch.
2. **Shared-contract findings:** incompatible API, schema, configuration, authorization, migration, or behavior assumptions across two or more nodes.
3. **Integration findings:** ordering, base drift, missing propagation, merge-conflict exposure, incomplete rollback, validation gaps, or target-convergence risk.
4. **Unknowns:** missing branch/base/PR evidence, disconnected nodes, and unreviewable code.

Produce a hierarchy roll-up with the tree, a per-node verdict table, and the smallest set of cross-branch findings. Trace each hierarchy-level claim back to its affected nodes and evidence. Never label a child integrated into the target merely because it is reachable from a local parent branch; only independently verified remote evidence supports that conclusion.

The final `Findings.md` must lead with the overall verdict, then include:

1. Scope, evidence boundary, and the observed branch tree.
2. At-a-glance node verdicts and review coverage.
3. Branch-local COP reviews.
4. Shared contracts and integration risks.
5. Unknowns, conflicts, and validation limitations.
6. Prioritized actions in dependency order, distinguishing coordinator decisions from branch-owner changes.

Use the COP visual-language palette. Cite repository evidence as `path:line` and identify Git refs, commit IDs, and DAC artifact paths precisely. Include evidenced strengths as well as concerns.

## Quality gate

Before returning:

- [ ] Every included node has an explicit evidence source and comparison basis, or is marked Unknown.
- [ ] All eight COP passes are represented for every reviewed node.
- [ ] The output separates branch-local findings from shared-contract and integration findings.
- [ ] No branch relationship, PR state, remote base, or merge outcome was inferred from naming or local ancestry alone.
- [ ] Cycles, duplicates, missing refs, and inaccessible workspaces are visible rather than silently omitted.
- [ ] No review action exceeded the user's granted authority.