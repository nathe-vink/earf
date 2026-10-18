"""Acid's kit pieces (round 31, spinoffs/barkhorn/dioramas/acid.py): acid rain in glass and resin.

- rain: resin drops hung on fine threads from a cloud, each the Acid icon's drop (a ball and the cone tangent to it,
  its tip rounded), with two air bubbles cast in it as the icon has two cut out. `drops` [[x, y, z, h], ...] (z the
  drop's bottom, h its height, world metres), `top` the threads' top z (or `tops` one per drop), `thread_color`,
  `bubbles` (true: the two air bubbles).
- ripples: rings spreading on a puddle where a drop has landed, `rings` [[x, y, R], ...] (or [x, y, R, dz], raised dz)
  at the piece's z, `width` the ring's section half-width, `height` its rise.
- puddle: a flat pool of resin with a rounded meniscus, its outline a wobbly ellipse `size` [rx, ry], `height` thick,
  `wobble` (share of the radius), `seed`.
"""
import math, random

import bmesh
from mathutils import Vector

R_ICON, D_ICON = 180.0, 395.0          # the icon's drop: its circle's radius and the tip's distance from the centre
BUBBLES = [(-48 / R_ICON, (145 - 105) / R_ICON, 70 / R_ICON), (62 / R_ICON, (45 - 105) / R_ICON, 40 / R_ICON)]


def _drop_profile(n=20, tip_round=0.12):
    """The drop's [r, z] profile, the ball's radius 1, its centre at z 0, the tip up at D_ICON / R_ICON."""
    d = D_ICON / R_ICON
    th = math.acos(1 / d)                       # the tangent point's angle from the +z axis
    prof = []
    for i in range(n + 1):                      # the ball, from its bottom pole to the tangent point
        a = math.pi - (math.pi - th) * i / n
        prof.append((math.sin(a), math.cos(a)))
    rt, zt = prof[-1]
    zc = d - tip_round * d * 0.6                # the cone, ending in a little rounded tip
    for i in range(1, 9):
        t = i / 8
        prof.append((rt + (0 - rt) * t * 0.97 + 0.0, zt + (zc - zt) * t))
    prof[-1] = (0.035, zc)
    prof.append((0.0, zc + 0.03))
    prof[0] = (0.0, -1.0)
    return prof


def _lathe(bm, profile, centre, scale, seg=32):
    cx, cy, cz = centre
    rings = []
    for r, z in profile:
        if r <= 1e-6:
            rings.append([bm.verts.new((cx, cy, cz + z * scale))])
        else:
            rings.append([bm.verts.new((cx + r * scale * math.cos(2 * math.pi * i / seg),
                                        cy + r * scale * math.sin(2 * math.pi * i / seg), cz + z * scale)) for i in range(seg)])
    for a, b in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1:
                bm.faces.new((a[0], b[i], b[j]))
            elif len(b) == 1:
                bm.faces.new((a[i], b[0], a[j]))
            else:
                bm.faces.new((a[i], b[i], b[j], a[j]))


def _bubble_material(bpy):
    m = bpy.data.materials.get('kit-acid-air')
    if m:
        return m
    m = bpy.data.materials.new('kit-acid-air'); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (1, 1, 1, 1)
    b.inputs['Roughness'].default_value = 0.0
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['IOR'].default_value = 1.0 / 1.54            # air in resin
    return m


def rain(bpy, name, p, kit):
    prof = _drop_profile()
    d = D_ICON / R_ICON
    bm = bmesh.new(); bb = bmesh.new()
    tops = p.get('tops') or [p.get('top', 4.0)] * len(p['drops'])
    threads = []
    rnd = random.Random(p.get('seed', 3))
    for (x, y, z, h), top in zip(p['drops'], tops):
        s = h / (1 + d)                                  # the ball's radius
        c = (x, y, z + s)
        _lathe(bm, prof, c, s)
        if p.get('bubbles', True):
            turn = rnd.uniform(0, 2 * math.pi)
            for bx, bz, br in BUBBLES:
                # the icon's bubbles, turned about the drop's axis, kept inside the ball
                q = (bx * math.cos(turn), bx * math.sin(turn))
                geom = bmesh.ops.create_uvsphere(bb, u_segments=16, v_segments=8, radius=br * s * 0.8)
                for v in geom['verts']:
                    v.co += Vector((c[0] + q[0] * s * 0.8, c[1] + q[1] * s * 0.8, c[2] - bz * s * 0.8))
        threads.append(((x, y, z + s * (1 + d) - s * 0.05), (x, y, top)))
    objs = kit.finish(bpy, name, bm, {**p, 'material': 'resin'})
    if p.get('bubbles', True):
        objs += kit.finish(bpy, name + '-air', bb, {'position': p.get('position', [0, 0, 0])}, mat=_bubble_material(bpy))
    tm = bmesh.new()
    r = p.get('thread_radius', 0.0012)
    for a, b in threads:
        a, b = Vector(a), Vector(b)
        g = bmesh.ops.create_cone(tm, cap_ends=True, segments=6, radius1=r, radius2=r, depth=(b - a).length)
        bmesh.ops.translate(tm, vec=(a + b) / 2, verts=g['verts'])
    objs += kit.finish(bpy, name + '-threads', tm, {'position': p.get('position', [0, 0, 0])},
                       mat=kit.material(bpy, 'paper', p.get('thread_color', '#EDEFD8'), {}))
    return objs


