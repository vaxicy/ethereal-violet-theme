# Asset notes

## What the assets are

- `screenshots/en/screenshot-1-browser.png` (1280x800) and `screenshot-2-introduction.png` (1280x800)
- `promo/440x280.png` and `promo/1400x560.png`

All four are rendered by `scripts/generate-store-assets.py` with headless Chromium from HTML/CSS. They are illustrative layouts built from the real `manifest.json` colors, not native screenshots of a running Chrome window.

## Colors

Theme-controlled surfaces (frame, toolbar, active tab, bookmark bar, address bar, new tab page, text, links) are read from `manifest.json` at render time.

Browser-owned elements are literals, because Chrome decides them:

| Element | Value | Note |
|---|---|---|
| Google mark on the new tab page | `#BC8BE4` | `ntp_logo_alternate` makes Chrome paint the mark in a single tint derived from the new tab background; the value here is a light orchid matching this plum background and should be confirmed against a real install |
| Search placeholder and address-bar glyphs | `#9AA0A6` | Chrome's standard dark-surface tone |
| New tab shortcut circles | `#2F3033` | Rendered by the page, not the theme |
| `Customize Chrome` pill | `#202124` / `#E8EAED` | Rendered by the page, not the theme |

## Regenerating

    python3 scripts/generate-logo.py              # logo/logo128.png (crystal mark)
    python3 scripts/generate-logo.py candidates   # exploration sheet
    python3 scripts/generate-store-assets.py      # screenshots + promo tiles

The composer renders all four assets in one pass; change the styling in the script and re-run instead of editing a PNG.
