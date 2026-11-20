# Tropos: the dimension drawing (2026-11-20)

The coordinator, 20 Nov: "A dimension drawing of Tropos from the CAD, line only, inches and millimeters, SVG plus a PNG
preview: front and side ... Draw only what is designed."

- `tropos-dims.svg` (line only, the text as outlines) and `tropos-dims.png` (2200 x 1700, the preview).
- Made by `spinoffs/barkhorn/drawing/tropos_dims.py` from the render models the site's pictures are made from:
  - the Cloud's parts (`out-cloud/render/barkhorn-cloud.glb`), less the parts the approved look hides (the cloth disc,
    the woofer ring, the Cloud's own posts);
  - the variants' parts it adds (`variants/out/render/barkhorn-variants.glb`: the Strata posts and collars, the
    caldera, the horn lead).
  - Each part is placed by its own node. All 112 Cloud parts were checked against the model's box list, within 0.6 mm.
- **How the lines are found:** every visible part's triangles are painted far to near into a part map at 0.5 mm a
  pixel, one map per view. Each part's visible outline is traced from that map. So a line falls only where one part
  meets another, or meets the air.
- **Left out:** the inside parts no view can see (linings, braces, the woofer's basket and motor, the amplifier module,
  the leads) and flat prints.

## The figures

| | mm | in |
|---|---|---|
| height, the feet's pads to the horn's top | 1295.1 | 51.0 |
| width, the cabinet (the horn 556 inside it) | 560.0 | 22.0 |
| depth overall, the caldera's front ring to the amplifier plate's hardware | 441.5 | 17.4 |
| depth, the cabinet | 420.0 | 16.5 |
| the cabinet's top above the floor | 892.0 | 35.1 |

**The depth is 441.5 mm, not the 428 the site prints.** The README's 428 (2026-11-09) was measured on the Cloud model
alone, from the horn's front at y −0.1 to the plate's hardware at 427.5. The approved look adds the caldera: three
terraced rings of the cabinet's own tinted resin around the woofer (`caldera-1` to `-3`). Its front ring stands
14.0 mm proud of the cabinet's front edge, at y −14.0. The site's depth is for the coordinator to settle.
