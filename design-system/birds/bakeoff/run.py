#!/usr/bin/env python3
"""Draft, trace and blind-sheet one vote round of bird icons. Run through run.sh.

  run.sh [--dir round2] gen [bird ...]   draft with OpenAI image generation via the Codex CLI (cached)
  run.sh [--dir round2] trace            normalize every raw draft with trace_icon.py
  run.sh [--dir round2] sheets           blind judging sheets + key.json

The first round (bakeoff/) also ran two Recraft V4 Styles contestants; OpenAI won (bakeoff/RESULTS.md) and the
Recraft code was removed afterwards. It is in git history up to commit 2a6cae9.
"""
import base64
import io
import json
import os
import pathlib
import random
import re
import subprocess
import sys

from PIL import Image

HERE = pathlib.Path(__file__).parent
BIRDS_DIR = HERE.parent
sys.path.insert(0, str(BIRDS_DIR))
import species as S  # noqa: E402
import trace_icon  # noqa: E402

def _take(flag, default):
    """Pop `flag value` from argv (so the subcommand parsing below never sees it)."""
    if flag in sys.argv:
        i = sys.argv.index(flag)
        value = sys.argv[i + 1]
        del sys.argv[i:i + 2]
        return value
    return default


# A round lives in its own folder (bakeoff/ by default, or e.g. --dir round2) with an optional config.json:
# {"birds": [...], "seeds": [...], "incumbents": {slug: svg path}}.
ROOT = BIRDS_DIR / _take("--dir", "bakeoff")
CONFIG = json.loads((ROOT / "config.json").read_text()) if (ROOT / "config.json").exists() else {}
RAW, TRACED, SHEETS = ROOT / "raw", ROOT / "traced", ROOT / "sheets"
STYLE_DIR = HERE / "raw" / "_style"  # the shared style references, for every round
SEEDS = CONFIG.get("seeds", [11, 23])
PILOTS = CONFIG.get("birds", ["black-skimmer", "american-kestrel", "brown-pelican", "northern-bobwhite", "eastern-screech-owl", "great-blue-heron"])

STYLE_BLOCK = (
    "Flat geometric bird icon in a Mondrian / De Stijl spirit, matching the reference images. "
    "A thick navy square frame (#0B0F24) around an ivory field (#FAF6EE). Right-facing head-and-upper-breast portrait "
    "(owls may face straight ahead). "
    "The bird is a bold navy silhouette with a few flat color fields; it may run off the bottom and left edges of the frame "
    "only, and leaves clear ivory space between the bill tip, crest and the frame. One simple round eye. "
    "Use only these colors: navy #0B0F24, ivory #FAF6EE, chrome yellow #F7B902, vermilion #C7301C, Klein blue #002FA7, "
    "slate #5E6178. Three or four colors in total. No gradients, shading, texture, outlines of feather detail, scenery, "
    "text or labels. Simple shapes that stay readable at 32 pixels."
)


def prompt(slug):
    r = json.loads((BIRDS_DIR / "references.json").read_text())[slug]
    ratios = "; ".join(f"{k.replace('_', ' ')} = {v}" for k, v in r["ratios"].items())
    return (f"{STYLE_BLOCK}\n\nSpecies: {r['name']} ({r['scientific']}). "
            f"Identifying features to show: {'; '.join(r['marks'])}. "
            f"Proportions measured from a photo: {ratios}. "
            f"Do not draw: {'; '.join(r['avoid'])}."
            + (f"\nArt director's change for this version: {r['notes']}" if r.get("notes") else ""))


def base_pngs(slug):
    """Earlier versions of this bird that the round's notes refer to (references.json `bases`), as PNGs."""
    r = json.loads((BIRDS_DIR / "references.json").read_text())[slug]
    out = []
    for i, rel in enumerate(r.get("bases", [])):
        png = RAW / "_bases" / f"{slug}-{i}.png"
        if not png.exists():
            png.parent.mkdir(parents=True, exist_ok=True)
            src = BIRDS_DIR / rel
            if src.suffix == ".svg":
                png.write_bytes(subprocess.run(["rsvg-convert", "-w", "512", str(src)], capture_output=True, check=True).stdout)
            else:  # a photo (e.g. one Chris supplied): pass it on as a 1024 px PNG
                im = Image.open(src).convert("RGB")
                im.thumbnail((1024, 1024))
                im.save(png)
        out.append(str(png))
    return out


