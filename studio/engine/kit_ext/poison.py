"""Poison's kit pieces (round 31, spinoffs/barkhorn/dioramas/poison.py): a velvet toadstool with felt spots, a foxglove
spire of velvet bells, a sprig of clay nightshade berries and the icon's skull in clay. Each is `shape: "ext", module:
"poison", fn: ...`, placed by the piece's `position`, `rotate` and `scale` like any kit piece.
"""
import math, random

import bmesh
from mathutils import Matrix, Vector
from mathutils.geometry import tessellate_polygon


def _new(bm, build):
    """Run `build(bm)` and return the verts it made."""
    before = set(bm.verts)
    build(bm)
    return [v for v in bm.verts if v not in before]


def _place(verts, m):
    for v in verts:
        v.co = m @ v.co


def _orient(z_to, at, roll=0.0):
    """A matrix taking local +z to the direction `z_to`, about local z by `roll`, then to `at`."""
    q = Vector(z_to).normalized().to_track_quat('Z', 'Y')
    return Matrix.Translation(Vector(at)) @ q.to_matrix().to_4x4() @ Matrix.Rotation(roll, 4, 'Z')


def _objects(bpy, name, p, kit, parts):
    """One object per material: parts is {(kind, colour, opts as a tuple): bmesh}."""
    obs = []
    for i, ((kind, color, opts), bm) in enumerate(parts.items()):
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        obs += kit.finish(bpy, f'{name}-{i}-{kind}', bm, p, True, kit.material(bpy, kind, color, dict(opts)))
    return obs


def _lean(verts, lean, h):
    """Bend a standing form: x and y pushed by lean * (z / h)^2."""
    lx, ly = lean
    for v in verts:
        t = max(0.0, v.co.z) / h
        v.co.x += lx * t * t; v.co.y += ly * t * t


# --- the toadstool ----------------------------------------------------------------------------------------------------
def toadstool(bpy, name, p, kit):
    """A velvet cap on a felt stem, felt spots on the cap. `height` to the cap's top, `cap` [radius, height], `stem`
    radius, `lean` [dx, dy] at the top, `spots` how many, `cap_color`, `spot_color`, `stem_color`, `gill_color`, `seed`."""
    rnd = random.Random(p.get('seed', 1))
    H = p.get('height', 0.6); R, CH = p.get('cap', [0.3, 0.2]); sr = p.get('stem', 0.06)
    z0 = H - CH                                          # the cap's rim
    stem, cap, spots, gill = bmesh.new(), bmesh.new(), bmesh.new(), bmesh.new()
    sprof = [(sr * 1.45, 0.0), (sr * 1.5, 0.03 * H), (sr * 1.25, 0.12 * H), (sr * 1.02, 0.35 * H), (sr * 0.9, 0.7 * H),
             (sr * 0.86, z0 + 0.02 * CH), (0.0, z0 + 0.05 * CH)]
    sprof = [(0.0, 0.0)] + sprof
    vs = _new(stem, lambda b: kit._lathe(b, sprof, 40))
    # a ring (the skirt) under the cap, as the fly agaric has
    ring = [(0.0, 0.62 * H), (sr * 0.95, 0.62 * H), (sr * 1.55, 0.585 * H), (sr * 1.6, 0.575 * H), (sr * 0.9, 0.6 * H), (0.0, 0.6 * H)]
    if p.get('skirt', True):
        vs += _new(stem, lambda b: kit._lathe(b, ring, 40))
    # the cap: a dome from a rounded rim, its underside lifted to the stem
    cprof = [(0.0, z0 + 0.22 * CH), (sr * 1.05, z0 + 0.2 * CH), (R * 0.93, z0 + 0.02 * CH), (R * 0.985, z0 + 0.04 * CH)]
    dome = []
    for i in range(18):
        th = (i / 17) * math.pi / 2
        dome.append((R * math.cos(th) ** 0.85, z0 + 0.08 * CH + 0.92 * CH * math.sin(th) ** 1.15))
    dome[-1] = (0.0, H)
    cprof += dome
    vc = _new(cap, lambda b: kit._lathe(b, cprof, 72))
    # the gills: a darker disc just under the cap, lines of it raised
    gp = [(sr * 1.1, z0 + 0.195 * CH), (R * 0.9, z0 + 0.03 * CH), (R * 0.9, z0 + 0.025 * CH), (sr * 1.1, z0 + 0.185 * CH)]
    vg = _new(gill, lambda b: kit._lathe(b, [(0.0, z0 + 0.19 * CH)] + gp[:2] + [(0.0, z0 + 0.03 * CH)], 72))
    # spots on the dome, along its normal
    n = p.get('spots', 9)
    sv = []
    for k in range(n):
        for _ in range(30):
            th = rnd.uniform(0.12, 1.25); ph = rnd.uniform(0, 2 * math.pi)
            r = R * math.cos(th) ** 0.85; z = z0 + 0.08 * CH + 0.92 * CH * math.sin(th) ** 1.15
            # the normal from the profile's slope
            dr = -R * 0.85 * math.cos(th) ** -0.15 * math.sin(th); dz = 0.92 * CH * 1.15 * math.sin(th) ** 0.15 * math.cos(th)
            nr, nz = dz, -dr; L = math.hypot(nr, nz); nr, nz = nr / L, nz / L
            c = Vector((r * math.cos(ph), r * math.sin(ph), z))
            if all((c - o).length > R * 0.3 for o in sv):
                break
        sv.append(c)
        s = R * rnd.uniform(0.07, 0.12)
        nrm = Vector((nr * math.cos(ph), nr * math.sin(ph), nz))
        m = _orient(nrm, c + nrm * s * 0.05, rnd.uniform(0, 6.28))
        _place(_new(spots, lambda b: kit._sphere(b, (0, 0, 0), (s, s * rnd.uniform(0.75, 1.0), s * 0.28), 24)), m)
    lean = p.get('lean', [0.0, 0.0])
    for bm in (stem, cap, gill, spots):
        _lean(bm.verts, lean, H)
    parts = {('felt', p.get('stem_color', '#E4DCC4'), ()): stem,
             ('velvet', p.get('cap_color', '#1E3A26'), ()): cap,
             ('suede', p.get('gill_color', '#BFB59A'), ()): gill,
             ('felt', p.get('spot_color', '#E9E4CF'), ()): spots}
    return _objects(bpy, name, p, kit, parts)


