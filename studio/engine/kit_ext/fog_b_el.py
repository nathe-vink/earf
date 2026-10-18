"""Fog (concept B, round 31b): San Francisco's fog on a Marin headland at dawn. The pieces the photographic kit has no
shape for: the land the headland falls away into and the hills across the water (`terrain`), and the fog itself, a
sea of it filling the valleys and pouring over a saddle in the hills (`fog`), a volume whose density is drawn by noise.

Both read one description of the hills, `hills` [[x, y, height, half-width along, half-width across, turn_deg], ...]
(metres; gaussian ridges), so the fog that pours over a saddle hugs the same ground the mesh is built on.

    {"kind": "kit", "shape": "ext", "module": "fog_b_el", "fn": "terrain", "hills": [...], ...}
    {"kind": "kit", "shape": "ext", "module": "fog_b_el", "fn": "fog", "hills": [...], ...}
"""
import math

import bmesh
from mathutils import Vector, noise


# --- the land --------------------------------------------------------------------------------------------------------
def _hills_h(hills, x, y):
    h = 0.0
    for hx, hy, hh, wa, wc, rot in hills:
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        dx, dy = x - hx, y - hy
        a, b = (dx * c + dy * s) / wa, (-dx * s + dy * c) / wc
        h += hh * math.exp(-(a * a + b * b))
    return h


def _headland_h(p, x, y):
    """The headland the speaker stands on: level ground round it, a brow at `brow` metres behind, then a steep fall
    toward the fog; it falls away to the sides beyond `wide`."""
    brow, drop, wide = p.get('brow', 9.0), p.get('drop', 90.0), p.get('wide', 45.0)
    t = max(0.0, y - brow)
    z = -drop * (1.0 - math.exp(-(t / p.get('steep', 28.0)) ** 1.6))
    u = max(0.0, abs(x) - wide)
    z -= drop * (1.0 - math.exp(-(u / 30.0) ** 1.6))
    return z


def _height(p, x, y):
    base = p.get('floor', -140.0)
    z = max(base, _headland_h(p, x, y)) if p.get('headland', True) else base
    hh = _hills_h(p.get('hills', []), x, y)
    if hh > 1.0 and p.get('gullies'):
        # ridges and gullies on the hills, deeper toward their tops
        amp, size = p['gullies']
        r = noise.ridged_multi_fractal(Vector((x / size, y / size, 0.5)), 0.9, 2.1, 5, 1.0, 2.0)
        hh += min(1.0, hh / 120.0) * amp * (r - 1.0)
    hz = base + hh
    z = max(z, hz)
    # broad and fine relief, scaled with the distance so the near brow stays gentle and the far hills are rugged
    d = math.hypot(x, y)
    amp = p.get('relief', 0.35) + p.get('relief_far', 0.012) * d
    z += amp * noise.noise(Vector((x / 37.0, y / 37.0, 0.3))) + 0.35 * amp * noise.noise(Vector((x / 9.0, y / 9.0, 1.7)))
    return z


