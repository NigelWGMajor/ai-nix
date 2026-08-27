---
skill: map
description: Generate a task-resumption navigator with structured overview and clickable code map for any branch
when_to_use: When the user invokes /map, asks to understand work in progress, needs to resume or pick up a task, wants to map out a branch, or needs navigation context for a PR or ticket
trigger_patterns:
  - "/map"
  - "map this branch"
  - "map out the work"
  - "show me what's been done"
  - "help me resume this task"
tools:
  - Bash (git operations)
  - Read, Glob, Grep
  - mcp__codebase-memory-mcp__* (code indexing)
  - mcp__plugin_jira-integration_atlassian__* (when ticket context exists)
output_location: .data/map-YYYY-MM-DD-a/
output_files:
  - map.md (rich context document)
  - map.upstream.md (concise navigation format for Upstream extension)
isolation: none
interactive: true
---

# /map — Task Resumption Navigator

You are the **map** skill, part of the `/umm` skill suite. Your purpose is to generate a navigable overview of work in progress on any git branch, helping the user quickly understand context, status, and next steps when picking up, resuming, or collaborating on a task.

## Core Directive

Generate two artifacts that map the current branch's work:
1. **map.md** — Rich context document with intent, contributors, participants, sequence, status, and actionable next steps
2. **map.upstream.md** — Concise navigation file following the Upstream document format (see References)

The output must be **100% navigable**: every code component, file change, ticket, and branch mentioned should be a clickable link (file:line, Jira URL, git reference).

## Entry Point Detection

When invoked, immediately detect the context type:

### Context Types
- **Ticket-driven** — Branch name contains `PD-nnnnnn` or 6-digit number → extract ticket
- **DAC project** — Detect DAC artifacts, sibling branches, hierarchical structure
- **Speckit project** — Detect `spec.md`, `plan.md`, `tasks.md` → assess process completeness
- **Utility/maintenance** — No ticket context (user's own utilities, skills, etc.)
- **Main branch history** — User wants recent history overview

### Scope Determination
- **Default**: All commits since branch diverged from parent, prioritize recent
- **Context-informed**: Adjust based on project type (e.g., Speckit → entire project lifecycle)

## Interactive Workflow

This skill runs **inline and interactive** — time varies with complexity. Pause for clarification when needed.

### Phase 1: Context Triage (seconds)

1. **Analyze current branch**
   ```bash
   git rev-parse --abbrev-ref HEAD
   git rev-parse --abbrev-ref HEAD@{upstream}  # parent branch
   git rev-list --count HEAD ^$(git merge-base HEAD main)  # depth to main
   ```

2. **Detect project context** (check in this order)
   
   **A. Find repository root:**
   ```bash
   git rev-parse --show-toplevel
   ```
   
   **B. Check for DAC project:**
   ```bash
   # Look for .dac/ directory in repository root OR in common subdirectories (like trunk/)
   REPO_ROOT=$(git rev-parse --show-toplevel)
   if test -d "$REPO_ROOT/.dac"; then
     echo "DAC project detected at repo root"
   elif test -d "$REPO_ROOT/trunk/.dac"; then
     echo "DAC project detected in trunk/"
   elif test -d ".dac"; then
     echo "DAC project detected in current directory"
   fi
   ```
   If `.dac/` exists in any of these locations, this is a DAC project. The DAC directory may be:
   - At the repository root: `$REPO_ROOT/.dac`
   - In a subdirectory like `trunk/`: `$REPO_ROOT/trunk/.dac`
   - Relative to current working directory: `./.dac`
   Look for:
   - `.dac/<workstream>/00-control.md` (identifies the workstream)
   - `.dac/<workstream>/portions/` (identifies portions and their branches)
   - Sibling branches matching the workstream pattern (use `git branch --list`)
   
   **C. Check for Speckit project:**
   ```bash
   # Look for specs/ directory OR .speckit/ directory
   REPO_ROOT=$(git rev-parse --show-toplevel)
   if test -d "$REPO_ROOT/specs"; then
     # Check for spec artifacts in subdirectories
     find "$REPO_ROOT/specs" -maxdepth 2 -name "spec.md" -o -name "plan.md" -o -name "tasks.md"
   fi
   test -d "$REPO_ROOT/.speckit" && echo "Speckit config detected"
   ```
   If either exists, this is a Speckit project. Typical artifacts:
   - `specs/<feature>/spec.md` → specification complete
   - `specs/<feature>/plan.md` → planning complete
   - `specs/<feature>/tasks.md` → task breakdown complete
   - `.speckit/` → configuration directory
   
   **D. Extract ticket:**
   ```bash
   # Regex: (PD-\d{6}|\b\d{6}\b) from branch name
   git rev-parse --abbrev-ref HEAD | grep -oE '(PD-[0-9]{6}|[0-9]{6})'
   ```
   
   **E. Check for other skill artifacts:**
   ```bash
   ls -d .data/fix-* .data/nix-* .data/wiz-* 2>/dev/null
   ```

3. **Report detection results**
   
   After automatic detection, report what was found:
   ```
   Detected: DAC project (workstream ABC-123, portion P-002)
   Branch: feature/PD-123456-implement-auth
   Ticket: PD-123456
   Sibling branches: 4 other portions (2 complete, 1 in progress, 1 not started)
   ```
   
4. **Interactive prompts** (only if needed)
   - Multiple related branches detected:
     > "This branch is 1 of 5 in a DAC set (3 complete, 2 in progress). Analyze:
     > 1) Only this branch [default]
     > 2) This + incomplete branches
     > 3) All branches
     > 4) Custom selection"
   
   - Multiple Speckit features found:
     > "Found 3 Speckit features. Which should I map?
     > 1) user-authentication (matches branch name) [default]
     > 2) content-management
     > 3) All features"
   
   - Large commit history:
     > "Found 47 commits since divergence. Analyze:
     > 1) All commits [default for DAC/Speckit]
     > 2) Last 10 commits
     > 3) Let me specify a range"

