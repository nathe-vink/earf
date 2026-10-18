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

### Pass 5: 5.5 ("iterate"; 7.0 if fixed)

The frame was r5: raking sun from the front right and a deep blue sky. The critic: a clean idea with room for type,
but the cloud sea is evenly lit with smooth faceted domes far off, the white lining and ring merge with the white
clouds, the near rock is soft, and the birds crowd the horn. A gain of 0.5 over pass 4, so the stopping rule (two
passes in a row gaining under 0.5) is not met.

What I did:
1. **A low raking sun from behind on the left:** `mpumalanga_veld_puresky`, the deepest blue of the low-sun skies,
   turned 184, so its sun and the lamp are at azimuth -130, 8.5 degrees up, in a warm #FFE2BE. Shaded cloud flanks now
   face the camera, rims fall on the acrylic, and shadows run long.
2. **Far deck:** smaller heaps (billow 140, height 45), fine bumps (4 m), out to 80 km.
3. **Haze:** 1.4e-4, #C9D6E6, anisotropy 0.7; the box widened to the new horizon.
4. **Rock sharpness:** f/11, focused a little in front of the speaker.
5. **Birds:** 5, moved to the upper right, clear of the horn.
6. **Footing:** the cliff moved 0.15 m in x and 5 mm up, so the flat block lies under the whole base.
7. **Bounce:** down to 0.4, azimuth -30, 15 degrees up: a lift only.
8. **Composition:** the speaker on the left third (target x 0.45), camera at 0.5 m, so the horizon falls below the
   cabinet's top and the right of the frame is open sky for type.

### Pass 6: 5.5 ("iterate"; 7.5 if fixed)

The frame was r6 (low sun behind on the left, speaker on the left third). It is the first frame without the blue bar
at the right horizon: a 190 km haze box had left a hole in the haze there (likely float precision), cured by holding
the box to 70 x 40 km.

The critic: a strong idea with room for type, but the speaker straddles a crevice and the lip hides its base; the
backlight leaves the foreground rock a muddy near-black slab and the lining a dull taupe; the near clouds are
even-sized CG cotton, neutral white under a warm sun. No gain on pass 5: the first of the two passes the stopping rule
counts.

