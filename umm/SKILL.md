---
name: umm
description: Show available skills and suggest which one to use. Use when unsure which skill fits the task, when exploring what's available, or when the user needs routing guidance. This is the entry point for the skill suite.
---

# UMM Skill Navigator

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user.

When invoked, read every `guidance.md` file from sibling skill directories and display a compact navigator. If the user included context in their prompt, suggest which skill(s) to use.

## Behavior

1. Read the first heading line from each sibling skill's `guidance.md`:
   - `nix/guidance.md`
   - `wiz/guidance.md`
   - `lit/guidance.md`
   - `kit/guidance.md`
   - `pix/guidance.md`
   - `dac/guidance.md`
   - `cop/guidance.md`
   - `fix/guidance.md`
   - `val/guidance.md`
   - `act/guidance.md`

2. Display this compact catalog:

```
Available skills:

🦄 /nix  — Quick discovery: explore a workspace or topic
🪄 /wiz  — Deep review: analyze a ticket, PR, or branch in depth
📚 /lit  — Document synthesis: turn dense sources into layered guides
📃 /kit  — Speckit analysis: review speckit-based project status
🖼️ /pix  — Slideshows: turn a document into a visual presentation
🧩 /dac  — Divide & conquer: coordinate Jira-backed delivery
👮 /cop  — Sanity review: challenge AI-generated code
🛠️ /fix  — Triage: diagnose bugs through multi-path hypotheses
🌡️ /val  — Validation: design tests, generate test data, assess coverage
🎬 /act  — Action extract: turn analysis into actionable info 
Tip: add ? to any skill for its capability card (e.g. /nix ?)
```

3. Display the applicability table:

```
Typical flows:

Documentation   📚 lit -> 🖼️ pix
Research        🦄 nix -> 📚 lit -> 🖼️ pix
Design          🦄 nix -> 📚 lit -> 🖼️ pix
Issue triage    🦄 nix -> 🪄 wiz -> 📚 lit -> 🖼️ pix
Epics           🦄 nix -> 🪄 wiz -> 🧩 dac
Stories         🦄 nix -> 🪄 wiz -> 🧩 dac
WIP             🦄 nix -> 🪄 wiz -> 👮 cop -> 🌡️ val
Speckit         📃 kit
PRs             🦄 nix -> 🪄 wiz -> 👮 cop
Bugs/Incidents  🛠️ fix -> 🎬 act or 🛠️ fix -> 👮 cop
Test planning   🌡️ val
Communication   (any) -> 🎬 act
```

4. Check for recent skill output. Scan `.data/` for instance directories modified today (by file timestamp on `Findings.md` or `00-control.md`). Also check `.dac/` for active workstreams. If any are found, show a "Recent work" section after the applicability table:

```
Recent work (today):

  📃 kit-26-08-14-a  — KIT review of feature-xyz (complete)
  🪄 wiz-26-08-14-a  — WIZ review of ABC-12345 (in progress)

  Continue with:
    /wiz    — resume the in-progress review
    /cop    — sanity-check the reviewed code
    /act    — extract a ticket or summary from the findings
    /pix    — turn the findings into a presentation
```

   Derive the skill icon from the instance prefix. Read the instance's `00-control.md` to get the subject and status. Show only the natural next skills for each instance based on the applicability flows. Keep it to 3-4 suggestions maximum.

5. If the user included any context beyond just invoking `/umm`:
   - Analyze their prompt for keywords and intent.
   - Suggest the most appropriate skill(s) with a one-line reason.
   - If a flow applies, show the recommended sequence.
   - Format as: `Suggestion: /skill — reason`

## Examples

**User:** `/umm`
→ Show the catalog, applicability table, and recent work if any exists today.

**User:** `/umm I have a failing test and I don't know why`
→ Show the catalog, then: `Suggestion: /fix — diagnose the failure through multi-path hypothesis triage`

**User:** `/umm I need to present our architecture to the team`
→ Show the catalog, then: `Suggestion: /nix -> /lit -> /pix — explore the architecture, synthesize a guide, then generate slides`

**User:** `/umm there's a big epic I need to break down`
→ Show the catalog, then: `Suggestion: /nix -> /wiz -> /dac — orient on the epic, review it in depth, then partition into coordinated portions`

**User:** `/umm I need to write a ticket for this bug`
→ Show the catalog, then: `Suggestion: /fix -> /act — diagnose the bug, then extract a ticket description`

## Constraints

- Do not start any analysis, review, or transformation. Umm only navigates.
- Keep the output compact — the whole point is quick orientation.
- Do not create instances, files, or state. Umm is purely conversational.
- If no context is provided and no recent work exists, do not guess — just show the catalog.
- If recent work exists, show follow-up options but do not assume the user wants to continue — they may be starting something new.
