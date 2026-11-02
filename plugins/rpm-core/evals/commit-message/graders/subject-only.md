---
type: llm
---

Judge only the commit message(s) shown in code blocks. Ignore any surrounding prose.
PASS if the recommended message is a single line in the form `type(scope): subject` or `type: subject`, in imperative mood, lowercase after the colon, with no trailing period, and with no body, footer, or trailer.
FAIL if the recommended message has a body, bullet list, footer, or trailer, or doesn't follow that form.
