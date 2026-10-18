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


def terrain(bpy, name, p, kit):
    ex, ey = p.get('eye', [0.0, -5.0])
    head, half = math.radians(p.get('heading', 90.0)), math.radians(p.get('half_angle', 40.0))
    r0, r1, seg = p.get('r0', 1.5), p.get('r1', 290.0), p.get('segments', 420)
    fx, fy, fr = p.get('flat', [0.0, 0.0, 2.5])
    swell, ssize, rim = p.get('swell', 0.25), p.get('swell_size', 9.0), p.get('rim', 1.5)
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
            far = _smooth((rr - 0.88 * r1) / (0.12 * r1))
            z = t * swell * n + far * rim
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
    if p.get('dual'):
        _dual(bpy, objs[0].data.materials[0], *p['dual'])
    if p.get('vary'):
        _vary(bpy, objs[0].data.materials[0], *p['vary'])
    return objs


def mesa(bpy, name, p, kit):
    R, H = p.get('radius', 20.0), p.get('height', 25.0)
    cliff, spread = p.get('cliff', 0.38), p.get('spread', 1.7)
    squash, wander = p.get('squash', 0.6), p.get('wander', 0.12)
    rnd = random.Random(p.get('seed', 1))
    seg = p.get('segments', 480)
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
    nc = 14                                                   # the cliff, near vertical, a slight batter
    for j in range(1, nc + 1):
        t = j / nc
        rings.append(ring(1.0 - 0.06 * t, H * (cliff + (1 - cliff) * t), flute=0.09, rough=0.02))
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
    return kit.finish(bpy, name, bm, p, smooth=True, mat=m)


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
