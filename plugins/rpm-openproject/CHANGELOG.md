# Changelog

## [0.2.0](https://github.com/rowpacmal/rpm-agentic-collection/compare/rpm-openproject-v0.1.1...rpm-openproject-v0.2.0) (2026-11-09)


### Features

* **rpm-openproject:** add ticket skill to work a work package end to end ([#3](https://github.com/rowpacmal/rpm-agentic-collection/issues/3)) ([5be44e7](https://github.com/rowpacmal/rpm-agentic-collection/commit/5be44e735ac7f0b0042869991bdd2d4fa6a2085f))

## [0.1.1] - 2026-11-02

### Changed

- Remove private project provenance from skill metadata.

## [0.1.0] - 2026-11-02

### Added

- `openproject` skill and helper script for any OpenProject instance via API v3, configured per project (`.env.local`) or per user (`~/.config/openproject/env`). No delete path, and a read-only switch.
