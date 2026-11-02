---
name: handoff
description: Writes a handoff note so a fresh session or another person can continue the work. Covers the goal, current state, what's done and verified, next steps, open questions, key files, and gotchas. Saves to the project's session notes if it keeps them (docs/SESSION.md and docs/TASKS.md), otherwise to a temp file. Use when the user says hand off, wrap up, save progress, log progress, update session notes, or the context is about to run out.
argument-hint: "[what the next session will do]"
license: MIT
metadata:
  sources: "mattpocock/skills handoff (MIT)"
---

# Handoff

The reader arrives cold, with none of this conversation. Write what they need to continue without repeating your mistakes.

## Where it goes

- If the project keeps session notes (`docs/SESSION.md`, `docs/TASKS.md`, or what `AGENTS.md` names), update those. Reconcile, don't rewrite.
- Otherwise, write `handoff-<topic>-<YYYY-MM-DD>.md` in the OS temp directory (`${TMPDIR:-/tmp}`). Don't put it in the repo unless asked.
- If the user passed an argument, it says what the next session will focus on. Shape the note around that.

## The note

```markdown
# Handoff: <topic>

**Goal:** <one sentence: what "done" looks like>
**Branch / state:** <branch, last commit, uncommitted changes, anything running>

## Done
- <what was finished, and how it was verified>

## Next
1. <the next concrete step, starting with the very next command or file>

## Open questions
- <decisions waiting on the user, with the options if known>

## Gotchas
- <dead ends already tried and why they failed, surprising behavior, flaky tests>

## Pointers
- <plan docs, ADRs, tickets, PRs, key files with line refs>

## Suggested skills
- <skills the next session should use, e.g. `debug`, `tdd`, `finish-branch`>
```

## Rules

- Only mark something done if it was verified. Say "untested" where it wasn't.
- Point to plans, ADRs, commits, and tickets instead of copying them.
- Include failed approaches. They save the next session the most time.
- Redact secrets, tokens, passwords, and personal data.
- With `docs/TASKS.md`: move finished and verified items to Done, add newly found work to Next, and keep the current focus to 1–3 items. With `docs/SESSION.md`: reset it to its empty template once the work is merged.
- Report the path of the note and a one-line summary.
