"""B1 fixed-8, the near horn's MOUTH (the coordinator, 20:08): the near waveguide's pixels (its mask, x > 1000 in the
1600 x 900 frame), the lemon share (C* >= 20 and hue 85-115) and the mouth's median L* / C* / hue.
   python3 meas8m.py NAME=PNG[@X,Y][:MASKSTEM] ...   (MASKSTEM: the mask pair to use, default fixed4 (the old position);
   a crop's own mask sits at the crop's offset)"""
import json, sys, numpy as np
from PIL import Image
from meas6 import lab
rows = ['| frame | mouth px | lemon share (C* >= 20, h 85-115) | mouth L* / C* / h (median) |', '|---|---|---|---|']
for arg in sys.argv[1:]:
    name, rest = arg.split('=')
    rest, stem = (rest.split(':') + ['fixed4'])[:2]
    png, off = (rest.split('@') + [None])[:2]
    ox, oy = (int(v) for v in off.split(',')) if off else (0, 0)
    m = {int(k): n for k, n in json.load(open(stem + '.mask.json')).items()}
    ids = np.asarray(Image.open(stem + '.mask.png').convert('RGB'))[..., 0].astype(int)
    mox, moy = (ox, oy) if stem != 'fixed4' else (0, 0)
    a = np.asarray(Image.open(png).convert('RGB')).astype(float); l, _ = lab(a); h, w = a.shape[:2]
    L = np.full((900, 1600, 3), np.nan); L[oy:oy + h, ox:ox + w] = l
    M = np.zeros((900, 1600), bool); mh, mw = ids.shape
    M[moy:moy + mh, mox:mox + mw] = np.isin(ids, [k for k, v in m.items() if v == 'waveguide'])
    M[:, :1000] = False
    v = L[M]; v = v[~np.isnan(v[:, 0])]
    C = np.hypot(v[:, 1], v[:, 2]); hue = np.degrees(np.arctan2(v[:, 2], v[:, 1])) % 360
    lemon = (C >= 20) & (hue >= 85) & (hue <= 115)
    rows.append(f'| {name} | {v.shape[0]} | {100 * lemon.mean():.1f} % | {np.median(v[:, 0]):.1f} / {np.median(C):.1f} / {np.median(hue):.0f} |')
print('\n'.join(rows))
