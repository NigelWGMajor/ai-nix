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

### Structure

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

### Syntax Rules

1. **Headers**
   - `# Upstream References Report` - Document title (required)
   - `Generated: <timestamp>` - Generation timestamp (optional, ignored on import)
   - `---` - Horizontal rule separates root searches (optional)
   - `## Search N: <MethodName>` - Root search heading

2. **Metadata Lines**
   - `**Namespace:** <value>` - Namespace declaration
   - `**Location:** [<link>](<url>)` - File location with markdown link
   - `**HTTP Attribute:** <value>` - HTTP attribute annotation

3. **Checkboxes**
   - `- [x]` - Checked item
   - `- [ ]` - Unchecked item
   - Checkboxes preserve pruning/selection state

4. **Indentation**
   - Each nesting level adds 2 spaces
   - Reference locations are indented 2 spaces deeper than their parent

5. **Special Nodes**
   - `- 👇 <CommentText>` - Comment node (no checkbox)
   - `- [x] 📍 <FileName>:<Line>` - Reference location node
   - Bold text (`**Name**`) indicates method/class nodes

6. **Links**
   - Markdown links use format: `[text](path:line)` or `[text](path#Lline)`
   - Links may be absolute or relative file paths

### Example Markdown

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

---

## Parsing Rules

### JSON Parsing

1. Standard JSON parser with UTF-8 encoding
2. All fields are case-sensitive
3. Missing optional fields default to undefined/null
4. `checked` defaults to `true` if not present
5. Line numbers are zero-based in storage, one-based in display

### Markdown Parsing

1. **Header Detection**
   - Line starting with `## Search N:` begins a new root tree
   - Capture method name after the colon

2. **Metadata Extraction**
   - `**Namespace:**` line captures namespace
   - `**Location:**` line extracts file path and line number from markdown link
   - `**HTTP Attribute:**` line captures attribute text

3. **Hierarchy Building**
   - Track indentation level (count leading spaces, divide by 2)
   - Child nodes are indented 2+ spaces relative to parent
   - Section headers (`### Upstream Callers:`, `### Reference locations:`) are ignored as structural markers

4. **Checkbox Parsing**
   - `[x]` → checked = true
   - `[ ]` → checked = false
   - No checkbox → ignored or comment node

5. **Node Type Detection**
   - Starts with `- 👇` → comment node (set isComment: true)
   - Starts with `- [x] 📍` or `- [ ] 📍` → reference location (set isReference: true)
   - Starts with `- [x] **` or `- [ ] **` → method/class node
   - Extract node name from between `**` markers

6. **Link Parsing**
   - Extract file path from markdown links: `[text](path:line)` or `[text](path#Lline)`
   - Parse line numbers (convert to zero-based for storage)
   - Parse character positions from `:character` suffix

7. **HTTP Attribute Extraction**
   - Pattern: `[[attribute]]` at end of method name
   - Remove from name, store in httpAttribute field

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
