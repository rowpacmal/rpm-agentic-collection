---
name: mockups
description: Explores visual directions for a product UI as rounds of static HTML mockups. Each round is a set of named design "picks" that apply different design systems to the same screens and copy, collected in a gallery for side-by-side comparison. Covers scoping an atomic component inventory, a reusable generator harness, verifying by screenshot, and promoting the winning pick into the design-system doc. Use when the user wants mockups, design directions, visual explorations, options to choose from, or to iterate on an existing mock gallery before building the real UI.
argument-hint: "[round theme or brief]"
license: MIT
metadata:
  sources: "daisyUI component list, atomic design"
---

# Mockup rounds

The surface is a `mock/` gallery: one static HTML page per **pick**, each page a complete design system (tokens, type, icons, components, screens) applied to the *same* product content, plus an `index.html` that links them all. Directions get compared side by side and killed cheaply, before anything is built in the real framework. Building the chosen direction for real is the `ui-design` skill's job.

## The invariant

**Same content in every pick. Only the design system changes.** Same screens, same copy, same numbers, same component inventory. A pick that also rewrites the content can't be compared with its neighbours.

- When a round's brief is "different layouts", say which layout. The **app screens** inside the device frame and the **gallery page** around them are separate surfaces. Leave the gallery page alone unless the user asks, since rearranging it makes picks harder to compare.
- Same content is not the same *structure*. A gallery where every pick reskins one dashboard tells the user nothing about how the product should work. Give each pick its own answer to three questions (what the home screen is, how you reach a decision, where detail lives) and hold the numbers and copy fixed.
- Express structural variation as CSS over an identical DOM where possible. Use a DOM transform only where the structure really differs (a nav that moves, a column that doesn't exist elsewhere). See [references/harness.md](references/harness.md).

## Steps

```
- [ ] 1. Inventory scoped: screens from capabilities, components from screens, cut list shown
- [ ] 2. Harness in the repo (first round only)
- [ ] 3. Picks named, one line each, confirmed by the user
- [ ] 4. Round generated
- [ ] 5. Every pick rendered and looked at
- [ ] 6. Gallery updated, links checked, committed
- [ ] 7. Feedback asked for, or the winner promoted
```

### 1. Scope the inventory

Derive **screens from the product's capabilities**, then **components from the screens**. The default inventory is daisyUI's 68 components, cut to what the screens use ([references/components.md](references/components.md)). Show the user the kept list and the cut list before building. The cut list is the part they'll want to argue with.

Done when every screen names the components it needs, and every kept component traces to a screen.

### 2. Stand up the harness (first round in a repo)

```
mock/
  index.html            gallery
  .harness/
    template.html       page skeleton with @@PLACEHOLDER@@ slots
    content.html        this project's components and screens markup
    generate.py         runner
    rounds/NN-name.py   one config module per round
  <theme>/<slug>.html   picks filed by theme, not by round
```

Copy `generate.py`, `template.html`, and `gallery.html` (as `mock/index.html`) from this skill's `assets/` folder (`${CLAUDE_SKILL_DIR}/assets/` in Claude Code). Then write `content.html` once: the real screens, in real copy, with surface classes left as `@@SURF@@` / `@@SURF2@@` / `@@SURFN@@` so each pick can skin them. Pick the device frame that fits the product: a phone for mobile apps, a browser or window frame for web and desktop. The harness lives in the repo, not in `/tmp`, because the next round depends on it.

### 3. Brief the round

Ask for references (links, screenshots, "like X but calmer") and read what the *system* is (material, depth, density, colour count, motion budget) rather than copying a screenshot. With no references, pick a theme from the round menu below.

Write one line per pick before generating any HTML: **a single-word name and the system it stands for** (`Vault: full skeuomorphism, tooled leather, real bevels`). Six picks is the default, four when the brief is narrow. Confirm the list with the user, then build.

### 4. Generate

One config module per round under `.harness/rounds/`, one entry per pick in `V`. `ROUND['dir']` is where the round's picks land. When picks belong to different themes, map them with `ROUND['dirs'] = {slug: theme}`. Each pick sets its own fonts, tokens, radius scale, shadow, surface classes, and three named accent themes on `--a7/--a5/--a1`, each with a caption saying what it's for. Placeholders and CSS gotchas: [references/harness.md](references/harness.md).

```bash
python3 mock/.harness/generate.py mock/.harness/rounds/01-skins.py
```

### 5. Verify by looking

Render every pick and read the image. Don't judge a pick from its source.

```bash
# Playwright CLI, if installed (see the browser-testing skill)
playwright-cli open "file://$PWD/mock/<theme>/<slug>.html" && playwright-cli screenshot && playwright-cli console
# or headless Chrome
google-chrome --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=4000 \
  --window-size=1700,5200 --screenshot=/tmp/shot.png "file://$PWD/mock/<theme>/<slug>.html"
```

- First check for JavaScript errors (the console, or `--dump-dom` with stderr grepped for `Uncaught`). A model that removes the tab bar or the screen title breaks page scripts, and count-up numbers silently stay at zero.
- Then crop to the device frames and look at every pick, plus one non-default tab for each pick that reworks navigation.
- Mid-count numbers and half-faded `.reveal` blocks are timing artifacts. A dark rail on a dark surface, a card floating in a void, or a band whose radius fights its card are real bugs.

Done when every pick in the round has been rendered and looked at.

### 6. Publish

File each pick under its theme. Give `mock/index.html` one section per theme (title, two-sentence brief, one card per pick) with three swatches, the name, and a pitch that leads with the material and says what's *different* about this pick. Check every link resolves. One commit per round (`feat(mock): add 6 skins picks`), and a separate commit for structural changes such as moving folders.

### 7. Iterate or promote

Rounds are cheap. Report the picks and ask what to push on. When the user settles on a direction, promote it into the design-system doc ([references/design-system.md](references/design-system.md)) so the doc and the winning pick can't drift apart.

## Round menu

Each round should push somewhere the last one didn't:

| Round theme | What varies | What stays |
|---|---|---|
| Skins | Palette, type pairing, radius, density | Layout, structure, motion |
| Material and period | The physical metaphor: paper, ceramic, steel, print era | Layout |
| Experimental | One rule broken per pick (no colour, no cards, one hue, brutalist) | Content |
| Dimensional | Depth: bevels, light from one direction, one moving part each | Layout |
| Layout: gallery | Where the showcase page puts its sections | The app screens |
| Layout: app screens | Where the app puts nav, content, and the eye's first stop | The gallery page |
| Flat and minimal | Shadows and material removed, navigation reworked (0, 2, 5, 7 tabs) | Content |

Motion budget: transitions plus at most one deliberate moving part per pick, all behind `@media (prefers-reduced-motion: reduce)`. No endless ambient animation.

Mockups load Tailwind and Google Fonts from CDNs. That's fine for throwaway exploration, but the real build follows the project's own stack.
