"""Planet EARF, round 36: the loft's shell made a designed place (spinoffs/barkhorn/planet/r36/r36_plan.py holds every
dimension; the lead's brief from the owner's note on round 34's set is in that file's docstring and in r36/README.md).

    {"kind": "kit", "shape": "ext", "module": "planet_r36", "fn": "room", "colourway": "green", ...}

Kept from the loft (planet_loft.py): the concrete, the fir deck and beams, the frosted screens, the shopfront and the
street. New here:
- a listening zone raised 200 behind the smoked partition, in one saturated colour (limewashed walls, wool carpet,
  velvet tub chairs), proofed in bottle green and in oxblood (`colourway`);
- the Ember pair on an altar: a niche in the back wall lined in end-grain blocks, on solid oak plinths, felt behind;
- a racetrack counter: a 70 mm zinc top with a rounded edge over a fluted dark-oak front, a brass foot rail, the
  turntables and a rotary mixer built in; behind it a quiet back bar (blackened-steel doors, one lit timber niche)
  under a floor-to-ceiling record wall with a frosted disc behind the DJ station, a now-playing ledge and an etched
  acrylic disc for the name;
- a built-in curved oak banquette, channel-tufted, with loose cushions, small round oak tables and chairs opposite;
- counter chairs: a low curved oak back with an upholstered pad, an upholstered seat, at 760;
- the owner's lamps as placeholders until the companions' kit pieces land: the Dome pendant low over the counter and a
  squat Sphere in a brass cup on every table, both tint-frost-tint (smoked resin, a frosted liner that glows, the lamp
  hidden from the camera, from transmission and from glossy rays, and the shells casting no shadow);
- fabric acoustic panels in brushed-steel frames with a ledge of record sleeves;
- the sink: a floating trough cast in Ember acrylic in an alcove of dark timber, lit from below through its depth;
- signs of life: a coat over a chair, a record out of its sleeve, glasses and a half-drunk coupe.
"""
import math, os, random, sys

import bmesh
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(ENGINE))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'r36'))
sys.path.insert(0, HERE)
if ENGINE not in sys.path:
    sys.path.insert(0, ENGINE)
import r36_plan as R                                                 # noqa: E402
import planet_loft as LK                                             # noqa: E402
import planet_den as D                                               # noqa: E402
import materials as MT                                               # noqa: E402

P = D.P                                                              # the den's plan module, patched while its builders run
lin, principled, emitter, Mesh, _cyl, _lathe = LK.lin, LK.principled, LK.emitter, LK.Mesh, LK._cyl, LK._lathe
_M = {}


# --- materials -----------------------------------------------------------------------------------------------------
def dark_oak(bpy, vertical=False, name='oak-dark'):
    """Dark oak, oiled: the walnut scan darkened and cooled toward fumed oak."""
    return D.walnut(bpy, vertical=vertical, coat=0.35, coat_rough=0.35, tint='#1A120C', mix=0.82, name='-' + name)


def zinc(bpy):
    """A zinc bar top: soft grey metal, its sheen worn unevenly by glasses and elbows."""
    if 'zinc' not in _M:
        _M['zinc'] = principled(bpy, 'zinc', '#8C8E8C', rough=0.34, metal=0.92, bump=(0.002, 0.5, 0.0003))
    return _M['zinc']


def brass(bpy):
    if 'brass-r36' not in _M:
        _M['brass-r36'] = principled(bpy, 'brass-r36', '#B08A52', rough=0.3, metal=1.0)
    return _M['brass-r36']


def brushed_steel(bpy):
    if 'steel-brushed' not in _M:
        _M['steel-brushed'] = principled(bpy, 'steel-brushed', '#9A9A98', rough=0.38, metal=1.0)
    return _M['steel-brushed']


def limewash(bpy, colour, name):
    """Limewash in the zone's colour: a soft, chalky, uneven matte."""
    if name not in _M:
        _M[name] = principled(bpy, name, colour, rough=0.93, bump=(0.004, 0.4, 0.0006))
    return _M[name]


def mohair(bpy, colour, name):
    """Mohair: the deep velvet, its sheen tinted with the pile (D.velvet's white sheen read chocolate as pale tan)."""
    return velvet_deep(bpy, colour, name)


def blackened_steel(bpy):
    if 'steel-black' not in _M:
        _M['steel-black'] = principled(bpy, 'steel-black', '#1E1C1A', rough=0.42, metal=0.85, bump=(0.003, 0.15, 0.0002))
    return _M['steel-black']


def leather(bpy, colour, name='leather-oxblood'):
    """Oxblood leather: a deep, slightly waxed hide with a fine grain."""
    if name not in _M:
        m = principled(bpy, name, colour, rough=0.48, bump=(0.0006, 0.25, 0.0002))
        LK.R._set(D._bsdf(m), 'Coat Weight', 0.15); LK.R._set(D._bsdf(m), 'Coat Roughness', 0.35)
        _M[name] = m
    return _M[name]


def velvet_deep(bpy, colour, name):
    """Velvet with its nap: a deep base, a soft sheen at grazing angles (the rim highlight), a fine pile bump."""
    if name not in _M:
        m = principled(bpy, name, colour, rough=0.85, bump=(0.0015, 0.3, 0.0002))
        b_ = D._bsdf(m); LK.R._set(b_, 'Sheen Weight', 1.0); LK.R._set(b_, 'Sheen Roughness', 0.3)
        LK.R._set(b_, 'Sheen Tint', tuple(min(1.0, c * 2.2) for c in lin(colour)[:3]) + (1.0,))
        LK.R._set(b_, 'Specular IOR Level', 0.15)
        _M[name] = m
    return _M[name]


def carpet(bpy, colour, name):
    """Wool loop carpet in the zone's colour: matte, a soft sheen, a fine loop bump; no stone mottle."""
    if name not in _M:
        m = principled(bpy, name, colour, rough=1.0, bump=(0.002, 0.5, 0.0004))
        b_ = D._bsdf(m); LK.R._set(b_, 'Sheen Weight', 0.5); LK.R._set(b_, 'Specular IOR Level', 0.1)
        # the sheen tinted with the wool, so the pile reads green (or oxblood), not grey (p2r: r35 g32 b31)
        LK.R._set(b_, 'Sheen Tint', tuple(min(1.0, c * 2.5) for c in lin(colour)[:3]) + (1.0,))
        _M[name] = m
    return _M[name]


def end_grain(bpy, name='oak-endgrain', lo='#1E140D', hi='#8A6242'):
    """End-grain oak: growth rings round random hearts (one per block, more or less), checks, tone varying block to
    block, a satin sheen."""
    if name in _M:
        return _M[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b_ = D._bsdf(m)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 16.0; vo.inputs['Randomness'].default_value = 1.0   # cells under a block
    nt.links.new(tc.outputs['Object'], vo.inputs['Vector'])
    ring = nt.nodes.new('ShaderNodeMath'); ring.operation = 'MULTIPLY'; ring.inputs[1].default_value = 260.0
    nt.links.new(vo.outputs['Distance'], ring.inputs[0])
    sn = nt.nodes.new('ShaderNodeMath'); sn.operation = 'SINE'; nt.links.new(ring.outputs[0], sn.inputs[0])
    tone = nt.nodes.new('ShaderNodeTexWhiteNoise'); tone.noise_dimensions = '3D'
    nt.links.new(vo.outputs['Position'], tone.inputs['Vector'])
    mix = nt.nodes.new('ShaderNodeMath'); mix.operation = 'MULTIPLY_ADD'
    nt.links.new(sn.outputs[0], mix.inputs[0]); mix.inputs[1].default_value = 0.18
    tm = nt.nodes.new('ShaderNodeMath'); tm.operation = 'MULTIPLY'; tm.inputs[1].default_value = 0.3   # p3: 0.8 read as camouflage across the blocks
    nt.links.new(tone.outputs['Value'], tm.inputs[0]); nt.links.new(tm.outputs[0], mix.inputs[2])
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = lin(lo)
    cr.color_ramp.elements[1].position = 0.9; cr.color_ramp.elements[1].color = lin(hi)
    nt.links.new(mix.outputs[0], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], b_.inputs['Base Color'])
    LK.R._set(b_, 'Roughness', 0.55); LK.R._set(b_, 'Coat Weight', 0.15); LK.R._set(b_, 'Coat Roughness', 0.4)
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.25; bp.inputs['Distance'].default_value = 0.0005
    nt.links.new(sn.outputs[0], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b_.inputs['Normal'])
    _M[name] = m
    return m


