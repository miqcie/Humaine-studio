"""Geometry for the 30 Virginia birds. Icon units: 240 x 240, field 13..227, right-facing.

Shared rules (and only these): navy frame, ivory field, head scale, eye spec, and the bird bleeds off the
left and bottom edges only. Pale plumage never touches the field: it sits inside a keyline of the bird's
own dark color (`pale`). Each species draws its own outline.
"""

# Klein & Linen palette. N is the brief's navy (Klein Night ground); the shipped logo frame uses #0E1230.
N = "#0B0F24"   # navy: frame, silhouettes
F = "#FAF6EE"   # surface: icon field, pale plumage
G = "#F3ECE0"   # ground: sheet background
SUNK = "#EAE2D4"
RULE = "#DCD3C3"
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


# ---------- drawing helpers ----------

def P(d, c):
    return f'<path d="{d}" fill="{c}"/>'


def C(x, y, r, c):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def E(x, y, rx, ry, c, rot=0):
    t = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"{t}/>'


def circ(x, y, r):
    return ell(x, y, r, r)


def ell(x, y, rx, ry):
    return f"M{x - rx},{y} a{rx},{ry} 0 1,0 {2 * rx},0 a{rx},{ry} 0 1,0 {-2 * rx},0 Z"


def eye(x, y, on=N, r=10, ring=None):
    """Eye spec. Dark plumage: an ivory ring around a pupil of the plumage color (as in the curlew logo).
    Pale or yellow plumage: a navy dot. `ring` gives species with a colored eye or orbital ring that color."""
    if ring:
        return C(x, y, r, ring) + C(x, y, r * 0.5, N)
    if on in (F, Y):
        return C(x, y, r * 0.6, N)
    return C(x, y, r, F) + C(x, y, r * 0.5, on)


def clip(cid, shape):
    """A clip path from a path `d` string or from ready-made shapes."""
    body = shape if shape.startswith("<") else f'<path d="{shape}"/>'
    return f'<clipPath id="{cid}">{body}</clipPath>'


def pale(slug, name, sil, region, line=N, key=6, color=F):
    """Pale plumage: `region` in `color`, clipped to `sil`. Where it meets the silhouette edge it keeps a
    `line`-colored keyline `key` wide, so pale plumage never touches the field."""
    fill = region if region.startswith("<") else P(region, color)  # a path, or ready-made shapes
    rid = f"{slug}-{name}-r"
    keyline = f'<g clip-path="url(#{rid})"><path d="{sil}" fill="none" stroke="{line}" stroke-width="{2 * key}"/></g>'
    return inside(slug, name, sil, fill + clip(rid, fill) + keyline)


def inside(slug, name, sil, body):
    """Paint `body` only where it falls inside the silhouette `sil`."""
    cid = f"{slug}-{name}"
    return clip(cid, sil) + f'<g clip-path="url(#{cid})">{body}</g>'


BIRDS = {}


def bird(slug, name, region, **kw):
    def deco(fn):
        BIRDS[slug] = {"name": name, "region": region, "art": fn, **kw}
        return fn
    return deco


# ======================= 1. Coastal Plain / Tidewater =======================

@bird("whimbrel", "Whimbrel", "coastal")
def _(s):
    head = circ(96, 86, 32)
    body = "M0,240 L0,150 C20,130 48,118 70,112 L122,104 C128,140 140,190 158,240 Z"
    stripes = (P("M40,40 L160,40 L160,68 L40,72 Z", N)        # dark lateral crown stripe
               + P("M84,59 L108,58 L108,63 L84,64 Z", F)       # pale median stripe
               + P("M82,74 L120,72 L120,79 L82,81 Z", F)       # pale eyebrow
               + P("M60,84 L160,82 L160,90 L60,92 Z", N))      # dark eye-line
    return (P(body, M) + inside(s, "wing", body, E(36, 214, 60, 34, Y, -30)) + P(head, M)
            + inside(s, "head", head, stripes)
            + P("M122,76 C156,78 186,100 204,140 C182,114 154,98 124,96 Z", N)   # long decurved bill
            + eye(108, 86, N, 8))


