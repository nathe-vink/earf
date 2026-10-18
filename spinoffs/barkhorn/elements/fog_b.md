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
| 1 | 5.5 | c1: the cabinet stood against bright fog, so move the brow back to 28 m. c2: the feet were hidden in tufts; clear them. c3: sun more to the side (az -125). c4: a warm bounce from camera-left. c5: a dense meadow, not tufts on dirt. c6: olive hills, sharper gullies. c7: wisps lower. c8: contrast 0.10, vignette 0.22. | All taken, except c1 adapted: the brow moved to 12.6 m, not 28. At 28 m the brow hides the fog sea entirely (proofs p1 to p6), but at 12.6 m the cabinet stands against the grass and the horn against the hills, with the fog between them and over the ridges. Grass 3500 tufts of three scans, short turf round the feet (z -0.015). Also: biased volumes (step rate 4), about 1.6x faster. |

Between passes 1 and 2 (0.3-scale checks q1 to q4):
- q1: pass 1's changes as given. The meadow was right, but the fog vanished: the brow at 12.6 m hid the fog sea, and
  the sharper gullies raised Alpine peaks above the marine layer.
- q2, q3: softer hills and a higher layer did not bring it back. An overhead debug view showed the fog sea gone flat:
  biased volume marching (step rate 4) smears the billows over an 8 km box. Back to unbiased.
- q4: back to the near brow (2.65 m), so the fog shows from eye level. Pass 1's c1 asked for a dark ground behind the
  cabinet, and a greywacke outcrop at the brow (`boulder_01`, about 1 m tall, flanked by `coast_rocks_05`) gives it
  one: the cabinet stands against rock, the horn against the hills and the fog pouring over them.
