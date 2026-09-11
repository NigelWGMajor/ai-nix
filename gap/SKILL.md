---
name: gap
description: Apply COP-style skeptical review to one branch or an evidence-backed DAC or Pro branch hierarchy, then produce per-branch verdicts and a cross-branch integration roll-up. Use when reviewing a branch in isolation or when related branches, portions, or parent integration need a combined review.
---

# GAP Hierarchical Review

> **Quick help:** If invoked with `?` as the only parameter, explain the supported single-branch, DAC-hierarchy, and Pro-hierarchy inputs. Do not begin a review.

GAP is an independent, read-only reviewer for branch relationships. It uses COP as its per-branch review engine, but adds an evidence-backed hierarchy and an integration-level verdict. It does not replace DAC coordination, create a Jira plan, switch branches, make commits, or create nested COP instances.

## Select the review scope

- `/gap` reviews the current branch as one node.
- `/gap <exact-branch>` reviews that exact local branch as one node.
- `/gap <path-to-.dac-workspace>` reviews the recorded DAC hierarchy rooted at that workspace.
- `/gap <path-to-pro-instance>` reviews the recorded Pro hierarchy rooted at its `00-control.md`.
- When the user supplies a DAC workstream or Pro branch plus a request for hierarchy, first resolve its exact recorded workspace or Pro instance; ask one question if more than one matching record is plausible.

Do not scan sibling branches, `.dac` workspaces, or Pro instances merely because their names look related. A supplied suffixed workspace label or Pro instance is an exact selector. A branch without recorded evidence remains a separate single-branch review.

## Authority and output

Read Git metadata, recorded DAC or Pro artifacts, local branch refs, code, tests, and available read-only integrations under R0. Do not switch branches or run tests merely to inspect them. Request the same explicit approval that COP requires before a build, test, generator, source edit, Git mutation, Jira action, or remote action.

