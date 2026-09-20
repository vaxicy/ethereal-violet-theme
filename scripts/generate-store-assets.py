"""Render the four Chrome Web Store assets for Ethereal Violet Theme.

    python3 scripts/generate-store-assets.py

Produces, from one HTML/CSS composer (headless Chromium, scale factor 1):

    store-assets/screenshots/en/screenshot-1-browser.png      1280x800
    store-assets/screenshots/en/screenshot-2-introduction.png 1280x800
    store-assets/promo/440x280.png                            440x280
    store-assets/promo/1400x560.png                           1400x560

Surface colors come from manifest.json's theme.colors. Colors of browser-owned
UI (search placeholder, shortcut circles, Customize pill, Google mark tone) are
literals - see LOGO_TINT and ASSET-NOTES.md.
"""

import base64
import json
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "store-assets" / "references"
REF.mkdir(parents=True, exist_ok=True)

C = json.loads((ROOT / "manifest.json").read_text("utf-8-sig"))["theme"]["colors"]

# Browser-owned tones (not theme colors): see ASSET-NOTES.md.
LOGO_TINT = "#BC8BE4"      # ntp_logo_alternate tint Chrome computes on this NTP
SEARCH_TEXT = "#9AA0A6"    # search placeholder + address-bar glyphs
SHORTCUT_BG = "#2F3033"    # new-tab shortcut circles
CUSTOMIZE_BG = "#202124"   # "Customize Chrome" pill
CUSTOMIZE_TEXT = "#E8EAED"


def color(key):
    return "#%02X%02X%02X" % tuple(C[key])


# Palette-sheet background: a theme tone that is NOT used as a swatch card, so no
# card can blend into the page behind it.
INTRO_BG = color("tab_text")

css = f"""
:root{{
  --frame:{color('frame')};--toolbar:{color('toolbar')};--ob:{color('omnibox_background')};
  --obt:{color('omnibox_text')};--tt:{color('tab_text')};--tbt:{color('tab_background_text')};
  --tbi:{color('toolbar_button_icon')};--bm:{color('bookmark_text')};
  --ntp:{color('ntp_background')};--nt:{color('ntp_text')};--nl:{color('ntp_link')};
  --edge:{color('button_background')};--sheet:{INTRO_BG};--ink:{color('frame')};
}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:Arial,Helvetica,sans-serif;background:var(--ntp)}}

/* ---- screenshot 1: full window mockup, layer by layer like real Chrome ---- */
.browser{{width:1280px;height:800px;background:var(--ntp);position:relative;overflow:hidden}}
.tabs{{height:44px;background:var(--frame);display:flex;align-items:end;gap:10px;
      padding:6px 12px 0;color:var(--tbt)}}
.tab{{height:37px;width:235px;padding:12px 18px;font-size:13px;border-radius:12px 12px 0 0}}
.tab.active{{background:var(--toolbar);color:var(--tt)}}
.close{{float:right}}
.wc{{margin-left:auto;padding:10px 12px;letter-spacing:22px;color:var(--tt)}}
.tools{{height:56px;background:var(--toolbar);display:flex;align-items:center;padding:0 20px;
       gap:24px;font-size:20px;color:var(--tbi)}}
.omni{{flex:1;height:36px;border-radius:22px;background:var(--ob);color:var(--obt);font-size:13px;
      display:flex;align-items:center;padding:0 18px}}
.bookmarks{{height:32px;background:var(--toolbar);color:var(--bm);font-size:12px;
           display:flex;gap:30px;padding:8px 22px}}
.content{{text-align:center;padding-top:96px;color:var(--nt)}}
.google{{font-size:80px;line-height:1.18;letter-spacing:-4px;font-weight:500;color:{LOGO_TINT};
        margin-bottom:44px}}
.search{{width:630px;height:48px;border-radius:28px;background:var(--ob);
        border:1px solid var(--frame);margin:auto;display:flex;align-items:center;gap:16px;
        padding:0 20px;color:{SEARCH_TEXT};font-size:16px}}
.shortcuts{{display:flex;justify-content:center;gap:40px;margin-top:34px}}
.shortcut{{width:86px;font-size:12px;text-align:center;color:var(--nt)}}
.shortcut .circle{{width:48px;height:48px;border-radius:50%;background:{SHORTCUT_BG};
                  margin:0 auto 10px;display:flex;align-items:center;justify-content:center;line-height:0}}
.customize{{position:absolute;right:22px;bottom:16px;background:{CUSTOMIZE_BG};
           color:{CUSTOMIZE_TEXT};font-size:12px;border-radius:16px;padding:8px 14px;
           display:flex;align-items:center;gap:6px}}

/* ---- screenshot 2: theme introduction + palette ----
   The palette sheet sits on tab_text, a light tone that no swatch uses, so no
   card can blend into the page behind it. */
.intro{{width:1280px;height:800px;padding:65px 72px;background:var(--sheet);color:var(--ink)}}
.kicker{{font-size:13px;letter-spacing:3px;color:var(--edge)}}
.intro h1{{font:54px Georgia,serif;margin:20px 0}}
.intro p{{font-size:21px;margin:0}}
.cards{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:35px}}
.card{{height:210px;border-radius:18px;padding:30px;border:1px solid var(--frame);
      display:flex;flex-direction:column;justify-content:end}}
.card strong{{font-size:28px}}
.card span{{font-size:17px;margin-top:12px}}
.intro p.chips{{font-size:16px;margin:44px 0 0;color:var(--edge)}}

/* ---- promo tiles ---- */
.promo{{position:relative;overflow:hidden}}
.small{{width:440px;height:280px;background:var(--ntp);text-align:center;color:var(--nt);padding-top:16px}}
.small img{{width:78px;height:78px;display:block;margin:0 auto 6px}}
.small h1{{font:38px Georgia,serif;font-weight:normal;margin:0}}
.small .sub{{font-size:15px;letter-spacing:4px;margin-top:8px;color:var(--nl)}}
.small p{{font-size:13px;margin:18px 0 0;color:var(--tbt)}}
.small:after{{content:'';position:absolute;left:0;right:0;bottom:0;height:14px;background:var(--nl)}}
.poster{{width:1400px;height:560px;background:var(--toolbar);position:relative;
        text-align:center;border-top:8px solid var(--nl)}}
.poster h1{{font:48px Georgia,serif;font-weight:normal;margin:23px 0 7px;color:var(--tt)}}
.poster p{{font-size:17px;margin:0;color:var(--nl)}}
.poster .preview{{position:absolute;left:284px;top:145px;transform:scale(.65);transform-origin:top left;
                 border:2px solid var(--nl);border-radius:16px;overflow:hidden;text-align:left}}
.poster .browser{{height:610px}}
.poster .content{{padding-top:85px}}
"""


