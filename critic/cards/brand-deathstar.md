# Card: the EARF globe as a Death Star (round 25)

## What it is for

EARF makes horn loudspeakers. Alongside its main mark (a 3D globe of six coloured discs) it is exploring a second
figure for the speakers: the globe as a Death Star whose dish is a loudspeaker driver seen from the front (its surround
red, its cone orange, its dust cap yellow: the Earth's hot core showing through), in flat colour, no strokes. It kicks
like a speaker in animation. It must also work in one colour (black only, white only).

## The owner's requirements, in their own words (fixed)

- "The speaker cross section is too big and has too much detail. I was thinking more like a death star with a slightly
  bigger divot. These don't feel minimal and polished enough." (round 24b)
- "Keep exploring. And a slightly larger divot is fine. And more earth on the outside." (round 25)

## Fixed

The palette (red #D2382F, orange #E5732A, yellow #E9B320, green #4F7F3A, blue #4A90C8, violet #6C4BA3, and the grounds
paper #F2EFEA and ink #121114); the dish as a driver in red, orange and yellow; flat colour without strokes.

## What is on the sheets, and its parameters

Sheet 1: the figure on paper and on ink, and in black only and white only (drawn by knock-outs: the disc solid, the land
and the dish's surround and dust cap knocked out to the ground, the cone solid). Sheet 2: every cut at 300, 64, 48, 32, 24
and 16 px: the full figure (for 49 px and up), the mid cut (25 to 48 px: only the land pieces of at least `MID` of the
disc, the two Americas) and the small cut (24 px and under: the disc and the dish, no land), in colour and in black.
Sheets 3 and 4: the kick, frame by frame, on paper and on ink, its frames picked round the beat.

- `DISH.ang` 24 degrees (its angular radius); `DISH.at` (0.32, 0.34) (its centre on the face, of the radius; round 2 moved
  it in from (0.40, 0.36)); `DISH.depth` 0.42 (how deep, of its radius: the inner rings sit off centre toward the middle)
- `RINGS` surround 1.0, cone 0.70, dust cap 0.40 (of the dish's radius); `LEAN` 8 degrees (the figure's lean; round 2: 18)
- `LAND.view` (-65, 12) (the longitude and latitude at the face's centre); `LAND.round` 0.05; `LAND.clear` 0.06 (the land's
  distance from the dish's rim, and in one colour from the limb); `LAND.min_piece` 0.015
- `MID` 48 px and 0.06 of the disc (the mid cut); `SMALL` 24 px (the cut without land)
- The kick: `CORE.beat` 1.0 s. The push, over 0.06 s (cubic ease-out): the dish's depth 0.42 to 0 (the rings concentric),
  the dust cap 1.2 times larger (`CORE.cap` 0.2), the whole driver 1.05 times about its centre (`CORE.throw` 0.05); held
  to `CORE.hold` 0.13 s; back through an overshoot (depth 0.50 at 0.24 s) to rest by `CORE.rest` 0.42 s. `CORE.ring`
  0.04 to 0.45 s: one ring of sound knocked out of the globe in the ground's colour (seen only where it crosses the
  globe), the rim's shape, growing to 2.5 times the dish (cubic ease-out), its width 0.05 of the radius thinning to
  nothing; then still until the next beat.
- Options for the owner, not shown: the violet cap at the dish's centre; the equator's trench in violet.

Say what holds the figure back from shipping, and prescribe the changes to it.
