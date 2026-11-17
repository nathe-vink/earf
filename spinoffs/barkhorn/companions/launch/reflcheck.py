"""Reflection audit (2026-11-17, the coordinator: audit the reflections, not only what is in frame).
reflcheck.py WITH.png WITHOUT.png OUT_DIFF.png
WITH is a frame rendered as usual, WITHOUT the same frame with STUDIO_NOGLOSS=1 (the studio lights hidden from glossy
rays). Their difference is every studio reflection in the picture. Prints the share of pixels the reflections lift by
more than 8 and 24 levels (of 255, display-referred), the largest lift, and the size of the largest connected patch
over 24 (a disc or a bar is a patch; an even sheen is not). Writes the difference, x4, as an image."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage
a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
b = np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(float)
d = (a - b).max(axis=2).clip(0, None)
d = ndimage.median_filter(d, 3)                     # render noise is per pixel; a reflection is a shape
lab, n = ndimage.label(d > 24)
big = max((int((lab == i).sum()) for i in range(1, n + 1)), default=0)
print(f"REFLCHECK lift>8 {100 * (d > 8).mean():.3f} %  lift>24 {100 * (d > 24).mean():.3f} %  max {d.max():.0f}  "
      f"largest patch>24 {big} px ({100 * big / d.size:.3f} %)")
Image.fromarray((d * 4).clip(0, 255).astype(np.uint8)).save(sys.argv[3])
