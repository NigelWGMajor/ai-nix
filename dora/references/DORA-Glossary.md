# DORA Discovery Graph - Glossary

This glossary defines key terms and concepts used in the DORA (Discovery Observation-Relationship Architecture) system.

## Core Concepts

### Discovery Graph
A persistent knowledge base that captures system understanding through observations and their relationships. The graph represents the current best explanation consistent with observed evidence, expected to be incomplete, evolving, and built incrementally across sessions.

### Observation
A recognizable system element that has been discovered and recorded. Each observation:
- Belongs to exactly **one realm**
- Has a unique, deterministic **ID**
- Contains a **strength** value (0.0 to 1.0) indicating confidence
- Stores discovery metadata in an **info** field (JSON object)
- Can participate in relationships across **multiple layers**

### Realm
A categorization of observations by their type. Each observation belongs to exactly one realm:

| Realm | Description | Example IDs |
|-------|-------------|-------------|
| **UI** | Visual elements, pages, buttons, menus, inputs | `ui.settings.save.button` |
| **Code** | Classes, functions, modules, services, APIs | `code.profile.service.get` |
| **Data** | Tables, entities, schemas, fields, queries | `data.dbo.users.email` |
| **Security** | Permissions, roles, auth mechanisms, feature flags | `security.ld.new_profile` |
| **Config** | Settings, feature toggles, environment configs | `config.app.max_upload_size` |
| **Glossary** | Business terms, domain concepts | `glossary.profile.visibility` |
| **Infra** | Servers, queues, pipelines, deployments | `infra.queue.profile_updates` |

### Relationship (Link)
A connection between two observations, created via the MCP `link()` function. Each relationship:
- Connects a **source** observation to a **target** observation
- Exists on exactly **one layer**
- Has directionality: source → target is **downstream**, target → source is **upstream**
- Can have a **strength** value indicating confidence in the relationship

### Layer
A categorization of relationships by perspective. Each relationship exists on exactly one layer:

| Layer | Description | Example Usage |
|-------|-------------|---------------|
| **Abstract** | Conceptual groupings, domain boundaries | Link Glossary concepts to their contained elements |
| **Browse** | Navigation, UI exposure, entry points | Link UI buttons to Code handlers they invoke |
| **CodePath** | Implementation calls, service dependencies | Link Code caller to callee (downstream = call direction) |
| **DataPath** | Entity boundaries, data flow, ownership | Link Code operations to Data entities they access |
| **EffectPath** | Conditions, flags, settings that gate behavior | Link Config/Security conditions to affected behaviors |
| **Flow** | Trigger-to-outcome sequences, user journeys | Link steps in temporal order across realms |
| **Reference** | Supporting documentation, external links | Link observations to documentation sources |

### Strength
A confidence value (0.0 to 1.0) assigned to observations and relationships:
- **0.5** - Normal default for new discoveries
- **1.0** - High confidence assertion
- **0.0** - Explicit invalidation (triggers removal)
- **Intermediate values** - Adjust confidence as needed

The MCP server automatically merges strength values when observations are re-observed, using a geometric mean formula (see dora-mcp.md for details).

## Key Distinctions

### Realm vs. Layer
- **Realm** answers: "What kind of thing is this observation?"
- **Layer** answers: "What kind of relationship exists between these observations?"
- An observation belongs to **one realm**
- A relationship exists on **one layer**
- An observation can have relationships on **multiple layers**

Example:
```
Observation: code.profile.service.get (Code realm)
- Has CodePath layer links to code it calls
- Has DataPath layer links to data entities it accesses
- Has Browse layer links from UI elements that invoke it
```

### Observation vs. Relationship
- **Observations** are the nodes (things discovered)
- **Relationships** are the edges (connections between things)
- Use `observe()` MCP function to create/update observations
- Use `link()` MCP function to create/update relationships

