"""Fog's own pieces for round 31b (in their element: the speaker on a summit above a sea of clouds).

- cloudsea: the top of a cloud deck seen from above, from `near` to `far` metres beyond the ledge (y), `width` across,
  its mean top at `z`, heaped into billows by layered noise (`billow` metres across the big heaps, `height` metres from
  trough to crest), deep-scattering white so it glows where the sun lights it and goes blue-grey in its troughs. The grid
  grows coarser with distance, so it is fine where it is near.
  `lean` (x per metre of y) swings the fan to follow a view that looks off the y axis.
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
            x = cx + p.get('lean', 0.0) * y + (i / (nx - 1) - 0.5) * w      # `lean`: the fan follows the view off axis
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


def cloudvol(bpy, name, p, kit):
    """The near part of the cloud deck as real cloud: a scattering volume in a box (`box` [x0, y0, z0, x1, y1, z1]) whose
    top is a heightfield of soft noise (`top` metres mean height, `amp` metres up and down, `scale` metres across the
    big heaps), eaten into billows and wisps by a finer noise (`detail` metres, `erode` metres of reach) and soft over
    `soft` metres; `density` per metre inside, white, scattering forward (`anisotropy`)."""
    x0, y0, z0, x1, y1, z1 = p['box']
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); v = nt.nodes.new('ShaderNodeVolumePrincipled')
    v.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#FFFFFF'))
    v.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.6)
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    def node(kind, **inputs):
        n = nt.nodes.new(kind)
        for k, val in inputs.items():
            n.inputs[k].default_value = val
        return n
    # the top: a 2D noise over x, y
    xy = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(sep.outputs['X'], xy.inputs['X']); nt.links.new(sep.outputs['Y'], xy.inputs['Y'])
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.noise_dimensions = '2D'
    n2.inputs['Scale'].default_value = 1.0 / p.get('scale', 300.0); n2.inputs['Detail'].default_value = p.get('octaves', 6.0)
    if 'Roughness' in n2.inputs:
        n2.inputs['Roughness'].default_value = 0.55
    nt.links.new(xy.outputs['Vector'], n2.inputs['Vector'])
    top = nt.nodes.new('ShaderNodeMath'); top.operation = 'MULTIPLY_ADD'
    top.inputs[1].default_value = p.get('amp', 40.0) * 3.0; top.inputs[2].default_value = p.get('top', -70.0) - p.get('amp', 40.0) * 1.5
    nt.links.new(n2.outputs['Fac'], top.inputs[0])
    # the billows: a 3D noise that pushes the surface in and out
    n3 = nt.nodes.new('ShaderNodeTexNoise'); n3.inputs['Scale'].default_value = 1.0 / p.get('detail', 18.0)
    n3.inputs['Detail'].default_value = p.get('billow_octaves', 5.0)
    if 'Roughness' in n3.inputs:
        n3.inputs['Roughness'].default_value = 0.6
    n3.inputs['Distortion'].default_value = p.get('distort', 0.4)
    nt.links.new(tc.outputs['Object'], n3.inputs['Vector'])
    er = nt.nodes.new('ShaderNodeMath'); er.operation = 'MULTIPLY_ADD'
    er.inputs[1].default_value = p.get('erode', 20.0) * 2.0; er.inputs[2].default_value = -p.get('erode', 20.0)
    nt.links.new(n3.outputs['Fac'], er.inputs[0])
    # depth below the (billowed) top
    d = nt.nodes.new('ShaderNodeMath'); d.operation = 'SUBTRACT'
    nt.links.new(top.outputs['Value'], d.inputs[0]); nt.links.new(sep.outputs['Z'], d.inputs[1])
    d2 = nt.nodes.new('ShaderNodeMath'); d2.operation = 'ADD'
    nt.links.new(d.outputs['Value'], d2.inputs[0]); nt.links.new(er.outputs['Value'], d2.inputs[1])
    sm = nt.nodes.new('ShaderNodeMapRange'); sm.interpolation_type = 'SMOOTHSTEP'
    sm.inputs['From Min'].default_value = 0.0; sm.inputs['From Max'].default_value = p.get('soft', 12.0)
    sm.inputs['To Max'].default_value = p.get('density', 0.05)
    nt.links.new(d2.outputs['Value'], sm.inputs['Value'])
    nt.links.new(sm.outputs['Result'], v.inputs['Density'])
    nt.links.new(v.outputs['Volume'], out.inputs['Volume'])
    m.cycles.volume_step_rate = p.get('step', 1.0)
    bm = bmesh.new()
    g = bmesh.ops.create_cube(bm, size=1.0)
    for vv in g['verts']:
        vv.co = Vector(((x0 + x1) / 2 + vv.co.x * (x1 - x0), (y0 + y1) / 2 + vv.co.y * (y1 - y0), (z0 + z1) / 2 + vv.co.z * (z1 - z0)))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return [ob]


def _desaturate(root, sat, val):
    """A scanned model's colour taken toward the grey of the rock it lies on (a Hue/Saturation node before its base
    colour)."""
    seen = set()
    for o in [root] + list(root.children_recursive):
        for slot in getattr(o, 'material_slots', []):
            m = slot.material
            if not m or m.name in seen or not m.use_nodes:
                continue
            seen.add(m.name)
            nt = m.node_tree
            b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            if not b or not b.inputs['Base Color'].links:
                continue
            src = b.inputs['Base Color'].links[0].from_socket
            hs = nt.nodes.new('ShaderNodeHueSaturation')
            hs.inputs['Saturation'].default_value = sat; hs.inputs['Value'].default_value = val
            nt.links.new(src, hs.inputs['Color']); nt.links.new(hs.outputs['Color'], b.inputs['Base Color'])


def summit(bpy, name, p, kit):
    """A summit of real rock: a patch of a Poly Haven texture (assets.ground, `texture` at `res`, `size`, `displace`,
    `relief`) that is level where the speaker stands and rolls over a brow `brow` metres behind it (y), falling `drop`
    metres over `fall` metres beyond, so the eye goes over the edge to what lies below. Stones (`stones`: a model id,
    `count`, `scale` [min, max], kept `clear` metres from the speaker, `area` [x0, y0, x1, y1]) are dropped onto it,
    each resting where a ray from above meets the rock."""
    import assets
    w, d = p.get('size', [30.0, 24.0])
    cx, cy, cz = p.get('position', [0.0, 0.0, 0.0])
    ob = assets.ground(bpy, name, p['texture'], (w, d), p.get('res', '2k'), (cx, cy, cz), p.get('cells'),
                       p.get('displace', 0.05), p.get('tint'), p.get('tint_mix', 0.0), p.get('tex_scale'),
                       p.get('rough_mul', 1.0), p.get('bump', 1.0), p.get('relief'), (0.0, 0.0, p.get('flat_r', 0.9)))
    brow, drop, fall = p.get('brow', 6.0), p.get('drop', 4.0), p.get('fall', 10.0)
    for v in ob.data.vertices:
        y = v.co.y + cy
        if y > brow:
            t = min(1.0, (y - brow) / fall)
            v.co.z -= drop * (t * t * (3 - 2 * t)) * (1.0 + 0.6 * max(0.0, (y - brow - fall) / fall))
    ob.data.update()
    obs = [ob]
    st = p.get('stones')
    if st:
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        rnd = random.Random(st.get('seed', 5))
        root = assets.place(bpy, st['model'], st.get('res', '1k'), location=(0, 0, -1000))
        _desaturate(root, st.get('saturation', 0.25), st.get('value', 0.8))
        x0, y0, x1, y1 = st.get('area', [-6, -3, 6, 6])
        made, tries = 0, 0
        while made < st.get('count', 200) and tries < st.get('count', 200) * 20:
            tries += 1
            x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
            if x * x + y * y < st.get('clear', 0.5) ** 2:
                continue
            hit, loc, nrm, idx, hob, mx = bpy.context.scene.ray_cast(dg, Vector((x, y, 50.0)), Vector((0, 0, -1)))
            if not hit or hob.name != ob.name:
                continue
            s = rnd.uniform(*st.get('scale', [0.3, 1.0]))
            assets.instance(bpy, root, (x, y, loc.z - 0.01 * s), (rnd.uniform(-20, 20), rnd.uniform(-20, 20), rnd.uniform(0, 360)), s)
            made += 1
        root.hide_render = True
        for o in root.children_recursive:
            o.hide_render = True
    return obs
