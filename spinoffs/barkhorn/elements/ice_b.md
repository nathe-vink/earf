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
