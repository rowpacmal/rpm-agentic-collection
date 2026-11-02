---
name: grill
description: Stress-tests a plan, design, or idea by interviewing the user in rounds of numbered questions, each with a recommended answer, until every decision is settled. Looks facts up itself instead of asking. Use when the user says grill me, poke holes, stress-test, challenge, or pressure-test a plan, or wants to sharpen an idea before building.
argument-hint: "[plan, doc, or idea]"
license: MIT
metadata:
  sources: "mattpocock/skills grilling and grill-me (MIT)"
---

# Grill

Interview the user until you both understand the plan the same way. Don't build anything during the grill.

## How it works

1. **Read first.** The plan, doc, or idea, plus relevant code, ADRs, and glossary. Facts are your job: look up anything the repo, docs, or tools can answer. Only decisions go to the user.
2. **Map the decisions.** Each decision may depend on others. The questions you can ask now are the ones whose prerequisites are settled.
3. **Ask a round.** Ask all of the currently answerable questions together, numbered, each with your recommended answer:

   ```
   **Q1. <short title>**
   <the question, with the options if there are several>
   → Recommended: <your answer and the one-line reason>
   ```

   Hold back any question that depends on an answer you haven't heard yet.
4. **Wait for answers.** Each answer settles decisions and unlocks new questions. Ask the next round.
5. **Stop** when no decision is left open or silently assumed. Summarize the settled decisions in a short list and ask the user to confirm it.

## What to probe

- What happens at the edges: empty, huge, concurrent, offline, failed, retried, malicious input.
- Who and what else is affected: users, data, other services, migrations, rollbacks.
- What "done" means and how it will be verified.
- What's out of scope, said out loud.
- Cheaper alternatives, including not building it.

## After the grill

Offer to record the result: a plan (the `plan` skill), lasting decisions as ADRs (`adr`), and new terms in the glossary (`glossary`). Don't start implementing until the user says so.
