#!/usr/bin/env python3
"""Trace one raster bird icon into the house frame and palette (the curlew logo's method, see trace_curlew.py).

Run: uv run --with pillow --with numpy --with scipy python design-system/birds/trace_icon.py SHEET.png X0 Y0 X1 Y1 OUT.svg
X0..Y1 is the outer edge of the source icon's frame. Needs potrace.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import species as S  # noqa: E402

UP, SIZE, RING = 4, 240, 13
# Source colors (sampled from the draft) -> house palette. Background and frame map to field and navy.
CLASSES = {"field": ((243, 236, 224), S.F), "navy": ((12, 16, 36), S.N), "yellow": ((246, 186, 2), S.Y),
           "red": ((196, 50, 30), S.R), "blue": ((4, 48, 168), S.B), "muted": ((94, 97, 120), S.M)}


def ring_width(a):
    """Navy run length along the top edge, measured at the middle column (the bird never touches the top)."""
    col = a[:, a.shape[1] // 2]
    dark = np.linalg.norm(col - CLASSES["navy"][0], axis=1) < 80
    n = int(np.argmin(dark))
    assert 5 < n < a.shape[0] // 8, f"frame ring not found ({n}px)"
    return n


def trace(mask):
    h, w = mask.shape
    m = ndimage.gaussian_filter(mask.astype("float32"), 1.0)
    big = np.asarray(Image.fromarray(m).resize((w * UP, h * UP), Image.BICUBIC))
    with tempfile.TemporaryDirectory() as td:
        pbm, svg = pathlib.Path(td) / "m.pbm", pathlib.Path(td) / "m.svg"
        Image.fromarray(np.where(big >= 0.5, 0, 255).astype("uint8")).convert("1").save(pbm)
        subprocess.run(["potrace", "-s", "--flat", "-t", "16", "-a", "1.2", "-O", "0.8", "-o", svg, pbm], check=True)
        text = svg.read_text()
    g = re.search(r'<g transform="([^"]+)"', text).group(1)
    return g, " ".join(re.findall(r' d="([^"]+)"', text))


def main(sheet, x0, y0, x1, y1, out):
    a = np.asarray(Image.open(sheet).convert("RGB")).astype(float)[y0:y1, x0:x1]
    r = ring_width(a)
    a = a[r:-r, r:-r]  # the source field only
    protos = np.array([c[0] for c in CLASSES.values()], float)
    label = np.argmin(np.linalg.norm(a[..., None, :] - protos, axis=-1), axis=-1)
    h, w = label.shape
    k = (SIZE - 2 * RING) / w
    layers = []
    for i, (name, (_, color)) in enumerate(CLASSES.items()):
        mask = label == i
        if name == "field" or mask.sum() < 30:
            continue
        g, d = trace(mask)
        layers.append(f'<path transform="translate({RING},{RING}) scale({k}) scale({1 / UP}) {g}" fill="{color}" d="{d}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}">'
           f'<rect width="{SIZE}" height="{SIZE}" fill="{S.N}"/>'
           f'<rect x="{RING}" y="{RING}" width="{SIZE - 2 * RING}" height="{SIZE - 2 * RING}" fill="{S.F}"/>'
           f'<clipPath id="f"><rect x="{RING}" y="{RING}" width="{SIZE - 2 * RING}" height="{SIZE - 2 * RING}"/></clipPath>'
           f'<g clip-path="url(#f)">{"".join(layers)}</g></svg>\n')
    fills = set(re.findall(r'fill="(#[0-9A-Fa-f]{6})"', svg))
    assert fills <= {c[1] for c in CLASSES.values()}, fills  # palette only
    pathlib.Path(out).write_text(svg)
    print(out, f"ring {r}px, {len(layers)} color layers, {len(svg)} bytes")


if __name__ == "__main__":
    s, *n, o = sys.argv[1:]
    main(s, *map(int, n), o)
