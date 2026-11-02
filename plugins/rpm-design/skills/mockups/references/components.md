# Component inventory

The default inventory is [daisyUI](https://daisyui.com/components/)'s **68
components**, because it is a maintained, opinionated answer to "what does a UI
kit contain" — a checklist to scope *against*, not a target to fill.

Mapped to atomic levels below. Counts: 30 atoms, 26 molecules, 8 organisms, 4
frames.

## Atoms (30)

One element, one job. Most fall out of the token layer for free once colour,
type, radius and shadow are set.

`Button` `Swap` `Theme Controller` · `Avatar` `Aura` `Badge` `Countdown` `Kbd`
`Status` `Text Rotate` · `Link` · `Loading` `Progress` `Radial progress`
`Skeleton` `Tooltip` · `Checkbox` `File Input` `Label` `Radio` `Range` `Rating`
`Select` `Input field` `Textarea` `Toggle` `Validator` · `Divider` `Indicator`
`Mask`

## Molecules (26)

A few atoms wired together with a single responsibility.

`Dropdown` · `Accordion` `Card` `Chat bubble` `Collapse` `Diff` `List` `Stat`
`Table` `Timeline` `Carousel` `Hover 3D card` `Hover Gallery` · `Breadcrumbs`
`Menu` `Pagination` `Steps` `Tab` · `Alert` `Toast` · `Calendar` `Fieldset`
`Filter` `OTP` · `Join` `Stack`

## Organisms (8)

Composed regions that own a chunk of a screen.

`FAB / Speed Dial` `Modal` · `Dock` `Megamenu` `Navbar` · `Drawer sidebar`
`Footer` `Hero`

## Frames (4)

Presentation shells for the mockup itself, not product UI: `Browser` `Code`
`Phone` `Window`. A mobile gallery usually needs `Phone` and nothing else.

## Scoping to the project

Build what the screens use. The rule in both directions:

- **Every kept component traces to a screen.** If no screen shows it, it is not
  in this round.
- **Every screen's needs are covered.** Walk each screen and name the components
  it is made of; anything unnamed is a gap in the inventory, not in the screen.

Then write both lists into the design-system doc's component inventory: what is
built, and — under a *Not built* heading — what was cut and the one-line reason
(`Table, Pagination — no list view in v1`). A cut list is a decision anyone can
reopen; silence is an omission nobody can see.

**Domain components.** Products need things no kit ships: `InsightCard`,
`ConfidenceMeter`, `SubscriptionRow`. Add them as organisms or molecules named
after the **domain**, not the widget — `InsightCard`, never `CardWithBadge`.
They are the components worth the most design attention, since they are the ones
the picks will actually be judged on.

**Level, not count, is the scope signal.** A mobile app that cuts to ~20
components is normal; what matters is that each level is coherent — atoms that
compose into the molecules, molecules that compose into the organisms the
screens are made of.
