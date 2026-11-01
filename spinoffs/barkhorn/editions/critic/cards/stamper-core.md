# Shot card: Stamper, product frame (the house set)

## What the frame is for
The edition's hero: Bedrock, a record stand (300 x 80 x 72 mm) in water-clear cast acrylic with a 7 mm slot along its top, holding a black board record sleeve (314 mm square). Set 9 mm behind its front
face, a curved sector of the nickel stamper that pressed the record (about 100 x 46 mm, its grooves a mirror, leaning
back 10 degrees in its pocket). On a marble floor in the house set. It must read as a $1,000-plus collectible, and the
shard as a polished mirror of grooves inside clear acrylic.

Frame: 1800 x 1200 px, 3:2.

## Fixed (never yours to change)
- The object's geometry and dimensions, and what is inside it (its shape, size and position).
- The acrylic's optics: polished cast acrylic, IOR 1.49; its tint absorption comes from the maker's measured transmission
  chart (thick clear acrylic is very slightly cyan; the tints are thin strata only).
- Air voids are real air: they read silver at their rims by total internal reflection. Do not ask for them to be
  "clearer" or "softer"; ask for light that shows them.
- The renderer: Blender Cycles path tracing, caustics on, denoised.


## Settings you may change (units: mm unless marked, W for area lights, degrees)
- Camera: position (-430, -760, 660), target (0, -10, 100), lens 70 mm, no depth of field; exposure +0.15 EV. The marble's
  top is at z 40; the stand stands on it.
- Set: a warm paper sweep #EAE4DA with a marble floor slab (a photographed CC0 marble, tinted toward #ECE7DF, its
  roughness x 1.1); a sky #D8D2C8, strength 0.35. View transform Khronos PBR Neutral, exposure +0.15 EV.
  This set is the house set for the product's own pictures; change its values only if a change is needed.
- Lights (area unless marked; azimuth 0 is in front of the object, +90 toward +x; the watts follow from the irradiance
  at the target):
  - key: 3000 x 500, azimuth -30, elevation 42, 2.6 m, 0.6 W/m2 at the target
  - fill: 2500 x 2000, azimuth 30, elevation 42, 3.0 m, 0.25 W/m2
  - bgwash: 3500 x 1000 at (0, -400, 3000) aimed at the sweep at (0, 2200, 250), 2.645 W/m2, #FFFFFF, unseen by
    camera and specular rays
  - back: 80 x 600 at (450, 150, 110) aimed at the object, 3.5 W/m2, unseen by the camera
  - strip: 700 x 30 at (430, -900, 130) aimed at the shard (0, -31, 75), 0.35 W/m2, unseen by the camera (the shard
    mirrors it), with a matte black flag 1000 x 450 behind it at (430, -1060, 150)
  - flags: matte black cards 600 x 300 at (-700, -200, 190) and (700, -200, 190), turned to the stand; all flags
    unseen by the camera
- You may add a light, a card (a white or black flag) or a prop by kind "asset", saying where, how big, how bright.
