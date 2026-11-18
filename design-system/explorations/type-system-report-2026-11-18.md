# Report to coordinator: Humaine Studio type system

- **From:** claude.ai session "type exploration", 18 Nov 2026
- **Ticket:** HUM-271 design system
- **Status:** Decided by Chris. Ready to implement.
- **Specimen page (Chris's account, private):** https://claude.ai/artifact/3KhNfmWZrqSaZ2NS4huMeN

## Decision

Humaine Studio drops SID's licensed fonts (Sirca, ABC Walter Neue) for three free, open-source fonts served by Google Fonts. License cost: zero.

| Role | Font | Setting |
|:--|:--|:--|
| Display | Fraunces | `"SOFT" 100, "WONK" 0` |
| Text | Schibsted Grotesk | defaults |
| Mono | Recursive | `"MONO" 1, "CASL" 0.5` |

The wordmark "Humaine Studio" is set in Fraunces at weight **800**, full softness, letter-spacing −0.02em. The Klein & Linen palette is unchanged.

## Roles and weights

| Role | Font | Weight | Size |
|:--|:--|--:|:--|
| Wordmark | Fraunces | 800 | by placement |
| Headline (h1) | Fraunces | 500 | 48–64px |
| Subhead (h2, h3) | Fraunces | 400 | 24–32px |
| Quiet line | Fraunces | 300 | 40px+, once a page |
| Emphasis | Fraunces | 700–900 | a word or two |
| Body and lede | Schibsted Grotesk | 400 | 16–20px |
| Buttons, nav | Schibsted Grotesk | 500 | 15–17px |
| Labels, code, data | Recursive Mono | 400–500 | 12–14px |
| Numbers in table columns | Schibsted Grotesk | 400 | tabular figures |

Headlines sit at 500 so the wordmark stays the heaviest thing on any page. Chris first said "headline around 800", then made clear he meant the wordmark. Ask him before setting headlines heavier.

## Paste-ready code

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,100..900,0..100,0..1;1,9..144,100..900,0..100,0..1&family=Schibsted+Grotesk:ital,wght@0,400..900;1,400..900&family=Recursive:wght,CASL,MONO@300..1000,0..1,0..1&display=swap">
```

```css
:root {
  --font-display: "Fraunces", Georgia, serif;
  --font-text: "Schibsted Grotesk", system-ui, sans-serif;
  --font-mono: "Recursive", ui-monospace, monospace;
  --soft: "SOFT" 100, "WONK" 0;
  --mono: "MONO" 1, "CASL" 0.5;
}
.wordmark { font-family: var(--font-display); font-weight: 800; font-variation-settings: var(--soft); letter-spacing: -0.02em; }
h1        { font-family: var(--font-display); font-weight: 500; font-variation-settings: var(--soft); }
h2, h3    { font-family: var(--font-display); font-weight: 400; font-variation-settings: var(--soft); }
.quiet    { font-family: var(--font-display); font-weight: 300; font-variation-settings: var(--soft); }
body      { font-family: var(--font-text); font-weight: 400; }
button, nav { font-family: var(--font-text); font-weight: 500; }
code, pre, .label { font-family: var(--font-mono); font-variation-settings: var(--mono); }
table     { font-family: var(--font-text); font-variant-numeric: tabular-nums lining-nums; }
```

The Google Fonts URL returned HTTP 200 on 18 Nov 2026.

## Gotchas

1. **Fraunces defaults to sharp.** Every Fraunces element needs `"SOFT" 100`, or it renders with Softness 0 and loses the look Chris chose.
2. **Recursive defaults to proportional.** Without `"MONO" 1` it is a sans, not a mono. Keep `CASL` at 0.6 or below; above that it turns brushy at 12px.
3. **`font-variation-settings` does not merge.** A later rule that sets it replaces the whole list. Set both axes every time, through the tokens.
4. **Schibsted's tabular comma runs wide.** Use `tabular-nums` only in table columns. Use proportional figures in running text.
5. **Keep Fraunces numerals out of tables.** Numbers in tables use Schibsted.
6. **Eagle Ridge now shares no type with Humaine.** Eagle Ridge stays on Newsreader and IBM Plex. The palette is the only tie.

## Accessibility

WCAG 2.x contrast ratios, computed 18 Nov 2026:

| Pair | Ratio | Result |
|:--|--:|:--|
| Ink #0e1230 on linen #f3ece0 | 15.6:1 | AAA |
| Ink-soft #2e3352 on linen | 10.4:1 | AAA |
| Mute #5e6178 on linen | 5.2:1 | AA; avoid for text under 14px |
| Klein #002fa7 on linen | 9.1:1 | AAA |
| Linen #faf6ee on Klein (reversed wordmark) | 9.9:1 | AAA |
| Dark mode: ink #f1eadc on ground #0b0f24 | 15.8:1 | AAA |
| Dark mode: mute #9c9aae on ground | 6.9:1 | AA |
| Dark mode: Klein #8da6ff on ground | 8.2:1 | AAA |

## Why these fonts (short)

- **Fraunces.** Chris liked Commercial Type's Pavonia ($325 family, one-time license). Pavonia blends Century Old Style and Cooper Black. Fraunces is an Old Style soft serif drawn after Windsor, Souvenir and the Cooper series, so it shares those roots and costs nothing. Full softness closes most of the gap.
- **Recursive Mono.** It was chosen over DM Mono, IBM Plex Mono and JetBrains Mono because it is the only mono whose corners soften to match Fraunces. All four are OFL 1.1.
- **Paid upgrade path.** If the free version ever falls short, Pavonia from Commercial Type is the drop-in upgrade.

## Changes needed in this repo

I read the worktree on 18 Nov 2026. The design system still carries the old stand-ins: Newsreader, IBM Plex Sans and IBM Plex Mono. To apply the decision:

1. **`design-system/project/tokens.json`, `type.families`.**
   - `serif`: `"Fraunces", Georgia, "Times New Roman", serif`
   - `sans`: `"Schibsted Grotesk", "Helvetica Neue", Helvetica, Arial, sans-serif`
   - `mono`: `"Recursive", ui-monospace, "SF Mono", Menlo, Consolas, monospace`
   - Add variation tokens: `soft` = `"SOFT" 100, "WONK" 0` and `mono-axes` = `"MONO" 1, "CASL" 0.5`.
2. **`tokens.json`, type styles.**
   - `display` and `headline`: weight 300 → 500.
   - `headline-sm`: weight 300 → 400.
   - `body-lg`: weight 300 → 400. Schibsted Grotesk starts at 400, so a 300 request falls back to 400 anyway.
   - Rewrite the `display` usage note that says "Newsreader 300 stands in for SID's licensed Sirca".
3. **`design-system/project/components/bundle.css`.**
   - Line 1 `@import`: swap in the Google Fonts URL above.
   - `.hs-lockup` (now `600 18px` sans): set it to Fraunces 800 with `font-variation-settings: "SOFT" 100, "WONK" 0`. This is the wordmark.
   - Every `var(--font-mono)` rule (`.hs-kbd`, `.hs-code`, `.hs-code__head`, `code.hs-inline`, `.hs-table th`): add `font-variation-settings: "MONO" 1, "CASL" 0.5`, or Recursive renders proportional.
   - `.hs-table` sets `tabular-nums` on the sans. That is right for table columns, but watch Schibsted's wide tabular comma (gotcha 4).
4. **The 11 `components/*/preview.html` files.** Each one hard-codes the old Google Fonts link on line 2. Swap in the new URL.
5. **`design-system/project/README.md`, the "Type" list (lines 25–28).** Rename the three families and drop the "stands in for SID" wording.
6. **`CLAUDE.md`, line 20.** No palette change, so `check_contrast.py` does not need a rerun. Republish the changed files to the design-system artifact (https://claude.ai/artifact/ES1ThCt8R3T8itN88QwtRD).
7. **`design-system/explorations/type-specimens.html`.** This is an earlier copy of the specimen page. The current version (14 pairings, the Pavonia twin, the mono comparison and the decision block) is the claude.ai page linked at the top of this report.

## Not done (for the coordinator to assign)

- [ ] Design-system tokens file in the repo (type scale, colors, spacing)
- [ ] Wordmark as SVG, converted to outlines, in a linen version and a Klein version
- [ ] Favicon and social card using the wordmark
- [ ] Decide between the Google Fonts CDN and self-hosted, subset WOFF2 files (better speed and privacy; OFL allows self-hosting)
- [ ] Apply the system to humaine.studio and check it at 400px width in light and dark mode

## Sources

1. Google Fonts, Fraunces: https://fonts.google.com/specimen/Fraunces/about. Confidence: high.
2. ArrowType, Recursive (OFL 1.1, MONO and CASL axes): https://github.com/arrowtype/recursive. Confidence: high.
3. Commercial Type, Pavonia (from Chris's screenshot, 18 Nov 2026): https://commercialtype.com/catalog/pavonia. Confidence: high.
4. WCAG 2.x relative-luminance formula, run locally on the palette hex values. Confidence: high.
