#!/usr/bin/env python3
"""Assemble the final 30 icons from final.json into final/: SVGO, checks, six regional sheets, confusable strips.

Run: uv run --with pillow --with fonttools --with brotli python design-system/birds/assemble.py
Needs: rsvg-convert, bun (SVGO 4.0.0 runs through bunx, nothing installed globally).
Checks (assert): exactly the 30 species of the brief; palette-only fills; SVGO output renders like its source
(at most 0.2% of pixels differ at 480 px). Reported, not failed: icons outside the brief's 3-4 colors.
"""
import io
import json
import pathlib
import re
import shutil
import subprocess

from PIL import Image, ImageChops

import build
import species as S

HERE = pathlib.Path(__file__).parent
OUT = HERE / "final"
PALETTE = {c.lower() for c in (S.N, S.F, S.Y, S.R, S.B, S.M)}


def png(svg_path, w=480):
    data = subprocess.run(["rsvg-convert", "-w", str(w), str(svg_path)], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(data)).convert("RGB")


def changed_share(a, b):
    """Share of pixels whose largest channel difference is over 25 (of 255)."""
    diff = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > 25 else 0)
    return sum(diff.histogram()[255:]) / (a.width * a.height)


def body(slug):
    """An icon's SVG body for embedding, with ids made unique per icon (several share one sheet)."""
    text = re.sub(r"</?svg[^>]*>", "", (OUT / f"{slug}.svg").read_text())
    text = re.sub(r'id="([^"]+)"', lambda m: f'id="{slug}-{m.group(1)}"', text)
    return re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{slug}-{m.group(1)})", text)


def main():
    manifest = {k: v for k, v in json.loads((HERE / "final.json").read_text()).items() if not k.startswith("_")}
    names = {s: b["name"] for s, b in build.BIRDS.items()}
    assert set(manifest) == set(names), f"manifest vs brief: {set(manifest) ^ set(names)}"
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for slug, entry in manifest.items():
        shutil.copy(HERE / entry["src"], OUT / f"{slug}.svg")
    before = {slug: png(OUT / f"{slug}.svg") for slug in manifest}
    svgo = lambda target, p: subprocess.run(["bunx", "--bun", "svgo@4.0.0", "--quiet", "--multipass", "-p", str(p), target, "-o", target],
                                            check=True, capture_output=True)
    svgo_dir = lambda p: subprocess.run(["bunx", "--bun", "svgo@4.0.0", "--quiet", "--multipass", "-p", str(p), "-f", str(OUT), "-o", str(OUT)],
                                        check=True, capture_output=True)
    svgo_dir(1)  # 0.1-unit precision halves the files; an icon that then renders differently is redone at 0.01
    notes = []
    for slug in manifest:
        share = changed_share(before[slug], png(OUT / f"{slug}.svg"))
        if share > 0.002:
            shutil.copy(HERE / manifest[slug]["src"], OUT / f"{slug}.svg")
            svgo(str(OUT / f"{slug}.svg"), 2)
            share = changed_share(before[slug], png(OUT / f"{slug}.svg"))
            notes.append(f"{slug}: SVGO precision 2 (precision 1 moved edges)")
        assert share <= 0.002, f"{slug}: SVGO changed {share:.2%} of pixels"
        svg = (OUT / f"{slug}.svg").read_text()
        fills = {f.lower() for f in re.findall(r'fill="(#[0-9a-fA-F]{3,6})"', svg)}
        fills = {"#" + "".join(c * 2 for c in f[1:]) if len(f) == 4 else f for f in fills}  # SVGO may shorten #rrggbb
        assert fills <= PALETTE, f"{slug}: off-palette {fills - PALETTE}"
        if not 3 <= len(fills) <= 4:
            notes.append(f"{slug}: {len(fills)} colors (brief: 3-4)")
    (OUT / "sheets").mkdir()
    for i, region in enumerate(S.REGIONS, 1):
        svg = build.sheet(i, region, art=body)
        (OUT / "sheets" / f"{i}-{region['key']}.svg").write_text(svg)
        (OUT / "sheets" / f"{i}-{region['key']}.png").write_bytes(build.rsvg(svg, build.W))
    (OUT / "strips").mkdir()
    for name, slugs in build.CONFUSABLE.items():
        svg = build.strip(slugs, art=body)
        (OUT / "strips" / f"{name}.png").write_bytes(build.rsvg(svg, int(re.search(r'width="(\d+)"', svg).group(1)) * 2))
    size = sum(f.stat().st_size for f in OUT.glob("*.svg"))
    print(f"final/: {len(manifest)} icons, {size // 1024} KB of SVG, 6 sheets, {len(build.CONFUSABLE)} strips")
    for n in notes:
        print("  NOTE", n)


if __name__ == "__main__":
    main()
