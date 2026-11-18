#!/usr/bin/env python3
"""Trace the curlew draft into vector marks recolored to the Klein & Linen palette.

Run: uv run --with pillow --with numpy --with scipy python design-system/trace_curlew.py
Needs: potrace (brew install potrace). Source: design-system/sources/curlew-draft.png (512px, draft 5 of 12).
Writes: design-system/project/assets/Logos/humaine-curlew.svg and humaine-curlew-vermilion.svg.
"""
import json
import pathlib
import re
import subprocess
import tempfile

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).parent
SRC = HERE / "sources" / "curlew-draft.png"
OUT = HERE / "project" / "assets" / "Logos"
UP = 4  # upsample masks before tracing so curves come out smooth

# Frame box measured from the draft (outer edge 45..466 x 45..461, ring 23px).
X0, Y0, X1, Y1, RING = 45, 45, 467, 462, 23

tokens = {t["name"]: t["value"] for t in json.loads((HERE / "project" / "tokens.json").read_text())["color"]["tokens"]}
INK, PAPER, BLUE, RED = tokens["mark-line"], tokens["mark-field"], tokens["mark-blue"], tokens["mark-red"]
CHROME = tokens["chrome"]

VARIANTS = {
    # name: (frame, field, bird, wing, eye ring)
    "humaine-curlew.svg": (INK, PAPER, BLUE, CHROME, PAPER),
    "humaine-curlew-vermilion.svg": (INK, RED, INK, CHROME, PAPER),
}


def masks():
    a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)[Y0:Y1, X0:X1]
    lum = a.mean(axis=2)
    yellow = (a[..., 0] > 170) & (a[..., 2] < 120)
    black = (lum < 110) & ~yellow
    white = ~black & ~yellow
    h, w = lum.shape
    inner = np.zeros_like(black)
    inner[RING:h - RING, RING:w - RING] = True
    # Self-checks: the ring really is black, and the field just inside it is mostly white.
    assert black[:RING].mean() > 0.95 and black[:, w - RING:].mean() > 0.95, "frame not where measured"
    assert white[RING + 2, RING:w - RING].mean() > 0.6, "field not where measured"
    lab, n = ndimage.label(white & inner)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    field_id = int(np.argmax(sizes)) + 1
    eye = (lab > 0) & (lab != field_id) & np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 40])
    assert 200 < eye.sum() < 8000, f"eye ring not found ({eye.sum()} px)"
    return w, h, {"bird": black & inner, "wing": yellow & inner, "eye": eye}


def trace(mask):
    h, w = mask.shape
    img = Image.fromarray((mask * 255).astype("uint8")).resize((w * UP, h * UP), Image.BICUBIC)
    bw = img.point(lambda v: 0 if v >= 128 else 255, "1")  # potrace traces black pixels
    with tempfile.TemporaryDirectory() as td:
        pbm, svg = pathlib.Path(td) / "m.pbm", pathlib.Path(td) / "m.svg"
        bw.save(pbm)
        subprocess.run(["potrace", "-s", "--flat", "-t", "8", "-a", "1.0", "-O", "0.4", "-o", svg, pbm], check=True)
        text = svg.read_text()
    g = re.search(r'<g transform="([^"]+)"', text).group(1)
    d = " ".join(re.findall(r' d="([^"]+)"', text))
    assert d, "potrace produced no path"
    return f'scale({1 / UP}) {g}', d


def main():
    w, h, m = masks()
    paths = {k: trace(v) for k, v in m.items()}
    for name, (frame, field, bird, wing, eye) in VARIANTS.items():
        layers = "".join(f'<path transform="{paths[k][0]}" fill="{c}" d="{paths[k][1]}"/>' for k, c in (("bird", bird), ("wing", wing), ("eye", eye)))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t"><title id="t">Humaine Studio curlew</title>'
               f'<rect width="{w}" height="{h}" fill="{frame}"/><rect x="{RING}" y="{RING}" width="{w - 2 * RING}" height="{h - 2 * RING}" fill="{field}"/>'
               f'<svg x="{RING}" y="{RING}" width="{w - 2 * RING}" height="{h - 2 * RING}" viewBox="{RING} {RING} {w - 2 * RING} {h - 2 * RING}" overflow="hidden">{layers}</svg></svg>\n')
        (OUT / name).write_text(svg)
        print(name, len(svg), "bytes")


main()