def resin(bpy, deep, name, radius=0.025, rough=0.04):
    """Cast acrylic (the engine's clear resin): clear at its surface, the tint deepening with the light's path."""
    if name not in _M:
        _M[name] = MT.make(bpy, name, 'clear_resin', {'deep': deep, 'radius': radius, 'roughness': rough})
    return _M[name]


def liner(bpy, glow, name='liner-frost'):
    """The frosted liner cast inside the tinted shell (tint, frost, tint): it glows by itself, warm ivory."""
    key = f'{name}-{glow}'
    if key not in _M:
        _M[key] = MT.make(bpy, key, 'frosted', {'color': '#F4F2EE', 'absorb': '#EFE6D8', 'roughness': 0.5,
                                                'radius': 0.02, 'clear': 0.1, 'glow': glow, 'glow_color': '#FF9A50'})
    return _M[key]


def _lamp(bpy, name, pos, watts, kelvin=2700, size=0.02):
    """A hidden lamp (Planet's rule since f7c99a4): it lights the room, never seen as a shape through anything."""
    import lights as LT
    d = bpy.data.lights.new(name, 'POINT')
    d.energy = watts; d.shadow_soft_size = size; d.specular_factor = 0.0
    LT.set_color(d, kelvin)
    ob = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(ob)
    ob.location = pos
    ob.visible_camera = False; ob.visible_transmission = False; ob.visible_glossy = False
    return ob


def _area(bpy, name, pos, rot, size, watts, colour='#FFFFFF', kelvin=None):
    import lights as LT
    d = bpy.data.lights.new(name, 'AREA'); d.size = size[0]; d.shape = 'RECTANGLE'; d.size_y = size[1]
    d.energy = watts
    if kelvin:
        LT.set_color(d, kelvin)
    else:
        d.color = lin(colour)[:3]
    ob = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(ob)
    ob.location = pos; ob.rotation_euler = rot
    ob.visible_camera = False; ob.visible_glossy = False
    return ob


def _noshadow(ob):
    ob.visible_shadow = False
    return ob


# --- geometry helpers ------------------------------------------------------------------------------------------------
def _prism(bm, pts, z0, z1):
    """A vertical prism over a closed plan polygon (counter-clockwise)."""
    b = [bm.verts.new((x, y, z0)) for x, y in pts]; t = [bm.verts.new((x, y, z1)) for x, y in pts]
    n = len(pts)
    bm.faces.new(b[::-1]).normal_update(); bm.faces.new(t).normal_update()
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([b[i], b[j], t[j], t[i]]).normal_update()


def stadium(x0, x1, y0, y1, d=0.0, seg=20):
    """A racetrack in plan: the rectangle x0..x1, y0..y1 with semicircular ends, grown by d; counter-clockwise."""
    r = (y1 - y0) / 2 + d; yc = (y0 + y1) / 2; ca, cb = x0 + (y1 - y0) / 2, x1 - (y1 - y0) / 2
    pts = []
    for i in range(seg + 1):                                          # the right end, from the front round to the back
        t = -math.pi / 2 + math.pi * i / seg
        pts.append((cb + r * math.cos(t), yc + r * math.sin(t)))
    for i in range(seg + 1):                                          # the left end, from the back round to the front
        t = math.pi / 2 + math.pi * i / seg
        pts.append((ca + r * math.cos(t), yc + r * math.sin(t)))
    return pts


def _rot(x, y, cx, cy, a):
    c, s = math.cos(a), math.sin(a)
    return cx + c * (x - cx) - s * (y - cy), cy + s * (x - cx) + c * (y - cy)


def _obox(bm, cx, cy, z0, w, d, h, a):
    """A box w (along the heading a) by d by h, centred on cx, cy."""
    pts = [_rot(cx + u, cy + v, cx, cy, a) for u, v in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2))]
    _prism(bm, pts, z0, z0 + h)


# --- 3 and 2: the zone ----------------------------------------------------------------------------------------------
def zone(bpy, kit, p, objs):
    """The listening zone: a dark-oak platform 200 high with a nosed step, wool carpet in the zone's colour, the side
    walls and the altar wall limewashed in it."""
    Z = R.ZONE; C = R.COLOURWAYS[p.get('colourway', 'green')]; W, L = R.W, R.L
    pl = Mesh('zone-platform'); pl.box(Z['x0'], 0.0, 0.0, L, W, Z['z'])
    objs.append(pl.object(bpy, dark_oak(bpy), bevel=0.012))
    cp = Mesh('zone-carpet'); cp.box(Z['x0'] + 0.03, 0.005, Z['z'] - 0.002, L - 0.005, W - 0.005, Z['z'] + 0.012)
    objs.append(cp.object(bpy, carpet(bpy, C['carpet'], 'carpet-' + p.get('colourway', 'green')), bevel=0.004))
    lw = Mesh('zone-limewash')
    holes = {'right': [], 'left': []}
    for nm, wall, a0, a1, z0, z1, img in R.SCREENS:
        if wall in holes and a1 > Z['x0']:
            holes[wall].append((a0, a1, z0, z1))
    LK._wall(lw, Z['x0'] + 0.10, R.ALTAR['x0'], Z['z'], R.CEIL, holes['right'], lambda a, b, za, zb: lw.box(a, 0.004, za, b, 0.012, zb))
    LK._wall(lw, Z['x0'] + 0.10, R.ALTAR['x0'], Z['z'], R.CEIL, holes['left'], lambda a, b, za, zb: lw.box(a, W - 0.012, za, b, W - 0.004, zb))
    objs.append(lw.object(bpy, limewash(bpy, C['wall'], 'limewash-' + p.get('colourway', 'green'))))
    # the cased opening: a fir header and jambs (the den's, its curtains gone; the smoked partition stands in it)
    X0 = P.LOUNGE_X0; hd = Mesh('opening')
    hd.box(X0 - 0.10, 0.0, P.HEADER_Z, X0 + 0.10, W, R.CEIL); hd.box(X0 - 0.10, 0.0, 0.0, X0 + 0.10, 0.18, P.HEADER_Z)
    hd.box(X0 - 0.10, W - 0.18, 0.0, X0 + 0.10, W, P.HEADER_Z)
    objs.append(hd.object(bpy, LK.fir(bpy, vertical=True), bevel=0.006))


# --- 1: the altar ---------------------------------------------------------------------------------------------------
def altar(bpy, kit, p, objs):
    """A niche across the back wall, its wall limewashed, its inside lined in end-grain blocks; the pair on solid
    dark-oak plinths; a felt panel behind each speaker; a dark-oak soffit."""
    A = R.ALTAR; Z = R.ZONE; W, L = R.W, R.L; C = R.COLOURWAYS[p.get('colourway', 'green')]
    aw = Mesh('altar-wall')
    aw.box(A['x0'], 0.0, Z['z'], L, A['y0'] - A['cheek'], R.CEIL)
    aw.box(A['x0'], A['y1'] + A['cheek'], Z['z'], L, W, R.CEIL)
    aw.box(A['x0'], A['y0'] - A['cheek'], A['z1'] + 0.06, L, A['y1'] + A['cheek'], R.CEIL)
    objs.append(aw.object(bpy, limewash(bpy, C['wall'], 'limewash-' + p.get('colourway', 'green'))))
    # the cheeks and the soffit in dark oak; the lining in end-grain blocks (each its own depth and turn)
    ch = Mesh('altar-cheeks')
    ch.box(A['x0'], A['y0'] - A['cheek'], Z['z'], L - 0.002, A['y0'], A['z1'] + 0.06)
    ch.box(A['x0'], A['y1'], Z['z'], L - 0.002, A['y1'] + A['cheek'], A['z1'] + 0.06)
    ch.box(A['x0'], A['y0'], A['z1'], L - 0.002, A['y1'], A['z1'] + 0.06)
    objs.append(ch.object(bpy, dark_oak(bpy, vertical=True), bevel=0.008))
    rnd = random.Random(36); B = A['block']
    # r37 listening p4 (both critics: a uniform tile grid): four tones dealt block by block, the joints tighter
    tones = (('#1E140D', '#8A6242'), ('#170F09', '#6E4A30'), ('#24180F', '#9A7050'), ('#1A110B', '#7A5638'))
    bls = [Mesh(f'altar-endgrain-{t}') for t in range(len(tones))]
    nz = int((A['z1'] - Z['z']) / B); ny = int((A['y1'] - A['y0']) / B)
    for i in range(ny):
        for k in range(nz):
            y0 = A['y0'] + i * B + 0.001; z0 = Z['z'] + k * B + 0.001
            dx = rnd.uniform(0.0, 0.012)
            bls[rnd.randrange(len(tones))].box(L - 0.075 - dx, y0, z0, L - 0.004, y0 + B - 0.0012, z0 + B - 0.0012)
    for t, (bm_, (lo, hi)) in enumerate(zip(bls, tones)):
        if bm_.bm.verts:
            objs.append(bm_.object(bpy, end_grain(bpy, f'oak-endgrain-{t}', lo, hi), bevel=0.002))
    fe = Mesh('altar-felt')
    for role, colour, x, y, z, rot in R.speakers():
        fe.box(L - 0.105, y - 0.55, Z['z'] + 0.25, L - 0.080, y + 0.55, Z['z'] + 2.05)
    objs.append(fe.object(bpy, velvet_deep(bpy, C['velvet'], 'velvet-' + p.get('colourway', 'green')), bevel=0.012))
    pl = Mesh('altar-plinths'); S = R.PAIR36
    for role, colour, x, y, z, rot in R.speakers():
        _obox(pl.bm, x, y, Z['z'], S['plinth_d'], S['plinth_w'], S['plinth'], math.radians(rot + 90))
    objs.append(pl.object(bpy, dark_oak(bpy, vertical=True), bevel=0.01))


