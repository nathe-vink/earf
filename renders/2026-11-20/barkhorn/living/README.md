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
