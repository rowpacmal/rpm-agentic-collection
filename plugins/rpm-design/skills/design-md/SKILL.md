---
name: design-md
description: Creates or updates a DESIGN.md design system file in Google's open format, with YAML design tokens plus prose rules, so every agent and session builds UI consistently. Use when starting a UI project, when the user wants to lock in or document a visual style, or when extracting a design system from existing code.
license: MIT
metadata:
  sources: "google-labs-code/design.md spec (Apache-2.0), VoltAgent/awesome-design-md"
---

# DESIGN.md

`DESIGN.md` at the repo root is the project's design system: machine-readable tokens plus human-readable rules.
Once it exists, it overrides generic design defaults, including the `ui-design` skill's.

## Create or update

1. **Extract before inventing.** Read the existing theme/tokens, Tailwind config, `:root` variables, fonts, and key components. Record what's there. Only propose new values where nothing exists, and confirm those with the user.
2. Write the file in the structure below. Omit sections that don't apply, but keep the order.
3. If Node is available, lint it with the official CLI and fix what it reports: `npx @google/design.md lint DESIGN.md`. Ask the user before the first run, because it downloads a package.
4. Point the project's AGENTS.md or CLAUDE.md at it in one line: "UI follows DESIGN.md."

## Structure

YAML front matter holds the tokens. `##` sections follow, in this order: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts.

```markdown
---
version: alpha
name: Product Name
colors:
  primary: "#1A1C1E"
  surface: "#FFFFFF"
  accent: "#B8422E"
typography:
  h1:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  body:
    fontFamily: Inter
    fontSize: 16px
    lineHeight: 1.5
spacing:
  unit: 4px
rounded:
  control: 8px
---

# Product Name

## Overview
Two or three sentences: personality, audience, the feeling to evoke.

## Colors
What each token is for. Accent only on the primary action.

## Typography
Roles and when to use each.

## Layout
Grid, max width, spacing scale, breakpoints.

## Elevation & Depth
How surfaces separate (tone steps, shadows only on floating layers).

## Shapes
Radius per role.

## Components
Buttons, inputs, cards, nav: their tokens and states. Reference tokens as `{colors.primary}`.

## Do's and Don'ts
- Do keep text contrast at WCAG AA (4.5:1).
- Don't mix rounded and sharp corners in one view.
```

## Rules

- Tokens are the normative values. Prose explains how to apply them and must not contradict them.
- Define each top-level token key once.
- Keep it short. A DESIGN.md that agents skim beats an exhaustive one they skip.