# --- 4: the counter, the back bar, the record wall ---------------------------------------------------------------
def counter(bpy, kit, p, objs):
    C = R.COUNTER; zt = C['top_z']; zb = zt - C['top_t']
    core = Mesh('counter-core'); _prism(core.bm, stadium(C['x0'], C['x1'], C['y0'], C['y1'], -0.02), 0.08, zb)
    objs.append(core.object(bpy, principled(bpy, 'counter-core', '#1A1714', rough=0.8)))
    kick = Mesh('counter-kick'); _prism(kick.bm, stadium(C['x0'], C['x1'], C['y0'], C['y1'], -0.05), 0.0, 0.085)
    objs.append(kick.object(bpy, LK.steel(bpy)))
    top = Mesh('counter-zinc'); _prism(top.bm, stadium(C['x0'], C['x1'], C['y0'], C['y1'], C['over'], seg=28), zb, zt)
    objs.append(top.object(bpy, zinc(bpy), bevel=0.028, seg=6))
    # the flutes: half-round dark oak staves round the room side and the ends (the bartender's side is steel)
    fl = Mesh('counter-flutes'); r = C['flute'] / 2
    pts = stadium(C['x0'], C['x1'], C['y0'], C['y1'], -0.02 + r * 0.6, seg=60)
    acc = 0.0; last = None
    ring = pts + [pts[0]]
    for a, b in zip(ring, ring[1:]):
        seglen = math.dist(a, b); n = max(1, int(seglen / C['flute']))
        for k in range(n):
            x = a[0] + (b[0] - a[0]) * (k + 0.5) / n; y = a[1] + (b[1] - a[1]) * (k + 0.5) / n
            if y > (C['y0'] + C['y1']) / 2 + 0.05 and C['x0'] + 0.36 < x < C['x1'] - 0.36:
                continue                                              # the back run: the work side
            _cyl(fl.bm, x, y, 0.09, r, zb - 0.095, seg=10)
    objs.append(fl.object(bpy, dark_oak(bpy, vertical=True), smooth=True))
    back = Mesh('counter-back'); back.box(C['x0'] + 0.35, C['y1'] - 0.03, 0.08, C['x1'] - 0.35, C['y1'] - 0.005, zb)
    objs.append(back.object(bpy, LK.steel(bpy)))
    # the brass foot rail on brackets
    rl = Mesh('counter-rail'); rp = stadium(C['x0'], C['x1'], C['y0'], C['y1'], C['rail_off'], seg=24)
    front = [q for q in rp if q[1] < (C['y0'] + C['y1']) / 2 + 0.2]
    for a, b in zip(front, front[1:]):
        LK._rod(rl.bm, (a[0], a[1], C['rail_z']), (b[0], b[1], C['rail_z']), 0.019, 0.019, seg=12)
    for x in [C['x0'] + 0.6 + 0.9 * k for k in range(int((C['x1'] - C['x0'] - 1.0) / 0.9) + 1)]:
        LK._rod(rl.bm, (x, C['y0'] - C['rail_off'], C['rail_z']), (x, C['y0'] - 0.005, C['rail_z'] + 0.08), 0.008, 0.008)
    objs.append(rl.object(bpy, brass(bpy), smooth=True))
    # the DJ station built into the top's back half: two turntables and a rotary mixer
    dj = Mesh('dj-plinths'); pt = Mesh('dj-platters'); kn = Mesh('dj-knobs')
    yd = C['y1'] - 0.22
    earf = p.get('decks') == 'earf'                                   # round 37: EARF's players stand on the top
    for dx in (() if earf else (-0.42, 0.42)):
        x = R.DJ['x'] + dx
        dj.box(x - 0.21, yd - 0.17, zt, x + 0.21, yd + 0.17, zt + 0.06)
        _cyl(pt.bm, x - 0.03, yd, zt + 0.06, 0.15, 0.012, seg=48)
        LK._rod(kn.bm, (x + 0.15, yd + 0.12, zt + 0.075), (x + 0.07, yd - 0.05, zt + 0.075), 0.005, 0.004)
    dj.box(R.DJ['x'] - 0.15, yd - 0.17, zt, R.DJ['x'] + 0.15, yd + 0.17, zt + 0.08)
    for i in range(4):
        for j in range(3):
            _cyl(kn.bm, R.DJ['x'] - 0.09 + 0.06 * i, yd - 0.09 + 0.08 * j, zt + 0.08, 0.016, 0.02, seg=16)
    objs.append(dj.object(bpy, principled(bpy, 'dj-body', '#1B1A19', rough=0.45, metal=0.3), bevel=0.004))
    if not earf:
        objs.append(pt.object(bpy, principled(bpy, 'dj-platter', '#121212', rough=0.55), smooth=True))
    objs.append(kn.object(bpy, brushed_steel(bpy), smooth=True))
    # a record on each platter, a label at its centre
    vr = Mesh('dj-records'); lb = Mesh('dj-labels')
    for dx in (-0.42, 0.42):
        if earf:                                       # on the player's platter (R3 Float: its top at 101 mm; turned
            _cyl(vr.bm, R.DJ['x'] + dx + 0.04, yd, zt + 0.1012, 0.15, 0.002, seg=64)   # 180, its spindle 40 to +x)
            _cyl(lb.bm, R.DJ['x'] + dx + 0.04, yd, zt + 0.1033, 0.05, 0.0004, seg=32)
            continue
        _cyl(vr.bm, R.DJ['x'] + dx - 0.03, yd, zt + 0.072, 0.15, 0.002, seg=64)
        _cyl(lb.bm, R.DJ['x'] + dx - 0.03, yd, zt + 0.0741, 0.05, 0.0004, seg=32)
    objs.append(vr.object(bpy, principled(bpy, 'vinyl', '#0B0B0C', rough=0.25), smooth=True))
    objs.append(lb.object(bpy, principled(bpy, 'vinyl-label', '#C9B48A', rough=0.6), smooth=True))


def _clear(a, b, holes):
    """The parts of [a, b] outside the (h0, h1) holes."""
    out = [(a, b)]
    for h0, h1 in sorted(holes):
        nxt = []
        for s0, s1 in out:
            if h1 <= s0 or h0 >= s1:
                nxt.append((s0, s1)); continue
            if h0 > s0:
                nxt.append((s0, h0))
            if h1 < s1:
                nxt.append((h1, s1))
        out = nxt
    return [(s0, s1) for s0, s1 in out if s1 - s0 > 0.005]


