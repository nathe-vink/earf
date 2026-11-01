# Shot card: Firn, detail macro (bright-field)

## What the frame is for
The detail frame for the Firn edition: close on a record weight (80 mm across, 36 mm tall) in clear cast acrylic under a
3 mm pale-blue top lamina, looking through its side and top into the columns of flat lens-shaped air voids, one at each
bond line, as glacier ice traps air. It must show what only lamination can make: voids exactly at the bond lines, crisp,
silver-rimmed, stacked.

Frame: 1800 x 1200 px, 3:2.

## Fixed (never yours to change)
- The object's geometry and dimensions, and what is inside it (its shape, size and position).
- The acrylic's optics: polished cast acrylic, IOR 1.49; its tint absorption comes from the maker's measured transmission
  chart (thick clear acrylic is very slightly cyan; the tints are thin strata only).
- Air voids are real air: they read silver at their rims by total internal reflection. Do not ask for them to be
  "clearer" or "softer"; ask for light that shows them.
- The renderer: Blender Cycles path tracing, caustics on, denoised.

## Settings you may change (units: mm, W for area lights, degrees)
- Camera: position (12, -200, 85), target (0, 5, 20), lens 65 mm (35 to 135), f/22 focused at 200 mm (off, or 2.8 to 22), exposure 0 EV (-2 to +2).
- Set: the seamless cove's colour #B2B0AC (any neutral, sRGB hex), roughness 0.8, matte with no specular (0.2 to 0.9).
- Lights (area unless marked; position -> aims at the target):
  - overhead (-40, 120, 520), 600 x 360, 4 W, #FFF4E6, beam spread 75 degrees
  - key (-460, -220, 220), 240 x 240, 1.5 W
  - wall: an area light 900 x 500 at (0, 500, 420) washing the cove behind at (0, 900, 520), 7 W
  - rimR (300, 240, 90), 60 x 400, 14 W
  - flag: a matte black card #0A0A0A 600 x 300 at (40, -520, 110 to 410), facing the object
  - flagL: a matte black card #111111 160 x 300 at (-320, 110, 0 to 300), square to the object
  - lowfill: an area light 300 x 80 at (0, -260, 30) aimed at the object, 2.0 W, unseen by the camera, #E8F0FF
  - glint: a spot at (260, -300, 160), 40 W, 5 mm source, 10 degree cone
  - whitecard: a matte white card #E6E6E6, 160 x 50, standing on the record behind the object at y 110
- You may add a light, a card (a white or black flag) or a prop by kind "asset", saying where, how big, how bright.
