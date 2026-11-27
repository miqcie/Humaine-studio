# Frontend design review: humaine.studio

**Date:** 2026-11-18
**Site:** https://humaine.studio (live, after #64)
**Pages:** home `/`, post `/posts/2026/11/16/how-i-work-with-agents/`, `/tools/`, `/calculator/`, `/privacy/`. The site has no separate writing index: the nav "Writing" link goes to `/#writing`.
**Views:** 1280px light, 1280px dark, 375px light. Playwright (Chromium), computed styles, and `design-system/check_contrast.py`.

This is a critique only. It changes no CSS or content.

## Decided, not reopened

The brand rollout recap (`docs/recap-2026-11-18-brand-rollout.md`) fixes these choices. This review judges execution inside them.

- Klein blue `#002FA7` on linen, with a serif display face. This is close to the most common generated look (cream ground plus serif display). It is decided; the curlew and the tick row keep it specific.
- Zero radius, 2px ink section rules, hairline item rules, alternate `surface` bands, 48px section headings with a Klein square.
- The curlew is the logo. The original home layout stays. Site copy is Chris's words; this review flags copy only where it is a UI label or a template slot.

## Findings, ranked

### 1. Mobile menu does not work with a keyboard or a screen reader

- **Page / view:** all pages, 375px.
- **What is wrong:** The menu is a checkbox hack. `.nav-toggle` (the checkbox) has `display: none`, so it cannot get focus. The `<label class="nav-toggle-label">` has no text, no `aria-label` and no `aria-expanded`. A keyboard user cannot open the menu. A screen reader announces an unlabelled control. When the menu is closed, `.nav-menu` uses `transform: scale(1, 0)`, so its five links stay in the tab order. Focus moves to links that the user cannot see (measured: `.nav-link` takes focus with a 0px box).
- **Why it matters:** On a phone, the menu is the only route to Philosophy, Research, Writing, Tools and Contact. WCAG 2.1.1 (keyboard) and 2.4.7 (focus visible) fail.
- **Fix:** Replace the checkbox and label with `<button class="nav-toggle-label" aria-expanded="false" aria-controls="nav-menu" aria-label="Menu">`. Toggle `aria-expanded` and a class with five lines of JS in `assets/js/main.js` (the theme toggle already uses JS). Hide the closed menu with `visibility: hidden` next to the transform, so the links leave the tab order: `.nav-menu { visibility: hidden; transition: transform .3s, visibility 0s .3s; }` and `.nav-menu.is-open { visibility: visible; transition-delay: 0s; }`.

### 2. Privacy page has no page styles

- **Page / view:** `/privacy/`, all views.
- **What is wrong:** `privacy.md` uses `layout: default`. Its Markdown renders directly into `main.main-content`, without the `.post-content` wrapper. The CSS reset sets heading and list margins to 0, so headings touch the text above and below them. Links are the browser default blue (`rgb(0, 0, 238)`), not Klein, because link color is set only for `.post-content a` and `.section-content a`. List bullets hang outside the text column. At 375px the bullets sit 2px from the screen edge.
- **Also:** "Last updated" prints `site.time`, which is the build time. It changes on every deploy, so the date does not show when the policy changed.
- **Why it matters:** The privacy page is a trust page. It looks broken next to the rest of the site.
- **Fix:** Add `_layouts/page.html` that extends `default` and wraps `{{ content }}` in `<article class="post-content">`. Set `layout: page` in `privacy.md`. Replace `{{ site.time }}` with a fixed `last_updated:` front-matter value. `posthog-cover-letter.md` also uses `layout: default` with Markdown; check it with the same fix.

### 3. Theme toggle covers body text on phones

- **Page / view:** all pages, 375px, after scroll.
- **What is wrong:** `assets/css/main.css` (mobile block) sets `.theme-toggle { position: fixed; top: 16px; right: 16px; }`. The header itself is `static`. When the page scrolls, the 58×44px "DARK" box floats over the text column with a transparent background. On the home page it covers the words "adapt" and "teams" in the research section.
- **Why it matters:** It hides content, and it is the only fixed element on the site.
- **Fix:** Remove `position: fixed` and its offsets from `.theme-toggle` in the 768px media block. Keep it in the header row next to the menu button. Then remove `margin-right: 60px` from `.nav-toggle-label` and `padding-inline-end: 3.5rem` from `.showcase-bar`, which exist only to clear the fixed button.

