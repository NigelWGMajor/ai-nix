---
name: umm
description: Show available skills and suggest which one to use. Use when unsure which skill fits the task, when exploring what's available, or when the user needs routing guidance. This is the entry point for the skill suite.
---

# UMM Skill Navigator

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user.
## `new` fresh-run override

When `new` is a standalone invocation keyword (for example, `/nix new <topic>`), start a fresh run. The ordinary word `new` within a topic or other prose does not enable this mode. This reset applies only to prior skill-run artifacts: continue to inspect the existing codebase, user-supplied material, and authoritative systems normally.

Do not inspect, resume, or reuse a prior `.data/` or `.dac/` run. After resolving the exact workspace folder this run would otherwise write into or update, if that folder already exists, first rename it in the same parent using the first unused alphabetic suffix: `<name>-a`, `<name>-b`, ..., `<name>-z`, then `<name>-aa`, and so on. Never overwrite, merge, or archive unrelated folders or folders used solely as read-only inputs. If the fresh run creates a distinct new destination or is read-only, do not rename anything.

The archive move needs the same local-write approval as writing the destination. Report the old and archive paths, then continue as though that run never existed. `new` does not authorize source changes, Git mutations, tests, deployment, Jira, or other remote actions.

## Output location

When searching for skill output, resolve `TOOLING_OUTPUT_PATH` first: absolute values are the output base and `./` or `.\\` is relative to the repository root or current folder. Search the output base directly for standard skill runs and `<output-base>/.dac/` for DAC workspaces; when unset, the output base is `<workspace-root>/.data`.

When invoked, read every `guidance.md` file from sibling skill directories and display a compact navigator. If the user included context in their prompt, suggest which skill(s) to use. When skill output exists in the workspace, surface what needs attention.

## Behavior

1. Read the first heading line from each sibling skill's `guidance.md`:
   - `nix/guidance.md`
   - `wiz/guidance.md`
   - `lit/guidance.md`
   - `kit/guidance.md`
   - `pix/guidance.md`
   - `dac/guidance.md`
   - `dac-help/guidance.md`
   - `pro/guidance.md`
   - `gap/guidance.md`
   - `cop/guidance.md`
   - `fix/guidance.md`
   - `val/guidance.md`
   - `act/guidance.md`
   - `mem/guidance.md`
   - `map/guidance.md`
   - `tut/guidance.md`

2. Display this compact catalog:

```
Available skills:

🦄 /nix *  — Quick discovery: explore a workspace, branch, or topic
🪄 /wiz *  — Deep review: analyze a ticket, PR, or branch in depth
📚 /lit *  — Document synthesis: turn dense sources into layered guides
📃 /kit =  — Speckit analysis: review speckit-based project status
🖼️ /pix *  — Slideshows: turn a document into a paged visual presentation
🧩 /dac *  — Divide & conquer: coordinate portioned Jira-backed delivery !!
🧩❓ /dac-help =  — DAC guidance: resolve allocation, routing, and execution uncertainty
🪜 /pro *  — PR reconstruction: split a broad PR, track child PRs, and converge a parent PR !!
👮 /cop *  — Sanity review: challenge AI-generated code
🔗 /gap *  — Hierarchical review: verify one branch or a recorded DAC/Pro hierarchy !!
🛠️ /fix *  — Triage: diagnose bugs through multi-path hypotheses
🌡️ /val *  — Validation: design tests, generate test data, coverage
🎬 /act +  — Action extract: distill analysis into actionable info
🎗️ /mem =  — Memo recall: search markdown notes for relevant information
🗺️ /map *  — Navigator: map wip on a branch or workspace
🎓 /tut *  — Tutorial: generate step-by-step how-to guides with diagrams
🔮 /umm =  — This navigator

=  read-only   +  adds to existing files   *  creates working files (.data/) !! multi-branch

Tip: add `?` to any skill for its capability card (for example, `/nix ?`). Add standalone `new` after a skill name for a fresh run; an existing `.data/` or `.dac/` destination is archived with the next alphabetic suffix before that skill writes.
```

3. Display the applicability table:

```
Typical flows:

Documentation   📚 lit -> 🖼️ pix
Research        🎗️ mem -> 🦄 nix -> 📚 lit -> 🖼️ pix
Design          🦄 nix -> 📚 lit -> 🖼️ pix
Issue triage    🦄 nix -> 🪄 wiz -> 📚 lit -> 🖼️ pix
Epics           🦄 nix -> 🪄 wiz -> 🧩 dac
Stories         🦄 nix -> 🪄 wiz -> 🧩 dac
DAC branches    🧩 dac -> 🔗 gap
DAC guidance    🧩❓ dac-help -> 🧩 dac
Broad PR split  🪜 pro -> 🔗 gap or 🧩 dac
Pro resume      🗺️ map -> 🪜 pro -> 🔗 gap
WIP             🗺️ map -> 🪄 wiz -> 👮 cop -> 🌡️ val
Speckit         📃 kit
PRs             🗺️ map -> 🪄 wiz -> 👮 cop
Branch resume   🗺️ map
Bugs/Incidents  🛠️ fix -> 🎬 act or 🛠️ fix -> 👮 cop
Test planning   🌡️ val
Tutorials       🦄 nix -> 🎓 tut -> 🖼️ pix
Communication   (any) -> 🎬 act
Note search     🎗️ mem
```

