"""Dust B's pieces (round 31b, spinoffs/barkhorn/elements/dust_b.py): Monument Valley under a blue afternoon sky, at true
scale. The terrain, the tumbleweed and the shader helpers come from dust_el.py; these are the rest.

- butte: a Monument Valley butte or mesa at its real size: a sheer cliff of red sandstone (`cliff_mat`) from `talus_h`
  to `height` metres, fluted by joints and buttresses, under a clean flat caprock, standing on a separate talus apron of
  paler shale and scree (`talus_mat`) that spreads to `spread` times the cliff's foot and is cut by gullies. Footprint:
  `radius` metres, stretched by `squash` in y, wandering by `wander`; `thumbs` [[angle_deg, distance (share of the
  radius), radius, height share], ...] add the slender spires of the Mittens. Each material is a dict like a piece's
  (`material: pbr`, `texture`, `tex_scale`, `tint`, `tint_mix`), plus `streaks` [size_m, amount] for the vertical stains of
  desert varnish and `beds` [band_m, contrast] for strata.
- prickly_pear: an Opuntia clump, `pads` pads (`size` m, the longest), each a flattened obovate disc set on the edge of
  another, studded with areoles in a quincunx, each areole carrying 1 to 4 straw spines that catch the light.
- yucca: a rosette (Yucca baccata / angustissima) of `leaves` stiff blue-green blades `length` m long and `width` m wide,
  curving out and up from a short stem, a skirt of dry leaves below.
- sagebrush: a rounded grey-green shrub, `size` [w, d, h] m: woody stems branching from the ground into a mass of fine
  silvery leaves.
- ground_mix: on a terrain material, a second photographed texture (`texture`, `tex_scale`, `tint`, `tint_mix`) blended
  in through a noise mask `mask` [size_m, coverage 0..1] (stony patches in sand).
"""
import math, os, random, sys

import bmesh
from mathutils import Matrix, Vector, noise

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dust_el as D                                         # noqa: E402


def _principled(bpy, name, color, rough=0.5, sss=0.0, spec=0.4, kit=None, emit=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    kit._set(b, 'Base Color', kit._mix(color, color, 0.0)); kit._set(b, 'Roughness', rough)
    kit._set(b, 'Specular IOR Level', spec)
    if sss:
        kit._set(b, 'Subsurface Weight', sss); kit._set(b, 'Subsurface Radius', Vector((0.01, 0.006, 0.003)))
    return m


def _noise_tint(m, size, c0, c1, lo=0.35, hi=0.7, kit=None, coord='Object'):
    """Base colour wandering between c0 and c1 in patches `size` metres across."""
    nt = m.node_tree; b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / size; nz.inputs['Detail'].default_value = 3.0
    nt.links.new(tc.outputs[coord], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = lo; cr.elements[0].color = kit._mix(c0, c0, 0)
    cr.elements[1].position = hi; cr.elements[1].color = kit._mix(c1, c1, 0)
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])


# --- materials on photographed textures ---------------------------------------------------------------------------
def _pbr(bpy, spec, name):
    import assets
    return assets.pbr(bpy, spec['texture'], spec.get('res', '2k'), scale=spec.get('tex_scale'),
                      displace=spec.get('displace', 0.0), tint=spec.get('tint'), tint_mix=spec.get('tint_mix', 0.0),
                      rough_mul=spec.get('rough_mul', 1.0), bump=spec.get('bump', 1.0), name=name)