# ---------- style references: the curlew plus three strong OpenAI concept icons ----------

def style_refs():
    """Paths of the style reference PNGs, made once in bakeoff/raw/_style/."""
    d = STYLE_DIR
    d.mkdir(parents=True, exist_ok=True)
    src = BIRDS_DIR / "concepts" / "OpenAI Astra Concepts"
    crops = {"wood-duck": ("06-rva.png", (387, 720, 855, 1188)), "great-blue-heron": ("06-rva.png", (108, 152, 576, 620)),
             "hooded-warbler": ("05-appalachian.png", (108, 152, 576, 620))}
    out = []
    logo = d / "curlew.png"
    if not logo.exists():
        svg = BIRDS_DIR.parent / "project" / "assets" / "Logos" / "humaine-curlew.svg"
        logo.write_bytes(subprocess.run(["rsvg-convert", "-w", "512", str(svg)], capture_output=True, check=True).stdout)
    out.append(str(logo))
    for name, (sheet, box) in crops.items():
        f = d / f"{name}.png"
        if not f.exists():
            Image.open(src / sheet).convert("RGB").crop(box).resize((512, 512)).save(f)
        out.append(str(f))
    return out


def gen_openai(slug, seed):
    """OpenAI image generation through the local Codex CLI (ChatGPT plan; no API key, no dollar cost here)."""
    import tempfile
    style = style_refs()
    bases = base_pngs(slug)
    ask = ("Use your built-in image generation tool to create ONE square 1024x1024 image. "
           f"The first {len(style)} attached images are STYLE references only (frame, flat shapes, palette); do not copy their birds. "
           + (f"The last {len(bases)} attached image(s) are references for this bird (earlier icon versions or a photo the "
              "art director chose): use them as the art director's change below says. " if bases else "")
           + "Save the generated PNG into the current working directory as out.png and reply with only its path. "
           f"This is variation {seed}; vary the composition a little. Image brief:\n{prompt(slug)}")
    style += bases
    with tempfile.TemporaryDirectory() as td:
        cmd = ["codex", "exec", "--ignore-user-config", "--skip-git-repo-check", "--sandbox", "workspace-write"]
        cmd += [a for f in style for a in ("-i", f)]  # -i takes many values, so the prompt goes in on stdin
        # Codex runs an agent with a shell: pass it no secrets (API keys, the 1Password service-account token).
        env = {k: v for k, v in os.environ.items() if not re.search(r"TOKEN|SECRET|API_KEY|PASSWORD", k)}
        r = subprocess.run(cmd, cwd=td, input=ask, capture_output=True, text=True, timeout=900, env=env)
        out = pathlib.Path(td) / "out.png"
        if r.returncode or not out.exists():
            raise SystemExit(f"codex {slug} {seed}: exit {r.returncode}, no image. {r.stderr[-300:]}")
        img = out.read_bytes()
    return img, "png", {"via": "codex exec (ChatGPT plan)", "prompt": ask}, "ChatGPT plan"


def gen(birds):
    for slug in birds:
        d = RAW / slug
        d.mkdir(parents=True, exist_ok=True)
        for key in ("O-ras",):  # file names keep the bake-off contestant key
            for seed in SEEDS:
                if any(d.glob(f"{key}-{seed}.*")):
                    side = d / f"{key}-{seed}.json"  # absent if the run stopped between image and sidecar
                    old = json.loads(side.read_text())["request"].get("prompt", "") if side.exists() else ""
                    if prompt(slug) not in old:  # notes or marks changed since this draft was made
                        print(f"STALE {slug} {key} {seed}: the prompt changed since this draft; delete it to redraw")
                    continue
                img, ext, req, billed = gen_openai(slug, seed)
                (d / f"{key}-{seed}.{ext}").write_bytes(img)
                (d / f"{key}-{seed}.json").write_text(json.dumps({"request": req, "billed": billed}, indent=1) + "\n")
                print(f"{slug} {key} {seed}: {len(img)} bytes, billed {billed}")


# ---------- normalize ----------

