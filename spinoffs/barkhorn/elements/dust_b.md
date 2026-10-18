# Dust B, in its element (round 31b, the owner's second note)

The set is `dust_b.py`, with its own pieces in `studio/engine/kit_ext/dust_b_el.py` (built on `dust_el.py`); the frames
are `studio/shots/barkhorn/element31/dust_b.json` and `dust_b-portrait.json`.

## The owner, verbatim (2026-10-18, 17:30)

"For Dust, the plateaus in the back don't look like what you'd find on route 66 or whatever. Might also need some cacti
and blue skies."

## The place: Monument Valley, done right

Of the coordinator's three choices I took (a), Monument Valley:
- its flat-topped buttes are what "route 66 or whatever" calls up for most people;
- its cacti are real (prickly pear), and they grow there with yucca and sagebrush;
- saguaros do not grow there, so there are none.

The pieces:
- **Sky:** Poly Haven `kloofendal_48d_partly_cloudy_puresky` at 8k, deep blue with fair-weather cumulus. The sun lamp
  matches its sun: 48 degrees up, from the speaker's right. The postcard's crisp afternoon light, not the hazy orange the
  owner turned down.
- **Buttes at true size and distance:** the engine's camera now sees past 300 m (clip_end 12 km). The two Mittens stand
  about 300 m tall at 3 and 3.6 km, with long mesas beyond. Each (`butte`) is a sheer cliff of red sandstone, jointed and
  fluted, under a clean flat caprock, on its own paler, gullied talus apron, with the Mittens' thumbs standing off.
  Distance does what the first round's tenth-scale models could not: the haze and the lens treat them as far.
- **Ground:** red sand with stony patches blended in (`ground_mix`), and wind ripples only in patches.
- **Plants:** all procedural, since Poly Haven and ambientCG have no cacti or yucca scans.
  - `prickly_pear`: obovate pads set edge on edge, with areoles in a quincunx and 1 to 4 straw spines each.
  - `yucca`: a rosette of stiff blue-green blades over a skirt of dry leaves.
  - `sagebrush`: woody stems in a crown of fine silvery leaves.
  - The tumbleweed from round one, fetched up against a sagebrush.

## Proofs before the critic

- **a01:** the place read at once. But a hard vertical line crossed the sky (the haze box reached past the clip
  distance), the buttes were striped tin cans (`cliff_side` tiles in rows), the prickly pear grew as a column, the
  sagebrush was sparse, and the left Mitten was cut by the frame.
- **a02 to a04:** cliffs in `rock_face` with deep, sharp joints; red, gullied talus; a lower, smaller haze box; a
  sprawling prickly pear; dense sagebrush. The Mittens' thumbs had been built off frame (each butte is about 400 m wide
  at 3 km), so they moved in. A test with the sun behind the speaker's right (a03b) left the buttes flat grey: kept the
  sun at the right.
- **a05, a06:** the speaker turned 20 degrees toward the sun with the camera at -12, so its acrylic reads bright orange.
  The rock's base colour brightened (x1.9; a COLOR tint keeps a dark texture's darkness), so the buttes read red.

## Critic passes

| Pass | Image | Score | Top changes | What I did |
|---|---|---|---|---|
