"""Fog, concept C (round 31b): San Francisco you can name. From a Marin headland above the Golden Gate, looking over
the bridge to the city: the bridge (`bridge`), the far shore and the city's hills (`land`), the city (`city`), Sutro
Tower on its hill (`sutro`), the water (`water`) and the fog through the Gate and over the west side (`fog`).

The world: the camera looks along +y; the water is at `water` metres (the camera's ground is at 0); a place far off is
given by its bearing (degrees right of the view's centre) and its distance from the origin.
"""
import math, random

import bmesh
from mathutils import Matrix, Vector, noise

import fog_b_el as B


def _at(b, d):
    return d * math.sin(math.radians(b)), d * math.cos(math.radians(b))


def _polar(x, y):
    return math.degrees(math.atan2(x, y)), math.hypot(x, y)


def _lin(h):
    return tuple(((int(h[i:i + 2], 16) / 255 + 0.055) / 1.055) ** 2.4 if int(h[i:i + 2], 16) / 255 > 0.04045
                 else int(h[i:i + 2], 16) / 255 / 12.92 for i in (1, 3, 5)) + (1.0,)


def _mat(bpy, name, color, rough=0.6, spec=0.4, noise_size=None, noise_mix=0.0, color2=None, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    bs = nt.nodes['Principled BSDF']
    bs.inputs['Roughness'].default_value = rough
    if 'Specular IOR Level' in bs.inputs:
        bs.inputs['Specular IOR Level'].default_value = spec
    bs.inputs['Metallic'].default_value = metal
    if noise_size and color2:
        tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 1.0 / noise_size; nz.inputs['Detail'].default_value = 6.0
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
        cr.elements[0].position = 0.5 - noise_mix / 2; cr.elements[0].color = _lin(color)
        cr.elements[1].position = 0.5 + noise_mix / 2; cr.elements[1].color = _lin(color2)
        nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    else:
        bs.inputs['Base Color'].default_value = _lin(color)
    return m


def _box(bm, c, size, rot=None):
    """A box centred at c (x, y, z_bottom), size (sx, sy, sz), turned by matrix rot about its own base centre."""
    g = bmesh.ops.create_cube(bm, size=1.0)
    for v in g['verts']:
        p = Vector((v.co.x * size[0], v.co.y * size[1], (v.co.z + 0.5) * size[2]))
        if rot is not None:
            p = rot @ p
        v.co = Vector(c) + p
    return g


def _obj(bpy, kit, name, bm, mat, smooth=False):
    return kit.finish(bpy, name, bm, {'position': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': 1.0}, smooth=smooth, mat=mat)


def _tube(bm, pts, r, sides=8):
    """A tube along pts (Vectors), radius r."""
    rings = []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        a = t.orthogonal().normalized(); b = t.cross(a).normalized()
        rings.append([bm.verts.new(p + r * (math.cos(2 * math.pi * k / sides) * a + math.sin(2 * math.pi * k / sides) * b))
                      for k in range(sides)])
    for r0, r1 in zip(rings, rings[1:]):
        for k in range(sides):
            bm.faces.new((r0[k], r0[(k + 1) % sides], r1[(k + 1) % sides], r1[k]))


# --- the bridge -------------------------------------------------------------------------------------------------------
def bridge(bpy, name, p, kit):
    """The Golden Gate at real scale: towers 227 m above the water, the main span 1280 m, side spans 343 m, the roadway at
    67 m, main cables sagging 144 m, suspenders every 15.2 m, a stiffening truss under the deck. `north` and `south` are
    the towers' world (x, y); `water` the water's z; `color` the paint (International Orange)."""
    W = p.get('water', -110.0)
    N, S = Vector((*p['north'], 0)), Vector((*p['south'], 0))
    ax = (S - N); span = ax.length; ax.normalize()
    side = Vector((-ax.y, ax.x, 0))                              # across the deck
    R = Matrix(((ax.x, side.x, 0), (ax.y, side.y, 0), (0, 0, 1)))   # local (along, across, up) -> world

    def P(u, v, z):                                              # a point along the bridge (u from the north tower)
        return N + ax * u + side * v + Vector((0, 0, W + z))

    paint = _mat(bpy, 'gg-paint', p.get('color', '#B8442C'), rough=0.55, spec=0.35, noise_size=6.0, noise_mix=0.6,
                 color2=p.get('color2', '#A63D29'))
    road = _mat(bpy, 'gg-road', '#3A3A3A', rough=0.8)
    concrete = _mat(bpy, 'gg-concrete', '#9C978C', rough=0.85, noise_size=8.0, noise_mix=0.6, color2='#857F74')
    deck_z, half = 67.0, 13.7
    bm = bmesh.new()
    # the towers: two legs of stepped, fluted shafts, joined by portal struts above the deck and a strut below it
    tiers = [(0, 67, 11.0, 17.0), (67, 118, 10.0, 15.0), (118, 160, 9.0, 13.5), (160, 196, 8.0, 12.0), (196, 227, 7.0, 10.5)]
    for u in (0.0, span):
        for sgn in (-1, 1):
            for z0, z1, w, d in tiers:
                c = P(u, sgn * (half + 0.5), z0)
                _box(bm, c, (d, w, z1 - z0), R)
                # the flutes: two set-back ribs on the faces along the bridge, so the shaft reads cellular
                for f in (-1, 1):
                    _box(bm, P(u + f * (d / 2 + 0.35), sgn * (half + 0.5), z0), (0.7, w * 0.45, z1 - z0), R)
            _box(bm, P(u, sgn * (half + 0.5), 227.0), (8.0, 5.5, 3.0), R)          # the cap
        # the portals: deep struts with a stepped Art Deco face, at each tier's top
        for zc, hgt in ((112.0, 9.0), (154.0, 8.0), (190.0, 8.0), (221.0, 7.0)):
            _box(bm, P(u, 0.0, zc - hgt / 2), (6.5, 2 * half - 6.0, hgt), R)
            for k in range(-3, 4):                                                 # vertical ribs on the strut
                _box(bm, P(u - 3.45, k * 3.4, zc - hgt / 2 + 0.6), (0.5, 0.9, hgt - 1.2), R)
                _box(bm, P(u + 3.45, k * 3.4, zc - hgt / 2 + 0.6), (0.5, 0.9, hgt - 1.2), R)
        _box(bm, P(u, 0.0, 52.0), (6.0, 2 * half - 6.0, 6.0), R)                  # below the deck
        # the pier the tower stands on, at the water
        _box(bm, P(u, 0.0, -2.0), (40.0, 2 * half + 20.0, 12.0), R)
    obs = _obj(bpy, kit, f'{name}-towers', bm, paint)
    # the deck and its stiffening truss, from the north approach to the south
    u0, u1 = -p.get('north_approach', 600.0), span + p.get('south_approach', 700.0)
    bm = bmesh.new()
    L = u1 - u0
    _box(bm, P((u0 + u1) / 2, 0.0, deck_z - 7.6), (L, 2 * half + 1.0, 1.0), R)     # the lower chord plane
    for sgn in (-1, 1):
        _box(bm, P((u0 + u1) / 2, sgn * half, deck_z - 7.6), (L, 0.8, 0.9), R)      # bottom chord
        _box(bm, P((u0 + u1) / 2, sgn * half, deck_z - 0.6), (L, 0.8, 1.4), R)      # top chord
        _box(bm, P((u0 + u1) / 2, sgn * (half + 0.4), deck_z + 0.8), (L, 0.25, 1.1), R)   # the railing
        n = int(L / 7.6)
        for i in range(n + 1):
            u = u0 + i * 7.6
            _box(bm, P(u, sgn * half, deck_z - 7.6), (0.6, 0.6, 7.6), R)           # verticals
            # a diagonal (Warren): a thin box turned in the bridge's vertical plane
            if i < n:                                                          # the panel's two diagonals (Warren)
                th = math.atan2(3.8, 7.6)
                for base, t in ((u, th), (u + 7.6, -th)):
                    _box(bm, P(base, sgn * half, deck_z - 7.6), (0.45, 0.45, 8.5), R @ Matrix.Rotation(t, 3, 'Y'))
    obs += _obj(bpy, kit, f'{name}-truss', bm, paint)
    bm = bmesh.new()
    _box(bm, P((u0 + u1) / 2, 0.0, deck_z - 0.2), (L, 2 * half - 1.0, 0.6), R)    # the roadway
    obs += _obj(bpy, kit, f'{name}-road', bm, road)
    # the main cables (a parabola in the main span, a shallow sag on the side spans) and the suspenders
    top, low = 215.0, 71.0
    side_len = 343.0

    def cable_z(u):
        if 0 <= u <= span:
            return low + (top - low) * ((u - span / 2) / (span / 2)) ** 2
        s = -u if u < 0 else u - span                                      # 0 at the tower, side_len at the anchorage
        t = s / side_len
        return top + (78.0 - top) * t - 18.0 * math.sin(math.pi * t)
    bm = bmesh.new()
    us = [-side_len + i * 8.0 for i in range(int((span + 2 * side_len) / 8.0) + 1)]
    for sgn in (-1, 1):
        _tube(bm, [P(u, sgn * half, cable_z(u)) for u in us], p.get('cable_r', 0.55), 8)
    obs += _obj(bpy, kit, f'{name}-cables', bm, paint, smooth=True)
    bm = bmesh.new()
    sr = p.get('suspender_r', 0.22)
    u = -side_len + 15.2
    while u < span + side_len - 10:
        if abs(u) > 12 and abs(u - span) > 12:
            for sgn in (-1, 1):
                z0, z1 = deck_z + 0.5, cable_z(u)
                if z1 - z0 > 1.5:
                    g = bmesh.ops.create_cone(bm, cap_ends=False, segments=5, radius1=sr, radius2=sr, depth=z1 - z0)
                    bmesh.ops.translate(bm, vec=P(u, sgn * half, (z0 + z1) / 2), verts=g['verts'])
        u += 15.2
    obs += _obj(bpy, kit, f'{name}-suspenders', bm, paint)
    # the anchorages and the approach piers, concrete
    bm = bmesh.new()
    for u in (-side_len, span + side_len):
        _box(bm, P(u, 0.0, 0.0), (55.0, 2 * half + 14.0, 80.0), R)
    for u in [-side_len - 60.0 * k for k in range(1, 6)] + [span + side_len + 60.0 * k for k in range(1, 7)]:
        for sgn in (-1, 1):
            _box(bm, P(u, sgn * (half - 2), -5.0), (5.0, 5.0, deck_z - 2.6), R)
    obs += _obj(bpy, kit, f'{name}-concrete', bm, concrete)
    return obs


# --- the far shore and the city's hills --------------------------------------------------------------------------------
def _interp(table, b):
    if b <= table[0][0]:
        return table[0][1]
    for (b0, v0), (b1, v1) in zip(table, table[1:]):
        if b <= b1:
            t = (b - b0) / (b1 - b0)
            return v0 + (v1 - v0) * t
    return table[-1][1]


def land_h(p, x, y):
    """The far shore's height at (x, y): water short of the shore (`shore` [[bearing, distance], ...]), rising over a
    `coast` metres to the city's ground, with `peaks` [[bearing, distance, height above the water, radius]]."""
    W = p.get('water', -110.0)
    b, d = _polar(x, y)
    sh = _interp(p['shore'], b)
    if sh is None or sh > 1e8:
        return W - 5.0
    t = d - sh
    if t < 0:
        return W - 5.0 + max(-20.0, t * 0.2)
    base = p.get('ground', 40.0) * (1 - math.exp(-t / p.get('coast', 250.0)))
    for pb, pd, ph, pr in p.get('peaks', []):
        px, py = _at(pb, pd)
        base += ph * math.exp(-((x - px) ** 2 + (y - py) ** 2) / (pr * pr))
    base += 8.0 * noise.noise(Vector((x / 400.0, y / 400.0, 0.2))) + 3.0 * noise.noise(Vector((x / 90.0, y / 90.0, 1.3)))
    return W + max(0.0, base)


def land(bpy, name, p, kit):
    """The far shore and the city's hills: a grid fanned over bearings `bearings` [b0, b1] from `d_range` [near, far]."""
    b0, b1 = p.get('bearings', [-50.0, 50.0]); d0, d1 = p.get('d_range', [1200.0, 14000.0])
    cols = p.get('cols', 700); ratio = p.get('row_ratio', 0.003)
    rows = [d0]
    while rows[-1] < d1:
        rows.append(rows[-1] * (1 + ratio))
    bm = bmesh.new(); grid = []
    for d in rows:
        row = []
        for i in range(cols + 1):
            b = b0 + (b1 - b0) * i / cols
            x, y = _at(b, d)
            row.append(bm.verts.new((x, y, land_h(p, x, y))))
        grid.append(row)
    for j in range(len(grid) - 1):
        for i in range(cols):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    m = _mat(bpy, 'sf-land', '#5E6247', rough=0.95, noise_size=150.0, noise_mix=0.7, color2='#3B4430')
    return _obj(bpy, kit, name, bm, m, smooth=True)


def water(bpy, name, p, kit):
    W = p.get('water', -110.0)
    bm = bmesh.new()
    s = p.get('size', 30000.0)
    vs = [bm.verts.new((x, y, W)) for x, y in ((-s, 0), (s, 0), (s, s), (-s, s))]
    bm.faces.new(vs)
    m = _mat(bpy, 'sf-water', '#1C2A31', rough=0.08, spec=0.5)
    return _obj(bpy, kit, name, bm, m)


# --- the city ------------------------------------------------------------------------------------------------------
def city(bpy, name, p, kit):
    """Massed buildings on the far shore: low houses over `houses` [b0, b1, d0, d1, count], a downtown of towers
    (`downtown` [b, d, radius, count]), and two you can name (`salesforce`, `transamerica`: [b, d])."""
    rnd = random.Random(p.get('seed', 4))
    W = p.get('water', -110.0)
    pastels = ['#D9D3C7', '#E6E1D6', '#CFC6B6', '#BFC2C0', '#E3D9C6', '#D2CBBE']
    mats = [_mat(bpy, f'sf-house-{i}', c, rough=0.75) for i, c in enumerate(pastels)]
    glass = _mat(bpy, 'sf-tower', '#9AA3A8', rough=0.3, spec=0.6, noise_size=4.0, noise_mix=0.8, color2='#C9CDCB')
    lp = p['land']
    bms = [bmesh.new() for _ in mats]
    b0, b1, d0, d1, n = p['houses']
    made = 0; tries = 0
    while made < n and tries < n * 20:
        tries += 1
        b, d = rnd.uniform(b0, b1), d0 * (d1 / d0) ** rnd.random()
        x, y = _at(b, d)
        z = land_h(lp, x, y)
        if z <= W + 3.0:
            continue
        w, dd, h = rnd.uniform(9, 22), rnd.uniform(12, 30), rnd.uniform(7, 14)
        rot = Matrix.Rotation(math.radians(p.get('grid_deg', 10.0) + rnd.choice((0, 90))), 3, 'Z')
        _box(bms[made % len(bms)], (x, y, z - 2.0), (w, dd, h + 2.0), rot)
        made += 1
    obs = []
    for i, bm in enumerate(bms):
        obs += _obj(bpy, kit, f'{name}-houses-{i}', bm, mats[i])
    bm = bmesh.new()
    db, dd0, dr, dn = p['downtown']
    cx, cy = _at(db, dd0)
    for _ in range(dn):
        r = dr * math.sqrt(rnd.random()); a = rnd.uniform(0, 2 * math.pi)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        z = land_h(lp, x, y)
        if z <= W + 2.0:
            continue
        h = 30 + 170 * (1 - r / dr) ** 1.5 * rnd.random() ** 0.7
        w = rnd.uniform(22, 45)
        rot = Matrix.Rotation(math.radians(p.get('grid_deg', 10.0)), 3, 'Z')
        _box(bm, (x, y, z - 2.0), (w, rnd.uniform(22, 45), h), rot)
        if h > 90 and rnd.random() < 0.5:                                   # a setback crown
            _box(bm, (x, y, z - 2.0 + h), (w * 0.7, w * 0.7, rnd.uniform(8, 25)), rot)
    # Salesforce Tower: 326 m, a tapering square with rounded corners and a domed crown
    sx, sy = _at(*p['salesforce']); sz = land_h(lp, sx, sy)
    prof = [(28, 0), (26, 150), (23, 270), (20, 305), (14, 318), (0, 326)]
    ring = []
    for r, z in prof:
        ring.append([bm.verts.new((sx + r * math.copysign(abs(math.cos(t)) ** 0.6, math.cos(t)),
                                   sy + r * math.copysign(abs(math.sin(t)) ** 0.6, math.sin(t)), sz + z))
                     for t in [2 * math.pi * k / 24 for k in range(24)]])
    for r0, r1 in zip(ring, ring[1:]):
        for k in range(24):
            bm.faces.new((r0[k], r0[(k + 1) % 24], r1[(k + 1) % 24], r1[k]))
    # the Transamerica Pyramid: 260 m, a slender four-sided pyramid with its two wings
    tx, ty = _at(*p['transamerica']); tz = land_h(lp, tx, ty)
    base = [bm.verts.new((tx + dx, ty + dy, tz)) for dx, dy in ((-27, -27), (27, -27), (27, 27), (-27, 27))]
    apex = bm.verts.new((tx, ty, tz + 260.0))
    for k in range(4):
        bm.faces.new((base[k], base[(k + 1) % 4], apex))
    for dx in (-1, 1):
        _box(bm, (tx + dx * 22, ty, tz), (8, 14, 150), None)
    obs += _obj(bpy, kit, f'{name}-downtown', bm, glass)
    return obs


def sutro(bpy, name, p, kit):
    """Sutro Tower: a three-legged mast 298 m tall on Mount Sutro, its legs converging, crossbars at three levels."""
    x, y = _at(*p['at']); z = land_h(p['land'], x, y)
    red = _mat(bpy, 'sutro-red', '#B2372E', rough=0.6)
    bm = bmesh.new()
    legs = []
    for k in range(3):
        a = math.radians(90 + 120 * k)
        legs.append((Vector((x + 28 * math.cos(a), y + 28 * math.sin(a), z)), Vector((x + 6 * math.cos(a), y + 6 * math.sin(a), z + 298))))
    for a0, a1 in legs:
        _tube(bm, [a0, a1], 2.6, 6)
    for f in (0.42, 0.66, 0.9):
        pts = [a0.lerp(a1, f) for a0, a1 in legs]
        for i in range(3):
            _tube(bm, [pts[i], pts[(i + 1) % 3]], 2.0, 6)
            _box(bm, (pts[i].x, pts[i].y, pts[i].z - 2), (10, 10, 4), None)
    return _obj(bpy, kit, name, bm, red)


# --- the fog -----------------------------------------------------------------------------------------------------------
def fog(bpy, name, p, kit):
    """The fog in the Gate and over the west side: a sea of it at `top` metres (under the deck), heaving and billowed;
    a `wall` [bearing, distance, height, bearing_width, distance_width] that rolls over the city's west hills; higher
    over the ocean to the right (`ocean` [bearing_from, metres]); a thin `haze` above it all."""
    import materials as M
    x0, y0, z0, x1, y1, z1 = p['box']
    m = bpy.data.materials.new('fog-c'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    g = B._G(nt)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = M.hex_lin(p.get('color', '#FFFFFF'))
    vol.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.65)
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    x, y, z = sep.outputs[0], sep.outputs[1], sep.outputs[2]
    flat = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(x, flat.inputs[0]); nt.links.new(y, flat.inputs[1])
    fv = flat.outputs[0]
    top = g.add(p.get('top', -60.0), g.mul(g.sub(g.noise(fv, p.get('heave_size', 500.0), 3.0), 0.5), 2 * p.get('heave', 8.0)))
    for size, amp in p.get('billows', []):
        top = g.add(top, g.mul(g.sub(g.noise(fv, size, 2.0, 0.5), 0.5), 2 * amp))
    # bearing and distance
    bdeg = g.mul(g.op('ARCTAN2', x, y), 180.0 / math.pi)
    dist = g.op('SQRT', g.add(g.mul(x, x), g.mul(y, y)))
    if p.get('wall'):
        wb, wd, wh, sb, sd = p['wall']
        a = g.div(g.sub(bdeg, wb), sb); c = g.div(g.sub(dist, wd), sd)
        e = g.exp(g.mul(g.add(g.mul(a, a), g.mul(c, c)), -1.0))
        # the wall's crest frays: modulate it by a coarse noise
        e = g.mul(e, g.add(0.6, g.mul(g.noise(fv, p.get('wall_fray', 300.0), 3.0), 0.8)))
        top = g.add(top, g.mul(e, wh))
    if p.get('ocean'):
        ob, oh = p['ocean']
        top = g.add(top, g.mul(g.smooth(g.div(g.sub(bdeg, ob), 15.0)), oh))
    layer = g.smooth(g.div(g.sub(top, z), p.get('soft', 4.0)))
    b1 = g.noise(tc.outputs['Object'], p.get('billow_size', 30.0), 5.0, 0.6)
    b2 = g.noise(tc.outputs['Object'], p.get('billow_size', 30.0) * 5.0, 3.0, 0.5)
    billow = g.clamp01(g.mul(g.sub(g.add(g.mul(b1, 0.6), g.mul(b2, 0.4)), p.get('billow_cut', 0.25)), p.get('billow_gain', 2.6)))
    dens = g.mul(g.mul(layer, billow), p.get('density', 0.03))
    if p.get('haze', 0) > 0:
        dens = g.add(dens, g.mul(g.exp(g.mul(g.sub(z, z0), -1.0 / p.get('haze_height', 250.0))), p['haze']))
    nt.links.new(dens, vol.inputs['Density'])
    bm = bmesh.new()
    gm = bmesh.ops.create_cube(bm, size=1.0)
    for v in gm['verts']:
        v.co = Vector(((x0 + x1) / 2 + v.co.x * (x1 - x0), (y0 + y1) / 2 + v.co.y * (y1 - y0), (z0 + z1) / 2 + v.co.z * (z1 - z0)))
    return _obj(bpy, kit, name, bm, m)
