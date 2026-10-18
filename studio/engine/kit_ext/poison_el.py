"""Poison's pieces for round 31b (spinoffs/barkhorn/elements/poison.py): a redwood rainforest on location, built from
Poly Haven's scans and textures (assets.py) where they exist and modelled here where they don't.

- redwood: a trunk metres across, flaring into buttresses at its foot, in a photographed bark (metasequoia, the dawn
  redwood) laid at its real size, rising out of the frame;
- plants: single plants picked out of a scanned set (fern_02 holds four ferns, moss_01 a dozen moss sprigs) and placed
  one by one, each a linked copy of the scan;
- mist: a scattering volume whose density falls off with height and can be torn into wisps;
- toadstool: a fly agaric in physically plausible materials (a waxy red cap, cream warts and stem), for the log.
"""
import math, random

import bmesh
from mathutils import Matrix, Vector

import assets


# --- the redwood ---------------------------------------------------------------------------------------------------
def redwood(bpy, name, p, kit):
    """A redwood's trunk: `radius` at breast height, `height` tall, flaring at its foot into `lobes` buttresses (`flare`
    times the radius, dying away over `foot` metres), fluted lightly up its length; its bark the Poly Haven texture
    `bark` (default metasequoia_bark) at `tex_scale` metres a tile, tinted by `tint` / `tint_mix`."""
    rnd = random.Random(p.get('seed', 1))
    R, H = p.get('radius', 1.2), p.get('height', 20.0); fl, foot = p.get('flare', 0.6), p.get('foot', 1.4)
    lobes, ph = p.get('lobes', 6), rnd.uniform(0, 6.28)
    seg = p.get('segments', 160)
    zs = [-0.5] + [H * (k / 79) ** 1.7 for k in range(80)]
    verts, faces, uvs = [], [], []
    for z in zs:
        e = math.exp(-max(z, 0.0) / foot)
        for i in range(seg):
            th = 2 * math.pi * i / seg
            lob = 0.5 + 0.5 * math.cos(lobes * th + ph + 0.5 * math.sin(3 * th + ph))
            flute = 0.018 * math.sin(23 * th + 0.3 * z) + 0.01 * math.sin(41 * th - 0.2 * z)
            r = R * (1.0 - 0.25 * z / H) * (1 + fl * e * (0.3 + 0.7 * lob ** 2)) * (1 + flute)
            verts.append((r * math.cos(th), r * math.sin(th), z))
    for j in range(len(zs) - 1):
        for i in range(seg):
            a, b = j * seg + i, j * seg + (i + 1) % seg
            faces.append((a, b, b + seg, a + seg))
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces)
    # UVs: around the trunk by arc length (so the bark keeps its real size), up it by height
    uv = me.uv_layers.new(name='UVMap'); circ = 2 * math.pi * R
    for f in me.polygons:
        for li in f.loop_indices:
            vi = me.loops[li].vertex_index; i, j = vi % seg, vi // seg
            if i == 0 and any(me.loops[l].vertex_index % seg == seg - 1 for l in f.loop_indices):
                i = seg
            uv.data[li].uv = (circ * i / seg, zs[j])
    for f in me.polygons:
        f.use_smooth = True
    me.materials.append(assets.pbr(bpy, p.get('bark', 'metasequoia_bark'), p.get('res', '4k'), scale=p.get('tex_scale', 1.6),
                                   tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0), bump=p.get('bump', 1.4),
                                   coords='uv', displace=p.get('displace', 0.0), name=f'{name}-bark'))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    ob.rotation_euler.z = math.radians(p.get('turn', 0.0))
    return [ob]


# --- plants picked out of a scanned set ------------------------------------------------------------------------------
_SETS = {}


