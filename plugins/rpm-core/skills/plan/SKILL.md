---
name: plan
description: Produces a short, verifiable implementation plan before any code is edited. The plan covers assumptions, open questions, files to touch, steps, success criteria, verification commands, and risks. It can be saved as a plan doc and tracked to completion. Use when starting a non-trivial feature or change, when the user asks to plan, spec, or scope work, or before multi-file edits.
argument-hint: "[task]"
license: MIT
metadata:
  sources: "mattpocock/skills to-spec and grilling (MIT), obra/superpowers writing-plans"
---

# Plan

Don't edit code while planning. An approved plan isn't permission to start, so wait until the user says go.

## 1. Understand

- Read the relevant code, ADRs, glossary, and the ticket or spec if there is one.
- If something that changes the design is unclear, list up to three sharp questions at the top of the plan, each with your recommended answer. Don't interview.
- Always deliver a plan, even when questions are open or the code isn't available. Base it on the recommended answers, and mark guessed file names as assumed.

## 2. Write the plan

```markdown
# <Title>

**Goal:** one sentence, from the user's point of view.

## Assumptions
- ...

## Changes
1. `path/to/file.ts`: what changes and why. Reuse <existing function> rather than adding a new one.
2. ...

## Success criteria
- Observable behavior that proves it works.

## Verification
- `pnpm test src/billing` (exact commands)

## Risks and out of scope
- ...
```

Rules:
- Use the smallest change that fully meets the goal. Don't invent requirements.
- Name real files and functions. Order the steps so each one leaves the code working and checkable.
- Prefer testing at the highest existing seam. A new seam is a decision worth stating.
- If the plan includes a lasting technical decision, note that it needs an ADR (`adr` skill).

## 3. Save it (when asked, or when the project keeps plans)

- Path: `docs/plans/<ticket>-<slug>.md`, or `docs/plans/<slug>.md` with no ticket. Follow the project's convention if it has one.
- Add `**Status:** Not started` and a `## Progress` checklist with one `- [ ]` per change, plus Verification.
- Report the path, then stop.

## 4. While implementing

Tick progress items as each step lands (with the commit hash), note deviations, and keep the status current.

## 5. Retire it when the work merges

1. Move lasting decisions into an ADR.
2. Move open items to the tracker or the project's task list, written so they stand alone.
3. Delete the plan file. Git history keeps it.