@bird("marbled-godwit", "Marbled Godwit", "coastal")
def _(s):
    head = circ(92, 94, 28)
    body = "M0,240 L0,160 C24,136 52,124 72,118 L114,110 C120,150 132,196 148,240 Z"
    sil = head + " " + body
    bill = "M114,88 C148,86 180,76 210,58 L212,64 C184,82 150,98 114,102 Z"
    marbling = "".join(P(f"M{x},{y} h10 v10 h-10 Z", N)
                       for x, y in [(14, 168), (36, 160), (24, 188), (48, 180), (14, 212), (40, 206), (62, 198), (30, 228), (56, 224)])
    return (P(body, Y) + P(head, Y)
            + inside(s, "back", sil, marbling)
            + P(bill, R) + inside(s, "tip", bill, P("M170,40 L230,40 L230,110 L170,110 Z", N))
            + eye(96, 90, Y))


@bird("american-oystercatcher", "American Oystercatcher", "coastal")
def _(s):
    head = circ(96, 86, 36)
    body = "M0,240 L0,140 C20,124 46,116 68,112 L126,110 C132,150 142,196 154,240 Z"
    sil = head + " " + body
    return (P(body, N) + P(head, N)
            + pale(s, "belly", sil, "M0,250 L36,240 L68,186 L150,158 L240,152 L240,250 Z")
            + P("M124,72 L208,86 L210,96 L126,106 Z", R)                           # heavy straight bill
            + C(106, 80, 12, R) + C(106, 80, 8, Y) + C(106, 80, 3.5, N))         # red orbital ring, yellow eye


@bird("brown-pelican", "Brown Pelican", "coastal")
def _(s):
    neck = ("M0,240 L0,182 C26,170 42,146 48,116 C54,84 56,60 68,46 C80,34 100,36 110,50 "
            "L114,84 C102,104 96,132 102,160 C108,192 128,214 148,240 Z")
    head = "M58,60 C58,38 74,28 92,30 C110,32 118,46 116,62 C114,80 98,88 82,86 C68,84 58,76 58,60 Z"
    return (P(neck, N)
            + pale(s, "foreneck", neck, "M96,86 C86,110 82,136 88,162 C94,192 112,216 130,240 L240,240 L240,86 Z")
            + P(head, N)
            + pale(s, "head", head, P("M0,0 H240 V240 H0 Z", F) + E(84, 34, 34, 12, Y))   # white head, yellow crown
            + P("M106,68 C140,84 176,98 204,104 C184,114 140,112 108,90 Z", N)           # dark pouch
            + P("M104,52 L208,96 L212,108 L202,104 L104,70 Z", M)                        # upper mandible, hooked tip
            + eye(96, 60, F))


@bird("black-skimmer", "Black Skimmer", "coastal")
def _(s):
    sil = ("M0,240 L0,140 C26,122 50,110 70,100 C70,74 86,56 106,56 C126,56 138,72 136,92 "
           "C136,140 142,196 154,240 Z")
    upper, lower = "M128,80 L188,102 L130,100 Z", "M130,104 L212,114 L128,120 Z"
    return (P(sil, N) + inside(s, "wing", sil, E(26, 204, 54, 30, Y, -30))
            + pale(s, "face", sil, "M140,98 C116,100 92,104 78,108 C66,150 54,200 46,240 L200,240 L200,98 Z")
            + P(upper, R) + inside(s, "ut", upper, P("M164,60 L240,60 L240,130 L164,130 Z", N))
            + P(lower, R) + inside(s, "lt", lower, P("M178,60 L240,60 L240,130 L178,130 Z", N))
            + eye(110, 80))


# ======================= 2. Piedmont =======================

@bird("eastern-bluebird", "Eastern Bluebird", "piedmont")
def _(s):
    head = circ(106, 94, 46)
    body = "M0,240 L0,150 C20,124 50,110 78,104 L148,110 C160,150 170,196 176,240 Z"
    sil = head + " " + body
    return (P(body, B) + P(head, B)
            + inside(s, "breast", sil, P("M240,114 L150,114 C128,132 112,172 108,240 L240,240 Z", R))
            + pale(s, "belly", sil, "M240,200 L136,200 C126,212 122,226 120,240 L240,240 Z", line=B)
            + P("M148,84 L170,92 L148,100 Z", N)
            + eye(124, 84, B))