| 2 | 6.0 | "A believable misty headland," but the light is flat and grey, with no dawn sun. The speaker looks propped against the boulder, its left edge lost against the fog. The left fog bank is a smooth gradient. The grass is a dark bottom third. The horn reads as chrome. c1: sun irradiance 7, azimuth -135. c2: boulder back and bigger. c3: bigger billows, a sharper edge. c4: clear the plinth. c5: camera 0.95 m, target 0.8, 1.2 m back. c6: a cool, soft bounce. c7: a warmer grade. c8: more relief on the hills. | All taken. c2 at scale 1.3, not 1.5, so the rock stays below the horn; the brow moved to 3.6 m to hold it. c7 without a split tone (the finish has none): saturation 0.08 and a warm lift instead. |
| 3 | 5.5 | "The 'fog' is a beige haze over everything," and the hills dissolve into mush. The sky is flat. The boulder reads as a pedestal, the cabinet as olive-grey, and its base is hidden. c1: less haze and a crisper, denser fog top, the marine layer lower. c2: a stronger neutral bounce. c3: a smaller rock tied in with grass. c4: short grass near the feet. c5: f/2.8. c6: a cloudier dawn sky. c7: a lighter foreground. c8: lower hills. | Down 0.5: pass 2's lower, farther camera and heavier haze hurt. Pass 4 goes back to pass 2's camera (1.15 m, 9.5 m) and takes c1 to c5 and c7: haze 0.0001, soft 1.2, density 0.08, rise +32; bounce 1.1 at az -35; boulder 1.05; no tall grass within 3 m, short within 1.2 m; f/2.8; lift 0.035, vignette 0.12. c6 and c8 are left for now (the sky's sun disc and the hills already work in pass 2). |
| 4a | (not sent) | My own check of pass 4's first proof: turning the boulder hid it behind the speaker (the cabinet against fog again), the 3 m ring cleared of tall grass was bare dirt, and `grass_bermuda_01` renders as black specks. | Boulder back to 75 degrees, scale 1.1. 900 short tufts fill the ring. Bermuda dropped everywhere. Re-rendered before the critic. |
| 4 | 6.0 | The grass is "the most convincing thing in the frame," but the fog stands up as a grey wall that drowns the hills and reads as a matte painting. A pale strip runs behind the brow. The front is in flat shade, so the acrylic reads olive. The boulder halos the speaker like a prop. Asks for: ridges clear above a lower layer with distinct pours, a thinner warm forward-scattering fog, a strong white reflector, a low rock ledge instead of the boulder, a warmer sun, a lower camera, deeper blacks. | **Concept change.** Scores ran 5.5, 6.0, 5.5, 6.0: three passes since pass 2 gained nothing, and every critic names the same things. The fog is a grey wall, not fog pouring over hills, and the speaker sits in flat shade against a prop. B2, below, keeps the place and turns the light round. |

### Concept B2 (from pass 5): the sun low behind the fog, in frame

Still the Marin headland and San Francisco's fog, now shot into the light, as the first brief put it ("a sun low
behind it"):
- The sun sits in the frame's right third, a few degrees up.
- The ridges across the water stand dark and backlit, above a lower marine layer that pours through the saddles and
  glows warm.
- The clear acrylic is rim-lit against them, and a white reflector opens its front.
- The boulder goes; the speaker stands in the meadow at the brow.
- Pass 4's prescriptions that fit are folded in: c1, c2, c3, c5, c6 and c8.
| 5 (B2) | 5.5 | A "quiet, well-composed idea," but washed out and high-key. The fog is a flat white smear and the clear cabinet disappears against it. The hills are soft CG bumps. The speaker is front-filled while the scene is backlit. The grass glitters. Asks for: a lower, thinner fog sea with dark land showing behind the cabinet, bigger billows and a sharper fog edge, a weak sky fill only, exposure -0.35, deeper gullies, the feet sunk in grass, f/4. | Down 0.5 from pass 4, the first pass after the concept change. Took c1 to c4, c6 and c8. c5's gullies at 28/100, not 35/90: 26/120 raised Alpine peaks in q1. c7 not taken: there is no setting for the scans' own grass material, so the glitter is left for the finals' higher sample count. |
| 6 (B2) | 4.5 | "The ridges read as a grainy, sepia, stucco-like procedural surface," jagged rather than Marin. The fog is a flat milky band right behind the cabinet. The speaker is grey and flat-filled, and the grass glitters. | **Stopped.** The two passes after the concept change each gained under 0.5 (5.5, then 4.5), the coordinator's stopping rule. |

## The stop, the duel and the finals

- **Best rig: pass 2** (6.0). Pass 4 also scored 6.0. A blind duel of their proofs chose pass 2, 6.6 to 6.0
  (`critic-fog_b/duel-p2-p4.json`):
  - for pass 2: its clear layers (crisp ridges over a bright fog sea), the clean grass silhouettes on the brow, and
    the rock framing the cabinet;
  - for pass 4: richer backlit grass and a more legible base.
- `fog_b.py` is restored to pass 2's rig (commit 19dc2e1). It rebuilds pass 2's shot exactly. The one change is the
  camera's far clip, now under main's key `clip_end`.
- Finals: 2400 x 1600 and 1600 x 2000 at 512 samples, denoised.

## Finals (2026-10-18)

| Frame | File | Render | Blind score |
|---|---|---|---|
| Landscape 2400 x 1600 | `renders/2026-10-18/barkhorn/element31/fog_b.png` (4.6 MB) | 256 spp, denoised, 3 h 31 min in one piece on 4 cores (plus 7 min to build the scene) | **6.0** |
| Portrait 1600 x 2000 | `renders/2026-10-18/barkhorn/element31/fog_b-portrait.png` (3.3 MB) | 256 spp, denoised, rendered on the coordinator's helper in four strips and finished once | (not scored separately) |

256 samples, not 512: the coordinator advised it (Fog A's volumes held at 256), since 512 would have been 7 to 9 hours
a frame. At full size the final shows no noise in the fog or the grass.

**The honest note.** 6.0 blind, the same as the best proof. It reads as "a quiet, believable dawn headland": the
critics consistently praise the fog sea, the ridges and the scanned grass. What holds it back:

- **The speaker's own clear surfaces.** Every pass read the clear cabinet as a beige or grey box and the horn as
  polished chrome rather than clear resin. Light can only move this so far (backlight through the edges, less front
  fill), because the material is the product's. It may be worth a look at the horn's resin (IOR, thickness,
  roughness) as a product question.
- **The base.** The grass swallows the plinth; clearing the turf in front of the feet is the first fix.
- **The fog high behind the ridges.** It reads as a band across the sky in places. A lower marine layer that pours
  only through the saddles would read more as weather.
- **The light.** Flat and grey rather than one dawn event. A stronger back-rim (sun 4.5 at about -165) is the
  critic's main ask.
- **Settings tried and lost.** Backlit with the sun in frame (B2) made the fog milky and the hills flat, 5.5 and 4.5.
  Sharper gullies made Alps, not Marin.
- **The next step, if wanted.** The final critic's c1 to c6 (clear the plinth, a stronger back-rim, a lower marine
  layer, f/2.8, shorter near grass, the boulder moved right).
