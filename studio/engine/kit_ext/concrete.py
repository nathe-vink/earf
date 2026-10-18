"""Board-formed concrete, wet paving and a river (barkhorn round 31, uplight31): kit `ext` pieces for a night set.

    {"kind": "kit", "shape": "ext", "module": "concrete", "fn": "wall", "position": [x, y, z], "size": [w, t, h], ...}

- wall: a block of board-formed concrete `size` [w, t, h] (x across, y thick, z up) standing on its base, centred on
  `position` in x and y. The boards' print is laid in world space, so blocks of one wall (piers, a cornice, recessed
  bays) read as one pour: boards `board_m` tall, each a shade of its own (`board_vary`), the grain of the timber pressed
  into the face (`grain`), a lip where two boards met (`joint`), the form ties' holes on a grid (`ties` [dx, dz] m, 0 to
  leave them out), slow stains and drips (`stain`), `color`, `roughness`. `bevel` eases the block's edges.
- paving: wet stone flags `size` [w, d] on the ground at `position`, flags `flag` [w, d] m, joints darker; `wet` (0 to 1)
  how much of it holds water (smooth, dark, mirroring), in puddles `puddle_m` across.
- on a wall or paving, `texture` (a Poly Haven texture id: concrete_layers_02 is board-formed) uses the photographed
  set instead, laid at its real size or `tex_scale` m a tile, `res`, `bump`, its repetition broken by a slow tone
  variation `vary` (0.25) `vary_m` across, form ties' holes on a grid `ties` [dx, dz] m, `tex_offset` [u, v, w] (in tiles) shifting this block's stretch of it; on paving, `wet` and `puddle_m` as above.
- water: a river's surface `size` [w, d] at `position` (its z the water line): near black, a mirror broken by slow
  ripples (`ripple_m` long across x, `ripple` their strength), so lights on the far bank draw down into long streaks.
"""
import math

import bmesh
from mathutils import Vector

_MATS = {}


def _hex(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1.0,)


