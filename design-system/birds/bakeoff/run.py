#!/usr/bin/env python3
"""Generator bake-off for the bird icons. Run through run.sh (it loads the Recraft key).

  run.sh check                      free: confirm each generator's key works
  run.sh gen [bird ...] [--only C]  generate (cached; stops at the budget cap)
  run.sh trace                      normalize every raw output with trace_icon.py
  run.sh sheets                     blind judging sheets + key.json

Contestants: R-vec (Recraft V4 Styles, SVG), R-ras (Recraft V4 Styles, raster), O-ras (OpenAI gpt-image, raster).
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

RAW, TRACED, SHEETS = HERE / "raw", HERE / "traced", HERE / "sheets"
LEDGER, STYLE = HERE / "ledger.json", HERE / "style.json"
BUDGET = 5.00
SEEDS = [11, 23]
PILOTS = ["black-skimmer", "american-kestrel", "brown-pelican", "northern-bobwhite", "eastern-screech-owl", "great-blue-heron"]
COST = {"R-vec": 0.05, "R-ras": 0.035, "O-ras": 0.07, "style": 0.005}  # O-ras: medium quality 1024 plus image inputs, estimate
RECRAFT = "https://external.api.recraft.ai/v1"
PALETTE = [S.N, S.F, S.Y, S.R, S.B, S.M]

STYLE_BLOCK = (
    "Flat geometric bird icon in a Mondrian / De Stijl spirit, matching the reference images. "
    "A thick navy square frame (#0B0F24) around an ivory field (#FAF6EE). Right-facing head-and-upper-breast portrait. "
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
            f"Do not draw: {'; '.join(r['avoid'])}.")


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
    """PNG bytes of the references, cached in raw/_style/."""
    d = RAW / "_style"
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


def recraft_style(token):
    if STYLE.exists():
        return json.loads(STYLE.read_text())["style_id"]
    spend("recraft style", COST["style"])
    r = call(f"{RECRAFT}/styles", token=token, multipart=[("model", "recraftv4_styles")] + [("files", (f"ref{i}.png", b)) for i, b in enumerate(style_refs())])
    record("recraft style", COST["style"])
    STYLE.write_text(json.dumps({"style_id": r["id"], "credits": r.get("credits")}, indent=1) + "\n")
    return r["id"]


# ---------- contestants ----------

def gen_recraft(slug, seed, vector):
    token = os.environ["RECRAFT_API_TOKEN"]
    key = "R-vec" if vector else "R-ras"
    body = {"prompt": prompt(slug), "model": "recraftv4_styles_vector" if vector else "recraftv4_styles",
            "style_id": recraft_style(token), "size": "1:1", "random_seed": seed,
            "controls": {"colors": [{"rgb": list(trace_icon.rgb(c))} for c in PALETTE], "background_color": {"rgb": list(trace_icon.rgb(S.F))}}}
    spend(f"{key} {slug} {seed}", COST[key])
    r = call(f"{RECRAFT}/images/generations", token=token, body=body)
    record(f"{key} {slug} {seed}", COST[key])
    return download(r["data"][0]["url"]), ("svg" if vector else "png"), body, r.get("credits")


def gen_openai(slug, seed):
    token = os.environ.get("OPENAI_API_KEY", "")
    fields = [("model", "gpt-image-1"), ("prompt", prompt(slug) + f"\n(variation {seed})"), ("size", "1024x1024"), ("quality", "medium")]
    fields += [("image[]", (f"ref{i}.png", b)) for i, b in enumerate(style_refs())]
    spend(f"O-ras {slug} {seed}", COST["O-ras"])
    r = call("https://api.openai.com/v1/images/edits", token=token, multipart=fields)
    record(f"O-ras {slug} {seed}", COST["O-ras"])
    return base64.b64decode(r["data"][0]["b64_json"]), "png", {k: v for k, v in fields if not isinstance(v, tuple)}, r.get("usage")


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
        if f.parent.name.startswith("_") or f.suffix not in (".png", ".svg"):
            continue
        src = f
        if f.suffix == ".svg":  # rasterize the vector first; the raw SVG is kept as-is for comparison
            src = f.with_suffix(".render.png")
            src.write_bytes(subprocess.run(["rsvg-convert", "-w", "1024", str(f)], capture_output=True, check=True).stdout)
        out = TRACED / f.parent.name / f"{f.stem}.svg"
        out.parent.mkdir(parents=True, exist_ok=True)
        stats[f"{f.parent.name}/{f.stem}"] = trace_icon.convert(str(src), str(out))
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
    (HERE / "key.json").write_text(json.dumps(key, indent=1) + "\n")


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["check"]
    only = list(CONTESTANTS)
    if "--only" in rest:
        i = rest.index("--only")
        only, rest = rest[i + 1].split(","), rest[:i] + rest[i + 2:]
    {"check": check, "gen": lambda: gen(rest or PILOTS, only), "trace": trace, "sheets": sheets}[cmd]()
