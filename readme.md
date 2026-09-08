# Nix general notes

**this file is maintained by the author**


## Intent

These tools provide similar skills, but differentiated and tuned for different purposes.



## Output formats

The tools here typically use intermediary files and output files to allow idempotent use, and also to have allow findings of one step to be used in the next.,

Set `TOOLING_OUTPUT_PATH` to choose the shared output base. When it is unset, the default is `<workspace-root>/.data`. An absolute value is used directly; a value starting `./` or `.\` is relative to the resolved workspace root. Standard tool runs are created directly beneath that base, organized by tool name and date. DAC workspaces are created beneath `<output-base>/.dac`.

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
  - Use `/wiz` for deeply analyzed, calibrated findings.

### 📃 KIT Speckit Analysis
  - Review and reconstruct SpecKit project status with evidence-backed traceability
  - Use `/kit` to reorient and sanity-check a speckit-based branch.

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

### 📚 LIT Layered Information Technique
  - Turn dense source documents into layered, traceable, evidence-linked guides
  - Use `/lit` to synthesize technical documents into a professional guide with progressive disclosure.

### 🖼️ PIX Slideshow generator
  - Present documented information as a Marp-compatible visual slideshow
  - Use `/pix` to transform a document through Survey, Storyboard, Compose, Polish, and Deliver.

###  Tutorial 
  - Format documentation or analysis as a tutorial
  - Use `/tut` to produce targeted tutorial from findings or research
     
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
| Research       | 🦄 nix -> 📚 lit -> 🖼️ pix or                        |
| Design         | 🦄 nix -> 📚 lit -> 🖼️ pix                           |
| Issue triage   | 🪄 wiz -> 📚 lit -> 🖼️ pix                           |
| Epics          | 🪄 wiz, then 🧩 dac to coordinate                    |
| Stories        | 🪄 wiz, then 🧩 dac to coordinate                    |
| WIP            | 🦄 nix or 🪄 wiz or 🛠️ fix -> 👮 cop -> 🌡️ val       |
| Speckit        | 📃 kit                                                |
| PRs            | 🦄 nix | 🪄 wiz or 🛠️ fix -> 👮 cop                  |
| Bugs/Incidents | 🛠️ fix -> 🎬 act (ticket) or 🛠️ fix -> 👮 cop        |
| Test planning  | 🌡️ val                                                |
| Communication  | (any skill) -> 🎬 act                                 |

All skills capture external references (Atlassian, web) into a `./md` folder as markdown snapshots before analysis. All use a shared visual language from `visual-language.md`.

## Infrastructure

### MCP Server: VSCode Workspace Discovery

Located in `mcp-servers/vscode-workspace/`, this MCP server provides reliable workspace root resolution for all skills, independent of terminal CWD.

**Setup:**
```bash
cd mcp-servers/vscode-workspace
npm install
```

**Configure in `~/.claude/config.json`:**
(use your appopriate paths)
```json
{
  "mcpServers": {
    "vscode-workspace": {
      "command": "node",
      "args": ["B:\\ai\\ai-nix\\mcp-servers\\vscode-workspace\\index.js"]
    }
  }
}
```

See `mcp-servers/vscode-workspace/README.md` for full documentation.

### Deployment

Run `00-propagate-skills-to-claude-agent-codex.cmd` to deploy all skills from this source repo to:
- `%USERPROFILE%\.claude\skills\`
- `%USERPROFILE%\.codex\skills\`
- `%USERPROFILE%\.agents\skills\`

**Important:** Always edit skills in this repo, not in the deployed locations. Deployed copies are overwritten on each propagation.

The master visual-language.md file and other standards are typically copied form the nix folders: check the deployment ps1 files to be sure! At the time of writing, the critical fles that propagate to other tools are:
- /nix/references/visual-language.md
- /nix/references/docuemntation-standard.md

Specific to our work environment, there is a yaml file that defines the ids of Jira fields:
- jira-fields.local.yaml