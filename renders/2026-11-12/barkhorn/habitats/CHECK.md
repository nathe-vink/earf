# Habitat finals, 2026-11-12

Each final: portrait 2400x3000 and wide 3200x2000 from the same scene and light, 96 samples. The speaker is the
approved build, asserted part by part against the asset's manifest before render.

| Tint | Files | Tropos asset | Sky | Lights | gt_audit | Scatter | Root-ray | Manifest | Weak |
|---|---|---|---|---|---|---|---|---|---|
| Fog (crest, released 13:03 on 82e81282) | fog-final-portrait-2400x3000.jpg, fog-final-wide-3200x2000.jpg | r33-speaker-horn 0f54ebee (before the detail pass) | syferfontein_6d_clear_puresky (Poly Haven), strength 1.0, its own sun at az 110, el 5.8 | the sun (SUN 3.0, colour (0.991, 0.823, 0.314)) and the sky; no emitters; one declared passive white board, 2 x 2 m at az -55, el 15, 3.5 m, out of frame (gt: no hidden object) | no hidden object, no area lamp (both frames) | wide CLEAN; portrait: 25 tufts based behind the crest (their roots hidden by the land, blades seen over it) | 0 fail (wide 534, portrait 278 seen roots; rootray.py) | Fog matches | the pale band under the tuft at wide 1247,742 (proxy) is fog over ground: the near fog box from 9.4 m, the ground at 10.7 m |