def _land_material(bpy, p, kit):
    """Coastal hills seen from far: dry summer grass, dark coyote-brush scrub in the folds, bare rock on the steeps."""
    if p.get('material') == 'pbr':
        return kit.piece_material(bpy, p)
    m = bpy.data.materials.new('fog-land'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(bs.outputs['BSDF'], out.inputs['Surface'])
    tc = nt.nodes.new('ShaderNodeTexCoord')
    n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 1 / p.get('patch', 60.0)
    n1.inputs['Detail'].default_value = 6.0; nt.links.new(tc.outputs['Object'], n1.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    lin = lambda h: tuple(((int(h[i:i + 2], 16) / 255 + 0.055) / 1.055) ** 2.4 for i in (1, 3, 5)) + (1.0,)
    cr.elements[0].position = 0.42; cr.elements[0].color = lin(p.get('scrub', '#2E3324'))
    cr.elements[1].position = 0.56; cr.elements[1].color = lin(p.get('grass', '#8C7C56'))
    nt.links.new(n1.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = 0.95
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 1 / 1.5; n2.inputs['Detail'].default_value = 8
    nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
    bn = nt.nodes.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = 0.6; bn.inputs['Distance'].default_value = 0.4
    nt.links.new(n2.outputs['Fac'], bn.inputs['Height']); nt.links.new(bn.outputs['Normal'], bs.inputs['Normal'])
    return m


def terrain(bpy, name, p, kit):
    """The land: a grid fanned out from the camera's side (`x_spread` [left, right] metres of x per metre of y, so the
    cells stay small near and grow far), rows from `y_range` [near, far] spaced by `row_ratio`, `cols` across."""
    y0, y1 = p.get('y_range', [6.0, 5000.0])
    ratio = p.get('row_ratio', 0.004)
    sl, sr = p.get('x_spread', [0.9, 0.6])
    margin = p.get('x_margin', 30.0)
    cols = p.get('cols', 500)
    rows = [y0]
    while rows[-1] < y1:
        rows.append(rows[-1] + max(p.get('min_row', 0.25), rows[-1] * ratio))
    bm = bmesh.new()
    grid = []
    for y in rows:
        xl, xr = -margin - sl * y, margin + sr * y
        row = []
        for i in range(cols + 1):
            x = xl + (xr - xl) * i / cols
            row.append(bm.verts.new((x, y, _height(p, x, y))))
        grid.append(row)
    for j in range(len(grid) - 1):
        for i in range(cols):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    return kit.finish(bpy, name, bm, {**p, 'position': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': 1.0},
                      mat=_land_material(bpy, p, kit))


# --- the fog -----------------------------------------------------------------------------------------------------------
class _G:
    """A tiny expression builder for shader math: operands are sockets or numbers."""
    def __init__(self, nt):
        self.nt = nt

    def op(self, operation, a, b=None, c=None):
        n = self.nt.nodes.new('ShaderNodeMath'); n.operation = operation
        for i, v in enumerate((a, b, c)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                self.nt.links.new(v, n.inputs[i])
        return n.outputs[0]

    def add(self, a, b): return self.op('ADD', a, b)
    def sub(self, a, b): return self.op('SUBTRACT', a, b)
    def mul(self, a, b): return self.op('MULTIPLY', a, b)
    def div(self, a, b): return self.op('DIVIDE', a, b)
    def max(self, a, b): return self.op('MAXIMUM', a, b)
    def exp(self, a): return self.op('EXPONENT', a)
    def clamp01(self, a): return self.op('MINIMUM', self.op('MAXIMUM', a, 0.0), 1.0)

    def smooth(self, a):                       # smoothstep of a clamped 0..1
        t = self.clamp01(a)
        return self.mul(self.mul(t, t), self.sub(3.0, self.mul(t, 2.0)))

    def noise(self, vec, size, detail=4.0, rough=0.55, dims='3D'):
        n = self.nt.nodes.new('ShaderNodeTexNoise'); n.noise_dimensions = dims
        n.inputs['Scale'].default_value = 1.0 / size; n.inputs['Detail'].default_value = detail
        if 'Roughness' in n.inputs:
            n.inputs['Roughness'].default_value = rough
        self.nt.links.new(vec, n.inputs['Vector'])
        return n.outputs['Fac']


def _hills_nodes(g, x, y, hills):
    h = None
    for hx, hy, hh, wa, wc, rot in hills:
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        dx, dy = g.sub(x, hx), g.sub(y, hy)
        a = g.div(g.add(g.mul(dx, c), g.mul(dy, s)), wa)
        b = g.div(g.sub(g.mul(dy, c), g.mul(dx, s)), wc)
        e = g.mul(g.exp(g.mul(g.add(g.mul(a, a), g.mul(b, b)), -1.0)), hh)
        h = e if h is None else g.add(h, e)
    return h


def fog(bpy, name, p, kit):
    """A box of fog `box` [x0, y0, z0, x1, y1, z1]: a sea of it with its top at `top` metres, heaving by `heave` metres
    over `heave_size`, its surface soft over `soft` metres and billowed by noise `billow_size` across; where `pours`
    [[x, y, along, across, turn_deg, thickness], ...] lie over the `hills` it climbs them as a layer `thickness` thick
    (the fog pouring over a saddle); above it all a thin `haze` (per metre) for the distance. `density` per metre in the
    fog's body, `anisotropy` its forward scatter (a backlit fog glows)."""
    import materials as M
    x0, y0, z0, x1, y1, z1 = p.get('box', [-3000, -50, -160, 3000, 6000, 400])
    m = bpy.data.materials.new('fog-volume'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    g = _G(nt)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = M.hex_lin(p.get('color', '#FFFFFF'))
    vol.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.6)
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sep.inputs[0])
    x, y, z = sep.outputs[0], sep.outputs[1], sep.outputs[2]
    pos = tc.outputs['Object']
    flat = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(x, flat.inputs[0]); nt.links.new(y, flat.inputs[1])
    # the sea's top, heaving
    hv = p.get('heave', 12.0)
    top = g.add(p.get('top', -45.0), g.mul(g.sub(g.noise(flat.outputs[0], p.get('heave_size', 420.0), 3.0), 0.5), 2 * hv))
    top = g.add(top, g.mul(g.sub(g.noise(flat.outputs[0], p.get('heave_size', 420.0) / 6.0, 4.0), 0.5), 0.8 * hv))
    # billows: domes on the top, big and small
    for size, amp in p.get('billows', []):
        top = g.add(top, g.mul(g.sub(g.noise(flat.outputs[0], size, 2.0, 0.5), 0.5), 2 * amp))
    # the fog banks up against the headland: its top rises toward the origin by `bank` metres over `bank_size`
    if p.get('bank'):
        r = g.op('SQRT', g.add(g.mul(x, x), g.mul(y, y)))
        top = g.add(top, g.mul(g.exp(g.div(r, -p.get('bank_size', 250.0))), p['bank']))
    # the marine layer behind the hills stands higher: the top rises by `rise` [d0, d1, dz] with the distance
    if p.get('rise'):
        d0, d1, dz = p['rise']
        r = g.op('SQRT', g.add(g.mul(x, x), g.mul(y, y)))
        top = g.add(top, g.mul(g.smooth(g.div(g.sub(r, d0), d1 - d0)), dz))
    # the pours: a layer over the hills where a saddle lets it through
    hills = p.get('hills', [])
    if hills and p.get('pours'):
        gh = g.add(p.get('floor', -140.0), _hills_nodes(g, x, y, hills))
        mask = None
        for px, py, pa, pc, rot, th in p['pours']:
            c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            dx, dy = g.sub(x, px), g.sub(y, py)
            a = g.div(g.add(g.mul(dx, c), g.mul(dy, s)), pa)
            b = g.div(g.sub(g.mul(dy, c), g.mul(dx, s)), pc)
            e = g.mul(g.exp(g.mul(g.add(g.mul(a, a), g.mul(b, b)), -1.0)), th)
            mask = e if mask is None else g.max(mask, e)
        # streaked down the slope by a stretched noise
        st = g.noise(flat.outputs[0], p.get('streak_size', 40.0), 3.0)
        mask = g.mul(mask, g.add(0.55, g.mul(st, 0.9)))
        top = g.max(top, g.add(gh, mask))
    layer = g.smooth(g.div(g.sub(top, z), p.get('soft', 14.0)))
    b1 = g.noise(pos, p.get('billow_size', 28.0), 5.0, 0.6)
    b2 = g.noise(pos, p.get('billow_size', 28.0) * 5.0, 3.0, 0.5)
    billow = g.clamp01(g.mul(g.sub(g.add(g.mul(b1, 0.6), g.mul(b2, 0.4)), p.get('billow_cut', 0.32)), p.get('billow_gain', 2.6)))
    dens = g.mul(g.mul(layer, billow), p.get('density', 0.06))
    # the thin haze above, thinning with height
    hz = p.get('haze', 0.0)
    if hz > 0:
        hd = g.mul(g.exp(g.mul(g.sub(z, z0), -1.0 / p.get('haze_height', 160.0))), hz)
        dens = g.add(dens, hd)
    nt.links.new(dens, vol.inputs['Density'])
    bm = bmesh.new()
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector(((x0 + x1) / 2 + v.co.x * (x1 - x0), (y0 + y1) / 2 + v.co.y * (y1 - y0), (z0 + z1) / 2 + v.co.z * (z1 - z0)))
    obs = kit.finish(bpy, name, bm, {**p, 'position': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': 1.0}, smooth=False, mat=m)
    for o in obs:
        o.visible_shadow = True
    return obs


# --- gulls ---------------------------------------------------------------------------------------------------------------
def gulls(bpy, name, p, kit):
    """Gulls far off: a few soft wing shapes (`birds` [[x, y, z, span_m, turn_deg, flap 0..1], ...]), grey."""
    obs = []
    mat = kit.material(bpy, 'paper', p.get('color', '#5A5E63'), {'roughness': 0.8})
    for i, (bx, by, bz, span, turn, flap) in enumerate(p.get('birds', [])):
        bm = bmesh.new()
        h = span / 2
        lift = 0.18 * span * (flap - 0.5) * 2
        # a gull's wings, seen at a distance: two swept, slightly bent wings from a short body
        pts = [(-h, lift * 0.6 + 0.04 * span), (-h * 0.55, lift + 0.07 * span), (-0.06 * span, 0.0),
               (0.0, -0.02 * span), (0.06 * span, 0.0), (h * 0.55, lift + 0.07 * span), (h, lift * 0.6 + 0.04 * span),
               (h * 0.5, lift + 0.035 * span), (0.04 * span, -0.035 * span), (-0.04 * span, -0.035 * span),
               (-h * 0.5, lift + 0.035 * span)]
        kit._extrude(bm, pts, 0.02 * span, 0.0)
        obs += kit.finish(bpy, f'{name}-{i}', bm, {'position': [bx, by, bz], 'rotate': [0, 0, turn], 'scale': 1.0},
                          smooth=False, mat=mat)
    return obs
