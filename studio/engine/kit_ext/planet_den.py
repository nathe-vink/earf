"""Planet EARF, round 33 (the den): the room as one kit `ext` piece, built from the plan
(spinoffs/barkhorn/planet/den/den_plan.py), every dimension read from there.

    {"kind": "kit", "shape": "ext", "module": "planet_den", "fn": "room", ...}

The owner asked for a cozier, warmer, smaller room without the rainbow (2026-10-19). What it builds, in world metres
(the plan's frame; x into the room from the shopfront, y across it, z up):

- the shell: a worn oak floor, tobacco limewash plaster over a walnut wainscot, a dark plaster ceiling, old brick
  bare in the listening room;
- the shopfront: a panelled bulkhead, the display window with café curtains, a recessed half-glazed door with a
  mosaic floor, prism-glass transoms, EARF's wordmark in gold leaf, a heavy velvet curtain inside the door;
- the bar: a reeded walnut front on an aged-brass kick, a brass footrail, an oiled walnut top with an oxblood leather
  armrest; the back-bar in walnut, its shelves on brass brackets before an antique mirror, each lit warm from under
  its front edge, two walnut niches for the Smoke pair;
- the banquette: oxblood leather, channel-tufted, along the right wall, walnut two-tops on brass pedestals;
- the listening room: a cased opening with velvet curtains drawn back, a walnut slat ceiling over absorber, the
  record wall and its console, books floor to 2.4 m, the Ember pair's walnut plinths, a worn rug, low side tables;
- small things: three spun-brass pendants, shaded sconces, candles, glasses, menus;
- the street (`street`: true): a three-storey Edwardian over the shop, its neighbours, the sidewalk and the road.
"""
import math, os, random, sys

import bmesh
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'den'))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'room31'))
sys.path.insert(0, HERE)
import den_plan as P                                                 # noqa: E402
import planet_room as R                                              # noqa: E402  (materials and mesh helpers)
import pieces as R31                                                 # noqa: E402  (credenza, rug)

lin, principled, emitter, Mesh, _cyl, _lathe, thin_glass = R.lin, R.principled, R.emitter, R.Mesh, R._cyl, R._lathe, R.thin_glass
_M = R._M


def _pbr(bpy, tex, rot=None, **k):
    """A scanned material laid by box projection; `rot` (deg about x, y, z) turns the grain."""
    import assets
    key = f'den-{tex}-{rot}-{sorted(k.items())}'
    if key not in _M:
        m = assets.pbr(bpy, tex, k.pop('res', '2k'), name=key, **k)
        if rot:
            mp = next(n for n in m.node_tree.nodes if n.type == 'MAPPING')
            mp.inputs['Rotation'].default_value = tuple(math.radians(a) for a in rot)
        _M[key] = m
    return _M[key]


def _bsdf(m):
    return next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')


def walnut(bpy, vertical=False, coat=0.6, coat_rough=0.28, tint='#4A2E1C', mix=0.25, name=''):
    """Smoked walnut, oiled and waxed: the scan a little darker and warmer, a soft satin coat. `vertical` runs the grain
    up the faces (a door's stile, a flute)."""
    m = _pbr(bpy, 'smoked_walnut_veneer', rot=(0, 90, 0) if vertical else None, tint=tint, tint_mix=mix,
             scale=0.9, res='2k')
    key = f'walnut-coat-{vertical}-{coat}-{coat_rough}-{tint}-{mix}-{name}'
    if key not in _M:
        b = _bsdf(m); R._set(b, 'Coat Weight', coat); R._set(b, 'Coat Roughness', coat_rough)
        _M[key] = m
    return m


def brass(bpy, aged=True):
    """Brass: aged (a soft, warm, unlacquered patina, a mottled roughness) or bright (a lit edge)."""
    name = 'brass-aged' if aged else 'brass'
    if name in _M:
        return _M[name]
    m = principled(bpy, name, '#A07A45' if aged else '#C49A5A', rough=0.32 if aged else 0.18, metal=1.0)
    nt = m.node_tree; b = _bsdf(m)
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 18.0; nz.inputs['Detail'].default_value = 8.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['To Min'].default_value = 0.22 if aged else 0.12; mr.inputs['To Max'].default_value = 0.48 if aged else 0.24
    nt.links.new(nz.outputs['Fac'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], b.inputs['Roughness'])
    if aged:                                    # darker in the hollows of the patina
        cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = lin('#6E5230')
        cr.color_ramp.elements[1].color = lin('#B08A52')
        nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    return m


def leather(bpy, colour='#5A1E1A', name='leather-oxblood'):
    if name not in _M:
        m = _pbr(bpy, 'leather_red_02', tint=colour, tint_mix=0.65, scale=0.5, res='2k')
        b = _bsdf(m); R._set(b, 'Coat Weight', 0.25); R._set(b, 'Coat Roughness', 0.35); R._set(b, 'Sheen Weight', 0.15)
        _M[name] = m
    return _M[name]


def velvet(bpy, colour, name):
    if name not in _M:
        m = _pbr(bpy, 'velour_velvet', tint=colour, tint_mix=0.85, scale=0.25, res='2k')
        b = _bsdf(m); R._set(b, 'Sheen Weight', 0.9); R._set(b, 'Sheen Roughness', 0.35); R._set(b, 'Specular IOR Level', 0.2)
        _M[name] = m
    return _M[name]


