# Habitat finals, 2026-11-12

Each final: portrait 2400x3000 and wide 3200x2000 from the same scene and light, 96 samples. The speaker is the
approved build, asserted part by part against the asset's manifest before render.

| Tint | Files | Tropos asset | Sky | Lights | gt_audit | Scatter | Root-ray | Manifest | Weak |
|---|---|---|---|---|---|---|---|---|---|
| Fog (crest, released 13:03 on 82e81282) | fog-final-portrait-2400x3000.jpg, fog-final-wide-3200x2000.jpg | r33-speaker-horn 0f54ebee (before the detail pass) | syferfontein_6d_clear_puresky (Poly Haven), strength 1.0, its own sun at az 110, el 5.8 | the sun (SUN 3.0, colour (0.991, 0.823, 0.314)) and the sky; no emitters; one declared passive white board, 2 x 2 m at az -55, el 15, 3.5 m, out of frame (gt: no hidden object) | no hidden object, no area lamp (both frames) | wide CLEAN; portrait: 25 tufts based behind the crest (their roots hidden by the land, blades seen over it) | 0 fail (wide 534, portrait 278 seen roots; rootray.py) | Fog matches | the pale band under the tuft at wide 1247,742 (proxy) is fog over ground: the near fog box from 9.4 m, the ground at 10.7 m |

## Proxies, 2026-11-13 (the owner's notes of 2026-11-12 23:45: a place's own light, seen and listed, is allowed)

| Habitat | File | Tropos asset | Sky | Lights | gt_audit | Measured (800x1000) | Weak |
|---|---|---|---|---|---|---|---|
| Ember d (lava field, 22 Oct) | ember-d-proxy.jpg (48 samples) | r33-speaker-horn fd8aa47eb (detail pass) | qwantani_dusk_2_puresky, strength 0.15 | the sun (SUN 15, (1.0, 0.491, 0.254), az -13, el 5: 35 deg left of the lens axis); the lava, seen: the river and cracks (prop1 lava surface, Lava001, emission 80 x gain 2.6), the far flow (prop2, 40 x 2.2) and molten pools (prop2, 30), the near terrain's flow and molten materials (prop0, 4), 12 sparks (emission 16); no lamps | no hidden object, no area lamp | front panel 0.729 (hue 5.3), cone 0.365 (hue 16.4), the speaker 0.39; 0 clipped pixels in the PNG master | the red front glows strongly from the lava behind it; it may read as lit from within |
