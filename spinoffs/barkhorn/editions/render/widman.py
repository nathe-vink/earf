"""An etched octahedrite's face as an image: kamacite lamellae laid down in three directions 60 degrees apart (a slice
cuts the octahedron's four plane sets as three or four), each set bright or dark by how its crystal faces catch the
light after the etch, edged with thin bright taenite, over a fine dark plessite ground. Gibeon is a fine octahedrite:
its bands are about 0.3 mm wide (the Meteoritical Bulletin's class, Of), so at slice scale the pattern is fine."""
import math
import random

import numpy as np


def make(path, w_mm=70.0, h_mm=52.0, px_per_mm=24, seed=11, band=(0.45, 1.2), n=1500):
    W, H = int(w_mm * px_per_mm), int(h_mm * px_per_mm)
    rnd = random.Random(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32) / px_per_mm
    # plessite: fine mottled grey
    rng = np.random.default_rng(seed)
    ground = 0.30 + 0.05 * rng.standard_normal((H // 4 + 1, W // 4 + 1)).astype(np.float32)
    ground = np.kron(ground, np.ones((4, 4), np.float32))[:H, :W]
    img = ground.copy()
    edge = np.zeros_like(img)
    dirs = [rnd.uniform(0, 180)]
    dirs += [dirs[0] + 60 + rnd.uniform(-4, 4), dirs[0] + 120 + rnd.uniform(-4, 4)]
    tone = [0.86, 0.46, 0.66]                  # each set's brightness after the etch
    for k in range(n):
        i = rnd.randrange(3)
        a = math.radians(dirs[i])
        ux, uy = math.cos(a), math.sin(a)
        cx, cy = rnd.uniform(0, w_mm), rnd.uniform(0, h_mm)
        L = rnd.uniform(4, 26)
        wdt = rnd.uniform(*band)
        # a window round the lamella to keep it cheap
        r = L / 2 + 1
        x0, x1 = max(int((cx - r) * px_per_mm), 0), min(int((cx + r) * px_per_mm), W)
        y0, y1 = max(int((cy - r) * px_per_mm), 0), min(int((cy + r) * px_per_mm), H)
        if x0 >= x1 or y0 >= y1:
            continue
        X, Y = xx[y0:y1, x0:x1] - cx, yy[y0:y1, x0:x1] - cy
        s = X * ux + Y * uy
        t = -X * uy + Y * ux
        inside = (np.abs(s) < L / 2) & (np.abs(t) < wdt / 2)
        rim = (np.abs(s) < L / 2 + 0.05) & (np.abs(t) < wdt / 2 + 0.05) & ~inside
        v = tone[i] + rnd.uniform(-0.05, 0.05)
        sub = img[y0:y1, x0:x1]
        sub[inside] = v
        e = edge[y0:y1, x0:x1]
        e[rim] = 1.0
        e[inside] = 0.0
    img = np.where(edge > 0, 0.80, img)
    # a slight sheen variation across the slice, as an etch never lands evenly
    img *= (0.92 + 0.08 * np.sin(xx / w_mm * 3.0 + 0.7) * np.cos(yy / h_mm * 2.0))
    out = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    import subprocess
    pgm = path + '.pgm'
    with open(pgm, 'wb') as f:                  # written as PGM and converted (the system PIL is not this Python's)
        f.write(b'P5 %d %d 255\n' % (W, H))
        f.write(np.ascontiguousarray(out[::-1]).tobytes())
    subprocess.run(['convert', pgm, path], check=True)
    import os
    os.remove(pgm)
    return path


if __name__ == '__main__':
    import sys
    make(sys.argv[1])