@bird("eastern-meadowlark", "Eastern Meadowlark", "piedmont")
def _(s):
    head = circ(110, 82, 36)
    body = "M0,240 L0,160 C20,130 50,112 80,106 L142,100 C158,140 172,190 180,240 Z"
    sil = head + " " + body
    return (P(body, M) + P(head, M)
            + inside(s, "breast", sil, P("M240,96 L134,96 C118,130 110,180 108,240 L240,240 Z", Y))
            + inside(s, "chevron", sil, P("M112,130 L148,164 L184,124 L186,146 L148,186 L110,150 Z", N))
            + inside(s, "brow", head, P("M88,64 L136,62 L136,70 L88,72 Z", F) + P("M40,40 L160,40 L160,54 L40,58 Z", N))
            + P("M140,74 L194,84 L140,92 Z", N)                                       # long pointed bill
            + eye(124, 80, M, 9))


@bird("indigo-bunting", "Indigo Bunting", "piedmont")
def _(s):
    head = circ(110, 100, 52)
    body = "M0,240 L0,156 C20,128 50,114 80,108 L154,120 C166,160 174,200 178,240 Z"
    sil = head + " " + body
    return (P(body, B) + P(head, B)
            + inside(s, "wing", sil, P("M0,170 L96,190 L118,240 L0,240 Z", N))            # dark flight feathers
            + P("M156,86 L192,102 L156,118 Z", M)                                          # conical bill
            + eye(132, 94, B))


@bird("northern-bobwhite", "Northern Bobwhite", "piedmont")
def _(s):
    head = circ(108, 100, 40)
    body = "M0,240 L0,170 C20,142 50,130 80,126 L146,126 C156,162 166,202 170,240 Z"
    sil = head + " " + body
    return (P(body, R) + P(head, R)
            + P("M90,70 C92,58 104,54 114,58 C106,60 102,64 102,72 Z", R)                    # small crest
            + P("M74,94 C90,84 112,80 140,80 L140,90 C114,90 94,94 78,104 Z", F)            # white eyebrow, sweeping back
            + inside(s, "mask", head, P("M60,106 C84,94 110,90 160,92 L160,104 C112,102 90,106 62,120 Z", N))  # black eye-stripe
            + P("M112,110 L142,106 C142,118 134,128 122,130 C114,130 108,122 112,110 Z", F)  # white throat
            + inside(s, "necklace", sil, P("M104,124 C116,136 132,136 150,124 L170,124 L170,138 L100,140 Z", N))
            + P("M146,92 L162,99 L146,106 Z", N)
            + eye(124, 99, N, 7))


@bird("red-headed-woodpecker", "Red-headed Woodpecker", "piedmont")
def _(s):
    head = circ(110, 88, 40)
    body = "M0,240 L0,150 C20,132 50,126 80,126 L148,126 C158,162 166,202 170,240 Z"
    return (P(body, N)
            + pale(s, "breast", body, "M120,120 L240,120 L240,240 L96,240 Z")
            + P("M30,152 h50 v44 h-50 Z", F)                                           # white secondaries block
            + inside(s, "head", "M0,0 H240 V126 H0 Z", P(head, R))                    # solid red head, cut straight
            + P("M146,78 L194,86 L194,90 L146,100 Z", N)                              # chisel bill
            + eye(124, 82, R))


# ======================= 3. Blue Ridge Mountains =======================

@bird("common-raven", "Common Raven", "blue-ridge")
def _(s):
    head = "M60,98 C56,66 78,44 106,44 C122,44 130,54 134,66 L138,110 C120,126 90,130 70,120 Z"
    body = "M0,240 L0,140 C20,120 50,110 70,112 L134,116 C144,158 152,200 158,240 Z"
    hackles = "M132,108 L150,116 L134,122 L152,132 L134,138 L152,150 L132,154 L136,170 L120,160 Z"
    return (P(body, N) + P(head, N) + P(hackles, N)
            + inside(s, "sheen", body, P("M0,240 L0,186 C30,168 70,166 96,182 L120,240 Z", B))
            + P("M128,62 C162,62 192,80 206,106 C190,108 160,108 132,108 Z", N)         # heavy bill
            + eye(106, 78))


@bird("scarlet-tanager", "Scarlet Tanager", "blue-ridge")
def _(s):
    head = ell(108, 94, 48, 42)
    body = "M0,240 L0,150 C20,126 50,114 80,108 L150,112 C160,152 168,200 172,240 Z"
    sil = head + " " + body
    return (P(body, R) + P(head, R)
            + inside(s, "wing", sil, P("M0,240 L0,168 C30,150 70,148 100,166 C110,190 112,216 110,240 Z", N))
            + P("M150,82 L182,96 L150,110 Z", M)                                       # stout bill
            + eye(126, 88, R))


