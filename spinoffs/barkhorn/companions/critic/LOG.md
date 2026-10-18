# The companions' critic log (round 31)

The studio's critic (`critic/PROMPT.md`, verbatim) in a fresh context, given only the staged image, its card
(`critic/cards/companions.yaml` through `critic/round.py stage --card`) and the measuring tool. Replies are in
`critic/rounds/2026-10-18/`. At most three rounds per shot per look.

| Date | Shot | Version | Round | Blind score | What most separates it from a 9 | Applied | Not applied, and why | Score if fixed |
|---|---|---|---|---|---|---|---|---|
| 2026-10-18 | companions-hero-turntable | e1 | 1 | 4.5 | The speaker dominates and runs into the bottom edge; the record player is 19 % of the width; flat, shadowless light; the record and the plinth tops mirror only the sweep | c1 speaker 0.41 back; c2 lens 62 to 72; c3 dome 0.7 to 0.25; c4 key 2.5 x 2 to 1.2 x 1; c5 key 2.2 to 3.2; c6 and c7 a graded card over the record; c8 a finer veneer; the speaker's back glow moved with it | out of scope (the card's fixed): the horn's driver reading black, the cloth disc's flatness, the sweep's pink | 6.5 |
| 2026-10-18 | companions-hero-lamp | e1 | 1 | 4.5 | The speaker cut at the bottom; the lamp's glow lights nothing; the dome flattens the wall; the lilac sweep shares the acrylic's hue | c1 lens 60 to 50; c2 the strip x4; c3 dome 0.7 to 0.25; c4 key 1.32 to 1.9; c5 a warm pool on the wall behind the shade; c6 the sweep warm grey #D8D2CA; c7 veneer grain 0.2 to 0.45; c8 contact shadows 0.6 | out of scope: the speaker's front lighter (its tint is fixed); the pair moved closer (revisit after c1) | 7.0 |

After round 1, Cumulus's hero was reframed by hand (e2): the critic's c1 and c2 together cropped the speaker at the left and left the record player at the same size, so the sideboard came 0.4 forward, the speaker stayed 0.45 back, and the camera went close and wide (35 mm at 2.45 m). Its light changes (c3 to c8) kept. Round 2 not run.

## Round 31b: promotional passes (`critic/PROMPT-promo.md`)

The owner, through the lead session: "Continue to do critic passes until you feel it's in a good enough place for
promotional images for a $20K product." Each pass is a fresh, blind critic given only the image, a short card
(`promo.py stage`), `critic/measure.py` and the prompt's text. Replies: `critic/rounds/2026-10-18/promo-*.json`.
Frames: `renders/2026-10-18/barkhorn/companions/promo/`. Stop at two passes in a row of 8.5 or more.

| Shot | Pass | Blind score | Verdict | The critic's top changes | What I did | Score if fixed |
|---|---|---|---|---|---|---|
| hero-turntable (room, Ember) | p1 | 5.0 | iterate | The record player the darkest thing in the frame (lum 12.7); the sun's long horn shadow fills the wall; the speaker a cropped red box; the walnut soft at 2k; the wall flat CG; denoiser smear | a softbox key on the player; sun 24/-72 to 38/-55; the cabinet at 4k; a Poly Haven plaster wall; samples 64 to 160; f/4 on the arm; the speaker moved and the camera reframed so its horn reads (the critic's position was inside the back wall); exposure +0.8 | 7.0 |
| hero-lamp (room, dusk, Haze) | p1 | 5.0 | iterate | Denoiser smear (64 samples); the speaker a cropped slab that reads as a TV; no dusk in frame; the sleeve clipping cold; the cabinet front crushed; a magenta grade; the shadow band off the right edge | samples 64 to 200; the dusk sky 2.5 to 6; the strip's glow 60 to 25; fill 0.04 to 0.12, lower; exposure 0.75; 3800 K; the lamp 7 cm off the wall; the camera wider but not to 35 mm (that made the lamp 15 % of the frame): 40 mm, the speaker further left | 7.0 |

After both first passes, the two heroes were made one set, one light and one grade (the lead: they sit side by side on
the site): Cumulus's hero moved from morning sun to the same dusk, with Bell lit beside it on the cabinet and a warm
softbox high at the left as its key. Its pass 2 in morning sun was stopped before it finished.
