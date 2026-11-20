# The house picture's edge lamps, per tint (2026-11-20)

Two low strip lamps, out of frame at the deck's height (1.0 m left, 1.5 m behind), send light into the deck's edges so
the acrylic carries its tint. Three levels were tested in every tint at 800 x 1000, glass shadows on: **none**, **a
tenth** (6 and 5 W/m2 at the deck) and **a third** (20 and 17). The frames are in `tests-2026-11-20/edge-rule/`.

## The rule (the coordinator, 2026-11-20)

Per tint, the lowest level at which:

- (a) no face of the deck reads brighter than the open floor beside it;
- (b) the deck still carries its tint: its front edge within about 6 L* of the Tropos front of the same tint, and its lit top not black.

From above: no edge lamps in any tint.

## What the measurements show

- From this camera the deck's front face is on the shadow side. Its median L* is 8 to 11 in every dark and mid tint at every level: the edge lamps light the inside of the deck, and the top face carries the tint.
- So (b) on the front edge alone is met only by Dust (a tenth), Haze (none) and Smoke (any level).
- For Ember, Acid, Poison and Ice no level meets (b). There the level is the one that brings the top face and the front edge closest to the Tropos front, and the gap is stated below.
- No level ever fails (a) except Fog at a tenth and at a third. There the deck glows brighter than the floor, as an edge-lit panel.

## Levels

| Tint | Level | Why |
|---|---|---|
| Ember | a third | (b) not met at any level: front edge 9 against the Tropos's 29.5; the top carries the red (median L* 17, C 17; 95th percentile 48) |
| Fog | a twentieth (3 and 2.5 W/m2) | the coordinator, 2026-11-20 18:27: the lowest that brings the front within 6 of the Tropos Fog (60.7) with no face brighter than the floor: front 56.1 (-4.6), brightest face 85.8 against the floor's 95.2. A thirtieth: 52.7 (-8.0). None: 35.7 (smoked glass). A tenth: brighter than the floor |
| Smoke | a third | the front is near the Tropos Smoke (6.0) at every level; nothing lifts it further. It reads as dark smoked acrylic, its top's highlights to L* 53 |
| Dust | a third | with the narrowed beams a tenth fell to front 34.8 (fails (b)); a third: front 46.1 against the Tropos's 43.4, brightest 67.1 against the floor's 94.5 (the coordinator, 2026-11-20 19:48) |
| Acid | a third | (b) not met: front 25.9 against 60.8; the top 60.5, C 56 |
| Poison | a third | (b) not met: front 9 against 39.1; the top 16.8, C 11 |
| Ice | a third | (b) not met: front 21.9 against 44.9; the top 38.3, C 88 |
| Haze | none | front 10.8 against 15.5 (within 6) |

## The numbers

- **front**: median L* and chroma over the deck's projected front face.
- **top**: median L* and chroma over the top face outside the record (95th percentile in brackets).
- **floor**: the open floor right of the deck.
- **Tropos front**: median over pixels with chroma over 40 (all pixels where under 20 % reach that).

