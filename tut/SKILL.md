---
name: tut
description: Generate a step-by-step tutorial document on a requested topic, complete with diagrams, examples, and verification checkpoints. Use when the user invokes tut, asks for a how-to guide, walkthrough, or hands-on tutorial. The first pass asks clarifying questions to scope the tutorial; the second pass researches and produces the durable document. Do not use for analysis, review, bug triage, or document synthesis — use nix, wiz, fix, or lit for those. Explicit invocation overrides task-shape exclusions but never authorizes mutation.
---

# TUT Tutorial Generator

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the tutorial workflow.
## `new` fresh-run override

When `new` is a standalone invocation keyword (for example, `/nix new <topic>`), start a fresh run. The ordinary word `new` within a topic or other prose does not enable this mode. This reset applies only to prior skill-run artifacts: continue to inspect the existing codebase, user-supplied material, and authoritative systems normally.

Do not inspect, resume, or reuse a prior `.data/` or `.dac/` run. After resolving the exact workspace folder this run would otherwise write into or update, if that folder already exists, first rename it in the same parent using the first unused alphabetic suffix: `<name>-a`, `<name>-b`, ..., `<name>-z`, then `<name>-aa`, and so on. Never overwrite, merge, or archive unrelated folders or folders used solely as read-only inputs. If the fresh run creates a distinct new destination or is read-only, do not rename anything.

The archive move needs the same local-write approval as writing the destination. Report the old and archive paths, then continue as though that run never existed. `new` does not authorize source changes, Git mutations, tests, deployment, Jira, or other remote actions.

## Output location

Resolve `TOOLING_OUTPUT_PATH` before locating or creating durable output. When set, an absolute value is the output base; a value beginning `./` or `.\\` is relative to the resolved repository root (or current folder when no repository is available); reject other relative forms. All standard run paths below are relative to `<output-base>`; do not append a further `.data` segment. When unset, the output base is `<workspace-root>/.data`.

Generate a professional, self-contained tutorial document that guides any reader through a task from start to finish using a two-pass method:

`Scope -> Research -> Outline -> Draft -> Verify -> Deliver`

The first pass (Scope) is interactive — ask the user clarifying questions to frame the tutorial. The second pass (Research through Deliver) researches, writes, and validates the tutorial document.

## Standalone contract

- Contain the entire method in this package.
- Never require, invoke, or read RECIPE, LIT, KIT, NIX, WIZ, their phase skills, their caches, or their outputs at runtime.
- Do not require subagents, mentor agents, special slash commands, or model routing.
- Use available workspace tools and repository guidance without depending on a particular tool name.
- Default Brief work to a response in the conversation. Create a durable workspace document for Standard and Comprehensive work unless the user explicitly requests chat-only output.
- Treat the tutorial as a read-only output. Do not modify the subject system, repository, or workspace beyond the TUT instance directory.

## Begin or resume

Determine whether the request identifies an existing TUT instance. If an `<output-base>/tut-*` directory exists:

1. Read its `00-control.md` first.
2. Ask the user whether to **resume** the prior tutorial or **start a new instance**.
3. If resuming, continue from the recorded next safe action and do not repeat completed stages.
4. If more than one instance is plausible, list them and ask which to use.

## Resolve the topic

Apply this precedence:

1. Use explicit prompt parameters as the tutorial topic and scope.
2. Treat supplied paths, files, URLs, issue identifiers, or pasted material as named context for the tutorial subject.
3. With no parameters, ask the user what they want the tutorial to cover.

Do not require a Git repository. When Git exists, use repository context only when it materially helps the tutorial content.

## Pass 1: Scope

Before researching or writing, ask the user concise clarifying questions. Ask only what would materially change the tutorial's content, level, or structure. Typical questions:

**Always ask:**
- **Audience**: Who is this tutorial for? (beginner, intermediate, expert; role; assumed knowledge)
- **Outcome**: What should the reader be able to do after completing the tutorial?

**Ask when not obvious from the prompt:**
- **Prerequisites**: What tools, access, or setup does the reader need before starting?
- **Scope boundaries**: Anything explicitly in or out of scope?
- **Environment**: What platform, language version, framework, or tooling should the tutorial target?
- **Depth**: Brief (chat-only quick guide), Standard (structured document), or Comprehensive (detailed with diagrams, examples, troubleshooting)?

