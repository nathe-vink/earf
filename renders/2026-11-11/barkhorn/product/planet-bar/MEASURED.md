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