def _torus_verts(bm, x, y, R, w, h, seg=96, sides=12):
    rings = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        ring = []
        for k in range(sides):
            b = 2 * math.pi * k / sides
            rr = R + w * math.cos(b)
            ring.append(bm.verts.new((x + rr * math.cos(a), y + rr * math.sin(a), h * math.sin(b))))
        rings.append(ring)
    for i in range(seg):
        a_, b_ = rings[i], rings[(i + 1) % seg]
        for k in range(sides):
            bm.faces.new((a_[k], b_[k], b_[(k + 1) % sides], a_[(k + 1) % sides]))
    return [v for r in rings for v in r]


def ripples(bpy, name, p, kit):
    bm = bmesh.new()
    w, h = p.get('width', 0.006), p.get('height', 0.003)
    for ring in p['rings']:
        x, y, R = ring[:3]
        for v in _torus_verts(bm, x, y, R, w, h):
            v.co.z += ring[3] if len(ring) > 3 else 0.0
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return kit.finish(bpy, name, bm, {**p, 'material': p.get('material', 'resin')})


def puddle(bpy, name, p, kit):
    """A pool with a rounded meniscus: rings of a wobbly outline, stepping in and up as a quarter round, then a flat top."""
    rx, ry = p.get('size', [0.3, 0.2])
    H = p.get('height', 0.01)
    wob = p.get('wobble', 0.12)
    rnd = random.Random(p.get('seed', 1))
    ph = [rnd.uniform(0, 6.283) for _ in range(3)]
    seg = 96

    def rad(a):
        return 1 + wob * (0.6 * math.sin(2 * a + ph[0]) + 0.3 * math.sin(3 * a + ph[1]) + 0.18 * math.sin(5 * a + ph[2]))
    bm = bmesh.new()
    dome = p.get('dome', 0.6)                     # the top rises toward the middle by this share of H (surface tension)
    rings = []
    edge = 6
    for j in range(edge + 1):                     # the meniscus: a quarter round at the edge
        t = j / edge * math.pi / 2
        rings.append((H * (1 - math.cos(t)), H * math.sin(t), 1.0))
    for j in range(1, 9):                         # the top, rising gently to the middle
        f = 1 - j / 9
        rings.append((None, H * (1 + dome * (1 - f ** 2)), f))
    verts = []
    for inset, z, f in rings:
        ring = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            k = rad(a)
            if inset is not None:
                ring.append(bm.verts.new((math.cos(a) * (rx * k - inset), math.sin(a) * (ry * k - inset), z)))
            else:
                ring.append(bm.verts.new((math.cos(a) * (rx * k - H) * f, math.sin(a) * (ry * k - H) * f, z)))
        verts.append(ring)
    for a_, b_ in zip(verts, verts[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            bm.faces.new((a_[i], a_[j], b_[j], b_[i]))
    top = bm.verts.new((0, 0, H * (1 + dome)))
    for i in range(seg):
        bm.faces.new((verts[-1][i], verts[-1][(i + 1) % seg], top))
    rings = verts
    bm.faces.new(rings[0][::-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return kit.finish(bpy, name, bm, {**p, 'material': p.get('material', 'resin')})


def umbrella(bpy, name, p, kit):
    """A paper cocktail umbrella, open: `gores` paper panels of a shallow cone `radius` wide and `rise` high, in
    `colors` by turns, on a stick `height` tall, its foot at the piece's origin (turn it with `rotate`)."""
    n, R, rise, H = p.get('gores', 8), p.get('radius', 0.13), p.get('rise', 0.045), p.get('height', 0.2)
    cols = p.get('colors', ['#FFE04A', '#FBF6E4'])
    objs = []
    for k, col in enumerate(cols):
        bm = bmesh.new()
        for i in range(k, n, len(cols)):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            steps = 6                                     # each gore sags a little between its ribs
            apex = bm.verts.new((0, 0, H))
            prev = None
            rim = []
            for j in range(steps + 1):
                a = a0 + (a1 - a0) * j / steps
                sag = 0.006 * math.sin(math.pi * j / steps)
                rim.append(bm.verts.new((R * math.cos(a), R * math.sin(a), H - rise - sag)))
            for j in range(steps):
                bm.faces.new((apex, rim[j], rim[j + 1]))
        bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.0015)
        objs += kit.finish(bpy, f'{name}-{k}', bm, {**p, 'material': 'paper', 'color': col}, smooth=False)
    bm = bmesh.new()
    g = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.004, radius2=0.003, depth=H + 0.03)
    bmesh.ops.translate(bm, vec=Vector((0, 0, (H + 0.03) / 2 - 0.03)), verts=g['verts'])
    objs += kit.finish(bpy, name + '-stick', bm, {**p, 'material': 'card', 'color': p.get('stick', '#F4EBD2')})
    return objs
