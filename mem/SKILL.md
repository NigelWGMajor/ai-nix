---
name: mem
description: Search markdown notes in the workspace root for content relevant to a user question, then return relevance-ranked matches with date hints, short excerpts, and file:line links for fast triage.
---

# MEM Markdown Recall

> Quick help: if invoked with ? as the only parameter, read guidance.md and display it to the user. Do not run search.
## `new` fresh-run override

When `new` is a standalone invocation keyword (for example, `/nix new <topic>`), start a fresh run. The ordinary word `new` within a topic or other prose does not enable this mode. This reset applies only to prior skill-run artifacts: continue to inspect the existing codebase, user-supplied material, and authoritative systems normally.

Do not inspect, resume, or reuse a prior `.data/` or `.dac/` run. After resolving the exact workspace folder this run would otherwise write into or update, if that folder already exists, first rename it in the same parent using the first unused alphabetic suffix: `<name>-a`, `<name>-b`, ..., `<name>-z`, then `<name>-aa`, and so on. Never overwrite, merge, or archive unrelated folders or folders used solely as read-only inputs. If the fresh run creates a distinct new destination or is read-only, do not rename anything.

The archive move needs the same local-write approval as writing the destination. Report the old and archive paths, then continue as though that run never existed. `new` does not authorize source changes, Git mutations, tests, deployment, Jira, or other remote actions.

Find likely-relevant note content fast.

Pipeline:
Question -> Candidate retrieval -> Relevance scoring -> Compact evidence list

## Purpose

Use this skill when the user asks where something was discussed in notes, wants references for a topic, or needs a quick ranked list of related markdown passages.

## Scope

- Search markdown files under the active workspace root.
- Default file extensions: .md and .markdown.
- Exclude obvious binary/media and dependency folders unless user asks otherwise.
- Read-only behavior: never modify note files.

## Required output format

Return results ordered by relevance (highest first). For each hit include:

1. Rank number.
2. Date (brief): prefer frontmatter date/captured, else infer from filename.
3. One clickable file:line link.
4. Brief excerpt (about 140-220 chars) with query terms preserved.
5. One-line relevance reason.

Use markdown links in this exact style:
[2026/2026-08.md#L123](2026/2026-08.md#L123)

If you cite more than one line from the same file, emit separate links.

## Search workflow

1. Resolve question intent
- Extract core terms and optional synonyms from user wording.
- Keep phrase queries for quoted text.

2. Collect candidates
- First pass: semantic search with one focused query based on user intent.
- Second pass: exact/regex text search across markdown files for key terms.
- Include title/path matches as lightweight signals.

3. Score each candidate

Use a simple additive score:
- +8 exact phrase match.
- +5 heading/title/path match.
- +3 multiple core terms in same line window.
- +2 semantic similarity signal.
- +1 recency boost when dates are available (newer notes win ties).

4. De-duplicate and cap
- Merge near-duplicate hits from the same section.
- Keep top 8 by default (top 12 if user asks for more).

5. Build excerpts
- Pull a compact snippet around the best matching line.
- Keep snippet readable; avoid giant blocks.
- Normalize whitespace and trim.

6. Present with confidence cue
- Add a short lead line such as:
  Found 8 likely matches in markdown notes, ranked by relevance.
- If confidence is low (few weak matches), say so briefly.

## Date extraction rules

Date priority:
1. YAML frontmatter fields: date, captured, updated.
2. Filename patterns: YYYY-MM-DD, YYYY-MM, YY-MM-DD.
3. Parent folder year markers like 2025/ or 2026/.
4. If unknown, display n/a.

Display dates in short ISO form, for example 2026-08 or 2026-08-19.

## Failure and fallback behavior

- If no relevant matches: say no high-confidence hits and suggest 2-4 alternate keywords.
- If only weak matches: still return up to 5 with a low-confidence note.
- If workspace has no markdown files: say so explicitly.

## Constraints

- Do not invent files, line numbers, quotes, or dates.
- Do not return huge raw dumps.
- Keep excerpts short and scan-friendly.
- Respect workspace boundaries; do not search outside root unless user explicitly requests it.

## Example response shape

Found 5 likely matches in markdown notes, ranked by relevance.

1. 2026-08  [2026/2026-08.md#L112](2026/2026-08.md#L112)
Excerpt: Discusses how agent skills should surface ranked evidence with quick snippets before deeper review.
Why relevant: Contains exact phrase plus two related terms in the same section.

2. 2026-07  [nix/2026-07-notes.md#L44](nix/2026-07-notes.md#L44)
Excerpt: Notes on retrieval flow and scoring tradeoffs for note search prompts.
Why relevant: Strong semantic similarity and heading match.
