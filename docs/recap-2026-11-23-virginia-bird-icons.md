# Session Recap: Virginia bird icons, from brief to merged set

**Date:** 2026-11-23 (work began 2026-11-19)
**Project:** humaine.studio (`design-system/birds/`)
**PRs Merged:** #67, #69, #71

## What Was Built

- **The approved set.** There are 30 Virginia bird icons in six regional sets of five, in the curlew logo's Mondrian style and the Klein & Linen palette. `design-system/birds/final/` holds the SVG masters, one sheet per region and strips of easily confused birds. `final.json` names the source of each bird.
- **References.** `refs.py` resolves the 30 species on iNaturalist and fetches CC0 and CC BY photos only. The 9 photos that `references.json` pins are committed. Field marks and bill-to-head ratios are measured from them. Audubon pages are read for field marks; their photos are never downloaded.
- **Drafts and tracing.** OpenAI image generation through the Codex CLI makes the drafts. `trace_icon.py` traces each one with potrace into the house frame and snaps every pixel to the palette. `assemble.py` runs SVGO and keeps an icon only if it renders the same as its source on every color channel.
- **Blind votes.** `bakeoff/run.py` drafts, traces and shuffles each round. `vote_page.py` builds a private claude.ai page that saves the votes. Three rounds ran: a generator bake-off, 8 redraws, and frontal owls with a Kestrel without blue.
- **Likeness check.** `qa.py` asks the TypeSafe Jev image model typed questions about each icon. Its calibration is in `qa/CALIBRATION.md`.

## Key Decisions

| Decision | Rationale |
|---|---|
| OpenAI (via Codex) over Recraft V4 Styles | Won the blind bake-off. Recraft broke the 3–4 color rule. Its code was removed in #71. |
| potrace + SVGO for the masters, not VTracer or Vectorizer.AI | Smoother edges than VTracer, no subscription, exact palette fills |
| iNaturalist CC0/CC BY photos; Audubon read-only | The licenses allow commercial use and redistribution with credit |
| The likeness check ranks drafts and never hides one | It put the voter's pick first for 5 of 5 birds across generators, but 0 of 4 among near-identical drafts |
| No Klein blue in the plumage | Every blue variant lost its vote |
| Commit the final set; ignore the vote-round sheets | They can be rebuilt, and the PR went from 31 MB to 13 MB |
| Retire SpecStory (#69) | Not installed; agent-session-backup backs up every session daily |

## Corrections Applied

- Birds drawn from coordinates failed on anatomy. An image model plus tracing replaced them, and the hand-drawn code was removed.
- The Black Skimmer's bill was too long. Bill ratios are now measured from reference photos.
- Mismatched owl eyes were rejected, so round 3 drew frontal owls from a photo.
- `tasks/` would have been published by Jekyll; `_config.yml` now excludes it.
- The SVGO render check compared brightness only. It now compares each color channel, and two masters were saved again at higher precision.
- The README had copied the likeness counts, and the copies drifted (16 against 17). It now points to `qa/CALIBRATION.md`.

## What's Next

- Linear HUM-314: dark (Klein Night) versions, transparent PNGs, favicons at 16–128 px and ICO files. Also the deferred redraws: the Screech-Owl, the 5-color Pelican and Godwit, the Ruffed Grouse, the Red-headed Woodpecker and the Cormorant.
- Linear HUM-318: remove the dead `OPENAI_API_KEY` line from `~/.zshrc`.
- The Whimbrel tracer comparison (autotrace, potrace, rasterless, VTracer) is saved in `~/GitHub/_inbox/2026-11-19-whimbrel-tracing-comparison/`.
