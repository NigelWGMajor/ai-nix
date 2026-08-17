# FIX output contract

Use this contract for Standard and Deep FIX triage reports. Adapt the exact sections to the symptom while preserving the six-stage method, hypothesis tracking, evidence integrity, and actionable prescription.

## Output spine

Use the shared output spine from `documentation-standard.md` with these FIX mappings:

| Shared role                | FIX section                                |
| -------------------------- | ------------------------------------------ |
| Title and reader contract  | Title block with symptom and diagnosis      |
| Orientation                | Capture - symptom and orientation           |
| At a glance                | Hypothesis summary table                   |
| Foundations                | Capture - context and recent changes        |
| Relationships and evidence | Investigate - evidence and relationships    |
| Detailed analysis          | Hypothesize + Narrow - triage trace         |
| Findings and decisions     | Diagnose - root cause and confidence        |
| Validation                 | Evidence for/against each hypothesis        |
| Next steps                 | Prescribe - proposed fix and validation     |
| Evidence index             | Evidence index                              |

## Hypothesis tracking

Use stable IDs that chain across stages:

| Stage       | Prefix | Example | Purpose                          |
| ----------- | ------ | ------- | -------------------------------- |
| Hypothesis  | H-XX   | H-01    | A specific testable cause claim  |
| Evidence    | E-XX   | E-01    | An observation for/against       |
| Diagnosis   | D-XX   | D-01    | The confirmed root cause         |
| Prescription| P-XX   | P-01    | A proposed fix action            |

Link evidence to hypotheses: "E-03 supports H-01, contradicts H-02."

## Hypothesis status

| Status      | Meaning                                                    |
| ----------- | ---------------------------------------------------------- |
| Active      | Under investigation, not yet confirmed or eliminated       |
| Confirmed   | Strong evidence supports this as the root cause            |
| Eliminated  | Strong evidence contradicts this hypothesis                |
| Merged      | Combined with another hypothesis (state which)             |
| Deferred    | Cannot be tested with available evidence                   |

## Visual presentation

Read `visual-language.md` before adding symbols. Use only its defined roles. The visual-language reference is authoritative; its current symbol assignments override any symbols appearing in templates or examples elsewhere in this package.

## Source identifiers and shorthand

When sources or the triage itself uses opaque identifiers (hypothesis IDs like H-01, evidence IDs like E-03, requirement codes, work item IDs, or internal acronyms) and those identifiers appear in the report:

1. **Define before use.** Provide a reference table or legend that maps each identifier to its full description before using it in running text.
2. **Link to origin.** Each identifier's first definition must include a link to the source location where it is defined when the source is a local document.
3. **Stand-alone readability.** A reader encountering any identifier must be able to resolve its meaning without leaving the document.
4. **Derivative documents.** When a derivative artifact (ticket, handoff, action plan) uses identifiers from the triage report, it must link back to the report's definitions.

## Quality gate

- [ ] The symptom is precisely documented before hypotheses are formed.
- [ ] At least two competing hypotheses were considered.
- [ ] Evidence is classified and linked to specific hypotheses.
- [ ] Eliminated hypotheses have recorded evidence for their elimination.
- [ ] The diagnosis explains all aspects of the observed symptom.
- [ ] Confidence level is stated and justified.
- [ ] The proposed fix is minimal and targets the root cause.
- [ ] Validation criteria for the fix are specific and testable.
- [ ] Symbols come from the configured `visual-language.md` palette.
- [ ] Source-originated identifiers (hypothesis IDs, requirement codes, work item IDs) are defined before first use and linked to their source.
- [ ] No code mutation was performed merely to complete the triage.
