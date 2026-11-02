---
name: debug
description: A disciplined loop for hard bugs, flaky failures, and performance regressions. Build a failing feedback loop first, reproduce and minimize, rank falsifiable hypotheses, probe one variable at a time, then add a regression test, fix, and clean up. Use when something is broken, throwing, failing, flaky, or slow, or the user says debug, diagnose, or "why does this…".
argument-hint: "[symptom]"
license: MIT
metadata:
  sources: "mattpocock/skills diagnosing-bugs (MIT), obra/superpowers systematic-debugging"
---

# Debug

No theorizing before there is a loop that fails on this exact bug.

## Checklist

```
- [ ] 1. Feedback loop: one command, already run, that fails on the user's exact symptom
- [ ] 2. Reproduced reliably and minimized
- [ ] 3. 3–5 ranked, falsifiable hypotheses
- [ ] 4. Probed one variable at a time until one is confirmed
- [ ] 5. Regression test fails, fix applied, test passes, original loop passes
- [ ] 6. Debug code removed, cause reported
```

## 1. Build the feedback loop

This is most of the work. Try these in order:
- a failing test at the seam that reaches the bug
- a curl or HTTP script against the dev server
- a CLI run with a fixture, diffed against known-good output
- a headless browser script (Playwright)
- a replay of a captured request or event
- a minimal harness around the failing function
- a fuzz loop for "sometimes wrong"
- `git bisect run` when it worked at a known commit

Tighten it: make it fast (seconds), deterministic (pin time, seed, network), and specific (assert the exact symptom, not "didn't crash").
For flaky bugs, raise the failure rate (loop 100×, add stress) until it's debuggable.

If you can't build a loop, stop. Say what you tried, and ask for access, logs, a HAR or trace, or permission to add instrumentation.

## 2. Reproduce and minimize

Confirm it's the user's failure, not a nearby one. Then cut inputs, steps, config, and data one at a time, re-running after each cut, until every remaining piece matters.

## 3. Hypothesize

Write 3–5 ranked hypotheses, each in the form: "If X is the cause, then changing Y makes it pass."
Share the list with the user before testing. They may know which ones are already ruled out. Don't block on an answer.

## 4. Probe

- Change one variable per probe, and tie each probe to a hypothesis.
- A debugger or REPL beats logs. Targeted logs at boundaries beat logging everything.
- Tag every temporary log with a unique prefix, such as `[DBG-7f3a]`, so cleanup is a single grep.
- For performance, measure a baseline first (profiler, timing harness, query plan), then bisect. Don't guess.

## 5. Fix

1. Turn the minimized repro into a test at a seam that exercises the real bug path, and watch it fail.
2. Fix the cause, not the symptom. Don't loosen the test or swallow the error.
3. Watch the test pass, then re-run the original, un-minimized loop.

If no seam can catch the bug, say so. That's an architecture finding.

## 6. Clean up and report

- Grep for and remove the debug prefix and any throwaway harnesses.
- Report the root cause, the fix, and the regression test.
- Suggest what would have prevented the bug, if anything.
