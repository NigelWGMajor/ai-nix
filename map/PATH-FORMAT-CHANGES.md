# Map Skill Path Format Changes

## Summary of Changes

The map skill has been updated to use **absolute file:/// URLs** instead of relative paths in both `map.md` and `map.upstream.md` output files.

---

## 1. File Path Format Changes

### Before (Relative Paths)
```markdown
- ContentController.CreateContent | [Controllers/ContentController.cs:42](Controllers/ContentController.cs#L42) | Controller
```

### After (Absolute file:/// URLs)
```markdown
- ContentController.CreateContent | [Controllers/ContentController.cs:42](file:///C:/source/project/Controllers/ContentController.cs#L42) | Controller
```

### Path Format Specification

**Display text**: Shortened relative path for readability
- Example: `Controllers/ContentController.cs:42`

**URL**: Absolute file:/// protocol
- Windows: `file:///C:/source/project/Controllers/ContentController.cs#L42`
- Linux: `file:///home/user/project/src/file.py#L15`
- macOS: `file:///Users/username/project/src/file.swift#L20`

**Key points**:
- Use forward slashes on all platforms (not backslashes)
- Use three slashes after `file:` (not two)
- URL-encode spaces: `Stored Procedures` becomes `Stored%20Procedures` in the URL part
- Use `#L` prefix for line numbers (GitHub-style)
- Line numbers are 1-based

---

## 2. Title/Prefix Determination (Name Field)

The **Name** field in the pipe-delimited format (`Name | [link](url) | Layer`) is extracted from code analysis:

### For Methods
**Format**: `ClassName.MethodName`

**Examples**:
- `ContentController.CreateContent`
- `UserService.GetUserById`
- `TagsOrchestrator.FindTagsAsync`

**Extraction**:
1. From `search_graph()` results → qualified name field
2. From `grep -n "class ClassName"` → parse class and method names
3. From Read tool → manual parsing of source code

### For Stored Procedures
**Format**: `ProcedureName` (no class prefix)

**Examples**:
- `Users_Select`
- `Content_Insert`
- `BulkUpsert`

**Extraction**:
1. From file name (e.g., `Users_Select.sql`)
2. From `CREATE PROCEDURE` statement in SQL file
3. From database schema analysis

### For Classes
**Format**: `ClassName`

**Examples**:
- `ContentService`
- `UserRepository`
- `AuthenticationMiddleware`

---

## 3. Complete Format Example

### Pipe-Delimited Format (Code Only)
```markdown
Name | [DisplayPath:Line](file:///AbsolutePath#LLine) | Layer
```

**Three required fields**:
1. **Name**: Component identifier (see section 2 above)
2. **Link**: Markdown link with display text and absolute URL
3. **Layer**: Code type (Controller, Service, Repository, SP, Orchestrator, etc.)

### Document Format (No Pipes)
```markdown
- [filename.md](file:///C:/project/docs/filename.md#L15)
```

---

## 4. Implementation Details

### Path Resolution
```bash
# Get repository root
PATH_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

# Convert to absolute file:/// URL
# Windows: file:///C:/source/project/...
# Linux:   file:///home/user/project/...
```

### Name Extraction from search_graph()
```javascript
// search_graph returns qualified names
{
  "name": "CreateContent",
  "qualified_name": "ContentController.CreateContent",
  "start_line": 42,
  "file": "/path/to/Controllers/ContentController.cs"
}

// Use qualified_name as the Name field
Name = "ContentController.CreateContent"
```

### Name Extraction from grep
```bash
# Find class and method
grep -n "class ContentController" file.cs
grep -n "public.*CreateContent" file.cs

# Combine: ClassName.MethodName
Name = "ContentController.CreateContent"
```

---

## 5. Updated Files

1. **map/SKILL.md** - Updated path resolution, link format, examples
2. **map/scripts/init_instance.py** - Updated UPSTREAM_TEMPLATE

---

## 6. Migration Notes

**Existing map outputs** with relative paths will continue to work but are not in the new format.

**New map runs** will automatically generate absolute file:/// URLs.

**Upstream extension compatibility**: Ensure your Upstream extension supports both:
- `file:///` protocol URLs
- `#L` line number format
- URL-encoded spaces in paths

---

## 7. Complete Examples

### Windows Example
```markdown
## Content Creation Flow

### Controller Layer
- ContentController.CreateContent | [Controllers/ContentController.cs:42](file:///C:/source/Degreed/trunk/Degreed.Web.vNext/Controllers/ContentController.cs#L42) | Controller

### Service Layer
- ContentService.ValidateAndCreateAsync | [Services/ContentService.cs:89](file:///C:/source/Degreed/trunk/Degreed.Core/Services/ContentService.cs#L89) | Service

### SQL Layer
- Content_Insert | [SqlDb/Stored Procedures/Content_Insert.sql:8](file:///C:/source/Degreed/trunk/Degreed.SqlDb/dbo/Stored%20Procedures/Content_Insert.sql#L8) | SP
```

### Linux Example
```markdown
## API Flow

### Controller Layer
- UserController.GetUser | [controllers/user.py:25](file:///home/user/project/src/controllers/user.py#L25) | Controller

### Service Layer
- UserService.find_by_id | [services/user.py:42](file:///home/user/project/src/services/user.py#L42) | Service
```

---

## 8. Testing Checklist

- [ ] Verify absolute paths on Windows (file:///C:/...)
- [ ] Verify absolute paths on Linux (file:///home/...)
- [ ] Verify absolute paths on macOS (file:///Users/...)
- [ ] Verify URL encoding of spaces in paths
- [ ] Verify Name extraction for classes
- [ ] Verify Name extraction for methods (ClassName.MethodName)
- [ ] Verify Name extraction for stored procedures
- [ ] Verify links are clickable in VS Code
- [ ] Verify links work in Upstream extension
- [ ] Verify line numbers are accurate (not default :1)
