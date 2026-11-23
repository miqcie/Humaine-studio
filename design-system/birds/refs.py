#!/usr/bin/env python3
"""Fetch commercial-safe reference photos (CC0 / CC BY) from iNaturalist for the bird icons.

Run: uv run --with pillow python design-system/birds/refs.py [slug ...]   (no slugs: resolve taxa only)
Writes: taxa.json (all 30, committed), reference-credits.csv (committed),
        refs/<slug>/<photo_id>.jpg + refs/<slug>/_sheet.png (git-ignored).
Photos are references for measuring and as model inputs. Never trace them. Audubon photos are never fetched.
"""
import csv
import hashlib
import json
import pathlib
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
REFS, CACHE = HERE / "refs", HERE / "refs" / "_cache"
TAXA, CREDITS = HERE / "taxa.json", HERE / "reference-credits.csv"
API, UA = "https://api.inaturalist.org/v1", "humaine-bird-refs"
OK_LICENSES = {"cc0", "cc-by"}  # commercial use allowed; NC, ND and SA are not
PER_SPECIES = 12
# Brief name -> iNat common name, where iNat's taxonomy splits a species. The brief's label stays as written.
ALIASES = {"Whimbrel": "Hudsonian Whimbrel"}  # the North American bird; Eurasian Whimbrel does not reach Virginia regularly


def get(path, **params):
    """Cached GET, at most one live request per second."""
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    CACHE.mkdir(parents=True, exist_ok=True)
    key = CACHE / (hashlib.sha256(url.encode()).hexdigest()[:32] + ".json")  # the full URL, so long URLs never collide
    if key.exists():
        return json.loads(key.read_text())
    time.sleep(1)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
        data = json.load(r)
    key.write_text(json.dumps(data))
    return data


def norm(s):
    return unicodedata.normalize("NFKD", s).replace("’", "'").replace("-", " ").lower().strip()


def resolve(names):
    """Common name -> iNat species taxon, by exact preferred common name."""
    out = {}
    for slug, label in names.items():
        name = ALIASES.get(label, label)
        res = get("taxa", q=name, rank="species", per_page=10)["results"]
        hits = [t for t in res if norm(t.get("preferred_common_name", "")) == norm(name)]
        assert len(hits) == 1, f"{name}: {len(hits)} exact matches in {[t.get('preferred_common_name') for t in res]}"
        t = hits[0]
        out[slug] = {"name": label, "inat_name": t["preferred_common_name"], "taxon_id": t["id"], "scientific": t["name"], "inat": f"https://www.inaturalist.org/taxa/{t['id']}"}
    return out


def observations(taxon_id):
    base = dict(taxon_id=taxon_id, photo_license="cc0,cc-by", quality_grade="research", order_by="votes", per_page=30, photos="true")
    res = get("observations", term_id=1, term_value_id=2, **base)["results"]  # Life Stage = Adult
    if len(res) < 10:
        res = get("observations", **base)["results"]
    return res


def fetch(slug, taxon):
    d = REFS / slug
    d.mkdir(parents=True, exist_ok=True)
    rows = []
    for obs in observations(taxon["taxon_id"]):
        for p in obs["photos"]:
            if p.get("license_code") not in OK_LICENSES:
                continue
            f = d / f"{p['id']}.jpg"
            if not f.exists():
                time.sleep(1)
                url = p["url"].replace("square", "medium")
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                    f.write_bytes(r.read())
            rows.append({"slug": slug, "photo_id": p["id"], "observer": obs["user"]["login"], "license": p["license_code"],
                         "observation": f"https://www.inaturalist.org/observations/{obs['id']}"})
            break  # one photo per observation, for variety
        if len(rows) == PER_SPECIES:
            break
    assert rows, f"{slug}: no CC0/CC BY photos"
    sheet(d, rows)
    return rows


def sheet(d, rows, cell=300):
    """Numbered contact sheet, 4 across, for picking a side-profile photo by eye."""
    cols = 4
    im = Image.new("RGB", (cols * cell, -(-len(rows) // cols) * cell), "#F3ECE0")
    draw = ImageDraw.Draw(im)
    for i, r in enumerate(rows):
        t = Image.open(d / f"{r['photo_id']}.jpg").convert("RGB")
        t.thumbnail((cell - 8, cell - 8))
        x, y = (i % cols) * cell + 4, (i // cols) * cell + 4
        im.paste(t, (x, y))
        draw.rectangle((x, y, x + 34, y + 22), fill="#0B0F24")
        draw.text((x + 6, y + 5), str(i + 1), fill="#FAF6EE")
    im.save(d / "_sheet.png")
    (d / "_index.json").write_text(json.dumps({i + 1: r["photo_id"] for i, r in enumerate(rows)}, indent=1))


def main(slugs):
    sys.path.insert(0, str(HERE))
    from species import BIRDS
    taxa = resolve({s: b["name"] for s, b in BIRDS.items()})
    assert len(taxa) == 30 and len({t["taxon_id"] for t in taxa.values()}) == 30
    TAXA.write_text(json.dumps(taxa, indent=2, ensure_ascii=False) + "\n")
    print(f"resolved {len(taxa)} taxa")
    if not slugs:
        return
    old = list(csv.DictReader(CREDITS.open())) if CREDITS.exists() else []
    rows = [r for r in old if r["slug"] not in slugs]
    for s in slugs:
        got = fetch(s, taxa[s])
        rows += got
        print(f"{s}: {len(got)} photos")
    assert all(r["license"] in OK_LICENSES for r in rows)
    with CREDITS.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["slug", "photo_id", "observer", "license", "observation"])
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["slug"], int(r["photo_id"]))))


if __name__ == "__main__":
    main(sys.argv[1:])
