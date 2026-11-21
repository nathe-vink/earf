# A, the critics' round 2: the proof (2026-11-21)

Five variants of A at 960 x 640, 64 samples, all with the subdivided sofa and the card sleeves behind Mantle. Made by
`gen.py` (from `living_room.py`) and `studio/engine/render.py`.

- `a-base`: the scene as it is.
- `a-pier`: the 4.6 m run of windows behind the camera as two windows of 1.7 m around a 1.2 m stretch of wall,
  centred behind the lens.
- `a-cam`: the camera at 1.15 m (from 1.5), the same target, level.
- `a-back`: the back window 0.6 m wide (from 0.75), its centre at x -2.33 (from -2.22).
- `a-all`: the three together, and the water in the glass at 78 mm of its 92 mm (from 60).

`sheet.png` puts the five side by side. `top-base-cam.png` zooms on the left cabinet's top, base above, cam below.

## Measured (CIELAB L* and C*, `living/lstar.py`, boxes in the 2400 x 1600 frame's pixels)

| | base | pier | cam | back | all |
|---|---|---|---|---|---|
| top, left (L* / C*) | 63.2 / 22.2 | 61.7 / 22.5 | a thin edge | 62.8 / 22.3 | a thin edge |
| top, right | 42.2 / 16.2 | 38.3 / 16.7 | a thin edge | 42.2 / 16.3 | a thin edge |
| throat, left / right (L* p95, the eye) | 62 / 49 | 51 / 38 | 64 / 51 | 62 / 49 | 53 / 41 |
| cone, left / right (L*) | 28.3 / 38.8 | 22.9 / 27.9 | 26.6 / 33.4 | 28.3 / 38.7 | 23.0 / 26.4 |
| ports, left / right (C*) | 47.0 / 33.8 | 50.6 / 33.5 | hidden by the sofa | 46.9 / 33.7 | hidden by the sofa |
| front above the woofer, left / right (C*) | 64.3 / 63.6 | 60.9 / 58.3 | 60.6 / 58.0 | 64.6 / 63.6 | 57.7 / 54.2 |
| Mantle's pillar (L* mean / max) | 58.7 / 100 | 57.5 / 100 | | 58.6 / 100 | |
| floor before the console (L*) | 55.7 | 50.1 | | 55.6 | |
| wall (L*) | 75.2 | 72.3 | 75.4 | 75.1 | 72.3 |

- **The stretch of wall** darkens the throats' eye by about 11 L*. It takes the cones' difference from 10.5 to 5 L*.
  It costs the room about 3 L* (wall, floor), and the fronts 3 to 5 C*.
- **The camera at 1.15 m** takes the beige top away: it is seen almost edge-on, a thin dark line under the horn. But the
  sofa's back rises across the foot of both speakers and hides their ports.
- **The back window, narrowed and moved left,** changes nothing measurable.
- **Mantle's pillar** keeps its highlight (max L* 100) in every variant: the sun.
