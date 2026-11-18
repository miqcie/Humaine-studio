Humaine Studio is the applied-AI studio for Chris McConnell. The system is square and quiet: square corners, solid block buttons, hairline rules, dashed optional steps. Its primary hero color is Yves Klein blue on linen, the same palette eagleridge.io uses. The curlew, the studio's logo, carries its own yellow and vermilion.

## Content fundamentals

- **Voice: plain, first person, specific.** The studio is "I" (Chris) on the site and "we" only for a team. Address the reader as "you".
- **Say what the thing does, with a real detail.** "Each tool writes down what it decided" beats "transparent AI". Real copy from the site: *"Applied AI for human-machine collaboration."* *"Systems that help us think better without taking decisions away."*
- **Display lines are lowercase** (`display`, `headline`): "applied ai for human-machine collaboration". Everything else is sentence case. Uppercase only in `label`.
- **No hype, no emoji, no exclamation marks.** Banned: revolutionary, seamless, cutting-edge, supercharge, unlock. Use parentheses for asides; use em dashes rarely.
- **Numbers are exact** and set in tabular figures: "12 posts since 2021", "1,152 words". Use a true minus sign (−).
- **Name the brand "Humaine Studio".** Never "Humane".
- The Curlew is the brand icon.

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
- `serif` **Fraunces**, always with `--soft` (`"SOFT" 100, "WONK" 0`). The wordmark is Fraunces 800, letter-spacing −0.02em (the `Lockup`). Headlines `display` and `headline` are 500, so the wordmark stays the heaviest thing on a page; subheads `headline-sm` are 400; a quiet line is 300 at 40px or more, once a page; 700–900 only for a word or two of emphasis.
- `sans` **Schibsted Grotesk** for UI and running text (`title`, `title-sm`, `body-lg`, `body`, `detail`): body and ledes 400, buttons and nav 500.
- `mono` **Recursive**, always with `--mono-axes` (`"MONO" 1, "CASL" 0.5`), for `label` eyebrows, data and `code`. Keep `CASL` at 0.6 or below.
- `font-variation-settings` does not merge: a later rule replaces the whole list, and the `font:` shorthand resets it. Set it only through `--soft` and `--mono-axes` (declared in `components/bundle.css`, since token values cannot hold quotes), after any `font:` shorthand on the same element.
- Numbers in table columns use Schibsted with tabular figures. Its tabular comma is wide, so running text keeps proportional figures, and Fraunces numerals stay out of tables.
- All three are free (OFL 1.1) and load from Google Fonts (see the top of `components/bundle.css`). Eagle Ridge keeps Newsreader and IBM Plex; the palette is the only shared part.
- Body is 16.5px / 1.6 and held to `measure` (42rem). Ledes use `body-lg` in `ink-soft`.

**Layout.** Content max `canvas` (68rem); text max `measure`. 4px base spacing (`space-1` … `space-28`); sections are `space-18` apart. Front-load meaning at the top and left. Body text is left-aligned, never justified.

**Rules over boxes.** Separate things with a 1px `rule` hairline and whitespace. A bordered box appears only where it means something: a diagram node, an input, the docs sidebar edge.

**Section breaks that survive a small view.** The `rule` hairline is only 1.2:1 on linen, so it vanishes when a page is seen small. Between page sections use a ranked set instead: a 2px `ink` rule on top of each section, about 96px of space, and every other section on a full-bleed `sunken` band. Section headings are 48px Fraunces with a 12px `klein` square before them. Hairlines stay for rows inside a section.

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
- **Square tick marks** (`TickRow`) are the system's own glyph: a 10px square. Solid `ink` for a count, solid `klein` for done, hollow for not yet, and one `chrome` square inside an `ink` ring for the thing to look at.
- **Unicode glyphs:** − for negatives, → for flow, · as a separator, ⌘K for the search shortcut.
- **No emoji, ever.**

## Marks

- **Logo: the curlew.** `assets/Logos/humaine-curlew.svg`, a Klein blue curlew with a chrome wing on paper inside an ink frame. **Alternate:** `humaine-curlew-vermilion.svg`, an ink curlew on vermilion.
- It is the header lockup, the favicon, the social card and the page hero. Birds are welcome: one curlew per view in content, plus the one in the header.
- Set the name beside it with the `Lockup` component. For places without the font, use the outlined wordmark (`humaine-wordmark-ink.svg`, `humaine-wordmark-linen.svg`).
- Regenerate the curlew with `design-system/trace_curlew.py` and the favicons with `design-system/build_brand.py`. Both read their colors from `tokens.json`.
- The Mondrian block mark is retired. Its colors and frame live on in the palette and the cover.

---

## Consuming this system (generated — do not edit)

Every path named below is under `project/` in this design system: read `project/api/tokens.md`, not `api/tokens.md`.

10 components are documented without a runnable `components/bundle.js`: read each component’s card, and its README where it has one (`components/<Comp>/README.md`), and build to those guidelines. Tokens: the values are on `api/tokens.md`; a Slides deck or Design canvas also takes `tokens.json` by file path. On a Design canvas, also copy `tokens.css` to `project/ds/<folder>/tokens.css` in the call that installs this system, and link it in each artboard that uses this system, right after the `support.js` line and before the system’s other stylesheets: `<link rel="stylesheet" href="ds/<folder>/tokens.css">` (with one `../` in front for each folder the artboard is in).

**Read, per thing:** a component’s props, parts and examples: `api/components/<Comp>.md`; token values: `api/tokens.md`; stored assets and their paths: `api/assets/<Group>.md`. After this README, fetch the cards and fonts you need in ONE message as parallel calls — none depends on another.

**Two rules.** Before you use a thing — a component, a token group, an icon, an asset — read its card from the index below; a value you did not read from a card is a guess. `tokens.json`, `manifest.json` and `design-system.json` are sources for tools: hand them over. `components/<Comp>/README.md` and `assets/<Group>/README.md` are the long-form second read a card links to; `SKILL.md` and `artifact-type/` beside them are authoring guidance, not needed to consume the system.

## Index (generated — do not edit)

**Tokens**

- `api/tokens.md` — Every token: surface, text, fill, palette, type, spacing, radius, layout. (12.1k)

**Icons and assets**

- `api/assets/Logos.md` — 4 files, by asset id. (3.7k)

**Components** (`api/components/<Comp>.md`, 10)

- **Actions**: `Button` — A solid square block, 44px tall, with the label set in Schibsted Grotesk 500 · `Link` — An underlined inline link whose underline thickness follows the text weight, and thickens on hover
- **Content**: `CodeBlock` — A square code block on sunken, with an optional mono header that names the language or file · `Diagram` — A left-to-right flow of square nodes joined by arrows, where a solid border is a step you build and a dashed border is optional
- **Data**: `DataTable` — A table separated by hairline rules, with a mono header on sunken and tabular figures · `StatusPill` — A short uppercase word on a square fill that states a status · `TickRow` — A row of small squares that counts or marks progress, with a short stat beside it; SID's square markers, which also echo the Mondrian mark
- **Navigation**: `DocsNav` — The docs layout from SID's research center: a 16rem sidebar with search and a page list, and a content column held to measure · `TopNav` — The site header: lockup on the left, a few text links, and one ink-block call to action on the right
- **Brand**: `Lockup` — The mark beside the name "Humaine Studio" set in type; the brand's signature in headers and footers