def _spk_holes():
    """The bar pair's niches (round 37: R.SPK_NICHES), as x-ranges and their top, or none."""
    if not getattr(R, 'SPK_NICHES', None):
        return [], 0.0, 0.0
    bx = [R.niche_box(x) for x in R.SPK_NICHES]
    return [(b[0], b[1]) for b in bx], bx[0][5], bx[0][4]


def backbar(bpy, kit, p, objs):
    """A quiet back bar: blackened-steel doors under a worktop; one lit niche lined in timber; above it the record
    wall to the beams, the frosted disc set into it behind the DJ station, the now-playing ledge."""
    W = R.W; B = R.BACKBAR36; RW = R.RECORD_WALL
    holes, htop, hz0 = _spk_holes()                                   # round 37: the bar pair's niches cut through
    low = holes if hz0 < B['low'] else []                             # a niche on a ledge: the doors run beneath
    st = Mesh('backbar-doors'); n = int((RW['x1'] - RW['x0']) / B['doors'])
    for k in range(n):
        x0 = RW['x0'] + k * B['doors'] + 0.003
        for a0, a1 in _clear(x0, x0 + B['doors'] - 0.006, low):
            if a1 - a0 > 0.12:
                st.box(a0, B['y'], 0.10, a1, W - 0.02, B['low'] - 0.03)
    for a0, a1 in _clear(RW['x0'], RW['x1'], low):
        st.box(a0, B['y'] + 0.03, 0.0, a1, W - 0.02, 0.10)
    objs.append(st.object(bpy, LK.steel(bpy), bevel=0.002))
    wt = Mesh('backbar-top')
    for a0, a1 in _clear(RW['x0'] - 0.02, RW['x1'] + 0.02, low):
        wt.box(a0, B['y'] - 0.03, B['low'] - 0.03, a1, W - 0.005, B['low'])
    objs.append(wt.object(bpy, zinc(bpy), bevel=0.006))
    # the record wall: dark-oak uprights and shelves, the cells clear of the disc and of the lit niche
    nx0, nx1, nz0, nz1 = B['niche']
    shelf = Mesh('records-shelving'); sl = Mesh('records-sleeves'); fo = Mesh('records-faceout')
    rnd = random.Random(361)
    pal = ['#1A1A1A', '#141414', '#26262A', '#E6E0D2', '#D8D0BE', '#C9BFA8', '#9C9488', '#6E6A64', '#3A2E2A', '#8A6E4E',
           '#B8A27A', '#4A3A30', '#2E3440', '#5A4A3A', '#7A3A2A', '#3A4A3A', '#C8B890', '#1E1E22']
    cell = RW['cell']; ncol = int((RW['x1'] - RW['x0']) / cell); nrow = int((RW['z1'] - RW['z0']) / cell)
    yb = W - 0.02; yf = yb - RW['depth']
    def blocked(cx, cz):
        if math.hypot(cx - R.DISC['x'], cz - R.DISC['z']) < R.DISC['r'] + cell * 0.55:
            return True
        if cz < htop + cell * 0.5 and any(h0 - 0.01 < cx < h1 + 0.01 for h0, h1 in holes):
            return True
        return nx0 - cell * 0.5 < cx < nx1 + cell * 0.5 and cz < nz1 + cell * 0.5
    for i in range(ncol + 1):
        x = RW['x0'] + i * cell
        inside = any(h0 - 0.011 < x < h1 + 0.011 for h0, h1 in holes)
        shelf.box(x - 0.011, yf, max(RW['z0'], htop) if inside else RW['z0'], x + 0.011, yb, RW['z1'])
    for k in range(nrow + 1):
        z = RW['z0'] + k * cell
        for a0, a1 in (_clear(RW['x0'], RW['x0'] + ncol * cell, holes) if z - 0.022 < htop else
                       [(RW['x0'], RW['x0'] + ncol * cell)]):
            shelf.box(a0, yf, z - 0.022, a1, yb, z)
    shelf.box(RW['x0'] - 0.02, yf, RW['z1'], RW['x0'] + ncol * cell + 0.02, yb, RW['z1'] + 0.04)
    for i in range(ncol):
        for k in range(nrow):
            xa = RW['x0'] + i * cell + 0.013; xb = RW['x0'] + (i + 1) * cell - 0.013; z = RW['z0'] + k * cell
            cx, cz = (xa + xb) / 2, z + cell / 2
            if blocked(cx, cz):
                continue
            if rnd.random() < 0.08:                                   # a sleeve face out
                fo.box(xa + 0.01, yf + 0.04, z + 0.004, xb - 0.01, yf + 0.046, z + 0.318,
                       col=lin(rnd.choice(pal)))
            fill = rnd.choice([1.0, 1.0, 0.95, 0.85, 0.7, 0.55])
            s = xa + 0.004
            while s < xa + (xb - xa) * fill - 0.004:
                t = rnd.choice([0.003, 0.0032, 0.0035, 0.004, 0.0045, 0.006, 0.009]) * rnd.uniform(0.9, 1.1)
                if rnd.random() < 0.025:
                    s += rnd.uniform(0.015, 0.04); continue
                pull = rnd.uniform(0.03, 0.08) if rnd.random() < 0.035 else 0.0
                col = lin(rnd.choice(pal)) if rnd.random() < 0.8 else LK.R._mixhex(rnd.choice(pal), '#D8CFBC', rnd.random() * 0.6)
                h = 0.315 + rnd.uniform(-0.005, 0.002); dz = rnd.uniform(0.0, 0.003)
                sl.box(s, yf + 0.012 - pull, z + dz, s + t, yf + 0.33 - pull, z + h + dz, col=col)
                s += t + 0.0004
    objs.append(shelf.object(bpy, dark_oak(bpy, vertical=True), bevel=0.003))
    objs.append(sl.object(bpy, LK.R.colour_attr_mat(bpy, 'sleeve-card-r36', rough=0.6)))
    objs.append(fo.object(bpy, LK.R.colour_attr_mat(bpy, 'sleeve-face-r36', rough=0.5)))
    # the frosted disc behind the DJ station: thick acrylic, its glow the changing light (warm white to deep red)
    dc = Mesh('dj-disc'); _cyl(dc.bm, R.DISC['x'], W - 0.06, R.DISC['z'], R.DISC['r'], 0.035, seg=96, axis='y')
    col = p.get('disc_col', '#FF5A3A')
    objs.append(dc.object(bpy, LK.acrylic(bpy, 'frosted', 'disc-frost-' + col, glow=p.get('disc_glow', 0.8),
                                          glow_col=col), smooth=True))
    rim = Mesh('dj-disc-rim'); _cyl(rim.bm, R.DISC['x'], W - 0.035, R.DISC['z'], R.DISC['r'] + 0.03, 0.03, seg=96, axis='y')
    objs.append(rim.object(bpy, LK.steel(bpy), smooth=True))
    if p.get('disc_lamp', 0) > 0:
        _area(bpy, 'dj-disc-lamp', (R.DISC['x'], W - 0.12, R.DISC['z']), (math.radians(90), 0, 0), (0.8, 0.8),
              p['disc_lamp'], colour=col)
    # the lit niche: lined in timber, a hidden strip at its head, a few bottles
    ni = Mesh('backbar-niche')
    ni.box(nx0, W - 0.02 - 0.30, nz0 - 0.03, nx1, W - 0.005, nz0)
    ni.box(nx0, W - 0.02 - 0.30, nz1, nx1, W - 0.005, nz1 + 0.03)
    ni.box(nx0 - 0.03, W - 0.02 - 0.30, nz0 - 0.03, nx0, W - 0.005, nz1 + 0.03)
    ni.box(nx1, W - 0.02 - 0.30, nz0 - 0.03, nx1 + 0.03, W - 0.005, nz1 + 0.03)
    ni.box(nx0, W - 0.03, nz0, nx1, W - 0.005, nz1)
    objs.append(ni.object(bpy, D.walnut(bpy, vertical=True, name='-niche'), bevel=0.003))
    nl = Mesh('backbar-niche-strip'); nl.box(nx0 + 0.04, W - 0.30, nz1 - 0.012, nx1 - 0.04, W - 0.27, nz1 - 0.004)
    lamp = nl.object(bpy, emitter(bpy, 'niche-strip', '#FFB870', p.get('niche_strip', 4.0)))
    lamp.visible_camera = False; objs.append(lamp)
    bt = Mesh('niche-bottles'); rb = random.Random(7)
    for k in range(6):
        x = nx0 + 0.12 + k * 0.15; h = rb.uniform(0.24, 0.32); r = rb.uniform(0.035, 0.045)
        _lathe(bt.bm, [(0, 0), (r, 0), (r, h * 0.65), (r * 0.35, h * 0.82), (r * 0.3, h), (0, h)], seg=24, z0=nz0,
               cx=x, cy=W - 0.17)
    objs.append(bt.object(bpy, principled(bpy, 'bottle-amber', '#7A4A1E', rough=0.05, trans=1.0, ior=1.5), smooth=True))
    # the now-playing ledge: a steel ledge, a sleeve on it
    le = Mesh('ledge'); le.box(R.LEDGE['x0'], yf - 0.10, R.LEDGE['z'] - 0.02, R.LEDGE['x1'], yf, R.LEDGE['z'])
    objs.append(le.object(bpy, LK.steel(bpy), bevel=0.002))
    np_ = Mesh('now-playing'); xm = (R.LEDGE['x0'] + R.LEDGE['x1']) / 2
    np_.box(xm - 0.157, yf - 0.06, R.LEDGE['z'], xm + 0.157, yf - 0.054, R.LEDGE['z'] + 0.314)
    objs.append(np_.object(bpy, principled(bpy, 'now-playing-cover', '#D9CDB4', rough=0.55)))
    nd = Mesh('now-playing-art'); _cyl(nd.bm, xm, yf - 0.061, R.LEDGE['z'] + 0.157, 0.09, 0.001, seg=48, axis='y')
    objs.append(nd.object(bpy, principled(bpy, 'now-playing-ring', '#1C1C1C', rough=0.6), smooth=True))


