<!-- Template note: symbols in this template are examples drawn from references/visual-language.md.
     Always read visual-language.md before generating output and use its current symbol assignments.
     If visual-language.md has been updated since this template was last edited, its symbols take precedence. -->

# Triage report: [symptom summary]

> **Purpose/question:** [What failure this triage investigates]
>
> **Audience/use:** [Who needs to act on this diagnosis]
>
> **Scope:** [Affected component, environment, and investigation boundary]
>
> **Evidence boundary:** [What was inspected, what was inaccessible]
>
> **Status/freshness:** [Triage timestamp, exact HEAD, worktree state]
>
> **Material limitations:** [Constraints that affect the diagnosis]
>
> **Depth:** [Quick, Standard, or Deep]
>
> **Diagnosis:** [One concise statement of the root cause and confidence]

## 💭 Capture - symptom and orientation

[Describe the observed failure precisely. Lead with the diagnosis, then provide the symptom context.]

### At a glance

| Dimension         | Status                        | Evidence                      |
| ----------------- | ----------------------------- | ----------------------------- |
| Symptom           | [What was observed]           | [Source]                      |
| Root cause        | [Confirmed or most supported] | [Confidence level]            |
| Impact            | [Who/what is affected]        | [Scope]                       |
| Proposed fix      | [Minimal change]              | [Risk level]                  |
| Validation        | [How to confirm the fix]      | [Specific test or check]      |

### 🧭 Context and recent changes

- **When observed:** [Timing, frequency, conditions]
- **Recent changes:** [Commits, deployments, configuration changes]
- **Already attempted:** [What has been tried]
- **Reproduction:** [Steps to reproduce or "not reproduced"]

## 🔗 Investigate - evidence and relationships

### Hypothesis register

| ID   | Hypothesis                    | Status      | Key evidence              |
| ---- | ----------------------------- | ----------- | ------------------------- |
| H-01 | [Specific testable claim]     | [Active/Confirmed/Eliminated] | [E-XX references]  |
| H-02 | [Alternative cause]           | [Status]    | [E-XX references]         |

### 🔎 Evidence log

| ID   | Observation                              | Source              | Supports    | Contradicts |
| ---- | ---------------------------------------- | ------------------- | ----------- | ----------- |
| E-01 | [What was observed]                      | [path:line or link] | [H-XX]      | [H-XX]      |

### Elimination log

| Hypothesis | Eliminated by  | Key contradicting evidence      |
| ---------- | -------------- | ------------------------------- |
| H-02       | E-03           | [Why this cause is ruled out]   |

## 💡 Triage trace - detailed analysis

[Walk through the reasoning: how hypotheses were formed, tested, and narrowed. Show the causal chain from root cause to observed symptom.]

## 🟰 Diagnose - findings and decisions

- **Root cause:** [Confirmed cause with evidence]
- **Causal chain:** [Root cause -> intermediate effects -> observed symptom]
- **Contributing factors:** [Conditions that enabled the bug but are not the root cause]
- **Confidence:** [High | Medium | Low] — [justification]
- **Unknowns:** [What could not be determined]

## 📋 Evidence for hypothesis evaluation

| Hypothesis | Evidence for           | Evidence against       | Verdict         |
| ---------- | ---------------------- | ---------------------- | --------------- |
| H-01       | E-01, E-04             | —                      | Confirmed       |
| H-02       | E-02                   | E-03, E-05             | Eliminated      |

## 🎬 Prescribe - next steps

1. **P-01: [Proposed fix]**
   - Change: [Minimal modification to address root cause]
   - Target: [Files, symbols, components]
   - Risk: [What could this break? Rollback options?]
   - Validation: [Specific test or check to confirm the fix]
   - Stop when: [How to know the fix worked]

### Preventive measures

- [What test, guard, or monitoring would have caught this earlier?]

## 📚 Evidence index

| ID   | Source                                           | Role                  | Evidence class or limitation                   |
| ---- | ------------------------------------------------ | --------------------- | ---------------------------------------------- |
| E001 | [Precise path, symbol, heading, output, or link] | [What it establishes] | [Observed, claimed, freshness, or scope limit] |
