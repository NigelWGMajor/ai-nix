# DORA Phase 1 - Implementation Checklist

**Target:** Core scaffolding for query-driven discovery  
**Status:** Ready to implement  
**Estimated Effort:** 3-5 days

---

## Prerequisites

- [ ] `dora-mcp` server is installed and running
- [ ] MCP server registered in Claude Code settings
- [ ] Test workspace with sample codebase available
- [ ] `~/.claude/dora/` directory accessible

---

## Phase 1.1: Database Management

### Task 1.1.1: List Available Databases
- [ ] Implement `list_databases()` function
  - [ ] Use Bash tool: `ls ~/.claude/dora/*.db 2>/dev/null || echo ""`
  - [ ] Parse output to extract database names (strip `.db` extension)
  - [ ] Handle empty directory (no databases yet)
  - [ ] Return list of database names

### Task 1.1.2: Database Selection UX
- [ ] Implement `select_database()` function
  - [ ] If databases exist: present numbered list
  - [ ] Allow user to select by number or enter new name
  - [ ] Validate database name (alphanumeric, dots, dashes, underscores)
  - [ ] Sanitize user input

### Task 1.1.3: MCP Connection
- [ ] Implement `connect_database(name)` function
  - [ ] Call `mcp__dora-mcp__connect(name=database_name)`
  - [ ] Handle connection success
  - [ ] Handle connection failure (server not running, permissions, etc.)
  - [ ] Return connection status

### Task 1.1.4: Session Persistence
- [ ] Store active database name in session context
  - [ ] Use conversation-scoped variable (if available)
  - [ ] Otherwise use in-memory state (reset per skill invocation)
- [ ] Implement `get_active_database()` to retrieve
- [ ] Implement `set_active_database(name)` to store

### Task 1.1.5: `/dora` Status Command
- [ ] Implement `/dora` command handler
  - [ ] Check if database connected
  - [ ] If connected: show status (database name, statistics)
  - [ ] If not connected: list available databases and prompt
  - [ ] Call `mcp__dora-mcp__status()` for graph statistics
  - [ ] Format output as readable markdown

### Task 1.1.6: `/dora --switch` Command
- [ ] Implement database switching
  - [ ] Disconnect from current database (if connected)
  - [ ] List available databases
  - [ ] Prompt for selection
  - [ ] Connect to new database

**Acceptance Test:** User can list databases, select one, see status, and switch databases.

---

## Phase 1.2: Observation CRUD

### Task 1.2.1: ID Generation Functions
- [ ] Implement `generate_ui_id(info)` 
  - [ ] Prefer `data-dgat` attribute if available
  - [ ] Fallback to route + element type + qualifier
  - [ ] Return `ui.{path}`
- [ ] Implement `generate_code_id(info)`
  - [ ] Use qualified name: namespace.class.member
  - [ ] Handle missing namespace (use file path as namespace)
  - [ ] Return `code.{path}`
- [ ] Implement `generate_data_id(info)`
  - [ ] Format: schema.table.column or schema.procedure
  - [ ] Handle non-SQL: namespace.variable
  - [ ] Return `data.{path}`
- [ ] Implement `generate_security_id(info)`
  - [ ] Format: type.name (ld.flag_name, orgsettings.setting_name)
  - [ ] Return `security.{path}`
- [ ] Implement `generate_config_id(info)`
  - [ ] Format: namespace.setting_name
  - [ ] Return `config.{path}`
- [ ] Implement `generate_glossary_id(info)`
  - [ ] Format: domain.concept
  - [ ] Return `glossary.{path}`
- [ ] Implement `generate_infra_id(info)`
  - [ ] Format: type.name
  - [ ] Return `infra.{path}`
- [ ] Implement `generate_observation_id(realm, info)` router
  - [ ] Dispatch to realm-specific generator
  - [ ] Validate generated ID format

### Task 1.2.2: Create Observation
- [ ] Implement `create_observation(realm, info, strength=0.5)`
  - [ ] Generate ID using realm-specific function
  - [ ] Call `mcp__dora-mcp__observe(id, realm, strength, info)`
  - [ ] Handle MCP errors (duplicate ID, invalid realm, etc.)
  - [ ] Return observation ID

### Task 1.2.3: Info Field Builders
- [ ] Implement `build_ui_info(...)` helper
  - [ ] Fields: elementType, selector, route, parentComponent
  - [ ] Return dict
- [ ] Implement `build_code_info(...)` helper
  - [ ] Fields: qualifiedName, filePath, lineNumber, signature
  - [ ] Return dict
- [ ] Implement `build_data_info(...)` helper
  - [ ] Fields: tableName, fieldName, dataType, nullable
  - [ ] Return dict
- [ ] Implement `build_config_info(...)` helper
  - [ ] Fields: key, source, defaultValue, scope
  - [ ] Return dict
- [ ] Implement `build_security_info(...)` helper
  - [ ] Fields: type, name, description, defaultValue, scope
  - [ ] Return dict
