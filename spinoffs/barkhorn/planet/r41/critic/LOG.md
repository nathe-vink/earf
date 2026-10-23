# Planet EARF round 41: critic log

The owner, 2026-10-22: "Bar people: empty rooms, as round 39" and "Bar globe: the site's multicolour". One pass:
round 39's empty door-mother final, its shot file unchanged, with Mother EARF in the site's multicolour (round 33c's
globe as on the site's mother-globe.jpg: six discs in the speakers' tints, every rim glowing its colour, no core),
`r41/r41_colour.py`. The same 1.25 m, place, heading and light. No edge light: the colours read without it (a look at
rim glow 0.22 neared clipping, so the judged proof is at 0.14). Proof 1200 x 800, 128 samples, round 39's lens step.
Staged with `r41/r41_stage.py` (the card describes the multicolour globe and says the colours are the owner's choice).

| pass | frame | critic a | critic b | mean | if fixed | main notes |
|---|---|---|---|---|---|---|
| p1 | door-mother, multicolour | 5.0 | 5.5 | 5.25 | 7.0, 7.0 | the rims read as "thin neon tubes", "a rave", the discs' faces invisible (globe p95 201, clip 0.19 %); the coloured shadow on the wall the brightest large surface (median 142); the near floor a hard bright pool (the globe's spot spill); the altar pair dim; both ask rim glow 0.06 and the spot 85 to 110 W, narrower |

Read test: a render ("a large neon-ringed sphere"; "surfaces too clean, furniture repeats exactly").

| frame | ab (image 1 = round 39) | ba | result |
|---|---|---|---|
| door-mother, multicolour, against round 39's finals/door-mother (Smoke) | r39, clear | r39, clear | round 39 2–0 (information only: the colour is the owner's) |

The full-size condition (both critics at least round 39's 5.5, nothing new wrong) is not met: critic a 5.0, and both
name two new faults, the neon read of the rims and the coloured shadow as the brightest surface. No 2400 render.

## p2 (the coordinator: "exactly as both critics converged"; one more pass, no third)

Only three numbers changed (`r41_colour.py --p2`): rim glow 0.14 -> 0.06; the globe's hard spot 140 W, 30 deg -> 100 W,
20 deg. Measured on the proof: the coloured shadow on the wall [960,90,1060,470] median 142 -> 108.5 (no longer the
brightest large surface); the globe [610,0,880,285] p95 201 -> 165; the near floor [200,600,500,800] unchanged at 105,
so that pool is not the globe's spot (both p2 critics now place it on the Domes' downlights, not in this brief).

| pass | frame | critic a | critic b | mean | if fixed | main notes |
|---|---|---|---|---|---|---|
| p2 | door-mother, multicolour | 5.0 | 5.5 | 5.25 | 6.8, 7.0 | the rims still "neon hoops", the blue ring clips 1.5 %; the disc faces invisible; the near floor's hard white pool (the Domes); the altar dim; Orbs white discs; both ask rim glow 0.02 to 0.025 with the spot raised again so the faces carry the colour |

Read test: a render ("a colourful ring-sphere light sculpture"; "surfaces too clean, lighting too even").

| frame | ab (image 1 = round 39) | ba | result |
|---|---|---|---|
| p2 against round 39's finals/door-mother (Smoke) | r39, clear | r39, clear | round 39 2–0 (information only) |

Gate not met (critic a 5.0 < 5.5; the rims' neon read persists). Stopped, as briefed: no 2400 render, no third pass.

## p3 (the coordinator, an exception to the two-pass limit: both p2 critics' converged change, nothing else)

`r41_colour.py --p3`: rim glow 0.025, the globe's hard spot 135 W at 20 deg. Measured: the globe [610,0,880,285]
p95 165 -> 117; the blue ring [700,100,740,280] clip 1.5 % -> 0.01 %; the wall's coloured shadow median 110.

| pass | frame | critic a | critic b | mean | if fixed | main notes |
|---|---|---|---|---|---|---|
| p3 | door-mother, multicolour | 5.5 | 5.5 | 5.5 | 7.3, 7.0 | the rims still read as LED hoops, the faces dark (both ask rim 0.010 to 0.012 and the spot 220 W); the near floor (the Domes, left as briefed); flat concrete; repeated seats; the altar batts hot; the globe's top near the frame edge |

Read test: a render ("a sphere of coloured neon rings").

| frame | ab (image 1 = round 39) | ba | result |
|---|---|---|---|
| p3 against round 39's finals/door-mother (Smoke) | r39, clear | r39, clear | round 39 2–0 (information only) |

Gate met: both critics 5.5 (round 39's 5.5), and no fault new to this pass (every one is named in p1 or p2: the neon
read, the floor, the concrete, the seats, the altar, the globe near the top edge). So the 2400 final is rendered from
the p3 shot (192 samples, round 39's lens step), with 2400 and 1200 px JPEGs.
