"""Smoke's second concept (round 31b): a misty birch wood on a white winter morning. Two pieces Poly Haven has no
asset for:

- birches: white birch trunks, each its own object (a tapered, slightly crooked tube), barked with a procedural birch
  skin: chalk-white with grey-green patches, short dark horizontal lenticels, black scars and a blackened, fissured
  foot, over a scanned bark's normal map for micro-relief. `trunks` [[x, y, radius, lean_deg, lean_dir_deg], ...],
  `height` metres (tall enough to leave the frame), `seed`, `bark` (a Poly Haven bark id for its normal map).
- smoke: woodsmoke drifting in a layer, a volume box `box` [x0, y0, z0, x1, y1, z1] whose density is wispy noise
  stretched along `drift` (degrees about z), banded about `height` (a band `thickness` thick), `density` per metre at
  its thickest, `color` its scatter colour and `absorb` how much it darkens (woodsmoke reads a little grey-blue against
  white mist), `seed`.
"""
import math, random

import bmesh
from mathutils import Vector, noise


def _lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return [((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c]


def _node(nt, kind, x, y, **inputs):
    n = nt.nodes.new(kind); n.location = (x, y)
    for k, v in inputs.items():
        n.inputs[k].default_value = v
    return n


def _ramp(nt, x, y, stops):
    r = nt.nodes.new('ShaderNodeValToRGB'); r.location = (x, y); cr = r.color_ramp
    cr.elements[0].position, cr.elements[0].color = stops[0][0], (*stops[0][1], 1)
    cr.elements[1].position, cr.elements[1].color = stops[-1][0], (*stops[-1][1], 1)
    for p, c in stops[1:-1]:
        e = cr.elements.new(p); e.color = (*c, 1)
    return r


def _noise(nt, vec, x, y, scale, detail=4.0, rough=0.55, distortion=0.0):
    n = _node(nt, 'ShaderNodeTexNoise', x, y, Scale=1.0, Detail=detail, Roughness=rough, Distortion=distortion)
    sc = _node(nt, 'ShaderNodeVectorMath', x - 200, y); sc.operation = 'MULTIPLY'
    sc.inputs[1].default_value = scale
    nt.links.new(vec, sc.inputs[0]); nt.links.new(sc.outputs['Vector'], n.inputs['Vector'])
    return n


def birch_material(bpy, bark='bark_willow', res='2k', name='birch-bark', p_len=(0.63, 0.69), p_scar=(0.665, 0.71)):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); L = nt.links.new
    out = _node(nt, 'ShaderNodeOutputMaterial', 1400, 0)
    bs = _node(nt, 'ShaderNodeBsdfPrincipled', 1100, 0)
    L(bs.outputs['BSDF'], out.inputs['Surface'])
    tc = _node(nt, 'ShaderNodeTexCoord', -1400, 0)
    oi = _node(nt, 'ShaderNodeObjectInfo', -1400, -300)
    # each trunk its own pattern: its object coordinates offset by its random number
    off = _node(nt, 'ShaderNodeVectorMath', -1200, 0); off.operation = 'ADD'
    rv = _node(nt, 'ShaderNodeCombineXYZ', -1400, -500)
    mr = _node(nt, 'ShaderNodeMath', -1600, -500); mr.operation = 'MULTIPLY'; mr.inputs[1].default_value = 97.0
    L(oi.outputs['Random'], mr.inputs[0])
    for k in ('X', 'Y', 'Z'):
        L(mr.outputs['Value'], rv.inputs[k])
    L(tc.outputs['Object'], off.inputs[0]); L(rv.outputs['Vector'], off.inputs[1])
    vec = off.outputs['Vector']
    sz = _node(nt, 'ShaderNodeSeparateXYZ', -1200, -700); L(tc.outputs['Object'], sz.inputs['Vector'])
    # the skin: chalk white wandering to a cool grey and, here and there, a warm peeled cream
    base = _noise(nt, vec, -800, 600, (2.2, 2.2, 0.9), detail=6)
    cbase = _ramp(nt, -550, 600, [(0.30, _lin('#C9C8C0')), (0.5, _lin('#E9E7E0')), (0.62, _lin('#F1EFEA')),
                                   (0.74, _lin('#DAD3C6'))])
    L(base.outputs['Fac'], cbase.inputs['Fac'])
    # lenticels: short dark dashes across the trunk, a few centimetres wide, a few millimetres tall
    len_n = _noise(nt, vec, -800, 250, (13.0, 13.0, 150.0), detail=2, rough=0.45)
    len_m = _node(nt, 'ShaderNodeMapRange', -550, 250, **{'From Min': p_len[0], 'From Max': p_len[1]})
    L(len_n.outputs['Fac'], len_m.inputs['Value'])
    # scars: broader black horizontal patches (old branch marks, cracks)
    scar_n = _noise(nt, vec, -800, -50, (2.6, 2.6, 11.0), detail=5, rough=0.62, distortion=0.5)
    scar_m = _node(nt, 'ShaderNodeMapRange', -550, -50, **{'From Min': p_scar[0], 'From Max': p_scar[1]})
    L(scar_n.outputs['Fac'], scar_m.inputs['Value'])
    # the foot: blackened and fissured, fading out over the first metre or so
    foot = _node(nt, 'ShaderNodeMapRange', -800, -350, **{'From Min': 1.3, 'From Max': 0.15})
    L(sz.outputs['Z'], foot.inputs['Value'])
    fiss = _noise(nt, vec, -800, -600, (9.0, 9.0, 2.0), detail=8, rough=0.7, distortion=0.8)
    fiss_m = _node(nt, 'ShaderNodeMath', -550, -450); fiss_m.operation = 'MULTIPLY'
    L(fiss.outputs['Fac'], fiss_m.inputs[0]); L(foot.outputs['Result'], fiss_m.inputs[1])
    fiss_t = _node(nt, 'ShaderNodeMapRange', -350, -450, **{'From Min': 0.30, 'From Max': 0.55})
    L(fiss_m.outputs['Value'], fiss_t.inputs['Value'])
    # dark = max(lenticel, scar, foot)
    mx1 = _node(nt, 'ShaderNodeMath', -300, 150); mx1.operation = 'MAXIMUM'
    L(len_m.outputs['Result'], mx1.inputs[0]); L(scar_m.outputs['Result'], mx1.inputs[1])
    mx2 = _node(nt, 'ShaderNodeMath', -150, 0); mx2.operation = 'MAXIMUM'
    L(mx1.outputs['Value'], mx2.inputs[0]); L(fiss_t.outputs['Result'], mx2.inputs[1])
    mix = _node(nt, 'ShaderNodeMix', 300, 400); mix.data_type = 'RGBA'
    mix.inputs['B'].default_value = (*_lin('#2B2825'), 1)
    L(mx2.outputs['Value'], mix.inputs['Factor']); L(cbase.outputs['Color'], mix.inputs['A'])
    L(mix.outputs['Result'], bs.inputs['Base Color'])
    rough = _node(nt, 'ShaderNodeMapRange', 600, -100, **{'To Min': 0.62, 'To Max': 0.88})
    L(mx2.outputs['Value'], rough.inputs['Value']); L(rough.outputs['Result'], bs.inputs['Roughness'])
    # relief: the dark marks sunk, the skin's fine papery grain, and a scanned bark's normals faintly under it all
    hgt = _node(nt, 'ShaderNodeMath', 300, -300); hgt.operation = 'SUBTRACT'
    grain = _noise(nt, vec, 0, -600, (60.0, 60.0, 300.0), detail=3)
    L(grain.outputs['Fac'], hgt.inputs[0]); L(mx2.outputs['Value'], hgt.inputs[1])
    bump = _node(nt, 'ShaderNodeBump', 800, -300, Strength=0.35, Distance=0.004)
    L(hgt.outputs['Value'], bump.inputs['Height'])
    try:
        import assets
        maps = assets.texture(bark, res, maps=('nor_gl',))
        img = nt.nodes.new('ShaderNodeTexImage'); img.location = (300, -700)
        img.image = bpy.data.images.load(maps['nor_gl'], check_existing=True); img.image.colorspace_settings.name = 'Non-Color'
        img.projection = 'BOX'; img.projection_blend = 0.3
        mp = _node(nt, 'ShaderNodeMapping', 100, -700); mp.inputs['Scale'].default_value = (2.5, 2.5, 1.2)
        L(vec, mp.inputs['Vector']); L(mp.outputs['Vector'], img.inputs['Vector'])
        nm = _node(nt, 'ShaderNodeNormalMap', 550, -700, Strength=0.45)
        L(img.outputs['Color'], nm.inputs['Color']); L(nm.outputs['Normal'], bump.inputs['Normal'])
    except Exception as e:                                           # no network: the procedural relief alone
        print('smoke_b_el: no bark normals', e)
    L(bump.outputs['Normal'], bs.inputs['Normal'])
    return m


def _trunk(bm, r0, height, lean, lean_dir, rnd, sides=28, step=0.2):
    """A tapered tube from z 0 (a little below the ground) to `height`, bending gently, its section a touch uneven."""
    rings = []
    n = int(height / step) + 1
    ph = rnd.uniform(0, 100)
    dx, dy = math.cos(math.radians(lean_dir)), math.sin(math.radians(lean_dir))
    for i in range(n + 1):
        z = -0.15 + i * step
        t = max(0.0, z) / height
        r = r0 * (1.0 - 0.55 * t) * (1.0 + 0.35 * max(0.0, 0.5 - z) ** 2)       # tapering, flaring at the foot
        bend = math.tan(math.radians(lean)) * z + 0.25 * math.sin(z * 0.45 + ph) * t
        cx = dx * bend + 0.06 * noise.noise(Vector((ph, z * 0.3, 0.0)))
        cy = dy * bend + 0.06 * noise.noise(Vector((ph, 0.0, z * 0.3)))
        ring = []
        for k in range(sides):
            a = 2 * math.pi * k / sides
            rr = r * (1.0 + 0.05 * noise.noise(Vector((math.cos(a) * 1.5 + ph, math.sin(a) * 1.5, z * 1.2))))
            ring.append(bm.verts.new((cx + rr * math.cos(a), cy + rr * math.sin(a), z)))
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for k in range(sides):
            bm.faces.new((a[k], a[(k + 1) % sides], b[(k + 1) % sides], b[k]))
    bm.faces.new(rings[-1])


def birches(bpy, name, p, kit):
    mat = birch_material(bpy, p.get('bark', 'bark_willow'))
    rnd = random.Random(p.get('seed', 3))
    obs = []
    for i, t in enumerate(p['trunks']):
        x, y, r = t[0], t[1], t[2]
        lean = t[3] if len(t) > 3 else rnd.uniform(0, 3)
        ldir = t[4] if len(t) > 4 else rnd.uniform(0, 360)
        bm = bmesh.new()
        _trunk(bm, r, p.get('height', 16.0) * rnd.uniform(0.9, 1.1), lean, ldir, rnd)
        for k in range(1, int(t[5]) if len(t) > 5 else 1):          # a clump: more stems from one foot, leaning apart
            sub = bmesh.new()
            a = ldir + 180 + rnd.uniform(-50, 50) * k
            _trunk(sub, r * rnd.uniform(0.6, 0.85), p.get('height', 16.0) * rnd.uniform(0.75, 0.95), lean + rnd.uniform(4, 9), a, rnd)
            off = Vector((math.cos(math.radians(a)), math.sin(math.radians(a)), 0)) * r * 0.9
            bmesh.ops.translate(sub, vec=off, verts=sub.verts[:])
            tmp = bpy.data.meshes.new('tmp'); sub.to_mesh(tmp); sub.free(); bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)
        me = bpy.data.meshes.new(f'{name}-{i}'); bm.to_mesh(me); bm.free()
        for f in me.polygons:
            f.use_smooth = True
        me.materials.append(mat)
        ob = bpy.data.objects.new(f'{name}-{i}', me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (x, y, 0.0)
        obs.append(ob)
    return obs


def smoke(bpy, name, p, kit):
    x0, y0, z0, x1, y1, z1 = p.get('box', [-10, 5, 0, 10, 30, 5])
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); L = nt.links.new
    out = _node(nt, 'ShaderNodeOutputMaterial', 1200, 0)
    vol = _node(nt, 'ShaderNodeVolumePrincipled', 900, 0)
    vol.inputs['Color'].default_value = (*_lin(p.get('color', '#D2D6DC')), 1)
    vol.inputs['Absorption Color'].default_value = (*_lin(p.get('absorb_color', '#6E7680')), 1)
    vol.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.2)
    L(vol.outputs['Volume'], out.inputs['Volume'])
    tc = _node(nt, 'ShaderNodeTexCoord', -1400, 0)
    rot = _node(nt, 'ShaderNodeMapping', -1200, 0)
    rot.inputs['Rotation'].default_value = (0.0, 0.0, -math.radians(p.get('drift', 0.0)))
    rot.inputs['Location'].default_value = (p.get('seed', 1) * 13.1, p.get('seed', 1) * 7.7, 0.0)
    L(tc.outputs['Object'], rot.inputs['Vector'])
    # wisps: the ridges of a distorted noise (thin streaks and curls where it crosses one half), sharpened by
    # `sharp`, inside patches of a broader noise (`lo`..`hi` of it), so the smoke comes in drifts, not a wall
    w = _noise(nt, rot.outputs['Vector'], -900, 200, tuple(p.get('scale', (0.5, 0.5, 1.6))), detail=p.get('detail', 3.0),
               rough=0.55, distortion=p.get('distortion', 1.6))
    r1 = _node(nt, 'ShaderNodeMath', -700, 200); r1.operation = 'MULTIPLY_ADD'
    r1.inputs[1].default_value = 2.0; r1.inputs[2].default_value = -1.0; L(w.outputs['Fac'], r1.inputs[0])
    r2 = _node(nt, 'ShaderNodeMath', -550, 200); r2.operation = 'ABSOLUTE'; L(r1.outputs['Value'], r2.inputs[0])
    r3 = _node(nt, 'ShaderNodeMath', -400, 200); r3.operation = 'SUBTRACT'; r3.inputs[0].default_value = 1.0
    L(r2.outputs['Value'], r3.inputs[1])
    r4 = _node(nt, 'ShaderNodeMath', -250, 200); r4.operation = 'POWER'; r4.inputs[1].default_value = p.get('sharp', 4.0)
    L(r3.outputs['Value'], r4.inputs[0])
    env = _noise(nt, rot.outputs['Vector'], -900, 500, tuple(v * 0.35 for v in p.get('scale', (0.5, 0.5, 1.6))), detail=2)
    em = _node(nt, 'ShaderNodeMapRange', -600, 500, **{'From Min': p.get('lo', 0.42), 'From Max': p.get('hi', 0.6)})
    em.interpolation_type = 'SMOOTHSTEP'; L(env.outputs['Fac'], em.inputs['Value'])
    pw = _node(nt, 'ShaderNodeMath', -100, 200); pw.operation = 'MULTIPLY'
    L(r4.outputs['Value'], pw.inputs[0]); L(em.outputs['Result'], pw.inputs[1])
    # the band: thickest at `height`, gone a `thickness` above and below (in world z: the object sits at the origin)
    sep = _node(nt, 'ShaderNodeSeparateXYZ', -700, -200); L(tc.outputs['Object'], sep.inputs['Vector'])
    dz = _node(nt, 'ShaderNodeMath', -500, -200); dz.operation = 'SUBTRACT'; dz.inputs[1].default_value = p.get('height', 1.5)
    L(sep.outputs['Z'], dz.inputs[0])
    dv = _node(nt, 'ShaderNodeMath', -350, -200); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = p.get('thickness', 1.5)
    L(dz.outputs['Value'], dv.inputs[0])
    sq = _node(nt, 'ShaderNodeMath', -200, -200); sq.operation = 'MULTIPLY'
    L(dv.outputs['Value'], sq.inputs[0]); L(dv.outputs['Value'], sq.inputs[1])
    ex = _node(nt, 'ShaderNodeMath', -50, -200); ex.operation = 'MULTIPLY'; ex.inputs[1].default_value = -1.0
    L(sq.outputs['Value'], ex.inputs[0])
    g = _node(nt, 'ShaderNodeMath', 100, -200); g.operation = 'EXPONENT'; L(ex.outputs['Value'], g.inputs[0])
    # and fading in along x from `fade_x` (the smoke drifts in from one side)
    fx = _node(nt, 'ShaderNodeMapRange', -200, -450, **{'From Min': p.get('fade_x', [x0, x0 + 4])[0],
                                                         'From Max': p.get('fade_x', [x0, x0 + 4])[1]})
    L(sep.outputs['X'], fx.inputs['Value'])
    a = _node(nt, 'ShaderNodeMath', 300, 0); a.operation = 'MULTIPLY'; L(pw.outputs['Value'], a.inputs[0]); L(g.outputs['Value'], a.inputs[1])
    b = _node(nt, 'ShaderNodeMath', 450, 0); b.operation = 'MULTIPLY'; L(a.outputs['Value'], b.inputs[0]); L(fx.outputs['Result'], b.inputs[1])
    d = _node(nt, 'ShaderNodeMath', 600, 0); d.operation = 'MULTIPLY'; d.inputs[1].default_value = p.get('density', 0.4)
    L(b.outputs['Value'], d.inputs[0]); L(d.outputs['Value'], vol.inputs['Density'])
    vol.inputs['Absorption Color'].default_value = (*_lin(p.get('absorb_color', '#6E7680')), 1)
    bm = bmesh.new()
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector((x0 + (v.co.x + 0.5) * (x1 - x0), y0 + (v.co.y + 0.5) * (y1 - y0), z0 + (v.co.z + 0.5) * (z1 - z0)))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return [ob]


