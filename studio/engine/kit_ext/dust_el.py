"""Dust's pieces for round 31b, the speaker in its element (spinoffs/barkhorn/elements/dust.py): the American Southwest
at golden hour.

- terrain: the whole desert floor as one mesh, so no seam: a fan of rings round the camera's ground point `eye` [x, y],
  across `heading` +- `half_angle` degrees, from `r0` to `r1` metres, its rings spaced in proportion to their radius so a
  cell stays about the same size on screen (dense under the speaker, coarse at the mesas). Level within `flat` [x, y, r];
  swells of `swell` metres beyond, in patches `swell_size` across; rising `rim` metres over the last 12 % so its edge sits
  on the horizon. `segments` across the fan. Material as any piece (`material: pbr`, `texture`, ...); `vary` [size, amount]
  darkens and reddens it in patches so a texture laid at a few metres a tile does not repeat to the eye.
- mesa: a flat-topped butte or mesa in the manner of Monument Valley: sheer, fluted cliffs from `cliff` (a share of
  `height`) to the top, standing on a concave talus slope that spreads to `spread` times its foot, a footprint of radius
  `radius` (m) wandering by `wander` and stretched by `squash` in y, `seed`. Material as any piece.
- tumbleweed: a Russian thistle's dead ball, `diameter` (m): `stems` stems from the core, each branching into `branches`
  twigs, each into `twigs` finer ones, all curling round inside the ball, `seed`; a dry straw colour `color`.
- dust: dust hanging in the air, a box `size` [w, d, h] of scattering volume whose density (`density` per metre at its
  thickest) is broken into wisps by noise `wisp` metres across and fades to nothing at the box's sides and top, `color`.
"""
import math, random

import bmesh
from mathutils import Vector, noise


def _smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def _vary(bpy, mat, size, amount, tint=(0.62, 0.36, 0.25)):
    """Multiply a material's base colour by a slow noise (patches `size` m across), toward a darker, redder sand."""
    nt = mat.node_tree
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    sock = bs.inputs['Base Color']
    if not sock.links:
        return
    src = sock.links[0].from_socket
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / size
    nz.inputs['Detail'].default_value = 3.0; nz.inputs['Roughness'].default_value = 0.55
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = 0.35; cr.elements[0].color = (1, 1, 1, 1)
    cr.elements[1].position = 0.7; cr.elements[1].color = (tint[0], tint[1], tint[2], 1)
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs['Factor'].default_value = amount
    nt.links.new(src, mul.inputs['A']); nt.links.new(ramp.outputs['Color'], mul.inputs['B'])
    nt.links.new(mul.outputs['Result'], sock)


