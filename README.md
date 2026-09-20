<div align="center">
  <img src="https://raw.githubusercontent.com/vaxicy/ethereal-violet-theme/main/logo/logo128.png" alt="Ethereal Violet Theme icon" width="88">
  <h1>Ethereal Violet Theme</h1>
  <p>A deep plum Chrome theme with soft lilac surfaces and a quiet orchid glow.</p>
  <p>
    <img src="https://img.shields.io/badge/version-1.0.0-C79BE0" alt="Version 1.0.0">
    <img src="https://img.shields.io/badge/license-Non--Commercial-lightgrey" alt="Non-Commercial License">
    <img src="https://img.shields.io/badge/Chrome%20Web%20Store-theme-BC8BE4?logo=googlechrome" alt="Chrome Web Store">
  </p>
</div>

---

## About

Ethereal Violet Theme gives the browser a quiet evening mood. A deep plum frame carries the window and tab strip, a slightly lighter plum toolbar and bookmark bar sit just below it, and the new-tab page opens on midnight violet with soft lilac text. A light orchid runs through links, headers and the store artwork as the single accent colour.

Every layer is painted as one flat solid colour, so the window stays calm and uncluttered, and the text colours are tuned so tab titles, toolbar icons, bookmarks and the address bar stay readable against the dark surfaces.

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Deep Plum | `#3B2A46` | Window frame, tab strip, window buttons |
| Twilight Plum | `#4A3854` | Toolbar, bookmark bar, active tab |
| Orchid Lift | `#5C4767` | Button surfaces |
| Midnight Violet | `#22182A` | New-tab page background |
| Midnight Ink | `#2C1F36` | Address bar background |
| Soft Lilac | `#E3D3EC` | Toolbar icons, primary text |
| Soft Orchid | `#C79BE0` | Links, new-tab headers, accent |

## Chrome UI Notes

Some parts of the browser are painted by Chrome itself rather than by the theme manifest. The store artwork follows what Chrome renders after installing this theme:

- **Google mark on the new-tab page:** Chrome draws it as one flat colour derived from the new-tab background. Against this midnight violet surface it reads as a light orchid, close to `#BC8BE4`.
- **Shortcut tiles:** the round new-tab shortcuts are rendered by the page, so they stay a neutral dark grey.
- **Window buttons:** Chrome keeps the minimize / maximize / close glyphs in the light tab-text tone against the plum frame.
- **Address bar:** the omnibox keeps its own darker plum surface, so it stands slightly apart from the toolbar.

## Features

| Feature | Detail |
|---------|--------|
| 🌌 Violet dusk palette | Deep plum frame with a midnight violet reading surface |
| 🟣 Flat colour layers | Each surface is one solid colour |
| 👓 Tuned contrast | Tab, toolbar, bookmark and address-bar text stays readable |
| 🕶️ Incognito styling | An even deeper plum frame keeps private windows distinct |
| 🪶 Pure theme package | A manifest and an icon |

## Install

### From source (unpacked)

1. Download or clone this repository.
2. Open Chrome and navigate to `chrome://extensions`.
3. Enable **Developer mode** in the top-right corner.
4. Click **Load unpacked** and select this folder.

### From Chrome Web Store

Search for **Ethereal Violet Theme** in the Chrome Web Store and install it.

## Preview

![Ethereal Violet Theme browser preview](https://raw.githubusercontent.com/vaxicy/ethereal-violet-theme/main/store-assets/screenshots/en/screenshot-1-browser.png)

![Ethereal Violet Theme color palette](https://raw.githubusercontent.com/vaxicy/ethereal-violet-theme/main/store-assets/screenshots/en/screenshot-2-introduction.png)

## Files

| File | Description |
|------|-------------|
| `manifest.json` | Chrome theme manifest (MV3) with inline `theme` config |
| `logo/logo128.png` | Theme icon (128x128) |
| `store-assets/screenshots/en/` | Store listing screenshots (1280x800) |
| `store-assets/promo/` | Promo tiles (440x280 and 1400x560) |
| `store-assets/store-description.txt` | Store listing description (English) |
| `store-assets/ASSET-NOTES.md` | How the store artwork is composed and calibrated |
| `scripts/generate-logo.py` | Draws the icon (and the exploration sheet of logo concepts) |
| `scripts/generate-store-assets.py` | Renders every store asset from one HTML/CSS source |

## License

Non-Commercial License — personal use permitted.

- ✅ Personal use, modification for personal use, sharing with attribution.
- ❌ Commercial use without permission.

Commercial licensing: contact the author.
