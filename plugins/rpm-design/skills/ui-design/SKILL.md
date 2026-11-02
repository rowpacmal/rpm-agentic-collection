---
name: ui-design
description: Builds and refines user interfaces that look designed rather than generated, for web (HTML/CSS, React, Next, Tailwind) and native (Expo, React Native). It enforces an accessibility and craft floor and avoids common AI-template tells. Use when building, redesigning, polishing, or reviewing a page, screen, or component, or when the user says a UI looks generic, templated, or "AI-made".
license: MIT
metadata:
  sources: "Nutlope/hallmark (floor idea, MIT), Leonxlnx/taste-skill (house rules, MIT), pbakaus/impeccable (surface modes, Apache-2.0), google-labs-code/design.md"
---

# UI design

## 1. Read before designing

- If `DESIGN.md` or `design.md` exists, it is the design system. Follow its tokens and rules over anything here. If it's missing and the user wants a lasting system, use the `design-md` skill.
- Otherwise read the project's existing system: theme/tokens files, Tailwind config, `:root` variables, component library, fonts. Extend it. Don't replace it.
- The brief wins. A named style, palette, font, or reference beats these defaults.
- Refining keeps the existing identity, copy, and behavior outside the requested scope. A redesign keeps content and function and replaces the look.

## 2. Pick the surface mode

| Mode | Visitor's job | Priority |
|---|---|---|
| **Persuade** | decide and act (landing, pricing, marketing) | one strong idea per screen, real proof, a clear primary action |
| **Operate** | finish a task (app, dashboard, settings, forms) | scanability, consistency, platform conventions, states. Brand shows only in details |
| **Read** | understand (docs, articles, changelog) | measure, hierarchy, navigation |
| **Experience** | be inside the work (portfolio, gallery) | the content leads and the interface recedes |

Choose by surface, not product: a dev tool's landing page is Persuade, and its docs are Read.

## 3. Build

1. **Tokens first.** Every color, font, size, radius, and spacing value comes from a named token or theme value. No raw hex or font names in components.
2. **Content first.** Use the user's real copy, data, and images. Missing proof (metrics, quotes, logos) is left out or marked as a slot. Never invented.
3. **Hierarchy through scale and contrast.** Use few sizes with big steps between them, one accent color for the primary action, and left alignment by default.
4. **Every interactive element gets every state:** default, hover, focus-visible, active/pressed, disabled, loading. Data views also get empty, error, and loading states.
5. **Motion with purpose:** animate only `transform` and `opacity`, keep it short, and give it a reduced-motion fallback.

## 4. Verify

Copy this checklist and work through it:

```
- [ ] Floor: every item in references/floor.md passes
- [ ] Looked at the result: phone (~390px), tablet (~768px), desktop (~1440px), or the device sizes for native
- [ ] Keyboard: tab through, focus always visible, order logical
- [ ] Contrast: text ≥ 4.5:1, large text and UI parts ≥ 3:1
- [ ] AI tells: none from references/tells.md unless the brief asks for them
```

If a browser tool (a Playwright MCP server, or a dev server plus screenshots) is available, use it to look, then fix everything you see in one batch before looking again. If you can't render, say so and list what still needs checking by eye.

- Floor (always applies): [references/floor.md](references/floor.md)
- AI-template tells to avoid: [references/tells.md](references/tells.md)
