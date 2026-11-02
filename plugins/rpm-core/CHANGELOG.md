# Changelog

## [0.3.1] - 2026-11-02

### Changed

- Remove private project provenance from skill metadata.

## [0.3.0] - 2026-11-02

### Added

- Skills: `tdd` (test-first loop, good-test reference), `release-please` (PR titles as changelog, release PR, overrides, setup), `pull-request` (Conventional Commit titles, what/why/verified description), `handoff` (session handoff note), `grill` (interview in rounds to settle a plan), `dependency-review` (need, trust, fit, and consistency checks).
- `verifier` subagent: independent PASS/FAIL check of a finished change with evidence.

### Changed

- `coding-guidelines`: test-first for behavior changes, check UIs and APIs by running them, and use `verifier` for multi-step work.
- `changelog`, `release`, and `finish-branch` defer to `release-please` when a repo uses it.
- `changelog`: one sentence per entry, no reasoning clauses, and one entry for changes reworked before release.
- `docs-style`: fix every mention of a renamed or removed name in the same change.
- `commit-msg` hook allows a release-please `Release-As:` footer.

## [0.2.0] - 2026-11-02

### Added

- Skills: `code-review` (spec and quality axes, severity labels, code-smell reference), `plan` (verifiable plan, optional plan doc, retired into an ADR on merge), `debug` (feedback loop first, ranked hypotheses).

### Changed

- `commit` triggers on "what should I commit" and replies with just the message.

## [0.1.0] - 2026-11-02

### Added

- Always-on `coding-guidelines`, injected by a SessionStart hook.
- Skills: `commit`, `changelog`, `release`, `finish-branch`, `resolve-conflicts`, `adr`, `glossary`, `docs-frontmatter`, `docs-style`.
- Optional `commit-msg` git hook for single-line Conventional Commits.
