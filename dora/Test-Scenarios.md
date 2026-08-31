# DORA Phase 1 - Test Scenarios

**Purpose:** Validation scenarios for Phase 1 core scaffolding  
**Status:** Ready for implementation testing  
**Version:** 1.0

---

## Test Environment Setup

### Prerequisites
1. dora-mcp server running and configured
2. Test workspace with sample codebase
3. `~/.claude/dora/` directory accessible
4. Claude Code with DORA skill loaded

### Sample Test Codebase
For consistent testing, use a simple profile management codebase with:
- UI components (profile page, upload button)
- Controller layer (ProfileController)
- Service layer (ProfileService, StorageService)
- Data layer (Users table, ProfilePhotos table)
- Config (feature flags, settings)

---

## Scenario 1: First Time Setup

### Objective
Verify database selection flow when no database exists.

### Steps
1. Start fresh (delete `~/.claude/dora/` if exists)
2. Run `/dora`

### Expected Results
- Message: "No databases found. Enter a name for your new database:"
- User enters: "test-profile"
- Response: "Connected to test-profile. Graph is empty. Use /dora-query to start exploring."

### Validation
- [ ] `~/.claude/dora/test-profile.db` file created
- [ ] Connection successful
- [ ] Status shows 0 observations, 0 relationships

---

## Scenario 2: Database Selection with Multiple Databases

### Objective
Verify database selection when multiple databases exist.

### Setup
Create two test databases:
- `test-profile.db`
- `test-skills.db`

### Steps
1. Run `/dora` with no active connection

### Expected Results
```
Available databases:
1. test-profile
2. test-skills

Enter number or new database name:
```

User selects: `1`

Response:
```
Connected to test-profile
Observations: 0
Relationships: 0
```

### Validation
- [ ] Both databases listed
- [ ] Selection works by number
- [ ] Connection established to correct database

---

## Scenario 3: Database Status Display

### Objective
Verify status display when database is connected.

### Setup
Connected to database with some observations (manually created via MCP if needed)

### Steps
1. Run `/dora`

### Expected Results
```
Connected to: test-profile

Observations: 5
  Code: 3
  UI: 1
  Data: 1

Relationships: 3
  CodePath: 2
  Browse: 1

Use /dora-query to explore, or /dora --switch to change database.
```

### Validation
- [ ] Database name shown
- [ ] Observation count by realm accurate
- [ ] Relationship count by layer accurate
- [ ] Helpful next steps provided

---

## Scenario 4: Database Switching

### Objective
Verify switching between databases mid-session.

### Setup
Two databases: test-profile, test-skills

### Steps
1. Connect to test-profile
2. Run `/dora --switch`
3. Select test-skills

### Expected Results
- Disconnect from test-profile
- List available databases
- Connect to test-skills
- Show new database status

### Validation
- [ ] Connection switched correctly
- [ ] Session state updated
- [ ] Status reflects new database

---

## Scenario 5: First Query - Empty Graph

### Objective
Verify query-driven discovery from empty graph.

### Steps
1. Connect to fresh database
2. Run `/dora-query How does profile photo upload work?`

### Expected Results
```
Exploring codebase...

## Answer
Profile photo upload is handled by the UploadButton component which 
triggers ProfileController.UploadPhoto, which validates the file and 
calls StorageService.SavePhoto to persist to blob storage.

## Discoveries
Created observations:
- ui.profile.photo.upload.button (UI realm)
- code.profile.controller.upload.photo (Code realm)
- code.storage.service.save.photo (Code realm)
- infra.blob.profile_photos (Infra realm)

Created links:
- ui.profile.photo.upload.button → code.profile.controller.upload.photo (Browse layer)
- code.profile.controller.upload.photo → code.storage.service.save.photo (CodePath layer)
- code.storage.service.save.photo → infra.blob.profile_photos (CodePath layer)

[Graph now contains 4 observations, 3 relationships]
```

### Validation
- [ ] Graph search attempted first
- [ ] Codebase exploration triggered
- [ ] Observations created with correct realms
- [ ] Observation IDs follow format rules
- [ ] Links created with correct layers
- [ ] Answer references created observations
- [ ] No duplicate observations created

