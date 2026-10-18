# Ice, concept B: Diamond Beach at sunrise (round 31b)

Branch `r31-element-ice-b`. Set `ice_b.py`; its beach, sea and ice are `studio/engine/kit_ext/ice_b_el.py`.

## The idea

Jokulsarlon's Diamond Beach, Iceland, at sunrise: black volcanic sand running down to the surf, chunks of glacier ice
the lagoon has given to the sea stranded on the sand and in the wash, the sun just up over the North Atlantic. The
low sun comes through the ice as it comes through the speaker's blue acrylic. Photographers there shoot into the sun
for exactly that reason: backlight lights the ice from inside (references: Arctic Adventures' Diamond Beach tips,
Gary Hart's "A Diamond in the Surf", Locationscout's Diamond Beach pages).

## Cave or beach

The brief offered a blue ice cave or the beach. I chose the beach before building either: the cave would be
entirely modelled (walls, ceiling, the light through them) with nothing photographed in frame, the thing the owner
called cheap; the beach puts a photographed sunrise sky and sea behind modelled sand and ice, so the light is real
light. The rhyme the brief asks for (light through ice, light through acrylic) works best backlit, and a low sun on a
beach gives that for free.

## What's built

- **Sky:** `umhlanga_sunrise` (Poly Haven, CC0), a sunrise over open sea, the sun on the horizon. Its land is turned
  out of frame.
- **Sun:** a lamp at the sky's own sun (azimuth 176, elevation 1.9). `assets.hdri_sun` gets the azimuth wrong (its
  equirectangular convention is mirrored against Cycles'); `ice_b.sky_sun` works the rotation out with Cycles'
  convention. I reported this to the coordinator; the engine is unchanged.
- **Sand:** Poly Haven `gravelly_sand` (4k) for grain, normal and displacement, laid twice and blended so it doesn't
  tile; its albedo remapped to basalt black (linear about 0.01 to 0.06), specular 0.06 (GGX at grazing turned a
  rough black sand into grey concrete at 0.35), soaked and mirror-like within 7 cm of the water, damp above.
