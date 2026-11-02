---
name: changelog
description: Updates CHANGELOG.md in Keep a Changelog format, with a separate Unreleased section per branch so parallel branches don't conflict. Use when a user-visible change lands (feature, fix, breaking change, removal), when a branch merges and its entries need folding, or when the user asks to update the changelog.
license: MIT
metadata:
  sources: "keepachangelog.com 1.1.0"
---

# Changelog

If the repo uses release-please (`release-please-config.json`, or a workflow using `release-please-action`), don't edit `CHANGELOG.md`. It is generated from commits, so follow the `release-please` skill instead.

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
If the project has no changelog, create one only when the user asks.

## What gets an entry

Changes that affect people who use, build, or deploy the project: features, fixes, breaking changes, removals, security fixes.
Skip internal refactors, CI-only changes, and chores that change nothing visible. When unsure, ask.

## While on a branch

One shared `## [Unreleased]` section causes merge conflicts, so each branch writes under its own heading.
Put it at the top, under the intro and above any released versions:

```markdown
## [Unreleased] feat/magic-link-auth

### Added

- Magic-link sign-in on the login screen.
```

- Subsections, in this order: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- One sentence per entry. Say what changed, not why. Link an ADR or PR for the why.
  Words like "so", "because", or "which" usually mean reasoning crept in: `Session timeout changed from 15 to 30 minutes.`, not `…to 30 minutes so users aren't logged out mid-form.`
- Name the user-visible thing, not internal files, components, or functions.
- If a change is reverted or reworked before release, keep one entry describing the final behavior.
- Only edit the section for the current branch (`git branch --show-current`). Never touch another branch's section.

## When the branch merges

Do this as part of the merge, not later:

1. Move the branch's entries into the single unscoped `## [Unreleased]` section.
   - If none exists, drop the branch name from the heading.
   - If one exists, merge matching subsections and remove the empty branch heading.
2. Commit as `docs(changelog): fold <branch> entries`.

## At release time

Turning `[Unreleased]` into a version number is the `release` skill's job. Don't do it here.

## File skeleton

```markdown
# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-01-31

### Added

- First release.

[Unreleased]: https://github.com/<owner>/<repo>/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/<owner>/<repo>/releases/tag/v0.1.0
```