# --- the foxglove ----------------------------------------------------------------------------------------------------
def _bell(L, r):
    """A foxglove's bell along +z from its mouth (z 0) to its tip (z L), its mouth hollowed."""
    return [(0.0, 0.22 * L), (0.7 * r, 0.1 * L), (0.95 * r, 0.0), (1.08 * r, 0.04 * L), (0.92 * r, 0.25 * L), (0.78 * r, 0.6 * L),
            (0.52 * r, 0.88 * L), (0.22 * r, L), (0.0, L * 1.01)]


def foxglove(bpy, name, p, kit):
    """A spire: a stem `height` tall bending by `lean`, `bells` velvet bells hung on one side (`side` degrees) down its
    upper part, small closed buds at the tip, a rosette of leaves at its foot. `bell_color`, `bud_color`, `leaf_color`."""
    rnd = random.Random(p.get('seed', 3))
    H = p.get('height', 1.4); lx, ly = p.get('lean', [0.05, 0.0]); side = math.radians(p.get('side', -90))
    stem, bells, buds, leaves, freckles, throat = bmesh.new(), bmesh.new(), bmesh.new(), bmesh.new(), bmesh.new(), bmesh.new()
    def axis(t):
        return Vector((lx * t * t, ly * t * t, H * t))
    pts = [tuple(axis(t)) for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
    kit._tube(stem, pts, [H * 0.012, H * 0.01, H * 0.008, H * 0.006, H * 0.003], 1.0, 0.0, 10, 8)
    n = p.get('bells', 12); br = p.get('bell', H * 0.052)
    for i in range(n):
        t = 0.3 + 0.58 * i / max(1, n - 1)
        size = br * (1.0 - 0.45 * i / n)
        a = side + (0.55 if i % 2 else -0.55) + rnd.uniform(-0.2, 0.2)
        out = Vector((math.cos(a), math.sin(a), 0.0))
        tip = axis(t) + out * H * 0.006
        L = size * 2.3
        d = (out * 0.8 + Vector((0, 0, -0.5))).normalized()   # mouth out and down; the tip at the stem
        m = _orient(-d, tip - (-d) * L)                          # local z from mouth to tip, toward the stem
        _place(_new(bells, lambda b: kit._lathe(b, _bell(L, size), 28)), m)
        # the throat: a pale felt disc set inside the mouth, freckled
        _place(_new(throat, lambda b: kit._lathe(b, [(0.0, 0.2 * L), (0.66 * size, 0.1 * L), (0.66 * size, 0.09 * L), (0.0, 0.19 * L)], 24)), m)
        for k in range(6):
            ph = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(0.15, 0.5) * size
            c = Vector((rr * math.cos(ph), rr * math.sin(ph), 0.1 * L + 0.11 * L * (1 - rr / (0.66 * size))))
            _place(_new(freckles, lambda b: kit._sphere(b, (0, 0, 0), (size * 0.07, size * 0.07, size * 0.03), 10)), m @ Matrix.Translation(c))
    for i in range(p.get('buds', 6)):
        t = 0.9 + 0.1 * i / 6
        a = rnd.uniform(0, 6.28)
        c = axis(t) + Vector((math.cos(a), math.sin(a), 0)) * H * 0.008
        s = br * (0.4 - 0.04 * i)
        _place(_new(buds, lambda b: kit._sphere(b, (0, 0, 0), (s * 0.8, s * 0.8, s * 1.2), 14)), Matrix.Translation(c))
    for i in range(p.get('leaves', 7)):
        a = 2 * math.pi * i / 7 + rnd.uniform(-0.3, 0.3)
        Ll = H * rnd.uniform(0.16, 0.24)
        dirv = Vector((math.cos(a), math.sin(a), 0.25)).normalized()
        m = _orient(dirv, dirv * Ll * 0.55, 0.0)
        _place(_new(leaves, lambda b: kit._sphere(b, (0, 0, 0), (Ll * 0.22, Ll * 0.06, Ll * 0.6), 20)), m @ Matrix.Rotation(math.pi / 2, 4, 'Z'))
    parts = {('flock', p.get('leaf_color', '#2D4A2A'), (('tint2', '#3E5E34'),)): stem,
             ('velvet', p.get('bell_color', '#8A3C78'), ()): bells,
             ('clay', p.get('freckle_color', '#3A0C2E'), ()): freckles,
             ('felt', p.get('throat_color', '#E6CFE0'), ()): throat,
             ('velvet', p.get('bud_color', '#5E6E3A'), ()): buds,
             ('flock', p.get('leaf_color', '#2D4A2A'), (('tint2', '#24401F'),)): leaves}
    return _objects(bpy, name, p, kit, parts)


# --- nightshade --------------------------------------------------------------------------------------------------------
def nightshade(bpy, name, p, kit):
    """A sprig of deadly nightshade: a curved stalk `height` tall, `berries` glossy clay berries at its end, each
    seated in a five-pointed felt calyx, two leaves. `berry_color`, `berry` radius."""
    rnd = random.Random(p.get('seed', 5))
    H = p.get('height', 0.25); br = p.get('berry', 0.02)
    stalk, berries, calyx, leaves = bmesh.new(), bmesh.new(), bmesh.new(), bmesh.new()
    lx, ly = p.get('lean', [0.06, 0.0])
    tip = Vector((lx, ly, H))
    kit._tube(stalk, [(0, 0, 0), (lx * 0.2, ly * 0.2, H * 0.6), tuple(tip)], [br * 0.22, br * 0.18, br * 0.12], 1.0, 0.0, 8, 8)
    for i in range(p.get('berries', 4)):
        a = 2 * math.pi * i / p.get('berries', 4) + rnd.uniform(-0.3, 0.3)
        dirv = Vector((math.cos(a) * 0.8, math.sin(a) * 0.8, -0.5)).normalized()
        L = br * rnd.uniform(1.8, 2.8)
        c = tip + dirv * L
        kit._tube(stalk, [tuple(tip), tuple(tip + dirv * L * 0.5 + Vector((0, 0, 0.2 * L))), tuple(c + Vector((0, 0, br)))],
                  br * 0.1, 1.0, 0.0, 6, 6)
        r = br * rnd.uniform(0.85, 1.15)
        _place(_new(berries, lambda b: kit._sphere(b, (0, 0, 0), (r, r, r * 0.95), 28)), Matrix.Translation(c))
        for k in range(5):
            ph = 2 * math.pi * k / 5 + a
            d = Vector((math.cos(ph), math.sin(ph), 0.9)).normalized()
            m = _orient(d, c + Vector((0, 0, r * 0.75)) + d * r * 0.25, 0.0)
            _place(_new(calyx, lambda b: kit._sphere(b, (0, 0, 0), (r * 0.18, r * 0.05, r * 0.42), 10)), m)
    for i in range(2):
        a = rnd.uniform(0, 6.28)
        d = Vector((math.cos(a), math.sin(a), 0.35)).normalized()
        Ll = H * 0.45
        base = Vector((lx * 0.1, ly * 0.1, H * (0.35 + 0.25 * i)))
        m = _orient(d, base + d * Ll * 0.5, math.pi / 2)
        _place(_new(leaves, lambda b: kit._sphere(b, (0, 0, 0), (Ll * 0.25, Ll * 0.04, Ll * 0.5), 18)), m)
    parts = {('felt', p.get('stalk_color', '#33472C'), ()): stalk,
             ('clay', p.get('berry_color', '#14091A'), (('roughness', 0.16),)): berries,
             ('felt', p.get('calyx_color', '#3E5A30'), ()): calyx,
             ('felt', p.get('leaf_color', '#2B4527'), ()): leaves}
    return _objects(bpy, name, p, kit, parts)


# --- the skull -----------------------------------------------------------------------------------------------------------
def _icon_skull(seg=48):
    """The Poison icon in icon units (y down, a circle of 215 at (0, -55) over a rectangle 250 wide to 235), as lists
    of (x, z) loops: the outline (its teeth's gaps notched in) and the holes (the eyes and the nose)."""
    cy, R = -55.0, 215.0
    out = []
    # walk the circle counter-clockwise in (x, z) from the right shoulder, over the top, to the left shoulder
    zs = -(119.9)                                         # the shoulders' z (= -y)
    th0 = math.atan2(zs - (-cy), 125.0)                   # the angle of (125, zs) about (0, -cy) in x-z
    th1 = math.pi - th0
    for i in range(seg + 1):
        th = th0 + (th1 - th0) * i / seg
        out.append((R * math.cos(th), -cy + R * math.sin(th)))
    out += [(-125, -235), (-60, -235), (-60, -175), (-26, -175), (-26, -235), (26, -235), (26, -175), (60, -175),
            (60, -235), (125, -235)]
    eyes = [[(x + 60 * math.cos(2 * math.pi * k / 28), 88 + 60 * math.sin(2 * math.pi * k / 28)) for k in range(28)] for x in (-82, 82)]
    nose = [(0, 28), (34, -42), (-34, -42)]
    return out, eyes + [nose]


def skull(bpy, name, p, kit):
    """The Poison icon's skull in clay, `size` metres tall (icon 0.0 at its centre), `depth` thick, standing on its jaw
    in the x-z plane, facing -y; its edges eased."""
    size = p.get('size', 0.08); depth = p.get('depth', size * 0.25)
    out, holes = _icon_skull()
    s = size / 505.0                                       # the icon's height: from 235 down to -270
    loops = [[Vector((x * s, 0, (z + 235) * s)) for x, z in L] for L in [out] + holes]
    bm = bmesh.new()
    flat = [v for L in loops for v in L]
    tris = tessellate_polygon([[(v.x, v.z, 0) for v in L] for L in loops])
    front = [bm.verts.new((v.x, -depth / 2, v.z)) for v in flat]
    back = [bm.verts.new((v.x, depth / 2, v.z)) for v in flat]
    for a, b, c in tris:
        for verts in (front, back):
            try:
                bm.faces.new((verts[a], verts[b], verts[c]))
            except ValueError:
                pass
    i0 = 0
    for L in loops:
        n = len(L)
        for k in range(n):
            a, b = i0 + k, i0 + (k + 1) % n
            try:
                bm.faces.new((front[a], front[b], back[b], back[a]))
            except ValueError:
                pass
        i0 += n
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    sharp = [e for e in bm.edges if len(e.link_faces) == 2 and e.calc_face_angle(0.0) > 0.6]
    bmesh.ops.bevel(bm, geom=sharp, offset=depth * 0.22, segments=3, affect='EDGES', profile=0.5)
    return kit.finish(bpy, name, bm, p, True, kit.material(bpy, 'clay', p.get('color', '#E3D8BD'), {'roughness': 0.55}))


# --- moss --------------------------------------------------------------------------------------------------------------
_MOSS = {}


def moss(bpy, name, p, kit):
    """Flock moss whose sheen is its own green, not white (the kit's flock catches a back light grey): any kit shape
    (`as`), its flock's sheen tinted toward `color` and softened."""
    q = dict(p); q['shape'] = p.get('as', 'box'); q['material'] = 'flock'
    return _mossify(p, kit, kit.piece(bpy, name, q))


# --- the swamp's glow ----------------------------------------------------------------------------------------------------
def glow_pool(bpy, name, p, kit):
    """A flat cut-out (`outline` [[x, z], ...], like the kit's extrude) that glows `emit` at its centre, fading to
    nothing at `fade` of the way to its rim `r` (an ellipse `squash` as deep as wide), so light seems to come from the
    swamp's depth rather than from a sheet."""
    bm = bmesh.new()
    kit._extrude(bm, p['outline'], p.get('depth', 0.004), p.get('ease', 0.001))
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#6CFF8A'))
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    r = p.get('r', 0.5); sq = p.get('squash', 0.66)
    mp.inputs['Scale'].default_value = (1.0 / r, 1.0, 1.0 / (r * sq))       # the outline lies in x-z
    ln = nt.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'
    mr.inputs['From Min'].default_value = p.get('core', 0.15); mr.inputs['From Max'].default_value = p.get('fade', 0.95)
    mr.inputs['To Min'].default_value = p.get('emit', 1.5); mr.inputs['To Max'].default_value = 0.0
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], ln.inputs[0])
    nt.links.new(ln.outputs['Value'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], em.inputs['Strength'])
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    obs = kit.finish(bpy, name, bm, p, True, m)
    for ob in obs:
        ob.visible_shadow = False
    return obs