- **Sea:** a closed body of water (absorbing, so it reads deep), its surface modelled from the shore to 420 m with
  four breakers rolling in, whitewater carried as a mesh attribute and torn into streaks in the shader, a lace of
  foam and a white rim where the wash runs thin over the sand (worked out from the beach's own profile).
- **Ice:** each chunk an icosphere cut by 8 to 12 fracture planes, worn a little, with melt scallops; refractive
  (IOR 1.31) under a wet coat, blue by absorption, white where bubbles drift (a scattering volume in patches), with
  modelled air bubbles in layers and a crack or two. Shadow rays pass through tinted, so the ice throws blue light
  rather than black shadow (caustics are off in the engine).

## Concept proofs (0.3 scale, 32 samples)

- **A, sun in frame** (azimuth 176): the sun just over the horizon left of the speaker, its glitter path running
  down the sea to the big chunk, long shadows toward the camera, the ice lit from behind.
- **B, sun out of frame left** (azimuth 198): softer, the ice and acrylic lit from the side and behind.

A is stronger: the sun in frame says sunrise and Diamond Beach at once, the glitter path leads to the ice, and the
backlight is the idea. B was flat and could be any grey beach. I went with A.

## Before the first critic pass

- p2: the sky turned the right way (the `hdri_sun` problem); the sun and its glitter path agree.
- p4/p5: sand blackened. The grey was all specular (a test with specular 0 read 2/255): albedo raised to real
  basalt sand, specular cut to 0.06.
- r1: ice less dense (1 m of ice was swallowing the orange sun); bubble patches added; foam made translucent;
  exposure -0.3.

## Critic passes

| pass | image | score | if fixed | verdict | top changes | what I did |
|---|---|---|---|---|---|---|
| 1 | r1 (half size, 128) | 5.5 | 7.5 | iterate | sand reads brown cork not black; sea smooth pale bands near sky's brightness; sun beside, not through, the speaker; glass-bead small ice and pieces cut by the frame; no wet reflections; no haze; horizon tangent to the cabinet top; big chunk lavender | Sand: albedo #0D0D0E-#2E2D2C, texture twice as fine, bump 1.0, displacement 6 mm, specular 0.05 (not 0.35: GGX sheen was what made it grey), damp only within 10 cm of the water (damp sand at grazing mirrors the sky), sparse glassy grains that glint. Sea: roughness 0.07, chop 0.9, absorption #2F4A48 at 6/m, crests broken along their length at two scales. Sun to azimuth 172.5, just off the cabinet's left edge. Removed ice 3, 4, 9; ice 7 moved to (2.0, 2.9) and enlarged. Shore starts 0.5 m behind the speaker so the wet band begins about 0.9 m behind it. Haze 0.002/m, 8 m deep, #F2C9A8, anisotropy 0.6. Camera to 0.70 m (the brief's floor; the critic asked 0.65). Ice absorption toward cyan (#4FAAD8 / #6CBCE2), coat roughness 0.03, big chunk to (-0.9, 2.6) with 3 cracks; cracks and bubbles now kept inside the finished chunk (two fins poked out of its top). |
| 2 | r3 (half size, 128) | 5.5 | 7.2 | iterate | sun beside the speaker, not behind it, so neither acrylic nor ice glows; hard straight water/sand seam with no wet band; empty foreground, all the ice in the water; milky low-contrast sea of parallel ribbons; sand warm brown with glitter sparkles; washed-out sky; no contact at the base; horizon at half height | Sun to azimuth 169.5, behind the cabinet's upper left; big chunk to (-0.5, 3.4) in the glitter path. A wave's reach line 0.7 m in front of the speaker: soaked mirror-wet sand behind it (the speaker stands in its own reflection), damp before it, a broken lace of spent foam along it. Three chunks stranded in front (one in the sun's strip). Sea rebuilt on Blender's FFT ocean (two spectra, 53 m and 131 m, summed so neither tiles), calming over 7 m as it shoals, plus two breakers with whitewater; absorption #1E3533 at 10/m. Haze 0.0008. Sand #0A0A0B-#232324, relief 6 cm, glints at 3 mm grains, 2 %, softer. Exposure -0.6, AgX Medium High Contrast, contrast 0.10, vignette 0.18. Sink 15 mm. Camera 0.65 m, 65 mm, 6.5 m, f/4. |
| 3 | r6 (half size, 128) | 5.5 | 7.6 | iterate | the cabinet a near-black silhouette against the bright sky (lum 37, red crushed); a hard straight wet/dry seam at the speaker's feet; a silky sea with no surf; brown sand; a flat black shadow slab; the blue ice reads grey glass | Not applied: see below. |

### Three passes at 5.5: the concept, not the settings

Three passes in a row gained nothing (5.5, 5.5, 5.5), though the frame changed a lot between them; the brief says
to change the concept then. Each critic's first complaint traces to the same root: shooting into a sun on the
horizon makes the speaker a silhouette, and every fix for that (a fill lamp, a sun through the side panel) fights the
light the image is built on. The beach also asks for the hardest things to fake at once (a sea, surf, a shoreline).

So I'm taking the brief's other concept B: **inside a blue glacier ice cave**. The daylight comes in at the mouth,
behind the camera, and lights the speaker's front; the cave's walls glow blue with the light through the ice, so the
speaker's blue acrylic sits in the same light as its setting (the owner: "too stark in contrast to the setting");
the tunnel recedes into deeper blue behind it; a hole in the roof drops one shaft of daylight through the cave's
mist. The ice material, the black sand and the haze carry over from the beach. The beach stays in the repo
(`ice_b.py`'s `beach_shot`) as the frame to duel with.

### Building the cave (proofs c1 to c9)

- **Shell:** one closed solid of ice: an arch 4.6 m wide and 3.3 m high (a superellipse, walls running below the floor),
  from the mouth 1.4 m behind the camera to a bend 22 m in that hides the far end; its size wanders along the tunnel;
  broad lumps of melt-out; scallops 0.5 m across and 6 cm deep (a jittered grid of cups with sharp ridges between, as
  melt carves them); the ice 0.9 to 2.2 m thick, thinning toward a hole in the roof; the hole's rim sealed so the
  solid stays closed.
- **Ice:** the inner face wet and refractive (IOR 1.31) under a coat; the outer face a translucent diffuser, like the
  firn and snow over a real cave, so the daylight comes through the ice diffused and the walls glow; blue by
  absorption only. A scattering volume this thick took six minutes a proof at 0.3 scale (c1); absorption alone takes
  70 s and looks right. Ash bands as a varying volume drew scribbles on the walls and cost ray marching; dropped.
- **Light:** `snowy_hillside` outside (snow all round, a clear winter sun at 20 degrees); the sun lamp from the engine's
  `sun_from_sky`, at azimuth 167 so its beam drops through the roof hole into the mist and lands on the floor left of
  the speaker. The mouth: its sky alone left the speaker's front black (c6, the mouth faces trees in the map), so a
  soft panel stands where the opening is, 3.6 x 2.6 m, daylight #EAF1FF, 0.85 W/m2 at the speaker: the mouth's light,
  as a photographer would let it in. The floor stops at the mouth so the snowfield's light comes in under it.
- **Mist:** 0.008/m through the cave, so the beam shows.

| pass | image | score | if fixed | verdict | top changes | what I did |
|---|---|---|---|---|---|---|
| 4 (cave 1) | c9 (half size, 128) | 5.0 | 7.0 | iterate | walls glossy plastic blobs, no inner structure; right wall dead navy; speaker pale, flat-lit, hazed and pasted on, no contact or reflection; crushed black floor; speaker small; the hole and tunnel end a neutral white patch | Ice rougher (0.06-0.3), scallops jittered 0.6-1.6x and 4 cm deep, finer lumps; a little even scatter (0.15/m: 2/m with thin walls turned the cave to white marble, c10-c11, so the thickness went back to 0.8-1.8 m, where the long path makes the blue); sky strength 2.5; sun warmer #FFE4C4, 3.0. Mouth light now a raking 1.5 x 2 m panel camera-left at 0.35 W/m2. A pool of meltwater under the speaker's front, ragged-edged, reflecting it; sunk 2 cm. Floor lighter (#141416-#34343A), specular 0.2, rougher grains glinting. Camera 50 mm, 0.8 m, 4.3 m, the speaker on the right third. Haze 0.004 through the cave, a mist column 0.012 where the beam falls. Grade: contrast 0.14, clarity 0.12, vignette 0.22, bloom 0.08. |
| 5 (cave 2) | c13 (half size, 128) | 5.5 | 7.8 | iterate | walls read as grey-lilac chrome or molten plastic, specular, no glow; right wall a navy void; the sun a white floor patch and a blown tunnel end, no shaft; speaker underlit (33); no edge against the wall; pool a cut-out; scallops repeat | Tried (c14-c17): firn behind the ice with patches and ash bands; a high-sun sky (pizzo_pernice_puresky) for a steep beam; thin ice with blue scatter (bleached it again); thick ice under a brighter sky (a bright subway tube); none convincing. Held a duel before going further (below). |

### Duel: beach or cave

A blind duel (critic/ab/PROMPT-DUEL.txt, run by hand so as not to touch `critic/best.json`) between the cave's best
(c13, pass 5) and the beach's best (r6, pass 3): **beach 6.0, cave 4.5, prefer the beach.** The judge read the
backlit beach as a clean silhouette with a rim, and the ice chunks held up at 3x (refraction, bubbles, highlights);
the cave's walls as glossy blue plastic with repeating lumps, its product dissolving blue into blue. Against the beach:
the straight water/sand seam with dry sand in front, colour fringing at the cabinet's edges, the dark front, the heavy
shadow. So the beach it is, after all; the cave stays in `ice_b.py` (`cave_shot`) and `ice_b_el.cave`. Two concepts
proven, the better one kept; the brief's half-point rule did its job by forcing the comparison.

### Back on the beach: pass 3's list

- Sun at azimuth 168, behind the cabinet's left half (pass 3 asked "+8 deg", the wrong way for this frame: at 175 the
  sun walked off to the left, r7).
- A photographer's bounce beside the camera: a 2.5 x 2 m white reflector, 1.5 W/m2 at the speaker, #FFE6CC, its
  reflections at 0.3, so the front reads in the backlight.
- The wash reaches 1.6 m in front of the speaker with a wobbling, lacy edge and damp sand grading over a metre before
  it: the speaker stands inside one wet surface, the dry sand only in the foreground.
- Breakers at 6 m (0.3 m high) and 14 m (0.45 m), whitewater 1.0 and 0.9, ocean foam coverage 0.5, chop 1.2; f/5.6.
- Sand cooler and grainier: #0B0B0D-#26282B, bump 1.5, glints 3 %. Wet roughness 0.06 (the mirror band was as bright
  as the sky).
- The big chunk to (-0.9, 3.0) at absorption 3.4/m, bluer. Shadows lifted 0.03 toward #1A2230; vignette 0.12.

| pass | image | score | if fixed | verdict | top changes | what I did |
|---|---|---|---|---|---|---|
| 6 (beach again) | r9 (half size, 128) | 5.5 | 7.0 | iterate | the sun hidden behind the speaker so nothing visibly backlit; front lit neutral like a studio; sea smeared, no surf; brown dry sand; the wet band a pale studio floor; a looming shadow trapezoid; a clipped green line on the cabinet top | Sun to azimuth 162: in clear sky right of the speaker, its glitter path down the sea and the wet sand (150 put it out of frame, r12; its elevation stays at the sky's own 1.9). The bounce now a weak warm ground bounce (0.5, #F6C9A0, no reflections, 0.3 m up). Breaker at 8 m, 0.55 m high; chop 2.2; sea roughness 0.04. Sand #08080A-#1C1D20, specular 0.1, bump 2.5. Wet film roughness varies 0.05-0.2 by noise. The wash reaches 3 m in front, wobble 1.2 m. Exposure -0.75, white_in 250. Haze 0.002 beyond 15 m. |

The coordinator's stopping rule since 08:20 (scores across every session sit at 4.5 to 6): after a concept change,
stop when two passes in a row gain under 0.5. Passes 4 to 6 went 5.0, 5.5, 5.5; pass 7 decides.

On the horn's throat (the coordinator's note): what reads black is the compression driver seen through the solid
resin of the waveguide. A card in front and a card behind, each lighting only the waveguide and the driver, changed
nothing (r10, r11): with refractive caustics off in the engine, no lamp reaches a surface seen through the resin. I
took both out rather than keep lamps that do nothing. Lighting it would mean an engine change (caustics) or a change
to the product's material, neither mine to make.
| 7 | r14 (half size, 128) | 5.5 | 7.8 | iterate | the soaked foreground reads as a pale mirror or ice sheet, not black sand; the cabinet dark navy with no warm rim; the sea glassy, no surf white water; a seam where the calmed sea meets the shore; seven evenly scattered ice props, the near one competing; a glare column | Not applied: the stopping rule (below). |

## Stop, the duel, the finals

Passes 5 to 7 went 5.5, 5.5, 5.5: two passes in a row after the concept change gained under 0.5, so by the
coordinator's rule the passes stop here. The critics had also begun to contradict each other: pass 6 wanted the sun
in clear sky beside the speaker and the foreground wetter; pass 7 wanted the sun back behind the cabinet and the
foreground dry.

Every beach pass scored 5.5, so a blind duel chose the rig: pass 7's frame (r14) against pass 3's (r6, the earlier
duel's winner over the cave). **r14 6.5, r6 5.5, prefer r14**: the wet shore runs unbroken from the waterline to the
frame's edge (r6 had a hard straight seam with dark sand in front); the low sun beside the speaker lays a warm streak
and the speaker's reflection across the wet sand (r6 had a black shadow wedge running at the camera); the sea has
wave texture and highlights. For r6: its big ice block read as clear, lit ice, where r14's reads darker, like grey
glass. Both: the cabinet's front is underlit.

The finals are rendered from r14's rig, unchanged: 2400 x 1600 and 1600 x 2000, 512 samples, the sky at 8k. The
portrait is re-framed, not cropped: 55 mm from 4.3 m, shifted left (-0.09) so the near chunk is whole and the speaker
sits on the right third, the sky above it left for type.

### What holds it back (honest)

- **Blind score 5.5**, stable across seven passes and two concepts; the duels give the final rig 6.5 against the
  runner-up. Nowhere near the brief's 8.5.
- **The speaker against the sun.** Shooting into a sunrise makes the cabinet's front dark and cool; every critic
  asked for it lit by the sunrise, and a stronger bounce reads as a studio light. The light that would carry it
  (sun through the acrylic and the horn) is caustic light, which the engine does not render.
- **The horn's throat** reads as a black blob: the driver seen through solid resin, which no lamp can reach without
  caustics (r10, r11).
- **The ground** reads as a mirror sheet more than black sand where it is soaked; dry, it read as brown dirt.
- **The sea** reads as glassy swell more than North Atlantic surf; the breakers' white water hardly shows from 0.65 m.
- **The ice** reads well close up (refraction, bubbles, cracks: the duels praised it), but the big block can go grey.

### The final, judged blind

The landscape final at full size, one more fresh critic: **5.8** (7.6 if fixed), the highest single blind score
of the set. It sees a calm pastel sunrise with a strong central silhouette and a believable warm glint on the wet
ground, but a well-lit CG set: the sea gel-like with no real foam, the ground pale wet concrete rather than black sand,
the ice sitting like props, and the speaker a dark navy block the sun never passes through. Its first three changes
(dry black sand in front, the sun grazing the cabinet's right edge, more bounce) are the same tug of war the passes
went round; the reply is in `critic_ice_b/final.json`.

Render times (CPU, this container): landscape 2400 x 1600 at 512 samples, 92 min; proofs at half size and 128
samples, 7 to 10 min; at 0.3 and 32 samples, about 1 min.

Portrait 1600 x 2000 at 512 samples: 76 min. Its near-left chunk just touches the frame's left edge, and the
speaker's reflection carries a green-gold streak (the low sun through the blue acrylic onto the wet sand: the
speaker's own light on the ground, as the brief asks, though greener than the acrylic reads).
