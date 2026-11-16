# THE MIX (2026-11-16)

Each tint moves the lamp that keeps its lit color rich. The sheet is assembled from the A2 (`../hemi-match/`), Step A (`../core-match/`) and corrected scratch cells. Three Hemisphere lit cells were missing and are rendered for this sheet in the same rig: Smoke at 0.3x and 1.2x, and Fog.

`mix-sheet.png` has eight columns and four rows: Hemisphere off, Core off (the one off rig), Hemisphere lit, Core lit (the rows' rig and exposure). Each cell is TODAY | MIX, with the changed lamp outlined and its sRGB (the median of the body away from highlights) underneath. Every number is in `mix-numbers.json`.

| Tint | Moves | Off gap, today > mix | Hemisphere light out | Core light out |
|---|---|---|---|---|
| Ember | Hemisphere 1 > 1.8 | 24 > 13 | 334 > 307 lm | 44.7 (same) |
| Dust | Core 3 > 1.6 | 21 > 14 | 353 (same) | 51.1 > 62.2 lm |
| Acid | Hemisphere 3 > 5 | 19 > 8 | 419 > 380 lm | 63.2 (same) |
| Poison | Core 1 > 0.6 | 23 > 9 | 282 (same) | 29.8 > 38.1 lm |
| Ice | Hemisphere 3 > 6 | 22 > 5 | 308 > 270 lm | 38.9 (same) |
| Haze | Hemisphere 1 > 1.8 | 28 > 10 | 281 > 258 lm | 33.0 (same) |
| Fog | left | 14 | 521 | 95.1 |
| Smoke | both: Hemisphere 0.3 > 1.2, Core 0.3 > 0.6 | 21 > 3 | 378 > 260 lm | 52.7 > 35.1 lm |

## Lit, today > mix (the changed lamp)

- **Ember, Hemisphere:** 255,165,157 > 253,145,136. A little deeper red, and still clear of Dust's Hemisphere (249,185,163, unchanged).
- **Dust, Core:** 217,124,86 > 210,157,124. Paler: orange goes toward peach.
- **Acid, Hemisphere:** 227,221,178 > 222,213,163. Barely moves.
- **Poison, Core:** 0,118,52 > 0,152,66. Brighter, still vivid green.
- **Ice, Hemisphere:** 144,195,233 > 79,153,234. Deeper blue.
- **Haze, Hemisphere:** 202,150,207 > 141,95,201. Deeper violet.

## Where the mix is worse than as built

- **Dust:** the one tint where the mix costs the lit look. Core's lit glass goes paler (G 124 > 157, B 86 > 124). It still reads apart from Ember's Core (228,85,71), but less orange. The off match gains only 21 > 14, because Core can't go lighter than about 117. Leaving Dust as built is a fair call.
- **Haze and Ice switched off:** the denser Haze (15,23,73) reads closer to Ice (2,34,91) as a dark blue on Hemisphere. Core's pair is already as close (7,13,74 and 0,36,86), so the mix doesn't make this worse than Core already is.
- Elsewhere the mix is at least as good as as built, lit and off.
