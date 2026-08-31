# DORA Discovery Skill - Rebuild Specification

## Executive Summary

Build a Claude Code skill that enables iterative system discovery and knowledge persistence through an observation-perspective model, using the `dora-mcp` server for all persistence operations.

## Problem Statement

Software exploration work (debugging, onboarding, architecture analysis, testing) generates valuable understanding that is typically lost after each task completes. Future investigations repeat the same discovery work rather than building on prior effort.

The solution: a persistent Discovery Graph that captures observations and their relationships across multiple perspectives, allowing both human and AI collaborators to incrementally build and reuse system understanding.

## Core Principles

### 1. Discovery Graph as Reusable Memory

The Discovery Graph represents **the current best explanation consistent with observed evidence**, not definitive truth. It is expected to be:

- Incomplete
- Partially incorrect  
- Continuously evolving
- Built incrementally across sessions

### 2. Observation-Realm and Relationship-Layer Model

**Observations** are recognizable system elements, each bound to a single **Realm**:

| Realm | Observation Types |
|-------|------------------|
| **UI** | Visual elements, pages, buttons, menus, inputs |
| **Code** | Classes, functions, modules, services, APIs |
| **Data** | Tables, entities, schemas, fields, queries |
| **Security** | Permissions, roles, auth mechanisms |
| **Config** | Settings, flags, feature toggles, environment |
| **Glossary** | Business terms, domain concepts |
| **Infra** | Servers, queues, pipelines, deployments |

**Relationships** (called "links" in the MCP) connect observations and are categorized by **Layer** (perspective through which we view the relationship):

| Layer | Purpose |
|------------|---------|
| **Abstract** | Conceptual groupings, domain boundaries |
| **Browse** | Navigation, UI exposure, entry points |
| **CodePath** | Implementation calls, service dependencies |
| **DataPath** | Entity boundaries, data flow, ownership |
| **EffectPath** | Conditions, flags, settings that gate behavior |
| **Flow** | Trigger-to-outcome sequences, user journeys |
| **Reference** | Supporting documentation, external links |

### 3. Strength-Based Confidence

All observations and relationships have a **strength** value (0.0 to 1.0):
- 1.0 = confirmed, directly observed
- 0.5 = normal default for new discoveries
- 0.0 = invalid, triggers removal

When re-observing an entity, strengths merge via odds-ratio geometric mean, allowing gradual refinement over time.

### 4. Stable Identity

Observations use stable, semantic IDs following dot-path convention:
- `ui.settings.save.button`
- `code.user.service.get.profile`
- `data.users.email`
- `config.feature.new.dashboard`

IDs are immutable once created. Discovery work adds and refines, never renames.

## Architecture

### Storage Layer: dora-mcp Server

All persistence operations go through the `dora-mcp` MCP server. The skill NEVER manages files directly.

**Connection:**
```
mcp__dora-mcp__connect(name="<graph-name>")
```
Opens or creates a SQLite database at `~/.claude/dora/<name>.db`

**Core Operations:**

| Tool                                          | Purpose                    |
| --------------------------------------------- | -------------------------- |
| `observe(id, realm, strength, info)`          | Create/update observation  |
| `link(source_id, target_id, layer, strength)` | Create/update relationship |
| `candidates(realm, info, limit)`              | Search before creating     |
| `traverse(id, direction, depth, layers)`      | Walk the graph             |
| `read(ids)`                                   | Get observation details    |
| `status()`                                    | Connection state & stats   |

### Skill Architecture - Query-Driven Discovery

The skill provides **scaffolding for query-driven discovery** that builds a navigable cache:

1. **Database Management** - List, select, create databases via file system
2. **Query-Driven Exploration** - Answer questions by exploring code and capturing discoveries
3. **Observation Recording** - Create observations with appropriate realms as discoveries are made
4. **Relationship Mapping** - Link observations in appropriate layers based on discovered connections
5. **Graph Navigation** - Traverse existing discoveries to answer subsequent queries
6. **Discovery Capture** - Cache exploration paths for reuse

**Layer-specific discovery workflows** will be implemented as sub-skills/internal commands after core scaffolding is in place.

## Functional Requirements

### FR-1: Database Selection and Connection