- [ ] Implement `build_glossary_info(...)` helper
  - [ ] Fields: domain, concept, definition, relatedTerms
  - [ ] Return dict
- [ ] Implement `build_infra_info(...)` helper
  - [ ] Fields: type, name, endpoint, technology
  - [ ] Return dict

**Acceptance Test:** Can create observations in all realms with proper IDs and info fields.

---

## Phase 1.3: Relationship CRUD

### Task 1.3.1: Create Link
- [ ] Implement `create_link(source_id, target_id, layer, strength=0.5)`
  - [ ] Validate source and target IDs exist (via `read()`)
  - [ ] Call `mcp__dora-mcp__link(source_id, target_id, layer, strength)`
  - [ ] Handle MCP errors
  - [ ] Return link confirmation

### Task 1.3.2: Layer Constants
- [ ] Define layer constants
  - [ ] LAYER_ABSTRACT = "Abstract"
  - [ ] LAYER_BROWSE = "Browse"
  - [ ] LAYER_CODEPATH = "CodePath"
  - [ ] LAYER_DATAPATH = "DataPath"
  - [ ] LAYER_EFFECTPATH = "EffectPath"
  - [ ] LAYER_FLOW = "Flow"
  - [ ] LAYER_REFERENCE = "Reference"

**Acceptance Test:** Can create links between observations on all layers.

---

## Phase 1.4: Candidate Search & Duplicate Prevention

### Task 1.4.1: Search Candidates
- [ ] Implement `search_candidates(realm, info, limit=10)`
  - [ ] Call `mcp__dora-mcp__candidates(realm, info, limit)`
  - [ ] Parse response (list of candidate observations)
  - [ ] Return candidates with match scores

### Task 1.4.2: Matching Heuristics
- [ ] Implement `find_best_match(candidates, realm, info)`
  - [ ] **Code realm:** Exact match on qualifiedName, else proximity on filePath+lineNumber
  - [ ] **UI realm:** Exact match on data-dgat, else fuzzy on route+elementType
  - [ ] **Data realm:** Exact match on schema.table.column
  - [ ] **Config/Security realm:** Exact match on type+name
  - [ ] If single high-confidence match (>0.9) → return it
  - [ ] If multiple ambiguous matches → use AI judgment or return None
  - [ ] If no match → return None

### Task 1.4.3: Get or Create Observation
- [ ] Implement `get_or_create_observation(realm, info, strength=0.5)`
  - [ ] Search candidates
  - [ ] If best match found → return existing ID
  - [ ] If no match → create new observation
  - [ ] Return observation ID and whether it was created or reused

**Acceptance Test:** Duplicate observations are avoided; re-discovery reuses existing IDs.

---

## Phase 1.5: Query-Driven Discovery

### Task 1.5.1: `/dora-query` Command Parser
- [ ] Implement `/dora-query <question>` command handler
  - [ ] Parse question text
  - [ ] Extract context/guidance from question
  - [ ] Validate database connection (auto-connect if needed)

### Task 1.5.2: Graph Search First
- [ ] Implement `search_graph_for_question(question)`
  - [ ] Extract keywords from question
  - [ ] Search candidates across all realms with keywords
  - [ ] Return relevant observations (if any)

### Task 1.5.3: Exploration Dispatcher
- [ ] Implement `explore_codebase(question, existing_observations)`
  - [ ] Determine exploration strategy based on question type:
    - [ ] "How does X work?" → CodePath exploration
    - [ ] "What settings affect X?" → EffectPath exploration
    - [ ] "Where is X used?" → Grep + candidates
    - [ ] "What data does X use?" → DataPath exploration
  - [ ] Use appropriate tools: Grep, Read, codebase-memory-mcp
  - [ ] Return discovered evidence

### Task 1.5.4: Discovery Capture
- [ ] Implement `capture_discovery(evidence)`
  - [ ] For each discovered element:
    - [ ] Determine realm
    - [ ] Build info dict
    - [ ] Get or create observation
  - [ ] For each discovered connection:
    - [ ] Determine layer
    - [ ] Create link between observations
  - [ ] Return list of observations and links created

### Task 1.5.5: Answer Synthesis
- [ ] Implement `synthesize_answer(question, observations, links, evidence)`
  - [ ] Combine graph data with fresh evidence
  - [ ] Format answer as markdown
  - [ ] Include references to observations
  - [ ] Cite observation IDs for traceability

### Task 1.5.6: `/dora-query` Integration
- [ ] Wire up full query flow:
  1. Search graph for existing observations
  2. If incomplete, explore codebase
  3. Capture discoveries as observations/links
  4. Synthesize answer with references
  5. Return to user

**Acceptance Test:** User asks question, skill explores, captures discoveries, returns answer with observation references. Subsequent related questions build on graph.

---

## Phase 1.6: Graph Traversal

