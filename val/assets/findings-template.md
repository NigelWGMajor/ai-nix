<!-- Template note: symbols in this template are examples drawn from references/visual-language.md.
     Always read visual-language.md before generating output and use its current symbol assignments.
     If visual-language.md has been updated since this template was last edited, its symbols take precedence. -->

# Validation report: [target summary]

> **Purpose/question:** [What this validation assesses]
>
> **Audience/use:** [Who needs this assessment and why]
>
> **Scope:** [Target implementation, acceptance criteria, and test boundary]
>
> **Evidence boundary:** [What was tested, what was not testable]
>
> **Status/freshness:** [Validation timestamp, exact HEAD, environment]
>
> **Material limitations:** [Constraints that affect the assessment]
>
> **Depth:** [Quick, Standard, or Deep]
>
> **Coverage assessment:** [One concise statement of validation confidence]

## 💭 Scope - target and orientation

[What solution is being validated, why it matters, and the overall confidence level.]

### At a glance

| Dimension             | Status                        | Evidence                      |
| --------------------- | ----------------------------- | ----------------------------- |
| Target                | [Implementation identity]     | [Branch, HEAD, or artifact]   |
| Acceptance criteria   | [Count covered / total]       | [Source of criteria]          |
| Test coverage         | [Summary]                     | [Levels used]                 |
| Highest risk          | [Most consequential gap]      | [Why]                         |
| Overall confidence    | [High | Medium | Low]         | [Justification]               |
| Recommended action    | [Ship / fix first / more tests] | [Basis]                     |

### 🧭 Requirements and existing tests

- **Acceptance criteria:** [Source and count]
- **Existing test coverage:** [What's already tested, framework, conventions]
- **Test infrastructure:** [Available frameworks, fixtures, CI]
- **Risk areas:** [Where failure is most likely or costly]

## 🔗 Design - test strategy

### Coverage matrix

| Criterion | Test cases  | Level           | Result   | Confidence |
| --------- | ----------- | --------------- | -------- | ---------- |
| [AC-01]   | T-01, T-02  | [unit/int/e2e]  | [status] | [level]    |

### Risk-based test priorities

| Risk area             | Test approach           | Coverage      |
| --------------------- | ----------------------- | ------------- |
| [Area]                | [Strategy]              | [T-XX refs]   |

## 💡 Generate - test cases and data

### Test cases

#### T-01: [Test name]

- **Input:** [Setup and input data]
- **Action:** [What to execute]
- **Expected:** [Expected output or behavior]
- **Level:** [unit | contract | integration | e2e | manual]

### Generated test data

[Test data in the format the project's test infrastructure expects — SQL, JSON, CSV, factory calls, etc.]

### Decision tables

[For complex conditional logic, generate the full input/output matrix.]

## 📋 Execute - test results

| ID   | Test                         | Result  | Evidence                       |
| ---- | ---------------------------- | ------- | ------------------------------ |
| T-01 | [Test name]                  | [status]| [Command, output, or "not run"]|

## 🟰 Assess - findings and decisions

### Coverage assessment

- **Covered:** [Which criteria are validated with confidence]
- **Partially covered:** [Which criteria have incomplete validation]
- **Uncovered:** [Which criteria have no validation]

### Gaps and risks

| ID   | Gap or risk                  | Impact            | Recommendation              |
| ---- | ---------------------------- | ----------------- | --------------------------- |
| G-01 | [What's not validated]       | [Consequence]     | [What to add]               |

### Existing test quality

[Are current tests meaningful? Do they test real behavior or trivial conditions?]

## 🎬 Recommended additions - next steps

1. **[Test to add permanently]**
   - Purpose: [What it validates]
   - Level: [unit | integration | e2e]
   - Priority: [Must-have | Should-have | Nice-to-have]

## 📚 Evidence index

| ID   | Source                                           | Role                  | Evidence class or limitation                   |
| ---- | ------------------------------------------------ | --------------------- | ---------------------------------------------- |
| E001 | [Precise path, symbol, heading, output, or link] | [What it establishes] | [Observed, claimed, freshness, or scope limit] |
