#!/usr/bin/env python3
"""Likeness check for the bird icons with TypeSafe Jev (image questions; experimental "dreamer-ready").

Run through qa.sh (it loads the key):
  qa.sh run SET [--dry-run] [--only slug,slug]   ask the questions (cached; reruns are free)
  qa.sh report SET                               qa/SET.md and qa/SET.json
  qa.sh calibrate                                qa/CALIBRATION.md against known errors and Chris's votes
SET is openai30 (concepts/openai-traced) or bakeoff36 (bakeoff/traced).

Jev makes the judgments; the verdict (PASS / UNSURE / FLAG) is decided in code below.
Every icon gets the same generic questions: nothing is tailored to a known error, so calibration is honest.
"""
import hashlib
import io
import json
import pathlib
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from PIL import Image as PIL

HERE = pathlib.Path(__file__).parent
QA, CACHE = HERE / "qa", HERE / "qa" / "_cache"
MODEL = "jev-1.14.0"                                   # Box needs 1.14
HEADERS = {"TypeSafe-Danger-Zone-Images": "true"}       # images and Box are opt-in
YES, NO = 0.7, 0.3                                      # skill v0.6.2 starting thresholds for a Noul
FEATURES = {k: v for k, v in json.loads((HERE / "features.json").read_text()).items() if not k.startswith("_")}
REFS = json.loads((HERE / "references.json").read_text())
TAXA = json.loads((HERE / "taxa.json").read_text())
STYLE_REF = HERE / "bakeoff" / "raw" / "_style" / "curlew.png"
SETS = {"openai30": ("concepts/openai-traced/*.svg", "stem"), "bakeoff36": ("bakeoff/traced/*/*.svg", "parent")}

# Answer keys for calibration (facts recorded before this check existed).
KNOWN_BAD = {  # OpenAI concept errors found in review, 2026-11-19
    "brown-pelican": "invented yellow plume", "american-kestrel": "no face stripes; reads as a toucan",
    "northern-bobwhite": "quail plume topknot", "eastern-screech-owl": "reads as a Great Horned Owl",
    "osprey": "exaggerated spiky crest", "marbled-godwit": "navy body instead of buff"}
VOTES = {  # bakeoff/RESULTS.md: Chris's blind picks, best first ([] = none works)
    "american-kestrel": ["O-ras-23", "O-ras-11"], "black-skimmer": ["O-ras-11", "O-ras-23"],
    "brown-pelican": ["R-vec-23", "O-ras-23"], "eastern-screech-owl": [],
    "great-blue-heron": ["O-ras-11"], "northern-bobwhite": ["O-ras-23"]}

SPECIES = {s.replace("-", "_"): f"{TAXA[s]['name']}: {', '.join(f)}" for s, f in FEATURES.items()}
STYLE_LEVELS = [
    "A photo, a sketch, or a detailed illustration with shading or texture.",
    "A flat illustration in a different style from `style_reference`: thin outlines, other colors, or no square frame.",
    "Flat colors and a square frame like `style_reference`, but the shapes are fussier or less bold.",
    "It looks like part of the same set as `style_reference`: bold flat shapes, a thick square frame, few colors and a simple round eye.",
]


def spec(slug):
    """All questions for one icon, as plain dicts (hashable, readable in the report)."""
    name = TAXA[slug]["name"]
    q = {
        "species": {"type": "choice", "instructions": "Which bird species is drawn in the flat icon `icon`?", "criteria": SPECIES},
        "species_small": {"type": "choice", "instructions": "Which bird species is drawn in the small, pixelated icon `icon_small`?", "criteria": SPECIES},
        "colors_plausible": {"type": "noul", "instructions": f"Are the colors of the bird in `icon` a believable flat-color version of a real {name}'s plumage?"},
        "head_shape_plausible": {"type": "noul", "instructions": f"Is the shape of the head and bill of the bird in `icon` true to a real {name}?"},
        "style": {"type": "score", "instructions": "How well does `icon` match the style of the brand icon `style_reference`?", "criteria": STYLE_LEVELS},
        "bill_visible": {"type": "noul", "instructions": "Is the bill of the bird in `icon` visible?"},
        "bill": {"type": "box", "instructions": "the bill of the bird in `icon`"},
        "head": {"type": "box", "instructions": "the head of the bird in `icon`"},
    }
    for i, f in enumerate(FEATURES[slug]):
        q[f"mark_{i}"] = {"type": "noul", "instructions": f"Does the bird drawn in `icon` show this feature: {f}?", "label": f}
    r = REFS.get(slug)
    if r:
        for i, a in enumerate(r["avoid"]):
            q[f"avoid_{i}"] = {"type": "noul", "instructions": f"Does `icon` show this: {a}?", "label": a}
        q["matches_reference"] = {"type": "noul", "instructions": f"Does the bird drawn in `icon` show the same field marks as the {name} in the photo `reference`?"}
    return q