@bird("cerulean-warbler", "Cerulean Warbler", "blue-ridge")
def _(s):
    head = circ(104, 94, 34)
    body = "M0,240 L0,150 C20,128 50,116 76,112 L132,114 C142,150 150,200 156,240 Z"
    sil = head + " " + body
    wing = "M0,240 L0,176 C24,158 60,156 86,170 L104,240 Z"
    return (P(body, B) + P(head, B)
            + pale(s, "under", sil, "M240,106 L128,108 C112,140 104,190 102,240 L240,240 Z", line=B)
            + inside(s, "band", sil, P("M106,148 L160,136 L160,148 L108,160 Z", N))   # dark breast band
            + inside(s, "wing", sil, P(wing, N))
            + inside(s, "bars", wing, P("M10,192 L72,180 L74,188 L12,200 Z", F) + P("M14,212 L80,200 L82,208 L16,220 Z", F))
            + P("M134,88 L166,94 L134,98 Z", N)                                        # fine bill
            + eye(116, 88, B, 9))


@bird("peregrine-falcon", "Peregrine Falcon", "blue-ridge")
def _(s):
    head = circ(102, 90, 40)
    body = "M0,240 L0,146 C20,126 48,118 72,116 L138,116 C148,154 154,200 158,240 Z"
    sil = head + " " + body
    # White cheek and throat, joined under a broad dark malar that drops from the eye.
    face = "M240,100 L122,100 L120,124 C118,132 110,132 108,124 L106,100 L76,104 L72,142 L96,240 L240,240 Z"
    return (P(body, N) + P(head, N)
            + inside(s, "back", sil, P("M0,240 L0,150 L60,140 L84,240 Z", M))
            + pale(s, "face", sil, face)
            + P("M136,78 C150,76 160,86 160,98 C160,104 158,108 154,112 C154,104 150,100 136,102 Z", N)  # hooked bill
            + eye(116, 84, ring=Y))


@bird("rose-breasted-grosbeak", "Rose-breasted Grosbeak", "blue-ridge")
def _(s):
    head = circ(106, 90, 40)
    body = "M0,240 L0,150 C20,128 50,118 78,114 L144,114 C154,152 162,200 166,240 Z"
    sil = head + " " + body
    return (P(body, N) + P(head, N)
            + pale(s, "breast", sil, "M240,124 L136,124 C120,150 112,196 110,240 L240,240 Z")
            + inside(s, "rose", sil, P("M122,124 L174,124 L140,182 Z", R))
            + P("M34,168 h18 v18 h-18 Z", F)                                           # white wing patch
            + P("M140,72 L182,92 L140,112 Z", M)                                       # large triangular bill
            + eye(120, 82))


# ======================= 4. Valley and Ridge =======================

@bird("american-kestrel", "American Kestrel", "valley")
def _(s):
    head = circ(104, 92, 42)
    body = "M0,240 L0,152 C20,130 50,120 76,116 L140,118 C150,156 156,200 160,240 Z"
    face = (P("M0,88 H240 V240 H0 Z", F)
            + P("M114,88 L128,88 L124,132 L116,132 Z", N)        # moustache below the eye
            + P("M84,92 L96,92 L94,128 L86,128 Z", N))           # second stripe on the ear
    return (P(body, R)
            + pale(s, "breast", body, "M240,128 L134,128 C120,160 114,200 112,240 L240,240 Z", line=R)
            + inside(s, "bars", body, P("M8,170 h30 v8 h-30 Z", N) + P("M18,194 h30 v8 h-30 Z", N) + P("M6,218 h30 v8 h-30 Z", N))
            + P(head, B)
            + C(98, 64, 9, R)                                     # rufous cap spot
            + pale(s, "face", head, face, line=R)
            + P("M140,80 C152,80 160,90 160,102 C160,108 158,112 154,116 C154,106 150,100 140,100 Z", N)  # small hooked bill
            + eye(122, 84, B, 8))