def _scan_parts(bpy, model, res):
    """The mesh objects of a scanned model (imported once, kept out of sight), each with the offset that stands it on
    the origin: (object, offset vector, its height, its matrix as imported)."""
    key = (model, res)
    if key not in _SETS:
        root = assets.place(bpy, model, res, location=(0, 0, 0))
        bpy.context.view_layer.update()
        parts = []
        for o in root.children_recursive:
            if o.type != 'MESH':
                continue
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
            cx = (min(v.x for v in bb) + max(v.x for v in bb)) / 2; cy = (min(v.y for v in bb) + max(v.y for v in bb)) / 2
            z0 = min(v.z for v in bb); h = max(v.z for v in bb) - z0
            parts.append((o, Vector((-cx, -cy, -z0)), h, o.matrix_world.copy()))
        root.location = (0, 0, -1000)
        for o in [root] + list(root.children_recursive):
            o.hide_render = True
        _SETS[key] = parts
    return _SETS[key]


def plants(bpy, name, p, kit):
    """Plants from the scanned set `model`: `place` [[x, y, z, scale, turn_deg, which, tilt_deg], ...] (which: the
    index of the plant in the set, or -1 for any), each a linked copy standing on (x, y, z)."""
    parts = _scan_parts(bpy, p['model'], p.get('res', '2k'))
    rnd = random.Random(p.get('seed', 1))
    if p.get('only'):
        parts = [parts[i] for i in p['only']]
    out = []
    for k, pl in enumerate(p['place']):
        x, y, z, s, turn = pl[:5]
        which = pl[5] if len(pl) > 5 else -1
        tilt = pl[6] if len(pl) > 6 else 0.0
        o, off, h, mw = parts[which] if which >= 0 else rnd.choice(parts)
        c = o.copy(); c.parent = None; c.hide_render = False
        bpy.context.scene.collection.objects.link(c)
        rot = (Matrix.Rotation(math.radians(turn), 4, 'Z') @ Matrix.Rotation(math.radians(tilt), 4, 'X'))
        c.matrix_world = (Matrix.Translation((x, y, z)) @ rot @ Matrix.Scale(s, 4) @ Matrix.Translation(off)
                          @ mw)
        c.name = f'{name}-{k}'
        out.append(c)
    return out


# --- mist ----------------------------------------------------------------------------------------------------------
def mist(bpy, name, p, kit):
    """A volume of mist: a box `size` [w, d, h] standing on its base at `position`, a scattering volume whose density is
    `density` at the ground thinning to `top` of that at its ceiling, torn into wisps `wisp` metres across (0: even)."""
    w, d, h = p.get('size', [10.0, 10.0, 4.0])
    bm = bmesh.new()
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector((v.co.x * w, v.co.y * d, (v.co.z + 0.5) * h))
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); vs = nt.nodes.new('ShaderNodeVolumeScatter')
    vs.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#FFFFFF'))
    vs.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.5)
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    fall = nt.nodes.new('ShaderNodeMapRange')
    fall.inputs['From Min'].default_value = 0.0; fall.inputs['From Max'].default_value = h
    fall.inputs['To Min'].default_value = p.get('density', 0.05); fall.inputs['To Max'].default_value = p.get('density', 0.05) * p.get('top', 0.3)
    nt.links.new(sep.outputs['Z'], fall.inputs['Value'])
    dens = fall.outputs['Result']
    if p.get('wisp', 0.0) > 0:
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p['wisp']
        nz.inputs['Detail'].default_value = 4.0
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        cut = nt.nodes.new('ShaderNodeMapRange'); cut.interpolation_type = 'SMOOTHSTEP'
        cut.inputs['From Min'].default_value = p.get('wisp_lo', 0.35); cut.inputs['From Max'].default_value = p.get('wisp_hi', 0.7)
        cut.inputs['To Min'].default_value = p.get('wisp_floor', 0.25)
        nt.links.new(nz.outputs['Fac'], cut.inputs['Value'])
        mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
        nt.links.new(dens, mul.inputs[0]); nt.links.new(cut.outputs['Result'], mul.inputs[1])
        dens = mul.outputs['Value']
    nt.links.new(dens, vs.inputs['Density']); nt.links.new(vs.outputs['Volume'], out.inputs['Volume'])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0])); ob.visible_shadow = False
    return [ob]


