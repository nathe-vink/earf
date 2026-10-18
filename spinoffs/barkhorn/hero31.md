# hero31: the home page's hero, remade for the campaign

The eight Clouds on a gentle arc in spectrum order, covers off, on pale paper, lit from behind and low so each tinted
cabinet throws its own colour onto the floor in front of it. Built by `hero31.py` (one table of settings, `P`) into
`studio/shots/barkhorn/hero31/`; the template it replaces (`site30/hero.json`, 5.5 with the blind promotional critic,
`critic/rounds/2026-10-18/promo-hero-r1.json`) is kept as it was.

## The set (as the final stands)

- **The eight** in spectrum order on a gentle arc (middle 0.5 m back), in two staggered ranks: Ember, Acid, Ice and
  Fog in front, Dust, Poison, Haze and Smoke 0.7 m behind in the gaps, centres 0.72 m apart across, so each throw runs
  in its own lane. Each faces the lens, then sits a few degrees off true, as if set down by hand. Covers off.
- **The key** is a sun from straight behind, 24 degrees up, 1.5 degrees across, 5200 K. The paper casts no shadow
  (`set.cast_shadow`), so the sun reaches the floor over the wall and its shadows run parallel. The engine's resin
  passes shadow rays tinted, so each horn lays a saturated pool of its colour, and the cabinet's clear parts a paler
  one. The batts are opaque, so the rest of each throw is shadow.
- **The set**: pale paper (#EEECE7, a fine tooth and a faint mottle) on a sweep 34 m wide, its wall 12 m back. A
  30 x 5 m softbox faces the wall (the cyc), with silks over the floor behind the line (top) and in front of it (over).
  A small photographed studio (Poly Haven `studio_small_03`, CC0, already in `studio/assets/hdri`) shows only in the
  acrylic's reflections and lends a little ambient.
- **The speakers' own light**, linked to their parts: a low softbox from the camera for the faces and linings (no
  reflection); tall strips either side for the acrylic's edges; a narrow high strip the top edges mirror; a strip for
  the cones and the horn drivers; and an edge light on the smoked unit alone.
- **The camera**: 70 mm at f/4 from 13.5 m, 2.2 m up, looking level (verticals true), focused on the front rank.
- **The finish**: PBR Neutral, 5000 K, tint 6; white point 228 -> 230 with a shoulder to 246; contrast 0.18, clarity
  0.10, sharpening 0.45, vibrance 0.4.
- **Kept as options** in `hero31.py`, from the passes: `cutters` (the key reaching the floor only through the acrylic,
  h6), an area key in place of the sun (`sun: 0`), a straight diagonal line (`diag`, tried for the phone frame).

## Engine changes (each in its own commit, each off by default)

- `materials.py`: the sweep's paper takes `tooth` / `tooth_mm` and `mottle` / `mottle_m`.
- `render.py`: `render.transmission_bounces`, `glossy_bounces`, `transparent_bounces`, `caustics_refractive` and
  `caustics_reflective` (main later made the first two settable too; the merge keeps one copy).
- `sets.py`: `set.cast_shadow: false` on a sweep.
- `lights.py`: a flag can be `see_through` (only its lamps' shadow rays meet it).

## What the critics kept naming that is the product's

- The batts are opaque, so most of each throw is grey shadow; only the horns and the cabinets' clear parts throw
  colour (every pass from h2).
- The horn throats read as black blobs: the compression driver seen through the thick tinted throat. Light linked to
  the drivers at 70 W/m2 does not open them (h3 to h8).
- The acrylic's edges seen edge-on render near-black. At 32 transmission bounces they look the same as at 8 (crops in
  this round). It is the long path through the tinted sheet, as in real tinted acrylic, not a bounce cutoff.
- The smoked unit's tint swallows its interior unless a light is aimed at it alone.

## Passes

