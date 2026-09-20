"""Ethereal Violet Theme - logo generator.

Two modes:

    python3 scripts/generate-logo.py              # final icon (default)
    python3 scripts/generate-logo.py candidates   # exploration sheet

The final mode renders the chosen concept (`CHOSEN`, currently the crystal mark)
on the deep plum card and writes the single 128px icon a Chrome theme needs:
logo/logo128.png.

The candidates mode draws every flat-vector concept at 8x supersampling in two
colorways (deep plum card + pale lilac card) plus a contact sheet, into
store-assets/icon-candidates/.
"""

import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

SS = 8                      # supersample factor
SIZE = 128                  # Chrome themes only need 128
S = SIZE * SS
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "store-assets" / "icon-candidates"

# --- palette sampled from manifest.json (theme.colors) -----------------------
DEEP = (59, 42, 70)         # frame             #3B2A46
DEEPER = (44, 31, 54)       # omnibox_background #2C1F36
PALE = (233, 220, 243)      # toolbar_button_icon #E3D3EC
ORCHID = (199, 155, 224)    # ntp_link          #C79BE0
SNOW = (246, 236, 250)      # tab_text          #F6ECFA

PLUM = (92, 71, 103)        # button_background #5C4767
ORCHID_D = (146, 104, 184)
LILAC_D = (178, 150, 202)
CARD_LIGHT = (243, 236, 249)

DARK_CW = {"card": DEEP, "mark": PALE, "accent": ORCHID, "hilite": SNOW}
LIGHT_CW = {"card": CARD_LIGHT, "mark": PLUM, "accent": ORCHID_D, "hilite": LILAC_D}

CARD_RADIUS = 0.22          # corner radius as a fraction of the icon size


# --- mask helpers ------------------------------------------------------------
def _blank():
    return Image.new("L", (S, S), 0)


def m_circle(cx, cy, r):
    m = _blank()
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    return m


def m_capsule(p0, p1, width):
    """Straight line with rounded ends (no sharp corners)."""
    m = _blank()
    d = ImageDraw.Draw(m)
    d.line([p0, p1], fill=255, width=int(round(width)))
    r = width / 2
    for x, y in (p0, p1):
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return m


def m_ellipse(cx, cy, rx, ry, angle=0.0):
    m = _blank()
    ImageDraw.Draw(m).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    if angle:
        m = m.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
    return m


def m_lens(cx, cy, hw, hh, angle=0.0):
    """Pointed oval (long axis vertical) = intersection of two circles."""
    d = (hh * hh - hw * hw) / (2 * hw)
    r = hw + d
    m = ImageChops.darker(m_circle(cx - d, cy, r), m_circle(cx + d, cy, r))
    if angle:
        m = m.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
    return m


def m_poly(pts):
    m = _blank()
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m


def m_ring(cx, cy, r, w):
    return ImageChops.difference(m_circle(cx, cy, r + w / 2), m_circle(cx, cy, r - w / 2))


def m_star4(cx, cy, r, waist):
    """Four-point sparkle = union of a vertical and a horizontal lens."""
    v = m_lens(cx, cy, waist, r)
    h = v.rotate(90, resample=Image.BICUBIC, center=(cx, cy))
    return ImageChops.lighter(v, h)


def m_ribbon(y0, amp, x0, x1, w_mid, phase=0.0):
    """Soft S-curve stroke, thick in the middle and tapered to nothing at both ends."""
    m = _blank()
    d = ImageDraw.Draw(m)
    n = 220
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = y0 + amp * math.sin(phase + t * math.pi * 1.35)
        w = w_mid * (0.14 + 0.86 * math.sin(math.pi * t) ** 0.75)
        r = max(w / 2, 1.0)
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return m


def union(*masks):
    out = masks[0]
    for m in masks[1:]:
        out = ImageChops.lighter(out, m)
    return out


def paint(layer, mask, rgb):
    layer.paste(Image.new("RGBA", (S, S), rgb + (255,)), (0, 0), mask)


# --- concepts ----------------------------------------------------------------
def c_moon(cw):
    """Crescent moon inside a thin halo ring, one sparkle in the hollow."""
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cx, cy = 0.500 * S, 0.500 * S
    paint(L, m_ring(cx, cy, 0.345 * S, 0.019 * S), cw["accent"])
    disc = m_circle(cx - 0.030 * S, cy, 0.245 * S)
    bite = m_circle(cx + 0.085 * S, cy, 0.235 * S)
    paint(L, ImageChops.subtract(disc, bite), cw["mark"])
    paint(L, m_star4(cx + 0.175 * S, cy - 0.105 * S, 0.078 * S, 0.015 * S), cw["hilite"])
    return L