@bird("american-barn-owl", "American Barn Owl", "valley")
def _(s):
    disc = ("M132,72 C120,50 72,54 74,100 C76,136 110,158 132,172 C152,158 182,136 184,100 "
            "C186,54 144,50 132,72 Z")
    rim = ("M132,62 C118,40 62,44 64,100 C66,142 104,166 132,182 C158,166 194,142 194,100 "
           "C196,44 146,40 132,62 Z")
    return (P("M36,240 C36,186 60,152 100,146 L164,146 C196,152 206,190 206,240 Z", Y)
            + E(126, 240, 44, 66, F)
            + E(128, 108, 72, 66, Y)
            + P(rim, N) + P(disc, F)
            + P("M134,112 C129,122 130,134 136,144 C142,134 143,122 138,112 Z", M)
            + eye(110, 104, F, 14) + eye(156, 104, F, 14))


@bird("eastern-screech-owl", "Eastern Screech-Owl", "valley")
def _(s):
    head = ("M66,122 C60,92 62,66 70,46 L86,66 C102,60 140,60 156,66 L172,46 C180,66 182,92 176,122 "
            "C170,150 142,164 120,164 C98,164 72,150 66,122 Z")
    return (P("M40,240 C40,190 64,156 100,152 L144,152 C182,158 200,196 200,240 Z", M)
            + P(head, M)
            + C(100, 108, 28, N) + C(100, 108, 21, M) + C(146, 108, 25, N) + C(146, 108, 18, M)
            + C(100, 108, 12, Y) + C(100, 108, 6, N) + C(146, 108, 11, Y) + C(146, 108, 5.5, N)
            + P("M118,118 L130,118 L124,136 Z", F)
            + P("M110,180 h6 v26 h-6 Z", N) + P("M128,186 h6 v26 h-6 Z", N) + P("M146,180 h6 v26 h-6 Z", N))


@bird("belted-kingfisher", "Belted Kingfisher", "valley")
def _(s):
    head = circ(102, 90, 40)
    crest = "M84,54 L36,46 L64,68 L28,76 L62,86 L34,102 L70,104 Z"
    body = "M0,240 L0,150 C20,132 46,124 74,122 L140,120 C150,158 156,200 160,240 Z"
    sil = head + " " + body
    return (P(body, B) + P(crest, B) + P(head, B)
            + pale(s, "collar", sil, "M240,104 L132,106 L112,126 L0,128 L0,146 L240,146 Z", line=B)
            + pale(s, "belly", sil, "M240,176 L108,180 L104,240 L240,240 Z", line=B)
            + C(132, 78, 5, F)                                                            # pale loral spot
            + P("M134,78 L208,92 L136,104 Z", N)                                          # long straight bill
            + eye(114, 82, B))


@bird("wild-turkey", "Wild Turkey", "valley")
def _(s):
    body = ("M0,240 L0,196 C10,168 40,150 74,146 C80,136 92,134 100,142 C106,132 120,132 126,142 "
            "C132,134 146,136 150,148 C180,158 200,196 208,240 Z")
    return (P("M100,160 C110,124 126,98 136,74 L162,80 C150,106 142,132 140,160 Z", B)  # bare neck
            + E(150, 62, 20, 17, B)
            + P("M166,56 L186,64 L166,72 Z", N)
            + P("M146,76 C162,78 170,96 162,118 C150,110 142,94 144,78 Z", R)  # wattle
            + C(128, 120, 6, R) + C(122, 136, 6, R)  # caruncles
            + P("M158,48 C170,42 178,50 176,62 C182,74 184,90 178,100 C172,94 168,78 164,66 Z", R)  # snood
            + P(body, N)
            + eye(150, 58, B, 9))


# ======================= 5. Appalachian Plateau =======================

@bird("hooded-warbler", "Hooded Warbler", "plateau")
def _(s):
    head = circ(106, 92, 38)
    body = "M0,240 L0,150 C20,128 48,118 76,114 L136,116 C146,152 152,200 156,240 Z"
    sil = head + " " + body
    return (P(body, M) + P(head, N)
            + inside(s, "bib", sil, P("M240,110 L104,110 L118,150 L240,150 Z", N))
            + inside(s, "breast", sil, P("M240,150 L120,150 C108,180 104,210 102,240 L240,240 Z", Y))
            + inside(s, "face", head, E(132, 86, 26, 22, Y))
            + P("M140,84 L170,90 L140,96 Z", N)
            + eye(126, 84, Y))


