"""An etched octahedrite's face as an image (v2, after the Iron critic's round 2: v1 drew outlined bars that overlapped
and read as "stacked translucent bars", not etched iron).

How the real pattern forms, and so how it is drawn: as the iron cooled, kamacite plates grew along the octahedron's
four plane sets; a slice cuts them as three or four families of straight bands. Plates stop where they meet a plate
already grown, so bands interlock and butt into each other rather than cross. Between plates, the last nickel-rich
taenite is a hairline border, bright after the etch; the leftover fields are plessite, a fine dark mottle. After the
acid etch each family catches light at its own angle, so a family reads as one tone with a slight drift along it.
Gibeon is a fine octahedrite (bandwidth about 0.3 mm in the Meteoritical Bulletin's class Of); at the scale of a
62 mm slice the bands are drawn 0.35 to 0.9 mm wide.
"""
import math
import random
import subprocess

import numpy as np


def make(path, w_mm=70.0, h_mm=52.0, px_per_mm=26, seed=11, band=(0.12, 0.34), tries=32000):
    W, H = int(w_mm * px_per_mm), int(h_mm * px_per_mm)
    rnd = random.Random(seed)
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32) / px_per_mm
    # plessite: a fine dark mottle
    g = rng.standard_normal((H // 3 + 1, W // 3 + 1)).astype(np.float32)
    img = 0.17 + 0.035 * np.kron(g, np.ones((3, 3), np.float32))[:H, :W]
    owner = np.full((H, W), -1, np.int16)                 # which family holds each pixel
    a0 = rnd.uniform(0, 180)
    dirs = [a0, a0 + 58 + rnd.uniform(-3, 3), a0 + 121 + rnd.uniform(-3, 3)]
    tone = [0.78, 0.44, 0.60]                            # each family's brightness after the etch
    drift = [rnd.uniform(0, 6.28) for _ in dirs]
    for k in range(tries):
        i = rnd.randrange(3)
        a = math.radians(dirs[i] + rnd.gauss(0, 0.6))
        ux, uy = math.cos(a), math.sin(a)
        cx, cy = rnd.uniform(0, w_mm), rnd.uniform(0, h_mm)
        L = rnd.uniform(6, 30)
        wdt = min(max(rnd.lognormvariate(math.log((band[0] * band[1]) ** 0.5), 0.42), 0.08), 1.6)   # lognormal widths, a few swathing bands
        r = L / 2 + 1
        x0, x1 = max(int((cx - r) * px_per_mm), 0), min(int((cx + r) * px_per_mm), W)
        y0, y1 = max(int((cy - r) * px_per_mm), 0), min(int((cy + r) * px_per_mm), H)
        if x0 >= x1 or y0 >= y1:
            continue
        X, Y = xx[y0:y1, x0:x1] - cx, yy[y0:y1, x0:x1] - cy
        s = X * ux + Y * uy
        t = -X * uy + Y * ux
        inside = (np.abs(s) < L / 2) & (np.abs(t) < wdt / 2)
        own = owner[y0:y1, x0:x1]
        # grow from the centre outward until the plate meets another: keep the run along s that is free
        free = inside & (own < 0)
        if free.sum() < 0.35 * max(inside.sum(), 1):
            continue
        # stop the plate at the first occupied pixel each way along its axis (a butt joint, not a crossing)
        blocked = inside & (own >= 0)
        if blocked.any():
            sb = s[blocked]
            lo = sb[sb < 0].max() if (sb < 0).any() else -L / 2
            hi = sb[sb > 0].min() if (sb > 0).any() else L / 2
            if hi - lo < 3.5:                            # too short a run: real plates are long, so skip it
                continue
            free = free & (s > lo + 0.05) & (s < hi - 0.05)
        own[free] = i
        v = tone[i] + 0.07 * math.sin(drift[i] + (cx * ux + cy * uy) * 0.15) + rnd.uniform(-0.06, 0.06)
        sub = img[y0:y1, x0:x1]
        sub[free] = v + 0.02 * rng.standard_normal(int(free.sum())).astype(np.float32)
    # taenite: a hairline bright border wherever two plates of different families meet, or a plate meets plessite
    o = owner
    edge = np.zeros((H, W), bool)
    edge[:, 1:] |= (o[:, 1:] != o[:, :-1])
    edge[1:, :] |= (o[1:, :] != o[:-1, :])
    img = np.where(edge, 0.9, img)
    # a slight domain warp: the plates bend a little, as real ones do, so the figure does not tile
    def smooth_noise(scale_px, amp_px):
        g = rng.standard_normal((H // scale_px + 2, W // scale_px + 2)).astype(np.float32)
        yi = np.linspace(0, g.shape[0] - 1.001, H); xi = np.linspace(0, g.shape[1] - 1.001, W)
        y0 = yi.astype(int); x0 = xi.astype(int); fy = (yi - y0)[:, None]; fx = (xi - x0)[None, :]
        a = g[y0][:, x0]; b = g[y0][:, x0 + 1]; c = g[y0 + 1][:, x0]; d = g[y0 + 1][:, x0 + 1]
        return amp_px * ((a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy)
    dx = smooth_noise(220, 5.0); dy = smooth_noise(220, 5.0)
    Y, X = np.mgrid[0:H, 0:W]
    img = img[np.clip((Y + dy).astype(int), 0, H - 1), np.clip((X + dx).astype(int), 0, W - 1)]
    out = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    pgm = path + '.pgm'
    with open(pgm, 'wb') as f:                   # written as PGM and converted (the system PIL is not this Python's)
        f.write(b'P5 %d %d 255\n' % (W, H))
        f.write(np.ascontiguousarray(out[::-1]).tobytes())
    subprocess.run(['convert', pgm, '-blur', '0x0.6', path], check=True)
    import os
    os.remove(pgm)
    return path


if __name__ == '__main__':
    import sys
    make(sys.argv[1])
