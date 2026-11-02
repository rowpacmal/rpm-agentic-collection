---
name: pull-request
description: Opens, updates, or squash-merges a GitHub pull request with gh. The title is a Conventional Commit, because squash merges and release-please turn it into the commit and changelog line. The description covers what changed and why, how it was verified, and linked tickets. Use when the user asks to open, create, raise, update, or merge a PR or pull request, or to write a PR title or description.
argument-hint: "[base branch]"
license: MIT
metadata:
  sources: "conventionalcommits.org, release-please docs"
---

# Pull request

## Steps

1. **Check the branch.** `git status`, `git log --oneline <base>..HEAD`, and `git diff <base>...HEAD --stat`. The base is the argument, the project's convention (some use `dev`), or the default branch. Uncommitted work: ask whether it belongs in the PR (the `commit` skill handles it).
2. **Run the checks** the project defines (lint, typecheck, tests). Don't open a PR on red without saying so in the description.
3. **Look for an existing PR:** `gh pr view --json number,title,url,state`. If one exists, update it rather than opening another.
4. **Write the title and description** (below). If the repo has `.github/pull_request_template.md`, fill that in instead of the default layout.
5. **Ask before pushing** and opening the PR, since both are visible to others. Then:
   ```bash
   git push -u origin HEAD
   gh pr create --base <base> --title "<title>" --body-file <file>   # --draft if work is unfinished
   ```
   Use `gh pr edit` to update. Write the body to a temp file to avoid shell-quoting problems.
6. Report the PR URL.

## Merging

Only when the user asks, and confirm first, since merging may publish a release or deploy.
1. Re-read the PR title. With squash merges it becomes the commit on main and the changelog line, so fix it with `gh pr edit --title` before merging.
2. Check that the PR's checks pass: `gh pr checks`.
3. Merge the way the repo allows (squash is usual):
   ```bash
   gh pr merge --squash --delete-branch
   ```
   Don't pass `--subject` or `--body`, so the PR title is used as is and no commit body is added.
4. Update the local default branch: `git switch <base> && git pull`.

## Title

A Conventional Commit subject: `type(scope): subject`, imperative, no trailing period.
When the PR is squash-merged it becomes the only commit on main, and release-please uses it as the changelog entry. Write it for a user reading release notes: `feat(billing): show prorated amount before upgrading`.
If the PR mixes unrelated changes, suggest splitting it.

## Description

```markdown
## What
One or two sentences on the change, from the user's or caller's side.

## Why
The problem or ticket. Link the ticket or issue, and an ADR or plan doc if there is one.

## How it was verified
- Commands run and their result (tests, typecheck, lint).
- Manual checks, with screenshots or a short recording for UI changes.

## Notes for reviewers
Risky spots, follow-ups left out on purpose, migration or deploy steps. Omit if empty.
```

- This is where the reasoning for the change lives, since commits are one line.
- Mark breaking changes with `!` in the title and say what callers must change.
- Link tickets the way the project does (`Closes #123`, or the tracker's ID format from `AGENTS.md`).
- No "generated with" footers or co-author trailers unless the project asks for them.
- Never paste secrets, tokens, or `.env` values, including in logs or screenshots.
