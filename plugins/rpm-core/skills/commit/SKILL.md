---
name: commit
description: Stages and commits changes as Conventional Commits with a single subject line, no body, and no attribution trailers. Splits unrelated changes into separate commits. Use when the user asks to commit, save work, write or suggest a commit message, or asks what or how to commit.
license: MIT
metadata:
  sources: "conventionalcommits.org"
---

# Commit

Default format, unless the project's own instructions say otherwise:

```
type(scope): subject
```

One line. No body, no footer, no `Co-Authored-By` or other attribution trailers.
A "why" that needs more than a subject goes in the PR description or an ADR, not the commit.
If the repo uses release-please, each `feat`/`fix` subject becomes a changelog line, so write it for users (see the `release-please` skill).

## Steps

1. Run `git status`, `git diff`, and `git diff --staged` to see what changed.
2. Run `git log --oneline -15` to learn the scopes and style already in use, and match them.
3. Group the changes into logical units. Commit unrelated changes separately, staging by path (`git add <paths>`). Avoid `git add -A` unless every change belongs together.
4. Before staging, check for secrets, `.env` files, build output, and stray debug code. Leave them out and mention them.
5. Commit each unit with `git commit -m "<subject>"`.
6. Don't push unless asked.

When asked only for a message, reply with the message in a code block, one per commit. Skip explaining the type or scope, and don't offer alternatives unless asked.

## Type

`feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
For a breaking change, add `!` after the type or scope: `feat(api)!: drop v1 endpoints`.

## Scope

The package, app, or area touched, named as in `git log` (for example `api`, `mobile`, `ci`, `docs`).
Omit the scope when the change is repo-wide or the repo doesn't use scopes.

## Subject

- Imperative mood ("add", not "added"), lowercase start, no trailing period.
- Say what changed, not the story of how.
- Aim for 72 characters or fewer. If it won't fit, the commit is doing too much, so split it.

```
feat(auth): add magic-link sign-in
fix(api): return 404 for unknown subscription ids
chore(deps): bump expo to 57.0.3
docs: add release checklist
```

## Enforcing the format (optional)

`assets/commit-msg` is a git hook that rejects messages with more than one line.
Install it only when the user asks:

```bash
mkdir -p .githooks && cp "<this skill dir>/assets/commit-msg" .githooks/ && chmod +x .githooks/commit-msg
git config core.hooksPath .githooks
```
