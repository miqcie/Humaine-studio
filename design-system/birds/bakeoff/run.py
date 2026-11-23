#!/usr/bin/env python3
"""Generator bake-off for the bird icons. Run through run.sh (it loads the Recraft key).

  run.sh check                      free: confirm each generator's key works
  run.sh gen [bird ...] [--only C]  generate (cached; stops at the budget cap)
  run.sh trace                      normalize every raw output with trace_icon.py
  run.sh sheets                     blind judging sheets + key.json

Contestants: R-vec (Recraft V4 Styles, SVG), R-ras (Recraft V4 Styles, raster), O-ras (OpenAI image generation via Codex CLI).
All three get the same style references, palette and prompt; all outputs go through the same tracer.
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
import urllib.error
import urllib.request
import uuid

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
LEDGER, STYLE = ROOT / "ledger.json", HERE / "style.json"
STYLE_DIR = HERE / "raw" / "_style"  # the shared style references, for every round
BUDGET = 5.00
SEEDS = CONFIG.get("seeds", [11, 23])
PILOTS = CONFIG.get("birds", ["black-skimmer", "american-kestrel", "brown-pelican", "northern-bobwhite", "eastern-screech-owl", "great-blue-heron"])
COST = {"R-vec": 0.05, "R-ras": 0.035, "O-ras": 0.0, "style": 0.005}  # O-ras runs on the ChatGPT plan via Codex
RECRAFT = "https://external.api.recraft.ai/v1"
PALETTE = [S.N, S.F, S.Y, S.R, S.B, S.M]

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


# ---------- ledger: every paid call is recorded; nothing runs past the cap ----------

def ledger():
    return json.loads(LEDGER.read_text()) if LEDGER.exists() else []


def spend(item, cost):
    """Check the cap before a paid call; record() after it succeeds, so a refused call costs nothing here."""
    total = sum(x["cost"] for x in ledger())
    if total + cost > BUDGET:
        raise SystemExit(f"budget cap: ${total:.3f} spent, next call ${cost} would pass ${BUDGET}")


def record(item, cost):
    rows = ledger() + [{"item": item, "cost": cost}]
    LEDGER.write_text(json.dumps(rows, indent=1) + "\n")


# ---------- HTTP ----------

def call(url, *, token, body=None, multipart=None, method=None):
    headers = {"Authorization": f"Bearer {token}"}
    data = None
    if body is not None:
        data, headers["Content-Type"] = json.dumps(body).encode(), "application/json"
    if multipart is not None:
        bnd = uuid.uuid4().hex
        parts = []
        for name, val in multipart:
            if isinstance(val, tuple):  # (filename, bytes)
                parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="{name}"; filename="{val[0]}"\r\n'
                             f"Content-Type: image/png\r\n\r\n".encode() + val[1] + b"\r\n")
            else:
                parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{val}\r\n'.encode())
        data = b"".join(parts) + f"--{bnd}--\r\n".encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={bnd}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method or ("POST" if data else "GET"))
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{url}: HTTP {e.code} {e.read()[:400].decode(errors='replace')}")


def download(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "humaine-bird-bakeoff"}), timeout=120) as r:
        return r.read()


# ---------- style references: the curlew plus three strong OpenAI concept icons ----------

def style_refs():
    """PNG bytes of the references, cached in bakeoff/raw/_style/."""
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
    out.append(logo.read_bytes())
    for name, (sheet, box) in crops.items():
        f = d / f"{name}.png"
        if not f.exists():
            Image.open(src / sheet).convert("RGB").crop(box).resize((512, 512)).save(f)
        out.append(f.read_bytes())
    return out


def data_url(b):
    return "data:image/png;base64," + base64.b64encode(b).decode()


def recraft_style(token, model):
    """One Recraft style per model (a raster style cannot drive the vector model)."""
    styles = json.loads(STYLE.read_text()) if STYLE.exists() else {}
    styles = styles if "style_id" not in styles else {"recraftv4_styles": styles}  # first run stored a single style
    if model not in styles:
        spend("recraft style", COST["style"])
        r = call(f"{RECRAFT}/styles", token=token, multipart=[("model", model)] + [("files", (f"ref{i}.png", b)) for i, b in enumerate(style_refs())])
        record(f"recraft style {model}", COST["style"])
        styles[model] = {"style_id": r["id"], "credits": r.get("credits")}
        STYLE.write_text(json.dumps(styles, indent=1) + "\n")
    return styles[model]["style_id"]


# ---------- contestants ----------

def gen_recraft(slug, seed, vector):
    token = os.environ["RECRAFT_API_TOKEN"]
    key = "R-vec" if vector else "R-ras"
    model = "recraftv4_styles_vector" if vector else "recraftv4_styles"
    body = {"prompt": prompt(slug), "model": model, "style_id": recraft_style(token, model), "size": "1:1", "random_seed": seed,
            "controls": {"colors": [{"rgb": list(trace_icon.rgb(c))} for c in PALETTE], "background_color": {"rgb": list(trace_icon.rgb(S.F))}}}
    spend(f"{key} {slug} {seed}", COST[key])
    r = call(f"{RECRAFT}/images/generations", token=token, body=body)
    record(f"{key} {slug} {seed}", COST[key])
    return download(r["data"][0]["url"]), ("svg" if vector else "png"), body, r.get("credits")


def gen_openai(slug, seed):
    """OpenAI image generation through the local Codex CLI (ChatGPT plan; no API key, no dollar cost here)."""
    import tempfile
    style = [str(STYLE_DIR / f"{n}.png") for n in ("curlew", "wood-duck", "great-blue-heron", "hooded-warbler")]
    style_refs()
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
        r = subprocess.run(cmd, cwd=td, input=ask, capture_output=True, text=True, timeout=900)
        out = pathlib.Path(td) / "out.png"
        if r.returncode or not out.exists():
            raise SystemExit(f"codex {slug} {seed}: exit {r.returncode}, no image. {r.stderr[-300:]}")
        img = out.read_bytes()
    record(f"O-ras {slug} {seed}", 0.0)
    return img, "png", {"via": "codex exec (ChatGPT plan)", "prompt": ask}, "ChatGPT plan"


CONTESTANTS = {"R-vec": lambda s, n: gen_recraft(s, n, True), "R-ras": lambda s, n: gen_recraft(s, n, False), "O-ras": gen_openai}


def gen(birds, only):
    for slug in birds:
        d = RAW / slug
        d.mkdir(parents=True, exist_ok=True)
        for key in only:
            for seed in SEEDS:
                if any(d.glob(f"{key}-{seed}.*")):
                    continue
                img, ext, req, billed = CONTESTANTS[key](slug, seed)
                (d / f"{key}-{seed}.{ext}").write_bytes(img)
                (d / f"{key}-{seed}.json").write_text(json.dumps({"request": req, "billed": billed}, indent=1) + "\n")
                print(f"{slug} {key} {seed}: {len(img)} bytes, billed {billed}")
    print(f"spent ${sum(x['cost'] for x in ledger()):.3f} of ${BUDGET}")


def check():
    t = os.environ.get("RECRAFT_API_TOKEN")
    me = call(f"{RECRAFT}/users/me", token=t) if t else None
    print("recraft:", {k: v for k, v in (me or {}).items() if isinstance(v, (int, float)) or k in ("api_units", "credits")} if me else "no token")
    o = os.environ.get("OPENAI_API_KEY")
    try:
        call("https://api.openai.com/v1/models", token=o or "none")
        print("openai: ok")
    except SystemExit as e:
        print("openai: not usable,", str(e)[:120])


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
    key = {}
    for slug in PILOTS:
        tiles = sorted(TRACED.glob(f"{slug}/*.svg"))
        if not tiles:
            continue
        rng.shuffle(tiles)
        letters = "ABCDEFGH"[:len(tiles)]
        key[slug] = {L: t.stem for L, t in zip(letters, tiles)}
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
    (ROOT / "key.json").write_text(json.dumps(key, indent=1) + "\n")


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["check"]
    only = list(CONTESTANTS)
    if "--only" in rest:
        i = rest.index("--only")
        only, rest = rest[i + 1].split(","), rest[:i] + rest[i + 2:]
    {"check": check, "gen": lambda: gen(rest or PILOTS, only), "trace": trace, "sheets": sheets}[cmd]()
