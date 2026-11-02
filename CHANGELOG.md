# Changelog

All notable changes to the `rpm` plugins are documented here, grouped by plugin.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Each plugin has its own [Semantic Versioning](https://semver.org/) version.

## [Unreleased]

## rpm-core 0.3.1 - 2026-11-02

### Changed

- Remove private project provenance from skill metadata.

## rpm-design 0.2.1 - 2026-11-02

### Changed

- Remove private project provenance from skill metadata.

## rpm-openproject 0.1.1 - 2026-11-02

### Changed

- Remove private project provenance from skill metadata.

## rpm-testing 0.1.0 - 2026-11-02

### Added

- `browser-testing` skill: Playwright CLI checks (snapshot, click, fill, screenshot, console, network) and Playwright Test e2e specs.
- `api-testing` skill: curl checks, request-level tests, and local runs of Bruno, Hurl, and Postman collections (Newman without an account).

## rpm-design 0.2.0 - 2026-11-02

### Added

- `mockups` skill: rounds of static HTML design picks on the same content, with a generator harness, a component inventory, screenshot checks, and promotion into the design-system doc.

## rpm-core 0.3.0 - 2026-11-02

### Added

- Skills: `tdd` (test-first loop, good-test reference), `release-please` (PR titles as changelog, release PR, overrides, setup), `pull-request` (Conventional Commit titles, what/why/verified description), `handoff` (session handoff note), `grill` (interview in rounds to settle a plan), `dependency-review` (need, trust, fit, and consistency checks).
- `verifier` subagent: independent PASS/FAIL check of a finished change with evidence.

### Changed

- `coding-guidelines`: test-first for behavior changes, check UIs and APIs by running them, and use `verifier` for multi-step work.
- `changelog`, `release`, and `finish-branch` defer to `release-please` when a repo uses it.
- `changelog`: one sentence per entry, no reasoning clauses, and one entry for changes reworked before release.
- `docs-style`: fix every mention of a renamed or removed name in the same change.
- `commit-msg` hook allows a release-please `Release-As:` footer.

## rpm-security 0.2.0 - 2026-11-02

### Added

- Bash guard asks before deleting Docker volumes (`docker system/volume prune`, `docker volume rm`, `compose down -v`).
- Bash guard asks before printing a local env file (`cat .env`, `grep KEY .env.local`); templates such as `.env.example` are allowed.
- Secret guard asks before any edit to a local env file (`.env`, `.env.*`, `.envrc`).

## rpm-core 0.2.0 - 2026-11-02

### Added

- Skills: `code-review` (spec and quality axes, severity labels, code-smell reference), `plan` (verifiable plan, optional plan doc, retired into an ADR on merge), `debug` (feedback loop first, ranked hypotheses).

### Changed

- `commit` triggers on "what should I commit" and replies with just the message.

## rpm-core 0.1.0 - 2026-11-02

### Added

- Always-on `coding-guidelines`, injected by a SessionStart hook.
- Skills: `commit`, `changelog`, `release`, `finish-branch`, `resolve-conflicts`, `adr`, `glossary`, `docs-frontmatter`, `docs-style`.
- Optional `commit-msg` git hook for single-line Conventional Commits.

## rpm-design 0.1.0 - 2026-11-02

### Added

- Skills: `ui-design` (with floor and AI-tells references), `design-md`.

## rpm-security 0.1.0 - 2026-11-02

### Added

- Bash guard hook: denies catastrophic commands and asks before risky ones.
- Secret guard hook: asks before writing high-confidence secrets into files.

## rpm-openproject 0.1.0 - 2026-11-02

### Added

- `openproject` skill and helper script for any OpenProject instance via API v3, configured per project (`.env.local`) or per user (`~/.config/openproject/env`). No delete path, and a read-only switch.

## Marketplace

### Added

- `security-audit`: upstream cloudflare/security-audit-skill pinned at `c1c8a8c`.
