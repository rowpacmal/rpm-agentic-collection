# release-please setup

Uses the manifest config (two files plus a workflow), which works for single packages and monorepos.

## 1. Pick the release type

| Project | `release-type` | Updates |
|---|---|---|
| Node / TypeScript | `node` | `package.json`, lockfile |
| Expo app | `expo` | `package.json` and `app.json` versions |
| Python | `python` | `pyproject.toml` (and related files) |
| Rust | `rust` | `Cargo.toml` |
| Go | `go` | changelog and tags only |
| Anything else | `simple` | `version.txt` |

Version strings in other files (an `app.config.ts`, a constants file) need help:
- JSON, YAML, or TOML: an `extra-files` entry with `"type": "json"` (or `yaml`, `toml`) and a `jsonpath`.
- Any text file: a `// x-release-please-version` comment at the end of the line holding the version, and the file listed in `extra-files`.

## 2. Config files

`release-please-config.json`:

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "release-type": "node",
  "bump-minor-pre-major": true,
  "include-component-in-tag": false,
  "packages": {
    ".": {
      "extra-files": [
        { "type": "json", "path": "app.json", "jsonpath": "$.expo.version" }
      ]
    }
  }
}
```

Drop `extra-files` if the release type already covers every version file.

`.release-please-manifest.json`, holding the current version (check `package.json` and the latest tag):

```json
{ ".": "1.4.0" }
```

Monorepo: one `packages` entry per package path, each with its own `component`. Add the `node-workspace` plugin to bump dependents. Add the `linked-versions` plugin when packages must share one version.

If the repo already has a hand-written `CHANGELOG.md`, keep it. release-please adds new versions on top.

## 3. Workflow

`.github/workflows/release-please.yml`:

```yaml
name: release-please
on:
  push:
    branches: [main]
permissions:
  contents: write
  pull-requests: write
  issues: write
jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        id: release
      # Optional follow-up, only when a release was created:
      # - if: ${{ steps.release.outputs.release_created }}
      #   run: echo "publish ${{ steps.release.outputs.tag_name }}"
```

Pin the action to a full commit SHA if the project pins its other actions.

PRs opened with the default `GITHUB_TOKEN` don't trigger other workflows, so CI won't run on the release PR. If branch protection requires checks, pass a fine-grained PAT or GitHub App token as `token:`. The user creates that secret, not you.

## 4. Repo settings

- Allow squash merging, with the PR title as the default commit message:
  `gh api -X PATCH repos/{owner}/{repo} -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=BLANK`
  This changes repo settings, so ask first.
- Optional: a CI check that PR titles are Conventional Commits, so a bad title can't reach main.

## 5. Hand-off to the team

Add a line to the project's `AGENTS.md`: releases are managed by release-please. PR titles must be Conventional Commits, and nobody edits `CHANGELOG.md` or versions by hand.
