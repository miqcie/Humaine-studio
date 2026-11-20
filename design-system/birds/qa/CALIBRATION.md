# Calibration of the likeness check

## 1. Known errors in the 30 OpenAI icons

Caught 6 of 6 known errors. Flagged 11 of the other 24 icons.
From the generic questions alone (without the review-derived "avoid" lists): caught 5 of 6.

| Known error | Verdict | Why |
|---|---|---|
| american-kestrel (no face stripes; reads as a toucan) | FLAG | reads as red headed woodpecker (0.36); missing: two dark vertical face stripes; shows: toucan-like shapes; colors not true to species; head shape not true to species |
| brown-pelican (invented yellow plume) | FLAG | shows: any plume or crest on the head; shows: an oversized bulging pouch |
| eastern-screech-owl (reads as a Great Horned Owl) | FLAG | colors not true to species; head shape not true to species |
| marbled-godwit (navy body instead of buff) | FLAG | reads as marbled godwit (0.46) |
| northern-bobwhite (quail plume topknot) | FLAG | shows: a tall plume or topknot (that is a California or Gambel's quail); colors not true to species |
| osprey (exaggerated spiky crest) | FLAG | reads as osprey (0.44); missing: bold dark eye stripe |

Flagged but not on the known-error list (check by eye: new errors or false alarms):

- american-barn-owl: colors not true to species; head shape not true to species
- black-and-white-warbler: reads as wood duck (0.46)
- blackburnian-warbler: reads as eastern meadowlark (0.33); head shape not true to species
- cerulean-warbler: head shape not true to species
- great-blue-heron: colors not true to species
- hooded-warbler: reads as american oystercatcher (0.55); colors not true to species; head shape not true to species
- peregrine-falcon: reads as american oystercatcher (0.33); colors not true to species; head shape not true to species
- ruffed-grouse: colors not true to species
- swainsons-warbler: reads as wood duck (0.33)
- whimbrel: colors not true to species
- wild-turkey: reads as double crested cormorant (0.46); missing: small bare head; missing: distinct wattle and snood

## 2. Chris's blind votes on the 36 bake-off tiles

Rank = position of Chris's best pick when the six tiles are sorted by likeness (1 = QA agrees).

| Bird | Chris's best | QA rank of it | QA's top tile | Tiles flagged |
|---|---|---|---|---|
| american-kestrel | O-ras-23 | 1 | O-ras-23 | 5 of 6 |
| black-skimmer | O-ras-11 | 1 | O-ras-11 | 0 of 6 |
| brown-pelican | R-vec-23 | 1 | R-vec-23 | 1 of 6 |
| eastern-screech-owl | none works | - | O-ras-23 | 6 of 6 (all should fail) |
| great-blue-heron | O-ras-11 | 1 | O-ras-11 | 3 of 6 |
| northern-bobwhite | O-ras-23 | 1 | O-ras-23 | 5 of 6 |

Chris's best pick is in QA's top 2 for 5 of 5 birds.
