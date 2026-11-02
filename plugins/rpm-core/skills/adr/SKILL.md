---
name: adr
description: Records an architecture decision record (ADR) in docs/adr/ when a decision with lasting consequences is made, such as a library or framework choice, a pattern, or a trade-off. Use when the user decides between technical options, asks to document a decision, or a "why" is being written into commits, comments, or the changelog instead.
license: MIT
metadata:
  sources: "Michael Nygard's ADR format"
---

# Architecture decision records

The reasoning behind decisions lives in `docs/adr/`, not in commit messages, code comments, or the changelog.
Those places should reference the ADR instead (`see docs/adr/0007-use-drizzle.md`).

## When to write one

Write one when a future reader would reasonably ask "why did we do it this way?" Examples:
- choosing a library or framework,
- an architecture pattern,
- ruling something out,
- accepting a real trade-off.

Not for routine implementation details.

## File

`docs/adr/NNNN-kebab-case-title.md`: a 4-digit, zero-padded number, one more than the highest existing number.
Use the project's existing ADR format if there is one. Otherwise use:

```markdown
# NNNN: Title

Date: YYYY-MM-DD

## Status

Proposed | Accepted | Superseded by NNNN | Deprecated

## Context

The situation that forces a decision: constraints and requirements.

## Decision

What was decided, as specific bullet points.

## Alternatives considered

What else was considered, and why it lost.

## Consequences

Trade-offs accepted, follow-up work, and constraints that future changes must respect.
```

## Rules

- Write it concisely. The audience is a future engineer, not the current conversation.
- Never rewrite the Decision of an accepted ADR. To reverse it, write a new ADR and set the old one's Status to `Superseded by NNNN`.
- If the user hasn't confirmed the decision yet, set Status to `Proposed`.