**As a** user  
**I want to** work with named Discovery Graph databases  
**So that** I can maintain separate knowledge bases for different systems or scopes

**Acceptance Criteria:**
- On first operation, if no database connected, list available databases
- List databases using file system: `ls ~/.claude/dora/*.db` (via Bash tool)
- Present numbered list to user, allow selection or new database name entry
- Connect to selected/new database via `mcp__dora-mcp__connect(name)`
- Database name stored in session context (persists across skill invocations)
- `/dora` command reports current database and connection state
- `/dora --switch` allows switching databases mid-session

**Database Location:**
All databases stored at `~/.claude/dora/{database-name}.db` via dora-mcp server.

### FR-2: Query-Driven Discovery

**As a** user  
**I want to** ask questions and have discoveries automatically captured  
**So that** subsequent queries can build on prior exploration

**Acceptance Criteria:**
- User provides natural language query with context/guidance
- Skill uses available exploration tools (Grep, Read, codebase-memory-mcp, etc.)
- As evidence is discovered, create observations with appropriate realms
- As connections are discovered, create links with appropriate layers
- Return answer to query with references to observations created
- Graph grows incrementally with each query

**Example Query Flow:**
```
User: "How does profile photo upload work?"
Skill:
1. Searches code for "profile photo upload" patterns
2. Finds UI button → creates ui.profile.photo.upload.button observation
3. Finds handler method → creates code.profile.controller.upload.photo observation  
4. Links via Browse layer: button → handler
5. Finds storage service → creates code.storage.service.save observation
6. Links via CodePath layer: handler → storage service
7. Returns answer citing observations
```

**Layer-Specific Discovery Commands:**
Layer-specific workflows (Abstract, Browse, CodePath, DataPath, EffectPath, Flow) will be implemented as **sub-skills or internal commands** after core scaffolding is complete. These are deferred to Phase 2.

### FR-3: Duplicate Prevention

**As a** system  
**I want to** avoid creating duplicate observations  
**So that** the graph remains coherent and queryable

**Acceptance Criteria:**
- Before creating observation, call `candidates(realm, info)` to search for existing
- Matching strategy varies by realm and will be refined in sub-skills
- If candidate found with high confidence → reuse existing ID
- If ambiguous matches → use AI judgment to select best match or create new
- Update strength and merge info when reusing observation
- Default: prefer creating new observation over forcing incorrect match

**Basic Matching Heuristics:**
- **Code realm:** Match on qualifiedName (exact) or filePath+lineNumber (proximity)
- **UI realm:** Match on data-dgat attribute (exact) or route+selector (fuzzy)  
- **Data realm:** Match on schema.table.column (exact)
- **Config/Security realm:** Match on type+name (exact)

Detailed fuzzy matching algorithms will be defined in layer-specific sub-skills.

### FR-4: Strength Evolution

**As a** system  
**I want to** refine confidence over time  
**So that** repeated observations strengthen findings and contradictions surface

**Acceptance Criteria:**
- Default strength for new discoveries: **0.5**
- Use 1.0 only for explicitly verified/confirmed observations
- Use 0.0 to explicitly invalidate (triggers removal)
- MCP server handles strength merging automatically (see dora-mcp.md for formula)
- Re-observing with same strength reinforces confidence
- Typically 0.5 is sufficient for query-driven discovery

### FR-5: Graph Traversal & Query

**As a** user  
**I want to** navigate existing discoveries and extend them as needed  
**So that** queries can leverage prior work and expand the graph

**Acceptance Criteria:**
- `/dora-query <question>` first searches graph for relevant observations
- If graph has relevant observations → traverse to answer
- If graph is incomplete → explore codebase and capture new discoveries
- Combine graph traversal with fresh exploration for comprehensive answers
- Traversal directions:
  - **Downstream**: source → target (e.g., caller → callee in CodePath)
  - **Upstream**: target → source (e.g., incoming calls)
  - **Both**: bidirectional exploration
- Filter traversal by layers to focus on specific relationship types
- Return answer with references to observations (existing and newly created)

### FR-6: State Reporting

**As a** user  
**I want to** see current DORA state and graph statistics  
**So that** I understand what's been discovered and what context is active