# --- mist --------------------------------------------------------------------------------------------------------------
def mist(bpy, name, p, kit):
    """A bank of mist: a box `size` [w, d, h] standing on its base, a scattering volume whose density is `density` at
    the ground, thinning to nothing at its top, and torn into wisps `wisp` metres across (0 for an even haze)."""
    w, d, h = p.get('size', [4.0, 4.0, 0.4])
    bm = bmesh.new()
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector((v.co.x * w, v.co.y * d, (v.co.z + 0.5) * h))
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); vs = nt.nodes.new('ShaderNodeVolumeScatter')
    vs.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#FFFFFF'))
    vs.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.3)
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    fall = nt.nodes.new('ShaderNodeMapRange'); fall.interpolation_type = 'SMOOTHSTEP'
    fall.inputs['From Min'].default_value = 0.0; fall.inputs['From Max'].default_value = h
    fall.inputs['To Min'].default_value = p.get('density', 0.3); fall.inputs['To Max'].default_value = 0.0
    nt.links.new(sep.outputs['Z'], fall.inputs['Value'])
    dens = fall.outputs['Result']
    if p.get('wisp', 0.0) > 0:
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p['wisp']
        nz.inputs['Detail'].default_value = 3.0
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        cut = nt.nodes.new('ShaderNodeMapRange'); cut.interpolation_type = 'SMOOTHSTEP'
        cut.inputs['From Min'].default_value = p.get('wisp_lo', 0.42); cut.inputs['From Max'].default_value = p.get('wisp_hi', 0.62)
        nt.links.new(nz.outputs['Fac'], cut.inputs['Value'])
        mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
        nt.links.new(dens, mul.inputs[0]); nt.links.new(cut.outputs['Result'], mul.inputs[1])
        dens = mul.outputs['Value']
    nt.links.new(dens, vs.inputs['Density']); nt.links.new(vs.outputs['Volume'], out.inputs['Volume'])
    obs = kit.finish(bpy, name, bm, p, False, m)
    for ob in obs:
        ob.visible_shadow = False
    return obs


