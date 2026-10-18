# Smoke: the night train (round 31)

`smoke.py` builds the set; `python3 spinoffs/barkhorn/dioramas/build.py smoke` writes
`studio/shots/barkhorn/diorama31/smoke.json` and `smoke-portrait.json`.

## The concept

A toy steam train made of black lacquered card runs along a card track behind the speaker at night, with its carriage
windows lit warm. Its stack gives off the Smoke icon in grey wool: the small puff of two circles, joined into the big puff
of three, drifting from left to right. Behind the train stand a row of card houses on a charcoal wool hill, with lit
windows and chimneys. Over the roofs hang a crescent moon cut from tissue on a thread, and paper stars, against
pin-prick stars on a dark card sky. The ground is soot-black velvet. Seen from above through a tilt-shift lens, the
speaker is the sharp band, and the train, the plume and the town melt into soft blur and bokeh.

- **Light, one idea: moonlight and lit windows.** The moon's light comes from the back left. Its full strength is linked
  to the plume and the speaker alone, so it rims the plume and rakes the speaker's left side. A weaker share falls on
  the land, so the wool hills stay charcoal and do not turn to snow, which is Ice's world. The carriages, the houses and the engine's firebox give the warm light.
  The firebox lights the plume's underside orange, and the windows show as warm streaks in the smoked acrylic.
- **The speaker against the smoke.** The plume's big puff sits behind the horn, so the smoked black horn reads against
  pale grey wool, not against the night. That is how the black speaker gets its separation.
- **The joke.** While the engine billows, the stove chimney of the little signal box beside the line puffs one neat
  smoke ring. The signal box is the only building in the set.
- **Palette.** Smoke-grey and night-navy, with warm window light as the one accent. The shadows are lifted into a cool
  night blue (`#1E2030`).

Why the train rather than a row of chimneys: the owner described the icon as "a train smoke stack shape", so a plume
from a moving engine reads at once and moves left to right as the icon does.

Why a valley and not a town: rounds 1 to 20 had a row of card houses with lit windows behind the line. Then the
coordinator relayed the owner's principle for all eight sets: stay on the theme of earth, with each speaker placed in
its atmosphere and the whimsy only as subtle nods. The houses made a toy town the subject, so I replaced them with a
landscape the smoke drifts across. The train stays as the smoke's source within that landscape.

## Proof rounds (24 samples at a scale of 0.3, then 32 to 64 at 0.4 to 0.5, plus crops of the speaker at full size)

1. A first layout at full scale. The train and the plume were huge and the speaker was small. Diagonal stripes ran
   across the ground.
2. I made the train a toy (`TOY` = 0.62, built at full size and then scaled with `scaled()`) and the plume smaller. The
   stripes stayed, and the frame cut the speaker off.
3. The track moved closer (y 1.75 to 1.3), the camera moved in, and two rim lights went onto the speaker's shell
   (`receivers`). The speaker was still a black box against the dark.
4. The ground stripes turned out to be the velvet drape's folds (14 across) catching the sheen. I replaced the drape
   with a flat floor. I lowered the elevation to 16 degrees and shifted the lens up, which brought the moon into frame.
5. The moon moved behind the speaker, and I added a reflection card for the front face. It helped little.
6. The engine moved right, so the plume billows behind the speaker's horn and gives the black horn something pale to
   read against. The moon's light became a side light from the back left. This was the turning point.
7. I turned the speaker to +22 degrees to show a side face for the moon to rake. Each puff became a billow, a ball with
   smaller balls on its rim.
8. The full moon became a crescent of tissue and I added paper stars. I added wool tufts in the foreground to frame it.
   I tried small wisps from the town's chimneys and a smoke ring.
9. I wrote a projection check for the camera (in the scratchpad) and recomposed: the speaker on the right third, the
   moon top left, the stack low left.
10. Mid proof. The moon was too bright (I lowered its emission). The hill's band was too pale (darkened). I raised the
    plume's start off the stack so the engine shows.
11. The smoke ring moved from a distant house to a signal box beside the line, where it can be read. I added a faint
    glow on the sky card so the roofs show as silhouettes.
