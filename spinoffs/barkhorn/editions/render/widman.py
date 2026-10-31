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


def make(path, w_mm=70.0, h_mm=52.0, px_per_mm=26, seed=11, band=(0.22, 0.55), tries=20000):
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
        L = rnd.uniform(8, 40)
        wdt = rnd.uniform(*band)
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
            if hi - lo < 5.0:                            # too short a run: real plates are long, so skip it
                continue
            free = free & (s > lo + 0.05) & (s < hi - 0.05)
        own[free] = i
        v = tone[i] + 0.05 * math.sin(drift[i] + (cx * ux + cy * uy) * 0.15) + rnd.uniform(-0.025, 0.025)
        sub = img[y0:y1, x0:x1]
        sub[free] = v + 0.02 * rng.standard_normal(int(free.sum())).astype(np.float32)
    # taenite: a hairline bright border wherever two plates of different families meet, or a plate meets plessite
    o = owner
    edge = np.zeros((H, W), bool)
    edge[:, 1:] |= (o[:, 1:] != o[:, :-1])
    edge[1:, :] |= (o[1:, :] != o[:-1, :])
    img = np.where(edge, 0.9, img)
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