```
ember: Tropos front L* 29.5 C 61.1 (chroma>40 share 0.34)
   none   front L* 11.2 C 2.9 | top L* 14.4 C 8.3 (95% 39.5) | brightest 39.5 vs floor 94.2 ok | front vs Tropos -18.3 off
   tenth  front L* 9.3 C 3.4 | top L* 15.8 C 13.4 (95% 41.5) | brightest 41.5 vs floor 94.5 ok | front vs Tropos -20.2 off
   third  front L* 8.9 C 3.6 | top L* 17.1 C 17.2 (95% 48.4) | brightest 48.4 vs floor 94.5 ok | front vs Tropos -20.6 off
fog: Tropos front L* 60.7 C 2.2 (chroma>40 share 0.00)
   none   front L* 35.7 C 2.7 | top L* 34.4 C 2.5 (95% 74.7) | brightest 74.7 vs floor 95.1 ok | front vs Tropos -25.0 off
   tenth  front L* 83.3 C 1.8 | top L* 83.4 C 1.9 (95% 95.4) | brightest 95.4 vs floor 94.8 BRIGHTER | front vs Tropos +22.6 off
   third  front L* 97.2 C 1.8 | top L* 97.1 C 1.8 (95% 98.6) | brightest 98.6 vs floor 94.8 BRIGHTER | front vs Tropos +36.5 off
smoke: Tropos front L* 6.0 C 1.3 (chroma>40 share 0.00)
   none   front L* 11.2 C 2.9 | top L* 13.8 C 2.8 (95% 44.4) | brightest 44.4 vs floor 94.8 ok | front vs Tropos +5.3 ok
   tenth  front L* 9.3 C 3.0 | top L* 14.0 C 2.5 (95% 49.6) | brightest 49.6 vs floor 94.7 ok | front vs Tropos +3.3 ok
   third  front L* 8.8 C 2.9 | top L* 16.2 C 2.4 (95% 53.0) | brightest 53.0 vs floor 94.7 ok | front vs Tropos +2.8 ok
dust: Tropos front L* 43.4 C 60.4 (chroma>40 share 0.59)
   none   front L* 19.3 C 28.1 | top L* 23.2 C 26.4 (95% 55.8) | brightest 55.8 vs floor 94.3 ok | front vs Tropos -24.1 off
   tenth  front L* 43.3 C 78.4 | top L* 47.3 C 72.5 (95% 66.1) | brightest 66.1 vs floor 94.5 ok | front vs Tropos -0.1 ok
   third  front L* 57.1 C 75.5 | top L* 60.5 C 62.2 (95% 71.0) | brightest 71.0 vs floor 94.5 ok | front vs Tropos +13.7 off
acid: Tropos front L* 60.8 C 60.1 (chroma>40 share 0.55)
   none   front L* 16.1 C 10.0 | top L* 27.4 C 22.1 (95% 66.3) | brightest 66.3 vs floor 95.0 ok | front vs Tropos -44.7 off
   tenth  front L* 21.3 C 21.4 | top L* 44.3 C 43.3 (95% 82.6) | brightest 82.6 vs floor 94.7 ok | front vs Tropos -39.5 off
   third  front L* 25.9 C 27.8 | top L* 60.5 C 55.9 (95% 91.3) | brightest 91.3 vs floor 94.7 ok | front vs Tropos -34.9 off
poison: Tropos front L* 39.1 C 58.4 (chroma>40 share 0.23)
   none   front L* 11.2 C 2.9 | top L* 15.0 C 6.2 (95% 40.9) | brightest 40.9 vs floor 95.2 ok | front vs Tropos -27.9 off
   tenth  front L* 9.3 C 3.4 | top L* 15.7 C 8.8 (95% 45.8) | brightest 45.8 vs floor 94.7 ok | front vs Tropos -29.8 off
   third  front L* 9.2 C 3.6 | top L* 16.8 C 11.3 (95% 54.4) | brightest 54.4 vs floor 94.7 ok | front vs Tropos -30.0 off
ice: Tropos front L* 44.9 C 48.2 (chroma>40 share 0.36)
   none   front L* 11.8 C 16.6 | top L* 18.8 C 19.4 (95% 52.4) | brightest 52.4 vs floor 95.3 ok | front vs Tropos -33.1 off
   tenth  front L* 16.2 C 61.0 | top L* 27.6 C 67.2 (95% 60.7) | brightest 60.7 vs floor 94.8 ok | front vs Tropos -28.8 off
   third  front L* 21.9 C 87.9 | top L* 38.3 C 87.9 (95% 64.0) | brightest 64.0 vs floor 94.8 ok | front vs Tropos -23.0 off
haze: Tropos front L* 15.5 C 68.5 (chroma>40 share 0.56)
   none   front L* 10.8 C 1.5 | top L* 12.8 C 14.0 (95% 39.0) | brightest 39.0 vs floor 94.6 ok | front vs Tropos -4.7 ok
   tenth  front L* 8.3 C 3.1 | top L* 15.1 C 33.0 (95% 41.5) | brightest 41.5 vs floor 94.5 ok | front vs Tropos -7.2 off
   third  front L* 7.8 C 5.9 | top L* 18.1 C 46.0 (95% 43.9) | brightest 43.9 vs floor 94.5 ok | front vs Tropos -7.7 off
```

## The beams narrowed (2026-11-20, evening)

The left lamp's beam grazed the deck's top and lit the glossy black arm base and the cue post (602 white px at the
arm's foot in Ember v2). Both lamps now stand at the deck's mid-thickness (z 79 and 80 mm) with beams of 1.5 and 1 deg
and 10 mm tall, so the beam stays inside the deck's 25.4 mm: 0 white px there in the Ember test at a third. The levels
above keep their names; the Fog numbers are measured with the narrowed beams (tests-2026-11-20/fixes/).

## The eight at full size, narrowed beams (2026-11-20, 19:45 to 19:53)

| Tint | Level | Front L* | Top L* (95 %) | Brightest / floor | Corners against the Tropos |
|---|---|---|---|---|---|
| Ember | a third | 9.0 | 14.0 (44.1) | 44.1 / 94.5 | within 0.3 |
| Fog | a twentieth | 55.4 | 52.3 (85.8) | 85.8 / 95.2 | within 0.5 |
| Smoke | a third | 8.8 | 11.5 (50.8) | 50.8 / 94.7 | within 0.3 |
| Dust | a third | 46.1 | 50.4 (67.1) | 67.1 / 94.5 | within 0.3 |
| Acid | a third | 23.1 | 46.2 (87.0) | 87.0 / 94.7 | within 0.4 |
| Poison | a third | 8.9 | 13.9 (50.0) | 50.0 / 94.7 | within 0.3 |
| Ice | a third | 17.2 | 27.8 (61.5) | 61.5 / 94.8 | within 0.3 |
| Haze | none | 10.3 | 11.8 (39.0) | 39.0 / 94.8 | within 0.4 |

The narrowed beams lowered the tops of Smoke, Acid and Ice by 5 to 14 against the old-beam tests; the coordinator kept
them as rendered (2026-11-20 19:48): Acid and Ice read as yellow and blue at a third, and the rule takes the closest
level where (b) cannot be met.
