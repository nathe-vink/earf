"""L* and chroma C*ab (CIELAB, D65), means of boxes given as fractions of the frame: lstar.py PNG name:x0,y0,x1,y1 ..."""
import sys, numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float) / 255
lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
XYZ = lin @ M.T / np.array([0.95047, 1.0, 1.08883])
f = lambda t: np.where(t > 216 / 24389, np.cbrt(t), (24389 / 27 * t + 16) / 116)
fx, fy, fz = f(XYZ[..., 0]), f(XYZ[..., 1]), f(XYZ[..., 2])
C = np.hypot(500 * (fx - fy), 200 * (fy - fz))
Y = lin @ np.array([0.2126, 0.7152, 0.0722])
L = np.where(Y > 216 / 24389, 116 * np.cbrt(Y) - 16, Y * 24389 / 27)
H, W = L.shape
for arg in sys.argv[2:]:
    n, b = arg.split(':'); x0, y0, x1, y1 = map(float, b.split(','))
    r = L[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
    c = C[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
    print(f'{n:14s} L* {r.mean():5.1f}  C* {c.mean():5.1f}  (L* p5 {np.percentile(r, 5):5.1f}, p95 {np.percentile(r, 95):5.1f}, max {r.max():5.1f})')
