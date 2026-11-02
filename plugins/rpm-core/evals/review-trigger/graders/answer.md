---
type: llm
---

PASS if the review flags the SQL injection (string-interpolated id) and the missing ownership/authorization check (any user can delete any comment), uses severity labels such as BLOCKER or HIGH, and gives concrete fixes. FAIL if it misses either issue or approves the change.
