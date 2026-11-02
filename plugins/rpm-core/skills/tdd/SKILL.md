---
name: tdd
description: Builds features and bug fixes test-first. Agree the behavior and where to test it, write one failing test, make it pass with the least code, repeat, then refactor on green. Covers what makes a test worth keeping and when to mock. Use when implementing a feature or fix that changes behavior, or when the user says TDD, test-first, red-green, or asks to write or add tests.
argument-hint: "[behavior]"
license: MIT
metadata:
  sources: "mattpocock/skills tdd (MIT), obra/superpowers test-driven-development"
---

# Test-driven development

Tests are how you know instead of guess. Write the test that proves the behavior before the code that provides it.

## When it applies

Default to test-first for any change in behavior: features, bug fixes, and changes to business logic, APIs, or data handling.

| Situation | What to do |
|---|---|
| Behavior change, project has a test runner | Test-first. No exceptions without saying so |
| Bug fix | First a test that fails on the bug (the `debug` skill builds it). Then fix |
| UI behavior (flows, forms, states) | An end-to-end test or a scripted browser check, not just reading the JSX (see the `browser-testing` skill if installed) |
| HTTP API | A request-level test against the running app or its handler (see `api-testing` if installed) |
| Pure styling, copy, config, or a throwaway spike | Skip the test, and say so in your report. Verify by running or looking |
| No test setup at all | Say so. Offer to add the smallest one the stack supports. Don't silently skip |

Follow the project's own test commands, folders, and naming (`AGENTS.md`, existing tests). Don't add a new test framework unless asked.

## The loop

```
- [ ] 1. Behaviors listed, and the seam to test each one at agreed
- [ ] 2. Red: one failing test, run, and failing for the right reason
- [ ] 3. Green: least code to pass, test run and passing
- [ ] 4. Repeat 2–3 per behavior
- [ ] 5. Refactor on green, tests still pass
- [ ] 6. Wider suite, typecheck, and lint pass
```

1. **Plan the tests.** List the behaviors as plain sentences ("rejects an expired coupon"). Pick the seam: the public interface where you can observe each behavior without reaching inside (a function's return value, an HTTP response, what's on screen). For anything non-trivial, show the list and seams to the user before writing tests.
2. **Red.** Write one test for one behavior. Run it. It must fail, and fail on the assertion, not on a typo or missing import. A test that passes before the code exists proves nothing.
3. **Green.** Write the least code that makes it pass. Don't build ahead for tests you haven't written.
4. **Repeat** one behavior at a time. Each test is a thin vertical slice. Writing all the tests first locks in a design you don't understand yet.
5. **Refactor** only on green, in small steps, re-running tests after each.
6. **Finish** with the wider suite, typecheck, and lint. Report which tests you added and the commands you ran.

## Rules

- Never weaken, skip, or delete a failing test to get to green. If the test is wrong, say why, then fix the test.
- Expected values come from the spec or a worked example, not from re-computing them the way the code does.
- Test behavior through public interfaces. If a refactor that keeps the behavior breaks the test, the test was wrong.
- Mock only at system boundaries you don't own: network, payment, email, clock, randomness. Prefer real code and in-memory fakes for everything else.
- Keep tests deterministic: pin time, seeds, and locale, and don't depend on test order or the real network.

What good and bad tests look like, with examples: [references/good-tests.md](references/good-tests.md).
