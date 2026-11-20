"""The off-colour study's table: per tint, Hemisphere's tint shell and Core's ball, each through its own mask (eroded
2 px), the mean L*, C*, h of the whole body and of its pixels with chroma over 40, and the gap (ball minus dome)."""
import sys, os, numpy as np
from PIL import Image
from scipy.ndimage import binary_erosion
S = os.path.dirname(os.path.abspath(__file__))
NAMES = {'red': 'Ember', 'orange': 'Dust', 'amber': 'Acid', 'green': 'Poison', 'blue': 'Ice', 'violet': 'Haze', 'ice': 'Fog', 'black': 'Smoke'}
def lab(a):
    a = a / 255.0; l = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = l @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)
def body(n):
    im = np.asarray(Image.open(f'{S}/{n}.png').convert('RGB')).astype(float)
    mk = np.asarray(Image.open(f'{S}/{n}-mask.png').convert('L')) > 128
    mk = binary_erosion(mk, iterations=2); L = lab(im)
    C = np.hypot(L[..., 1], L[..., 2])
    out = []
    for m in (mk, mk & (C > 40)):
        if m.sum() < 50: out.append(None); continue
        l, a, b = (L[..., i][m].mean() for i in range(3)); out.append((l, np.hypot(a, b), np.degrees(np.arctan2(b, a)) % 360, int(m.sum())))
    return out
pre = sys.argv[1] if len(sys.argv) > 1 else ''
f = lambda v: '   -  ' if v is None else f'{v[0]:5.1f} {v[1]:5.1f} {v[2]:5.0f}'
print(f'{"Tint":7s} | {"Hemisphere body L C h":20s} | {"Core body L C h":20s} | gap L | {"Hemi C>40 L C h":18s} | {"Core C>40 L C h":18s} | gap L')
for k, nm in NAMES.items():
    try:
        d, o = body(f'{pre}dome-{k}'), body(f'{pre}orb-{k}')
    except FileNotFoundError:
        continue
    g0 = o[0][0] - d[0][0]; g1 = (o[1][0] - d[1][0]) if d[1] and o[1] else None
    print(f'{nm:7s} | {f(d[0]):20s} | {f(o[0]):20s} | {g0:+5.1f} | {f(d[1]):18s} | {f(o[1]):18s} | ' + ('  -  ' if g1 is None else f'{g1:+5.1f}'))
