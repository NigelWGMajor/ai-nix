---
name: dora
description: Discover and maintain a persistent graph of codebase observations and relationships through dora-mcp. Use for query-driven system discovery, tracing, debugging, and onboarding.
---

# DORA - Discovery Observation-Relationship Architecture

**Phase:** 1 - Core Scaffolding  
**Status:** In Development  
**Version:** 0.1.0

## Description

Query-driven system discovery that builds a persistent, navigable cache of observations and relationships via the dora-mcp server.

DORA captures your exploration work (code tracing, debugging, onboarding) as a graph of observations (code elements, UI components, data entities, settings) connected by relationships (calls, navigates to, accesses, controls). Each query extends the graph, making subsequent queries faster and more comprehensive.

## Triggers

- `/dora` - Status and database management
- `/dora-query <question>` - Query-driven discovery with graph capture

## Commands

### `/dora`
Show current DORA status and manage databases.

**Usage:**
```
/dora                    # Show status and graph statistics
/dora --switch          # Switch to different database
```

**First Time:**
If no database is connected, lists available databases from `~/.claude/dora/` and prompts for selection or new database name.

**Output:**
- MCP connection status
- Active database name
- Graph statistics (observation count by realm, relationship count by layer)

---

### `/dora-query <question>`
Ask a question about the codebase. DORA will explore code, capture discoveries, and return an answer with references.

**Usage:**
```
/dora-query How does profile photo upload work?
/dora-query What settings affect profile visibility?
/dora-query Show me the data flow for user search
/dora-query What calls the ProfileController?
```

**How it works:**
1. Searches existing graph for relevant observations
2. If incomplete, explores codebase using Grep, Read, codebase-memory-mcp
3. Creates observations (UI, Code, Data, Security, Config elements)
4. Creates links showing relationships (Browse, CodePath, DataPath, EffectPath, Flow)
5. Returns answer with observation references
6. Graph grows incrementally - subsequent queries build on prior discoveries

**Output:**
- Answer to question (2-5 sentences)
- Evidence from code exploration
- References to observations created/reused (e.g., `code.profile.controller.upload:42`)
- Related observations in graph

---

## Core Concepts

### Observation
A discovered system element with:
- **Realm:** Type of element (UI, Code, Data, Security, Config, Glossary, Infra)
- **ID:** Unique, deterministic identifier (e.g., `code.profile.service.get.photo`)
- **Strength:** Confidence value (0.0-1.0, default 0.5)
- **Info:** Metadata (file path, line number, signature, etc.)

### Relationship (Link)
A connection between observations with:
- **Source → Target:** Directional relationship
- **Layer:** Type of relationship (Abstract, Browse, CodePath, DataPath, EffectPath, Flow, Reference)
- **Strength:** Confidence in the relationship

### Realms (7)
- **UI:** Visual elements, pages, buttons, menus, inputs
- **Code:** Classes, functions, modules, services, APIs
- **Data:** Tables, entities, schemas, fields, queries
- **Security:** Permissions, roles, auth mechanisms, feature flags
- **Config:** Settings, feature toggles, environment configs
- **Glossary:** Business terms, domain concepts
- **Infra:** Servers, queues, pipelines, deployments

### Layers (7)
- **Abstract:** Conceptual groupings, domain boundaries
- **Browse:** Navigation, UI exposure, entry points
- **CodePath:** Implementation calls, service dependencies
- **DataPath:** Entity boundaries, data flow, ownership
- **EffectPath:** Conditions, flags, settings that gate behavior
- **Flow:** Trigger-to-outcome sequences, user journeys
- **Reference:** Supporting documentation, external links

---

## Example Session

```
User: /dora
DORA: No database connected. Available databases:
      1. degreed-profile
      2. degreed-skills
      Enter number or new database name:

User: 1
DORA: Connected to degreed-profile
      Observations: 42 (Code: 25, UI: 10, Data: 7)
      Relationships: 38 (CodePath: 20, Browse: 12, DataPath: 6)

User: /dora-query How does profile photo upload work?
DORA: Exploring codebase...
      
      ## Answer
      Profile photo upload is handled by a UI button that triggers 
      ProfileController.UploadPhoto, which validates the file and calls 
      StorageService.SaveProfilePhoto to persist to blob storage.
      
      ## Discoveries
      Created observations:
      - ui.profile.photo.upload.button (UI realm)
      - code.profile.controller.upload.photo (Code realm)
      - code.storage.service.save.profile.photo (Code realm)
      - infra.blob.profile_photos (Infra realm)
      
      Created links:
      - ui.profile.photo.upload.button → code.profile.controller.upload.photo (Browse layer)
      - code.profile.controller.upload.photo → code.storage.service.save.profile.photo (CodePath layer)
      - code.storage.service.save.profile.photo → infra.blob.profile_photos (Infra layer)

User: /dora-query What validates the uploaded file?
DORA: Building on prior discoveries...
      
      ## Answer
      File validation is handled by FileValidator.ValidateImage which checks
      file size, type, and dimensions before upload proceeds.
      
      ## Evidence
      Found in code.profile.controller.upload.photo:42
      Calls code.file.validator.validate.image before storage
      
      Created observations:
      - code.file.validator.validate.image (Code realm)
      
      Created links:
      - code.profile.controller.upload.photo → code.file.validator.validate.image (CodePath layer)
      
      [Notice: Reused code.profile.controller.upload.photo from previous query]
```

