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
| 4 | p4 | 5.0 | The smoke a flat glowing curtain with no shafts in the air; the ground smeared (no needles at full size); halo lines on the trunks (the kickers grazing them); a weak left rim; the front muddy; the horn's head clipping; a curly branch beside the base | The low sun (elevation 8) beamed almost straight at the camera, so no shaft could cross the view. I changed the light's idea to god rays through the crowns. **Canopy.** Two shadow-only layers out of frame, at 10 m and 13 m, cut by noise into clumps and gaps. **Light.** The sun to azimuth 150, elevation 24, irradiance 30. The kickers light the speaker only (receivers), which ends the halos; the right one went to 26. The bounce went warm (#C9BBA8, 3.0). Exposure -0.3, bloom 0.04. **Smoke.** Density 0.15 with an even floor of 0.06, so the shafts show in the air. **Set.** The trunks varied (radius 0.10 to 0.42, lean up to 6, bump 4); five branches, none within 2.5 m. |
| 5 | p5 | 5.5 | The speaker's lower body against dark ground, not the glow; the body crushed (median 11.5); a rim on the right edge only; the glow dull (148 to 178); smooth trunks; a seam where the lit floor meets the haze; no cool in the shadows; a lit sliver under the base | **Camera.** The critic asked for a lens at 0.35 m to put the glow behind the whole body. The brief's eye level is 0.7 to 1.2 m, so I took 0.7 m and brought the glow down to the ground instead: a ground-hugging layer of smoke (0.18, gone by 1.6 m), centred 7 m back. **Light.** Exposure 0 (it was -0.3), bounce 7, left kicker 42 and wider, sky fill 2.0 over 4 × 3 m. **Set.** The bark tint 30 % with bump 5; the feet sunk 20 mm. |
| 6 | p6 | 5.5 | Smooth-column trunks; a dead dark band across the foreground with a ruler-straight edge; a rim on the right only; no light through the tint; the shafts only at the left; blotchy photo leaves through the haze; a featureless mid-ground; all sepia | **Set.** The band came from the canopy: at a sun this low, light slipped under its far edge and flooded everything beyond 2 m. Taking the canopy out and lowering the sun to 16 lets the trunks themselves cut the shafts, and their shadows streak toward the camera. True displacement (0.025 m) on the near trunks, with larger bark plates and a lighter tint; ten more trunks 14 to 25 m back, and the sky down to 0.08. **Light.** The left kicker to 75 at elevation 30; a through-light behind the cabinet (8, cabinet only) for amber at the tint's edges; a cooler sky fill (4.0, #9FB0C8). **Smoke.** Crisper (density 0.10, cut 0.5, soft 0.15) and kept clear of the camera. |
| 7 | p7 | 5.0 | The trunks still smeared and smooth; the ground a soft leaf smear; the smoke a flat wall; the cabinet near black with a weak left rim; no shadow of the speaker along the shafts; one sepia tone | Stopped here, under the coordinator's rule (two passes in a row since the concept change gained less than 0.5: 5.5, 5.5, 5.0). |

## The duel and the finals

**The duel.** A blind duel (`critic/ab/PROMPT-DUEL.txt`) set p7 (A) against p6 (B). B won, 5.6 to 4.8. The judge preferred
p6's dappled canopy light, its god rays, its bark, its darker anchors and its irregular light pool. It found p7 milky,
with synthetic, regular radiating shadows. Against p6 it named one thing, the foreground's "hard, straight upper edge,
like a wall offscreen" (`critic-smoke/duel-p7-vs-p6.json`).

**The finals are p6's rig, with that edge fixed.** I traced the edge, removing one piece at a time:
- **Not the canopy's edge.** A canopy of 400 × 400 m still showed it, and so did other noise seeds.
- **Not the near trunks, not the smoke box.**
- **The cause: the sky fill and the bounce.** These two big area lamps stand about 2 m in front of the speaker, so they
  lit the floor only on their far side. Linked to the speaker's parts alone, as a photographer's reflector would be,
  they leave the floor to the sun, and the floor is dappled to the frame's bottom edge.

The portrait was re-framed, not cropped: 5.5 m away on the same 65 mm lens, the speaker 42 % of the frame's height, with
the shafts through the crowns above it.

## The final, and its blind pass

`renders/2026-10-18/barkhorn/element31/smoke.png`: 2400 × 1600 at 512 samples, 3 h 11 min (11,434 s) on 4 CPU cores.
The portrait (`smoke-portrait.png`, 1600 × 2000, 512 samples) went to the coordinator's render helper, which runs it on
its own box from this branch.

A blind critic on the final at full size scored it **6.5** ("a very good render, not yet a photograph"), the best of the
run; the half-size proofs at 128 samples had scored 5.0 to 5.5. Its top changes, not made:
1. Real bark on the trunks (displacement, bump 8, lichen).
2. A brighter bounce, so the woofer and lining read.
3. A left rim to match the right.
4. A cooler white balance (about 500 K) against the single orange cast.
5. A firmer contact shadow.
6. Denser far smoke, to hide the photo plate's leaves.
7. A floating branch stub at the top centre.
8. Grain and a little clarity.

It estimated 7.6 with all eight (`critic-smoke/final.json`).

## An honest note: where it stands and what holds it back

The blind critics scored seven passes from 5.0 to 5.5 (scale: 6 is "a competent render that still reads as CG"). The
duel judge gave the chosen rig 5.6. None reached 8.5. It is a mood piece that reads at once: a dark speaker against
woodsmoke glowing in a pine wood. But it is not yet a $20,000 campaign photograph. What holds it back, as every critic
named it:
- **The trunks.** Modelled columns in a scanned bark texture still read as smooth cylinders through the haze. Real
  scanned pine trunks (Poly Haven's `pine_tree_01`, 17 M polygons) would not fit in this container's 15 GB; one copy
  imported per tree ran out of memory. A decimated scan, or a trunk-only cut of it, is the single biggest gain left.
- **The smoke.** A noise volume reads as an even wall or fog, not woodsmoke. Real smoke has structure at many scales:
  a simulated plume (Mantaflow, or an OpenVDB cache) would carry it.
- **The ground.** Litter from one texture lacks the cones, twigs and needle clumps that sell scale at the speaker's
  feet.
- **The speaker.** Smoked black acrylic against a bright ground stays a near-black box unless it is lit as a studio
  would light it. The critics asked for more rim, more light through the tint and more fill, while the brief asks for
  location light. I kept the fills motivated (litter bounce, sky, the smoke's glow behind) and linked to the speaker.
- **The grade.** Warm smoke everywhere reads as one sepia tone. The cool fills helped the shadows only a little.

Concept B (the high-key birch wood) puts the black speaker against pale mist, which may solve the speaker's legibility
more simply.

## Software and environment notes

- **bpy 5.0.1 on Python 3.11, plus Pillow and scipy 1.13 (numpy 1).** The container's python3 is 3.13. Renders run with
  `python3.11 studio/engine/render.py`.
- **`.venv-fab` on Python 3.11**, with build123d, for the speaker's model.
- **No engine core change.** My pieces are in `studio/engine/kit_ext/smoke_el.py`: woodsmoke, trunks and canopy.

## The re-finish (after the duel with Smoke B)

Smoke A beat the Smoke B birch wood in two blind duels (6.5 to 3.5, 6.5 to 4.5). Both judges marked down the grade: the
cabinet was underexposed and merged with the shadowed ground, and the amber hid the acrylic's own smoked tint. The
coordinator asked for a re-finish from the raw frames, with no re-render.

`critic-smoke/refinish.py` (RAW MASK SHOT OUT wb_r wb_b lift dodge) does it in four steps:
1. **White balance toward neutral.** It runs in linear light, with luminance kept: R × 0.84, B × 1.25.
2. **A small toe lift.** It adds up to 0.003 linear at black.
3. **A 0.7-stop dodge on the speaker's darker tones**, feathered over the part mask. The mask came from
   `render.py --masks-only` with the set switched off: nothing stands in front of the speaker, and the full set ran
   out of memory in the mask pass.
4. **The shot's own finish chain**, run on top.

**Results.**
- The cabinet's mean luma rose from 45 to 55, and its colour from orange-brown (54/43/36) to grey-brown (62/54/50).
- The ground below stays darker (38).
- In a blind duel (`critic-smoke/duel-refinish.json`) the re-finish won, 6.4 to 6.0. The judge liked the lifted body,
  the readable woofer, panels and ports, and the base separated from the litter. It found the shell a touch cool
  against the amber forest, and the original's grade richer.

The portrait (rendered by the coordinator's helper, 457212b) got the same re-finish. Both finals in `element31/` are now
the re-finished frames.

## Round C (the owner, 2026-10-18 17:30)

The owner, verbatim: "Smoke's still looks bad. Doesn't look like a smokey environment and the speaker is too stark and
crisp relative to the environment."

The place stays a pine wood at dawn, now with a **smouldering burn pile** in frame, 3.6 m right and 5 m behind the
speaker (`burnpile` in `kit_ext/smoke_el.py`: charred logs, ember chips, an ember light). Its smoke fills the wood:
- a plume of seven noise cells that widen and drift left as they rise, with a cool fill on the plume alone so it reads
  pale, not as a dark column;
- a drifting layer at 2 to 5 m;
- low wisps between the camera and the speaker;
- a uniform haze through the whole scene, the camera inside it, so the smoke lies between the lens and the speaker and
  lifts its blacks.

Clarity and sharpening are off, so the speaker is no crisper than the set.

| Pass | Image | Score | Top changes | What I did |
|---|---|---|---|---|
| C1 | c-p1 | 5.0 | All one sepia-orange (the smoke read as dust); the speaker's body as dark as the ground (31 against 29); the fire a placeholder of logs and dots; flat tonal range (p99 156); a muddy ground; waxy trunks | **Grade.** A cool grey haze (#C4CAD2), a paler sun (#FFCC9A, 40) and the sky at 0.35, so shadowed smoke goes blue-grey and the shafts stay warm. **Fire.** A 250 W ember light, plus a 150 W glow up from under the logs; the plume denser (5.0) with its fill at 8. **Speaker.** The sky fill to 4, the bounce to 14, the left kicker to 55, and an orange (#FF8A40) rim of 45 from the pile's side. **Exposure and contrast.** Exposure +0.3, contrast 0.10. **Not done.** The camera at 0.55 m: it is below the brief's eye level. |
| C2 | c-p2 | 5.0 | The plume read as a dark trunk; CG logs and sprite embers; the speaker flat and slightly cool; no fire rim; shafts not reading as rays; flat tones; the bottom fifth dead | **Plume.** Thinner (1.8), front-lit by its fill from the camera's side (22). **Fire.** A grey ash bed. **Speaker.** A warm sky fill (2.0, #B8B4AE); the left kicker 95 and lower; the fire rim 120 at log height. **Grade.** Sky 0.7, a cooler and thinner haze (0.012, #BCC4CE). **Sun.** 75 at elevation 18. **Smoke.** The drifting layer to 0.5. **Finish.** Contrast 0.15, vignette 0.18. **Camera.** 6.2 m at f/2.8 (height kept at 0.7 m, the brief's eye level). |
| C3 | c-p3 | 5.0 | The haze bleaching the top half into a flat cream; no plume structure (reads as fog); the fire a salmon cast on blocky logs; the speaker warm brown, not smoked grey-black; blotches on the horn; smooth trunks; a gravel-like floor | Stopped: C1, C2 and C3 all scored 5.0, so two passes in a row gained under 0.5. A blind duel between p2 and p3 picks the finals' rig. |

**Round C's duel.** p2 (A) against p3 (B), blind: p3 won, 5.5 to 5.0. The judge preferred p3's larger, better-lit
cabinet (its woofer, panels and ports legible), its warm edges and its raking light on the ground. It preferred p2's
darker, moodier trunks and its clearer fire. Both frames' horn showed blotchy denoiser smear at 128 samples. The finals
use p3's rig.
| C4 | c-p4 | 5.0 | A milky peach wash; no readable plume; cone flames and dot embers; the speaker warm brown with copper outlines; smooth trunks; a hard shaft stripe on the ground | The coordinator's focused pass (c-p4) had made the plume a leaning column with two-scale wisps (`detail_weight` in `woodsmoke`), moved the pile into the bright gap, added flames and hotter embers, and a cool fill. From C4 I took the quick fixes: the trunk smoke to 0.04 and the haze to 0.003, so the plume is the main mass of smoke; the plume denser (12 falling by 0.7); no cone flames (a smouldering pile); the warm rims calmer (kicker 30, fire rim 50); the cool fill 6. A 32-sample check (g1) shows the plume's grey billows and a smoked-black cabinet. **Finals use this rig, on the rebuilt model with main's drivers (01267eb).** |

## Round D (the owner, 2026-10-19: "the speaker appears to be floating ... there's no smoke in the background")

Built on round C's rig (8d2526e to the d-p7 head). Read tests, a fresh judge at site size each:

| Proof | Stands? | Smoke? | What changed |
|---|---|---|---|
| d-p0 | floats | smoke | Duff drifts on four faces, a fern over the front corner, roots, a stump, branches; the plume self-shaded and greyer, its fill off |
| d-p1 | floats | smoke | Taller, darker drifts; a damp contact patch; feet sunk 45 mm |
| d-p2 | floats | smoke | A sun shaft through a canopy gap onto the speaker (its own long shadow) |
| d-p3 | **stands** | smoke | The camera up to 1.1 m at f/4: at 0.7 m the contact line and shadow were foreshortened away |
| d-p7 | floats | smoke | No uniform haze, thinner wisps in front, fills halved (depth) |

A 512-sample full-size crop (d-p6) proved the grime seen at 128 samples was noise: the acrylic reads as clean smoked glass.

**Duel, d-p7 (960 px, 256 samples) against Smoke A on the new drivers (595c55b, scaled down to match): A won, 6.0 to
3.5.** Part of the gap is resolution (a downscaled 512-sample final against a 256-sample proof: "smeared horn, mushy
woofer"). Two points are not: the plume read as "a ghostly half-formed figure", and the lumpy drifts and debris
"muddy" the base, where A "sits cleanly with a believable contact shadow". This rig fails the gate (within 0.5 of A).
