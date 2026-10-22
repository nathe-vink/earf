# Planet EARF round 39: finals and scores

Every critic's JSON is verbatim in `critic/`, and the round table is in `critic/LOG.md`. Scores are a blind critic's stage-1 score out of 10.
The target was 7 or more on the heroes. **It was not reached.** Every pass sat at 4.5 to 6.0. The critics' "if fixed" estimates were 7.0 to 7.5.

## The frames kept

The paths below are relative to `renders/2026-10-22/barkhorn/planet39/`.

| frame | kept | best blind score | duel against round 38's best | status |
|---|---|---|---|---|
| door (hero 1), with Mother EARF | finals/door-mother.png (2400 × 1600) | 5.5 / 5.5 | not dueled: round 38 had no door frame | final |
| door (hero 1), without | finals/door.png (2400 × 1600) | 5.5 / 5.5 | not dueled | final |
| door, Mother EARF in colour (a labelled variant, not a proposal) | proofs-p4/door-mother-colour.png (half size) | not judged | — | variant |
| bar (hero 2) | proofs-p2/bar.png (half size) | 5.5 / 5.5 | round 39 wins 2–0 | proof only |
| listening (hero 3) | proofs-p3/listening.png (half size) | 4.5 / 4.5 | round 39 wins 2–0 (slight) | proof only |
| decks (detail) | **round 38's** coins-decks.png (round 39's proofs/decks lost 0–2) | 4.5 to 5.5 | round 38 wins 2–0 | round 38 kept |
| door and coin bowl (detail) | proofs-p3/bowl.png (half size) | 5.5 / 5.5 | round 39 wins 2–0 | proof only |
| shopfront at blue hour (detail) | proofs-p2/street.png (half size) | 6.0 / 6.0 | round 39 wins 2–0 | proof only |

Four of the six full-size finals were not rendered. On the coordinator's re-plan, a frame gets a full-size render only once a proof scores 6 or more. Only the street proof did (p2), and that was before the re-plan. It is the next full-size render if wanted. The command:
`python3 spinoffs/barkhorn/planet/r39/r39_shots.py street` and then `render.py` at scale 1.0, 192 samples. Then apply `photo.py`.

## Passes

| pass | door | door-mother | bar | listening | decks | bowl | street |
|---|---|---|---|---|---|---|---|
| p1 | 4.0 to 5.5 | 4.0 to 5.5 | | | | 4.5 / 5.0 | 4.0 / 4.0 |
| p2 | 5.0 / 5.5 | 5.5 / 5.5 | 5.5 / 5.5 | 4.0 / 4.5 | 4.5 / 5.5 | 5.0 / 4.5 | 6.0 / 6.0 |
| p3 | 5.5 / 5.0 | 5.5 / 5.5 | 5.0 / 5.0 | 4.5 / 4.5 | 5.0 / 5.5 | 5.5 / 5.5 | 5.0 / 5.0 |
| finals | 5.5 / 5.5 | 5.5 / 5.5 | | | | | |
| p4 (lived in) | 5.0 | | 5.5 | 4.5 | | | |

(The full p1 rows are in `critic/LOG.md`.) **Read test:** the read tests on p1 to p3 called every frame a render. The reasons they gave:
- repeated identical furniture;
- surfaces that are too even;
- CG-style shadows.

## Mother EARF, with and without

The two door finals differ only in the globe. Both critics scored them the same (5.5 / 5.5 each). The globe neither helps nor hurts the score. As drawn, it is the Smoke one-colour globe over the middle banquette table under a hard spot, with a rim spot. The critics read it as "a large dark wire-sphere pendant", then "a black cage". The rim light lifted it a little. The multicolour version is a labelled variant only, and it carries the owner's rainbow note. The other ways the name could live in the bar are in the README, under "Mother EARF in the bar".

## What still holds the frames back (all the critics agree)

1. **The light.**
   - The street lamps throw a hard stool-shadow fan across the door's floor.
   - The zinc is the brightest surface.
   - The altar pair is dim.
   - The Domes read as white milk glass.
2. **Repetition.**
   - The stools, the tables, the Cores and the glasses are copies.
   - The jitter and the props in p4 did not break that read.
3. **The listening room** is still a showroom niche over an empty floor. It needs a seated camera with chairs, a table and a Core in front.
4. **Materials.**
   - The fir is one texture.
   - The floor is dead.
   - There is chroma grain at 128 to 192 samples.

## For the owner

- **Mother EARF:** in the bar or not? If in the bar, is it over the banquette (as drawn) or elsewhere? Or any of the other ways in the README?
- **Coin colours:** the bowl is rendered brass and the coins as modelled in round 38. Confirm the coins' finish and colours.
- **The counter seams:** where do the zinc top's joints fall? The model does not settle that.
- **People:** the brief says no people. The critics keep naming empty rooms as a "render" tell. Would you allow traces only (as now), or blurred figures?
- **Budget:** every figure in "Round 39: the house" is an estimate. It is marked so, and it is to be confirmed with a QS and the SF permit desk.
