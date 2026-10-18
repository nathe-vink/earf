"""Ice's own pieces for round 31b (spinoffs/barkhorn/elements/ice.py): snow country at blue hour.

- firs: Poly Haven's scanned firs (each model holds three trees side by side), split into single trees standing on
  their own base, their needles and bark loaded with snow where they face the sky, placed as instances that share
  their meshes. `trees` [[x, y, turn_deg, scale, 'model:variant'], ...], `snow` (0 to 1, how much), `res`.
- cabin: a log cabin at real scale, its logs in weathered wood, a gable roof under a deep blanket of snow, a stone
  chimney, one lit window (`window_emit`, `window_color`) with a lamp inside that spills onto the snow before it.
  `position`, `turn` (degrees), `size` [w, d] metres.
"""
import math, random, sys, os

import bmesh
from mathutils import Matrix, Vector

_TREES = {}


def _hex(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]


def snow_material(bpy, name, color='#F2F6FA', rough=0.6):
    """Fresh snow: bright, slightly blue in its depths (subsurface), a fine sparkle of grains."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*_hex(color), 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Subsurface Weight'].default_value = 0.35
    b.inputs['Subsurface Radius'].default_value = (0.05, 0.08, 0.12)
    b.inputs['Subsurface Scale'].default_value = 0.05
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 40.0; nz.inputs['Detail'].default_value = 8.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.25; bp.inputs['Distance'].default_value = 0.01
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def _snowed(bpy, mat, amount):
    """A copy of a scanned model's material with snow laid on where it faces up: a mix by the world normal's z and a
    patchy noise, keeping the original's alpha (needle cards stay cut out)."""
    m = mat.copy(); m.name = mat.name + '-snow'
    nt = m.node_tree
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output)
    link = out.inputs['Surface'].links[0] if out.inputs['Surface'].links else None
    if link is None:
        return m
    src = link.from_socket
    bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    sn = nt.nodes.new('ShaderNodeBsdfPrincipled')
    sn.inputs['Base Color'].default_value = (*_hex('#F0F4F8'), 1); sn.inputs['Roughness'].default_value = 0.65
    sn.inputs['Subsurface Weight'].default_value = 0.3; sn.inputs['Subsurface Scale'].default_value = 0.03
    if bsdf is not None and bsdf.inputs['Alpha'].links:
        nt.links.new(bsdf.inputs['Alpha'].links[0].from_socket, sn.inputs['Alpha'])
    elif bsdf is not None:
        sn.inputs['Alpha'].default_value = bsdf.inputs['Alpha'].default_value
    geo = nt.nodes.new('ShaderNodeNewGeometry'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(geo.outputs['Normal'], sep.inputs['Vector'])
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 2.5; nz.inputs['Detail'].default_value = 4.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    add = nt.nodes.new('ShaderNodeMath'); add.operation = 'ADD'
    nt.links.new(sep.outputs['Z'], add.inputs[0])
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 0.6
    nt.links.new(nz.outputs['Fac'], mul.inputs[0]); nt.links.new(mul.outputs['Value'], add.inputs[1])
    mr = nt.nodes.new('ShaderNodeMapRange')
    lo = 0.95 - 0.6 * amount
    mr.inputs['From Min'].default_value = lo; mr.inputs['From Max'].default_value = lo + 0.25
    nt.links.new(add.outputs['Value'], mr.inputs['Value'])
    mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(mr.outputs['Result'], mix.inputs['Fac'])
    nt.links.new(src, mix.inputs[1]); nt.links.new(sn.outputs['BSDF'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    return m


def _tree_meshes(bpy, aid, res, amount):
    """The model's trees as meshes standing on their own base at the origin, snowed; imported once."""
    key = (aid, res, round(amount, 3))
    if key in _TREES:
        return _TREES[key]
    import assets
    path = assets.model(aid, res)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    bpy.context.view_layer.update()
    meshes = {}
    cache = {}
    for o in new:
        if o.type != 'MESH':
            continue
        me = o.data.copy()
        me.transform(o.matrix_world)
        xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]; zs = [v.co.z for v in me.vertices]
        me.transform(Matrix.Translation((-(min(xs) + max(xs)) / 2, -(min(ys) + max(ys)) / 2, -min(zs))))
        for i, mat in enumerate(me.materials):
            if mat is None:
                continue
            if mat.name not in cache:
                cache[mat.name] = _snowed(bpy, mat, amount) if amount > 0 and 'dead' not in mat.name else mat
            me.materials[i] = cache[mat.name]
        variant = o.name.split('_LOD')[0][len(aid) + 1:] or 'a'      # 'a', 'b', 'c' (or 'large_a', 'mid_b', ...)
        meshes[variant] = me
    for o in new:
        bpy.data.objects.remove(o, do_unlink=True)
    _TREES[key] = meshes
    return meshes


def firs(bpy, name, p, kit):
    out = []
    amount = p.get('snow', 0.7)
    for i, (x, y, turn, s, which) in enumerate(p['trees']):
        aid, variant = which.split(':') if ':' in which else (which, 'a')
        me = _tree_meshes(bpy, aid, p.get('res', '1k'), amount)[variant]
        ob = bpy.data.objects.new(f'{name}-{i}', me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (x, y, p.get('z', -0.05))
        ob.rotation_euler = (0, 0, math.radians(turn))
        ob.scale = (s, s, s)
        out.append(ob)
    return out


# --- the cabin ---------------------------------------------------------------------------------------------------
def _cyl(bm, a, b, r, seg=14):
    a, b = Vector(a), Vector(b)
    geom = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=(b - a).length)
    q = (b - a).to_track_quat('Z', 'Y')
    bmesh.ops.rotate(bm, verts=geom['verts'], cent=Vector((0, 0, 0)), matrix=q.to_matrix())
    bmesh.ops.translate(bm, vec=(a + b) / 2, verts=geom['verts'])


def _box(bm, c, size, rot=None):
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
        if rot is not None:
            v.co = rot @ v.co
        v.co += Vector(c)


def _obj(bpy, name, bm, mat, loc, turn, smooth=True):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = smooth
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = (0, 0, math.radians(turn))
    return ob


def cabin(bpy, name, p, kit):
    import assets
    loc = tuple(p.get('position', [0, 0, 0])); turn = p.get('turn', 0.0)
    W, D = p.get('size', [6.0, 4.5]); r = 0.15; H = p.get('wall', 2.5)
    pitch = math.radians(p.get('pitch', 38))
    wood = assets.pbr(bpy, p.get('wood', 'pine_bark'), p.get('res', '1k'), scale=p.get('wood_scale'), name=f'{name}-wood')
    stone = assets.pbr(bpy, p.get('stone', 'rock_05'), p.get('res', '1k'), name=f'{name}-stone')
    snow = snow_material(bpy, f'{name}-snow')
    out = []
    # logs, interlocking at the corners, the ends standing proud; a gap in the front wall's logs for the window
    bm = bmesh.new()
    n = int(H / (2 * r))
    wx0, wx1, wz0, wz1 = W * 0.2 - 0.5, W * 0.2 + 0.5, 0.9, 1.9
    for k in range(n):
        z = r + k * 2 * r
        for yy in (-D / 2, D / 2):
            zz = z
            if yy < 0 and wz0 < zz < wz1:                         # the window's gap in the front wall
                _cyl(bm, (-W / 2 - 0.35, yy, zz), (wx0, yy, zz), r * (0.92 + 0.08 * ((k * 7) % 3)))
                _cyl(bm, (wx1, yy, zz), (W / 2 + 0.35, yy, zz), r * (0.92 + 0.08 * ((k * 5) % 3)))
            else:
                _cyl(bm, (-W / 2 - 0.35, yy, zz), (W / 2 + 0.35, yy, zz), r * (0.92 + 0.08 * ((k * 7) % 3)))
        for xx in (-W / 2, W / 2):
            _cyl(bm, (xx, -D / 2 - 0.35, z + r), (xx, D / 2 + 0.35, z + r), r * (0.92 + 0.08 * ((k * 3) % 3)))
    top = r + n * 2 * r
    # the gables, logs shortening toward the ridge
    rise = (D / 2) * math.tan(pitch)
    k = 0
    zz = top
    while zz < top + rise - r:
        half = (D / 2) * (1 - (zz - top) / rise)
        for xx in (-W / 2, W / 2):
            _cyl(bm, (xx, -half, zz + r), (xx, half, zz + r), r * 0.95)
        zz += 2 * r; k += 1
    out.append(_obj(bpy, f'{name}-logs', bm, wood, loc, turn))
    # the roof: two slabs of boards, a deep blanket of snow on each, its edge rounded over the eaves
    over = 0.55
    slope = (D / 2 + over) / math.cos(pitch)
    for side in (-1, 1):
        rot = Matrix.Rotation(-side * pitch, 3, 'X')
        mid = Vector((0, side * (D / 2 + over) / 2, top + rise - (D / 2 + over) / 2 * math.tan(pitch)))
        bm = bmesh.new()
        _box(bm, mid + rot @ Vector((0, 0, 0.06)), (W + 1.1, slope, 0.12), rot)
        out.append(_obj(bpy, f'{name}-roof{side}', bm, wood, loc, turn, smooth=False))
        bm = bmesh.new()
        _box(bm, mid + rot @ Vector((0, 0, 0.12 + 0.18)), (W + 1.3, slope + 0.12, 0.36), rot)
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=0.15, segments=4, affect='EDGES')
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=3, use_grid_fill=True)
        rnd = random.Random(7 + side)
        for v in bm.verts:                                    # drifted, not machined
            v.co += Vector((0, 0, 0.06 * math.sin(v.co.x * 1.7 + rnd.random()) * math.cos(v.co.y * 2.3)))
        out.append(_obj(bpy, f'{name}-snow{side}', bm, snow, loc, turn))
    # the chimney, stone, capped with snow
    bm = bmesh.new()
    _box(bm, (W * 0.25, D * 0.12, (top + rise) / 2 + 0.4), (0.7, 0.7, top + rise + 0.8))
    out.append(_obj(bpy, f'{name}-chimney', bm, stone, loc, turn, smooth=False))
    bm = bmesh.new()
    _box(bm, (W * 0.25, D * 0.12, top + rise + 0.85), (0.8, 0.8, 0.14))
    bmesh.ops.bevel(bm, geom=bm.edges[:], offset=0.06, segments=3, affect='EDGES')
    out.append(_obj(bpy, f'{name}-chimney-snow', bm, snow, loc, turn))
    # the window: a warm room behind glass, a frame and a cross of mullions; a lamp inside
    em = bpy.data.materials.new(f'{name}-room'); em.use_nodes = True; nt = em.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
    e.inputs['Color'].default_value = (*_hex(p.get('window_color', '#FFB25A')), 1)
    e.inputs['Strength'].default_value = p.get('window_emit', 12.0)
    nt.links.new(e.outputs['Emission'], o.inputs['Surface'])
    cx = (wx0 + wx1) / 2; cz = (wz0 + wz1) / 2
    bm = bmesh.new()
    _box(bm, (cx, -D / 2 + 0.25, cz), (wx1 - wx0, 0.04, wz1 - wz0 + 0.1))
    out.append(_obj(bpy, f'{name}-room', bm, em, loc, turn, smooth=False))
    frame = assets.pbr(bpy, p.get('frame', 'dark_planks'), p.get('res', '1k'), name=f'{name}-frame')
    bm = bmesh.new()
    t = 0.08
    for (c, s) in [((cx, -D / 2 - 0.02, wz1 + t / 2), (wx1 - wx0 + 2 * t, 0.2, t)), ((cx, -D / 2 - 0.02, wz0 - t / 2), (wx1 - wx0 + 2 * t, 0.26, t)),
                   ((wx0 - t / 2, -D / 2 - 0.02, cz), (t, 0.2, wz1 - wz0)), ((wx1 + t / 2, -D / 2 - 0.02, cz), (t, 0.2, wz1 - wz0)),
                   ((cx, -D / 2 - 0.02, cz), (0.05, 0.12, wz1 - wz0)), ((cx, -D / 2 - 0.02, cz), (wx1 - wx0, 0.12, 0.05))]:
        _box(bm, c, s)
    out.append(_obj(bpy, f'{name}-frame', bm, frame, loc, turn, smooth=False))
    # a door, planks
    bm = bmesh.new()
    _box(bm, (-W * 0.22, -D / 2 - 0.12, 1.0), (0.95, 0.08, 2.0))
    out.append(_obj(bpy, f'{name}-door', bm, frame, loc, turn, smooth=False))
    # the lamp inside, its light out through the window onto the snow
    L = bpy.data.lights.new(f'{name}-lamp', 'POINT'); L.energy = p.get('lamp_w', 400.0); L.color = _hex(p.get('window_color', '#FFB25A'))
    L.shadow_soft_size = 0.3
    lo = bpy.data.objects.new(f'{name}-lamp', L); bpy.context.scene.collection.objects.link(lo)
    c, s_ = math.cos(math.radians(turn)), math.sin(math.radians(turn))
    lx, ly = cx, -D / 2 + 0.6
    lo.location = (loc[0] + lx * c - ly * s_, loc[1] + lx * s_ + ly * c, loc[2] + cz)
    return out


