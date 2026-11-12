# Lamp colours against the lamps lane's finals (2026-11-11)

Median HSV of a patch at each lamp's centre (hue in degrees, saturation and value 0-1), against r32-lamps-final's
renders/2026-11-10/barkhorn/lamp-site/final/ measured the same way. Exposed as the lamps lane exposes them: AgX,
Punchy, white balance 4000 K; Core alone at EV -1 (its finals'), the wide at EV -1.5 (between Core -1 and Hemisphere -2).

| lamp | frame | ours (h, s, v) | finals (h, s, v) |
|---|---|---|---|
| Core Ember | core-bar-table | 4.9, 0.63, 0.92 (RGB 235 100 88) | 5.0, 0.64, 0.91 (RGB 232 98 86) |
| Hemisphere Acid | bar-backbar | 51.7, 0.19, 0.91 | 52.4, 0.19, 0.91 |
| Hemisphere Ember | bar-backbar | 5.0, 0.35, 1.00 | 5.1, 0.34, 1.00 |
| Hemisphere Dust | bar-backbar | 15.1, 0.31, 0.99 | 16.9, 0.30, 0.98 |
| Core Dust | bar-backbar | 21.9, 0.86, 0.68 | 17.1, 0.60, 0.86 |

All match but the Dust Core in the wide (half a stop under its own exposure: darker and more saturated). What fixed
Core: the lamps lane's own exposure for it (EV -1 and 4000 K, not -5) and its own LED colours (no 4000 K override for
Dust and Acid), with the room's declared light low enough that the ball's glow carries it.

## Round 3 (2026-11-11, after the coordinator's 20:47 notes)

Exposure EV -2.0 in the wide (was -1.5); core-bar-table keeps EV -1 and its room as approved.

| what | frame | measured |
|---|---|---|
| Core Ember centre (h, s, v) | core-bar-table | 5.0, 0.67, 0.90 (finals 5.0, 0.64, 0.91) |
| near Tropos, its lit cabinet face against the record wall | bar-backbar | top 0.70, side 0.26, wall 0.25: face 1.9x the wall (round 2's whole-speaker box 2.45x; now 0.7x, the cone near black pulling it down) |
| near Tropos woofer cone, mean | bar-backbar | 0.21 (grey-white before) |
| covered by nearer things | bar-backbar | near 1.8 % (Mantle's corner, below its foot), far 0.2 % |
| audit (reaudit.py) | both | hidden 0, equipment 0 |

Grey levels are the frame's 0-1 luminance on a 1200 px copy (cabinet top, cabinet side, cone, and a patch of the record wall
between the bays).

## Round 4 (2026-11-11/12, after the coordinator's 22:32 notes)

| what | frame | measured |
|---|---|---|
| Core Ember centre (h, s, v) | core-bar-table | 5.0, 0.67, 0.91 (finals 5.0, 0.64, 0.91) |
| near Tropos cabinet face against the wall; cone | bar-backbar | face 1.8x the wall; cone 0.20 |
| audit (reaudit.py) | both | hidden 0, equipment 0 |

The ball's pale rectangle was the house fill's reflection, a 3 m disc cut flat by the ceiling: in core-bar-table it
is a 1.6 m disc inside the room now (a round soft highlight, as on the lamps lane's own Core). The black square was
the book of matches, out of that frame. The near horn reads by a graduated warm card over its bay, seen only in
reflections (declared in the emitters file). Mantle's plinth is clear Ember acrylic in layers: a narrow low head from
past the frame's right edge passes through it.

## Full size and two test frames (2026-11-12, after the coordinator's 00:33 batch)

| frame | size, samples | file |
|---|---|---|
| bar-backbar | 3200 x 1800, 256 (adaptive 0.005) | 4.5 MB, lossless (the opaque alpha dropped) |
| core-bar-table | 3200 x 2133, 512 | 4.2 MB, lossless |
| bar-backbar-portrait | 2400 x 3000, 224 | 4.9 MB: lossless was 5.4 MB (zopfli), so the lowest bit of channel values under 24 is dropped (at most 1/255, deep shadows only) |
| bar-pendants (test) | 1920 x 1920, 256 | 2.7 MB, lossless |
| mantle-bar (test) | 1920 x 1280, 256 | 1.7 MB, lossless |

| what | frame | measured |
|---|---|---|
| Core Ember centre (h, s, v) | core-bar-table | 5.1, 0.59, 0.94 (finals 5.0, 0.64, 0.91; the patch takes in the soft highlight) |
| near Tropos, whole box against the wall; covered | bar-backbar | 0.79x the wall (the cone near black pulls the box down; round 4's face-only figure 1.8x); covered 1.8 % |
| audit (reaudit.py) | all five | hidden 0, equipment 0 |

Contact edges, checked in full-size crops: the Tropos feet on the bay floor (wide and portrait), the glasses on the
stone (wide, portrait, pendants), Mantle's plinth on the stone (wide, mantle-bar), the Core bases (wide, core-bar-table,
pendants). In the portrait the near Core is close and seen from above: the ball hides its narrower base, and the pink
under it is its reflection on the stone in front of the base.
