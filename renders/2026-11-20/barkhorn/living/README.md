# The living room by day (2026-11-20)

The coordinator, 20 Nov: a living room by day for Tropos, Mantle and Core. **Step 1, the proof:** camera A in Ember,
small and fast, for the room and the composition. Nothing further is rendered before the coordinator's word.

`living-a-proof-ember.png`: 1500 x 1000, 48 samples. Rendered by `spinoffs/barkhorn/campaign/living_room.py`:

    TROPOS_BASE=A LAMPS_ROOT=/home/user/lamps-mix MANTLE_ASSET_SHA=b64c6bd37b8ff5eb8007d2d04ee7c0859962dd3b \
        python3 spinoffs/barkhorn/campaign/living_room.py OUTDIR ember

## Built from three photographs (looked at 20 Nov, public pages)

- **Klipsch, the Klipschorn AK7 hero:**
  - the pair against the wall, a low console between them with the turntable on it, records below;
  - the seat's back across the foot of the frame, a plant at the side.
- **KEF, the Blade Two lifestyle frame:**
  - daylight from a side window raking across a plain wall and a pale floor;
  - a chair cut by the frame, little else.
- **Design Within Reach, the Panthella 160:**
  - a small lamp on wood;
  - the window's sun throwing a hard shadow on a limewash wall.

(Also looked at: the Klipsch La Scala heroes, Avantgarde's Opus 1, U-Turn's Orbit and HAY's living rooms. HAY's Mimi room,
with a low shelf of books and a rug, backs the same choices.)

## The room

- **Shell:** 5.4 x 6.0 m, a 2.75 m ceiling, plaster walls, oak planks (Poly Haven), one wool rug.
- **Console:** walnut, 1.5 x 0.45 x 0.64 m.
- **Chair:** a mid-century lounge chair (scanned, CC0), its back across the foot of the frame.
- **The rest:** a plant (scanned), books on the console, sleeves leaning at its end, one quiet print.
- **The pair:**
  - Tropos, the approved look (base A, horn A polished), in Ember;
  - 2.5 m apart, 0.3 m off the back wall, toed in 6 degrees.