def plaster(bpy, p, name='limewash', colour=None):
    """Limewash plaster: a warm ground mottled by the brush (two tones by a broad noise), a trowelled bump."""
    if name in _M:
        return _M[name]
    c = colour or p.get('plaster', '#6E4F37')
    m = principled(bpy, name, c, rough=0.88, spec=0.3)
    nt = m.node_tree; b = _bsdf(m)
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.6; nz.inputs['Detail'].default_value = 9.0; nz.inputs['Roughness'].default_value = 0.62
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); e = cr.color_ramp.elements
    e[0].position = 0.3; e[0].color = R._mixhex(c, '#000000', 0.22); e[1].position = 0.72; e[1].color = R._mixhex(c, '#FFF2DC', 0.12)
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    fn = nt.nodes.new('ShaderNodeTexNoise'); fn.inputs['Scale'].default_value = 60.0; fn.inputs['Detail'].default_value = 6.0
    nt.links.new(tc.outputs['Object'], fn.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.12; bp.inputs['Distance'].default_value = 0.002
    nt.links.new(fn.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    _M[name] = m
    return m


def candle_glass(bpy):
    return principled(bpy, 'votive-amber', '#C98A3E', rough=0.08, trans=0.9, ior=1.5)


# --- the shell ------------------------------------------------------------------------------------------------------
def shell(bpy, kit, p, objs):
    W, L, H, T = P.W, P.L, P.CEIL, P.WALL_T
    fl = Mesh('floor'); fl.box(0.0, 0.0, -0.1, L, W, 0.0)
    fm = _pbr(bpy, p.get('floor_tex', 'wood_floor_worn'), tint=p.get('floor_tint', '#3A2416'),
              tint_mix=p.get('floor_mix', 0.45), rot=(0, 0, 90), res='2k')
    b = _bsdf(fm); R._set(b, 'Coat Weight', p.get('floor_coat', 0.35)); R._set(b, 'Coat Roughness', 0.3)
    objs.append(fl.object(bpy, fm))
    # the walls' plaster: the right wall to the listening room, the left wall behind the bar, the front's piers
    pl = Mesh('plaster')
    pl.box(0.0, -T, 0.0, P.BOOKS['x0'], 0.0, H)                                # right wall (y = 0)
    pl.box(0.0, W, 0.0, P.LOUNGE_X0, W + T, H)                                 # left wall to the opening
    pl.box(L, -T, P.REC['z1'], L + T, W + T, H)                                # the back wall over the record wall
    objs.append(pl.object(bpy, plaster(bpy, p)))
    # the old brick, bare, on the listening room's left wall and its back wall's corners
    br = Mesh('brick')
    br.box(P.LOUNGE_X0, W, 0.0, L + T, W + T, H)
    br.box(L, -T, 0.0, L + T, P.REC['y0'], P.REC['z1']); br.box(L, P.REC['y1'], 0.0, L + T, W, P.REC['z1'])
    objs.append(br.object(bpy, _pbr(bpy, 'large_red_bricks', tint=p.get('brick_tint', '#4E3429'), tint_mix=p.get('brick_mix', 0.5),
                                    scale=p.get('brick_scale', 0.8), res='2k')))
    rb = Mesh('books-back'); rb.box(P.BOOKS['x0'], -T, 0.0, L, 0.0, H)
    objs.append(rb.object(bpy, principled(bpy, 'dark-paint', '#1E1712', rough=0.8)))
    # the ceiling: plaster, painted a dark warm brown, with a plain crown
    ce = Mesh('ceiling'); ce.box(-0.2, -T, H, L + T, W + T, H + 0.2)
    objs.append(ce.object(bpy, plaster(bpy, p, 'ceiling-plaster', p.get('ceiling', '#2E221A'))))
    cr = Mesh('crown')
    cr.box(0.0, 0.0, H - 0.09, P.LOUNGE_X0, 0.06, H); cr.box(0.0, W - 0.06, H - 0.09, P.LOUNGE_X0, W, H)
    objs.append(cr.object(bpy, principled(bpy, 'crown-paint', '#2A1F18', rough=0.6), bevel=0.01))
    # the wainscot: walnut panels between stiles, a cap rail and a skirting, on the plaster walls of the front room
    ws = Mesh('wainscot'); wsv = Mesh('wainscot-stiles'); cap = Mesh('wainscot-cap')
    for (xa, xb, side) in ((0.0, P.BOOKS['x0'], 0), (P.BAR_X1 + 0.2, P.LOUNGE_X0, 1), (0.0, P.BAR_X0 - 0.2, 1)):
        yf = 0.02 if side == 0 else W - 0.02; yb = 0.0 if side == 0 else W
        ws.box(xa, yb, 0.0, xb, yf, P.WAINSCOT)
        n = max(1, int((xb - xa) / 0.62)); pw = (xb - xa) / n
        for k in range(n + 1):
            x = xa + k * pw
            wsv.box(x - 0.035, yb, 0.0, x + 0.035, yf + (0.012 if side == 0 else -0.012), P.WAINSCOT)
        wsv.box(xa, yb, 0.0, xb, yf + (0.014 if side == 0 else -0.014), 0.14)       # skirting
        wsv.box(xa, yb, P.WAINSCOT - 0.10, xb, yf + (0.012 if side == 0 else -0.012), P.WAINSCOT - 0.03)
        cap.box(xa, yb, P.WAINSCOT - 0.03, xb, yf + (0.035 if side == 0 else -0.035), P.WAINSCOT)
    objs.append(ws.object(bpy, walnut(bpy, vertical=True)))
    objs.append(wsv.object(bpy, walnut(bpy, vertical=True), bevel=0.004))
    objs.append(cap.object(bpy, walnut(bpy), bevel=0.008))


# --- the shopfront ----------------------------------------------------------------------------------------------------
def shopfront(bpy, kit, p, objs):
    W, H = P.W, P.CEIL
    E, Dr, Wn, Tr = P.ENTRY, P.DOOR, P.WINDOW, P.TRANSOM
    paint = principled(bpy, 'storefront-paint', P.STOREFRONT_PAINT, rough=0.38, coat=0.4, coat_rough=0.2,
                       bump=(0.02, 0.04, 0.0005))
    fr = Mesh('storefront')
    x0, x1 = -0.16, 0.0                                                     # the front's depth
    fr.box(x0, -P.WALL_T, 0.0, x1, E['y0'], Tr['z0'])                          # the right pier
    fr.box(x0, Wn['y1'], 0.0, x1, W + P.WALL_T, Tr['z0'])                      # the left pier
    fr.box(x0, E['y1'], 0.0, x1, Wn['y0'], Tr['z0'])                           # between the entry and the window
    fr.box(x0, Wn['y0'], 0.0, x1, Wn['y1'], Wn['sill'])                        # the bulkhead
    fr.box(x0 - 0.05, Wn['y0'] - 0.03, Wn['sill'] - 0.04, x1, Wn['y1'] + 0.03, Wn['sill'])   # the sill
    fr.box(x0, Wn['y0'], Wn['head'], x1, Wn['y1'], Tr['z0'])                   # the head
    fr.box(x0 - 0.06, -P.WALL_T, Tr['z0'] - 0.04, x1, W + P.WALL_T, Tr['z0'] + 0.04)        # the transom bar
    for yy in [-P.WALL_T + (W + 2 * P.WALL_T - 0.06) * k / 6 for k in range(7)]:
        fr.box(x0, yy, Tr['z0'], x1, yy + 0.06, Tr['z1'])                     # the transom's mullions
    fr.box(x0, -P.WALL_T, Tr['z1'], x1, W + P.WALL_T, H + 0.3)                 # the fascia over it
    # the bulkhead's raised panels
    for k in range(4):
        a = Wn['y0'] + 0.08 + k * (Wn['y1'] - Wn['y0'] - 0.16) / 4
        fr.box(x0 - 0.02, a + 0.04, 0.10, x0, a + (Wn['y1'] - Wn['y0'] - 0.16) / 4 - 0.04, Wn['sill'] - 0.10)
    # the window's two mullions
    for yy in (Wn['y0'] + (Wn['y1'] - Wn['y0']) / 3, Wn['y0'] + 2 * (Wn['y1'] - Wn['y0']) / 3):
        fr.box(x0 + 0.04, yy - 0.025, Wn['sill'], x1 - 0.06, yy + 0.025, Wn['head'])
    # the vestibule: its side walls panelled, its back wall round the door, its soffit
    fr.box(0.0, E['y0'] - 0.08, 0.0, E['depth'], E['y0'], Tr['z0'])
    fr.box(0.0, E['y1'], 0.0, E['depth'], E['y1'] + 0.08, Tr['z0'])
    fr.box(E['depth'], E['y0'] - 0.08, 0.0, E['depth'] + 0.10, Dr['y0'], Tr['z0'])
    fr.box(E['depth'], Dr['y1'], 0.0, E['depth'] + 0.10, E['y1'] + 0.08, Tr['z0'])
    fr.box(E['depth'], Dr['y0'], Dr['h'], E['depth'] + 0.10, Dr['y1'], Tr['z0'])
    fr.box(0.0, E['y0'] - 0.08, Tr['z0'] - 0.06, E['depth'] + 0.10, E['y1'] + 0.08, Tr['z0'])
    objs.append(fr.object(bpy, paint, bevel=0.004))
    # the vestibule's floor: a small white hexagon mosaic with a black border (a brick-pattern stand-in, 25 mm)
    vf = Mesh('vestibule-floor'); vf.box(-0.16, E['y0'], -0.02, E['depth'], E['y1'], 0.002)
    if 'mosaic' not in _M:
        m = bpy.data.materials.new('mosaic'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
        tc = nt.nodes.new('ShaderNodeTexCoord'); bt = nt.nodes.new('ShaderNodeTexBrick')
        bt.inputs['Scale'].default_value = 40.0; bt.inputs['Mortar Size'].default_value = 0.012
        bt.inputs['Color1'].default_value = lin('#E8E2D6'); bt.inputs['Color2'].default_value = lin('#D9D2C4')
        bt.inputs['Mortar'].default_value = lin('#6A645C')
        nt.links.new(tc.outputs['Object'], bt.inputs['Vector']); nt.links.new(bt.outputs['Color'], b.inputs['Base Color'])
        R._set(b, 'Roughness', 0.3); _M['mosaic'] = m
    objs.append(vf.object(bpy, _M['mosaic']))
    # the glass: the display window, the vestibule's side lights, the transoms (prism glass, frosted), the door's light
    gl = Mesh('glass')
    gl.quad([(-0.09, Wn['y0'], Wn['sill']), (-0.09, Wn['y1'], Wn['sill']), (-0.09, Wn['y1'], Wn['head']),
             (-0.09, Wn['y0'], Wn['head'])])
    if not p.get('no_glass'):
        objs.append(gl.object(bpy, thin_glass(bpy, p.get('glass_gloss', 1.0))))
    tg = Mesh('transom-glass')
    tg.box(-0.10, -P.WALL_T, Tr['z0'] + 0.04, -0.09, W + P.WALL_T, Tr['z1'])
    objs.append(tg.object(bpy, principled(bpy, 'prism-glass', '#EFE8DA', rough=0.35, trans=1.0, ior=1.5)))
    # the door: half-glazed, walnut-stained, its bottom rail and panel, a brass pull and kick plate
    dr = Mesh('door'); dx = E['depth'] + 0.03
    dr.box(dx, Dr['y0'], 0.0, dx + 0.05, Dr['y1'], 1.00)
    dr.box(dx, Dr['y0'], 1.00, dx + 0.05, Dr['y0'] + 0.12, Dr['h'])
    dr.box(dx, Dr['y1'] - 0.12, 1.00, dx + 0.05, Dr['y1'], Dr['h'])
    dr.box(dx, Dr['y0'], Dr['h'] - 0.14, dx + 0.05, Dr['y1'], Dr['h'])
    objs.append(dr.object(bpy, paint, bevel=0.004))
    dg = Mesh('door-glass'); dg.quad([(dx + 0.025, Dr['y0'] + 0.12, 1.0), (dx + 0.025, Dr['y1'] - 0.12, 1.0),
                                      (dx + 0.025, Dr['y1'] - 0.12, Dr['h'] - 0.14), (dx + 0.025, Dr['y0'] + 0.12, Dr['h'] - 0.14)])
    if not p.get('no_glass'):
        objs.append(dg.object(bpy, thin_glass(bpy, p.get('glass_gloss', 1.0))))
    hw = Mesh('door-brass')
    hw.box(dx - 0.004, Dr['y0'] + 0.02, 0.0, dx, Dr['y1'] - 0.02, 0.22)
    _cyl(hw.bm, Dr['y1'] - 0.10, 1.05, dx - 0.07, 0.012, 0.07, seg=16, axis='x')
    hw.box(dx - 0.075, Dr['y1'] - 0.115, 0.85, dx - 0.06, Dr['y1'] - 0.085, 1.25)
    objs.append(hw.object(bpy, brass(bpy, aged=False)))
    # the café curtains: unbleached linen, gathered on a brass rod across the window's lower half
    if p.get('cafe', True):
        C = P.CAFE; cu = Mesh('cafe-curtain'); n = 160
        for k in range(n):
            ya = Wn['y0'] + 0.02 + (Wn['y1'] - Wn['y0'] - 0.04) * k / n
            yb = Wn['y0'] + 0.02 + (Wn['y1'] - Wn['y0'] - 0.04) * (k + 1) / n
            xa = 0.06 + 0.018 * math.sin(k * 1.9); xb = 0.06 + 0.018 * math.sin((k + 1) * 1.9)
            cu.quad([(xa, ya, C['z0']), (xb, yb, C['z0']), (xb, yb, C['z1']), (xa, ya, C['z1'])])
        if 'linen' not in _M:
            m = principled(bpy, 'linen', '#E6D8BE', rough=0.85, sss=0.0, sheen=0.4)
            R._set(_bsdf(m), 'Transmission Weight', 0.35)
            _M['linen'] = m
        objs.append(cu.object(bpy, _M['linen'], smooth=True))
        rod = Mesh('cafe-rod'); _cyl(rod.bm, 0.06, C['rod'], Wn['y0'], 0.008, Wn['y1'] - Wn['y0'], seg=12, axis='y')
        objs.append(rod.object(bpy, brass(bpy), smooth=True))
    # the heavy curtain inside the door: oxblood velvet on a ring rail, drawn to one side
    cv = Mesh('door-curtain'); n = 40; y0c, y1c = 0.04, 0.85; xc = E['depth'] + 0.35
    for k in range(n):
        ya = y0c + (y1c - y0c) * k / n; yb = y0c + (y1c - y0c) * (k + 1) / n
        xa = xc + 0.05 * math.sin(k * 1.4); xb = xc + 0.05 * math.sin((k + 1) * 1.4)
        cv.quad([(xa, ya, 0.01), (xb, yb, 0.01), (xb, yb, 2.75), (xa, ya, 2.75)])
    objs.append(cv.object(bpy, velvet(bpy, P.CURTAIN['colour'], 'velvet-oxblood'), smooth=True))
    rl = Mesh('door-rail'); _cyl(rl.bm, xc, 2.78, 0.0, 0.012, 1.85, seg=12, axis='y')
    objs.append(rl.object(bpy, brass(bpy), smooth=True))
    # EARF's wordmark in gold leaf on the display window, read from the street (+y is to the reader's left)
    if p.get('sign', True):
        from mathutils.geometry import tessellate_polygon
        sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn'))
        import marks as MK
        w = P.SIGN['w']; sc = w / MK.WORDMARK_W
        yc = (Wn['y0'] + Wn['y1']) / 2; z0 = P.SIGN['z'] + 300 * sc / 2; xg = -0.0915
        def circ(cx, cy, r):
            return [(cx + r * math.cos(t), cy + r * math.sin(t)) for t in (2 * math.pi * k / 72 for k in range(72))]
        bm = bmesh.new()
        for sh in MK.WORDMARK:
            holes = []
            if sh[0] == 'rect':
                a0, b0, a1, b1 = sh[1:5]; pts = [(a0, b0), (a1, b0), (a1, b1), (a0, b1)]
            elif sh[0] == 'circle':
                pts = circ(*sh[1:4])
            elif sh[0] == 'ring':
                pts, holes = circ(sh[1], sh[2], sh[3]), [circ(sh[1], sh[2], sh[4])]
            else:
                pts = list(sh[1:])
            loops = [[Vector((xg, yc + w / 2 - u * sc, z0 - v * sc)) for u, v in lp] for lp in [pts] + holes]
            for tri in tessellate_polygon(loops):
                flat = [v for lp in loops for v in lp]
                f = bm.faces.new([bm.verts.new(flat[i]) for i in tri]); f.normal_update()
        me = bpy.data.meshes.new('gold-leaf'); bm.to_mesh(me); bm.free()
        me.materials.append(principled(bpy, 'gold-leaf', '#D9A94E', rough=0.12, metal=1.0, emit='#E8B45A',
                                       strength=p.get('gold_glow', 0.25)))
        ob = bpy.data.objects.new('gold-leaf', me); bpy.context.scene.collection.objects.link(ob); objs.append(ob)


# --- the bar ------------------------------------------------------------------------------------------------------
def bar(bpy, kit, p, objs):
    x0, x1, yF, zt = P.BAR_X0, P.BAR_X1, P.BAR_FRONT, P.BAR_TOP_Z
    yB = yF + P.BAR_DEPTH
    body = Mesh('bar-body'); body.box(x0, yF + 0.02, 0.0, x1, yB, zt)
    body.box(x0 - 0.04, yF - 0.01, 0.0, x0, yB, zt); body.box(x1, yF - 0.01, 0.0, x1 + 0.04, yB, zt)
    objs.append(body.object(bpy, walnut(bpy, vertical=True), bevel=0.003))
    # the reeding: half-round walnut flutes, floor (over the kick) to the top
    fl = Mesh('bar-flutes'); r = P.FLUTE / 2; n = int((x1 - x0) / P.FLUTE)
    k0 = P.KICK['h']; seg = 8
    for i in range(n):
        cx = x0 + r + i * P.FLUTE
        ring_b, ring_t = [], []
        for j in range(seg + 1):
            a = math.pi * j / seg
            yy = yF + 0.02 - r * math.sin(a) * 0.9; xx = cx - r * math.cos(a)
            ring_b.append(fl.bm.verts.new((xx, yy, k0))); ring_t.append(fl.bm.verts.new((xx, yy, zt - 0.03)))
        for j in range(seg):
            f = fl.bm.faces.new([ring_b[j], ring_b[j + 1], ring_t[j + 1], ring_t[j]]); f.normal_update()
    objs.append(fl.object(bpy, walnut(bpy, vertical=True), smooth=True))
    rail = Mesh('bar-rail'); rail.box(x0, yF - 0.004, zt - 0.03, x1, yF + 0.02, zt)          # a plain rail under the top
    objs.append(rail.object(bpy, walnut(bpy), bevel=0.004))
    kick = Mesh('bar-kick'); kick.box(x0, yF + P.KICK['set'] - 0.04, 0.0, x1, yF + 0.02, k0)
    objs.append(kick.object(bpy, brass(bpy), bevel=0.002))
    top = Mesh('bar-top'); top.box(x0 - 0.08, yF - P.TOP_OVER, zt, x1 + 0.08, yB + 0.03, zt + P.TOP_T)
    objs.append(top.object(bpy, walnut(bpy, coat=0.8, coat_rough=0.18), bevel=0.006))
    # the armrest: oxblood leather rolled along the top's front edge
    ar = Mesh('bar-armrest'); A = P.ARMREST
    ar.box(x0 - 0.08, yF - P.TOP_OVER - 0.012, zt + P.TOP_T - 0.01, x1 + 0.08, yF - P.TOP_OVER + A['d'], zt + P.TOP_T + A['h'])
    objs.append(ar.object(bpy, leather(bpy), bevel=0.026, seg=5))
    # the footrail: 50 mm aged brass on brackets
    fr = Mesh('footrail'); fy = yF - P.FOOTRAIL['off']; fz = P.FOOTRAIL['z']
    _cyl(fr.bm, fy, fz, x0 + 0.1, P.FOOTRAIL['d'] / 2, x1 - x0 - 0.2, seg=24, axis='x')
    for k in range(8):
        bx = x0 + 0.15 + k * (x1 - x0 - 0.3) / 7
        _cyl(fr.bm, bx, fy, fz - 0.006, 0.009, P.FOOTRAIL['off'] + 0.02, seg=10, axis='y')
    objs.append(fr.object(bpy, brass(bpy), smooth=True))
    # the working side: a dark counter and wells (seen only from behind the bar)
    wk = Mesh('bar-working'); wk.box(x0, yB - 0.05, 0.0, x1, yB, 0.85)
    objs.append(wk.object(bpy, principled(bpy, 'steel-dark', '#2A2724', rough=0.4, metal=0.8)))


def antique_mirror(bpy):
    if 'antique-mirror' in _M:
        return _M['antique-mirror']
    m = principled(bpy, 'antique-mirror', '#B8A88C', rough=0.06, metal=1.0)
    nt = m.node_tree; b = _bsdf(m)
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 3.5; nz.inputs['Detail'].default_value = 12.0; nz.inputs['Roughness'].default_value = 0.7
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); e = cr.color_ramp.elements
    e[0].position = 0.42; e[0].color = lin('#3A2E22'); e[1].position = 0.62; e[1].color = lin('#A8987C')
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    rr = nt.nodes.new('ShaderNodeMapRange'); rr.inputs['From Min'].default_value = 0.4; rr.inputs['From Max'].default_value = 0.65
    rr.inputs['To Min'].default_value = 0.35; rr.inputs['To Max'].default_value = 0.05
    nt.links.new(nz.outputs['Fac'], rr.inputs['Value']); nt.links.new(rr.outputs['Result'], b.inputs['Roughness'])
    _M['antique-mirror'] = m
    return m


def backbar(bpy, kit, p, objs):
    W, y0 = P.W, P.BACKBAR_Y
    x0, x1 = P.BAR_X0 - 0.30, P.BAR_X1 + 0.30
    rnd = random.Random(33)
    niches = [(nx, nx + nw) for nx, nw in P.NICHES]

    def runs(a, b, gap=0.04):
        out, cur = [], a
        for n0, n1 in niches:
            out.append((cur, n0 - gap)); cur = n1 + gap
        out.append((cur, b))
        return out
    base = Mesh('backbar-base'); doors = Mesh('backbar-doors'); tops = Mesh('backbar-top')
    for a, b in runs(x0, x1):
        base.box(a, y0 + 0.02, 0.0, b, W, P.BASE_H)
        nd = max(1, int((b - a) / 0.55)); dw = (b - a) / nd
        for k in range(nd):
            doors.box(a + k * dw + 0.004, y0, 0.12, a + (k + 1) * dw - 0.004, y0 + 0.02, P.BASE_H - 0.02)
        tops.box(a - 0.01, y0 - 0.03, P.BASE_H, b + 0.01, W, P.BASE_H + 0.035)
    objs.append(base.object(bpy, walnut(bpy, vertical=True)))
    objs.append(doors.object(bpy, walnut(bpy, vertical=True), bevel=0.003))
    objs.append(tops.object(bpy, walnut(bpy, coat=0.8, coat_rough=0.18), bevel=0.004))
    # the mirror behind the shelves, the uprights (walnut) between the bays, the cornice
    mi = Mesh('backbar-mirror'); up = Mesh('backbar-uprights')
    bays = [x0]
    for a, b in runs(x0, x1):
        nb = max(1, round((b - a) / 1.1))
        bays += [a + (b - a) * k / nb for k in range(1, nb)] + [b]
    for a, b in runs(x0, x1):
        mi.box(a, W - 0.02, P.BASE_H + 0.035, b, W - 0.01, P.BACKBAR_TOP)
    for xb in bays:
        up.box(xb - 0.025, y0 + 0.02, P.BASE_H + 0.035, xb + 0.025, W - 0.02, P.BACKBAR_TOP)
    for n0, n1 in niches:                                                  # the niches' walnut surrounds
        for xa in (n0 - 0.04, n1):
            up.box(xa, y0, 0.0, xa + 0.04, W, P.BACKBAR_TOP)
        up.box(n0 - 0.04, y0, P.NICHE_Z0 + P.NICHE_H, n1 + 0.04, W, P.NICHE_Z0 + P.NICHE_H + 0.05)
        up.box(n0, y0, 0.0, n1, W, P.NICHE_Z0)
    up.box(x0 - 0.04, y0 - 0.06, P.BACKBAR_TOP, x1 + 0.04, W, P.BACKBAR_TOP + 0.16)        # the cornice
    up.box(x0 - 0.06, y0 - 0.08, P.BACKBAR_TOP + 0.16, x1 + 0.06, W, P.BACKBAR_TOP + 0.20)
    objs.append(mi.object(bpy, antique_mirror(bpy)))
    objs.append(up.object(bpy, walnut(bpy, vertical=True), bevel=0.004))
    # the niches: lined in walnut, their backs a warm-lit linen panel, so the Smoke cabinet stands against a glow
    nl = Mesh('niche-lining'); nb_ = Mesh('niche-back')
    for n0, n1 in niches:
        nb_.box(n0, W - 0.03, P.NICHE_Z0, n1, W - 0.01, P.NICHE_Z0 + P.NICHE_H)
        nl.box(n0, y0 + 0.02, P.NICHE_Z0 + P.NICHE_H - 0.02, n1, W, P.NICHE_Z0 + P.NICHE_H)
    objs.append(nl.object(bpy, walnut(bpy, vertical=True, tint='#2A1A10', mix=0.5)))
    objs.append(nb_.object(bpy, principled(bpy, 'niche-linen', '#D9BE94', rough=0.85, emit='#FFB868',
                                           strength=p.get('niche_glow', 0.35))))
    # the shelves: 35 mm walnut on brass brackets, each with a warm strip under its front edge
    sh = Mesh('backbar-shelves'); bk = Mesh('backbar-brackets'); led = Mesh('backbar-led')
    for z in P.SHELVES_Z:
        for a, b in runs(x0, x1):
            sh.box(a + 0.03, y0 + 0.05, z - P.SHELF_T, b - 0.03, W - 0.02, z)
            led.box(a + 0.04, y0 + 0.07, z - P.SHELF_T - 0.004, b - 0.04, y0 + 0.08, z - P.SHELF_T - 0.001)
            for xb in [a + 0.25 + k * 0.8 for k in range(int((b - a - 0.3) / 0.8) + 1)]:
                bk.box(xb - 0.008, W - 0.25, z - P.SHELF_T - 0.07, xb + 0.008, W - 0.02, z - P.SHELF_T)
    objs.append(sh.object(bpy, walnut(bpy), bevel=0.004))
    objs.append(bk.object(bpy, brass(bpy)))
    objs.append(led.object(bpy, emitter(bpy, 'shelf-led', p.get('shelf_color', '#FFB067'), p.get('shelf_glow', 8.0))))
    # the bottles: the counter's back row and each shelf, gaps where one is out
    bodies = R._bottle_meshes(bpy)
    glass = {}
    spirits = ['#B5651D', '#C87A2A', '#8E4A1A', '#D49A3A', '#7A3A14', '#E8E4D8', '#5A2A12', '#A0521C', '#6E1E14']
    labels = [R.label_mat(bpy, f'label-den-{i}', c, rnd) for i, c in
              enumerate(['#EFE8DA', '#D9C9A6', '#E6DCC8', '#7A2A22', '#E9E3D3', '#1F2A24', '#C8A15A', '#F4F1EA', '#2A2420'])]
    caps = [principled(bpy, 'cap-black', '#151413', rough=0.4), principled(bpy, 'cap-gold', '#B08A4E', rough=0.3, metal=1.0),
            principled(bpy, 'cap-wood', '#6A4A30', rough=0.6), principled(bpy, 'cap-wax', '#6E1A16', rough=0.35)]
    levels = [P.BASE_H + 0.035] + P.SHELVES_Z
    for li, z in enumerate(levels):
        top_free = (P.SHELVES_Z + [P.BACKBAR_TOP])[li] - P.SHELF_T - z if li < len(P.SHELVES_Z) else P.BACKBAR_TOP - z
        for a, b in runs(x0, x1):
            x = a + 0.08
            while x < b - 0.08:
                k = rnd.choice(list(bodies)); body, label, cap, r = bodies[k]
                if x + 2 * r > b - 0.05:
                    break
                if rnd.random() < 0.14:
                    x += rnd.uniform(0.07, 0.15); continue
                sr, shz = rnd.uniform(0.92, 1.1), rnd.uniform(0.9, 1.1)
                if 0.36 * shz > top_free - 0.03:
                    shz = (top_free - 0.04) / 0.36
                cx = x + r * 1.1; cy = W - 0.14 - rnd.uniform(0.0, 0.02) - (0.13 if rnd.random() < 0.4 else 0.0)
                c = rnd.choice(spirits) if k != 'gin' else rnd.choice(['#EEF2EE', '#E2EEF0'])
                if c not in glass:
                    glass[c] = principled(bpy, f'bottle-glass-den-{c}', c, rough=0.02, trans=1.0, ior=1.45)
                rot = rnd.uniform(-0.4, 0.4) - math.pi * 0.5 + math.pi * 0.35       # the labels toward the room (-y)
                for me, mm in ((body, glass[c]), (label, rnd.choice(labels)), (cap, rnd.choice(caps))):
                    ob = bpy.data.objects.new(f'{me.name}@den{li}.{x:.2f}', me)
                    ob.location = (cx, cy, z); ob.rotation_euler.z = rot; ob.scale = (sr, sr, shz)
                    bpy.context.scene.collection.objects.link(ob)
                    if not me.materials:
                        me.materials.append(mm)
                    ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = mm
                    objs.append(ob)
                x += 2.2 * r * sr + rnd.uniform(0.01, 0.03)


# --- the banquette and tables -------------------------------------------------------------------------------------
def banquette(bpy, kit, p, objs):
    x0, x1, d = P.BANQ_X0, P.BANQ_X1, P.BANQ_D
    base = Mesh('banq-base'); seat = Mesh('banq-seat'); back = Mesh('banq-back')
    yw = 0.035
    base.box(x0, yw, 0.0, x1, d, P.BANQ_SEAT - 0.12)
    base.box(x0 - 0.05, yw, 0.0, x0, d + 0.02, P.BANQ_BACK + 0.04); base.box(x1, yw, 0.0, x1 + 0.05, d + 0.02, P.BANQ_BACK + 0.04)
    nseat = int((x1 - x0) / 0.76)
    for k in range(nseat):                                         # a seat cushion per sitter
        a = x0 + k * (x1 - x0) / nseat
        seat.box(a + 0.006, yw + 0.10, P.BANQ_SEAT - 0.12, a + (x1 - x0) / nseat - 0.006, d, P.BANQ_SEAT)
    nch = int((x1 - x0) / 0.15)
    for k in range(nch):                                           # the back, in channels
        a = x0 + k * (x1 - x0) / nch
        back.box(a + 0.004, yw, P.BANQ_SEAT + 0.02, a + (x1 - x0) / nch - 0.004, yw + 0.11, P.BANQ_BACK)
    objs.append(base.object(bpy, walnut(bpy), bevel=0.004))
    objs.append(seat.object(bpy, leather(bpy), bevel=0.04, seg=4))
    objs.append(back.object(bpy, leather(bpy), bevel=0.035, seg=4))
    # the two-tops: walnut on a brass pedestal; and the round one by the window
    tops = Mesh('tables'); legs = Mesh('table-legs')
    T = P.TABLE
    for cx in P.TABLES:
        tops.box(cx - T['w'] / 2, T['y'] - T['d'] / 2, T['h'] - 0.03, cx + T['w'] / 2, T['y'] + T['d'] / 2, T['h'])
        _cyl(legs.bm, cx, T['y'], 0.0, 0.03, T['h'] - 0.03, seg=20)
        _cyl(legs.bm, cx, T['y'], 0.0, 0.20, 0.02, seg=32)
    wx, wy = P.WINDOW_TABLE
    _cyl(tops.bm, wx, wy, T['h'] - 0.03, 0.34, 0.03, seg=48)
    _cyl(legs.bm, wx, wy, 0.0, 0.03, T['h'] - 0.03, seg=20); _cyl(legs.bm, wx, wy, 0.0, 0.20, 0.02, seg=32)
    objs.append(tops.object(bpy, walnut(bpy, coat=0.8, coat_rough=0.18), bevel=0.005))
    objs.append(legs.object(bpy, brass(bpy), smooth=True))


# --- small things: sconces, pendants, candles, glasses -----------------------------------------------------------
def shade_mat(bpy, p):
    """A pleated linen shade: lit from within, warm where the lamp shows through, its weave a fine bump."""
    if 'shade-linen' in _M:
        return _M['shade-linen']
    m = principled(bpy, 'shade-linen', '#E9D3AE', rough=0.8, emit='#FFB86A', strength=p.get('shade_glow', 1.2))
    R._set(_bsdf(m), 'Transmission Weight', 0.2)
    _M['shade-linen'] = m
    return m


def _shade(bm, cx, cy, z0, r0, r1, h, seg=36):
    """An open drum (or a cone), its pleats a ripple round it."""
    rings = []
    for zz, rr in ((z0, r0), (z0 + h, r1)):
        ring = []
        for i in range(seg):
            a = 2 * math.pi * i / seg; rp = rr * (1 + 0.025 * (1 if i % 2 else -1))
            ring.append(bm.verts.new((cx + rp * math.cos(a), cy + rp * math.sin(a), zz)))
        rings.append(ring)
    for i in range(seg):
        j = (i + 1) % seg
        f = bm.faces.new([rings[0][i], rings[0][j], rings[1][j], rings[1][i]]); f.normal_update()


def sconces(bpy, kit, p, objs):
    sh = Mesh('sconce-shades'); hw = Mesh('sconce-brass')
    def one(x, yw, side):
        s = 1 if side == 0 else -1                                  # +y off the right wall, -y off the left
        yc = yw + s * 0.20; z = P.SCONCE_Z
        _cyl(hw.bm, x, yw + s * 0.008, z - 0.06, 0.05, 0.12, seg=24)          # the backplate (approx.)
        hw.box(x - 0.008, min(yw, yc), z - 0.004, x + 0.008, max(yw, yc), z + 0.012)   # the arm
        _cyl(hw.bm, x, yc, z, 0.014, 0.05, seg=12)                           # the socket
        _shade(sh.bm, x, yc, z - 0.02, 0.105, 0.085, 0.17)
    for x in P.SCONCES_RIGHT:
        one(x, 0.02, 0)
    for x in P.SCONCES_LEFT_LOUNGE:
        one(x, P.W, 1)
    objs.append(sh.object(bpy, shade_mat(bpy, p), smooth=True))
    objs.append(hw.object(bpy, brass(bpy), smooth=True))


def pendants(bpy, kit, p, objs):
    """Spun-brass domes over the bar: a 360 mm shade, its inside painted white, on a cloth cord from the ceiling."""
    sh = Mesh('pendant-shades'); inn = Mesh('pendant-inside'); cord = Mesh('pendant-cords')
    y = P.BAR_FRONT + 0.18; zr = P.PENDANT_RIM
    prof = [(0.18, 0.0), (0.175, 0.03), (0.16, 0.08), (0.12, 0.14), (0.06, 0.18), (0.025, 0.19), (0.02, 0.26)]
    for x in P.PENDANTS:
        _lathe(sh.bm, prof, seg=48, z0=zr, cx=x, cy=y)
        _lathe(inn.bm, [(r - 0.003, z + 0.002) for r, z in prof[:5]], seg=48, z0=zr, cx=x, cy=y)
        _cyl(cord.bm, x, y, zr + 0.26, 0.003, P.CEIL - zr - 0.26, seg=8)
    objs.append(sh.object(bpy, brass(bpy), smooth=True))
    objs.append(inn.object(bpy, principled(bpy, 'pendant-white', '#F2E8D8', rough=0.5, emit='#FFC27A',
                                           strength=p.get('pendant_glow', 0.6)), smooth=True))
    objs.append(cord.object(bpy, principled(bpy, 'cord', '#1A1612', rough=0.7), smooth=True))


def candles(bpy, kit, p, objs):
    """Amber glass votives with a tea light, each flame a small emitter (the shots light them)."""
    gl = Mesh('votives'); wax = Mesh('tealights'); fl = Mesh('flames')
    for x, y, z in P.candle_spots():
        _lathe(gl.bm, [(0, 0), (0.032, 0), (0.034, 0.075), (0.031, 0.075), (0.029, 0.004), (0, 0.004)], seg=32, z0=z, cx=x, cy=y)
        _cyl(wax.bm, x, y, z + 0.004, 0.019, 0.016, seg=20)
        _lathe(fl.bm, [(0, 0), (0.004, 0.004), (0.0045, 0.010), (0.002, 0.018), (0, 0.022)], seg=12, z0=z + 0.022, cx=x, cy=y)
    objs.append(gl.object(bpy, candle_glass(bpy), smooth=True))
    objs.append(wax.object(bpy, principled(bpy, 'wax', '#F1E6D2', rough=0.5, sss=0.4), smooth=True))
    objs.append(fl.object(bpy, emitter(bpy, 'flame', '#FFB04A', p.get('flame', 30.0)), smooth=True))


def glassware(bpy, kit, p, objs):
    rnd = random.Random(12)
    glass = principled(bpy, 'tumbler-glass', '#FFFFFF', rough=0.01, trans=1.0, ior=1.5)
    pour = principled(bpy, 'pour-den', '#B5601A', rough=0.0, trans=1.0, ior=1.36)
    paper = principled(bpy, 'menu-card', '#EDE6D8', rough=0.75, bump=(0.004, 0.06, 0.0004))
    rocks = [(0, 0), (0.041, 0), (0.0425, 0.09), (0.0385, 0.09), (0.037, 0.016), (0, 0.016)]
    coupe = [(0, 0), (0.038, 0), (0.038, 0.004), (0.006, 0.010), (0.0045, 0.100), (0.030, 0.113), (0.056, 0.140),
             (0.0535, 0.140), (0.028, 0.117), (0, 0.111)]
    zt = P.BAR_TOP_Z + P.TOP_T; yb = P.BAR_FRONT - 0.12; T = P.TABLE
    spots = [(x, yb + rnd.uniform(-0.03, 0.03), zt, rnd.choice(['rocks', 'rocks', 'coupe'])) for x in (3.9, 4.75, 5.4, 7.1, 7.9, 9.4)]
    spots += [(cx - 0.12, T['y'] + 0.10, T['h'], 'rocks') for cx in P.TABLES] + \
             [(cx + 0.10, T['y'] + 0.16, T['h'], 'coupe') for cx in P.TABLES[1::2]]
    wx, wy = P.WINDOW_TABLE                                           # two at the window table, a pour in each
    spots += [(wx + 0.12, wy + 0.14, T['h'], 'rocks'), (wx - 0.06, wy - 0.18, T['h'], 'coupe')]
    spots += [(P.SIDE_TABLES[0][0] - 0.06, P.SIDE_TABLES[0][1] - 0.07, 0.50, 'rocks'),
              (P.SIDE_TABLES[1][0], P.SIDE_TABLES[1][1] + 0.08, 0.50, 'rocks')]
    gl = Mesh('glasses'); lq = Mesh('pours')
    for x, y, z, kind in spots:
        _lathe(gl.bm, rocks if kind == 'rocks' else coupe, seg=40, z0=z, cx=x, cy=y)
        if kind == 'rocks':
            _cyl(lq.bm, x, y, z + 0.0165, 0.0366, rnd.uniform(0.02, 0.04), seg=40)
    objs.append(gl.object(bpy, glass, smooth=True))
    objs.append(lq.object(bpy, pour, smooth=True))
    mn = Mesh('menus')
    for x, y, z in [(4.45, yb - 0.04, zt), (8.2, yb - 0.02, zt)] + [(cx + 0.12, T['y'] - 0.05, T['h']) for cx in P.TABLES[1::2]]:
        mn.box(x - 0.075, y - 0.11, z + 0.0005, x + 0.075, y + 0.11, z + 0.0035)
    objs.append(mn.object(bpy, paper, bevel=0.001))


# --- the listening room -------------------------------------------------------------------------------------------
def _curtain(m, x, ya, yb, z1, folds=0.055, n=48, seed=0):
    """A velvet curtain gathered into folds, hanging in the plane x = const from y ya to yb."""
    for k in range(n):
        y1 = ya + (yb - ya) * k / n; y2 = ya + (yb - ya) * (k + 1) / n
        d1 = folds * math.sin(k * 1.3 + seed); d2 = folds * math.sin((k + 1) * 1.3 + seed)
        m.quad([(x + d1, y1, 0.005), (x + d2, y2, 0.005), (x + d2, y2, z1), (x + d1, y1, z1)])


def lounge(bpy, kit, p, objs):
    W, L = P.W, P.L
    X0 = P.LOUNGE_X0
    # the cased opening: a walnut header and jambs
    hd = Mesh('opening'); hd.box(X0 - 0.10, 0.0, P.HEADER_Z, X0 + 0.10, W, P.CEIL)
    hd.box(X0 - 0.10, 0.0, 0.0, X0 + 0.10, 0.18, P.HEADER_Z); hd.box(X0 - 0.10, W - 0.18, 0.0, X0 + 0.10, W, P.HEADER_Z)
    objs.append(hd.object(bpy, walnut(bpy, vertical=True), bevel=0.006))
    # the curtains drawn back to either side, on the lounge side of the opening
    cv = Mesh('lounge-curtains')
    _curtain(cv, X0 + 0.22, 0.18, 0.18 + P.CURTAIN['w'], P.HEADER_Z - 0.02, seed=0.0)
    _curtain(cv, X0 + 0.22, W - 0.18 - P.CURTAIN['w'], W - 0.18, P.HEADER_Z - 0.02, seed=1.7)
    objs.append(cv.object(bpy, velvet(bpy, P.CURTAIN['colour'], 'velvet-oxblood'), smooth=True))
    # the slat ceiling: walnut over a black absorber
    ab = Mesh('lounge-absorber'); ab.box(X0 + 0.10, 0.0, P.CEIL - 0.06, L, W, P.CEIL - 0.01)
    objs.append(ab.object(bpy, kit.material(bpy, 'felt', '#141110')))
    sl = Mesh('lounge-slats'); S = P.LOUNGE_CEILING; y = 0.02
    while y + S['slat'] < W:
        sl.box(X0 + 0.12, y, P.CEIL - 0.13, L - 0.01, y + S['slat'], P.CEIL - 0.07); y += S['pitch']
    objs.append(sl.object(bpy, walnut(bpy)))
    # the plinths under the Ember pair (walnut)
    pl = Mesh('plinths')
    for role, colour, x, yy, z, rot in P.speakers():
        if role != 'lounge':
            continue
        a = math.radians(rot); w, d = P.PLINTH['w'] / 2, P.PLINTH['d'] / 2; c, s = math.cos(a), math.sin(a)
        corners = [(x + c * u - s * v, yy + s * u + c * v) for u, v in ((-w, -d), (w, -d), (w, d), (-w, d))]
        vb = [pl.bm.verts.new((cx, cy, 0.0)) for cx, cy in corners]; vt = [pl.bm.verts.new((cx, cy, P.PLINTH['h'])) for cx, cy in corners]
        for f in ([vb[3], vb[2], vb[1], vb[0]], vt, *[[vb[i], vb[(i + 1) % 4], vt[(i + 1) % 4], vt[i]] for i in range(4)]):
            fa = pl.bm.faces.new(f); fa.normal_update()
    objs.append(pl.object(bpy, walnut(bpy), bevel=0.004))
    # the rug: a worn floral wool, its edge relaxed onto the floor
    Rg = P.RUG
    objs += R31.rug(bpy, 'lounge-rug', {'position': [(Rg['x0'] + Rg['x1']) / 2, (Rg['y0'] + Rg['y1']) / 2],
                                        'size': [Rg['x1'] - Rg['x0'], Rg['y1'] - Rg['y0']], 'pile': 0.008,
                                        'texture': p.get('rug_tex', 'floral_jacquard'), 'tint': p.get('rug_tint', '#6A2E1E'),
                                        'tint_mix': p.get('rug_mix', 0.45), 'tex_scale': 0.9, 'displace': 0.002,
                                        'cell': 0.02, 'sheen': 0.5, 'value': p.get('rug_value', 0.8)}, kit)
    # the low side tables: walnut drums
    st = Mesh('side-tables')
    for x, yy in P.SIDE_TABLES:
        _cyl(st.bm, x, yy, 0.0, 0.21, 0.50, seg=48)
    objs.append(st.object(bpy, walnut(bpy, vertical=True), smooth=True, bevel=0.006))
    # the books on the right wall, floor to 2.4 m
    rnd = random.Random(21); B = P.BOOKS
    sh = Mesh('bookshelves'); bk = Mesh('books')
    pal = ['#5A1E1A', '#2A3A2A', '#1E2430', '#6E5A3A', '#D9CFB8', '#3A2A20', '#8A6A3A', '#1A1A1A', '#7A3A22', '#4A4038',
           '#B8A27A', '#2E2A26']
    nb = 6; bw = (B['x1'] - B['x0']) / nb
    for k in range(nb + 1):
        x = B['x0'] + k * bw
        sh.box(x - 0.012, 0.0, 0.0, x + 0.012, B['depth'], B['z1'])
    shelf_z = [0.08 + 0.33 * i for i in range(8)]
    for z in shelf_z:
        sh.box(B['x0'], 0.0, z - 0.025, B['x1'], B['depth'], z)
    sh.box(B['x0'] - 0.02, 0.0, B['z1'] - 0.03, B['x1'] + 0.02, B['depth'] + 0.03, B['z1'] + 0.03)
    for z in shelf_z[:-1]:
        for k in range(nb):
            x = B['x0'] + k * bw + 0.015
            while x < B['x0'] + (k + 1) * bw - 0.03:
                t = rnd.uniform(0.018, 0.045); h = rnd.uniform(0.19, 0.29); d = rnd.uniform(0.15, 0.24)
                if rnd.random() < 0.05:
                    x += rnd.uniform(0.04, 0.10); continue
                col = R._mixhex(rnd.choice(pal), '#000000', rnd.uniform(0.0, 0.3))
                bk.box(x, B['depth'] - d, z, x + t, B['depth'] - 0.005, z + h, col=col)
                x += t + 0.001
    objs.append(sh.object(bpy, walnut(bpy, vertical=True), bevel=0.003))
    objs.append(bk.object(bpy, R.colour_attr_mat(bpy, 'book-cloth', rough=0.7), bevel=0.0015))


def record_wall(bpy, kit, p, objs):
    W, L = P.W, P.L
    Rc = P.REC; rnd = random.Random(7)
    cell = Rc['cell']; ncols = int((Rc['y1'] - Rc['y0']) / cell); y0 = (Rc['y0'] + Rc['y1']) / 2 - ncols * cell / 2
    nrows = int((Rc['z1'] - 0.05) / cell)
    C = P.CONSOLE
    boards = Mesh('record-boards'); sleeves = Mesh('sleeves')
    pal = ['#1A1A1A', '#EDE7DA', '#A8321E', '#2B3C5E', '#D9A93C', '#4E6A3E', '#D8D2C4', '#3A2E2A', '#7A2D2B',
           '#F2EEE6', '#2F2F33', '#B88A5A', '#5D7486', '#C8642E', '#9C9A93', '#141414', '#C9C1AE']
    xf = L - Rc['depth']
    for ci in range(ncols + 1):
        ya = y0 + ci * cell
        boards.box(xf, ya, 0.0, L, ya + 0.02, Rc['z1'])
    for ri in range(nrows + 1):
        z = 0.05 + ri * cell
        boards.box(xf, y0, z - 0.02, L, y0 + ncols * cell + 0.02, z)
        if ri == nrows:
            continue
        for ci in range(ncols):
            ya, yb = y0 + ci * cell + 0.02, y0 + (ci + 1) * cell
            if C['y0'] - 0.1 < (ya + yb) / 2 < C['y1'] + 0.1 and z < C['h'] + 0.05:
                continue                                                # the console stands here
            s = ya + 0.01
            while s < yb - 0.01:
                t = rnd.uniform(0.0025, 0.0045)
                if rnd.random() < 0.03:
                    s += rnd.uniform(0.02, 0.05); continue
                col = lin(rnd.choice(pal)) if rnd.random() < 0.7 else R._mixhex(rnd.choice(pal), '#E8DCC4', rnd.random() * 0.5)
                sx = xf + 0.03 + rnd.uniform(0.0, 0.015)
                sleeves.box(sx, s, z, sx + 0.31, s + t, z + 0.315 + rnd.uniform(-0.004, 0.002), col=col)
                s += t + 0.0003
    boards.box(L - 0.02, y0, 0.0, L, y0 + ncols * cell, Rc['z1'])
    boards.box(xf - 0.03, y0 - 0.02, Rc['z1'], L, y0 + ncols * cell + 0.04, Rc['z1'] + 0.10)       # the cornice
    objs.append(boards.object(bpy, walnut(bpy, vertical=True), bevel=0.002))
    objs.append(sleeves.object(bpy, R.colour_attr_mat(bpy, 'sleeve-card', rough=0.62)))
    # a picture light's warm strip under the cornice
    st = Mesh('record-strip'); st.box(xf - 0.02, y0, Rc['z1'] - 0.012, xf - 0.005, y0 + ncols * cell, Rc['z1'] - 0.004)
    objs.append(st.object(bpy, emitter(bpy, 'record-strip', '#FFC27A', p.get('record_glow', 3.0))))
    # the console in the middle: a low walnut credenza (room 31's), back to the wall
    cobj = R31.credenza(bpy, 'console', {'position': [0.0, 0.0], 'size': [C['y1'] - C['y0'], C['d'], C['h']], 'doors': 4,
                                          'texture': 'smoked_walnut_veneer', 'lift': 1.1, 'res': '2k'}, kit)
    for ob in cobj:
        ob.rotation_euler.z = math.radians(-90); ob.location = (L - C['d'] / 2 - 0.02, W / 2, 0.0)
    objs += cobj
    # the amplifier on it, beside the record player (a dark-faced valve amp)
    am = Mesh('amp'); ax, ay = L - 0.30, W / 2 + 0.55
    am.box(ax - 0.17, ay - 0.21, C['h'], ax + 0.17, ay + 0.21, C['h'] + 0.13)
    objs.append(am.object(bpy, principled(bpy, 'amp-face', '#26221E', rough=0.35, metal=0.6), bevel=0.004))
    vu = Mesh('amp-vu'); vu.box(ax - 0.172, ay - 0.12, C['h'] + 0.06, ax - 0.169, ay - 0.02, C['h'] + 0.11)
    vu.box(ax - 0.172, ay + 0.02, C['h'] + 0.06, ax - 0.169, ay + 0.12, C['h'] + 0.11)
    objs.append(vu.object(bpy, emitter(bpy, 'vu', '#FFB45A', p.get('vu', 2.0))))


# --- the street ---------------------------------------------------------------------------------------------------
def street(bpy, kit, p, objs):
    W, T = P.W, P.WALL_T
    xf = -0.16                                                            # the shopfront's face
    SW = 3.4; RD = 12.0
    yA, yB = -40.0, W + 40.0
    sw = Mesh('sidewalk'); sw.box(xf - SW, yA, -0.15, xf, yB, 0.0)
    objs.append(sw.object(bpy, R._pbr(bpy, kit, 'concrete_pavement', res='2k', tint='#77746F', tint_mix=0.3)))
    cb = Mesh('curb'); cb.box(xf - SW - 0.15, yA, -0.15, xf - SW, yB, 0.0)
    objs.append(cb.object(bpy, principled(bpy, 'curb', '#8A8781', rough=0.8)))
    rd = Mesh('road'); rd.box(xf - SW - 0.15 - RD, yA, -0.30, xf - SW - 0.15, yB, -0.15)
    rm = R._pbr(bpy, kit, 'asphalt_02', res='2k', tint='#3A3A3C', tint_mix=0.4, rough_mul=p.get('road_rough', 0.4))
    if p.get('wet'):
        rm = rm.copy(); rm.name = 'asphalt-wet-den'; nt = rm.node_tree; rb = _bsdf(rm)
        R._set(rb, 'Coat Weight', 1.0); R._set(rb, 'Coat IOR', 1.33)
        tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 0.35; nz.inputs['Detail'].default_value = 6.0
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.35; mr.inputs['From Max'].default_value = 0.62
        mr.inputs['To Min'].default_value = 0.005; mr.inputs['To Max'].default_value = 0.2
        nt.links.new(nz.outputs['Fac'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], rb.inputs['Coat Roughness'])
    objs.append(rd.object(bpy, rm))
    # the building over the shop: three storeys of painted wood siding, two bay windows on each upper floor, a cornice
    H0 = P.CEIL + 0.45; H1 = H0 + 2 * 3.1 + 0.9
    sid = Mesh('siding')
    sid.box(xf - 0.02, -T, H0, 0.0, W + T, H1)
    for z in [H0 + 0.15 * k for k in range(int((H1 - H0) / 0.15))]:                # the siding's laps
        sid.box(xf - 0.035, -T, z, xf - 0.02, W + T, z + 0.02)
    objs.append(sid.object(bpy, principled(bpy, 'siding-paint', p.get('siding', '#B8AE98'), rough=0.6,
                                           bump=(0.03, 0.05, 0.0005))))
    trim = Mesh('trim'); dark = Mesh('flat-glass'); lit = Mesh('flat-lit')
    trim.box(xf - 0.30, -T - 0.05, H1, 0.0, W + T + 0.05, H1 + 0.45)                 # the cornice
    trim.box(xf - 0.40, -T - 0.08, H1 + 0.45, 0.0, W + T + 0.08, H1 + 0.55)
    trim.box(xf - 0.12, -T, P.CEIL + 0.20, xf, W + T, H0)                           # the shop's cornice band
    trim.box(xf - 0.22, -T - 0.03, H0 - 0.05, xf, W + T + 0.03, H0 + 0.05)
    rnd = random.Random(9)
    for storey in range(2):
        z0 = H0 + 0.35 + storey * 3.1
        for yc in (1.75, W - 1.75):                                                # a bay: three faces, a window in each
            bw, bd, bh = 2.4, 0.62, 2.35
            trim.box(xf - bd, yc - bw / 2, z0 - 0.25, xf, yc + bw / 2, z0)          # its apron
            trim.box(xf - bd - 0.05, yc - bw / 2 - 0.05, z0 + bh, xf, yc + bw / 2 + 0.05, z0 + bh + 0.25)   # its hood
            trim.box(xf - bd, yc - bw / 2, z0, xf - bd + 0.06, yc - bw / 2 + 0.12, z0 + bh)                 # posts
            trim.box(xf - bd, yc + bw / 2 - 0.12, z0, xf - bd + 0.06, yc + bw / 2, z0 + bh)
            trim.box(xf - 0.10, yc - bw / 2, z0, xf, yc - bw / 2 + 0.06, z0 + bh)
            trim.box(xf - 0.10, yc + bw / 2 - 0.06, z0, xf, yc + bw / 2, z0 + bh)
            on = rnd.random() < p.get('windows_lit', 0.5)
            (lit if on else dark).box(xf - bd + 0.02, yc - bw / 2 + 0.12, z0 + 0.08, xf - bd + 0.04, yc + bw / 2 - 0.12, z0 + bh - 0.08)
            (lit if on else dark).box(xf - bd + 0.06, yc - bw / 2 + 0.01, z0 + 0.08, xf - 0.10, yc - bw / 2 + 0.03, z0 + bh - 0.08)
            (lit if on else dark).box(xf - bd + 0.06, yc + bw / 2 - 0.03, z0 + 0.08, xf - 0.10, yc + bw / 2 - 0.01, z0 + bh - 0.08)
            trim.box(xf - bd - 0.02, yc - bw / 2 + 0.12, z0 + bh * 0.62, xf - bd + 0.06, yc + bw / 2 - 0.12, z0 + bh * 0.62 + 0.05)
    objs.append(trim.object(bpy, principled(bpy, 'trim-paint', '#E4DCCB', rough=0.55), bevel=0.006))
    objs.append(dark.object(bpy, principled(bpy, 'dark-glass', '#0A0B0D', rough=0.03, spec=0.6)))
    objs.append(lit.object(bpy, emitter(bpy, 'lit-blind', '#FFC07A', p.get('flat_glow', 0.25))))
    # the neighbours: an older shop each side, closed for the night (their windows dark, a light at the back of one)
    nb = Mesh('neighbours'); ng = Mesh('neighbour-glass'); nl = Mesh('neighbour-lit')
    for (ya, yb, h, col) in ((-T - 7.6, -T, 9.6, 0), (W + T, W + T + 8.2, 11.4, 1), (-T - 15.4, -T - 7.6, 8.4, 2),
                             (W + T + 8.2, W + T + 15.0, 9.8, 3)):
        nb.box(xf + 0.05, ya, 0.0, 6.0, yb - 0.02, h)
        ng.box(xf + 0.04, ya + 0.5, 0.55, xf + 0.05, yb - 1.6, 2.6)
        if col == 1:
            nl.box(xf + 0.03, ya + 0.6, 0.6, xf + 0.035, ya + 2.4, 2.3)
        for storey in range(int((h - 4.0) / 3.1)):
            z0 = 4.4 + storey * 3.1
            for k in range(int((yb - ya - 1.0) / 2.2)):
                yy = ya + 0.8 + k * 2.2
                (nl if rnd.random() < 0.35 else ng).box(xf + 0.03, yy, z0, xf + 0.05, yy + 1.1, z0 + 1.8)
    nm = (principled(bpy, 'neighbour-plain', p.get('neighbour', '#7E7468'), rough=0.8) if p.get('neighbour_plain')
          else R._pbr(bpy, kit, 'white_stucco_02', res='1k', tint=p.get('neighbour', '#7E7468'), tint_mix=0.55))
    objs.append(nb.object(bpy, nm))
    objs.append(ng.object(bpy, principled(bpy, 'dark-glass', '#0A0B0D', rough=0.03, spec=0.6)))
    objs.append(nl.object(bpy, emitter(bpy, 'neighbour-lit', '#FFB070', p.get('across_glow', 0.04))))
    # the block across the street, behind the camera: a dark mass for the glass to mirror
    ac = Mesh('across'); ac.box(xf - SW - RD - 0.15 - 3.4 - 12.0, yA, 0.0, xf - SW - RD - 0.15 - 3.4, yB, 12.0)
    objs.append(ac.object(bpy, principled(bpy, 'across-dark', '#15141A', rough=0.8)))
    acs = Mesh('sidewalk-across'); acs.box(xf - SW - RD - 0.15 - 3.4, yA, -0.15, xf - SW - RD - 0.15, yB, 0.0)
    objs.append(acs.object(bpy, R._pbr(bpy, kit, 'concrete_pavement', res='2k', tint='#77746F', tint_mix=0.3)))


def room(bpy, name, p, kit):
    objs = []
    shell(bpy, kit, p, objs)
    shopfront(bpy, kit, p, objs)
    bar(bpy, kit, p, objs)
    backbar(bpy, kit, p, objs)
    banquette(bpy, kit, p, objs)
    sconces(bpy, kit, p, objs)
    pendants(bpy, kit, p, objs)
    lounge(bpy, kit, p, objs)
    record_wall(bpy, kit, p, objs)
    if p.get('props', True):
        candles(bpy, kit, p, objs)
        glassware(bpy, kit, p, objs)
    if p.get('street', True):
        street(bpy, kit, p, objs)
    return objs