---

## Architecture

### Storage
All observations and relationships stored in SQLite via **dora-mcp** server:
- Location: `~/.claude/dora/{database-name}.db`
- Multiple databases supported (separate contexts/projects)
- Persistent across sessions

### Discovery Flow
```
User Query
    ↓
Search Graph (candidates)
    ↓
[If incomplete] Explore Codebase (Grep, Read, codebase-mcp)
    ↓
Create Observations (realm-specific IDs)
    ↓
Create Links (layer-specific relationships)
    ↓
Return Answer + References
```

### Observation ID Format

| Realm | Format | Example |
|-------|--------|---------|
| UI | `ui.{data-dgat}` or `ui.{route}.{element}` | `ui.profile.photo.upload.button` |
| Code | `code.{namespace}.{class}.{member}` | `code.profile.controller.upload.photo` |
| Data | `data.{schema}.{table}.{column}` | `data.dbo.users.profile_photo_url` |
| Security | `security.{type}.{name}` | `security.ld.show_profile_photo` |
| Config | `config.{namespace}.{setting}` | `config.app.max_photo_size` |
| Glossary | `glossary.{domain}.{concept}` | `glossary.profile.photo_management` |
| Infra | `infra.{type}.{name}` | `infra.blob.profile_photos` |

---

## Limitations (Phase 1)

### Not Yet Implemented (Phase 2)
- `/dora-browse` - Comprehensive UI/navigation discovery
- `/dora-codepaths` - Comprehensive call chain tracing
- `/dora-datapaths` - Comprehensive data flow mapping
- `/dora-effectpath` - Comprehensive condition/flag discovery
- `/dora-flows` - Comprehensive user journey tracing
- `/dora-abstract` - Domain concept mapping
- `/dora-fulltest` - Orchestrated multi-layer discovery

These will be built as sub-skills once Phase 1 core infrastructure is stable.

### Current Scope
Phase 1 focuses on **query-driven discovery** infrastructure:
- Database management
- Basic observation/link CRUD
- Candidate search and duplicate prevention
- Graph traversal
- Query-based exploration with capture

Goal: Prove that incremental, query-driven graph building is useful and viable.

---

## Technical Details

### Dependencies
- **dora-mcp** server (must be running and configured in Claude Code settings)
- **MCP tools:** connect, observe, link, candidates, traverse, read, status
- **Exploration tools:** Grep, Read, Glob, codebase-memory-mcp (optional)

### Session State
- Active database name stored in session context
- Connection persists across skill invocations within same conversation
- Auto-reconnect on stale connection

### Duplicate Prevention
Before creating observation:
1. Search candidates via MCP with realm + info
2. If high-confidence match found → reuse existing ID
3. If ambiguous → use AI judgment
4. If no match → create new observation

### Error Handling
- MCP server not running → helpful error message with setup guidance
- Database not found → prompt to create
- Invalid input → validation with format guidance
- Connection timeout → auto-retry with exponential backoff

---

## Development

### Implementation Status

**Completed:**
- [ ] Database listing and selection
- [ ] MCP connection management
- [ ] Observation CRUD (all realms)
- [ ] Link CRUD (all layers)
- [ ] Candidate search
- [ ] `/dora` status command
- [ ] `/dora-query` query-driven discovery
- [ ] Graph traversal integration
- [ ] Session persistence
- [ ] Error handling

**See:** `Phase1-Implementation-Checklist.md` for detailed task breakdown

### Testing
**See:** `Test-Scenarios.md` for validation scenarios

### References
- **Specification:** `DORA-Rebuild-Prompt.md`
- **Glossary:** `references/DORA-Glossary.md`
- **MCP API:** `references/dora-mcp.md` (if available)

---

## Future (Phase 2)

Once Phase 1 is stable and proven useful:
- Build layer-specific sub-skills for comprehensive automated discovery
- Implement `/dora-fulltest` for bootstrapping new codebases
- Add observation staleness detection and cleanup
- Add graph visualization
- Add graph export/import
- Add cross-database querying

---

## Support

**Issues:**
- MCP server not running: Check MCP server configuration in Claude Code settings
- Database access errors: Check `~/.claude/dora/` directory permissions
- Unexpected observations: File issue with example query and expected vs actual observations

**Questions:**
- See `references/DORA-Glossary.md` for terminology
- See `DORA-Rebuild-Prompt.md` for full specification
- Use `/dora-help` (future) for interactive help

---

**Last Updated:** 2026-08-28  
**Author:** DORA Team  
**License:** Internal Use
