# C, two crops before the full frame (2026-11-21)

These crops are from C's own shot file (`c.shot.json`) with only the audit's fixes put in, at 256 samples, the frame's
pixels exactly (`--crop`):
- **The water:** the set piece `water_glass`. Glass to air at 1.5, glass to water at 1.5/1.33 with no air film between
  them, water to air at 1.33, and a 1.5 mm meniscus. The water stands at 78 mm, as in A.
- **`filter_glossy` 0.**
- **The Core:** at the lamps lane's ecb1650c24. That commit's skin is 6 mm along its normals with the lip closed, both
  passes tinted, and the liner in contact. The commit is pinned in `living_room.py` and checked by `cores_off`.
  `base.report.json` carries it under `lamps`.

The glass crop's build was at 7e08871d9 for the Core, which is not in that crop. Each crop took 4 minutes.

- `glass-before-after.png`, at 2x:
  - **Left, the current C:** the water 0.6 mm inside the wall, at 1.5, read as a silvery funnel.
  - **Right:** the glass now reads as full of water. The water line is near the rim, and the table and the room
    refract through it.
- `base-v2-v3-v4.png`, the base in the frame's pixels:
  - **v2:** the gap between the skin and the liner.
  - **v3:** 7e08871d9, contact only.
  - **v4:** ecb1650c24, with the water and `filter_glossy` 0.

**The base and the ball** (L* / C* / hue; the same boxes as `base_readings.py`, rows y 1320 to 1380):

| | left flank | centre | right flank | ball (x 640-760, y 1150-1190) |
|---|---|---|---|---|
| v2 | 26.8 / 31.0 / 37 | 38.8 / 54.6 / 36 | 39.5 / 20.9 / 12 | |
| v3 | 37.5 / 53.2 / 36 | 41.0 / 55.5 / 35 | 45.4 / 33.9 / 22 | 38.4 / 60.4 / 35 |
| v4 | 32.0 / 42.2 / 37 | 37.1 / 48.6 / 35 | 42.7 / 25.2 / 16 | 46.6 / 66.8 / 36 |

- **The base in v4** is deeper and less pink than in v3: both passes are now tinted. Its flanks hold the centre's hue
  (37 against 35), with no gray-brown band.
- **The ball in v4** is lighter and deeper, 8 L* and 6 C* up. That comes from `filter_glossy` 0: the caustics through
  its polished shell are no longer blurred.
