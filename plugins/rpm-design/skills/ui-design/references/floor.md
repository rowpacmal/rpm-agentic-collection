# UI floor

Each item applies to every build, web and native. Treat a failure as a bug, not a matter of taste.

## Accessibility

- Text contrast is at least 4.5:1, or 3:1 for large text (≥ 24px, or ≥ 18.7px bold) and for icons and control borders.
- Every interactive element is reachable by keyboard (web) or screen reader (native), and has a visible focus state that appears instantly.
- Touch targets are at least 44×44pt (iOS) or 48×48dp (Android). On web, at least 24×24px, with spacing between targets.
- Every input has a real label. Placeholder text isn't a label. Field rules and errors are linked to the field (`aria-describedby`, or `accessibilityHint` on native).
- Images have meaningful alt text, or empty alt if decorative. Icon-only buttons have an accessible name.
- Use semantic elements: `button` for actions, `a` for navigation, one `h1`, ordered headings, landmarks. On native, set `accessibilityRole`.
- Never use color as the only signal (errors, status, required fields).
- Respect reduced motion (`prefers-reduced-motion`, or `useReducedMotion` / `AccessibilityInfo` on native), and keep content visible without animation.

## Layout and resilience

- Nothing overflows horizontally at 320px wide. On web, use `overflow-x: clip` rather than `hidden` on `html`/`body`, and never use `100vw` for widths.
- Grid tracks that hold media use `minmax(0, 1fr)`. Long words and URLs wrap (`overflow-wrap: anywhere`, `min-width: 0`).
- Content width is capped and centered on large screens. Body text runs about 45–75 characters per line.
- Native: respect safe areas, keyboard avoidance, and dynamic type / font scaling.
- Long, empty, and error content doesn't break the layout. Test with a 3× longer name and with zero items.

## Craft

- Body text is ≥ 16px, line height ~1.5. Display text is tighter (1.0–1.15) with slight negative tracking.
- Use at most two type families, and a single type scale.
- Use one primary button style per screen and one radius scale, applied consistently.
- Never use `transition: all`, and never animate `width`, `height`, `top`, or `left`.
- Spacing comes from one scale, and the gaps between sections are clearly larger than gaps inside a section.

## Honesty

- No invented metrics, testimonials, customer logos, ratings, or "trusted by" claims.
- No fake product screenshots or dashboards of grey bars standing in for a real interface.
- Placeholder media is clearly a placeholder slot that the user replaces, and you tell them which slots need real assets.
