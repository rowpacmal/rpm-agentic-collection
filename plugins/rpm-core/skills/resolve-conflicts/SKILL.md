---
name: resolve-conflicts
description: Resolves an in-progress git merge, rebase, or cherry-pick conflict by working out what each side intended, keeping both intents where possible, and re-running the project's checks before finishing. Use when git reports conflicts or the user asks to fix a merge or rebase.
license: MIT
metadata:
  sources: "mattpocock/skills resolving-merge-conflicts (MIT)"
---

# Resolve conflicts

## 1. Get the state

- `git status`: which operation is in progress (merge, rebase, cherry-pick) and which files conflict.
- `git log --oneline --left-right --merge` (merge), or the rebase todo in `.git/rebase-merge/`.

## 2. Understand both sides

For each conflicting file, read what each side changed and why:

```bash
git diff --name-only --diff-filter=U
git log --oneline -3 --format='%h %s' MERGE_HEAD -- <file>   # theirs (merge)
git log --oneline -3 --format='%h %s' HEAD -- <file>         # ours
```

Read the commit messages, and the linked PR or ticket when the intent isn't clear.
During a rebase, `ours` is the branch being rebased onto and `theirs` is your commit.

## 3. Resolve each hunk

- Keep both intents when they're compatible: a combined change, not one side picked blindly.
- When they truly conflict, follow the stated goal of the merge and note the trade-off in your report.
- Don't add new behavior while resolving.
- Lockfiles: don't hand-merge. Take one side, then regenerate with the package manager (`pnpm install`, `npm install`, `uv lock`, and so on).
- Generated files: regenerate them, don't merge them.
- Ask the user only when the right resolution depends on product intent you can't find.

## 4. Verify

Make sure no conflict markers remain: `git diff --check` and `grep -rn '^<<<<<<<\|^>>>>>>>' -- <files>`.
Then run the project's typecheck, tests, and lint, whichever exist, and fix what the merge broke.

## 5. Finish

`git add <files>`, then `git merge --continue`, `git rebase --continue` (repeat until done), or `git cherry-pick --continue`.
Don't `--abort` unless the user asks.
Report each conflicted file, how you resolved it, and any trade-offs.