# --- the snowfield ------------------------------------------------------------------------------------------------
def _snow_pbr(bpy, name, res='2k', displace=0.03, ripple=0.012, sparkle=1.0):
    """Fresh snow from two photographed sets (snow_02, snow_01) blended by a broad noise so neither tile repeats, each
    sampled at its own scale and turn; wind ripples running across; subsurface for its translucent edges; a sparse
    glitter of grains catching the light."""
    import assets
    A = assets.texture('snow_02', res); B = assets.texture('snow_01', res)
    sa, sb = assets.size_m('snow_02') or (2.0, 2.0), assets.size_m('snow_01') or (2.0, 2.0)
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(bs.outputs['BSDF'], out.inputs['Surface'])
    tc = nt.nodes.new('ShaderNodeTexCoord')

    def mapping(scale, rot):
        mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = (1 / scale, 1 / scale, 1 / scale)
        mp.inputs['Rotation'].default_value = (0, 0, math.radians(rot))
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); return mp.outputs['Vector']
    va, vb = mapping(sa[0] * 1.15, 0), mapping(sb[0] * 1.4, 37)

    def img(path, colour, vec):
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(os.path.abspath(path), check_existing=True)
        if not colour:
            n.image.colorspace_settings.name = 'Non-Color'
        nt.links.new(vec, n.inputs['Vector']); return n.outputs['Color']
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.12; nz.inputs['Detail'].default_value = 3
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    fac = nt.nodes.new('ShaderNodeMapRange'); fac.inputs['From Min'].default_value = 0.42; fac.inputs['From Max'].default_value = 0.58
    nt.links.new(nz.outputs['Fac'], fac.inputs['Value'])

    def mix(a, b, kind='RGBA'):
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = kind
        nt.links.new(fac.outputs['Result'], mx.inputs['Factor'])
        ia, ib = (mx.inputs[6], mx.inputs[7]) if kind == 'RGBA' else (mx.inputs[2], mx.inputs[3])
        nt.links.new(a, ia); nt.links.new(b, ib)
        return mx.outputs[2] if kind == 'RGBA' else mx.outputs[0]
    col = mix(img(A['diff'], True, va), img(B['diff'], True, vb))
    bright = nt.nodes.new('ShaderNodeHueSaturation'); bright.inputs['Value'].default_value = 1.08
    nt.links.new(col, bright.inputs['Color']); nt.links.new(bright.outputs['Color'], bs.inputs['Base Color'])
    rough = mix(img(A['rough'], False, va), img(B['rough'], False, vb))
    nt.links.new(rough, bs.inputs['Roughness'])
    nor = mix(img(A['nor_gl'], False, va), img(B['nor_gl'], False, vb))
    nm = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(nor, nm.inputs['Color'])
    # glitter: a sparse field of tiny facets tilted at random, mirror-smooth
    vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 900.0
    nt.links.new(tc.outputs['Object'], vor.inputs['Vector'])
    glint = nt.nodes.new('ShaderNodeMapRange'); glint.inputs['From Min'].default_value = 0.975; glint.inputs['From Max'].default_value = 1.0
    glint.inputs['To Min'].default_value = 0.0; glint.inputs['To Max'].default_value = sparkle
    nt.links.new(vor.outputs['Color'], glint.inputs['Value'])
    bs.inputs['Coat Roughness'].default_value = 0.02; bs.inputs['Coat IOR'].default_value = 1.31
    nt.links.new(glint.outputs['Result'], bs.inputs['Coat Weight'])
    cn = nt.nodes.new('ShaderNodeVectorMath'); cn.operation = 'NORMALIZE'
    vo = nt.nodes.new('ShaderNodeVectorMath'); vo.operation = 'MULTIPLY_ADD'
    vo.inputs[1].default_value = (0.0, 0.0, 0.0)
    nt.links.new(vor.outputs['Color'], vo.inputs[0]); vo.inputs[1].default_value = (1.2, 1.2, 0.4)
    vo.inputs[2].default_value = (-0.6, -0.6, 1.0)
    nt.links.new(vo.outputs['Vector'], cn.inputs[0]); nt.links.new(cn.outputs['Vector'], bs.inputs['Coat Normal'])
    bs.inputs['Subsurface Weight'].default_value = 0.25; bs.inputs['Subsurface Radius'].default_value = (0.4, 0.7, 1.0)
    bs.inputs['Subsurface Scale'].default_value = 0.02
    # height: the two scans' displacement, plus wind ripples across
    disp = mix(img(A['disp'], False, va), img(B['disp'], False, vb))
    wave = nt.nodes.new('ShaderNodeTexWave'); wave.inputs['Scale'].default_value = 1.6; wave.inputs['Distortion'].default_value = 6.0
    wave.inputs['Detail'].default_value = 3.0; wave.bands_direction = 'DIAGONAL'
    nt.links.new(tc.outputs['Object'], wave.inputs['Vector'])
    dp = nt.nodes.new('ShaderNodeDisplacement'); dp.inputs['Scale'].default_value = displace; dp.inputs['Midlevel'].default_value = 0.5
    nt.links.new(disp, dp.inputs['Height'])
    # ripples only where the wind scoured: a broad noise masks them
    pm = nt.nodes.new('ShaderNodeTexNoise'); pm.inputs['Scale'].default_value = 0.35; pm.inputs['Detail'].default_value = 2
    nt.links.new(tc.outputs['Object'], pm.inputs['Vector'])
    pr = nt.nodes.new('ShaderNodeMapRange'); pr.inputs['From Min'].default_value = 0.55; pr.inputs['From Max'].default_value = 0.7
    nt.links.new(pm.outputs['Fac'], pr.inputs['Value'])
    wm = nt.nodes.new('ShaderNodeMath'); wm.operation = 'MULTIPLY'
    nt.links.new(wave.outputs['Fac'], wm.inputs[0]); nt.links.new(pr.outputs['Result'], wm.inputs[1])
    dw = nt.nodes.new('ShaderNodeDisplacement'); dw.inputs['Scale'].default_value = ripple; dw.inputs['Midlevel'].default_value = 0.0
    nt.links.new(wm.outputs['Value'], dw.inputs['Height'])
    ad = nt.nodes.new('ShaderNodeVectorMath'); ad.operation = 'ADD'
    nt.links.new(dp.outputs['Displacement'], ad.inputs[0]); nt.links.new(dw.outputs['Displacement'], ad.inputs[1])
    nt.links.new(ad.outputs['Vector'], out.inputs['Displacement'])
    nt.links.new(nm.outputs['Normal'], bs.inputs['Normal'])
    m.displacement_method = 'BOTH'
    return m