def sdk_questions(q):
    from typesafe_sdk import Box, Choice, Noul, Score
    out = {}
    for k, v in q.items():
        t = v["type"]
        out[k] = (Noul(instructions=v["instructions"]) if t == "noul" else
                  Choice(instructions=v["instructions"], criteria=v["criteria"]) if t == "choice" else
                  Score(instructions=v["instructions"], criteria=v["criteria"]) if t == "score" else
                  Box(instructions=v["instructions"]))
    return out


def items(set_name, only=None):
    pattern, how = SETS[set_name]
    out = []
    for f in sorted(HERE.glob(pattern)):
        slug = f.stem if how == "stem" else f.parent.name
        if slug in FEATURES and (not only or slug in only):
            out.append({"id": str(f.relative_to(HERE)), "slug": slug, "svg": f, "variant": f.stem})
    return out


def renders(it):
    """480 px icon, and a 64 px icon upscaled to 320 px (nearest) to test small-size legibility."""
    d = CACHE / "renders"
    d.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(it["svg"].read_bytes()).hexdigest()[:16]
    big, small = d / f"{key}-480.png", d / f"{key}-64x5.png"
    if not big.exists():
        big.write_bytes(subprocess.run(["rsvg-convert", "-w", "480", str(it["svg"])], capture_output=True, check=True).stdout)
        tiny = PIL.open(io.BytesIO(subprocess.run(["rsvg-convert", "-w", "64", str(it["svg"])], capture_output=True, check=True).stdout))
        tiny.convert("RGB").resize((320, 320), PIL.NEAREST).save(small)
    return big, small


def request(it):
    big, small = renders(it)
    q = spec(it["slug"])
    images = {"icon": big, "icon_small": small, "style_reference": STYLE_REF}
    r = REFS.get(it["slug"])
    if r:
        images["reference"] = HERE / "refs" / it["slug"] / f"{r['photo_id']}.jpg"
    h = hashlib.sha256(json.dumps([MODEL, q, {k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in images.items()}],
                                  sort_keys=True).encode()).hexdigest()[:20]
    return q, images, CACHE / f"{h}.json"


def check_limits(images):
    for k, p in images.items():
        w, h = PIL.open(p).size
        assert 280 <= w <= 1568 and 280 <= h <= 1568, f"{k} {p.name}: {w}x{h} is outside 280-1568 px"
    assert sum(p.stat().st_size for p in images.values()) < 16 * 2**20, "images too large for one request"


def ask(it):
    q, images, cache = request(it)
    if cache.exists():
        return json.loads(cache.read_text())
    from typesafe_sdk import Image, TypeSafeClient
    try:
        with TypeSafeClient() as client:
            r = client.system_one(state={k: Image(p) for k, p in images.items()}, questions=sdk_questions(q),
                                  model=MODEL, extra_headers=HEADERS)
    except Exception as e:  # a failed call is an error, never an answer
        return {"id": it["id"], "error": f"{type(e).__name__}: {e}"[:300]}
    out = {"id": it["id"], "slug": it["slug"], "variant": it["variant"], "model": r.model,
           "usage": {"in": r.usage.input_tokens, "out": r.usage.output_tokens},
           "answers": {k: v.model_dump(mode="json") for k, v in r.answers.items()}, "questions": q}
    cache.write_text(json.dumps(out, indent=1))
    return out


