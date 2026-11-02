---
type: llm
---

PASS if the steps say to understand both sides' intent, to regenerate the lockfile with the package manager instead of hand-merging it, to run checks, and to finish with git rebase --continue. FAIL if they suggest aborting, or hand-editing the lockfile conflict markers.
