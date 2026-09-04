---
name: dac-help
description: Get guidance on DAC (Divide-and-Conquer) workflow. Use when stuck, unsure about next steps, or need advice on partitioning strategy, Jira allocation, executor choice, or solo ticket management.
---

# DAC Help

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the help workflow.
## `new` fresh-run override

When `new` is a standalone invocation keyword (for example, `/nix new <topic>`), start a fresh run. The ordinary word `new` within a topic or other prose does not enable this mode. This reset applies only to prior skill-run artifacts: continue to inspect the existing codebase, user-supplied material, and authoritative systems normally.

Do not inspect, resume, or reuse a prior `.data/` or `.dac/` run. After resolving the exact workspace folder this run would otherwise write into or update, if that folder already exists, first rename it in the same parent using the first unused alphabetic suffix: `<name>-a`, `<name>-b`, ..., `<name>-z`, then `<name>-aa`, and so on. Never overwrite, merge, or archive unrelated folders or folders used solely as read-only inputs. If the fresh run creates a distinct new destination or is read-only, do not rename anything.

The archive move needs the same local-write approval as writing the destination. Report the old and archive paths, then continue as though that run never existed. `new` does not authorize source changes, Git mutations, tests, deployment, Jira, or other remote actions.

## Objective

Provide contextual guidance for users working with the DAC (Divide-and-Conquer) coordination skill.

## When to Use

- Unsure if you need DAC for your work
- Stuck in a DAC phase and not sure what to do next
- Need advice on how to partition work
- Confused about Jira allocation strategy
- Don't know which executor to choose for a portion
- Want to understand what phase you're in
- Need to recover from a mistake or drift

## Approach

1. With `new`, do not scan `.dac/` or read any `00-control.md`. Give only fresh-start guidance: explain that `/dac new <workstream>` archives the exact target when necessary and begins at Align after W1 approval.
2. **Otherwise, check for an active DAC workspace** in current directory (`.dac/<workstream>/`)
3. If found, **read `00-control.md`** to understand current phase and state
4. If a `references/visual-language.md` exists in the DAC skill directory, read it and use its symbol palette when formatting help output. Do not hardcode symbols.
5. **Provide contextual help** based on:
   - Current phase (Align, Partition, Jira, Execute, Integrate)
   - User's specific question
   - Common patterns and anti-patterns

## Help Topics

### When Should I Use DAC?

Use DAC when:
- Work spans multiple PRs with dependencies
- Multiple implementers need coordination
- You need to pause/resume work over days/weeks
- Jira tracking is important for your team
- Work is too large for single context window

Don't use DAC when:
- Single PR with clear scope
- Exploratory spike or prototype
- Quick bug fix

**Consider solo tickets when:**
- You have existing tickets that need structure but no parent coordination
- Work items share a common ancestor but aren't tightly coupled
- You want acceptance criteria discipline for standalone work
- Tickets might later become part of larger initiatives

### Partitioning Strategies

Partitioning is about splitting *work* into clean, testable, independently reviewable portions. Jira ticket allocation is a separate decision that comes after.

**Good partitions:**
- Each has one coherent outcome and can be tested independently
- Boundaries follow vertical slices, not architecture layers
- Dependencies are explicit and acyclic
- Each maps naturally to one PR

**Anti-patterns:**
- Portions that can't be tested independently
- Circular dependencies between portions
- Portions that merely mirror layers (all DB work in one portion)

### Jira Allocation Strategies

DAC always pauses after partitioning to let the user decide how (or whether) to allocate Jira tickets. The coordinator presents context and options — it never creates tickets without explicit permission.

**No new tickets (strategy: none):**
- Work fits in 1-2 PRs under the parent ticket
- Same implementer throughout
- Portions are tightly coupled or small
- Natural sequence doesn't need separate tracking

**One ticket per partition (strategy: per-partition):**
- Multiple independent work items needing separate tracking
- Different implementers or reviewers per portion
- Each portion is substantial enough to warrant its own Story
- Team needs individual status visibility in Jira

