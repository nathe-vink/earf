"""Haze, in its element (round 31b): a lavender field at dusk. Pieces for spinoffs/barkhorn/elements/haze.py.

- field: rows of lavender bushes running away from the camera, each bush a mound of grey-green leafy shoots under a
  dome of flower stems, each stem ending in a spike of violet florets in whorls. A handful of bushes are modelled and
  the rows are linked copies of them (Cycles instances them), turned, sized and leant at random so no two neighbours
  repeat. `rows` [x0, x1, spacing], `span` [y0, y1], `step` (along a row), `clear` [[x, y, r], ...] (no bush within),
  `variants`, `seed`, `detail` (stems a bush), `colors` {flower, leaf, stem}.
- hills: a range of hills far off, a height field of layered noise (`size` [w, d], `position` its centre, `height`,
  `cells`), laid with a photographed texture (`texture`), for the haze to turn violet.
- sun: the sun's disc, `distance` metres off at `azimuth_deg` and `elevation_deg` (the engine's convention), `diameter_deg`
  across, glowing at `strength` in `color`, so it can sink behind the haze and the hills (an environment's sun is
  infinitely far and cannot).
- plane: a plain textured plane (`size`, `position`, `texture`, `tex_scale`), the far field the rows run into.
"""
import math, random

import bmesh
from mathutils import Matrix, Vector, noise

_BUSHES = {}


def _hex(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c) + (1.0,)


