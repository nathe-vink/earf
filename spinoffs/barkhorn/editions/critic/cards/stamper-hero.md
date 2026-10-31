# Shot card: Stamper, studio hero

## What the frame is for
The edition's hero: a record stand (300 x 80 x 72 mm) in clear cast acrylic with a 3 mm smoke-grey base stratum and a slot along its top holding a black record sleeve. The shard is nickel, polished with fine grooves (roughness 0.14, anisotropic 0.7 along the grooves). Set 9 mm behind its front face, a curved sector of the nickel stamper that pressed the record: a mirror finely grooved. The frame must read as a $1,000-plus collectible and the shard as a mirror of grooves.

Frame: 1800 x 1200 px, 3:2.

## Fixed (never yours to change)
- The object's geometry and dimensions, and what is inside it (its shape, size and position).
- The acrylic's optics: polished cast acrylic, IOR 1.49; its tint absorption comes from the maker's measured transmission
  chart (thick clear acrylic is very slightly cyan; the tints are thin strata only).
- Air voids are real air: they read silver at their rims by total internal reflection. Do not ask for them to be
  "clearer" or "softer"; ask for light that shows them.
- The renderer: Blender Cycles path tracing, caustics on, denoised.

## Settings you may change (units: mm, W for area lights, degrees)
- Camera: position (-330, -760, 190), target (0, 0, 95), lens 60 mm (35 to 135), f-stop off (off, or 2.8 to 22), exposure 0 EV (-2 to +2).
- Set: the seamless cove's colour #A9A7A3 (any neutral, sRGB hex), roughness 0.6, matte with no specular (0.2 to 0.9).
- Lights (area unless marked; position -> aims at the target):
  - overhead (-60, 260, 900), 1000 x 600, 30 W
  - key (-560, -420, 380), 320 x 320, 18 W
  - front (-80, -760, 560), 1600 x 160, 10 W (what the mirror shard reflects)
  - the shard leans back 10 degrees in its pocket (fixed: the pocket is cut so)
  - rimL (-420, 420, 260), 90 x 900, 28 W; rimR (440, 380, 260), 90 x 900, 32 W
  - glint: a spot at (420, -460, 300) on the shard, 40 W, 8 mm source, 6 degree cone
- You may add a light, a card (a white or black flag) or a prop by kind "asset", saying where, how big, how bright.
