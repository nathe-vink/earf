# Lamp colours against the lamps lane's finals (2026-11-11)

Centre colour of each lit lamp (median HSV of a patch at the centroid of its brightest pixels; hue in degrees, saturation
and value 0-1), against r32-lamps-final's renders/2026-11-10/barkhorn/lamp-site/final/ (core-<tint>.png,
hemisphere-<tint>.png), measured the same way.

| lamp | frame | ours (h, s, v) | finals (h, s, v) |
|---|---|---|---|
| Core Ember | core-bar-table | 8.8, 1.00, 0.68 | 5.0, 0.64, 0.91 |
| Core Ember | bar-wide | 10.1, 1.00, 0.78 | 5.0, 0.64, 0.91 |
| Core Dust | bar-wide | 16.0, 0.84, 0.84 | 17.1, 0.60, 0.86 |
| Core Acid | bar-wide | 46.3, 0.79, 0.70 | 52.4, 0.40, 0.76 |
| Core Ember | bar-pendants | 9.4, 0.71, 0.87 | 5.0, 0.64, 0.91 |
| Core Acid | bar-pendants | 43.0, 0.49, 0.82 | 52.4, 0.40, 0.76 |
| Hemisphere Ember | bar-pendants | 6.7, 0.48, 1.00 | 5.1, 0.34, 1.00 |
| Hemisphere Dust | bar-pendants | 15.4-15.9, 0.45, 0.98 | 16.9, 0.30, 0.98 |
| Hemisphere Acid | bar-pendants | 40.8-41.0, 0.23-0.34, 0.90 | 52.4, 0.19, 0.91 |

Ember and Dust within a few degrees, saturation at or above the finals everywhere. Acid reads 9-11 degrees toward orange
(the warm declared soffit on its shell). In bar-wide the shades are small and the frame is a stop under the pendants
frame's light per lamp area; their measurement there is dominated by the shelves behind.
