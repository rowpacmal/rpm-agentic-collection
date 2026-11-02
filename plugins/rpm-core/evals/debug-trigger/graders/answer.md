---
type: llm
---

PASS if the reply starts by building a reproducible feedback loop (for example running the test in a loop to raise the failure rate), proposes several falsifiable hypotheses (floating point rounding, ordering, time or locale), and says a regression test comes before the fix. FAIL if it immediately asserts one cause and a fix without a reproduction step.
