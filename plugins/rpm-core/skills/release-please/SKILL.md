---
name: release-please
description: Works with release-please, which builds the changelog, version bumps, tags, and GitHub releases from Conventional Commits on the main branch. Covers PR titles that read well as changelog entries, reviewing and merging the release PR, fixing a wrong entry, forcing a version, and first-time setup. Use when the repo has release-please-config.json or a release-please workflow, or the user mentions release-please, the release PR, or automating releases and changelogs.
license: MIT
metadata:
  sources: "googleapis/release-please and release-please-action docs, conventionalcommits.org"
---

# release-please

release-please watches the main branch. From the Conventional Commits that land there it keeps one open **release PR** with the next version and its changelog. Merging that PR tags the release and creates the GitHub release.

The repo uses it if any of these exist: `release-please-config.json`, `.release-please-manifest.json`, or a workflow using `googleapis/release-please-action`.

## Rules when it's in use

- Commit subjects are the changelog. Never edit `CHANGELOG.md`, version fields, or the manifest by hand, and never create release tags yourself.
- The `changelog` and `release` skills don't apply. Their job moves to commit and PR titles and to the release PR.
- With squash merges (recommended), the **PR title becomes the commit** on main. Write it as a Conventional Commit for the reader of the changelog: `feat(auth): add magic-link sign-in`.
- Pick the type honestly, because it decides what ships:

| Type | Changelog | Version bump |
|---|---|---|
| `feat` | Features | minor |
| `fix` | Bug Fixes | patch |
| `perf`, `revert`, `deps` | Shown | patch |
| `docs`, `chore`, `refactor`, `test`, `build`, `ci`, `style` | Hidden | none |
| any type with `!` (`feat!:`) | Marked breaking | major (minor while 0.x if `bump-minor-pre-major`) |

A user-visible change committed as `chore` disappears from the changelog, and a refactor committed as `feat` adds a fake feature.

## Releasing

1. Find the release PR: `gh pr list --label "autorelease: pending"`.
2. Read its diff: the proposed version, the changelog entries, and the version files it bumps. Check that each entry is a sentence a user understands and the bump matches the changes.
3. Fix problems at the source (see below), not by editing the release PR's changelog by hand. release-please regenerates it on the next push to main.
4. Merging publishes a tag and release, and may trigger deploys. Ask before merging. After merging, check the workflow run and the new tag: `gh run list --workflow <file> -L 1`, `gh release view`.

Never start paid or quota-limited builds or store submissions (EAS and similar) as part of this without explicit approval for that run.

## Fixing the changelog or version

- **Wrong entry from a squash-merged PR:** edit that merged PR's description and add the replacement message. The next run uses it:
  ```
  BEGIN_COMMIT_OVERRIDE
  fix(api): return 404 for unknown subscription ids
  END_COMMIT_OVERRIDE
  ```
  This doesn't work for merge commits.
- **Force a specific version:** an empty commit with a `Release-As` footer. This is the one place a commit gets a second line:
  ```bash
  git commit --allow-empty -m "chore: release 2.0.0" -m "Release-As: 2.0.0"
  ```
- **Something landed with the wrong type:** add the override above, or a follow-up commit with the right type if the PR wasn't squash-merged.

## Setup

Only when the user asks. Details and example files: [references/setup.md](references/setup.md).
