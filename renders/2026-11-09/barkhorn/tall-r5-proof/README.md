# Tall, the re-fitted rig (0c6acd5d + the back-edge card trim): proof, Haze, 1000 x 1250, 48 samples

- `haze-tall-6deg-half.png`: the tall on 0c6acd5d (the corrected cast's one floor card, the speaker turned 6 deg). No
  card in frame (0cbf23a5's wedges are gone). Its mask pass found 3 px of the back-edge card's right end past the
  cabinet's back-right corner (716-717, 1003-1004); the trim (8 mm off that end, the tall only) takes it to 0 px.
- `haze-tall-6deg-half.mask.png`: part ids; 255 is studio equipment (flags and bounce cards, drawn visible to the camera).
- `bottom-edge-card-*.png`: the bottom edge before and after the trim, seam 4 and 4 (bottom_edge_sheet.seam); 33 px
  differ, the card's end.

Audits on the rig with the trim: hidden 22 objects, 0 in frame (hiddencast, corrected cast); cardcast: only the
back-edge card's rectangle, 0.48 %, behind the speaker; equipment in frame 0 px (the mask pass).
The pod at 6 deg: x 601-622 against the waveguide's right edge at x 600, 22 px past the mouth.