**Custom mapping (strategy: custom):**
- Some portions share a ticket, others get their own
- Some portions map to existing tickets already in the hierarchy
- Mixed ownership where only some parts need separate tracking

### Executor Choice

| Executor | Use When | Example |
|----------|----------|---------|
| `speckit` | Ambiguous requirements, design decisions needed | New API design with unclear edge cases |
| `direct` | Clear, well-understood implementation | Add validation to existing endpoint |
| `skill:<name>` | Specialized workflow available | `skill:db-migration` for schema changes |
| `discovery` | Need research before design | "What libraries handle this use case?" |
| `human` | Requires organizational decision | "Which team owns this service?" |

### Solo Tickets vs. Portions

**Use solo tickets when:**
- Existing tickets need DAC structure without artificial parent Epic
- Work items share common ancestor but aren't coordinated
- You want acceptance criteria discipline and branch tracking for standalone work
- Tickets might later become part of larger initiatives

**Use portions when:**
- Work is part of coordinated parent outcome
- Dependencies between work items matter
- Parent decisions affect multiple portions
- You need integration planning across portions

**You can use both:** Portions for coordinated work under a parent, solo tickets for related but independent work in the same workstream.

**Solo ticket commands:**
```bash
# Adopt existing ticket
python <skill-dir>/scripts/dac.py solo adopt \
  --workspace .dac/ABC-123 \
  --ticket-id ABC-456 \
  --title "Fix auth bug" \
  --outcome "Users can log in reliably"

# Check solo ticket status
python <skill-dir>/scripts/dac.py solo status --workspace .dac/ABC-123

# Transition solo ticket state
python <skill-dir>/scripts/dac.py solo transition \
  --workspace .dac/ABC-123 \
  --ticket-id ABC-456 \
  --to executing
```

### Branch Sync
Use `/dac sync` (or ask `/dac` to check sync) to see whether portion branches and solo ticket branches are up to date with the parent integration branch.
```bash
python <skill-dir>/scripts/dac.py sync --workspace .dac/ABC-123
```
This reports behind/ahead counts, remote push status, and suggests merge or push commands for any out-of-sync active branches. Shows both portions (P:) and solo tickets (S:). Useful after:
- Merging a portion PR into the parent branch
- Pulling updates from the recorded target branch into the parent
- Resuming work after time away
The report is read-only. To act on its suggestions, ask `/dac` to merge and push (C3/R4 approval required).

### Safe DAC Branch Switching

Use `/dac switch` when you need to change between the parent integration branch, portions, DAC-managed solo tickets, or the recorded target branch while preserving in-progress work. First run `/dac switch` with no target to list the available choices. The leading `A`, `B`, `C` selector is the unambiguous switch key; an asterisk means DAC has recorded stashed work for that target.

DAC must have C3 approval before it performs a switch. If the current branch has uncommitted work, DAC creates an include-untracked named stash, records it in `00-control.md`, switches, and restores the target branch's recorded stash when safe. A restore conflict leaves the stash intact and stops for user resolution. Do not use raw `git stash` or `git switch` for DAC-managed context switches.

Before the first switch, DAC records the approved parent integration and target branches from `06-integration-plan.md`:

```bash
python <skill-dir>/scripts/dac.py switch --workspace .dac/PD-123456 configure \
  --master-branch <parent-integration-branch> --target-branch <recorded-target-branch>
python <skill-dir>/scripts/dac.py switch --workspace .dac/PD-123456
python <skill-dir>/scripts/dac.py switch --workspace .dac/PD-123456 A
python <skill-dir>/scripts/dac.py switch --workspace .dac/PD-123456 <recorded-target-branch>
```

### Preview Mode

Run `/dac preview ABC-123` to plan without side effects. Preview mode:

- Runs Align and Partition phases fully (mission, evidence, decisions, portion plan, Jira proposal with acceptance criteria checklists)
- **Requests W1 approval once** at the start, then writes all `.dac/` artifacts without further permission prompts
- **Stops before Jira ticket creation** — no code (C3), Jira/remote (R4), or build/test (V2) actions are taken
- Produces a complete, reviewable plan in `.dac/<workstream>/`

