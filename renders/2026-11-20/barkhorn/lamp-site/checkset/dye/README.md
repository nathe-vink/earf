# Core dye-balance test (2026-11-21)

This is a test for the owner, not a change to any product. `CORE_ABS=R,G,B` multiplies the Core's own per-channel dye absorption (ball, base and cast colour alike), at today's Core pour. The tint name is the same and the pendant is untouched: a maker re-mixing the thick part's dyes.

All frames are Core OFF, half size, 128 spp, with the row-off settings. Values are the body's median L* / C* / h.

| Tint | Today | Round 1 | Round 2 | Pendant pick |
|---|---|---|---|---|
| Dust | 54.2 / 79.0 / 37.6 | 1.0, 0.70, 1.48: 57.9 / 74.9 / 43.5 | 1.0, 0.61, 2.0: 59.8 / 73.1 / 46.7 | 2.1x: 54.3 / 71.7 / 50.1 |
| Ice | 39.1 / 73.4 / 294.3 | 1.61, 0.88, 1.15: 41.9 / 64.2 / 289.4 | 2.5, 0.87, 1.19: 42.1 / 62.8 / 288.7 | 3x: 38.4 / 59.5 / 287.9 |
| Haze | 26.3 / 79.8 / 306.0 | 0.89, 1.46, 1.08: 26.8 / 77.6 / 307.6 | 0.89, 2.5, 1.09: 26.8 / 77.3 / 307.7 | 1x: 22.7 / 75.8 / 308.2 |

What each mix means physically:

- **Dust:** less green absorption and more blue.
- **Ice:** more red absorption and slightly less green.
- **Haze:** more green absorption and slightly less red.

After round 2 the hue is within about 1° for Ice and Haze, and 3.4° for Dust (12.5° before). Chroma is within 1.5-3.3. Each Core is now 4-5.5 L* lighter than its pick; a heavier Core pour (CORE_LOAD) would close that.

The darkest channel of each tint (Dust's B, Ice's R, Haze's G) barely responds to its factor: the clear ball's neutral surface reflections set its floor.

## Rounds 3-4 (17:00-18:55), the Core's pour as well (CORE_LOAD; today Dust 1.5, Ice 1.5, Haze 0.5)

dE00 is the CIEDE2000 colour difference between the Core body's median L*/C*/h and the pendant pick's.

| Tint | Today | Round 2 | Round 3 | Round 4 |
|---|---|---|---|---|
| Dust | 9.4 | 5.6 | pour 2.1, 1.0 / 0.61 / 2.0: 54.6 / 77.5 / 40.6, 7.2 | pour 2.1, 1.0 / 0.45 / 2.5: 58.6 / 73.1 / 47.1, **4.6** |
| Ice | 4.2 | 3.3 | pour 1.95, 2.5 / 0.87 / 1.19: 34.5 / 68.1 / 295.1, 5.9 | pour 1.72, 3.2 / 0.85 / 1.19: 38.6 / 64.9 / 291.7, **2.4** |
| Haze | 3.4 | 3.0 | pour 0.7, 0.89 / 2.5 / 1.09: 21.6 / 65.7 / 304.5, 3.4 | pour 0.65, 0.89 / 1.6 / 1.09: 22.6 / 68.3 / 305.0, **2.7** |

The pour and the dye mix interact. A heavier pour on round 2's mix (round 3) reached the lightness but pulled the hue back, so round 4 retuned the mix at the heavier pour. Round 4 is the best on every tint so far.

## Round 5 (19:10-19:40)

dE00 to the pick, with round 4 in brackets:

| Tint | Pour; R / G / B | L* / C* / h | dE00 |
|---|---|---|---|
| Haze | 0.6; 0.89 / 2.2 / 1.09 | 23.8 / 71.2 / 305.8 | **2.1** (2.7) |
| Haze | 0.65; 0.89 / 2.5 / 1.09 | 22.6 / 68.3 / 305.0 | 2.7 |
| Ice | 1.72; 3.2 / 0.75 / 1.19 | 41.9 / 58.8 / 287.0 | 3.1 (2.4; round 4 stays best) |
| Dust | 2.6; 1.0 / 0.35 / 2.5 | 58.4 / 71.1 / 49.1 | **3.9** (4.6) |
| Dust | 2.9; 1.0 / 0.30 / 2.5 | 58.6 / 69.2 / 51.0 | 4.1 |

- **Haze:** the 0.65 frame matches round 4 exactly although its green factor changed. Haze's green absorption is already saturated, so raising it shows nothing.
- **Dust:** the hue and chroma now match, but it stays about 4 L* light at any pour. Its dye passes red almost whole, so multiplying the red absorption does nothing.
- **Round 6:** Dust with a neutral absorption added to every channel (CORE_ABS_ADD, a touch of black in the mix).