**Acceptance Criteria:**
- `/dora` command shows:
  - MCP connection status
  - Active database name
  - Graph statistics (observation count by realm, relationship count by layer)
- If not connected, list available databases from `~/.claude/dora/`
- Provide guidance on how to get started

### FR-7: Session Persistence

**As a** system  
**I want to** maintain database connection across skill invocations  
**So that** users don't need to reconnect each time

**Acceptance Criteria:**
- Store active database name in session context variable
- On skill invocation, check if database connection exists
- If exists and healthy → reuse connection
- If stale or missing → reconnect to last-used database
- Provide `/dora --switch` to change databases mid-session
- Connection timeout: auto-reconnect transparently on first use after idle period

## Workflow Patterns

### Pattern 1: Starting New Investigation

```
1. User: /dora (no database connected)
2. Skill: Lists available databases, prompts for selection or new name
3. User: Selects "user-profile" or enters new name
4. Skill: Connects to database via dora-mcp
5. User: Investigate how profile photos are uploaded
6. Skill:
   - Searches candidates for existing "profile photo" observations (fuzzy match)
   - Creates/updates observations in appropriate realms (UI, Code, Data)
   - Discovers upload button (UI realm) → UploadPhoto endpoint (Code realm)
   - Links in Browse and CodePath layers
   - Returns findings with graph context
```

### Pattern 2: Building on Prior Work

```
1. User: /dora-query "What settings affect profile visibility?"
2. Skill:
   - Uses exploration tools to search codebase and graph
   - Traverses from "profile" observations
   - Filters to EffectPath layer
   - Returns subgraph showing conditions and effects
3. User: Also check LaunchDarkly flags
4. Skill:
   - Performs EffectPath discovery using code exploration
   - Searches for LD SDK calls in profile code (e.g., security.ld.* IDs)
   - Creates new Config realm observations for flags
   - Links to profile visibility behaviors in EffectPath layer
   - Updates strength on re-observed elements
```

### Pattern 3: Cross-Layer Analysis

```
1. User: /dora-fulltest
2. Skill runs sequential discovery across all layers:
   - Abstract: Maps "Profiles" domain concept (Glossary realm)
   - Browse: Finds /profile route and settings page (UI realm, Browse layer)
   - CodePath: Traces ProfileController → ProfileService → ProfileRepo (Code realm, CodePath layer)
   - DataPath: Maps Users table → Profile fields (Data realm, DataPath layer)
   - EffectPath: Finds privacy settings and LD flags (Config/Security realms, EffectPath layer)
   - Flow: Traces "View Profile" user journey (Flow layer across realms)
3. Result: Comprehensive multi-layer graph ready for querying
```

## Technical Specifications

### ID Generation

**Observation IDs must be unique and deterministic, with format varying by realm:**

**UI Realm:**
- Prefer `data-dgat` attribute values for active elements: `ui.{data-dgat-value}`
- If missing, use ancestor's `data-dgat` with suffix: `ui.{ancestor-dgat}.{qualifier}`
- Example: `ui.settings.save.button` or `ui.profile.menu.privacy.item`

**Code Realm:**
- Use fully qualified name: `code.{namespace}.{class}.{member}`
- Add qualifiers if needed for overloads: `code.{namespace}.{class}.{member}.{signature-hash}`
- Example: `code.profile.service.update.photo` or `code.degreed.user.profile.controller.get`

**Data Realm:**
- SQL: `data.{schema}.{table}.{column}` or `data.{schema}.{procedure}`
- Variables: `data.{namespace}.{variable}`
- Example: `data.dbo.users.profile_photo_url` or `data.dbo.sp_update_profile`

**Security Realm:**
- Format: `security.{type}.{name}`
- Types: `ld` (LaunchDarkly), `orgsettings` (Organization Settings), `permission`, `role`
- Use name as defined in code
- Example: `security.ld.new_profile_ui` or `security.orgsettings.privacy_mode`

**Config Realm:**
- Format: `config.{namespace}.{setting-name}`
- Use namespace to disambiguate
- Example: `config.feature.new_profile_ui` or `config.app.max_upload_size`

**Glossary Realm:**
- Use domain language with feature/operation chain
- Format: `glossary.{domain}.{concept}`
- Example: `glossary.profile.visibility` or `glossary.skills.recommendation`

