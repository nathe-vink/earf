# Card: the EARF ident (round 25, after critic round 3)

## What it is for

EARF makes horn loudspeakers. Its mark is a 3D globe: three parallels (40 N, the equator, 40 S) and three meridians, 60
degrees apart, the axis leaning 23.4 degrees (the Earth's) and tipped 22 degrees toward the viewer. In colour each of the
six rings is a flat disc in one colour, flush, no strokes, the discs crossing as slotted sheets would: the equator blue,
the meridian facing the viewer green, north red, south yellow, the two side meridians orange and
violet. The ident is the globe arriving, then it moves aside and EARF appears beside it. It plays on the brand's site
and in its videos, on paper (#F2EFEA) and on ink (#121114). Styles: discs (the default), acrylic (the discs
see-through) and lines (each ring a stroke, for one colour).

## The owner's requirements, in their own words (fixed)

- The era: "More like late 90s early 2000s computer software animation and design." (round 21)
- The coin's brief: "A spinning disc silhouette that looks like a coin spinning. It can flash each color and eventually
  become a globe." (round 21) and "The coin was still supposed to flash between all colors first." (round 25)
- "Instead of them being drawn, what else can we try?" and "It doesn't seem fluid or quick enough." (round 23)
- "The gyroscope is too chaotic." "The coin spin still has an animation between the coin spin and tilt." "These don't
  feel minimal and polished enough. I'm still open to other ideas." (round 24b)
- "Still not loving anything ... Keep spitballing ideas and refining." (round 25)
- Each ident ends on the whole globe, upright, and then it tilts to the Earth's 23.4 degrees. (round 24)
- No fill completing the circle: the globe is its six discs alone ("this artificial green completing the circle shape
  that isn't one of the discs"), and in acrylic each disc has "a little thickness" (round 25, after round 3)

## Fixed

The globe's geometry, colours and styles; the wordmark; that the globe moves aside and the name appears beside it; the
grounds. The coin's flashes stay under three a second (WCAG 2.3.1: each swaps a large area between the ground and a
colour).

## The idents and their parameters

The sheets (round 3): 1 Coin (discs, on paper; its frames picked at the faces and one edge-on moment, 0.68 s), 2 Open,
3 Roll, 4 Coin (acrylic, on ink). After round 3 a storyboard of Iris joins them. Round 2 advised keeping these three and retiring the Gyroscope, Earthrise and Download; the
owner decides, so those stay on the page and are not judged here. Times in seconds.

- Every tilt (shared): `TILT.dur` 0.3 (round 3: 0.4), leaning a little past 23.4 degrees and settling: `TILT.keys` (share of the time,
  share of the lean) (0, 0), (0.55, 1.12), (0.8, 0.98), (1, 1), each reached smoothly. Each ident's tilt starts `lap`
  before its arrival ends.
- The hand-off (its timings may change): it holds `HOLD` 0 (round 3: 0.1; round 2: 0.35), moves aside over `MOVE` 0.5 (smooth), and EARF is wiped
  out of the globe's right rim, left to right, over `WIPE.dur` 0.45 (cubic ease-out), starting `WIPE.lead` 0.1 before
  the move ends (round 3: 0; round 2: 0.15); then it holds 1.0 (`REST`; round 26: 1.3, the owner chose 1.0). (Round 1 typed the letters in, four one-frame jumps.)
- Coin: it spins on its edge about the vertical from edge on, a new face each half turn at one steady speed:
  `COIN.half` 0.34 (each colour's half turn), six colours round the colour wheel (yellow, orange, red, violet, blue,
  green), then it lands on the globe (whose facing disc is green) over a quarter turn, `COIN.land` 0.51 (cubic ease-out, its
  speed at the start the colours' own). Its rim shows its thickness, of the radius, in the face's
  colour, flat (`COIN.thick` 0.14, round 2: 0.07). `COIN.lap` 0.3 (round 3: 0.25; round 2: 0.15). In acrylic each face is its colour
  (a single sheet shows its own colour), the globe it lands on the acrylic (see-through discs on a green backing); in
  lines, rings.
- Gyroscope: the globe spins on its own axis, the three meridians turning about the pole (the parallels stay), slowing
  to rest (quadratic ease-out; cubic until the acrylic critic's round 3 found it spent by half time). `GYRO.spin` 1.0,
  `GYRO.turns` 0.5, `GYRO.lap` 0.3 (0.2).
- Earthrise: the whole globe rises from behind a horizon (the bottom of the globe's own resting place), slowing as it
  clears it (cubic ease-out). `RISE.up` 1.2, `RISE.from` 2.3 (radii below its rest), `RISE.lap` 0.25.
- Open: the globe begins as the flat globe icon, each disc edge on (a line); each turns about its line and opens into
  its disc, a beat after another (equator, the facing meridian, the side meridians, the parallels), cubic ease-out
  each. Until a disc is `OPEN.whole` 0.3 open it is drawn whole in front, as
  one band, with its edge (the line's width times what is left of the 0.3). `OPEN.lead` 0.3 (round 3: 0.12), `OPEN.each` 0.65 (round
  2: 0.4), `OPEN.stagger` 0.04 (0.07), `OPEN.lap` 0.3 (round 3: 0.4; round 2: 0.2).
- Roll (new, from round 1): the globe rolls in from the right like a ball, upright, turning as it travels (its turn its
  distance over its radius), slowing evenly to a stop at its place (quadratic ease-out), then rocks back into its lean.
  `ROLL.roll` 0.9, `ROLL.from` 3.7 (radii right of its rest), `ROLL.lap` 0.
- Iris (new, from round 3): the finished globe, upright, still and full size at its place, revealed through a circle
  opening from its centre to its own outline (cubic ease-out on the radius); nothing inside moves or scales, and the
  circle has no stroke. The lean starts `IRIS.lap` 0.1 before it is open. `IRIS.open` 0.3.
- Download (new): the globe arrives as a picture did over a modem in 1999, an interlaced GIF: coarse blocks at once,
  then each pass finer (the blocks halving), every pass sweeping down over the last, until it is sharp; then it tilts.
  `LOADGIF.passes` 1/4, 1/8, 1/16, 1/32 (block sizes, of the radius), `LOADGIF.each` 0.2, `LOADGIF.lap` 0.1.

You may also propose a new ident (kind "new"): what it shows, frame by frame, with timings, in the brand's terms. Say
which two or three idents the brand should keep.
