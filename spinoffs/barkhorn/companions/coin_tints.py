"""EARFcoin's tint check (round 33): each coin's lit colour in a render of the eight (coin_shots.py tints), against its
speaker's swatch (earth._C), in CIE LCh. The hue must land within 10 degrees of the swatch's; the owner caught a lamp
lineup reading "two reds and an orange", so the neighbours' hues are printed too.

    python3.11 spinoffs/barkhorn/companions/coin_tints.py renders/2026-10-20/barkhorn/coin/tints.png
"""
import json, math, os, sys

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
SPECTRUM = ['Ember', 'Dust', 'Acid', 'Poison', 'Ice', 'Haze', 'Fog', 'Smoke']
SWATCH = {'Ember': '#D2382F', 'Dust': '#E5732A', 'Acid': '#E9B320', 'Poison': '#4F7F3A', 'Ice': '#4A90C8',
          'Haze': '#6C4BA3', 'Fog': '#F6F8F8', 'Smoke': '#34323A'}          # earth._C


def lch(rgb):
    c = np.asarray(rgb, float) / 255
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = M @ c / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    L, a, b = 116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def project(shot, pts, W, H):
    """World points to pixels through the shot's camera (render.py: horizontal sensor fit, 36 mm, no shift)."""
    c = shot['camera']
    P, Tg = np.array(c['position'], float), np.array(c['target'], float)
    f = -(Tg - P) / np.linalg.norm(Tg - P)                 # the camera's +z (it looks down -z)
    r = np.cross([0, 0, 1.0], f); r /= np.linalg.norm(r)
    u = np.cross(f, r)
    fpx = c.get('lens_mm', 50) / c.get('sensor_mm', 36.0) * W
    out = []
    for q in pts:
        d = np.array(q, float) - P
        x, y, z = d @ r, d @ u, d @ f
        out.append((W / 2 + fpx * x / -z, H / 2 - fpx * y / -z, fpx / -z))
    return out


def coins(img):
    """The coins' median colours, left to right, each sampled inside 0.55 of its radius (inside the words; the globe's
    lines a few per cent of it), found from the shot written beside the render."""
    v = np.asarray(Image.open(img).convert('RGB')).astype(float)
    H, W = v.shape[:2]
    shot = json.load(open(img[:-4] + '.shot.json'))
    spots = [sp['position'] for pr in shot['set']['props'] if pr.get('fn') == 'coin' for sp in pr['spots']]
    yy, xx = np.mgrid[:H, :W]
    out = []
    for (x, y, k) in project(shot, [[a, b, c + 0.006] for a, b, c in spots], W, H):
        out.append(np.median(v[np.hypot(yy - y, xx - x) < 0.020 * k * 0.55], axis=0))
    return out


def main(img):
    rows = []
    for name, rgb in zip(SPECTRUM, coins(img)):
        L, C, h = lch(rgb)
        sw = SWATCH[name]
        Ls, Cs, hs = lch([int(sw[i:i + 2], 16) for i in (1, 3, 5)])
        dh = (h - hs + 180) % 360 - 180
        rows.append(dict(tint=name, lit='#%02X%02X%02X' % tuple(int(x) for x in rgb), L=round(L, 1), C=round(C, 1),
                         h=round(h, 1), swatch=sw, swatch_h=round(hs, 1), swatch_C=round(Cs, 1), dh=round(dh, 1),
                         ok=bool(abs(dh) <= 10 or (Cs < 8 and C < 12))))
    for r in rows:
        print(f"{r['tint']:7s} lit {r['lit']} L{r['L']:5.1f} C{r['C']:5.1f} h{r['h']:6.1f} | swatch {r['swatch']} h{r['swatch_h']:6.1f} "
              f"C{r['swatch_C']:5.1f} | dh {r['dh']:+6.1f} {'ok' if r['ok'] else 'OFF'}")
    return rows


if __name__ == '__main__':
    rows = main(sys.argv[1])
    if len(sys.argv) > 2:
        json.dump(rows, open(sys.argv[2], 'w'), indent=1)
