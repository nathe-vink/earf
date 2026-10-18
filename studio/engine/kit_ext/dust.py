"""Dust's own kit pieces (round 31, spinoffs/barkhorn/dioramas/dust.py).

- dunes: a sheet of corduroy laid over ridges, as a model-maker would drape cloth over a carved former: each ridge a long
  gentle windward slope and a steeper slip face, its crest wandering and rising and falling along its length; the sheet
  fades into the floor at its edges. `size` [w, d] (x, y), `ridges` [[y, height, width], ...] in the sheet's own frame
  (y from -d/2 to d/2), `wander` (m), `seed`, `res`.
- strata: a mesa of cut suede, irregular slabs stacked with an inset at each: `radius` (m), `height` (m), `layers`
  [colour, ...] from the foot up (the first is the talus, wider and low), `squash` (y over x), `seed`. Returns one object
  per layer (each its own colour).
- tumbleweed: a loose ball of tangled raffia, as a model-maker winds one: `count` strands, each a soft curve wandering
  through random points in a ball of `radius`, most near its shell so it reads hollow and airy; `strand` the strands'
  radius, `seed`.
"""
import math, random

import bmesh
from mathutils import Vector


def _smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def dunes(bpy, name, p, kit):
    w, d = p.get('size', [8.0, 3.0])
    ridges = p.get('ridges', [[0.0, 0.4, 0.8]])
    wander, res = p.get('wander', 0.25), p.get('res', 180)
    rnd = random.Random(p.get('seed', 1))
    ph = [[rnd.uniform(0, 6.283) for _ in range(4)] for _ in ridges]
    nu, nv = res, max(12, int(res * d / w))
    bm = bmesh.new()
    grid = []
    for j in range(nv + 1):
        y = (j / nv - 0.5) * d
        row = []
        for i in range(nu + 1):
            x = (i / nu - 0.5) * w
            u = i / nu
            h = 0.0
            for (yr, A, W), q in zip(ridges, ph):
                yc = yr + wander * (math.sin(x * 0.9 + q[0]) + 0.4 * math.sin(x * 2.1 + q[1]))
                a = A * (0.7 + 0.3 * math.sin(x * 0.7 + q[2]))
                s = (y - yc) / W
                # the windward slope faces the camera (-y), the slip face falls away behind the crest
                prof = math.exp(-(s / 1.0) ** 2) if s < 0 else math.exp(-(s / 0.5) ** 2)
                h = max(h, a * prof) if p.get('max', True) else h + a * prof
            edge = _smooth(min(u, 1 - u) / 0.12) * _smooth(min(j / nv, 1 - j / nv) / 0.15)
            row.append(bm.verts.new((x, y, h * edge - 0.012 * (1 - edge))))
        grid.append(row)
    for j in range(nv):
        for i in range(nu):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return kit.finish(bpy, name, bm, p)


def _blob(R, squash, rnd, n=72):
    a = [rnd.uniform(0, 6.283) for _ in range(3)]
    k = [rnd.uniform(0.07, 0.13), rnd.uniform(0.04, 0.08), rnd.uniform(0.02, 0.05)]
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = R * (1 + k[0] * math.sin(2 * t + a[0]) + k[1] * math.sin(3 * t + a[1]) + k[2] * math.sin(5 * t + a[2]))
        pts.append((r * math.cos(t), r * math.sin(t) * squash))
    return pts


def strata(bpy, name, p, kit):
    R, H = p.get('radius', 1.0), p.get('height', 1.0)
    layers = p.get('layers', ['#B5533A'])
    squash, ease = p.get('squash', 0.7), p.get('ease', 0.012)
    rnd = random.Random(p.get('seed', 1))
    base = _blob(1.0, squash, rnd)
    x0, y0, z0 = p.get('position', [0, 0, 0])
    objs, z = [], -0.01
    n = len(layers) - 1
    for i, c in enumerate(layers):
        if i == 0:                                     # the talus: wide, low and rounded over like a scree slope
            r, t = R * 1.42, H * 0.2
        else:
            r, t = R * (0.985 ** i) * rnd.uniform(0.97, 1.0), (H * 0.86) / n * rnd.uniform(0.8, 1.2)
        jitter = rnd.uniform(-0.03, 0.03) * R
        bm = bmesh.new()
        vs = [bm.verts.new((x * r + jitter, y * r, 0.0)) for x, y in base]
        f = bm.faces.new(vs)
        bmesh.ops.recalc_face_normals(bm, faces=[f])
        if f.normal.z < 0:
            f.normal_flip()
        ext = bmesh.ops.extrude_face_region(bm, geom=[f])
        moved = [e for e in ext['geom'] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=Vector((0, 0, t)), verts=moved)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        rings = [e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) < 1e-6]
        bmesh.ops.bevel(bm, geom=rings, offset=(t * 0.48 if i == 0 else min(ease, t * 0.4)), segments=(5 if i == 0 else 3), affect='EDGES')
        q = dict(p, color=c, position=[x0, y0, z0 + z], shape='strata')
        objs += kit.finish(bpy, f'{name}-{i}', bm, q, smooth=True)
        z += t * 0.995
    return objs


def tumbleweed(bpy, name, p, kit):
    R, n, sr = p.get('radius', 0.25), p.get('count', 90), p.get('strand', 0.0035)
    rnd = random.Random(p.get('seed', 1))

    def point():
        while True:
            v = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)))
            if 0.05 < v.length <= 1.0:
                break
        r = R * (0.55 + 0.45 * rnd.random() ** 0.5)          # mostly toward the shell
        return v.normalized() * r

    bm = bmesh.new()
    for _ in range(n):
        a = point()
        pts = [a]
        for _ in range(rnd.randint(3, 5)):                   # each strand curls on round the ball
            b = point()
            pts.append((pts[-1] * 0.45 + b * 0.55).normalized() * b.length)
        kit._tube(bm, [list(q) for q in pts], sr * rnd.uniform(0.7, 1.3), 1.0, 0.0, 6, 6)
    return kit.finish(bpy, name, bm, p)