def nameplate(bpy, kit, p, objs):
    """An etched acrylic disc by the door: thick frosted acrylic in a steel ring, EARF's wordmark etched into it."""
    N = R.NAMEPLATE; W = R.W
    dc = Mesh('nameplate'); _cyl(dc.bm, N['x'], N['y'] - 0.013, N['z'], N['r'], 0.025, seg=96, axis='y')
    objs.append(dc.object(bpy, LK.acrylic(bpy, 'frosted', 'nameplate-frost', glow=p.get('name_glow', 0.25),
                                          glow_col='#FFC890'), smooth=True))
    rg = Mesh('nameplate-ring'); _cyl(rg.bm, N['x'], N['y'] - 0.011, N['z'], N['r'] + 0.015, 0.02, seg=96, axis='y')
    objs.append(rg.object(bpy, LK.steel(bpy), smooth=True))
    try:
        from mathutils.geometry import tessellate_polygon
        sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn'))
        import marks as MK
        w = N['r'] * 1.25; sc = w / MK.WORDMARK_W; ye = N['y'] - 0.0265
        bm = bmesh.new()
        for loops_uv in D._wordmark_outlines():
            loops = [[Vector((N['x'] - w / 2 + u * sc, ye, N['z'] + 150 * sc - v * sc)) for u, v in lp] for lp in loops_uv]
            flat = [v for lp in loops for v in lp]
            for tri in tessellate_polygon(loops):
                bm.faces.new([bm.verts.new(flat[i]) for i in tri]).normal_update()
        me = bpy.data.meshes.new('nameplate-etch'); bm.to_mesh(me); bm.free()
        me.materials.append(LK.acrylic(bpy, 'frosted', 'nameplate-etch', glow=p.get('name_glow', 0.25) * 3, glow_col='#FFD8A8'))
        ob = bpy.data.objects.new('nameplate-etch', me); bpy.context.scene.collection.objects.link(ob); objs.append(ob)
    except Exception as e:                                            # the disc reads without the mark
        print('nameplate: no wordmark', e)


# --- 5: the seats ---------------------------------------------------------------------------------------------------
def _chair(stl, uph, br, x, y, face, seat_h, back=0.20):
    """The brief's counter (or dining) chair: four slim blackened-steel legs, splayed; a thick upholstered round seat in
    oxblood leather; a low curved upholstered back on two steel posts, wrapping the sitter (opposite `face`, degrees);
    on the counter chair a brass foot ring."""
    f = math.radians(face); sr = R.CHAIRS36['seat_r']
    _cyl(stl.bm, x, y, seat_h - 0.075, sr - 0.03, 0.012, seg=40)                       # the seat pan
    _cyl(uph.bm, x, y, seat_h - 0.065, sr, 0.055, seg=48)                              # the cushion
    _cyl(uph.bm, x, y, seat_h - 0.012, sr - 0.012, 0.012, seg=48)                      # its crown, eased
    for k in range(4):
        t = f + math.radians(45 + 90 * k)
        top = (x + 0.12 * math.cos(t), y + 0.12 * math.sin(t), seat_h - 0.07)
        foot = (x + 0.21 * math.cos(t), y + 0.21 * math.sin(t), 0.0)
        LK._rod(stl.bm, foot, top, 0.009, 0.011, seg=12)
    if seat_h > 0.6:                                                  # the brass foot ring
        zr = 0.30; rr = 0.21 - 0.09 * zr / (seat_h - 0.07)
        LK._arc(br.bm, x, y, rr - 0.008, rr + 0.008, 0.0, 2 * math.pi, zr - 0.008, zr + 0.008, seg=48)
    b = f + math.pi; zb = seat_h + 0.06
    for da in (-0.62, 0.62):                                          # two posts
        t = b + da
        LK._rod(stl.bm, (x + 0.15 * math.cos(t), y + 0.15 * math.sin(t), seat_h - 0.06),
                (x + 0.19 * math.cos(t), y + 0.19 * math.sin(t), zb + 0.02), 0.008, 0.008, seg=10)
    LK._arc(stl.bm, x, y, 0.200, 0.208, b - 1.15, b + 1.15, zb, zb + back)              # the back's steel shell
    LK._arc(uph.bm, x, y, 0.168, 0.200, b - 1.10, b + 1.10, zb + 0.008, zb + back - 0.004)  # its pad


def seats(bpy, kit, p, objs):
    stl = Mesh('chairs-steel'); uph = Mesh('chairs-leather'); br = Mesh('chairs-brass')
    C = R.COUNTER; n = R.NCHAIRS
    for i in range(n):
        x = C['x0'] + 0.55 + i * (C['x1'] - C['x0'] - 1.1) / (n - 1) + ((i * 7) % 5 - 2) * 0.02
        y = C['y0'] - 0.48 - (0.12 if i in (2, 5) else 0.0)
        _chair(stl, uph, br, x, y, 90.0 + ((i * 5) % 7 - 3) * 5.0, R.CHAIRS36['seat_h'], R.CHAIRS36['back'])
    for x in R.TABLES36:                                              # a chair opposite each banquette table
        _chair(stl, uph, br, x + 0.03, R.CHAIR_Y36, 270.0 + ((int(x * 10) % 5) - 2) * 4.0, 0.46, back=0.26)
    wx, wy = R.WINDOW_TABLE
    _chair(stl, uph, br, wx, wy - 0.62, 90.0, 0.46, back=0.26); _chair(stl, uph, br, wx, wy + 0.62, 270.0, 0.46, back=0.26)
    objs.append(stl.object(bpy, blackened_steel(bpy), smooth=True))
    objs.append(uph.object(bpy, leather(bpy, p.get('chair_leather', R.CHAIRS36['leather'])), smooth=True, bevel=0.012))
    objs.append(br.object(bpy, brass(bpy), smooth=True))