Do not ask more than 6 questions. Combine related questions. If the prompt already answers a question, skip it and state the assumption. Default to Standard depth when unspecified.

Wait for the user's answers before proceeding to Pass 2.

## Choose depth

- **Brief**: A quick-reference guide in the conversation. Steps, commands, and key notes only. No instance created unless the user asks to save.
- **Standard**: A structured tutorial document with numbered steps, code examples, diagrams where helpful, and verification checkpoints. Default.
- **Comprehensive**: A thorough guide with detailed explanations, multiple diagrams, alternative approaches, troubleshooting sections, edge cases, and a glossary.

## Create the tutorial instance

For Standard or Comprehensive work, initialize a durable instance before substantial research.

### Resolve the workspace root

The `<output-base>/tut-*` instance directory MUST be created under the resolved output base. Resolve the workspace root, used for the default base and relative `TOOLING_OUTPUT_PATH`, in this order:

1. An explicit user-supplied workspace path.
2. The repository root (the nearest ancestor containing `.git`).
3. Only as a last resort: the current working directory.

**Trunk workspace preference:** when multiple workspace roots are available (e.g. a multi-root VS Code workspace), check each for a `trunk` folder. If exactly one workspace root contains a `trunk` folder, use that root when resolving the output base regardless of which root the current file or working directory belongs to.

Always pass `--workspace` explicitly with the resolved root.

### Initialize

```text
python <skill-directory>/scripts/init_instance.py --workspace <workspace-root> --topic "<topic>" --audience "<audience>" --outcome "<outcome>" --depth <standard|comprehensive>
```

Optional arguments:

- `--slug "<slug>"`: override the auto-generated filename slug (derived from `--topic` when omitted).
- `--part "<letter>"`: append a `-part-<letter>` suffix for multi-part tutorials.

The initializer creates the next collision-safe `<output-base>/tut-YY-MM-DD-<suffix>` directory. It creates the output base when needed, never overwrites an existing instance, and copies the reader-facing template with a descriptive name derived from the topic (e.g., `tutorial-local-spicedb-dev-environment.md`).

### Output file naming

The reader-facing tutorial file is named `tutorial-<slug>.md` where `<slug>` is a lowercase-hyphenated version of the topic. For multi-part tutorials, each part is suffixed: `tutorial-<slug>-part-a.md`, `tutorial-<slug>-part-b.md`, etc. The actual filename is recorded in `00-control.md` under `Final document`.

When a tutorial is large enough to warrant splitting (e.g., distinct stages that can be followed independently), create separate instance parts using the `--part` argument.

### Instance contents

Maintain:

- `00-control.md`: identity, topic, audience, outcome, scope, phase, progress, assumptions, questions, and next safe action.
- `01-evidence.md`: material sources, references, tools, and limitations.
- `02-outline.md`: tutorial structure, step sequence, and planned diagrams.
- `tutorial-<slug>.md`: professional reader-facing tutorial document (name recorded in `00-control.md`).

Checkpoint `00-control.md` after each meaningful stage and before stopping. If the user explicitly requests chat-only output, do not create an instance. For Brief work, create an instance only when the user asks to save the result.

## Pass 2: Research through Deliver

### 2a. Research

Build the evidence landscape for the tutorial topic:

- Locate authoritative sources: official documentation, specifications, repository code, configuration files, API references.
- Inspect the subject system, components, conventions, and interfaces relevant to the tutorial steps.
- Identify common pitfalls, edge cases, and prerequisite checks.
- Note version-specific behavior, platform differences, and deprecation warnings.
- Record sources in `01-evidence.md`.

Prefer targeted retrieval over broad exploration. Gather only what the tutorial steps need.

### 2b. Outline

Design the tutorial structure in `02-outline.md`:

- **Prerequisites section**: tools, access, versions, and setup verification commands.
- **Step sequence**: ordered steps following the task's natural dependency chain. Each step should be independently verifiable.
- **Diagram plan**: identify where a visual (flowchart, architecture diagram, sequence diagram, state diagram) would materially help comprehension. Plan at least one diagram for Standard depth and two or more for Comprehensive.
- **Verification checkpoints**: after each major step or group of steps, plan a concrete check the reader can perform to confirm success.
- **Troubleshooting plan** (Comprehensive only): anticipate common failure modes and their resolutions.

