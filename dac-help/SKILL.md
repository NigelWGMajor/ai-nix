---
name: dac-help
description: Get guidance on DAC (Divide-and-Conquer) workflow. Use when stuck, unsure about next steps, or need advice on partitioning strategy, Jira organization, or executor choice.
---

# DAC Help

> **Quick help:** If invoked with `?` as the only parameter, read [guidance.md](guidance.md) and display its contents to the user. Do not begin the help workflow.

## Objective

Provide contextual guidance for users working with the DAC (Divide-and-Conquer) coordination skill.

## When to Use

- Unsure if you need DAC for your work
- Stuck in a DAC phase and not sure what to do next
- Need advice on how to partition work
- Confused about Jira organization strategy
- Don't know which executor to choose for a portion
- Want to understand what phase you're in
- Need to recover from a mistake or drift

## Approach

1. **Check for active DAC workspace** in current directory (`.dac/<workstream>/`)
2. If found, **read `00-control.md`** to understand current phase and state
3. If a `references/visual-language.md` exists in the DAC skill directory, read it and use its symbol palette when formatting help output. Do not hardcode symbols.
4. **Provide contextual help** based on:
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
- Solo work with no coordination needs

### Partitioning Strategies

**Simple case (1 Jira ticket):**
- Split into 2-3 portions for clean PRs
- Example: "DB schema" + "Backend API" under one ticket
- No new Jira tickets needed

**Complex case (Epic or multiple stories):**
- Each portion gets its own Jira sub-task
- Clear dependency tracking
- Independent review and merge

**Anti-patterns:**
- Portions that can't be tested independently
- Circular dependencies between portions
- Portions that merely mirror layers (all DB work in one portion)

### Jira Organization Strategies

**When to create sub-tasks:**
- Multiple independent work items under one story
- Need separate tracking for each deliverable
- Different implementers

**When to keep it simple:**
- Work fits in 1-2 PRs
- Same implementer throughout
- Natural sequence (DB → API → Tests)

### Executor Choice

| Executor | Use When | Example |
|----------|----------|---------|
| `speckit` | Ambiguous requirements, design decisions needed | New API design with unclear edge cases |
| `direct` | Clear, well-understood implementation | Add validation to existing endpoint |
| `skill:<name>` | Specialized workflow available | `skill:db-migration` for schema changes |
| `discovery` | Need research before design | "What libraries handle this use case?" |
| `human` | Requires organizational decision | "Which team owns this service?" |

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
- Focus: Ensure team visibility matches technical plan
- Key artifacts: Jira plan, Jira issues created
- Common mistake: Skipping this on "simple" work
- Tip: Always pause here - answer might be "no new tickets needed" but still ask

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
2. Show the progress indicator if in active DAC workspace
3. Provide specific, actionable guidance
4. Reference relevant documentation sections
5. Offer to help with next step

Be concise but complete. Users asking for help are often stuck - give them a clear path forward.
