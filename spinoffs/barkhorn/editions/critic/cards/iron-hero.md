# Shot card: Iron, studio hero

## What the frame is for
The edition's hero: a 160 mm ball of water-clear cast acrylic resting on a black anodised base with a warm LED ring; at its centre stands a 5 mm etched slice of an iron meteorite (Widmanstatten pattern), about 62 x 44 mm, seen magnified through the ball. The frame must read as a $4,000 to $7,000 object: the meteorite, the ball's clarity, the base.

Frame: 1800 x 1200 px, 3:2.

## Fixed (never yours to change)
- The object's geometry and dimensions, and what is inside it (its shape, size and position).
- The acrylic's optics: polished cast acrylic, IOR 1.49; its tint absorption comes from the maker's measured transmission
  chart (thick clear acrylic is very slightly cyan; the tints are thin strata only).
- Air voids are real air: they read silver at their rims by total internal reflection. Do not ask for them to be
  "clearer" or "softer"; ask for light that shows them.
- The renderer: Blender Cycles path tracing, caustics on, denoised.

## Settings you may change (units: mm, W for area lights, degrees)
- Camera: position (40, -900, zc+150), target (0, 0, zc-22) where zc = 94.0 is the ball's centre height, lens 85 mm (35 to 135), f-stop off (off, or 2.8 to 22), exposure 0 EV (-2 to +2).
- Set: the seamless cove's colour #262628 (any neutral, sRGB hex), roughness 0.45, matte with no specular (0.2 to 0.9).
- Lights (area unless marked; position -> aims at the target):
  - overhead, a disc 700 across at (-80, 520, 700), 18 W
  - key (-700, -220, 460), 300 x 300, 18 W
  - front (0, -1300, zc+520), 700 x 300, 12 W
  - glow (0, 330, 40) aimed at the cove at (0, 640, 110), 220 x 110, 3 W
  - flag: a strip light 700 x 80 at (0, -420, 25), 3 W
  - rimL (-360, 380, 240), 80 x 800, 12 W; rimR (380, 360, 260), 80 x 800, 14 W, #E6EEFF
  - glint: a spot at (460, -300, 520), 120 W, 8 mm source, 14 degree cone
  - the base's LED ring: emission 2.5, #FFC890
- You may add a light, a card (a white or black flag) or a prop by kind "asset", saying where, how big, how bright.
