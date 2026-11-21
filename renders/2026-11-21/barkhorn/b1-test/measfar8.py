"""B1 fixed-8 P3/P4 boxes, on full frames or crops of the 1600 x 900 frame.  python3 measfar8.py NAME=PNG[@X,Y] ..."""
import sys, numpy as np
from PIL import Image
from meas6 import lab
B = {'P3 far horn screen (478,328-528,380)': (478, 328, 528, 380), 'far bay (450,240-590,620)': (450, 240, 590, 620),
     'record wall (620,200-980,600)': (620, 200, 980, 600), 'wall top (620,0-980,120)': (620, 0, 980, 120),
     'ceiling (240,0-600,60)': (240, 0, 600, 60), 'green print (360,440-440,520)': (360, 440, 440, 520),
     'hemispheres (240,220-440,460)': (240, 220, 440, 460)}
F = {}
for arg in sys.argv[1:]:
    n, rest = arg.split('='); png, off = (rest.split('@') + [None])[:2]; ox, oy = (int(v) for v in off.split(',')) if off else (0, 0)
    a = np.asarray(Image.open(png).convert('RGB')).astype(float); l, _ = lab(a)
    L = np.full((900, 1600, 3), np.nan); h, w = a.shape[:2]; L[oy:oy + h, ox:ox + w] = l; F[n] = L
print('| box | ' + ' | '.join(F) + ' |'); print('|---|' + '---|' * len(F))
for n, (x0, y0, x1, y1) in B.items():
    c = []
    for L in F.values():
        v = L[y0:y1, x0:x1].reshape(-1, 3); v = v[~np.isnan(v[:, 0])]
        c.append(f'{v[:, 0].mean():.1f} / {np.hypot(v[:, 1], v[:, 2]).mean():.1f}' if v.size else '-')
    print(f'| {n} | ' + ' | '.join(c) + ' |')
