# Haze, concept B: layered hills at blue hour

"Dusk, kept indoors." Coastal hills recede range after range into violet haze, each paler than the last; a pale sun
sinks into the haze behind the far ridge (the icon: a sun behind three bars of haze). The speaker stands on the near
ridge in dry grass at eye level, the last light behind it, so its violet acrylic glows with the dusk instead of
standing out from it.

- Set: `haze_b.py` (shot and portrait), its pieces in `studio/engine/kit_ext/haze_b_el.py`.
- Build: `python3 spinoffs/barkhorn/elements/build.py haze_b`, then
  `python3 studio/engine/render.py studio/shots/barkhorn/element31/haze_b.json --out OUT.png [--scale S --samples N]`.

## How the set is made

- **Sky.** Poly Haven `qwantani_dusk_2_puresky` (CC0), a clear dusk after sunset, pink at the horizon and lavender
  above, turned 60 degrees so its afterglow sits behind the speaker.
- **Sun.** A sun lamp at azimuth 173, elevation 1.3 (just behind the speaker, a little to the camera's left), warm
  (#FFB48C), and a disk the camera sees (0.6 degrees) at the same place. Both reach the camera and the set through the
  haze, so the sun is pale and the light it throws is soft: one sun, one set of shadows, and the speaker's shadow runs
  toward the camera.
- **Ranges.** Six heightfield layers behind the ridge, their crests wandering along x with ravines down their faces,
  textured with Poly Haven `rocky_terrain_02` (aerial) and dotted with scanned shrubs and trees (`searsia_lucida`,
  `searsia_burchellii`, `island_tree_01`) on the nearest three: the chaparral texture of coastal California hills. The
  engine's camera clips at 300 m, so the ranges stand at a tenth of their true distance and size (25 to 255 m for
  250 m to 2.6 km): from one viewpoint perspective is the same at any scale, and at these distances an 85 mm lens
  focused at 10 m is at infinity either way. The haze's density is scaled with them.
- **Haze.** Two boxes of scattering volume over the ranges: a dense lower layer (to 6 m above the eye, 0.006/m) and a
  thin upper one (0.0006/m), lavender, scattering forward (anisotropy 0.45 and 0.75) so it glows round the sun.
- **Ridge.** A dense heightfield (2 cm) with Poly Haven `withered_grass` at its real size and true displacement,
  level under the speaker, falling away 5 m behind its crest.
- **Grass.** Dry grass as hair strands (Principled Hair, straw), tall in tufts round the frame, short round the speaker
  so its feet show; the low sun comes through the blades and rims them. The scanned grass models tried first
  (`grass_medium_01/02`, dried by a hue shift) read as dark weeds against the sky and were dropped.
- **Camera.** 85 mm at 10 m, eye 1.0 m, f/5.6, verticals level by lens shift, the speaker on the right third and
  turned 25 degrees to the camera (rotate_z 10, the camera at azimuth -15). The long lens stacks the ranges.
- **Finish.** AgX, Medium High Contrast, exposure -1.0, a little saturation and a little bloom round the sun.

## Concept proofs (scale 0.3, 32 samples)

- **A: 85 mm at 10 m, the speaker on the right third, the sun a third in from the left.** The long lens compresses the
  ranges into big, stacked bands of haze; the sun sits on the far ridge.
- **B: 50 mm at 6.5 m, the speaker near the centre, the sun at its shoulder.** The ranges shrink to a thin strip
  under a big sky; the near ground and its bare patch take over the bottom of the frame.
- **Chosen: A.** The idea is the layers, and only the long lens makes them the picture. B makes the sky the picture,
  and the sky here is a plain dusk gradient.

## Critic passes

| Pass | Scale, samples | Blind score | If fixed | Verdict | Top changes | What I did |
|---|---|---|---|---|---|---|
| 1 | 0.5, 128 | 5.5 | 7.5 | iterate | sun not behind the speaker, so nothing glows; tall grass veils its base; nearest range a smooth mound with toy trees; ranges merge into one wash; set as lilac as the speaker (white balance 4800 K, tint 6); a weak white sun; a murky front (bounce 3.5 at 3.5 m, warmer); flat grass | All eight: sun, disk and sky turned to sit at the horn's left shoulder (azimuth 166.6, sky 246.4), sun 14, disk 40 and warmer, bloom 0.2; tall grass kept 4 m clear on the camera side, short grass 4 to 15 cm round the feet; trees off the nearest range, which now carries dry grass at its true scale (darkened, a first try left it a pale dune); haze 0.0035 to 4 m and 0.0004 above, anisotropy 0.6/0.8; white balance 4800 K / 6; bounce as prescribed; grass with bleached tips and ±15 % per strand, clarity 0.1 |
