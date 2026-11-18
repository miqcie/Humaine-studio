# Logos

The curlew is the logo. The wordmark sets the name for places without the font.

## Curlew

A curlew's head and shoulders inside an ink frame. It is traced from draft 5 of the twelve October drafts (`design-system/sources/curlew-draft.png`) by `design-system/trace_curlew.py`. The script reads its colors from `tokens.json`, so rerun it after a palette change.

- `humaine-curlew.svg`: primary. A Klein blue bird (`mark-blue`) with a chrome wing on a paper field in an ink frame. The bird reads 10:1 on paper; the wing reads 6:1 on the bird. The bird is blue, not black, because ink on Klein is only 1.7:1.
- `humaine-curlew-vermilion.svg`: alternate, for a second voice (a talk, a sticker). An ink bird with a chrome wing on a vermilion field (3.4:1).
- Uses: the header lockup (32px), the favicon set, the social card, avatars, title slides, a page hero.
- Sizes: comfortable from 32px up. At 16px (the smallest favicon) the eye and beak soften; a hand-tuned 16px version is a planned iteration.
- The favicons (`favicon.svg`, `.ico`, 32, 180 and 512px PNGs) are rendered from this file by `design-system/build_brand.py`, squared off with the frame's ink.

## Wordmark

"Humaine Studio" in Fraunces 800 at full softness (`"SOFT" 100, "WONK" 0`), letter-spacing −0.02em, converted to outlines by `design-system/build_brand.py`, so it renders the same without the font.

- `humaine-wordmark-ink.svg`: `mark-line` ink, for linen, paper and other light grounds.
- `humaine-wordmark-linen.svg`: paper, for Klein and Klein Night grounds.
- Use it where live text is not available: social cards, email signatures, slides, print. On the web, set the name in type with the `Lockup` component instead.

## Rules

- Fixed colors in both themes. On the Klein Night ground the curlew's ink frame merges into the background; where it sits large (a hero), give it a 1px `rule` outline so it does not float.
- Do not recolor, rotate, crop, add a shadow or round the corners. Do not put text on the curlew.
- The Mondrian block mark is retired; the other curlew drafts and the "Humane Studio" concept image are not part of the system.
