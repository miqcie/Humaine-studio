Humaine Studio is Chris McConnell's applied-AI studio. The system is square and quiet: square corners, solid block buttons, hairline rules, dashed optional steps. Its color is Yves Klein blue on linen, the same palette eagleridge.io uses. The Mondrian block mark carries the studio's own yellow and vermilion.

## Content fundamentals

- **Voice: plain, first person, specific.** The studio is "I" (Chris) on the site and "we" only for a team. Address the reader as "you".
- **Say what the thing does, with a real detail.** "Each tool writes down what it decided" beats "transparent AI". Real copy from the site: *"Applied AI for human-machine collaboration."* *"Systems that help us think better without taking decisions away."*
- **Display lines are lowercase** (`display`, `headline`): "applied ai for human-machine collaboration". Everything else is sentence case. Uppercase only in `label`.
- **No hype, no emoji, no exclamation marks.** Banned: revolutionary, seamless, cutting-edge, supercharge, unlock. Use parentheses for asides; use em dashes rarely.
- **Numbers are exact** and set in tabular figures: "12 posts since 2021", "1,152 words". Use a true minus sign (−).
- **Name the brand "Humaine Studio".** Never "Humane".

## Visual foundations

**Color: Klein & Linen.** Two themes. `klein-linen` (light, default) and `klein-night` (dark, follows the OS).

- Grounds: `ground` for the page, `surface` for raised areas, `sunken` for code and table headers. Linen is never pure white; night is never pure black.
- Text: `ink` for headlines and body, `ink-soft` for secondary copy, `mute` for meta text only.
- **One accent: `klein`.** Use it for the primary button, links, focus and the current state, and keep it to one Klein area per view. In dark mode `klein` lifts to #8DA6FF; pure #002FA7 stays in the mark.
- **Mondrian signals: `chrome` and `vermilion`.** Chrome yellow is a fill only (the mark, one tick, the warn pill). Vermilion is for errors and the alternate mark.
- **Why these balance.** Klein blue sits at OKLCH hue 263°. Its complement is 83°, and linen (81°) and the rebalanced chrome (84°) both sit on that warm axis. The three brand colors also step in lightness: Klein 0.38, vermilion 0.55, chrome 0.82. They stay distinct in grayscale and for color-blind readers. All inks lean blue and all grounds lean warm.
- **Proportion, Mondrian style:** mostly linen, a frame of ink, small fields of color. Roughly 70% ground, 20% ink, under 10% Klein, a few percent chrome or vermilion.
- **Status has no green.** `status-ok` is Klein, `status-warn` is chrome, `status-err` is vermilion, and a word always goes with the color.

**Type.**
- `serif` Newsreader 300 for `display`, `headline` and `headline-sm`. It stands in for SID's licensed Sirca.
- `sans` IBM Plex Sans for UI and running text (`title`, `title-sm`, `body-lg`, `body`, `detail`). It stands in for SID's licensed ABC Walter Neue.
- `mono` IBM Plex Mono for `label` eyebrows, data and `code`.
- All three load from Google Fonts (see the top of `components/bundle.css`).
- Body is 16.5px / 1.6 and held to `measure` (42rem). Ledes use `body-lg` in `ink-soft`.

**Layout.** Content max `canvas` (68rem); text max `measure`. 4px base spacing (`space-1` … `space-28`); sections are `space-18` apart. Front-load meaning at the top and left. Body text is left-aligned, never justified.

**Rules over boxes.** Separate things with a 1px `rule` hairline and whitespace. A bordered box appears only where it means something: a diagram node, an input, the docs sidebar edge.

**Corners and elevation.** `radius-0` everywhere. No shadows. Depth comes from `surface` vs `sunken`, not from elevation.

**States.**
- Hover darkens a fill (`klein` to `klein-press`, `ink` to `ink-soft`) or thickens an underline.
- Focus is a 2px solid `focus` outline offset 2px, on every interactive element, never removed.
- Pressed and selected use `klein-wash`.
- Motion is 150ms ease on color and underline only. Respect `prefers-reduced-motion`.

**Imagery.** Flat color fields and real screenshots. No gradients, no glossy 3D, no stock photos, no blue-purple AI glow. Charts are Tufte-lean: gray marks in `ink-soft`, the one series that matters in `klein`.

**Accessibility.** WCAG 2.2 AA in both themes: text 4.5:1, large text, controls and focus 3:1. `design-system/check_contrast.py` in the repo checks every pair named in the token notes; run it after any color change. Known limit: `vermilion` on `sunken` is 4.2:1, so it is not used there.

## Iconography

- **No icon set ships yet.** Where an icon is needed, use [Lucide](https://lucide.dev) at 1.5px stroke, 16–20px, in `currentColor`, always with a text label. This is a recommendation, not a Humaine asset.
- **Square tick marks** (`TickRow`) are the system's own glyph: a 10px `ink` square, `klein` when on, one `chrome` square for the thing to look at.
- **Unicode glyphs:** − for negatives, → for flow, · as a separator, ⌘K for the search shortcut.
- **No emoji, ever.**

## Marks

- **Primary:** `assets/Logos/humaine-mark.svg`, the Mondrian block mark with a Klein blue field. **Alternate:** `humaine-mark-vermilion.svg`.
- Both keep the original geometry. The colors moved: cream became paper, black became blue-black ink, the blue became Klein, and the yellow moved onto Klein's complement.
- Set the name in type beside the mark with the `Lockup` component; there is no drawn wordmark file.
- The curlew bird drafts are not part of the system.