| pass | frame | blind score | verdict | top changes | what I did |
|---|---|---|---|---|---|
| r1 | finals31/hero.png (site30) | 5.5 | iterate | small hard key behind with caustics; front fill linked to the speakers; strip for the cones; pale even sweep; gentler arc with margins; paper tooth | the set rebuilt as hero31 (below) |
| h2 | proofs/p2.png | 6.5 | iterate | key 0.25 -> 0.8 m and moved far back (no fanning, soft penumbra); fill 2 -> 3.5; sky 0.7 -> 0.4, key 4.4 -> 5.5, exposure -2.2; face 5 -> 8; cyc 10 -> 14 (cove band); camera nearer the title; paper tooth 0.3 at 1.2 mm | all taken; the key's new place needs a deeper set (wall 17 m back); a 58 mm lens would have cut the margins, so the line is tightened (pitch 0.80) and moved up by shift instead, with a 53 mm lens |
| h3 | proofs/p3.png | 5.5 | iterate | eye at 1.35 m on a 70 mm lens from 15 m; arc 0.9 m deep, turned 12 deg in; key a 1.2 m disc 30 m back (parallel shadows); over 2 -> 4.5; light the horn drivers; cyc 13, top 11; side strips on the cabinets, face 4; white out 234, shoulder 246, coarser tooth | a different critic, and a point lower: it wants stature and visible acrylic edges where h2 wanted square baffles. Taken: 70 mm from 15 m, the arc and the turn, the drivers on the strip, the side strips, cyc/top, the finish and tooth. The distant key became a sun behind the wall (engine: `set.cast_shadow`), parallel shadows without a 30 m set. Not taken as written: an eye at 1.35 m flattened the throws to slivers (tried, t16), so 2.6 m; over 4.5 washed the pools (both critics' shadow and pool tests cannot pass together: a pool is lit by the same ambient as its shadow, plus the key), so 2.0 |
| h4 | proofs/p4.png | 6.0 | iterate | white balance (magenta cast, dE 5.8); sun 22 -> 30 deg; over 2 -> 4.5; strip 45 W/m2 lower, for the throats; right side strip 10, face 5; arc 2 m deep, 18 deg; tooth 0.7 at 1.5 mm, mottle 0.08, 256 samples; contrast 0.14, clarity 0.10, sharpen 0.45 | taken, the arc only to 1.4 m and 15 deg (2 m makes the ends 15 % bigger than the middle, r1's complaint); every light at 5200 K, white balance 5150 K, tint 4 (wall dE 1.5); a vibrance of 0.15 to give back the pools' colour the lifted shadows take; 192 samples. The throats stay black under 45 W/m2 on the drivers: it is the horn's thick tinted throat, the product (r1 said as much) |
| h5 | proofs/p5.png | 6.0 | iterate | over 4.5 -> 1.5, sky 0.15, fill 2 (deeper shadows, deeper casts); sun 30 -> 18 deg; wall falling off upward; face 8, sides 10/12; finer tooth, less mottle; strip 70; vibrance 0.25, contrast 0.18 | three passes since h2 (5.5, 6.0, 6.0) without gaining on its 6.5: the approach changes (below). The critics pull the shadows both ways (h3 and h4: lift them to 140-165; h5: drop them to 105-130) because a colour pool sits in the same ambient as its grey shadow, plus the key; the grey slabs are the batts' shadows, the product's. New approach: **cutters** behind the row that only the sun meets, an opening for each speaker the shape of its cabinet and horn seen from the sun, so the key reaches the floor in front only through the acrylic. The grey slabs vanish into an evenly lit floor and the throws read as light. Taken from h5 as well: sun 20 deg, face 8, sides 10/12, tooth 0.5 at 0.6 mm, mottle 0.02, vibrance 0.3, contrast 0.18 |
| h6 | proofs/p6.png (cutters) | 6.0 | iterate | the cutter's floor edge reads as a table edge; throws pastel (key 34, over 6, exposure -2.95, vibrance 0.4); front floor at paper value; edge light on the smoked unit; an edge strip in reflections, sun 16 deg; arc 2.6 m deep; 75 mm from 13 m at 2.0 m; contact 0.6 | the new approach scored as the old (6.0, the same 7.6 if fixed). Light added to pale paper is either ghostly (the paper bright) or dingy (the paper dark), so the cutters go, kept as an option (`cutters`), and the coloured shadows return, where the horns' colour is saturated. Taken: the camera (75 mm, 13 m, 2.0 m), the smoked unit's own edge light, the edge strip, the heavier contact shadow, the side strip moved. And a second change of approach for what every critic names first, a flat line-up of identical copies: the eight in two staggered ranks on the arc (orange, green, violet and smoke 1.2 m back, in the gaps), so each is a third bigger in the frame and the throws interleave; each turned a few degrees off true; f/2.8 focused between the ranks |
| h7 | proofs/p7.png (ranks) | 6.0 | iterate | key 23, over 2, top 7 (deeper casts); face 3, edge 6, sides 14/20 (backlit glow, not face light); smoke 22 W/m2, wider; wall falling off upward (cyc 11 at 1.5 m); sun 29 deg (casts inside the frame); tooth 0.8 at 0.9 mm, mottle 0.04; 50 mm from 9.5 m at 1.7 m, f/2.0 on the front rank (the ranks read as depth); 640 samples | all taken (the camera at 8.8 m to keep 12 % margins; 256 samples in the proof, the finals at 640+). Three approaches have now scored 6.0 to 6.5, each critic's first word "render", so one more cue nobody had tried: the acrylic mirrored nothing. The sky is now a photographed small studio with softboxes (Poly Haven studio_small_03, CC0, already in studio/assets), at 0.15 so it shows in the reflections without tinting the paper blue (at 0.4 the floor read 230/238/249) |
| h8 | proofs/p8.png (studio reflections) | 6.0 | iterate | over 3 -> 6 (batt shadows to 135-160); face 5.5, strip 70; tooth 1.6 at 0.6 mm, mottle 0.08, roughness 0.9; smoke 45 W/m2 nearer; top 4, cyc centred 3 m up (no cove band); 5000 K, tint 6; back rank 0.7 m behind, centres 0.72 (a lane each); 70 mm from 12.5 m at 1.15 m, f/4 | taken but the camera height and the mottle: at 1.15 m the throws flatten to slivers and the lower third empties (tried, s9), and this critic's camera contradicts h7's (nearer and higher); so 70 mm, f/4 from 13.5 m at 2.2 m, the sun 24 deg so the throws reach into the lower third. Mottle 0.05 (h5 read 0.08 as blotches) |
| d1 (duel) | finals31/hero.png (1280 copy) vs proofs/p8.png | 6.5 vs 5.5 | template preferred | — | the judge preferred p8's coloured throws, its glassier horns and its smoked unit, and the template's crispness (a full-size frame scaled down, against a half-size proof the denoiser smeared), its calm backdrop and its even row. Every pass so far judged half-size proofs, and every critic named smear and "render": from here frames are judged as full-size renders scaled to the proof size |
| h9 (final v1) | hero31/hero.png v1 (full size, 512 samples, scaled to 1280) | 6.0 | iterate | the paper blue (236/237/247, dE 7.45) and the wall dull (211) with a cove band; key 32 W/m2, over 3 (deeper shadows, denser pools); sun 32 deg; tooth 3.0, mottle 0.12; 5500 K, tint 8; one rank, arc 1.4 m; smoke 80 W/m2, higher; cyc 21 at 2 m | the paper colour is a real flaw in a hero, so v2 is rendered: key 32, over 3, cyc 21 at 2 m, smoke 80 higher, tooth 2.2 at 0.9 mm, mottle 0.06, and the white balance tested to the swatch (5250 K, tint 3: floor dE 2.0, wall 1.0; the critic's 5500/8 read pink-warm at dE 5.2). The sun to 30 deg, not 32 (at 32 the lower third empties). The ranks stay: both duels below preferred this composition |
| d2 (duel) | final v1 vs finals31/hero.png, both 1280 | 5.5 vs 5.0 | **final preferred** | — | for: the cones' detail, the crisp coloured throws, clean horn throats, even row with margins; against: the template's warm graded backdrop, its side faces |
| d3 (duel) | final v1 vs proofs/p2.png (h2, 6.5) | 6.5 vs 6.0 | **final preferred** | — | for: sharpness, the product filling the frame, the smooth sweep, the clear unit reading as glass; against: p2's longer raking throws and glowing bodies |
| q1 (phone) | hero-portrait.png v1 (scaled to 800) | 6.0 | iterate | nearer 60 mm camera, centres 0.68 m (less overlap); cyc 24 at 3 m; face 9 raised over the front horns, smoke 75; warmer balance; sun 31; over 3.5 nearer; vibrance 0.55, contrast 0.22 | the light and colour taken. The camera and spacing cannot both hold: eight at 0.68 m need a frame far wider than 4:5 from 6.2 m, and fitting them (0.56 m from 9 m) left small speakers on empty paper (tried, q8). So the cluster stays as delivered, the content lifted a little, sun 26 so the throws fill the lower half |

## Finals
