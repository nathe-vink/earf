# Shot card: Iron, product frame (the Core house set)

## What the frame is for
The edition's picture beside the product's own: Core, EARF's cordless table lamp (a 160 mm ball of water-clear cast
acrylic resting on a black anodised aluminium base, 120 across and 30 tall), here as the Iron edition: at the ball's
centre, standing upright in a dry pocket cut 0.5 mm larger all round, a 5 mm etched slice of the Gibeon iron meteorite
(a fine octahedrite: its Widmanstatten figure of interlocking kamacite bands, hairline taenite, dark plessite), about
62 x 44 mm, with a dark sawn rind. The ball magnifies it. Unlit here (the base's light ring is off). It must read as a
$4,000-plus object and as the same product as the lamp's own pictures.

Frame: 1600 x 2000 px, 4:5.

## Fixed (never yours to change)
- The object's geometry and dimensions, and what is inside it (its shape, size and position).
- The acrylic's optics: polished cast acrylic, IOR 1.49; its tint absorption comes from the maker's measured transmission
  chart (thick clear acrylic is very slightly cyan; the tints are thin strata only).
- Air voids are real air: they read silver at their rims by total internal reflection. Do not ask for them to be
  "clearer" or "softer"; ask for light that shows them.
- The renderer: Blender Cycles path tracing, caustics on, denoised.


## Settings you may change (units: mm unless marked, W for area lights, degrees)
- Camera: position (-160, -620, 168), target (0, 0, 148), lens 75 mm, f/5.6 focused on the slice at the ball's centre (0, 0, 142); exposure +0.15 EV.
  The ball's centre is at z 142; the marble's top at z 40.
- Set: a warm paper sweep #EAE4DA with a marble floor slab (a photographed CC0 marble, tinted toward #ECE7DF, its
  roughness x 0.6); a sky #D8D2C8, strength 0.35. View transform Khronos PBR Neutral, exposure +0.15 EV.
  This set is the house set for the product's own pictures; change its values only if a change is needed.
- Lights (area unless marked; azimuth 0 is in front of the object, +90 toward +x; the watts follow from the irradiance
  at the target):
  - key: 3000 x 500, azimuth -30, elevation 50, 2.6 m, 0.6 W/m2 at the target
  - fill: 2500 x 2000, azimuth 30, elevation 12, 3.0 m, 0.25 W/m2
  - bgwash: 3500 x 1000 at (0, -400, 3000) aimed at the sweep at (0, 2200, 0), 2.645 W/m2, #FFF4E8, unseen by
    camera and specular rays
  - back: 80 x 600 at (450, 150, 200) aimed at the object, 1.6 W/m2, unseen by the camera
  - flags: two matte black cards 400 x 700 at x = -420 and +420 (y 0, from the floor up), facing the ball
  - softbox: 900 x 500 at (-180, -1500, 260) aimed at the slice, 0.5 W/m2, #FFF8F0, unseen by the camera
  - lowcard: an area light 500 x 60 at (0, -300, 60) aimed at the base, 0.6 W, unseen by the camera
- You may add a light, a card (a white or black flag) or a prop by kind "asset", saying where, how big, how bright.
