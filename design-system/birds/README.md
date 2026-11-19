# Virginia birds: concept sheets

30 bird icons in six regional sets of five. They extend the curlew logo. These are **concepts in the light Klein & Linen treatment**. They are not finished production assets.

## Files

- `species.py`: the geometry of each bird (240 × 240 units) and the palette.
- `build.py`: the checks, and the builder for the icons, sheets and strips.
- `concepts/sheets/`: one sheet per region, SVG and PNG (1800 px wide).
- `concepts/icons/`: one icon per species, SVG and PNG (480 px).
- `concepts/strips/`: the birds that are easy to confuse, side by side at 96 px.

## Build

```sh
uv run --with pillow --with fonttools --with brotli python design-system/birds/build.py           # all
uv run --with pillow --with fonttools --with brotli python design-system/birds/build.py osprey    # one icon, checks only
```

You need `rsvg-convert` (`brew install librsvg`). The labels are converted to outlines from `assets/fonts/`, so the sheets do not need installed fonts.

## Rules that every icon shares

- A navy frame 13 units wide (5.5%, the same as the logo). An ivory field. The bird faces right.
- The bird can go off the left and bottom edges only. Bills, crests and wing tips stay 10 units or more inside the frame. `build.py` checks this on the unclipped art.
- The eye has an ivory ring on dark plumage and is a navy dot on pale or yellow plumage. A species with a colored eye or eye ring uses that color (Oystercatcher, Peregrine, Osprey, Cormorant, Wood Duck).
- Pale plumage never touches the field. It sits inside the dark silhouette, or behind a keyline in the bird's own color.
- The chrome-yellow wing from the logo recurs on five birds: Whimbrel, Black Skimmer, Osprey, Chimney Swift and the Barn Owl's body. It is not used where the wing is the identifying mark.
- Only flat fills from the palette. Each icon has 3 or 4 colors, frame and field included. `build.py` checks this.

## Open decisions

- **Navy.** The icons use `#0B0F24` (Klein Night ground), as the brief's palette table gives. The live logo frame is `#0E1230` (`mark-line`). To change it, edit `N` in `species.py`.
- **Weakest forms:** American Kestrel (the face reads as a helmet), Peregrine Falcon and Osprey (similar structure, told apart only by crown color), Ruffed Grouse (small crest).

## Not done yet (after a direction is chosen)

Dark Klein Night versions, clean master SVGs (the keylines are clipped strokes now; expand them to paths), transparent PNGs, separate favicon designs at 16, 32, 64 and 128 px, and ICO files.
