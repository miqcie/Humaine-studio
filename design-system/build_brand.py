#!/usr/bin/env python3
"""Build the Humaine Studio brand files from the three OFL variable fonts and the block-mark geometry.

Run:  uv run --with fonttools --with brotli --with uharfbuzz --with pillow --with resvg-py python design-system/build_brand.py
Writes:
  design-system/project/assets/Logos/humaine-wordmark-ink.svg    ink wordmark, for linen and paper grounds
  design-system/project/assets/Logos/humaine-wordmark-linen.svg  linen wordmark, for Klein and night grounds
  favicon.ico, assets/images/favicon.svg, favicon-32x32.png, apple-touch-icon.png
  assets/fonts/*.woff2  self-hosted fonts with the brand axes baked in (SOFT 100 / MONO 1, CASL 0.5)
Fonts are downloaded once into ~/.cache/humaine-brand (not committed).
"""
import io
import json
import pathlib
import urllib.request

import uharfbuzz as hb
from fontTools import subset
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
import resvg_py
from PIL import Image

HERE = pathlib.Path(__file__).parent
REPO = HERE.parent
LOGOS = HERE / "project" / "assets" / "Logos"
# Pinned google/fonts commit: the sources cannot change under us. Bump deliberately to update the fonts.
FONTS_SHA = "5bd87dfc525c8a0d1d8529d3684716e00c3fc59a"
CACHE = pathlib.Path.home() / ".cache" / "humaine-brand" / FONTS_SHA[:12]
RAW = f"https://raw.githubusercontent.com/google/fonts/{FONTS_SHA}/ofl/"
SOURCES = {
    "fraunces": RAW + "fraunces/Fraunces%5BSOFT,WONK,opsz,wght%5D.ttf",
    "schibsted": RAW + "schibstedgrotesk/SchibstedGrotesk%5Bwght%5D.ttf",
    "schibsted-italic": RAW + "schibstedgrotesk/SchibstedGrotesk-Italic%5Bwght%5D.ttf",
    "recursive": RAW + "recursive/Recursive%5BCASL,CRSV,MONO,slnt,wght%5D.ttf",
}

tokens = {t["name"]: t["value"] for t in json.loads((HERE / "project" / "tokens.json").read_text())["color"]["tokens"]}
INK, PAPER = tokens["mark-line"], tokens["mark-field"]

# Latin, punctuation and the few symbols the system uses (− → · ⌘ etc.).
# None of the three fonts draws box-drawing lines, ↩, ▶, ⚠ or emoji; those fall back to the system font.
UNICODES = "U+0000-00FF,U+0131,U+0152-0153,U+02C6,U+02DA,U+02DC,U+2013-2014,U+2018-201E,U+2022,U+2026,U+2030,U+2039-203A,U+20AC,U+2122,U+2190-2193,U+2212,U+2318,U+00B7"


