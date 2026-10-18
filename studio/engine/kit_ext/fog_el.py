"""Fog's own pieces for round 31b (in their element: the speaker on a summit above a sea of clouds).

- cloudsea: the top of a cloud deck seen from above, from `near` to `far` metres beyond the ledge (y), `width` across,
  its mean top at `z`, heaped into billows by layered noise (`billow` metres across the big heaps, `height` metres from
  trough to crest), deep-scattering white so it glows where the sun lights it and goes blue-grey in its troughs. The grid
  grows coarser with distance, so it is fine where it is near.
- bird: a bird far off in flight, a dark silhouette of swept wings `span` metres across, `flap` -1 (down) to 1 (up).

Called by kit.py as fn(bpy, name, p, kit); each returns its objects.
"""
import math, random

import bmesh
from mathutils import Vector, noise


def _domes(p, seed):
    """Cumulus heaps: in each cell of a grid `billow` metres across, one big dome and a few small ones riding on it
    (the cauliflower tops), each a squashed sphere cap; the surface is the highest cap over a point."""
    rnd = random.Random(seed)
    b = p.get('billow', 40.0); H = p.get('height', 12.0)
    cells = {}
    def cell(i, j):
        k = (i, j)
        if k not in cells:
            r = random.Random(hash((i, j, seed)) & 0xffffffff)
            cx, cy = (i + r.uniform(0.2, 0.8)) * b, (j + r.uniform(0.2, 0.8)) * b
            R = b * r.uniform(0.55, 0.85); h = H * r.uniform(0.45, 1.0)
            d = [(cx, cy, R, h, 0.0)]
            for _ in range(r.randint(2, 4)):
                a = r.uniform(0, 6.283); q = r.uniform(0.15, 0.55) * R
                rr = R * r.uniform(0.22, 0.42)
                base = h * (1 - (q / R) ** 2) ** 0.5 * 0.82          # sits on the big dome's surface there
                d.append((cx + q * math.cos(a), cy + q * math.sin(a), rr, rr * 0.75 * H / b * 2.2, base))
            cells[k] = d
        return cells[k]
    def height(x, y):
        i, j = math.floor(x / b), math.floor(y / b)
        top = 0.0
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for cx, cy, R, h, base in cell(i + di, j + dj):
                    d2 = (x - cx) ** 2 + (y - cy) ** 2
                    if d2 < R * R:
                        top = max(top, base + h * (1 - d2 / (R * R)) ** 0.5)
        return top
    return height


def cloudsea(bpy, name, p, kit):
    near, far, width = p.get('near', 8.0), p.get('far', 1500.0), p.get('width', 2400.0)
    z0 = p.get('z', -30.0)
    cx = p.get('x', 0.0)
    height = _domes(p, p.get('seed', 1))
    ny = p.get('rows', 260)
    nx = p.get('cols', 360)
    # rows spaced geometrically from near to far; columns widening with distance (a fan of the frame's width)
    ys = [near * (far / near) ** (j / (ny - 1)) for j in range(ny)]
    bm = bmesh.new()
    top, bot = [], []
    for y in ys:
        w = min(width, max(60.0, y * p.get('fan', 2.4)))
        rt, rb = [], []
        for i in range(nx):
            x = cx + (i / (nx - 1) - 0.5) * w
            rt.append(bm.verts.new((x, y, z0 + height(x, y))))
            rb.append(bm.verts.new((x, y, z0 - p.get('depth', 25.0))))
        top.append(rt); bot.append(rb)
    for j in range(ny - 1):
        for i in range(nx - 1):
            bm.faces.new((top[j][i], top[j][i + 1], top[j + 1][i + 1], top[j + 1][i]))
            bm.faces.new((bot[j][i], bot[j + 1][i], bot[j + 1][i + 1], bot[j][i + 1]))
    # close it into a slab (subsurface light needs a closed body)
    for j in range(ny - 1):
        for i in (0, nx - 1):
            bm.faces.new((top[j][i], top[j + 1][i], bot[j + 1][i], bot[j][i]))
    for i in range(nx - 1):
        for j in (0, ny - 1):
            bm.faces.new((top[j][i], bot[j][i], bot[j][i + 1], top[j][i + 1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    kit._set(b, 'Base Color', kit.M.hex_lin(p.get('color', '#F4F6F8')))
    kit._set(b, 'Roughness', 1.0); kit._set(b, 'Specular IOR Level', 0.0)
    kit._set(b, 'Subsurface Weight', p.get('sss', 1.0))
    kit._set(b, 'Subsurface Radius', Vector((1.0, 1.0, 1.0)))
    kit._set(b, 'Subsurface Scale', p.get('sss_r', 8.0))
    kit._set(b, 'Sheen Weight', p.get('sheen', 0.5)); kit._set(b, 'Sheen Roughness', 0.9)
    # fine detail on the heaps: cauliflower bumps a few metres across
    kit._bump(m.node_tree, b, p.get('bump_size', 3.0), p.get('bump', 0.4), p.get('bump_dist', 1.0), detail=6.0)
    return kit.finish(bpy, name, bm, {**p, 'position': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': 1.0}, True, m)


def bird(bpy, name, p, kit):
    sp = p.get('span', 0.9)
    flap = p.get('flap', 0.0)
    def zf(a):
        return (0.16 + 0.2 * flap) * math.sin(math.pi * a) * (1 - 0.3 * a) - 0.06 * a * a + 0.05 * (1 - a) ** 8
    up, lo = [], []
    n = 16
    for i in range(n + 1):
        t = -1 + 2 * i / n; a = abs(t)
        up.append((t * sp / 2, zf(a) * sp))
        lo.append((t * sp / 2, (zf(a) - (0.01 + 0.08 * (1 - a) ** 1.6)) * sp))
    bm = bmesh.new()
    kit._extrude(bm, up + lo[::-1], p.get('depth', 0.03), 0.0)
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    kit._set(b, 'Base Color', kit.M.hex_lin(p.get('color', '#26282C'))); kit._set(b, 'Roughness', 0.8)
    return kit.finish(bpy, name, bm, p, False, m)
