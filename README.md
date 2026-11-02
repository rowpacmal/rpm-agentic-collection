# rpm-agentic-collection

Reusable agent skills, hooks, and project config, maintained in one place.
This repo is a Claude Code plugin marketplace (`rpm`). The skills follow the open [Agent Skills](https://agentskills.io) format, so other agents can use them too.

## Plugins

| Plugin | What you get |
|---|---|
| `rpm-core` | Always-on coding guidelines (injected at session start), plus skills: `commit`, `pull-request`, `changelog`, `release`, `release-please`, `finish-branch`, `resolve-conflicts`, `code-review`, `plan`, `grill`, `tdd`, `debug`, `dependency-review`, `handoff`, `adr`, `glossary`, `docs-frontmatter`, `docs-style`. Subagent: `verifier` |
| `rpm-design` | `ui-design` (accessibility and craft floor, avoids AI-template tells, web and Expo/React Native), `design-md` (Google's DESIGN.md format), and `mockups` (rounds of HTML design directions to compare before building) |
| `rpm-security` | Hooks: the bash guard (blocks catastrophic commands, asks before risky ones such as force push, `reset --hard`, Docker volume wipes, printing `.env` files, EAS builds, or publishing) and the secret guard (asks before writing API keys or private keys into files, or editing `.env` files) |
| `rpm-testing` | `browser-testing` (Playwright CLI checks and Playwright Test e2e) and `api-testing` (curl, request-level tests, Bruno, Hurl, Postman collections via Newman), so the agent checks the running app instead of guessing |
| `rpm-openproject` | `openproject`: read and update work packages on any OpenProject instance, configured per project (`.env.local`) or per user (`~/.config/openproject/env`). No delete path, and a read-only switch |
| `security-audit` | Upstream [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill), pinned to a reviewed commit |

Plugin skills are namespaced (`/rpm-core:commit`), so they never clash with other plugins or project skills.
`release` and `finish-branch` run only when you call them. The other skills load automatically when relevant.

## Install

### Claude Code: every project on this machine

```
/plugin marketplace add rowpacmal/rpm-agentic-collection
/plugin install rpm-core@rpm
/plugin install rpm-security@rpm
/plugin install rpm-design@rpm        # UI projects
/plugin install rpm-testing@rpm       # browser and API checks
/plugin install rpm-openproject@rpm   # projects tracked in OpenProject
```

### Claude Code: one project, shared with the team

Copy the starter files (`AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`) into the project. Existing files are never overwritten:

```bash
scripts/init-project.sh ~/projects/my-app            # core + security
scripts/init-project.sh ~/projects/my-app --design   # + design (add --testing for rpm-testing)
```

The settings file registers the `rpm` marketplace and enables the plugins. It also turns off commit/PR attribution, pre-approves read-only git commands, and blocks reads of `.env` files.
Anyone who opens the project and trusts the folder is prompted to install. Then fill in the `TODO`s in `AGENTS.md`.

### Other agents (Codex, Cursor, Copilot, OpenCode, …)

```bash
npx skills add rowpacmal/rpm-agentic-collection
```

This installs only the skills. Hooks, including always-on guidelines and the guards, are Claude Code features.

## Updating

- **Users:** run `/plugin marketplace update rpm`, or turn on auto-update under `/plugin` → Marketplaces.
- **Maintainers:** a plugin only reaches users when its `version` changes. release-please bumps versions and writes each plugin's `CHANGELOG.md` from Conventional Commits. Merge its release PR to ship.

## Develop

```bash
scripts/validate.sh                           # skill lint, hook tests, claude plugin validate
claude plugin marketplace add ./ --scope local   # load plugins in place from this checkout
cd plugins/rpm-core && claude plugin eval . --runs 1 --ablation none   # evals (uses model quota)
```

How to write skills here: [AGENTS.md](AGENTS.md). Background and decisions: [docs/](docs/).

## Credits

These skills are our own text, informed by the sources credited in each skill's `metadata.sources`, chiefly:
- [obra/superpowers](https://github.com/obra/superpowers)
- [mattpocock/skills](https://github.com/mattpocock/skills)
- [Nutlope/hallmark](https://github.com/Nutlope/hallmark)
- [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable)
- [google-labs-code/design.md](https://github.com/google-labs-code/design.md)
- Karpathy's notes on LLM coding pitfalls

The full list of tracked sources is in [docs/github-links.md](docs/github-links.md).

MIT licensed.