---

## Scenario 6: Second Query - Building on Graph

### Objective
Verify that second query reuses prior discoveries.

### Setup
Run Scenario 5 first (graph has upload flow observations)

### Steps
1. Run `/dora-query What validates the uploaded file?`

### Expected Results
```
Building on prior discoveries...

## Answer
File validation is handled by FileValidator.ValidateImage which checks
file size, type, and dimensions before storage.

## Evidence
Found in code.profile.controller.upload.photo:42
Calls code.file.validator.validate.image

## Discoveries
Created observations:
- code.file.validator.validate.image (Code realm)

Created links:
- code.profile.controller.upload.photo → code.file.validator.validate.image (CodePath layer)

Reused observations:
- code.profile.controller.upload.photo (from previous query)

[Graph now contains 5 observations, 4 relationships]
```

### Validation
- [ ] Prior observation reused (not duplicated)
- [ ] New observation created for validator
- [ ] Link created between existing and new observation
- [ ] Graph statistics incremented correctly
- [ ] Answer cites both new and reused observations

---

## Scenario 7: Observation ID Generation - All Realms

### Objective
Verify ID generation for all realms.

### Test Cases

**UI Realm:**
```
Input: { "data-dgat": "profile-photo-upload-button" }
Expected: ui.profile.photo.upload.button
```

**Code Realm:**
```
Input: { "qualifiedName": "Degreed.Profile.Controller.UploadPhoto" }
Expected: code.degreed.profile.controller.upload.photo
```

**Data Realm:**
```
Input: { "schema": "dbo", "table": "Users", "column": "profile_photo_url" }
Expected: data.dbo.users.profile_photo_url
```

**Security Realm:**
```
Input: { "type": "ld", "name": "show_profile_photo" }
Expected: security.ld.show_profile_photo
```

**Config Realm:**
```
Input: { "namespace": "app", "setting": "max_photo_size" }
Expected: config.app.max_photo_size
```

**Glossary Realm:**
```
Input: { "domain": "profile", "concept": "photo_management" }
Expected: glossary.profile.photo_management
```

**Infra Realm:**
```
Input: { "type": "blob", "name": "profile_photos" }
Expected: infra.blob.profile_photos
```

### Validation
- [ ] All realm ID generators produce deterministic, valid IDs
- [ ] IDs follow documented format rules
- [ ] IDs are lowercase with dot separators

---

## Scenario 8: Duplicate Prevention - Exact Match

### Objective
Verify duplicate prevention when exact match exists.

### Steps
1. Create observation: `code.profile.controller.upload.photo`
2. Attempt to create same observation again with identical info

### Expected Results
- Candidate search finds existing observation
- Exact match detected
- Existing observation ID returned
- No duplicate created
- Strength may be updated via MCP merge

### Validation
- [ ] Only one observation exists in graph
- [ ] ID reused correctly
- [ ] No error thrown

---

## Scenario 9: Duplicate Prevention - Fuzzy Match

### Objective
Verify fuzzy matching for similar observations.

### Steps
1. Create observation: `code.profile.controller.upload.photo` with filePath `ProfileController.cs:42`
2. Attempt to create observation with:
   - Slightly different qualifiedName
   - Same filePath `ProfileController.cs:42`

### Expected Results
- Candidate search finds similar observation
- Fuzzy match based on filePath proximity
- AI judgment or high-confidence heuristic
- Existing observation reused

### Validation
- [ ] Fuzzy matching detects similarity
- [ ] Appropriate heuristic applied
- [ ] No duplicate created if high confidence match

---

## Scenario 10: Link Creation - All Layers

### Objective
Verify link creation for all layers.

### Test Cases

**Browse Layer:**
```
Source: ui.profile.photo.upload.button
Target: code.profile.controller.upload.photo
Layer: Browse
Expected: Link created showing UI → handler relationship
```

**CodePath Layer:**
```
Source: code.profile.controller.upload.photo
Target: code.storage.service.save.photo
Layer: CodePath
Expected: Link created showing caller → callee relationship
```