def _streaks(mat, size, amount, seed=0.0):
    """Vertical stains (desert varnish): a noise stretched tall, darkening the base colour in streaks `size` m wide."""
    nt = mat.node_tree; bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    sock = bs.inputs['Base Color']
    if not sock.links:
        return
    src = sock.links[0].from_socket
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1.0 / size, 1.0 / size, 1.0 / (size * 9.0))
    mp.inputs['Location'].default_value = (seed, seed * 0.7, 0.0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Detail'].default_value = 6.0; nz.inputs['Roughness'].default_value = 0.6
    nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = 0.3; cr.elements[0].color = (0.42, 0.36, 0.34, 1)
    cr.elements[1].position = 0.62; cr.elements[1].color = (1.08, 1.04, 1.0, 1)
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs['Factor'].default_value = amount
    nt.links.new(src, mul.inputs['A']); nt.links.new(ramp.outputs['Color'], mul.inputs['B'])
    nt.links.new(mul.outputs['Result'], sock)


def _rock_mat(bpy, spec, name, seed):
    m = _pbr(bpy, spec, name)
    if spec.get('vary'):
        D._vary(bpy, m, *spec['vary'], tint=(0.6, 0.45, 0.4))
    if spec.get('beds'):
        D._beds(m, *spec['beds'], seed=float(seed))
    if spec.get('streaks'):
        _streaks(m, *spec['streaks'], seed=float(seed) * 13.1)
    return m


# --- butte ---------------------------------------------------------------------------------------------------------
def butte(bpy, name, p, kit):
    R, H = p.get('radius', 300.0), p.get('height', 300.0)
    th = p.get('talus_h', 0.38)                              # the talus rises to this share of the height
    spread, squash, wander = p.get('spread', 2.0), p.get('squash', 0.6), p.get('wander', 0.18)
    rnd = random.Random(p.get('seed', 1)); seg = p.get('segments', 720)
    off = Vector((rnd.uniform(-90, 90), rnd.uniform(-90, 90), 0.0))
    ph = [rnd.uniform(0, 6.283) for _ in range(6)]
    pos = Vector(p.get('position', [0, 0, 0]))
    rot = math.radians((p.get('rotate') or [0, 0, 0])[2])

    def foot(th_):
        return 1 + wander * (math.sin(2 * th_ + ph[0]) + 0.5 * math.sin(3 * th_ + ph[1]) + 0.3 * math.sin(5 * th_ + ph[2])
                             + 0.6 * noise.noise(Vector((math.cos(th_) * 2.0, math.sin(th_) * 2.0, 0.4)) + off))

    def flute(th_, z):
        # joints and buttresses: angular, a few metres deep, constant up the face (as joints are), a little ragged
        a = noise.noise(Vector((math.cos(th_) * 9, math.sin(th_) * 9, 0.2)) + off)
        b = noise.noise(Vector((math.cos(th_) * 26, math.sin(th_) * 26, z / H * 0.6)) + off)
        c = noise.noise(Vector((math.cos(th_) * 70, math.sin(th_) * 70, z / H * 1.5)) + off)
        # joints read as sharp grooves: fold the mid band so its troughs are narrow and its ridges broad
        return 0.05 * a - 0.04 * abs(b) + 0.015 * c

    def xy(r, th_):
        x, y = r * math.cos(th_), r * math.sin(th_) * squash
        return x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)

    def ring(rf, z, fl=1.0, gully=0.0):
        out = []
        for i in range(seg):
            t = 2 * math.pi * i / seg
            k = foot(t) * rf * (1 + fl * flute(t, z))
            if gully:                                       # gullies and spurs down the talus
                k *= 1 + gully * noise.noise(Vector((math.cos(t) * 14, math.sin(t) * 14, z / H * 3)) + off)
            x, y = xy(R * k, t)
            out.append((pos.x + x, pos.y + y, pos.z + z))
        return out

    def mesh(rings, close_top, mat, nm):
        bm = bmesh.new()
        vr = [[bm.verts.new(v) for v in r] for r in rings]
        for a, b in zip(vr, vr[1:]):
            for i in range(seg):
                bm.faces.new((a[i], a[(i + 1) % seg], b[(i + 1) % seg], b[i]))
        if close_top:
            c = Vector((0, 0, 0))
            for v in vr[-1]:
                c += v.co
            top = bm.verts.new(c / seg)
            for i in range(seg):
                bm.faces.new((vr[-1][i], vr[-1][(i + 1) % seg], top))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        q = {k: v for k, v in p.items() if k not in ('position', 'rotate', 'scale')}
        return kit.finish(bpy, nm, bm, q, smooth=True, mat=mat)

    cliff_m = _rock_mat(bpy, p['cliff_mat'], f'{name}-cliff', p.get('seed', 1))
    talus_m = _rock_mat(bpy, p['talus_mat'], f'{name}-talus', p.get('seed', 1) + 7)
    # the cliff: from a little inside the talus top (hidden) up to the rim, nearly vertical
    cliff, nc = [], 40
    z0 = H * th * 0.9
    for j in range(nc + 1):
        t = j / nc
        cliff.append(ring(1.0 - 0.025 * t, z0 + (H - z0) * t))
    cap = ring(0.995, H * 1.002, fl=1.0)
    cliff.append(cap)
    objs = mesh(cliff, True, cliff_m, f'{name}-cliff')
    # the talus: concave, steep under the cliff and spreading out to the plain, gullied
    talus, ntl = [], 18
    for j in range(ntl + 1):
        t = j / ntl                                          # 0 at the plain, 1 at the cliff's foot
        rf = 1.0 + (spread - 1.0) * (1 - t) ** 1.7
        z = H * th * (t ** 0.85) - 0.5
        talus.append(ring(rf * 1.01, z, fl=1.0 if t > 0.8 else 0.5, gully=0.16 * (1 - abs(2 * t - 1)) + 0.03))
    objs += mesh(talus, False, talus_m, f'{name}-talus')
    # the Mittens' thumbs: slender spires standing off the main block
    for k, (ang, dist, tr, hs) in enumerate(p.get('thumbs', [])):
        a = math.radians(ang)
        cx, cy = xy(R * dist, a)
        sub = dict(p, position=[pos.x + cx, pos.y + cy, pos.z], radius=tr, height=H * hs, spread=1.6, thumbs=[],
                   squash=1.0, seed=p.get('seed', 1) * 31 + k, talus_h=th / hs * 0.9, wander=0.12, segments=240)
        objs += butte(bpy, f'{name}-thumb{k}', sub, kit)
    return objs


