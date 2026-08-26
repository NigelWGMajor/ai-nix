# Jira Integration Reference

## Purpose

Guide DAC coordinators on proper Jira issue creation, field usage, and synchronization with private `.dac/` artifacts.

## Core Principle

**`.dac/` artifacts are private (local file system). Jira is the public, shared source of truth for the team.**

Acceptance criteria, deliverables, and key behavior must be visible in Jira for:
- Developers implementing the work
- Reviewers verifying completeness
- Test automation consuming structured criteria
- PMs tracking progress

## Atlassian MCP Server

All Jira and Confluence access MUST use the Atlassian MCP server tools (prefixed `mcp__atlassian__`). Before the first Atlassian access in a session, verify the server is available by attempting a lightweight call. If the server is unreachable or returns a connection error, do not proceed with Atlassian-dependent operations. Instead, advise the user:

> Could you try restarting the MCP server? You can either:
> 1. Run `! /mcp` in this prompt to check MCP server status
> 2. Use `curl` with your MCP credentials to access the Atlassian API directly

## Jira Issue Structure for DAC Portions

### Description Field

Use the description field for:
- **DAC Portion:** Reference to portion ID (e.g., `P-001`)
- **Deliverables:** Bulleted list of concrete outputs
- **Key Behavior:** Summary of how the feature works
- **Depends on:** Parent Jira issue references
- **See:** Reference to private `.dac/` portion file (for internal team use only)

**Format (Markdown):**
```markdown
**DAC Portion:** P-001

**Deliverables:**
- `FileName.cs` - Purpose
- Unit tests
- Integration tests

**Key Behavior:**
- Feature works this way
- Handles edge cases like this

**Depends on:** ABC-123 (dependency description)

**See:** `.dac/PROJECT-123/portions/P-001.md` for full envelope
```

### Acceptance Criteria Field

**CRITICAL:** Do NOT put acceptance criteria in the description field under a heading. Use the dedicated acceptance criteria custom field.

#### Field Discovery Process

1. **Check for local overrides first:**
   - Read `jira-fields.local.yaml` in the repository root (or workspace root) if it exists.
   - This file is gitignored and contains instance-specific field mappings.
   - If found, use its values instead of running discovery.

2. **If no local overrides, discover manually:**
   - Manually add a test value (e.g., "boo") to the Acceptance Criteria field in Jira UI
   - Fetch the issue with all fields: `getJiraIssue` with `fields=["*all"]`
   - Search response for the test value to identify the field name

3. **Common field patterns:**
   - Varies by Jira instance: `customfield_XXXXX`, `customfield_10XXX`, or native `acceptanceCriteria`

4. **Save discovered fields:**
   - After discovery, offer to write the result to `jira-fields.local.yaml` so it doesn't need repeating.
   - Document in Jira plan as well:
   ```markdown
   **Acceptance Criteria Field:** `customfield_XXXXX`
   ```

#### Atlassian Document Format (ADF)

The acceptance criteria field uses ADF (Atlassian Document Format) with task lists:

**Structure:**
```json
{
  "type": "doc",
  "version": 1,
  "content": [{
    "type": "taskList",
    "attrs": {"localId": "unique-id"},
    "content": [
      {
        "type": "taskItem",
        "attrs": {"localId": "item-1", "state": "TODO"},
        "content": [{"type": "text", "text": "Criterion text here"}]
      },
      {
        "type": "taskItem",
        "attrs": {"localId": "item-2", "state": "TODO"},
        "content": [{"type": "text", "text": "Another criterion"}]
      }
    ]
  }]
}
```

**Key points:**
- `taskItem` content is a direct array with text nodes (NOT wrapped in paragraph)
- Each `taskItem` needs unique `localId` (use sequential: "a1", "a2", etc.)
- `state` is "TODO" for unchecked, "DONE" for checked
- Jira UI renders this as interactive checkboxes

