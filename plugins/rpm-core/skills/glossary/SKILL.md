---
name: glossary
description: Maintains docs/GLOSSARY.md as the project's single vocabulary. It picks one term per concept and lists the aliases to avoid. Use when domain terms come up that could be ambiguous, when naming new concepts, types, or tables, or when code, docs, and conversation use different words for the same thing.
license: MIT
metadata:
  sources: "mattpocock/skills domain-modeling (CONTEXT.md idea)"
---

# Glossary

`docs/GLOSSARY.md` is the project's vocabulary. Create it the first time a term needs pinning down. Don't fill it in ahead of time.
Read it before naming new domain concepts, and use its terms in code, docs, and replies.

## When to add a term

- A domain-specific word that general engineering vocabulary doesn't cover.
- A word used in two different senses, or two words used for one concept.
- A deliberate distinction that's easy to blur (for example "cancellation guidance" vs "auto-cancel").

## Format

```markdown
# Glossary

## Terms

**Renewal**:
The recurring billing date of a tracked subscription.
_Avoid_: due date (ambiguous with one-off bills)
```

## Rules

- Be opinionated: pick one term, list the rejected aliases under `_Avoid_`, and then use the picked term everywhere, including inside other definitions.
- Keep each definition to one or two sentences: what the thing is, not how it's built.
- Group terms under `##` headings only once natural clusters appear.
- Revise definitions in place when understanding changes, rather than adding a second entry next to the old one.