4. With `new`, do not scan `.data/`, `.dac/`, or `./md`, and do not read a control, Findings, or Actions file. Show the catalog and any intent-based routing only; state that prior workspace state was intentionally skipped, then stop before steps 5 and 6.

5. Otherwise, check for recent skill output. Scan `.data/` for instance directories modified today (by file timestamp on `Findings.md` or `00-control.md`). Also check `.dac/` for active workstreams. If any are found, show a "Recent work" section after the applicability table:

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

6. **Deep scan for needs-attention items.** When completed instances exist in `.data/` (any date, not just today), read the most recent `Findings.md` (and `Actions.md` if present) for the workspace and surface a "Needs attention" section. Scan for:

   **Open questions and unresolved decisions:**
   - Headings or table rows containing "open question", "unresolved", "TBD", "to be determined", "to be confirmed", or "policy decision"
   - Decision tables where the "Default" or "Who decides" column contains unresolved markers
   - Sections titled "Open questions", "Gaps", or "Conflicts"

   **Blocked work:**
   - Task list items marked as "Blocked", or containing "blocked on", "waiting on", "gated on"
   - Critical path items with unmet dependencies
   - Work items with a "Start now?" value of "Blocked" or similar

   **Stale captures:**
   - Files in `./md/` with a `captured:` frontmatter date older than 14 days — these may need refreshing

   **Missing derivative artifacts:**
   - A completed LIT instance with no corresponding PIX or ACT output (suggest the natural next skill)
   - A completed FIX instance with no corresponding ACT ticket extraction

   **Unactioned action items:**
   - An `Actions.md` whose task list items are all still unchecked

   Format the output as:

```
Needs attention:

  ❓ 6 open questions unresolved (Findings.md — "Open questions from Skills scope")
     → Resolve before locking implementation plan

  ⚠️ 3 work items blocked on F1 (Actions.md — Auth/Schema track)
     → F1 (schema + NuGet publish) is the critical path gate

  🔵 md/rebac-migration-playbook.md captured 21 days ago
     → Consider re-capturing if the source page has changed

  💡 LIT complete, no /act output yet
     → /act — extract task list or handoff summary from the findings
```

   **Rules for the deep scan:**
   - Read at most 2 Findings files (the most recent completed instances). Do not read every historical instance.
   - Read at most 1 Actions file.
   - Keep the scan fast — use grep-style searches for markers, not full document analysis.
   - Show at most 6 needs-attention items. If more exist, show the top 6 by severity (open questions > blocked work > stale captures > missing derivatives > unactioned items) and note how many were suppressed.
   - Do not repeat items already visible in the "Recent work" section.
   - If no attention items are found, omit the section entirely — do not show an empty "Needs attention" block.

6. If the user included any context beyond just invoking `/umm`:
   - Analyze their prompt for keywords and intent.
   - Suggest the most appropriate skill(s) with a one-line reason.
   - If a flow applies, show the recommended sequence.
   - If needs-attention items are relevant to the user's context, highlight them.
   - Format as: `Suggestion: /skill — reason`

## Examples

**User:** `/umm`
→ Show the catalog, applicability table, recent work if any exists today, and needs-attention items if completed instances exist.

**User:** `/umm I have a failing test and I don't know why`
→ Show the catalog, then: `Suggestion: /fix — diagnose the failure through multi-path hypothesis triage`

**User:** `/umm I need to present our architecture to the team`
→ Show the catalog, then: `Suggestion: /nix -> /lit -> /pix — explore the architecture, synthesize a guide, then generate slides`

**User:** `/umm there's a big epic I need to break down`
→ Show the catalog, then: `Suggestion: /nix -> /wiz -> /dac — orient on the epic, review it in depth, then partition into coordinated portions`

**User:** `/umm I need to write a ticket for this bug`
→ Show the catalog, then: `Suggestion: /fix -> /act — diagnose the bug, then extract a ticket description`

**User:** `/umm review the parent integration branch and all DAC portions`
→ Show the catalog, then: `Suggestion: /gap — apply a COP-style review to the recorded branch hierarchy and summarize integration risks`

**User:** `/umm where did we discuss caching strategy?`
→ Show the catalog, then: `Suggestion: /mem — search your markdown notes for passages about caching strategy`

**User:** `/umm what needs my attention?`
→ Show the catalog, then run the deep scan and show needs-attention items prominently. If no instances exist, say so.

## Constraints

- Do not start any analysis, review, or transformation. Umm only navigates and surfaces status.
- Keep the output compact — the whole point is quick orientation.
- Do not create instances, files, or state. Umm is purely conversational.
- If no context is provided and no recent work or instances exist, do not guess — just show the catalog.
- If recent work exists, show follow-up options but do not assume the user wants to continue — they may be starting something new.
- The deep scan reads existing output files but never modifies them.
- Do not read more than 2 Findings + 1 Actions file per invocation to keep response time fast.
