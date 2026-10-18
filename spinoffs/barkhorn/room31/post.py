"""Room 31's photographic finish: what a lens and a sensor add to a frame and a path tracer does not, applied after the
engine (render.py) and before the critic, so the critic judges what ships.

    python3 spinoffs/barkhorn/room31/post.py IN.png OUT.png [--grain 1.4] [--vignette 0.22] [--bloom 0.05]

- vignette: the lens's natural fall-off, `vignette` stops at the corners, on a cos^4-like curve;
- bloom: the glow a real lens gives a bright patch (light scattered in the glass), `bloom` of a wide blur of what lies
  above 200 added back;
- grain: fine luminance noise, `grain` levels (sRGB, 1 sigma) at mid-grey and less in the deep shadows and highlights,
  the same seed every time, so a frame and its re-render match.
No colour moves: every operation is on luminance or a neutral gain in linear light.
"""
import argparse

import numpy as np
from PIL import Image, ImageFilter


def lin(a):
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def srgb(a):
    a = np.clip(a, 0, 1)
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)


def finish(img, grain=1.4, vignette=0.22, bloom=0.05, seed=31):
    a = np.asarray(img.convert('RGB'), np.float32) / 255.0
    H, W, _ = a.shape
    L = lin(a)
    # vignette: stops of fall-off by normalised radius (corner = 1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / np.sqrt(2)
    L *= (2.0 ** (-vignette * r ** 2.2))[..., None]
    # bloom: highlights blurred wide and added back
    if bloom > 0:
        hi = np.clip(srgb(L) - 200 / 255.0, 0, None) / (55 / 255.0)
        hi_img = Image.fromarray((np.clip(hi, 0, 1) * 255).astype(np.uint8))
        rad = max(2, W // 90)
        bl = np.asarray(hi_img.filter(ImageFilter.GaussianBlur(rad)), np.float32) / 255.0
        L += bloom * bl * L.mean(axis=(0, 1), keepdims=True) * 4.0
    out = srgb(L)
    # grain, on luminance, weighted toward the midtones
    if grain > 0:
        rng = np.random.default_rng(seed)
        n = rng.normal(0, grain / 255.0, (H, W)).astype(np.float32)
        Y = out @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        w = 4 * Y * (1 - Y)
        out = out + (n * w)[..., None]
    return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--grain', type=float, default=1.4)
    ap.add_argument('--vignette', type=float, default=0.22)
    ap.add_argument('--bloom', type=float, default=0.05)
    a = ap.parse_args()
    finish(Image.open(a.src), a.grain, a.vignette, a.bloom).save(a.dst, optimize=True)
    print(a.dst)


if __name__ == '__main__':
    main()
