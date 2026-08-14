<!-- Template note: symbols in this template are examples drawn from references/visual-language.md.
     Always read visual-language.md before generating output and use its current symbol assignments.
     If visual-language.md has been updated since this template was last edited, its symbols take precedence. -->

# KIT status review: [feature name]

> **Purpose/question:** [What project-recovery decision or activity this review supports]
>
> **Audience/use:** [Who needs to resume, assess, or hand off the work]
>
> **Scope:** [Selected feature and material integration surfaces]
>
> **Evidence boundary:** [Local artifacts, code, Git state, external read-only context, and exclusions]
>
> **Status/freshness:** [Reviewed timestamp, exact HEAD, and remote-refresh status]
>
> **Material limitations:** [Unresolved base, inaccessible context, omitted validation, or other global constraints]
>
> **Mode:** [Review, Snapshot, or Resume]
>
> **Previous KIT:** [Instance path or not applicable]

## 💭 Orientation

[Explain what the project is, where it stands, the dominant uncertainty, and the safest next action.]

### At a glance

| Dimension | Current status | Evidence and confidence |
| --- | --- | --- |
| Repository / branch / HEAD | [Identity] | [Freshly resolved local Git evidence] |
| Feature / base / merge base | [Resolved or unresolved] | [Resolution evidence and limitation] |
| Spec Kit lifecycle | [Phase] | [Artifacts and evidence] |
| Worktree | [Clean, staged, unstaged, untracked, or mixed] | [Git snapshot] |
| Implementation | [Summary] | [Evidence class and confidence] |
| Validation | [Passed, failed, partial, blocked, or not run] | [Exact scope] |
| Integration | [Local, committed, upstream, PR, merge-ready, or unknown] | [Freshness limit] |
| Material uncertainty | [Most consequential unknown] | [Impact and resolution path] |
| Best next step | [Action] | [Prerequisite and stopping condition] |

## Content map

[Include this section when the report has more than three substantial reading paths; otherwise remove it.]

| Area | Why it matters | Read this when |
| --- | --- | --- |
| [Area] | [Recovery or decision value] | [Reader need] |

## 🧭 Foundations

### Problem and intended outcome

[Re-educate the reader on the problem, users, desired outcomes, and why the work matters.]

### Scope and exclusions

- **In scope:** [Bounded feature scope]
- **Out of scope:** [Explicit exclusions]
- **Material assumptions:** [Assumptions that affect interpretation]

### Architecture and key decisions

[Summarize only the technical model and decisions needed to resume responsibly. Link to plan, research, model, and contracts.]

### Vocabulary

| Term | Meaning in this project | Source |
| --- | --- | --- |
| [Term] | [Meaning] | [Precise artifact link] |

## 🔗 Relationships and evidence

### Lifecycle and artifact status

| Layer | Artifact or evidence | Status | Important limitation |
| --- | --- | --- | --- |
| Constitution | | | |
| Specification | | | |
| Clarification/checklists | | | |
| Plan/research/design/contracts | | | |
| Tasks | | | |
| Implementation | | | |
| Validation | | | |
| Integration | | | |

### Progress by story or phase

#### [Story or phase]

| Requirement/task | Intended outcome | Implementation evidence | Validation | Status and confidence | Remaining work |
| --- | --- | --- | --- | --- | --- |
| [ID] | [Outcome] | [Paths, symbols, commits, or diff] | [Exact evidence] | [KIT status, evidence class, confidence] | [Bounded remainder] |

### Traceability and sanity check

[Summarize requirement coverage, design consistency, task accuracy, implementation drift, and acceptance coverage. Link to `03-analysis.md` for detailed mappings.]

#### Coverage gaps

| Requirement/design element | Missing or contradictory layer | Impact | Resolution path |
| --- | --- | --- | --- |
| | | | |

### Resume delta

[Remove this subsection outside Resume mode.]

| Dimension | Previous snapshot | Current evidence | Meaning |
| --- | --- | --- | --- |
| Repository/branch/HEAD | | | |
| Worktree | | | |
| Artifacts and scope | | | |
| Implementation | | | |
| Validation | | | |
| Findings/blockers | | | |
| Next action | | | |

## 🟰 Findings and decisions

### [KIT-001] [Finding title]

- **Severity:** [Critical, High, Medium, Low, or Note]
- **Confidence:** [High, Medium, or Low]
- **Evidence class:** [Observed, Claimed, Inferred, or Unknown]
- **Evidence:** [Precise links, Git facts, and command output]
- **Impact:** [Why this matters]
- **Next step:** [Concrete resolution or verification]

### Strengths

- [Evidence-backed strength that reduces recovery or delivery risk]

### Open decisions and external blockers

| Decision or blocker | Owner/input needed | Impact if unresolved | Safe interim state |
| --- | --- | --- | --- |
| | | | |

## 📋 Validation

| Result | Command or check | Purpose | Reviewed state | Important output or limitation |
| --- | --- | --- | --- | --- |
| [Passed, failed, partial, blocked, or not run] | [Exact command/procedure] | [Requirement or risk] | [HEAD and worktree context] | [Concise evidence] |

## 🎬 Next steps

1. **[Action]**
   - Outcome: [What this establishes or completes]
   - Why next: [Dependency or risk]
   - Prerequisite: [Decision, access, clean state, or none]
   - Targets: [Requirements, task IDs, files, or components]
   - Validation: [Focused check]
   - Stop when: [Checkpoint]

## 📚 Evidence index

| ID | Source | Role | Snapshot/freshness limitation |
| --- | --- | --- | --- |
| E001 | [Artifact, code area, Git command, test output, PR, or issue] | [What it establishes] | [Time, commit, access, or confidence limit] |

