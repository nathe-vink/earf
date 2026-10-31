# Shot card: Iron, detail macro

## What the frame is for
The detail frame: the meteorite slice's etched pattern through the ball's front, magnified by the ball, the thin silver rim of its dry pocket around it.

Frame: 1800 x 1200 px, 3:2.

## Fixed (never yours to change)
- The object's geometry and dimensions, and what is inside it (its shape, size and position).
- The acrylic's optics: polished cast acrylic, IOR 1.49; its tint absorption comes from the maker's measured transmission
  chart (thick clear acrylic is very slightly cyan; the tints are thin strata only).
- Air voids are real air: they read silver at their rims by total internal reflection. Do not ask for them to be
  "clearer" or "softer"; ask for light that shows them.
- The renderer: Blender Cycles path tracing, caustics on, denoised.

## Settings you may change (units: mm, W for area lights, degrees)
- Camera: position (10, -330, zc+30), target (0, 0, zc), lens 100 mm (35 to 135), f-stop 11 (focus 332) (off, or 2.8 to 22), exposure 0 EV (-2 to +2).
- Set: the seamless cove's colour #262628 (any neutral, sRGB hex), roughness 0.45, matte with no specular (0.2 to 0.9).
- Lights (area unless marked; position -> aims at the target):
  - overhead, a disc 600 across at (0, 520, 560), 18 W
  - key, a disc 200 across at (-620, -60, zc+260), 14 W
  - front (0, -900, zc+60), 500 x 260, 5 W
  - rimR (300, 300, zc+80), 70 x 500, 8 W
  - glint: a spot at (220, -260, zc+260), 50 W
- You may add a light, a card (a white or black flag) or a prop by kind "asset", saying where, how big, how bright.