# --- the ground --------------------------------------------------------------------------------------------------------
def _smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def ground_z(g, x, y):
    """The terrain's height at world (x, y): `g` is the terrain piece's spec (see terrain)."""
    from mathutils import noise
    amp, feat = g.get('amp', 0.06), g.get('feature', 1.2)
    cx, cy = g.get('calm', [0.6, 0.5]); waver = g.get('waver', 0.18)
    k = _smooth((math.hypot(x / cx, y / cy) - 1.0) / 1.5)
    for bx, by, rx, ry, dep in g.get('dents', []):      # calm round a swamp too, so its shore is the bed's own
        k *= _smooth((math.hypot((x - bx) / rx, (y - by) / ry) - 1.2) / 0.8)
    z = g.get('position', [0, 0, 0])[2] + amp * k * noise.noise(Vector((x / feat, y / feat, 0.3)))
    for bx, by, rx, ry, h in g.get('bumps', []):
        r = math.hypot((x - bx) / rx, (y - by) / ry)
        if r < 1.0:
            z += h * (1 - r * r) ** 1.5
    for bx, by, rx, ry, dep in g.get('dents', []):
        a = math.atan2((y - by) / ry, (x - bx) / rx)
        wv = 1.0 + waver * noise.noise(Vector((math.cos(a) * 1.3, math.sin(a) * 1.3, bx)))
        r = math.hypot((x - bx) / rx, (y - by) / ry) / wv
        if r < 1.0:
            z -= dep * _smooth(1.0 - r) ** g.get('dent_edge', 0.3)
    return z


