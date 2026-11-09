"""The proxy 8 pendant sweep's measures (the coordinator, 2026-11-09 20:49), on regraded crops [0.40, 0.0, 0.68, 0.46].

    python3 spinoffs/barkhorn/night-pictures/sweep_measure.py NAME [NAME ...]    # reads /home/user/night-work/NAME-rg.png

The lamp's bottom (its dome, L* over 88, right of the horn) against the horn's top line (the waveguide's top row, from
proxy 7's mask), in px of the crop; the cabinet's top band (the top, its land and pad) in L*; then horn_metrics.py.
"""
import json, sys, subprocess
import numpy as np
from PIL import Image
sys.path.insert(0, '/home/user/earf/spinoffs/barkhorn/night-pictures')
from horn_metrics import lstar
R = '/home/user/earf/renders/2026-11-09/barkhorn/night-pictures/night-ice-wide-proxy7'
x0, y0, x1, y1 = 0.40, 0.0, 0.68, 0.46
ids = np.asarray(Image.open(R + '.mask.png'))[..., 0]
leg = {int(k): v for k, v in json.load(open(R + '.mask.json')).items()}
H, W = ids.shape
ids = ids[int(round(y0 * H)):int(round(y1 * H)), int(round(x0 * W)):int(round(x1 * W))]
for v in sys.argv[1:]:
    im = np.asarray(Image.open(f'/home/user/night-work/{v}-rg.png').convert('RGB')).astype(float)
    L = lstar(im)
    idc = ids if ids.shape == L.shape else np.asarray(Image.fromarray(ids).resize((L.shape[1], L.shape[0]), Image.NEAREST))
    wg = idc == [k for k, n in leg.items() if n == 'waveguide'][0]
    horn_top = np.where(wg)[0].min()
    # the lamp: the bright dome, right of the horn
    hx1 = np.where(wg)[1].max()
    lamp = (L > 88); lamp[:, :hx1 + 5] = False; lamp[horn_top:, :] = False
    ys = np.where(lamp)[0]
    lb = ys.max() if len(ys) else -1
    topband = np.isin(idc, [k for k, n in leg.items() if n in ('top', 'land-top', 'top-pad')])
    print(f'== {v}: lamp bottom row {lb}, horn top row {horn_top}, clearance {horn_top - lb} px (crop at half scale; '
          f'{2 * (horn_top - lb)} px at 3840), cabinet top band L* median {np.median(L[topband]):.0f} p95 {np.percentile(L[topband], 95):.0f}')
    out = subprocess.run(['python3', '/home/user/earf/spinoffs/barkhorn/night-pictures/horn_metrics.py', f'/home/user/night-work/{v}-rg.png',
                          R + '.mask.png', R + '.mask.json', '--crop', str(x0), str(y0), str(x1), str(y1)], capture_output=True, text=True)
    print(out.stdout + out.stderr)
