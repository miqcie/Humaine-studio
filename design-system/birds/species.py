"""Palette, regions and the 30 species of the Virginia bird icons. Names are verbatim from the brief.

The hand-drawn concept geometry that used to live here was retired after the traced OpenAI drafts replaced it
(tasks/lessons.md: do not draw anatomy from coordinates); it is in git history up to commit 2a6cae9.
"""
import re

# Klein & Linen palette. N is the brief's navy (Klein Night ground); the shipped logo frame uses #0E1230.
N = "#0B0F24"   # navy: frame, silhouettes
F = "#FAF6EE"   # surface: icon field, pale plumage
G = "#F3ECE0"   # ground: sheet background
M = "#5E6178"   # muted
Y = "#F7B902"   # chrome yellow
R = "#C7301C"   # vermilion
B = "#002FA7"   # Klein blue

REGIONS = [
    {"key": "coastal", "title": "Coastal Plain / Tidewater", "sub": "Including the Eastern Shore"},
    {"key": "piedmont", "title": "Piedmont"},
    {"key": "blue-ridge", "title": "Blue Ridge Mountains"},
    {"key": "valley", "title": "Valley and Ridge", "sub": "Including the Shenandoah Valley"},
    {"key": "plateau", "title": "Appalachian Plateau", "sub": "Far Southwest Virginia"},
    {"key": "rva", "title": "RVA / Fall Line", "sub": "Richmond and the James River"},
]

BRIEF = {  # verbatim from the brief, in order
    "coastal": ["Whimbrel", "Marbled Godwit", "American Oystercatcher", "Brown Pelican", "Black Skimmer"],
    "piedmont": ["Eastern Bluebird", "Eastern Meadowlark", "Indigo Bunting", "Northern Bobwhite", "Red-headed Woodpecker"],
    "blue-ridge": ["Common Raven", "Scarlet Tanager", "Cerulean Warbler", "Peregrine Falcon", "Rose-breasted Grosbeak"],
    "valley": ["American Kestrel", "American Barn Owl", "Eastern Screech-Owl", "Belted Kingfisher", "Wild Turkey"],
    "plateau": ["Hooded Warbler", "Blackburnian Warbler", "Black-and-white Warbler", "Swainson’s Warbler", "Ruffed Grouse"],
    "rva": ["Great Blue Heron", "Osprey", "Double-crested Cormorant", "Wood Duck", "Chimney Swift"],
}

# slug -> {name, region}; "Swainson’s Warbler" -> swainsons-warbler
BIRDS = {re.sub(r"[^a-z0-9]+", "-", n.lower().replace("’", "")).strip("-"): {"name": n, "region": k}
         for k, names in BRIEF.items() for n in names}
assert len(BIRDS) == 30 and [r["key"] for r in REGIONS] == list(BRIEF)
