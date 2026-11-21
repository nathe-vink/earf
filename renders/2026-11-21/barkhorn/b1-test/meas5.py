"""B1 fixed-5 crop test against fixed-4, in the same boxes as meas.py (full-frame pixels; the crops sit at x 960, y 0
(near, 576 x 630) and x 560, y 270 (wide, 1040 x 630) of the 1600 x 900 frame).   python3 meas5.py -> meas5.md"""
import numpy as np
from PIL import Image
def lab(a):
    a = a / 255; lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    X = lin @ M.T / np.array([0.95047, 1, 1.08883]); f = np.where(X > 216 / 24389, np.cbrt(X), (24389 / 27 * X + 16) / 116)
    return 116 * f[..., 1] - 16, np.hypot(500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2]))
F4 = lab(np.asarray(Image.open('fixed4.png').convert('RGB')).astype(float))
C = {'near': ((960, 0), lab(np.asarray(Image.open('fixed5-near.png').convert('RGB')).astype(float))),
     'wide': ((560, 270), lab(np.asarray(Image.open('fixed5-wide.png').convert('RGB')).astype(float)))}
BOX = [('near horn, bell', 'near', (1040, 40, 1320, 240)), ('near cabinet, front', 'near', (1060, 260, 1300, 560)),
       ('bay pillar, left', 'near', (1000, 150, 1040, 550)), ('bay pillar, right', 'near', (1320, 150, 1360, 550)),
       ('deck and Mantle', 'wide', (860, 720, 1300, 840)), ('bar top', 'wide', (700, 820, 1000, 900)),
       ('drinks, the right one (the crop starts at x 560)', 'wide', (560, 760, 620, 880)), ('record wall, lower', 'wide', (620, 300, 980, 600)),
       ('the wide crop, whole', 'wide', (560, 270, 1600, 900)), ('the near crop, whole', 'near', (960, 0, 1536, 630))]
rows = ['| box | fixed-4 L* / C* | fixed-5 L* / C* |', '|---|---|---|']
for n, c, (x0, y0, x1, y1) in BOX:
    (ox, oy), (L5, C5) = C[c]
    a = f'{F4[0][y0:y1, x0:x1].mean():5.1f} / {F4[1][y0:y1, x0:x1].mean():5.1f}'
    b = f'{L5[y0 - oy:y1 - oy, x0 - ox:x1 - ox].mean():5.1f} / {C5[y0 - oy:y1 - oy, x0 - ox:x1 - ox].mean():5.1f}'
    rows.append(f'| {n} | {a} | {b} |')
d = (C['wide'][1][0].mean() - F4[0][270:900, 560:1600].mean()) * (1040 * 630) / (1600 * 900)
rows.append(f'\nwhole frame: fixed-4 {F4[0].mean():.1f}; fixed-5 about {F4[0].mean() + d:.1f} (fixed-4 plus the wide crop\'s change, weighted by its area)')
open('meas5.md', 'w').write('\n'.join(rows) + '\n'); print('\n'.join(rows))
