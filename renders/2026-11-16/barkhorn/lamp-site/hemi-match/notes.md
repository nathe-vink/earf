# Hemisphere matched to Core, switched off (2026-11-16, A2)

This is the other direction from Step A (`../core-match/`), so the owner can compare like with like. Core stays as built. Each Hemisphere gets a denser dye until its off color meets Core's.
- Seven tints. Smoke stays the approved pair (Hemisphere 1.2x, Core 0.6x). Fog is left as it is.
- Scratch cells only, made with the corrected method (lamp_site.py since 9a6a2913).
- Off cells: the one off rig, 128 spp.
- Lit cells: the rows' rig and exposure, 256 spp.
- Light out: launch/isphere.py, split above and below at the rim. Lux: the LUXPTS probe, with the table as a gray card.

`hemi-match-sheet.png` rows:
1. Core off as built.
2. Hemisphere off, matched.
3. Hemisphere lit, today | matched.

| Tint | Hemisphere dye (x the stock pour) | Core off | Hemisphere off, today > matched | Largest gap | Hemisphere lit glass, today > matched | Light out, today > matched (down share) | Lux at the center |
|---|---|---|---|---|---|---|---|
| Ember | 1 > **1.8** | 72, 0, 0 | 96, 14, 10 > 71, 13, 12 | 13 (green) | 255, 165, 157 > 253, 145, 136 | 334 > 307 lm (67 > 70 %) | 336 > 336 |
| Dust | 3 > **9** | 106, 16, 0 | 126, 37, 6 > 109, 15, 5 | 5 | 249, 185, 163 > 253, 149, 139 | 353 > 312 lm (65 > 69 %) | 347 > 345 |
| Acid | 3 > **5** | 81, 72, 0 | 100, 90, 10 > 83, 71, 8 | 8 (blue) | 227, 221, 178 > 222, 213, 163 | 419 > 380 lm (61 > 64 %) | 347 > 346 |
| Poison | 1 > **2.3** | 0, 15, 3 | 9, 38, 15 > 15, 17, 15 | 15 (red) | 15, 188, 87 > 0, 93, 40 | 282 > 251 lm (73 > 77 %) | 341 > 341 |
| Ice | 3 > **6** | 0, 36, 86 | 2, 55, 108 > 2, 34, 91 | 5 | 144, 195, 233 > 79, 153, 234 | 308 > 270 lm (70 > 74 %) | 345 > 345 |
| Haze | 1 > **1.8** | 7, 13, 74 | 35, 31, 94 > 15, 23, 73 | 10 (green) | 202, 150, 207 > 141, 95, 201 | 281 > 258 lm (73 > 76 %) | 343 > 343 |
| Smoke | the approved pair, 1.2x; lit in B-SMOKE | | | | | | |

## Where Hemisphere's floor stops the match

Hemisphere's glass faces reflect the room. That floor is about 13–15 in every channel when the lamp is off, however dense the dye. Core's ball takes a channel to 0; Hemisphere's cannot.
- **Poison:** 15, 17, 15 against Core's 0, 15, 3. More dye only darkens it toward a neutral near-black (green at 4x reads 15, 15, 15). Off, it stops looking green.
- **Ember:** Core's green and blue are 0. Hemisphere's stay at 13 and 12.
- **Haze:** Core's red is 7 and green 13. Hemisphere's stay at 15 and 23.
- **Dust, Acid, Ice:** match within 5–8.

## Lit

- **The center lux does not move** (within 2). The light the table gets comes straight out of the open bottom.
- **The glass darkens and deepens in proportion to the dye.** Poison and Haze lose the most: Poison's green goes 188 > 93, Haze's red 202 > 141. Ember, Dust and Acid change only a little.
- **Light out falls 8 to 12 %, almost all of it from the up-light through the shade.** The down share rises 3 to 4 points.

This is the opposite of Step A, where the matched Core glows paler and lighter. Here, the matched Hemisphere glows richer and darker.

## Audit and emitters

- Audit: Hemisphere off (dome-red at 1.8x) in the off rig. Hidden lights in frame 0.0.
- Emitters, off: the strip key (hidden) and the lifted world.
- Emitters, lit: the LED faces, plus the hidden key and fill.