def c_blossom(cw):
    """Five round petals around a small centre dot."""
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cx = cy = 0.5 * S
    petals = []
    for i in range(5):
        a = math.radians(-90 + 72 * i)
        petals.append(m_circle(cx + 0.175 * S * math.cos(a), cy + 0.175 * S * math.sin(a),
                               0.118 * S))
    paint(L, union(*petals), cw["mark"])
    paint(L, m_circle(cx, cy, 0.108 * S), cw["accent"])
    return L


def c_crystal(cw):
    """Faceted gem with a two-tone table and two sparkles."""
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    top = (0.50 * S, 0.15 * S)
    right = (0.79 * S, 0.50 * S)
    bottom = (0.50 * S, 0.85 * S)
    left = (0.21 * S, 0.50 * S)
    paint(L, m_poly([top, right, bottom, left]), cw["mark"])
    paint(L, m_poly([top, left, (0.50 * S, 0.50 * S)]), cw["accent"])
    paint(L, m_star4(0.775 * S, 0.285 * S, 0.070 * S, 0.014 * S), cw["hilite"])
    paint(L, m_star4(0.265 * S, 0.735 * S, 0.045 * S, 0.010 * S), cw["accent"])
    return L


def c_butterfly(cw):
    """Symmetric butterfly: two wing pairs, body, antennae."""
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cx, cy = 0.5 * S, 0.5 * S
    up = m_ellipse(0.655 * S, 0.355 * S, 0.185 * S, 0.145 * S, 30)
    lo = m_ellipse(0.610 * S, 0.615 * S, 0.135 * S, 0.105 * S, -28)
    half = union(up, lo)
    paint(L, union(half, ImageOps.mirror(half)), cw["mark"])

    spot = m_ellipse(0.660 * S, 0.345 * S, 0.068 * S, 0.050 * S, 30)
    paint(L, union(spot, ImageOps.mirror(spot)), cw["accent"])

    paint(L, m_capsule((cx, 0.335 * S), (cx, 0.700 * S), 0.052 * S), cw["accent"])
    ant = m_capsule((cx, 0.345 * S), (0.425 * S, 0.215 * S), 0.016 * S)
    paint(L, union(ant, ImageOps.mirror(ant)), cw["accent"])
    paint(L, union(m_circle(0.418 * S, 0.208 * S, 0.022 * S),
                   m_circle(0.582 * S, 0.208 * S, 0.022 * S)), cw["accent"])
    return L


def c_sparkle(cw):
    """One large four-point sparkle with two smaller companions."""
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    paint(L, m_star4(0.465 * S, 0.470 * S, 0.290 * S, 0.048 * S), cw["mark"])
    paint(L, m_star4(0.740 * S, 0.725 * S, 0.125 * S, 0.026 * S), cw["accent"])
    paint(L, m_star4(0.735 * S, 0.275 * S, 0.085 * S, 0.018 * S), cw["hilite"])
    return L


def c_mist(cw):
    """Three flowing ribbons, tapered at both ends, like drifting mist."""
    L = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    paint(L, m_ribbon(0.345 * S, 0.058 * S, 0.170 * S, 0.830 * S, 0.105 * S, 0.0), cw["mark"])
    paint(L, m_ribbon(0.505 * S, 0.062 * S, 0.215 * S, 0.785 * S, 0.090 * S, 0.55), cw["accent"])
    paint(L, m_ribbon(0.660 * S, 0.052 * S, 0.170 * S, 0.830 * S, 0.100 * S, 1.10), cw["mark"])
    return L


CONCEPTS = [
    ("01", "moon-halo", "Moon halo", "Moon Halo", c_moon),
    ("02", "blossom", "Blossom", "五瓣花", c_blossom),
    ("03", "crystal", "Crystal", "水晶", c_crystal),
    ("04", "butterfly", "Butterfly", "蝶", c_butterfly),
    ("05", "sparkle", "Sparkle", "星芒", c_sparkle),
    ("06", "mist", "Mist", "雾纱", c_mist),
]

CHOSEN = "crystal"          # user picked candidate 03 (deep plum card colorway)

# Boxes (in canvas fractions) that a mark must be centred on. The crystal gem is
# the visual mass of that mark, so it is centred on its own outline - centring on
# the drawn bounding box instead would drag it off-centre towards the sparkles.
GEM_BOX = (0.21, 0.15, 0.79, 0.85)
ANCHORS = {"crystal": GEM_BOX}


# --- composition -------------------------------------------------------------
def card(card_rgb):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    plate = _blank()
    ImageDraw.Draw(plate).rounded_rectangle([0, 0, S - 1, S - 1],
                                            radius=CARD_RADIUS * S, fill=255)
    img.paste(Image.new("RGBA", (S, S), card_rgb + (255,)), (0, 0), plate)
    return img