Ask clarifying questions only if multiple valid interpretations exist (see Interactive prompts above).

### Phase 3: Evidence Gathering (varies)

#### Git Evidence
```bash
# Recent commits (chronological, highlight contributors)
git log --oneline --since="[scope]" --pretty=format:"%h|%an|%ar|%s"

# Changed files
git diff --name-status $(git merge-base HEAD [parent])..HEAD

# Sibling branches (if DAC context)
git branch --list '[pattern]*'
```

#### Jira Evidence (if ticket detected)
Use `mcp__plugin_jira-integration_atlassian__getJiraIssue` with cloudId `151636d7-9099-4803-a108-4f053f36c9fe`.

Extract:
- Ticket status, summary, description
- Acceptance criteria (for status matching)
- **Hierarchical links only** (parent Epic, child tasks, siblings) — surface structure, don't dive deep

If no Jira access or ticket not found, note it and continue.

#### Project Context Evidence

**DAC Project:**
```bash
# Find .dac directory (may be at repo root, in trunk/, or in cwd)
REPO_ROOT=$(git rev-parse --show-toplevel)
if test -d "$REPO_ROOT/.dac"; then
  DAC_DIR="$REPO_ROOT/.dac"
elif test -d "$REPO_ROOT/trunk/.dac"; then
  DAC_DIR="$REPO_ROOT/trunk/.dac"
elif test -d ".dac"; then
  DAC_DIR=".dac"
fi
# Find workstream directory
WORKSTREAM=$(ls -d $DAC_DIR/*/ 2>/dev/null | head -1 | xargs basename)
# Read control file for workstream identity
cat "$DAC_DIR/$WORKSTREAM/00-control.md"
# List portions
ls "$DAC_DIR/$WORKSTREAM/portions/"
# Check portion status and branches
cat "$DAC_DIR/$WORKSTREAM/portions/P-"*.md
```
Gather:
- Workstream ID and parent ticket from `00-control.md`
- Mission and success criteria from `01-mission.md`
- Portion IDs, titles, and assigned branches from `portions/P-*.md`
- Sibling branch status: `git branch --list '<pattern>*'` + recent commit dates
- Check which portions have results in `results/`
- PR links and status from portion metadata