def _mat(bpy, name, color, rough=0.6, sss=0.0, sheen=0.0, vary=None):
    """A plant material: base colour wandering toward `vary` by object and by a fine noise, so no two florets or bushes
    are dyed the same."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = rough
    if 'Subsurface Weight' in b.inputs:
        b.inputs['Subsurface Weight'].default_value = sss
        b.inputs['Subsurface Radius'].default_value = (0.004, 0.003, 0.004)
    if 'Sheen Weight' in b.inputs:
        b.inputs['Sheen Weight'].default_value = sheen
    if vary:
        info = nt.nodes.new('ShaderNodeObjectInfo'); tc = nt.nodes.new('ShaderNodeTexCoord')
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 60.0
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        mix = nt.nodes.new('ShaderNodeMath'); mix.operation = 'MULTIPLY_ADD'
        nt.links.new(info.outputs['Random'], mix.inputs[0]); mix.inputs[1].default_value = 0.6
        nt.links.new(nz.outputs['Fac'], mix.inputs[2])
        ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
        cr.elements[0].position = 0.2; cr.elements[0].color = _hex(color)
        cr.elements[1].position = 1.0; cr.elements[1].color = _hex(vary)
        nt.links.new(mix.outputs[0], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    else:
        b.inputs['Base Color'].default_value = _hex(color)
    return m


def _floret(bm, c, axis, r, rnd):
    """One floret: a small closed bud (an icosphere squashed along the stem), tilted off it a little."""
    g = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)
    s = Matrix.Diagonal((r, r, r * 1.5)).to_4x4()
    q = axis.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    t = Matrix.Rotation(rnd.uniform(-0.4, 0.4), 4, 'X')
    for v in g['verts']:
        v.co = (Matrix.Translation(c) @ q @ t @ s) @ v.co
    return [f for v in g['verts'] for f in v.link_faces]


def _tube(bm, pts, r0, r1, sides=4):
    rings = []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        n = t.orthogonal().normalized(); b = t.cross(n)
        r = r0 + (r1 - r0) * i / (len(pts) - 1)
        rings.append([bm.verts.new(p + (n * math.cos(2 * math.pi * k / sides) + b * math.sin(2 * math.pi * k / sides)) * r)
                      for k in range(sides)])
    faces = []
    for a, b in zip(rings, rings[1:]):
        for k in range(sides):
            faces.append(bm.faces.new((a[k], a[(k + 1) % sides], b[(k + 1) % sides], b[k])))
    return faces


def _bush(bpy, seed, detail, colors):
    """One lavender bush, about 0.9 m across and 0.75 m tall: leafy shoots, then flower stems in a dome."""
    key = (seed, detail)
    if key in _BUSHES:
        return _BUSHES[key]
    rnd = random.Random(seed)
    bm = bmesh.new()
    leaf_f, stem_f, flower_f = [], [], []
    R = rnd.uniform(0.36, 0.46)                           # the bush's radius
    # the leafy mound: grey-green shoots, each with pairs of narrow leaves, up to about 0.35 m
    for _ in range(int(detail * 1.6)):
        a = rnd.uniform(0, 2 * math.pi); d = R * 0.8 * math.sqrt(rnd.random())
        base = Vector((math.cos(a) * d * 0.4, math.sin(a) * d * 0.4, 0.0))
        tip = Vector((math.cos(a) * d * 1.05, math.sin(a) * d * 1.05, 0.12 + 0.24 * (1 - (d / R) ** 2) + rnd.uniform(-0.03, 0.03)))
        ax = (tip - base).normalized()
        n_leaf = 7
        for j in range(n_leaf):
            c = base.lerp(tip, 0.35 + 0.65 * j / n_leaf)
            for side in (-1, 1):
                perp = ax.cross(Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), 0.3))).normalized() * side
                L = rnd.uniform(0.025, 0.045)
                out = (perp * 0.8 + ax * 0.6).normalized()
                w = ax.cross(out).normalized() * 0.0022
                v = [bm.verts.new(c - w), bm.verts.new(c + w), bm.verts.new(c + out * L + w * 0.3), bm.verts.new(c + out * L - w * 0.3)]
                leaf_f.append(bm.faces.new(v))
        stem_f += _tube(bm, [base.lerp(tip, k / 3) for k in range(4)], 0.0018, 0.001, 3)
    # the flower stems: long, bare, a gentle arch outward, each with a spike of florets in whorls
    for _ in range(detail):
        a = rnd.uniform(0, 2 * math.pi); d = R * 0.55 * math.sqrt(rnd.random())
        base = Vector((math.cos(a) * d, math.sin(a) * d, 0.18 + rnd.uniform(0, 0.08)))
        lean = rnd.uniform(0.05, 0.75) * (0.4 + 0.6 * d / (R * 0.55))   # the dome: outer stems lean further
        out = Vector((math.cos(a), math.sin(a), 0.0))
        L = rnd.uniform(0.38, 0.52) * (1.0 - 0.18 * lean)
        pts = []
        for k in range(6):
            t = k / 5
            ang = lean * (0.5 + 0.5 * t)
            pts.append(base + out * (L * t * math.sin(ang)) + Vector((0, 0, L * t * math.cos(ang))))
        stem_f += _tube(bm, pts, 0.0016, 0.0011, 4)
        tip = pts[-1]; ax = (pts[-1] - pts[-2]).normalized()
        spike = rnd.uniform(0.055, 0.085)
        whorls = rnd.randint(6, 8)
        for w_ in range(whorls):
            t = w_ / (whorls - 1)
            gap = 1.0 if t > 0.35 else 1.6                 # the lowest whorls stand apart, as on the real spike
            c = tip - ax * (spike * (1 - t) * gap * 0.75)
            nf = 5 if t < 0.85 else 3
            rr = 0.0042 * (1.0 - 0.35 * t)
            for k in range(nf):
                ph = 2 * math.pi * k / nf + w_ * 0.7
                n = ax.orthogonal().normalized(); b = ax.cross(n)
                dirn = (n * math.cos(ph) + b * math.sin(ph))
                flower_f += _floret(bm, c + dirn * rr * 1.1, (ax + dirn * 0.6).normalized(), rr, rnd)
    me = bpy.data.meshes.new(f'lavender-{seed}')
    for f in bm.faces:
        f.material_index = 0
    for f in set(stem_f):
        f.material_index = 1
    for f in set(flower_f):
        f.material_index = 2
    bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    me.materials.append(_mat(bpy, 'lavender-leaf', colors.get('leaf', '#6E7A5C'), 0.7, 0.15, 0.6, vary=colors.get('leaf2', '#8A9273')))
    me.materials.append(_mat(bpy, 'lavender-stem', colors.get('stem', '#62704A'), 0.65, 0.1, 0.3))
    me.materials.append(_mat(bpy, 'lavender-flower', colors.get('flower', '#5E4BA0'), 0.55, 0.35, 0.5, vary=colors.get('flower2', '#8A6BC0')))
    _BUSHES[key] = me
    return me


def _bushes(bpy, seeds, detail, colors):
    """The bushes for `seeds`, built once and kept in the asset cache as a .blend (a bush takes half a minute to build)."""
    import hashlib, json, os
    tag = hashlib.md5(json.dumps([BUSH_VERSION, seeds, detail, sorted(colors.items())]).encode()).hexdigest()[:10]
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'cache', 'haze_el')
    path = os.path.abspath(os.path.join(d, f'lavender-{tag}.blend'))
    names = [f'lavender-{s_}-{tag}' for s_ in seeds]
    if os.path.exists(path):
        with bpy.data.libraries.load(path, link=False) as (src, dst):
            dst.meshes = [n for n in src.meshes if n in names]
        got = {m.name: m for m in dst.meshes if m is not None}
        if all(n in got for n in names):
            return [got[n] for n in names]
    meshes = []
    for s_, n in zip(seeds, names):
        me = _bush(bpy, s_, detail, colors); me.name = n; meshes.append(me)
    os.makedirs(d, exist_ok=True)
    bpy.data.libraries.write(path, set(meshes), fake_user=True)
    return meshes


BUSH_VERSION = 1                                          # raise when _bush changes, so the cache is rebuilt


def field(bpy, name, p, kit):
    x0, x1, dx = p.get('rows', [-12.0, 12.0, 1.7])
    y0, y1 = p.get('span', [-4.0, 60.0])
    step = p.get('step', 0.85)
    clear = p.get('clear', [])
    nv = p.get('variants', 6)
    rnd = random.Random(p.get('seed', 3))
    colors = p.get('colors', {})
    meshes = _bushes(bpy, [100 + i for i in range(nv)], p.get('detail', 120), colors)
    far = _bushes(bpy, [200 + i for i in range(3)], max(30, p.get('detail', 120) // 3), colors)
    obs = []
    nrow = int(round((x1 - x0) / dx))
    for i in range(nrow + 1):
        x = x0 + i * dx
        y = y0 + rnd.uniform(0, step)
        while y < y1:
            px, py = x + rnd.uniform(-0.06, 0.06), y
            if not any((px - cx) ** 2 + (py - cy) ** 2 < cr ** 2 for cx, cy, cr in clear):
                dist = math.hypot(px, py + 5)
                me = rnd.choice(meshes) if dist < p.get('near', 25.0) else rnd.choice(far)
                ob = bpy.data.objects.new(f'{name}-{i}-{int(y * 10)}', me)
                bpy.context.scene.collection.objects.link(ob)
                ob.location = (px, py, -0.01)
                ob.rotation_euler = (rnd.uniform(-0.12, 0.12), rnd.uniform(-0.12, 0.12), rnd.uniform(0, 2 * math.pi))
                s = rnd.uniform(0.75, 1.25)
                ob.scale = (s * rnd.uniform(0.95, 1.05), s, s * rnd.uniform(0.92, 1.06))
                obs.append(ob)
            y += step * rnd.uniform(0.75, 1.3)
    return obs


def hills(bpy, name, p, kit):
    """A range of hills: a grid displaced by layered noise, highest along its middle, falling to the plain in front."""
    import assets
    w, d = p.get('size', [1200.0, 300.0])
    cx, cy, cz = p.get('position', [0.0, 600.0, 0.0])
    H = p.get('height', 60.0)
    nx = p.get('cells', 400); ny = max(8, int(nx * d / w))
    seed = p.get('seed', 1)
    off = Vector((seed * 13.1, seed * 7.7, 0.0))
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=nx, y_segments=ny, size=0.5)
    for v in bm.verts:
        x, y = v.co.x * w, v.co.y * d
        u = v.co.y + 0.5                                      # 0 at the front edge, 1 at the back
        ridge = math.sin(math.pi * min(1.0, u * 1.3)) ** 1.5
        n = noise.fractal(Vector((x / p.get('scale', 260.0), y / p.get('scale', 260.0), 0)) + off, 0.5, 2.0, p.get('octaves', 5))
        z = H * ridge * (0.55 + 0.45 * n) + H * p.get('rough', 0.12) * noise.noise(Vector((x / 60.0, y / 60.0, 1)) + off)
        v.co = Vector((x, y, max(0.0, z)))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    me.materials.append(assets.pbr(bpy, p.get('texture', 'aerial_grass_rock'), p.get('res', '2k'), scale=p.get('tex_scale', 40.0),
                                   tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0), coords='object', name=f'{name}-mat'))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (cx, cy, cz)
    return [ob]


def _far_rows(bpy, name, p):
    """The field far off, where a bush is less than a pixel: rows of violet bloom with soil and grey-green between,
    as stripes along y every `period` metres, broken by noise so they are not ruled."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    per = p.get('period', 1.7)
    mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'DIVIDE'; mx.inputs[1].default_value = per
    nt.links.new(sep.outputs['X'], mx.inputs[0])
    fr = nt.nodes.new('ShaderNodeMath'); fr.operation = 'FRACT'; nt.links.new(mx.outputs[0], fr.inputs[0])
    tri = nt.nodes.new('ShaderNodeMath'); tri.operation = 'PINGPONG'; tri.inputs[1].default_value = 0.5
    nt.links.new(fr.outputs[0], tri.inputs[0])                    # 0 at a row's middle, 0.5 in the path
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.6
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    add = nt.nodes.new('ShaderNodeMath'); add.operation = 'MULTIPLY_ADD'; add.inputs[1].default_value = 0.25
    nt.links.new(nz.outputs['Fac'], add.inputs[0]); nt.links.new(tri.outputs[0], add.inputs[2])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    c = p.get('colors', {})
    cr.elements[0].position = 0.2; cr.elements[0].color = _hex(c.get('flower', '#5A4A9E'))
    cr.elements[1].position = 0.42; cr.elements[1].color = _hex(c.get('soil', '#7A6A58'))
    e = cr.elements.new(0.3); e.color = _hex(c.get('leaf', '#6B775A'))
    nt.links.new(add.outputs[0], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.9
    return m


def plane(bpy, name, p, kit):
    import assets
    w, d = p.get('size', [400.0, 400.0])
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    for v in bm.verts:
        v.co.x *= w; v.co.y *= d
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if p.get('rows'):
        me.materials.append(_far_rows(bpy, f'{name}-mat', p))
    else:
        me.materials.append(assets.pbr(bpy, p.get('texture', 'brown_mud_dry'), p.get('res', '2k'), scale=p.get('tex_scale'),
                                       tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0), coords='object', name=f'{name}-mat'))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = tuple(p.get('position', [0.0, 0.0, 0.0]))
    return [ob]


