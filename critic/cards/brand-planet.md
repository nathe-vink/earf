# Card: the EARF Planet ident (round 26)

## What it is for

EARF makes horn loudspeakers. One of its marks is the Planet: the Earth as a flat graphic (the continents in green on a
blue sea, the Americas facing the viewer) with a dish in the North Atlantic like the Death Star's, the dish drawn as a
loudspeaker seen from the front (the surround red, the cone orange, the dust cap yellow) and a small violet core at its
centre. The Planet ident is how the mark arrives: a violet meteor strikes the sea, and the strike makes the crater.
Then the planet moves aside and EARF appears beside it, as every EARF ident ends. It plays on the brand's site and in
its videos, on paper (#F2EFEA) and on ink (#121114), in colour. (Black and white is the still figure's: the ident is not
animated in it.) Sheet 1 is the ident on paper (frames picked at its moments), sheet 2 on ink.

## The owner's requirements, in their own words (fixed)

- "For the planet, it would be cool if the purple was a meteor, creates white cloud, disperses into black wisps, then
  the crater is visible. The water ripples on impact too. Then the purple meteor can stay in the core." (round 25)
- "You gotta really spruce up that planet animation. Pixar quality baby. Or at least early Disney" (round 26)
- Round 25's thump (the cone thumping once after the smoke): "Drop it" (round 26).
- "I like how the planet looks in black and white too" (round 25). Asked whether to add a black-and-white Planet, "Yes,
  add black and white", and then: "The black and white doesn't need to be animated" (round 26). So the ident is in
  colour only, and black and white stays the still figure.
- "These don't feel minimal and polished enough." (round 24b) and "It doesn't seem fluid or quick enough." (round 23)

## Fixed

The planet's drawing (its land, sea, dish, sizes and colours); the ident in colour only; the hand-off every ident
shares (the move aside over 0.5 s, EARF wiped out of the globe's rim over 0.45 s starting 0.1 s before the move ends,
then a 1.0 s hold, 1.3 until the owner shortened it in round 26); the grounds; flat colour (no gradients or fades on the planet). Flashes stay under three a second (WCAG 2.3.1).

## How it moves, and its parameters

After round 2 (`critic/rounds/2026-10-16/brand-planet-r2.json`). Times in seconds from the start; sizes as shares of
the planet's radius. The animators' principles, one by one.

- The twinkle (staging, anticipation): a four-point violet sparkle with a lesser one across it (`star.size` 0.15) pops
  in at `star.at` 0.04 over `star.pop` 0.16, spinning in, past its size and back; its long rays reach out 1.55 times at
  `star.ting` 0.24; where the meteor will start, upper right.
- The wind-up: from `wind.at` 0.24 (round 1: 0.34), on the glint, over `wind.dur` 0.1 (0.12) the meteor (a violet
  ball, `meteor` 0.12 (0.085), its leading face a lighter violet) grows out of the sparkle, which shrinks away, and
  draws back `wind.back` 0.1 along its path, squashed to 0.65 along it.
- The fall (arcs, slow in, stretch): on a quadratic arc from `from` (1.36, -0.98) radii from the hit, bowed `bow` 0.14
  of its chord up to the left, the distance gone u = s^`ease` (1.8; round 1: 2.4, which left it at its start until
  halfway) so it speeds up all the way; stretched along its
  path 1 + `stretch` (1.5) times its speed share, thinned to keep its area; a flame behind it along the arc: an outer
  ribbon in light violet, 2.3 times the ball wide and `tail` 0.95 long at full speed, an inner one in violet 1.4 wide
  and 0.6 as long, both tapering, their edges flickering; eight sparks shed along the path, drifting off and shrinking
  over 0.22.
- The splat: for `contact` 0.034 before `hit` 0.62 (0.72) (one frame at 30 fps) the ball sits on the hit, squashed to 0.5
  along its path and 1.55 across.
- The starburst (timing): at the hit, for `flash` 0.06 (two frames), a nine-point star 0.5 across in Fog white with a
  pale yellow star inside, the second frame 0.72 the size. One flash.
- The planet (follow-through): squashed along the blow by `squash.k` 0.075 (stretched across by 0.6 of that) on a
  damped spring (`hz` 3.4, `damp` 6.5 a second), starting at full squash; and knocked along the blow `knock.dist` 0.07
  times a damped sine (`hz` 2.8, `damp` 7.5), so it goes out about 0.04 and back past rest.
- The shock: one thin Fog ring (`shock.width` 0.012, thinning to nothing as (1 - p)^1.5) on the sphere, from the
  dish's rim to `shock.to` 1.0 radians from the dish's axis (1.95: a hairline inside the limb) over `shock.dur` 0.28
  (0.34) (cubic ease-out), over land and sea.
- The ripples (solid drawing): `ripples.n` 3 rings on the sea only, `gap` 0.15 apart, each from the dish's rim to
  `to` 0.9 radians (1.3) over `dur` 0.55 (0.85), a light crest (the sea's blue 60 % of the way to white) with a dark trough inside it
  (28 % of the way to ink), `width` 0.024 thinning to nothing; drawn as circles on the sphere, so they foreshorten.
- The cloud (overlapping action): eleven puffs (`PUFFS`, shares of `cloud.size` 0.5: five fat ones round the edge at
  15, 85, 160, 225 and 300 degrees (round 1: a ring of eight small ones, read as beads), five inside, one in the middle), each popping in over `cloud.pop` 0.15, past its size and back, a beat later the
  further it is from the middle (`stagger` 0.06 a cloud size); the whole drifting out `drift` 0.16 over 0.7 and
  boiling (`boil` 0.035 at 1.7 Hz); each puff lit from the upper left: its shadow (a cool white-blue) and its lit part
  over it (0.86 the size, moved up and left), so the cloud is two tones.
- The char: from `char.start` 1.02, a front from the middle out reaches each puff over `char.dur` 0.12; each turns
  over `char.turn` 0.07, through a beat of a middle tone to flat Smoke (#34323A), swelling 12 %.
- The smoke (the wisps): from `smoke.after` 0.05 after it begins to char, each puff is eaten over `smoke.eat` 0.3 (0.42)
  (smoothstep) by a growing circle biting in from its inner side (from 0.5 of its size, 1.5 away, to 1.6, 0.55 away),
  the circle's side turning `smoke.swirl` 0.9 radians as it goes, while the smoke drifts out `smoke.drift` 0.22: so a
  hole opens at the middle first, over the crater, and the last of the smoke is crescents curling round it, thinning
  to nothing. The middle puff is eaten from its centre. The last is gone by 1.49; the clean crater then holds
  `smoke.hold` 0.12 (new) before the move aside.
- The crater: from `crater.at` 1.15 its rings spring open one by one, `stagger` 0.055 apart, each over `pop` 0.2 past
  its size and back, then wobbling `wob` 0.05 (`hz` 3.0, `damp` 5); the bowl sinks past its depth by `sink` 0.5 and
  settles; then the core (the meteor) drops in 1.55 times its size and bounces to rest, white-hot (Haze 80 % of the way
  to white), cooling to violet over `ember.cool` 0.7.
- The move aside starts at 1.61 (the crater clean since 1.49); the core's cooling finishes during it; the ident runs
  3.46 in all.

You may propose additions (kind "new"), with exact values.
