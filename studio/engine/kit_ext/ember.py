"""Ember's own kit pieces (round 31, spinoffs/barkhorn/dioramas/ember.py): the icon's campfire cut from layered felt,
and a devil's toasting fork with a marshmallow on it.

    {"kind": "kit", "shape": "ext", "module": "ember", "fn": "campfire", "size": 0.6, ...}
    {"kind": "kit", "shape": "ext", "module": "ember", "fn": "fork", "length": 0.9, ...}
"""
import math

import bmesh
from mathutils import Matrix, Vector

# the icon (spinoffs/barkhorn/icons.py, ember()): a bar and three triangles standing on it, in icon units (y down)
BAR = (-260, 220, 260, 300)
FLAMES = [((-250, 260), (-30, 260), (-140, -150)), ((-120, 260), (120, 260), (0, -330)), ((30, 260), (250, 260), (140, -150))]


def rounded(pts, r, n=6):
    """A polygon with its corners filleted to radius `r` (a felt cutter's soft corners), [[x, z], ...]."""
    out = []
    k = len(pts)
    for i in range(k):
        p0, p1, p2 = Vector(pts[i - 1]), Vector(pts[i]), Vector(pts[(i + 1) % k])
        a, b = (p0 - p1).normalized(), (p2 - p1).normalized()
        half = math.acos(max(-1.0, min(1.0, a.dot(b)))) / 2
        d = r / math.tan(half)                                   # from the corner to where the arc meets each side
        c = p1 + (a + b).normalized() * (r / math.sin(half))
        s, e = p1 + a * d, p1 + b * d
        a0, a1 = math.atan2(s.y - c.y, s.x - c.x), math.atan2(e.y - c.y, e.x - c.x)
        da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        for j in range(n + 1):
            t = a0 + da * j / n
            out.append((c.x + r * math.cos(t), c.y + r * math.sin(t)))
    return out


def _shrink(tri, f):
    """The triangle scaled by f about its base's middle (an inner layer of felt, standing on the same base)."""
    bx, bz = (tri[0][0] + tri[1][0]) / 2, (tri[0][1] + tri[1][1]) / 2
    return [(bx + (x - bx) * f, bz + (z - bz) * f) for x, z in tri]


def campfire(bpy, name, p, kit):
    """The Ember icon as a model-maker would cut it: each flame three layers of felt (red, orange, a gold heart) stacked
    a few millimetres apart, standing on a felt log; `size` its width (m), `colors` the layers, `log` the log's colour,
    `emit` how much the felt glows (a fire lit from within)."""
    S = p.get('size', 0.6) / 520.0
    cols = p.get('colors', ['#C21A12', '#F0571B', '#FFB238'])
    th = p.get('thickness', 0.012)
    objs = []
    for fi, tri in enumerate(FLAMES):
        base = [(x * S, (300 - y) * S) for x, y in tri]     # the bar's underside at z = 0
        for li, (f, col) in enumerate(zip((1.0, 0.68, 0.38), cols)):
            pts = rounded(_shrink(base, f), 34 * S * (0.6 + 0.4 * f))
            bm = bmesh.new()
            kit._extrude(bm, pts, th, th * 0.35)
            y = -li * th * 0.9 + (0.0 if fi == 1 else th * 2.2)       # the middle flame in front, the inner layers forward
            bmesh.ops.translate(bm, vec=Vector((0, y, 0)), verts=bm.verts[:])
            q = {**p, 'material': 'felt', 'color': col, 'emit': p.get('emit', 0.6) * (0.5 + li * 0.6), 'emit_color': col}
            objs += kit.finish(bpy, f'{name}-f{fi}{li}', bm, q, smooth=False, mat=kit.piece_material(bpy, q))
    x0, y0, x1, y1 = BAR                                          # the bar: a felt log, its ends rounded
    L, R = (x1 - x0) * S, (y1 - y0) * S / 2
    bm = bmesh.new()
    kit._tube(bm, [((x0 * S) + R, th * 1.2, (300 - (y0 + y1) / 2) * S), ((x1 * S) - R, th * 1.2, (300 - (y0 + y1) / 2) * S)], R * 1.15, 0.8, 0, 20, 4)
    q = {**p, 'material': 'felt', 'color': p.get('log', '#2A0D0A'), 'emit': p.get('log_emit', 0.0), 'emit_color': '#FF4A12'}
    objs += kit.finish(bpy, f'{name}-log', bm, q, mat=kit.piece_material(bpy, q))
    return objs