**Example API call:**
```json
{
  "fields": {
    "customfield_XXXXX": {
      "type": "doc",
      "version": 1,
      "content": [{
        "type": "taskList",
        "attrs": {"localId": "ac-list"},
        "content": [
          {
            "type": "taskItem",
            "attrs": {"localId": "c1", "state": "TODO"},
            "content": [{"type": "text", "text": "Unit test passes with valid input"}]
          },
          {
            "type": "taskItem",
            "attrs": {"localId": "c2", "state": "TODO"},
            "content": [{"type": "text", "text": "Integration test verifies end-to-end flow"}]
          }
        ]
      }]
    }
  }
}
```

## Workflow Integration

### Before Creating Portion Envelopes

**Add Jira Organization Review Step** between "Portion Plan Approval" and "Portion Envelope Creation"

Present proposed Jira structure to user:

| Portion | Proposed Jira | Type | Parent | Rationale |
|---------|--------------|------|--------|-----------|
| P-001   | New sub-task | Sub-task | ABC-123 | ... |
| P-002   | New sub-task | Sub-task | ABC-123 | ... |

**Questions to ask:**
1. Should these portions be sub-tasks under a parent story, or peer stories?
2. Is there a natural parent issue for grouping?
3. Should we reuse existing issues or create new ones?
4. What work is in DAC scope vs. handled separately (e.g., frontend, docs)?

**Get explicit approval before proceeding to portion envelope creation.**

### When Creating Jira Issues (R4 Phase)

1. **Discover acceptance criteria field** (if not already known)
   - Use the field discovery process above
   - Document in `05-jira-plan.md`

2. **Create issue with full content in single call:**
   ```javascript
   createJiraIssue({
     summary: "Portion title",
     description: "**DAC Portion:** P-001\n\n**Deliverables:**\n...",
     customfield_XXXXX: { /* ADF task list with acceptance criteria */ }
   })
   ```

3. **Extract acceptance criteria from portion envelope:**
   - Read portion file `portions/P-XXX.md`
   - Locate `## Acceptance and validation` section
   - Transform table rows into ADF task items
   - Map "Criterion" column to task text

### After Creating Jira Issues

**Clean up description field if acceptance criteria were accidentally duplicated there.**

Remove any "**Acceptance Criteria:**" section from description, as it should only be in the dedicated field.

## Portion Envelope Template Updates

Add explicit Jira content section to portion template:

```markdown
## Jira Visibility

**Description content:**
- DAC Portion: P-XXX
- Deliverables: [list from "Outcome and boundaries"]
- Key Behavior: [summary from "Outcome and boundaries"]
- Dependencies: [from "Dependency contract"]

**Acceptance Criteria (for customfield_XXXXX):**
- [Extract from "Acceptance and validation" table]
- [Each criterion becomes one task item]
- [Include test type and proof in criterion text]
```

## Common Mistakes to Avoid

❌ **Wrong:** Putting acceptance criteria in description under a heading
```markdown
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
```

✅ **Right:** Using dedicated `customfield_XXXXX` with ADF format

---

❌ **Wrong:** Using markdown bullet format `- [ ]` 
```json
{"type": "text", "text": "- [ ] Criterion"}
```

✅ **Right:** Using ADF taskItem structure
```json
{
  "type": "taskItem",
  "attrs": {"localId": "c1", "state": "TODO"},
  "content": [{"type": "text", "text": "Criterion"}]
}
```

---

❌ **Wrong:** Wrapping taskItem content in paragraph
```json
{
  "type": "taskItem",
  "content": [
    {"type": "paragraph", "content": [{"type": "text", "text": "Criterion"}]}
  ]
}
```

✅ **Right:** Direct text content in taskItem
```json
{
  "type": "taskItem",
  "content": [{"type": "text", "text": "Criterion"}]
}
```

## Validation Checklist

Before marking Jira integration complete:

- [ ] All portion Jira issues created
- [ ] Description field contains deliverables, key behavior, dependencies, and `.dac/` reference
- [ ] Acceptance criteria in dedicated field (NOT in description)
- [ ] Acceptance criteria use proper ADF task list format
- [ ] Dependency links established between Jira issues
- [ ] Jira keys recorded in portion envelope frontmatter
- [ ] Team can see all acceptance criteria without accessing `.dac/` files

## Reference Implementation

See your workstream for example:
- Portion files: `.dac/ABC-123/portions/P-001.md` through `P-004.md`
- Jira issues: ABC-201, ABC-202, ABC-203, ABC-204
