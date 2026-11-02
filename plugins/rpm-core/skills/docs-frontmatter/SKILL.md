---
name: docs-frontmatter
description: Adds minimal YAML frontmatter (title, description, optional updated date) to Markdown files under docs/, so agents and people can tell from one line whether to open a file. Use when creating or editing files in docs/.
paths: "docs/**/*.md"
user-invocable: false
license: MIT
metadata:
  sources: "Original rpm workflow guidance"
---

# Docs frontmatter

Every Markdown file under `docs/` starts with:

```yaml
---
title: One-line title
description: Read when <situation>. One sentence on what's inside.
updated: YYYY-MM-DD
---
```

- `title` and `description` are required. Write `description` like a skill description: lead with when to read the file.
- Add `updated` only for files that go stale (session logs, status, roadmaps), and refresh it whenever you edit the file.
- ADRs keep their `## Status` section. Frontmatter adds to it and doesn't replace it.
- Don't add `tags`, `author`, `category`, or other fields until a real need for them exists.
- Skip files whose format forbids frontmatter or that a tool generates.
