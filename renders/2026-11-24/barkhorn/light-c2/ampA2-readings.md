# Amp rig A2, the eight at full size beside A

ampA2-<tint>: amp rig A with the front strip a real body (casts shadows, black back and box) moved to orbit azimuth
-55, clear of the key's beam; flag 1 seen by the camera; path depth 32 total / 16 glossy / 32 transmission; -0.2 EV
for all eight; 1600 x 1600, 128 spp. Shot files from amp-test/a2/make_a2.py; picked in amp-test/a2/readings.md.
Rendered by the eight helpers (r33-lightc-{smoke,poison,ember,ice,dust}, r33-lightc2-{haze,fog,acid}) and merged here.
Every frame: equipment 0, hidden 0, no_glass_shadows.cut 6, shadow_ray_links_left.count 0, no crossing.
Measured with amp-test/meas.py (each frame's own mask) and amp-test/a2box.py (lining slab, deep inside: boxes, since
the clear back makes the mask call everything behind it `back`). Sheet: sheet-ampA2.png (A beside A2, per tint).

| frame | plate face L* | plate L* | plate C* | surround L* | surround C* | surround Y share | pinned >= 251 | panel blotch L* RMS | print L* | print - plate |
|---|---|---|---|---|---|---|---|---|---|---|
| A-acid | 20.4 | 22.2 | 2.6 | 57.8 | 50.8 | 100 % | 0.2 % | 2.30 | 90.3 | 70.0 |
| A2-acid | 19.9 | 21.8 | 2.6 | 61.9 | 54.7 | 114 % | 0.2 % | 2.38 | 89.7 | 69.7 |
| A-dust | 20.3 | 22.1 | 2.8 | 45.0 | 47.6 | 56 % | 1.7 % | 1.90 | 90.3 | 70.0 |
| A2-dust | 19.8 | 21.7 | 2.9 | 48.0 | 52.2 | 62 % | 2.2 % | 1.94 | 89.6 | 69.8 |
| A-ember | 20.1 | 22.0 | 2.8 | 23.1 | 40.1 | 14 % | 0.0 % | 0.83 | 90.2 | 70.1 |
| A2-ember | 19.7 | 21.6 | 2.8 | 24.1 | 42.6 | 15 % | 0.0 % | 0.86 | 89.5 | 69.8 |
| A-fog | 20.6 | 22.5 | 2.8 | 68.2 | 1.1 | 148 % | 0.0 % | 2.69 | 90.5 | 69.9 |
| A2-fog | 20.3 | 22.1 | 2.8 | 73.7 | 1.2 | 172 % | 0.0 % | 2.65 | 89.9 | 69.6 |
| A-haze | 20.1 | 22.0 | 3.0 | 21.9 | 60.9 | 12 % | 0.0 % | 0.79 | 90.2 | 70.0 |
| A2-haze | 19.7 | 21.6 | 3.1 | 22.9 | 65.5 | 13 % | 0.0 % | 0.83 | 89.5 | 69.8 |
| A-ice | 20.3 | 22.1 | 3.1 | 41.3 | 34.4 | 47 % | 0.7 % | 1.71 | 90.2 | 70.0 |
| A2-ice | 19.8 | 21.7 | 3.2 | 43.6 | 38.8 | 52 % | 0.9 % | 1.78 | 89.5 | 69.7 |
| A-poison | 20.2 | 22.0 | 2.7 | 26.8 | 33.5 | 19 % | 0.0 % | 0.82 | 90.2 | 70.0 |
| A2-poison | 19.7 | 21.6 | 2.8 | 27.7 | 35.1 | 20 % | 0.0 % | 0.85 | 89.5 | 69.8 |
| A-smoke | 20.1 | 22.0 | 2.8 | 15.0 | 1.0 | 8 % | 0.0 % | 0.69 | 90.2 | 70.0 |
| A2-smoke | 19.7 | 21.6 | 2.8 | 15.2 | 1.0 | 8 % | 0.0 % | 0.68 | 89.5 | 69.8 |

| frame | lining slab | deep inside | clipped >= 251 |
|---|---|---|---|
| A-acid | 81.5 | 41.6 | 0.2 % |
| A2-acid | 84.8 | 50.4 | 0.2 % |
| A-dust | 64.9 | 31.6 | 1.7 % |
| A2-dust | 67.2 | 37.8 | 2.2 % |
| A-ember | 33.9 | 16.3 | 0.0 % |
| A2-ember | 35.4 | 17.8 | 0.0 % |
| A-fog | 92.6 | 50.1 | 0.0 % |
| A2-fog | 94.7 | 61.6 | 0.0 % |
| A-haze | 32.1 | 15.6 | 0.0 % |
| A2-haze | 33.7 | 17.2 | 0.0 % |
| A-ice | 61.3 | 27.8 | 0.7 % |
| A2-ice | 63.7 | 32.0 | 0.9 % |
| A-poison | 41.3 | 17.5 | 0.0 % |
| A2-poison | 43.1 | 18.2 | 0.0 % |
| A-smoke | 12.9 | 17.4 | 0.0 % |
| A2-smoke | 12.9 | 18.3 | 0.0 % |

Surround Y share is per row against the first row (A-acid); compare A and A2 of a tint by L*.

Looked at by the coordinator: Fog's lighter interior (deep inside +11.5) is the depth fix (felt reads white, not
grey; still front-lit); Dust's pinned 2.2 % sits where A's was (the acrylic's top edge under the scrim, the floor
seen lower left), red only, against FA123's 9.5 %. Both kept; one rig, one exposure.