- **On the console:**
  - Mantle in Ember (the Mantle lane's asset at b64c6bd3, its newest, until the lane names its file), a record on;
  - a Core in Ember at the console's right end, switched off.
- **Cables, in frame:**
  - each Tropos's mains lead along the skirting to a socket beside it;
  - Mantle's signal leads down the console's ends to each speaker's back.

## Light

- **The only source:** the sky and its own sun (Poly Haven `garden_nook`, an unclipped sun at 16,000 times the sky's
  median).
- **Its way in:** the room's three windows:
  - the back wall's left corner (in frame);
  - the left wall (out of frame), the sun's way in;
  - the wall behind the lens (out of frame).
- **What the sun does:** it comes from the front left, at 25.9 degrees. It falls across the left speaker's front, and
  through its red acrylic onto the floor.
- **No lamp, card or fill.** The emitter list is `living-a-proof-ember.emitters.json`.
- **Audit:** hidden 0, equipment 0, both from the mask pass and from `reaudit.py`. The window in frame has no portal,
  removed by the set piece `no_portal`: a portal is a lamp object, though it adds no light.

## Proof 2 (`living-a-proof2-ember.png`, the coordinator's seven points, 20 Nov 11:58)

Same size and speed (1500 x 1000, 48 samples). Proof 1 is kept beside it. L* is measured by `living/lstar.py` (CIELAB,
D65), on the same boxes for both speakers.

1. **One colour twice.**

   | | proof 1 | proof 2 |
   |---|---|---|
   | cabinet, left / right | 44.6 / 17.0 | 39.9 / 40.7 |
   | horn, left / right | 49.8 / 28.2 | 40.4 / 30.2 |

   - The sun now comes from straight left (azimuth -90), parallel to the fronts.
   - A run of windows behind the lens gives both fronts the same sky.
   - The window in frame moved 0.3 m left: the garden had shown through the left horn and cabinet.
2. **No sun on a cone.** The cones read 25 and 30, both black.
   - The sun enters by a narrow window at the left wall's back corner.
   - It grazes the backs of the cabinets' sides, and their red light falls on the floor and the console's end.
   - It lies in stripes on the floor before the pair, and crosses the console's top.
3. **By day.** The lit wall reads 73 to 77, and 0.5 % of pixels are clipped (the sun's patches). Exposure is 5.35,
   and there is a fourth window, on the right wall, out of frame.
4. **The console.** A walnut credenza, 1500 x 450 x 640, built as a maker would:
   - a case with the top's grain along it;
   - a door, three drawers and a door, 4 mm reveals onto a dark inside;
   - blackened bar pulls;
   - a base rail and four tapered legs.

   Its wood is Poly Haven `walnut_veneer_02`. `american_walnut_veneer` averages #726E69, a grey: proof 1's pale box.
5. **Mantle and the Core in daylight.**
   - Mantle is turned 30 degrees toward the window, in the sun's band on the console: its Ember plinth's lit face shows.
   - The Core is at the console's front edge, in the band. Switched off, its Ember ball reads as dark red glass, as in
     the lamps lane's own unlit day proof (`renders/2026-11-01/barkhorn/tint-proof/core-ember-unlit.png` on
     r32-lamps-final). The pale core inside shows only when it is on.
6. **The window.** A steel casement: a dark frame, its bars set 6 mm behind the frame's faces. The engine's own bars
   share the frame's faces, and coplanar faces render black in Cycles: proof 1's notches.
7. **The rug.** Herringbone wool (Poly Haven, photographed) in a field, inside an 80 mm border band much darker,
   16 mm thick, its edge rounded.

Emitters: the sky and its sun, through four windows (`living-a-proof2-ember.emitters.json`). Audit: hidden 0,
equipment 0, from the masks and from `reaudit.py`.

## The Ember finals (2026-11-20)

| frame | size | samples | minutes | audit |
|---|---|---|---|---|
| `living-a-ember.png` | 2400 x 1600 | 256; the two cabinets 1024 | 28 + 31 (two bands); 26 + 24 (the boxes) | hidden 0, equipment 0 |
| `living-b-ember.png` (held: Mantle's arm and label, the Mantle lane) | 1600 x 2000 | 256 | 39 | hidden 0, equipment 0 |
| `living-c-ember.png` | 1600 x 2000 | 256 | 26 | hidden 0, equipment 0 |

- **A, the bands:** two bands (`--crop`, rows 0 to 52 % and 48 to 100 %), joined by `living/bands.py` over 64 rows. The
  bands differ there by 0.60/255 on average.
- **A, the cabinets:** at full size the insides were soft (the coordinator, 15:45), so each cabinet's box
  (x 420 to 799 and 1650 to 2029, y 640 to 1319) was rendered again at 1024 samples, from the same shot file. Each box
  was joined in by `living/region.py` over a 16 px feather:
  - over the feather the two renders differ by 1.69 and 2.00/255 on average (p99 10 and 11);
  - the boxes sit at offset (0, 0), found by edge correlation;
  - nothing else in the frame changed;
  - the 256-sample frame is kept as `living-a-ember-256.png`.
- **Depth of colour:** the coordinator's measure of A (pixels over chroma 40) reads the cabinets at chroma 51.9 and
  54.7, and the studio's front at 59.7.
  - Narrowing the run of windows behind the lens (2.0 m, then 1.2 m) made the fronts darker and no deeper (chroma
    42/37, then 36/33), so proof 2's run was kept.
  - Correction (21 Nov): an earlier line here said the studio's depth comes from its `through` lamp. That lamp is at 0 in
    all eight tallr7 shots. The lamps on there are the key, fill, kick, horn, `wall_left` and the three background
    lamps. The room's light through the cabinets is the sun.
- **C:** the Core switched off, on the side table by the window, off its dock (no dock, no cable), beside a book and a
  glass.
  - The narrow left window is in this frame. It has no portal, and its bars are set pieces set back from the frame
    (the engine's own bars share the frame's faces and render black where they meet).
  - A and B were rendered with that window's own engine bars, 30 mm; C's are 22 mm, in the same places. Their sun
    shadows in A and B differ only by that width.

## The Ember finals again: one light model (2026-11-20, evening)

C (`living-c-ember.png`) and A (`living-a-ember.png`) were rendered again. The first finals are kept as
`living-c-ember-v1.png` and `living-a-ember-v1.png`.

- **One light model:** refractive and reflective caustics on. The acrylics' glass-shadow shortcut (a shadow ray switched
  to a transparent surface) is cut in all 22 materials that carry it, by the set piece `no_glass_shadows`. With both on,
  the light through the acrylic was counted twice (about +7 L*).
- **Toe-in 15.5 degrees,** aimed at the seat: at 6 degrees the cabinets' inner sides mirrored the window white.
- **The credenza is 1.8 m,** and the sofa's back crosses the foot of A in place of the lounge chair.
- **Mantle** is the Mantle lane's asset at 66ccac7890 (its polished deck), with plain dark sleeves leaning behind it.
- **C:** the Core is out of the sun, the window behind it. Switched off, its ball reads L* 39.3, C* 60.5, hue 39
  (median); 92 % of it is over chroma 40. The book shows its cream page block.
- **A:** two bands joined by `living/bands.py` over 64 rows (mean difference 0.67/255); 256 samples; 33 + 32 minutes.
  The masks were made afterwards with `--masks-only` from the same shot file.

Measured on A by `living/lstar.py` (CIELAB, D65), boxes in pixels of the 2400 x 1600 frame:

| | L* | C* |
|---|---|---|
| cabinet above the woofer, left / right (y 880 to 930) | 32.1 / 29.8 | 64.2 / 62.9 |
| cabinet below the woofer, left / right (y 1180 to 1220) | 32.1 / 28.6 | 46.7 / 44.1 |
| horn, left / right (its outer edge) | 49.4 / 35.0 | 72.1 / 69.2 |
| the Core, off | 35.5 | 48.0 |
| Mantle's deck top, left / right of the platter | 36.2 / 54.3 | 15.3 / 7.6 |
| Mantle's deck front edge | 26.3 | 6.0 |
| the wall behind | 75.3 | 9.6 |

- **The deck does not read as Ember.** Polished, it mirrors what stands behind and above it: the dark sleeves and the
  pale wall. Red shows only at its far left; the rest reads near black or grey (chroma 6 to 15, against the cabinets'
  44 to 64).
- **Emitters:** the sky and its sun only, through the windows. No lamp, card or fill. The Core's lamp is removed
  (`cores_off`), and the window in frame has no portal (`no_portal`).
- **Audit:** hidden 0, equipment 0 on A and C, from the masks and from `reaudit.py`.

## Sources of the room's scanned and photographed pieces

All from Poly Haven (polyhaven.com), CC0: public domain, free for commercial use, no attribution required. They are
credited here all the same. They are fetched and cached by `studio/engine/assets.py` and are not kept in git.

| piece | Poly Haven id | by |
|---|---|---|
| the sofa (its back across the foot of A) | `sofa_02` | Kirill Sannikov |
| the side table | `side_table_01` | James Ray Cock |
| the plant | `potted_plant_02` | Rico Cilliers |
| the lounge chair (proofs 1 and 2 and the first finals only) | `mid_century_lounge_chair` | Kuutti Siitonen |
| the sky and garden through the windows | `garden_nook` (HDRI) | Dimitrios Savva, Jarod Guest |
| the oak floor | `oak_wood_planks` | Dimitrios Savva |
| the credenza's walnut | `walnut_veneer_02` | Jenelle van Heerden |
| the rug | `poly_wool_herringbone` | colormass, Rico Cilliers |

The record covers are this repository's own (`spinoffs/barkhorn/campaign/bar_life/tex`, invented covers).

## C again: the Core's base with its liner in contact (2026-11-21)

The owner saw the Core's base as "smoke frosted" at its edges: red in the middle, a gray-brown band down each side. The
cause was in the lamps lane's `lamp_site.py`: a 0.4 mm air gap between the satin skin's smooth inner face and the white
liner, where the CAD has them in contact. Light leaving the base at grazing angles was lost in that gap.

C was rendered again from its own shot file, unchanged. The only differences are the lamps lane's code at 7e08871d9
(`LAMPS_ROOT`) and `BASE_CONTACT=1`. That commit also brings the lane's other new defaults for the Core: the skin's foot
lifted 0.2 mm off the table, and its turned surfaces in 768 segments. The previous C is kept as `living-c-ember-v2.png`.

- 1600 x 2000, 256 samples, 35 minutes. Audit: hidden 0, equipment 0.
- Outside the Core's box (x 500 to 950, y 1150 to 1450) the frame is unchanged: the mean difference is 0.02/255.
- `c-base-v2-v3.png`: the base before (left) and after (right), at 1.5x.

**The base** (`base_readings.py`, L* / C* / hue, 60 rows at y 1320 to 1380):

| | left flank (x 565-600) | centre (x 690-750) | right flank (x 840-875) |
|---|---|---|---|
| before (v2) | 26.8 / 31.0 / 37 | 38.8 / 54.6 / 36 | 39.5 / 20.9 / 12 |
| after | 37.5 / 53.2 / 36 | 41.0 / 55.5 / 35 | 45.4 / 33.9 / 22 |

The left flank now matches the centre's colour. The right flank is still paler: its box takes in the table's warm
highlight through the satin edge, which lowers the hue.

## C, the fourth: the base fixed, the water in contact, filter_glossy 0 (2026-11-21)

C was rendered again from its own shot file with only the audit's fixes:
- **The Core:** at the lamps lane's ecb1650c24, pinned in the shot (`cores_off` checks LAMPS_ROOT against it) and
  written into `living-c-ember.report.json` under `lamps`. That commit's skin is 6 mm along its normals with the lip
  closed, both passes tinted, and the liner in contact.
- **The water:** the set piece `water_glass`. Glass to air at 1.5, glass to water at 1.5/1.33 with no air film, water
  to air at 1.33, a 1.5 mm meniscus. It stands at 78 mm, as in A.
- **`filter_glossy` 0.**

The previous C is kept as `living-c-ember-v3.png`, and the crops are in `c-crops-r3/`.

- 1600 x 2000, 256 samples, 37 minutes. Audit: hidden 0, equipment 0.

**The ball and base against the lamps lane's studio Core OFF** (r32-lamps-final 35d059fec,
`house7/core-ember-off.png`; `c_ball_vs_studio.py`, medians of L* / C* / hue):

| | ball, whole disc | ball, lower middle | base centre | base flanks, left / right |
|---|---|---|---|---|
| room C | 47.6 / 65.0 / 38 | 43.4 / 76.8 / 41 | 37.2 / 49.2 / 35 | 32.0 / 44.5 / 38 and 42.0 / 25.0 / 16 |
| studio | 39.5 / 64.2 / 35 | 41.0 / 65.7 / 34 | 34.0 / 64.3 / 36 | 34.9 / 37.2 / 30 and 29.0 / 40.4 / 32 |

- **The ball:** the same chroma and nearly the same hue in both. The room's ball is lighter: the window behind it
  fills its disc with daylight reflections. In the lower middle, away from most reflections, the two are within 2.4 L*.
- **The base:**
  - Its centre is within 3.2 L* and 1 degree of hue of the studio's.
  - Its chroma is lower in the room (49 against 64): the room's light is soft daylight from behind, the studio's a key
    from the front.
  - The room's right flank box takes in the table's warm highlight.
- **The two transforms differ:** the room renders through AgX (Base Contrast), the studio through its own view, so
  C* is not strictly comparable. That is the audit's L4.
