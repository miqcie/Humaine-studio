#!/usr/bin/env python3
"""Build the blind voting page for a round: <round>/vote/ (index.html + tiles/ + ref/).

Run: uv run --with pillow python design-system/birds/bakeoff/vote_page.py [--dir round2]
Tiles are copied as <bird>-<letter>.svg from <round>/key.json, so nothing about a tile's source reaches the page.
Votes are saved to the artifact's db (collection "votes", one document per bird) and read back by Claude.
Page text comes from <round>/config.json "page" (title, eyebrow, intro), with the bake-off text as the default.
"""
import html
import json
import pathlib
import shutil
import sys

from PIL import Image

HERE = pathlib.Path(__file__).parent
BIRDS = HERE.parent
ROOT = BIRDS / (sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else "bakeoff")
OUT = ROOT / "vote"
DEFAULT_PAGE = {
    "title": "Bird Bake-off",
    "eyebrow": "Humaine Studio · Virginia birds · Blind bake-off",
    "intro": "Six birds, six tiles each. Every tile came from one of three image generators and was traced into the same "
             "frame and palette. The letters are shuffled, so nothing tells you which tool made which. For each bird, pick "
             "your best and your second best. Judge it as an icon: is it this species, at a glance and at small size?",
}


def main():
    key = json.loads((ROOT / "key.json").read_text())
    config = json.loads((ROOT / "config.json").read_text()) if (ROOT / "config.json").exists() else {}
    page = {**DEFAULT_PAGE, **config.get("page", {})}
    refs = json.loads((BIRDS / "references.json").read_text())
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "tiles").mkdir(parents=True)
    (OUT / "ref").mkdir()
    birds = []
    for slug, letters in key.items():
        for letter, stem in letters.items():
            shutil.copy(ROOT / "traced" / slug / f"{stem}.svg", OUT / "tiles" / f"{slug}-{letter}.svg")
        r = refs[slug]
        im = Image.open(BIRDS / "refs" / slug / f"{r['photo_id']}.jpg").convert("RGB")
        im.thumbnail((720, 720))
        im.save(OUT / "ref" / f"{slug}.jpg", "JPEG", quality=84)
        birds.append({"slug": slug, "name": r["name"], "sci": r["scientific"], "marks": r["marks"],
                      "credit": r["credit"], "obs": r["observation"], "audubon": r["audubon"], "letters": sorted(letters),
                      "notes": r.get("notes", "") if config else ""})
    text = (HERE / "vote_template.html").read_text()
    for k in ("title", "eyebrow", "intro"):
        text = text.replace(f"__{k.upper()}__", html.escape(page[k]))
    (OUT / "index.html").write_text(text.replace("__BIRDS__", json.dumps(birds)))
    print(f"wrote {OUT} with {len(birds)} birds, {sum(len(b['letters']) for b in birds)} tiles")


if __name__ == "__main__":
    main()
