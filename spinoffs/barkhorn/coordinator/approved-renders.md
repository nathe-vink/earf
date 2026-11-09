# EARF approved pictures: the one list every asset draws from

Started 9 Nov 2026, 21:10 UTC, at the owner's direction ("we need to sequence the work, so the marketing and brand assets use the
right product renders"). Kept by the coordinator. A picture goes on this list only after it passes the blind gate (majority SHOW)
and the studio honesty rules (nothing hidden from the camera standing in frame; one sun, the sky's own; every object casts shadows).
The site, the Brand Book, social, the deck and press use ONLY pictures on this list. When a picture is replaced, the old line moves to
"Pulled" with the reason, and every asset that used it is refreshed in one batch.

## The order of work
1. LOCK EACH PRODUCT'S DESIGN AND MATERIALS. Tropos: locked (base A, no light; the polished horn; one dye per tint from
   tints-trucast.json), except Haze's horn pour (walkthrough 132). Lamps: DESIGN LOCKED 9 Nov 21:12 (the owner: Core B, "assuming we're still
   using the same materials we would use for the speakers and mantle": the outer ball in the speaker's TruCast tints, one dye per tint;
   a 3 mm white opal inner ball, the same opal as Hemisphere's diffuser); the lamps lane to confirm the CAD, BOM and stock in writing.
   The lamp kit's Ember dye was a stale hand value until 9 Nov, now the speaker's 2423. Mantle: locked as drawn (Strata Float).
2. LOCK THE STUDIO PICTURES OF EACH LOCKED PRODUCT. Tropos: the seven fronts (9 Nov), then the backs, close-ups and wides. Lamps:
   in Core B. Mantle: the day frame is in.
3. ONLY THEN REBUILD THE ASSETS (site, Book, social, deck) from this list, one batch per lock.
Scenes (habitats, night pictures) use the locked models and can run alongside; each enters an asset only after it passes.

ASSETS OUT OF DATE (checked 9 Nov 22:33), not to be sent until rebuilt from this list:
- the investor deck (artifact 3sihYaT4ckNTF6WE7SWR7x, v68): lit plinths, the stepped horn, Smoke as an eighth color, glowing
  Hemisphere and Core (light.html, line.html), the uplit eight (cover, colours); rebuilt in step 3.
- the brand lane's parked pieces: the investor one-pager (its lamp row), the launch grid (posts 2 and 5), the teaser (beats 3, 6):
  marked held in their manifests.

