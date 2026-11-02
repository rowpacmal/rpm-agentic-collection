# Harness

`generate.py` fills one template per pick: it loads `template.html`, injects the
project's `content.html` into the `@@COMPONENTS@@` and `@@SCREENS@@` slots, runs
the pick's optional DOM transform, substitutes every `@@PLACEHOLDER@@`, fails if
any is left unfilled, and writes `mock/<ROUND_DIR>/<slug>.html`.

```bash
python3 mock/.harness/generate.py mock/.harness/rounds/09-minimal.py
```

The copy under `mock/.harness/` belongs to the project: adapt the template's
page furniture to fit the product, and let `content.html` introduce its own
placeholders (`@@OB_H@@`, `@@OB_P@@`) — the runner fills anything a pick's
config defines.

Adopting the harness in a repo that already has hand-built mockups: lift each
committed page back into a round config and a content pack, regenerate, and
compare screenshots with animation frozen. Expect zero differing pixels before
trusting the harness with the next round.

## Round module

```python
ROUND = dict(dir='09-minimal', title='Flat & minimal')
V = {'plain': dict(NAME='Plain', SLUG='plain', ...), 'duo': dict(...)}
TRANSFORM = {'plain': t_plain}          # optional, per slug
```

## Placeholders

| Placeholder | Fills |
|---|---|
| `NAME` `SLUG` | Pick name (title case) and file/localStorage slug |
| `BRAND` | Product name in the header and footer |
| `FONTLINK` `FONTNAME` | Google Fonts `<link>` href, and the pairing's label |
| `TWCONFIG` | Body of `tailwind.config.theme.extend` — colors, fontFamily, borderRadius, boxShadow |
| `THEMECSS` | `:root` and `[data-theme="x"]` blocks defining `--a7/--a5/--a1` |
| `THEMES` | List of `(key, label)` pairs → theme buttons (consumed by the runner) |
| `THEMECAPTIONS` | `{key: sentence}` — one line per theme, shown under the header |
| `THEME_DEFAULT` | Theme key applied on first load |
| `BASECSS` | `body` font-family and `.font-display` |
| `FRAMECSS` | The device frame: `.phone-frame`/`.phone-screen` for mobile, a browser or window frame for web and desktop |
| `EXTRACSS` | Surface classes, `.app-*` layout rules, everything pick-specific |
| `EXTRAJS` | Appended inside the main script — same scope as the shared JS |
| `SURF` `SURF2` `SURFN` | Surface class names: primary card, secondary/inset, nav button |
| `DW` | Display weight utility (`font-medium`, `font-semibold`) |
| `STROKE` | Icon stroke width |
| `HERO_H1` `HERO_P` `HERO_TRK` | Hero line, paragraph, tracking utility |
| `T_FIGURE` `T_HEADLINE` `T_SAMPLE` | Type specimen rows: a big number, a headline, a body sentence |
| `T_DISP` `T_HEAD` `T_BODY` | Labels naming the face and weight used in each specimen row |
| `ICON_NOTE` `SWATCH_TEX` | Icon-section sentence; the texture/extra swatch tile |
| `COMPONENTS` `SCREENS` | Injected from `content.html` |

`content.html` is one file split by marker comments — everything after a marker
fills that slot:

```html
<!-- @@COMPONENTS@@ -->
  ...button, badge, input, card samples...
<!-- @@SCREENS@@ -->
  ...phone frames...
```

## Themes

Each pick ships **three** themes as CSS variables, so the theme switcher swaps
accents without touching any other token:

```css
:root, [data-theme="pine"] { --a7:#2F5340; --a5:#3F6E54; --a1:#DEE8E1; }
```

Tailwind side: `accent: { 700: 'var(--a7)', 500: 'var(--a5)', 100: 'var(--a1)' }`.
Every caption says what that theme is *for* ("Pine — closest to the current lead
accent"), because that is what the user picks between.

## DOM transforms

A transform is `str -> str`, run on the raw template **before** placeholder
substitution — so patterns match the literal `@@SURF@@` text, not the filled
class name. Anchor on the exact opening tags the template ships (screen wrapper,
`#tab-panels`, `<nav>`), assert every match, and keep the surgery minimal: swap
a class, move a block, inject one element. Anything expressible in CSS belongs
in `EXTRACSS` instead.

## Authored screens

When a pick needs its own *interaction model* — a different home screen, a
different route to a decision, a different place for detail — reskinning is not
enough and the surgical transform stops being surgical. Replace the phone frames
wholesale instead. Keep a shared `kit.py` next to the rounds that holds the
product's fixed copy and numbers plus helpers that render screens from them,
written in the canonical vocabulary (`@@SURF@@` / `@@SURF2@@` / `@@SURFN@@`,
`@@DW@@`, and the semantic colour scales). Each model then hands
`kit.screens(...)` to `TRANSFORM`. Numbers and copy come from `kit`, never from
the model, so structure is the only thing that varies.

Two things break the moment a model drops something the page assumed:

- **Page JS binds to what the old screen had.** A missing `#tab-title`, a nav
  button with no `.morph-icon`, or a sheet trigger that moved from an element id
  to `[data-sheet-open]` throws on load — and because it throws *before* the
  IntersectionObserver is wired, every count-up numeral silently stays at `0`.
  Null-guard the lookups rather than forcing every model to keep the furniture.
- **The first `[data-tab]` in the DOM need not be the home tab.** A model whose
  nav reads top-down from the last destination (a lobby board, a page index)
  opens on the wrong panel. Mark the home tab's button with `data-home`; the
  template opens on it when present.

A pick whose gallery page is light but whose *device* is dark needs the ink
scale flipped inside `.phone-screen` only — the surrounding page still wants
dark text on light paper.

## Gotchas

These each cost real debugging time:

- **Tailwind CDN injects its stylesheet after the inline `<style>`.** Equal
  specificity loses. Beat it with a tag qualifier (`header.sticky {}`), a longer
  selector, or `!important`.
- **`space-y-*` is `(0,3,0)`.** Tailwind's `.space-y-2 > :not([hidden]) ~
  :not([hidden])` overrides a `.app-x [data-panel]` rule of the same weight and
  silently kills vertical `margin: auto` centring. Use `!important` on margin
  rules aimed at panel children.
- **`.hidden` fights `display`.** A rule that sets `display` on `[data-panel]`
  must be written `[data-panel]:not(.hidden)` or it un-hides every panel.
- **`background:` shorthand paints over `bg-*`.** A surface class using the
  shorthand wipes Tailwind's background-color; set `background-color` plus
  `background-image` separately, or reset `background-image` on the utility.
- **Flat picks set the token, not the markup.** `boxShadow: { soft: 'none' }`
  neutralises every `shadow-soft` in the shared content — leave the classes
  alone.
- **Every `[data-tab]` button needs its icon slot.** The shared JS touches
  `.morph-icon` on each one; a nav button added by a transform without
  `<span class="morph-stage" data-icon-slot="...">` throws on first click.
- **`ICONS` and `TAB_TITLE` are extensible from `EXTRAJS`.** It runs in the same
  scope, so a pick that adds destinations does
  `TAB_TITLE.renewals = 'Renewals'; setActiveTab('home');` rather than
  editing the template.
