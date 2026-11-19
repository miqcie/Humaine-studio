#!/usr/bin/env python3
"""Build the blind voting page for the bake-off: bakeoff/vote/ (index.html + tiles/ + ref/).

Run: uv run --with pillow python design-system/birds/bakeoff/vote_page.py
Tiles are copied as <bird>-<letter>.svg from key.json, so no contestant name reaches the page.
Votes are saved to the artifact's db (collection "votes", one document per bird) and read back by Claude.
"""
import json
import pathlib
import shutil

from PIL import Image

HERE = pathlib.Path(__file__).parent
BIRDS = HERE.parent
OUT = HERE / "vote"


def main():
    key = json.loads((HERE / "key.json").read_text())
    refs = json.loads((BIRDS / "references.json").read_text())
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "tiles").mkdir(parents=True)
    (OUT / "ref").mkdir()
    birds = []
    for slug, letters in key.items():
        for letter, stem in letters.items():
            shutil.copy(HERE / "traced" / slug / f"{stem}.svg", OUT / "tiles" / f"{slug}-{letter}.svg")
        r = refs[slug]
        im = Image.open(BIRDS / "refs" / slug / f"{r['photo_id']}.jpg").convert("RGB")
        im.thumbnail((720, 720))
        im.save(OUT / "ref" / f"{slug}.jpg", "JPEG", quality=84)
        birds.append({"slug": slug, "name": r["name"], "sci": r["scientific"], "marks": r["marks"],
                      "credit": r["credit"], "obs": r["observation"], "audubon": r["audubon"], "letters": sorted(letters)})
    html = (HERE / "vote_template.html").read_text().replace("__BIRDS__", json.dumps(birds))
    (OUT / "index.html").write_text(html)
    print(f"wrote {OUT} with {len(birds)} birds, {sum(len(b['letters']) for b in birds)} tiles")


if __name__ == "__main__":
    main()
