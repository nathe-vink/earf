"""Haze, concept B (round 31b): layered hills at blue hour. The set's own pieces, as kit `ext` pieces
({"shape": "ext", "module": "haze_b_el", "fn": ...}):

- ridge: the near ridge the speaker stands on, a dense heightfield laid with a photographed texture, level under the
  speaker, its crest `crest_y` metres behind it and the ground falling away beyond (`drop`, metres at the far edge);
- hills: layer after layer of hills behind, each a heightfield whose crest wanders along x, with scrub on its crest
  (`fuzz`); `layers` [{d, crest, amp, front, back, height, seed}], laid with a photographed aerial texture. The far
  layers stand at a tenth of their true distance and size (the camera clips at 300 m; perspective from one point is
  the same at any scale, and at these distances the lens is at infinity either way);
- haze: boxes of scattering haze (`boxes` [{box, density, color, anisotropy}]) the layers recede into;
- sundisk: the pale sun, a disk facing the camera at `azimuth`/`elevation` and `distance`, seen through the haze, that
  lights nothing (the sun lamp does);
- tufts: scanned grass, scattered and dried: their green turned to straw (`hue`, `sat`, `val`).
"""
import math, random

import bmesh
from mathutils import Vector, noise


def _fbm(x, y, octaves=5, seed=0.0):
    a, f, s = 1.0, 1.0, 0.0
    for _ in range(octaves):
        s += a * noise.noise(Vector((x * f, y * f, seed)))
        a *= 0.5; f *= 2.03
    return s


def _grid(nx, ny, x0, x1, y0, y1, zf):
    bm = bmesh.new()
    vs = []
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        row = []
        for i in range(nx + 1):
            x = x0 + (x1 - x0) * i / nx
            row.append(bm.verts.new((x, y, zf(x, y))))
        vs.append(row)
    for j in range(ny):
        for i in range(nx):
            bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
    return bm


def _mat(bpy, p, kit):
    import assets
    m = assets.pbr(bpy, p['texture'], p.get('res', '2k'), scale=p.get('tex_scale'), displace=p.get('displace', 0.0),
                   tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0), rough_mul=p.get('rough_mul', 1.0),
                   bump=p.get('bump', 1.0), name=p.get('name'))
    if p.get('value', 1.0) != 1.0:                                    # the texture's albedo scaled (a darker ground)
        nt = m.node_tree
        bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
        src = bs.inputs['Base Color'].links[0].from_socket
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'
        mx.inputs['Factor'].default_value = 1.0
        v = p['value']; mx.inputs['B'].default_value = (v, v, v, 1.0)
        nt.links.new(src, mx.inputs['A']); nt.links.new(mx.outputs['Result'], bs.inputs['Base Color'])
    if p.get('matte'):                                                # dry soil: no sheen of the sky on it
        bs = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
        for l in list(bs.inputs['Roughness'].links):
            m.node_tree.links.remove(l)
        bs.inputs['Roughness'].default_value = 1.0
        bs.inputs['Specular IOR Level'].default_value = 0.0
    return m


