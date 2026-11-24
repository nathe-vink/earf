"""The big left panel's blotch energy, as the coordinator measures it (24 Nov 19:47): L* band-passed 2-14 px (Gaussian
blur at 2 px less blur at 14 px), RMS over the panel left of the plate (x 40-640, y 100-1500 of the 1600 x 1600 frame).
    python3 blotch.py NAME=PNG[@X0,Y0] ...     (@X0,Y0: where a crop sits in the full frame)"""
import sys, numpy as np
from PIL import Image, ImageFilter
def L(a):
    a = a / 255; lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    Y = lin @ np.array([0.2126, 0.7152, 0.0722]); f = np.where(Y > 216 / 24389, np.cbrt(Y), (24389 / 27 * Y + 16) / 116)
    return 116 * f - 16
def g(x, r):
    return np.asarray(Image.fromarray(np.clip(x * 2.55, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(float) / 2.55
for arg in sys.argv[1:]:
    name, rest = arg.split('=')
    png, off = (rest.split('@') + [None])[:2]
    ox, oy = (int(v) for v in off.split(',')) if off else (0, 0)
    l = L(np.asarray(Image.open(png).convert('RGB')).astype(float))
    d = g(l, 2) - g(l, 14)
    x0, x1, y0, y1 = 40 - ox, 640 - ox, 100 - oy, 1500 - oy
    r = d[max(y0, 20):y1, max(x0, 20):x1]
    print(f'{name}: left panel band-pass 2-14 px L* RMS {np.sqrt((r ** 2).mean()):.2f}  (mean L* {l[max(y0,0):y1, max(x0,0):x1].mean():.1f})')
