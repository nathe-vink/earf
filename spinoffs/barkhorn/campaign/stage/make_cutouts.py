"""The stage's cutout props (the owner, 2026-11-11: "some cutout prop near it, like a white cutout cloud on the ground
for fog, a cutout of grass for poison"): each one's outline traced from the brand's own tint icon (r47-brand,
spinoffs/barkhorn/brandbook/book/img/icon-<tint>.png, copied unchanged into icons/), so the painted face is the icon
itself. Poison's is a tuft of grass (the owner's word), drawn here in the icons' style (flat fill, a heavy black line),
with the skull icon kept for a small sign on a stake; Ice's icicles stand up as ice spikes (flipped).

    .venv-fab/bin/python spinoffs/barkhorn/campaign/stage/make_cutouts.py     ->  stage/cutouts.json, icons/grass-poison.png

cutouts.json: tint -> {image, flip, outline: [[u, v], ...]} in the image's 0-1 frame (v up), the outer silhouette only
(holes filled), simplified to about 1 px.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
TINTS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']


def grass(path, n=256):
    """A tuft of grass in the icons' style: blades of the icon's green (#027614) on a low mound, a black line."""
    S = 4; W = n * S
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    g, k = (2, 118, 20, 255), (26, 26, 26, 255)
    base = 0.86 * W
    blades = [(-0.30, 0.42, -0.12), (-0.18, 0.22, -0.05), (-0.05, 0.10, 0.02), (0.08, 0.18, 0.10), (0.20, 0.30, 0.16),
              (0.31, 0.48, 0.26), (-0.38, 0.58, -0.28), (0.40, 0.62, 0.36)]      # (root x, tip height from top, tip x)
    polys = []
    for rx, ty, tx in blades:
        r0, r1 = (0.5 + rx - 0.06) * W, (0.5 + rx + 0.06) * W
        polys.append([(r0, base), ((0.5 + tx) * W, ty * W), (r1, base)])
    mound = [(0.08 * W, base), (0.92 * W, base), (0.88 * W, 0.80 * W), (0.12 * W, 0.80 * W)]
    lw = 9 * S
    for p in polys + [mound]:                                  # the line first, a little wider, then the fill inside it
        d.line(p + [p[0]], fill=k, width=lw, joint='curve')
    for p in polys + [mound]:
        d.polygon(p, fill=g)
    for p in polys:                                            # the line again over the fills where blades cross
        d.line(p + [p[0]], fill=k, width=lw // 2, joint='curve')
    d.line(mound + [mound[0]], fill=k, width=lw // 2, joint='curve')
    im.resize((n, n), Image.LANCZOS).save(path)


def _filled(alpha):
    """The silhouette with its holes filled: everything not reachable from the border through clear pixels."""
    clear = alpha < 128
    H, W = clear.shape
    out = np.zeros_like(clear)
    stack = [(y, x) for y in range(H) for x in (0, W - 1)] + [(y, x) for x in range(W) for y in (0, H - 1)]
    while stack:
        y, x = stack.pop()
        if 0 <= y < H and 0 <= x < W and clear[y, x] and not out[y, x]:
            out[y, x] = True
            stack += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    return ~out


def _simplify(pts, eps):
    """Douglas-Peucker."""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    ab = b - a; L = np.hypot(*ab) or 1e-9
    v = pts - a
    d = np.abs(ab[0] * v[:, 1] - ab[1] * v[:, 0]) / L
    i = int(np.argmax(d))
    if d[i] > eps:
        return np.vstack([_simplify(pts[:i + 1], eps)[:-1], _simplify(pts[i:], eps)])
    return np.vstack([a, b])


def outline(path, flip=False):
    a = np.asarray(Image.open(path).convert('RGBA'))[:, :, 3].astype(float)
    if flip:
        a = a[::-1]
    m = _filled(a).astype(float)
    m = np.pad(m, 2)
    cs = plt.contour(m, levels=[0.5])
    segs = max(cs.allsegs[0], key=len)
    plt.close('all')
    H, W = a.shape
    p = np.array(segs) - 2.0
    j = int(np.argmax(np.hypot(*(p - p[0]).T)))               # a ring: split at the point farthest from its start
    p = np.vstack([_simplify(p[:j + 1], 0.8)[:-1], _simplify(np.vstack([p[j:], p[:1]]), 0.8)[:-1]])
    uv = [[round(float(x) / (W - 1), 4), round(1.0 - float(y) / (H - 1), 4)] for x, y in p]
    return uv


def main():
    grass(os.path.join(HERE, 'icons', 'grass-poison.png'))
    out = {}
    for t in TINTS:
        img = f'icons/{"grass-poison" if t == "poison" else t}.png'
        flip = t == 'ice'
        out[t] = {'image': img, 'flip': flip, 'outline': outline(os.path.join(HERE, img), flip)}
    out['poison-sign'] = {'image': 'icons/poison.png', 'flip': False, 'outline': [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]}
    json.dump(out, open(os.path.join(HERE, 'cutouts.json'), 'w'), indent=1)
    for k, v in out.items():
        print(k, len(v['outline']), 'points')


if __name__ == '__main__':
    main()
