#!/usr/bin/env python3
"""Check every text and control color pair in project/tokens.json, in every theme.

Run: python3 design-system/check_contrast.py   (exit 1 if any pair fails)
Edit PAIRS when a token's usage note names a new ground.
"""
import json
import pathlib
import sys

TOKENS = pathlib.Path(__file__).parent / "project" / "tokens.json"

# (foreground, background, minimum ratio). 4.5 = text, 3.0 = focus rings and control borders.
PAIRS = [
    *[(fg, bg, 4.5) for fg in ("ink", "ink-soft") for bg in ("ground", "surface", "sunken")],
    *[("mute", bg, 4.5) for bg in ("ground", "surface")],
    *[(fg, bg, 4.5) for fg in ("klein", "klein-press", "vermilion") for bg in ("ground", "surface")],
    ("on-klein", "klein", 4.5), ("on-klein", "klein-press", 4.5),
    ("on-ink", "ink", 4.5), ("on-chrome", "chrome", 4.5),
    ("surface", "vermilion", 4.5),
    ("ink", "klein-wash", 4.5), ("klein", "klein-wash", 4.5), ("ink-soft", "klein-wash", 4.5),
    ("klein", "sunken", 4.5), ("mute", "sunken", 4.5),  # code keywords and comments
    ("on-ink", "ink-soft", 4.5),  # ink button hover
    *[("focus", bg, 3.0) for bg in ("ground", "surface", "sunken")],
]


def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main():
    data = json.loads(TOKENS.read_text())
    themes = [t["id"] for t in data["color"]["themes"]]
    table = {t["name"]: t["value"] for t in data["color"]["tokens"]}

    def resolve(name, theme, depth=0):
        v = table[name]
        if isinstance(v, dict):
            v = v.get(theme, v[themes[0]])  # a missing theme inherits the first theme's value
        if v.startswith("{"):
            assert depth < 16, f"alias chain too deep at {name}"
            return resolve(v.strip("{}"), theme, depth + 1)
        return v

    failed = 0
    for theme in themes:
        for fg, bg, need in PAIRS:
            r = ratio(resolve(fg, theme), resolve(bg, theme))
            ok = r >= need
            failed += not ok
            print(f"{'ok  ' if ok else 'FAIL'} {theme:12} {fg:12} on {bg:12} {r:5.2f} (need {need})")
    print(f"\n{failed} failing pair(s)")
    return 1 if failed else 0


assert abs(ratio("#000000", "#ffffff") - 21) < 0.01
sys.exit(main())