### 4. Calculator is outside the design system

- **Page / view:** `/calculator/`, all views.
- **What is wrong:**
  - Inputs, select, the unit button and the disclaimer have `border-radius: 6px`. The system radius is 0.
  - The select and the "Switch to mmol/L" button render in Arial. Form controls do not inherit the font.
  - The disclaimer uses hard-coded colors `#fff5f5` / `#feb2b2` (light) and `#3d2020` / `#feb2b2` (dark), not tokens. In dark mode it is a brown box on navy.
  - Input borders use `--rule`: about 1.2:1 against `--ground` in light and about 1.4:1 in dark. The fields have the same background as the page, so the field edge is almost invisible.
  - At 375px the unit toggle is a full-width ink button above the disclaimer. A unit preference is the heaviest element on the page.
  - "⚠️Medical Disclaimer" has no space after the emoji.
- **Why it matters:** This is a dosing tool. Field edges must be visible (WCAG 1.4.11 needs 3:1 for the boundary of a form control). The page also reads as a different site.
- **Fix:**
  - In `assets/css/calculator.css`, set `border-radius: 0` on inputs, select, buttons and the disclaimer.
  - Add `input, select, button, textarea { font: inherit; }` to the base layer.
  - Use `border: 1px solid var(--mute)` on fields (`--mute` passes 4.5:1 on `--ground` and `--sunken`).
  - Build the disclaimer from tokens: `border-left: 4px solid var(--vermilion); background: var(--surface);`.
  - Style the unit toggle as a secondary text button (the `.hs-link` style), not a full-width block.

### 5. Writing list says 12 posts but shows 10, with no archive

- **Page / view:** home, all views.
- **What is wrong:** The hero stat says "12 posts since 2021" and draws 12 ticks. The writing list uses `limit:10`. The site has no archive page and the nav "Writing" link goes to `/#writing`, so the two oldest posts have no index link. Also, the tick loop uses `limit:12`. From post 13, the ticks stop growing but the number keeps counting.
- **Why it matters:** The tick row is the best idea on the page. It must stay true to the data it shows.
- **Fix:** Remove `limit:10` from the writing loop (12 rows is short), or add a `/writing/` page and a "See all writing" link under the list. Remove `limit:12` from the tick loop, or change the stat to match the tick count.

### 6. Post typography details

- **Page / view:** agents post, all views.
- **What is wrong:**
  - Post `h2` (24px) inherits the body `line-height` of 1.7 (40.8px). A heading that wraps will have a wide gap between its lines.
  - Ordered-list markers render as "1 ." with a gap. Browser default `::marker` uses `tabular-nums`, and Schibsted Grotesk tabular digits are wide.
  - Table cells use `vertical-align: middle`, so "Gatekeeper" floats in the middle of a tall row instead of on the first line.
  - The text column is 700px at 17px, about 80 characters per line. This is the upper limit.
- **Fix:** `.post-content h2, .post-content h3 { line-height: 1.2; }`. `.post-content ol li::marker { font-variant-numeric: proportional-nums; }`. `.post-content th, .post-content td { vertical-align: top; }`. Optionally set the post column to `max-width: 38rem` (about 70 characters).

### 7. Post dek repeats the first paragraph

- **Page / view:** agents post, all views. More visible at 375px.
- **What is wrong:** The layout prints the front-matter `excerpt` as a dek under the title. In this post the dek and the first paragraph are almost the same sentence.
- **Why it matters:** The reader sees the same sentence twice in the first screen.
- **Fix:** This is a copy decision for Chris. Either cut the first paragraph, or write a dek that adds something. A layout guard is optional: hide the dek when it matches the first paragraph.

### 8. Home hero eyebrow is a template tell

- **Page / view:** home, all views.
- **What is wrong:** "CHRIS MCCONNELL · HUMAINE STUDIO" is an uppercase mono eyebrow joined with a middle dot. It repeats the wordmark that sits 100px above it.
- **Why it matters:** The uppercase mono eyebrow with a middle dot is the most common sign of a generated page. Here it adds no information.
- **Fix:** Remove `.home-eyebrow`. If the byline must stay, set it in sentence case in the sans: `text-transform: none; font-family: var(--font-sans); letter-spacing: 0;`, and drop "Humaine Studio".

### 9. One status, two pill styles