def mist(bpy, name, p, kit):
    """Mist that thickens with distance: a scattering volume in `box`, clear in front of `clear_y`, rising to `density`
    per metre by `full_y`, and denser near the ground (`ground_boost` more at z 0, gone by `ground_h`)."""
    x0, y0, z0, x1, y1, z1 = p.get('box', [-45, -14, 0, 45, 95, 30])
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); L = nt.links.new
    out = _node(nt, 'ShaderNodeOutputMaterial', 900, 0)
    v = _node(nt, 'ShaderNodeVolumeScatter', 650, 0, Anisotropy=p.get('anisotropy', 0.3))
    v.inputs['Color'].default_value = (*_lin(p.get('color', '#FFFFFF')), 1)
    L(v.outputs['Volume'], out.inputs['Volume'])
    tc = _node(nt, 'ShaderNodeTexCoord', -900, 0)
    sep = _node(nt, 'ShaderNodeSeparateXYZ', -700, 0); L(tc.outputs['Object'], sep.inputs['Vector'])
    ry = _node(nt, 'ShaderNodeMapRange', -450, 100, **{'From Min': p.get('clear_y', 1.0), 'From Max': p.get('full_y', 12.0)})
    ry.interpolation_type = 'SMOOTHSTEP'; L(sep.outputs['Y'], ry.inputs['Value'])
    rz = _node(nt, 'ShaderNodeMapRange', -450, -150, **{'From Min': 0.0, 'From Max': p.get('ground_h', 3.0),
                                                       'To Min': 1.0 + p.get('ground_boost', 0.6), 'To Max': 1.0})
    L(sep.outputs['Z'], rz.inputs['Value'])
    a = _node(nt, 'ShaderNodeMath', -200, 0); a.operation = 'MULTIPLY'
    L(ry.outputs['Result'], a.inputs[0]); L(rz.outputs['Result'], a.inputs[1])
    f = _node(nt, 'ShaderNodeMath', 100, 0); f.operation = 'ADD'; f.inputs[1].default_value = p.get('floor', 0.0)
    L(a.outputs['Value'], f.inputs[0])
    d = _node(nt, 'ShaderNodeMath', 350, 0); d.operation = 'MULTIPLY'; d.inputs[1].default_value = p.get('density', 0.05)
    L(f.outputs['Value'], d.inputs[0]); L(d.outputs['Value'], v.inputs['Density'])
    bm = bmesh.new()
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for vv in geom['verts']:
        vv.co = Vector((x0 + (vv.co.x + 0.5) * (x1 - x0), y0 + (vv.co.y + 0.5) * (y1 - y0), z0 + (vv.co.z + 0.5) * (z1 - z0)))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return [ob]