**Infra Realm:**
- Use unique infrastructure identifiers based on names
- Format: `infra.{type}.{name}`
- Example: `infra.queue.profile_updates` or `infra.service.auth_api`

**Relationship IDs:**
Relationships are identified by the MCP server; the skill provides source_id, target_id, and layer when creating links.

### Realm and Layer Summary

**Realms** categorize observations (what kind of thing is being observed):
- UI, Code, Data, Security, Config, Glossary, Infra

**Layers** categorize relationships (what kind of connection exists between observations):
- Abstract, Browse, CodePath, DataPath, EffectPath, Flow, Reference

**Key Distinction:**
- An observation belongs to **one realm** (e.g., `code.profile.service.get` is in Code realm)
- A relationship exists on **one layer** (e.g., link from UI button to Code handler uses Browse layer)
- An observation can have relationships on **multiple layers** (e.g., a service may have CodePath links to callees and DataPath links to entities it accesses)

### Info Field Structure

The `info` dict in observations stores domain-specific payload:

**UI Observations:**
```json
{
  "elementType": "button|menu|page|input",
  "selector": "data-testid or CSS selector",
  "route": "/path/to/page",
  "parentComponent": "ui.parent.id"
}
```

**Code Observations:**
```json
{
  "qualifiedName": "Namespace.Class.Method",
  "filePath": "src/relative/path.cs",
  "lineNumber": 123,
  "signature": "method signature"
}
```

**Data Observations:**
```json
{
  "tableName": "Users",
  "fieldName": "profile_photo_url",
  "dataType": "varchar(255)",
  "nullable": false
}
```

**Config Observations:**
```json
{
  "key": "feature.new_profile_ui",
  "source": "LaunchDarkly|OrgSettings|AppConfig",
  "defaultValue": false,
  "scope": "organization|user"
}
```

### Workflow Protocol

**Every Discovery Operation:**
```
1. Check/establish MCP connection to database
2. Use exploration tools to gather evidence
3. Search candidates before creating (fuzzy match on realm + info)
4. Create observations with deterministic ID, appropriate realm & strength (default 0.5)
5. Link observations in appropriate layer(s) with source → target directionality
6. MCP handles strength merging on re-observed entities
7. Return findings with graph context
```

## Non-Functional Requirements

### NFR-1: Idempotency
Re-running discovery on same scope strengthens existing findings, doesn't duplicate

### NFR-2: Incremental
Each operation adds value; no requirement to complete all perspectives

### NFR-3: Read-Only by Default  
Skill never mutates code, only reads and records observations

### NFR-4: Evidence-Based
Only record what can be observed or reasonably inferred from code/config

### NFR-5: Uncertainty Tolerance
Record uncertain findings with lower strength rather than omitting

### NFR-6: Cross-Session Coherence
Graph usable across sessions, by different agents, with consistent interpretation

## Command Specification

### /dora
**Purpose:** Report DORA connection state and available databases  
**Output:**
- MCP connection status
- Connected database name (or prompt for selection if not connected)
- Graph statistics (observation count, relationship counts by layer)
- List of available databases in `~/.claude/dora/` if not connected

### /dora-query <question>
**Purpose:** Answer question by exploring graph and codebase, capturing discoveries  
**Arguments:** Natural language question with optional context/guidance  
**Process:**
1. Search graph for relevant existing observations using `candidates()`
2. If relevant observations found → traverse to gather evidence
3. If graph incomplete → use exploration tools (Grep, Read, codebase-memory-mcp) to discover
4. As discoveries are made → create observations and links in real-time
5. Return answer with references to observations (mix of existing and new)
6. Graph grows incrementally with each query

**Examples:**
- `/dora-query How does profile photo upload work?`
- `/dora-query What settings affect profile visibility?`
- `/dora-query Show me the data flow for user search`

### /dora --switch
**Purpose:** Switch to different database mid-session  
**Process:**
- Disconnect from current database
- List available databases
- Prompt for selection or new name
- Connect to selected database

---

## Future Commands (Phase 2 - Sub-Skills)

The following commands will be implemented as **sub-skills or internal commands** after core scaffolding:

