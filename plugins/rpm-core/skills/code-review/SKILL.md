---
name: code-review
description: Reviews a diff, branch, PR, or uncommitted changes on two separate axes. Spec checks that it does what was asked. Quality checks correctness, security, tests, and project standards. Findings are reported with severity, location, and a concrete fix. Use when the user asks to review changes, a branch, a PR, or "what I did since X", or before merging.
argument-hint: "[base ref | PR number | path]"
license: MIT
metadata:
  sources: "mattpocock/skills code-review (two axes, smell baseline; MIT), obra/superpowers requesting-code-review"
---

# Code review

Review only. Don't edit files unless the user asks for fixes afterward.

## 1. Pin the diff

- **PR:** `gh pr diff <n>` and `gh pr view <n>` (the description is the spec).
- **Base ref given:** `git diff <ref>...HEAD` (three dots, against the merge base) and `git log --oneline <ref>..HEAD`.
- **Nothing given:** uncommitted changes (`git diff HEAD`), or if those are empty, the branch against the default branch.

Check that the ref resolves and the diff isn't empty before going further. Read the changed files in full where context matters, not just the hunks.

## 2. Find the spec and the standards

- **Spec:** linked ticket or PR description, ticket ids in commits or the branch name, a plan in `docs/plans/`, or what the user said. If there is none, say so and skip that axis.
- **Standards:** AGENTS.md, CLAUDE.md, CONTRIBUTING, lint and format config, ADRs in the touched area. A documented project rule beats any default here.

## 3. Review two axes, separately

**Spec:** what was asked against what was built.
- Requirements missing or only partly done.
- Behavior that wasn't asked for (scope creep).
- Requirements that look implemented but behave wrongly.

**Quality:**
- Correctness: edge cases, error paths, null and empty, concurrency, off-by-one, time zones.
- Security: input validation, authz and tenant isolation, injection (SQL, shell, prompt), secrets, unsafe deserialization.
- Tests: does a test cover the new behavior and fail without it? Are any tests weakened or skipped?
- Simplicity: speculative abstraction, dead code, changes outside the task.
- Project standards. Code smells from [references/smells.md](references/smells.md) count only as judgement calls.

Skip anything a linter or formatter in the project already enforces.
For a large diff on a platform with subagents, review each axis in its own subagent so one doesn't mask the other.

## 4. Report

```markdown
## Spec
- **HIGH** `src/billing/renew.ts:42`: <issue>. Impact: <what breaks>. Fix: <concrete change>.

## Quality
- **BLOCKER** ...
- **LOW** (judgement: possible Feature Envy) ...

Summary: Spec 2 findings (worst: HIGH), Quality 3 findings (worst: BLOCKER). Verdict: changes needed.
```

Severities:
- `BLOCKER`: must fix before merge.
- `HIGH`: likely bug or incident.
- `MEDIUM`: should fix.
- `LOW`: minor.
- `NOTE`: observation.

Keep the axes apart, and don't rerank across them. If something looks good, one line saying so is enough. Don't pad the report.
