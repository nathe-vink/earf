"""The bar's printed things as boards with their faces printed (kit 'ext'): record sleeves, a newspaper, a book of
matches, a tent card. Each is a thin box, its print on the face toward -y (before turning), the rest its ground.

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/campaign/bar_life/bar_life.py", "fn": "boards",
     "boards": [{"image": "tex/cover-03.png", "w": 0.315, "h": 0.315, "t": 0.003, "x": .., "y": .., "z": ..,
                 "rot": [rx, ry, rz], "ground": "#1C1B1A", "rough": 0.6}, ...]}

`rot` in degrees, about the board's bottom-front-centre; a board lies flat with rot [-90, 0, rz] (its print up).
"""
import math, os
import bmesh
from mathutils import Euler, Vector

HERE = os.path.dirname(os.path.abspath(__file__))


def _hex(h):
    c = [int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    return [((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c]


def _print(bpy, img, ground, rough):
    key = f'print-{os.path.basename(img)}-{ground}-{rough}'
    m = bpy.data.materials.get(key)
    if m:
        return m
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'); b.inputs['Roughness'].default_value = rough
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(os.path.join(HERE, img), check_existing=True)
    tex.extension = 'EXTEND'
    nt.links.new(nt.nodes.new('ShaderNodeUVMap').outputs['UV'], tex.inputs['Vector'])
    nt.links.new(tex.outputs['Color'], b.inputs['Base Color'])
    return m


def _plain(bpy, hx, rough):
    key = f'ground-{hx}-{rough}'
    m = bpy.data.materials.get(key)
    if m:
        return m
    m = bpy.data.materials.new(key); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value = (*_hex(hx), 1.0); b.inputs['Roughness'].default_value = rough
    return m


def boards(bpy, name, p, kit):
    objs = []
    for k, c in enumerate(p['boards']):
        w, h, t = c['w'], c['h'], c.get('t', 0.003)
        bm = bmesh.new()
        g = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((w, t, h)), verts=g['verts'])
        bmesh.ops.translate(bm, vec=Vector((0, t / 2, h / 2)), verts=g['verts'])
        if c.get('ease', 0.0005) > 0:
            bmesh.ops.bevel(bm, geom=bm.edges[:], offset=min(c.get('ease', 0.0005), t * 0.45), segments=1, affect='EDGES')
        uv = bm.loops.layers.uv.new('UVMap')
        for f in bm.faces:
            front = f.normal.y < -0.9
            f.material_index = 0 if front else 1
            for lp in f.loops:
                lp[uv].uv = (lp.vert.co.x / w + 0.5, lp.vert.co.z / h)
        me = bpy.data.meshes.new(f'{name}-{k}'); bm.to_mesh(me); bm.free()
        me.materials.append(_print(bpy, c['image'], c.get('ground', '#1C1B1A'), c.get('rough', 0.6)))
        me.materials.append(_plain(bpy, c.get('ground', '#1C1B1A'), c.get('rough', 0.6)))
        ob = bpy.data.objects.new(f'{name}-{k}', me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (c['x'], c['y'], c['z'])
        ob.rotation_euler = Euler([math.radians(a) for a in c.get('rot', [0, 0, 0])], 'XYZ')
        objs.append(ob)
    return objs


def remove(bpy, name, p, kit):
    """Take out of a reused room the objects it built that the picture must not show (by name, exactly or with a
    .NNN suffix): the old DJ station's mixer and the records that floated where the old players stood."""
    gone = []
    for o in list(bpy.data.objects):
        base = o.name.split('.')[0]
        if base in p['names']:
            gone.append(o.name); bpy.data.objects.remove(o, do_unlink=True)
    print('REMOVED', gone)
    return []


def fill_records(bpy, name, p, kit):
    """Fill the reused room's record wall (the coordinator, 18:36: "the wall of records is the soul of this room"):
    every cell a ray from the room finds open to its back (the old screens, dark now, and the thin ones) gets dense
    spines that differ (thickness, height, colour, a few pulled a little), and a few cells books (cloth spines,
    leaning), one a face-out cover, one or two a small turned vase. Cells: `x0`, `x1`, `z0`, `z1`, `cell`, `y` (the
    wall's front face), `depth`; `skip` [[x0, x1, z0, z1], ...] left alone (the speaker bays)."""
    import random
    rnd = random.Random(p.get('seed', 11))
    dg = bpy.context.evaluated_depsgraph_get()
    cell, y0, depth = p['cell'], p['y'], p['depth']
    pal = ['#1A1A1A', '#141414', '#26262A', '#E6E0D2', '#D8D0BE', '#C9BFA8', '#9C9488', '#6E6A64', '#3A2E2A', '#8A6E4E',
           '#B8A27A', '#4A3A30', '#2E3440', '#5A4A3A', '#7A3A2A', '#3A4A3A', '#C8B890', '#1E1E22']
    cloth = ['#5A2A22', '#2E3A2E', '#6E5A3E', '#3A2E26', '#7A6448', '#2A2A30', '#5E4A36', '#8A3A2A']
    mats = [_plain(bpy, h, 0.62) for h in pal]
    bmats = [_plain(bpy, h, 0.75) for h in cloth]
    bm = bmesh.new(); ib = 0
    def box(x0, y0_, z0, x1, y1, z1, mi):
        g = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((x1 - x0, y1 - y0_, z1 - z0)), verts=g['verts'])
        bmesh.ops.translate(bm, vec=Vector(((x0 + x1) / 2, (y0_ + y1) / 2, (z0 + z1) / 2)), verts=g['verts'])
        for f in {f for v in g['verts'] for f in v.link_faces}:
            f.material_index = mi
    ncol = int(round((p['x1'] - p['x0']) / cell)); nrow = int(round((p['z1'] - p['z0']) / cell))
    filled = 0; extras = []
    special = {}
    cand = [(i, k) for i in range(ncol) for k in range(nrow)]
    rnd.shuffle(cand)
    for (i, k) in cand[:7]:
        special[(i, k)] = 'books'
    for (i, k) in cand[7:9]:
        special[(i, k)] = 'face'
    for (i, k) in cand[9:11]:
        special[(i, k)] = 'vase'
    for i in range(ncol):
        for k in range(nrow):
            xa = p['x0'] + i * cell + 0.014; xb = p['x0'] + (i + 1) * cell - 0.014
            z = p['z0'] + k * cell + 0.001; cx, cz = (xa + xb) / 2, z + cell / 2
            if any(s[0] < cx < s[1] and s[2] < cz < s[3] for s in p.get('skip', [])):
                continue
            hit = bpy.context.scene.ray_cast(dg, Vector((cx, y0 - 0.6, z + 0.16)), Vector((0, 1, 0)), distance=0.6 + depth * 0.55)
            if hit[0]:
                continue                                          # something already in it near the front
            yb = y0 + depth * 0.9; yf = yb - 0.32
            kind = special.get((i, k), 'records')
            if kind == 'books':
                s = xa + 0.01
                while s < xb - 0.05:
                    t = rnd.uniform(0.022, 0.045); h = rnd.uniform(0.2, 0.3)
                    box(s, yb - rnd.uniform(0.15, 0.22), z, s + t, yb, z + h, len(pal) + rnd.randrange(len(cloth)))
                    s += t + 0.001
                filled += 1; continue
            if kind == 'face':
                box(xa + 0.01, yf + 0.03, z, xb - 0.01, yf + 0.036, z + 0.315, rnd.randrange(len(pal)))
            if kind == 'vase':
                extras.append((cx, yb - 0.12, z)); filled += 1; continue
            fill = rnd.choice([1.0, 1.0, 1.0, 0.95, 0.9, 0.8])
            s = xa + 0.003
            while s < xa + (xb - xa) * fill - 0.004:
                t = rnd.choice([0.003, 0.0032, 0.0035, 0.004, 0.0045, 0.006, 0.009]) * rnd.uniform(0.9, 1.1)
                pull = rnd.uniform(0.02, 0.07) if rnd.random() < 0.04 else 0.0
                h = 0.315 + rnd.uniform(-0.006, 0.002) - rnd.choice([0, 0, 0, 0, 0.012, 0.03])
                box(s, yf - pull, z, s + t, yb - pull, z + h, rnd.randrange(len(pal)))
                s += t + 0.0004
            filled += 1
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats + bmats:
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    out = [ob]
    for (x, y, z) in extras:                                      # a small turned stoneware vase
        bm2 = bmesh.new()
        prof = [(0.0, 0.0), (0.045, 0.0), (0.06, 0.06), (0.055, 0.12), (0.03, 0.17), (0.028, 0.2), (0.0, 0.2)]
        rings = []
        for r, zz in prof:
            rings.append([bm2.verts.new((r * math.cos(2 * math.pi * j / 32), r * math.sin(2 * math.pi * j / 32), zz)) for j in range(32)])
        for a, b in zip(rings, rings[1:]):
            for j in range(32):
                try:
                    bm2.faces.new((a[j], a[(j + 1) % 32], b[(j + 1) % 32], b[j]))
                except ValueError:
                    pass
        bmesh.ops.remove_doubles(bm2, verts=bm2.verts, dist=1e-5)
        me2 = bpy.data.meshes.new(f'{name}-vase'); bm2.to_mesh(me2); bm2.free()
        me2.materials.append(_plain(bpy, rnd.choice(['#8A6E56', '#3A3633', '#B8AA94']), 0.7))
        for poly in me2.polygons:
            poly.use_smooth = True
        o2 = bpy.data.objects.new(f'{name}-vase', me2); bpy.context.scene.collection.objects.link(o2)
        o2.location = (x, y, z); out.append(o2)
    print('RECORDS filled', filled, 'cells')
    return out
