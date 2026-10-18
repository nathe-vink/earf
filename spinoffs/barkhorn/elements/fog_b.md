# Fog, concept B: San Francisco's fog (round 31b)

`fog_b.py` (the shot), `studio/engine/kit_ext/fog_b_el.py` (the land, the fog volume, the gulls). Built with
`python3 spinoffs/barkhorn/elements/build.py fog_b`.

## The set

- **Place.** A Marin headland at dawn. The speaker stands in the headland's grass at its brow, which falls steeply
  about 2 m behind it. Below and beyond: a sea of fog with billowing tops, banked up toward the headland. Across the
  water, hills 0.9 to 2.6 km off. Behind them the marine layer stands about 44 m higher and pours over the ridges and
  through a saddle toward us, which is San Francisco's signature. Wisps rise up the cliff behind the brow.
- **Assets (all CC0).**
  - Sky: Poly Haven `syferfontein_6d_clear_puresky` (a clear dawn, the sun 5.8 degrees up).
  - Ground: `sparse_grass`.
  - Grass tufts: `grass_medium_01`/`02`.
  - The land, the hills and the fog are procedural (`fog_b_el.py`). The hills are gaussian ridges cut by ridged
    noise into gullies. The fog is one volume whose density is drawn by noise: a sea with billows, banked toward the
    headland, rising behind the hills, poured over them.
- **Light.** One sun, low, behind and to the left (out of frame). The lamp is matched to the sky's sun with
  `sun_from_sky`.
- **Camera.** 85 mm from 9.5 m, 1.15 m up, level. The long lens compresses the fog and the hills behind the speaker.
  The clear horn stands against the dark ridge, the cabinet against the grass and the fog band.

## Engine changes (each in its own commit)

- `render.py`: a shot's camera may set `clip_end_m`. The default stays 300 m, as before. The hills are 1 to 3 km off.
- `assets.py`, `hdri_sun`: the returned direction was 180 degrees off the sky's sun. Blender's equirect lookup is
  u = 0.5 - atan2(y, x)/2pi, and the code had the direction negated.
  - Proven by aiming a camera along the result: before the fix it saw sky at 1/400 of the sun's brightness; after
    it, the sun's disc.
  - So every `sun_from_sky` lamp faced the sky's own sun. The coordinator was told at once, since all eight sets use
    it.

## Concept proofs (0.3 scale, 32 samples)

- p1 to p6, the layout:
  - 50 mm from 5.5 m with the brow 11 m back: the brow hid the whole fog sea. The fog can only be seen from eye
    level if the ground falls away just behind the speaker, so the brow moved to 2 m.
  - A debug view from 80 m up showed the fog volume working (billows, a ridge as an island).
- **Proof A** (sun 6 degrees right of centre, behind: a backlit frame) against **proof B** (the sun 62 degrees left,
  side light). Chose **B's direction, three-quarter back light (the sun 35 degrees left of the view)**:
  - Backlight flattened the hills and the fog sea into a milky haze, and the speaker's front went to grey.
  - Side and three-quarter light gives the hills relief and the pouring fog a lit top and a shadowed underside.
  - It keeps the clear horn against a darker ridge, and it still reads as dawn.
- p7, p8: a higher marine layer behind the ridges and pours over them gave the San Francisco look at once (fog
  draping over the ridge line). Then gullies on the hills, darker scrub, less haze, and wisps up the cliff.

## Critic passes (critic/PROMPT-promo.md; fresh blind critic each pass, proofs at 0.5 scale, 128 samples)

| Pass | Score | Top changes | What I did |
|---|---|---|---|
