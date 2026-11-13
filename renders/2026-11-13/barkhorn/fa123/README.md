# Tropos on the FA123 (2026-11-13): the pictures

The coordinator's FA123 batch (13 Nov 19:59; Hypex not written to for now): the asset and engine files on the published
data, the front proved unchanged, the eight backs and "The amplifier" re-rendered.

**The package.** `spinoffs/barkhorn/out-cloud` built from `product.py` at c1af6d69 (b98c99dd): the FA123's plate 360 x
120 with its print (from a retailer's square-on photograph of the FA123: the FA122's print, its top block 22.5 higher,
the marks and mains about 23 lower, the name and badge about 25 lower, the module's 20 screws measured), the
compartment 125 x 75 x 365 inside (45 deeper, downward), the rating engraved 45 lower. The plate's ten mount holes
are a PLACEHOLDER (five a side, 5 in from the edges, evenly spaced; the photograph agrees). The asset
`spinoffs/barkhorn/asset/tropos-strata.blend` rebuilt from it (b597165b). The bridged load stays OPEN (`make/fa123.md`).

## The front is unchanged

`front-detail.png` and `front-fa123.png`: Ice's site front (the passed `site-front-off-tall-ice.shot.json`, the same
camera, light and seed), 400 x 500 at 64 samples, from the detail-pass package (rebuilt from 3896c7e9) and from the
FA123's. `front-diff.png`: the two and their difference, 8 x amplified.

- Mean difference **0.12** of 255; max **116**; 633 pixels (0.3 %) differ by more than 8.
- Every one of them is inside the cabinet, seen through the clear wall: 193 in the side grip's window, where the
  back's lining and the compartment behind it show through (the compartment is 45 longer and the back's lower batt
  shorter by as much), the rest a sparse speckle over the interior where the changed geometry moves the path tracer's
  samples. The outside (the shell, the horn, the posts, the feet, the woofer and its ring) is the same.
