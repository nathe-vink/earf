# In-frame card audit, 2026-11-03 (the coordinator, 23:39 UTC)

## Method

`tools/cardcast.py <shot.json> [extra_cards.json]` casts rays across the frame and records which rays hit each reflect-only
card's rectangle (`set.flags` with `reflect_only`).
- Rays are cast every `max(W,H)/240` px.
- Sensor: 36 mm on the frame's larger side, with the lens shift applied.
- A card counts as IN FRAME if any ray hits it. The share of rays that hit is the part of the picture a real card there would block.

`shots.py _in_frame` tests points only: the corners and the centre. A large card close to the camera can have all five points
outside the frustum while its middle crosses the frame. Every case below is one of those.

`tools/rigaudit.py < shot.json` lists every lamp and flags the following:
- ruling 2: a linked spec-only lamp, or a scoped flag
- ruling 3: `transmission: False`
- ruling 4: `set.cast_shadow: false`
- every reflect-only card, as a reminder to ray-cast it

## Results (rendered rigs on r33-rollout-c2/c3/c4 and r33-speaker-horn, read 23:3x)

| Rig | Card (centre, size, normal) | Share of frame |
|---|---|---|
| deck-hero (c3 569006681818, final) | [1.76,-1.32,1.2] 2.2x2.2 [-0.8,0.6,0] | 15.9 % (19.9 % without the lens shift) |
| deck-hero (older copy on c2/c4) | same family | 30.9 % |
| site-front-off-tall x7 (phase 1) and fix1 tall acid, poison, ice, haze, fog | [1.6,-1.2,1.2] 2.0x2.0 [-0.8,0.6,0] | 34.1 % (x 655-995 of 1000) |
| base-question/gate2 A-ice-polished and A-ice-polished-honest (f7f03850) | [1.6,-1.2,1.2] 2.0x2.0 [-0.8,0.6,0] | 34.1 % |
| site-front-off-wide x7 (phase 1) | [1.6,-1.2,1.2] 2.0x2.0 [-0.8,0.6,0] | 46.6 % |
| site-front-off-wide x7 (phase 1), second card | [1.8,2.7,1.3] 3.0x2.6 [-0.37,-0.93,0] | 9.1 % |
| site-front-off-wide x7 (phase 1), third card | [1.6,1.8,0.005] floor card | 2.2 % |
| fix1 front-off-wide x7 | [2.24,-1.68,1.2] 2.8x2.8 [-0.8,0.6,0] | 43.8 % |
| fix1 side ember, dust, acid, poison | [1.526,-1.152,0.5] 2.34x1.69 [-0.829,0.56,0] | 100 % (between the camera and the speaker) |
| site-back x7 (phase 1) | [-0.8,0.3,0.9] 1.6x2.2 [0.66,-0.76,0] | 44.9 % |
| round 2's new overhead card (f6d0eda7) in tall, wide, side | [0,-1,2.2] 2.0x1.2 [0,0.42,-0.91] | 0.0 % (out) |

No card is in frame in any of these:
- deck-row (both)
- deck-cover
- deck-home-portrait (both)
- phase-1 side x7
- hero-light x7
- horn-back x7
- amp-plate-ember
- inside-ice
- turn-ember 00-04
- horn-closeup A polished and satin (a381aefb)

Rulings 1 and 2 by the lamp audit:
- `edge`: linked to six parts in the deck hero, gate2 A-ice-polished(-honest) and the horn close-ups.
- The horn close-ups (a381aefb), which predate the rulings, also have `horn` at specular 0.3, and `back` and `kick` linked to the
  product's parts.
- The deck cover's key is a sun through the paper (`cast_shadow: false`): ruling 4.

## What it means

- No picture with an in-frame card can be shown or swapped in. That includes tall Ice and tall Fog (fix1), which passed 3/3 at 22:5x.
- Each card has to go out until it covers 0.0 % by this test, or be removed. Its honest residue (a face mirroring the bright set) is
  then answered by real means: a darker set or sweep on that side, real flags just outside the frame, or another camera angle.
