"""Stitch a final rendered in two horizontal strips, then apply the shot's finish once.

A frame that takes over 90 minutes is split between two machines: each renders its half with a small overlap and the
finish off (the finish's clarity and vignette must see the whole frame), e.g. for a 1600 px tall frame

    python3.11 studio/engine/render.py SHOT --samples 512 --crop 0 0 1 0.51 --set finish.enabled=false --out top.png
    python3.11 studio/engine/render.py SHOT --samples 512 --crop 0 0.49 1 1 --set finish.enabled=false --out bottom.png

and this joins them at the frame's middle (each strip's denoised edge falls in the overlap and is dropped) and runs the
finish on the joined raw:

    python3.11 spinoffs/barkhorn/elements/stitch.py SHOT top.png bottom.png --out final.png
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'studio' / 'engine'))
import finish as Fn  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('shot'); ap.add_argument('top'); ap.add_argument('bottom'); ap.add_argument('--out', required=True)
    ap.add_argument('--scale', type=float, default=1.0, help='as given to render.py (for a test at a smaller size)')
    a = ap.parse_args()
    sh = json.loads(Path(a.shot).read_text())
    W, H = (int(v * a.scale) for v in sh['size'])
    t = np.asarray(Image.open(a.top).convert('RGB')); b = np.asarray(Image.open(a.bottom).convert('RGB'))
    assert t.shape[1] == W and b.shape[1] == W, (t.shape, b.shape, W)
    assert t.shape[0] + b.shape[0] > H, 'the strips must overlap'
    mid = H // 2
    # the top strip starts at row 0, the bottom one ends at row H
    full = np.concatenate([t[:mid], b[mid - (H - b.shape[0]):]], axis=0)
    assert full.shape[:2] == (H, W), full.shape
    out = Path(a.out); raw = out.with_suffix('.raw.png')
    Image.fromarray(full).save(raw)
    fin = sh.get('finish') or {}
    if fin.get('enabled'):
        pr = Fn.post(str(raw), str(out), fin)
        print('finish', pr['finish'])
    else:
        Image.fromarray(full).save(out)
    print(out, full.shape[1], 'x', full.shape[0])


if __name__ == '__main__':
    main()
