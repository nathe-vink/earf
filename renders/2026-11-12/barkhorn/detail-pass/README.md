# Tropos detail pass, Ice (2026-11-12)

The coordinator's items A to H (08:59). The notes are in `spinoffs/barkhorn/make/detail-pass.md`, the prices in
`spinoffs/barkhorn/rfq/tropos/PARTS-FINAL-DESIGN.md` ("Detail pass").

| file | what |
|---|---|
| `ice-before-after.png` | front three-quarter (top) and the full back with the amplifier (bottom), before left and after right, each 1000 x 1250 |
| `crop-ports.png` | the ports and the IR receiver, at 2x |
| `crop-horn-back.png` | the back of the horn, at 2x |
| `crop-feet.png` | the feet and the back's lower screws, at 2x |
| `ice-*-after.shot.json` | the shots as rendered |

**How the pictures were made:**
- Both frames are the site's own shots (`shots.site('front-off-tall', 'ice')` and `site('back', 'ice')`), at 96 samples.
- The before and after shot files are identical. Only the model changed: the engine files (`studio/products/barkhorn-cloud.json`,
  `barkhorn-variants.json`) rebuilt from the CAD.
- The crops are the same after shots at scale 2, cropped with `--crop`.

**What to look for:**
- **The ports:** round rings with one polished chamfer, bonded, no screws.
- **The feet:** black, stem, jam nut and pad.
- **The back:** 24 countersunk heads, flush and evenly spaced.
- **The rating:** grey engraving in the black band under the amplifier's plate.
- **The leads:** in black braid.
- **The IR receiver:**
  - It sits low between the ports, in a cup in the lining's own colour, inside a pocket in the bottom batt.
  - Its lead is sleeved in the same colour, in a channel and a groove in the batt.
  - A black cup was tried first. Against the white batt it read as a black mark, so it was changed.
- **The HF lead:** up the hollow rear post, then out of sight behind the driver's motor in the pod.
