# Acid, concept B: acid rain, real (round 31b)

A storm in sulphurous light over a field of wet black lava rock; the light breaking through low behind the rain, so
the streaks catch it; puddles that mirror the golden speaker. The set is `acid_b.py`; its pieces (rain streaks,
splash crowns, rippled puddles, wet ground with lava forms, wet scanned rocks, far ridges) are
`studio/engine/kit_ext/acid_rain_el.py`, a module of its own (no engine core changed).

## Assets (all CC0)

- Sky: Poly Haven `belfast_sunset_puresky` (4k): a low sun, 2.6 deg up, under an overcast deck. Others looked at:
  `kloppenheim_01_puresky` (proof B), `kloppenheim_03/07_puresky`, `overcast_soil_puresky` (no low sun).
- Ground: Poly Haven `dark_rock` (4k) near, `dark_rock_02` far and on the hills. Rocks: `rock_09`, `rock_07`,
  `moon_rock_01`, `moon_rock_04`, desaturated and darkened toward black lava, wet.

## Concept proofs (0.3 scale, 32 samples)

- A: `belfast_sunset_puresky`, the sun low behind the speaker and to its right: the sulphur haze glows, the gap's
  light streaks across the wet ground toward the camera, the speaker is backlit through its acrylic.
- B: `kloppenheim_01_puresky`, the sun to the back left: flat, blue-grey, the rain barely there.
- **Chose A**: it has one idea of light (the break in the storm behind the rain), and its colour is the sulphur the
  brief asks for; B reads as an overcast afternoon.

Lessons on the way: the camera's clip end is 300 m, so a haze box or a ridge beyond it shows as a hard-edged
rectangle (p4); a huge haze box starves the set of the low sun (p3); a single water plane over modelled hollows makes
the puddles, and hollows laid along the line to the camera make the speaker's mirror image (a low camera's reflection
of the speaker's top lands about 5 m in front of it).

## Critic passes (0.5 scale, 128 samples; a fresh blind critic each, critic/PROMPT-promo.md)

