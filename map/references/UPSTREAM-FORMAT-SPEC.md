# Upstream File Format Specification

**Version:** 1.0  
**Last Updated:** 2026-08-26

This document describes the canonical formats for exporting and importing upstream reference data in the Nix Upstream Check extension. Both JSON and Markdown formats support full round-trip conversion without data loss.

---

## Overview

Upstream files capture the call hierarchy and reference relationships discovered during code analysis. The extension supports two interchange formats:

1. **JSON** (`.upstream.json`) - Machine-readable, preserves all metadata
2. **Markdown** (`.upstream.md`) - Human-readable, optimized for documentation and review

Both formats are **semantically equivalent** and support bidirectional conversion.

---

## JSON Format

### File Extension
`.upstream.json`

### MIME Type
`application/json`

### Root Structure

```typescript
{
  "exportedAt": string,        // ISO 8601 timestamp
  "trees": Array<TreeNode>,    // Top-level search results
  "expandedNodes"?: string[]   // Optional: UI state preservation
}
```

### TreeNode Structure

```typescript
{
  // Identity
  "name": string,              // Method/class/comment text
  "namespace"?: string,        // Full namespace (e.g., "Degreed.Data.Services")
  
  // Location
  "file": string,              // Absolute or relative file path
  "line": number,              // Zero-based line number
  "character"?: number,        // Zero-based character offset
  
  // Type Markers
  "isComment"?: boolean,       // True for comment nodes
  "isReference"?: boolean,     // True for reference location nodes
  "isClass"?: boolean,         // True for class/interface nodes
  "isInterface"?: boolean,     // True for interface method nodes
  
  // Attributes
  "httpAttribute"?: string,    // HTTP attribute (e.g., "[HttpGet]")
  "commentText"?: string,      // Full comment text (for isComment nodes)
  "referenceType"?: string,    // Reference type: "N" (new), "P" (parameter), "I" (interface)
  
  // State
  "checked": boolean,          // Checkbox state (default: true)
  
  // Relationships
  "children"?: Array<TreeNode>,           // Upstream callers/references
  "referenceLocations"?: Array<ReferenceNode>  // Reference sites within methods
}
```

### ReferenceNode Structure

```typescript
{
  "file": string,
  "line": number,
  "character": number,
  "checked": boolean,
  "referenceType"?: string     // "N", "P", or "I"
}
```

### Example JSON

```json
{
  "exportedAt": "2025-10-20T19:22:26.965Z",
  "trees": [
    {
      "name": "AddTargetAuthorAsync",
      "namespace": "Degreed.Data.Services.Targets",
      "file": "c:\\source\\Degreed\\trunk\\Degreed.Data.Standard\\Services\\Targets\\TargetsDataService.cs",
      "line": 164,
      "checked": false,
      "children": [
        {
          "name": "UpdateTargetAuthorsAsync",
          "namespace": "Degreed.Common.Orchestrators",
          "file": "c:\\source\\Degreed\\trunk\\Degreed.Common.Standard\\Orchestrators\\TargetsOrchestrator.cs",
          "line": 787,
          "character": 42,
          "checked": true,
          "httpAttribute": "[HttpPost(\"UpdateTargetAuthors\")]",
          "referenceLocations": [
            {
              "file": "c:\\source\\Degreed\\trunk\\Degreed.Common.Standard\\Orchestrators\\TargetsOrchestrator.cs",
              "line": 822,
              "character": 42,
              "checked": false
            }
          ]
        }
      ]
    }
  ],
  "expandedNodes": []
}
```

---

## Markdown Format

### File Extension
`.upstream.md`

### Supported Formats

The extension supports **two markdown format variants** for maximum flexibility:

1. **Call Hierarchy Format** - Detailed upstream call chains with metadata
2. **Navigation Map Format** - Component/file navigation with layer grouping

Both formats can be mixed in the same file, and unrecognized sections are gracefully skipped.

---

### Format 1: Call Hierarchy (Detailed)

For detailed upstream reference tracking with full metadata.

