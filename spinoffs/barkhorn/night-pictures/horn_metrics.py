"""The gate's horn targets (the coordinator's skeptic, 2026-11-09 19:54), in CIELAB L* (D65), on a frame or a crop of it.

    python3 spinoffs/barkhorn/night-pictures/horn_metrics.py IMAGE.png MASK.png MASK.json [--crop X0 Y0 X1 Y1]
        MASK: the engine's part mask of the full frame (render.py --masks; any frame from the same camera); with --crop
        (fractions of the full frame, top left), IMAGE is that region of it

- every horn pixel at or under L* 90;
- the X's arms (the creases from the horn's corners to its pod): L* p95 in the horn's four corner quarters, the pod's
  middle left out, against proxy 4's about 10 / 5 / 19 / 35 (upper-left, upper-right, lower-left, lower-right);
- the arc under the pod: the band below the pod, under about L* 30.
"""
import json
import sys

import numpy as np
from PIL import Image

HORN = ('horn-', 'waveguide', 'hf-', 'caldera-', 'strata-')


def lstar(rgb):
    a = rgb / 255.0
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    Y = lin @ np.array([0.2126, 0.7152, 0.0722])
    return np.where(Y > 216 / 24389, 116 * np.cbrt(Y) - 16, Y * 24389 / 27)


def main():
    im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float64)
    ids = np.asarray(Image.open(sys.argv[2]))[..., 0]
    leg = {int(k): v for k, v in json.load(open(sys.argv[3])).items()}
    if '--crop' in sys.argv:
        i = sys.argv.index('--crop'); x0, y0, x1, y1 = (float(v) for v in sys.argv[i + 1:i + 5])
        H, W = ids.shape
        ids = ids[int(round(y0 * H)):int(round(y1 * H)), int(round(x0 * W)):int(round(x1 * W))]
    if ids.shape != im.shape[:2]:
        ids = np.asarray(Image.fromarray(ids).resize((im.shape[1], im.shape[0]), Image.NEAREST))
    horn = np.isin(ids, [k for k, v in leg.items() if v.startswith(HORN)])
    L = lstar(im)
    shell = np.isin(ids, [k for k, v in leg.items() if v == 'waveguide'])      # the horn's flare: its box
    ys, xs = np.where(shell)
    hx0, hx1, hy0, hy1 = xs.min(), xs.max(), ys.min(), ys.max()
    cx, cy = (hx0 + hx1) / 2, (hy0 + hy1) / 2
    yy, xx = np.mgrid[0:horn.shape[0], 0:horn.shape[1]]
    u = (xx - cx) / ((hx1 - hx0) / 2); v = (yy - cy) / ((hy1 - hy0) / 2)
    pod = (u ** 2 + v ** 2) < 0.30 ** 2
    print(f'horn: L* max {L[horn].max():.0f} (target <= 90), p99.9 {np.percentile(L[horn], 99.9):.0f}, '
          f'pixels over 90: {(L[horn] > 90).sum()}')
    arms = []
    for name, q in (('upper-left', (u < 0) & (v < 0)), ('upper-right', (u > 0) & (v < 0)),
                    ('lower-left', (u < 0) & (v > 0)), ('lower-right', (u > 0) & (v > 0))):
        m = shell & q & ~pod
        arms.append(f'{name} {np.percentile(L[m], 95):.0f}')
    print('X arms, L* p95:', ', '.join(arms), '(proxy 4: about 10, 5, 19, 35)')
    arc = shell & (np.abs(u) < 0.45) & (v > 0.25) & (v < 0.65)
    print(f'arc under the pod: L* p95 {np.percentile(L[arc], 95):.0f}, max {L[arc].max():.0f} (target under about 30)')


if __name__ == '__main__':
    main()
