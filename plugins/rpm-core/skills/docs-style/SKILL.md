---
name: docs-style
description: Writing rules for Markdown docs, READMEs, and the placement of reasoning. Docs stay concise and operational, and each kind of "why" goes to one home (ADR, PR description, code comment, or changelog). Use when writing or editing Markdown or code comments.
paths: "**/*.md"
user-invocable: false
license: MIT
metadata:
  sources: "Original rpm workflow guidance"
---

# Docs style

- Keep it concise and operational: commands, file paths, and examples over abstract prose.
- Write for a reader who arrives cold. Define terms on first use, or link to the glossary.
- Update `README.md` when you add top-level commands, setup steps, or architecture layers.
- Never document behavior that the code or tests contradict. Fix the doc or flag the mismatch.
- Don't add speculative structure (empty sections, TODO headings) for needs that don't exist yet.
- When a change renames or removes a feature, command, env var, file, route, or UI label, search the docs, README, and agent files for the old name and fix every hit in the same change.

## Where reasoning goes

| Kind of "why" | Home |
|---|---|
| Lasting technical decision | ADR in `docs/adr/` (see the `adr` skill). Elsewhere, link it |
| Reasoning specific to one change | PR description. The commit stays a subject line |
| Non-obvious code behavior | A short code comment, only where the code can't speak for itself |
| What changed for users | One factual line in `CHANGELOG.md` |

No narration in comments of what was tried, discussed, or considered.
