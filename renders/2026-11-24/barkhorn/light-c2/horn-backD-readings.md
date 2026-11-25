# Horn-backs at path depth 32/16/32 beside today's

horn-backD-<tint>: horn-back-<tint> with only the render block changed (bounces 32, glossy 16, transmission 32; it
was 12 with no other keys, which render.py takes as 12 total / 6 diffuse / 8 glossy / 8 transmission). Same rig, exposure and size (1200 x 900, 128 spp). Rendered
by the eight helpers on fab53bafab and merged here. Every frame: equipment 0, hidden 0, no_glass_shadows.cut 6,
shadow_ray_links_left.count 0, no crossing. Sheet: sheet-horn-backD.png (today's beside depth, per tint, same size).

Per tint: frame mean L*, the share of pixels that move by 3 and 6 L*, the largest pixel shift (99.9th percentile of
|dL*|), pinned (any channel >= 251). Per part (each frame's own mask): mean L* today -> depth (mean shift; the part's
99th-percentile shift, its largest local change).

| tint | frame L* | px dL* >= 3 | px dL* >= 6 | largest pixel shift (p99.9) | pinned | right | grip-left | left | back | waveguide-cap | top | horn-pod |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| acid | 77.8 -> 78.4 | 6.4 % | 3.7 % | 23.1 | 0.00 -> 0.00 % | 35.0 -> 43.4 (+8.5, p99 +20.8) | 57.0 -> 64.3 (+7.3, p99 +11.4) | 53.1 -> 56.0 (+2.9, p99 +16.5) | 54.8 -> 58.3 (+3.4, p99 +25.0) | 20.8 -> 21.0 (+0.2, p99 +2.0) | 63.3 -> 63.9 (+0.6, p99 +4.7) | 21.3 -> 21.4 (+0.2, p99 +1.5) |
| dust | 73.7 -> 74.3 | 6.3 % | 3.2 % | 26.6 | 0.00 -> 0.00 % | 31.1 -> 42.8 (+11.7, p99 +32.9) | 51.5 -> 56.9 (+5.4, p99 +8.6) | 42.2 -> 45.4 (+3.2, p99 +22.1) | 41.8 -> 44.8 (+3.0, p99 +21.0) | 16.3 -> 16.5 (+0.2, p99 +2.0) | 59.3 -> 60.0 (+0.6, p99 +5.7) | 16.7 -> 16.8 (+0.2, p99 +1.7) |
| ember | 68.8 -> 69.0 | 0.9 % | 0.0 % | 4.9 | 0.00 -> 0.00 % | 23.0 -> 23.9 (+0.8, p99 +5.7) | 28.3 -> 30.8 (+2.5, p99 +4.1) | 21.1 -> 21.7 (+0.6, p99 +4.7) | 19.0 -> 19.7 (+0.7, p99 +4.1) | 16.2 -> 16.4 (+0.1, p99 +1.6) | 49.5 -> 49.6 (+0.1, p99 +0.9) | 14.8 -> 14.9 (+0.1, p99 +1.3) |
| fog | 85.7 -> 87.7 | 11.1 % | 8.5 % | 78.0 | 0.00 -> 0.00 % | 45.6 -> 77.4 (+31.8, p99 +84.4) | 63.0 -> 75.1 (+12.0, p99 +18.1) | 66.5 -> 76.3 (+9.8, p99 +66.2) | 65.9 -> 73.9 (+7.9, p99 +53.3) | 50.7 -> 58.6 (+7.9, p99 +70.5) | 82.3 -> 84.8 (+2.6, p99 +16.1) | 39.6 -> 42.1 (+2.5, p99 +25.2) |
| haze | 67.0 -> 67.2 | 0.6 % | 0.0 % | 4.4 | 0.00 -> 0.00 % | 23.0 -> 23.8 (+0.8, p99 +4.6) | 39.0 -> 41.2 (+2.1, p99 +3.8) | 19.0 -> 19.6 (+0.6, p99 +4.1) | 16.2 -> 16.9 (+0.7, p99 +3.9) | 11.4 -> 11.5 (+0.1, p99 +1.2) | 48.1 -> 48.2 (+0.1, p99 +1.1) | 11.6 -> 11.7 (+0.1, p99 +1.0) |
| ice | 71.7 -> 72.1 | 4.5 % | 1.2 % | 11.3 | 0.00 -> 0.00 % | 28.5 -> 32.9 (+4.4, p99 +10.7) | 50.3 -> 54.8 (+4.5, p99 +7.4) | 37.9 -> 39.6 (+1.7, p99 +9.3) | 36.9 -> 38.7 (+1.8, p99 +11.5) | 12.7 -> 12.8 (+0.1, p99 +0.9) | 54.5 -> 54.7 (+0.3, p99 +2.8) | 13.9 -> 14.0 (+0.1, p99 +0.8) |
| poison | 69.6 -> 69.7 | 1.0 % | 0.1 % | 5.5 | 0.00 -> 0.00 % | 23.9 -> 24.4 (+0.5, p99 +4.9) | 42.1 -> 44.6 (+2.5, p99 +3.9) | 25.7 -> 26.4 (+0.7, p99 +5.3) | 21.9 -> 22.4 (+0.5, p99 +4.5) | 12.6 -> 12.6 (+0.0, p99 +0.6) | 49.9 -> 49.9 (+0.1, p99 +1.1) | 12.3 -> 12.3 (+0.0, p99 +0.4) |
| smoke | 70.1 -> 70.2 | 0.1 % | 0.0 % | 3.3 | 0.00 -> 0.00 % | 23.2 -> 23.2 (+0.0, p99 +0.5) | 3.7 -> 3.7 (+0.0, p99 +0.4) | 8.3 -> 8.5 (+0.2, p99 +2.1) | 2.5 -> 2.6 (+0.2, p99 +3.5) | 19.9 -> 20.0 (+0.1, p99 +1.2) | 51.3 -> 51.3 (+0.1, p99 +1.5) | 14.8 -> 14.8 (+0.0, p99 +0.4) |

The mask part 'right' is not the right wall's face: from this camera it is mostly the wall's 20 mm rear edge seen end-on
(a strip about 13 px wide at x 202-215, with a few stray pixels further right), so its mean mixes edge and background.
Eroded by 2 px (2,360 px left), the edge reads, today -> depth: Fog 24.8 -> 73.6, Dust 9.6 -> 28.6, Acid 13.4 -> 26.6,
Ice 6.5 -> 13.3 (L*).

Reading: the 20 mm edges, the frames and the grip opened up, in proportion to how pale and clear the tint is: Fog
most, Dust and Acid plainly, Ice a little, Ember, Haze and Poison only on the left grip (about +2.5), Smoke not at all.
At depth 12 the light ran out inside the thick acrylic and its edges rendered near black (the "black edge lines" were
cut paths). The paper and the horn's faces do not move, nothing pins, and the horn-pod moves only in Fog (+2.5).
