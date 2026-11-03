# Tropos, horn A, against IEC 62368-1:2018/2023's stability tests (2026-11-03)

**Why this file:** since 2026-11-01 the base has been designed to a 20 % (at most 250 N) push at the top, up to 2 m. The coordinator's research (wf_a73d7898-d30; 57 claims checked against sources, 50 confirmed, none contradicted) found that rule does not apply to Tropos:
- The "2 m" is IEC 60950-1 clause 4.1.
- The "20 % in 8.6.2.2" is the superseded 2014 text, which allowed a 10° tilt instead anyway.

The text below is as the research read it. That was not from a licensed copy of the standard, so **a test lab's written pre-assessment is needed before anything is tooled.**

Numbers from `standard_2018.py` (`standard_2018.json`). The model is horn A, the default since 2026-11-03: the formed horn on the bronze posts, with the caldera, on the cabinet's own four M8 swivel feet, with no base. The mass and centre of mass come from the render models, as in `com.py`.

## The speaker

| | |
|---|---|
| mass | **72.6 kg** (MS3: more than 25 kg) |
| centre of mass | 533 mm up, 14 mm behind the middle, central side to side |
| top of the horn | 1.295 m |
| the horn's overhang past the cabinet | **none** (it sits inside 560 x 420 at every side) |
| front-mounted user controls, moving-image display | none (RC-5 remote, controls on the rear plate) |

## The clauses

| clause | test | applies to Tropos | result on its own feet |
|---|---|---|---|
| 8.6.2.2 | any one of: a 10° tilt; a 10° incline rotated 360°; or 13 % of the weight horizontally (at most 100 N) with 50 % down (at most 100 N), at 1.5 m or lower | yes (MS3, floor standing) | **passes**: it tips at 17.5° at the least (back), against 10° |
| 8.6.2.3 | 800 N down at 1 m or lower, on any surface at least 125 x 200 that could be stood on | yes: the cabinet's top, 560 x 420 at 0.892 m | **passes**: restoring at least 4.1 times overturning |
| 8.6.3 | a 10° tilt | yes | **passes**: 17.5° at the least |
| 8.6.5 | 20 % of the weight (at most 250 N) at the top, or a 15° tilt or incline instead | **no**: only MS3 with front-mounted accessible controls or a moving-image display, or equipment on a maker-specified stand (8.10) | would pass by the 15° tilt (17.5° at the least) |
| 8.10 | equipment on a stand the maker specifies or sells | only with a stand sold for it (the plate below) | the plate: 15° passes (below) |

## The numbers, on the cabinet's own feet

**Tilt to tipping.** The arm is the centre of mass's distance inside the tipping edge; it tips when tan(angle) = arm / 533 mm.

| edge | feet centres: arm, tips at | pad edges: arm, tips at | 10° | 15° |
|---|---|---|---|---|
| back | 168 mm, **17.5°** | 188 mm, 19.4° | pass | pass |
| forward | 202 mm, 20.8° | 222 mm, 22.6° | pass | pass |
| left / right | 230 mm, 23.4° | 250 mm, 25.1° | pass | pass |

The feet centres are the conservative edge: a swivel base pivots on its ball.

**The 13 % option** (92.6 N at the horn's top, 1.295 m, below 1.5 m), restoring over overturning, without the downward part, which only helps:
- forward 1.2;
- back **1.0**, just;
- sides 1.37.

It is not needed: the 10° tilt already satisfies 8.6.2.2.

**The old 20 % reading,** for the record: 142 N at the top would tip it back (0.65). That is why the wide plinth was drawn; under the 2018 text it is not required.

**800 N on the top** (0.892 m). The top's edge reaches past the feet's line by 25 mm front and back and 50 mm at the sides:

| edge | overturning | restoring | ratio |
|---|---|---|---|
| front | 20 N m | 144 N m | 7.2 |
| back | 20 N m | 119 N m | 6.0 |
| sides | 40 N m | 164 N m | 4.1 |

The horn's top is above 1 m and is not a surface to stand on.

**A 5° tilt back on the feet** (a speaker leaned back, or set back on its levelling feet): the arm to the back feet falls from 168 to 121 mm. It still tips only at 17.5° from upright, 12.5° more.

## On a slim light plate (a separately sold stand, 8.10)

The plate's numbers are an estimate until it is drawn (`variants/BASES.md`). It has the cabinet's footprint, 560 x 420, is 50 mm tall and weighs 5.6 kg, with its feet 20 mm in from its corners. The speaker with the plate weighs 78.2 kg, with its centre of mass 543 mm up.

| edge | plate feet centres: arm, tips at | plate edges: arm, tips at | 8.6.5 by 15° tilt | 8.6.3 at 15° |
|---|---|---|---|---|
| back | 174 mm, **17.8°** | 194 mm, 19.6° | pass | pass |
| forward | 206 mm, 20.8° | 226 mm, 22.6° | pass | pass |
| left / right | 260 mm, 25.6° | 280 mm, 27.3° | pass | pass |

**What this means:**
- Tropos passes on its own feet. The wide plinth is not needed for the standard, so a base can be optional.
- On the slim plate it passes the stricter stand test (8.10, 8.6.5) by the 15° tilt, with 2.8° to spare at the feet centres and 4.6° at the plate's edges.
- To confirm with the lab's pre-assessment: the clause readings, and whether the swivel feet's ball or the pad edge is the tipping edge.
