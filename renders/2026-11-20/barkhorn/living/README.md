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
  - The studio's depth comes from its `through` lamp. The honest twin here is the sun through the cabinets.
- **C:** the Core switched off, on the side table by the window, off its dock (no dock, no cable), beside a book and a
  glass.
  - The narrow left window is in this frame. It has no portal, and its bars are set pieces set back from the frame
    (the engine's own bars share the frame's faces and render black where they meet).
  - A and B were rendered with that window's own engine bars, 30 mm; C's are 22 mm, in the same places. Their sun
    shadows in A and B differ only by that width.