class _G:
    """Node shorthands on one material's tree."""
    def __init__(self, nt):
        self.nt = nt

    def n(self, t, **kw):
        x = self.nt.nodes.new(t)
        for k, v in kw.items():
            setattr(x, k, v)
        return x

    def link(self, a, b):
        self.nt.links.new(a, b)

    def math(self, op, a, b=None, c=None):
        m = self.n('ShaderNodeMath', operation=op)
        for i, v in enumerate((a, b, c)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                m.inputs[i].default_value = v
            else:
                self.link(v, m.inputs[i])
        return m.outputs[0]

    def xyz(self):
        geo = self.n('ShaderNodeNewGeometry'); s = self.n('ShaderNodeSeparateXYZ')
        self.link(geo.outputs['Position'], s.inputs[0])
        return geo.outputs['Position'], s.outputs['X'], s.outputs['Y'], s.outputs['Z']

    def combine(self, x, y, z):
        c = self.n('ShaderNodeCombineXYZ')
        for i, v in enumerate((x, y, z)):
            if isinstance(v, (int, float)):
                c.inputs[i].default_value = v
            else:
                self.link(v, c.inputs[i])
        return c.outputs[0]

    def noise(self, vec, scale, detail=4.0, rough=0.55, distort=0.0, out='Fac'):
        t = self.n('ShaderNodeTexNoise'); t.inputs['Scale'].default_value = scale; t.inputs['Detail'].default_value = detail
        t.inputs['Roughness'].default_value = rough; t.inputs['Distortion'].default_value = distort
        self.link(vec, t.inputs['Vector'])
        return t.outputs[out]

    def white(self, vec):
        t = self.n('ShaderNodeTexWhiteNoise'); t.noise_dimensions = '3D'
        self.link(vec, t.inputs['Vector'])
        return t.outputs['Value']

    def ramp(self, f, a, b):
        """f mapped from [a, b] to [0, 1], clamped and smoothed."""
        m = self.n('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP')
        m.inputs['From Min'].default_value = a; m.inputs['From Max'].default_value = b
        self.link(f, m.inputs['Value'])
        return m.outputs['Result']

    def rgb(self, f):
        c = self.n('ShaderNodeCombineColor')
        for ch in ('Red', 'Green', 'Blue'):
            self.link(f, c.inputs[ch])
        return c.outputs[0]


def concrete(bpy, p):
    key = ('concrete',) + tuple((k, str(p.get(k))) for k in ('color', 'board_m', 'board_vary', 'grain', 'joint', 'ties', 'stain', 'roughness'))
    if key in _MATS:
        return _MATS[key]
    m = bpy.data.materials.new('concrete'); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']; g = _G(nt)
    bh = p.get('board_m', 0.15); vary = p.get('board_vary', 0.10); grain = p.get('grain', 1.0)
    joint = p.get('joint', 1.0); tx, tz = p.get('ties', [0.6, 0.6]) or [0, 0]; stain = p.get('stain', 1.0)
    pos, X, Y, Z = g.xyz()
    # the board a point is on, and where in it: band = floor(z / bh), f = fract(z / bh)
    zb = g.math('DIVIDE', Z, bh)
    band = g.math('FLOOR', zb)
    f = g.math('SUBTRACT', zb, band)
    # each board: a shade, and its plank's own grain shifted along x (boards were sawn from different trees)
    r1 = g.white(g.combine(band, 1.7, 0.0))
    r2 = g.white(g.combine(band, 5.3, 2.0))
    shade = g.math('ADD', 1.0 - vary, g.math('MULTIPLY', r1, 2 * vary))
    # the timber's grain: long noise along x, tight across the board, distorted so it wanders like real grain
    gx = g.math('ADD', g.math('MULTIPLY', X, 0.35), g.math('MULTIPLY', r2, 40.0))
    gvec = g.combine(gx, g.math('MULTIPLY', Y, 0.35), g.math('MULTIPLY', Z, 1.0 / (bh * 0.09)))
    gr = g.noise(gvec, 1.0, detail=6.0, rough=0.6, distort=2.5)
    knot = g.noise(g.combine(g.math('MULTIPLY', X, 1.2), Y, g.math('MULTIPLY', Z, 3.0)), 3.0, detail=2.0)
    grain_h = g.math('ADD', gr, g.math('MULTIPLY', g.ramp(knot, 0.62, 0.75), 0.4))
    # the joint: a thin ridge where the concrete squeezed between two boards, and a faint step from board to board
    near = g.math('MINIMUM', f, g.math('SUBTRACT', 1.0, f))
    ridge = g.math('SUBTRACT', 1.0, g.ramp(near, 0.0, 0.035))
    # the ties' holes: a cone pocket ~25 mm across on a grid offset half a board
    holes = None
    if tx > 0 and tz > 0:
        hx = g.math('SUBTRACT', g.math('FRACT', g.math('DIVIDE', X, tx)), 0.5)
        hz = g.math('SUBTRACT', g.math('FRACT', g.math('DIVIDE', g.math('ADD', Z, tz * 0.25), tz)), 0.5)
        d = g.math('SQRT', g.math('ADD', g.math('POWER', g.math('MULTIPLY', hx, tx), 2.0), g.math('POWER', g.math('MULTIPLY', hz, tz), 2.0)))
        holes = g.math('SUBTRACT', 1.0, g.ramp(d, 0.008, 0.016))
    # slow stains, and drips run down from the ties and the joints: vertical streaks
    blot = g.noise(pos, 0.45, detail=3.0)
    streak = g.noise(g.combine(g.math('MULTIPLY', X, 6.0), Y, g.math('MULTIPLY', Z, 0.25)), 1.0, detail=4.0)
    stainf = g.math('MULTIPLY', g.math('ADD', g.math('MULTIPLY', g.ramp(blot, 0.35, 0.7), 0.6), g.math('MULTIPLY', g.ramp(streak, 0.45, 0.75), 0.5)), stain)
    # colour: base x board shade x grain x stains x the ridge a touch lighter, the holes dark
    v = g.math('MULTIPLY', shade, g.math('ADD', 0.9, g.math('MULTIPLY', grain_h, 0.2 * grain)))
    v = g.math('MULTIPLY', v, g.math('SUBTRACT', 1.0, g.math('MULTIPLY', stainf, 0.22)))
    v = g.math('ADD', v, g.math('MULTIPLY', ridge, 0.06 * joint))
    if holes is not None:
        v = g.math('MULTIPLY', v, g.math('SUBTRACT', 1.0, g.math('MULTIPLY', holes, 0.6)))
    mix = g.n('ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mix.inputs['Factor'].default_value = 1.0
    ins = [x for x in mix.inputs if x.type == 'RGBA']; outs = [x for x in mix.outputs if x.type == 'RGBA']
    ins[0].default_value = _hex(p.get('color', '#A29E96'))
    g.link(g.rgb(v), ins[1]); g.link(outs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = p.get('roughness', 0.86)
    if 'Specular IOR Level' in b.inputs:
        b.inputs['Specular IOR Level'].default_value = 0.3
    # relief: the grain pressed in, the ridge proud, the holes sunk, fine pitting over all
    pits = g.noise(pos, 260.0, detail=2.0)
    h = g.math('ADD', g.math('MULTIPLY', grain_h, 0.6 * grain), g.math('MULTIPLY', ridge, 1.2 * joint))
    h = g.math('ADD', h, g.math('MULTIPLY', g.ramp(pits, 0.62, 0.72), -0.5))
    h = g.math('ADD', h, g.math('MULTIPLY', g.math('MULTIPLY', r1, 0.6), 1.0))        # boards stand a hair proud of each other
    if holes is not None:
        h = g.math('ADD', h, g.math('MULTIPLY', holes, -3.0))
    bn = g.n('ShaderNodeBump'); bn.inputs['Strength'].default_value = p.get('relief', 0.5); bn.inputs['Distance'].default_value = 0.0015
    g.link(h, bn.inputs['Height']); g.link(bn.outputs['Normal'], b.inputs['Normal'])
    _MATS[key] = m
    return m


def paving_mat(bpy, p):
    key = ('paving',) + tuple((k, str(p.get(k))) for k in ('color', 'flag', 'wet', 'puddle_m'))
    if key in _MATS:
        return _MATS[key]
    m = bpy.data.materials.new('paving'); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']; g = _G(nt)
    fw, fd = p.get('flag', [0.9, 0.6]); wet = p.get('wet', 0.6)
    pos, X, Y, Z = g.xyz()
    # flags laid in running bond
    row = g.math('FLOOR', g.math('DIVIDE', Y, fd))
    xo = g.math('ADD', g.math('DIVIDE', X, fw), g.math('MULTIPLY', g.math('MODULO', row, 2.0), 0.5))
    col = g.math('FLOOR', xo)
    fx = g.math('SUBTRACT', xo, col); fy = g.math('SUBTRACT', g.math('DIVIDE', Y, fd), row)
    edge = g.math('MINIMUM', g.math('MINIMUM', g.math('MULTIPLY', fx, fw), g.math('MULTIPLY', g.math('SUBTRACT', 1.0, fx), fw)),
                  g.math('MINIMUM', g.math('MULTIPLY', fy, fd), g.math('MULTIPLY', g.math('SUBTRACT', 1.0, fy), fd)))
    joint = g.math('SUBTRACT', 1.0, g.ramp(edge, 0.002, 0.007))
    rf = g.white(g.combine(col, row, 3.0))
    speck = g.noise(pos, 180.0, detail=2.0)
    v = g.math('MULTIPLY', g.math('ADD', 0.82, g.math('MULTIPLY', rf, 0.3)), g.math('ADD', 0.85, g.math('MULTIPLY', speck, 0.3)))
    # water: puddles where a slow noise is high, and in the joints
    pd = g.noise(pos, 1.0 / p.get('puddle_m', 1.2), detail=3.0)
    puddle = g.math('MAXIMUM', g.ramp(pd, 0.62 - 0.25 * wet, 0.66 - 0.25 * wet), g.math('MULTIPLY', joint, wet))
    damp = wet * 0.7
    v = g.math('MULTIPLY', v, g.math('SUBTRACT', 1.0, g.math('ADD', damp * 0.35, g.math('MULTIPLY', puddle, 0.25))))
    v = g.math('MULTIPLY', v, g.math('SUBTRACT', 1.0, g.math('MULTIPLY', joint, 0.35)))
    mix = g.n('ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mix.inputs['Factor'].default_value = 1.0
    ins = [x for x in mix.inputs if x.type == 'RGBA']; outs = [x for x in mix.outputs if x.type == 'RGBA']
    ins[0].default_value = _hex(p.get('color', '#5A5852'))
    g.link(g.rgb(v), ins[1]); g.link(outs[0], b.inputs['Base Color'])
    rough = g.math('SUBTRACT', 0.55 - 0.3 * wet, g.math('MULTIPLY', puddle, 0.5 - 0.3 * wet))
    g.link(g.math('MAXIMUM', rough, 0.02), b.inputs['Roughness'])
    if 'Specular IOR Level' in b.inputs:
        b.inputs['Specular IOR Level'].default_value = 0.5
    # relief everywhere but in the water
    h = g.math('MULTIPLY', g.math('ADD', g.math('MULTIPLY', speck, 0.6), g.math('MULTIPLY', joint, -2.0)), g.math('SUBTRACT', 1.0, puddle))
    bn = g.n('ShaderNodeBump'); bn.inputs['Strength'].default_value = 0.35; bn.inputs['Distance'].default_value = 0.002
    g.link(h, bn.inputs['Height']); g.link(bn.outputs['Normal'], b.inputs['Normal'])
    _MATS[key] = m
    return m


def water_mat(bpy, p):
    key = ('water',) + tuple((k, str(p.get(k))) for k in ('color', 'ripple', 'ripple_m'))
    if key in _MATS:
        return _MATS[key]
    m = bpy.data.materials.new('water'); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']; g = _G(nt)
    pos, X, Y, Z = g.xyz()
    b.inputs['Base Color'].default_value = _hex(p.get('color', '#06080A'))
    b.inputs['Roughness'].default_value = p.get('roughness', 0.03)
    b.inputs['IOR'].default_value = 1.33
    if 'Specular IOR Level' in b.inputs:
        b.inputs['Specular IOR Level'].default_value = 0.5
    L = p.get('ripple_m', 1.6)
    # ripples: long across x, short in y, so a light's reflection draws out into a vertical streak
    r1 = g.noise(g.combine(g.math('DIVIDE', X, L), g.math('DIVIDE', Y, L * 0.08), 0.0), 1.0, detail=5.0, rough=0.6, distort=0.4)
    r2 = g.noise(g.combine(g.math('DIVIDE', X, L * 0.3), g.math('DIVIDE', Y, L * 0.03), 7.0), 1.0, detail=3.0)
    h = g.math('ADD', r1, g.math('MULTIPLY', r2, 0.35))
    bn = g.n('ShaderNodeBump'); bn.inputs['Strength'].default_value = p.get('ripple', 0.25); bn.inputs['Distance'].default_value = 0.02
    g.link(h, bn.inputs['Height']); g.link(bn.outputs['Normal'], b.inputs['Normal'])
    _MATS[key] = m
    return m


def _photo(bpy, p, kind):
    """A photographed texture set (assets.py, Poly Haven) under this module's breakers of repetition: a slow world-space
    variation in tone and vertical streaks multiplied into its colour, so a 2 m tile laid across a 60 m wall does not
    repeat to the eye; on paving, `wet` puddles (dark, smooth, mirroring) and a damp darkening over all."""
    import assets
    key = ('photo', kind) + tuple((k, str(p.get(k))) for k in ('texture', 'res', 'tex_scale', 'tex_offset', 'bump', 'vary', 'vary_m', 'ties', 'wet', 'puddle_m', 'tint', 'tint_mix', 'rough_mul'))
    if key in _MATS:
        return _MATS[key]
    m = assets.pbr(bpy, p['texture'], p.get('res', '2k'), scale=p.get('tex_scale'), bump=p.get('bump', 1.0),
                   tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0), rough_mul=p.get('rough_mul', 1.0), name=f'{kind}-{p["texture"]}')
    nt = m.node_tree; g = _G(nt)
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    if p.get('tex_offset'):                              # this block's own stretch of the texture (no two blocks alike)
        mp = next(n for n in nt.nodes if n.type == 'MAPPING')
        ox, oy, oz = (list(p['tex_offset']) + [0, 0, 0])[:3]
        mp.inputs['Location'].default_value = (ox, oy, oz)
    pos, X, Y, Z = g.xyz()

    def into(sock_name, fn):
        sock = b.inputs[sock_name]
        src = sock.links[0].from_socket if sock.is_linked else None
        fn(src, sock)
    vary = p.get('vary', 0.25)
    blot = g.noise(pos, 1.0 / p.get('vary_m', 3.0), detail=3.0)
    streak = g.noise(g.combine(g.math('MULTIPLY', X, 3.0), Y, g.math('MULTIPLY', Z, 0.15)), 1.0, detail=4.0)
    tone = g.math('SUBTRACT', 1.0 + 0.5 * vary, g.math('ADD', g.math('MULTIPLY', g.ramp(blot, 0.3, 0.7), vary),
                                                      g.math('MULTIPLY', g.ramp(streak, 0.45, 0.75), 0.6 * vary)))
    holes = None
    tx, tz = p.get('ties') or (0, 0)
    if tx > 0 and tz > 0:                                # the form ties' holes, on their grid, sunk and dark
        hx = g.math('SUBTRACT', g.math('FRACT', g.math('DIVIDE', X, tx)), 0.5)
        hz = g.math('SUBTRACT', g.math('FRACT', g.math('DIVIDE', g.math('ADD', Z, tz * 0.25), tz)), 0.5)
        d = g.math('SQRT', g.math('ADD', g.math('POWER', g.math('MULTIPLY', hx, tx), 2.0), g.math('POWER', g.math('MULTIPLY', hz, tz), 2.0)))
        holes = g.math('SUBTRACT', 1.0, g.ramp(d, 0.009, 0.015))
        tone = g.math('MULTIPLY', tone, g.math('SUBTRACT', 1.0, g.math('MULTIPLY', holes, 0.55)))
    puddle = None
    if kind == 'paving' and p.get('wet', 0) > 0:
        wet = p['wet']
        pd = g.noise(pos, 1.0 / p.get('puddle_m', 1.2), detail=3.0)
        puddle = g.ramp(pd, 0.62 - 0.25 * wet, 0.67 - 0.25 * wet)
        tone = g.math('MULTIPLY', tone, g.math('SUBTRACT', 1.0 - 0.3 * wet, g.math('MULTIPLY', puddle, 0.2)))

    def colour(src, sock):
        mix = g.n('ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mix.inputs['Factor'].default_value = 1.0
        ins = [x for x in mix.inputs if x.type == 'RGBA']; outs = [x for x in mix.outputs if x.type == 'RGBA']
        if src is not None:
            g.link(src, ins[0])
        else:
            ins[0].default_value = sock.default_value
        g.link(g.rgb(tone), ins[1]); g.link(outs[0], sock)
    into('Base Color', colour)
    if puddle is not None:
        def rough(src, sock):
            base = src if src is not None else sock.default_value
            damp = g.math('MULTIPLY', base, 1.0 - 0.45 * p['wet']) if src is not None else base * (1.0 - 0.45 * p['wet'])
            r = g.math('ADD', g.math('MULTIPLY', damp, g.math('SUBTRACT', 1.0, puddle)), g.math('MULTIPLY', puddle, 0.03))
            g.link(r, sock)
        into('Roughness', rough)
        nsock = b.inputs['Normal']                       # water lies flat: the relief fades in the puddles
        if nsock.is_linked:
            nm = nsock.links[0].from_node
            if 'Strength' in nm.inputs:
                g.link(g.math('MULTIPLY', g.math('SUBTRACT', 1.0, puddle), p.get('bump', 1.0)), nm.inputs['Strength'])
    if holes is not None:                                # the holes' cones: a bump chained over the texture's normal
        nsock = b.inputs['Normal']
        bn = g.n('ShaderNodeBump'); bn.inputs['Strength'].default_value = 0.8; bn.inputs['Distance'].default_value = 0.004
        g.link(g.math('MULTIPLY', holes, -1.0), bn.inputs['Height'])
        if nsock.is_linked:
            g.link(nsock.links[0].from_socket, bn.inputs['Normal'])
        g.link(bn.outputs['Normal'], nsock)
    _MATS[key] = m
    return m


def _block(bm, w, t, h):
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector((v.co.x * w, v.co.y * t, (v.co.z + 0.5) * h))


def wall(bpy, name, p, kit):
    w, t, h = p.get('size', [6.0, 0.4, 5.0])
    bm = bmesh.new(); _block(bm, w, t, h)
    if p.get('bevel', 0) > 0:
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=p['bevel'], segments=2, affect='EDGES')
    return kit.finish(bpy, name, bm, p, smooth=False, mat=_photo(bpy, p, 'wall') if p.get('texture') else concrete(bpy, p))


def paving(bpy, name, p, kit):
    w, d = p.get('size', [10.0, 4.0])
    bm = bmesh.new(); _block(bm, w, d, p.get('thick', 0.1))
    bmesh.ops.translate(bm, vec=Vector((0, 0, -p.get('thick', 0.1))), verts=bm.verts[:])
    return kit.finish(bpy, name, bm, p, smooth=False, mat=_photo(bpy, p, 'paving') if p.get('texture') else paving_mat(bpy, p))


def water(bpy, name, p, kit):
    w, d = p.get('size', [40.0, 20.0])
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, 0.0)) for x, y in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2))]
    bm.faces.new(vs)
    return kit.finish(bpy, name, bm, p, smooth=False, mat=water_mat(bpy, p))
