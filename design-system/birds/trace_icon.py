#!/usr/bin/env python3
"""Trace one raster bird icon into the house frame and palette (the curlew logo's method, see trace_curlew.py).

Run: uv run --with pillow --with numpy --with scipy python design-system/birds/trace_icon.py SRC.png OUT.svg [X0 Y0 X1 Y1]
X0..Y1 (optional) is the outer edge of the source icon's frame on a sheet. Without it, the frame is found by
itself; a source with no frame is treated as all field. Needs potrace.
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
# Every pixel snaps to its nearest house color. Field first: it is the background and is not traced.
PALETTE = [S.F, S.N, S.Y, S.R, S.B, S.M]


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def find_frame(a):
    """Outer box and ring width of a dark square frame, or None. A frame edge is a row or column that is
    at least 85% dark; the ring width is measured on the top and right edges, which the bird never touches."""
    dark = a.mean(axis=2) < 70
    rows, cols = np.where(dark.mean(axis=1) > 0.85)[0], np.where(dark.mean(axis=0) > 0.85)[0]
    if len(rows) < 2 or len(cols) < 2:
        return None
    y0, y1, x0, x1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
    if min(y1 - y0, x1 - x0) < 0.5 * min(a.shape[:2]):
        return None
    top = int(np.argmin(dark[y0:, (x0 + x1) // 2])) if dark[y0, (x0 + x1) // 2] else 0
    right = int(np.argmin(dark[(y0 + y1) // 2, x0:x1][::-1]))
    ring = min(top, right)
    assert 2 < ring < (x1 - x0) // 6, f"frame ring {ring}px is implausible"
    return x0, y0, x1, y1, ring


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


def convert(src, out, box=None):
    a = np.asarray(Image.open(src).convert("RGB")).astype(float)
    if box:
        a = a[box[1]:box[3], box[0]:box[2]]
    fr = find_frame(a)
    if fr:
        x0, y0, x1, y1, r = fr
        a = a[y0 + r:y1 - r, x0 + r:x1 - r]  # the source field only
    s = min(a.shape[:2])
    a = a[:s, :s] if fr else a[(a.shape[0] - s) // 2:][:s, (a.shape[1] - s) // 2:][:, :s]
    protos = np.array([rgb(c) for c in PALETTE], float)
    label = np.argmin(np.linalg.norm(a[..., None, :] - protos, axis=-1), axis=-1)
    k = (SIZE - 2 * RING) / s
    layers, share = [], {}
    for i, color in enumerate(PALETTE):
        mask = label == i
        share[color] = round(float(mask.mean()), 3)
        if i == 0 or mask.mean() < 0.002:  # field, or specks
            continue
        g, d = trace(mask)
        if d:
            layers.append(f'<path transform="translate({RING},{RING}) scale({k:.5f}) scale({1 / UP}) {g}" fill="{color}" d="{d}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}">'
           f'<rect width="{SIZE}" height="{SIZE}" fill="{S.N}"/>'
           f'<rect x="{RING}" y="{RING}" width="{SIZE - 2 * RING}" height="{SIZE - 2 * RING}" fill="{S.F}"/>'
           f'<clipPath id="f"><rect x="{RING}" y="{RING}" width="{SIZE - 2 * RING}" height="{SIZE - 2 * RING}"/></clipPath>'
           f'<g clip-path="url(#f)">{"".join(layers)}</g></svg>\n')
    fills = set(re.findall(r'fill="(#[0-9A-Fa-f]{6})"', svg))
    assert fills <= set(PALETTE), fills  # palette only, always
    n = len(fills)
    note = "" if 3 <= n <= 4 else f"  NOTE {n} colors (brief: 3-4)"
    pathlib.Path(out).write_text(svg)
    print(f"{out}: frame {'found, ring %dpx' % fr[4] if fr else 'none'}, {len(layers)} layers, {n} colors{note}")
    return {"frame": bool(fr), "colors": n, "share": share}


if __name__ == "__main__":
    src, out, *box = sys.argv[1:]
    convert(src, out, tuple(map(int, box)) or None)