## Tropos
IN-FRAME AUDIT UNPROVEN (9 Nov 23:10): the speaker lane's cast (shots._frame_rays) built the camera differently from render.py
(the sensor fitted to the larger side and the lens aimed, where render.py fits it horizontal and shifts a level camera). On portrait
frames it was 20 % too narrow and pitched wrong: 0cbf23a5's floor cards cast 0 % and showed; two reflect-only back cards stood 4.9 %
in the tall's frame. Fixed in 0c6acd5d. A second error (23:23): with sensor_fit HORIZONTAL Blender measures lens shift in frame
widths, not the larger side; the cast sat 54 rows high on the tall, and the tall's bg-left lamp (camera-hidden) stood in frame,
441 px at the top-left, on every tall rig up to 3603508e. Fixed in fa7665dc (checked against bpy's world_to_camera_view), whose mask
pass now draws every camera-hidden mesh and lit area lamp as well as the equipment. Every "0 hidden in frame" below is being
re-proven by that mask (the speaker lane, one render per distinct camera and set) and by the Mantle lane's gt_audit.py (b730fe6b)
elsewhere; a picture with anything hidden in frame is pulled at once. Verified so far: Mantle by day (41232b56) and the Ice wide
night final (78e440ba), 0 px hidden. Lamps (23:34): the bpy rigs' audit read the camera at its rest pose (fixed; the mask check
hiddencast_bpy.mask_check now rules); clean by the mask: the dome and orb heroes, lamps-domes-7, Core A/B day and night, Hemisphere
night and day, the unlit Ember 4:5 and the full Ember pair; NOT clean: round 3's orb row (see Pulled).
Lights audit (9 Nov 21:40, from each shot.json): the turning views, the horn-backs and the amp plate are lit by key, fill and wash
(area lights) plus background lamps linked to the sweep (flagged background lights); chunks 4 and 05 (06b829ce, 52ad76ba) also carry
the old glow lamp, which I let stand at 21:40 as noise-level. WRONG: it is camera-hidden, emits (irradiance 1.6) with specular 0, and
stands in frame (16-20 % by the corrected cast; 61,101 px on a horn-back by the mask, 23:27). Every picture carrying it is pulled below. No specular-only source in any of them. The tallr2 fronts carried
three specular-only panels (scrim, sheen, topline at diffuse 0): withdrawn from the re-shoot (21:34) so the fronts are lit only by
lights a real studio could use.
| Picture | Source (branch @ commit: path) | Gate | Used by |
|---|---|---|---|
| Seven fronts ("talls"), honest rig round 2 | helpers r33-rollout-c2/c3/c4 and r33-speaker-horn, renders/2026-11-04/barkhorn/rollout/A-polished-tallr2/site-front-off-tall-<k>.png on 63d83f47 | FAILED 9 Nov 21:24: Ember, Acid, Ice 3/3 NO; Dust 1/3 (21:28); Fog 2/3 SHOW (founder, skeptic; photo NO), kept only as a fallback since the set is re-shot on one rig; Poison, Haze 0/3 (21:31: the lower side face milky, see-through fails). tallr3 FAILED 0/3 (22:39); tallr4 pulled as tests (23:05); tallr5 on 3603508e stopped (bg-left lamp hidden in frame); next on fa7665dc (one floor card out of frame, the speaker turned 6°, bg-left slid out, 0 px hidden and 0 px equipment by the mask), tag tallr6 | none until the re-shoot passes; the site and the Book wait for it |
| Turning view, Dust, Acid, Poison, Ice, Haze (Ember HELD: its frames 00-04 pulled, see Pulled) | r33-rollout-c3 52ad76ba (Ember 00-04, PULLED); c4 0a0a83bd (Ember 05-23, Dust); c4 42fa8eee (Acid 00-16); c3 66126d53 (Acid 17-23, Haze); c4 eef18db2 (Poison, Ice): renders/2026-11-04/barkhorn/rollout/A-polished-p2*/turn-<k>-NN.png | PASSED (wf_c0448c65-cd3); VERIFIED by mask 9 Nov 23:44 (r33-speaker-horn c7907aca REAUDIT.md: 0 px hidden, 0 px equipment, every group) | site galleries (Ember's turn held whole) |
| Turning view, Fog, neutral ground | r33-rollout-c3 a688c59e: A-polished-p2-rc2/turn-fog-00..23.png | PASSED 3/3 (9 Nov 21:11; the stage at the rendered 211,212,207); VERIFIED by mask 9 Nov 23:44 (rc2 fog: 0 / 0) | site gallery (FOG_TURN on) |
| Horn from behind, Acid only | a1322583 (A-polished-p2-backrig-acid), cut 4:5 at x 270-990 | PASSED; VERIFIED by mask 9 Nov 23:44 (its group, backfix/backrig horn-back-acid: 0 / 0) | site galleries (the other six PULLED 23:27, see Pulled) |
| Amp plate, Ember | 488fbec9 (amp-plate-ember) | PASSED; VERIFIED by mask 9 Nov 23:44 (0 / 0) | site galleries ("The built-in amplifier, from behind.") |
| Backs (rear three-quarter) | r33-speaker-horn e85bd44f (round 3, bright-field glow) | NOT YET: full-size renders and gate pending | none |
| Wides | r33-speaker-horn 89d95763 (the wide's horn lamp off) | NOT YET: renders and gate pending | none |

## Habitats (scenes)
The shadow rule (9 Nov 21:25, biomes 3122f00c, proven by a slab test): until then a tinted wall passed tr² × volume to shadow rays (the tint
three times, the Fresnel loss twice). From now on each face carries √0.92 and the welded volume gives the tint once. Files made under
the old rule are marked; each is re-rendered under the new rule and gated against its passed file before it is swapped.
| Picture | Source | Gate | Used by |
|---|---|---|---|
| Ice, "Out in the snow at dusk." | 0f619953 | PASSED (verified 9 Nov 22:56 under the current rules: tint once, the horn under the rule, angle-dependent Fresnel; within noise, the file stays; gt_audit 23:40: no hidden object, no area lamp: sun and sky only) | site (home band, /tropos/ice, /colors/ice), Book |
| Dust, "On rippled sand among desert buttes." | r48-biomes 43c91242: renders/2026-11-03/barkhorn/habitats/dust-portrait-1200x1500-nopanel.jpg | PASSED 3/3 (9 Nov; under the current rules 22:56 the table is within noise but the horn's pod changes: re-render with the horn under the rule queued; this file stays until it passes). GROUNDED FLAGGED 9 Nov 23:13: the biomes lane's gate on the re-render saw a 6-8 px band of lit sand between the front edge and the shadow's start (no dark contact line; lifted at phone size), and this file's base is identical; a deeper bed in the sand is in test, then the fixed final is gated against this file, "grounded" first | site, Book |
| Fog, "In the grass on a hillside, in fog at dawn." | PULLED 9 Nov 23:40, see Pulled; a re-render without the fill lamp follows | | none |
| Acid | r48-biomes 539c3772 | HOLD 1/3 (rain stops at the speaker; dry; dark cabinet) | none |
| Poison | r48-biomes P8 proxy (b60934b7, the horn under the rule) | PROXY PASSED for the final 2/3 (9 Nov 23:08; exposure 0.75 by all three; watch the horn's crease glint at full samples); the final queued after Dust | none |
| Ember, Haze | not started (Haze waits on the horn pour) | | none |

## Lamps
HEMISPHERE AS DRAWN DOES NOT GLOW (lamps lane photometry, 9 Nov 22:22; confirmed in the Mantle lane's scene 22:31): the COB sits at
the top of its 46 mm bore and all its light leaves through the mouth; every lit Hemisphere picture so far took its glow from an
added emitter on the liner ('opal-lit'). No lit Hemisphere picture may enter any asset until the owner answers walkthrough 135.
None approved. Hemisphere switched off in Ember, native 4:5 (e7847359): HOLD 0/4 (9 Nov 23:49): the colour now right (hue 35, dE00 2.5 to the
speaker's Ember; plum and violet gone), held for the backdrop (cream-peach, dE00 4.6 from the Tropos white), a rose key glint, the strip's
neon-like arc, and the hub under the cap; fixes sent 23:50. Earlier: the 4:5 crop HOLD 0/4 (9 Nov 21:42): honest and clearly off, but the Ember reads
crimson (a rose reflection over 28-44 % of the face; cool lights on the shell) and the right-rear strip was specular-only. The lit set,
round 3: HOLD 0/3 (critic 4 out): the pale four read pastel, every Core B orb a milk-glass globe (walkthrough 133), no pools in the row.
The owner's decision sheets (Hemisphere glow b/a1/a2/off; Core B Ø120 vs Ø90): HOLD from the honesty gate (9 Nov 23:09, critics 3-4):
tinted front-surface highlights (the shader may carry the tint; checking), two unexplained teal discs on every Hemisphere frame, (a2)'s glow
4-10x short of its label, the studio fill too high for a night comparison, the Core B cores bleached by the view transform, and the
captions. Walkthrough 133 and 135 wait for the fixed sheets.
Core B, decided by the owner 9 Nov 21:12 (the dark border he liked comes from B's nested build). Every lamp picture is re-rendered as B.

## Mantle
| Picture | Source | Gate | Used by |
|---|---|---|---|
| Mantle by day (C3e), shown in Ember | 41232b56 (three files) | PASSED | site (/mantle, the home's Mantle band) |
Night picture (Ice Tropos under a Hemisphere pendant): proxy 9 seen (c256eb64); the final renders (about 22:50). Its pendant glows
from the lamp kit's added liner emitter, which the drawing does not have (walkthrough 135), so it cannot pass as it stands; an
as-drawn variant (the COB alone: a downlight, the shade dark) follows about 23:50. The owner's answer to 135 decides which can ship.

## Pulled (do not use)
| Picture | Why | Pulled |
|---|---|---|
| Fog habitat aa1ca856 (fog_b-portrait-1200x1500-onesun.jpg) | a 2 x 2 m fill EMITTER `fill_l` (hidden from the camera, out of frame) breaks the habitats' rule: the sun and the sky's own are the only emitters, and the caption says "lit by one sun"; a passive reflector would be allowed. (The first report, "in frame", was withdrawn 23:46: the gt_audit hits were the panel seen through the speaker's glass; projected, it lies wholly past the left edge.) Re-render without it, or with a real reflector, queued | 9 Nov 23:40 |
| Poison habitat P8 scene (not yet a final) | a 1.2 x 0.4 m fill emitter `litter` (out of frame; the in-frame flag withdrawn as for Fog); dropped or replaced by a real reflector before the final | 9 Nov 23:40 |
| Lamps, round 3's orb-row proxies (lamps-orbs-7, a/, b/, c/) | the 4 m key stood in frame with its back to the camera (22.1 % by the mask), hidden from the camera; never approved, never to be used; the rows' key is now 3 m (0 % in frame) | 9 Nov 23:34 |
| Horn from behind: Ember, Dust, Poison (06b829ce), Ice, Haze, Fog (52ad76ba) | the camera-hidden 'glow' area lamp (0.7 x 0.32 m at (0, 0.66, 1.12), irradiance 1.6, specular 0) standing in frame beside the horn mouth: 16.1 % by the corrected cast, 61,101 px by the mask on a horn-back; re-render without it queued | 9 Nov 23:27 |
| Turning view, Ember frames 00-04 (52ad76ba) | the same glow lamp in frame (19.5 % by the corrected cast); Ember's turn held whole until the five are replaced | 9 Nov 23:27 |
| The old talls (img/rc/<k>-tall.*) and wides | a lamp hidden from the camera standing in frame | 9 Nov |
| 15931e00 talls (tag tallfix) | a hard arched light pool on the backdrop (the grid's hard cone) | 9 Nov 20:25 |
| tallr4 talls (A-polished-tallr4, rig 0cbf23a5; Ember, Acid, Ice rendered as tests, the rest held) | two real black floor cards in frame at the right edge (rows ~850-1200; the cast's camera bug hid them), and a pale band in the lowest fifth of the right face (~70-80 levels of white under a hard edge at row ~905); the line itself is fixed (+0.8 L against +51.7) and the upper veil cleared (sat 0.65-0.72) | 9 Nov 23:05 |
| tallr3 talls (A-polished-tallr3, rig 74f17d7c, all seven) | the same line (it was the wedge of rising cove between the upright card's foot and the floor flag, found 22:31; the floor-flag fix had missed it) and the same veil (the lower right face mirroring the lit floor at ~64-73 degrees); critics 0/3 on every color tested; the three reflection-only panels were removed in this round, which is kept | 9 Nov 22:39 |
| tallr2 talls (A-polished-tallr2, all seven) | a thin white line on the right side face at mid-height (a strip of lit sweep between the floor flag and the slanted upright card), and a milky lower side face below a hard diagonal (the camera-right fill card in its mirror path) | 9 Nov 21:24 |
| Backs (rigB, img/rc/<k>-back) | lamps hidden from the camera standing in frame | 9 Nov |
| lamps-unlit (the Smoke pair) | hidden lamps in frame; Smoke is held | 9 Nov |
| Dust habitat 26493989 | an 8 x 3 m bounce panel hidden from the camera in frame | 9 Nov |
| Fog habitat b61474c0 | two suns 100° apart | 9 Nov |
| Fog turn rc1 (pale blue ground) | read as Ice | 9 Nov |
| Fog habitat cd5aa4e6 (same path) | superseded by aa1ca856, the same frame with the glass's real light loss in its shadows; not a fault | 9 Nov 21:21 |
| Every picture in Smoke | Smoke is held | |
