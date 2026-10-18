# Fog, concept A: on a summit above a sea of clouds (round 31b)

## The owner, verbatim

- For Fog: "For the fog, I want it to be a shot of the speaker sitting on thick felt clouds, with blue skies in the
  backdrop, a flock of birds in the distance out of focus, etc."
- On the dioramas: "the diorama looks cheap, like a bad video game. I was hoping for more texture in a lot of these. The
  speakers are too stark in contrast to the setting too. Tilt shift may have been a bad direction. Lighting in general
  in a lot of them is off. ... Maybe don't think about them so much like dioramas, and think more about placing them in
  there element, so to speak."
- "Continue to do critic passes until you feel it's in a good enough place for promotional images for a $20K product.
  Install any skills or software you need to make it happen. Tokenmaxx my guy."
- For all eight: "All of them should be looking at the speaker in a way that's more level with the speaker, with the
  speaker turned slightly in either direction depending on the setting."

## The concept

The owner's picture made real. The clear speaker stands on a lichened granite summit in the morning, the camera at its
height. A dark scanned boulder stands right behind the cabinet, so the clear acrylic and its white lining read against
rock while the horn stands against the blue. Beyond the ledge, 130 m below, a sea of cloud runs to the horizon, lit
from the side, with one peak standing out of it far off. A skein of birds crosses the frame far off and soft.

## References (real cloud inversions from summits)

- A sea of white fills the valleys below while you stand in clear sunlight above it. Inversions are common in mountains
  and in winter, need calm air, and are best at dawn and in the morning. Sources: livefortheoutdoors, PetaPixel, Shainblum
  Photo, Mount Seymour, Mount St. Helens and Europhotometeo inversion photographs.
- What to match: cloud tops heaped and brilliant where the sun reaches them, cool blue-grey in the troughs; the sea
  running out flat to a hazy horizon; peaks as islands; the sky deepest blue overhead and about 90 degrees from the sun.

## Choices and why

- **Sky:** `qwantani_puresky`, the deepest blue of the clear Poly Haven skies (previews compared side by side), turned
  169 degrees. Its sun is then at azimuth 65, 28 degrees up, at the camera's right. The sky behind the speaker is about
  90 degrees from the sun, where a clear sky is bluest, and the clouds are lit from the side, which shows their shape.
- **Ground:** `lichen_rock` at real size, displaced, with 0.12 m of relief; `boulder_01` scans behind the speaker and
  along the ledge.
- **Cloud deck:** `kit_ext/fog_el.py` `cloudsea`. It went through four versions:
  1. Perlin noise: snowy ridges with hard blue shadows.
  2. Heaped domes, with small cauliflower domes riding on big ones, as a closed slab with deep subsurface scattering:
     soft and white, but it read as a snowbank because it was too close.
  3. Rescaled to a real inversion: base 130 m below, heaps 170 m across and 85 m high, running out to 26 km.
  4. Haze capped at 300 m altitude: over tens of kilometres of box it had whitened the sky.
- **Engine:** `camera.clip_end` (render.py, knobs.py) in its own commit, because the camera clipped everything beyond
  300 m. The default is unchanged.

## Concept proofs

- c1: the rock's relief rose behind the speaker and hid the clouds; the haze greyed the sky.
- c2: ledge 2.4 m behind the speaker, camera at 0.75 m; the deck read as a flat snowfield, with void in front of it.
- c3: bluer sky with the sun at the side; the noise deck read as snowy hills.
- c4: domed deck, soft but close.
- c5 to c7: rescaled deck, clip distance, haze cap. It reads as a summit above a sea of cloud.

## Critic passes

### Pass 1: 5.0 ("iterate"; 7.3 if fixed)

The frame was r1. Main's `hdri_sun` fix landed after this pass: in r1 the sky's own sun was at azimuth -115 while
the sun lamp shone from 65, so there were two suns. The critic read that as "flat light, no shadow".

The critic: the speaker is crisp and believable, but the world reads as CG. Its changes, and what I did:

1. **The cloud sea is smooth foam; make it a volume.** Done: `cloudvol`, a scattering volume from 250 m to 3.2 km
   whose top is a 2D noise heightfield (220 m heaps, 110 m of amplitude), eroded by a 3D noise into billows, with 6
   volume bounces so it stays white. The domed slab now carries only the far distance, from 2.8 km.
2. **No sun shadow; put the sun behind the speaker on the camera's left.** Done: the sky turned to 189, which puts its
   sun and the lamp at azimuth -135, 28 degrees up. The shadow now runs forward and right, and the edges catch a rim.
   Bounce reflector lowered from 0.5 to 0.25.
3. **The ground ends in a straight tabletop edge.** Done: 0.15 m of relief and the ground ends 3.2 m back. I tried
   scanned cliffs as the drop; they intersected the ledge and showed flat cut tops, so I removed them.
4. **The boulder crowds the cabinet.** Done: moved to the camera's left with clear air before the cabinet, scaled 0.75.
5. **The near rock is a smeared decal.** Done: 4k texture, 7 cm of true displacement, a denser mesh.
6. **The peak floats.** Removed.
7. **The birds form a column.** Done: 11 birds in a loose diagonal in the open sky, upper right, at about 60 m.
8. **Flat tonality.** Done: exposure +0.3, AgX Medium High Contrast, finish contrast 0.08.

### Pass 2: 5.5 ("iterate"; 7.8 if fixed)

