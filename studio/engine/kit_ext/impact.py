"""An impact trench in a road (round 31b, Smoke E8: spinoffs/barkhorn/elements/smoke_impact.py; the owner, 2026-10-20:
"it looked like the speaker slid along the asphalt and ground it up, like an asteroid might").

trench: the gouge itself, a channel along +y from `y0` (the impact point, where it starts shallow) to `y1` (where the
speaker came to rest), `width` metres across its floor, its depth rising to `depth` within `ramp` metres of the impact
and holding, its walls ragged (`ragged` metres of noise), its floor a torn aggregate (`texture`), scorched darker toward
the speaker (`tint`, `tint_mix`). It is the surface the road's two slabs leave open between them.

slabs: the asphalt torn up along both lips: `count` fractured plates, each an irregular slab `thickness` thick, its top
the road's asphalt (`top`), its broken edges and underside the grey sub-base (`under`), heaved up and tilted outward off
the lip by up to `tilt` degrees, larger near the impact's deepest part. `seed`.

debris: chunks of asphalt and aggregate thrown forward and to the sides of the path: `count` of them, finer and sparser
with distance (`reach` metres), lying on the road at random tilt. `seed`.
"""
import math, random

import bmesh
from mathutils import Euler, Matrix, Vector, noise


def _mat(bpy, kit, texture, tex_scale, tint=None, tint_mix=0.0, rough=1.0, bump=1.5):
    return kit.piece_material(bpy, {'material': 'pbr', 'texture': texture, 'tex_scale': tex_scale, 'tint': tint,
                                    'tint_mix': tint_mix, 'rough_mul': rough, 'bump': bump})


def trench(bpy, name, p, kit):
    y0, y1 = p.get('y0', -20.0), p.get('y1', 0.0)
    W, D = p.get('width', 1.0) / 2, p.get('depth', 0.35)
    ramp, rag = p.get('ramp', 4.0), p.get('ragged', 0.08)
    lip = p.get('lip', 0.75)                                   # half the opening at road level
    sd = p.get('seed', 1) * 7.3
    ny = int((y1 - y0) / 0.06); nx = 28
    bm = bmesh.new()
    rows = []
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        dep = D * min(1.0, (y - y0) / ramp) ** 0.7
        end = p.get('end', 0.0)
        if end and y > y1 - end:
            dep *= max(0.0, (y1 - y) / end) ** 0.8          # the gouge's end, where the speaker ploughed to rest
        row = []
        for i in range(nx + 1):
            u = -1.0 + 2.0 * i / nx                            # across: -1 at one lip, +1 at the other
            # a U: flat floor across the width, walls rising to the lips, ragged where the slabs tore away
            w = abs(u)
            z = -dep * (1.0 if w < W / lip else max(0.0, 1.0 - ((w - W / lip) / (1.0 - W / lip)) ** 1.5))
            x = u * lip
            n = noise.noise(Vector((x * 6.0 + sd, y * 3.0, 0.0)))
            x += rag * n * (0.3 + w)
            z += 0.04 * noise.noise(Vector((x * 9.0, y * 9.0 + sd, 1.0))) * (dep / max(D, 1e-3))
            row.append(bm.verts.new((x, y, z)))
        rows.append(row)
    for j in range(ny):
        for i in range(nx):
            bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
    mat = _mat(bpy, kit, p.get('texture', 'gravel_concrete'), p.get('tex_scale', 1.2), p.get('tint', '#2E2A26'),
               p.get('tint_mix', 0.35), 1.0, 2.0)
    q = {k: v for k, v in p.items() if k in ('position', 'rotate')}
    return kit.finish(bpy, name, bm, q, smooth=True, mat=mat)


