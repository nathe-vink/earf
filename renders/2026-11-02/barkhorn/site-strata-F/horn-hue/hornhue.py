"""Median hue and luminance of the horn against the cabinet's front panel above the woofer, front-off-tall framing.
Boxes are fractions of the frame (from the 1000 x 1250 final); the horn box inset 12 % at the sides, 15 % top, 20 % bottom."""
import sys, colorsys; from PIL import Image; import numpy as np
HORN = (0.300, 0.148, 0.625, 0.336)     # x0, y0, x1, y1 of the horn's mouth face
CAB = (0.330, 0.375, 0.600, 0.430)      # the front panel above the woofer
def box(a, b, inset=None):
    H, W = a.shape[:2]; x0, y0, x1, y1 = b
    if inset:
        w, h = x1 - x0, y1 - y0; x0 += w * inset[0]; x1 -= w * inset[0]; y0 += h * inset[1]; y1 -= h * inset[2]
    return a[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)].reshape(-1, 3)
def stats(px):
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in px / 255.0])
    m = (hsv[:, 1] > 0.3) & (hsv[:, 2] > 0.25) & (hsv[:, 2] < 0.95)
    h = hsv[m, 0] * 360; z = np.exp(1j * np.radians(h)); c = np.degrees(np.angle(z.mean()))
    d = (h - c + 180) % 360 - 180; hue = (c + np.median(d) + 180) % 360 - 180
    lin = np.where(px / 255 <= 0.04045, px / 255 / 12.92, ((px / 255 + 0.055) / 1.055) ** 2.4)
    Y = (lin @ [0.2126, 0.7152, 0.0722]).mean()
    return hue, Y, m.mean()
for f in sys.argv[1:]:
    a = np.asarray(Image.open(f).convert('RGB')).astype(float)
    h, Yh, fh = stats(box(a, HORN, (0.12, 0.15, 0.20))); c, Yc, fc = stats(box(a, CAB))
    print(f'{f.split("/")[-1]}: horn hue {h:.0f} Y {Yh:.3f} ({fh:.0%} sat px) | cabinet hue {c:.0f} Y {Yc:.3f} | diff {((h - c + 180) % 360 - 180):+.0f}')
