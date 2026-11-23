#!/usr/bin/env python3
"""Shared helpers for the bird sheets: rsvg, outlined type, the regional sheet and the confusable strip.

Used by assemble.py (final set) and bakeoff/run.py (blind sheets). Needs rsvg-convert and fontTools.
"""
import pathlib
import subprocess

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

from species import BIRDS
import species as S

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent

SIZE = 240  # icon units: one icon is 240 x 240


def rsvg(svg: str, width: int) -> bytes:
    return subprocess.run(["rsvg-convert", "-w", str(width), "-f", "png"], input=svg.encode(), capture_output=True, check=True).stdout


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


def sheet(i: int, region: dict, art) -> str:
    """One regional sheet. `art(slug)` returns the icon body in 240-unit space."""
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
            out.append(f'<g transform="translate({x},{y}) scale({k})">{art(slug)}</g>')
            out.append(text(BIRDS[slug]["name"], x + CELL / 2, y + CELL + 54, 30, "sans", S.N, anchor="middle"))
            x += CELL + GAP
        y += CELL + 130
    h = y + 40
    out[0] = f'<rect width="{W}" height="{h}" fill="{S.G}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">{"".join(out)}</svg>'


def strip(slugs, art, px=96) -> str:
    """Confusable sets side by side at display size."""
    gap = 24
    w = len(slugs) * (px + gap) + gap
    body = "".join(f'<g transform="translate({gap + n * (px + gap)},{gap}) scale({px / SIZE})">{art(s)}</g>'
                   for n, s in enumerate(slugs))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {px + 2 * gap}" width="{w}" height="{px + 2 * gap}"><rect width="{w}" height="{px + 2 * gap}" fill="{S.G}"/>{body}</svg>'


CONFUSABLE = {
    "blues": ["eastern-bluebird", "indigo-bunting", "cerulean-warbler"],
    "warblers": ["cerulean-warbler", "hooded-warbler", "blackburnian-warbler", "black-and-white-warbler", "swainsons-warbler"],
    "raptors": ["peregrine-falcon", "american-kestrel", "osprey"],
    "shorebirds": ["whimbrel", "marbled-godwit", "american-oystercatcher"],
    "owls": ["american-barn-owl", "eastern-screech-owl"],
}
