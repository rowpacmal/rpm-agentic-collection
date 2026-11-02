---
type: llm
---

Judge only the commit messages shown in code blocks. Ignore any surrounding prose.
PASS if there are two separate commit messages: one `fix` for the login crash, and one `chore`, `build`, or similarly typed message for the eslint bump. Each is a single subject line with no body.
FAIL if there is a single combined commit, or any message has a body or trailer.
