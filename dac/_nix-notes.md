# DAC deployment and usage notes

This is a concise operator note. Deploy the entire `dac` folder so `SKILL.md`, `references/`, `assets/`, and `scripts/` remain together.

## Requirements

- Codex or Claude Code with Agent Skills support
- Python 3 to use `scripts/dac.py`; it has no third-party dependencies
- Optional Jira, GitHub, Spec Kit, and specialist-skill access for the routes you intend to use

The helper edits only a selected `.dac/<workstream>/` Markdown workspace. It does not call Jira, Git, GitHub, Spec Kit, tests, builds, or network services.

## Install for Codex

Personal, available in every repository:

```text
~/.agents/skills/dac/
```

Project-scoped, shared with a repository:

```text
<repository>/.agents/skills/dac/
```

Copy this entire folder to the chosen location. Codex normally detects skill changes automatically; restart it if the skill does not appear. Verify with `/skills` or invoke it explicitly with `$dac`.

## Install for Claude Code

Personal, available in every project:

```text
~/.claude/skills/dac/
```

Project-scoped, shared with a repository:

```text
<repository>/.claude/skills/dac/
```

Copy this entire folder to the chosen location. Claude Code watches existing skill directories for changes; restart it if you created the top-level skills directory during the current session. Invoke the skill with `/dac`.

## Start a workstream

Launch Codex or Claude from the target repository and use a prompt such as:

```text
Use $dac to examine ABC-123, align on the parent outcome, and propose dependency-aware delivery portions. Remain read-only until an approval gate is reached.
```

For Claude Code, use `/dac` instead of `$dac`.

DAC will first gather evidence and propose the mission. After explicit W1 approval, initialize its editable workspace:

```bash
python <dac-skill-dir>/scripts/dac.py init --workstream ABC-123 --repo-root . --title "Outcome"
```

Runtime state belongs under the target repository, not inside the installed skill:

```text
.dac/ABC-123/
```

Resume later by asking the client to use DAC for `ABC-123`; it should read `.dac/ABC-123/00-control.md` first.

## Common helper commands

```bash
python <dac-skill-dir>/scripts/dac.py status --workspace .dac/ABC-123
python <dac-skill-dir>/scripts/dac.py validate --workspace .dac/ABC-123
python <dac-skill-dir>/scripts/dac.py ready --workspace .dac/ABC-123 --all
```

Use the assistant-led workflow for approvals, decisions, portion creation, execution routing, Jira writes, and PR integration. Do not treat a helper state change as authorization to modify code or remote systems.

## Update or remove

- Update by replacing the installed `dac` folder with the new complete folder.
- Keep repository `.dac/` workspaces; they are runtime records and are independent of the installed skill.
- Remove by deleting only the installed `dac` skill folder from `.agents/skills/` or `.claude/skills/`.

Current platform references: [OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills), [Claude Code skill guidance](https://code.claude.com/docs/en/slash-commands).