**DataPath Layer:**
```
Source: code.storage.service.save.photo
Target: data.dbo.profile_photos
Layer: DataPath
Expected: Link created showing code → data access
```

**EffectPath Layer:**
```
Source: security.ld.enable_photo_upload
Target: ui.profile.photo.upload.button
Layer: EffectPath
Expected: Link created showing flag → controlled behavior
```

**Flow Layer:**
```
Source: ui.profile.photo.upload.button
Target: ui.profile.photo.success.message
Layer: Flow
Expected: Link created showing user journey step
```

**Abstract Layer:**
```
Source: glossary.profile.photo_management
Target: code.profile.controller.upload.photo
Layer: Abstract
Expected: Link created showing concept → implementation
```

**Reference Layer:**
```
Source: code.profile.controller.upload.photo
Target: (external doc URL in info)
Layer: Reference
Expected: Link created showing code → documentation
```

### Validation
- [ ] All layer links created successfully
- [ ] Directionality preserved (source → target)
- [ ] Layer recorded correctly
- [ ] Strength set to default or provided value

---

## Scenario 11: Graph Traversal - Downstream

### Objective
Verify downstream graph traversal.

### Setup
Graph with chain:
```
ui.button → code.controller → code.service → data.table
```

### Steps
1. Traverse from `ui.button`, direction: "downstream", depth: 3

### Expected Results
```
Subgraph:
Observations:
- ui.button
- code.controller
- code.service
- data.table

Links:
- ui.button → code.controller (Browse)
- code.controller → code.service (CodePath)
- code.service → data.table (DataPath)
```

### Validation
- [ ] All downstream observations returned
- [ ] Links follow source → target direction
- [ ] Depth limit respected
- [ ] No upstream observations included

---

## Scenario 12: Graph Traversal - Upstream

### Objective
Verify upstream graph traversal.

### Setup
Same chain as Scenario 11

### Steps
1. Traverse from `data.table`, direction: "upstream", depth: 3

### Expected Results
```
Subgraph:
Observations:
- data.table
- code.service
- code.controller
- ui.button

Links:
- code.service → data.table (DataPath)
- code.controller → code.service (CodePath)
- ui.button → code.controller (Browse)
```

### Validation
- [ ] All upstream observations returned
- [ ] Links show what leads to starting observation
- [ ] Depth limit respected
- [ ] No downstream observations included

---

## Scenario 13: Graph Traversal - Layer Filter

### Objective
Verify layer filtering in traversal.

### Setup
Graph with:
```
code.controller → code.service (CodePath)
code.controller → data.table (DataPath)
```

### Steps
1. Traverse from `code.controller`, direction: "downstream", layers: ["CodePath"]

### Expected Results
```
Subgraph:
Observations:
- code.controller
- code.service

Links:
- code.controller → code.service (CodePath)
```

### Validation
- [ ] Only CodePath layer included
- [ ] DataPath link excluded
- [ ] data.table observation excluded (not reachable via CodePath)

---

## Scenario 14: Session Persistence

### Objective
Verify database connection persists across skill invocations.

### Steps
1. Run `/dora` and connect to test-profile
2. Run `/dora-query` (some query)
3. Simulate new skill invocation (if possible)
4. Run `/dora` again

### Expected Results
- Second `/dora` shows still connected to test-profile
- No need to reconnect
- Graph statistics include observations from step 2

### Validation
- [ ] Connection persisted
- [ ] Session state maintained
- [ ] No re-connection prompt

---

## Scenario 15: Error Handling - MCP Server Not Running

### Objective
Verify graceful error when MCP server is down.

### Setup
Stop dora-mcp server

### Steps
1. Run `/dora`

### Expected Results
```
Error: Cannot connect to dora-mcp server.

Please ensure:
1. dora-mcp server is installed
2. Server is running
3. Server is configured in Claude Code MCP settings

See SKILL.md for setup instructions.
```

### Validation
- [ ] Clear, helpful error message
- [ ] No stack trace shown to user
- [ ] Guidance on resolution

