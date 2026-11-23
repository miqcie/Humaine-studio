#!/usr/bin/env python3
"""Trace a folder of raster bird icons (<slug>.png) into house-palette SVGs, plus a contact sheet.

Run: uv run --with pillow --with numpy --with scipy python design-system/birds/trace_folder.py SRC_DIR OUT_DIR
"""
import json
import pathlib
import subprocess
import sys

from PIL import Image

import trace_icon


def main(src, out):
    src, out = pathlib.Path(src), pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    stats, pngs = {}, []
    for f in sorted(src.glob("*.png")):
        svg = out / f"{f.stem}.svg"
        stats[f.stem] = trace_icon.convert(str(f), str(svg))
        png = out / f"{f.stem}.png"
        png.write_bytes(subprocess.run(["rsvg-convert", "-w", "480", str(svg)], capture_output=True, check=True).stdout)
        pngs.append(png)
    (out / "stats.json").write_text(json.dumps(stats, indent=1) + "\n")
    # Contact sheet: 6 across, 240 px each, for a quick look.
    cols, cell = 6, 240
    sheet = Image.new("RGB", (cols * cell, -(-len(pngs) // cols) * cell), "#F3ECE0")
    for i, p in enumerate(pngs):
        sheet.paste(Image.open(p).convert("RGB").resize((cell - 12, cell - 12)), ((i % cols) * cell + 6, (i // cols) * cell + 6))
    sheet.save(out / "_contact.png")
    print(f"traced {len(pngs)} -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:])
