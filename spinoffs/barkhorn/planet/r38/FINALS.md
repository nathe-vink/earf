# Planet EARF, round 38 finals (in Smoke)

The owner on round 37 (verbatim, through the lead): "Planet: Smoke, ledge at counter height".

Six frames at 1200 x 800, 256 samples, in `renders/2026-10-20/barkhorn/planet38/finals/`; the sheet
`planet38-smoke.png`. Two fresh critics each (blind stage-1 scores; `critic/`), and a read test each from a judge told
nothing (`finals-readtests.json`).

| Frame | Median | Critics | Mean | If fixed |
|---|---|---|---|---|
| bar-smoke | 32.2 | 5.0, 5.5 | 5.25 | 7.5, 7.5 |
| coins-decks | 40.5 | 5.0, 5.0 | 5.0 | 7.0, 7.5 |
| listening-smoke | 31.7 | 4.5, 4.5 | 4.5 | 7.0, 6.5 |
| street | 30.4 | 5.5, 5.5 | 5.5 | 7.5, 7.3 |
| sink | 53.4 | 5.0, 5.0 | 5.0 | 7.0, 7.0 |
| coins-door | 12.2 | 4.5, 4.5 | 4.5 | 7.0, 7.0 |

Shared notes, all frames: the speakers' Smoke cabinets read dark against what lights them (bar 26-37, listening 20-21);
denoiser smear and repeated textures (fir, fluted oak, spines); no sign of life where the camera looks. Per frame:
the bar's record-wall concrete is the brightest, coolest flat; the column's coins read dark with a cold LED sliver; the
listening niche's fir clips above the pair and the near Orb blows (18 %); the street has no glass or name and a clipped
disc; the sink's bowl is crushed and its slab cropped; the door frame is underexposed (12) and its coins lie in one
ring, not a heap.

## r38b, the fix pass (2026-10-21)

The lead's fix list, the companions Orb level (0.8 shade glow, 3.0 W, #FFDCB8, flavour gains) and 384 samples at
scale 0.5 in `finals-b/`; two fresh critics each (`critic-b/`) and a read test each (`finals-b-readtests.json`).
The stop rule per frame keeps the better of r38 and r38b; the chosen frames and the sheet are in `finals-best/`.

| Frame | r38 median | r38 critics (mean) | r38b median | r38b critics (mean) | Kept |
|---|---|---|---|---|---|
| bar-smoke | 32.2 | 5.0, 5.5 (5.25) | 25.9 | 5.5, 4.5 (5.0) | r38 |
| coins-decks | 40.5 | 5.0, 5.0 (5.0) | 39.3 | 5.0, 5.0 (5.0) | r38b, tie: carries the fixes |
| listening-smoke | 31.7 | 4.5, 4.5 (4.5) | 19.0 | 4.5, 4.5 (4.5) | r38b, tie: fir and Orb no longer clip |
| street | 30.4 | 5.5, 5.5 (5.5) | 22.6 | 5.0, 5.0 (5.0) | r38 |
| sink | 53.4 | 5.0, 5.0 (5.0) | 85.8 | 5.0, 5.0 (5.0) | r38b, tie: read as black glass |
| coins-door | 12.2 | 4.5, 4.5 (4.5) | 25.8 | 4.0, 4.5 (4.25) | r38 |

r38b read tests: the sink "a glossy black block, probably black glass or lacquered or polished stone"; the column
"a stack of red, black and white coins or tokens"; the door "hammered copper or bronze bowl holding about a dozen
coloured coins or tokens".

Still open: the kept sink is overexposed (85.8; both critics ask about a stop down) and has no contact shadow; the
door's coins lie in a ring, not a heap; the street's Orbs read cyan and the etch reads as a pink overlay; the bar's
record wall reads empty; the speakers still read dark against what lights them.