The frame was r2. The pass-1 accept tests on r2: 5 of 8 passed (cloud range, clear silhouette, rock range, horizon, birds).
The shadow test missed because the shadow falls right of its test region; the edge and highlight tests missed narrowly.

The critic: a clean idea, and the horn reads beautifully against the sky. But the plateau ends in a tabletop edge with
the clouds directly behind it, the clouds look smeared, the ground is a uniform speckled decal, and the lining reads
grey. Its changes, and what I did:

1. **A believable far edge.** Done: `summit`, my own ground. It is level at the speaker, rolls over a brow 6 m behind
   it and falls 5 m over the next 10 m. Three `mountainside` scans (scale 2.6 to 3.6) stand as outcrops down the
   falling ridge, 34 to 60 m out.
2. **Lower camera, longer lens.** Done in part: 0.6 m (the brief's eye-level band starts at about 0.7; the critic asked
   for 0.42), 65 mm, 6.8 m back. The horizon now crosses the cabinet at mid-height, so the cabinet's top and the whole
   horn stand against sky.
3. **The lining reads grey.** Done: the bounce card at azimuth -60, 18 degrees up, 2.5 m away, 2 x 2 m, irradiance
   0.8, warm white.
4. **Crisper billows.** Done: soft 1.2, density 0.18, detail 12, erode 18.
5. **Aerial perspective.** Done: haze only beyond 200 m, density 1.2e-4, #BFD3EA; the far deck runs out to 40 km.
6. **The ground is a uniform decal.** Done: `dark_rock` at 4k, 12 cm of displacement, 0.3 m of relief. 260 scanned
   `stone_01` pebbles are dropped onto the rock by ray cast, desaturated toward its grey, and none sits within 0.55 m
   of the speaker.
7. **The boulder looks imported.** Done in part: bedded 18 cm into the rock and moved left. A scan's colour can't be
   tinted through `common.asset`, so its colour is unchanged.

Out of scope, as the critic noted: the woofer's black and the acrylic's clarity are the product's.

### Pass 3: 5.5 ("iterate"; 7.5 if fixed). Concept change.

The frame was r3. The critic: clean and legible, but "a careful CG render": the summit is a uniform grey slab with
repeated pale pebbles, the brow cuts the clouds in a straight line, the sky is milky, and the clouds are soft. (Its sun
azimuths use another convention than the engine's: it read the sun as behind the camera when it was behind the speaker
on the left. Its point stands, though: the bounce card made the speaker look front-lit.)

**Three passes: 5.0, 5.5, 5.5.** All three critics flagged the same thing: the modelled ground (a texture on a plane,
however displaced) and its edge read as CG. Per the protocol I changed the concept, not the settings: **the speaker now
stands on a photographed rock**, not a textured plane.

- I searched the scanned rocks for a standing place: ray casts over each scan, looking for a disc 0.9 m across within
  12 cm of level near its top. Only `namaqualand_cliff_02` has one, at (3.72, 3.11, 6.91) in the scan. Its top is a
  narrow ridge about 1.3 m deep, falling away 1.6 m in front and ending behind.
- The scan is moved so that spot is at the origin, sunk 3.5 cm. The speaker stands on a real ridge of sandstone with
  real colour and form, and beyond it the sea of cloud fills the band behind.
- Dropped with the plane: the stones, the outcrops and the boulder.
- Kept from the critic's list: haze density down to 8e-5 (a bluer sky); bounce card down to 0.5 (less front light);
  camera at 0.82 m, so the line of sight clears the 3 cm lip in front of the speaker's feet.

**Render cost.** The cloud volume is about 85 % of the time. In Blender 5 a procedural volume is traced by null
scattering, so the material's step rate does nothing; the cost goes with the box's size, its peak density and the
noise's octaves. The box is now held to what the lens sees (x -400 to 2600 m, y 250 to 2800 m), with density 0.14 and
4 + 3 octaves: 70 s down to about 45 s at the test size, with the clouds still reading as cloud.

### Pass 4: 5.0 ("iterate"; 7.3 if fixed). The first pass after the concept change.

The frame was r4. The critic: the idea works but reads as CG. The sky is washed grey-blue, the clouds are soft cotton
with no sunlit tops, the rock is soft and crushes to black at the bottom, the light is flat with no visible speaker
shadow, and the horizon runs through the cabinet-horn joint.

Its sun azimuths are mirrored again (it read the sun at -135 as near the camera axis, and asked for -40, which in the
engine's convention would be almost straight behind the camera). I took its meaning, not its number: raking sun from
the camera's right front.

What I did:
1. **Light:** the sky turned to 354, so its sun and the lamp are at azimuth 60, 28 degrees up. The speaker's face gets
   raking sun and its shadow falls back and left across the ledge; the sky behind is about 100 degrees from the sun.
2. **Sky:** exposure 0 (was +0.3), finish saturation 0.12.
3. **Camera:** 0.6 m, so the horizon clears the cabinet-horn joint; f/8.
4. **Clouds:** deck lowered 50 m (top -140, more distance and haze over it), soft 0.5, detail 7, octaves 5 and 4.
5. **Rock:** the cliff scan at 8k (was 4k) for texel density up close.
6. **Shadows:** finish lift 0.03 in #3A3530, a warm rock-shadow colour.
7. **Bounce:** warm #D9B49A, 5 degrees up, 0.8 (the rock's colour bounced into the clear base).
8. **Birds:** 7 in a loose V, spread in depth.
