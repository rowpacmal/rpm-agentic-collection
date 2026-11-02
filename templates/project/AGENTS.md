# PROJECT_NAME

One sentence: what this project is and who it's for.

## Agent priority

Instructions here, and the project's skills, win over default behavior.
Check for a matching skill before acting.

## Structure

- `src/`: what lives here
- `docs/adr/`: architecture decision records

## Commands

- Install: `TODO`
- Dev: `TODO`
- Lint / typecheck / test / build: `TODO`

## Conventions

- Commits: Conventional Commits, one subject line, no body, no attribution.
- Changelog: `CHANGELOG.md`, with branch-scoped `[Unreleased] <branch>` sections that get folded on merge.
- Decisions: `docs/adr/`. The "why" doesn't go in commits or comments.
- Vocabulary: `docs/GLOSSARY.md`.
- Work tracking: TODO (Linear / GitHub Issues / none). Branches: `type/<ticket-id>-short-slug`.

## Release

- Version files: TODO (e.g. `package.json`, `app.json`)
- Extra steps: TODO (e.g. run migrations before pushing the tag)

## Never

- Start paid or quota-limited builds or deploys (EAS, store submits, cloud deploys) without explicit approval each time.
- Commit secrets or `.env` files.
