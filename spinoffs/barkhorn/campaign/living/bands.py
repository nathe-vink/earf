"""Join two horizontal bands of one frame rendered with --crop (top 0..t1, bottom b0..1), blended linearly over their
overlap; prints the mean difference there (noise if the bands agree).

    python3 bands.py TOP.png BOTTOM.png HEIGHT OUT.png
"""
import sys
import numpy as np
from PIL import Image

top = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
bot = np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(float)
H = int(sys.argv[3]); W = top.shape[1]
b0 = H - bot.shape[0]                                  # the bottom band's first row (Blender rounds the border its own way)
ov = top.shape[0] - b0
assert ov > 8, (top.shape, bot.shape, H)
out = np.zeros((H, W, 3))
out[:b0] = top[:b0]; out[top.shape[0]:] = bot[ov:]
w = np.linspace(0, 1, ov)[:, None, None]
out[b0:top.shape[0]] = top[b0:] * (1 - w) + bot[:ov] * w
d = np.abs(top[b0:] - bot[:ov]).mean()
Image.fromarray(np.clip(out.round(), 0, 255).astype(np.uint8)).save(sys.argv[4], optimize=True)
print(f'rows {b0}..{top.shape[0]} overlap {ov}, mean difference {d:.2f}/255 -> {sys.argv[4]}')
