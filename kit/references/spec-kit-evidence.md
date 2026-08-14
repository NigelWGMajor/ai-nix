# Spec Kit evidence model

Use this reference to discover and audit a Spec Kit feature. Treat the installed repository as authoritative for its own version and customizations; upstream conventions are discovery hints, not proof that every artifact is required.

## Contents

- [Artifact map](#artifact-map)
- [Discovery order](#discovery-order)
- [Evidence chain](#evidence-chain)
- [Cross-artifact sanity checks](#cross-artifact-sanity-checks)
- [Implementation and completion evidence](#implementation-and-completion-evidence)
- [Validation and integration](#validation-and-integration)
- [Version and workflow cautions](#version-and-workflow-cautions)

## Artifact map

| Artifact | Typical location | Audit role | Important caution |
| --- | --- | --- | --- |
| Constitution | `.specify/memory/constitution.md` | Project principles and gates | Check project-specific amendments and versioning. |
| Feature specification | `specs/<feature>/spec.md` | Problem, scope, stories, requirements, and acceptance scenarios | Focus on what and why; do not treat plan details as original requirements. |
| Clarifications | Usually incorporated into `spec.md` | Resolved ambiguity | Search for unresolved clarification markers or dated clarification sections. |
| Requirements checklists | `specs/<feature>/checklists/*.md` | Quality of the written requirements | These test completeness and clarity of requirements, not whether code works. |
| Implementation plan | `specs/<feature>/plan.md` | Technical context, architecture, constraints, structure, and constitution gates | Compare its assumptions with the implemented project and current dependencies. |
| Research | `specs/<feature>/research.md` | Decisions, rationale, and alternatives | Check whether selected versions and constraints remain applicable. |
| Data model | `specs/<feature>/data-model.md` | Entities, relationships, validation, and state transitions | Confirm whether it is applicable before treating absence as a gap. |
| Contracts | `specs/<feature>/contracts/` | External or user-facing interfaces | Purely internal features may legitimately have no contract directory. |
| Quickstart | `specs/<feature>/quickstart.md` | Runnable end-to-end validation scenarios | A documented command is not evidence that it was run successfully. |
| Tasks | `specs/<feature>/tasks.md` | Dependency-ordered implementation roadmap | Checkboxes are source claims, not independent proof of completion. |
| Feature roadmap | `specs/<epic>/roadmap.md` | Spec-of-specs decomposition and dependencies | Keep stable roadmap IDs and sub-feature relationships visible. |
| Repository roadmap | `ROADMAP.md` | Cross-cutting decomposition | Confirm that the selected feature is the intended slice. |
| Agent context | Repository-specific guidance file | Active technologies and plan references | Read applicable agent instructions before operating. |
| Extensions and presets | `.specify/` configuration | Customized commands, templates, hooks, and artifact expectations | Inspect before assuming upstream defaults. |

Recognize additional project-specific artifacts. Record their role rather than forcing them into an upstream category.

## Discovery order

1. Resolve repository, current branch, HEAD, worktree status, and applicable repository instructions.
2. Inspect `.specify` configuration, memory, templates, extensions, presets, and available integration metadata.
3. Enumerate `specs/` feature directories without selecting one by loose similarity.
4. Prefer an explicitly supplied feature directory.
5. Otherwise accept an exact match between the current branch leaf and a feature-directory name.
6. If more than one feature remains plausible, present candidates and ask.
7. Inventory the selected directory recursively, then classify known and custom artifacts.

If available, `specify version` and `specify integration list` are read-only orientation commands. Do not install, upgrade, or reinitialize Spec Kit during a KIT review.

## Evidence chain

Audit each material user story or requirement across these layers:

| Layer | Primary question | Typical evidence |
| --- | --- | --- |
| Intent | What outcome and scope were approved? | Constitution, spec, clarification history, roadmap |
| Design | How was the outcome intended to be built? | Plan, research, data model, contracts, quickstart |
| Scheduling | What work was identified and ordered? | Tasks, dependencies, phase checkpoints, issue links |
| Implementation | What behavior or structure actually exists? | Base diff, commits, working tree, code, configuration, migrations |
| Validation | What proves the outcome works? | Tests, build output, quickstart execution, acceptance evidence |
| Integration | What state is shareable or reviewable? | Commits, upstream, PR state, merge base, local-only or dirty changes |
| Recovery | What can safely happen next? | Open decisions, blockers, prerequisites, next task and validation gate |

Keep the direction of derivation visible. A task may trace to a requirement; it does not redefine that requirement unless the source artifacts were deliberately updated.

## Cross-artifact sanity checks

### Constitution and specification

- Map mandatory constitution principles to spec constraints and plan gates.
- Identify constitutional gates marked passed without supporting design or validation evidence.
- Check that scope exclusions do not conflict with required user outcomes.
- Find unresolved placeholders, ambiguous terms, or non-measurable acceptance language.

### Specification and design

- Map every material requirement and acceptance scenario to plan coverage.
- Identify design decisions that add scope, weaken requirements, or contradict exclusions.
- Compare research decisions with plan technologies and current project versions.
- Check data-model states and validation rules against requirements.
- Compare contracts with named actors, failure modes, and compatibility constraints.
- Ensure quickstart scenarios cover the feature's meaningful end-to-end outcomes.

### Design and tasks

- Map each planned component, contract, migration, test layer, and rollout concern to tasks.
- Map each task back to a requirement, story, design element, or justified enabling activity.
- Check dependency order, phase boundaries, `[P]` claims, file targets, and independent-story checkpoints.
- Identify tasks that became obsolete after a design change.
- Identify missing work for testing, failure handling, security, accessibility, observability, migration, documentation, or rollout when relevant.

### Tasks and implementation

- Compare every checked task with concrete implementation evidence.
- Search for implementation that has no corresponding task or requirement.
- Check whether named file paths still match the actual project.
- Distinguish committed base-to-HEAD changes from staged, unstaged, and untracked work.
- Identify partial implementations hidden behind a broad checked task.
- Check TODOs or temporary workarounds only when they fall within the feature scope.

### Implementation and validation

- Map acceptance scenarios and important failure paths to appropriate tests or executed quickstart evidence.
- Distinguish test existence from test execution and execution from passing results.
- Confirm that the validation evidence applies to the exact reviewed HEAD and relevant worktree state.
- Check skipped, quarantined, filtered, or environment-dependent tests.
- Identify generated output or build artifacts introduced during review.

## Implementation and completion evidence

Use this evidence hierarchy without applying it mechanically:

1. Executed acceptance evidence against the exact implementation state.
2. Focused automated tests plus direct implementation inspection.
3. Direct implementation inspection with coherent integration evidence.
4. Commit messages, pull-request descriptions, or task checkboxes.
5. Assumption based on filenames, timestamps, or branch naming.

Higher evidence can still be incomplete or misleading. A passing unit test may not prove an end-to-end requirement; direct code inspection may reveal an unreachable path; a checked task may be entirely stale.

Classify evidence explicitly:

- **Observed**: directly inspected in artifacts, Git state, code, or command output.
- **Claimed**: asserted by a task, commit message, PR, or narrative document.
- **Inferred**: derived from observed facts with stated reasoning.
- **Unknown**: unavailable, ambiguous, or not responsibly derivable.

Use timestamps and hashes to detect possible drift, not to infer completion or causal order on their own.

## Validation and integration

Record validation as a ledger:

- Command or manual check.
- Purpose and mapped requirement or risk.
- Exact HEAD and whether uncommitted changes were included.
- Environment and prerequisites.
- Timestamp and result.
- Important output, omissions, or confidence limits.

Before running validation, capture worktree status. Capture it again afterward and classify new artifacts.

For integration state, distinguish:

- Local uncommitted work.
- Local commits not known to be on the upstream.
- Local tracking information whose remote freshness is unknown.
- Read-only PR evidence retrieved during the review.
- Merge or deployment readiness, which requires more than implementation completion.

Do not fetch merely to make the report look current. Request approval if fresh remote evidence is necessary.

## Version and workflow cautions

Current Spec Kit commonly follows `constitution -> specify -> clarify/checklist -> plan -> tasks -> analyze -> implement -> converge`, but repositories can use older versions, skill-mode integrations, presets, extensions, or custom templates.

- Treat `speckit.analyze` as a read-only cross-artifact consistency aid only after confirming the installed behavior.
- Treat `speckit.checklist` as mutating because it creates or appends checklist artifacts.
- Treat `speckit.converge` as mutating because current behavior can append remaining work to `tasks.md`.
- Treat `speckit.implement`, task generation, clarification, planning, and specification commands as mutating workflows.
- Do not use any of them during a read-only review without explicit authorization.

When installed behavior differs from this reference, record the version and follow the local implementation and repository guidance.
