"""B1 fixed-8 P1 pass tests (the coordinator, 18:05), on full frames or crops of the 1600 x 900 frame.
   python3 meas8.py NAME=PNG[@X,Y] ...
   horn box (1030,38)-(1308,238): median L*, median C*, median hue (of pixels over L* 5), and the share over L* 5 (fixed-7:
   L* 0.8, C* 0.3, 2.5 %); pass: hue 85-110, median C* 15 or more.
   batt band: the near front panel's pixels above the woofer (mask rows 270-380): mean C* / mean L* (live 0.33 fails;
   pass about 0.6 or more).  cone/batts as meas6.py (pass 0.25 or below)."""
import json, sys, numpy as np
from PIL import Image
sys.path.insert(0, '.')
from meas6 import lab, part, CONE, BATTS, ids          # noqa: E402  (the same masks as meas6.py)
HORN = np.zeros(ids.shape, bool); HORN[38:238, 1030:1308] = True
BAND = part('front-panel'); BAND[:270] = False; BAND[380:] = False; BAND[:, :1000] = False
rows = ['| frame | horn L* med | horn C* med | horn h med | horn > L*5 | batt band C*/L* | cone/batts Y |', '|---|---|---|---|---|---|---|']
for arg in sys.argv[1:]:
    name, rest = arg.split('=')
    png, off = (rest.split('@') + [None])[:2]
    ox, oy = (int(v) for v in off.split(',')) if off else (0, 0)
    a = np.asarray(Image.open(png).convert('RGB')).astype(float); h, w = a.shape[:2]
    L = np.full(ids.shape + (3,), np.nan); Y = np.full(ids.shape, np.nan)
    l, y = lab(a); L[oy:oy + h, ox:ox + w] = l; Y[oy:oy + h, ox:ox + w] = y
    hv = L[HORN]; hv = hv[~np.isnan(hv[:, 0])]
    C = np.hypot(hv[:, 1], hv[:, 2]); hue = np.degrees(np.arctan2(hv[:, 2], hv[:, 1])) % 360
    lit = hv[:, 0] > 5
    hm = f'{np.median(hue[lit]):.0f}' if lit.any() else '-'
    bv = L[BAND]; bv = bv[~np.isnan(bv[:, 0])]
    band = f'{np.hypot(bv[:, 1], bv[:, 2]).mean() / bv[:, 0].mean():.2f}' if bv.size else '-'
    r = f'{np.nanmean(Y[CONE]) / np.nanmean(Y[BATTS]):.2f}'
    rows.append(f'| {name} | {np.median(hv[:, 0]):.1f} | {np.median(C):.1f} | {hm} | {100 * lit.mean():.1f} % | {band} | {r} |')
print('\n'.join(rows))