```
# Upstream References Report

Generated: <LocaleDateTime>

[--- (separator between root searches) ---]

## Search N: <MethodName>

**Namespace:** <Namespace>

**Location:** [<FilePath>:<LineNumber>](<FilePath>#L<LineNumber>)

**HTTP Attribute:** <HttpAttribute> (if present)

### Upstream Callers:

  - [x] **<MethodName>** [<HttpAttribute>] (if present)
    - Location: [<FilePath>:<LineNumber>](<FilePath>#L<LineNumber>)
    - Namespace: <Namespace>
    - **Reference locations:**
      - [x] [<FileName>:<LineNumber>:<Character>](<FilePath>#L<LineNumber>)
    - [x] **<ChildMethodName>**
      ...
```

---

### Format 2: Navigation Map (Simplified)

For project navigation and component mapping.

```
# Upstream Navigation: <Project Name>

## <Section-ID>: <Component Description>

### <Layer Name>
- <Component Name> | [<FilePath>:<LineNumber>](<FilePath>#L<LineNumber>) | <Layer>
  - <Sub-component> | [<FilePath>:<LineNumber>](<FilePath>#L<LineNumber>) | <Layer>

---

## End-to-End Flow

### N. <Step Name>
- <Component> | [<FilePath>:<LineNumber>](<FilePath>#L<LineNumber>) | <Layer>
```

**Section ID patterns recognized:**
- `## Search N:` - Call hierarchy search result
- `## P-NNN:` - Project partition/component
- `## <Any text>` - Generic section (creates a tree node)

**Item formats recognized:**
- `- [x] **Name**` - Checkbox format (call hierarchy)
- `- Name | [link](url) | Layer` - Pipe-delimited format (navigation map)
- `- [link text](url)` - Simple link format

**Parser behavior:**
- ✅ Parses all recognized formats
- ✅ Creates tree nodes from level-2 headers (`##`)
- ✅ Skips unrecognized content without error
- ✅ Preserves hierarchical indentation
- ✅ Extracts namespace from pipe-delimited layer field

### Syntax Rules (Flexible)

1. **Headers** (Any of these patterns creates a tree root)
   - `## Search N: <MethodName>` - Call hierarchy search result
   - `## P-NNN: <Description>` - Project partition/component  
   - `## <Any text>` - Generic section (creates tree node with name from text)
   - Level-1 headers (`#`) are treated as document titles (optional)

2. **Metadata Lines** (Optional, Format 1 only)
   - `**Namespace:** <value>` - Namespace declaration
   - `**Location:** [<link>](<url>)` - File location with markdown link
   - `**HTTP Attribute:** <value>` - HTTP attribute annotation

3. **List Items** (Multiple formats supported)
   - `- [x] **Name**` - Checkbox format with bold name (Format 1)
   - `- Name | [file:line](url) | Layer` - Pipe-delimited (Format 2)
   - `- [link text](url)` - Simple link format (extracts file/line from URL)
   - Checkboxes: `[x]` = checked, `[ ]` = unchecked (defaults to checked if absent)

