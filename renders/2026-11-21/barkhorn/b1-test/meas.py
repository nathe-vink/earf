"""B1: live, fixed, fixed-3 and fixed-4 (fixed-2 in git history), L* / C* means in boxes of the 1600 x 900 frame.
    python3 meas.py   ->  meas.md"""
import numpy as np
from PIL import Image
def lab(a):
    a = a / 255; lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    X = lin @ M.T / np.array([0.95047, 1, 1.08883]); f = np.where(X > 216 / 24389, np.cbrt(X), (24389 / 27 * X + 16) / 116)
    return 116 * f[..., 1] - 16, np.hypot(500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2]))
BOX = {'near horn, bell': (1040, 40, 1320, 240), 'near cabinet, front': (1060, 260, 1300, 560),
       'far cabinet': (450, 240, 590, 620), 'hemispheres': (100, 220, 440, 460), 'cores': (60, 620, 350, 720),
       'drinks': (340, 760, 620, 880), 'deck and Mantle': (860, 720, 1300, 840), 'record wall': (620, 200, 980, 600),
       'bar top': (700, 820, 1000, 900), 'dark left wall': (0, 0, 300, 200), 'whole frame': (0, 0, 1600, 900)}
im = {v: np.asarray(Image.open(v + '.png').convert('RGB')).astype(float) for v in ('live', 'fixed', 'fixed3', 'fixed4')}
lc = {v: lab(a) for v, a in im.items()}
rows = ['| box | live | fixed | fixed-3 | fixed-4 |', '|---|---|---|---|---|']
for n, (x0, y0, x1, y1) in BOX.items():
    s = np.s_[y0:y1, x0:x1]
    c = [f'{lc[v][0][s].mean():5.1f} / {lc[v][1][s].mean():5.1f}' for v in ('live', 'fixed', 'fixed3', 'fixed4')]
    rows.append(f'| {n} | {c[0]} | {c[1]} | {c[2]} | {c[3]} |')
open('meas.md', 'w').write('\n'.join(rows) + '\n'); print('\n'.join(rows))
