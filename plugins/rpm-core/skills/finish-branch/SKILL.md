---
name: finish-branch
description: Wraps up a feature branch after its PR merges or when merging it locally. Merges or verifies the merge, folds its changelog entries, updates the ticket, offers a release, and deletes the branch locally and on the remote. Use when the user says a branch or PR is merged, done, or ready to clean up.
disable-model-invocation: true
argument-hint: "[branch]"
license: MIT
metadata:
  sources: "obra/superpowers finishing-a-development-branch"
---

# Finish branch

The target is the branch in `$ARGUMENTS`, or the current branch if none is given.
The base is the repo's default branch: `git symbolic-ref --short refs/remotes/origin/HEAD`, minus the `origin/` prefix.

## Checklist

```
- [ ] 1. Branch is merged into the base
- [ ] 2. Local base updated
- [ ] 3. Changelog folded
- [ ] 4. Ticket updated
- [ ] 5. Release offered
- [ ] 6. Branch deleted locally and on the remote
```

## 1. Merged?

- If there is a PR: `gh pr view <branch> --json state,mergedAt,mergeCommit`.
- If there is no PR, and the user wants a local merge: run the project's checks on the branch first, then `git switch <base> && git merge --no-ff <branch>`. If it conflicts, use the `resolve-conflicts` skill.
- If the branch isn't merged and the user didn't ask to merge it, stop and say so.

## 2. Update the base

`git switch <base> && git pull --ff-only`.

## 3. Changelog

With release-please, skip this step: the changelog comes from commits.
Otherwise, if `CHANGELOG.md` has a `## [Unreleased] <branch>` section, fold it into `## [Unreleased]` following the `changelog` skill, then commit `docs(changelog): fold <branch> entries`.

## 4. Ticket

If the project uses a tracker (see its CLAUDE.md or AGENTS.md, or a ticket id in the branch name such as `feat/abc-123-...`), update or close the ticket with whatever tool the project uses. If there's no tracker, skip this step.

## 5. Release

If the merge contains user-visible changes (`feat`, `fix`, or breaking), ask whether to cut a release now with the `release` skill (with release-please: offer to review the release PR). Skip this for chore-, CI-, or docs-only merges.

## 6. Clean up

Pushing to the remote and deleting branches both need confirmation:

```bash
git push origin <base>               # only if step 2 or 3 created local commits
git branch -d <branch>               # -d, not -D: refuses if unmerged
git push origin --delete <branch>    # skip if the remote branch is already gone
git fetch --prune
```

Squash-merged PRs make `git branch -d` refuse. Use `-D` only after step 1 confirmed the PR merged, and say that you're doing it.
Finally, report the base commit, what was deleted, and anything you skipped.
