---
name: ticket
description: Works an OpenProject work package end to end. Checks the ticket against the project's spec and code before trusting it, settles gaps with the user, plans, stops for approval, builds test-first, verifies, and drafts the ticket update. Use when the user says /ticket, gives a work package number to build, or asks to start, pick up, or work on a ticket.
argument-hint: "<work package id> [check]"
license: MIT
metadata:
  sources: "Own workflow; composes the openproject skill with rpm-core plan, grill, tdd, verifier, and code-review"
---

# Work a ticket

Tickets are often AI-written. They can sound certain and still be wrong: invented files, endpoints or fields, scope the spec never asked for, missing edge cases, vague acceptance criteria. Treat the ticket as a draft. The project's sources of truth and the code are the evidence.

Argument: the work package id. If the user adds `check`, stop after step 2.

## 0. Project context

Read the project's `AGENTS.md` or `CLAUDE.md` for:

- **Sources of truth**, in priority order (spec, ADRs, API or architecture plans). When they disagree, the higher one wins.
- **Paths never to use** (archives, superseded docs).
- **API contract sources** for deciding whether an endpoint exists.
- **A build plan or module map**, if the project keeps one that work must fit into.
- **Checks** to run per repo or package.
- **Claiming a ticket**: which status means "in progress", and whether to self-assign.
- **Project ticket rules**, if any. They extend or override the steps below.

If none of this is written down, ask the user which documents are authoritative before step 2.

## 1. Fetch and prime

- Use the `openproject` skill to fetch the work package, its parent, and its children.
- If it is assigned to someone else, already in progress, or closed, say so first. Someone else may be on it.
- Read the parts of the sources of truth for this capability, any matching ADR, and the code and tests the ticket touches. Don't read whole repos.

## 2. Ticket check (report, no code)

Report in this shape, each item with its evidence (doc section, file path, or "not found"):

- **Confirmed**: what the ticket says that matches the sources and the code.
- **Wrong**: contradicts the sources, an ADR, or the code.
- **Invented**: files, endpoints, fields, or behaviour that exist in neither the code nor the sources. An endpoint counts as invented if it is in none of the project's API contract sources (for example the live OpenAPI schema and the planned-API docs).
- **Plan fit** (if the project keeps a build plan or module map): where this work belongs, and where the ticket disagrees with the plan.
- **Missing**: what the sources require for this capability that the ticket leaves out (errors, permissions, idempotency, empty states).
- **Out of scope**: what the ticket asks for that the sources exclude or defer.
- **Ambiguous**: what the docs can't settle.
- **Where**: which repos or packages; suggest a split if the work spans several.

Then stop and ask whether to continue.

When the user continues, the work has started. Offer to assign the ticket to them and move it to the in-progress status (from project context, or the closest match in `statuses`; ask if unclear). Change it only after they say yes, and don't block the work on it.

## 3. Settle the gaps

Use the `grill` skill on the Wrong, Missing, Out of scope, and Ambiguous items only. Look up facts yourself; ask only what is the user's call. Each question comes with a recommended answer.

## 4. Plan, then stop

Use the `plan` skill. Make sure the plan includes:

- **Success criteria** as checkable statements, based on the settled decisions rather than the ticket text.
- **Deviations from the ticket**, one line each with the reason.
- **Changes to the build plan** (if the project keeps one): the exact edit, made in the same task, so code and plan never drift silently. "None" if the work fits.
- **Draft human handoff** (the four sections from step 6).

End the turn and wait for explicit approval ("go", "approved", "yes"). If the user edits the plan, show it again before implementing.

## 5. Implement

Use the `tdd` skill. Follow the project's rules for the files you touch. If the plan turns out wrong, stop and return to step 4.

## 6. Validate

- Run the project's checks for each repo or package touched. After two failed fixes on the same check, stop and show the output.
- UI change: the `browser-testing` skill. Route change: the `api-testing` skill.
- Run the `verifier` agent with the plan's success criteria, then the `code-review` skill.
- Report check results, then a human handoff the user can follow in about 10 minutes. Always include all four sections; write "none" where one does not apply:
  1. **What we built**: the behaviour in plain words, for someone new to the tech. 3–6 sentences, no file dump.
  2. **Review**: the few files or decisions to read, and the one question that means "this is correct".
  3. **Test manually**: exact steps and what "pass" looks like.
  4. **API calls**: which requests to send (in the project's API client) and the expected result, if a route changed; otherwise "none".

## 7. Close the loop (ask first)

- Offer the `commit` and `pull-request` skills. Run git only after the user says yes.
- Draft an OpenProject comment: what was built, the PR link, and every deviation from the ticket with its reason. Post it with the `openproject` skill only after the user approves the text.
- If a decision with lasting effect came up, offer the `adr` skill. If terms clashed, offer the `glossary` skill.