# --- plants --------------------------------------------------------------------------------------------------------
def _ellipsoid(bm, centre, axes, rot, seg=20):
    g = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=1.0)
    for v in g['verts']:
        v.co = centre + rot @ Vector((v.co.x * axes[0], v.co.y * axes[1], v.co.z * axes[2]))
    return g


def prickly_pear(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 1))
    S = p.get('size', 0.24)
    bm_pad, bm_ar, bm_sp = bmesh.new(), bmesh.new(), bmesh.new()
    pads = []                                               # (centre, frame matrix, half-width, half-height)

    def add_pad(c, M, w, h):
        g = bmesh.ops.create_uvsphere(bm_pad, u_segments=28, v_segments=14, radius=1.0)
        for v in g['verts']:
            x, y, z = v.co
            # obovate: wider toward the top (+z in the pad's frame), thin (y)
            ww = w * (0.82 + 0.22 * (z + 1) / 2)
            v.co = c + M @ Vector((x * ww, y * S * 0.07, z * h))
        # areoles in a quincunx on both faces, spines from each
        rows, cols = 7, 5
        for i in range(rows):
            for j in range(cols):
                u = (j + 0.5 * (i % 2)) / (cols - 0.5) * 2 - 1
                vv = i / (rows - 1) * 1.7 - 0.85
                if u * u + vv * vv > 0.92:
                    continue
                for side in (-1, 1):
                    ww = w * (0.82 + 0.22 * (vv + 1) / 2)
                    yy = side * S * 0.07 * math.sqrt(max(0.0, 1 - u * u - vv * vv)) * 0.98
                    a = c + M @ Vector((u * ww * 0.92, yy, vv * h * 0.92))
                    nrm = (M @ Vector((u * 0.4, side, vv * 0.3))).normalized()
                    D_ = 0.0028
                    g2 = bmesh.ops.create_icosphere(bm_ar, subdivisions=1, radius=1.0)
                    for v in g2['verts']:
                        v.co = a + v.co * D_
                    for _ in range(rnd.randint(0, 3)):
                        d = (nrm + Vector((rnd.gauss(0, 0.5), rnd.gauss(0, 0.5), rnd.gauss(0, 0.5) + 0.2))).normalized()
                        L = rnd.uniform(0.012, 0.035)
                        g3 = bmesh.ops.create_cone(bm_sp, cap_ends=False, segments=5, radius1=0.0007, radius2=0.0, depth=L)
                        q = d.to_track_quat('Z', 'Y').to_matrix()
                        for v in g3['verts']:
                            v.co = a + q @ (v.co + Vector((0, 0, L / 2)))
        pads.append((c, M, w, h))

    def frame(tilt_x, tilt_y, yaw):
        return (Matrix.Rotation(math.radians(yaw), 3, 'Z') @ Matrix.Rotation(math.radians(tilt_x), 3, 'X')
                @ Matrix.Rotation(math.radians(tilt_y), 3, 'Y'))

    n = p.get('pads', 10)
    # first pads: near the ground, leaning out
    base = []
    for k in range(max(3, n // 2)):
        yaw = rnd.uniform(0, 360); M = frame(rnd.uniform(-50, 50), rnd.uniform(-45, 45), yaw)
        h = S * rnd.uniform(0.42, 0.5); w = h * rnd.uniform(0.72, 0.85)
        c = Vector((rnd.uniform(-1.4, 1.4) * S, rnd.uniform(-1.4, 1.4) * S, h * 0.55))
        add_pad(c, M, w, h); base.append(len(pads) - 1)
    while len(pads) < n:
        pi = rnd.randrange(len(pads)); pc, PM, pw, ph = pads[pi]
        if (pc.z > S * 1.3):
            continue
        t = rnd.uniform(-0.8, 0.8)                           # a point on the parent's upper rim
        rim = pc + PM @ Vector((math.sin(t) * pw, 0.0, math.cos(t) * ph))
        yaw = rnd.uniform(-50, 50); M = PM @ frame(rnd.uniform(-45, 45), math.degrees(t) * 1.2 + rnd.uniform(-25, 25), yaw)
        h = S * rnd.uniform(0.36, 0.48); w = h * rnd.uniform(0.7, 0.85)
        c = rim + M @ Vector((0, 0, h * 0.9))
        if c.z < h * 0.5:
            continue
        add_pad(c, M, w, h)
    mats = [_principled(bpy, f'{name}-pad', p.get('color', '#73885E'), rough=0.42, sss=0.12, spec=0.45, kit=kit),
            _principled(bpy, f'{name}-areole', '#6A5A44', rough=0.9, kit=kit),
            _principled(bpy, f'{name}-spine', p.get('spine', '#E9DFC6'), rough=0.35, sss=0.4, spec=0.5, kit=kit)]
    _noise_tint(mats[0], S * 0.6, p.get('color', '#73885E'), p.get('color2', '#8C8F6A'), kit=kit)
    objs = []
    for bm, m, suffix in ((bm_pad, mats[0], 'pads'), (bm_ar, mats[1], 'areoles'), (bm_sp, mats[2], 'spines')):
        objs += kit.finish(bpy, f'{name}-{suffix}', bm, p, smooth=suffix != 'spines', mat=m)
    return objs


def yucca(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 1))
    L, W, n = p.get('length', 0.6), p.get('width', 0.025), p.get('leaves', 60)
    bm, bm_dry = bmesh.new(), bmesh.new()
    for k in range(n):
        yaw = rnd.uniform(0, 2 * math.pi)
        up = rnd.uniform(15, 85) if k > n * 0.15 else rnd.uniform(70, 88)   # some stand up in the centre
        L1 = L * rnd.uniform(0.75, 1.1) * (1.0 - 0.3 * (up < 30))
        pts, rad = [], []
        for i in range(7):
            t = i / 6
            el = math.radians(up - 18 * t * t * (1 - up / 95))                 # stiff, a slight droop at the tip
            r = L1 * t
            pts.append([math.cos(yaw) * r * math.cos(el), math.sin(yaw) * r * math.cos(el), 0.04 + r * math.sin(el)])
            rad.append(W * (0.55 + 0.6 * math.sin(math.pi * min(1.0, t * 0.9 + 0.1))) * (1 - t) ** 0.7 + 0.0008)
        kit._tube(bm, pts, rad, 0.22, rnd.uniform(-25, 25), 8, 4)
    for k in range(int(n * 0.5)):                            # the skirt of dry leaves, hanging
        yaw = rnd.uniform(0, 2 * math.pi); L1 = L * rnd.uniform(0.4, 0.75)
        pts = []
        for i in range(5):
            t = i / 4; el = math.radians(10 - 45 * t)
            pts.append([math.cos(yaw) * L1 * t * math.cos(el), math.sin(yaw) * L1 * t * math.cos(el), 0.06 + L1 * t * math.sin(el) * 0.6])
        kit._tube(bm_dry, pts, [W * 0.6 * (1 - t / 5) + 0.0006 for t in range(5)], 0.2, rnd.uniform(-60, 60), 6, 3)
    m = _principled(bpy, f'{name}-leaf', p.get('color', '#6F8466'), rough=0.5, sss=0.15, spec=0.45, kit=kit)
    _noise_tint(m, L * 0.4, p.get('color', '#6F8466'), p.get('color2', '#8A9468'), kit=kit)
    md = _principled(bpy, f'{name}-dry', '#9A8466', rough=0.8, kit=kit)
    return kit.finish(bpy, f'{name}-leaves', bm, p, smooth=True, mat=m) + kit.finish(bpy, f'{name}-dry', bm_dry, p, smooth=True, mat=md)


def sagebrush(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 1))
    w, d, h = p.get('size', [0.9, 0.8, 0.7])
    bm_w, bm_l = bmesh.new(), bmesh.new()
    tips = []
    for k in range(p.get('stems', 14)):
        a = rnd.uniform(0, 2 * math.pi); r0 = rnd.uniform(0, 0.12) * w
        base = Vector((math.cos(a) * r0, math.sin(a) * r0, -0.02))
        top = Vector((math.cos(a) * w * rnd.uniform(0.15, 0.45), math.sin(a) * d * rnd.uniform(0.15, 0.45), h * rnd.uniform(0.55, 0.9)))
        mid = base.lerp(top, 0.5) + Vector((rnd.gauss(0, 0.05), rnd.gauss(0, 0.05), 0))
        kit._tube(bm_w, [list(base), list(mid), list(top)], [0.012, 0.008, 0.004], 1.0, 0.0, 6, 3)
        for j in range(6):
            s = base.lerp(top, rnd.uniform(0.4, 0.95))
            e = s + Vector((rnd.gauss(0, 0.18) * w, rnd.gauss(0, 0.18) * d, rnd.uniform(0.05, 0.2) * h))
            kit._tube(bm_w, [list(s), list(e)], [0.004, 0.0015], 1.0, 0.0, 5, 2)
            tips.append(e)
    # foliage: clusters of fine leaves round the tips, filling a rounded crown
    for _ in range(p.get('leaves', 7000)):
        c = rnd.choice(tips)
        v = c + Vector((rnd.gauss(0, 0.11), rnd.gauss(0, 0.11), rnd.gauss(0, 0.08)))
        ex = ((v.x / (w * 0.5)) ** 2 + (v.y / (d * 0.5)) ** 2 + ((v.z - h * 0.5) / (h * 0.55)) ** 2)
        if ex > 1.0 or v.z < 0.05:
            continue
        g = bmesh.ops.create_icosphere(bm_l, subdivisions=1, radius=1.0)
        q = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).to_track_quat('Z', 'Y').to_matrix()
        s = rnd.uniform(0.6, 1.2)
        for vv in g['verts']:
            vv.co = v + q @ Vector((vv.co.x * 0.006 * s, vv.co.y * 0.003 * s, vv.co.z * 0.016 * s))
    mw = _principled(bpy, f'{name}-wood', '#6E6253', rough=0.9, kit=kit)
    ml = _principled(bpy, f'{name}-leaf', p.get('color', '#8E977F'), rough=0.75, sss=0.1, spec=0.3, kit=kit)
    _noise_tint(ml, 0.15, p.get('color', '#8E977F'), p.get('color2', '#A7A991'), kit=kit)
    return kit.finish(bpy, f'{name}-wood', bm_w, p, smooth=True, mat=mw) + kit.finish(bpy, f'{name}-leaf', bm_l, p, smooth=True, mat=ml)