What I did:
1. **Footing:** the cliff moved to x -4.00, z -6.90, so the flat block lies under the whole base.
2. **Camera:** up to 0.85 m (not the critic's 1.05, which would put the horizon through the horn), focused on the
   speaker's front face, so the footing shows over the lip.
3. **Sun:** swung 65 degrees toward the camera's left. `qwantani_late_afternoon_puresky` turned 119, so its sun and the
   lamp are at azimuth -65, 19 degrees up, raking the speaker's front and the rock faces.
4. **Bounce:** a warm #E8D6C4 reflector just off the lens, low, at 1.1.
5. **Rock:** finish clarity 0.08. A scan detail layer would take an engine change; left for later.
6. **Clouds:** bigger, irregular heaps near (scale 380, amp 160, soft 0.7, erode 26); haze up to 2.4e-4.
7. **Cloud colour:** the volume's scattering colour #FFF6EC, so sunlit tops carry the rock's warmth.
8. **Birds:** pushed out to 120 to 160 m, spans to 1.4 m, so they fall soft.
- (Before pass 7: the warm scattering tint #FFF6EC turned the whole cloud sea brown, because the tint compounds at
  every scattering event, and haze at 2.4e-4 greyed the sky. Both reverted, to white and 1.4e-4, before the critic
  saw the frame.)

### Pass 7: 5.0 ("iterate"; 7.2 if fixed). Stop.

The frame was r7: the sun on the speaker's front from the camera's left, `qwantani_late_afternoon_puresky`. The critic:
calm but flat and grey. The sky is a neutral grey wash, the speaker is evenly lit with no sun modelling, there is no
contact or cast shadow in frame, the rock is soft up close, and the birds are specks.

**The stopping rule** (the coordinator's, from 08:20): after a concept change, stop when two passes in a row gain under
0.5. Pass 6 gained 0 and pass 7 lost 0.5, so I stopped here.

Scores, pass by pass: 5.0, 5.5, 5.5 (then the concept change), 5.0, 5.5, 5.5, 5.0.

## The duel and the finals

**Blind duel** (critic/ab/PROMPT-DUEL.txt, a fresh agent, the frames named A and B with the key kept elsewhere):

| Frame | Rig | Score |
|---|---|---|
| A | pass 6 (r6): low backlight, speaker on the left third | 5.8 |
| B | pass 5 (r5): raking sun from the front right, deep blue sky | **6.4, preferred** |

The judge preferred B for:
- the woofer and tweeter reading as real drivers;
- a clean white interior behind clear edges;
- warm, key-lit rock with grain;
- a deeper sky that separates the silhouette;
- a stronger hero layout.

A's softer clouds were the one thing in its favour.

**The finals' rig** is pass 5's (`fog.py` as at dcbb4ff), with one change: the birds moved up and right, off the horn,
which pass 5's critic flagged as a defect. The 4:5 frame keeps the same place and turns, on a 100 mm lens aimed a
little higher; the speaker fills 42 % of its height.

**Samples:** the finals render at 256 samples with the denoiser, not the brief's 512 to 1024. The near cloud deck is a
procedural volume: at 128 samples a half-size proof took 23 minutes, so 512 at full size would be about 6 hours a frame
on this 4-core machine. 256 is about 3 hours, and the denoiser cleans the volume's noise.

## The final, and an honest note

**Landscape:** `renders/2026-10-18/barkhorn/element31/fog.png`, 2400 x 1600, 256 samples, 3 h 05 min. It has its
`.report.json` and `.shot.json`.

**Portrait:** `fog-portrait.png`, 1600 x 2000, from the same rig on a 100 mm lens, rendered by the coordinator's helper
session on `r31-element-fog-portrait`.

**Blind critic on the final: 6.5** ("iterate"; 8.2 if fixed), the best score of the round. The critic: a clear,
well-art-directed idea with a believable photographed sky and plenty of room for type; a strong render, not yet a
location photograph.

What holds it back, in its words and mine:

1. **The far cloud deck** (the modelled slab beyond 2.6 km) is a field of smooth, repeated white domes. It is the
   biggest tell. The near volume reads as real cloud; carrying the volume out to about 9 km would fix it, at a large
   render cost (the volume is already about 85 % of the time).
2. **Footing.** The speaker's left base sits over the crack between two slabs of the scan, with no contact shadow it
   owns. Moving the speaker about 0.3 m onto the right slab would fix it.
3. **The scanned rock** is soft at 1:1 in the bottom third. It needs a micro-detail normal and grit (an engine change to
   the asset material), or a longer lens (85 mm) so the rock band shrinks and the speaker grows.
4. **Flat front fill.** The warm bounce flattens the speaker's modelling a little against the hard sun on the rock; a
   lower bounce (0.3) would give the acrylic more sun-made form.
5. **The flock** is one silhouette repeated: vary the spans, glides and banks.

Scores, pass by pass: 5.0, 5.5, 5.5, then the concept change, then 5.0, 5.5, 5.5, 5.0; the final scored 6.5. The
fixes above are concrete, and the critic puts them at 8.2. The next round should start with 1 (the far deck as a
volume) and 2 (footing).

## Round 2, for the record

The coordinator asked for one more round on the final critic's cheap fixes. The rig is a31e7bc:
- **Footing:** the speaker on the scan's flattest place (found by ray casts; level within 4.8 cm, off the crack).
- **Birds:** varied in size and pose.
- **Rock:** a grain bump (kit_ext `scan`).
- **Bounce:** down from 0.8 to 0.3.
- **Far domes:** broken with noise.

**Landscape:** fog.png, 2400 x 1600, 256 samples, 3 h 02 min.

**Portrait:** fog-portrait.png, 1600 x 2000, 256 samples, 79 min, by the helper session (r31-element-fog-portrait-r2 at
d1002aa, merged here). The helper notes the speaker stands square on the slab with no gap, though the contact shadow
is faint, and two of the six birds are edge-on dashes.

These replace round 1's frames on this branch; round 1's are in main (0e6c7db, 008c243) and in this branch's history.
Neither frame got a duel or a critic pass. Fog B won the blind duel against Fog A's round 1, 6.7 to 4.7, and is on the
site, and the owner has asked for a San Francisco Fog (Fog C, by the Fog B session). So this concept stops here.