To continue after reviewing, run `/dac` normally — it resumes from the Jira approval step.

Preview is useful for:
- Getting stakeholder buy-in on partitioning before committing to tickets
- Reviewing acceptance criteria before they're written to Jira
- Validating the approach when you're unsure about scope or splitting

### Common Issues

**"I skipped the Jira review and regret it"**
- Pause execution on affected portions
- Run Jira review now (it's never too late)
- Update portion envelopes with correct Jira keys
- Resume execution

**"My portion is blocked by something unexpected"**
- Mark portion status as `blocked` in control file
- Document the blocker in portion envelope
- Escalate to coordinator (that's you or the person who started DAC)
- Create new decision or portion to address blocker

**"I need to add a portion mid-stream"**
- That's fine! DAC is designed for this
- Create new portion with next ID (P-005, etc.)
- Update portion plan to show new dependency
- Route when ready

**"I started work informally and now need structure"**
- Use `dac solo adopt` to bring ticket under management
- Establish proper acceptance criteria in envelope
- Track branch sync status
- Later promote to portion if it becomes part of larger coordination

**"Jira and .dac/ are out of sync"**
- Treat `.dac/` as source of truth for decisions and dependencies
- Treat Jira as source of truth for ownership and visible status
- Record the discrepancy in evidence or decisions
- Get explicit decision on how to reconcile

### Phase-Specific Guidance

**Align Phase:**
- Focus: Shared understanding before committing to approach
- Key artifacts: Mission, Evidence, Decisions
- Common mistake: Rushing through evidence gathering
- Tip: Spend extra time on Evidence - it pays off later

**Partition Phase:**
- Focus: Define clean boundaries with testable outcomes
- Key artifact: Portion plan
- Common mistake: Portions that can't be independently verified
- Tip: Each portion should have its own PR and test evidence

**Jira Phase:**
- Focus: User decides Jira allocation strategy — no tickets created without explicit permission
- Key artifacts: Jira plan with chosen strategy (none / per-partition / custom)
- Common mistake: Assuming tickets should be created; creating tickets without asking
- Tip: Present partition context (scope, dependencies, complexity) so the user can make an informed choice. "No new tickets" is a valid and common outcome

**Execute Phase:**
- Focus: Route portions to appropriate executors
- Key artifacts: Portion envelopes, executor results
- Common mistake: Not checking portion readiness (dependencies complete?)
- Tip: Only route portions when dependencies are `integrated` or `complete`

**Integrate Phase:**
- Focus: Merge PRs in dependency order, verify convergence
- Key artifacts: Integration review, PR merge sequence
- Common mistake: Merging out of dependency order
- Tip: Check the integration plan before merging anything

## Quick Decision Tree

```
Is work too big for one PR?
├─ No → Don't use DAC, just implement
└─ Yes → Has dependencies between parts?
   ├─ No → Consider splitting PRs but maybe not DAC
   └─ Yes → Use DAC
          ├─ Already started? → Run /dac to resume
          └─ Not started? → Run /dac to begin
```

## Recovery Patterns

**"I made a mistake in Mission"**
→ Decisions can supersede Mission items - document why and continue

**"Portion scope changed during execution"**
→ Mark current portion as `superseded`, create new portion with correct scope

**"I forgot to get approval before changing code"**
→ Pause, document what was done, get retroactive approval or revert

**"I lost my place after days away"**
→ Run `/dac` - it will resume from control file state

## References

- Full DAC workflow: `/dac` skill documentation
- Jira integration: `references/jira-integration.md` in DAC skill
- Artifact structure: `references/artifact-contract.md` in DAC skill
- Quality guidelines: `references/quality-and-integration.md` in DAC skill

## Response Format

Always:
1. Acknowledge the user's current situation
2. Show the progress indicator if in active DAC workspace, unless `new` is active
3. Provide specific, actionable guidance
4. Reference relevant documentation sections
5. Offer to help with next step

Be concise but complete. Users asking for help are often stuck - give them a clear path forward.
