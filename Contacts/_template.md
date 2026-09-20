# Contacts note guide

Purpose: Role-based responsibilities without personal details. This guide is **not** a live note and is excluded from `Update`.

## Completed synthetic example

Read [BUILDING_Roles.md](BUILDING_Roles.md) for a fully populated note in this category. Copy its structure into a separate private working folder and replace every synthetic field with a verified fact. Classify the new note before use: keep real `local_only` notes under `local_only/`, and use `cloud_ok` only after a person approves cloud processing. Keep source originals outside the AI-readable folder.

## Required structure

```yaml
---
object: U01
as_of: 2026-09-20
status: current
ai_access: local_only
source: Synthetic example
---
```

Add a descriptive title, a `## Summary` of at most three lines, and the category-specific fields shown in the linked example. Add `deadlines:` only for genuine follow-up dates. Use `BUILDING` for shared topics and a unit ID for unit-specific topics. A real unknown can be marked `OPEN: <what is missing>` in a private copy.
