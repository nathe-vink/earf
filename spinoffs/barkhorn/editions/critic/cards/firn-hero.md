# Shot card: Firn, studio hero

## What the frame is for
The edition's hero for a launch page and a collector's catalogue: a record weight (80 mm across, 36 mm tall) in clear cast acrylic under a 3 mm pale-blue top lamina, sitting on a black LP (glossy black vinyl, roughness 0.16; its 100 mm centre label is dark, #2B2B2D, satin, and is lit by the light the weight gathers and drops through its base). Inside, at each bond line, flat lens-shaped air voids stacked in columns, like the air trapped in glacier ice. The frame must make the voids read as air sealed inside a solid, and the object as a $600 to $900 collectible, not a paperweight or a candle holder.

Frame: 1800 x 1200 px, 3:2.

## Fixed (never yours to change)
- The object's geometry and dimensions, and what is inside it (its shape, size and position).
- The acrylic's optics: polished cast acrylic, IOR 1.49; its tint absorption comes from the maker's measured transmission
  chart (thick clear acrylic is very slightly cyan; the tints are thin strata only).
- Air voids are real air: they read silver at their rims by total internal reflection. Do not ask for them to be
  "clearer" or "softer"; ask for light that shows them.
- The renderer: Blender Cycles path tracing, caustics on, denoised.

## Settings you may change (units: mm, W for area lights, degrees)
- Camera: position (60, -470, 220), target (0, 0, 14), lens 85 mm (35 to 135), f-stop off (off, or 2.8 to 22), exposure 0 EV (-2 to +2).
- Set: the seamless cove's colour #0B0B0C (any neutral, sRGB hex), roughness 0.75, matte with no specular (0.2 to 0.9).
- Lights (area unless marked; position -> aims at the target):
  - overhead (-60, 160, 620), 700 x 420, 11 W, #FFF4E6, beam spread 75 degrees
  - key (-420, -260, 300), 220 x 220, 2 W
  - rimL (-260, 300, 140), 60 x 520, 3 W; rimR (280, 280, 160), 60 x 520, 2 W, #E8F0FF
  - glint: a spot at (300, -260, 180), 60 W, 6 mm source, 12 degree cone
  - card: an area light 600 x 160 at (0, -520, 40), 4 W, white (a low front fill)
- You may add a light, a card (a white or black flag) or a prop by kind "asset", saying where, how big, how bright.
