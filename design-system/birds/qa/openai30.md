# Likeness check: openai30

Palette note in state: no. "Colors not true to species" fired on 9 of 30 icons.

Model `jev-1.14.0` (image questions are experimental). 30 icons: 1 pass, 13 unsure, 16 flagged.
Noul read as yes above 0.7, no below 0.3. Species is read from a 30-way Choice at 480 px and at 64 px.

| Icon | Verdict | Species p (480 / 64) | Style | Likeness | Bill ÷ head (ref) | Why |
|---|---|---|---|---|---|---|
| american-barn-owl | FLAG | 0.97 / 0.96 | 2.48 | 0.72 | - | colors not true to species; head shape not true to species |
| american-kestrel | FLAG | 0.04 / 0.13 | 2.77 | 0.188 | 0.26 (0.25) | reads as red headed woodpecker (0.36); missing: two dark vertical face stripes; shows: toucan-like shapes; colors not true to species; head shape not true to species |
| american-oystercatcher | UNSURE | 1.0 / 1.0 | 2.82 | 0.91 | 0.93 | unsure: head shape |
| belted-kingfisher | UNSURE | 0.95 / 0.94 | 2.48 | 0.85 | 0.33 | unsure: colors, head shape |
| black-and-white-warbler | FLAG | 0.4 / 0.52 | 2.31 | 0.714 | 0.22 | reads as wood duck (0.46) |
| black-skimmer | UNSURE | 0.9 / 0.9 | 2.37 | 0.676 | 0.52 (1.45) | unsure: colors, head shape, bill longer than 1.5x head |
| blackburnian-warbler | FLAG | 0.11 / 0.14 | 2.82 | 0.579 | 0.22 | reads as eastern meadowlark (0.33); head shape not true to species |
| brown-pelican | FLAG | 0.98 / 0.98 | 2.66 | 0.583 | 1.41 (3.2) | shows: any plume or crest on the head; shows: an oversized bulging pouch |
| cerulean-warbler | FLAG | 0.66 / 0.69 | 2.38 | 0.743 | 0.21 | head shape not true to species |
| chimney-swift | UNSURE | 1.0 / 1.0 | 2.62 | 0.821 | 0.29 | unsure: compact body, short tail, colors, head shape |
| common-raven | PASS | 0.98 / 0.95 | 2.47 | 0.897 | 0.38 |  |
| double-crested-cormorant | UNSURE | 0.71 / 0.79 | 2.66 | 0.783 | 0.61 | unsure: colors, head shape |
| eastern-bluebird | UNSURE | 0.81 / 0.93 | 2.76 | 0.844 | 0.25 | unsure: head shape |
| eastern-meadowlark | UNSURE | 0.78 / 0.83 | 2.75 | 0.819 | 0.36 | unsure: head shape |
| eastern-screech-owl | FLAG | 0.93 / 0.94 | 2.69 | 0.564 | 0.09 | colors not true to species; head shape not true to species |
| great-blue-heron | FLAG | 0.97 / 0.97 | 2.4 | 0.769 | 0.64 (1.05) | colors not true to species |
| hooded-warbler | FLAG | 0.27 / 0.32 | 2.86 | 0.591 | 0.26 | reads as american oystercatcher (0.55); colors not true to species; head shape not true to species |
| indigo-bunting | UNSURE | 0.71 / 0.67 | 2.79 | 0.782 | 0.23 | unsure: colors, head shape |
| marbled-godwit | UNSURE | 0.46 / 0.13 | 2.78 | 0.657 | 1.31 (2.8) | unsure: species only 0.46, very long, slightly upturned bill, colors, head shape |
| northern-bobwhite | FLAG | 0.94 / 0.91 | 2.75 | 0.57 | 0.16 (0.3) | shows: a tall plume or topknot (that is a California or Gambel's quail); colors not true to species |
| osprey | FLAG | 0.44 / 0.43 | 2.57 | 0.637 | 0.23 (0.3) | missing: bold dark eye stripe |
| peregrine-falcon | FLAG | 0.17 / 0.14 | 2.43 | 0.523 | 0.19 | reads as american oystercatcher (0.33); colors not true to species; head shape not true to species |
| red-headed-woodpecker | UNSURE | 0.97 / 0.97 | 2.82 | 0.853 | 0.51 | unsure: sharply divided body and wing fields, head shape |
| rose-breasted-grosbeak | UNSURE | 0.98 / 0.96 | 2.3 | 0.883 | 0.33 | unsure: head shape |
| ruffed-grouse | FLAG | 0.61 / 0.58 | 2.33 | 0.642 | 0.22 | colors not true to species |
| scarlet-tanager | UNSURE | 0.82 / 0.92 | 2.85 | 0.856 | 0.34 | unsure: head shape |
| swainsons-warbler | FLAG | 0.16 / 0.15 | 2.52 | 0.585 | 0.27 | reads as wood duck (0.33) |
| whimbrel | FLAG | 0.96 / 0.99 | 2.54 | 0.835 | 0.96 | colors not true to species |
| wild-turkey | FLAG | 0.15 / 0.18 | 2.76 | 0.491 | 0.47 | reads as double crested cormorant (0.46); missing: small bare head; missing: distinct wattle and snood |
| wood-duck | UNSURE | 1.0 / 0.99 | 2.63 | 0.879 | 0.25 | unsure: colors, head shape |