def banquette(bpy, kit, p, objs):
    """Built-in along the right-hand wall: a dark-oak plinth and frame with rounded ends, a channel-tufted back,
    loose seat and back cushions, an oak cap; small round oak tables on blackened-steel pedestals."""
    B = R.BANQ36; T = R.TABLE36
    base = Mesh('banq-base'); _prism(base.bm, [(B['x0'], 0.02), (B['x1'], 0.02)] + [
        (B['x1'] - 0.30 + 0.30 * math.cos(t), B['d'] - 0.30 + 0.30 * math.sin(t)) for t in
        [math.pi * (i / 10) / 2 for i in range(11)]] + [
        (B['x0'] + 0.30 + 0.30 * math.cos(t), B['d'] - 0.30 + 0.30 * math.sin(t)) for t in
        [math.pi / 2 + math.pi * (i / 10) / 2 for i in range(11)]], 0.0, 0.30)
    objs.append(base.object(bpy, dark_oak(bpy, vertical=True, name='oak-banq'), bevel=0.01))
    seat = Mesh('banq-seat'); n = int((B['x1'] - B['x0']) / 0.62)
    for k in range(n):
        a = B['x0'] + 0.03 + k * (B['x1'] - B['x0'] - 0.06) / n
        seat.box(a + 0.006, 0.16, 0.30, a + (B['x1'] - B['x0'] - 0.06) / n - 0.006, B['d'] - 0.02, B['seat'])
    objs.append(seat.object(bpy, mohair(bpy, p.get('banq_col', '#2B2420'), 'mohair-banq'), bevel=0.04, seg=4))
    back = Mesh('banq-back'); nch = int((B['x1'] - B['x0']) / 0.14)
    for k in range(nch):
        a = B['x0'] + k * (B['x1'] - B['x0']) / nch
        back.box(a + 0.004, 0.02, B['seat'] + 0.02, a + (B['x1'] - B['x0']) / nch - 0.004, 0.15, B['back'] - 0.04)
    objs.append(back.object(bpy, mohair(bpy, p.get('banq_col', '#2B2420'), 'mohair-banq'), bevel=0.03, seg=4))
    frame = Mesh('banq-frame')
    frame.box(B['x0'] - 0.06, 0.0, B['back'] - 0.04, B['x1'] + 0.06, 0.18, B['back'])            # the cap
    for x0 in (B['x0'] - 0.06, B['x1']):                                                      # the ends
        frame.box(x0, 0.0, 0.0, x0 + 0.06, 0.18, B['back'])
    objs.append(frame.object(bpy, dark_oak(bpy, name='oak-banq-frame'), bevel=0.012))
    cu = Mesh('banq-cushions'); rc = random.Random(3)
    for x in (3.85, 5.25, 6.55, 8.15, 9.55):
        cx = x + rc.uniform(-0.1, 0.1)
        _obox(cu.bm, cx, 0.24, B['seat'] - 0.01, 0.42, 0.13, 0.38, math.radians(rc.uniform(-8, 8)))
    objs.append(cu.object(bpy, mohair(bpy, B['cushion'], 'mohair-cushion'), bevel=0.05, seg=4))
    tp = Mesh('tables36'); lg = Mesh('tables36-bases')
    for x in R.TABLES36:
        _cyl(tp.bm, x, T['y'], T['h'] - 0.04, T['r'], 0.04, seg=64)
        _cyl(lg.bm, x, T['y'], 0.02, 0.03, T['h'] - 0.06, seg=20); _cyl(lg.bm, x, T['y'], 0.0, 0.22, 0.022, seg=48)
    wx, wy = R.WINDOW_TABLE
    _cyl(tp.bm, wx, wy, T['h'] - 0.04, 0.36, 0.04, seg=64)
    _cyl(lg.bm, wx, wy, 0.02, 0.03, T['h'] - 0.06, seg=20); _cyl(lg.bm, wx, wy, 0.0, 0.22, 0.022, seg=48)
    objs.append(tp.object(bpy, dark_oak(bpy, name='oak-tables'), smooth=True, bevel=0.008))
    objs.append(lg.object(bpy, LK.steel(bpy), smooth=True))


def tubs(bpy, kit, p, objs):
    """Low 1970s tub chairs in velvet, open toward the altar; small hexagonal dark-oak tables on steel stems."""
    T = R.TUB; z0 = R.ZONE['z']; C = R.COLOURWAYS[p.get('colourway', 'green')]
    sh = Mesh('tubs'); cu = Mesh('tub-cushions')
    ax, ay = R.PAIR36['x'], R.YC
    for x, y in R.TUBS:
        face = math.atan2(ay - y, ax - x)
        half = math.radians(T['open_deg']) / 2
        b0, b1 = face + half, face + 2 * math.pi - half                # the shell round the back, open at the face
        mid0, mid1 = face + math.radians(125), face + 2 * math.pi - math.radians(125)
        LK._arc(sh.bm, x, y, T['r'] - 0.10, T['r'], mid0, mid1, z0, z0 + T['h'], seg=24)
        LK._arc(sh.bm, x, y, T['r'] - 0.10, T['r'], b0, mid0, z0, z0 + T['arm'], seg=8)
        LK._arc(sh.bm, x, y, T['r'] - 0.10, T['r'], mid1, b1, z0, z0 + T['arm'], seg=8)
        _cyl(cu.bm, x, y, z0, T['r'] - 0.10, T['seat'], seg=40)
    vel = velvet_deep(bpy, C['velvet'], 'velvet-' + p.get('colourway', 'green'))
    objs.append(sh.object(bpy, vel, smooth=True, bevel=0.04, seg=4))
    objs.append(cu.object(bpy, vel, smooth=True, bevel=0.05, seg=4))
    tt = Mesh('tub-tables'); ts = Mesh('tub-table-stems'); TT = R.TUB_TABLE
    for x, y in R.TUB_TABLES:
        _cyl(tt.bm, x, y, z0 + TT['h'] - TT['top'], TT['r'], TT['top'], seg=6)
        _cyl(ts.bm, x, y, z0, 0.018, TT['h'] - TT['top'], seg=16); _cyl(ts.bm, x, y, z0, 0.15, 0.015, seg=6)
    objs.append(tt.object(bpy, dark_oak(bpy, name='oak-tub-tables'), bevel=0.006))
    objs.append(ts.object(bpy, LK.steel(bpy), smooth=True))


# --- 7: the lamps (placeholders for the companions' Dome and Sphere) -----------------------------------------------
def domes(bpy, kit, p, objs):
    """The Dome pendant, low over the counter: a smoked resin dome, a frosted liner within it and a thin tinted skin
    under the liner (tint, frost, tint), a brass cap and canopy, a black cord; the lamp hidden inside."""
    Dm = R.DOME; y = (R.COUNTER['y0'] + R.COUNTER['y1']) / 2
    shell = Mesh('dome-shells'); lin_ = Mesh('dome-liners'); skin = Mesh('dome-skins'); br = Mesh('dome-brass'); cd = Mesh('dome-cords')
    def prof(r, h, t, n=16):
        out = []
        for i in range(n + 1):
            a = math.pi / 2 * i / n
            out.append((r * math.cos(a), h * math.sin(a)))
        inner = [(max(0.0, x - t), max(0.0, z - t * 0.8)) for x, z in out[::-1]]
        return out + inner
    for x in R.DOMES:
        z = Dm['rim_z']
        _lathe(shell.bm, prof(Dm['r'], Dm['h'], Dm['t']), seg=64, z0=z, cx=x, cy=y)
        _lathe(lin_.bm, prof(Dm['r'] - 0.008, Dm['h'] - 0.008, 0.0025), seg=64, z0=z + 0.004, cx=x, cy=y)
        _lathe(skin.bm, prof(Dm['r'] - 0.0115, Dm['h'] - 0.0115, 0.003), seg=64, z0=z + 0.006, cx=x, cy=y)
        _cyl(br.bm, x, y, z + Dm['h'] - 0.004, 0.028, 0.03, seg=32)
        top = R.CEIL - (R.BEAM['d'] if any(abs(x - bx) < R.BEAM['w'] / 2 + 0.03 for bx in R.BEAMS_X) else 0.0)
        _cyl(br.bm, x, y, top - 0.025, 0.06, 0.025, seg=32)
        _cyl(cd.bm, x, y, z + Dm['h'] + 0.02, 0.0035, top - z - Dm['h'] - 0.045, seg=8)
        _lamp(bpy, f'dome-lamp-{x}', (x, y, z + 0.088), p.get('dome_w', 30.0), 2700)
    objs.append(_noshadow(shell.object(bpy, resin(bpy, p.get('lamp_deep', '#6E655C'), 'dome-resin'), smooth=True)))
    objs.append(_noshadow(lin_.object(bpy, liner(bpy, p.get('dome_glow', 0.6)), smooth=True)))
    objs.append(_noshadow(skin.object(bpy, resin(bpy, p.get('lamp_deep', '#6E655C'), 'dome-resin'), smooth=True)))
    objs.append(br.object(bpy, brass(bpy), smooth=True))
    objs.append(cd.object(bpy, principled(bpy, 'cord', '#151413', rough=0.7), smooth=True))


