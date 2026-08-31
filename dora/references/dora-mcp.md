# DORA MCP Protocol Reference

This file is intended to be placed in a skill's `references/` folder so the skill knows how to interact with the DORA Discovery Graph.

## Connection

Call `mcp__dora-mcp__connect(name="<graph-name>")` before any other DORA tool. This opens or creates a SQLite database at `~/.claude/dora/<name>.db` and returns the full protocol summary. If already connected in this session, calling connect again switches to the named database.

## Tools

### Write

**observe** — Create or update an observation.
```
mcp__dora-mcp__observe(
    id: str,          # stable unique id, lowercase dot-path (e.g. "ui.save.button")
    realm: str,       # category: UI, Code, Data, Security, Config, Glossary, Infra, or custom
    strength: float,  # 0..1, default 0.5. 0.0 = remove.
    info: dict        # JSON object with domain-specific payload, optional
)
```
- If the observation exists, strength merges and info keys are merged (new added, existing overwritten).
- Strength 0 removes the observation and all its links.

**link** — Create or update a directed relationship between two observations.
```
mcp__dora-mcp__link(
    source_id: str,   # must exist
    target_id: str,   # must exist
    layer: str,       # perspective: Abstract, Browse, CodePath, DataPath, EffectPath, Flow, Reference, or custom
    strength: float   # 0..1, default 0.5. 0.0 = remove.
)
```

### Read

**candidates** — Find observations by realm and/or text match.
```
mcp__dora-mcp__candidates(
    realm: str,       # filter by realm, optional
    info: str,        # text to search in ids and info fields, optional
    limit: int        # max results, default 50
)
```
Call this before creating a new observation to avoid duplicates.

**traverse** — Walk the graph from an observation.
```
mcp__dora-mcp__traverse(
    id: str,          # starting observation
    direction: str,   # "upstream", "downstream", or "both" (default)
    depth: int,       # hops, default 1
    layers: list[str] # filter to specific layers, optional (None = all)
)
```
Returns `{root, nodes[], edges[]}`.

**read** — Get full details for specific observations.
```
mcp__dora-mcp__read(ids: list[str])
```
Returns id, realm, strength, info, created_at, updated_at for each.

### Control

**status** — Show connection state and graph statistics.
```
mcp__dora-mcp__status()
```

## Strength

Values are between 0 and 1:
- **1.0** — maximum, confirmed
- **0.5** — normal (default for new observations)
- **0.0** — invalid, triggers removal

When an observation or link is re-observed, the existing and incoming strengths merge via an odds-ratio geometric mean centered on 0.5:
- Same + same = same (idempotent)
- Slight differences pull slowly toward the center (0.5)
- Symmetric opposites cancel to 0.5
- Either value being 0 produces 0 (deletion)

## Realms

Category for an observation. Seeded defaults:

| Realm | Use for |
|-------|---------|
| UI | Visual elements, pages, buttons, menus |
| Code | Classes, functions, modules, services |
| Data | Tables, entities, schemas, fields |
| Security | Permissions, roles, auth, access control |
| Config | Settings, flags, feature toggles, environment |
| Glossary | Business terms, domain concepts, definitions |
| Infra | Servers, queues, pipelines, deployments |

Custom realms are created automatically on first use.

## Layers

Perspective for a relationship. Seeded defaults:

| Layer | Connects |
|-------|----------|
| Abstract | Conceptual groupings, domain boundaries |
| Browse | Navigation, UI exposure, entry points |
| CodePath | Implementation calls, service dependencies |
| DataPath | Entity boundaries, data flow, ownership |
| EffectPath | Conditions, flags, settings that gate behavior |
| Flow | Trigger-to-outcome sequences, user journeys |
| Reference | Supporting documentation, external links |

Custom layers are created automatically on first use.

## Workflow Pattern

```
1. candidates(realm, info)     # search before creating — avoid duplicates
2. read(ids)                   # inspect existing observations
3. traverse(id, ...)           # explore known relationships
4. observe(id, realm, ...)     # record new findings
5. link(source, target, layer) # connect observations
6. observe(id, realm, 0.0)     # retire invalid findings with strength 0
```

## ID Convention

Use lowercase dot-path ids with a realm-derived prefix:
- `ui.settings.save.button`
- `code.user.service.get.profile`
- `data.users.email`
- `config.feature.new.dashboard`
- `concept.reporting.domain`

IDs are stable and immutable once created. Reuse existing IDs; do not create duplicates.