def _plate(bm, rnd, w, d, t):
    """An irregular plate: a polygon of 6 to 9 corners, `t` thick, its edges jagged."""
    k = rnd.randint(6, 9)
    pts = []
    for i in range(k):
        a = 2 * math.pi * (i + rnd.uniform(-0.3, 0.3)) / k
        r = rnd.uniform(0.65, 1.0)
        pts.append((w / 2 * r * math.cos(a), d / 2 * r * math.sin(a)))
    top = [bm.verts.new((x, y, t / 2 + rnd.uniform(-0.006, 0.006))) for x, y in pts]
    bot = [bm.verts.new((x * rnd.uniform(0.9, 1.05), y * rnd.uniform(0.9, 1.05), -t / 2)) for x, y in pts]
    ft = bm.faces.new(top); fb = bm.faces.new(bot[::-1])
    sides = []
    for i in range(k):
        sides.append(bm.faces.new((top[i], bot[i], bot[(i + 1) % k], top[(i + 1) % k])))
    return ft, fb, sides


def _place(bm, verts, rot, loc):
    m = Euler([math.radians(a) for a in rot]).to_matrix()
    for v in verts:
        v.co = m @ v.co + Vector(loc)


def slabs(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 1))
    y0, y1 = p.get('y0', -20.0), p.get('y1', 0.0)
    lip, t = p.get('lip', 0.75), p.get('thickness', 0.08)
    D, ramp = p.get('depth', 0.35), p.get('ramp', 4.0)
    bm = bmesh.new()
    tops = []
    for k in range(p.get('count', 40)):
        y = rnd.uniform(y0 + 0.5, y1 - 0.2)
        s = 1 if rnd.random() < 0.5 else -1
        f = min(1.0, (y - y0) / ramp)                          # bigger, steeper plates where the trench is deep
        sz = p.get('size', 1.0)
        w, d = sz * rnd.uniform(0.25, 0.7) * (0.5 + f), sz * rnd.uniform(0.3, 0.8) * (0.5 + f)
        before = set(bm.verts)
        ft, fb, sides = _plate(bm, rnd, w, d, t)
        new = [v for v in bm.verts if v not in before]
        tilt = rnd.uniform(p.get('tilt_min', 15.0), p.get('tilt', 55.0)) * f
        x = s * (lip + w * 0.25 * rnd.uniform(0.2, 1.0))
        z = 0.02 + 0.5 * w * math.sin(math.radians(tilt)) * 0.4 - (0.0 if rnd.random() < 0.7 else 0.1)
        _place(bm, new, (rnd.uniform(-8, 8), s * tilt, rnd.uniform(-25, 25)), (x, y, z))
        tops.append(ft)
    for f in bm.faces:
        f.material_index = 0 if f in tops else 1
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(_mat(bpy, kit, p.get('top', 'asphalt_02'), 4.0, '#2C2C2E', 0.3, 0.3))
    me.materials.append(_mat(bpy, kit, p.get('under', 'gravel_concrete'), 0.8, '#5A5650', 0.25))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    return [ob]


def debris(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 2))
    y0, y1 = p.get('y0', -20.0), p.get('y1', 0.0)
    reach = p.get('reach', 6.0)
    bm = bmesh.new()
    tops = []
    for k in range(p.get('count', 300)):
        # along the path, thrown sideways (and some forward past the speaker); size falls with distance thrown
        y = rnd.uniform(y0 + 1.0, y1 + 2.5)
        r = reach * rnd.random() ** 2.2
        x = (1 if rnd.random() < 0.5 else -1) * (p.get('inner', 0.8) + r)
        size = max(0.015, 0.16 * (1.0 - r / reach) ** 1.6 * rnd.uniform(0.3, 1.0))
        before = set(bm.verts)
        ft, fb, sides = _plate(bm, rnd, size * rnd.uniform(0.8, 1.6), size * rnd.uniform(0.8, 1.6),
                               size * rnd.uniform(0.3, 0.6))
        new = [v for v in bm.verts if v not in before]
        _place(bm, new, (rnd.uniform(-40, 40), rnd.uniform(-40, 40), rnd.uniform(0, 360)), (x, y, p.get('z', 0.0) + size * 0.2))
        if rnd.random() < 0.6:
            tops.append(ft)
    for f in bm.faces:
        f.material_index = 0 if f in tops else 1
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(_mat(bpy, kit, p.get('top', 'asphalt_02'), 4.0, '#2C2C2E', 0.3, 0.3))
    me.materials.append(_mat(bpy, kit, p.get('under', 'gravel_concrete'), 0.8, '#55514B', 0.3))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    return [ob]