def fork(bpy, name, p, kit):
    """A devil's toasting fork: a slim black handle, three tines on a crossbar, a marshmallow on the middle tine. It lies
    along +x from its position (rotate it to lean); `length` its length (m)."""
    L = p.get('length', 0.9)
    r = L * 0.016
    objs = []
    def tube(nm, pts, rad, q):
        bm = bmesh.new(); kit._tube(bm, pts, rad, 1.0, 0, 12, 4)
        return kit.finish(bpy, f'{name}-{nm}', bm, q, mat=kit.piece_material(bpy, q))
    metal = {**p, 'material': p.get('handle', 'card'), 'color': p.get('color', '#1A0A0A'), 'roughness': 0.35}
    tip = L * 0.78
    objs += tube('handle', [(0, 0, 0), (tip, 0, 0)], r, metal)
    w = L * 0.09
    objs += tube('bar', [(tip, 0, -w), (tip + w * 0.15, 0, -w * 0.4), (tip + w * 0.15, 0, w * 0.4), (tip, 0, w)], r * 0.8, metal)
    for z in (-w, 0.0, w):
        x0 = tip + (w * 0.15 if z == 0 else 0)
        objs += tube(f't{z:+.2f}', [(x0, 0, z), (L, 0, z * 1.05)], [r * 0.75, r * 0.35], metal)
    mq = {**p, 'material': 'cotton', 'color': '#EBCFA8', 'emit': 0.0}
    bm = bmesh.new()
    geom = bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=L * 0.05, radius2=L * 0.05, depth=L * 0.08)
    bmesh.ops.bevel(bm, geom=bm.edges[:], offset=L * 0.012, segments=3, affect='EDGES')
    bmesh.ops.rotate(bm, verts=bm.verts[:], cent=Vector((0, 0, 0)), matrix=Matrix.Rotation(math.pi / 2, 3, 'Y'))
    bmesh.ops.translate(bm, vec=Vector((L * 0.9, 0, 0)), verts=bm.verts[:])
    objs += kit.finish(bpy, f'{name}-mallow', bm, mq, mat=kit.piece_material(bpy, mq))
    # finish() placed every part at the fork's position and turn: they share one frame, so the fork holds together
    return objs


def pool(bpy, name, p, kit):
    """A pool of lava in satin: an irregular round sheet (`radius` [rx, ry], its edge wandering by `wobble`), rumpled in
    soft folds `amplitude` high, glowing; and its shore, a roll of velvet (`shore` its colour, `shore_r` its radius)
    along the edge. Lies in x-y at the piece's position."""
    import random
    rx, ry = p.get('radius', [1.0, 0.7])
    rnd = random.Random(p.get('seed', 0))
    ph = [rnd.uniform(0, 6.283) for _ in range(6)]
    wob = p.get('wobble', 0.12)
    def edge(t):
        return 1.0 + wob * (0.6 * math.sin(2 * t + ph[0]) + 0.3 * math.sin(3 * t + ph[1]) + 0.25 * math.sin(5 * t + ph[2]))
    amp, nr, ns = p.get('amplitude', 0.008), p.get('rings', 20), p.get('segments', 120)
    def height(x, y):
        return amp * (math.sin(x * 9.0 + ph[3] + 2.0 * math.sin(y * 5.0)) * 0.6 + math.sin(y * 13.0 + ph[4] + x * 3.0) * 0.4)
    bm = bmesh.new()
    centre = bm.verts.new((0, 0, height(0, 0)))
    rings = []
    for i in range(1, nr + 1):
        f = i / nr
        ring = []
        for k in range(ns):
            t = 2 * math.pi * k / ns
            e = edge(t) * f
            x, y = rx * e * math.cos(t), ry * e * math.sin(t)
            ring.append(bm.verts.new((x, y, height(x, y) * (1 - f ** 4) - p.get('tuck', 0.0) * f ** 6)))   # its hem tucked under
        rings.append(ring)
    for k in range(ns):
        bm.faces.new((centre, rings[0][k], rings[0][(k + 1) % ns]))
    for a, b in zip(rings, rings[1:]):
        for k in range(ns):
            bm.faces.new((a[k], b[k], b[(k + 1) % ns], a[(k + 1) % ns]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    for f_ in bm.faces:                                       # facing up
        if f_.normal.z < 0:
            f_.normal_flip()
    objs = kit.finish(bpy, f'{name}-lava', bm, p)
    if not p.get('shore'):
        return objs
    sr = p.get('shore_r', 0.05)
    pts = []
    for k in range(ns + 1):
        t = 2 * math.pi * k / ns
        e = edge(t) + sr * 0.4 / max(rx, ry)
        pts.append((rx * e * math.cos(t), ry * e * math.sin(t), 0.0))
    bm = bmesh.new()
    kit._tube(bm, pts[::4] + [pts[4]], [sr * (1 + 0.15 * math.sin(2 * j * 4 * 2 * math.pi / ns + ph[5])) for j in range(len(pts[::4]) + 1)], 1.6, 0, 16, 6)
    q = {**p, 'material': 'velvet', 'color': p.get('shore', '#140507')}
    q.pop('emit', None)
    objs += kit.finish(bpy, f'{name}-shore', bm, q, mat=kit.piece_material(bpy, q))
    return objs
