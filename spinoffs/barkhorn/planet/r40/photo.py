"""Round 40's last step: round 39's lens and sensor (halation, vignette, lateral CA), and before them the chroma
noise reduction every camera applies to a high-ISO night frame (the p4 critics: "chroma grain on the oak front").

    python3.11 spinoffs/barkhorn/planet/r40/photo.py IN.png OUT.png [--chroma 1.6] [--halation 0.10] [--vignette 0.18] [--ca 0.6]

- **chroma**: the colour-difference channels (YCbCr) smoothed over `chroma` px (at 2400 wide), the luminance left as
  it is, so the colour blotches go and the detail and the grain stay;

- **halation**: light from the practicals spreads a little in the glass and the sensor, a soft warm glow round each lamp
  and flame, over a few tens of pixels; only what is near clipping spreads (above `knee`), so midtones stay crisp;
- **vignette**: a 24-35 mm lens wide open falls off toward the corners, about a third of a stop at f/4 (cos^4 law,
  softened), so the eye stays in the frame;
- **ca**: lateral chromatic aberration, red and blue scaled about the centre by a fraction of a pixel at the corners,
  as an uncorrected wide lens does; at 1:1 it fringes the high-contrast edges at the frame's edge and nothing else.

Every amount is small on purpose: the frame must look photographed, not filtered.
"""
import argparse

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates


def s2l(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def l2s(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('inp'); ap.add_argument('out')
    ap.add_argument('--chroma', type=float, default=1.6)
    ap.add_argument('--halation', type=float, default=0.10)
    ap.add_argument('--knee', type=float, default=0.55, help='linear level above which light spreads')
    ap.add_argument('--vignette', type=float, default=0.18)
    ap.add_argument('--ca', type=float, default=0.6, help='pixels of red/blue shift at the corners, at 2400 wide')
    a = ap.parse_args()
    im = np.asarray(Image.open(a.inp).convert('RGB')).astype(np.float64) / 255.0
    h, w, _ = im.shape
    k = w / 2400.0
    if a.chroma > 0:                                                  # in sRGB, as a camera's pipeline does it
        y = im @ np.array([0.299, 0.587, 0.114])
        cb = gaussian_filter(im[..., 2] - y, a.chroma * k); cr = gaussian_filter(im[..., 0] - y, a.chroma * k)
        r = y + cr; b = y + cb; g = (y - 0.299 * r - 0.114 * b) / 0.587
        im = np.clip(np.stack([r, g, b], -1), 0, 1)
    lin = s2l(im)
    if a.halation > 0:
        hi = np.clip(lin - a.knee, 0, None)
        glow = sum(gaussian_filter(hi, sigma=(s * k, s * k, 0)) * wt for s, wt in ((6, 0.5), (24, 0.35), (70, 0.15)))
        glow *= np.array([1.0, 0.82, 0.62])                           # the warm fringe of a real lens's flare
        lin = lin + a.halation * glow
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    cx, cy = (w - 1) / 2, (h - 1) / 2
    r = np.hypot((xx - cx) / cx, (yy - cy) / cx)                      # 1 at the frame's side edges
    if a.vignette > 0:
        lin = lin * (1 - a.vignette * np.clip(r / 1.2, 0, 1) ** 2.2)[..., None]
    if a.ca > 0:
        out = np.empty_like(lin)
        rmax = np.hypot(1, h / w)
        for ch, sgn in ((0, 1), (1, 0), (2, -1)):
            if sgn == 0:
                out[..., ch] = lin[..., ch]; continue
            sc = 1 + sgn * a.ca * k / (cx * rmax)
            out[..., ch] = map_coordinates(lin[..., ch], [cy + (yy - cy) / sc, cx + (xx - cx) / sc], order=1, mode='nearest')
        lin = out
    Image.fromarray((l2s(lin) * 255 + 0.5).astype(np.uint8)).save(a.out, optimize=True)


if __name__ == '__main__':
    main()