**Speckit Project:**
```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
# Find feature directories
find "$REPO_ROOT/specs" -maxdepth 1 -type d -not -name specs
# For each feature, check artifacts
for feature in $REPO_ROOT/specs/*/; do
  echo "Feature: $(basename $feature)"
  test -f "$feature/spec.md" && echo "  ✅ spec.md"
  test -f "$feature/plan.md" && echo "  ✅ plan.md"
  test -f "$feature/tasks.md" && echo "  ✅ tasks.md"
done
```
Check completeness for the relevant feature:
- `spec.md` exists → specification complete
- `plan.md` exists → planning complete
- `tasks.md` exists → task breakdown complete
- Read `tasks.md` to compare checked tasks vs. actual commits
- Implementation commits → work in progress

**Other skills:**
```bash
ls -ltr .data/*/00-control.md 2>/dev/null
```
Check `.data/` for recent skill outputs (fix, nix, wiz, etc.) — reference if relevant to current work

#### Code Evidence (use code-indexing MCP)
Use `search_graph`, `trace_path`, `get_code_snippet` to:
1. Identify changed code components (from git diff)
2. **Get actual line numbers** — `search_graph` results include `start_line` field
3. Trace call chains: `trace_path(function_name, mode=calls)` for key entry points
4. Detect layers from namespace/folder/name conventions:
   - **Orchestrator**: `*.Orchestrator`, `/Orchestrators/`
   - **Controller**: `*.Controller`, `/Controllers/`
   - **Service**: `*.Service`, `/Services/`
   - **Repository**: `*.Repository`, `/Repositories/`
   - **Data**: `*.Data`, `/Data/`
   - **SQL**: `.sql` files, `/Stored Procedures/`, `/Tables/`, `/Views/`
   - **Other**: Utility, Model, DTO, etc.

Focus on **invocation sequence** (what needs to be in place for functionality), not individual method calls.

**CRITICAL for upstream.md**: Every code reference MUST have its actual line number from search_graph or grep -n. 
The upstream navigation file is useless with default `:1` line numbers. When code doesn't exist on current branch 
(e.g., DAC portions on sibling branches), note "on branch X" rather than linking with `:1`.
### Phase 4: Status Analysis (inline)

Classify each contribution as:
- ✅ **Complete** — Fully implemented, tested, no TODOs
- 🔶 **Partial** — Started, needs more work, has TODOs/FIXMEs
- ⬜ **Needed** — Not yet implemented, referenced but missing

#### Evidence Sources (context-dependent)
- **Jira**: Match acceptance criteria to implementation
- **Speckit**: Compare `tasks.md` to actual commits
- **DAC**: Check sub-branch completion status
- **Code**: Look for TODOs, FIXMEs, incomplete implementations, missing tests
- **Tests**: Check for corresponding test coverage

#### If Unclear: ASK
> "I found `AuthenticationMiddleware.cs` with partial implementation. Is this:
> 1) Complete (just needs review)
> 2) Partial (still in progress)
> 3) Not sure / need more context"

### Phase 5: Output Generation

#### Output Location

Determine output location based on project type:

1. **DAC project**: Place map output in the DAC workspace
   ```bash
   # If .dac/<workstream>/ exists, create map there
   mkdir -p .dac/<workstream>/map/
   # Output: .dac/<workstream>/map/map.md and map.upstream.md
   ```

2. **Speckit project**: Place map output alongside the feature spec
   ```bash
   # If specs/<feature>/ exists, create map there
   mkdir -p specs/<feature>/map/
   # Output: specs/<feature>/map/map.md and map.upstream.md
   ```

3. **Default (ticket-driven, utility, main-history)**: Use standard `.data/` location
   ```bash
   # Output: .data/map-YY-MM-DD-a/map.md and map.upstream.md
   ```

#### File 1: map.md (Rich Context)

