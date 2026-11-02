# Changelog

## [0.2.0] - 2026-11-02

### Added

- Bash guard asks before deleting Docker volumes (`docker system/volume prune`, `docker volume rm`, `compose down -v`).
- Bash guard asks before printing a local env file (`cat .env`, `grep KEY .env.local`); templates such as `.env.example` are allowed.
- Secret guard asks before any edit to a local env file (`.env`, `.env.*`, `.envrc`).

## [0.1.0] - 2026-11-02

### Added

- Bash guard hook: denies catastrophic commands and asks before risky ones.
- Secret guard hook: asks before writing high-confidence secrets into files.
