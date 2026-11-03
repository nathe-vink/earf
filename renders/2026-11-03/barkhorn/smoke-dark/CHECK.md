# Smoke on horn A: the blind four-test check (2026-11-03)

Both frames are 1200 x 1500 at 48 samples. Both use horn A (built from r33-speaker-horn 4ec3bc96), Smoke 2074 with a
black lining, settled on its M8 feet, with the black flag and side cards. The fills are off: skyfill 0, bounce 0,
kicker 0.3, kicker_r 0. A fire backlight lights the cabinet from behind. Each frame was judged by a fresh blind agent
that was told only the owner's four tests.

| frame | glass | see-through | grounded | no light down | smooth horn |
|---|---|---|---|---|---|
| smoke-hornA-surfaceglass | the tint on the faces (sqrt of the 20 mm TT a face), shadow rays through the walls; backlight 20 | PASS | PASS | PASS | PASS |
| smoke-hornA-weldvolume | the asset's volume, its panels welded so they close, shadow rays through the walls; backlight 40 | FAIL ("a near-black opaque box") | PASS | PASS | PASS |

The welded volume is how the speaker lane's own renders treat the sheet. In that material, Smoke 2074 behind a black
lining reads as nearly opaque, even with the fire directly behind it.
