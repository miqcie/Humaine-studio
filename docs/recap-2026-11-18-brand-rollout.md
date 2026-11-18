# Session Recap: Humaine Studio design system and brand rollout

**Date:** 2026-11-18
**Project:** miqcie/Humaine-studio (HUM-271, HUM-272)
**PRs Merged:** #58 (design system), #59 (brand rollout)

## What Was Built

- **Design system "Klein & Linen"** as a claude.ai Design System artifact (https://claude.ai/artifact/ES1ThCt8R3T8itN88QwtRD), source in `design-system/project/`. Yves Klein blue `#002FA7` on linen, shared with eagleridge.io, plus a "Klein Night" dark theme. `design-system/check_contrast.py` checks every named color pair.
- **Type:** Fraunces (SOFT 100, WONK 0), Schibsted Grotesk, Recursive (MONO 1, CASL 0.5), self-hosted as instanced WOFF2 with the axes baked in.
- **Curlew logo:** traced by `design-system/trace_curlew.py`; header lockup, favicons, social card and home hero. The Mondrian block mark is retired.
- **Brand build:** `design-system/build_brand.py` regenerates the wordmark SVGs, favicons, fonts and the site's generated CSS (`assets/css/humaine-tokens.css`, `humaine-components.css`).
- **Site restyle:** new home page, header, footer and post styles (`assets/css/humaine-site.css`), checked with axe (WCAG 2.2 AA, no violations) in both themes and at phone width.
- **Home mockup canvas** (https://claude.ai/artifact/8wkG8QtpoPiXC69xaNDuEu): desktop, dark, phone, two rejected alternate directions and a separation-tweaks artboard. Source in `design-system/explorations/home-mockup/`.

## Key Decisions

| Decision | Rationale |
|---|---|
| SID is inspiration, not a spec | Usability wins: 44px buttons instead of SID's tight block |
| The curlew is the logo | Chris's call; one bird per view in content, plus the header |
| Self-host fonts | 207 KB vs 349 KB from Google Fonts, and no third-party requests |
| Keep the original home layout | Archive (after Shahnameh Forever) and Klein/night Bands directions reviewed and rejected |
| Section breaks: 2px ink rule, ~96px space, alternate `surface` bands, 48px headings | The 1px hairline is 1.2:1 on linen and vanishes at small sizes; `sunken` stays for code and table headers |
| Stay on static Jekyll + GitHub Pages | Nothing needs a server; revisit for stored forms, auth or shared Astro components |

## Corrections Applied

- Site copy stays Chris's words verbatim; mockup labels are placeholders for him to rewrite.
- Main-branch Link Check can race the Pages deploy on new files: noted in `CLAUDE.md`, tracked in #56.

## What's Next

- #60: deploy once (Pages source "GitHub Actions"), enforce HTTPS, align Ruby.
- #61: brand build drift check, font hashes, CSS consolidation, linked tool cards.
- #62: 16px curlew favicon, vermilion curlew use, curlew cover.
- HUM-273 (Chris): save the design system page once so its `tokens.css` lists the new fonts.