### /dora-<layer> commands
- `/dora-browse` - Comprehensive UI/navigation discovery
- `/dora-codepaths` - Comprehensive call chain tracing  
- `/dora-datapaths` - Comprehensive data flow mapping
- `/dora-effectpath` - Comprehensive condition/flag discovery
- `/dora-flows` - Comprehensive user journey tracing
- `/dora-abstract` - Domain concept mapping

### /dora-fulltest
Orchestrated comprehensive discovery across all layers.

These will be specified and implemented separately once core query-driven infrastructure proves viable.

## Migration from Old System

### What to PRESERVE:
- ✅ Core observation-realm and relationship-layer model
- ✅ Stable semantic IDs (deterministic, realm-specific)
- ✅ Confidence/strength values (0.0-1.0)
- ✅ Incremental, query-driven discovery
- ✅ Duplicate prevention via search-before-create
- ✅ Cross-session/cross-agent coherence
- ✅ Graph as navigable cache for subsequent queries

### What to REPLACE:
- ❌ YAML file storage → MCP server persistence (SQLite)
- ❌ Canonicalization scripts → Server handles ordering
- ❌ Manual graph merging → Server handles updates
- ❌ File-based focus selection → Database selection via file listing
- ❌ `whenAdded`/`whenValidated` tracking → Server timestamps
- ❌ Pre-defined layer workflows → Query-driven discovery (Phase 1)
- ❌ Complex ID migration logic → Deterministic realm-based ID generation

### What to SIMPLIFY:
- Database selection - simple file listing via `ls`
- ID generation - deterministic realm-specific formats (no hashing needed for Phase 1)
- Discovery trigger - queries drive exploration, not pre-defined workflows
- Serialization - irrelevant with MCP server storage
- Relationship directionality - source → target is downstream
- Temporal tracking - server handles automatically
- Strength merging - MCP handles the math (default 0.5 for Phase 1)

## Success Criteria

### Discovery Quality
- [ ] Observations have appropriate realms and semantic IDs
- [ ] Relationships use correct layers
- [ ] Duplicate observations avoided through search
- [ ] Strength values reflect confidence appropriately
- [ ] Info fields contain relevant metadata

### Workflow Effectiveness  
- [ ] Database context provides appropriate scope
- [ ] Layer-specific workflows gather appropriate evidence
- [ ] Queries return relevant subgraphs using fuzzy matching
- [ ] Full discovery creates comprehensive multi-layer graph

### Persistence Reliability
- [ ] MCP connection established reliably
- [ ] Observations persist across sessions
- [ ] Strength merging works as expected
- [ ] Graph traversal returns accurate relationships

### Usability
- [ ] Commands are intuitive and discoverable
- [ ] State reporting is clear
- [ ] Error handling follows standard AI-prompt response patterns

## Implementation Notes

### EffectPath Special Requirements

EffectPath discovery requires comprehensive condition mapping:

1. **Control Service Inventory** - Before examining individual conditions:
   - Find Organization Settings providers/services/clients
   - Find LaunchDarkly SDK clients/wrappers
   - Map their DI registrations and call sites

2. **Service Observations** - Represent control services in **Config realm** with service metadata in info field (e.g., `config.service.launchdarkly.client`)

3. **Condition Observations** - Each setting/flag as **Security** or **Config** realm observation:
   - LaunchDarkly: `security.ld.{flag-name}`
   - Organization Settings: `security.orgsettings.{setting-name}`
   - App Config: `config.{namespace}.{setting-name}`

4. **Complete Chain Tracing** - Map: call site → control service → evaluation → decision → effect

5. **Combined Gates** - Accurately model AND/OR/negation in condition relationships using EffectPath links

6. **Coverage Passes** - Both provider-first (find all LD calls) and effect-first (work backward from UI elements)

### Query Pattern Examples

**"What settings affect X?"**
- Find X observation(s) using exploration tools and fuzzy search
- Traverse upstream in EffectPath layer (find conditions that control X)
- Return Config/Security realm observations linked via EffectPath

**"How does user get to Y?"**  
- Find Y observation (fuzzy search)
- Traverse upstream in Browse and Flow layers (find navigation path)
- Return UI observations showing entry points and journey