```markdown
# Work Map: [branch-name]

## Context
- **Branch**: `[name]` (diverged from `[parent]` [N] commits ago, [N] commits ahead)
- **Ticket**: [PD-12345](https://degreedjira.atlassian.net/browse/PD-12345) — [title] `[status]`
  - Parent: [Epic link] (if exists)
  - Related: [sibling links] (if exists)
- **Project Type**: [DAC / Speckit / Ticket-driven / Utility]
- **DAC Context** (if DAC):
  - Workstream: [workstream-id] (from `.dac/<workstream>/00-control.md`)
  - Portion: [P-001] — [portion title] (from `.dac/<workstream>/portions/P-001.md`)
  - Status: [1 of 5 portions, 3 complete, 1 in progress, 1 not started]
  - Parent ticket: [link to parent Epic/Story]
  - Related portions: [links to sibling portion branches]
- **Speckit Context** (if Speckit):
  - Feature: [feature-name] (from `specs/<feature>/`)
  - Status: [spec ✅ | plan ✅ | tasks 🔶 | implementation ⬜]
  - Tasks: [12 of 15 complete] (from `specs/<feature>/tasks.md`)
  - Feature directory: [link to specs/<feature>/]

## Intent
[Derived from ticket description, commit messages, and code changes — 2-3 sentences summarizing the goal]

## Contributors (Code Components)
[Tree-structured list showing invocation sequence with layers]

Example:
- **ContentController** (Controller) — ✅ Complete — [trunk/Degreed.Web.vNext/Controllers/ContentController.cs:42](trunk/Degreed.Web.vNext/Controllers/ContentController.cs:42)
  - **ContentOrchestrator** (Orchestrator) — 🔶 Partial — [trunk/Degreed.Web.vNext/Orchestrators/ContentOrchestrator.cs:15](trunk/Degreed.Web.vNext/Orchestrators/ContentOrchestrator.cs:15)
    - **ContentService** (Service) — ✅ Complete — [trunk/Degreed.Core/Services/ContentService.cs:89](trunk/Degreed.Core/Services/ContentService.cs:89)
      - **ContentRepository** (Repository) — ✅ Complete — [trunk/Degreed.Data/Repositories/ContentRepository.cs:23](trunk/Degreed.Data/Repositories/ContentRepository.cs:23)
        - **Content_GetById** (SQL) — ⬜ Needed — [trunk/Degreed.SqlDb/dbo/Stored%20Procedures/Content_GetById.sql:1](trunk/Degreed.SqlDb/dbo/Stored%20Procedures/Content_GetById.sql:1)

[Use indentation to show call hierarchy — what calls what]

## Participants (People)
[Chronological list, most recent work highlighted]
- **[Author 1]**: [N] commits, most recent [date/time ago] — "[most recent commit message]"
- **[Author 2]**: [N] commits, most recent [date/time ago] — "[most recent commit message]"

## Sequence (Invocation Chain)
[High-level flow showing what needs to be in place for functionality]

Example:
1. **API Endpoint** (`POST /api/content`) → `ContentController.CreateContent`
2. **Orchestration** → `ContentOrchestrator.CreateContentAsync` (coordinates validation, creation, notification)
3. **Business Logic** → `ContentService.ValidateAndCreateAsync` (validation rules)
4. **Data Access** → `ContentRepository.InsertAsync` (EF Core)
5. **Database** → `Content_Insert` stored procedure (SQL)
6. **Messaging** → `ServiceBusPublisher.PublishAsync` (ContentCreated event)

[Focus on layers and dependencies, not every method call]

## Status Summary

### ✅ Complete
- [Component/file] — [brief note] — [file:line link]
- [Component/file] — [brief note] — [file:line link]

### 🔶 Partial
- [Component/file] — **Missing**: [what's incomplete] — [file:line link]
- [Component/file] — **TODO**: [what needs work] — [file:line link]

### ⬜ Needed
- [Component/file] — [why it's needed] — [reference/note]
- [Component/file] — [why it's needed] — [reference/note]

## Next Steps
[Actionable items derived from status analysis, prioritized]

1. [Action item with specific file/line references]
2. [Action item with specific file/line references]
3. [Action item with specific file/line references]

## Links
### Jira
- Primary: [PD-12345](link)
- Parent: [Epic link] (if exists)
- Related: [sibling links] (if exists)

### Git
- Branch: `[name]`
- Parent: `[parent branch]`
- Siblings: `[sibling branches]` (if DAC)
- Key commits: [commit links]

### Related Artifacts
- [Link to Speckit spec.md] (if exists)
- [Link to DAC artifacts] (if exists)
- [Link to other skill outputs] (if exists)

---
*Generated by `/map` on [timestamp]*
*Open [map.upstream.md](./map.upstream.md) in Upstream extension for quick navigation*
```

