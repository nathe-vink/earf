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
| 1 | p1 (0.5 / 128) | **5.0** | A grey overcast-looking sky against a warm sun; no aerial perspective, so buttes 3 to 8 km off read darker than the sand and razor-sharp (a miniature); extruded cliffs with level rims and no strata; even ripples with white specks; a tree-like sagebrush and plants crowding the speaker, the yucca cut by the frame; the acrylic shaded on its front with no glow on the sand; a seam at the horizon. Prescribed: a blue cumulus sky with a low sun, haze 0.00011 #C9D3DE, broken rims, a caprock band, beds 0.45, weaker streaks, bigger buttresses, sun behind the right (140, 14), bounce 1.2, varied ripples (bump 0.55), no specks, plants moved off, a domed sagebrush, an 85 mm camera at 11 m. | The coordinator's notes before the pass had already moved the light to a low warm sun (kloppenheim_06, 21 degrees), the horn against the sky, the shale ledges and more plants. For this pass: sky `evening_road_01_puresky` (blue, clouds, a warm sun at 14 degrees), its sun at 115 (between the side light that models the buttes and the backlight that lights the acrylic); haze 0.00011; broken rims (notches up to 28 m) and a darker caprock band; beds 0.45 at 9 m, streaks 0.3; buttresses 1.4x; the stony patches fully tinted (no white); ripples bump 0.55, more wander; the prickly pear to (3.5, 1.7), the yucca to (-1.4, 2.4), the near sagebrush and tumbleweed to 10 m; sagebrush domed, many stems from the ground, foliage low; bounce 1.2; camera 85 mm, 0.4 m, 11 m, f/4. |
| 2 | p2 (0.5 / 128) | **5.0** | The face backlit and muddy (46 against sand 89), the horn's throat crushed; buttes flat and soft with no thumbs in frame (the 85 mm crop lost them); an empty gradient sky; a pale seam at the horizon; the stony patches invisible; the plants in one clump; the speaker dead centre. Prescribed: the sun front-right (55, 14), the thumbs in silhouette, beds 0.7, varnish 0.5, rock at 15 m a tile, the cumulus sky, rolling relief far off, haze 0.00005, stones at 40 % through a 2 m mask, ripples 0.35, the speaker on the left third, the prickly pear back and apart. | Between passes, the first sky change (evening_road at 14 degrees) and the haze had made the sky grey: low rays cross kilometres of haze, and an 85 mm view sees only the pale bottom 10 degrees of any sky. So: back to the cumulus sky `kloofendal_48d` with its sun at azimuth 55 (front-right); the sun lamp lowered from the sky's 48 degrees to 24 for longer shadows, warm #FFD3A0; a soft blue grade on the horizon only; 60 mm at 8 m, f/5.6, shift_x 0.17 (left third); beds 0.7, varnish 0.5, rock at 15 m; haze 0.00004; stones through a 2 m mask at 40 %; ripples bump 0.35 in 3 m patches; long low rises of up to 8 m from 400 m out (`swell3` in dust_el's terrain, optional); the prickly pear to (4.3, 6.0). |
| 3 | p3 (0.5 / 128) | **4.5** | Cliffs as extruded blocks with a repeating vertical stripe and combed aprons; no thumbs in frame; a ruled seam where the flat ground meets the butte bases; the sand uniform from horizon to edge; floating pads, a particle-blob sagebrush; a stray shadow at the right edge (an off-frame plant); the orange speaker merging with the orange sand; flat high light. Prescribed: a low backlight (golden hour at 10 to 12 degrees), real Monument Valley geometry or a backplate, rises of 15 to 30 m and a dune ridge to hide the butte bases, pebbles, joined pads, twig sage, a lower camera, a stronger contrast. | Stopped by the plateau rule (5.0, 5.0, 4.5). Pass 2's critic asked for front light to open the acrylic; pass 3's asks for a low backlight: the passes now trade one fault for another. All three name the same three gaps, which need assets this set does not have: photographed Monument Valley geometry, scanned desert plants and a varied real ground. |

### The duels among the three proofs, and the focused fix

Blind duels (critic/ab/PROMPT-DUEL.txt, fresh judges):
- p1 beat p3, 6.0 to 5.5;
- p2 beat p3, 6.0 to 4.5;
- p1 beat p2, 6.0 to 5.5.

p1 is the best rig. The judges preferred:
- its low warm side light, which models the acrylic (p2's cabinet went dull brown, p3's pink and flat);
- its cumulus sky;
- its prickly pear and sagebrush.

Against it they counted the white specks in its sand (gone since pass 1's stony tint went to 1.0) and stray shadows from off-frame plants.

While the rebuilt drivers come to main, the coordinator asked for one focused fix on p1's rig, then one blind pass:
- **Cliffs:** flutes on three noise scales that merge into broad smooth faces in places; two alcoves or big joints a butte; beds at 0.7; varnish streaks strongest at the rim and fading down the face; a broken caprock edge (kept from pass 1).
- **Talus:** horizontal ledges stepped in (0.02 to 0.09), with the radial gullies cut back (0.16 to 0.07).
- **Distance:** a thin, low haze only beyond 1.2 km (box from y 1200, 420 m high, density 0.00009, #C4CFDE). The near air and the sky above stay clear, while the buttes lift and cool.
- **Sand:**
  - tonal patches at 40 m;
  - about 1,000 pebbles of 1 to 6 cm and 160 stones of 6 to 14 cm, half buried near the camera;
  - low wind mounds of sand on the lee side of each near plant;
  - the plinth sunk 12 mm.
- **Light and frame:** p1's sky (`kloppenheim_06`), sun (azimuth 92, 21 degrees, 9, #FFC98E) and framing (50 mm, 6.5 m, 0.5 m). The prickly pear moved from beside the speaker to (1.6, 1.0), off its silhouette.
| 4 (the fix) | p4 (0.5 / 128) | **5.0** | The buttes still read as procedural extrusions (flat faces, vertical stretch, stepped talus); a hard seam at the horizon; a grey sky; the speaker darker than the sand (59 against 86), no glow through it; brick-red, even sand; wire-ball sagebrush, plastic pads; pebbles as black dots in a band. Prescribed: a blue desert HDRI, haze from 250 m with a dust layer, the sun behind the right at 125/14, scanned or DEM buttes, salmon sand with finer ripples, an 85 mm camera, scanned plants, sand-tinted pebbles. | The focused fix held the score (5.0) but did not raise it: every critic since pass 1 names the same three gaps (the buttes, the plants, the sand), and they need real Monument Valley geometry and scanned desert plants, which no CC0 library here has. The one safe change made before the finals: the pebbles tinted into the sand's colours (#B07050, #9A5A3E). Then main merged (the drivers at 01267eb: the FaitalPRO 15PR400 as made, its ring in opaque polished acrylic) and the model rebuilt. |

### The coordinator's two fixes before the finals (proof a18, 0.3 scale)

- **The speaker darker than the sand (59 against 86).** The sun moved behind it to 110 (a17) left the buttes in flat grey shade and the face at 63 against 99. So the sun went back to 92, and the low warm bounce off the sand (azimuth -25, 4 degrees up, 6 x 1.5 m, #F6C9A0) went from 0.8 to 6. The face now measures 93 against the sunlit sand's 110, and the acrylic glows orange. The bounce lifts the near sand too, so the face stays a little under it.
- **The hard seam at the butte bases.** Long low rises of up to 14 m from 140 m out (`swell3` [14, 380, 140]) now hide the far bases behind the ground.