# --- a fly agaric --------------------------------------------------------------------------------------------------
def _mat(bpy, name, base, rough, sss=0.0, sss_col=None, bump=0.0, bump_size=0.003, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*base, 1.0); b.inputs['Roughness'].default_value = rough
    if sss:
        b.inputs['Subsurface Weight'].default_value = sss
        b.inputs['Subsurface Radius'].default_value = sss_col or (0.004, 0.002, 0.001)
    if coat:
        b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = 0.25
    if bump:
        tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 1.0 / bump_size; nz.inputs['Detail'].default_value = 6.0
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        bn = nt.nodes.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = bump; bn.inputs['Distance'].default_value = bump_size * 0.3
        nt.links.new(nz.outputs['Fac'], bn.inputs['Height']); nt.links.new(bn.outputs['Normal'], b.inputs['Normal'])
    return m


def toadstool(bpy, name, p, kit):
    """A fly agaric `height` tall, cap `cap` [radius, height], stem radius `stem`, `lean` [dx, dy] at the top, `warts`
    on its cap; a waxy red cap fading to orange at the rim, cream warts, a cream stem with a ring and a bulb."""
    rnd = random.Random(p.get('seed', 1))
    H = p.get('height', 0.12); R, CH = p.get('cap', [0.05, 0.03]); sr = p.get('stem', 0.008)
    z0 = H - CH
    def lathe(prof, seg=64):
        bm = bmesh.new(); kit._lathe(bm, prof, seg); return bm
    stem = lathe([(0.0, 0.0), (sr * 1.6, 0.0), (sr * 1.7, 0.04 * H), (sr * 1.3, 0.14 * H), (sr * 1.02, 0.4 * H), (sr * 0.9, 0.75 * H),
                  (sr * 0.85, z0 + 0.1 * CH), (0.0, z0 + 0.12 * CH)], 40)
    ring = lathe([(sr * 0.8, 0.72 * H), (sr * 1.7, 0.69 * H), (sr * 1.9, 0.675 * H), (sr * 0.85, 0.705 * H)], 40)
    dome = [(0.0, z0 + 0.2 * CH), (sr * 1.05, z0 + 0.18 * CH), (R * 0.9, z0 + 0.02 * CH), (R * 0.985, z0 + 0.05 * CH)]
    for i in range(20):
        th = (i / 19) * math.pi / 2
        dome.append((R * math.cos(th) ** 0.8, z0 + 0.1 * CH + 0.9 * CH * math.sin(th) ** 1.2))
    dome[-1] = (0.0, H)
    cap = lathe(dome, 96)
    warts = bmesh.new()
    for k in range(p.get('warts', 22)):
        th = rnd.uniform(0.15, 1.3); ph = rnd.uniform(0, 2 * math.pi)
        r = R * math.cos(th) ** 0.8; z = z0 + 0.1 * CH + 0.9 * CH * math.sin(th) ** 1.2
        s = R * rnd.uniform(0.03, 0.065)
        tmp = bmesh.new(); kit._sphere(tmp, (0, 0, 0), (s, s * rnd.uniform(0.7, 1.0), s * 0.5), 12)
        nrm = Vector((math.cos(ph) * math.cos(th), math.sin(ph) * math.cos(th), math.sin(th) * 1.4)).normalized()
        mt = Matrix.Translation(Vector((r * math.cos(ph), r * math.sin(ph), z))) @ nrm.to_track_quat('Z', 'Y').to_matrix().to_4x4()
        for v in tmp.verts:
            v.co = mt @ v.co
        me = bpy.data.meshes.new('_w'); tmp.to_mesh(me); tmp.free(); warts.from_mesh(me); bpy.data.meshes.remove(me)
    lx, ly = p.get('lean', [0.0, 0.0])
    cream = _mat(bpy, f'{name}-cream', (0.78, 0.72, 0.6), 0.65, sss=0.3, sss_col=(0.004, 0.003, 0.002), bump=0.3, bump_size=0.002)
    red = _mat(bpy, f'{name}-cap', (0.55, 0.035, 0.02), 0.38, sss=0.15, sss_col=(0.006, 0.002, 0.001), bump=0.15,
               bump_size=0.004, coat=0.25)
    out = []
    for nm, bm, mat in (('stem', stem, cream), ('ring', ring, cream), ('cap', cap, red), ('warts', warts, cream)):
        for v in bm.verts:
            t = max(0.0, v.co.z) / H; v.co.x += lx * t * t; v.co.y += ly * t * t
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        me = bpy.data.meshes.new(f'{name}-{nm}'); bm.to_mesh(me); bm.free()
        for f in me.polygons:
            f.use_smooth = True
        me.materials.append(mat)
        ob = bpy.data.objects.new(f'{name}-{nm}', me); bpy.context.scene.collection.objects.link(ob)
        ob.location = Vector(p.get('position', [0, 0, 0]))
        ob.rotation_euler = [math.radians(a) for a in p.get('rotate', [0, 0, 0])]
        out.append(ob)
    return out


