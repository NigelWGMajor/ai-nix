# DORA Rebuild - Implementation Readiness Review

**Review Date:** 2026-08-28  
**Reviewer:** Analysis of DORA-Rebuild-Prompt.md  
**Status:** NEEDS CLARIFICATION - Multiple blocking issues identified

---

## Executive Summary

The specification is **70% implementation-ready**. The core model (observation-realm, relationship-layer) is clear and well-defined, but **critical implementation details are missing** that would block a developer from building the skill without making assumptions.

### Readiness Score by Section:
- ✅ **READY (90%+):** Core Principles, ID Generation, Realm/Layer Model, Info Field Structures
- ⚠️ **NEEDS WORK (60-90%):** MCP Integration, Discovery Workflows, Query Patterns
- ❌ **BLOCKING (0-60%):** Database Selection UX, Fuzzy Matching, Scope Management, Error Handling

---

## Critical Blockers (Must Fix Before Implementation)

### 1. Database Selection Mechanism Underspecified ⛔
**Lines:** 112-132, 262-264

**Issue:** 
- How does the skill list databases? MCP tool? File system command?
- What if `~/.claude/dora/` doesn't exist?
- Cross-platform path handling not addressed
- What if no databases exist yet?

**Impact:** Cannot implement `/dora` command without this.