12. Full-size crop of the speaker. The front face showed no gloss, because the reflection cards were not where the
    camera sees them. I turned the speaker to +6 degrees so the horn's mouth and the woofer face the camera. The cards
    became reflection-only (`diffuse` 0) at the angles where the camera sees them in the front (azimuth 32) and in the
    left side (azimuth -150). Now the box reads as smoked glass, the woofer's ring reads, and the windows streak in the
    left side.
13. A full proof. The bottom of the frame was a dead black.
14. I found that the "black velvet" floor in rounds 4 to 13 was a coplanar black, because the floor box's top met the
    sweep's floor. Lifting it showed the sweep's floor instead.
15. I laid the velvet as a drape again, with 3 broad folds and noise, resting on the sweep. Now the ground reads as dark
    aubergine velvet with warm spill from the windows.
16. I removed the chimney wisps, which turned into out-of-focus blobs, and the foreground tufts, which turned into blue
    balls. The camera moved in so the speaker is 42 % of the frame's height.
17. The right rim went up. Lower saturation (0.1) cooled the blue.
18. The small puff's lumps made a "face", dark pockets between the balls. A bigger core helped a little.
19. I made the billows top-only, which smoke does, so no pockets are left underneath. Exposure went to 1.0.
20. I moved the sky glow out of the hill, which was blocking it, so the roofs now show faintly against the sky.

Rework for the earth setting (s1 to s7, after the coordinator's note):

- **s1.** I swapped the town for ridges of wool and felt with card firs. Lit by the moon, the hills read as snow.
- **s2.** Darker wool and a denser forest. The wool's sheen still turned the hills pale.
- **s3.** I split the moon's light: full strength on the plume and the speaker alone (light linking), and a 0.6 share
  on everything else. The hills are now charcoal with fir silhouettes.
- **s4 to s5.** I removed two far cottages, which could not be seen. I raised the moon clear of the frame's edge and
  softened the plume's grey.
- **s6 to s7.** I traced the dark spot on the small puff, there in every round since round 10, to the firebox lamp
  sitting inside the puff. Moved below it, at 45 W, it lit the whole set orange. At 5 W and 4 cm, just above the stack,
  it gives a warm glow under the plume, as from a firebox.

Portrait proofs:

- **q1.** Lens 40. The speaker was 20 % of the frame.
- **q2.** Lens 60. The speaker was 30 %, with too much floor.
- **q3.** The camera went round to the right (azimuth 24) with the lights turned to match. The plume went dark behind
  the horn and the moon swapped sides, so I dropped it.
- **q4.** The landscape's light and side kept, on a 78 mm lens with a lens shift. The moon, the plume and the speaker
  stack up the frame on a diagonal, and the speaker is 40 % of the frame.

## Final settings

- **Landscape.** 2400 × 1600, 256 samples. Camera elevation 16°, azimuth -18°, distance 6.7 m, 52 mm, f/2.8 at
  miniature 8, shift_y 0.07, focused on the speaker's front face.
- **Portrait.** 1600 × 2000, 256 samples. Elevation 20°, azimuth -14°, distance 6.0 m, 78 mm, shift -0.055 / 0.13.
- **Speaker.** At (0.6, 0, 0), turned +6°, cover off.
- **Kit.** kit_scale 11.
- **Finish.** Bloom 0.35 (threshold 0.7), saturation 0.1, lift 0.04 (`#1E2030`), vignette 0.25, exposure +1.0.
- **Render times.** Listed in the report to the coordinator and in each `.report.json`.

## Environment notes (not the set)

- This container's `python3` is 3.13, and there is no `bpy` 5.0.1 wheel for it. I installed `bpy==5.0.1`, Pillow and
  scipy < 1.14 (numpy 1) into Python 3.11, and ran the renders with `python3.11 studio/engine/render.py ...`.
  `.venv-fab` was made with Python 3.11 too. I changed nothing in the repository for this.

## What I would still improve

- The plume reads as soft balls, plush more than wool, because it sits in the blur. A fibrous edge (a halo of teased
  wool) would sell the craft better, either as a scatter of fine fibres or as a kit_ext wool-tease piece.
- The engine is a sketch: boiler, stack, cab and wheels, but no rods and no lamp beam. It hides in the blur, but a
  sharper engine would add charm.
- The fir silhouettes on the far ridges could take a thin rim of moonlight to draw the skyline more crisply. One fir
  crosses the moon's lower tip; I kept it as a depth cue, but the crescent reads slightly bitten.
