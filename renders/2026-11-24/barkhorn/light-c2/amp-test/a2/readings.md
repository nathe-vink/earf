# A2 test: real body panels, the front strip three ways (Ice, Acid)

800 x 800, 128 samples, path depth 32 total / 16 glossy / 32 transmission, exposure -0.2, with masks. A is the full
1600 x 1600 ampA frame at depth 16 (measured at its own size). Ad is A's rig at the new depth, so Ad to A shows what
the depth did and Ad to A2x shows what the strip did. Audits: equipment 0 px, hidden 0 px in all eight; no crossings.

- **Ad**: A's rig at the new depth (strip seen by the camera, no body, casts no shadow).
- **A2a**: the strip a real body (casts shadows, black back and box), moved clear of the key's beam from the plate
  and the floor patch: orbit azimuth -25 to -55 (geometric check: 35.2 % of the key blocked from the plate and 19.9 %
  from the floor where it was; 0.0 % and 0.1 % moved).
- **A2b**: the strip a real body where it is.
- **A2c**: the strip out.

All: flag 1 seen by the camera.

Readings (`../meas.py`, `../a2box.py`; lining slab and deep inside are boxes, because the back is clear and the mask
calls all of it `back`; print L* reads about 7 low at 800 px from the smaller letters, in Ad too):

| frame | plate face L* | surround L* | pinned >= 251 | panel blotch L* RMS |
|---|---|---|---|---|
| A-ice | 20.3 | 41.3 | 0.7 % | 1.71 |
| Ad-ice | 20.8 | 42.7 | 0.7 % | 1.53 |
| A2a-ice | 20.3 | 43.6 | 0.9 % | 1.61 |
| A2b-ice | 16.8 | 40.3 | 0.5 % | 1.53 |
| A2c-ice | 20.1 | 43.3 | 0.8 % | 1.61 |

| frame | lining slab | deep inside | clipped >= 251 |
|---|---|---|---|
| A-ice | 61.3 | 27.8 | 0.7 % |
| Ad-ice | 61.4 | 32.2 | 0.7 % |
| A2a-ice | 63.7 | 32.1 | 0.9 % |
| A2b-ice | 57.7 | 30.6 | 0.5 % |
| A2c-ice | 63.4 | 31.9 | 0.8 % |

| frame | plate face L* | surround L* | pinned >= 251 | panel blotch L* RMS |
|---|---|---|---|---|
| A-acid | 20.4 | 57.8 | 0.2 % | 2.30 |
| Ad-acid | 20.9 | 60.6 | 0.1 % | 2.36 |
| A2a-acid | 20.5 | 61.9 | 0.1 % | 2.47 |
| A2b-acid | 16.9 | 57.8 | 0.1 % | 2.34 |
| A2c-acid | 20.2 | 61.6 | 0.1 % | 2.47 |

| frame | lining slab | deep inside | clipped >= 251 |
|---|---|---|---|
| A-acid | 81.5 | 41.6 | 0.2 % |
| Ad-acid | 81.7 | 50.7 | 0.1 % |
| A2a-acid | 84.8 | 50.6 | 0.1 % |
| A2b-acid | 77.5 | 49.0 | 0.1 % |
| A2c-acid | 84.3 | 50.4 | 0.1 % |

Pick: **A2a**. The plate face holds within 0.3 L* of Ad and A, so the exposure stays at -0.2. A2b puts the plate in
the strip's real shadow: its face drops 3.5 L* (over the 3 L* line), the lining slab 4. A2c reads within 0.3 L* of
A2a everywhere; A2a keeps A's rig with one lamp moved, and the strip's small catch on the lining. Against A, the
change is the depth (Ad): deep inside +4 L* (Ice) and +9 (Acid), surround +1 to +3.

The eight A2 shot files are `../../ampA2-<tint>.json` (from `make_a2.py`).
