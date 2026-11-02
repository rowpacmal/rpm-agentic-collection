# Promoting a pick

The design-system document is the record; the gallery is the surface. Use the project's existing one if it has one. Otherwise write `DESIGN.md` in Google's format (the `design-md` skill), or `docs/design-system.md` if the user prefers. This skill
owns exactly one moment of that document — the promote step — because the tokens
are already written, in the winning pick's `tailwind.config`. Copy them; do not
retype them. Everything after promotion (component specs, revisions as the app
gets built) is ordinary doc work.

## When

As soon as one pick is the lead, even if rounds continue. An un-promoted lead
pick is a design system living only in a variant file nobody has agreed to.
Mark it `status: draft` and say what it is iterating against.

## Steps

1. Copy the pick's colour, font, radius and shadow values out of its
   `TWCONFIG` verbatim, into the token tables. Same names, same hex.
2. Name the pick and its file, so the doc points at its own surface.
3. Fill the component inventory from `COMPONENTS.md` — kept list by atomic
   level, plus the *Not built* list with reasons.
4. Write the rules that the picks made visible but a token table cannot hold:
   how many accents may share a screen, what is reserved for risk states, what
   is banned outright (the anti-brief).
5. Commit doc and mock together whenever a token changes. One value living in
   two places drifts the moment they are committed apart.

## Outline

Sections that earned their place:

1. **Brand read** — what the product is, the adjectives, and the anti-brief: the
   defaults being rejected, named concretely (`no gradient hero cards`, `no
   glassmorphism`, `no ambient looping motion`).
2. **Colour** — token table (name, hex, usage) then the rules: accent count per
   screen, semantic hues reserved for risk/destructive, gradients and blur.
3. **Typography** — the pairing, the scale, what the display face is *for*
   (usually numbers and headline stats).
4. **Spacing, radius, elevation** — the grid unit, the radius scale, and how
   many elevations exist. One shadow is a healthy answer.
5. **Motion** — the budget, the named interactions, and the
   `prefers-reduced-motion` rule.
6. **Iconography** — the set, stroke width, fill policy, stateful icons.
7. **Component inventory (atomic)** — atoms, molecules, organisms, screens, and
   *Not built*.
8. **Voice & content rules** — how numbers, dates and AI-derived claims are
   written, with any hard limits from the product itself.
9. **Accessibility** — contrast floor, touch target minimum, reduced motion, and
   never encoding meaning by colour alone.
10. **Porting** — how tokens map into the real framework's theme file, named
    1:1 so nothing gets renamed at port time.
11. **Open questions** — dark mode, thin screens, anything deferred.

Frontmatter and doc conventions come from the repo's own doc rules, not this
skill.
