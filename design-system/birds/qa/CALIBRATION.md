# Calibration of the likeness check

## 1. Known errors in the 30 OpenAI icons

Base rate: the check flags 17 of 30 icons, so a catch is weak evidence on its own.

- Major errors (6): flagged 6; from generic questions alone, 4.
- Minor errors (5): flagged 1; from generic questions alone, 1.
- Other 19 icons: flagged 10.

| Known error | Kind | Verdict | Why (check whether the reason matches the error) |
|---|---|---|---|
| american-kestrel (no face stripes; reads as a toucan) | major | FLAG | reads as red headed woodpecker (0.36); missing: two dark vertical face stripes; shows: toucan-like shapes; colors not true to species; head shape not true to species |
| black-skimmer (bill too long) | minor | UNSURE | unsure: colors, head shape, bill longer than 1.5x head |
| brown-pelican (invented yellow plume) | major | FLAG | shows: any plume or crest on the head; shows: an oversized bulging pouch |
| double-crested-cormorant (crests and throat patch too large) | minor | UNSURE | unsure: colors, head shape |
| eastern-screech-owl (reads as a Great Horned Owl) | major | FLAG | colors not true to species; head shape not true to species |
| marbled-godwit (navy body instead of buff) | major | FLAG | shows: a navy or black body; colors not true to species |
| northern-bobwhite (quail plume topknot) | major | FLAG | shows: a tall plume or topknot (that is a California or Gambel's quail); colors not true to species |
| osprey (exaggerated spiky crest) | major | FLAG | shows: a tall spiky crest |
| red-headed-woodpecker (no white wing patch) | minor | UNSURE | unsure: sharply divided body and wing fields, head shape |
| rose-breasted-grosbeak (bill drawn as an outline only) | minor | UNSURE | unsure: head shape |
| ruffed-grouse (looks like a chicken) | minor | FLAG | colors not true to species |

Flagged and not on either list, each looked at by eye at 96 px against the brief's features:

- american-barn-owl: shows: a dark navy body; colors not true to species; head shape not true to species. **Eye check:** arguable: heart disc and bill are right; the navy body is unlike a pale barn owl
- black-and-white-warbler: reads as wood duck (0.46). **Eye check:** false alarm: bold stripes and slender bill are right
- blackburnian-warbler: reads as eastern meadowlark (0.33); head shape not true to species. **Eye check:** false alarm: angular face marks and bright throat are right
- cerulean-warbler: head shape not true to species. **Eye check:** false alarm: fine bill, wing bars and breast band are right
- great-blue-heron: colors not true to species. **Eye check:** palette: navy and ivory stand in for blue-grey; S-neck, plume and bill are right
- hooded-warbler: reads as american oystercatcher (0.55); colors not true to species; head shape not true to species. **Eye check:** false alarm: dark hood around a bright face is right
- peregrine-falcon: reads as american oystercatcher (0.33); colors not true to species; head shape not true to species. **Eye check:** false alarm: hood, cheek stripe and hooked bill are right
- swainsons-warbler: reads as wood duck (0.33). **Eye check:** false alarm: long bill and pale eyebrow are right
- whimbrel: colors not true to species. **Eye check:** palette: navy stands in for brown; crown stripes and curved bill are right
- wild-turkey: reads as double crested cormorant (0.46); missing: small bare head; missing: distinct wattle and snood. **Eye check:** false alarm: the bare red head, wattle and snood are clearly drawn

## 2. Chris's blind votes on the 36 bake-off tiles

Rank = position of Chris's best pick when the six tiles are sorted by likeness (1 = QA agrees).
"Generic" ranks by likeness without the review-derived avoid lists. By chance, rank 1 happens 1 time in 6 per bird.

| Bird | Chris's best | QA rank | QA rank (generic) | Tiles flagged |
|---|---|---|---|---|
| american-kestrel | O-ras-23 | 1 | 1 | 4 of 6 |
| black-skimmer | O-ras-11 | 1 | 3 | 0 of 6 |
| brown-pelican | R-vec-23 | 1 | 1 | 1 of 6 |
| eastern-screech-owl | none works | - | - | 6 of 6 (all should fail) |
| great-blue-heron | O-ras-11 | 1 | 1 | 3 of 6 |
| northern-bobwhite | O-ras-23 | 1 | 1 | 5 of 6 |

Chris's best pick ranks first for 5 of 5 birds (4 of 5 generic). n = 5: all five first by chance would be (1/6)^5, about 1 in 7,800.
The verdict fails in both directions: it flags good tiles, and it passes tiles Chris rejected (see the skimmer and pelican rows).

## 3. Chris's blind votes on round 2 (40 tiles: 4 new drafts plus the current version per bird)

Rank among 5 tiles (chance of rank 1 is 1 in 5 per bird), with and without the palette note in state.

| Bird | Chris's best | QA rank | QA rank (palette note) | Tiles flagged (no note / note) |
|---|---|---|---|---|
| brown-pelican | O-ras-1 | 2 | 1 | 2 / 3 of 5 |
| great-blue-heron | O-ras-2 | 4 | 1 | 1 / 0 of 5 |
| marbled-godwit | O-ras-2 | 3 | 3 | 5 / 5 of 5 |
| osprey | O-ras-4 | 4 | 4 | 1 / 1 of 5 |
| eastern-screech-owl | none works | - | - | 5 / 5 of 5 |
| american-barn-owl | none works | - | - | 1 / 4 of 5 |
| american-kestrel | none works | - | - | 1 / 1 of 5 |
| black-skimmer | none works | - | - | 0 / 0 of 5 |

Chris's best pick ranks first for 0 of 4 birds (2 of 4 with the palette note).