def trace():
    stats = {}
    for f in sorted(RAW.glob("*/*-*.*")):
        if f.parent.name.startswith("_") or f.suffix not in (".png", ".svg") or f.name.endswith(".render.png"):
            continue
        src = f
        if f.suffix == ".svg":  # rasterize the vector first; the raw SVG is kept as-is for comparison
            src = f.with_suffix(".render.png")
            src.write_bytes(subprocess.run(["rsvg-convert", "-w", "1024", str(f)], capture_output=True, check=True).stdout)
        out = TRACED / f.parent.name / f"{f.stem}.svg"
        out.parent.mkdir(parents=True, exist_ok=True)
        stats[f"{f.parent.name}/{f.stem}"] = trace_icon.convert(str(src), str(out))
    # The current version of each bird joins the lineup as one more tile, so "keep what I have" is a choice.
    for slug, rel in CONFIG.get("incumbents", {}).items():
        out = TRACED / slug / "incumbent.svg"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text((BIRDS_DIR / rel).read_text())
    TRACED.mkdir(parents=True, exist_ok=True)
    (TRACED / "stats.json").write_text(json.dumps(stats, indent=1) + "\n")


# ---------- blind sheets ----------

def sheets():
    import build
    SHEETS.mkdir(parents=True, exist_ok=True)
    refs = json.loads((BIRDS_DIR / "references.json").read_text())
    rng = random.Random(20261119)
    key, lineups = {}, {}
    for slug in PILOTS:
        tiles = sorted(TRACED.glob(f"{slug}/*.svg"))
        if not tiles:
            continue
        rng.shuffle(tiles)
        assert len(tiles) <= 8, f"{slug}: {len(tiles)} tiles, the page has letters for 8"
        lineups[slug] = tiles
        key[slug] = {L: t.stem for L, t in zip("ABCDEFGH", tiles)}
    old = ROOT / "key.json"
    if old.exists() and json.loads(old.read_text()) != key:  # checked before any sheet is rewritten
        # Votes taken under the old letters would be read against the wrong tiles.
        raise SystemExit(f"{old} would change (the tile set changed). If no votes were taken yet, delete it and rerun.")
    for slug, tiles in lineups.items():
        letters = "ABCDEFGH"[:len(tiles)]
        W, cell, gap, small = 1800, 400, 40, 64
        cols = 3
        rows = -(-len(tiles) // cols)
        top = 520
        h = top + rows * (cell + 90) + 200
        r = refs[slug]
        photo = BIRDS_DIR / "refs" / slug / f"{r['photo_id']}.jpg"
        im = Image.open(photo)
        im.thumbnail((420, 300))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=85)
        parts = [f'<rect width="{W}" height="{h}" fill="{S.G}"/>',
                 build.text("BAKE-OFF · BLIND · PICK YOUR BEST TWO", 80, 80, 22, "sans", S.M, track=0.12),
                 build.text(r["name"], 80, 150, 56, "serif", S.N),
                 f'<image x="80" y="190" width="{im.width}" height="{im.height}" href="data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}"/>',
                 build.text(f"Reference: {r['credit']}", 80, 190 + im.height + 30, 18, "sans-reg", S.M)]
        y = 210
        for m in r["marks"]:
            parts.append(build.text("· " + m[:90], 560, y, 22, "sans-reg", S.N))
            y += 34
        for i, (L, t) in enumerate(zip(letters, tiles)):
            x, yy = 80 + (i % cols) * (cell + gap), top + (i // cols) * (cell + 90)
            body = re.sub(r"</?svg[^>]*>", "", t.read_text()).replace('id="f"', f'id="f{L}"').replace("url(#f)", f"url(#f{L})")
            parts.append(f'<g transform="translate({x},{yy}) scale({cell / 240})">{body}</g>')
            parts.append(build.text(L, x, yy + cell + 50, 34, "sans", S.N))
            sx = 80 + i * (small + 40)
            parts.append(f'<g transform="translate({sx},{h - 160}) scale({small / 240})">{body.replace(f"f{L}", f"s{L}")}</g>')
            parts.append(build.text(L, sx + small / 2, h - 60, 22, "sans", S.N, anchor="middle"))
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">{"".join(parts)}</svg>'
        (SHEETS / f"{slug}.svg").write_text(svg)
        (SHEETS / f"{slug}.png").write_bytes(build.rsvg(svg, W))
        print("sheet", slug, len(tiles), "tiles")
    old.write_text(json.dumps(key, indent=1) + "\n")


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["help"]
    commands = {"gen": lambda: gen(rest or PILOTS), "trace": trace, "sheets": sheets}
    if cmd not in commands:
        raise SystemExit(__doc__)
    commands[cmd]()
