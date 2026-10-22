# Planet EARF round 40: critic log

Blind critics (critic/PROMPT-interiors.md, staged by `r40/r40_stage.py`, a fresh context each, the image and its card
only); read tests (the images only); duels against round 39's best per frame (critic duel prompt, two judges with the
order swapped; ab: image 1 = round 39). Verbatim JSON beside this file.

| pass | frame | critic a | critic b | mean | if fixed | main notes |
|---|---|---|---|---|---|---|
| p1 | door-mother | 6.0 | 5.5 | 5.75 | 7.5, 7.0 | ghosts translucent double copies; the altar pair clipped; the right wall and screens brightest; the globe's spot reads as daylight; floor crackle and hard polygon shadows; haze veil |
| p1 | bar | 5.0 | 5.0 | 5.0 | 7.0, 7.5 | ghosts in front of both speaker niches; white card at the left horn; Domes near clip; zinc reads as plaster (177) |
| p1 | listening | 5.5 | 5.0 | 5.25 | 7.3, 7.0 | the guest a big translucent ghost near the lens; the foreground chair crushed; the left speaker under-lit; batts near white; no shell in frame |

Read test p1: all three called renders ("blurred people ... ghostly blobs with no real anatomy", "smudged placeholder
shapes", "a translucent smear").

Duels p1 against round 39's best:

| frame | round 39 entry | ab | ba | result |
|---|---|---|---|---|
| door-mother | finals/door-mother (at 1200) | r39, slight | r39, clear | round 39 2–0 |
| bar | proofs-p2/bar | r40, clear | r40, slight | round 40 2–0 |
| listening | proofs-p3/listening | r40, clear | r40, slight | round 40 2–0 |

p2a (proofs-p2 at its first commit) was not judged: with the blur cut to a few centimetres the figures read as smooth
dummies with ball heads (seen before staging). p2 below is p2b: the bodies a little softer, the heads always smeared,
the door on a full shutter, the Core nearest the lens dimmer.

| pass | frame | critic a | critic b | mean | if fixed | main notes |
|---|---|---|---|---|---|---|
| p2 | door-mother | 4.5 | 5.5 | 5.0 | 6.5, 7.3 | figures "translucent grey mannequins"; the altar batts clip; the globe a black wire cage; zinc and the near floor brightest; Orbs cold white |
| p2 | bar | 4.5 | 4.5 | 4.5 | 6.8, 6.5 | figures "pale mannequins ... the brightest mass"; the white wedge in the left niche; zinc plaster; Domes white bowls |
| p2 | listening | 4.5 | 4.5 | 4.5 | 6.5, 6.8 | dead-centre frontal camera; flat white batt squares; the near Orb a grey disc on the axis; floor and chairs crushed; no shell |

Read test p2: all three renders ("faceless mannequins", "smooth, featureless blurred shapes", "flat white placeholder blocks").

| frame | ab | ba | result |
|---|---|---|---|
| door-mother | r39, clear | r39, clear | round 39 2–0 |
| bar | r39, clear | r39, clear | round 39 2–0 |
| listening | r39, clear | r39, clear | round 39 2–0 |

p2 is worse than p1 everywhere. The procedural figures are the binding limit: sharp, they read as mannequins; blurred,
as composited ghosts. p3 (the last round per frame) goes back to p1's framing, keeps the figures few and dark, in shadow.

| pass | frame | critic a | critic b | mean | if fixed | main notes |
|---|---|---|---|---|---|---|
| p3 | door-mother | 5.0 | 5.0 | 5.0 | 6.8, 7.0 | the altar dim; the globe a black cage; floor brightest with hard shadows; Orbs white plates; figures "grey clay" |
| p3 | bar | 4.5 | 4.5 | 4.5 | 6.5, 7.0 | figures "grey untextured clay mannequins"; white wedge in the niche; zinc a flat grey plane |
| p3 | listening | 5.0 | 4.0 | 4.5 | 6.8, 6.5 | the guest a mannequin with floating legs; the near chair crushed; floor flat; speakers darker than the fir |

Read test p3: all three renders ("smooth featureless mannequins").

| frame | ab | ba | result |
|---|---|---|---|
| door-mother | r39, clear | r39, clear | round 39 2–0 |
| bar | r39, clear | r39, clear | round 39 2–0 |
| listening | r39, slight | r39, clear | round 39 2–0 |

Three rounds per frame reached. No frame reached 6 on both critics, so none was rendered at full size. Kept per frame:
door, round 39's finals/door-mother (it won every duel); bar and listening, round 40's p1 proofs (they beat round 39's
best 2–0; no later pass beat them).

## The edge-light test (the coordinator, approved as render lighting: one pass)

Round 39's empty door-mother final, its shot file unchanged, plus one narrow spot on Mother EARF (`r40/r40_edge.py`):
120 W, 2700 K, cone 40 deg, from [7.1, 0.45, 3.3] behind and above the globe, raking through the discs toward the lens.
Two unjudged looks from the camera's side (40 W and 150 W) lit the smoked faces dull grey and changed nothing, so the
judged pass is the back rake the p2 and p3 critics proposed. Proof at 1200 x 800, 128 samples, round 39's lens step.
The globe's crush in [610,0,880,285] fell from 14.0 % (round 39's final) to 7.65 %.

| pass | frame | critic a | critic b | mean | if fixed | main notes |
|---|---|---|---|---|---|---|
| edge | door-mother + edge light | 5.5 | 5.0 | 5.25 | 7.0, 7.0 | the globe still "a black blob", "a black wire ball" (median 9, p95 39); the edge light "barely registers"; both ask for 260 to 350 W from further behind |

Read test: a render ("a large dark wire-sphere pendant"; "surfaces too clean, furniture repeats exactly").

| frame | ab | ba | result |
|---|---|---|---|
| door-mother + edge light, against round 39's finals/door-mother (2400 scaled to 1200) | r39, clear | r39, clear | round 39 2–0 |

Both judges chose on the proof's denoiser smear (the 2400 final, scaled down, is cleaner), not on the globe. The test
fails both conditions (both duels and 6 with both critics), so no full-size render. Round 39's final stays the door hero.