---

## Scenario 16: Error Handling - Invalid Database Name

### Objective
Verify validation of database names.

### Steps
1. Run `/dora`
2. Enter invalid name: `test/profile!@#`

### Expected Results
```
Error: Invalid database name.

Database names must contain only:
- Letters (a-z, A-Z)
- Numbers (0-9)
- Dots (.)
- Dashes (-)
- Underscores (_)

Example: test-profile or degreed.skills
```

### Validation
- [ ] Invalid name rejected
- [ ] Clear validation rules provided
- [ ] User can retry

---

## Scenario 17: Complex Query - Multi-Realm Discovery

### Objective
Verify discovery across multiple realms.

### Steps
1. Run `/dora-query What data does the profile photo upload feature use?`

### Expected Results
```
## Answer
Profile photo upload uses the Users table (profile_photo_url column)
and ProfilePhotos table (id, user_id, photo_blob columns) for storage.

## Discoveries
Created observations:
- ui.profile.photo.upload.button (UI realm)
- code.profile.controller.upload.photo (Code realm)
- code.storage.service.save.photo (Code realm)
- data.dbo.users.profile_photo_url (Data realm)
- data.dbo.profile_photos (Data realm)

Created links:
- ui.profile.photo.upload.button → code.profile.controller.upload.photo (Browse)
- code.profile.controller.upload.photo → code.storage.service.save.photo (CodePath)
- code.storage.service.save.photo → data.dbo.users.profile_photo_url (DataPath)
- code.storage.service.save.photo → data.dbo.profile_photos (DataPath)
```

### Validation
- [ ] Multiple realms discovered (UI, Code, Data)
- [ ] Multiple layers used (Browse, CodePath, DataPath)
- [ ] All observations related to query topic
- [ ] Answer synthesizes cross-realm understanding

---

## Scenario 18: Performance - Reasonable Query Time

### Objective
Verify queries complete in reasonable time.

### Steps
1. Run query on moderately complex feature (5-10 observations expected)
2. Measure time from command to response

### Expected Results
- Query completes in < 30 seconds
- If longer, progress indicator shown (Phase 2 feature)

### Validation
- [ ] Response time acceptable
- [ ] No timeout errors
- [ ] User experience is responsive

---

## Performance Benchmarks

### Target Metrics (Phase 1)

| Metric | Target | Critical |
|--------|--------|----------|
| Database listing | < 1 sec | < 3 sec |
| Database connection | < 2 sec | < 5 sec |
| Simple query (1-3 obs) | < 10 sec | < 20 sec |
| Complex query (5-10 obs) | < 20 sec | < 45 sec |
| Graph traversal (depth 3) | < 2 sec | < 5 sec |
| Duplicate check | < 1 sec | < 3 sec |

### Memory Constraints
- Graph size limit: 1000 observations (Phase 1)
- Single query observation limit: 50 observations

---

## Acceptance Criteria Summary

Phase 1 is ready for release when:

- [ ] All 18 test scenarios pass
- [ ] Performance targets met for 80%+ of operations
- [ ] No critical bugs (crashes, data loss, corruption)
- [ ] Error messages are clear and helpful
- [ ] Documentation matches implementation
- [ ] Code quality meets standards (docstrings, type hints, style)

---

## Test Execution Checklist

### Pre-Testing
- [ ] dora-mcp server running
- [ ] Test codebase prepared
- [ ] `~/.claude/dora/` directory clean/backed up
- [ ] DORA skill loaded in Claude Code

### During Testing
- [ ] Record actual vs expected results for each scenario
- [ ] Note any deviations or unexpected behavior
- [ ] Capture error messages verbatim
- [ ] Measure performance for benchmark scenarios

### Post-Testing
- [ ] Document all failures with steps to reproduce
- [ ] Create issues for bugs found
- [ ] Update test scenarios if spec changed
- [ ] Archive test database for regression testing

---

**Last Updated:** 2026-08-28  
**Test Coverage:** Phase 1 Core Scaffolding  
**Next:** Phase 2 test scenarios (layer-specific sub-skills)
