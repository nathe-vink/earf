"""Poison A4's post-only retouch (2026-10-19, the coordinator's follow-up, one pass): on the finished frames,
1. the fly agaric caps, keyed by hue inside the foreground band (nothing else there is that salmon-orange), feathered
   2-3 px: the hue toward a deeper scarlet, chroma down 20 %, value down 10 %; the white warts untouched;
2. the hot streak down the clear front corner over the woofer's right edge: only its smooth excess over the panel
   beside it is compressed, feathered, so the edge line stays.

    python3.11 spinoffs/barkhorn/elements/retouch_a4.py IN.png OUT.png landscape|portrait [--mask MASK.png] [--streak-only]
"""
import argparse

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, binary_dilation

# per frame (full-size pixels): the foreground band the caps sit in, and the streak's band on the clear corner
FRAMES = {
    'landscape': dict(caps=(360, 1230, 1120, 1540), streak=(1160, 610, 1300, 1190)),
    'portrait': dict(caps=(120, 1500, 760, 1800), streak=(780, 1070, 870, 1600)),
}
HUE_SHIFT = -8.0 / 360          # salmon-orange toward scarlet
CHROMA, VALUE = 0.8, 0.9
STREAK = 0.5                    # how much of the streak's smooth excess goes


def rgb_hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1); d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-6
    rm = m & (mx == r); gm = m & (mx == g) & ~rm; bm = m & ~rm & ~gm
    h[rm] = ((g - b)[rm] / d[rm]) % 6
    h[gm] = (b - r)[gm] / d[gm] + 2
    h[bm] = (r - g)[bm] / d[bm] + 4
    h /= 6
    s = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0)
    return h, s, mx


def hsv_rgb(h, s, v):
    i = np.floor(h * 6) % 6; f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    out = np.zeros(h.shape + (3,))
    for k, (r, g, b) in enumerate(((v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q))):
        sel = i == k
        out[sel] = np.stack([r[sel], g[sel], b[sel]], -1)
    return out


def feathered_box(shape, box, f):
    x0, y0, x1, y1 = box
    m = np.zeros(shape); m[y0:y1, x0:x1] = 1.0
    return gaussian_filter(m, f)


def retouch(a, frame, caps_on=True):
    P = FRAMES[frame]
    H, W = a.shape[:2]
    # 1. the caps
    h, s, v = rgb_hsv(a)
    hue_ok = (h < 22 / 360) | (h > 350 / 360)
    key = hue_ok & (((s > 0.45) & (v > 0.45)) | ((s > 0.55) & (v > 0.28) & (h < 18 / 360)))   # the shaded side too
    x0, y0, x1, y1 = P['caps']
    band = np.zeros((H, W), bool); band[y0:y1, x0:x1] = True
    key &= band
    key = binary_dilation(key, iterations=1)
    m = np.clip(gaussian_filter(key.astype(float), 1.2) * 1.4, 0, 1)
    h2 = (h + HUE_SHIFT) % 1.0
    caps = hsv_rgb(h2, np.clip(s * CHROMA, 0, 1), v * VALUE)
    if not caps_on:                                       # the streak half alone
        m = np.zeros_like(m)
    out = a * (1 - m[..., None]) + caps * m[..., None]
    # 2. the streak: the panel's level either side of the band, per row, is the floor; the band's smooth excess over
    # it is compressed (the fine edge line rides on top, untouched)
    x0, y0, x1, y1 = P['streak']
    L = out.mean(-1)
    side = np.concatenate([L[:, max(0, x0 - 24):x0], L[:, x1:x1 + 24]], 1)
    floor = gaussian_filter(np.median(side, 1), 12)[:, None]
    Ls = gaussian_filter(L, 5)
    excess = np.clip(Ls - floor, 0, None)
    mb = feathered_box((H, W), P['streak'], 10)
    L2 = L - STREAK * excess * mb
    g = np.clip(L2 / np.maximum(L, 1e-4), 0, 1)
    out = out * g[..., None]
    return np.clip(out, 0, 1), m, mb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('dst'); ap.add_argument('frame', choices=list(FRAMES))
    ap.add_argument('--mask')
    ap.add_argument('--streak-only', action='store_true', help='leave the caps as rendered')
    a = ap.parse_args()
    img = np.asarray(Image.open(a.src).convert('RGB')).astype(float) / 255.0
    out, m, mb = retouch(img, a.frame, caps_on=not a.streak_only)
    Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(a.dst)
    if a.mask:
        Image.fromarray((np.stack([m, mb, np.zeros_like(m)], -1) * 255).astype(np.uint8)).save(a.mask)
    print(a.dst, 'caps px', int((m > 0.5).sum()))


if __name__ == '__main__':
    main()