def sun(bpy, name, p, kit):
    az, el = math.radians(p.get('azimuth_deg', 180.0)), math.radians(p.get('elevation_deg', 2.0))
    D = p.get('distance', 20000.0)
    d = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    r = D * math.tan(math.radians(p.get('diameter_deg', 0.53)) / 2)
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, radius=r, segments=96)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = _hex(p.get('color', '#FFB070')); em.inputs['Strength'].default_value = p.get('strength', 40.0)
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = d * D
    ob.rotation_euler = (-d).to_track_quat('Z', 'Y').to_euler()        # facing the set
    ob.visible_shadow = False
    for attr in ('visible_diffuse', 'visible_glossy', 'visible_transmission', 'visible_volume_scatter'):
        setattr(ob, attr, False)                           # the sun lamp does its lighting; the disc is only seen
    return [ob]


def litter(bpy, name, p, kit):
    """The path's litter, lying on the soil inside `area` [x0, y0, x1, y1], clear of `avoid` circles: `clods` of the soil
    (lumpy, flattened, half sunk, in the soil's own texture), `pebbles` (small, rounder, paler) and `straws` (dry cut
    stems lying flat)."""
    import assets
    rnd = random.Random(p.get('seed', 1))
    x0, y0, x1, y1 = p.get('area', [-0.5, -5.0, 0.5, 5.0])
    avoid = p.get('avoid', [])

    def spot():
        while True:
            x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
            if not any((x - ax) ** 2 + (y - ay) ** 2 < ar ** 2 for ax, ay, ar in avoid):
                return x, y

    out = []
    for kind, n in (('clods', p.get('clods', 600)), ('pebbles', p.get('pebbles', 300))):
        bm = bmesh.new()
        off = Vector((rnd.uniform(0, 99), rnd.uniform(0, 99), 0))
        for _ in range(n):
            x, y = spot()
            if kind == 'clods':
                r = rnd.uniform(0.005, 0.03) * (1 if rnd.random() < 0.85 else 1.6); sq = rnd.uniform(0.45, 0.7); bumpy = 0.35
            else:
                r = rnd.uniform(0.003, 0.012); sq = rnd.uniform(0.55, 0.8); bumpy = 0.12
            g = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
            a = rnd.uniform(0, 6.28); ax_ = rnd.uniform(0.7, 1.3)
            for v in g['verts']:
                k = 1.0 + bumpy * noise.noise(v.co * 1.7 + off + Vector((x * 37, y * 37, 0)))
                lx, ly, lz = v.co.x * r * k * ax_, v.co.y * r * k / ax_, v.co.z * r * k * sq
                v.co = Vector((x + lx * math.cos(a) - ly * math.sin(a), y + lx * math.sin(a) + ly * math.cos(a), lz + r * sq * 0.25))
        me = bpy.data.meshes.new(f'{name}-{kind}'); bm.to_mesh(me); bm.free()
        for f in me.polygons:
            f.use_smooth = True
        if kind == 'clods':
            me.materials.append(assets.pbr(bpy, p.get('texture', 'farm_soil'), p.get('res', '2k'), scale=0.4, coords='object',
                                           name=f'{name}-clod-mat'))
        else:
            me.materials.append(_mat(bpy, f'{name}-pebble', '#7A6C5E', 0.75, 0.0, 0.0, vary='#9C8E7C'))
        ob = bpy.data.objects.new(f'{name}-{kind}', me); bpy.context.scene.collection.objects.link(ob)
        out.append(ob)
    bm = bmesh.new()
    for _ in range(p.get('straws', 200)):
        x, y = spot()
        a = rnd.uniform(0, 6.28); L = rnd.uniform(0.04, 0.16); c = Vector((x, y, 0.004))
        dvec = Vector((math.cos(a), math.sin(a), rnd.uniform(-0.02, 0.06)))
        pts = [c + dvec * (L * (k / 3 - 0.5)) + Vector((0, 0, 0.002 * math.sin(k))) for k in range(4)]
        _tube(bm, pts, 0.0012, 0.0008, 4)
    me = bpy.data.meshes.new(f'{name}-straws'); bm.to_mesh(me); bm.free()
    me.materials.append(_mat(bpy, f'{name}-straw', '#8C7A56', 0.7, 0.1, 0.4, vary='#B8A27A'))
    ob = bpy.data.objects.new(f'{name}-straws', me); bpy.context.scene.collection.objects.link(ob)
    out.append(ob)
    return out