- **Page / view:** home tools section vs `/tools/`.
- **What is wrong:** The home page shows "LIVE" as a filled Klein block in uppercase mono. `/tools/` shows "Live" as an outlined box in sentence case. On the home page all three cards say LIVE, so the pill tells the reader nothing there.
- **Fix:** Use one component (`.hs-pill`) on both pages. On the home section, drop the pill, because every tool shown there is live. The linked-card work in #61 can include this.

### 10. Dark mode: curlew art is the brightest block on the page

- **Page / view:** home hero, 1280px dark.
- **What is wrong:** The hero art (`humaine-curlew.svg` in an `<img>`) keeps its cream field in dark mode. Its navy frame (`#0e1230`) is part of the SVG and disappears into the `#0b0f24` ground. `humaine-site.css` line 51 adds `outline: 1px solid var(--rule)` in dark mode, but `--rule` is about 1.4:1 on the ground, so the outline is almost invisible. The result is a bright unframed square.
- **Fix:** Change that outline to `2px solid var(--ink-soft)`, so the art reads as a framed object again. Keep the cream field; the logo colors are decided.

### 11. Type scale has a gap, and page titles drift

- **Page / view:** all pages.
- **What is wrong:**
  - Home: h1 64px, h2 48px, h3 22px. The step from 48 to 22 has no middle size, so the research titles read as body text with bold.
  - Body size changes by page: home and privacy 16.5px, post 17px.
  - Inner-page h1 sizes are 48px (post), 32px (calculator) and 33px (privacy).
- **Fix:** Pick one inner-page title size (48px, the post size) for `.post-title`, `.showcase-header h1`, the calculator header and the new `page` layout. Set body to 17px on all pages. Set research and tool titles to 24px with `margin-bottom: var(--space-2)`.

### 12. Smaller items

- **Tools, all views:** Group labels ("Civic", 16px) are smaller than the card titles below them (22px). Make the group label the larger element, or set it in the sans at 14px with `--mute`, so it reads as a label and not as a weak heading.
- **Tools, 375px:** The filter row scrolls sideways. The fade mask is 2rem wide and "Data and site…" cuts mid-word next to "Open all". Widen the fade to 3rem, or let the row wrap (`flex-wrap: wrap`) below 640px.
- **Home, writing list:** Excerpts use `truncate: 200`, which cuts mid-sentence ("solopreneurs in…"). Use `truncatewords: 30`, or a `description` front-matter field.
- **Home, writing list:** Dates align to the top of the title row, not the title baseline. Use `align-items: baseline` on the row.
- **All pages:** No skip link. Add `<a class="skip-link" href="#main">Skip to content</a>` as the first element in `default.html`, visible on focus.
- **All pages:** The theme toggle focus ring is 3px `--ink-soft` with no offset. Other controls use a 2px Klein ring with a 2px offset. Remove the `.theme-toggle:focus-visible` rule in `main.css` so it uses the shared ring.
- **Home contact, 375px:** Contact links are 20px tall. They are inline text, so WCAG 2.5.8 exempts them. Use `display: inline-block; padding-block: 12px` for an easier tap.

## What works: keep it

- **The tick row.** Twelve solid squares for twelve posts is real data drawn as the brand mark. It is the one bold element that belongs only to this site. Fix finding 5 so it stays accurate.
- **The writing list.** Mono ISO dates in a fixed column, serif titles, sans excerpts and hairline rules. It is the clearest component on the site.
- **Contrast.** `check_contrast.py` reports 0 failing pairs in Klein & Linen and Klein Night. Dark mode is complete: bands, links, buttons and tables all read well.
- **Focus.** Links and buttons show a 2px Klein ring with an offset in both themes.
- **Motion.** Motion is limited to two 150ms hover transitions and the menu open. `prefers-reduced-motion` turns transitions off.
- **No sideways scroll.** No page overflows at 375px. Tables scroll inside their own box below 640px (#64).
- **Tools page structure.** The filter is a real radio `fieldset`. "Open all" uses `aria-pressed`. Each card says what the tool is before how it was built.

## Not checked

- Real iOS Safari and VoiceOver. Findings 1 and 3 come from Chromium and the source.
- 320px width on every page (checked only at 375px; tables were checked at 320px in #64).
- The calculator result state after the user enters values.
- `weeks-of-life.html`, `religion-origins-map.html`, `posthog-cover-letter.md` (out of scope).
