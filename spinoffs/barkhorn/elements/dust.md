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
| 2 | p2 (0.5 / 128) | **6.0** | Sand pale pink-beige, not red (dE 26.9 vs #B9592A); a neutral grey sky; flat mesa faces (range 13); a bright dust band at the horizon; one ripple scale; speaker 46 % high with the horizon at its top; the tumbleweed competes; a black woofer. Prescribed: tint #A9502A at 1.0, a warmer sky, rock at 3 m with ledges, a thin wispy dust, three ripple samplings, a 75 mm camera at 0.45 m f/2.8, the tumbleweed farther back, bounce 2.0. | All of these, adjusted. Tint at 1.0, albedo x0.85, specular 0.2 (the backlit sand glared pale at a grazing view). Warm white balance 7200 K for the sky: one grade over the frame, since the engine's sky takes no tint. Rock at 3 m, ledged beds of uneven thickness (a regular ledge read as a staircase on the silhouette). Dust sheet at 0.2 with 3 m wisps; three ripple samplings; small 0.15 m swells near the speaker. Camera 65 mm at 0.6 m and 7.4 m, f/2.8 (75 mm made the mesa a wall), with the mesas made smaller. The tumbleweed rolls past at (3.2, 4.5), snapped onto the terrain by a ray cast. Bounce 2.0 on 5 x 1.5 m. |
| 3 | p3 (0.5 / 128) | **6.0** | Mesas still flat cut-outs (range 12.5) with no talus; the tumbleweed hovers, its shadow straight down; one ripple pattern; a muddy front; the lamp at 11 degrees vs the disc at 6; no grain. Prescribed: displaced rock with fractures and talus, the tumbleweed grounded and sparser, haze 0.0016, lamp at 7, bounce 3.5, finer ripples, grain, a broken dust band. | Three passes gained only 0.5 (5.5, 6.0, 6.0), so per the protocol I changed the idea of light, not the settings. With the sun behind them the mesa faces can only be silhouettes; "flat" was the light, not only the rock. Tried sun azimuths 75, 85, 118 and 90 (d01 to d05). Chose 90: the sun from the speaker's right, out of frame, raking the mesas' fluted faces and the ripples, its light passing through the cabinet toward the camera's side, as in the classic Monument Valley evening photographs. Also: rock with true displacement 0.6 m on a denser mesh and colour banding by bed; ripple bump 1.6; the tumbleweed snapped by its lowest stem (the ray first hit its own mesh); haze 0.0008 (0.0016 fogged the frame); lamp 15 at 8 degrees; bounce 1.5 (3.5 flattened the front); exposure +0.25. The engine's finish has no grain. |
| 4 | p4 (0.5 / 128) | **5.5** | The side light leaves the acrylic dull and brown with no glow; the sky a neutral grey; the three rotated samplings cross-hatch the ripples, pinkish; weak shadows (0.84 of the lit sand); soft mesas; no visible dust; the tumbleweed a pale blob, its shadow a stripe across the frame. Prescribed: a three-quarter backlight (sun at 125, 6 degrees, out of frame), tint #B8632F, near-parallel samplings with bump 2.2, sky 0.3 with the sun at 20, white balance 7800, displacement 1.5 with bed contrast 0.35, dust ribbons, the tumbleweed at (2.6, 3.0) thinner and darker, more contrast and vignette. | All made. Pass 1 asked for 115 and pass 4 for 125: a three-quarter backlight is the middle between the in-frame sun (glow, but silhouette mesas) and the side light (mesas, but no glow). The first try, with dust ribbons at 0.45 and haze 0.0012 at anisotropy 0.7, was a dust storm (d06). Settled at haze 0.0009 / 0.6, ribbons 0.16 from 7 to 19 m back, the tumbleweed's puff 0.12. |
| 5 | p5 (0.5 / 128) | **5.5** | A muddy face (lum 69); bump-mapped regular sand with wet glints; a neutral grey sky (193/191/187), as in every pass; mesas as soft slabs; a bright flat band at the horizon; sand as saturated as the speaker; a static tumbleweed that competes. Prescribed: bounce 4.5 on 8 x 3 m, sun at 105, bump 1.0 with specular 0.05, a warm sky, talus and a turned mesa, thinner wisps, browner sand, the tumbleweed mid-bounce farther back, an 85 mm camera low at 10 m. | The grey sky came up in every pass, and the engine's sky took no tint. So I added `sky.grade` (a graduated filter over a photographed sky, in its own engine commit, backward compatible), set #F7C49A at the horizon fading by 30 degrees. Tried the 85 mm low camera (d08, d09): the frame went soft and hazy, and a near swell banded the foreground, so I kept the 65 mm. Made the rest, in between where critics disagree: sun at 118; bounce 3.2 on 8 x 3 m; sand #B06540 at 0.85, bump 1.4, specular 0.05, 3.4 m a tile; wisps 0.07; haze 0.0008; the right mesa turned 20 degrees; the tumbleweed 0.6 m caught 5 cm off the sand mid-bounce, with a puff where it touched. |