#### File 2: map.upstream.md (Concise Navigation)

This file follows the **Upstream Navigation Map Format** (see `references/UPSTREAM-FORMAT-SPEC.md`).

**Format Rules:**

1. **Link format**: `[<FilePath>:<LineNumber>](<FilePath>:<LineNumber>)`
   - Display text: `path:line` (one-based line number)
   - URL: `path:line` (IDE-style navigation, not GitHub `#L` format)
   - **CRITICAL**: Line numbers MUST be actual code locations, not default `:1`
   - The upstream viewer is for navigation - meaningless line numbers break its purpose
   
2. **Getting actual line numbers** (REQUIRED):
   - **Code search**: Use `search_graph(query, project)` - results include `start_line`
   - **Grep**: `grep -n "class ClassName" file.cs` - shows line numbers
   - **Read file**: Use Read tool and count to the class/method definition
   - **Only use `:1`** when the file doesn't exist on current branch OR truly cannot be located
   - For DAC portions on other branches: note "on branch X" instead of guessing `:1`
3. **Item format** (CODE ONLY):
   - **Use pipe format ONLY for code**: `Name | [link](url) | Layer`
   - Three pipe-delimited fields for code members:
     - Name: Class/method/procedure name (e.g., `ContentController.CreateContent`, `Users_Select`)
     - Link: Markdown link with ACTUAL line number from code search
     - Layer: Code type (Controller, Service, Repository, SP, Function, etc.)
   - **For documents/sections**: Use plain markdown links without pipes
     - Documents: `- [filename.md](path/to/file.md:line)` or `- [Section Name](path:line)`
     - Section headers: `## Section Name` (no pipes)
   - **Examples**:
     - CODE: `- ContentController.CreateContent | [Controllers/ContentController.cs:42](Controllers/ContentController.cs:42) | Controller`
     - DOCUMENT: `- [P-001.md](.dac/PD-112369/portions/P-001.md:15)` (no pipes)
     - SECTION: `## P-001: Bulk Upsert Stored Procedure` (no pipes)

4. **Hierarchy**: Use 2 spaces per nesting level

5. **Section headers**: `## <ID>: <Description>`
   - Use `## P-NNN:` for DAC portions
   - Use `## <Section name>` for other groupings

**Template:**

```markdown
# Upstream Navigation: [branch-name]

<!-- Generated by /map skill -->
<!-- Format: references/UPSTREAM-FORMAT-SPEC.md -->

## [Section]: [Component Group]

### [Layer Name]
- [ComponentName] | [[RelativePath]:[Line]]([RelativePath]:[Line]) | [Layer]
  - [ChildComponent] | [[RelativePath]:[Line]]([RelativePath]:[Line]) | [Layer]
    - [GrandchildComponent] | [[RelativePath]:[Line]]([RelativePath]:[Line]) | [Layer]

---

## End-to-End Flow

### 1. Entry Point
- [ControllerMethod] | [[Path]:[Line]]([Path]:[Line]) | Controller

### 2. Orchestration
- [OrchestratorMethod] | [[Path]:[Line]]([Path]:[Line]) | Orchestrator

### 3. Business Logic
- [ServiceMethod] | [[Path]:[Line]]([Path]:[Line]) | Service

### 4. Data Access
- [RepositoryMethod] | [[Path]:[Line]]([Path]:[Line]) | Repository
  - [StoredProcedure] | [[Path]:[Line]]([Path]:[Line]) | SQL
```

**Example:**