def fetch(url, filename):
    """Download once into the cache; write to a temp file and rename, so an interrupted download is never reused."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / filename
    if not path.exists():
        with urllib.request.urlopen(url, timeout=60) as r:
            tmp = path.with_suffix(".part")
            tmp.write_bytes(r.read())
            tmp.rename(path)
    return path


def font(name):
    return TTFont(fetch(SOURCES[name], f"{name}.ttf"))


def instance(name, axes):
    tt = instantiateVariableFont(font(name), axes, inplace=False, updateFontNames=False)
    tt.recalcTimestamp = False  # keep the source's head.modified so rebuilds are byte-identical
    return tt


def to_bytes(tt):
    buf = io.BytesIO()
    tt.save(buf)
    return buf.getvalue()


# ---------- wordmark: Fraunces 800, SOFT 100, WONK 0, letter-spacing -0.02em, outlined ----------
def wordmark():
    tt = instance("fraunces", {"wght": 800, "SOFT": 100, "WONK": 0, "opsz": 72})
    upem = tt["head"].unitsPerEm
    hbfont = hb.Font(hb.Face(to_bytes(tt)))
    buf = hb.Buffer()
    buf.add_str("Humaine Studio")
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    glyphs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    track = -0.02 * upem
    pen, bounds = SVGPathPen(glyphs), BoundsPen(glyphs)
    x = 0
    infos, positions = buf.glyph_infos, buf.glyph_positions
    for i, (info, pos) in enumerate(zip(infos, positions)):
        g = glyphs[order[info.codepoint]]
        m = (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)  # flip y for SVG
        g.draw(TransformPen(pen, m))
        g.draw(TransformPen(bounds, m))
        x += pos.x_advance + (track if i < len(infos) - 1 else 0)
    x0, y0, x1, y1 = bounds.bounds
    pad = round(0.04 * upem)
    vb = f"{round(x0) - pad} {round(y0) - pad} {round(x1 - x0) + 2 * pad} {round(y1 - y0) + 2 * pad}"
    d = pen.getCommands()
    assert len(d) > 1000, "wordmark path looks empty"
    for name, fill in (("ink", INK), ("linen", PAPER)):
        (LOGOS / f"humaine-wordmark-{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-labelledby="t">'
            f'<title id="t">Humaine Studio</title><path fill="{fill}" d="{d}"/></svg>\n')
    print("wordmark", vb, len(d), "chars")


# ---------- favicons: the curlew (the logo since 2026-11-18) ----------
def curlew_png(size):
    """Render the curlew large, square it off with its own ink frame color, then downsample."""
    big = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_path=str(LOGOS / "humaine-curlew.svg"), width=1024)))).convert("RGB")
    side = max(big.size)
    sq = Image.new("RGB", (side, side), INK)  # the frame is 422x417; pad in frame ink so it reads as one square
    sq.paste(big, ((side - big.width) // 2, (side - big.height) // 2))
    return sq.resize((size, size), Image.LANCZOS)


def favicons():
    img = REPO / "assets" / "images"
    curlew_png(32).save(img / "favicon-32x32.png")
    curlew_png(180).save(img / "apple-touch-icon.png")
    ico = [curlew_png(n) for n in (16, 32, 48)]
    ico[-1].save(REPO / "favicon.ico", append_images=ico[:-1], sizes=[(16, 16), (32, 32), (48, 48)])
    (img / "favicon.svg").write_text((LOGOS / "humaine-curlew.svg").read_text())
    (img / "humaine-curlew.svg").write_text((LOGOS / "humaine-curlew.svg").read_text())  # header lockup and home hero
    print("favicons written")


# ---------- self-hosted fonts: axes baked in, Latin subset, WOFF2 ----------
WEBFONTS = {
    # file: (source, axes to pin or limit)
    "fraunces-soft.woff2": ("fraunces", {"SOFT": 100, "WONK": 0, "wght": (300, 900), "opsz": (9, 144)}),
    "schibsted-grotesk.woff2": ("schibsted", {"wght": (400, 700)}),
    "schibsted-grotesk-italic.woff2": ("schibsted-italic", {"wght": (400, 700)}),
    "recursive-mono.woff2": ("recursive", {"MONO": 1, "CASL": 0.5, "CRSV": 0, "slnt": 0, "wght": (400, 500)}),
}


LICENSES = {"fraunces": "fraunces", "schibsted-grotesk": "schibstedgrotesk", "recursive": "recursive"}


def webfonts():
    out = REPO / "assets" / "fonts"
    out.mkdir(exist_ok=True)
    # OFL 1.1: each redistributed copy carries its license and copyright notice.
    for name, folder in LICENSES.items():
        text = fetch(f"{RAW}{folder}/OFL.txt", f"{name}-OFL.txt").read_text()
        assert "SIL OPEN FONT LICENSE" in text.upper()
        header = text.split("PREAMBLE")[0]  # an RFN is declared here; the phrase also appears in the license body
        assert "Reserved Font Name" not in header, f"{name} has a Reserved Font Name; a subset must be renamed"
        (out / f"{name}-OFL.txt").write_text(text)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.unicodes = subset.parse_unicodes(UNICODES)
    for fname, (src, axes) in WEBFONTS.items():
        tt = TTFont(io.BytesIO(to_bytes(instance(src, axes))), recalcTimestamp=False)  # reload: subsetting a lazily loaded instance fails
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=opts.unicodes)
        sub.subset(tt)
        tt.flavor = "woff2"
        tt.save(out / fname)
        print(fname, (out / fname).stat().st_size // 1024, "KB")


# ---------- site CSS, generated from the design system (do not hand-edit the outputs) ----------
FONT_FACES = """@font-face { font-family: "Fraunces"; src: url("../fonts/fraunces-soft.woff2") format("woff2"); font-weight: 300 900; font-style: normal; font-display: swap; }
@font-face { font-family: "Schibsted Grotesk"; src: url("../fonts/schibsted-grotesk.woff2") format("woff2"); font-weight: 400 700; font-style: normal; font-display: swap; }
@font-face { font-family: "Schibsted Grotesk"; src: url("../fonts/schibsted-grotesk-italic.woff2") format("woff2"); font-weight: 400 700; font-style: italic; font-display: swap; }
@font-face { font-family: "Recursive"; src: url("../fonts/recursive-mono.woff2") format("woff2"); font-weight: 400 500; font-style: normal; font-display: swap; }
"""


def site_css():
    t = json.loads((HERE / "project" / "tokens.json").read_text())
    themes = [th["id"] for th in t["color"]["themes"]]  # [light, dark]

    def val(v, theme):
        v = v if isinstance(v, str) else v.get(theme, v[themes[0]])
        return f"var(--{v[1:-1]})" if v.startswith("{") else v

    light = [f"  --{c['name']}: {val(c['value'], themes[0])};" for c in t["color"]["tokens"]]
    dark = [f"  --{c['name']}: {val(c['value'], themes[1])};" for c in t["color"]["tokens"]
            if not isinstance(c["value"], str) or c["value"].startswith("{")]
    other = [f"  --{x['name']}: {x['value']};" for fam in ("spacing", "radius", "layout") for x in t[fam]["tokens"]]
    fams = [f"  --font-{k}: {v};" for k, v in t["type"]["families"].items()]
    classes = []
    for g in t["type"]["groups"]:
        for s in g["styles"]:
            ls = f" letter-spacing: {s['letterSpacing']};" if "letterSpacing" in s else ""
            classes.append(f".{s['name']} {{ font: {s['fontWeight']} {s['fontSize']}/{s['lineHeight']} var(--font-{s.get('family', g['family'])});{ls} }}")
    css = ("/* GENERATED by design-system/build_brand.py from design-system/project/tokens.json. Do not edit. */\n"
           + FONT_FACES
           + ":root {\n" + "\n".join(light + other + fams) + "\n  color-scheme: light;\n}\n"
           + '[data-theme="dark"] {\n' + "\n".join(dark) + "\n  color-scheme: dark;\n}\n"
           + "\n".join(classes) + "\n")
    out = REPO / "assets" / "css"
    (out / "humaine-tokens.css").write_text(css)
    bundle = (HERE / "project" / "components" / "bundle.css").read_text().split("\n", 1)[1]  # drop the Google Fonts @import
    (out / "humaine-components.css").write_text("/* GENERATED by design-system/build_brand.py from design-system/project/components/bundle.css. Do not edit. */\n" + bundle)
    assert "--klein:" in css and "--font-serif:" in css
    print("site css written")


wordmark()
favicons()
webfonts()
site_css()
