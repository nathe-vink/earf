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