# --- ground ---------------------------------------------------------------------------------------------------------
def ground_mix(mat, spec):
    """Blend a second photographed texture set into a terrain's material through a noise mask: its colour, roughness and
    normal mixed in where the mask is high (stony patches in sand)."""
    import assets
    import bpy
    maps = assets.texture(spec['texture'], spec.get('res', '2k'))
    sz = spec.get('tex_scale') or (assets.size_m(spec['texture']) or (2.0, 2.0))[0]
    nt = mat.node_tree; bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1.0 / sz, 1.0 / sz, 1.0 / sz)
    mp.inputs['Rotation'].default_value = (0, 0, math.radians(spec.get('rot', 23.0)))
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    msize, cover = spec.get('mask', [6.0, 0.35])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / msize
    nz.inputs['Detail'].default_value = 5.0; nz.inputs['Roughness'].default_value = 0.6
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    mr = nt.nodes.new('ShaderNodeMapRange')
    lo = 0.62 - cover * 0.3
    mr.inputs['From Min'].default_value = lo; mr.inputs['From Max'].default_value = lo + 0.06
    nt.links.new(nz.outputs['Fac'], mr.inputs['Value'])

    def img(key, colour):
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(os.path.abspath(maps[key]), check_existing=True)
        if not colour:
            n.image.colorspace_settings.name = 'Non-Color'
        n.projection = 'BOX'; n.projection_blend = 0.25
        nt.links.new(mp.outputs['Vector'], n.inputs['Vector'])
        return n

    def mixin(sock, new_out, data='RGBA'):
        if not sock.links:
            return
        src = sock.links[0].from_socket
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = data
        nt.links.new(mr.outputs['Result'], mx.inputs['Factor'])
        if data == 'RGBA':
            nt.links.new(src, mx.inputs['A']); nt.links.new(new_out, mx.inputs['B']); res = mx.outputs['Result']
        else:
            nt.links.new(src, mx.inputs[2]); nt.links.new(new_out, mx.inputs[3]); res = mx.outputs[0]
        nt.links.new(res, sock)

    if 'diff' in maps:
        col = img('diff', True).outputs['Color']
        if spec.get('tint') and spec.get('tint_mix', 0) > 0:
            h = spec['tint'].lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
            c = [((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c]
            tm = nt.nodes.new('ShaderNodeMix'); tm.data_type = 'RGBA'; tm.blend_type = 'COLOR'
            tm.inputs['Factor'].default_value = spec['tint_mix']; tm.inputs['B'].default_value = (*c, 1.0)
            nt.links.new(col, tm.inputs['A']); col = tm.outputs['Result']
        # the base-colour chain may already be multiplied (patch variation, albedo): mix in at the BSDF's input
        mixin(bs.inputs['Base Color'], col)
    if 'rough' in maps:
        mixin(bs.inputs['Roughness'], img('rough', False).outputs['Color'])
    if 'nor_gl' in maps:
        nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = spec.get('bump', 1.0)
        nt.links.new(img('nor_gl', False).outputs['Color'], nm.inputs['Color'])
        sock = bs.inputs['Normal']
        if sock.links:
            src = sock.links[0].from_socket
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'VECTOR'
            nt.links.new(mr.outputs['Result'], mx.inputs['Factor'])
            nt.links.new(src, mx.inputs[4]); nt.links.new(nm.outputs['Normal'], mx.inputs[5])
            nt.links.new(mx.outputs[1], sock)
        else:
            nt.links.new(nm.outputs['Normal'], sock)


def terrain(bpy, name, p, kit):
    """dust_el.terrain, then any `mixes` blended in (ground_mix)."""
    objs = D.terrain(bpy, name, p, kit)
    for spec in p.get('mixes', []):
        ground_mix(objs[0].data.materials[0], spec)
    return objs


tumbleweed = D.tumbleweed
