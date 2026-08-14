<!-- Template note: symbols in this template are examples drawn from references/visual-language.md.
     Always read visual-language.md before generating output and use its current symbol assignments.
     If visual-language.md has been updated since this template was last edited, its symbols take precedence. -->

# Sanity review: [target description]

> **Purpose/question:** [What this review assesses]
>
> **Audience/use:** [Who needs this assessment and why]
>
> **Scope:** [Target change, included files, and review boundary]
>
> **Evidence boundary:** [What was inspected, what was inaccessible]
>
> **Status/freshness:** [Review timestamp, exact HEAD, worktree state]
>
> **Material limitations:** [Constraints that affect the review]
>
> **Depth:** [Quick, Standard, or Deep]

## 💭 Executive verdict

[One paragraph: overall assessment and confidence level (High, Medium, or Low).]

## ⚠️ Major risks

- [Most consequential risks, bullet list]

## 🧭 Requirement alignment review

- **Intended goal:** [What the implementation appears to solve]
- **Alignment score:** [Aligned | Minor drift | Significant drift]
- **Drift items:** [Features or behavior not requested]

## 🔎 Assumption audit

| Assumption                | Classification | Evidence                     |
| ------------------------- | -------------- | ---------------------------- |
| [Assumption]              | [Verified/Probable/Unsupported/Contradicted] | [Source or MISSING EVIDENCE] |

## 🔗 Schema and contract verification

| Element   | Used as        | Evidence       | Status         |
| --------- | -------------- | -------------- | -------------- |
| [Name]    | [How used]     | [Source]       | [Verified/Partially verified/Assumed/Contradicted] |

## 💡 Simplicity review

- **Unnecessary abstractions:** [Items or none]
- **Unnecessary layers:** [Items or none]
- **Premature generalization:** [Items or none]
- **Premature optimization:** [Items or none]

## 🟰 Failure analysis and risk assessment

### Failure modes

| Trigger          | Impact           | Detection        | Mitigation       |
| ---------------- | ---------------- | ---------------- | ---------------- |
| [Trigger]        | [Impact]         | [How detected]   | [Prevention]     |

### Risk assessment

| Risk dimension    | Rating           | Justification                     |
| ----------------- | ---------------- | --------------------------------- |
| Correctness       | [Low/Medium/High]| [Why]                             |
| Maintainability   | [Low/Medium/High]| [Why]                             |
| Operational       | [Low/Medium/High]| [Why]                             |
| Security          | [Low/Medium/High]| [Why]                             |

## ❓ Skeptical challenge

- **Most likely wrong:** [What is probably incorrect]
- **Breaking assumption:** [What would break this immediately]
- **Deceptive correctness:** [What looks right but probably isn't]

## 🎬 Recommended actions

### Keep
- [What is well done and should be preserved]

### Change
- [What must be modified, prioritized]

### Delete
- [What should be removed to reduce risk]

## 📚 Evidence index

| ID   | Source                                           | Role                  | Evidence class or limitation                   |
| ---- | ------------------------------------------------ | --------------------- | ---------------------------------------------- |
| E001 | [Precise path, symbol, heading, output, or link] | [What it establishes] | [Observed, claimed, freshness, or scope limit] |
