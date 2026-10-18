"""Acid in its element (round 31b, spinoffs/barkhorn/elements/acid.py): an acid spring in the spirit of Dallol.

- terrain: the ground, a terraced crust whose hollows fill with acid. A height field (broad swells, terraces a few
  centimetres high, raised salt rims at the water's edge) on a polar grid, dense under the speaker and coarse at the
  horizon; coloured by height and a slow noise into white salt, lemon sulphur and rust iron, over a photographed crust
  texture (its cracks, grain and relief); and the acid in its hollows, a glossy milky surface at `water` that is clear
  at a shallow edge and deepens to green (`acid_colors` by depth, `acid_deep`, `acid_edge`). `water` the pools' level, `pools` [[x, y, depth, sigma], ...] dug in, `flat`
  [x, y, r] level ground where the speaker stands, `texture` (Poly Haven id), `seed`.
- chimney: a lumpy sulphur or salt chimney, `height`, `radius`, `colors` [salt, sulphur, deep], `texture`, `seed`.
- steam: a soft plume of steam (a volume), `size` [rx, ry, rz], `density`, `seed`.
"""
import math, random

import bmesh
from mathutils import Vector, noise

import assets


def _hex(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c) + (1.0,)


def _smooth(e0, e1, x):
    t = min(1.0, max(0.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def _fbm(x, y, off, oct=4):
    s, a, f = 0.0, 1.0, 1.0
    for _ in range(oct):
        s += a * noise.noise(Vector((x * f + off, y * f - off, off * 0.37)))
        a *= 0.5; f *= 2.03
    return s


def height(x, y, p):
    """The ground's height (m) at (x, y)."""
    off = p.get('seed', 1) * 17.3
    r = math.hypot(x, y)
    f = 0.16 * _fbm(x / 5.0, y / 5.0, off) + 0.05 * _fbm(x / 1.4, y / 1.4, off + 3) + 0.01 * _fbm(x / 0.35, y / 0.35, off + 7, 2)
    step = p.get('terrace', 0.045)
    g = f / step
    h = step * (math.floor(g) + _smooth(0.3, 0.7, g - math.floor(g)))
    h *= 1.0 - 0.75 * _smooth(25.0, 90.0, r)                       # the plain flattens toward the horizon
    for px, py, depth, sig in p.get('pools', []):
        h -= depth * math.exp(-((x - px) ** 2 + (y - py) ** 2) / (2 * sig * sig))
    fx, fy, fr = p.get('flat', [0.0, 0.0, 0.55])
    t = _smooth(fr, fr * 2.4, math.hypot(x - fx, y - fy))
    h = h * t + p.get('stand', 0.0) * (1 - t)
    W = p.get('water', -0.04)
    d = h - W
    h += 0.018 * math.exp(-(d / 0.022) ** 2) * (1 - _smooth(30.0, 60.0, r))   # salt rims where the acid has dried
    return h


def terrain(bpy, name, p, kit):
    R = p.get('radius', 320.0)
    seg = p.get('segments', 900)
    # rings from the centre out, spaced finely near the speaker and the camera and coarser with distance
    rings = [0.0]
    r = 0.012
    while r < R:
        rings.append(r)
        r += max(0.012, min(4.0, r * (0.0065 if r < 12 else 0.02)))
    rings.append(R)
    W = p.get('water', -0.04)
    bm = bmesh.new(); wm = bmesh.new()
    lay = bm.verts.layers.float.new('acid_d')
    wl = wm.verts.layers.float.new('acid_depth')
    grid, wgrid = [], []
    for ri in rings:
        n = 1 if ri == 0.0 else seg
        ring, wring = [], []
        for i in range(n):
            a = 2 * math.pi * i / seg
            x, y = ri * math.cos(a), ri * math.sin(a)
            z = height(x, y, p)
            v = bm.verts.new((x, y, z)); v[lay] = z - W
            w = wm.verts.new((x, y, W)); w[wl] = W - z
            ring.append(v); wring.append(w)
        grid.append(ring); wgrid.append(wring)
    for G, M, wet in ((grid, bm, False), (wgrid, wm, True)):
        for k in range(1, len(G)):
            a_, b_ = G[k - 1], G[k]
            for i in range(seg):
                j = (i + 1) % seg
                quad = (a_[0], b_[i], b_[j]) if len(a_) == 1 else (a_[i], b_[i], b_[j], a_[j])
                if wet and max(v[wl] for v in quad) <= 0.0:           # the acid only where the ground dips under it
                    continue
                M.faces.new(quad)
    objs = []
    for M, nm, mat in ((bm, name, crust_material(bpy, p)), (wm, name + '-acid', acid_material(bpy, p))):
        loose = [v for v in M.verts if not v.link_faces]
        bmesh.ops.delete(M, geom=loose, context='VERTS')
        for f in M.faces:
            if f.normal.z < 0:
                f.normal_flip()
        me = bpy.data.meshes.new(nm); M.to_mesh(me); M.free()
        for f in me.polygons:
            f.use_smooth = True
        me.materials.append(mat)
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
        objs.append(ob)
    return objs


def acid_material(bpy, p):
    """The acid, Dallol's: milky with dissolved minerals, clear at a shallow edge, pale lime over the crust, deepening to
    an opaque green; a glossy skin with a faint breeze on it."""
    m = bpy.data.materials.new('acid-water'); m.use_nodes = True; nt = m.node_tree
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = 'acid_depth'
    dep = nt.nodes.new('ShaderNodeMapRange'); dep.inputs['From Min'].default_value = 0.0
    dep.inputs['From Max'].default_value = p.get('acid_deep', 0.09)
    nt.links.new(at.outputs['Fac'], dep.inputs['Value'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    stops = p.get('acid_colors', [(0.0, '#DCE08A'), (0.35, '#B4C84A'), (1.0, '#6E9426')])
    while len(cr.elements) < len(stops):
        cr.elements.new(0.5)
    for e, (pos, col) in zip(cr.elements, stops):
        e.position = pos; e.color = _hex(col)
    nt.links.new(dep.outputs['Result'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    edge = nt.nodes.new('ShaderNodeMapRange'); edge.inputs['From Min'].default_value = 0.0
    edge.inputs['From Max'].default_value = p.get('acid_edge', 0.012); edge.inputs['To Min'].default_value = 0.0
    nt.links.new(at.outputs['Fac'], edge.inputs['Value'])
    nt.links.new(edge.outputs['Result'], bs.inputs['Alpha'])
    bs.inputs['Roughness'].default_value = p.get('acid_roughness', 0.03)
    bs.inputs['IOR'].default_value = 1.34
    bs.inputs['Subsurface Weight'].default_value = 0.35
    bs.inputs['Subsurface Radius'].default_value = (0.03, 0.05, 0.015)
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 2.5; nz.inputs['Detail'].default_value = 5.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.035; bp.inputs['Distance'].default_value = 0.01
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], bs.inputs['Normal'])
    return m


def crust_material(bpy, p, attribute='acid_d', name='acid-crust'):
    """The photographed crust (its grain, cracks and relief) coloured as Dallol is: salt at the water, sulphur, rust."""
    m = assets.pbr(bpy, p.get('texture', 'rock_boulder_cracked'), p.get('res', '2k'), scale=p.get('tex_scale'),
                   rough_mul=p.get('rough_mul', 1.0), bump=p.get('bump', 1.0), name=name,
                   displace=p.get('displace', 0.008))
    nt = m.node_tree
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    link = next((l for l in nt.links if l.to_socket == bs.inputs['Base Color']), None)
    tex_col = link.from_socket if link else None
    # the texture's own light and dark, kept as detail (normalised round its middle grey)
    bw = nt.nodes.new('ShaderNodeRGBToBW')
    if tex_col:
        nt.links.new(tex_col, bw.inputs['Color'])
    det = nt.nodes.new('ShaderNodeMath'); det.operation = 'MULTIPLY'; det.inputs[1].default_value = p.get('detail_gain', 2.4)
    nt.links.new(bw.outputs['Val'], det.inputs[0])
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = p.get('detail_pow', 0.8)
    nt.links.new(det.outputs['Value'], pw.inputs[0])
    # where: height above the acid (attribute) and a slow noise in world space
    at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = attribute or 'none'
    dn = nt.nodes.new('ShaderNodeMapRange'); dn.inputs['From Min'].default_value = 0.0
    dn.inputs['From Max'].default_value = p.get('zone_h', 0.25)
    nt.links.new(at.outputs['Fac'], dn.inputs['Value'])
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = p.get('zone_scale', 0.22)
    nz.inputs['Detail'].default_value = 6.0; nz.inputs['Roughness'].default_value = 0.62
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    mix = nt.nodes.new('ShaderNodeMath'); mix.operation = 'MULTIPLY_ADD'
    mix.inputs[1].default_value = p.get('noise_w', 1.1)
    mix.inputs[2].default_value = -0.55 * p.get('noise_w', 1.1) + p.get('zone_bias', 0.0)
    nt.links.new(nz.outputs['Fac'], mix.inputs[0])
    add = nt.nodes.new('ShaderNodeMath'); add.operation = 'ADD'
    nt.links.new(dn.outputs['Result'], add.inputs[0]); nt.links.new(mix.outputs['Value'], add.inputs[1])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    stops = p.get('zones', [(0.0, '#EAE6CF'), (0.12, '#F0E58A'), (0.3, '#E2C52A'), (0.55, '#CFA82A'),
                            (0.72, '#B8681F'), (0.9, '#8C3F18')])
    while len(cr.elements) < len(stops):
        cr.elements.new(0.5)
    for e, (pos, col) in zip(cr.elements, stops):
        e.position = pos; e.color = _hex(col)
    nt.links.new(add.outputs['Value'], ramp.inputs['Fac'])
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs['Factor'].default_value = 1.0
    nt.links.new(ramp.outputs['Color'], mul.inputs['A'])
    cm = nt.nodes.new('ShaderNodeCombineColor')
    for k in ('Red', 'Green', 'Blue'):
        nt.links.new(pw.outputs['Value'], cm.inputs[k])
    nt.links.new(cm.outputs['Color'], mul.inputs['B'])
    nt.links.new(mul.outputs['Result'], bs.inputs['Base Color'])
    # damp near the acid: smoother, darker
    wet = nt.nodes.new('ShaderNodeMapRange'); wet.inputs['From Min'].default_value = 0.0
    wet.inputs['From Max'].default_value = 0.03; wet.inputs['To Min'].default_value = 0.25; wet.inputs['To Max'].default_value = 1.0
    nt.links.new(at.outputs['Fac'], wet.inputs['Value'])
    rl = next((l for l in nt.links if l.to_socket == bs.inputs['Roughness']), None)
    if rl:
        rm = nt.nodes.new('ShaderNodeMath'); rm.operation = 'MULTIPLY'
        nt.links.new(rl.from_socket, rm.inputs[0]); nt.links.new(wet.outputs['Result'], rm.inputs[1])
        nt.links.new(rm.outputs['Value'], bs.inputs['Roughness'])
    return m


def chimney(bpy, name, p, kit):
    """A lumpy chimney of sulphur or salt: a tapering column swollen and pinched by noise, standing in the crust."""
    H, R = p.get('height', 0.8), p.get('radius', 0.3)
    rnd = random.Random(p.get('seed', 1)); off = rnd.uniform(0, 100)
    bm = bmesh.new()
    rows, seg = 90, 96
    rings = []
    for j in range(rows + 1):
        t = j / rows
        z = H * t - 0.05
        base = R * (1 - 0.45 * t) * (1 + 0.5 * (1 - t) ** 5)       # a column, flared at its foot
        if t > 0.8:                                                  # a knobbly rounded top
            base *= math.sqrt(max(0.0, 1 - ((t - 0.8) / 0.2) ** 2)) * 0.9 + 0.1 * (1 - t) / 0.2
        ring = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            n = noise.noise(Vector((math.cos(a) * 1.3 + off, math.sin(a) * 1.3, z / H * 3.2 + off)))
            n2 = noise.noise(Vector((math.cos(a) * 4 + off, math.sin(a) * 4, z / H * 10)))
            n3 = noise.noise(Vector((math.cos(a) * 9 + off, math.sin(a) * 9, z / H * 22)))
            r = base * (1 + 0.3 * n + 0.12 * abs(n2) + 0.06 * abs(n3))      # knobs on knobs, a cauliflower crust
            ring.append(bm.verts.new((r * math.cos(a), r * math.sin(a), z)))
        rings.append(ring)
    for a_, b_ in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            bm.faces.new((a_[i], a_[j], b_[j], b_[i]))
    top = bm.verts.new((0, 0, H + 0.01))
    for i in range(seg):
        bm.faces.new((rings[-1][i], rings[-1][(i + 1) % seg], top))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    c = p.get('colors', ['#F2EDCF', '#E9D33A', '#D9B62A'])
    mat = crust_material(bpy, {'texture': p.get('texture', 'rock_boulder_cracked'), 'res': p.get('res', '2k'), 'zone_scale': 1.6,
                               'noise_w': 1.4, 'zone_h': 1.0, 'zone_bias': 0.5, 'detail_gain': p.get('detail_gain', 2.2),
                               'zones': [(0.0, c[0]), (0.45, c[1]), (1.0, c[2])]}, attribute=None, name=f'{name}-mat')
    return kit.finish(bpy, name, bm, p, True, mat)


def steam(bpy, name, p, kit):
    """A plume of steam: a soft volume whose density thins to its edge and breaks up in noise."""
    rx, ry, rz = p.get('size', [1.0, 1.0, 2.5])
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * rx, v.co.y * ry, (v.co.z + 1) * rz * 0.5))
    m = bpy.data.materials.new(f'{name}-steam'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = _hex(p.get('color', '#F4F1E6'))
    vol.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.55)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    # density: 1 at the axis, 0 at the skin, thinning upward, broken by noise
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    sc = nt.nodes.new('ShaderNodeVectorMath'); sc.operation = 'MULTIPLY'
    sc.inputs[1].default_value = (1 / rx, 1 / ry, 0.0)
    nt.links.new(tc.outputs['Object'], sc.inputs[0])
    ln = nt.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'; nt.links.new(sc.outputs['Vector'], ln.inputs[0])
    rad = nt.nodes.new('ShaderNodeMapRange'); rad.inputs['From Min'].default_value = 1.0; rad.inputs['From Max'].default_value = 0.0
    nt.links.new(ln.outputs['Value'], rad.inputs['Value'])
    up = nt.nodes.new('ShaderNodeMapRange'); up.inputs['From Min'].default_value = rz; up.inputs['From Max'].default_value = 0.0
    nt.links.new(sep.outputs['Z'], up.inputs['Value'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = p.get('noise_scale', 2.6)
    nz.inputs['Detail'].default_value = 10.0; nz.inputs['Roughness'].default_value = 0.65
    nz.inputs['Distortion'].default_value = p.get('distortion', 1.2)
    st = nt.nodes.new('ShaderNodeVectorMath'); st.operation = 'MULTIPLY'; st.inputs[1].default_value = (1.0, 1.0, 0.45)
    nt.links.new(tc.outputs['Object'], st.inputs[0])                # stretched upward: it rises
    nt.links.new(st.outputs['Vector'], nz.inputs['Vector'])
    nr = nt.nodes.new('ShaderNodeMapRange'); nr.inputs['From Min'].default_value = 0.5; nr.inputs['From Max'].default_value = 0.8
    nt.links.new(nz.outputs['Fac'], nr.inputs['Value'])
    m1 = nt.nodes.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'
    nt.links.new(rad.outputs['Result'], m1.inputs[0]); nt.links.new(up.outputs['Result'], m1.inputs[1])
    m2 = nt.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'
    nt.links.new(m1.outputs['Value'], m2.inputs[0]); nt.links.new(nr.outputs['Result'], m2.inputs[1])
    sq = nt.nodes.new('ShaderNodeMath'); sq.operation = 'POWER'; sq.inputs[1].default_value = 1.6
    nt.links.new(m2.outputs['Value'], sq.inputs[0])
    m3 = nt.nodes.new('ShaderNodeMath'); m3.operation = 'MULTIPLY'; m3.inputs[1].default_value = p.get('density', 1.5)
    nt.links.new(sq.outputs['Value'], m3.inputs[0])
    nt.links.new(m3.outputs['Value'], vol.inputs['Density'])
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    ob.rotation_euler.z = math.radians(p.get('turn', 0.0))
    return [ob]