def icon(kind):
    """New-tab shortcut glyphs (browser-owned, so drawn in a neutral tone)."""
    g = CUSTOMIZE_TEXT
    if kind == "play":
        return f'<svg width="18" height="18" viewBox="0 0 24 24"><path d="M8 5l11 7-11 7z" fill="{g}"/></svg>'
    if kind == "globe":
        return (f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{g}" stroke-width="2">'
                '<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c2.6 3.4 2.6 12.6 0 16'
                'M12 4c-2.6 3.4-2.6 12.6 0 16"/></svg>')
    return (f'<svg width="18" height="18" viewBox="0 0 24 24" stroke="{g}" stroke-width="2.4" '
            'stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>')


def search_box():
    s = SEARCH_TEXT
    return ('<div class="search">'
            f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{s}" stroke-width="2.4">'
            '<circle cx="10" cy="10" r="6"/><path d="M15 15l6 6"/></svg>'
            '<span>Search Google or type a URL</span>'
            f'<svg style="margin-left:auto" width="16" height="18" viewBox="0 0 24 24" fill="{s}">'
            '<path d="M12 14a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v5a3 3 0 0 0 3 3zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.9V21h2v-3.1A7 7 0 0 0 19 11z"/></svg>'
            f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{s}" stroke-width="2">'
            '<rect x="4" y="5" width="16" height="15" rx="4"/><circle cx="12" cy="12" r="3"/></svg>'
            '</div>')


