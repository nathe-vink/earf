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

## On the drivers made real (2026-10-19)

Both finals rendered again on the drivers as made (the 15PR400 woofer, the DE1085TN's exit and phase plug, the opaque
polished ring), on the same rig: eight helpers, four strips a frame at 512 samples with the finish off and 32 rows of
overlap each side, stitched with feathered overlaps (landscape fd50f94, 9e2248d, b675fe4, 43d34af; phone 88004bf,
0b71533, 226db37, de091a6; 13,900 s and 14,000 s of render). Then the same re-finish from the raw, with the same
numbers (R x 0.84, B x 1.25, a 0.003 toe, a 0.7-stop dodge). The speaker's mask came from `render.py --masks-only
--set set.kind=none --set finish.enabled=false`, so nothing stands in front of it. The cabinet lands where it did:
mean luma 55.5 against 55, the ground below 37 against 38, grey-brown (62/54/51). The joins show no line at 3x, and
the row-to-row grain sits at its neighbours' at every join.

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

## Round D2 (A's rig plus the owner's asks only)

On A's rig: the camera at 1.0 m, a fern over the near front corner, three small twigs, and a sun shaft onto the speaker. Far back in the bright gap (8, 9) sits a small smouldering pile (charred logs and embers). A thin column of woodsmoke rises from it, backlit and leaning left. No drifts.

| Proof | Stands? | Smoke? | Figure? |
|---|---|---|---|
| d2-p0 (k4) | stands | smoke | none |
| d2-p1 (k5, 960 px, 256 spp), run 1 | stands | smoke, from the fire | none |
| d2-p1, run 2 | stands | smoke, from the fire | none |

**Duel at 720 px (both scaled down, order swapped across two judges): A won, 6.0 to 4.75** (5.0 v 6.5, 4.5 v 5.5). The gate is within 0.5, so this fails. Both judges read the glowing ember pile as "a forest fire next to a loudspeaker" that pulls the eye. That glow is the visible source the owner asked for. They also called the fern sparse and dropped in, the speaker too high in the frame with empty ground in front, and the cabinet softer. Part of the softness is 256 against 512 samples. One judge credited D2 for its grounding and its stronger, more atmospheric shafts. See `critic-smoke/d2-duel-vs-A-newdrivers.json`.

## Round D3 (the coordinator's last pass: no glow, a natural clump, A's framing, a fair duel)

Tests at 64 samples:
- **t1:** the embers off. The dark column alone read as a figure.
- **t2 and t3:** the source moved off frame right, plus a wispy drift across the far shafts. A read test said "no smoke: haze or light fog, no visible source".
- **t4 and t5:** an unlit pile in the bright gap, then nearer in a sunlit patch. Each read as a dark lump or a log heap, and the smoke didn't show.

Without a visible, faintly glowing source, this set's smoke reads as fog.

The proof, d3-p0 (k6, 960 px, 512 samples), goes back to D2's column with the embers at 6 instead of 60, keeps the fern at the near-left corner, and uses A's framing (shift_y 0).

| d3-p0 | Stands? | Smoke? | Figure? |
|---|---|---|---|
| run 1 | stands | smoke, from the orange glow | "could faintly suggest a standing figure" |
| run 2 | stands | smoke, from the ember patch | "could be mistaken for a vague figure at a glance" |

**Duel at 720 px, order swapped: A won, 5.65 to 4.25** (4.5 v 5.8, 4.0 v 5.5). This fails the gate. Both judges still call even a small orange glow "a forest fire", and both say the fern hides the base's lower-left corner. They credit D3 with stronger shafts and more depth, and with the ferns giving it a sense of place.

This stops here, as the coordinator set: the best proofs go to the owner beside A. See `critic-smoke/d3-duel-vs-A-newdrivers.json`.

## Round E: three settings without the forest (the owner, 2026-10-19)

The owner: "I just don't think the forest is a good setting for smoke, it's too hazy and forests are just like that in the morning without smoke, and then the fire seems forced." The site keeps A until a new Smoke wins. These are three settings, proofed at 0.3 scale (720 × 480, 256 samples) on the drivers made real, so the owner can pick one. Each keeps A's speaker rig: the fills and kickers are linked to the speaker alone, and the acrylic is the same.

The smoke in all three is a new piece, `ribbon` (studio/engine/kit_ext/smoke_el.py). It is a volume inside nested tubes along a curve, with a laminar thread at its start. Noise tears the wider parts, a ragged wall (`wobble`) keeps it from reading as a hose, and a broad noise (`break_*`) thins and thickens it along its length.

| Setting | File | Proof | Read test (600 px, fresh judge) |
|---|---|---|---|
| E1 incense in a concrete hall | `smoke_incense.py` | element-smoke-e1-incense-p0 | stands; "smoke, not fog or haze: a thin wispy plume rising from the incense stick"; no flame, "only a small red ember"; no figure. One note: a short bright streak partway up (the thread where it crosses the beam) "looks a little odd". |
| E2 after hours in a cigar room | `smoke_cigar.py` | element-smoke-e2-cigar-p0 | stands (contact shadow on the lit floor); "clearly smoke, not fog or haze", from "a cigar resting in an ashtray"; no fire, no ember seen; no figure. |
| E3 the studio take | `smoke_studio.py` | element-smoke-e3-studio-p0 | stands (its reflection in the gloss floor); "smoke, a dense coiling plume rather than flat fog or haze"; no fire; no figure. |

The three side by side: `element-smoke-e-settings.jpg`. No duels yet: the owner picks the setting first.

How each was found:
- **E1:** the slot was first placed behind the speaker, where the beam fell out of frame. It now sits low in the right wall, in front, so the sun's slab crosses the smoke and lands on the back wall as a bar behind the speaker.
- **E2:** the spot was first over the table, which lit the smoke dull. It now comes from behind, so the smoke glows. The chair faces the camera. A brass vase was dropped because it read as clutter.
- **E3:** three thick strands read as cotton-wool coils, and thin ones read as tubing. One wide, billowing strand plus a fainter second reads as smoke. It starts low at the front so the cabinet stays clear, and the rims are hidden from the gloss floor.

## E3, the studio take (the owner's pick), passes 1 to 3, and E4 black smoke

The coordinator's fixes: the front kept clear; one rising column, not a creature; the speaker legible on black; nothing like fire.

- **Pass 1** (g1): one column rising behind and left and rolling over the top.
  - Reads: smoke, no fire. But the dark horn fins against the blown panel read as "a clawed hand", and the smoke seemed to come out of the speaker's top.
  - Duel: A 5.75, E3 4.0.
- **Root cause of the "card".** A surface seen through the smoke (the floor, and later a backdrop) showed lit, whatever the smoke's density. It persisted with a single clean tube, without light linking, and with a matte floor. Shading inside a mesh volume was the cause: ribbon now fills a voxel grid from each tube (`grid=True`, a MESH_TO_VOLUME object), and the card is gone. The "hose" and "painted" edges the judges saw came from the same thing.
- **Pass 2** (g2): the column rises from the floor behind-left as a grid, with a backdrop pool, fills up and the kicker down.
  - Reads, twice: stands, "smoke from the floor at the far left, not from the speaker", no fire, no figure, the front readable but dim.
  - Duel: A 6.0, E3 4.75. The judges: crushed blacks, the plume "flat, cut-out", the floor contact weak, the product small.
- **Pass 3** (h3, a 64-sample test): fills and the backdrop pool lifted, a softer lit floor, a softer column, the camera nearer. Its proof was stopped when the owner wrote.

**The owner, 2026-10-20:** "Maybe studio for the smoke isn't right, since it should really be black smoke."

**E4** (`smoke_studio_black.py`, proof element-smoke-e4-black-p0): the same column made black, sooty and absorbing (albedo #0A0A0A, density 60), on a pale grey seamless lit soft from the front-left. The black smoke reads like ink in water, and the speaker reads clean against the pale ground. It is a test frame for the owner's direction, not yet read-tested.

### E4 and E5 for the owner (the coordinator, 2026-10-20: carry E4 to a passing read; add a location with real black smoke)

- **E5** (`smoke_saltflat.py`): a salt pan (Poly Haven `aarfontein_pan`, a real dry lake bed), the ground `dry_ground_01` whitened, the frame near-monochrome. A black smoke canister lies on the crust behind and right of the speaker; its plume rolls low behind the speaker, then climbs.
  - p0 read: "floats", because there was no contact shadow (the sky's sun sat 3° up and behind).
  - The sky was turned to bring its sun front-left and raised to 14°.
  - p1 read: **stands** ("a soft contact shadow and a cast shadow to the right"). "Thick black smoke, sooty, close to ink", rising from the ground behind the box. No fire, no figure. The front readable.
- **E4** (`smoke_studio_black.py`):
  - p1 read: "ink dispersing, soot or a smudge painted on the backdrop".
  - The smoke was made grey-black (albedo #383838) so its billows shade, given a rim from behind, and made to rise visibly from the floor.
  - p2 read: stands. "A wisp of dark grey to black smoke, though blurry enough to also look like an ink smudge." No fire. "Mostly no" figure (the streak "could faintly suggest a tendril"). The front readable. A marginal pass.
- **Side by side:** `element-smoke-e4-e5-e3.jpg` (E4, E5, then E3 pass 2 for reference). No duels until the owner picks.

### E6 and E7, the owner's two routes (2026-10-20)

The owner, via the coordinator: "Salt flat, but a smoke canister on a salt flat is so random. It really comes down to the quality and pervasiveness of the smoke if we go that route. Another route could be like an apocalyptic or riot scene, with cars crashed and burning on a bridge, billowing black smoke, with the speaker in the foreground." E4 and the canister are dropped.

- **E6** (`smoke_pan.py`): the salt pan with no source in sight.
  - A black plume of stacked woodsmoke cells (soot #161616) rises 300 m off, behind the rise, and shears left. Mid billows lie along the horizon, and near wisps sit low over the crust.
  - A 40 mm lens, so the tower fits the frame. The sun is front-left and gives a long cast shadow.
  - The first tests showed nothing: black smoke needs about ten times the density of white to read against a bright sky.
  - Read: stands. "Black smoke… rises in a column from behind the earth bank… as if something is burning out of sight." No fire, no figure ("the top unit's dark fins could read loosely as a hand or claw"). "Cinematic, but somewhat CG… a clean render dropped into a softer backdrop."
  - Not yet done: the plume spreading across half the sky, layers rolling up to the speaker, and the smoke's shadow on the crust.
- **E7** (`smoke_bridge.py`): a freeway bridge at blue hour (Poly Haven `highway_bridge_sunset`), with wet asphalt, lane markings and modelled Jersey barriers.
  - Three sedans are simple extruded forms, two of them charred, with fire cores glowing inside their cabins, embers, and black smoke billowing up and left. Low smoke pools round the wrecks.
  - No CC0 car model was available, so the cars are forms in silhouette. The first pass, with cut-out flames and lit cars, read as toys.
  - Read: "a roadway or overpass at dusk… a vehicle is burning", stands, thick black smoke from the burning car, no figure. The weakest element is the car: "a flat, low-detail silhouette with a uniform orange glow". The HDRI's own trees and mast show to the right.
- **Side by side:** `element-smoke-e6-e7.jpg`. No duels until the owner picks.

### E6 and E7 to a realistic standard (the owner: "Both need more work and realism for me to make a call")

**The gate**, restated by the coordinator after calibration: each image scores at least 4.5 from two fresh realism critics (the live A scores 4.0 and 4.0 on the same critic), passes the read test, and has no fake-looking element.

Fixes common to both:
- `smoke_el.occluder`: a shadow-only disc in the speaker's base for its contact shadow. It is a set piece; the product is untouched.
- Grain (2.5) and shallower focus.
- A long `ground()` patch subdivides at 1.5 cm and ran past the container's memory, so E7's deck is a textured slab.

**E6, the salt pan** (`smoke_pan.py`):
- What changed: the plume's head is a sheet spreading across the sky, low layers roll toward the speaker, there is haze to the horizon, and a high shadow layer lays the smoke's shadow across the crust while the speaker stands in a sunlit gap. The crust is 4k on a 7 m tile, the soot has some albedo so its sunlit sides show, and the sun is 3.5° wide.
- Realism, by proof: p1 3.5 / 3.5; p2 3.5 / 3.5; p3 4.5 / 4.5.
- Read (p3): stands (a long firm shadow), "black smoke, a tall column like a burning oil well", no fire, no figure.
- The critics' remaining tells: the speaker's clean surfaces (the product), the smoke's soft edges, and the crack tile repeating.

**E7, the bridge** (`smoke_bridge.py`, `kit_ext/wreck.py`):
- No CC0 car was reachable, so `wreck.sedan` is a burnt-out saloon from real proportions: charred paint, rust and bare steel, a crumpled nose, no glass, a sagging roof, charred seats, bare rims on puddles of melted tyre.
- `wreck.flame` is fire as a volume whose emission follows its density in a black-body colour (1050 to 1800 K). The volume's own black-body emission ignored density and lit the whole box.
- The scene: a four-lane overpass with footways, railings and lamp posts, and the city at twilight (Poly Haven `sunset_jhbcentral`). The fire lights the road and rims the speaker, and the smoke rises from the wreck, darkening as it climbs.
- Realism, by proof: p1 4.0 / 4.5; p2 4.5 / 4.5; p3 5.0 / 5.0; p4 5.0 / 4.5.
- Reads: p3 "floats", because there was no contact shadow or reflection. p4, with a shallow puddle the speaker stands in, reads **stands** ("its base sits in the puddle, with a reflection and contact darkening"), "an urban overpass at dusk… a car is on fire", black smoke from the burning car, no figure.
- Flagged as fake on p4: the puddle's sharp edge ("like a cut-out decal"), the smoke column too uniform, and the fire small for its smoke. The puddle is the one I'd fix next, with soft wet margins.

**Side by side:** `element-smoke-e6-e7-real.jpg` (E6 p3, E7 p4).

**The coordinator's follow-up pass (during the owner's wait), reverted.**
- **E6 p4:** sharper, finer smoke edges and a longer crust tile. Realism fell to 3.5 / 3.5, and the read test saw "a mushroom cloud or a giant hooded figure" in the sharpened plume.
- **E7 p5:** a bigger fire, a broken-up column, a smaller puddle with a wet margin. Realism 4.5 / 4.5 and "floats" again, with the puddle still read as a decal.
- Both are worse than E6 p3 and E7 p4, so the set files are restored to those proofs (5811e3e), which stay the ones in front of the owner.
- The critics vary by about half a point between runs, so gains under that are noise.

**E6 structural pass (the coordinator, while the owner decides): p5.**
- What changed: three modelled folds of land (`smoke_el.ridge`) stand at 330, 540 and 860 m, each lighter and bluer. The plume rises behind them and its top shears downwind as one column; the separate dark mass is gone. A warm, 4°-wide sun comes through the smoke. The crust has a 22 m cell beyond the near patch, plus salt patches. The kickers are off the horn's mirror top.
- Realism, scored beside the live A in the same run, order swapped: E6 4.5 against A 5.5, then E6 4.5 against A 5.0. Paired, A scores higher than it did alone (4.0 / 4.0), so E6 trails A by 0.5 to 1.0 and does not clear "A + 0.5".
- Read: "a dark, boxy loudspeaker… stands alone on a cracked, dry lakebed, with a thick column of black smoke rising from the hazy horizon behind it". No mushroom ("no distinct cap on a narrow stem"), no figure, no face.
- Remaining tells: the plume is "a soft, uniform volumetric blob" without fine turbulence, the crack tile still repeats near the camera, the hills read as a "blurred backdrop band", and the horn's top is still a white field.
- No Smoke horn preset exists in this repo or on main (searched), so that fix is not applied.

**E6: p3 against p5, then p6 (the last pass under the stop rule).**
- **p3 against p5:** the blind duel on two critics, order swapped, came out 4.5 v 5.5 and 5.5 v 4.5. Each judge preferred the image shown second, so it is a tie with a position bias, and p3, the incumbent with the owner, stands.
- **p6** (`4400ad6d4b85ddd832525dd55e4d3e1ad36fd431`) put p3's low warm sun back (1.75°) and graded the sky warm near the horizon. It added turbulent, brown-grey plume edges, gullies on the near fold, salt patches near the camera, and a black flag high behind the camera so the horn's resin mirrors dark there. (From a 0.8 m camera, the horn's faces mirror the sky behind the camera, not above the speaker.)
- **p6 against p3:** p3 5.5 v p6 4.5, then p6 5.5 v p3 5.0. Split again, the same position bias, so no 0.5 win on both.
- **p6 read:** "a thick plume of black smoke rises from the horizon behind it", but the shapes check failed: "it reads easily as an explosion or a mushroom cloud". The billowing, sheared top is the cause.
- **Result:** p6 fails the gate. E6 stops at p3 and its set is restored to p3 (88532b0). The ridge and gully pieces stay in smoke_el for later use.
- **On the critic:** two passes in a row have split 1–1 with each judge preferring the second image. At this level the paired duel measures order more than quality.

## E8, the speaker came down like an asteroid (the owner, 2026-10-20)

The owner chose **"Smoke: A, salt flat"** (E6 p3; its finals go to helpers from bf7ae75), with a note: "The Smoke options are both weak. The bridge could be a lot cooler if it looked like the speaker slid along the asphalt and ground it up, like an asteroid might. It needs way more realism though, like a movie still."

**The set:** `smoke_impact.py` and `kit_ext/impact.py`.
- E7's overpass, with a 1 m by 0.34 m gouge 22 m long down the near lane, and the speaker at its end, sunk 0.3 m.
- Along both lips, asphalt plates torn up: an asphalt top, with sub-base under and at the broken edges.
- A scorched aggregate floor, debris thrown wide and finer with distance, and grit at the speaker's feet.
- Dust and smoke still rising from the gouge, and embers in the air.
- A low camera along the gouge: 40 mm at f/2.

**p0** (960 px, 128 samples):
- **Read:** "a dusk city overpass after some kind of disaster: a burning car sends up black smoke… and a dark rectangular speaker-like box sits in a cracked trench in the asphalt, surrounded by broken concrete and drifting sparks or embers". No figure. The read doesn't say "crashed" or "slid".
- **Movie-still realism:** 4.0 and 4.0. The tells:
  - the trench floor reads as sand;
  - debris is even on both sides, not thrown forward along the slide;
  - no scorch or dust on the speaker's lower faces;
  - the embers are uniform dots;
  - no halation;
  - the speaker is dark and flat, with no fire on its faces.
- **Duel against E6 p3**, four judges, each order twice:
  - E8 first: 4.0 v 6.0, and 4.0 v 6.0, both preferring E6.
  - E6 first: 4.5 v 5.5, and 4.5 v 5.5, both preferring E8.
  - Means: E6 5.25, E8 4.75. Every judge preferred the second image shown, and E6 carries the net by 0.5.
  - The judges who preferred E8 cite its impact ("one clear cinematic idea"). Those who preferred E6 cite the product being legible.

**E8 p1** (the coordinator's composition note): the gouge turned to run away behind the speaker toward the wrecks, a bow wave of heaved plates in front, an 8 cm asphalt course in section on the walls, backlit dust over the trench, a camera low and off-axis on the speaker's face, a burning fragment by the lens as the key, finer embers, halation, and a black flag for the horn's mirror.
- **Read:** "a boxy speaker sits on a wet, rubble-strewn rooftop at dusk… broken concrete chunks lie around it… a burning vehicle giving off sparks and smoke". No figure. "The top box: its white blob around the black hole could be seen as a mouth or a face at a glance."
- **The read target failed.** There is no crash, slide or impact in the sentence, and the gouge doesn't read from this angle.
- **Movie-still realism:** 4.5 and 4.5, up from 4.0 and 4.0. The tells:
  - clean, faceted low-poly slabs with no fines, aggregate or rebar;
  - debris scattered radially, not trailing one way;
  - no dust skirt at the speaker's base;
  - fire spill missing from the speaker's far side.
- **Duel against E6 p3**, four judges, each order twice:
  - E8 first: 4.5 v 6.0 and 5.0 v 6.5, E6 preferred both times.
  - E6 first: 5.0 v 6.5, E8 preferred; and 5.5 v 4.5, E6 preferred.
  - Means: E6 5.75, E8 5.125. E6 is preferred 3 to 1.
- **The flag misfired.** Three judges read the horn's black-and-white reflection as a "texture error". The horn mirrors the flag as a hard black blotch against the white sky.

**E8 p2:** the camera at 1.2 m on a 35 mm lens with the furrow running to the burning wreck, crumbled near-black asphalt, fines sprayed along the slide, the flag removed, the speaker turned to 26°, and a deeper grade. Also a fix: plate vertices are now tracked by index, because bmesh vertex wrappers are not stable after `subdivide_edges`. Every earlier plate had been re-placed with each new one.
- **Read** (neutral): "a tall, dark speaker cabinet stands upright in the middle of a cracked, rubble-strewn city road at dusk… behind it a car burns". This misses the slide. The figure check is "mildly": a robot, with the waveguide as its eye.
- **Realism:** 4.0 and 4.5. The rubble reads as "crumpled paper or styrofoam", pale where the foreground fire lights it.
- **Duel against E6 p3**, four judges, each order twice: all four prefer E6, scoring E6 6.0, 6.0, 5.5, 5.5 against E8's 4.0, 4.0, 4.0, 4.0. Means: E6 5.75, E8 4.0.
- **Stop rule:** the read missed again, so one higher three-quarter frame follows (p3), and then E8 stops.

**E8 p3** (the stop-rule frame): a high three-quarter view from above the bow wave, looking down the furrow to the wrecks, with darker debris and the foreground key on the speaker only.
- **Read:** "an upright, box-shaped speaker-like object… sits in a broken trench cut along the centre of a wet, cracked multi-storey car-park deck at dusk… a burning car and a wrecked car behind it". It names the trench but not the slide. No figure.
- **Realism:** 3.5 and 3.5. The trench reads as "a clean, flat-bottomed rectangular cutout… a boolean cut with scattered props", and the debris is evenly spaced, not thrown.
- **Duel against E6 p3**, four judges, each order twice: all four prefer E6. E6 scores 6.0, 5.5, 6.0, 5.0 against E8's 4.0, 4.0, 4.0, 4.0. Means: E6 5.625, E8 4.0.

**E8 stops here, per the stop rule.**

| | Read names the slide | Realism | Duel mean, E8 v E6 p3 | Judges preferring E8 |
|---|---|---|---|---|
| p0 | no ("a box in a cracked trench") | 4.0 / 4.0 | 4.75 v 5.25 | 2 of 4 |
| **p1** | no ("rubble-strewn rooftop") | **4.5 / 4.5** | **5.125 v 5.75** | **1 of 4** |
| p2 | no | 4.0 / 4.5 | 4.0 v 5.75 | 0 of 4 |
| p3 | no ("a broken trench cut along…") | 3.5 / 3.5 | 4.0 v 5.625 | 0 of 4 |

- **The best E8 is p1** (element-smoke-e8-impact-p1.jpg), with the highest realism and the closest duel. p0 split by position.
- **The constant** across every judge: the disaster story buries the product, and the trench and rubble read as CG.