# --- the canopy ----------------------------------------------------------------------------------------------------
def canopy(bpy, name, p, kit):
    """The forest's roof, for its shadow alone: a sheet `size` [w, d] at height `position` z, opaque but for gaps
    `gap` metres across covering about `open` of it, unseen by the camera and in reflections, so a sun lamp through it
    falls as shafts and dapples."""
    w, d = p.get('size', [60.0, 60.0])
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    for v in bm.verts:
        v.co.x *= w; v.co.y *= d
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); mix = nt.nodes.new('ShaderNodeMixShader')
    dif = nt.nodes.new('ShaderNodeBsdfDiffuse'); dif.inputs['Color'].default_value = (0.02, 0.03, 0.015, 1)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / p.get('gap', 2.0); nz.inputs['Detail'].default_value = 6.0
    nz.inputs['Roughness'].default_value = 0.6
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    cut = nt.nodes.new('ShaderNodeMapRange')
    from statistics import NormalDist                 # the noise's values fall about normally round 0.5
    lo = 0.5 + p.get('spread', 0.09) * NormalDist().inv_cdf(1.0 - p.get('open', 0.15))
    cut.inputs['From Min'].default_value = lo; cut.inputs['From Max'].default_value = lo + 0.03
    nt.links.new(nz.outputs['Fac'], cut.inputs['Value'])
    fac = cut.outputs['Result']
    # holes: [x, y, r] in the sheet's own plane, open whatever the noise says (a gap placed so the sun reaches a spot)
    for hx, hy, hr in p.get('holes', []):
        d = nt.nodes.new('ShaderNodeVectorMath'); d.operation = 'DISTANCE'
        nt.links.new(tc.outputs['Object'], d.inputs[0]); d.inputs[1].default_value = (hx, hy, 0.0)
        ed = nt.nodes.new('ShaderNodeMapRange'); ed.interpolation_type = 'SMOOTHSTEP'
        ed.inputs['From Min'].default_value = hr * 0.6; ed.inputs['From Max'].default_value = hr
        ed.inputs['To Min'].default_value = 1.0; ed.inputs['To Max'].default_value = 0.0
        nt.links.new(d.outputs['Value'], ed.inputs['Value'])
        mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'
        nt.links.new(fac, mx.inputs[0]); nt.links.new(ed.outputs['Result'], mx.inputs[1]); fac = mx.outputs['Value']
    nt.links.new(fac, mix.inputs['Fac'])
    nt.links.new(dif.outputs['BSDF'], mix.inputs[1]); nt.links.new(tr.outputs['BSDF'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 15]))
    ob.visible_camera = False; ob.visible_glossy = False; ob.visible_transmission = False; ob.visible_diffuse = False
    return [ob]