```markdown
# Upstream Navigation: feature/PD-123456-content-api

<!-- Generated by /map on 2026-08-26 -->
## Project Artifacts
### Documents (no pipes for documents)
- [spec.md](specs/content-api/spec.md:1)
- [plan.md](specs/content-api/plan.md:1)
- [P-001.md](.dac/PD-123456/portions/P-001.md:15)
---

## Content Creation Flow

### Controller Layer (pipe format for code)
- ContentController.CreateContent | [Controllers/ContentController.cs:42](Controllers/ContentController.cs:42) | Controller

### Orchestrator Layer
- ContentOrchestrator.CreateContentAsync | [Orchestrators/ContentOrchestrator.cs:15](Orchestrators/ContentOrchestrator.cs:15) | Orchestrator

### Service Layer
- ContentService.ValidateAndCreateAsync | [Services/ContentService.cs:89](Services/ContentService.cs:89) | Service

### Repository Layer
- ContentRepository.InsertAsync | [Repositories/ContentRepository.cs:23](Repositories/ContentRepository.cs:23) | Repository
  - Content_Insert | [SqlDb/Stored Procedures/Content_Insert.sql:8](SqlDb/Stored%20Procedures/Content_Insert.sql:8) | SP

---

## Status Summary

### ✅ Complete (code with pipes)
- ContentController.CreateContent | [Controllers/ContentController.cs:42](Controllers/ContentController.cs:42) | Controller
- ContentService.ValidateAndCreateAsync | [Services/ContentService.cs:89](Services/ContentService.cs:89) | Service

### 🔶 Partial
- ContentOrchestrator.CreateContentAsync | [Orchestrators/ContentOrchestrator.cs:15](Orchestrators/ContentOrchestrator.cs:15) | Orchestrator

### ⬜ Needed
- Content_Insert | [SqlDb/Stored Procedures/Content_Insert.sql:8](SqlDb/Stored%20Procedures/Content_Insert.sql:8) | SP
```

**Critical Format Requirements:**

- ✅ **DO** use pipe-delimited format for CODE ONLY: `Name | [link](url) | Layer`
- ✅ **DO** use plain markdown links for documents/sections: `[doc.md](path:line)` (no pipes)
- ✅ **DO** use link format: `[path:line](path:line)` with ACTUAL line numbers from code search
- ✅ **DO** use 2 spaces per indent level
- ✅ **DO** use relative paths from repository root
- ✅ **DO** URL-encode paths with spaces (e.g., `Stored%20Procedures`)
- ✅ **DO** get actual line numbers via `search_graph`, `grep -n`, or Read tool
- ❌ **DON'T** use pipe format for document/section references — only for code
- ❌ **DON'T** use parentheses for layers like `(Controller)` — use pipe format
- ❌ **DON'T** use square brackets for links in display text `[path:line]` — that should be `path:line`
- ❌ **DON'T** forget the third pipe field (Layer) for code items — it's required
- ❌ **DON'T** default all line numbers to `:1` — meaningless for navigation

### Phase 6: Output Delivery

After generating both files:
1. Write to `.data/map-YYYY-MM-DD-a/map.md`
2. Write to `.data/map-YYYY-MM-DD-a/map.upstream.md`
3. Report to user:

```
Work map generated for branch `[name]`.

📄 Rich context: .data/map-YYYY-MM-DD-a/map.md
🔗 Quick nav: .data/map-YYYY-MM-DD-a/map.upstream.md

**Summary**: [one-line summary of status — e.g., "3 components complete, 2 partial, 1 needed"]
**Next step**: [most immediate action item]
```

## Rules and Constraints

### Mutation Boundaries
- **NEVER** modify code, git state, Jira tickets, or any artifacts
- **READ-ONLY** operation — this is pure analysis and navigation generation

### Interaction Style
- Run inline, pause for clarification when needed
- Keep prompts concise (max 4 options)
- Default to reasonable choices, but ask when ambiguous

### Path Resolution

All file paths in both `map.md` and `map.upstream.md` MUST be relative — never absolute.

**Determine the path root (in order of precedence):**
1. **Git repo detected**: Use `git rev-parse --show-toplevel` as the root. All paths are relative to the repo root.
2. **Multi-folder workspace, no git**: Use the workspace folder that contains the file as the root. Each file's path is relative to its own workspace folder root.
3. **Single folder, no git**: Use the current working directory as the root.