def _mossify(p, kit, obs):
    for ob in obs:
        m0 = ob.data.materials[0]
        if m0.name not in _MOSS:
            m = m0.copy(); b = m.node_tree.nodes['Principled BSDF']
            kit._set(b, 'Sheen Tint', kit._mix(p.get('tint2', p.get('color')), '#FFFFFF', 0.2))
            kit._set(b, 'Sheen Weight', p.get('sheen', 0.5))
            _MOSS[m0.name] = m
        ob.data.materials[0] = _MOSS[m0.name]
    return obs


def terrain(bpy, name, p, kit):
    """Moss ground as a grid `size` [w, d] centred on the piece, `res` metres a cell: rolling by `amp` over features
    `feature` metres across, calm within `calm` [rx, ry] of the origin (where the speaker stands), raised by `bumps`
    [[x, y, rx, ry, h], ...] and sunk by `dents` [[x, y, rx, ry, depth], ...] (a swamp's bed), its shore wavering by
    `waver`. Its material is the moss's (`color`, `tint2`)."""
    w, d = p.get('size', [20.0, 20.0]); cell = p.get('res', 0.05)
    nx, ny = int(w / cell), int(d / cell)
    px, py, pz = p['position']
    bm = bmesh.new()
    rows = []
    for j in range(ny + 1):
        y = -d / 2 + d * j / ny
        rows.append([bm.verts.new((-w / 2 + w * i / nx, y, ground_z(p, -w / 2 + w * i / nx + px, y + py) - pz))
                     for i in range(nx + 1)])
    for j in range(ny):
        for i in range(nx):
            bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
    q = dict(p); q['material'] = 'flock'
    return _mossify(p, kit, kit.finish(bpy, name, bm, q, True, kit.piece_material(bpy, q)))


