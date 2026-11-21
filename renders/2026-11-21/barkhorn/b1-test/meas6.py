"""B1 fixed-6: the critics' pass tests (the coordinator, 13:24), on full frames or crops of the 1600 x 900 frame.
   python3 meas6.py NAME=PNG[@X,Y] ...   (X, Y: where a crop sits in the frame; parts from fixed4.mask, same geometry)
Tests: cone and cap within about 10 L* of the approved front's 22 / 24; cone to batts luminance <= 0.2 (approved 0.06);
the walnut sill (1010,712-1240,735) near live's 18; the bell's (1040,40-1320,240) brightest 5 % yellow (h 95-105, C* well
over 10; approved horn L* 54, C* 55, h 97); the far bay (450,240-590,620) near live's."""
import json, sys, numpy as np
from PIL import Image
def lab(a):
    a = a / 255; lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    X = lin @ M.T / np.array([0.95047, 1, 1.08883]); f = np.where(X > 216 / 24389, np.cbrt(X), (24389 / 27 * X + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1), X[..., 1]
m = {int(k): n for k, n in json.load(open('fixed4.mask.json')).items()}
ids = np.asarray(Image.open('fixed4.mask.png').convert('RGB'))[..., 0].astype(int)
part = lambda n: np.isin(ids, [k for k, v in m.items() if v == n])
near = np.zeros(ids.shape, bool); near[370:570, 1080:1290] = True
CONE, CAP = part('woofer-cone') & near, part('woofer-cap') & near
# the batts beside the woofer at its height, seen through the clear front panel (the mask's first hit): the front panel's
# pixels in the woofer's rows (400-546), left of x 1095 and right of x 1245
BATTS = part('front-panel'); BATTS[:400] = False; BATTS[546:] = False; BATTS[:, 1095:1245] = False
def box(x0, y0, x1, y1):
    b = np.zeros(ids.shape, bool); b[y0:y1, x0:x1] = True; return b
SILL, BELL, FAR, FRONT = box(1010, 712, 1240, 735), box(1040, 40, 1320, 240), box(450, 240, 590, 620), box(1060, 260, 1300, 560)
rows = ['| frame | cone L* | cap L* | cone/batts Y | sill L* | bell L* | bell top 5 % L* / C* / h | far bay L* (% > 10) | front L* |',
        '|---|---|---|---|---|---|---|---|---|']
for arg in sys.argv[1:]:
    name, rest = arg.split('=')
    png, off = (rest.split('@') + [None])[:2]
    ox, oy = (int(v) for v in off.split(',')) if off else (0, 0)
    a = np.asarray(Image.open(png).convert('RGB')).astype(float)
    L = np.full(ids.shape + (3,), np.nan); Y = np.full(ids.shape, np.nan)
    l, y = lab(a); h, w = a.shape[:2]
    L[oy:oy + h, ox:ox + w] = l; Y[oy:oy + h, ox:ox + w] = y
    def mean(mask, ch=0, arr=None):
        v = (arr if arr is not None else L[..., ch])[mask]; v = v[~np.isnan(v)]
        return f'{v.mean():.1f}' if v.size else '-'
    cy, by = Y[CONE], Y[BATTS]
    ratio = f'{np.nanmean(cy) / np.nanmean(by):.2f}' if (~np.isnan(cy)).any() and (~np.isnan(by)).any() else '-'
    bl = L[BELL]; bl = bl[~np.isnan(bl[:, 0])]
    if bl.size:
        top = bl[bl[:, 0] >= np.percentile(bl[:, 0], 95)]; la, aa, bb = top.mean(0)
        bt = f'{la:.1f} / {np.hypot(aa, bb):.1f} / {np.degrees(np.arctan2(bb, aa)) % 360:.0f}'
    else:
        bt = '-'
    fv = L[FAR][:, 0]; fv = fv[~np.isnan(fv)]
    far = f'{fv.mean():.1f} ({100 * (fv > 10).mean():.0f} %)' if fv.size else '-'
    rows.append(f'| {name} | {mean(CONE)} | {mean(CAP)} | {ratio} | {mean(SILL)} | {mean(BELL)} | {bt} | {far} | {mean(FRONT)} |')
print('\n'.join(rows))