**"What calls Z?"**
- Find Z observation in Code realm
- Traverse upstream in CodePath layer (target → source)
- Return Code realm observations for calling functions

**"What data does W touch?"**
- Find W observation in Code realm
- Traverse DataPath layer (either direction)
- Return Data realm observations for accessed entities

## Skill Metadata

```yaml
---
name: dora
description: Query-driven system discovery that builds a persistent, navigable cache of observations and relationships via dora-mcp server
triggers:
  - /dora           # Status and database management
  - /dora-query     # Query-driven discovery with graph capture
phase: 1            # Core scaffolding only
future_commands:    # Phase 2 - sub-skills
  - /dora-browse
  - /dora-codepaths
  - /dora-datapaths
  - /dora-effectpath
  - /dora-flows
  - /dora-abstract
  - /dora-fulltest
---
```

## References

**Glossary:** See `references/DORA-Glossary.md` for definitions of all key terms

**MCP Protocol:** See `ref/dora-mcp.md` for complete dora-mcp server API

**Legacy Vision:** See `ref/Observation-Perspective Modeling Vision.md` for problem context

**Legacy Skill:** See `ref/observation-perspective-for-claude-skill.md` for prior implementation patterns (file-based)

---

## Building the Skill: Step-by-Step

### Phase 1: Core Scaffolding (Implementation Priority)

1. **Database Management**
   - List databases via `ls ~/.claude/dora/*.db`
   - Prompt for selection or new database name
   - Connect via `mcp__dora-mcp__connect(name)`
   - Store connection in session context
   - Implement `/dora` status command

2. **Basic Observation CRUD**
   - Implement `observe(id, realm, strength, info)` wrapper
   - Test creating observations in each realm
   - Implement deterministic ID generation per realm rules
   - Test info field population

3. **Basic Relationship CRUD**
   - Implement `link(source, target, layer, strength)` wrapper
   - Test creating links in each layer
   - Verify directionality (source → target)

4. **Candidate Search**
   - Implement `candidates(realm, info, limit)` wrapper
   - Test basic matching heuristics per realm
   - Use AI judgment for ambiguous matches
   - Prefer creating new over forcing bad match

5. **Query-Driven Discovery**
   - Implement `/dora-query` command
   - Search graph first via `candidates()`
   - If incomplete, use exploration tools (Grep, Read, codebase-memory-mcp)
   - Capture discoveries as observations/links in real-time
   - Return answer with observation references

6. **Graph Traversal**
   - Implement `traverse(id, direction, depth, layers)` wrapper
   - Test upstream/downstream/both traversal
   - Filter by layers
   - Integrate traversal into query responses

7. **Session Management**
   - Persist active database in session context
   - Auto-reconnect on skill invocation
   - Implement `/dora --switch` command
   - Handle connection errors gracefully

### Phase 2: Layer-Specific Sub-Skills (Deferred)

After Phase 1 proves viable:
- Build Browse discovery sub-skill
- Build CodePath discovery sub-skill
- Build DataPath discovery sub-skill
- Build EffectPath discovery sub-skill
- Build Flow discovery sub-skill
- Build Abstract discovery sub-skill
- Implement `/dora-fulltest` orchestration

---

## Implementation Scope

### Phase 1 Scope (This Specification)
Build **core scaffolding for query-driven discovery**:
- Database management (list, select, connect)
- Basic observation/link CRUD via MCP
- Query-driven exploration with discovery capture
- Graph traversal to answer queries
- Session persistence

**Goal:** Prove that query-driven discovery with persistent graph cache is viable and useful.

### Phase 2 Scope (Future Sub-Skills)
Build **layer-specific discovery workflows** as separate sub-skills:
- Comprehensive Browse discovery
- Comprehensive CodePath tracing
- Comprehensive DataPath mapping
- Comprehensive EffectPath condition discovery
- Comprehensive Flow journey tracing
- Abstract domain modeling
- `/dora-fulltest` orchestration

**Goal:** Automate comprehensive system discovery once core infrastructure proves viable.

---

## End of Specification

This document provides requirements for **Phase 1: Core Scaffolding** of the DORA discovery skill using the dora-mcp server for persistence. The focus is on building a queryable, navigable cache infrastructure that captures discoveries incrementally through natural query-driven exploration.