Resolve `TOOLING_OUTPUT_PATH` before creating output: when set, it is the priority output boundary; use an absolute value directly, resolve `./` or `.\` from the repository root, and reject other relative forms. No inferred or explicitly requested output location may escape that base; ask the user to reconcile any conflict. When unset, use `<repository-root>/.data`. With W1 approval, write a collision-safe `<output-base>/gap-YY-MM-DD-<letter>-<context>/` instance containing `00-control.md`, `01-hierarchy.md`, `02-branch-reviews.md`, and `Findings.md`. A Quick review stays in chat unless the user asks to save it.

## Establish the branch hierarchy

Read the current COP contract and every file in `../cop/references/` before making COP-derived findings. Also read repository-local instructions and, for DAC mode, the selected workspace's `00-control.md`, portions, solo envelopes, results, and integration plan; for Pro mode, read `00-control.md`, `01-source-evidence.md`, `02-repartition-plan.md`, `03-pr-payloads.md`, and `04-convergence.md`.
For branch code review, read [references/codebase-scope.md](references/codebase-scope.md) before treating a branch checkout as the complete implementation boundary.


Build the tree only from observed evidence. In DAC mode:

1. Record the selected workspace label and its parent Jira workstream separately.
2. Read `target_branch` and `master_branch` from `00-control.md`.
3. Add portion branches only from recorded envelope or result metadata. Their expected base is the recorded master branch.
4. Add solo branches only from their recorded `branch` and `base_branch` metadata.
5. Recurse into another DAC workspace only when the current artifacts explicitly link to that exact workspace or the user names it.
In Pro mode, read `target_branch`, `feature_master_branch`, and child IDs, branches, bases, dependencies, and statuses from the selected Pro records. The original broad source branch is read-only evidence, not a child node. Build `target -> feature-master -> children`; each child's expected base is feature-master. Recurse nowhere unless the Pro records explicitly name another hierarchy.

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
| Node | DAC/Pro local ID or exact branch name |
| Base and evidence | Recorded base, local ref status, and comparison boundary |
| COP verdict | Yes, Yes with changes, No, or Unable to verify |
| Findings | Severity, confidence, and evidence links for material concerns and strengths |
| Contract effects | Upstream inputs, downstream consumers, and changed shared contracts |
| Coverage | COP passes completed, gaps, and validation evidence |

Do not inflate duplicated inherited concerns. State the first affected node, then reference it from descendants unless the descendant introduces a distinct failure mode.

## Evidence gathering discipline
### Complete file reading
Before making any finding about a file:
- Read the **entire file**, not just the first 50-100 lines
- For stored procedures and large files, use multiple Read calls with offset if needed
- Never claim something is "missing" from a file without reading to the end
- Example: Don't claim "missing commit transaction" without reading the full SP body and cleanup section
### Schema and dependency verification
When a branch references database objects, API contracts, types, or other dependencies not present in its diff:
**Before claiming they are missing:**
1. **Check the recorded baseline branch** (do not assume `main`, and do not check out another branch during a read-only review):
   ```bash
   git ls-tree -r --name-only <base-branch> | rg "<ObjectName>\\.sql$"
   git grep -n "class <TypeName>" <base-branch> --
   ```
2. **Check sibling portions** in the same hierarchy (P-001 may define tables used by P-002)
3. **Check parent directories** (root vs. trunk working directory confusion)
4. **Verify import paths** are correct for the project structure
**Never claim** 🔴 **Missing** or 🔴 **Critical** without explicit verification attempt.
**When verification is impossible** (no baseline access, build-time dependency):
- Mark as ❓ **Not verified** or ⏳ **Blocked pending <prerequisite>**
- State the limitation explicitly: "Cannot verify table existence — requires checkout of main branch"
- Include this in evidence gaps, not as a critical finding
### Example verification pattern
```markdown
**Finding**: P-002 references `Bulk_SkillLevelDetailsStaging_Preprocess_Json` type from P-001
**Verification steps**:
1. Check the recorded remote state for P-001; if it cannot be read, record it as Unknown.
2. If P-001 is not merged, inspect its recorded branch without switching: `git ls-tree -r --name-only pro/<branch>-sql -- TolerableSql/`
3. If still unclear: ⏳ **Build dependency** — P-002 requires P-001 deployed for code generation
**Verdict**: ⏳ **Blocked** (documented constraint) NOT 🔴 **Missing** (critical defect)
```
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

**Evidence integrity:**
- [ ] Every included node has an explicit evidence source and comparison basis, or is marked Unknown.
- [ ] All files with findings were read **completely** (not just first N lines).
- [ ] Schema/dependency "missing" claims were verified against baseline branch or marked ❓ **Not verified**.
- [ ] Build-time dependencies are marked ⏳ **Blocked** not 🔴 **Missing** when they require prior deployment.
**Review completeness:**
- [ ] All eight COP passes are represented for every reviewed node.
- [ ] The output separates branch-local findings from shared-contract and integration findings.
- [ ] No branch relationship, PR state, remote base, or merge outcome was inferred from naming or local ancestry alone.
- [ ] Cycles, duplicates, missing refs, and inaccessible workspaces are visible rather than silently omitted.
**Verification discipline:**
- [ ] For every 🔴 **Critical** or 🔴 **High** finding, evidence shows what verification was attempted.
- [ ] Database object references checked against the recorded baseline without switching branches: `git ls-tree -r --name-only <base-branch> | rg "<Table>\\.sql$"`.
- [ ] Type/class references checked against: (1) baseline, (2) sibling branches, (3) recorded as build dependency.
- [ ] "Missing" findings include the file path searched and search result, not just absence claim.
**Authority:**
- [ ] No review action exceeded the user's granted authority.
**Self-correction:**
- [ ] If a finding seems obvious but verification was skipped, that finding is downgraded or marked ❓ **Unverified**.
- [ ] Limitations are visible in evidence gaps, not hidden by confident-sounding incorrect findings.