### 2c. Draft

Write the tutorial to the named output file (recorded in `00-control.md`) using the template from `assets/findings-template.md`.

Before drafting:

1. Read [references/documentation-standard.md](references/documentation-standard.md) and apply its shared document, link, visual, handoff, and workspace-storage rules.
2. Read [references/output-contract.md](references/output-contract.md) for TUT-specific presentation rules.
3. Read [references/visual-language.md](references/visual-language.md). This file is the authoritative source for all symbols. Its current assignments override any symbols hardcoded in templates, output contracts, or other reference files.
4. Adapt [assets/findings-template.md](assets/findings-template.md) to the topic; do not force empty sections. Replace any template symbols with the current assignments from visual-language.md.

**Tutorial writing rules:**

- Lead with what the reader will achieve and what they need before starting.
- Number all steps. Use sub-steps (1a, 1b) only when a step has parallel or optional paths.
- Show every command, configuration change, or action the reader must perform in a fenced code block with the appropriate language identifier.
- After each significant step or group, include a **verification checkpoint** — a command, expected output, or observable state that confirms the step succeeded. Mark checkpoints with ✔️ so they are easy to scan.
- Use inline symbols from `visual-language.md` to mark recurring item types throughout the tutorial. These aid scanning without cluttering prose:
  - ✔️ for verification checkpoints and expected results.
  - 🩹 for gotchas, workarounds, common pitfalls, and "if this fails" recovery notes.
  - ⚠️ for consequential warnings the reader must heed before proceeding.
  - 📌 for key points that affect later steps or are easy to miss.
  - ❓ for open questions or things the reader may need to investigate.
  Keep symbol density restrained — a step with no gotchas or warnings needs no inline symbols beyond its checkpoint marker.
- Include diagrams using Mermaid where they materially improve understanding. Always follow a diagram with a prose interpretation. Use `%%{init: {'theme':'dark'}}%%` after the mermaid fence.
- Explain the *why* behind non-obvious steps — not every step, just the ones where skipping the explanation would leave the reader cargo-culting.
- For Comprehensive depth, include an "Alternative approaches" or "Variations" section where meaningful alternatives exist, and a "Troubleshooting" section covering common failure modes.
- Keep the tutorial self-contained: a reader should not need to leave the document to complete the task.
- Use precise, tested commands rather than pseudocode or placeholder paths.

### 2d. Verify

Before declaring the tutorial complete, perform these checks:

- **Completeness**: every step from the outline is present in the draft.
- **Order**: steps follow dependency order — no step references a result from a later step.
- **Verifiability**: every major step has a verification checkpoint.
- **Diagrams**: planned diagrams are present, use Mermaid correctly, and have prose interpretation.
- **Code blocks**: all commands and configuration snippets have correct language identifiers.
- **Prerequisites**: everything the reader needs is listed before the first step.
- **Self-containment**: no dangling references to external documents the reader cannot access.

### 2e. Deliver

Write the final tutorial to the named output file and return a concise chat handoff.

## Compose the output

The tutorial document uses the shared output spine adapted for instructional content. See [references/output-contract.md](references/output-contract.md) for the TUT-specific mapping.

For Brief output, follow the same clarity and verification rules without loading or reproducing the full template.

Always have an overview of the process, followed by the execution steps, followed by a troubleshooting appendix, and relegate details to a final appendix or appendices. Provide bookmark links to the appendices were appropriate.

Use visual language conventions to aid communication

If the procedures being documented have different cardinality (e.g. single-time setup, everyday use) use sections to clarify the different use cases. Use the same visual language symbols in the tutorial as in the template.

## Complete the tutorial

Apply the shared quality gate in [references/documentation-standard.md](references/documentation-standard.md) and the TUT-specific gate in [references/output-contract.md](references/output-contract.md). Report:

- The tutorial document path.
- The topic and intended outcome.
- Material limitations or environment assumptions.
- The most useful next action (e.g., follow the tutorial, review with the team, adapt for a different environment).

## Self-improvement signals

After real use, note recurring friction in `00-control.md`, such as missing question types in the Scope pass, unclear step structure, awkward template sections, or missing visual roles. Recommend a narrowly scoped skill adjustment rather than silently editing the installed skill during tutorial generation.
