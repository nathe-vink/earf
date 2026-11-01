# Where the site states or shows a tint's look (2026-11-01)

The owner, 2026-11-01 (r46-owner-notes 8832050e): "I like the darker colors." The line takes stock sheet's deeper
tints for all eight (r33-speaker-horn `asset/TINTS.md`: Ember 2423, Dust 2422, Acid 9097, Poison 2092, Ice 2069,
Haze 2287, Fog 0000, Smoke 2074). The site's new picture set will be rendered in them. **Nothing below has been
changed yet**: this is the list to work from when the set lands. Line numbers are `web.py` on `r47-site-next` at the
commit that adds this file.

## 1. Color values (hex and RGB) the page draws itself

| What | Where | Values today | Needs |
|---|---|---|---|
| The eight swatch colors (`MARK`, from `marks.M.SPEAKERS`, line `Cloud`) | `web.py` 193 (`MARK`); used as each color's `col` in the page data (898), the debut's tint bar (2915), and each `/s/` page's `theme-color` (3086) | Ember #D2382F, Dust #E5732A, Acid #E9B320, Poison #4F7F3A, Ice #4A90C8, Haze #6C4BA3, Fog #F6F8F8, Smoke #34323A | new values sampled from the new set (or from the chips), set in `marks.py`, the brand's source, not here |
| The color wheel's six hues (`E.HUES`) | `web.py` 901 (page data `hues`), from `earth.py` | the six above, Ember to Haze | as above (the brand lane owns `earth.py`) |
| "Lit from below": each color's light on the wall, and how bright its photograph is (`glow`) | `web.py` 756 | sampled from the uplight renders: e.g. Poison 136 234 131 at 0.57, Smoke 146 181 235 at 0.28 | sample again from the new uplight renders |
| Each card's panel color (where the photograph meets the card) | `image_meta()` (`panel[k]`), sampled from `<k>-on.jpg` | computed at build | recomputes itself from the new pictures |
| Each picture's ground (the colors the stage carries past its edges) | `ground()`, sampled from each picture | computed at build | recomputes itself |
| The 3D view's tints (off) | `view3d()` 1196, from `studio/products/barkhorn-cloud.json` flavours | the engine's `deep`/`horn_deep` | follows the engine file, if the 3D view is ever turned on |

## 2. Pictures that carry the tints (made from renders; replaced by the new set)

- **Coin sprites**: `img/coins-light.jpg`, `img/coins-dark.jpg` (every swatch, color picker, color dot and coin on the
  site); made from the acrylic coin renders (r46/coins, via `--sources`).
- **Icons**: `img/icon-<name>-light.webp` (each color's pictogram in its acrylic), from `icons_real.py`.
- **Every product picture** in the eight colors: Tropos (`<k>-on/off/studio/studio-light/back/amp/horn-*/inside/reel/
  habitat`, the hero, the facade, the room, `turn-<k>.jpg`, the `spin/` frames), Hemisphere and Core (`dome-<k>`,
  `orb-<k>`, the rows), Mantle (`tt-<k>-*`), and their WebP copies, thumbnails and `og/` preview cards (these three
  rebuild themselves from the pictures).
- **The press kit** (`press/earf-press-kit.pdf`, printed from the page) and **the what-changes sheet**
  (`launch/r47-what-changes.pdf`): rebuild after the pictures.

## 3. Words that describe a tint's look

Today's words, and a note where the darker stock tint may no longer fit (to check against the chips and renders):

| Color | The acrylic (`CLOUDS`, 113-120: cards, particulars, press) | Its line (`CLOUDS`) | Its cover | Check |
|---|---|---|---|---|
| Ember | Translucent red | The last light of the fire. | Oxblood | fits a deeper red |
| Dust | Translucent orange | A long, dry afternoon. | Rust | fits |
| Acid | Translucent golden yellow | A yellow with an edge. | Ochre | check against 9097's yellow |
| Poison | Translucent bottle green | Bottle green. Keep out of reach. | Bottle green | fits a deeper green |
| Ice | Translucent ice blue | Glacier blue, and in no hurry. | Deep blue | "ice blue" may read light for 2069 |
| Haze | Translucent violet | Dusk, kept indoors. | Deep violet | fits |
| Fog | Water-clear | Water-clear. Almost not there. | White | 0000 is clear: fits |
| Smoke | Smoked black | Smoked glass, for after dark. | Black | 2074 is a mid smoke through the horn (TINTS.md, R1): "Smoked black" may read too dark; "Smoked gray"? |

Other sentences that describe a tint's look:
- Home hero alt (2087): "red through violet, then **the clear Fog and the smoked Smoke**, each throwing its color on
  the floor".
- Journal, "Eight colors, all the way through" (998, 1011): "Fog is water-clear, almost not there; Smoke is smoked
  glass, for after dark"; "Fog and Smoke … the same acrylic, light and dark".
- The colors' company (2655, 2660): "Clear and smoked: the same acrylic, light and dark."; "{Fog/Smoke} has no hue of
  its own, so it pairs by lightness with …".
- Lamps, the pair switched off (176, 2431, 2435): "A Core and a Hemisphere in Smoke, switched off: dark, polished
  acrylic, **pale at the center**".
- The stacked-horn post (dark; 1231-1232): "A Smoke horn … dark acrylic between the bright edges of its terraces";
  "Smoke: dark between the bright edges of its layers." (rendered in 2074 already).
- Mantle (863, 865): "a violet plinth floating on clear posts over a violet base" (Haze).
- Studio captions (981, 2417): "on a pale ground" (the studio's ground, not a tint: no change).
- Planet EARF post (1046): "The acrylic stays clear, frosted or smoked" (the bar's own acrylic: no change).

## 4. Not tint statements (listed so they are not chased)

"Lit from below", "light" in the studio's name (`studio-light`), the page's one light theme, the night intro's
"glowing edges", and Hemisphere's or Mantle's base "glowing" (the light, not the tint).