def browser(with_bookmarks=False):
    bookmarks = ('<div class="bookmarks"><span>Bookmarks</span><span>Reading</span>'
                 '<span>Design</span><span>Inspiration</span></div>' if with_bookmarks else "")
    shortcuts = ('<div class="shortcuts">'
                 f'<div class="shortcut"><div class="circle">{icon("play")}</div>Videos</div>'
                 f'<div class="shortcut"><div class="circle">{icon("globe")}</div>Web</div>'
                 f'<div class="shortcut"><div class="circle">{icon("plus")}</div>Add shortcut</div>'
                 '</div>')
    customize = (f'<div class="customize"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" '
                 f'stroke="{CUSTOMIZE_TEXT}" stroke-width="2"><path d="M4 20l4-1 10-10-3-3L5 16z"/></svg>'
                 'Customize Chrome</div>')
    return ('<div class="browser"><div class="tabs">'
            '<div class="tab active">New Tab <span class="close">&#215;</span></div>'
            '<div class="tab">Reading list <span class="close">&#215;</span></div>'
            '<span style="padding:10px">+</span>'
            '<span class="wc">&#8722; &#9633; &#215;</span></div>'
            '<div class="tools"><span>&#8592;</span><span>&#8594;</span><span>&#8635;</span>'
            f'{search_box()}<span>&#9733;</span><span>&#8942;</span></div>'
            f'{bookmarks}<div class="content"><div class="google">Google</div>'
            f'{search_box()}{shortcuts}</div>{customize}</div>')


def page(body):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<style>{css}</style></head><body>{body}</body></html>')


logo_uri = "data:image/png;base64," + base64.b64encode(
    (ROOT / "logo" / "logo128.png").read_bytes()).decode()

SMALL = ('<div class="promo small">'
         f'<img src="{logo_uri}" alt="">'
         '<h1>Ethereal Violet</h1><div class="sub">CHROME THEME</div>'
         '<p>Deep plum evenings, soft lilac light.</p></div>')

WIDE = ('<div class="promo poster"><h1>Ethereal Violet Theme</h1>'
        '<p>Deep plum, soft lilac, and a quiet orchid glow.</p>'
        f'<div class="preview">{browser(True)}</div></div>')

PALETTE = [
    ("Deep Plum", "frame", "Window frame & buttons", color("tab_text")),
    ("Twilight Plum", "toolbar", "Toolbar, active tab, bookmark bar", color("tab_text")),
    ("Midnight Violet", "ntp_background", "New tab background", color("ntp_text")),
    ("Soft Orchid", "ntp_link", "Links, headers, accent", color("frame")),
]
cards = "".join(
    f'<div class="card" style="background:{color(key)};color:{fg}">'
    f'<strong>{name}</strong><span>{color(key)} &#183; {role}</span></div>'
    for name, key, role, fg in PALETTE)

INTRO = ('<div class="intro"><div class="kicker">A VIOLET EVENING FOR THE NEW TAB</div>'
         '<h1>Ethereal Violet Theme</h1>'
         '<p>Deep plum, soft lilac, and a quiet orchid glow.</p>'
         f'<div class="cards">{cards}</div>'
         '<p class="chips">Solid colors &#183; Flat surfaces &#183; Quiet contrast</p></div>')

JOBS = [
    ("screenshot-1-browser", 1280, 800, browser(True), ROOT / "store-assets/screenshots/en"),
    ("screenshot-2-introduction", 1280, 800, INTRO, ROOT / "store-assets/screenshots/en"),
    ("promo-440x280", 440, 280, SMALL, ROOT / "store-assets/promo"),
    ("promo-1400x560", 1400, 560, WIDE, ROOT / "store-assets/promo"),
]


def main():
    # The palette sheet background must not be one of the swatches, or that card
    # blends into the page (see the "bg must differ from swatches" rule).
    swatches = {color(key) for _name, key, _role, _fg in PALETTE}
    assert INTRO_BG not in swatches, f"palette sheet bg {INTRO_BG} collides with a swatch"
    with sync_playwright() as p:
        engine = p.chromium.launch(headless=True)
        tab = engine.new_page(device_scale_factor=1)
        for name, w, h, body, out_dir in JOBS:
            html = page(body)
            (REF / f"{name}.html").write_text(html, "utf-8")
            tab.set_viewport_size({"width": w, "height": h})
            tab.set_content(html)
            shot = REF / f"{name}.png"
            tab.screenshot(path=str(shot))
            out_dir.mkdir(parents=True, exist_ok=True)
            target = out_dir / f"{name.removeprefix('promo-')}.png"
            with Image.open(shot) as img:
                assert img.size == (w, h), f"{name}: {img.size} != {(w, h)}"
                temp = target.with_suffix(".new.png")
                img.convert("RGB").save(temp)
            temp.replace(target)
            print(f"wrote {target.relative_to(ROOT)} {w}x{h}")
        engine.close()


if __name__ == "__main__":
    main()
