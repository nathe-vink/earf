# Card: the EARF Planet ident (round 25)

## What it is for

EARF makes horn loudspeakers. One of its marks is the Planet: the Earth as a flat graphic (the continents in green on a
blue sea, the Americas facing the viewer) with a dish in the North Atlantic like the Death Star's, the dish drawn as a
loudspeaker seen from the front (the surround red, the cone orange, the dust cap yellow) and a small violet core at its
centre. The Planet ident is how the mark arrives: a violet meteor strikes the sea, and the strike makes the crater.
Then the planet moves aside and EARF appears beside it, as every EARF ident ends. It plays on the brand's site and in
its videos, on paper (#F2EFEA) and on ink (#121114). Sheet 1 is the ident on paper (frames picked at its moments),
sheet 2 on ink.

## The owner's requirements, in their own words (fixed)

- "For the planet, it would be cool if the purple was a meteor, creates white cloud, disperses into black wisps, then
  the crater is visible. The water ripples on impact too. Then the purple meteor can stay in the core." (round 25)
- "I like how the planet looks in black and white too." (round 25)
- The era: "More like late 90s early 2000s computer software animation and design." (round 21)
- "These don't feel minimal and polished enough." (round 24b) and "It doesn't seem fluid or quick enough." (round 23)
- Of the planet: "a death star with a slightly bigger divot" (round 24b); "a slightly larger divot is fine. And more
  earth on the outside." (round 25)

## Fixed

The planet's drawing (its land, sea, dish, sizes and colours); the hand-off every ident shares (the move aside over 0.5
s, EARF wiped out of the globe's rim over 0.45 s starting 0.1 s before the move ends, then a 1.3 s hold); the grounds.
Flashes stay under three a second (WCAG 2.3.1).

## How it moves, and its parameters

After round 1. Times in seconds from the start; sizes as shares of the planet's radius.

- The meteor: a violet disc (`PLANET.meteor` 0.09, round 1: 0.07) with a tail (`tail` 1.25, round 1: 0.85, violet
  holding to 0.45 of its length at 70 % and fading to nothing), from `from` (1.55, -1.3) radii away from the hit
  (upper right) to the hit, accelerating (its distance to go 1 - s^1.6); it strikes at `hit` 0.45.
- The knock: at the hit the whole planet moves `knock.dist` 0.04 along the meteor's path in `knock.out` 0.034 (cubic
  ease-out) and back over `knock.back` 0.133 (smoothstep).
- The cloud: eight white circles (`PUFFS`, shares of `cloud.size` 0.46) bursting from the hit over `cloud.grow` 0.04
  (round 1: 0.12).
- The wisps: from `wisps.start` 0.64 (0.72) over `wisps.dur` 0.55 (0.85), each puff turns from white to black over the
  first `dark` 0.18 of that time and draws out into two tapered wisps curling away, clipped to the planet (new), each
  moving out `drift` 0.45 (times 0.7 to 1.2), growing to 4.7 times its puff's radius long, thinning from 0.95 to 0.2 of
  it, fading from a quarter of the way.
- The crater: drawn from `wisps.start` (round 1: once the cloud was full), the dish as it rests, the violet core at its
  centre (the meteor, lodged).
- The thump (new): at `thump.at` 0.97 the cone, the dust cap and the core grow `thump.k` 0.15 about the core in
  `thump.out` 0.067 (cubic ease-out) and back over `thump.back` 0.1 (smoothstep); the surround stays.
- The ripples: three rings, `gap` 0.13 apart, each the dish's rim growing to 4.4 times its size over `dur` 0.65 (1.05),
  `width` 0.03 thinning to 0.4 of it, fading linearly to nothing, in the sea's blue 60 % of the way to white, on the sea
  only; all gone by 1.36, after which nothing moves on the planet (round 1: the ident's clock stopped at the move aside
  and froze the last ring, faint, into the lockup).
- The move aside starts at 1.19 (the wisps gone); the ident runs 3.34 in all.

You may propose additions (kind "new"), with exact values.
