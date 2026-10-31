# Shot card: Firn, studio hero (bright-field)

## What the frame is for
The edition's hero for a launch page and a collector's catalogue: a record weight (80 mm across, 36 mm tall) in clear cast acrylic under a 3 mm pale-blue top lamina, sitting on a black LP (glossy black vinyl; its 100 mm centre label dark satin #2B2B2D, lit by the light the weight gathers through its base). Inside, at each bond line, flat lens-shaped air voids stacked in columns, like the air trapped in glacier ice. The frame must make the voids read as air sealed inside a solid, and the object as a $600 to $900 collectible, not a paperweight or a candle holder.

Frame: 1800 x 1200 px, 3:2.

## Fixed (never yours to change)
- The object's geometry and dimensions, and what is inside it (its shape, size and position).
- The acrylic's optics: polished cast acrylic, IOR 1.49; its tint absorption comes from the maker's measured transmission
  chart (thick clear acrylic is very slightly cyan; the tints are thin strata only).
- Air voids are real air: they read silver at their rims by total internal reflection. Do not ask for them to be
  "clearer" or "softer"; ask for light that shows them.
- The renderer: Blender Cycles path tracing, caustics on, denoised.

## Settings you may change (units: mm, W for area lights, degrees)
- Camera: position (40, -420, 150), target (0, 0, 18), lens 100 mm (35 to 135), f-stop off (off, or 2.8 to 22), exposure 0 EV (-2 to +2).
- Set: the seamless cove's colour #B9B7B3 (any neutral, sRGB hex), roughness 0.8, matte with no specular (0.2 to 0.9).
- Lights (area unless marked; position -> aims at the target):
  - overhead (-40, 120, 520), 600 x 360, 9 W, #FFF4E6, beam spread 75 degrees
  - key (-460, -220, 220), 240 x 240, 6 W
  - wall: an area light 900 x 500 at (0, 500, 200) washing the cove behind at (0, 900, 260), 10 W
  - rimR (300, 240, 90), 60 x 400, 3 W, #E8F0FF
  - glint: a spot at (260, -300, 160), 40 W, 5 mm source, 10 degree cone
- You may add a light, a card (a white or black flag) or a prop by kind "asset", saying where, how big, how bright.
