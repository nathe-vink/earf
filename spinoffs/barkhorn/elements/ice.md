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
