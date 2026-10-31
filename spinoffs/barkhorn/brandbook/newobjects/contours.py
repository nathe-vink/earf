"""Relief's landscape: a heightfield of a few hills, contoured into closed loops by marching squares (numpy only;
matplotlib is not installed beside Blender's numpy, and must not be). Coordinates in mm on the 600 x 600 panel,
origin at its centre. Used by the drawing and the render, so both show the same contours."""
import numpy as np

SIZE, N, LEVELS = 600.0, 161, 12
HILLS = [(-120, 80, 105, 1.0), (140, -70, 85, 0.85), (-30, -175, 60, 0.55), (175, 165, 55, 0.5), (-200, -70, 55, 0.4), (30, 60, 140, 0.18)]

def height(x, y):
    h = np.zeros_like(x)
    for cx, cy, s, a in HILLS:
        h += a * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * s ** 2))
    r = np.maximum(np.abs(x), np.abs(y))
    return h * np.clip((SIZE / 2 - 14 - r) / 30, 0, 1)   # fall to nothing before the edge, so every loop closes inside

def grid():
    xs = np.linspace(-SIZE / 2, SIZE / 2, N)
    X, Y = np.meshgrid(xs, xs)
    return xs, height(X, Y)

def _segments(xs, H, lev):
    segs = []
    d = xs[1] - xs[0]
    for j in range(N - 1):
        for i in range(N - 1):
            v = [H[j, i], H[j, i + 1], H[j + 1, i + 1], H[j + 1, i]]
            c = sum(1 << k for k in range(4) if v[k] >= lev)
            if c in (0, 15):
                continue
            pts = []
            corners = [(xs[i], xs[j]), (xs[i] + d, xs[j]), (xs[i] + d, xs[j] + d), (xs[i], xs[j] + d)]
            for k in range(4):
                a, b = k, (k + 1) % 4
                if (v[a] >= lev) != (v[b] >= lev):
                    t = (lev - v[a]) / (v[b] - v[a])
                    pa, pb = corners[a], corners[b]
                    pts.append((round(pa[0] + t * (pb[0] - pa[0]), 6), round(pa[1] + t * (pb[1] - pa[1]), 6)))
            if len(pts) == 2:
                segs.append(tuple(pts))
            elif len(pts) == 4:   # saddle: pair in order
                segs.append((pts[0], pts[1])); segs.append((pts[2], pts[3]))
    return segs

def _join(segs):
    adj = {}
    for a, b in segs:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    seen, loops = set(), []
    for start in list(adj):
        if start in seen:
            continue
        loop, prev, cur = [start], None, start
        seen.add(start)
        while True:
            nxt = [p for p in adj[cur] if p != prev and p not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            seen.add(cur); loop.append(cur)
        if len(loop) > 8:
            loops.append(loop)
    return loops

def _chaikin(loop, n=2):
    p = np.array(loop)
    for _ in range(n):
        q = 0.75 * p + 0.25 * np.roll(p, -1, 0); r = 0.25 * p + 0.75 * np.roll(p, -1, 0)
        p = np.empty((2 * len(q), 2)); p[0::2] = q; p[1::2] = r
    return p[::2]

def layers():
    """[(level index 1..LEVELS, [loop as Nx2 array mm, ...]), ...]"""
    xs, H = grid()
    top = H.max()
    out = []
    for k in range(1, LEVELS + 1):
        lev = top * (k - 0.5) / (LEVELS + 0.4)
        out.append((k, [_chaikin(l) for l in _join(_segments(xs, H, lev))]))
    return out

if __name__ == '__main__':
    for k, ls in layers():
        print(k, len(ls), [len(l) for l in ls])
