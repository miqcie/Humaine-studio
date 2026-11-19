#!/usr/bin/env python3
"""Build the Virginia bird concept sheets (light linen treatment).

Run: uv run --with pillow --with fonttools --with brotli python design-system/birds/build.py [slug ...]
Needs: rsvg-convert (brew install librsvg).
Writes: design-system/birds/concepts/{icons,sheets}/ as SVG + PNG.

Self-checks (assert): 30 species, 5 per region, labels verbatim from the brief; every fill in the palette;
3-4 colors per icon; no thin strokes; no geometry within CLEAR of the frame except where the bird bleeds.
"""
import io
import pathlib
import re
import subprocess
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image

from species import BIRDS, REGIONS
import species as S

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
OUT = HERE / "concepts"

# Frame geometry, icon units (one icon = 240 x 240). Ring is 5.5% of the width, as in the curlew logo.
SIZE, RING, CLEAR = 240, 13, 10
LO, HI = RING, SIZE - RING
PALETTE = {S.N, S.F, S.G, S.SUNK, S.RULE, S.M, S.Y, S.R, S.B}


def rsvg(svg: str, width: int) -> bytes:
    return subprocess.run(["rsvg-convert", "-w", str(width), "-f", "png"], input=svg.encode(), capture_output=True, check=True).stdout


# ---------- icons ----------

def icon(slug: str, bird: dict) -> str:
    """Icon body in 0..240 units: navy frame, ivory field, bird clipped to the field."""
    return (f'<rect width="{SIZE}" height="{SIZE}" fill="{S.N}"/>'
            f'<rect x="{LO}" y="{LO}" width="{HI - LO}" height="{HI - LO}" fill="{S.F}"/>'
            f'<clipPath id="{slug}-field"><rect x="{LO}" y="{LO}" width="{HI - LO}" height="{HI - LO}"/></clipPath>'
            f'<g clip-path="url(#{slug}-field)">{bird["art"](slug)}</g>')


def icon_svg(slug: str, bird: dict) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" role="img">'
            f'<title>{bird["name"]}</title>{icon(slug, bird)}</svg>')


def check(slug: str, bird: dict):
    art = bird["art"](slug)
    fills = {c.upper() for c in re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"', art)}
    assert not re.search(r"Gradient|filter|opacity", art), f"{slug}: gradient, filter or opacity"
    assert fills <= {c.upper() for c in PALETTE}, f"{slug}: off-palette {fills - {c.upper() for c in PALETTE}}"
    n = len(fills | {S.N.upper(), S.F.upper()})
    assert 3 <= n <= 4, f"{slug}: {n} colors {sorted(fills)}"
    for w in re.findall(r'stroke-width="([\d.]+)"', art):
        assert float(w) >= 6, f"{slug}: stroke {w} is too thin"  # keylines are clipped in half: 3 units minimum
    # Overflow: render the unclipped bird and look for paint near the frame on sides it does not bleed through.
    pad = 60
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {SIZE + 2 * pad} {SIZE + 2 * pad}">{art}</svg>')
    a = Image.open(io.BytesIO(rsvg(svg, SIZE + 2 * pad))).getchannel("A").load()
    bleed = bird.get("bleed", {"left", "bottom"})
    lo, hi = LO + CLEAR, HI - CLEAR
    bad = []
    for y in range(SIZE + 2 * pad):
        for x in range(SIZE + 2 * pad):
            if a[x, y] < 128:
                continue
            u, v = x - pad, y - pad
            if (u < lo and "left" not in bleed) or (u > hi and "right" not in bleed) or \
               (v < lo and "top" not in bleed) or (v > hi and "bottom" not in bleed):
                bad.append((u, v))
    if bad:
        xs, ys = [p[0] for p in bad], [p[1] for p in bad]
        raise AssertionError(f"{slug}: paint within {CLEAR} of the frame at x {min(xs)}..{max(xs)}, y {min(ys)}..{max(ys)}")


# ---------- type (outlined, so sheets do not depend on installed fonts) ----------

_fonts = {}


def font(key):
    if key not in _fonts:
        file, axes = {"serif": ("fraunces-soft.woff2", {"wght": 500, "SOFT": 100, "WONK": 0, "opsz": 72}),
                      "sans": ("schibsted-grotesk.woff2", {"wght": 500}),
                      "sans-reg": ("schibsted-grotesk.woff2", {"wght": 400})}[key]
        f = TTFont(ROOT / "assets" / "fonts" / file)
        if "fvar" in f:
            have = {a.axisTag for a in f["fvar"].axes}
            f = instantiateVariableFont(f, {k: v for k, v in axes.items() if k in have})
        _fonts[key] = f
    return _fonts[key]


def text(s, x, y, size, key="sans", fill=S.N, anchor="start", track=0.0):
    """Outline a string. shortcut: no kerning pairs; fine for short labels, use a shaper (uharfbuzz) for body copy."""
    f = font(key)
    upm, cmap, gs, hmtx = f["head"].unitsPerEm, f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    k = size / upm
    names = [cmap[ord(ch)] for ch in s]
    widths = [hmtx[n][0] * k + track * size for n in names]
    total = sum(widths) - (track * size if names else 0)
    x0 = x - {"start": 0, "middle": total / 2, "end": total}[anchor]
    parts = []
    for n, w in zip(names, widths):
        pen = SVGPathPen(gs)
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, x0, y)))
        if pen.getCommands():
            parts.append(pen.getCommands())
        x0 += w
    return f'<path fill="{fill}" d="{" ".join(parts)}"/>'


