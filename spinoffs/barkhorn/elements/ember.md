# Ember, concept A: a lava field at blue hour (round 31b)

The owner, on the dioramas: "the diorama looks cheap, like a bad video game. I was hoping for more texture in a lot of
these. The speakers are too stark in contrast to the setting too. ... Maybe don't think about them so much like
dioramas, and think more about placing them in there element." On Ember: "a volcanic cavern", "well lit by lava pools
and lava falls". And: "Continue to do critic passes until you feel it's in a good enough place for promotional images
for a $20K product."

## References

Fagradalsfjall (Geldingadalir, Iceland, 2021 to 2024) and Kīlauea at blue hour and night: black crusted pāhoehoe and
ʻaʻā, glowing seams and channels, steam lit orange from below, a deep-blue sky above. The light is two-sided: the
lava's orange from below and the dusk sky's blue from above. Campaign touchstones for volcanic ground: Chanel Coco Beach
2026 (black volcanic sand as a near-studio backdrop), ICON Italy "Black Salt" (tailoring against basalt).

## Assets and software

- Poly Haven (CC0): dark_rock, dark_rock_02 (basalt), qwantani_dusk_2_puresky (sky).
- ambientCG (CC0): Lava001 (crusted flow), Lava004 (molten), through my own material (`ember_el.lava_material`): the
  set's emission map drives a black, red, orange, yellow-white ramp, so the lava keeps its hue; its colour map, darkened,
  is all that reflects.
