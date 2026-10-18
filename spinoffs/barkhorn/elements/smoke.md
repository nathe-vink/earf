# Smoke, concept A: woodsmoke at dawn in a pine wood (round 31b)

The owner, on round 31's dioramas (verbatim): "Smoke is too hard to see and the diorama looks cheap, like a bad video
game. I was hoping for more texture in a lot of these. The speakers are too stark in contrast to the setting too. Tilt
shift may have been a bad direction. Lighting in general in a lot of them is off. ... Maybe don't think about them so
much like dioramas, and think more about placing them in there element, so to speak." And: "Continue to do critic
passes until you feel it's in a good enough place for promotional images for a $20K product."

`smoke.py` builds the set. `studio/engine/kit_ext/smoke_el.py` holds its own pieces:
- **woodsmoke:** a noise-carved scattering volume, fading at its edges and top;
- **trunks:** pine trunks at real scale, UV-mapped in metres, so Poly Haven's `pine_bark` lies at its real size all
  round.

## The idea

A pine wood just after sunrise. Woodsmoke from a fire out of frame hangs between the trunks. The sun, low behind and to
the right, lights the smoke from behind into a warm glowing wall. The trunks stand dark in it and throw long shadows
across the needle floor toward the camera. The smoked black speaker stands in front of the brightest smoke, so it reads
at once as a dark, clean silhouette, the reverse of the dioramas, where it was black on black.

**Why this light:**
- **Contrast.** A black object reads only against something lighter, and backlit smoke is the brightest, softest
  background a forest can give.
- **Unity.** It is one light (the low sun), so the shadows, the glow and the colour agree.
- **Separation.** The forward-scattering smoke puts the glow exactly where the silhouette needs it.

## Building it (before the critic passes, 32 samples at a scale of 0.3)

- **The sky.** `misty_pines` (Poly Haven), a real pine wood in mist, as the far background.
- **The trees.** Poly Haven's `pine_tree_01` (17 M polygons) ran out of the container's 15 GB: each placed copy
  imported again. At eye level a pine wood is bare trunks, so I modelled the trunks (`trunks`) in the scanned
  `pine_bark` texture: 46 of them, denser toward the sun.
- **a1.** The smoke at density 0.5 and the sky at 0.5: a beige fog, with no shafts.
- **a2.** The sky at 0.14, the sun at 14 and the smoke at 0.2: long trunk shadows, but the trunks were too few for
  shafts.
- **a3.** The ground became `forest_leaves_04` (pine litter). An 80 m displaced ground ran out of memory, so it went
  back to 40 m.
- **a4.** Forty-six trunks, the sun at azimuth 140 and elevation 12, irradiance 24, the smoke's anisotropy 0.8, and the
  sky at 0.04. Shafts and glow appear.
- **p1.** The bark darkened and the sun warmed (#FFB978). This was the first critic proof (128 samples at a scale of
  0.5, 8.4 minutes).

## Critic passes (`critic/PROMPT-promo.md`, a fresh blind subagent each)

| Pass | Image | Score | Top changes | What I did |
|---|---|---|---|---|
| 1 | p1 | 5.0 | The speaker crushed to black (median 6) with a rim on one side; smoke a flat sepia wash with no shafts; the trunks smooth CG columns; the glow to the right, not behind the speaker; all one sepia tone; a pasted fallen trunk; the speaker centred | **Light.** A warm bounce from the litter (0.35) and a kicker behind-left (6). The sun moved behind the speaker as the camera sees it (azimuth 164, elevation 8, angle 0.5). The smoke's wisps went to 3 m at density 0.22, and the sky to 0.12 for cool shadows. **Set.** The bark darker (75 %, bump 2.2), with dead branch stubs; the fallen trunk removed. **Camera.** 65 mm at 7.2 m and 0.8 m height, the speaker on the left third. **Finish.** Clarity 0.10. |
| 2 | p2 | 5.5 | The speaker still near black (median 11); a rim on one edge only; the HDRI's blue strip showing outside the smoke; the floor a flat board (OSB-like); roots like pasted mats and trunks with no flare; a flat cream haze; foreground stripes as bright as the glow; a matte line on the trunks | **Light.** The bounce to 2.4 m and 1.4; kickers on both sides (14 and 10). **Smoke.** The volume to 40 × 15 × 14 m, so nothing of the sky shows, and the sky to 0.04. Density 0.14 with crisper wisps (scale 1.6, cut 0.58, soft 0.14): at 0.15 and 0.08 with soft edges it washed the forest out (b2, b3). **Set.** A pine-needle ground (`forrest_ground_03`) with 0.12 m relief, fallen dry branches in place of the roots, and a stronger root flare. **Finish.** Clarity 0.03, vignette 0.25 (the engine has no graduated filter). From p3 the merged main renders without the look book's 5600 K white balance, so the colour shifted warmer. |
| 3 | p3 | 5.5 | The ground reads as sand or carpet; the shadows have no cool skylight (all sepia); the smoke an even wall, not shafts; no left or top rim and the front crushed; the mid trunks smooth repeats; the sky still a strip at the volume's edge; the near trunks veiled pale | Three passes gained only 0.5, so I changed the approach, not just the settings. **Background.** The photographed misty pine wood (`misty_pines`, sky 0.15) now shows through beyond 14 m in place of modelled far trunks, so the distance is a real photograph, cool against the warm sun. **Trees.** Only 22 modelled trunks, near, where the bark holds up (radius 0.12 to 0.35, lean up to 3.5, bump 2.6), plus two dark trunks framing the near left. **Light.** A cool sky fill and bounce (#A9B4C2), the kickers narrowed and raised (20 and 16), the sun at 36. **Set.** The `forest_leaves_04` ground (displacement 0.06, relief 0.12), twelve dry branches, the feet sunk 10 mm. |
