"""Amp test readings: the plate (every amp-plate-* part) and its surround (everything else in frame), L* and C*, by
the frame's own mask (or, with @MASKSTEM, another frame's of the same geometry and size).
    python3 meas.py NAME=PNG[@MASKSTEM] ...      also prints each frame's share of the first frame's surround light (Y)"""
import json, sys, numpy as np
from PIL import Image
def lab(a):
    a = a / 255; lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    X = lin @ M.T / np.array([0.95047, 1, 1.08883]); f = np.where(X > 216 / 24389, np.cbrt(X), (24389 / 27 * X + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1), X[..., 1]
rows = ['| frame | plate face L* | plate L* | plate C* | surround L* | surround C* | surround Y share |', '|---|---|---|---|---|---|---|']
ref = None
for arg in sys.argv[1:]:
    name, rest = arg.split('=')
    png, stem = (rest.split('@') + [None])[:2]
    stem = stem or png[:-4]
    m = json.load(open(stem + '.mask.json'))
    ids = np.asarray(Image.open(stem + '.mask.png').convert('RGB'))[..., 0].astype(int)
    plate = np.isin(ids, [int(k) for k, v in m.items() if v.startswith('amp-plate')])
    face = np.isin(ids, [int(k) for k, v in m.items() if v == 'amp-plate-plate'])
    L, Y = lab(np.asarray(Image.open(png).convert('RGB')).astype(float))
    sur = ~plate
    y = Y[sur].mean(); ref = ref if ref is not None else y
    c = lambda r: np.hypot(L[r][:, 1], L[r][:, 2]).mean()
    rows.append(f'| {name} | {L[face][:, 0].mean():.1f} | {L[plate][:, 0].mean():.1f} | {c(plate):.1f} | {L[sur][:, 0].mean():.1f} | {c(sur):.1f} | {y / ref * 100:.0f} % |')
print('\n'.join(rows))