def run(set_name, dry=False, only=None):
    its = items(set_name, only)
    assert its, f"no icons in {set_name}"
    CACHE.mkdir(parents=True, exist_ok=True)
    for it in its:
        q, images, _ = request(it)
        check_limits(images)
    q0 = spec(its[0]["slug"])
    print(f"{set_name}: {len(its)} icons, {len(q0)} questions for {its[0]['slug']} (limits OK)")
    if dry:
        for k, v in q0.items():
            print(f"  {k:22} {v['type']:6} {v['instructions'][:110]}")
        return
    with ThreadPoolExecutor(4) as pool:
        results = list(pool.map(ask, its))
    errs = [r for r in results if "error" in r]
    tok = [r["usage"] for r in results if "usage" in r]
    print(f"answered {len(results) - len(errs)}, errors {len(errs)}, tokens in {sum(t['in'] for t in tok)} out {sum(t['out'] for t in tok)}")
    for e in errs[:5]:
        print("  ERROR", e["id"], e["error"])


# ---------- verdicts (code owns the decision) ----------

def judge(r):
    a, q, slug = r["answers"], r["questions"], r["slug"]
    key = slug.replace("-", "_")
    p_big, p_small = a["species"]["probabilities"].get(key, 0), a["species_small"]["probabilities"].get(key, 0)
    top = lambda x: max(a[x]["probabilities"].items(), key=lambda kv: kv[1])
    marks = {q[k]["label"]: a[k]["noul"] for k in a if k.startswith("mark_")}
    avoids = {q[k]["label"]: a[k]["noul"] for k in a if k.startswith("avoid_")}
    plaus = {"colors": a["colors_plausible"]["noul"], "head shape": a["head_shape_plausible"]["noul"]}
    reasons, unsure = [], []
    if top("species")[0] != key or p_big < 0.5:
        reasons.append(f"reads as {top('species')[0].replace('_', ' ')} ({top('species')[1]:.2f})")
    reasons += [f"missing: {m}" for m, p in marks.items() if p < NO]
    reasons += [f"shows: {m}" for m, p in avoids.items() if p > YES]
    reasons += [f"{k} not true to species" for k, p in plaus.items() if p < NO]
    unsure += [m for m, p in {**marks, **plaus}.items() if NO <= p <= YES]
    unsure += [m for m, p in avoids.items() if NO <= p <= YES]
    ratio = None
    if a["bill_visible"]["noul"] > YES:
        b, h = a["bill"]["box"], a["head"]["box"]
        hw = h["right"] - h["left"]
        if hw > 0:
            ratio = max(b["right"] - b["left"], b["bottom"] - b["top"]) / hw
    ref_ratio = next(iter(REFS[slug]["ratios"].values()), None) if slug in REFS else None
    likeness = statistics.mean([p_big, statistics.mean(marks.values()), statistics.mean(plaus.values()),
                                1 - max(avoids.values(), default=0)])
    # The "avoid" lists in references.json came from the review of the OpenAI concepts, so a calibration
    # against those known errors also reports the verdict from the generic questions alone.
    generic = [x for x in reasons if not x.startswith("shows: ")]
    return {"id": r["id"], "slug": slug, "variant": r["variant"],
            "verdict": "FLAG" if reasons else "UNSURE" if unsure else "PASS",
            "flag_generic": bool(generic),
            "reasons": reasons, "unsure": unsure, "p_species": round(p_big, 2), "p_species_64": round(p_small, 2),
            "top": top("species")[0], "style": round(a["style"]["score"], 2), "likeness": round(likeness, 3),
            "bill_head": round(ratio, 2) if ratio else None, "ref_ratio": ref_ratio,
            "matches_reference": round(a["matches_reference"]["noul"], 2) if "matches_reference" in a else None}


def load(set_name):
    out = []
    for it in items(set_name):
        _, _, cache = request(it)
        if cache.exists():
            out.append(judge(json.loads(cache.read_text())))
    return out


