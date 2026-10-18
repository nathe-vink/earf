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
