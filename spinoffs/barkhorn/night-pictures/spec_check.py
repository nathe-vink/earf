"""Checks a night picture against the coordinator's spec (r46-owner-notes 65ec7c5f, night-picture-spec-2026-11-04.md).

    python3 spinoffs/barkhorn/night-pictures/spec_check.py IMAGE.png wide|tall [--lamp-box x0 y0 x1 y1]

- The box: the speaker's parts from the engine's report beside the image (NAME.report.json, parts_2d), as fractions of
  the frame; with --lamp-box (fractions) the lamp's own extent is added ('the speaker with its lamp').
- The text zones: relative luminance (sRGB to linear, Rec. 709 weights) at or under 0.09, as the 99th percentile, so
  no speculars either.
- The floor pool outside the speaker's column: the wide file's floor (y >= 0.78) outside x 0.42-0.58, and below
  y 0.88 anywhere, should stay as dark as the text zones.
- The edges: nothing bright within 4 % of an edge (the 99th percentile there, against the zones' limit).
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

BOX = {'wide': (0.418, 0.20, 0.582, 0.78), 'tall': (0.35, 0.25, 0.65, 0.59)}
ZONES = {
    'wide': {'lower-left': (0.02, 0.69, 0.44, 1.0), 'lower-right': (0.55, 0.77, 0.98, 1.0),
             'top-left': (0.0, 0.0, 0.41, 0.22), 'top-right': (0.61, 0.0, 1.0, 0.22)},
    'tall': {'lower-band': (0.0, 0.61, 1.0, 1.0), 'top-left': (0.0, 0.0, 0.50, 0.25), 'top-right': (0.77, 0.0, 1.0, 0.25)},
}
LIMIT = 0.09


def lum(img):
    a = np.asarray(img.convert('RGB')).astype(np.float64) / 255.0
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    return lin @ np.array([0.2126, 0.7152, 0.0722])


def main():
    path, fmt = sys.argv[1], sys.argv[2]
    im = Image.open(path); W, H = im.size
    L = lum(im)
    rep = Path(path).with_suffix('.report.json')
    parts = json.loads(rep.read_text()).get('parts_2d', {}) if rep.exists() else {}
    if parts:
        RW, RH = json.loads(rep.read_text()).get('size', [W, H])
        xs0 = min(p['box_px'][0] for p in parts.values()); ys0 = min(p['box_px'][1] for p in parts.values())
        xs1 = max(p['box_px'][2] for p in parts.values()); ys1 = max(p['box_px'][3] for p in parts.values())
        box = [xs0 / RW, ys0 / RH, xs1 / RW, ys1 / RH]
        if '--lamp-box' in sys.argv:
            i = sys.argv.index('--lamp-box'); lb = [float(v) for v in sys.argv[i + 1:i + 5]]
            box = [min(box[0], lb[0]), min(box[1], lb[1]), max(box[2], lb[2]), max(box[3], lb[3])]
        B = BOX[fmt]
        ok = box[0] >= B[0] and box[1] >= B[1] and box[2] <= B[2] and box[3] <= B[3]
        print(f'box: speaker{" with its lamp" if "--lamp-box" in sys.argv else ""} x {box[0]:.3f}-{box[2]:.3f} y {box[1]:.3f}-{box[3]:.3f};'
              f' the spec\'s x {B[0]}-{B[2]} y {B[1]}-{B[3]}: {"INSIDE" if ok else "OUTSIDE"}')
    worst = 0.0
    for name, (x0, y0, x1, y1) in ZONES[fmt].items():
        z = L[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
        p99, mean = float(np.percentile(z, 99)), float(z.mean())
        worst = max(worst, p99)
        print(f'zone {name:12s} mean {mean:.3f}  p99 {p99:.3f}  {"ok" if p99 <= LIMIT else "TOO BRIGHT"}')
    if fmt == 'wide':
        fl = np.concatenate([L[int(0.78 * H):, :int(0.42 * W)].ravel(), L[int(0.78 * H):, int(0.58 * W):].ravel()])
        below = L[int(0.88 * H):, :].ravel()
        print(f'floor outside the column (y >= 0.78) p99 {np.percentile(fl, 99):.3f}; below y 0.88 p99 {np.percentile(below, 99):.3f}'
              f'  {"ok" if max(np.percentile(fl, 99), np.percentile(below, 99)) <= LIMIT else "TOO BRIGHT"}')
    e = int(0.04 * min(W, H))
    edges = np.concatenate([L[:e].ravel(), L[-e:].ravel(), L[:, :e].ravel(), L[:, -e:].ravel()])
    print(f'edges (4 %) mean {edges.mean():.3f} p99 {np.percentile(edges, 99):.3f}  {"ok" if np.percentile(edges, 99) <= LIMIT else "BRIGHT"}')


if __name__ == '__main__':
    main()
