# A, the critics' round 2: proof 2 (2026-11-21)

Three cameras for A at 960 x 640, 64 samples. Each has the room's current code: the 1.2 m stretch of wall behind the
camera, exposure 5.5, the water at 78 mm, the subdivided sofa and the card sleeves. Made by `gen.py` (from
`living_room.py`) and `studio/engine/render.py`, with lamps at 5fa6ef9. Audits: hidden 0, equipment 0 in all three.

- `a-p15`: the camera at 1.5 m (as A is now).
- `a-p125`: the camera at 1.25 m, the same target, level.
- `a-p115s`: the camera at 1.15 m, and the sofa 0.4 m nearer the camera.

`sheet.png` puts the three side by side, in that order. `tops.png` zooms on the left cabinet's top and `feet.png` on
the speakers' feet, top to bottom in the same order.

## Measured by part (`meas.py`: the engine's part masks, CIELAB L* / C*)

Proof 1 measured with hand-placed boxes. This proof measures each part's own visible pixels, so its numbers are not
comparable with proof 1's table. Compare them only across these three.

| | 1.5 m | 1.25 m | 1.15 m, sofa nearer |
|---|---|---|---|
| top, left: L* / C* (pixels) | 48.6 / 10.2 (1131) | 49.0 / 8.7 (957) | 48.7 / 8.9 (813) |
| top, right | 33.4 / 10.9 (1167) | 35.0 / 8.2 (989) | 36.5 / 8.7 (818) |
| throat's eye, left / right (L* p95) | 31.8 / 23.2 | 32.1 / 25.7 | 29.7 / 26.8 |
| phase plug, left / right (L*) | 51.6 / 39.6 | 52.5 / 40.7 | 54.1 / 42.1 |
| cone, left / right (L*) | 21.8 / 24.9 | 21.6 / 24.7 | 21.7 / 24.6 |
| front above the woofer, left / right (C*) | 56.3 / 52.2 | 57.8 / 50.5 | 56.2 / 52.6 |
| front below the woofer, the ports, left / right (C*) | 53.5 / 44.7 | 55.6 / 46.8 | 54.9 / 43.3 |
| wall (L*) | 74.3 | 74.3 | 74.3 |
| floor before the console (L*) | 54.1 | 54.6 | 55.4 |

- **The tops:** the masks show that the pale band under each horn is the cabinet's top: a pale neutral, C* about 9,
  mirroring the back wall. It does not become a dark line at the lower cameras, but it gets smaller: 28 % fewer pixels
  at 1.15 m than at 1.5 m. A strip of wall shows between the horn and the top, about 3 px, in all three cameras.
- **The sofa and the feet** (`feet.png`):
  - At 1.25 m the sofa's arms rise over each speaker's outer bottom corner and cut off its foot.
  - At 1.15 m with the sofa 0.4 m nearer, its back sits about 10 px below both feet. The ports, the feet and the floor
    between them all show.
  - At 1.5 m everything is clear.
- **Everything else** moves by 1 to 3 L* or C*: the throats, the cones, the fronts and the room.
