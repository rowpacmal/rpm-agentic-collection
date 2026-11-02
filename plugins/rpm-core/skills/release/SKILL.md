---
name: release
description: Cuts a versioned release. Picks the SemVer bump, updates every version file in lockstep, turns the changelog's Unreleased section into a version, commits, and tags. Pushes only after confirmation. Use when the user asks to cut, tag, or ship a release or bump the version.
disable-model-invocation: true
argument-hint: "[major|minor|patch|X.Y.Z]"
license: MIT
metadata:
  sources: "semver.org"
---

# Release

Run this only when the user asks. Never bump versions as a side effect of other work.
If the repo uses release-please (`release-please-config.json`, or a workflow using `release-please-action`), don't bump or tag by hand. Follow the `release-please` skill, which releases by merging the release PR.
Project instructions (CLAUDE.md, AGENTS.md) may add release steps, such as migrations or deploy order. Follow them.

## Checklist

Copy this list and tick items off as you go:

```
- [ ] 1. Preflight: on the release branch (usually main), clean tree, up to date with remote
- [ ] 2. Bump type confirmed
- [ ] 3. All version files updated to the same X.Y.Z
- [ ] 4. CHANGELOG.md cut
- [ ] 5. Checks pass
- [ ] 6. Release commit and annotated tag created
- [ ] 7. User confirmed push; commit and tag pushed together
```

## 1. Preflight

`git status`, `git fetch`, `git log --oneline @{u}..` and `..@{u}`. Stop and report if the tree is dirty or behind.

## 2. Bump type

SemVer `MAJOR.MINOR.PATCH`:
- breaking change → major
- new backward-compatible feature → minor
- fix only → patch

While the version is `0.y.z`, a breaking change bumps minor.
Read the Unreleased changelog entries and the commits since the last tag (`git describe --tags --abbrev=0`) to propose a bump. If the user didn't state one, confirm it before editing anything.

## 3. Version files

Find every file that carries the project version and bump them all to the same value in one commit:

```bash
git ls-files | grep -E '(^|/)(package\.json|app\.json|app\.config\.(js|ts)|pyproject\.toml|Cargo\.toml|build\.gradle(\.kts)?|pubspec\.yaml|plugin\.json|marketplace\.json|version\.txt|VERSION)$'
```

- Only bump the project's own version field. Leave dependency versions alone.
- In a monorepo, check whether packages are versioned together or independently (look at past release commits) and follow that.
- Expo: keep `app.json` `expo.version` equal to `package.json`. Bump `ios.buildNumber` and `android.versionCode` only if the project does so in past releases.
- Afterwards, grep the old version string to confirm nothing was missed.

## 4. Changelog

If `CHANGELOG.md` exists:
- Rename the unscoped `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` (today's date).
- Add a fresh empty `## [Unreleased]` above it.
- Update the compare links at the bottom to match the existing format.
- Fold any leftover branch-scoped Unreleased sections first (see the `changelog` skill).

## 5. Checks

Run the project's lint, typecheck, test, and build commands, whichever exist. Don't release on red.

## 6. Commit and tag

```bash
git add <version files> CHANGELOG.md
git commit -m "chore(release): vX.Y.Z"
git tag -a vX.Y.Z -m "vX.Y.Z"
```

Match the tag prefix the repo already uses (`v1.2.3` vs `1.2.3`).

## 7. Push

Pushing is visible to others and may trigger deploys, so ask first.
Once confirmed, push the commit and the tag together in the same step:

```bash
git push origin HEAD && git push origin vX.Y.Z
```

Don't leave a tag only on the local machine.

Never start paid or quota-limited builds or deploys (EAS builds, store submissions, cloud deploys) without explicit approval for that specific run.
Offer `gh release create vX.Y.Z --notes-from-tag` or changelog-based notes if the project uses GitHub releases.