### Task 1.6.1: Traverse Graph
- [ ] Implement `traverse_from(observation_id, direction, depth=3, layers=None)`
  - [ ] Call `mcp__dora-mcp__traverse(id, direction, depth, layers)`
  - [ ] direction: "downstream" | "upstream" | "both"
  - [ ] layers: list of layer names to filter, or None for all
  - [ ] Parse response (subgraph of observations and links)
  - [ ] Return subgraph

### Task 1.6.2: Format Traversal Results
- [ ] Implement `format_subgraph(subgraph)`
  - [ ] Display observations with IDs, realms, info summaries
  - [ ] Display links showing source → target relationships
  - [ ] Group by layers
  - [ ] Return formatted markdown

### Task 1.6.3: Integrate Traversal into Query
- [ ] When graph has relevant observations, traverse to gather context
- [ ] Use traversal results to enhance answer
- [ ] Show relationship paths in answer

**Acceptance Test:** Can traverse graph in all directions, filter by layers, and get subgraph results.

---

## Phase 1.7: Error Handling & Edge Cases

### Task 1.7.1: MCP Connection Errors
- [ ] Handle server not running
  - [ ] Friendly error: "dora-mcp server not running. Please start MCP server."
- [ ] Handle connection timeout
  - [ ] Retry with exponential backoff (3 attempts)
- [ ] Handle permission errors
  - [ ] Check `~/.claude/dora/` directory permissions

### Task 1.7.2: Invalid Input Handling
- [ ] Validate database names (alphanumeric + dots, dashes, underscores)
- [ ] Validate observation IDs format
- [ ] Validate realms (must be one of 7 valid realms)
- [ ] Validate layers (must be one of 7 valid layers)
- [ ] Handle malformed info dicts gracefully

### Task 1.7.3: Orphaned Links
- [ ] Before creating link, verify both observations exist
- [ ] If observation missing, warn and skip link creation
- [ ] Optionally: create placeholder observation with low strength

### Task 1.7.4: Empty Graph Handling
- [ ] When graph is empty, guide user on how to get started
- [ ] First query should explain it's building the graph from scratch
- [ ] Provide examples of good starting questions

**Acceptance Test:** Errors are handled gracefully with helpful messages. No crashes.

---

## Phase 1.8: Testing & Validation

### Task 1.8.1: Unit Tests
- [ ] Test ID generation for all realms
- [ ] Test info field builders
- [ ] Test candidate matching heuristics
- [ ] Test observation creation
- [ ] Test link creation
- [ ] Test traversal parsing

### Task 1.8.2: Integration Tests
- [ ] Test full database selection flow
- [ ] Test full query-driven discovery flow
- [ ] Test graph traversal integration
- [ ] Test session persistence across invocations

### Task 1.8.3: End-to-End Scenarios
- [ ] Run all test scenarios from test-scenarios.md
- [ ] Verify observations created correctly
- [ ] Verify links created with proper layers
- [ ] Verify duplicate prevention works
- [ ] Verify graph grows incrementally

**Acceptance Test:** All test scenarios pass without errors.

---

## Phase 1.9: Documentation & Polish

### Task 1.9.1: Help Text
- [ ] Add help text for `/dora` command
- [ ] Add help text for `/dora-query` command
- [ ] Add usage examples in SKILL.md

### Task 1.9.2: Error Messages
- [ ] Ensure all error messages are clear and actionable
- [ ] Provide next steps in error messages
- [ ] No technical jargon in user-facing messages

### Task 1.9.3: Performance
- [ ] Ensure queries complete in reasonable time (<30 seconds typical)
- [ ] Limit exploration scope to avoid runaway discovery
- [ ] Add progress indicators for long-running operations

### Task 1.9.4: Code Quality
- [ ] Add docstrings to all functions
- [ ] Add type hints (if using Python)
- [ ] Consistent code style
- [ ] Remove debug code and commented-out sections

**Acceptance Test:** Skill is well-documented, user-friendly, and performs well.

---

## Definition of Done

### Phase 1 is complete when:

- [x] User can list and select databases
- [x] User can ask questions via `/dora-query`
- [x] Questions trigger code exploration
- [x] Discoveries are captured as observations with correct realms and IDs
- [x] Connections are captured as links with correct layers
- [x] Subsequent questions build on prior discoveries (graph traversal)
- [x] Duplicate observations are prevented
- [x] Session state is maintained across invocations
- [x] All test scenarios pass
- [x] Documentation is complete
- [x] Error handling is robust

### Success Metrics:

1. **Graph Growth:** Each query adds 3-10 observations on average
2. **Reuse Rate:** 40%+ of observations in query 2+ are reused from prior queries
3. **Answer Quality:** Answers include references to 2+ observations
4. **User Satisfaction:** Users find the navigable cache helpful for subsequent queries

---

## Ready for Phase 2 When:

- [ ] Phase 1 metrics achieved
- [ ] User feedback collected and positive
- [ ] Core infrastructure stable and tested
- [ ] Performance acceptable (queries <30s)
- [ ] No critical bugs

**Phase 2 Goal:** Build layer-specific sub-skills for comprehensive automated discovery.

---

**Next Step:** Begin Task 1.1.1 - Implement database listing
