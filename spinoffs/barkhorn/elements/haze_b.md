# Haze, concept B: layered hills at blue hour

"Dusk, kept indoors." Coastal hills recede range after range into violet haze, each paler than the last; a pale sun
sinks into the haze behind the far ridge (the icon: a sun behind three bars of haze). The speaker stands on the near
ridge in dry grass at eye level, the last light behind it, so its violet acrylic glows with the dusk instead of
standing out from it.

- Set: `haze_b.py` (shot and portrait), its pieces in `studio/engine/kit_ext/haze_b_el.py`.
- Build: `python3 spinoffs/barkhorn/elements/build.py haze_b`, then
  `python3 studio/engine/render.py studio/shots/barkhorn/element31/haze_b.json --out OUT.png [--scale S --samples N]`.

## How the set is made

- **Sky.** Poly Haven `qwantani_dusk_2_puresky` (CC0), a clear dusk after sunset, pink at the horizon and lavender
  above, turned 60 degrees so its afterglow sits behind the speaker.
- **Sun.** A sun lamp at azimuth 173, elevation 1.3 (just behind the speaker, a little to the camera's left), warm
  (#FFB48C), and a disk the camera sees (0.6 degrees) at the same place. Both reach the camera and the set through the
  haze, so the sun is pale and the light it throws is soft: one sun, one set of shadows, and the speaker's shadow runs
  toward the camera.
- **Ranges.** Six heightfield layers behind the ridge, their crests wandering along x with ravines down their faces,
  textured with Poly Haven `rocky_terrain_02` (aerial) and dotted with scanned shrubs and trees (`searsia_lucida`,
  `searsia_burchellii`, `island_tree_01`) on the nearest three: the chaparral texture of coastal California hills. The
  engine's camera clips at 300 m, so the ranges stand at a tenth of their true distance and size (25 to 255 m for
  250 m to 2.6 km): from one viewpoint perspective is the same at any scale, and at these distances an 85 mm lens
  focused at 10 m is at infinity either way. The haze's density is scaled with them.
- **Haze.** Two boxes of scattering volume over the ranges: a dense lower layer (to 6 m above the eye, 0.006/m) and a
  thin upper one (0.0006/m), lavender, scattering forward (anisotropy 0.45 and 0.75) so it glows round the sun.
- **Ridge.** A dense heightfield (2 cm) with Poly Haven `withered_grass` at its real size and true displacement,
  level under the speaker, falling away 5 m behind its crest.
- **Grass.** Dry grass as hair strands (Principled Hair, straw), tall in tufts round the frame, short round the speaker
  so its feet show; the low sun comes through the blades and rims them. The scanned grass models tried first
  (`grass_medium_01/02`, dried by a hue shift) read as dark weeds against the sky and were dropped.
- **Camera.** 85 mm at 10 m, eye 1.0 m, f/5.6, verticals level by lens shift, the speaker on the right third and
  turned 25 degrees to the camera (rotate_z 10, the camera at azimuth -15). The long lens stacks the ranges.
- **Finish.** AgX, Medium High Contrast, exposure -1.0, a little saturation and a little bloom round the sun.

## Concept proofs (scale 0.3, 32 samples)

- **A: 85 mm at 10 m, the speaker on the right third, the sun a third in from the left.** The long lens compresses the
  ranges into big, stacked bands of haze; the sun sits on the far ridge.
- **B: 50 mm at 6.5 m, the speaker near the centre, the sun at its shoulder.** The ranges shrink to a thin strip
  under a big sky; the near ground and its bare patch take over the bottom of the frame.
- **Chosen: A.** The idea is the layers, and only the long lens makes them the picture. B makes the sky the picture,
  and the sky here is a plain dusk gradient.

## Critic passes

| Pass | Scale, samples | Blind score | If fixed | Verdict | Top changes | What I did |
|---|---|---|---|---|---|---|
| 1 | 0.5, 128 | 5.5 | 7.5 | iterate | sun not behind the speaker, so nothing glows; tall grass veils its base; nearest range a smooth mound with toy trees; ranges merge into one wash; set as lilac as the speaker (white balance 4800 K, tint 6); a weak white sun; a murky front (bounce 3.5 at 3.5 m, warmer); flat grass | All eight: sun, disk and sky turned to sit at the horn's left shoulder (azimuth 166.6, sky 246.4), sun 14, disk 40 and warmer, bloom 0.2; tall grass kept 4 m clear on the camera side, short grass 4 to 15 cm round the feet; trees off the nearest range, which now carries dry grass at its true scale (darkened, a first try left it a pale dune); haze 0.0035 to 4 m and 0.0004 above, anisotropy 0.6/0.8; white balance 4800 K / 6; bounce as prescribed; grass with bleached tips and ±15 % per strand, clarity 0.1 |
| 2 | 0.5, 128 | 5.5 | 7.0 | iterate | nothing glows through the acrylic: the cabinet dark and pasted on (sun behind the horn, 24; bounce 7); grass pale mauve hair (darker, warmer straw, varied strands); white balance 5000 K / 0; sky blown (strength 0.75); hills a miniature (haze 0.0055, shrubs off range 2); contact at the feet (denser short grass); sun disk clipped (18, bloom 0.3) | The same score twice, so the systemic faults first. The critic's sun azimuth (172) pointed the wrong way: the horn is 2 degrees right of the disk, so the sun went to 164.5, elevation 1.5, where the horn hides it and rims its top. All the rest as prescribed; the grass now four systems (fine, coarse, short, a ring at the feet) in a darker straw (#5A4834/#33291F, bleached tips, ±30 % per strand); a first try at coarse grass (0.7 m) towered over the frame and was cut to 0.45 m |
| 3 | 0.5, 128 | 5.5 | 7.5 | iterate | the acrylic does not glow (sun 40, bounce 11); a cleared ring round the feet; the sun tangent to the horn; ranges collapse into one band; a flat pink sky; the hills smooth CG mounds with miniature trees; the grass an even hair system; a smear in the horn | **Changed the concept, not the settings**: three passes at 5.5, and every critic named the same faults in the modelled ranges and the sky. See below. |

### The concept changed after pass 3

Three blind critics in a row scored 5.5 whatever the light did, and each named the modelled ranges (smooth mounds,
miniature trees, one band of haze) and the plain sky. Those were the parts I had built, and no setting was going to
make a noise heightfield read as a mountain range. So the ranges are now photographed: Poly Haven `kiara_9_dusk`
(CC0, 8k for proofs and finals), real mountains at dusk with the sun just gone behind them, turned so its glow sits
left of the speaker (rotation -118, sun azimuth 168, elevation 4.2, matched by `sun_from_sky` at irradiance 2.5). What
stays modelled is only what the camera is close to: the near ridge, the dry grass and the speaker. A single veil of
lavender haze (0.0012/m, anisotropy 0.75) between them and the photograph puts the violet in the ranges and a glow
round the sun.

Two lessons on the way, both about the haze box:
- **The camera's clip (300 m) must hold the box's far wall.** With the wall at 290 to 300 m, rays angled more than a
  couple of degrees off the axis reached it beyond the clip, never found their exit and took no haze, which left a
  hard vertical seam down the frame. The wall now stands at 200 m. (The passes 1 to 3 boxes ran to 300 m, so their
  haze was cut the same way wherever no hill stopped the ray first.)
- **The bounce card stands beside the camera now** (11.5 m out, irradiance 10), as a reflector would, not in the
  frame's left third.

| Pass | Scale, samples | Blind score | If fixed | Verdict | Top changes | What I did |
|---|---|---|---|---|---|---|
| 4 | 0.5, 128 | 5.0 | 6.8 | iterate | "the photographed ranges and sky read as real"; but the speaker flat and pasted on (no rim); sky blown above the ridge; the grass curly CG hair, pale as frost; a uniform veil flattens the photo's own layers; dull lining (bounce 16 at 6 m); no footing; a dark band of ridge through the grass; milky overall (contrast 0.10, bloom 0.08) | Agreed at full size on the grass: its noise roughness curled every blade. Straw now stiff (no roughness along the blade), darker (#4E3E2C/#3A2E22, tips #8A7050), denser; the sun from the photograph's azimuth (168; the critic's 155 would have been the camera's right) at elevation 6 to clear the ridge, irradiance 6, warmer; exposure -2.6 for the sky; veil 0.0007; bounce as prescribed at azimuth -25 to keep it out of the line of sight; a shorter, thinner ring at the feet; ridge displacement 0.06; contrast and bloom as prescribed |
| 5 | 0.5, 128 | 5.5 | 7.5 | iterate | sky blown neutral (exposure -3.2); the grass front-lit by the bounce (bounce 2.5 m, 1 x 1 m); sun too weak to rim (12); a single soft range, the 8k plate upsampled (a 40 MP backplate); the glow left of the speaker (turn sky and sun 4.3 deg); no contact at the feet; pale flecks on the ground (matte, albedo 0.4); a hot streak on the horn (bloom 0.04, bounce higher) | +0.5 on pass 4, so on to pass 6 (the coordinator's new rule: stop after two passes in a row gain under 0.5). All but the backplate: the sky and sun turned to -113.7 / 163.5 (which also brings a nearer dark range in on the left: three layers now); exposure -3.2; sun 12; the bounce 2.5 m out, 1 x 1 m, at elevation 25 so its reflection leaves the horn's face; the ground matte, and `sparse_grass` (darker litter) in place of `withered_grass`, whose pale patches were the flecks; a thinner ring at the feet with a bare strip at the front. No CC0 40 MP plate of layered ranges is in the toolkit; the finals use the same sky at 16k |
| 6 | 0.5, 128 | 5.5 | 7.5 | iterate | the speaker crushed dark (bounce 40, 2 x 1.5 m at 2 m); no rim from the sun (22, elevation 4, #FFB878); a hard shadow column toward the camera (turn sky and sun 18 deg); grass too bright and even (darker straw, brighter tips); the ridge crest a straight cut line (grass over the crest); a grey sky (5400 K / 20 and graduated filters); a ghosted base (shorter grass at the feet); only two planes of range (a low veil in the valley) | No gain on pass 5: one pass under 0.5. All but two: the shadow column softened by a sun 4 deg across (a sun through haze) rather than turning the plate 18 deg, which would have moved its glow off the speaker; no graduated filters (the finish has none), white balance only, and 5000 K / 20 in the end because 5400 K turned the haze salmon. The low veil came out at 0.0009 (0.003 washed the ranges once the sun was 22) and the main veil at 0.0005 |
| 7 | 0.5, 128 | 4.5 | 6.5 | iterate | the speaker front-lit by the bounce while the sun is behind (bounce 12, sun 45); a cleared patch round it; stiff, uniform straw; no sun glow in the sky; magenta cast (tint 6); a dark crest band; weak depth (valley veil 0.0022); camera lower so the horn rises into the sky | Stopped (below) |

### Stopping

Passes 6 and 7 both gained under half a point (5.5 to 5.5, then 5.5 to 4.5), which is the coordinator's stopping rule
after a concept change. The critics' notes in the last three passes swung back and forth (pass 6: the speaker too
dark, so a bounce of 40; pass 7: the speaker front-lit by that bounce), which says the light on the speaker, not a
setting, is what holds the image down. Five frames scored 5.5 (passes 1, 2, 3, 5, 6), so the best rig was chosen by
blind duels between them before the finals.

### The duels

Blind, by the duel prompt (`critic/ab/PROMPT-DUEL.txt`, run by hand so `critic/best.json` stays as it is), proofs at
0.5 scale:

| Duel | A | B | Scores | Preferred | What decided it |
|---|---|---|---|---|---|
| 1 | pass 6 (photographed ranges) | pass 3 (modelled ranges) | 5.0 / 6.2 | pass 3 | the cabinet lifted and legible, the horn rimmed with light, one continuous grass layer; pass 6's murky cabinet, a seam and a boxy shadow in its grass. Pass 6 won only on its crisper ridge and sky |
| 2 | pass 5 | pass 6 | 5.0 / 5.8 | pass 6 | the cast shadow grounding the speaker, a cleaner stem bed, warmer backlit grass |

So the order is pass 3, then pass 6, then pass 5, and the finals are rendered from pass 3's rig (`haze_b.py` is back at
that version; the photographed version is in git at b761a8d). Pass 6 is the runner-up.

## Finals

`renders/2026-10-18/barkhorn/element31/haze_b.png` (2400 x 1600) and `haze_b-portrait.png` (1600 x 2000), each with
its `.report.json` and `.shot.json`, from pass 3's rig at 512 samples, denoised. The container restarted twice under a
single two-hour render, so the finals render in eight horizontal strips with the finish off, each strip saved as it
lands (a restart resumes at the next), then stitched (32 px overlaps, aligned and feathered) and finished once over the
whole frame: `haze_b_strips.py`. Landscape: 99.3 min of rendering (the sky's strips about 2 min each, the grass's 16
to 27); portrait: 74.7 min. Both on four CPU cores. The portrait is re-framed, not cropped: 105 mm from 7.5 m, the speaker on the right, the sky above for type.

**The blind critic on the landscape final: 5.5** ("a competent atmospheric CG render, not a photograph"; if fixed, 7.3).

### What holds it at 5.5, honestly

- **The speaker's light.** Every critic, in every pass and both concepts, found the cabinet either flat and front-lit
  (with a reflector) or dark and murky (without one), and never glowing. The cabinet is violet acrylic lined white
  inside, so a sun behind it cannot shine through it; only the horn's resin and the cabinet's edges can carry the
  backlight. A backlit dusk is the brief's light, and in it this speaker reads dark unless it is filled from the
  front. The answer is probably a side light (the low sun raking across the cabinet's visible side), which moves the
  sun out of the frame and breaks the icon's "sun behind the haze"; that is a change to the concept for the owner to
  choose.
- **The grass reads as CG hair.** Hair-strand grass, however coloured or stiffened, was called fur by most critics.
  Scanned grass models were tried first and read as weeds. A photogrammetric dry-grass asset at this scale is not in
  the CC0 toolkit.
- **The modelled ranges.** The nearest range reads as a smooth mound, and the ranges' haze as one band. Photographed
  ranges (passes 4 to 7) fixed that ("the ranges and sky read as real") but lost the duel on the speaker and the grass,
  which stayed the same.
- **The sun disc touches the horn's top edge** in the final, and the frame is milky (the critic's c2 and c5). These
  are fixable in one more pass, but they would not move the score past the three above.