def clumps(bpy, name, p, kit):
    """Cushion moss: `points` [[x, y, r], ...] (world x, y), each a squashed ball half sunk in the `ground` (a
    terrain's spec), in one mesh."""
    g = p['ground']; rnd = random.Random(p.get('seed', 1))
    verts, faces = [], []
    nu, nv = 14, 7
    for x, y, r in p['points']:
        z = ground_z(g, x, y)
        c, rad = (x, y, z - r * 0.25), (r, r * rnd.uniform(0.8, 1.0), r * rnd.uniform(0.5, 0.75))
        i0 = len(verts)
        verts.append((c[0], c[1], c[2] - rad[2]))
        for j in range(1, nv):
            ph = math.pi * j / nv
            for i in range(nu):
                th = 2 * math.pi * i / nu
                verts.append((c[0] + rad[0] * math.sin(ph) * math.cos(th), c[1] + rad[1] * math.sin(ph) * math.sin(th),
                              c[2] - rad[2] * math.cos(ph)))
        verts.append((c[0], c[1], c[2] + rad[2]))
        top = len(verts) - 1
        ring = lambda j, i: i0 + 1 + (j - 1) * nu + i % nu
        for i in range(nu):
            faces.append((i0, ring(1, i + 1), ring(1, i)))
            faces.append((top, ring(nv - 1, i), ring(nv - 1, i + 1)))
            for j in range(1, nv - 1):
                faces.append((ring(j, i), ring(j, i + 1), ring(j + 1, i + 1), ring(j + 1, i)))
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces)
    bm = bmesh.new(); bm.from_mesh(me); bpy.data.meshes.remove(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    q = dict(p); q['material'] = 'flock'; q['position'] = [0, 0, 0]
    return _mossify(p, kit, kit.finish(bpy, name, bm, q, True, kit.piece_material(bpy, q)))