### Info vs. Links
- **Info** is a JSON field stored *within* an observation containing discovery metadata
- **Links** are relationships *between* observations, stored separately via `link()`
- Info can include URLs, documentation references, source locations, etc.
- Links represent structural relationships in the graph

### Upstream vs. Downstream
- **Downstream** - Follow relationships from source → target (direction of discovery)
- **Upstream** - Follow relationships from target → source (reverse direction)

Example in CodePath layer:
```
ClassA.Method1 → ClassB.Method2 (downstream = outgoing calls)
ClassB.Method2 ← ClassA.Method1 (upstream = incoming calls)
```

### Layer vs. Perspective
These terms are used interchangeably:
- **Layer** is the MCP terminology (used in code/API)
- **Perspective** is the conceptual terminology (used in documentation)

Both refer to the same categorization of relationships.

## Discovery Concepts

### Fuzzy Matching
When searching for candidate observations before creating new ones, the system uses fuzzy matching based on:
- Realm type
- Info field contents (varies by context)
- Semantic similarity
- Purpose: avoid duplicates while allowing flexible discovery

### Deterministic IDs
Observation IDs must be unique and reproducible. Format varies by realm:
- **UI**: Use `data-dgat` attributes or qualified paths
- **Code**: Use fully qualified names with namespace
- **Data**: Use schema.table.column or schema.procedure
- **Security**: Use type.name format (e.g., `security.ld.{flag-name}`)
- **Config**: Use namespace.setting format
- **Glossary**: Use domain.concept format
- **Infra**: Use type.name format

### Database
The SQLite database file managed by the dora-mcp server, stored at `~/.claude/dora/{database-name}.db`. Contains all observations and relationships for a specific discovery context.

### Session Context
The currently connected database for a DORA session. Selected on first connection or when invoking `/dora` command.

## Workflow Terms

### Discovery Operation
Any activity that:
1. Explores the codebase or system
2. Identifies observations
3. Records them in the Discovery Graph
4. Links them via appropriate layers

### Layer-Specific Discovery
Focused exploration through a single layer (e.g., `/dora-codepaths` explores CodePath layer, creating Code realm observations and CodePath layer links).

### Multi-Layer Discovery
Comprehensive exploration across all layers (e.g., `/dora-fulltest` runs all layer discoveries sequentially).

### Graph Traversal
Navigation through the Discovery Graph following relationships:
- Can specify direction (upstream/downstream/both)
- Can filter by layer
- Returns subgraph of relevant observations and relationships

## MCP Functions Reference

### Core Operations
- `connect(name)` - Connect to or create database
- `observe(id, realm, strength, info)` - Create/update observation
- `link(source_id, target_id, layer, strength)` - Create/update relationship
- `candidates(realm, info, limit)` - Fuzzy search for existing observations
- `traverse(id, direction, depth, layers)` - Navigate the graph
- `read(ids)` - Get observation details
- `status()` - Connection state and statistics

See `dora-mcp.md` for complete API documentation.

## Legacy Terms (Deprecated)

The following terms from earlier iterations are **no longer used**:

- ❌ **Focus** - Replaced by database selection
- ❌ **Perspective** when referring to observation types - Use "Realm" instead
- ❌ **Canonicalization** - Replaced by deterministic ID generation
- ❌ **Graph merging** - MCP server handles updates automatically
- ❌ **YAML storage** - Replaced by MCP/SQLite

## Abbreviations

- **DORA** - Discovery Observation-Relationship Architecture
- **MCP** - Model Context Protocol (server providing persistence)
- **LD** - LaunchDarkly (feature flag service)
- **UI** - User Interface
- **API** - Application Programming Interface
- **SQL** - Structured Query Language
- **JSON** - JavaScript Object Notation

---

**Document Version:** 1.0  
**Last Updated:** 2026-08-28  
**Related Documents:**
- `DORA-Rebuild-Prompt.md` - Complete specification
- `dora-mcp.md` - MCP server API reference
