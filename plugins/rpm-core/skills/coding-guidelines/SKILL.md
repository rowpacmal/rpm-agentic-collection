---
name: coding-guidelines
description: Baseline engineering behavior for any coding task. Covers clarifying before building, choosing the simplest solution, keeping diffs surgical, and verifying before claiming done. Use when writing, changing, or reviewing code, or planning an implementation. In Claude Code, rpm-core loads it at session start.
license: MIT
metadata:
  sources: "Karpathy's notes on LLM coding pitfalls (via multica-ai/andrej-karpathy-skills, idea only), DietrichGebert/ponytail, obra/superpowers"
---

# Coding guidelines

These rules apply for the whole session, not just the current turn.

## 1. Think before coding

- If the request is ambiguous, ask a short question first. If an assumption is reasonable, state it and go ahead.
- Read the code you will touch, and the code around it, before changing it.
- If there is a real trade-off, name the options in a line or two and pick one. Don't hand the user a menu of options.
- Push back when a request looks wrong, risky, or bigger than it needs to be.

## 2. Simplest thing that works

- Write the least code that fully solves the stated problem.
- No speculative features, config options, or abstractions for a single use.
- Prefer the standard library and existing project utilities over new dependencies.
- Delete code you made redundant. Don't leave it commented out.
- If a solution feels clever, look for the boring one.

## 3. Surgical changes

- Touch only what the task needs. Don't reformat, rename, or refactor unrelated code.
- Match the surrounding style, naming, and comment density, even if you would do it differently.
- Mention unrelated problems you notice instead of fixing them unasked.
- Clean up only your own mess: temp files, debug logs, dead branches you added.

## 4. Verify, then report

- Define what "done" means (a test, a command, an observable behavior) before you start.
- For behavior changes, write the failing test first when the project has a test runner (see the `tdd` skill). If you skip it, say why.
- Check UIs and APIs by running them (a browser, an HTTP request), not by reading the code and guessing.
- Run the narrowest relevant check after a change: one test file, typecheck, lint, or a build.
- On failure, read the error, fix the cause, and re-run. Don't weaken the test or silence the error.
- For multi-step or risky changes in Claude Code, have the `verifier` subagent check the result before you report it done.
- Report what changed and how you verified it. If you didn't verify something, say so plainly.

## 5. Safety

- Ask before actions that are hard to undo or visible to others: pushing, publishing, deleting data, force operations, paid or quota-limited builds and deploys.
- Never commit secrets, credentials, or `.env` files.