def report(set_name):
    rows = load(set_name)
    (QA / f"{set_name}.json").write_text(json.dumps(rows, indent=1) + "\n")
    n = {v: sum(r["verdict"] == v for r in rows) for v in ("PASS", "UNSURE", "FLAG")}
    lines = [f"# Likeness check: {set_name}", "",
             f"Model `{MODEL}` (image questions are experimental). {len(rows)} icons: {n['PASS']} pass, {n['UNSURE']} unsure, {n['FLAG']} flagged.",
             f"Noul read as yes above {YES}, no below {NO}. Species is read from a 30-way Choice at 480 px and at 64 px.", "",
             "| Icon | Verdict | Species p (480 / 64) | Style | Likeness | Bill ÷ head (ref) | Why |", "|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["slug"], -r["likeness"])):
        why = "; ".join(r["reasons"]) or ("unsure: " + ", ".join(r["unsure"]) if r["unsure"] else "")
        ratio = f"{r['bill_head']}" + (f" ({r['ref_ratio']})" if r["ref_ratio"] else "") if r["bill_head"] else "-"
        name = r["slug"] if set_name == "openai30" else f"{r['slug']} {r['variant']}"
        lines.append(f"| {name} | {r['verdict']} | {r['p_species']} / {r['p_species_64']} | {r['style']} | {r['likeness']} | {ratio} | {why} |")
    (QA / f"{set_name}.md").write_text("\n".join(lines) + "\n")
    print(f"wrote qa/{set_name}.md: {n}")
    return rows


def calibrate():
    lines = ["# Calibration of the likeness check", ""]
    a = {r["slug"]: r for r in load("openai30")}
    if a:
        flagged = {s for s, r in a.items() if r["verdict"] == "FLAG"}
        tp, fn = sorted(flagged & KNOWN_BAD.keys()), sorted(KNOWN_BAD.keys() - flagged)
        fp = sorted(flagged - KNOWN_BAD.keys())
        tp_generic = sorted(s for s in KNOWN_BAD if a[s]["flag_generic"])
        lines += ["## 1. Known errors in the 30 OpenAI icons", "",
                  f"Caught {len(tp)} of {len(KNOWN_BAD)} known errors. Flagged {len(fp)} of the other {len(a) - len(KNOWN_BAD)} icons.",
                  f"From the generic questions alone (without the review-derived \"avoid\" lists): caught {len(tp_generic)} of {len(KNOWN_BAD)}.", "",
                  "| Known error | Verdict | Why |", "|---|---|---|"]
        lines += [f"| {s} ({KNOWN_BAD[s]}) | {a[s]['verdict']} | {'; '.join(a[s]['reasons']) or ', '.join(a[s]['unsure'])} |" for s in sorted(KNOWN_BAD)]
        lines += ["", "Flagged but not on the known-error list (check by eye: new errors or false alarms):", ""]
        lines += [f"- {s}: {'; '.join(a[s]['reasons'])}" for s in fp] or ["- none"]
        lines.append("")
    b = load("bakeoff36")
    if b:
        lines += ["## 2. Chris's blind votes on the 36 bake-off tiles", "",
                  "Rank = position of Chris's best pick when the six tiles are sorted by likeness (1 = QA agrees).", "",
                  "| Bird | Chris's best | QA rank of it | QA's top tile | Tiles flagged |", "|---|---|---|---|---|"]
        hits = []
        for slug, picks in VOTES.items():
            tiles = sorted([r for r in b if r["slug"] == slug], key=lambda r: -r["likeness"])
            flagged = sum(r["verdict"] == "FLAG" for r in tiles)
            if picks:
                rank = next((i + 1 for i, r in enumerate(tiles) if r["variant"] == picks[0]), None)
                hits.append(rank is not None and rank <= 2)
                lines.append(f"| {slug} | {picks[0]} | {rank} | {tiles[0]['variant']} | {flagged} of {len(tiles)} |")
            else:
                lines.append(f"| {slug} | none works | - | {tiles[0]['variant']} | {flagged} of {len(tiles)} (all should fail) |")
        lines += ["", f"Chris's best pick is in QA's top 2 for {sum(hits)} of {len(hits)} birds."]
    (QA / "CALIBRATION.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:]
    only = None
    if "--only" in rest:
        i = rest.index("--only")
        only, rest = set(rest[i + 1].split(",")), rest[:i] + rest[i + 2:]
    if cmd == "run":
        run(rest[0], dry="--dry-run" in rest, only=only)
    elif cmd == "report":
        report(rest[0])
    elif cmd == "calibrate":
        calibrate()