def spheres(bpy, kit, p, objs):
    """The squat Sphere on every table: a 160 smoked resin ball sitting low in a shallow brass cup, a frosted liner
    within it; the lamp hidden inside."""
    S = R.SPHERE
    ball = Mesh('sphere-balls'); inner = Mesh('sphere-liners'); cup = Mesh('sphere-cups')
    for x, y, zt in R.sphere_spots():
        cz = zt + S['cup_h'] + S['r'] * S['squash'] - 0.014
        for m, r in ((ball, S['r']), (inner, S['r'] - 0.009)):
            g = bmesh.ops.create_uvsphere(m.bm, u_segments=48, v_segments=24, radius=r)
            for v in g['verts']:
                v.co = Vector((x + v.co.x, y + v.co.y, cz + v.co.z * S['squash']))
        _lathe(cup.bm, [(0, 0), (S['cup_r'] * 0.7, 0), (S['cup_r'], S['cup_h'] * 0.6), (S['cup_r'] + 0.006, S['cup_h']),
                        (S['cup_r'] - 0.004, S['cup_h']), (S['cup_r'] * 0.6, 0.006), (0, 0.006)], seg=48, z0=zt, cx=x, cy=y)
        _lamp(bpy, f'sphere-lamp-{x:.2f}-{y:.2f}', (x, y, cz), p.get('sphere_w', 6.0), 2700, size=0.015)
    objs.append(_noshadow(ball.object(bpy, resin(bpy, p.get('lamp_deep', '#6E655C'), 'sphere-resin'), smooth=True)))
    objs.append(_noshadow(inner.object(bpy, liner(bpy, p.get('sphere_glow', 0.6), 'sphere-frost'), smooth=True)))
    objs.append(cup.object(bpy, brass(bpy), smooth=True))


# --- 8: acoustic panels -----------------------------------------------------------------------------------------------
def panels(bpy, kit, p, objs):
    C = R.COLOURWAYS[p.get('colourway', 'green')]
    fr = Mesh('panel-frames'); fa = Mesh('panel-fabric'); sv = Mesh('panel-sleeves'); rnd = random.Random(8)
    pal = ['#D8CFBC', '#1A1A1A', '#8A6E4E', '#C9BFA8', '#3A3A3E']
    for wall, a0, a1, z0, z1 in R.PANELS:
        fa.box(a0 + 0.02, 0.014, z0 + 0.02, a1 - 0.02, 0.07, z1 - 0.02)
        for (xa, xb, za, zb) in ((a0, a1, z0, z0 + 0.025), (a0, a1, z1 - 0.025, z1), (a0, a0 + 0.025, z0, z1), (a1 - 0.025, a1, z0, z1)):
            fr.box(xa, 0.012, za, xb, 0.08, zb)
        fr.box(a0 + 0.04, 0.08, z0 + 0.30, a1 - 0.04, 0.12, z0 + 0.32)                # the ledge
        fr.box(a0 + 0.04, 0.114, z0 + 0.32, a1 - 0.04, 0.12, z0 + 0.35)               # its lip
        x = a0 + 0.10
        while x < a1 - 0.45:
            w = 0.314
            sv.box(x, 0.085, z0 + 0.32, x + w, 0.09, z0 + 0.32 + w, col=lin(rnd.choice(pal)))
            x += w + rnd.uniform(0.06, 0.20)
    objs.append(fr.object(bpy, brushed_steel(bpy), bevel=0.002))
    objs.append(fa.object(bpy, kit.material(bpy, 'felt', C['felt']), bevel=0.01))
    objs.append(sv.object(bpy, LK.R.colour_attr_mat(bpy, 'panel-sleeves', rough=0.55)))


# --- 6: the sink ------------------------------------------------------------------------------------------------------
def sink(bpy, kit, p, objs):
    """An alcove of vertical dark-timber boards; a floating trough cast in Ember acrylic, its basin soft and rounded,
    lit from below so it glows through its depth; a brushed-steel spout from the wall."""
    A = R.ALCOVE; S = R.SINK
    boards = [Mesh(f'alcove-boards-{k}') for k in range(3)]; x = A['x0']; k = 0
    bk = Mesh('alcove-back'); bk.box(A['x0'], 0.001, 0.0, A['x1'], 0.003, A['z1'])
    while x < A['x1'] - 0.01:
        boards[(k * 2) % 3].box(x + 0.002, 0.004, 0.0, min(x + 0.116, A['x1']), A['depth'], A['z1'])
        x += 0.12; k += 1
    objs.append(bk.object(bpy, principled(bpy, 'alcove-shadow', '#0A0806', rough=0.9)))
    for k, (m, tint) in enumerate(zip(boards, ('#22180F', '#2B1F15', '#1B130D'))):
        objs.append(m.object(bpy, D.walnut(bpy, vertical=True, coat=0.25, coat_rough=0.45, tint=tint, mix=0.6,
                                           name=f'-alcove{k}'), bevel=0.003))
    hd = Mesh('alcove-head'); hd.box(A['x0'] - 0.02, 0.0, A['z1'], A['x1'] + 0.02, A['depth'] + 0.04, A['z1'] + 0.05)
    objs.append(hd.object(bpy, dark_oak(bpy, name='oak-alcove-head'), bevel=0.004))
    y0 = A['depth'] + S.get('gap', 0.01); z0 = S['top'] - S['t']
    blk = Mesh('sink-block'); blk.box(S['x'] - S['w'] / 2, y0, z0, S['x'] + S['w'] / 2, y0 + S['d'], S['top'])
    ob = blk.object(bpy, resin(bpy, p.get('sink_deep', '#C8262B'), 'sink-ember', radius=p.get('sink_radius', 0.12),
                               rough=0.03))
    # the basin: a flattened ellipsoid cut from the top, the cut and the block both eased
    me = bpy.data.meshes.new('sink-cut'); bmc = bmesh.new()
    g = bmesh.ops.create_uvsphere(bmc, u_segments=128, v_segments=64, radius=1.0)
    for fc in bmc.faces:                               # the basin smooth-shaded (sink-p2r, both critics: faceted)
        fc.smooth = True
    bx, by, bz = S['basin']
    for v in g['verts']:
        v.co = Vector((S['x'] + v.co.x * bx, y0 + S['d'] / 2 + v.co.y * by, S['top'] + 0.03 + v.co.z * bz))
    bmc.to_mesh(me); bmc.free()
    cut = bpy.data.objects.new('sink-cut', me); bpy.context.scene.collection.objects.link(cut)
    mod = ob.modifiers.new('basin', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = cut; mod.solver = 'EXACT'
    bev = ob.modifiers.new('ease', 'BEVEL'); bev.width = 0.012; bev.segments = 5; bev.limit_method = 'ANGLE'
    cut.hide_render = True; cut.hide_viewport = True
    objs.append(ob)
    # the light within (the lead, 2026-10-20: a glow that deepens with thickness, never an emissive slab): an emitting
    # volume filling the slab a hair inside its faces, cut by the same basin, so every path through the cast adds light
    # in proportion to its length; no surface of its own
    inn = Mesh('sink-glow'); e = 0.003
    inn.box(S['x'] - S['w'] / 2 + e, y0 + e, z0 + e, S['x'] + S['w'] / 2 - e, y0 + S['d'] - e, S['top'] - e)
    vm = bpy.data.materials.new('sink-glow-vol'); vm.use_nodes = True; nt = vm.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); vol = nt.nodes.new('ShaderNodeEmission')
    vol.inputs['Color'].default_value = lin(p.get('sink_glow_col', '#FF3A22'))
    vol.inputs['Strength'].default_value = p.get('sink_glow', 6.0)
    nt.links.new(vol.outputs['Emission'], out.inputs['Volume'])
    vo = inn.object(bpy, vm)
    m2 = vo.modifiers.new('basin', 'BOOLEAN'); m2.operation = 'DIFFERENCE'; m2.object = cut; m2.solver = 'EXACT'
    vo.visible_shadow = False
    objs.append(vo)
    _area(bpy, 'sink-uplight', (S['x'], y0 + S['d'] / 2, z0 - 0.03), (0, 0, 0), (S['w'] - 0.1, S['d'] - 0.1),
          p.get('sink_w', 0.0) or 0.0001, kelvin=2600)
    # the spout and its plate
    sp = Mesh('sink-spout')
    _cyl(sp.bm, S['x'], 0.03, S['top'] + 0.22, 0.035, 0.012, seg=32, axis='y')
    LK._rod(sp.bm, (S['x'], 0.035, S['top'] + 0.22), (S['x'], 0.035 + 0.20, S['top'] + 0.22), 0.011, 0.011, seg=16)
    LK._rod(sp.bm, (S['x'], 0.235, S['top'] + 0.225), (S['x'], 0.25, S['top'] + 0.17), 0.011, 0.010, seg=16)  # its nose, down
    LK._rod(sp.bm, (S['x'] + 0.10, 0.035, S['top'] + 0.22), (S['x'] + 0.10, 0.09, S['top'] + 0.22), 0.012, 0.012, seg=16)
    LK._rod(sp.bm, (S['x'] + 0.10, 0.09, S['top'] + 0.22), (S['x'] + 0.10, 0.09, S['top'] + 0.30), 0.005, 0.004, seg=10)
    objs.append(sp.object(bpy, brushed_steel(bpy), smooth=True))
    # a linen hand towel over a short brass rod on the boards, right of the slab (the slab's top is the basin)
    rx = S['x'] + S['w'] / 2 + 0.12; rz = S['top'] + 0.18
    rod = Mesh('sink-rod'); LK._rod(rod.bm, (rx - 0.09, 0.07, rz), (rx + 0.09, 0.07, rz), 0.006, 0.006, seg=12)
    LK._rod(rod.bm, (rx - 0.09, A['depth'], rz), (rx - 0.09, 0.07, rz), 0.005, 0.005, seg=10)
    LK._rod(rod.bm, (rx + 0.09, A['depth'], rz), (rx + 0.09, 0.07, rz), 0.005, 0.005, seg=10)
    objs.append(rod.object(bpy, brass(bpy), smooth=True))
    tw = Mesh('sink-towel'); tw.box(rx - 0.075, 0.064, rz - 0.30, rx + 0.075, 0.078, rz + 0.008)
    objs.append(tw.object(bpy, principled(bpy, 'linen-warm', '#CDBFA6', rough=0.95, bump=(0.0015, 0.5, 0.0004)), bevel=0.004, seg=3))