def _dual(bpy, mat, scale_mul, rot_deg, mask_size):
    """A second sampling of every image in the material, at `scale_mul` the size and turned `rot_deg` about z, blended
    with the first through a noise mask `mask_size` metres across: two ripple fields of different wavelength and
    direction, so the ground does not read as one print."""
    nt = mat.node_tree
    imgs = [n for n in nt.nodes if n.type == 'TEX_IMAGE']
    if not imgs:
        return
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    src_map = next((n for n in nt.nodes if n.type == 'MAPPING' and n is not mp), None)
    sc = src_map.inputs['Scale'].default_value if src_map else (1, 1, 1)
    mp.inputs['Scale'].default_value = (sc[0] / scale_mul, sc[1] / scale_mul, sc[2] / scale_mul)
    mp.inputs['Rotation'].default_value = (0.0, 0.0, math.radians(rot_deg))
    mp.inputs['Location'].default_value = (13.7, 5.3, 0.0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / mask_size
    nz.inputs['Detail'].default_value = 2.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    mask = nt.nodes.new('ShaderNodeMapRange'); mask.inputs['From Min'].default_value = 0.4; mask.inputs['From Max'].default_value = 0.6
    nt.links.new(nz.outputs['Fac'], mask.inputs['Value'])
    for n in imgs:
        outs = [l for l in nt.links if l.from_node is n and l.from_socket.name == 'Color']
        if not outs:
            continue
        m = nt.nodes.new('ShaderNodeTexImage'); m.image = n.image; m.projection = n.projection
        m.projection_blend = n.projection_blend; m.interpolation = n.interpolation
        nt.links.new(mp.outputs['Vector'], m.inputs['Vector'])
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
        nt.links.new(mask.outputs['Result'], mix.inputs['Factor'])
        nt.links.new(n.outputs['Color'], mix.inputs['A']); nt.links.new(m.outputs['Color'], mix.inputs['B'])
        for l in outs:
            to = l.to_socket
            nt.links.remove(l)
            nt.links.new(mix.outputs['Result'], to)


def _albedo(mat, k, spec=None):
    """Scale a material's base colour by `k` (a lighter photographed texture brought down to a darker sand), and set its
    specular level (`spec`: dry sand glares less than the texture's default at a grazing angle)."""
    nt = mat.node_tree
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    if spec is not None:
        bs.inputs['Specular IOR Level'].default_value = spec
    sock = bs.inputs['Base Color']
    if not sock.links:
        return
    src = sock.links[0].from_socket
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs['Factor'].default_value = 1.0; mul.inputs['B'].default_value = (k, k, k, 1.0)
    nt.links.new(src, mul.inputs['A']); nt.links.new(mul.outputs['Result'], sock)


def _ripples(mat, wavelength, strength, dir_deg, wander, patch):
    """Wind ripples in the shader: a sine wave across `dir_deg`, its
    crests wandering by a noise distortion (`wander`) and its wavelength drifting 0.6 to 1.6x by a slow noise, fading out in patches
    `patch` metres across where the wind has scoured the sand smooth; chained after the texture's own normal map."""
    nt = mat.node_tree
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    prev = bs.inputs['Normal'].links[0].from_socket if bs.inputs['Normal'].links else None
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (0.0, 0.0, math.radians(dir_deg))
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    # the wavelength drifts: scale the coordinates by 0.8 to 1.25 in slow patches
    dn = nt.nodes.new('ShaderNodeTexNoise'); dn.inputs['Scale'].default_value = 1.0 / (patch * 1.7)
    nt.links.new(tc.outputs['Object'], dn.inputs['Vector'])
    dr = nt.nodes.new('ShaderNodeMapRange'); dr.inputs['To Min'].default_value = 0.6; dr.inputs['To Max'].default_value = 1.6
    nt.links.new(dn.outputs['Fac'], dr.inputs['Value'])
    sc = nt.nodes.new('ShaderNodeVectorMath'); sc.operation = 'SCALE'
    nt.links.new(mp.outputs['Vector'], sc.inputs[0]); nt.links.new(dr.outputs['Result'], sc.inputs['Scale'])
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'; wv.wave_profile = 'SIN'
    wv.inputs['Scale'].default_value = 1.0 / wavelength; wv.inputs['Distortion'].default_value = wander
    wv.inputs['Detail'].default_value = 3.0; wv.inputs['Detail Scale'].default_value = 1.6
    wv.inputs['Detail Roughness'].default_value = 0.55
    nt.links.new(sc.outputs['Vector'], wv.inputs['Vector'])
    # scoured patches: the ripples fade where a slow noise is low
    pn = nt.nodes.new('ShaderNodeTexNoise'); pn.inputs['Scale'].default_value = 1.0 / patch
    nt.links.new(tc.outputs['Object'], pn.inputs['Vector'])
    pr = nt.nodes.new('ShaderNodeMapRange'); pr.inputs['From Min'].default_value = 0.42; pr.inputs['From Max'].default_value = 0.58
    nt.links.new(pn.outputs['Fac'], pr.inputs['Value'])
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    nt.links.new(wv.outputs['Fac'], mul.inputs[0]); nt.links.new(pr.outputs['Result'], mul.inputs[1])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = strength
    bp.inputs['Distance'].default_value = wavelength * 0.12
    nt.links.new(mul.outputs['Value'], bp.inputs['Height'])
    if prev is not None:
        nt.links.new(prev, bp.inputs['Normal'])
    nt.links.new(bp.outputs['Normal'], bs.inputs['Normal'])


def terrain(bpy, name, p, kit):
    ex, ey = p.get('eye', [0.0, -5.0])
    head, half = math.radians(p.get('heading', 90.0)), math.radians(p.get('half_angle', 40.0))
    r0, r1, seg = p.get('r0', 1.5), p.get('r1', 290.0), p.get('segments', 420)
    fx, fy, fr = p.get('flat', [0.0, 0.0, 2.5])
    swell, ssize, rim = p.get('swell', 0.25), p.get('swell_size', 9.0), p.get('rim', 1.5)
    s2, s2size = p.get('swell2', [0.0, 5.0])
    step = 2 * half / seg
    radii, r = [], r0
    while r < r1:
        radii.append(r); r *= 1 + step
    radii.append(r1)
    off = Vector((17.3, -4.1, 2.2))
    bm = bmesh.new()
    rows = []
    for rr in radii:
        row = []
        for i in range(seg + 1):
            a = head - half + step * i
            x, y = ex + rr * math.cos(a), ey + rr * math.sin(a)
            d = math.hypot(x - fx, y - fy)
            t = _smooth((d - fr) / (fr * 2.5))                  # level under the speaker, swelling beyond
            n = noise.noise(Vector((x / ssize, y / ssize, 0.3)) + off)
            n += 0.35 * noise.noise(Vector((x / (ssize * 0.37), y / (ssize * 0.37), 1.7)) + off)
            t2 = _smooth((d - fr * 0.7) / fr)                 # small swells start nearer the speaker
            n2 = noise.noise(Vector((x / s2size, y / (s2size * 1.8), 4.1)) + off)
            far = _smooth((rr - 0.88 * r1) / (0.12 * r1))
            z = t * swell * n + t2 * s2 * n2 + far * rim
            row.append(bm.verts.new((x, y, z)))
        rows.append(row)
    for a, b in zip(rows, rows[1:]):
        for i in range(seg):
            bm.faces.new((a[i], a[i + 1], b[i + 1], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    for f in bm.faces:
        if f.normal.z < 0:
            f.normal_flip()
    q = dict(p); q.pop('position', None)
    objs = kit.finish(bpy, name, bm, q)
    for dl in p.get('duals', [p['dual']] if p.get('dual') else []):
        _dual(bpy, objs[0].data.materials[0], *dl)
    if p.get('ripples'):
        _ripples(objs[0].data.materials[0], *p['ripples'])
    if p.get('albedo', 1.0) != 1.0 or 'spec' in p:
        _albedo(objs[0].data.materials[0], p.get('albedo', 1.0), p.get('spec'))
    if p.get('vary'):
        _vary(bpy, objs[0].data.materials[0], *p['vary'])
    return objs


def _beds(mat, band, contrast, seed=0.0):
    """Horizontal beds in the rock's colour: bands of uneven thickness, lighter and darker, wavering a little, so the
    strata read through haze and at a distance."""
    nt = mat.node_tree
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    sock = bs.inputs['Base Color']
    if not sock.links:
        return
    src = sock.links[0].from_socket
    tc = nt.nodes.new('ShaderNodeTexCoord')
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'
    wv.inputs['Scale'].default_value = 1.0 / band; wv.inputs['Distortion'].default_value = 3.0
    wv.inputs['Detail'].default_value = 3.0; wv.inputs['Detail Scale'].default_value = 0.4
    nt.links.new(tc.outputs['Object'], wv.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / (band * 2.7)
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = 0.25; cr.elements[0].color = (1 - contrast, 1 - contrast * 1.1, 1 - contrast * 1.2, 1)
    cr.elements[1].position = 0.75; cr.elements[1].color = (1 + contrast * 0.3, 1 + contrast * 0.25, 1 + contrast * 0.2, 1)
    mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'MULTIPLY'
    nt.links.new(wv.outputs['Fac'], mx.inputs[0]); nt.links.new(nz.outputs['Fac'], mx.inputs[1])
    nt.links.new(mx.outputs['Value'], ramp.inputs['Fac'])
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs['Factor'].default_value = 1.0
    nt.links.new(src, mul.inputs['A']); nt.links.new(ramp.outputs['Color'], mul.inputs['B'])
    nt.links.new(mul.outputs['Result'], sock)


def mesa(bpy, name, p, kit):
    R, H = p.get('radius', 20.0), p.get('height', 25.0)
    cliff, spread = p.get('cliff', 0.38), p.get('spread', 1.7)
    squash, wander = p.get('squash', 0.6), p.get('wander', 0.12)
    rnd = random.Random(p.get('seed', 1))
    seg = p.get('segments', 900)
    ph = [rnd.uniform(0, 6.283) for _ in range(6)]
    off = Vector((rnd.uniform(-90, 90), rnd.uniform(-90, 90), 0))

    def foot(th):
        k = 1 + wander * (math.sin(2 * th + ph[0]) + 0.6 * math.sin(3 * th + ph[1]) + 0.35 * math.sin(5 * th + ph[2])
                          + 0.5 * noise.noise(Vector((math.cos(th) * 2.2, math.sin(th) * 2.2, 0.5)) + off))
        return k

    def ring(rad_f, z, flute=0.0, rough=0.0):
        out = []
        for i in range(seg):
            th = 2 * math.pi * i / seg
            k = foot(th) * rad_f
            if flute:                                         # gullies and buttresses down the cliff
                k *= 1 + flute * (noise.noise(Vector((math.cos(th) * 14, math.sin(th) * 14, z / H * 0.8)) + off)
                                   + 0.5 * noise.noise(Vector((math.cos(th) * 40, math.sin(th) * 40, z / H * 2.0)) + off))
            if rough:
                k *= 1 + rough * noise.noise(Vector((math.cos(th) * 3, math.sin(th) * 3, z / H * 4)) + off)
            out.append((R * k * math.cos(th), R * k * math.sin(th) * squash, z))
        return out

    rings = []
    nt = 9                                                    # the talus, concave, from the plain to the cliff's foot
    for j in range(nt + 1):
        t = j / nt
        rf = spread - (spread - 1.0) * (1 - (1 - t) ** 1.8)
        rings.append(ring(rf, H * cliff * t, rough=0.05 * (1 - t) + 0.02))
    nc = p.get('cliff_rings', 110)                             # the cliff, near vertical, a slight batter, in ledges
    band, ledge = p.get('band', 2.2), p.get('ledge', 0.025)
    for j in range(1, nc + 1):
        t = j / nc
        z = H * (cliff + (1 - cliff) * t)
        zw = z + band * (0.45 * math.sin(z * 0.61 + ph[3]) + 0.3 * math.sin(z * 1.37 + ph[4]))   # beds of uneven thickness
        f = (zw / band) % 1.0                                 # each bed overhangs the softer one below it
        step = ledge * (f ** 3 - 0.5)
        rings.append(ring((1.0 - 0.06 * t) * (1 + step), z, flute=0.09, rough=0.02))
    rings.append(ring(0.9, H * 1.004, flute=0.03))           # the caprock's rim, eased over
    bm = bmesh.new()
    vrows = [[bm.verts.new(v) for v in r] for r in rings]
    for a, b in zip(vrows, vrows[1:]):
        for i in range(seg):
            bm.faces.new((a[i], a[(i + 1) % seg], b[(i + 1) % seg], b[i]))
    top = bm.verts.new((0.0, 0.0, H * 1.006))
    last = vrows[-1]
    for i in range(seg):
        bm.faces.new((last[i], last[(i + 1) % seg], top))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    objs = kit.finish(bpy, name, bm, p, smooth=True)
    if p.get('vary'):
        _vary(bpy, objs[0].data.materials[0], *p['vary'], tint=(0.55, 0.42, 0.38))
    if p.get('beds'):
        _beds(objs[0].data.materials[0], *p['beds'], seed=float(p.get('seed', 0)))
    return objs


def tumbleweed(bpy, name, p, kit):
    D = p.get('diameter', 0.7)
    R = D / 2
    rnd = random.Random(p.get('seed', 1))
    bm = bmesh.new()

    def contain(v):
        if v.length > R * 0.97:
            v = v.normalized() * R * rnd.uniform(0.85, 0.97)
        return v

    def grow(start, direction, length, radius, n_pts=5, curl=0.5):
        pts, v, d = [start.copy()], start.copy(), direction.normalized()
        for _ in range(n_pts - 1):
            d = (d + Vector((rnd.gauss(0, curl), rnd.gauss(0, curl), rnd.gauss(0, curl)))).normalized()
            # curl round the ball rather than out of it: lean the heading toward the tangent near the shell
            if v.length > R * 0.6:
                d = (d - v.normalized() * d.dot(v.normalized()) * 0.8).normalized()
            v = contain(v + d * length / (n_pts - 1))
            pts.append(v.copy())
        kit._tube(bm, [list(q) for q in pts], radius, 1.0, 0.0, 5, 3)
        return pts

    def rdir():
        return Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).normalized()

    for _ in range(p.get('stems', 36)):
        s = rdir() * R * 0.08
        pts = grow(s, s if s.length else rdir(), R * rnd.uniform(0.8, 1.1), D * 0.0055, 6, 0.35)
        for _ in range(p.get('branches', 6)):
            a = pts[rnd.randint(1, len(pts) - 1)]
            bp = grow(a, rdir(), R * rnd.uniform(0.35, 0.6), D * 0.0032, 5, 0.6)
            for _ in range(p.get('twigs', 5)):
                b = bp[rnd.randint(1, len(bp) - 1)]
                grow(b, rdir(), R * rnd.uniform(0.12, 0.25), D * 0.0018, 3, 0.8)
    m = bpy.data.materials.new(f'{name}-straw'); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    kit._set(b, 'Base Color', kit._mix(p.get('color', '#B39572'), p.get('color', '#B39572'), 0.0))
    kit._set(b, 'Roughness', 0.62); kit._set(b, 'Specular IOR Level', 0.35)
    kit._set(b, 'Subsurface Weight', 0.25); kit._set(b, 'Subsurface Radius', Vector((0.004, 0.003, 0.0015)))
    # the stems' colour wanders from pale straw to a darker, weathered brown
    nt = m.node_tree
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / (D * 0.08); nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = 0.3; cr.elements[0].color = kit._mix(p.get('color', '#B39572'), '#FFFFFF', 0.15)
    cr.elements[1].position = 0.75; cr.elements[1].color = kit._mix(p.get('color', '#B39572'), '#5A4030', 0.45)
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    objs = kit.finish(bpy, name, bm, p, smooth=True, mat=m)
    if p.get('snap'):                                         # rest on whatever ground lies under it, bedded `snap` m
        ob = objs[0]
        dg = bpy.context.evaluated_depsgraph_get()
        x, y = ob.location.x, ob.location.y
        start = Vector((x, y, 50.0))
        for _ in range(20):                                   # skip its own stems and any volume boxes
            hit, loc, nrm, idx, hob, mtx = bpy.context.scene.ray_cast(dg, start, Vector((0, 0, -1)))
            if not hit or (hob is not ob and hob.type == 'MESH' and not any(
                    sl.material and sl.material.name.endswith('-dust') for sl in hob.material_slots)):
                break
            start = loc - Vector((0, 0, 0.001))
        if hit:                                               # its lowest stem, not its nominal radius, meets the sand
            bpy.context.view_layer.update()
            low = min((ob.matrix_world @ v.co).z for v in ob.data.vertices)
            ob.location.z += loc.z - low - p['snap']
    return objs


def dust(bpy, name, p, kit):
    w, d, h = p.get('size', [4.0, 2.0, 1.0])
    bm = bmesh.new()
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector((v.co.x * w, v.co.y * d, (v.co.z + 0.5) * h))
    m = bpy.data.materials.new(f'{name}-dust'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); vs = nt.nodes.new('ShaderNodeVolumeScatter')
    vs.inputs['Color'].default_value = kit._mix(p.get('color', '#E8B890'), p.get('color', '#E8B890'), 0.0)
    vs.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.65)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    # wisps: noise in object space (metres), contrast stretched
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p.get('wisp', 0.6)
    nz.inputs['Detail'].default_value = 6.0; nz.inputs['Roughness'].default_value = 0.6
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeMapRange'); ramp.inputs['From Min'].default_value = 0.42
    ramp.inputs['From Max'].default_value = 0.75
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Value'])
    # fade to nothing at the sides and the top (generated coordinates run 0..1 across the box)
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Generated'], sep.inputs['Vector'])

    def edge(sock, lo, hi):
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = lo; mr.inputs['From Max'].default_value = hi
        nt.links.new(sock, mr.inputs['Value']); return mr.outputs['Result']

    def mul(a, b):
        mm = nt.nodes.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'
        nt.links.new(a, mm.inputs[0])
        if isinstance(b, float):
            mm.inputs[1].default_value = b
        else:
            nt.links.new(b, mm.inputs[1])
        return mm.outputs['Value']
    fx = mul(edge(sep.outputs['X'], 0.0, 0.25), edge(sep.outputs['X'], 1.0, 0.75))
    fy = mul(edge(sep.outputs['Y'], 0.0, 0.25), edge(sep.outputs['Y'], 1.0, 0.75))
    fz = edge(sep.outputs['Z'], 1.0, 0.0)                     # thickest at the ground
    dens = mul(mul(mul(fx, fy), mul(fz, fz)), ramp.outputs['Result'])
    nt.links.new(mul(dens, float(p.get('density', 0.4))), vs.inputs['Density'])
    nt.links.new(vs.outputs['Volume'], out.inputs['Volume'])
    return kit.finish(bpy, name, bm, p, smooth=False, mat=m)