def ridge(bpy, name, p, kit):
    x0, y0, x1, y1 = p.get('area', [-8.0, -14.0, 8.0, 7.0])
    cell = p.get('cell', 0.02)
    cy, drop, relief = p.get('crest_y', 1.2), p.get('drop', 5.0), p.get('relief', 0.12)
    slope_front = p.get('slope_front', 0.03)                      # metres of fall per metre toward the camera
    fr = p.get('flat_r', 0.8)

    def z(x, y):
        r = math.hypot(x, y)
        t = min(1.0, max(0.0, (r - fr) / fr)); t = t * t * (3 - 2 * t)
        h = t * relief * _fbm(x * 0.4, y * 0.4, 3, 1.7)
        cyx = cy + 0.6 * noise.noise(Vector((x * 0.15, 0.3, 2.2)))   # the crest wanders
        if y > cyx:
            u = (y - cyx) / max(0.01, y1 - cyx)
            h -= drop * (u ** 1.6) * (1.0 + 0.3 * noise.noise(Vector((x * 0.3, 5.0, 0.0))))
        elif y < -fr:
            h -= slope_front * (-fr - y) * t
        return h
    nx = int((x1 - x0) / cell); ny = int((y1 - y0) / cell)
    bm = _grid(nx, ny, x0, x1, y0, y1, z)
    return kit.finish(bpy, name, bm, {**p, 'position': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': 1.0}, mat=_mat(bpy, p, kit))


def hills(bpy, name, p, kit):
    """Layers of hills: each crest at y = d (wandering), `crest` metres high (on average), `amp` its rise and fall along
    x, falling `height` metres to the valley in front over `front` metres and behind over `back`."""
    out = []
    base = {k: p[k] for k in ('texture', 'res', 'tex_scale', 'tint', 'tint_mix', 'bump', 'rough_mul', 'value') if k in p}
    for k, L in enumerate(p['layers']):
        d, crest, amp = L['d'], L['crest'], L.get('amp', 2.0)
        wf, wb, H = L.get('front', d * 0.25), L.get('back', d * 0.2), L.get('height', d * 0.15)
        X = L.get('half_width', d * 0.7)
        seed = L.get('seed', k * 3.1)
        feat = L.get('feature', d * 0.35)                          # the length of a hill along the range
        fuzz, fuzz_f = L.get('fuzz', 0.0), L.get('fuzz_feature', 0.6)
        x_off = L.get('x', 0.0)

        def cz(x):
            c = crest + amp * _fbm(x / feat, 0.5, 4, seed)
            c += amp * 0.35 * abs(noise.noise(Vector((x / (feat * 0.25), 1.3, seed))))
            if fuzz:
                c += fuzz * max(0.0, _fbm(x / fuzz_f, 2.7, 3, seed + 9.0))
            return c

        def cy(x):
            return d + L.get('wander', min(wf * 0.35, 8.0)) * noise.noise(Vector((x / feat, 4.4, seed)))

        def z(x, y):
            c, yc = cz(x), cy(x)
            u = (y - yc) / (wf if y < yc else wb)
            g = math.exp(-u * u * 1.6)
            # the slope's own folds: ravines down the face
            folds = L.get('folds', p.get('folds', 0.12)) * H * _fbm(x / (feat * 0.3), y / (wf * 0.5), 3, seed + 3.0) * (1 - g)
            return (c - H) + H * g + folds
        nx = L.get('nx', 500); ny = L.get('ny', 60)
        bm = _grid(nx, ny, x_off - X, x_off + X, d - 2.4 * wf, d + 1.8 * wb, z)
        lp = {**base, **{k2: L[k2] for k2 in ('texture', 'tex_scale', 'tint', 'tint_mix', 'value') if k2 in L},
              'name': f'{name}-mat{k}'}
        ob = kit.finish(bpy, f'{name}-{k}', bm, {'position': [0, 0, 0]}, mat=_mat(bpy, lp, kit))
        out += ob
        T = L.get('trees')                                         # trees and scrub on the crest and down its face
        if T:
            import assets
            rnd = random.Random(T.get('seed', 7 + k))
            roots = _roots.setdefault('t', {})
            for mid in T['models']:
                if mid not in roots:
                    roots[mid] = assets.place(bpy, mid, T.get('res', '1k'), (0, 0, -1000))
            x0, x1 = T.get('x', [x_off - X * 0.8, x_off + X * 0.8])
            for _ in range(T['count']):
                x = rnd.uniform(x0, x1)
                yb = cy(x) - rnd.uniform(0.0, T.get('down', 0.25)) ** 1.5 * wf      # mostly on the crest
                zz = z(x, yb) - 0.02 * T.get('scale', [0.2, 0.3])[1]
                sc = rnd.uniform(*T.get('scale', [0.2, 0.3]))
                out.append(assets.instance(bpy, roots[rnd.choice(T['models'])], (x, yb, zz),
                                           (0, 0, rnd.uniform(0, 360)), sc))
    for r in _roots.get('t', {}).values():
        r.hide_render = True
        for o in r.children_recursive:
            o.hide_render = True
    return out


_roots = {}


def haze(bpy, name, p, kit):
    out = []
    for k, b in enumerate(p['boxes']):
        x0, y0, z0, x1, y1, z1 = b['box']
        m = bpy.data.materials.new(f'{name}-vol{k}'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        o = nt.nodes.new('ShaderNodeOutputMaterial'); v = nt.nodes.new('ShaderNodeVolumeScatter')
        v.inputs['Density'].default_value = b.get('density', 0.005)
        v.inputs['Anisotropy'].default_value = b.get('anisotropy', 0.5)
        v.inputs['Color'].default_value = kit.M.hex_lin(b.get('color', '#FFFFFF'))
        nt.links.new(v.outputs['Volume'], o.inputs['Volume'])
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for vt in bm.verts:
            vt.co.x = x0 if vt.co.x < 0 else x1
            vt.co.y = y0 if vt.co.y < 0 else y1
            vt.co.z = z0 if vt.co.z < 0 else z1
        me = bpy.data.meshes.new(f'{name}-{k}'); bm.to_mesh(me); bm.free()
        me.materials.append(m)
        ob = bpy.data.objects.new(f'{name}-{k}', me); bpy.context.scene.collection.objects.link(ob)
        out.append(ob)
    return out


def sundisk(bpy, name, p, kit):
    az, el, D = math.radians(p['azimuth']), math.radians(p['elevation']), p.get('distance', 280.0)
    eye = Vector(p.get('eye', [0.0, 0.0, 1.0]))
    dirv = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    c = eye + dirv * D
    r = D * math.tan(math.radians(p.get('diameter_deg', 0.53) / 2))
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, radius=r, segments=96)
    m = bpy.data.materials.new(f'{name}-mat'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
    e.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#FFE2C8'))
    e.inputs['Strength'].default_value = p.get('emit', 40.0)
    nt.links.new(e.outputs['Emission'], o.inputs['Surface'])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = c
    ob.rotation_euler = (-dirv).to_track_quat('Z', 'Y').to_euler()
    for a in ('visible_diffuse', 'visible_glossy', 'visible_transmission', 'visible_shadow', 'visible_volume_scatter'):
        setattr(ob, a, False)
    return [ob]


def tufts(bpy, name, p, kit):
    """Scanned grass scattered (assets.scatter) and dried: every material of the models gets its colour turned."""
    import assets
    made = assets.scatter(bpy, p['models'], p.get('res', '1k'), p.get('count', 40), tuple(p['area']),
                          [tuple(a) for a in p.get('avoid', [])], tuple(p.get('scale', [0.8, 1.2])), p.get('z', 0.0),
                          p.get('seed', 1), True, p.get('tilt_deg', 6.0))
    zf = p.get('ground')
    if zf:                                                            # sit each on the ridge's surface
        for r in made:
            r.location.z = _ridge_z(zf, r.location.x, r.location.y)
    seen = set()
    for ob in bpy.data.objects:
        if ob.type != 'MESH' or not any(ob.name.startswith(mm) for mm in p['models']):
            continue
        for m in ob.data.materials:
            if m is None or m.name in seen or not m.use_nodes:
                continue
            seen.add(m.name)
            nt = m.node_tree
            bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            if not bs or not bs.inputs['Base Color'].links:
                continue
            src = bs.inputs['Base Color'].links[0].from_socket
            hs = nt.nodes.new('ShaderNodeHueSaturation')
            hs.inputs['Hue'].default_value = p.get('hue', 0.40)
            hs.inputs['Saturation'].default_value = p.get('sat', 0.75)
            hs.inputs['Value'].default_value = p.get('val', 1.25)
            nt.links.new(src, hs.inputs['Color']); nt.links.new(hs.outputs['Color'], bs.inputs['Base Color'])
            if p.get('translucent', 0) > 0:                       # thin blades: the low sun comes through them
                out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
                tr = nt.nodes.new('ShaderNodeBsdfTranslucent'); mx = nt.nodes.new('ShaderNodeMixShader')
                nt.links.new(hs.outputs['Color'], tr.inputs['Color'])
                if bs.inputs['Normal'].links:
                    nt.links.new(bs.inputs['Normal'].links[0].from_socket, tr.inputs['Normal'])
                mx.inputs['Fac'].default_value = p['translucent']
                nt.links.new(bs.outputs['BSDF'], mx.inputs[1]); nt.links.new(tr.outputs['BSDF'], mx.inputs[2])
                if bs.inputs['Alpha'].links:                       # keep the cut-out: blend the mix with transparency
                    tp = nt.nodes.new('ShaderNodeBsdfTransparent'); m2 = nt.nodes.new('ShaderNodeMixShader')
                    nt.links.new(bs.inputs['Alpha'].links[0].from_socket, m2.inputs['Fac'])
                    nt.links.new(tp.outputs['BSDF'], m2.inputs[1]); nt.links.new(mx.outputs['Shader'], m2.inputs[2])
                    nt.links.new(m2.outputs['Shader'], out.inputs['Surface'])
                else:
                    nt.links.new(mx.outputs['Shader'], out.inputs['Surface'])
    return made


def _ridge_z(rp, x, y):
    """The ridge's height at (x, y), for things set on it (the same function as `ridge` builds, without its relief
    detail beyond a few centimetres)."""
    cy, drop, relief = rp.get('crest_y', 1.2), rp.get('drop', 5.0), rp.get('relief', 0.12)
    y1 = rp.get('area', [-8.0, -14.0, 8.0, 7.0])[3]
    fr = rp.get('flat_r', 0.8); sf = rp.get('slope_front', 0.03)
    r = math.hypot(x, y)
    t = min(1.0, max(0.0, (r - fr) / fr)); t = t * t * (3 - 2 * t)
    h = t * relief * _fbm(x * 0.4, y * 0.4, 3, 1.7)
    cyx = cy + 0.6 * noise.noise(Vector((x * 0.15, 0.3, 2.2)))
    if y > cyx:
        u = (y - cyx) / max(0.01, y1 - cyx)
        h -= drop * (u ** 1.6) * (1.0 + 0.3 * noise.noise(Vector((x * 0.3, 5.0, 0.0))))
    elif y < -fr:
        h -= sf * (-fr - y) * t
    return h


def place_on(bpy, name, p, kit):
    """Scanned models (rocks) each placed on the ridge: `items` [{model, x, y, rotate, scale, sink}]."""
    import assets
    out = []
    for k, it in enumerate(p['items']):
        z = _ridge_z(p['ground'], it['x'], it['y']) - it.get('sink', 0.05)
        out.append(assets.place(bpy, it['model'], p.get('res', '2k'), (it['x'], it['y'], z),
                                tuple(it.get('rotate', [0, 0, 0])), it.get('scale', 1.0), f'{name}-{k}'))
    return out


def grass(bpy, name, p, kit):
    """Dry grass as strands (a hair system on a patch of the ridge): straw-coloured blades in clumps, tall and thin, so
    the low sun comes through them and rims them. `area` [x0, y0, x1, y1], `avoid` circles [x, y, r], `count` parent
    strands (each with `children` around it), `length` [min, max] metres, `color` the straw's colour."""
    rp = p['ground']
    x0, y0, x1, y1 = p['area']
    cell = p.get('cell', 0.1)
    avoid = p.get('avoid', [])
    nx, ny = int((x1 - x0) / cell), int((y1 - y0) / cell)
    bm = bmesh.new()
    vs = [[bm.verts.new((x0 + (x1 - x0) * i / nx, y0 + (y1 - y0) * j / ny, 0.0)) for i in range(nx + 1)] for j in range(ny + 1)]
    for row in vs:
        for v in row:
            v.co.z = _ridge_z(rp, v.co.x, v.co.y)
    rnd = random.Random(p.get('seed', 3))
    dens = p.get('patchy', 0.6)
    for j in range(ny):
        for i in range(nx):
            cx = x0 + (x1 - x0) * (i + 0.5) / nx; cyy = y0 + (y1 - y0) * (j + 0.5) / ny
            if any(math.hypot(cx - a[0], cyy - a[1]) < a[2] for a in avoid):
                continue
            if p.get('within') and math.hypot(cx - p['within'][0], cyy - p['within'][1]) > p['within'][2]:
                continue
            if noise.noise(Vector((cx * 0.7, cyy * 0.7, 9.1))) < -dens + 0.4:           # bare patches
                continue
            bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
    for row in vs:
        for v in row:
            if not v.link_faces:
                bm.verts.remove(v)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location.z = p.get('lift', -0.01)
    ps = ob.modifiers.new('grass', 'PARTICLE_SYSTEM').particle_system
    st = ps.settings
    st.type = 'HAIR'; st.count = p.get('count', 6000); st.hair_length = p.get('length', [0.25, 0.55])[1]
    st.use_advanced_hair = True
    st.length_random = 1.0 - p.get('length', [0.25, 0.55])[0] / p.get('length', [0.25, 0.55])[1]
    st.emit_from = 'FACE'; st.distribution = 'RAND'; st.use_even_distribution = True
    st.normal_factor = 1.0; st.tangent_factor = 0.0
    st.brownian_factor = 0.0
    st.hair_step = 6; st.display_step = 3; st.render_step = 4
    st.child_type = 'SIMPLE'; st.rendered_child_count = p.get('children', 14); st.child_percent = 2
    st.child_radius = p.get('clump_r', 0.06); st.child_roundness = 0.6
    st.clump_factor = p.get('clump', -0.4)                            # a tuft fanning out from its root
    st.clump_shape = 0.2
    st.roughness_1 = p.get('rough', 0.04); st.roughness_1_size = p.get('rough_size', 0.6)
    st.roughness_endpoint = p.get('rough_end', 0.05)
    st.roughness_2 = p.get('rough2', 0.03); st.roughness_2_size = 1.0
    st.kink = 'NO'
    st.radius_scale = 1.0
    st.root_radius = p.get('root_mm', 0.9) / 1000.0
    st.tip_radius = p.get('tip_mm', 0.15) / 1000.0
    st.shape = -0.3
    st.use_close_tip = True
    st.hair_length = p.get('length', [0.25, 0.55])[1]
    st.factor_random = p.get('random', 0.3) * st.normal_factor   # strands leaning every way (velocity units: hair_length / 4)
    st.material = 1
    mat = bpy.data.materials.new(f'{name}-straw'); mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    hb = nt.nodes.new('ShaderNodeBsdfHairPrincipled')
    try:
        hb.parametrization = 'COLOR'
    except Exception:
        pass
    col = kit.M.hex_lin(p.get('color', '#B59A72'))
    info = nt.nodes.new('ShaderNodeHairInfo')
    ramp = nt.nodes.new('ShaderNodeMix'); ramp.data_type = 'RGBA'
    ramp.inputs['A'].default_value = kit.M.hex_lin(p.get('color', '#B59A72'))
    ramp.inputs['B'].default_value = kit.M.hex_lin(p.get('color2', '#8C7660'))
    nt.links.new(info.outputs['Random'], ramp.inputs['Factor'])
    col_out = ramp.outputs['Result']
    if p.get('tip'):                                                  # paler, bleached tips
        tip = nt.nodes.new('ShaderNodeMix'); tip.data_type = 'RGBA'
        pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 2.0
        nt.links.new(info.outputs['Intercept'], pw.inputs[0]); nt.links.new(pw.outputs['Value'], tip.inputs['Factor'])
        nt.links.new(col_out, tip.inputs['A']); tip.inputs['B'].default_value = kit.M.hex_lin(p['tip'])
        col_out = tip.outputs['Result']
    if p.get('value_jitter'):                                         # each strand a little lighter or darker
        j = p['value_jitter']
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 1 - j; mr.inputs['To Max'].default_value = 1 + j
        nt.links.new(info.outputs['Random'], mr.inputs['Value'])
        sc = nt.nodes.new('ShaderNodeVectorMath'); sc.operation = 'SCALE'
        nt.links.new(col_out, sc.inputs[0]); nt.links.new(mr.outputs['Result'], sc.inputs['Scale'])
        col_out = sc.outputs['Vector']
    nt.links.new(col_out, hb.inputs['Color'])
    hb.inputs['Roughness'].default_value = p.get('roughness', 0.35)
    try:
        hb.inputs['Radial Roughness'].default_value = 0.6
        hb.inputs['Coat'].default_value = 0.0
    except KeyError:
        pass
    nt.links.new(hb.outputs['BSDF'], out.inputs['Surface'])
    me.materials.append(mat)
    return [ob]
