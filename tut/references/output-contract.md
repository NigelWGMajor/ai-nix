# TUT output contract

Use this contract for Standard and Comprehensive TUT tutorials. Adapt the exact sections to the topic while preserving the step-based method, verification checkpoints, visual aids, and actionable structure.

## Contents

- [Reader contract](#reader-contract)
- [Output spine](#output-spine)
- [Tutorial structure](#tutorial-structure)
- [Steps and verification](#steps-and-verification)
- [Diagrams and visuals](#diagrams-and-visuals)
- [Code blocks](#code-blocks)
- [Troubleshooting](#troubleshooting)
- [Evidence index](#evidence-index)
- [Quality gate](#quality-gate)

## Reader contract

State, explicitly or through unmistakable context:

- Topic and task being taught.
- Audience and assumed prior knowledge.
- Outcome: what the reader can do after completing the tutorial.
- Scope and material exclusions.
- Prerequisites: tools, access, versions, and environment.
- Status and freshness.
- Material limitations (platform-specific, version-specific, etc.).
- Depth: Brief, Standard, or Comprehensive.

Lead with the outcome and prerequisites so the reader can quickly decide whether this tutorial is right for them.

## Output spine

Use the shared output spine from `documentation-standard.md` with these TUT mappings:

| Shared role                | TUT section                |
| -------------------------- | -------------------------- |
| Title and reader contract  | Title block                |
| Orientation                | What you will build/learn  |
| At a glance                | Overview diagram           |
| Content map                | Steps at a glance          |
| Foundations                | Prerequisites              |
| Relationships and evidence | Architecture / context     |
| Detailed analysis          | Step-by-step instructions  |
| Findings and decisions     | Variations / alternatives  |
| Validation                 | Verification checkpoints   |
| Next steps                 | What to do next            |
| Evidence index             | References                 |

Begin Orientation with:

1. What the reader will achieve.
2. Why this task matters or when it is useful.
3. A high-level diagram showing the end state or workflow.
4. Estimated time to complete.

## Tutorial structure

### Prerequisites

List every prerequisite before the first step:

- Required tools and their minimum versions.
- Required access, credentials, or permissions.
- Required prior knowledge or completed prior tutorials.
- Environment setup verification commands with expected output.

### Steps at a glance

Provide a numbered summary of all major steps so the reader can see the full journey before starting. Use a compact table or ordered list.

### Architecture / context

When the tutorial involves multiple components, services, or layers, include a Mermaid diagram showing how the pieces relate. Follow with prose interpretation. This helps the reader build a mental model before diving into steps.

## Steps and verification

### Step format

Each step must include:

1. **Step number and title**: a clear, action-oriented heading (e.g., "Step 3: Configure the database connection").
2. **Purpose**: one sentence explaining what this step achieves and why.
3. **Action**: the exact command, configuration change, or procedure in a fenced code block.
4. **Explanation** (when non-obvious): why this action is needed or what the key parameters mean.
5. **Verification checkpoint**: a concrete way to confirm the step succeeded — a command with expected output, a screenshot description, or an observable state change.

### Verification checkpoint format

Mark checkpoints distinctly using the visual-language palette. Each checkpoint should include:

- The check to perform (command, URL to visit, file to inspect).
- The expected result (exact output, status code, visible state).
- What to do if the check fails (brief pointer to Troubleshooting or a corrective action).

### Step dependencies

Steps must follow dependency order. If step N depends on step M, M must come first. Never reference a result from a later step. If steps can be performed in any order, say so explicitly.

## Diagrams and visuals

Include diagrams when they materially improve understanding. At minimum:

- **Standard depth**: at least one diagram (typically an overview or workflow).
- **Comprehensive depth**: two or more diagrams (overview, detailed flow, state transitions, or architecture).

Diagram types to consider:

| Relationship                               | Preferred form       |
| ------------------------------------------ | -------------------- |
| Overall workflow or process                | Flowchart            |
| Component relationships and data flow      | Architecture diagram |
| Request/response or multi-actor sequences  | Sequence diagram     |
| State changes through the tutorial         | State diagram        |
| Hierarchy or nesting                       | Tree                 |
| Repeated comparisons                       | Table                |

For Mermaid:

- Use `%%{init: {'theme':'dark'}}%%` immediately after the fence.
- Keep diagrams scannable (6-20 elements).
- Label important relationships.
- Follow every diagram with prose interpretation.

Read `visual-language.md` before adding symbols. Use only its palette. The visual-language reference is authoritative.

## Code blocks

- Use fenced code blocks with the correct language identifier for every command, configuration snippet, or code example.
- Show complete, copy-pasteable commands — not fragments that require the reader to guess context.
- When a command produces output the reader should verify, show the expected output in a separate code block labeled as output or with no language identifier.
- Distinguish between commands the reader types and output they should see.
- For long configuration files, show only the relevant section with enough context to locate it, and note where the section lives in the full file.

## Troubleshooting

For Comprehensive depth, include a Troubleshooting section after the main steps:

| Symptom | Likely cause | Resolution |
| ------- | ------------ | ---------- |
| [Error message or observed state] | [Root cause] | [Fix with exact commands] |

For Standard depth, include inline troubleshooting notes at verification checkpoints where failures are common.

## Evidence index

For Standard and Comprehensive output, include a compact references section:

| ID   | Source                              | Role                    | Limitation         |
| ---- | ----------------------------------- | ----------------------- | ------------------ |
| R001 | [Link or path]                      | [What it establishes]   | [Version, date]    |

Include only sources that materially informed the tutorial content.

## Quality gate

- [ ] Topic, audience, outcome, and prerequisites are explicit.
- [ ] The opening shows what the reader will achieve.
- [ ] An overview diagram or summary gives the big picture before steps begin.
- [ ] Every step has a number, title, action, and verification checkpoint.
- [ ] Steps follow dependency order with no forward references.
- [ ] All commands use fenced code blocks with correct language identifiers.
- [ ] Commands are complete and copy-pasteable.
- [ ] Verification checkpoints are concrete and include expected results.
- [ ] At least one diagram is present (Standard) or two (Comprehensive).
- [ ] Diagrams use Mermaid with dark theme and have prose interpretation.
- [ ] The tutorial is self-contained — no dangling external references.
- [ ] Troubleshooting covers common failure modes (Comprehensive).
- [ ] Symbols come from the configured palette and remain restrained.
- [ ] The ending provides a clear next action.
- [ ] The instance path uses `<workspace-root>/.data/tut-YY-MM-DD-<suffix>` and did not overwrite existing work.
- [ ] Generated artifacts remain outside source control.
