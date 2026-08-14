# VAL output contract

Use this contract for Standard and Deep VAL validation reports. Adapt the exact sections to the target while preserving the five-stage method, coverage traceability, and honest assessment.

## Output spine

Use the shared output spine from `documentation-standard.md` with these VAL mappings:

| Shared role                | VAL section                                |
| -------------------------- | ------------------------------------------ |
| Title and reader contract  | Title block with target and assessment      |
| Orientation                | Scope - target and coverage summary         |
| At a glance                | Coverage matrix summary                    |
| Foundations                | Scope - requirements and existing tests     |
| Relationships and evidence | Design - test strategy and risk areas       |
| Detailed analysis          | Generate - test cases and test data         |
| Findings and decisions     | Assess - coverage and confidence            |
| Validation                 | Execute - test results                      |
| Next steps                 | Recommended permanent test additions        |
| Evidence index             | Evidence index                              |

## Test case tracking

Use stable IDs:

| Type        | Prefix | Example | Purpose                          |
| ----------- | ------ | ------- | -------------------------------- |
| Test case   | T-XX   | T-01    | A specific validation scenario   |
| Gap         | G-XX   | G-01    | An identified coverage gap       |
| Risk        | R-XX   | R-01    | An untested risk area            |

## Coverage matrix

Map acceptance criteria to test cases:

| Criterion | Test cases | Level | Result | Confidence |
| --- | --- | --- | --- | --- |
| [From ticket/spec] | T-01, T-02 | [unit/integration/e2e] | [passed/failed/not run] | [high/medium/low] |

## Test result status

| Status   | Meaning                                                 |
| -------- | ------------------------------------------------------- |
| Passed   | Test executed and produced expected result               |
| Failed   | Test executed and produced unexpected result             |
| Blocked  | Test could not execute due to environment or dependency  |
| Skipped  | Test intentionally omitted with recorded reason          |
| Not run  | Test designed but not yet executed                        |

## Visual presentation

Read `visual-language.md` before adding symbols. Use only its defined roles. The visual-language reference is authoritative; its current symbol assignments override any symbols appearing in templates or examples elsewhere in this package.

## Quality gate

- [ ] Every acceptance criterion maps to at least one test case.
- [ ] Test levels are appropriate (not over-mocking, not over-integrating).
- [ ] Boundary values and error cases are covered, not just happy paths.
- [ ] Generated test data is realistic and representative.
- [ ] Test results distinguish passed, failed, blocked, skipped, and not run.
- [ ] Coverage gaps are explicitly identified with risk assessment.
- [ ] The confidence assessment is honest about what remains unvalidated.
- [ ] Existing test quality is assessed, not just new coverage.
- [ ] Symbols come from the configured `visual-language.md` palette.
- [ ] Test code was not written without explicit authorization.
