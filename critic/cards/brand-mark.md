# Card: the EARF mark set (round 27; after its round 1, `critic/rounds/2026-10-16/brand-mark-r1.json`)

## What it is for

EARF makes horn loudspeakers. Its Cloud line (Atmosphere 01 to 08) is cabinets of tinted cast acrylic, one colour
each: 01 Flare red, 02 Dust orange, 03 Acid amber, 04 Poison bottle green, 05 Ice blue, 06 Haze violet, 07 Fog clear
white, 08 Smoke black. The mark is the acrylic globe: a sphere's three parallels and three meridians as six discs,
tilted as the Earth is (its axis leaning 23.4 degrees, tipped 16 toward us, 22 until round 27f), each disc a thin slab of tinted acrylic,
see-through. This set is every version the brand prints, etches and shows: colour (the six tints together, on its
site, its look book, its boxes), black and white (one ink, flat: paper, print, an etch, an emboss; white out of dark
grounds and photographs), and one in each speaker's own tint (that speaker's page, its box, its corner). Sheet 1 is the
set, each version on the ground it shows on; sheet 2 seven of them at 300, 64, 32 and 16 px; sheet 3 the lockups with
the wordmark EARF; sheet 4 the spins, a frame every 0.4 s (round 27f: black and colour, steady); sheet 5 (round 27e)
the angle study, the tip since chosen.

## The owner's requirements, in their own words (fixed)

- "Let's go with the acrylic globe and have a color version, a black version, and a white version, and a version for
  each speaker" (round 27, 2026-10-16), and after this card's round 1: "I like discs for monochrome and acrylic for
  multicolor". So black, white and each speaker's own are the seamed discs, flat; the colour is the acrylic.
- After 27d trimmed the one-colour discs to the green disc: "I kind of like it untrimmed because it's true to the shape
  of the combined discs. Maybe the angle Is wrong. Maybe if we add a spinning animation like a top it will help."
  (round 27e)
- "the logo has to work in white only, black only, single color, multicolor and animated" (round 22)
- "The acrylic is meant to be a transparent version of the discs" and "For acrylic I was expecting each disc to have a
  little thickness to it" (round 25)
- Of a fill completing the circle: "this artificial green completing the circle shape that isn't one of the discs"
  (round 25: no fill; the globe is its six discs alone)
- "These don't feel minimal and polished enough." (round 24b)

## Fixed

The globe's geometry (parallels at 40 N, 0 and 40 S; meridians 60 degrees apart; the lean 23.44 and the tip 16, the owner's pick in round 27f, from 22); the
six discs alone, nothing filling the circle; the colour version as it is (round 25's acrylic: the green meridian
facing us the backing, a single disc its own flat colour, crossings stacked a step deeper; red north, blue the equator,
yellow south, green the meridian facing us, orange and violet the side meridians); the speakers' colours; the wordmark
EARF and the lockup's proportions; the grounds (paper #F2EFEA, ink #121114).

Chosen in round 27f: the tip 16 (sheet 5: the tips reach 0.04 of the radius past the front disc, against 0.07 at 22
and 0.02 at 10, where the parallels close toward lines; turning the globe on its axis only makes them reach further)
and the steady spin.

## The versions, and their parameters

- Black, white and each speaker's own (after round 1): the seamed discs, flat, each speaker's on the ground where it
  holds 3:1. Every piece shrunk by half of `seam` (0.035 of the radius) on every side, the outline's too, so no band
  runs round the outside (the owner: "The stroke around the monochromatic ones looks odd. Don't think we need it");
  pieces thinner than one and a half seams dropped; the tips kept, so the outline is the discs' own (round 27d trimmed
  every piece to the green disc; the owner liked it untrimmed). The acrylic's thickness is a crescent inside each
  disc's edge, its cells the discs' faces and crossings alone ("clipping on the multicolor one wherever there is
  overlap"). Small cuts widen the seam to 0.05, 0.08 and 0.10 for marks up to 64, 32 and 16 px.
- In motion (round 27e, new): the spin. The mark turns on its axis the Earth's way (the meridians round the pole, the
  parallels still), `rate` 45 degrees a second (a turn in 8 s), each loop `turn` 180 degrees (4 s: every coloured disc
  back in its place, so it loops without a seam and starts on the mark at rest), 30 frames a second, 720 px square
  with the mark's clear space, `clear` a quarter of its width, round it. Steady (the owner, round 27f): the top's
  version, its axis wobbling round a circle `wobble` 5 degrees across, moved the lean off the Earth's and is not made.
  In motion no piece is dropped (each narrows into its seam) and the scale back to the discs' width is the seam's own,
  so nothing pops between frames. Black and colour, as MP4 and WebM; sheet 4 is a frame every 0.4 s.
- In line (round 27i, new; the owner: "Can we also do stroke versions of these in addition to fill, or will that not
  work?"): every version again as strokes, beside the fills. In one colour the discs' visible edges, every piece the
  fill keeps outlined once, the outline too, `w` 0.05 of the radius, round joins and ends; in colour the six rims,
  see-through, in their colours, the far halves thinner (round 22's lines), `wc` 0.065 in front. At 64 px a heavier
  cut (0.07); below 64 px the fills' small cuts. Sheet 6 is the set in line.
- Round 1 judged the acrylic's own one-colour forms, kept in the code:
- Black and white (one ink, no tints): a point is inked where an odd number of discs cover it (parity: the discs
  cancel where they cross, as two films do in one ink), the discs as flat ovals. Tried and left: a solid ball cut by
  every disc's outline as a seam (`seam` 0.035 of the radius), which read as any globe icon.
- Each speaker's own tint: the discs as stacked sheets of that speaker's acrylic held up to the light. Every disc a
  line of sight crosses (its face, or its side) is one sheet passing T = c ^ (1 / `at`) of the light (c the tint, in
  linear light); where a disc's side is nearest it counts `side_extra` 1 sheet more. So `at` sheets make the speaker's
  own colour. `at` is 2 (Flare, Dust, Acid, Ice), or more for a dark tint, so that four sheets (the ball's broad middle,
  a third of it) are no darker than OKLab lightness `mid` 0.40, or than the tint itself where that is darker: Poison
  2.6, Haze 3.0, Smoke 4.0. Fog, its tint nearly clear: 0.3 (round 1: 0.5). Inside the ball the ground takes nothing,
  so a tint is the same on paper and on ink; Smoke is shown on paper, Fog on ink.
- The slabs: each disc `thick` 0.05 of the radius thick; its side, where we see it, a sheet deeper.
- Small cuts (round 1, new) of black and white: every inked part grown by `spread` (of the radius) for the largest
  size it is drawn at, then scaled back to the master's width: 0.035 up to 16 px, 0.025 up to 32 px, 0.02 up to 64 px
  (4.2, 8.5 and 17 mm in print); above 64 px the master. The lockups whose globe is that small use them too.
- Smallest sizes (round 1, new): the colour and the tints never below 24 px (6.4 mm) across; below it the small black
  (on light grounds) or white (on dark) stands in.
- Sheet 2 shows each version at 300, 64, 32 and 16 px as it is meant to be used (the small cuts at 64 px and under).

You may propose additions (kind "new"), with exact values.