def snow(bpy, name, p, kit):
    """Fresh snow: a scanned snow's height and normals (its relief, true displacement near the lens) under a clean,
    bright skin of our own (the scan's colour carries dark twigs that tile), faintly translucent, with a fine sparkle."""
    import assets
    ob = assets.ground(bpy, name, p.get('texture', 'snow_02'), tuple(p.get('size', [60.0, 60.0])), p.get('res', '4k'),
                       tuple(p.get('position', [0, 0, 0])), p.get('cells'), p.get('displace', 0.015), None, 0.0,
                       p.get('tex_scale'), 1.0, p.get('bump', 1.0), p.get('relief'), tuple(p.get('flat', [0.0, 0.0, 1.2])))
    m = ob.data.materials[0]; nt = m.node_tree; L = nt.links.new
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    for l in list(bs.inputs['Base Color'].links):
        nt.links.remove(l)
    tc = _node(nt, 'ShaderNodeTexCoord', -200, 900)
    n1 = _noise(nt, tc.outputs['Object'], 100, 900, (0.6, 0.6, 0.6), detail=5)
    col = _ramp(nt, 350, 900, [(0.35, _lin(p.get('shade', '#DCDFE3'))), (0.65, _lin(p.get('color', '#F3F4F5')))])
    L(n1.outputs['Fac'], col.inputs['Fac']); L(col.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Subsurface Weight'].default_value = p.get('subsurface', 0.25)
    bs.inputs['Subsurface Radius'].default_value = (0.02, 0.025, 0.03)
    for l in list(bs.inputs['Roughness'].links):
        nt.links.remove(l)
    # sparkle: a few grains turned to the light, smoother than the rest
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.location = (100, 600); vo.inputs['Scale'].default_value = 900.0
    L(tc.outputs['Object'], vo.inputs['Vector'])
    sp = _node(nt, 'ShaderNodeMapRange', 350, 600, **{'From Min': 0.08, 'From Max': 0.02, 'To Min': 0.75, 'To Max': 0.25})
    L(vo.outputs['Distance'], sp.inputs['Value'])
    L(sp.outputs['Result'], bs.inputs['Roughness'])
    return [ob]


def dry_scatter(bpy, name, p, kit):
    """Scanned plants scattered (assets.scatter's arguments) and turned to winter: their colour drained and lifted
    toward straw (`saturation`, `value`, `hue`), so last summer's grass pokes dry through the snow."""
    import assets
    before = set(bpy.data.materials)
    made = assets.scatter(bpy, p['models'], p.get('res', '1k'), p.get('count', 20), tuple(p.get('area', [-3, -3, 3, 3])),
                          [tuple(a) for a in p.get('avoid', [])], tuple(p.get('scale', [0.8, 1.2])), p.get('z', 0.0),
                          p.get('seed', 1), True, p.get('tilt_deg', 0.0))
    for m in set(bpy.data.materials) - before:
        if not m.use_nodes:
            continue
        nt = m.node_tree
        bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not bs or not bs.inputs['Base Color'].links:
            continue
        src = bs.inputs['Base Color'].links[0].from_socket
        hs = nt.nodes.new('ShaderNodeHueSaturation')
        hs.inputs['Hue'].default_value = p.get('hue', 0.42)
        hs.inputs['Saturation'].default_value = p.get('saturation', 0.35)
        hs.inputs['Value'].default_value = p.get('value', 1.5)
        nt.links.new(src, hs.inputs['Color']); nt.links.new(hs.outputs['Color'], bs.inputs['Base Color'])
    return made


def snow_lip(bpy, name, p, kit):
    """Snow banked a little against the speaker's foot: a soft ring round its footprint (`size` [w, d] m, turned
    `rotate_z` degrees), `height` at the wall falling to nothing over `reach`, in the snow's own material (taken from
    the object `mat_object`), so the cabinet stands in the snow, not on it."""
    w, d = p.get('size', [0.56, 0.42]); h = p.get('height', 0.022); reach = p.get('reach', 0.12)
    rings, seg = 7, 96
    bm = bmesh.new()
    rows = []
    for i in range(rings + 1):
        t = i / rings                                              # 0 at the wall (inside it a little), 1 at the edge
        off = -0.01 + t * (reach + 0.01)
        z = h * (1 - t) ** 1.6 * (0.9 + 0.1 * math.cos(t * math.pi))
        row = []
        for k in range(seg):
            a = 2 * math.pi * k / seg
            # a rounded rectangle: the superellipse through the footprint, pushed out by `off`
            ca, sa = math.cos(a), math.sin(a)
            x = math.copysign(abs(ca) ** 0.25, ca) * (w / 2 + off)
            y = math.copysign(abs(sa) ** 0.25, sa) * (d / 2 + off)
            n = noise.noise(Vector((x * 9, y * 9, 0.3)))
            row.append(bm.verts.new((x, y, max(0.0, z * (1 + 0.35 * n)) - 0.004)))
        rows.append(row)
    for a_, b_ in zip(rows, rows[1:]):
        for k in range(seg):
            bm.faces.new((a_[k], a_[(k + 1) % seg], b_[(k + 1) % seg], b_[k]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    src = bpy.data.objects.get(p.get('mat_object', 'prop0-kit'))
    if src and src.data.materials:
        me.materials.append(src.data.materials[0])
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = tuple(p.get('position', [0, 0, 0])); ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    return [ob]
