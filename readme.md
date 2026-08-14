# Nix general notes

**this file is maintained by the author**

Need to assist with reviewing information.
- reduce cognitive load by organizing and layering info
- link sources for audit and provenance
- summarize and visualize

## Typical tasks:
  - 💭 orientation - intent, overview
  - 🧭 navigation  - content, links
  - 🧩 separation  - layers, sequence
  - ⚖️ decisions   - premises, rationale
  - ⭐ quality     - responsibility, validation
  - 🎬 action      - gaps, priorities

## Typical contexts:
  - Documentation
  - Research
  - Design
  - Epics
  - Stories
  - WIP
  - Speckit
  - PRs

## Tools:

### 🦄 NIX Quick discovery
  - Explain workspaces using a six-stage reasoning cycle (Reflect, Explore, Connect, Imagine, Produce, Empower)
  - Use `/nix` to quickly discover where action is needed and build a usable mental model.

### 🪄 WIZ Deep work-in-progress review
  - Review Jira ticket, PR, or branch work with traceable finding chains (F-01 -> I-01 -> A-01)
  - Use `/wiz` to follow up a nix discovery with deeply analyzed, calibrated findings.

### 📚 LIT Layered Information Technique
  - Turn dense source documents into layered, traceable, evidence-linked guides
  - Use `/lit` to synthesize technical documents into a professional guide with progressive disclosure.

### 📃 KIT Speckit Analysis
  - Review and reconstruct SpecKit project status with evidence-backed traceability
  - Use `/kit` to reorient and sanity-check a speckit-based branch.

### 🖼️ PIX Slideshow generator
  - Present documented information as a Marp-compatible visual slideshow
  - Use `/pix` to transform a document through Survey, Storyboard, Compose, Polish, and Deliver.

### 🧩 DAC Divide and conquer
  - Coordinate complex Jira-backed delivery through dependency-aware portions
  - Use `/dac` to partition a feature into coordinated, independently executable portions.

### 👮 COP Sanity review
  - Independent engineering reviewer targeting AI-specific vulnerabilities
  - Use `/cop` to challenge assumptions, detect hallucinations, and prevent overengineering.

### 🛠️ FIX Triage and diagnosis
  - Multi-path hypothesis triage for bugs, errors, and unexpected behavior
  - Use `/fix` to diagnose a symptom through competing hypotheses and systematic elimination.

### 🌡️ VAL Validation design
  - Test strategies, test data generation, and coverage assessment
  - Use `/val` to design validation, generate test cases, and assess whether a solution works.

### 🎬 ACT Action extraction
  - Turn analysis into tickets, summaries, task lists, and handoff notes
  - Use `/act` to extract a concise actionable artifact from any analysis output.

### 🤔 UMM Skill navigator
  - Don't know where to start? Shows available skills, recent work, and suggests what to use
  - Use `/umm` to see the skill catalog, or `/umm <context>` for a targeted suggestion.

## Applicability

| Context        | Typical flow                                          |
| -------------- | ----------------------------------------------------- |
| Documentation  | 📚 lit -> 🖼️ pix                                     |
| Research       | 🦄 nix -> 📚 lit -> 🖼️ pix                           |
| Design         | 🦄 nix -> 📚 lit -> 🖼️ pix                           |
| Issue triage   | 🦄 nix -> 🪄 wiz -> 📚 lit -> 🖼️ pix                 |
| Epics          | 🦄 nix -> 🪄 wiz, then 🧩 dac to coordinate          |
| Stories        | 🦄 nix -> 🪄 wiz, then 🧩 dac to coordinate          |
| WIP            | 🦄 nix -> 🪄 wiz -> 👮 cop -> 🌡️ val                 |
| Speckit        | 📃 kit                                                |
| PRs            | 🦄 nix -> 🪄 wiz -> 👮 cop                            |
| Bugs/Incidents | 🛠️ fix -> 🎬 act (ticket) or 🛠️ fix -> 👮 cop         |
| Test planning  | 🌡️ val                                                |
| Communication  | (any skill) -> 🎬 act                                 |

All skills capture external references (Atlassian, web) into a `./md` folder as markdown snapshots before analysis. All use a shared visual language from `visual-language.md`.

🚧 🚧 🚧 🚧 🚧 🚧 🚧 🚧 tasks

✔️ make the graphics consistent through the skill series
✔️ make lit capable of exporting confluence/jira to a md capture (all skills now have ./md capture)
✔️ update the skill descriptions
✔️ review the wiz skill compared with the nix
  - nix is quicker, more concise (Compact/Standard/Deep)
  - wiz is deeper with traceable finding chains (Quick/Standard/Deep)
  - both use the shared visual language
✔️ review the dac skill
  - uses shared visuals in all workspace templates
✔️ review cop
  - reads prefactoring development guidance
  - AI-specific vulnerabilities extracted to references/ai-vulnerabilities.md
  - uses shared visual language
✔️ review the yaml for consistency