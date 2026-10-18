# Dust, in its element (round 31b, concept A)

The set is `dust.py`, with its own pieces in `studio/engine/kit_ext/dust_el.py`; the frames are
`studio/shots/barkhorn/element31/dust.json` and `dust-portrait.json`.

## The owner, verbatim

- "the diorama looks cheap, like a bad video game. I was hoping for more texture in a lot of these. The speakers are too
  stark in contrast to the setting too. Tilt shift may have been a bad direction. Lighting in general in a lot of them
  is off. ... Maybe don't think about them so much like dioramas, and think more about placing them in there element,
  so to speak."
- "Continue to do critic passes until you feel it's in a good enough place for promotional images for a $20K product."
- "Dust should have something like a tumbleweed too, with the big flat desert plateaus in the back."

## References

Monument Valley and the Colorado Plateau at golden hour, from photographers' guides:
- the low raking light turns the sandstone burnt orange, and long shadows define the terrain;
- the buttes rise from a flat valley floor of red sand;
- shoot low, to give the buttes their scale against the sky.

Wind-rippled red sand, as in Coral Pink Sand Dunes. Backlit sand glows and its ripples catch the light. Sources are in
the notes I sent the coordinator; my scratchpad has the list.

## Concept

The speaker stands on wind-rippled red sand, at eye level, on the left third. Behind it a broad flat-topped mesa and a
slim butte rise from the valley floor into a warm evening haze. The horn stands against the clear sky in the gap
between them.

The low sun is behind the speaker and a little to its right:
- the acrylic glows;
- its long shadow runs toward the camera, filled with the orange light that came through it;
- the ripples catch the light.

A tumbleweed has come to rest to its right.

### Building it

- **Sky:** Poly Haven `qwantani_sunset_puresky`, a clear Southwest-like evening. Its sun is 6 degrees up; the pure-sky
  version, because I model my own horizon.
- **Ground:** one terrain mesh (`terrain`), a fan of rings from the camera out to 292 m: dense under the speaker, coarse
  far off, so no seam. It is laid with Poly Haven `aerial_beach_01` (real wind ripples) at 2.6 m a tile, tinted to
  red sand, with patch variation against tiling. Its far rim rises onto the horizon.
- **Plateaus:** modelled (`mesa`): sheer fluted cliffs on a concave talus, in Poly Haven `cliff_side` rock. The
  engine's camera sees only 300 m, so they stand at 215 to 285 m at a tenth of Monument Valley's size. The angle they
  fill is the same, and a lens focused at 6 m sees both distances at infinity.
- **Tumbleweed:** modelled (`tumbleweed`), a Russian thistle's dead ball: stems branching into twigs and finer twigs,
  curling inside a 0.62 m ball.
- **Dust:** a noisy scattering volume behind the tumbleweed (`dust`), plus a faint haze over everything.

## Concept proofs

- **a01.** The sun 25 degrees right of the frame. The light was flat and mauve: the blue sky overpowered a 6-degree sun
  on flat sand.
- **a02 / b01, sun off frame right vs. sun behind the speaker.** With a stronger sun (irradiance 9), the sky at 0.5 and
  the haze halved, both read. B (sun at azimuth 150) backlights the tumbleweed so it glows. B chosen.
- **b02.** The sun lamp raised to 11 degrees: still golden hour and long shadows, but the flat sand gets direct light.
  The sand turned orange, the backlit ripples glow, and the acrylic throws orange into its own shadow. The mesas read
  as cardboard, and the horn sat against a mesa.
- **b03.** The sun at azimuth 115, to model the mesas. Rejected: the sand and acrylic lose their glow.
- **b04.** Back to 150. The rock darkened so the backlit mesas read under the haze. The mesas moved apart so the horn
  stands in the gap against the sky, the camera lowered to 0.78 m, and the speaker shifted to the left third.

## Critic passes

| Pass | Image | Score | Top changes | What I did |
|---|---|---|---|---|
| 1 | p1 (0.5 / 128) | **5.5** | Mesas flat, evenly lit cards; a grey moon-like disc in a cool sky; the tumbleweed floats on stilts; one ripple scale everywhere; magenta shadow; a murky front. Prescribed: sun to azimuth 115, layered rock at 6 m, a warm sky, the tumbleweed bedded in and denser, two ripple scales, saturation 0, a bigger bounce, a low dust sheet. | The "moon" was the sky's own sun: `assets.hdri_sun` was 180 degrees off until main's fix (b49838c), so my lamp at 150 stood opposite the sky's sun at -30. The look book's 5600 K white balance also coloured this frame (also fixed on main). After merging, the sky's sun stands at 150 and shows in frame just above the big mesa: backlit mesas, a warm sky, one light. So I kept the sun in frame rather than moving it to 115. Made the rest: the tumbleweed bedded 4 cm with 46 stems x 8 x 6; two ripple samplings (1.55x, 27 degrees) through a 9 m mask; swells 0.6 m; rock at 8 m, darker; bounce 1.2 on 4 x 1.5 m; saturation 0; haze 0.0007 at anisotropy 0.35 (forward scatter had washed the frame); a low dust sheet behind. |
