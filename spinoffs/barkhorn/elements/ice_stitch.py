"""Ice's landscape final in horizontal strips, rendered on several boxes and joined (round 31b, the drivers made real).

A full 2400 x 1600 frame at 512 samples takes about 110 minutes on one box. Each strip is the same shot rendered with
`--crop` (the renderer keeps the strip's raw frame beside it as STRIP.raw.png); this joins the raw strips top to bottom
and runs the shot's own finish once over the whole frame, so the vignette, bloom and grain are the full frame's, not
each strip's.

    # the four strips' commands (they overlap by 2.5 % of the height, blended when joined), one per box:
    python3.11 spinoffs/barkhorn/elements/ice_stitch.py commands
    # then, with the four strips' .raw.png in place:
    python3.11 spinoffs/barkhorn/elements/ice_stitch.py
"""
import json, os, sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
import finish as Fn                                       # noqa: E402

SHOT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'element31', 'ice.json')
OUT = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'element31')
N = 4
OVERLAP = 0.025          # each strip runs this share of the frame's height past its neighbours, to blend the seam


def crop(k):
    """Strip k's --crop, top to bottom: x0 y0 x1 y1 as fractions from the top left, overlapping its neighbours."""
    return [0.0, max(0.0, k / N - OVERLAP), 1.0, min(1.0, (k + 1) / N + OVERLAP)]


def main():
    sh = json.load(open(SHOT))
    W, H = sh['size']
    d = os.environ.get('ICE_STRIPS', os.path.join(OUT, 'strips'))
    acc = np.zeros((H, W, 3)); wsum = np.zeros((H, 1, 1))
    for k in range(N):
        a = np.asarray(Image.open(os.path.join(d, f'ice-{k}.raw.png')).convert('RGB')).astype(np.float64)
        y0, y1 = crop(k)[1], crop(k)[3]
        r0 = int(round(y0 * H)); r1 = r0 + a.shape[0]
        assert a.shape[1] == W and abs(r1 - y1 * H) <= 1, f'strip {k} is {a.shape[1]} x {a.shape[0]}'
        # a weight ramping across the overlaps (linear light would be truer; at 512 samples the strips agree closely)
        w = np.ones(a.shape[0])
        ov = int(round(OVERLAP * H)) * 2
        if k > 0:
            w[:ov] = np.linspace(0, 1, ov + 2)[1:-1]
        if k < N - 1:
            w[-ov:] = np.minimum(w[-ov:], np.linspace(1, 0, ov + 2)[1:-1])
        acc[r0:r1] += a * w[:, None, None]; wsum[r0:r1] += w[:, None, None]
    raw = np.clip(np.rint(acc / np.maximum(wsum, 1e-9)), 0, 255).astype(np.uint8)
    raw_png = os.path.join(d, 'ice.raw.png')
    Image.fromarray(raw).save(raw_png)
    rep = Fn.post(raw_png, os.environ.get('ICE_OUT', os.path.join(OUT, 'ice.png')), sh['finish'])
    print(json.dumps(rep['finish']))


def commands():
    """The render command for each strip."""
    for k in range(N):
        x0, y0, x1, y1 = crop(k)
        print(f'python3.11 studio/engine/render.py studio/shots/barkhorn/element31/ice.json --samples 512 '
              f'--crop {x0:g} {y0:g} {x1:g} {y1:g} --out renders/2026-10-18/barkhorn/element31/strips/ice-{k}.png')

if __name__ == '__main__':
    commands() if sys.argv[1:] == ['commands'] else main()
