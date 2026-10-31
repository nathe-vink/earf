# Shot card: Stamper, detail macro

## What the frame is for
The detail frame: the stamper shard close, its grooves, the mirror's light band, through the acrylic's front face.

Frame: 1800 x 1200 px, 3:2.

## Fixed (never yours to change)
- The object's geometry and dimensions, and what is inside it (its shape, size and position).
- The acrylic's optics: polished cast acrylic, IOR 1.49; its tint absorption comes from the maker's measured transmission
  chart (thick clear acrylic is very slightly cyan; the tints are thin strata only).
- Air voids are real air: they read silver at their rims by total internal reflection. Do not ask for them to be
  "clearer" or "softer"; ask for light that shows them.
- The renderer: Blender Cycles path tracing, caustics on, denoised.

## Settings you may change (units: mm, W for area lights, degrees)
- Camera: position (-60, -380, 66), target (0, -31, 34), lens 100 mm (35 to 135), f-stop 11 (off, or 2.8 to 22), exposure 0 EV (-2 to +2).
- Set: the seamless cove's colour #19191B (any neutral, sRGB hex), roughness 0.4, matte with no specular (0.2 to 0.9).
- Lights (area unless marked; position -> aims at the target):
  - overhead (0, 160, 480), 500 x 300, 16 W
  - key (-280, -300, 180), 180 x 180, 10 W
  - front (60, -420, 470), 700 x 140, 9 W (the mirror's light band)
  - rimR (260, 120, 160), 60 x 400, 6 W
  - glint: a spot at (200, -330, 120), 70 W
- You may add a light, a card (a white or black flag) or a prop by kind "asset", saying where, how big, how bright.