@bird("blackburnian-warbler", "Blackburnian Warbler", "plateau")
def _(s):
    head = circ(104, 92, 36)
    body = "M0,240 L0,150 C20,128 48,118 76,114 L134,116 C144,152 152,200 156,240 Z"
    sil = head + " " + body
    return (P(body, N) + P(head, N)
            + inside(s, "brow", head, P("M140,72 L84,68 L68,100 L80,102 L90,80 L140,82 Z", R))   # angular eyebrow
            + inside(s, "throat", sil, P("M240,98 L136,98 L104,134 L104,240 L240,240 Z", R))      # flame throat
            + inside(s, "crown", head, P("M102,54 l8,8 l-8,8 l-8,-8 Z", R))
            + P("M22,166 h40 v26 h-40 Z", F)                                                      # white wing patch
            + P("M136,88 L168,93 L136,98 Z", N)
            + eye(116, 90, N, 8))


@bird("black-and-white-warbler", "Black-and-white Warbler", "plateau")
def _(s):
    head = circ(104, 92, 36)
    body = "M0,240 L0,150 C20,128 48,118 76,114 L134,116 C144,152 152,200 156,240 Z"
    sil = head + " " + body
    stripes = (P("M60,62 L150,60 L150,67 L60,69 Z", F)        # median crown stripe
               + P("M78,76 L150,74 L150,81 L78,83 Z", F)       # eyebrow
               + P("M84,96 L150,96 L150,104 L90,106 Z", F)     # cheek
               + P("M240,124 L124,124 C112,160 106,200 104,240 L240,240 Z", F)  # breast
               + P("M10,170 L70,154 L72,161 L12,177 Z", F) + P("M12,194 L80,176 L82,183 L14,201 Z", F))  # back stripes
    return (P(body, N) + P(head, N)
            + pale(s, "stripes", sil, stripes, key=4)
            + inside(s, "streaks", sil, P("M120,150 h40 v6 h-40 Z", N) + P("M114,172 h50 v6 h-50 Z", N) + P("M110,196 h56 v6 h-56 Z", N))
            + P("M136,86 C150,86 162,90 172,96 C160,98 148,98 136,98 Z", M)                       # slender bill
            + eye(116, 88, N, 7))


@bird("swainsons-warbler", "Swainson’s Warbler", "plateau")
def _(s):
    head = ell(100, 96, 42, 30)
    body = "M0,240 L0,150 C20,132 48,124 72,122 L132,118 C142,156 150,200 154,240 Z"
    sil = head + " " + body
    return (P(body, M) + P(head, M)
            + inside(s, "crown", head, P("M40,40 L160,40 L160,80 L40,84 Z", R))                 # rufous crown
            + pale(s, "brow", head, "M84,82 L150,80 L150,88 L84,90 Z", line=M, key=3)           # strong pale eyebrow
            + inside(s, "line", head, P("M80,94 L150,94 L150,100 L80,102 Z", N))
            + pale(s, "breast", sil, "M240,124 L128,124 C116,160 110,200 108,240 L240,240 Z", line=M)
            + P("M136,86 L190,96 L136,104 Z", N)                                                 # long pointed bill
            + eye(116, 97, N, 7))


@bird("ruffed-grouse", "Ruffed Grouse", "plateau")
def _(s):
    body = "M0,240 L0,128 C30,108 70,108 100,118 C140,130 170,170 180,240 Z"
    head = circ(122, 92, 26)
    return (P(body, M) + P(head, M)
            + P("M100,84 C98,70 106,60 118,62 L106,52 C122,50 136,58 140,72 Z", M)       # small peaked crest
            + P("M80,112 C94,104 112,110 120,122 C116,142 100,152 82,150 C76,138 76,124 80,112 Z", N)  # dark neck ruff
            + P("M126,74 C132,68 142,68 148,74 L144,78 C140,74 132,74 128,78 Z", R)       # eye comb
            + P("M120,170 h40 v7 h-40 Z", N) + P("M116,190 h50 v7 h-50 Z", N) + P("M114,210 h56 v7 h-56 Z", N)
            + P("M144,86 L160,92 L144,98 Z", N)
            + eye(134, 86, M, 8))


# ======================= 6. RVA / Fall Line =======================

