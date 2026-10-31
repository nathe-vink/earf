# Shot card: Firn, detail macro

## What the frame is for
The detail frame: close on the record weight's top and side, looking through the pale-blue top lamina into the stacked columns of lens-shaped air voids. It must show what only lamination can make: voids exactly at the bond lines, crisp, silver-rimmed, stacked.

Frame: 1800 x 1200 px, 3:2.

## Fixed (never yours to change)
- The object's geometry and dimensions, and what is inside it (its shape, size and position).
- The acrylic's optics: polished cast acrylic, IOR 1.49; its tint absorption comes from the maker's measured transmission
  chart (thick clear acrylic is very slightly cyan; the tints are thin strata only).
- Air voids are real air: they read silver at their rims by total internal reflection. Do not ask for them to be
  "clearer" or "softer"; ask for light that shows them.
- The renderer: Blender Cycles path tracing, caustics on, denoised.

## Settings you may change (units: mm, W for area lights, degrees)
- Camera: position (10, -190, 120), target (0, 0, 22), lens 100 mm (35 to 135), f-stop 11 (off, or 2.8 to 22), exposure 0 EV (-2 to +2).
- Set: the seamless cove's colour #0B0B0C (any neutral, sRGB hex), roughness 0.75, matte with no specular (0.2 to 0.9).
- Lights (area unless marked; position -> aims at the target):
  - overhead (0, 120, 420), 500 x 300, 14 W, beam spread 40 degrees
  - back (40, 260, 30), 300 x 90, 7 W, #EAF2FF
  - key (-260, -160, 200), 140 x 140, 5 W
  - glint: a spot at (300, -120, 300), 30 W, 5 mm source, 10 degree cone
- You may add a light, a card (a white or black flag) or a prop by kind "asset", saying where, how big, how bright.
