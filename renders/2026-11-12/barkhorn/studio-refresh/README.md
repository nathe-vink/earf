# Studio refresh with the cleaned Tropos (2026-11-12/13)

The product pages' sixteen pictures, re-rendered after the detail pass (fd8aa47e, passed 2026-11-12).

**The frames:**
- The eight fronts are `site-front-off-tall-<tint>.png`, 1000 x 1250 at 96 samples.
- The eight horn-backs are `horn-back-<tint>.png`, 1200 x 900 at 128 samples.
- `contact-sheet.png` shows all sixteen.

**What changed:**
- **The same shot files as the passed set:**
  `renders/2026-11-04/barkhorn/rollout/A-polished-tallr7/site-front-off-tall-*.shot.json` and
  `A-polished-p2-p2b/horn-back-*.shot.json`. The camera, light, set and exposure are unchanged.
- **The model:** the shots load `studio/products/barkhorn-cloud.json` and `barkhorn-variants.json`. These are the
  engine files the cleaned asset (`spinoffs/barkhorn/asset/tropos-strata.blend`) was built from, from the same CAD, so
  every frame shows the detail pass.
- **What to look for:**
  - The round, bonded port rings, with no screws.
  - Black feet.
  - The flush black back screws.
  - The IR eye, a small pale square in the bottom batt.
  - Braided leads, and no loose lead behind the horn.

**The masks:**
- Each frame was rendered with `--masks`, so its `.mask.png`, `.mask.json` and `.equipment.txt` are beside it.
- All sixteen read **hidden 0 px, equipment 0 px**.