# --- a fallen redwood, furred in moss ------------------------------------------------------------------------------
def mossy_log(bpy, name, p, kit):
    """A fallen trunk from `a` to `b` (world points on its axis), `radius` at `a` tapering to `radius_b`, its broken
    end at `b`; its bark the texture `bark`, and over its back a blanket of moss (`moss`, an ambientCG or Poly Haven
    set) where the surface faces up, its edge ragged; the blanket lifted `pile` metres and displaced by its height."""
    from mathutils import noise
    a, b = Vector(p['a']), Vector(p['b'])
    R0, R1 = p.get('radius', 0.45), p.get('radius_b', p.get('radius', 0.45) * 0.85)
    L = (b - a).length; ax = (b - a).normalized()
    q = ax.to_track_quat('Z', 'Y').to_matrix()
    seg, nl = 200, max(8, int(L / 0.022))                # fine, so the moss's edge is ragged rather than stepped
    def ring_pt(t, th, extra=0.0):
        r = R0 + (R1 - R0) * t
        bumpy = 1 + 0.035 * noise.noise(Vector((math.cos(th) * 2, math.sin(th) * 2, t * L * 1.5))) + 0.015 * math.sin(19 * th)
        rr = r * bumpy + extra
        # sag a little where it lies: flatten its underside
        y = rr * math.sin(th); x = rr * math.cos(th)
        return a + q @ Vector((x, y, t * L))
    def tube(extra, keep=None):
        verts, faces, uvs = [], [], []
        for j in range(nl + 1):
            t = j / nl
            for i in range(seg + 1):
                th = 2 * math.pi * i / seg
                verts.append(ring_pt(t, th, extra)); uvs.append((2 * math.pi * R0 * i / seg, t * L))
        for j in range(nl):
            for i in range(seg):
                f = (j * (seg + 1) + i, j * (seg + 1) + i + 1, (j + 1) * (seg + 1) + i + 1, (j + 1) * (seg + 1) + i)
                if keep is None or keep(j / nl, 2 * math.pi * (i + 0.5) / seg):
                    faces.append(f)
        return verts, faces, uvs
    def obj(nm, verts, faces, uvs, mat, cap=False):
        me = bpy.data.meshes.new(nm); me.from_pydata([tuple(v) for v in verts], [], faces)
        uv = me.uv_layers.new(name='UVMap')
        for f in me.polygons:
            for li in f.loop_indices:
                uv.data[li].uv = uvs[me.loops[li].vertex_index]
            f.use_smooth = True
        me.materials.append(mat)
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
        return ob
    out = []
    v, f, u = tube(0.0)
    # end caps: the near end closed, the broken end a rough face
    out.append(obj(f'{name}-bark', v, f, u, assets.pbr(bpy, p.get('bark', 'metasequoia_bark'), p.get('res', '2k'),
                                                         scale=p.get('bark_scale', 1.2), coords='uv', bump=1.3,
                                                         tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0), name=f'{name}-barkmat')))
    for t, nm in ((0.0, 'end-a'), (1.0, 'end-b')):
        c = a + (b - a) * t
        vv = [c] + [ring_pt(t, 2 * math.pi * i / seg, -0.004) for i in range(seg)]
        ff = [(0, 1 + i, 1 + (i + 1) % seg) for i in range(seg)]
        uu = [(0.5, 0.5)] + [(0.5 + 0.5 * math.cos(2 * math.pi * i / seg), 0.5 + 0.5 * math.sin(2 * math.pi * i / seg)) for i in range(seg)]
        out.append(obj(f'{name}-{nm}', vv, ff, uu, assets.pbr(bpy, p.get('end', 'acg:TreeEnd005'), '2k', scale=1.0, coords='uv',
                                                             tint=p.get('end_tint'), tint_mix=p.get('end_tint_mix', 0.0),
                                                             name=f'{name}-{nm}-mat')))
    # the moss: where the surface faces up (th near 90 degrees in the log's frame, with the up direction found)
    up = (q.inverted() @ Vector((0, 0, 1))); th_up = math.atan2(up.y, up.x)
    cover = p.get('cover', 0.55)
    def keep(t, th):
        d = math.cos(th - th_up)
        n = (0.25 * noise.noise(Vector((math.cos(th) * 3, math.sin(th) * 3, t * L * 2.5)))
             + 0.1 * noise.noise(Vector((math.cos(th) * 14, math.sin(th) * 14, t * L * 12))))
        return d + n > 1.0 - 2 * cover and 0.03 < t < 0.97
    v, f, u = tube(p.get('pile', 0.012), keep)
    out.append(obj(f'{name}-moss', v, f, u, assets.pbr(bpy, p.get('moss', 'acg:Moss004'), p.get('res', '2k'),
                                                         scale=p.get('moss_scale', 0.8), coords='uv', bump=1.5,
                                                         displace=p.get('moss_displace', 0.02), name=f'{name}-mossmat')))
    return out


