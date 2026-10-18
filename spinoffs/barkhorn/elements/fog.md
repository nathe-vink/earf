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
