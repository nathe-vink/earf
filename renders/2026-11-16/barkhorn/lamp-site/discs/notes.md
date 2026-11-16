# The discs on the lit glass (2026-11-16)

**The problem.** At Smoke's denser dye, the round key (4 m ellipse) and the round fill (1.6 m) reflect as two pale, flat discs with hard outlines on the lit glass. The coordinator's check found them on hemisphere-smoke-direct (bowl 104–127, discs 135–140) and on core-smoke (two discs on the ball). At 0.3x Smoke, the glow hid them.

**The new placement.** Honest means only: lamps moved, reshaped, re-aimed or switched off. None is hidden in frame, and none lights without reflecting. The new switches in lamp_site.py are FILL_POS, FILL_AIM, FILL_SIZE and FILL_W, all off by default. The recipes are in final/smoke.sh and final-mix/mix.sh.

- **Hemisphere (hero and direct views):**
  - The key is the off rig's 3.0 x 0.5 m strip overhead, at (0, -0.5, 2.2) aimed at (0, 0, 0.55). Its reflection sits on the black shoulder.
  - The fill is moved behind the lamp as a wash on the back paper, at (0, 0.75, 2.1) aimed at (0, 1.0, 0.8), at 2.6x. The bowl's front can't see it.
  - Paper: 29.
- **Core (lit pictures):**
  - A ball reflects every lamp in front of or above it. The overhead strip was tried and showed as a band across the top, so there is no key.
  - The fill faces the back paper square, at (0, 0.55, 1.3) aimed at (0, 1.0, 1.3), at 0.25x. The ball sees only its dark back.
  - The world (a 4000 K grey, #FFD4A5, strength 0.38: even, no discrete reflection) lifts the floor. It is a declared light.
  - Paper: 33 on the upper wall, 28 on the lower paper.
- **Unchanged:** the kicker's slim strip on the right edge, the camera, the lamps, the exposure and the white balance.
- **hemisphere-smoke-under:** keeps its approved render. From below, the moved fill would be in frame (4.3 % in the audit), so that view keeps the old placement.

**Before > after** (`smoke-before-after.png`; `-stretched` is the same at high contrast):

| Picture | Lit glass | Paper | Audit |
|---|---|---|---|
| hemisphere-smoke-direct | bowl 136,142,145 > 136,141,144 | 29 > 29 | hidden in frame 0.0 |
| core-smoke | ball 129,131,132 > 130,132,132 | 28–29 > 33 / 28 | hidden in frame 0.0 |

**The coloured tints.** The mix's denser Hemispheres carry the same two discs under the old placement (Ice 6 and Acid 5, `ice6-acid5-old-new.png`, left). The new placement removes them, and the glass is unchanged within 4 levels:

| Tint | Old placement | New placement |
|---|---|---|
| Ice | 86,158,235 | 82,157,235 |
| Acid | 223,214,166 | 223,215,166 |

The mix singles use the new placement from now on.
