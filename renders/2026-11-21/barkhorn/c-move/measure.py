"""C's Core against the lamps lane's studio Core OFF (r32-lamps-final 35d059fec, house7/core-ember-off.png): medians of
CIELAB in the ball's whole disc, its lower middle and the base's centre, scaled to the frame's size, with CIEDE2000 to
the studio's. The camera and the Core move together in the move tests, so the regions hold.
    python3 measure.py STUDIO_PNG FRAME.png ..."""
import sys, numpy as np
from PIL import Image
def lab(p):
    a = np.asarray(Image.open(p).convert('RGB')).astype(float) / 255
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    X = lin @ M.T / np.array([0.95047, 1, 1.08883]); f = np.where(X > 216 / 24389, np.cbrt(X), (24389 / 27 * X + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)
def de00(l1, l2):
    L1, a1, b1 = l1; L2, a2, b2 = l2
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2); Cb = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7))); a1p, a2p = a1 * (1 + G), a2 * (1 + G)
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2); h1 = np.degrees(np.arctan2(b1, a1p)) % 360; h2 = np.degrees(np.arctan2(b2, a2p)) % 360
    dL, dC = L2 - L1, C2p - C1p; dh = h2 - h1
    dh = dh - 360 if dh > 180 else dh + 360 if dh < -180 else dh
    dH = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dh / 2)); Lb, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    hb = (h1 + h2) / 2 + (180 if abs(h1 - h2) > 180 else 0)
    T = 1 - 0.17 * np.cos(np.radians(hb - 30)) + 0.24 * np.cos(np.radians(2 * hb)) + 0.32 * np.cos(np.radians(3 * hb + 6)) - 0.2 * np.cos(np.radians(4 * hb - 63))
    SL = 1 + 0.015 * (Lb - 50) ** 2 / np.sqrt(20 + (Lb - 50) ** 2); SC = 1 + 0.045 * Cbp; SH = 1 + 0.015 * Cbp * T
    RT = -2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) * np.sin(np.radians(60 * np.exp(-((hb - 275) / 25) ** 2)))
    return float(np.sqrt((dL / SL) ** 2 + (dC / SC) ** 2 + (dH / SH) ** 2 + RT * (dC / SC) * (dH / SH)))
def disc(H, W, cx, cy, r):
    Y, X = np.ogrid[:H, :W]; return (X - cx) ** 2 + (Y - cy) ** 2 <= r * r
def measure(p, ball, lower, centre):
    Lab = lab(p); H, W = Lab.shape[:2]; k = W / (1000 if ball[2] == 400 else 1600)
    if ball[2] == 400: k = 1.0
    sel = {'ball, whole disc': disc(H, W, ball[0] * k, ball[1] * k, ball[2] * k),
           'ball, lower middle': (slice(int(lower[1] * k), int(lower[3] * k)), slice(int(lower[0] * k), int(lower[2] * k))),
           'base centre': (slice(int(centre[1] * k), int(centre[3] * k)), slice(int(centre[0] * k), int(centre[2] * k)))}
    return {n: np.median(Lab[s].reshape(-1, 3), 0) for n, s in sel.items()}
fmt = lambda v: f'{v[0]:.1f} / {np.hypot(v[1], v[2]):.1f} / {np.degrees(np.arctan2(v[2], v[1])):.0f}'
st = measure(sys.argv[1], (822, 1045, 400), (700, 1180, 940, 1320), (760, 1500, 880, 1580))
print('| | ' + ' | '.join(st) + ' |\n|---|---|---|---|')
print('| studio (house7) | ' + ' | '.join(fmt(st[n]) for n in st) + ' |')
for p in sys.argv[2:]:
    r = measure(p, (720, 1110, 170), (660, 1160, 780, 1230), (690, 1320, 750, 1380))
    print(f'| {p.split("/")[-1]} | ' + ' | '.join(f'{fmt(r[n])}, dE {de00(st[n], r[n]):.1f}' for n in st) + ' |')
