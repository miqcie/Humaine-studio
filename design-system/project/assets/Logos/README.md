# Logos

Two marks that share one frame. The Mondrian block mark is the logo. The curlew is the studio's character.

## Block mark

A framed field split into a large open field, a yellow block, a small colored block and a small open block. Same geometry as the favicon in `assets/images/icons/`, measured from the 512px PNG; only the colors changed.

- `humaine-mark.svg`: primary. Klein blue block. `mark-line` #0E1230, `mark-field` #FAF6EE, `mark-yellow` #F7B902, `mark-blue` #002FA7.
- `humaine-mark-vermilion.svg`: alternate. `mark-red` #C7301C in place of the blue.
- Use it for the favicon, the Lockup, and anywhere under 32px. Smallest size 16px.

## Curlew

A curlew's head and shoulders inside the same ink frame. It is traced from draft 5 of the twelve October drafts (`design-system/sources/curlew-draft.png`) by `design-system/trace_curlew.py`. The script reads its colors from `tokens.json`, so rerun it after a palette change.

- `humaine-curlew.svg`: primary. A Klein blue bird (`mark-blue`) with a chrome wing on a paper field in an ink frame. The bird reads 10:1 on paper; the wing reads 6:1 on the bird. The bird is blue, not black, because ink on Klein is only 1.7:1.
- `humaine-curlew-vermilion.svg`: alternate. An ink bird with a chrome wing on a vermilion field (3.4:1).
- Use it for avatars, social cards, talk title slides, stickers and a page hero. Smallest size 32px: below that the beak and eye blur, so use the block mark.
- One curlew per view. Do not put it beside the block mark at the same size; the block mark goes in the header, the curlew in the content.

## Rules for both

- Fixed colors in both themes. On the Klein Night ground the blue-black frame merges into the background and the colored fields carry the mark. That is intended; there is no inverted file.
- Do not recolor, rotate, crop, add a shadow or round the corners. Do not put text on a mark.
- The name is set in type next to the block mark (see the Lockup component), not drawn into a file.
- The other curlew drafts and the "Humane Studio" concept image are not part of the system.
