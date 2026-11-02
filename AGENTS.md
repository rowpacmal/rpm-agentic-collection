# rpm-agentic-collection

This repo is a Claude Code plugin marketplace (`rpm`) of reusable skills and hooks. See [README.md](README.md).

## Layout

- `.claude-plugin/marketplace.json`: the catalog. Plugin entries use relative `source` paths. Third-party entries are pinned to a reviewed `sha`.
- `plugins/<plugin>/`: `.claude-plugin/plugin.json`, `skills/<skill>/SKILL.md`, `hooks/hooks.json`, `scripts/`, `evals/`.
- `templates/project/`: starter files that `scripts/init-project.sh` copies into projects.
- `tests/`: unit tests for hook scripts.
- `docs/`: tracked source links.

## Commands

- `scripts/validate.sh`: run before every commit. It runs the skill linter, hook tests, and `claude plugin validate`.
- `cd plugins/<plugin> && claude plugin eval . --runs 1 --ablation none`: run evals. This costs model usage, so run only the cases you touched (`--case`, `--tag`).

## Writing skills

Rules:

- Write our own text. Credit what inspired a skill in `metadata.sources`. Copy upstream text only from MIT/Apache sources.
- Skill names are plain lowercase-hyphen (`commit`, not `rpm-commit`), unique across all plugins, and match the folder.
- The description is in the third person: what the skill does, then "Use when …" with the words users actually type. It must stay under 1024 characters.
- Keep the body under 500 lines, with no background the model already knows. Detail goes in `references/` (one level deep).
- Never include private project or organization names, internal skill identifiers, or local project paths in public files, including source credits, roadmaps, examples, and changelogs. Describe private inspiration generically; retain public third-party attribution.
- Keep skills generic. Project specifics (scopes, trackers, deploy steps) belong in each project's `AGENTS.md`, and skills tell the agent to follow those.
- Set `disable-model-invocation: true` for skills with side effects (release, branch cleanup).
- Make path-scoped rules background skills (`paths:` plus `user-invocable: false`). Rules that must always hold become hooks.
- Hooks are stdlib Python or POSIX shell, fail open on bad input, and come with tests in `tests/`.
- Each new skill gets at least a trigger eval and a should-not-trigger eval. Prefer free graders (`regex`, `tool_used`, `file_exists`) over `llm`.

## Releasing a plugin change

Users only receive a change when the plugin's `version` changes. In the same commit:
1. Bump `version` in `plugins/<plugin>/.claude-plugin/plugin.json` (SemVer).
2. Add an entry to `CHANGELOG.md` under the plugin's heading.

## Commits

Conventional Commits, one subject line, no body, no attribution. Scopes: the plugin name (`rpm-core`, `rpm-design`, `rpm-security`, `rpm-testing`, `rpm-openproject`), or none for repo-wide changes.
