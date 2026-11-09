Does the COB's light reach the Hemisphere's opal liner in the night pictures' geometry? (2026-11-09 23:40 UTC)

The lamp alone (night_room._append_lamp, honest_cob 0.011 at the bore's top, the CAD's aluminium reflector), black
world, no room; 400 x 300, 256 samples, caustics on, no clamp (spinoffs/barkhorn/night-pictures/lamp_alone.py). The
dome's face is the pixels over 0.5 in the liner-on frame; means in linear light:

  liner-on  (the kit's opal-lit emission)        4.751
  liner-off (the COB the only light)             0.126   (2.6 % of liner-on; speckled: specular paths only)
  liner-off, the reflector matte black           0.025   (0.5 %)

In the room at 3840 (the same dome window): the final 4.738, the as-drawn variant 0.075 (1.6 %).

So some COB light does reach the opal in this geometry, about 2-3 % of the kit's liner glow. About four fifths of it
arrives by the aluminium reflector's specular paths, the rest by another path within the fitting. With the grade's
exposure (+4.6 EV), 1.6 % still renders the as-drawn dome pale (luma about 208 against 247), not dark. The PNGs are
each normalized to its own p99, for the shape of the light, not its level.