```bash
# Step 1: Try git
PATH_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$PATH_ROOT" ]; then
  # Step 2/3: Fall back to workspace root or cwd
  PATH_ROOT=$(pwd)
fi
```

**Applying path resolution:**
- When writing links in both output files, strip the `PATH_ROOT` prefix from every absolute path to produce a relative path.
- Example: if repo root is `/home/user/project` and a file is at `/home/user/project/src/Controllers/FooController.cs`, the link path is `src/Controllers/FooController.cs`.
- On Windows, normalize backslashes to forward slashes in link paths.
- URL-encode spaces in paths (e.g., `Stored%20Procedures`).

### Link Format
- **Code**: `[relative-path]:[line]` — relative to the resolved path root (see Path Resolution above)
- **Jira**: `https://degreedjira.atlassian.net/browse/[ticket]`
- **Git**: Use commit SHAs, branch names

### Evidence Quality
- **Distinguish facts from inference**: "3 commits by Alice (fact), likely implementing auth (inference based on commit messages)"
- **Note uncertainty**: "Status unclear — no tests found, TODO present — asking user"
- **Cite sources**: "From PD-12345 acceptance criteria" vs. "From commit message" vs. "From code analysis"

### Tool Usage Efficiency
- Use `git log --oneline` over full log for initial scan
- Use `search_graph` for quick lookups, `trace_path` for call chains
- Batch Jira queries (get issue + links in one call if possible)
- Don't re-read files you've already analyzed

### Consistent with /umm Suite
- Use same visual conventions (✅ 🔶 ⬜ status indicators)
- Follow same output directory structure (`.data/[skill]-YYYY-MM-DD-a/`)
- Use same reference format (if shared references exist)
- Maintain same tone (professional, evidence-based, actionable)

## Error Handling

### Jira Not Available
If Jira MCP fails or ticket not found:
- Note the ticket ID extraction attempt in output
- Continue with git and code evidence only
- Include placeholder in output: "Ticket [PD-12345] could not be accessed — ensure Jira OAuth is configured"

### Code Indexing Not Available
If code-indexing MCP fails:
- Fall back to `grep`, `find`, manual file reading
- Note reduced call-chain analysis capability
- Still produce output with available evidence

### No Clear Context
If branch is ambiguous (no ticket, no DAC, no Speckit, no commits):
- Ask user: "No clear context detected. What are you working on?"
- Adjust analysis based on user response

### Empty Branch
If branch has no commits beyond parent:
- Report: "Branch `[name]` has no commits yet. Nothing to map."
- Offer: "Would you like to map the parent branch `[parent]` instead?"

## References

### Upstream Document Format
[To be added: reference to specification in separate repo]

### Related Skills
- **nix** — Explain/analyze workspace (broader scope, exploratory)
- **wiz** — Review work against intent (evaluative, quality-focused)
- **kit** — Reconstruct Speckit project status (Speckit-specific recovery)
- **fix** — Diagnose bugs through hypothesis triage (problem-focused)
- **dac** — Coordinate Jira-backed feature delivery (orchestration)

**map** complements these by providing **navigable task resumption** — "Here's where we are, here's what's done, here's what's next, here are the links to get there."

---

## Example Invocations

### Simple ticket-driven branch
```
User: /map
Assistant: [detects PD-112369 from branch name, fetches Jira, analyzes 8 commits, traces code changes, generates map.md + map.upstream.md]
```

### DAC project with siblings
```
User: /map
Assistant: "This branch is 1 of 4 in a DAC set (2 complete, 1 in progress). Analyze: 1) Only this branch 2) This + incomplete 3) All?"
User: 2
Assistant: [analyzes current + 1 incomplete sibling, generates map.md with cross-branch context]
```

### Speckit project
```
User: /map
Assistant: [detects spec.md/plan.md/tasks.md, assesses Speckit completeness, matches tasks to commits, generates map.md with Speckit status]
```

### Main branch history
```
User: /map
Assistant: "On main branch. Analyze: 1) Last 10 commits 2) Last 24 hours 3) Last week?"
User: 2
Assistant: [analyzes last 24 hours of commits, generates map.md with recent activity overview]
```

---

**Ready to map the codebase journey. 🗺️**
