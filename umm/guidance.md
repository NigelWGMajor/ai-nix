# 🤔 UMM helps you choose the right skill

| Capability           | Support | Alternative |
| -------------------- | ------- | ----------- |
| Workspace-aware      | ✔️      | nix         |
| Repo-aware           | ❌      | wiz         |
| Jira-aware           | ❌      | wiz         |
| Layered              | ❌      |             |
| Distilled            | ✔️      |             |
| Stateful             | ❌      |             |
| Safe output folder   | ❌      |             |
| Needs write approval | ❌      |             |

| Compatible skills |             |
| ----------------- | ----------- |
| Preprocessors     | —           |
| Postprocessors    | any skill, mem |

## What it does

UMM is the entry point for the skill suite. It shows the skill catalog, suggests which skill fits your task, and surfaces what needs attention in the current workspace.

**Three modes:**
- **Bare `/umm`** — catalog + recent work + needs-attention scan
- **`/umm <context>`** — catalog + skill suggestion based on your intent
- **`/umm ?`** — this capability card
- **`/<skill> new ...`** — start that stateful skill fresh; it archives an existing `.data/` or `.dac/` destination using the next alphabetic suffix before writing.

**Needs-attention scan** reads completed Findings and Actions in `.data/` and flags:
- Open questions and unresolved decisions
- Blocked work items
- Stale captured documents (>14 days)
- Missing derivative artifacts (e.g., LIT done but no PIX/ACT yet)
- Unactioned task lists

UMM never modifies files, creates instances, or starts analysis. It navigates and surfaces status — nothing more.