4. **Indentation** (Hierarchical structure)
   - Each nesting level adds 2 spaces
   - Indented items become children of the parent item
   - Sub-sections (###) group items but don't create tree nodes

5. **Special Nodes**
   - `- 👇 <CommentText>` - Comment node (no checkbox)
   - `- [x] 📍 <FileName>:<Line>` - Reference location node
   - Bold text (`**Name**`) indicates method/class nodes (Format 1)

6. **Links** (Flexible parsing)
   - `[text](path:line)` or `[text](path#Lline)` - Standard formats
   - Absolute or relative file paths supported
   - URLs with `#L<line>` or `:<line>` suffix parsed for line numbers

7. **Namespace Extraction**
   - Format 1: Explicit `**Namespace:**` metadata line
   - Format 2: Third pipe-delimited field (`| Layer |`) becomes namespace
   - Falls back to empty string if not present

### Example: Format 1 (Call Hierarchy)

```markdown
# Upstream References Report

Generated: 10/21/2025, 10:20:41 AM

---

## Search 1: FindTagsAsync

**Namespace:** Degreed.Data.Services.Tags

**Location:** [c:\source\Degreed\trunk\Degreed.Data.Standard\Services\Tags\TagsDataService.cs:53](c:\source\Degreed\trunk\Degreed.Data.Standard\Services\Tags\TagsDataService.cs#L53)

### Upstream Callers:

  - [x] **FindTagsAsync**
    - Location: [c:\source\Degreed\trunk\Degreed.Common.Standard\Orchestrators\TagsOrchestrator.cs:428](c:\source\Degreed\trunk\Degreed.Common.Standard\Orchestrators\TagsOrchestrator.cs#L428)
    - Namespace: Degreed.Common.Orchestrators
    - [x] **FindTags** [[HttpGet("FindTags")]]
      - Location: [c:\source\Degreed\trunk\Degreed.Web.vNext\Controllers\Api\TagController.cs:184](c:\source\Degreed\trunk\Degreed.Web.vNext\Controllers\Api\TagController.cs#L184)
      - Namespace: Degreed.Web.vNext.Controllers.Api
      - **Reference locations:**
        - [ ] [TagController.cs:193:53](c:\source\Degreed\trunk\Degreed.Web.vNext\Controllers\Api\TagController.cs#L193)
```

### Example: Format 2 (Navigation Map)

```markdown
# Upstream Navigation: Feature Implementation

<!-- Quick navigation file for Upstream extension -->

## P-001: Database Layer (✅ Complete)

### SQL Layer
- BulkUpsert stored procedure | [Degreed.SqlDb/etl/Stored Procedures/BulkUpsert.sql:1](file:///C:/source/Degreed/trunk/Degreed.SqlDb/etl/Stored%20Procedures/BulkUpsert.sql#L1) | SQL
- Staging table | [Degreed.SqlDb/dbo/Tables/Staging.sql:1](file:///C:/source/Degreed/trunk/Degreed.SqlDb/dbo/Tables/Staging.sql#L1) | SQL

### Tests
- BulkUpsert approval tests | [Database/SQL/ApprovalTests/BulkUpsert.sql:1](file:///C:/source/Degreed/trunk/Database/SQL/ApprovalTests/BulkUpsert.sql#L1) | Test

---

## P-002: API Layer (🔶 In Progress)

### Controller Layer
- SkillsController file upload endpoint | [Degreed.Web.vNext/Controllers/SkillsController.cs:1](file:///C:/source/Degreed/trunk/Degreed.Web.vNext/Controllers/SkillsController.cs#L1) | Controller
  - CSV upload action | [Degreed.Web.vNext/Controllers/SkillsController.cs:50](file:///C:/source/Degreed/trunk/Degreed.Web.vNext/Controllers/SkillsController.cs#L50) | Controller

### Tests
- Controller unit tests | [Degreed.Web.vNext.Tests/Controllers/SkillsControllerTests.cs:1](file:///C:/source/Degreed/trunk/Degreed.Web.vNext.Tests/Controllers/SkillsControllerTests.cs#L1) | Test
```

---

## Parsing Rules

### JSON Parsing

1. Standard JSON parser with UTF-8 encoding
2. All fields are case-sensitive
3. Missing optional fields default to undefined/null
4. `checked` defaults to `true` if not present
5. Line numbers are zero-based in storage, one-based in display

### Markdown Parsing

**Philosophy:** The parser is **tolerant and flexible** - it recognizes multiple format patterns and gracefully skips unrecognized content.

1. **Header Detection** (Flexible patterns)
   - Line matching `/^##\s+Search\s+\d+:\s*/` → Call hierarchy format
   - Line matching `/^##\s+P-\d+:/` → Navigation map partition format  
   - Line matching `/^##\s+(.+)/` → Generic section (fallback)
   - **Behavior:** Any level-2 header creates a root tree node; unmatched headers are skipped

2. **Metadata Extraction** (Optional, format-specific)
   - `**Namespace:**` line captures namespace (Format 1)
   - `**Location:**` line extracts file path and line number from markdown link (Format 1)
   - `**HTTP Attribute:**` line captures attribute text (Format 1)
   - **Behavior:** Missing metadata is tolerated; fields default to empty/undefined

3. **List Item Parsing** (Multiple formats)
   - **Checkbox format:** `- [x] **Name**` → Parse as method node
   - **Pipe format:** `- Name | [link](url) | Layer` → Parse name, link, namespace (layer)
   - **Simple format:** `- [link text](url)` → Extract name and file from link
   - **Behavior:** Parser tries all patterns; unmatched lines are skipped

4. **Hierarchy Building**
   - Track indentation level (count leading spaces, divide by 2)
   - Child nodes are indented 2+ spaces relative to parent
   - Section headers (`###`) are recognized but don't create nodes
   - **Behavior:** Indentation determines parent-child relationships

5. **Checkbox Parsing** (Optional)
   - `[x]` → checked = true
   - `[ ]` → checked = false
   - No checkbox → checked = true (default)
   - **Behavior:** Preserves pruning/selection state when present

6. **Node Type Detection** (Pattern-based)
   - Starts with `- 👇` → comment node (isComment: true)
   - Starts with `- [x] 📍` or `- [ ] 📍` → reference location (isReference: true)
   - Contains `**Name**` → method/class node
   - Contains `| [link](url) |` → navigation item
   - **Behavior:** First matching pattern wins; defaults to generic node

7. **Link Parsing** (Flexible extraction)
   - Patterns: `[text](path:line)`, `[text](path#Lline)`, `[text](path)`
   - Parse line numbers (convert to zero-based for storage)
   - Parse character positions from `:character` suffix (if present)
   - **Behavior:** Extracts file path from URL, line defaults to 0 if missing

8. **HTTP Attribute Extraction** (Format 1 only)
   - Pattern: `[[attribute]]` at end of method name
   - Remove from name, store in httpAttribute field
   - **Behavior:** Only applies to checkbox format items

9. **Error Handling** (Graceful degradation)
   - Unrecognized lines → skipped silently
   - Malformed links → file/line default to empty/0
   - Invalid indentation → attached to last valid parent
   - **Philosophy:** Never fail due to unexpected content

### Round-Trip Guarantees

To ensure data integrity across conversions:

1. **Preserved Fields**
   - name, namespace, file, line, character
   - checked state for all nodes
   - httpAttribute, isComment, isReference, referenceType
   - Complete tree hierarchy and reference locations

2. **Reconstructed Fields**
   - exportedAt (regenerated on export)
   - expandedNodes (UI state, not in markdown)

3. **Normalization**
   - File paths: preserve as-is (absolute or relative)
   - Line numbers: markdown displays one-based, stores zero-based
   - Whitespace: markdown indentation is semantic, JSON is not

---

## Implementation Guidelines

### For Applications Generating Upstream Files

1. **Always include required fields**: name, file, line, checked
2. **Use ISO 8601 timestamps** for exportedAt
3. **Zero-base line numbers** in JSON
4. **Preserve checkbox state** for all nodes
5. **Maintain tree hierarchy** (parent → children → referenceLocations)

### For Applications Consuming Upstream Files

1. **Validate structure** before parsing (check for required fields)
2. **Handle missing optional fields** gracefully (use defaults)
3. **Support both absolute and relative paths**
4. **Normalize line numbers** (convert display ↔ storage)
5. **Preserve unknown fields** during round-trip if possible

### Testing Round-Trip Conversion

To verify implementation correctness:

```typescript
// Test: JSON → Markdown → JSON
const originalJson = loadUpstreamJson("test.upstream.json");
const markdown = convertJsonToMarkdown(originalJson);
const reconstructedJson = convertMarkdownToJson(markdown);
assert.deepEqual(originalJson, reconstructedJson);

// Test: Markdown → JSON → Markdown
const originalMd = loadMarkdown("test.upstream.md");
const json = convertMarkdownToJson(originalMd);
const reconstructedMd = convertJsonToMarkdown(json);
assert.equal(normalizeMarkdown(originalMd), normalizeMarkdown(reconstructedMd));
```

---

## Version History

- **1.0** (2026-08-26) - Initial specification with JSON and Markdown formats

---

## See Also

- Extension documentation: [README.md](./README.md)
- Package metadata: [package.json](./package.json)
- Source code: [src/extension.ts](./src/extension.ts)