# ---------- sheets ----------

W, CELL, GAP, MX = 1800, 440, 90, 150
TOP = 300


def sheet(i: int, region: dict) -> str:
    slugs = [s for s, b in BIRDS.items() if b["region"] == region["key"]]
    out = [f'<rect width="{W}" height="0" fill="{S.G}"/>']
    out.append(text(f"HUMAINE STUDIO · VIRGINIA BIRDS · {i} OF 6", MX, 120, 22, "sans", S.M, track=0.12))
    out.append(text(region["title"], MX, 196, 64, "serif", S.N))
    if region.get("sub"):
        out.append(text(region["sub"], MX, 246, 26, "sans-reg", S.M))
    rows = [slugs[:3], slugs[3:]]
    y = TOP
    for row in rows:
        span = len(row) * CELL + (len(row) - 1) * GAP
        x = (W - span) / 2
        for slug in row:
            k = CELL / SIZE
            out.append(f'<g transform="translate({x},{y}) scale({k})">{icon(slug, BIRDS[slug])}</g>')
            out.append(text(BIRDS[slug]["name"], x + CELL / 2, y + CELL + 54, 30, "sans", S.N, anchor="middle"))
            x += CELL + GAP
        y += CELL + 130
    h = y + 40
    out[0] = f'<rect width="{W}" height="{h}" fill="{S.G}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">{"".join(out)}</svg>'


def strip(slugs, px=96) -> str:
    """Confusable sets side by side at display size."""
    gap = 24
    w = len(slugs) * (px + gap) + gap
    body = "".join(f'<g transform="translate({gap + n * (px + gap)},{gap}) scale({px / SIZE})">{icon(s, BIRDS[s])}</g>'
                   for n, s in enumerate(slugs))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {px + 2 * gap}" width="{w}" height="{px + 2 * gap}"><rect width="{w}" height="{px + 2 * gap}" fill="{S.G}"/>{body}</svg>'


CONFUSABLE = {
    "blues": ["eastern-bluebird", "indigo-bunting", "cerulean-warbler"],
    "warblers": ["cerulean-warbler", "hooded-warbler", "blackburnian-warbler", "black-and-white-warbler", "swainsons-warbler"],
    "raptors": ["peregrine-falcon", "american-kestrel", "osprey"],
    "shorebirds": ["whimbrel", "marbled-godwit", "american-oystercatcher"],
    "owls": ["american-barn-owl", "eastern-screech-owl"],
}

BRIEF = {  # verbatim from the brief, in order
    "coastal": ["Whimbrel", "Marbled Godwit", "American Oystercatcher", "Brown Pelican", "Black Skimmer"],
    "piedmont": ["Eastern Bluebird", "Eastern Meadowlark", "Indigo Bunting", "Northern Bobwhite", "Red-headed Woodpecker"],
    "blue-ridge": ["Common Raven", "Scarlet Tanager", "Cerulean Warbler", "Peregrine Falcon", "Rose-breasted Grosbeak"],
    "valley": ["American Kestrel", "American Barn Owl", "Eastern Screech-Owl", "Belted Kingfisher", "Wild Turkey"],
    "plateau": ["Hooded Warbler", "Blackburnian Warbler", "Black-and-white Warbler", "Swainson’s Warbler", "Ruffed Grouse"],
    "rva": ["Great Blue Heron", "Osprey", "Double-crested Cormorant", "Wood Duck", "Chimney Swift"],
}


def main(only):
    (OUT / "icons").mkdir(parents=True, exist_ok=True)
    (OUT / "sheets").mkdir(parents=True, exist_ok=True)
    (OUT / "strips").mkdir(parents=True, exist_ok=True)
    todo = only or list(BIRDS)
    for slug in todo:
        check(slug, BIRDS[slug])
        svg = icon_svg(slug, BIRDS[slug])
        (OUT / "icons" / f"{slug}.svg").write_text(svg)
        (OUT / "icons" / f"{slug}.png").write_bytes(rsvg(svg, 480))
    print(f"checked {len(todo)} icons")
    if only:
        return
    for key, names in BRIEF.items():
        got = [b["name"] for b in BIRDS.values() if b["region"] == key]
        assert got == names, f"{key}: {got} != {names}"
    assert len(BIRDS) == 30 and len({b["name"] for b in BIRDS.values()}) == 30
    for i, region in enumerate(REGIONS, 1):
        svg = sheet(i, region)
        name = f"{i}-{region['key']}"
        (OUT / "sheets" / f"{name}.svg").write_text(svg)
        (OUT / "sheets" / f"{name}.png").write_bytes(rsvg(svg, W))
    for name, slugs in CONFUSABLE.items():
        svg = strip(slugs)
        (OUT / "strips" / f"{name}.svg").write_text(svg)
        (OUT / "strips" / f"{name}.png").write_bytes(rsvg(svg, int(re.search(r'width="(\d+)"', svg).group(1)) * 2))
    print("wrote 6 sheets and", len(CONFUSABLE), "strips")


if __name__ == "__main__":
    main(sys.argv[1:])