# --- signs of life -----------------------------------------------------------------------------------------------------
def life(bpy, kit, p, objs):
    """Glasses (a half-drunk coupe, rocks glasses), a record out of its sleeve on the counter, a coat over a chair."""
    glass = principled(bpy, 'tumbler-glass', '#FFFFFF', rough=0.01, trans=1.0, ior=1.5)
    pour = principled(bpy, 'pour-r36', '#B5601A', rough=0.0, trans=1.0, ior=1.36)
    rocks = [(0, 0), (0.041, 0), (0.0425, 0.09), (0.0385, 0.09), (0.037, 0.016), (0, 0.016)]
    coupe = [(0, 0), (0.038, 0), (0.038, 0.004), (0.006, 0.010), (0.0045, 0.100), (0.030, 0.113), (0.056, 0.140),
             (0.0535, 0.140), (0.028, 0.117), (0, 0.111)]
    C = R.COUNTER; zt = C['top_z']; yb = C['y0'] + 0.13
    spots = [(4.20, yb, zt, 'rocks', 0.03), (5.40, yb + 0.04, zt, 'coupe', 0.5), (8.30, yb, zt, 'rocks', 0.02),
             (9.40, yb + 0.03, zt, 'coupe', 0.8)]
    spots += [(x - 0.15, R.TABLE36['y'] + 0.12, R.TABLE36['h'], 'rocks', 0.025) for x in R.TABLES36]
    spots += [(x + 0.11, y - 0.11, R.ZONE['z'] + R.TUB_TABLE['h'], 'rocks', 0.03) for x, y in R.TUB_TABLES]
    wx, wy = R.WINDOW_TABLE
    spots += [(wx + 0.14, wy - 0.12, R.TABLE36['h'], 'coupe', 0.6), (wx - 0.10, wy + 0.14, R.TABLE36['h'], 'rocks', 0.02)]
    gl = Mesh('glasses-r36'); lq = Mesh('pours-r36')
    for x, y, z, kind, fill in spots:
        _lathe(gl.bm, rocks if kind == 'rocks' else coupe, seg=40, z0=z, cx=x, cy=y)
        if kind == 'rocks':
            _cyl(lq.bm, x, y, z + 0.0165, 0.0366, fill, seg=40)
        else:                                                         # a coupe a little over half drunk
            r = 0.050 * fill ** 0.5
            _lathe(lq.bm, [(0, 0), (r * 0.6, 0.0), (r, 0.022 * fill), (0, 0.022 * fill)], seg=40, z0=z + 0.113, cx=x, cy=y)
    objs.append(gl.object(bpy, glass, smooth=True))
    objs.append(lq.object(bpy, pour, smooth=True))
    # a record out of its sleeve, on the counter by the DJ station
    rx, ry = R.DJ['x'] - 1.05, C['y0'] + 0.28
    vr = Mesh('life-record'); _cyl(vr.bm, rx, ry, zt + 0.001, 0.15, 0.0018, seg=64)
    objs.append(vr.object(bpy, principled(bpy, 'vinyl', '#0B0B0C', rough=0.25), smooth=True))
    lb = Mesh('life-label'); _cyl(lb.bm, rx, ry, zt + 0.0029, 0.05, 0.0004, seg=32)
    objs.append(lb.object(bpy, principled(bpy, 'vinyl-label-red', '#8A2A22', rough=0.6), smooth=True))
    sl = Mesh('life-sleeve'); _obox(sl.bm, rx + 0.25, ry + 0.02, zt + 0.0005, 0.314, 0.314, 0.003, math.radians(12))
    objs.append(sl.object(bpy, principled(bpy, 'sleeve-life', '#D2C6AE', rough=0.6)))
    # a coat over the back of the third counter chair
    n = R.NCHAIRS; i = 2
    x = C['x0'] + 0.55 + i * (C['x1'] - C['x0'] - 1.1) / (n - 1) + ((i * 7) % 5 - 2) * 0.02
    y = C['y0'] - 0.48 - 0.12 - 0.20
    co = Mesh('life-coat'); zb = R.CHAIRS36['seat_h'] + 0.10 + 0.13
    co.box(x - 0.24, y - 0.03, zb - 0.62, x + 0.22, y + 0.02, zb + 0.01)
    co.box(x - 0.24, y - 0.03, zb - 0.01, x + 0.22, y + 0.10, zb + 0.035)
    objs.append(co.object(bpy, LK.wool(bpy, '#6A5440', 'wool-coat'), bevel=0.02, seg=3))


# --- the room --------------------------------------------------------------------------------------------------------
def room(bpy, name, p, kit):
    objs = []
    p = {**p, 'lounge_slats': False, 'cafe': False}
    LK.LP.SCREENS = R.SCREENS                                         # the lounge screen moved clear of the altar
    if p.get('screen_tint'):
        LK._SCREEN_TINT['tint'] = p['screen_tint']
    LK.shell(bpy, kit, p, objs)
    LK.screens(bpy, kit, p, objs)
    with LK._patched(**LK.patches(p)):
        D.shopfront(bpy, kit, p, objs)
        with LK._patched(plan={'candle_spots': R.candle_spots}):
            if p.get('props', True):
                D.candles(bpy, kit, p, objs)
        if p.get('street', True):
            D.street(bpy, kit, p, objs)
    LK.partition(bpy, kit, p, objs)
    zone(bpy, kit, p, objs)
    altar(bpy, kit, p, objs)
    counter(bpy, kit, p, objs)
    backbar(bpy, kit, p, objs)
    nameplate(bpy, kit, p, objs)
    seats(bpy, kit, p, objs)
    banquette(bpy, kit, p, objs)
    tubs(bpy, kit, p, objs)
    if p.get('placeholders'):                         # the owner's Dome and Orb are kit pieces now (earf_moon)
        domes(bpy, kit, p, objs)
        spheres(bpy, kit, p, objs)
    panels(bpy, kit, p, objs)
    sink(bpy, kit, p, objs)
    if p.get('props', True):
        life(bpy, kit, p, objs)
    return objs