# --- strewing scanned plants over a surface (geometry nodes) ------------------------------------------------------
_COLS = {}


def _scan_collection(bpy, model, res, only=None):
    """A collection holding the scanned set's plants, each standing on its own origin (for instancing; not linked to
    the scene, so only its instances render)."""
    key = (model, res, tuple(only or ()))
    if key not in _COLS:
        parts = _scan_parts(bpy, model, res)
        col = bpy.data.collections.new(f'strew-{model}')
        for k, (o, off, h, mw) in enumerate(parts):
            if only and k not in only:
                continue
            me = o.data.copy(); me.transform(Matrix.Translation(off) @ mw)
            ob = bpy.data.objects.new(f'{model}-part{k}', me); col.objects.link(ob)
        _COLS[key] = col
    return _COLS[key]


def strew(bpy, name, p, kit):
    """Scanned plants (`model`, its parts `only`) strewn over the objects whose names hold any of `on`, `density` per square
    metre where their surface faces up by more than `up` (the normal's z), in patches (`patch` metres across, `patch_cut`
    0 to 1: how much is bare), each sized at random within `scale` and turned at random about its normal, none inside
    an `avoid` circle [[x, y, r], ...]."""
    col = _scan_collection(bpy, p['model'], p.get('res', '2k'), p.get('only'))
    obs = []
    for o in list(bpy.context.scene.objects):
        if o.type == 'MESH' and any(pre in o.name for pre in p['on']):
            obs.append(o)
    ng = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes; Lk = ng.links.new
    gi = N.new('NodeGroupInput'); go = N.new('NodeGroupOutput')
    dist = N.new('GeometryNodeDistributePointsOnFaces'); dist.distribute_method = 'RANDOM'
    dist.inputs['Density'].default_value = p.get('density', 200.0); dist.inputs['Seed'].default_value = p.get('seed', 1)
    Lk(gi.outputs['Geometry'], dist.inputs['Mesh'])
    # where it may grow: facing up, in patches, outside the avoid circles
    nrm = N.new('GeometryNodeInputNormal'); sep = N.new('ShaderNodeSeparateXYZ'); Lk(nrm.outputs['Normal'], sep.inputs['Vector'])
    cmp = N.new('FunctionNodeCompare'); cmp.data_type = 'FLOAT'; cmp.operation = 'GREATER_THAN'
    cmp.inputs['B'].default_value = p.get('up', 0.4); Lk(sep.outputs['Z'], cmp.inputs['A'])
    sel = cmp.outputs['Result']
    pos = N.new('GeometryNodeInputPosition')
    if p.get('patch', 0) > 0:
        nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p['patch']; nz.inputs['Detail'].default_value = 3.0
        Lk(pos.outputs['Position'], nz.inputs['Vector'])
        c2 = N.new('FunctionNodeCompare'); c2.data_type = 'FLOAT'; c2.operation = 'GREATER_THAN'
        c2.inputs['B'].default_value = 0.3 + 0.4 * p.get('patch_cut', 0.3); Lk(nz.outputs['Fac'], c2.inputs['A'])
        an = N.new('FunctionNodeBooleanMath'); an.operation = 'AND'; Lk(sel, an.inputs[0]); Lk(c2.outputs['Result'], an.inputs[1])
        sel = an.outputs['Boolean']
    for x, y, r in p.get('avoid', []):
        sub = N.new('ShaderNodeVectorMath'); sub.operation = 'DISTANCE'
        Lk(pos.outputs['Position'], sub.inputs[0]); sub.inputs[1].default_value = (x, y, 0.0)
        # distance in the plane: flatten z by comparing against a point at the same height
        mulz = N.new('ShaderNodeVectorMath'); mulz.operation = 'MULTIPLY'; mulz.inputs[1].default_value = (1, 1, 0)
        Lk(pos.outputs['Position'], mulz.inputs[0]); Lk(mulz.outputs['Vector'], sub.inputs[0])
        c3 = N.new('FunctionNodeCompare'); c3.data_type = 'FLOAT'; c3.operation = 'GREATER_THAN'; c3.inputs['B'].default_value = r
        Lk(sub.outputs['Value'], c3.inputs['A'])
        an = N.new('FunctionNodeBooleanMath'); an.operation = 'AND'; Lk(sel, an.inputs[0]); Lk(c3.outputs['Result'], an.inputs[1])
        sel = an.outputs['Boolean']
    Lk(sel, dist.inputs['Selection'])
    ci = N.new('GeometryNodeCollectionInfo'); ci.inputs['Collection'].default_value = col
    ci.inputs['Separate Children'].default_value = True; ci.inputs['Reset Children'].default_value = True
    iop = N.new('GeometryNodeInstanceOnPoints'); iop.inputs['Pick Instance'].default_value = True
    Lk(dist.outputs['Points'], iop.inputs['Points']); Lk(ci.outputs['Instances'], iop.inputs['Instance'])
    ri = N.new('FunctionNodeRandomValue'); ri.data_type = 'INT'; ri.inputs['Min'].default_value = 0
    ri.inputs['Max'].default_value = len(col.objects) - 1; ri.inputs['Seed'].default_value = p.get('seed', 1) + 7
    Lk(ri.outputs['Value'], iop.inputs['Instance Index'])
    # upright, leaning toward the normal by `follow`
    if p.get('follow', 0.4) > 0:
        Lk(dist.outputs['Rotation'], iop.inputs['Rotation'])
    rs = N.new('FunctionNodeRandomValue'); rs.data_type = 'FLOAT'
    s0, s1 = p.get('scale', [0.8, 1.2]); rs.inputs['Min'].default_value = s0; rs.inputs['Max'].default_value = s1
    rs.inputs['Seed'].default_value = p.get('seed', 1) + 13
    Lk(rs.outputs['Value'], iop.inputs['Scale'])
    rz = N.new('FunctionNodeRandomValue'); rz.data_type = 'FLOAT_VECTOR'
    rz.inputs['Min'].default_value = (0, 0, 0); rz.inputs['Max'].default_value = (0, 0, 6.2832)
    rz.inputs['Seed'].default_value = p.get('seed', 1) + 29
    rot = N.new('GeometryNodeRotateInstances'); Lk(iop.outputs['Instances'], rot.inputs['Instances'])
    Lk(rz.outputs['Value'], rot.inputs['Rotation']); rot.inputs['Local Space'].default_value = True
    j = N.new('GeometryNodeJoinGeometry'); Lk(gi.outputs['Geometry'], j.inputs['Geometry']); Lk(rot.outputs['Instances'], j.inputs['Geometry'])
    Lk(j.outputs['Geometry'], go.inputs['Geometry'])
    for o in obs:
        md = o.modifiers.new(name, 'NODES'); md.node_group = ng
    return []
