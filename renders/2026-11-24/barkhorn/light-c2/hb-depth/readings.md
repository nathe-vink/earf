# Horn-back path depth test (Fog, Acid)

The horn-backs rendered at bounces 12 with no glossy or transmission keys (render.py: 12 / 6 glossy / 8 / 8). Here
the same shot files at 32 total / 16 glossy / 32 transmission (hb32-<tint>.json), full size 1200 x 900, same rig
and exposure, beside the committed horn-back-<tint>.png. Audits: equipment 0, hidden 0. Fog 14 min, Acid 10 min.
Sheet: sheet-hb-depth.png (current, depth 32, difference with white at 12 % or more).

| tint | frame L* | px with dL* >= 3 | px with dL* >= 6 | pinned |
|---|---|---|---|---|
| fog | 85.7 -> 87.7 | 119,544 (11.1 %) | 91,570 (8.5 %) | 0.0 -> 0.0 % |
| acid | 77.8 -> 78.4 | 68,645 (6.4 %) | 39,764 (3.7 %) | 0.0 -> 0.0 % |

Parts that move most (mean L*, current -> depth 32):

| part | fog | acid |
|---|---|---|
| right | 45.6 -> 77.4 (+31.8) | 35.0 -> 43.4 (+8.5) |
| grip-left | 63.0 -> 75.1 (+12.0) | 57.0 -> 64.3 (+7.3) |
| left | 66.5 -> 76.3 (+9.8) | 53.1 -> 56.0 (+2.9) |
| back | 65.9 -> 73.9 (+7.9) | 54.8 -> 58.3 (+3.4) |
| waveguide-cap | 50.7 -> 58.6 (+7.9) | 20.8 -> 21.0 (+0.2) |
| top | 82.3 -> 84.8 (+2.6) | 63.3 -> 63.9 (+0.6) |

The thick acrylic (the cabinet walls, edges and grips, Fog's clear waveguide cap) opens up the way A2's amp did:
visible at sheet size in Fog, smaller but plain in Acid. The paper and the horn's flat faces do not move. Verdict:
the eight horn-backs want re-rendering at depth before the light-C push.
