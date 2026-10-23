"""Copy-edit the /tools/ cards as plain Markdown instead of YAML.

  uv run --with pyyaml scripts/showcase-copy.py export ~/Desktop/tools-copy.md
  uv run --with pyyaml scripts/showcase-copy.py import ~/Desktop/tools-copy.md
  uv run --with pyyaml scripts/showcase-copy.py check   # round-trip self-test

Export writes every card's words to one Markdown file. Import reads that file
back and rewrites _data/showcase.yml. Images and links stay in the YAML.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

import yaml

DATA = Path(__file__).resolve().parent.parent / "_data" / "showcase.yml"

# Markdown label -> YAML key, in the order they appear on a card
LABELS = [
    ("Status", "status"),
    ("What is it", "what"),
    ("Why does it exist", "why"),
    ("What problem does it solve", "problem"),
    ("How was it built", "built"),
    ("Mistakes and lessons", "lessons"),
    ("Other uses", "uses"),
    ("Note", "note"),
]
KEY_ORDER = ["id", "title", "status", "image", "alt", "what", "why", "problem", "built", "lessons", "uses", "note"]

HEADER = """# Tools page copy

Edit the words after each bold label. Keep the bold labels and the `id:` lines as they are.
You can change a title (the ### line). Status is one of: Live, Open source, Private, Archived.
Delete a **Note:** line to remove the note. When you are done, tell Claude "import the tools copy".
"""


def export(out):
    data = yaml.safe_load(DATA.read_text())
    lines = [HEADER]
    for g in data["groups"]:
        lines.append(f"## {g['name']}\n")
        for p in g["projects"]:
            lines.append(f"### {p['title']}\nid: {p['id']}\n")
            for label, key in LABELS:
                if key in p:
                    lines.append(f"**{label}:** {p[key]}\n")
            lines.append("")
    Path(out).expanduser().write_text("\n".join(lines))


def parse(md):
    """Return {id: {field: value}} from the edited Markdown."""
    cards, card, key, title = {}, None, None, None
    by_label = dict(LABELS)
    for raw in md.splitlines():
        line = raw.strip()
        if line.startswith("### "):
            title, card, key = line[4:].strip(), None, None
        elif line.startswith("id: ") and title:
            card = cards.setdefault(line[4:].strip(), {"title": title})
        elif line.startswith("#"):
            card, key = None, None
        elif card is not None:
            m = re.match(r"\*\*(.+?):\*\*\s*(.*)", line)
            if m and m.group(1) in by_label:
                key = by_label[m.group(1)]
                card[key] = m.group(2).strip()
            elif line and key:
                card[key] += " " + line  # a value wrapped onto more lines
    return cards


def dump(data):
    out = ["# Cards for /tools/. Each value is Markdown (inline links and code work).", "groups:"]
    for g in data["groups"]:
        out.append(f"  - name: {json.dumps(g['name'])}")
        out.append("    projects:")
        for p in g["projects"]:
            first = True
            for k in KEY_ORDER:
                if k in p:
                    out.append(f"      {'- ' if first else '  '}{k}: {json.dumps(p[k], ensure_ascii=False)}")
                    first = False
            if p.get("links"):
                out.append("        links:")
                for link in p["links"]:
                    out.append(f"          - label: {json.dumps(link['label'], ensure_ascii=False)}")
                    out.append(f"            url: {json.dumps(link['url'])}")
    return "\n".join(out) + "\n"


def import_(src, target=DATA):
    data = yaml.safe_load(target.read_text())
    edits = parse(Path(src).expanduser().read_text())
    known = {p["id"] for g in data["groups"] for p in g["projects"]}
    unknown = set(edits) - known
    if unknown:
        sys.exit(f"Unknown id lines (were they edited?): {', '.join(sorted(unknown))}")
    for g in data["groups"]:
        for p in g["projects"]:
            e = edits.get(p["id"])
            if e is None:
                sys.exit(f"Card missing from the copy file: {p['id']}")
            for k in ["title"] + [k for _, k in LABELS]:
                if e.get(k):
                    p[k] = e[k]
                elif k == "note":
                    p.pop("note", None)  # a deleted Note line removes the note
    target.write_text(dump(data))
    return len(edits)


def check():
    with tempfile.TemporaryDirectory() as d:
        md, copy = Path(d) / "copy.md", Path(d) / "showcase.yml"
        copy.write_text(DATA.read_text())
        export(md)
        import_(md, copy)
        assert copy.read_text() == DATA.read_text(), "round trip changed showcase.yml"
    print("round trip ok")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "export" and len(sys.argv) == 3:
        export(sys.argv[2])
        print(f"wrote {sys.argv[2]}")
    elif cmd == "import" and len(sys.argv) == 3:
        print(f"updated {import_(sys.argv[2])} cards in {DATA.name}")
    elif cmd == "check":
        check()
    else:
        sys.exit(__doc__)
