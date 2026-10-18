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