- bpy 5.0.1 on python3.11 (setup.sh pins it; this container's python3 is 3.13).

## Critic passes (critic/PROMPT-promo.md, a fresh blind subagent each)

| Pass | Image | Score | Verdict | Top changes | What I did |
|---|---|---|---|---|---|
| 1 | e1: basalt-column gorge, lava fall in a slot, river behind, pool front left (0.5 scale, 96 samples; still under the old 5600 K / tint 3 white balance) | 4.5 | rethink | columns read as masonry with one repeated texture; lava flat decals with stair-stepped edges, no hot cores; no cool sky; the speaker as dim as the ground; embers uniform dots; the fall competes with the speaker. Its advice: narrow the set (pahoehoe foreground, one lava seam behind as a backlight, an open blue-hour sky) | Rebuilt: open lava field under a visible dusk sky, the column wall dropped, lava as a level surface under carved rock (natural shorelines), hot cores, a backlight through the acrylic, streaked sparks, soft steam |
| 2 | e2: open pahoehoe field, lava below the rock, a backlight, steam, sparks; crater rim with a fall 30 m back (0.5 scale, 128 samples) | 5.0 | iterate | near ground glossy salmon (lum 121), brighter than the speaker (58), horn dark (25); sparks uniform dashes everywhere; the fall lights nothing; haze flattens the rim (p5 48); rim has no geology; sky flat lavender; everything equally sharp | Ground albedo 0.10, roughness x0.9, point lights dimmed and raised; a bigger backlight through horn and cabinet plus a low strip; sparks 70 % fewer, near the lava only, varied; the fall brighter with its own light and a splash pool; haze 0.0012, steam in plumes; the rim as basalt columns with flow layering; sky 0.2; f/2 |
| 3 | e3: black basalt, a terraced rim 30 m back with its fall, sparks near the lava, f/2, lights rebuilt (0.5 scale, 128 samples; first render after main's lining and cloth shaders) | 4.5 | iterate | acrylic not glowing (cabinet 22 vs ground 38); lava dim (p95 79); near ground reads as sand; rim a palisade of stretched streaks; fall a blobby column; sky flat and bright; sparks uniform | Three passes at 4.5 to 5.0: by the brief's rule, the approach changes, not the settings. The procedural heightfields read as CG; next: a photographed landscape as the visible background (an HDRI with real rock), scanned rock models in front, darkened to basalt, and only the lava modelled |
| 4 | e4: **concept changed** to a volcanic cavern: Poly Haven scanned rock faces regraded to basalt, a lava river along the back wall, a fall at the left, a crack at the speaker's feet (0.5 scale, 128 samples) | 4.5 | iterate | the fall a flat card and the loudest element (median 103); the arch tan, not basalt; the floor sand dunes with stepped displacement; a hot spot from the hidden lamp (19 % clipped), the horn crushed (median 10); the sky patch flat; the river a thin glittery line; sparks uniform | Soft area lamps hidden behind the cabinet and the horn (no point), the crack light up; rock albedo x0.03, fully desaturated, roughness 0.55; floor displacement cut (no terraces), lobes smaller, ropes sharper; the fall at strength 12, thicker; the river wider with bigger crust plates; the sky turned to show its gradient; sparks clustered at the sources; vignette 0.25 |
| 5 | e5: the cavern after pass 4's changes (lamps hidden behind the acrylic, darker basalt, crusted fall) | 4.5 | iterate | lava not incandescent (fall p95 127, the sky brighter at 167), glossy like plastic; lights nothing (back wall p95 32); the cabinet's core dark (21); the slab warm sandstone; floor like crumpled cloth; sparks tracer dashes | Lava at strength 60 to 70 with a matte crust (roughness 0.85, specular 0.2) and its hottest cracks yellow; the sky at 0.07; grazing river lamps 350 W low by the wall, the crack 200 W; lamps behind the acrylic doubled and lowered; the slab fully desaturated x0.02; steam denser and lower |
| 6 | e6: incandescent lava (fall p95 187), a darker sky, grazing lamps by the river, more light through the acrylic | 4.5 | iterate | the fill washes every rock tan (back wall R44 G11 B0), the slab reads as driftwood; the fall a lit pillar; the sky a flat grey card; the horn throat crushed (26 %); no red cast on the floor; sparks white dashes; a monochrome orange frame | (pass 5 asked for more light on the walls, pass 6 for less: the critics disagree on fill.) Next: the river lamps out, the lava and steam carry the light; a cool sky rim (strength 0.25, its gradient in the opening); the horn lamp x2.5; the cabinet lamp tilted down for a red pool on the floor; 8 warm curved embers; the left lobe darker |
| 7 | e7: the cavern after pass 6's changes (fill out, sky in the opening, horn lit through, fewer embers) | 4.5 | iterate | the speaker lit only from behind (lower front 26, the floor beside it 48); a clipped hotspot on the horn (2.4 %); the fall reads as foil; the slab as a plank; the river as thin threads; the floor brown leather; the sky a flat card | Six passes at 4.5 to 5.0. The coordinator (who sees every session at 4.5 to 6.0, so the critic is harsh for all) asked for a return to the open field at blue hour (p2 and p3 had the best sense of place), with no fall, incandescent cracks, one river and a distant vent, then two more passes; if neither gains 0.5, finals from the best rig, a duel and an honest note |
| 8 | e8: **back to the open field at blue hour** (the coordinator's call): no fall, cracks and a river in black crust, a far ridge and vent, white balance 4500 K | 5.0 | iterate | basalt reads as grey-violet plaster (R48 G33 B48); lava a decal (p95 155); the speaker dimmer than the sky (33 vs 107); a rectangular pit at the bottom and a straight lit ledge at left; the ridge a soft cut-out; little steam; score_if_fixed 7.5 | The pit and the ledge's crack removed; basalt neutral and darker; lava strength 80 with gain; the lamps through the acrylic x3, the foot points 120 W low in the cracks; the speaker sunk 3 mm; the sky 0.15 at 4800 K; steam x3 behind the speaker, 30 embers; haze 0.003 for the ridge |
| 9 | e9: the field after pass 8's changes (neutral darker basalt, lava strength 80, no pit or ledge, the face lit low from the cracks, more steam and embers, sky 0.15 at 4800 K) | 5.0 | iterate | lava reads as sequins (speckled, no continuous core); the cabinet dark (31); a pale pink-white side panel (203); two spotlight pools on the rock from the crack lamps; the ridge a flat cut-out; the sky grainy and magenta; embers even; score_if_fixed 7.3 | Two passes on the field without a 0.5 gain: by the coordinator's stopping rule, finals from the best rig after a blind duel |

## The duel and the final rig

A blind duel (critic/ab/PROMPT-DUEL.txt, a fresh agent, frames in random order) between pass 9 and pass 8 preferred
pass 9, 5.5 to 5.0: its warm haze and lava bounce tie the speaker and the ground into one scene, and pass 8 still had the
rectangular pit and the stepped ledge. It favoured pass 8 for a clearer sky and ridge and a crisper cabinet. The finals
are pass 9's rig with two defect fixes from pass 9's critic, checked in a proof: the two crack lamps, which threw oval
spotlight pools on the rock, now lie flat in their cracks as thin area lamps, and the embers are twelve, rising off the
river's right-hand seam, not thirty spread over the frame. The portrait is the same set and light from the same place
on a 92 mm lens, the speaker about 42 % of the height with sky above it for type.

## Where it stands, honestly

Nine blind passes: 4.5, 5.0, 4.5 (an open lava field), 4.5, 4.5, 4.5, 4.5 (a volcanic cavern of scanned rock), 5.0,
5.0 (the open field again, at blue hour). The bar was 8.5; the critic scored every one of the eight colours' sessions
between 4.5 and 6.0, so it is harsh for all, but this is still a 5: competent, and still read as CG. What holds it back,
as the critics agree pass after pass:

- **The lava.** Built from tileable ambientCG textures through an emission ramp, it reads as speckle, sequins or a decal,
  not as molten rock with crust rafts, incandescent seams and a heat gradient. Real lava photography or a simulated
  flow (a crust-plate mask with open channels, displacement, a proper blackbody ramp) is the next step, and the biggest.
- **The rock.** A photographed basalt texture on a heightfield reads as plaster or leather at this distance; it lacks
  ropy pahoehoe and fractured a'a relief at real scale. A scanned pahoehoe surface would do more than any setting.
- **The speaker's glow.** Its dense red acrylic transmits little, so the cabinet reads dark with the woofer black;
  lamps hidden behind it light its edges more than its body. The acrylic is the product and fixed; only the light can
  help.
- **The distance.** The far ridge is a heightfield silhouette with little relief, and the dusk sky (qwantani_dusk_2) is
  more lavender than blue even graded to 4800 K.

## Final settings

- Landscape 2400 x 1600 and portrait 1600 x 2000, 512 samples, the denoiser, Cycles on the CPU (python3.11, bpy 5.0.1).
- Camera: 0.95 m, 6.5 m from the speaker, azimuth +22, f/2.8; 60 mm (landscape), 92 mm (portrait). Speaker turned 15,
  sunk 3 mm.
- Ground: dark_rock_02 (Poly Haven), albedo x0.06 neutralised, 30 mm displacement; lava: ambientCG Lava001 through a
  black-red-orange-yellow ramp, strength 80, gain 2.6, a matte crust (roughness 0.85).
- Sky: qwantani_dusk_2_puresky at 0.15; white balance 4800 K; haze 0.003; AgX, base contrast; bloom 0.18, vignette 0.2.
- Lamps: soft orange lamps hidden behind the cabinet and the horn; a low lamp from the front left as if from the
  cracks; thin lamps lying in the two cracks by the speaker; one in the steam over the river; one at the far vent.

## The finals

- `renders/2026-10-18/barkhorn/element31/ember.png`, 2400 x 1600, 512 samples, the denoiser. Rendered as four horizontal
  strips (`render.py --crop`, finish off), stitched, then `finish.py apply` once on the whole frame, because the
  container is restarted when the session sits idle and takes any untracked render with it. Strip times 1153, 4373, 3348
  and 4041 s (the last by a helper session from the same commit): 3.6 h of rendering in all. The strip seams do not
  show at full size.
- `ember-portrait.png`, 1600 x 2000, 512 samples, rendered whole by a helper session from 3d757bf (branch
  r31-element-ember-portrait, 69e9086): the same set and light on a 92 mm lens.
- A blind pass on the landscape final, full size: **5.5**, iterate (the best of the ten). Score if fixed: 7.5. What
  it names: the cabinet front still dark (median 26) with the light through the acrylic only at its edges; a pale,
  clipped right side (6.8 % clipped) and a studio-clean sheen on the horn's right half from the lamps behind; the far
  ridge a flat cut-out with a serrated crest that reads as a treeline; the midground lava as horizontal streaks and
  bokeh (f/2.8 smears the bright cracks); the sky flat and grainy; no lava close enough to light the base. Its next
  steps, if the owner wants another round: lava close to the speaker, the lamps behind moved low and out of the horn's
  reflection, a smoother caldera rim lit by the vent, larger crust plates at f/5.6, and a three-quarter view with the
  speaker on the left third.

## A2: the lava field refined (2026-10-19, the lead's round; it goes up only if it beats A in a blind duel)

`ember_a2.py`: one main flow from the left foreground past the speaker's left with a broken core ribbon, plated crust,
clinker and slabs, a volcanic cone with a crater and plume, a deeper blue hour. A fix on the way: `kit.finish` reads a
piece's `scale` as the object's scale, so a lava piece's texture `scale` also blew the mesh up (A2's core lay buried
under the crust); lava pieces now take `tex_scale`, and A, which still says `scale`, is unchanged.

| Pass | Proof | Score | What it names |
|---|---|---|---|
| A2-1 | `proofs31/element-ember-a2-p1.jpg` (5123b2a) | 4.5 iterate (if fixed 7.0) | the lava glossy, like wet plastic, the core pink-white; a hard hotspot on the horn's right half and a strip down the cabinet's edge from the hidden lamps; the front still dark (median 19.5); the slab striated; no red pool at the base; few embers, no steam seen; the cone a soft dome, the sky a flat band |
| A2-2 | `proofs31/element-ember-a2-p2.jpg` (189231d) | 5.5 iterate (if fixed 7.0) | the speaker lights no ground round it, no contact shadow; the cabinet dim (median 25) under a bright horn; the rock right of it cold blue; the slab a smooth plane; embers thin straight dashes, no steam seen; the crater a pink sun; the sky the brightest area (median 82); dark blobs of slab at the bottom edge |
| A2-3 | `proofs31/element-ember-a2-p3.jpg` (2acaff8) | 5.0 iterate (if fixed 7.3) | the horn a lightbox (median 98) four times the cabinet (24), the cabinet evenly red with no key from the lava's side; still no red pool at its foot (the rock there bluish); the foreground slab a smooth dark mass; the lava too far from the speaker, a set piece on the left; embers uniform dashes; the cone a silhouette with a blob of glow |
