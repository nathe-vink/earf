# Ice, concept A: snow country at blue hour (round 31b)

The owner, verbatim:

- "the diorama looks cheap, like a bad video game. I was hoping for more texture in a lot of these. The speakers are
  too stark in contrast to the setting too. Tilt shift may have been a bad direction. Lighting in general in a lot of
  them is off. ... Maybe don't think about them so much like dioramas, and think more about placing them in there
  element, so to speak."
- "Ice could have a snow covered wood cabin in the back" (a subtle nod).

Set: `ice.py`. Its own pieces are in `studio/engine/kit_ext/ice_el.py`:

- `firs`: Poly Haven's scanned firs, split into single trees and loaded with snow where they face up;
- `cabin`: logs, a roof under deep snow, a stone chimney, one lit window with a lamp inside;
- `snowfield`: two snow scans blended so neither tile repeats, wind ripples, subsurface, glitter, and a drift banked
  against the speaker's base.

## Concept

The speaker stands in deep fresh snow in a clearing at the edge of a fir wood after sunset.

- The sky is a photographed dusk (`kiara_9_dusk`, its sun 4° up), turned so its last glow sits straight behind the
  speaker from the lens. Through the gap in the wood, that light reaches the acrylic.
- Everything else is lit by the cold blue of the sky on snow.
- The cabin stands far back (about 58 m) among the firs. Its one warm window is the frame's only warm note.

**Why this framing.** I made six quick proofs (a01 to a06):

- At 1 m and 65 mm, the cabin sat too near and too big, then cut by the frame.
- Facing away from the glow gave flat light.
- Backlit by the glow through a gap in the wood is the one where the acrylic has something to glow with.

## References

- Diamond Beach and the Vatnajökull ice caves (the B concept's ground).
- Alpine and Lapland cabins at blue hour: deep blue snow, firs heavy with snow, one window lit amber, the sky's last
  peach band low behind the trees.

## Engine changes (each in its own commit, both off by default)

- `render.caustics_refractive` in `render.py`. With refractive caustics off, no light reaches what stands behind clear
  acrylic, so the speaker's lining rendered near black and the cabinet read as navy. With them on (a 0.3-scale crop,
  t-caus), it reads as lit ice.
- `finish.dream.grain` in `finish.py`: film grain on luminance, as critic pass 1 asked.

## Software

- bpy 5.0.1 on python3.11, plus pillow, numpy 1 and scipy for the finish.
- The CAD venv on python3.13.

## Critic passes (critic/PROMPT-promo.md, a fresh blind subagent each time)

