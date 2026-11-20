"""L* (CIELAB, D65) mean of boxes given as fractions of the frame: lstar.py PNG name:x0,y0,x1,y1 ..."""
import sys, numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float) / 255
lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
Y = lin @ np.array([0.2126, 0.7152, 0.0722])
L = np.where(Y > 216 / 24389, 116 * np.cbrt(Y) - 16, Y * 24389 / 27)
H, W = L.shape
for arg in sys.argv[2:]:
    n, b = arg.split(':'); x0, y0, x1, y1 = map(float, b.split(','))
    r = L[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
    print(f'{n:14s} L* {r.mean():5.1f}  (p5 {np.percentile(r, 5):5.1f}, p95 {np.percentile(r, 95):5.1f}, max {r.max():5.1f})')
