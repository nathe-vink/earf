# The corrected method, v3 (2026-11-15, night)

Supersedes notes-v2.md's verdict. v2's reference was itself biased (Filter Glossy on).

## What was wrong

1. **Filter Glossy (`blur_glossy` 1.0)**, set in studio/strata scene.render_settings for every frame. After a diffuse bounce
   it roughens glass refraction, and rough glass at that strength loses energy. That is exactly the path of light
   reaching a matte surface through glass, so it made every such light 30 to 40 % too dark. No clamp was on: direct
   and indirect read 0.0 in every frame type used.
2. **Hemisphere's opal was counted twice.** The scattering face carries the datasheet's whole-sheet figures, and a
   separate clear refracting face 3 mm outside it traps and returns light a second time. With Filter Glossy on, the
   rough-glass loss hid it.
3. **Core's ball counted room light twice**: thin_shadow on its faces plus real refraction.

## The corrected method (scratch rig, env only; lamp_site.py unchanged)

- Filter Glossy off (`BLUR=0`).
- Hemisphere's opal sheet acting once: its outer face a pass-through (`OPALFACE=pass`).
- Core's ball as plain refracting glass (`OPALTEST=corerefr`).

## The checks

**(a) The sheet alone**, flat, lit evenly by a large uniform emitter. Transmission and reflection are read against the
emitter, linear:

| Model | T | R |
|---|---|---|
| Datasheet (GS 041) | 0.54 | 0.39 |
| Old, Filter Glossy off | 0.655 | 0.559 |
| Old, Filter Glossy on | 0.579 | 0.447 |
| Corrected | 0.538 | 0.352 |

The old model returns 1.21 of the light that hits it, which is impossible.

**Converged cells** (1024 samples, no denoiser, the mean; no fireflies, max pixel within 1.6x the median):

| | Filter Glossy on | Off |
|---|---|---|
| Hemisphere Fog off | 101 | 120 |
| Core Fog off, plain refraction | 91 | 116 |
| Core Smoke 0.3x off, plain refraction | 34 | 51 |

**The bound, the reflection measured** (a black core behind the same ball, 0.0098 linear): 0.0098 + 0.922 x bare core
0.1827 = 0.178. Corrected Core Fog reads 0.175, within 2 %. Today's ball, Filter Glossy off, reads 0.196, 10 % over:
the double count.

## (b) Photometry: published against corrected

The published figures are photometry.txt. The lux is the published value scaled by the measured old-to-new ratio, both
probes on the same paper; Ember measured directly on #9A9A9A gives 324 / 210.

| Tint | Hemisphere lm (published > corrected) | Down share | Lux centre | Lux 0.3 m | Core lm (published / old rig today > corrected) |
|---|---|---|---|---|---|
| Ember | 272 > **334** (+23 %) | 73 % > **67 %** | 345 > **325** | 217 > **211** | 9.0 / 33.6 > **44.7** (+33 % on today) |
| Dust | 280 > **353** (+26 %) | 72 % > **65 %** | 351 > **331** | 220 > **214** | 12.5 / 38.0 > **51.1** (+34 % on today) |
| Acid | 301 > **419** (+39 %) | 69 % > **61 %** | 352 > **332** | 220 > **215** | 18.3 / 43.5 > **63.2** (+45 % on today) |
| Poison | 256 > **282** (+10 %) | 75 % > **73 %** | 345 > **325** | 216 > **210** | 3.0 / 23.3 > **29.8** (+28 % on today) |
| Ice | 264 > **308** (+16 %) | 74 % > **70 %** | 350 > **328** | 219 > **213** | 6.6 / 31.2 > **38.9** (+25 % on today) |
| Haze | 254 > **281** (+10 %) | 75 % > **73 %** | 346 > **326** | 216 > **210** | 3.2 / 27.3 > **33.0** (+21 % on today) |
| Fog | 339 > **521** (+54 %) | 66 % > **56 %** | 352 > **334** | 220 > **215** | 34.6 / 64.6 > **95.1** (+47 % on today) |
| Smoke | 287 > **378** (+32 %) | 71 % > **64 %** | 348 > **329** | 218 > **213** | 12.9 / 35.2 > **52.7** (+50 % on today) |

For the site lane:
- Hemisphere's Light-facts lumens rise 10 to 54 % (Ember 272 > 334, Fog 339 > 521).
- "about 350 lux" becomes **about 330 lux** (325 to 334 by tint).
- "73 % down" becomes **about 67 %** for Ember (56 to 73 % by tint).
- Core's published lumens (9.0, 12.5 and so on) were already out of date before this: today's unchanged rig gives
  23 to 65. The corrected values are 30 to 95 lm.

## (c) Lit cells at the finals' exposure (lit-correction.png)

The approved rows' crops beside the corrected method; nothing re-tuned. The lit glass is unchanged within 2 levels:
- Hemisphere Ember 253, 153, 144 > 253, 152, 143
- Hemisphere Smoke 209, 210, 210 > 209, 210, 209
- Core Fog 212, 192, 172 > 213, 193, 173
- Core Smoke 170, 171, 171 > 172, 172, 172

What moves is the glow on the paper round Core: Fog 46, 40, 36 > 56, 47, 42; Smoke 37 > 43. Hemisphere's paper barely
moves (36 > 38).

## (d) Off match, corrected (tints-off-v3.png)

Every tint still reads lighter on Hemisphere when off: Fog 131 against 117 (14); the rest 19 to 28 levels.
The Smoke pair: **Hemisphere 1.2x with Core 0.6x**.
- Off: 20, 20, 21 against 17, 19, 20, within 3.
- Lit: 125, 131, 134 against 136, 138, 140, both gray beside Fog. The lit glass doesn't change with the method.
- Light out against today's Smoke, corrected: Hemisphere 260 lm (69 %), Core 35.1 lm (67 %).
- Hemisphere 0.8x with Core 0.45x also matches off (30 / 31), but Hemisphere at 0.8x still reads as a white lamp lit.

## (e) The finals that would change visibly

- **Off and daylight** (clearly):
  - `hemisphere-ember-off.png`, `hemisphere-ember-cap.png`: Hemisphere is lighter off (Ember body 73, 14, 13 >
    96, 14, 10).
  - `core-row-day.png`, `core-base-options-day.png`: Core is lighter, by about 10 levels.
  - About 50 minutes.
- **Core lit** (the glow on the paper is about 20 % brighter; the ball unchanged):
  - `core-<tint>.png` x8, `core-row.png`, `core-base-b-lit.png`, `core-base-options.png`.
  - About 1 h 50 min.
- **Hemisphere lit** (glass unchanged, pool about 6 % lower: below visibility): no re-render needed.
- **All of it:** about 2 h 40 min.

## Audits and emitters

The corrected off rig (dome-black): hidden objects none, hidden lights in frame 0.0. The lit cells use the rows' rig.
- Emitters off: the strip key (hidden) and the lifted world.
- Emitters lit: the LED faces, plus the hidden key and fill.
