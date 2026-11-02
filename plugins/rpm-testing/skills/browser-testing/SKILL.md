---
name: browser-testing
description: Checks web UIs in a real browser instead of guessing from the code, using the Playwright CLI for quick interactive checks (open, click, fill, screenshot, console errors, network) and Playwright Test for lasting end-to-end tests. Use when building or fixing a web page, form, or flow, when verifying a UI change, reproducing a UI bug, taking screenshots, or when the user mentions Playwright, e2e, or browser tests.
argument-hint: "[url or flow]"
license: MIT
metadata:
  sources: "microsoft/playwright-cli README (Apache-2.0), playwright.dev docs"
---

# Browser testing

Look at the running app. Reading JSX and assuming it renders correctly is guessing.

## Pick the tool

| Need | Tool |
|---|---|
| Check a change, reproduce a bug, take a screenshot, explore a flow | Playwright CLI (`playwright-cli`), interactive and token-efficient |
| A test that guards the flow from now on | Playwright Test (`npx playwright test`), committed with the code |

Use what the project already has first (`playwright.config.*`, Cypress, an `e2e/` folder). Follow its commands in `AGENTS.md` or `package.json`.

## Setup (ask before installing)

```bash
playwright-cli --help                        # already installed?
npm install -g @playwright/cli@latest        # global, or:
npm install -D @playwright/cli@latest        # per project, then use `npx playwright cli`
```

Needs Node 20 or newer. If the CLI reports a missing browser, run the install command it suggests, after asking.
For Playwright Test in a project without it: `npm init playwright@latest`. This adds config and files, so ask first.

## Interactive check

1. Start the dev server in the background (the project's dev command) and wait until it answers: `curl -sf http://localhost:<port> >/dev/null`.
2. Drive the page:
   ```bash
   playwright-cli open http://localhost:3000/login   # headless by default; --headed to watch
   playwright-cli snapshot                           # page structure with element refs
   playwright-cli fill <ref> "test@example.com"
   playwright-cli click <ref>
   playwright-cli snapshot                           # did the expected state appear?
   playwright-cli screenshot                         # look at it for layout and visual bugs
   playwright-cli console error                      # any errors?
   playwright-cli requests                           # failed or unexpected API calls?
   playwright-cli close
   ```
   Use `-s=<name>` (or `PLAYWRIGHT_CLI_SESSION=<name>`) to keep separate sessions apart, and `--persistent` only when you need a login to survive between runs.
3. Check the states that usually break: empty, loading, error, long text, narrow viewport, keyboard-only navigation.
4. Report what you saw with evidence: the screenshot path, console errors, failing requests. Close sessions you opened (`playwright-cli close-all`).

## Lasting e2e test

When a flow matters (sign-up, checkout, anything a bug report came from), add a Playwright Test spec through the `tdd` loop: write the spec, watch it fail, then make it pass.

- Locate elements the way users do: `getByRole`, `getByLabel`, `getByText`. Avoid CSS paths and test-only classes.
- Assert with web-first assertions (`await expect(locator).toBeVisible()`), never fixed sleeps.
- Each test sets up its own data and doesn't depend on another test's leftovers.
- Run one spec while iterating (`npx playwright test e2e/login.spec.ts`), then the suite.
- `npx playwright codegen <url>` records a flow as a starting point. Clean up what it produces.

## Limits and safety

- Use local or staging environments and test accounts only. Never automate real users' accounts or production writes without explicit approval.
- Credentials come from environment variables, never typed into commands or committed.
- React Native or Expo native screens can't be driven this way. Use Expo web (`npx expo start --web`) for logic and layout checks, and the project's native e2e tool (such as Maestro or Detox) for the rest.
- Screenshots can show personal data. Don't commit or share them unless asked.