def snowfield(bpy, name, p, kit):
    """A snowfield (assets.ground's displaced patch) dressed in the blended snow above; and round the speaker's base
    a drift banked against it (`bank` [cx, cy, w, d, turn_deg, height]), the snow piled up its sides and falling away
    unevenly, level with the field beyond."""
    import assets
    ob = assets.ground(bpy, name, 'snow_02', tuple(p.get('size', [26, 26])), p.get('res', '2k'), tuple(p.get('position', [0, 0, 0])),
                       p.get('cells'), 0.0, None, 0.0, None, 1.0, 1.0, p.get('relief'),
                       tuple(p.get('flat', [0.0, 0.0, 0.9])) if p.get('flat') is not False else None)
    mat = _snow_pbr(bpy, f'{name}-snow', p.get('res', '2k'), p.get('displace', 0.03), p.get('ripple', 0.012), p.get('sparkle', 1.0))
    ob.data.materials[0] = mat
    bank = p.get('bank')
    if bank:
        from mathutils import noise
        cx, cy, w, d, turn, h = bank
        me = ob.data
        c, s = math.cos(math.radians(-turn)), math.sin(math.radians(-turn))
        ox, oy = ob.location.x, ob.location.y
        for v in me.vertices:
            x, y = v.co.x + ox - cx, v.co.y + oy - cy
            lx, ly = x * c - y * s, x * s + y * c                      # in the speaker's frame
            dx, dy = max(0.0, abs(lx) - w / 2), max(0.0, abs(ly) - d / 2)
            dist = math.hypot(dx, dy)
            if abs(lx) <= w / 2 and abs(ly) <= d / 2:
                continue                                              # inside the cabinet: the field's own level
            fall = 0.15 + 0.2 * (0.5 + 0.5 * noise.noise(Vector((lx * 3.0, ly * 3.0, 4.2))))
            if dist < fall:
                t = 1.0 - dist / fall
                # wind from the front: a scoop hollowed under the front face, banked up behind and at the back corners
                k = 1.0                                                  # a soft drift lapping the base all round
                v.co.z += h * k * (t ** 1.6) * (0.75 + 0.5 * noise.noise(Vector((lx * 9.0, ly * 9.0, 1.3))))
    return [ob]