| Pass | Frame | Score | Top changes | What I did |
|---|---|---|---|---|
| 1 | c1 (80 mm, 9.2 m, haze 0.005) | 5.0 | speaker backlit to dull ochre (bounce 0.25 -> 1.1 + fill); rock a grey rolling sea (darker, tint, less swell); flat beige sky; a sparkle cluster upper right; seam band; puddles too still; low contrast; soft hills | All eight applied. The sparkles were near drops refracting the sun as round bokeh: the streaks' glass made rough (0.25), so each glint spreads along its streak. Rock displacement 3 -> 7 cm (the texture's own cracks make it craggy), coat 0.5 -> 0.3. The hills moved to 320 m, which the 300 m clip end cut off: engine change (camera.clip_end_m). Haze kept under 22 m so the sky above shows. The yellow-green from white balance 7500 K, tint -18 (tint < 0 is green, checked). |
| 2 | c2 (sun gap absent, WB 7500/-18) | 5.0 | rain reads as CG pins (thinner, per-streak opacity, tapered, none ending on the rock, a fine far curtain, a few defocused near drops); flat beige sky, no break (darker olive haze, a break behind the horn); speaker flat-lit (less bounce, more sun); still puddles (4x rings, 1,500 crowns); seam band; a stray bright bar at the right horizon; tar-like rock (film roughness varied 0.1 to 0.45); WB 6800 / -28 | All applied: the rain in three layers (160 near 1 to 3 m, 60,000 at 3 to 60 m, 150,000 at 15 to 120 m), opacity and an end fade per vertex; a pass cut in the ridge where the sun sets, nothing on the sun's line. Then main's fix to `assets.hdri_sun` (its azimuth was 180 deg off): every proof so far had the sun lamp, and the sky's sun, in FRONT of the speaker, which is why it read front-lit and flat. Sky turned 68 -> 248 deg so the sun really is behind it (azimuth 165). Pass 3's first render (on the old sun) was dropped. |
| 3 | c3 (sun back-right, haze split and thinned, a card into the throat) | 5.5 | hills read as olive grassy slopes (far haze 0.005 -> 0.0028, #A8AA90); seams between hills, far field and near ground (the near rock carried out, film 0.18, 40 blocks on the line); cabinet flat, no glow (sun 30 -> 20 deg right of the axis, 8.0, reflector 1.4); clay-like near rock (tile 0.8 m, bump 3, film 0.05 to 0.35); far specks; edge streaks like strings (main layer from 5 m, 5 to 11 cm); tint -26, sun #E8DC7A | All applied. Before this pass: the low sun was being put out by 500 m of haze on its path (split the haze into a near box and a far box off the sun's path, both thinner: `haze_box` in kit_ext); backlit rain against a bright sky vanishes, so the sun went out of frame right with the dark deck behind the speaker. |
| 4 | c4 (sun 20 deg right of axis, rock retextured) | 5.0 | hills read as front-lit green grass (ridge darker, haze #6E7058); stepped haze bands (one continuous haze); pale cream sky (strength down, WB 6200 / -18); rain an even overlay (more, varied, a veil, near drops); puddle rings unread (more crowns, rings x1.5); speaker unlit by the sun (11, reflector 0.9); a dark mound under it (stand it in water); soft edges (f/4.5, sharpen 0.35) | Four passes, 5.0 to 5.5: the far world kept failing (hills, haze slabs). Simplified rather than tuned: the hills and the far haze box removed, one thin haze (0.0012 /m), the black field carried flat to the horizon (900 x 700 m) so the storm's bright band is the horizon itself; the speaker stands 2 cm deep in water in a hollow (instance z -0.09); the rest of the changes as prescribed. |
| 5 | c5 (no hills, one haze, the plain to the horizon, in water) | 5.5 | rain still pins (45,000, 8 to 16 cm, opacity 0.04 to 0.25, lean jittered 3 deg, clear 0.5 m); featureless plain and a ruler horizon (4 boulders at 12 to 30 m, a low ridge 3.5 m across the left horizon); puddle darker than its sky (big rings halved, roughness 0.01); no glints (film 0.03 to 0.15, far 0.08); no aerial perspective (haze 0.0018 to 900 m, 20 m up; sun raised to 14 so it still arrives); horizon tangent to the cabinet top (camera 0.85 -> 0.55 m); glitter splashes (900, 3 to 14 mm, 0.2); flat front (reflector 0.7 at 60 deg left, fill off, a rim card behind right) | All applied (the critic asked for haze 0.003 to 1,500 m; that would put the low sun out again, so a compromise). |
| 6 | c6 (camera 0.55 m, boulders and a low ridge, haze 0.0006, sky 0.2) | 6.0 | cabinet a dark block (reflector 0.7 -> 2.2 at 40 deg left); no light through the acrylic (rim card 0.6 -> 2.0, at mid-height); beige-pink sky (haze 0.001 #BFC85A, tint -24); far-field seam (film 0.08 -> 0.18); rain pins on the ground (clear 0.6 m, half the drops below 1.5 m, lean 6 deg); glitter splashes (450, 0.12); no wet contact (4 cm deep); green ridge (darker) | Before the pass: the haze, lit by the low sun, was what made every sky flat and bright; at 0.0006 the photographed storm shows and the rain reads against it. Then all applied, the haze only partly (the critic's 0.0018 is the flat sky again). |
| 7 | c7 (reflector 2.2, rim card 2.0, 4 cm deep, quieter rain) | 5.5 | cabinet lit flat, both faces equal (reflector to 70 deg left at 1.2, rim card 3.0); a hard mirror copy (rings full strength, roughness 0.02, 1,200 splashes near the speaker); ground grey clay (darker, #121210, film 0.6 at 0.03 to 0.1); yellow clipped, blue at 0 (WB 5700 / -12, green from the haze #B5C24A); rain missing over the ground (100,000, opacity 0.12 to 0.5, clear 0.3, 70 % kept below 1 m); a bright green ridge (darker, haze 0.0014); denoise smear (finals at full size and samples) | Applied. The critics now pull against each other (pass 6: fewer streaks over the ground and a stronger reflector; pass 7: more streaks over the ground and a weaker one), so these are middle settings. Pass 6's rig (6.0, the best) is commit a06d754. |
| 8 | c8 (darker rock, more rain, splashes at the speaker) | 6.0 | cabinet underexposed mustard-brown (reflector 1.2 -> 4.0 at 40 deg left, mid-height); a pale sky (strength 0.2 -> 0.13); no rim (card 3 -> 9, 20 deg further behind); splashes a field of identical beads (700 near + 900 at 3 to 10 m, 2 to 20 mm, fainter); blue crushed (Base Contrast, tint -6, contrast 0.15); a lime ridge (haze 0.0018 #A9AE84); glints compete (film 0.06 to 0.16, coat 0.45); a black woofer (a second low card) | Applied. Scores since the simplification: 5.5, 6.0, 5.5, 6.0, a plateau. One more pass; then the finals from the best rig. |
| 9 | c9 (reflector 4.0, rim card 9.0 on the speaker alone, sky 0.13, Base Contrast) | 6.0 | beige, not acid (haze greener, HDRI tinted); no rim on the sun side (card 22); the sun closer to frame; sea-like chop (bigger pillows, boulders nearer); glassy crowns (fewer, smaller); a seam under the horizon; sticks over the far field; soft, greyed (contrast, sharpen) | Not applied: stopped here (below). |

## Stopping

Blind scores by pass: 5.0, 5.0, 5.5, 5.0, 5.5, 6.0, 5.5, 6.0, 6.0. Under the coordinator's rule for round 31b (stop
after a concept change when the passes stop gaining half a point) the set has plateaued at 6.0 since pass 6: three of
the last four passes score 6.0 and the critics' prescriptions now pull against each other from pass to pass (the
reflector up, then down, then up; rain over the ground fewer, then more). Finals render from the best rig, chosen by a
blind duel between pass 6 and pass 9 (both 6.0).

Duel (blind, critic/ab/PROMPT-DUEL.txt): pass 9 beat pass 6, 6.0 to 5.0 (`critic-acid_b/duel-p6-p9.json`). Its one
point for pass 6: there the speaker stands; in pass 9 the water line cuts its base and it looks sunk. So the finals are
pass 9's rig with pass 6's standing depth (the hollow 16 cm deep, the speaker at z -0.09, about 2 cm in the water).

## Finals

- `renders/2026-10-18/barkhorn/element31/acid_b.png` (2400 x 1600, 512 samples, denoised): 98 min render + 3 min build
  on the container's CPU. 3.7 MB.
- `acid_b-portrait.png` (1600 x 2000, the same set re-framed: 85 mm from 6 m, the same height and light).

The blind critic on the landscape final: **6.5** ("a strong idea that reads at once ... the mood and the reflection
work, but it still reads as CG"), `critic-acid_b/pass-final.json`.

## What holds it back (honest note)

- The speaker is lit by reflector cards more than by the storm: every critic wanted either more front fill (to see
  the gold) or less (to agree with a sun behind it). With the sun 2.6 deg up behind, the acrylic only glows at its
  edges; the front needs cards, and the cards read as a studio.
- The near lava reads as soft, rounded dough at full size: the forms are noise displacement on a photographed rock
  texture; real basalt's fractured edges and vesicles would need scanned ground or modelled clinker.
- Backlit rain is invisible against a bright sky and reads as pins against dark ground; the streaks are spindles with a
  translucent term, not refracting drops, so they never sparkle toward the sun the way real ones do.
- The splash crowns read as bright glassy cups at 2400 px (they are 2 to 20 mm, a few px at 9 m; the transmission
  of a thin crown wall makes them bright).
- The bright horizon band is the photographed sky's own low break (Poly Haven's `belfast_sunset_puresky`); no CC0 sky
  had a dark storm deck with a low sun, so the deck is that sky dimmed (strength 0.13), not a storm.

Re-graded on the coordinator's note (the judges of the A/B duel read the grade as olive, the acrylic as mustard):
`acid_b_grade.py` takes the raw frame through a linear white-balance shift (green x 0.95, blue x 1.06) and then the
same finish. The horn's hue was already on Acid's #E9B320 (its (g-b)/(r-b) 0.744 against 0.731; the mustard is its
lightness, not its hue), so the shift neutralises the sky without moving the horn green. A blind duel preferred the
re-graded frame, 6.2 to 5.9 (`critic-acid_b/duel-refinish.json`); the finals carry it. `acid_b.raw.png` stays the frame
as rendered.