| Pass | Image | Score | If fixed | Verdict | Top changes | What I did |
|---|---|---|---|---|---|---|
| 1 | p1 (1 m, 6.6 m, 65 mm, f/4, exp -0.9) | 5.5 | 7.5 | iterate | the acrylic must glow (glow behind it); a blue-hour sky, not white; bank snow against the base; camera 0.7 m, 9.5 m, 85 mm, f/2; non-repeating snow with ripples and glitter; a stronger warm window; widen the gap behind the speaker; contrast and grain | the HDRI turned to 292° (its glow behind the speaker from the lens); exposure -1.3; `snowfield` (two scans blended, ripples, glitter, subsurface, a drift on the base, feet 8 cm deep); the camera as asked; the window at emission 45 and 2400 K, a 2500 W lamp; the gap ±10°; contrast 0.10, clarity 0.06, vignette 0.2; refractive caustics on for the lining; grain added to the finish |
| 2 | p2 (0.7 m, 9.5 m, 85 mm, f/2, exp -1.3; before the merge of main) | 6.0 | 7.6 | iterate | brighter exposure (-0.6); the glow 40° off the axis for a rim, plus a snow bounce; f/2.8, sharpen 0.35; finer, patchy ripples and more glitter; WB 5500 K; a stronger amber window; remove the near sapling; grain | tried them as asked (b02): bright, peach and milky, no longer blue hour. So I kept the bounce, the f-stop, the sharpening, the snow, the window (emission 90), the sapling's removal and the grain (0.022), but turned the sky so the sun sits behind the lens (rotation 110, now that main's `hdri_sun` fix reads it right: azimuth -60). A wood behind the camera shades the clearing, so the light is the sky's and the sky ahead shows the blue and the pink belt of the sky away from the sun. Exposure -1.1, WB 5200 K, haze 0.006 |
| 3 | p3 (0.7 m, 9.5 m, 85 mm, f/2.8, exp -1.1, the sky away from the sun) | 6.5 | 8.0 | iterate | light the speaker (bounce 0.35 raking at -45°, a back card through the horn); camera 0.45 m at 8 m, so the horn clears the ridge into the sky; WB 5800 K with tint +4 (snow lavender, not blue); a wind scoop at the base for contact; clear the trees behind the horn; grain 0.010; extend the ground (a dark wedge at the bottom right); a softer window | all of them, except WB 5400 K at tint 13 (5800 K turned the speaker pale). The bank is now a scoop under the front face, up to 10 cm behind. The gap behind runs to 70 m. The ground is 32 x 30 m. The window is at emission 45 with an 1800 W lamp |
| 4 | p4 (0.45 m, 8 m, 85 mm, f/2.8, exp -1.1, WB 5400 K tint 13) | 6.5 | 7.8 | iterate | a soft drift lapping the base instead of the scoop's crater (feet 4 cm); a stronger back card (0.6, azimuth 165) so light passes through the acrylic; the window down to emission 18; the bounce down to 0.15 and laid low; WB 6100 K tint 8; sastrugi ripples, 50 cm relief, more glitter; a soft foreground of grass at bottom left; contrast 0.14 | all of them (b05). But at 6100 K the acrylic went pale and cyan-white, and it still didn't glow, which is the note every pass has made. So I turned the sky to 275°: the sun, 4° up, sits behind the wood at the right rear, its glow behind the speaker and a dark hill behind the cabinet (b06). Against that, the acrylic reads as lit blue ice. Kept WB 5400 K tint 10, exposure -1.4, the bounce at 0.25, and the window at emission 28 with a 1000 W lamp so it stays the warm accent without clipping. Grass is from Poly Haven's grass_medium_01, at the frame's bottom left |
| 5 | p5 (the dusk glow behind at the right rear, exp -1.4) | 6.0 | 7.4 | iterate | a strong tall back card (1.6) to rim the cabinet off the hill; a deeper, bluer sky (exposure -1.7); remove the dark grass blobs; finer snow without blotches, more glitter; a 6 cm drift; window spill; grain 0.005 | **Three passes gained under half a point (6.0, 6.5, 6.5, 6.0), so per the brief I changed the concept's light, not its settings.** I tried and rejected two things: the cabin close behind the speaker (c01, c02), which filled the backdrop and hid the window; and falling snow (c04), whose flakes read as dark specks against the bright sky. The new light is moonlight on snow: a clear night sky (`kloppenheim_02_puresky`) with the moon 17° up behind the wood at the right rear, raking the snow and rimming the horn. The window reads as the one warm light in a blue night. Distant snow hills close the pure sky's horizon. Also: the gentler snow blend and glitter, the grass pared to two small tufts, the 6 cm drift, the back card at 1.6 and the bounce at 0.8, exposure -0.6, haze 0.003, grain 0.005 |
| 6 | p6 (moonlight: kloppenheim_02_puresky, moon behind right, exp -0.6) | 5.5 | 7.0 | iterate | light the cabinet (it read dark navy, 2 stops under the horn); a darker sky for real night; tame the horn's chrome look; a heavier drift; sparkle; a neutral WB; haze to soften the far ridge; remove or rework the snowfall specks | **A blind duel, p4 (blue hour) against p6 (night), went to p4: 7.0 to 6.0.** The judge preferred p4's bright, legible cabinet, its soft blue horn and its pink-to-lilac sky, but liked p6's natural drift and rolling terrain. So, as the coordinator ruled, back to blue hour: p4's rig (kiara_9_dusk at 110°, the clearing shaded, exp -1.1, WB 5400 K tint 13), with p6's soft drift lapping the base (6 cm), the 50 cm relief and more glitter, and a small white card held in front at the horn's height for its throat (on the waveguide only, 0.5) |