**Fix Needed:**
```yaml
Specify:
1. Does dora-mcp provide `list_databases()` tool? Or use Bash `ls ~/.claude/dora/*.db`?
2. Initial state when directory is empty - auto-create first database? Prompt for name?
3. Database selection UX:
   - Interactive prompt with numbered list?
   - Free-text entry?
   - Default database mechanism?
4. Error handling if directory is not accessible
```

---

### 2. Layer Discovery Workflows Lack Implementation Steps ⛔
**Lines:** 144-184

**Issue:**
Each layer describes WHAT to discover but not HOW. Current text:
- "Find navigation entry points" - how?
- "Trace function/service calls" - how?
- "Map entity relationships" - how?

**Impact:** Implementer must guess which tools/techniques to use.

**Fix Needed:**
Add concrete workflow steps for each layer:

```markdown
**Browse Discovery - Concrete Steps:**
1. Use codebase-memory-mcp search_graph(label="Route") to find route definitions
2. Use Grep "route|router" in framework config files  
3. For each route found:
   - Create UI realm observation: ui.{route-path}
   - Find handler method via route config
   - Create Code realm observation for handler
   - Link via Browse layer: route → handler
4. Use Grep "data-dgat" to find UI element attributes
5. Create UI observations for interactive elements
6. Link to handlers via Browse layer

**CodePath Discovery - Concrete Steps:**
1. Use codebase-memory-mcp trace_path(function, mode=calls) for call chains
2. For each function in chain:
   - Create Code realm observation with qualified name
   - Extract file path, line number for info field
   - Create CodePath link: caller → callee
3. Handle cross-service calls:
   - Identify HTTP clients, gRPC calls
   - Create Infra observations for external services
   - Link via CodePath layer

[Similar detail for all layers]
```

---

### 3. Fuzzy Matching Algorithm Not Defined ⛔
**Lines:** 193-197, 268

**Issue:**
"Fuzzy matching" mentioned but no specification:
- What similarity metric?
- What threshold determines a match?
- What if multiple candidates match?
- Which info fields are compared?

**Impact:** Cannot implement duplicate prevention without this.

**Fix Needed:**
```markdown
**Fuzzy Matching Specification:**

When calling `candidates(realm, info, limit)`:

1. **Matching Strategy by Realm:**
   - **Code realm:** Match on qualifiedName (exact) or filePath+lineNumber (proximity)
   - **UI realm:** Match on data-dgat (exact) or route+elementType (fuzzy)
   - **Data realm:** Match on tableName.fieldName (exact)
   - **Security realm:** Match on type+name (exact)
   - **Config realm:** Match on namespace+key (exact)
   - **Glossary realm:** Match on domain+concept (semantic similarity)

2. **Decision Logic:**
   - If 1 exact match → reuse automatically
   - If 1 fuzzy match with confidence > 0.8 → reuse automatically
   - If multiple matches → present to AI for disambiguation, include match reasons
   - If no matches → create new observation

3. **Fallback:** If uncertain, create new and rely on human review to merge later
```

---

### 4. Scope Parameter Missing for Discovery Commands ⛔
**Lines:** 239, 462-478

**Issue:**
Commands like `/dora-codepaths` and `/dora-fulltest` don't specify scope:
- Entire codebase? (could be thousands of observations)
- User must specify starting point?
- Use conversation context?

**Impact:** Unbounded discovery could overwhelm the graph.

**Fix Needed:**
```markdown
**Scope Specification:**

All `/dora-<layer>` commands accept optional scope parameter:

Usage:
- `/dora-codepaths` - Uses conversation context (current file or recent discussion)
- `/dora-codepaths ProfileController` - Scopes to ProfileController class
- `/dora-codepaths profile photo upload` - Scopes to features matching keywords
- `/dora-fulltest --scope="profile management"` - Full discovery within scope

Scope Resolution:
1. Explicit scope parameter → use as-is
2. No parameter + conversation context → infer from recent files/functions discussed
3. No parameter + no context → ERROR: "Please specify scope or discuss code first"

Default depth limits:
- CodePath traversal: max 3 levels deep
- Browse discovery: max 50 UI elements per page
- DataPath: max 10 tables unless explicitly requested
```

---

### 5. "Exploration Tools" Never Defined ⛔
**Lines:** 223, 280, 414, 456

**Issue:**
Repeated references to "exploration tools" but never specified which tools.

**Fix Needed:**
```markdown
**Exploration Tools Reference:**

The skill uses the following tools for evidence gathering:

**Code Exploration:**
- `codebase-memory-mcp` (search_graph, trace_path, get_code_snippet)
- `Grep` (pattern matching across files)
- `Glob` (file discovery)
- `Read` (file content inspection)

**Graph Exploration:**
- `dora-mcp` (candidates, traverse, read)

**Per-Layer Tool Mapping:**
- **Browse:** Grep for routes, Read route config files, codebase search for UI components
- **CodePath:** codebase trace_path, Grep for class/method definitions
- **DataPath:** Grep for SQL, Read schema files, codebase search for entity models
- **EffectPath:** Grep for "LaunchDarkly|GetSetting", Read feature flag configs
- **Flow:** Combine Browse + CodePath + DataPath traversal
- **Abstract:** Manual/AI-driven domain analysis from code structure
```

---

## High-Priority Issues (Should Fix Before Implementation)

### 6. MCP Function Return Types Missing ⚠️
**Lines:** 84-90

**Issue:** Tool signatures shown but not return structures.

**Fix Needed:**
```markdown
Add to Technical Specifications:

**MCP Function Signatures:**

`candidates(realm: str, info: dict, limit: int) -> list[Candidate]`
```json
// Response structure:
[
  {
    "id": "code.profile.service.get",
    "realm": "code",
    "strength": 0.7,
    "info": { "qualifiedName": "...", ... },
    "match_score": 0.85,
    "match_reason": "Exact qualifiedName match"
  }
]
```

`traverse(id: str, direction: str, depth: int, layers: list[str]) -> Subgraph`
```json
{
  "observations": [ { "id": "...", "realm": "...", ... } ],
  "links": [ { "source": "...", "target": "...", "layer": "...", "strength": ... } ]
}
```

[Similar for read(), status()]
```

---

### 7. Info Field Structures Incomplete ⚠️
**Lines:** 365-407

**Issue:** Missing info structures for Security, Glossary, Infra realms.

**Fix Needed:**
```json
**Security Observations:**
{
  "type": "ld|orgsettings|permission|role",
  "name": "feature_flag_name",
  "description": "Human-readable description",
  "defaultValue": true,
  "scope": "organization|user|global"
}

**Glossary Observations:**
{
  "domain": "profile",
  "concept": "visibility",
  "definition": "User's control over who can view their profile",
  "relatedTerms": ["privacy", "permissions"]
}

**Infra Observations:**
{
  "type": "queue|service|deployment",
  "name": "profile_updates",
  "endpoint": "https://queue.internal/profile",
  "technology": "RabbitMQ|Kafka|HTTP"
}
```

---

### 8. Duplicate FR-1 and FR-2 ⚠️
**Lines:** 105-132

**Issue:** FR-1 and FR-2 describe identical functionality.

**Fix:** Merge into single FR-1: "Database Selection and Connection Management"

---

### 9. ID Generation for Method Overloads Unclear ⚠️
**Line:** 320

**Issue:** `{signature-hash}` mentioned but not defined.

**Fix:**
```markdown
**Code Realm - Method Overloads:**
When multiple methods have same name, append parameter type signature:

Examples:
- `code.profile.service.get.user_id` (takes userId parameter)
- `code.profile.service.get.email` (takes email parameter)
- `code.profile.service.get.void` (no parameters)

For complex signatures, use hash of parameter types:
- `code.profile.service.save.a1b2c3` (hash of param types)

Info field must include full signature for human reference.
```

---

### 10. EffectPath "Control Service" Format Inconsistent ⚠️
**Lines:** 545

**Issue:** `config.service.launchdarkly.client` doesn't match Config realm format `config.{namespace}.{setting-name}`.

**Fix:**
```markdown
**Control Services should use Code realm, not Config realm:**

Control services (LD clients, settings providers) are code constructs:
- `code.launchdarkly.client` (the LD SDK client class)
- `code.orgsettings.provider` (org settings service)

Feature flags use Security realm:
- `security.ld.new_profile_ui` (the flag itself)

Settings use Config realm:
- `config.app.max_upload_size` (the setting itself)

EffectPath links:
- Code observation → Security/Config observation (code uses flag/setting)
- Security/Config observation → Code observation (flag/setting affects code path)
```

---

## Medium-Priority Issues (Nice to Have)

### 11. Combined Gates Implementation Not Specified 📋
**Line:** 554

**Recommendation:**
```markdown
**Modeling Complex Conditions:**

For AND conditions:
- Create multiple EffectPath links from same source to multiple conditions
- Add to link info: `{ "operator": "AND" }`

For OR conditions:  
- Create multiple EffectPath links with info: `{ "operator": "OR" }`

For negation:
- Add to link info: `{ "negated": true }`

Example: `if (flagA && !flagB)`
- Link: behavior → flagA { "operator": "AND", "negated": false }
- Link: behavior → flagB { "operator": "AND", "negated": true }
```

---

### 12. Query Result Format Not Specified 📋
**Lines:** 452-460

**Recommendation:**
```markdown
**Query Response Format:**

Return markdown with:
1. Summary answer (2-3 sentences)
2. Evidence section with links to observations
3. Graph visualization (optional, if small subgraph)

Example:
```
## Answer
Profile visibility is controlled by 3 settings: privacy_mode, profile_public, and LD flag show_profile.

## Evidence
- `security.orgsettings.privacy_mode` → affects `code.profile.controller.get:42`
- `security.ld.show_profile` → affects `ui.profile.page:15`

## Graph
[Mermaid diagram or link to graph view]
```
```

---

### 13. Cross-Realm Flow Links Underspecified 📋
**Line:** 178

**Recommendation:**
```markdown
**Flow Layer Cross-Realm Links:**

Create discrete links for each transition:
1. UI button → Code handler (Flow layer)
2. Code handler → Data query (Flow layer)  
3. Data query → Code response (Flow layer)
4. Code response → UI update (Flow layer)

Each link should have temporal info:
```json
{
  "step": 1,
  "trigger": "user click",
  "transition": "invocation"
}
```
```

---

### 14. Error Handling Cases Not Enumerated 📋

**Recommendation:** Add Error Handling section:
```markdown
## Error Handling

**MCP Connection Failures:**
- Retry connection 3 times with exponential backoff
- If fails, report: "Cannot connect to dora-mcp server. Ensure MCP server is running."

**Database Not Found:**
- If user selects non-existent DB: "Database '{name}' not found. Create it? [Y/n]"

**Invalid Observation ID:**
- If ID doesn't match realm format: ERROR with format guidance
- Suggest correct format based on realm

**Orphaned Links:**
- If link references non-existent observation: WARNING, skip link creation
- Log for later cleanup

**Scope Too Large:**
- If discovery would create >500 observations: WARNING
- Suggest narrowing scope or confirm to proceed
```

---

### 15. Observation Granularity Guidance Missing 📋

**Recommendation:**
```markdown
## Observation Granularity Guidelines

**Code Realm:**
- Create observations for: public APIs, service methods, controllers, exported functions
- Skip: private helpers unless referenced externally, trivial getters/setters
- Threshold: Method complexity >5 lines or has external callers

**UI Realm:**
- Create observations for: interactive elements (buttons, inputs, links, forms)
- Skip: static text, decorative elements, internal DOM structure
- Threshold: Has event handler or user interaction

**Data Realm:**
- Create observations for: tables, views, stored procedures
- Optionally: frequently-accessed columns (not all columns)
- Threshold: Used in queries discovered during CodePath/DataPath discovery

**Config/Security Realm:**
- Create observations for: settings/flags actually checked in code
- Skip: Default framework configs unless customized
```

---

### 16. No Session State Management Spec 📋

**Recommendation:**
```markdown
## Session State Management

**Database Connection Persistence:**
- Connection is session-scoped (persists across skill invocations in same conversation)
- Stored in conversation context variable: `dora_active_database`
- On skill load: check if `dora_active_database` exists → reconnect, else prompt

**Switching Databases:**
- `/dora --switch` → disconnect current, prompt for new selection
- `/dora --db=profile` → connect to specific database by name

**Connection Timeout:**
- If MCP connection idle >30 minutes → may need reconnection
- Auto-reconnect on first use, transparent to user
```

---

## Minor Issues (Polish)

### 17. Terminology Inconsistency
- Line 96: "Focus concept" should be "Database selection"
- Line 487: "Focus-based scoping" in PRESERVE section should be removed
- Line 617: "Handle graph name derivation" should be "Handle database selection"
- Line 641: "Sequential perspective runs" should be "Sequential layer runs"

### 18. Missing Worked Example
**Recommendation:** Add appendix with complete end-to-end example showing:
- User invokes `/dora-browse`
- Skill searches for routes via Grep
- Creates UI observation with full JSON
- Creates Code observation for handler
- Creates Browse layer link with MCP calls
- Shows actual MCP tool invocations with responses

### 19. Reference Layer Still Vague
**Line 180-184:** Needs clarity on when/how References are added vs. discovered.

### 20. Abstract Layer Needs Concrete Examples
**Line 144-148:** Needs examples of what triggers Glossary observation creation.

---

## Recommendations for Next Steps

### Immediate (Blocking):
1. ✅ Define database listing mechanism and UX flow
2. ✅ Specify fuzzy matching algorithm and thresholds
3. ✅ Add concrete workflow steps for each layer discovery
4. ✅ Define scope parameter for all discovery commands
5. ✅ Document "exploration tools" explicitly

### High Priority:
6. ✅ Add MCP function return type specifications
7. ✅ Complete info field structures (Security, Glossary, Infra)
8. ✅ Merge duplicate FR-1/FR-2
9. ✅ Clarify method overload ID generation
10. ✅ Fix EffectPath control service realm assignment

### Medium Priority:
11. ✅ Specify combined gates implementation
12. ✅ Define query result format
13. ✅ Add error handling section
14. ✅ Add observation granularity guidelines

### Polish:
15. ✅ Fix terminology inconsistencies
16. ✅ Add complete worked example
17. ✅ Add session state management section

---

## Conclusion

**Current State:** Specification has strong conceptual foundation but lacks implementation details.

**Readiness Assessment:**
- **Can start implementation?** Yes, for core architecture (MCP connection, basic observe/link)
- **Can complete implementation?** No, without resolving blockers 1-5
- **Estimated rework needed:** 20-30% of spec needs additions/clarifications

**Recommendation:** Address Critical Blockers (1-5) before beginning layer discovery implementation. Core infrastructure can be built in parallel.

**Timeline Impact:** Resolving these issues will add 2-3 days to spec refinement but will save 1-2 weeks of implementation confusion and rework.