@bird("great-blue-heron", "Great Blue Heron", "rva")
def _(s):
    return (P("M0,240 L0,166 C22,150 56,150 78,164 L118,240 Z", B)
            + P("M62,178 L124,138 L96,90 L126,84 L150,140 L88,198 Z", B)
            + P("M18,170 L58,156 L66,176 L26,190 Z", N)                                   # black shoulder
            + E(112, 72, 22, 19, B)
            + P("M128,64 L208,74 L130,80 Z", Y)
            + P("M98,56 C110,52 124,54 132,60 L126,64 C110,62 92,68 76,80 L54,94 L72,74 C80,66 88,60 98,56 Z", N)
            + eye(120, 70, B, 8))


@bird("osprey", "Osprey", "rva")
def _(s):
    head = circ(102, 88, 38)
    body = "M0,240 L0,146 C20,126 48,118 72,116 L136,114 C146,152 152,200 156,240 Z"
    sil = head + " " + body
    crown = "M240,0 L0,0 L0,78 L70,84 L124,78 L240,78 Z"
    throat = "M240,96 L124,96 L98,110 L88,126 L104,240 L240,240 Z"
    return (P(body, N) + P(head, N) + inside(s, "wing", sil, E(26, 210, 54, 30, Y, -30))
            + pale(s, "crown", sil, crown + " " + throat)
            + P("M136,78 C152,76 166,86 168,102 C168,110 164,116 160,120 C158,108 152,100 138,98 Z", N)  # hooked bill
            + eye(118, 87, ring=Y))


@bird("double-crested-cormorant", "Double-crested Cormorant", "rva")
def _(s):
    body = ("M0,240 L0,178 C20,160 50,156 72,166 C86,130 96,100 104,80 L130,74 "
            "C124,120 118,170 132,240 Z")
    return (P(body, N)
            + E(118, 62, 24, 18, N)
            + P("M104,46 L100,34 L112,44 Z", N) + P("M118,44 L118,32 L126,44 Z", N)      # the two crests
            + P("M126,66 L152,72 L134,88 L118,82 Z", Y)                                  # orange throat patch
            + P("M136,56 L196,64 C204,66 206,72 200,78 L196,72 L136,68 Z", N)           # slender hooked bill
            + eye(122, 58, ring=B, r=8))


@bird("wood-duck", "Wood Duck", "rva")
def _(s):
    head = ("M142,76 C138,62 126,52 108,52 C84,52 56,58 44,78 C38,88 36,100 32,114 C46,106 62,104 80,106 "
            "C82,114 86,120 92,124 C110,128 132,120 144,100 Z")
    body = "M0,240 L0,168 C30,148 70,140 100,140 L142,128 C150,168 156,206 160,240 Z"
    return (P(body, N)
            + inside(s, "breast", body, P("M240,120 L118,128 C108,160 104,200 104,240 L240,240 Z", R))
            + P("M98,150 h10 v60 h-10 Z", F)                                                # white shoulder bar
            + P(head, B)
            + P("M138,80 C132,70 122,64 106,64 C84,64 62,70 54,86 C50,94 48,100 46,106 L54,104 "
                "C56,98 58,92 62,88 C72,76 88,72 106,72 C118,72 128,76 134,86 Z", F)      # stripe: bill, over the eye, to the crest tip
            + P("M112,92 C96,92 80,96 66,104 L74,106 C86,100 98,98 114,98 Z", F)          # stripe behind the eye
            + P("M138,104 C130,112 118,116 104,118 L112,108 L120,110 C126,108 132,106 138,104 Z", F)  # chin strap and finger
            + P("M142,78 L174,88 L172,96 L144,100 Z", R)
            + eye(124, 86, ring=R, r=8))


@bird("chimney-swift", "Chimney Swift", "rva", bleed=set())
def _(s):
    return (P("M138,110 C140,70 104,40 42,34 C82,56 102,86 112,114 Z", Y)        # far wing
            + P("M70,118 C100,108 140,104 168,108 C180,110 188,116 186,122 C182,130 150,136 120,136 "
                "C100,136 84,134 70,130 L52,132 L58,124 L50,116 Z", N)             # body, spiny tail
            + P("M186,118 L196,121 L186,124 Z", N)
            + P("M146,122 C150,166 114,200 52,210 C92,186 108,156 112,128 Z", N)   # near wing
            + eye(172, 116, N, 6))
