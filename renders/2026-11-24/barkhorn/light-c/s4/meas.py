"""S4 readings: each light-C front against its S4 frame (the five reflect-only flags as real cards), by region, from
the front's own mask (same geometry). L* and C* (sRGB to Lab), and the share of pixels that moved more than 2 L*.
    python3 meas.py TINT...      (run here)"""
import json, os, sys, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.dirname(HERE)
def lab(a):
    a = a / 255; lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    X = lin @ M.T / np.array([0.95047, 1, 1.08883]); f = np.where(X > 216 / 24389, np.cbrt(X), (24389 / 27 * X + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)
REGIONS = {'front panel (batts behind)': ['front-panel'], 'right side': ['right'], 'left side': ['left'], 'top': ['top'],
           'base (bottom, feet)': ['bottom', 'feet-base', 'feet-stem'], 'horn': ['waveguide']}
rows = ['| tint | region | px | L* now | L* S4 | dL* | C* now | C* S4 | moved > 2 L* |', '|---|---|---|---|---|---|---|---|---|']
for t in sys.argv[1:]:
    m = {int(k): v for k, v in json.load(open(os.path.join(SRC, f'front-{t}.mask.json'))).items()}
    ids = np.asarray(Image.open(os.path.join(SRC, f'front-{t}.mask.png')).convert('RGB'))[..., 0].astype(int)
    a = lab(np.asarray(Image.open(os.path.join(SRC, f'front-{t}.png')).convert('RGB')).astype(float))
    b = lab(np.asarray(Image.open(os.path.join(HERE, f'front-{t}-s4.png')).convert('RGB')).astype(float))
    reg = {k: np.isin(ids, [i for i, n in m.items() if n in v]) for k, v in REGIONS.items()}
    # the paper: no part in the mask; the floor under and round the base (rows 1000-1250), and the backdrop above
    paper = ~np.isin(ids, list(m))
    fl = paper.copy(); fl[:1000] = False; reg['floor round the base (paper)'] = fl
    bd = paper.copy(); bd[700:] = False; reg['backdrop (paper)'] = bd
    for k, r in reg.items():
        if not r.any():
            continue
        la, lb = a[r], b[r]; ca, cb = np.hypot(la[:, 1], la[:, 2]), np.hypot(lb[:, 1], lb[:, 2])
        mv = (np.abs(lb[:, 0] - la[:, 0]) > 2).mean() * 100
        rows.append(f'| {t} | {k} | {r.sum()} | {la[:, 0].mean():.1f} | {lb[:, 0].mean():.1f} | {lb[:, 0].mean() - la[:, 0].mean():+.1f} | '
                    f'{ca.mean():.1f} | {cb.mean():.1f} | {mv:.0f} % |')
print('\n'.join(rows))