def compose(concept, cw, anchor=None):
    """Draw the mark on the card, centring it on `anchor` (canvas fractions) if given."""
    layer = concept(cw)
    if anchor is None:
        box = layer.split()[3].getbbox()
        assert box is not None, "nothing drawn"
    else:
        box = (anchor[0] * S, anchor[1] * S, anchor[2] * S, anchor[3] * S)
    centered = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    centered.alpha_composite(layer, (int(round(S / 2 - (box[0] + box[2]) / 2)),
                                     int(round(S / 2 - (box[1] + box[3]) / 2))))
    b = centered.split()[3].getbbox()
    margin = 0.14 * S
    assert b[0] >= margin and b[1] >= margin, f"mark too close to card edge: {b}"
    assert b[2] <= S - margin and b[3] <= S - margin, f"mark too close to card edge: {b}"
    out = card(cw["card"])
    out.alpha_composite(centered)
    return out


def load_font(size, bold=False):
    names = (("msyhbd.ttc", "segoeuib.ttf", "arialbd.ttf") if bold
             else ("msyh.ttc", "segoeui.ttf", "arial.ttf"))
    for name in names:
        p = Path("C:/Windows/Fonts") / name
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def contact_sheet(rows):
    """3 x 2 comparison sheet: each tile shows the dark card + the light card."""
    W, H = 1280, 800
    MARGIN, GAP = 60, 40
    HEADER = 110
    TILE_W = (W - 2 * MARGIN - 2 * GAP) // 3
    TILE_H = (H - HEADER - GAP - MARGIN) // 2
    sheet = Image.new("RGB", (W, H), DEEPER)
    d = ImageDraw.Draw(sheet)
    f_head = load_font(30, bold=True)
    f_sub = load_font(15)
    f_name = load_font(23, bold=True)
    f_cn = load_font(19)
    f_note = load_font(13)

    d.text((MARGIN, 34), "Ethereal Violet — Logo Candidates", font=f_head, fill=SNOW)
    d.text((MARGIN, 74), "left: deep plum card   ·   right: pale lilac card",
           font=f_sub, fill=ORCHID)

    for i, (num, _slug, en, cn, dark, light) in enumerate(rows):
        col, row = i % 3, i // 3
        x = MARGIN + col * (TILE_W + GAP)
        y = HEADER + row * (TILE_H + GAP)
        d.rounded_rectangle([x, y, x + TILE_W, y + TILE_H], radius=22, fill=DEEP)
        d.text((x + 24, y + 20), f"{num}", font=f_name, fill=ORCHID)
        d.text((x + 66, y + 20), f"{en}  {cn}", font=f_name, fill=SNOW)

        big = dark.resize((178, 178), Image.LANCZOS)
        small = light.resize((96, 96), Image.LANCZOS)
        sheet.paste(big, (x + 26, y + 74), big)
        sheet.paste(small, (x + 230, y + 115), small)
        d.text((x + 26, y + TILE_H - 26), "dark 128 preview / light 128 preview",
               font=f_note, fill=ORCHID)

    sheet.save(OUT / "contact-sheet.png")
    print(f"wrote {OUT / 'contact-sheet.png'}")


def write_candidates():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for num, slug, en, cn, concept in CONCEPTS:
        anchor = ANCHORS.get(slug)
        dark = compose(concept, DARK_CW, anchor)
        light = compose(concept, LIGHT_CW, anchor)
        dark.resize((512, 512), Image.LANCZOS).save(OUT / f"candidate-{num}-{slug}.png")
        light.resize((512, 512), Image.LANCZOS).save(
            OUT / f"candidate-{num}-{slug}-light.png")
        rows.append((num, slug, en, cn, dark, light))
        print(f"wrote candidate-{num}-{slug} (dark + light)")
    contact_sheet(rows)


def write_final():
    """The chosen mark on the deep plum card, as the only size a theme needs: 128."""
    concept = next(c for _num, slug, _en, _cn, c in CONCEPTS if slug == CHOSEN)
    dest = ROOT / "logo"
    dest.mkdir(parents=True, exist_ok=True)
    icon = compose(concept, DARK_CW, ANCHORS.get(CHOSEN)).resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(dest / "logo128.png")
    print(f"wrote logo/logo128.png ({SIZE}x{SIZE}) - concept '{CHOSEN}', deep plum card")
    assert icon.size == (SIZE, SIZE)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "final"
    if mode == "candidates":
        write_candidates()
    elif mode == "final":
        write_final()
    else:
        raise SystemExit(f"unknown mode '{mode}' - use 'final' or 'candidates'")


if __name__ == "__main__":
    main()
