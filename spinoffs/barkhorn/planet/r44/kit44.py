"""Planet EARF, round 44: the lantern, built from plan44.py as one kit `ext` piece (renders and the axonometric).

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r44/kit44.py", "fn": "house", ...}

The frame is plan44's: x from the shopfront glass into the shell, y from the right-hand party wall, z up from the floor.
Materials chosen to last (DESIGN.md): honed terrazzo floors (marble and glass chips in a grey cement-look epoxy), a honed
quartzite bar top, oiled white oak, blackened steel, lime plaster, an acoustic-plaster ceiling, end-grain oak in the
lantern. Acrylic only where nothing wears it: the lantern's lit band (fins in the outer cavity, behind the oak), and the
offcut chips in the terrazzo of Mother EARF's plinth and the bar's die.

Calibrated acrylic: `acrylic()` is a Principled transmission surface at IOR 1.49 (ASTM D542) with a volume absorption
set so a sheet transmits what the maker's data says: clear cast acrylic about 92% at 3 mm (ASTM D1003; A&C's TruCast
clear 0001 is listed at 89.4%), of which about 7.5% is the two faces' Fresnel loss at n = 1.49, so the bulk absorbs
almost nothing; a tint's internal transmittance per channel sets its absorption: sigma = -ln(Ti) / d.
"""
import math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine', 'kit_ext'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'r43'))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'r39'))
import planet_r36 as K                                               # noqa: E402
import plan44 as P                                                   # noqa: E402

LK, D, R = K.LK, K.D, K.LK.R
Mesh, principled, emitter, _cyl = R.Mesh, R.principled, R.emitter, R._cyl
_M = R._M
W, L = P.W, P.L


# --- materials --------------------------------------------------------------------------------------------------------
def acrylic(bpy, name, Ti=(0.995, 0.995, 0.995), d_ref=0.003, rough=0.015):
    """Cast acrylic, calibrated: IOR 1.49; Ti is the internal transmittance per channel (R, G, B) through d_ref metres
    of sheet, after the faces' Fresnel loss (which the BSDF supplies). Cycles' Volume Absorption gives
    sigma_c = density x (1 - colour_c), so density = max sigma and colour_c = 1 - sigma_c / density."""
    if name in _M:
        return _M[name]
    sig = [-math.log(max(t, 1e-4)) / d_ref for t in Ti]
    dens = max(max(sig), 1e-3)
    col = [1.0 - s / dens for s in sig]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    R._set(b, 'Base Color', (1.0, 1.0, 1.0, 1.0)); R._set(b, 'Transmission Weight', 1.0); R._set(b, 'IOR', 1.49)
    R._set(b, 'Roughness', rough)
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    va = nt.nodes.new('ShaderNodeVolumeAbsorption')
    va.inputs['Color'].default_value = (col[0], col[1], col[2], 1.0); va.inputs['Density'].default_value = dens
    nt.links.new(va.outputs['Volume'], out.inputs['Volume'])
    _M[name] = m
    return m


# the band's tint: the house's own Smoke (a warm grey-amber), internal transmittance at 3 mm (est., to be measured on
# the chosen sheet): red 0.80, green 0.62, blue 0.42
SMOKE_TI = (0.78, 0.55, 0.30)


def terrazzo(bpy, name, ground='#4A4743', chips=('#D9D4CA', '#8E8A84', '#2B2928', '#B9AE9C'), accent=(),
             scale=34.0, rough=0.32):
    """Honed epoxy terrazzo: chips (marble, glass) in a ground, sealed. `accent` adds acrylic-offcut chips in the
    product tints, as a share of the chips (each accent colour one slot in the palette)."""
    if name in _M:
        return _M[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = D._bsdf(m)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    share = 0.15 if accent else 0.0                                # accent chips: 15% of the chips
    pal = [(i * (1 - share) / len(chips), c) for i, c in enumerate(chips)] + \
          [(1 - share + i * share / len(accent), c) for i, c in enumerate(accent)]
    layers = []
    for k, sc in enumerate((scale, scale * 2.6)):
        ve = nt.nodes.new('ShaderNodeTexVoronoi'); ve.feature = 'DISTANCE_TO_EDGE'; ve.inputs['Scale'].default_value = sc
        vc = nt.nodes.new('ShaderNodeTexVoronoi'); vc.inputs['Scale'].default_value = sc
        for v in (ve, vc):
            nt.links.new(tc.outputs['Object'], v.inputs['Vector'])
        mk = nt.nodes.new('ShaderNodeMapRange'); mk.inputs['From Min'].default_value = 0.10 + 0.04 * k
        mk.inputs['From Max'].default_value = 0.13 + 0.04 * k
        nt.links.new(ve.outputs['Distance'], mk.inputs['Value'])
        sp = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(vc.outputs['Color'], sp.inputs['Color'])
        cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.interpolation = 'CONSTANT'
        els = cr.color_ramp.elements
        els[0].position = pal[0][0]; els[0].color = R.lin(pal[0][1])
        els[1].position = pal[1][0]; els[1].color = R.lin(pal[1][1])
        for pos, c in pal[2:]:
            e = els.new(pos); e.color = R.lin(c)
        nt.links.new(sp.outputs['Red'], cr.inputs['Fac'])
        layers.append((mk, cr))
    mix0 = nt.nodes.new('ShaderNodeMix'); mix0.data_type = 'RGBA'
    mix0.inputs[6].default_value = R.lin(ground)
    nt.links.new(layers[0][0].outputs['Result'], mix0.inputs['Factor']); nt.links.new(layers[0][1].outputs['Color'], mix0.inputs[7])
    mix1 = nt.nodes.new('ShaderNodeMix'); mix1.data_type = 'RGBA'
    nt.links.new(layers[1][0].outputs['Result'], mix1.inputs['Factor'])
    nt.links.new(mix0.outputs[2], mix1.inputs[6]); nt.links.new(layers[1][1].outputs['Color'], mix1.inputs[7])
    nt.links.new(mix1.outputs[2], b.inputs['Base Color'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.8; nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    rr = nt.nodes.new('ShaderNodeMapRange'); rr.inputs['To Min'].default_value = rough - 0.08; rr.inputs['To Max'].default_value = rough + 0.10
    nt.links.new(nz.outputs['Fac'], rr.inputs['Value']); nt.links.new(rr.outputs['Result'], b.inputs['Roughness'])
    R._set(b, 'Coat Weight', 0.25); R._set(b, 'Coat Roughness', 0.18)
    _M[name] = m
    return m


ACCENT = ('#B8241C', '#1F4FA8', '#E0B320', '#2F8A4A', '#D9661E', '#6A3C9C')   # the six disc tints, as offcut chips


def oak(bpy, vertical=True, name='oak-white-oiled', tint='#5C4A38', mix=0.6):
    """Oiled white oak (fumed a shade): the walnut scan pulled warm and light."""
    return D.walnut(bpy, vertical=vertical, coat=0.25, coat_rough=0.4, tint=tint, mix=mix, name='-' + name)


def quartzite(bpy):
    if 'quartzite-honed' not in _M:
        _M['quartzite-honed'] = principled(bpy, 'quartzite-honed', '#2E2D2B', rough=0.36, spec=0.5,
                                           bump=(0.004, 0.15, 0.0002))
    return _M['quartzite-honed']


def felt(bpy, colour='#151413', name='felt-black'):
    return principled(bpy, name, colour, rough=0.97, spec=0.1, sheen=0.2)


# --- pieces -----------------------------------------------------------------------------------------------------------
def _battens(m, axis, a0, a1, fixed0, fixed1, z0, z1, w, gap):
    """Vertical battens along `axis` ('x' or 'y') from a0 to a1, each w wide with gap between, between fixed0 and fixed1
    on the other horizontal axis."""
    a = a0
    while a + w <= a1 + 1e-6:
        if axis == 'x':
            m.box(a, fixed0, z0, a + w, fixed1, z1)
        else:
            m.box(fixed0, a, z0, fixed1, a + w, z1)
        a += w + gap


def shell(bpy, p, objs):
    H = P.CEIL; T = P.WALL
    fl = Mesh('h44-floor'); fl.box(-0.2, 0.0, -0.1, P.LANT['x0'], W, 0.0); fl.box(P.LANT['x1'], 0.0, -0.1, L, W, 0.0)
    fl.box(P.LANT['x0'], 0.0, -0.1, P.LANT['x1'], P.LANT['y0'], 0.0)
    objs.append(fl.object(bpy, terrazzo(bpy, 'terrazzo-floor', ground=p.get('floor_ground', '#3E3C39'))))
    wl = Mesh('h44-walls')
    wl.box(-0.30, -T, 0.0, L + T, 0.0, P.JOISTS)
    wl.box(-0.30, W, 0.0, L + T, W + T, P.JOISTS)
    wl.box(L, 0.0, 0.0, L + T, P.REAR_EXIT['y0'], P.JOISTS); wl.box(L, P.REAR_EXIT['y1'], 0.0, L + T, W, P.JOISTS)
    wl.box(L, P.REAR_EXIT['y0'], 2.13, L + T, P.REAR_EXIT['y1'], P.JOISTS)
    objs.append(wl.object(bpy, D.plaster(bpy, p, name='h44-plaster', colour=p.get('plaster', '#8F877B'))))
    ce = Mesh('h44-ceiling'); ce.box(-0.30, -T, H, L + T, W + T, H + 0.05)
    objs.append(ce.object(bpy, principled(bpy, 'h44-acoustic-plaster', p.get('ceiling', '#26231F'), rough=0.95, spec=0.2)))
    # linear slot diffusers in the ceiling over the route and the bar, and the downlights' black trims
    sd = Mesh('h44-slots')
    sd.box(1.0, 0.70, H - 0.002, P.LANT['x0'] - 1.8, 0.74, H); sd.box(P.SHOP_X1 + 0.5, W - 2.10, H - 0.002, P.LANT['x0'] - 0.6, W - 2.06, H)
    for x in [1.6 + 1.45 * i for i in range(8)]:
        _cyl(sd.bm, x, 3.4, H - 0.004, 0.045, 0.004, seg=20)
    for x in P.STOOLS + [7.6, 8.4]:
        _cyl(sd.bm, x, P.COUNTER['y0'] + 0.25, H - 0.004, 0.04, 0.004, seg=20)
    objs.append(sd.object(bpy, principled(bpy, 'h44-trim-black', '#0C0C0C', rough=0.6)))
    # the rear lobby and rooms' partitions (seen down the route), plain plaster
    rp = Mesh('h44-rear')
    rp.box(P.LOBBY['x1'], P.ROUTE_Y[1], 0.0, P.LOBBY['x1'] + 0.12, W, P.CEIL_REAR)
    for i in (1, 2):
        rp.box(P.LOBBY['x1'], P.ROUTE_Y[1] + 2.0 * i - 0.06, 0.0, L, P.ROUTE_Y[1] + 2.0 * i + 0.06, P.CEIL_REAR)
    rp.box(P.LOBBY['x0'], P.ROUTE_Y[1], P.CEIL_REAR, L, W, P.CEIL_REAR + 0.05)
    objs.append(rp.object(bpy, D.plaster(bpy, p, name='h44-plaster', colour=p.get('plaster', '#8F877B'))))
    # the rear exit door, steel, with a lit exit sign
    rd = Mesh('h44-rear-door'); rd.box(L - 0.05, P.REAR_EXIT['y0'] + 0.01, 0.0, L - 0.01, P.REAR_EXIT['y1'] - 0.01, 2.12)
    objs.append(rd.object(bpy, principled(bpy, 'h44-door-steel', '#2A2928', rough=0.5, metal=0.5)))


def shopfront(bpy, p, objs):
    """Blackened steel and clear glass on an 18 in terrazzo bulkhead; the entry alcove and its glass vestibule."""
    T = P.WALL; H = P.JOISTS
    sf = Mesh('h44-storefront'); gl = Mesh('h44-glass')
    y0, y1 = P.GLASS
    sf.box(-0.12, y0 - 0.06, 0.0, 0.0, y0, H)                         # the mullion by the entry
    sf.box(-0.12, W - 0.04, 0.0, 0.0, W + T, H)
    sf.box(-0.12, (y0 + y1) / 2 - 0.03, P.BULKHEAD, 0.0, (y0 + y1) / 2 + 0.03, 3.30)
    sf.box(-0.14, -T, 3.30, 0.0, W + T, 3.38)                          # the transom bar
    sf.box(-0.30, -T, 3.38, 0.0, W + T, H)                             # the fascia above (the sign band)
    sf.box(-0.30, -T, 0.0, 0.0, P.ENTRY['y0'], H)                     # the pier at the right
    # the entry alcove: the outer door frame at x = 0.90 and the vestibule's glass walls to x = 3.20
    V = P.VEST
    for x in (V['x0'], V['x1']):
        sf.box(x - 0.03, V['y0'], 0.0, x + 0.03, V['y0'] + 0.05, 2.40)
        sf.box(x - 0.03, V['y1'] - 0.05, 0.0, x + 0.03, V['y1'], 2.40)
        sf.box(x - 0.03, V['y0'], 2.34, x + 0.03, V['y1'], 2.40)
    sf.box(0.0, V['y1'], 0.0, V['x1'], V['y1'] + 0.05, 2.40)          # the vestibule's inner side, a steel frame
    sf.box(0.0, V['y1'], 2.40, V['x1'], V['y1'] + 0.05, 2.46)
    objs.append(sf.object(bpy, K.blackened_steel(bpy), bevel=0.002))
    bk = Mesh('h44-bulkhead'); bk.box(-0.12, y0, 0.0, 0.0, W, P.BULKHEAD)
    objs.append(bk.object(bpy, terrazzo(bpy, 'terrazzo-floor'), bevel=0.004))
    gl.box(-0.07, y0, P.BULKHEAD, -0.06, W - 0.04, 3.30)
    gl.box(-0.07, -0.0, 3.38, -0.06, W, 3.38)                          # (no transom glass: the fascia is solid)
    for x in (V['x0'], V['x1']):                                       # the two doors, glass in steel stiles
        gl.box(x - 0.01, V['y0'] + 0.08, 0.05, x + 0.01, V['y1'] - 0.08, 2.32)
    gl.box(0.05, V['y1'] + 0.015, 0.05, V['x1'] - 0.05, V['y1'] + 0.035, 2.36)
    if not p.get('no_glass'):
        objs.append(gl.object(bpy, R.thin_glass(bpy, p.get('glass_gloss', 0.7))))


def shop(bpy, p, objs):
    S = P.SHOP_WALL
    sh = Mesh('h44-shop-oak'); st = Mesh('h44-shop-steel')
    for z in (0.30, 0.78, 1.26, 1.74, 2.22, 2.70):
        sh.box(S['x0'], S['y0'], z - 0.035, S['x1'], W, z)
    for x in [S['x0'] + 0.9 * i for i in range(7)]:
        st.box(x, W - 0.04, 0.0, x + 0.03, W - 0.01, S['z1'])
    sh.box(S['x0'], W - 0.02, 0.0, S['x1'], W, S['z1'])               # an oak back panel
    objs.append(sh.object(bpy, oak(bpy, vertical=False, name='oak-shop'), bevel=0.003))
    objs.append(st.object(bpy, K.blackened_steel(bpy)))
    # the shelf-edge light: a warm line under each shelf's front, hidden
    sl = Mesh('h44-shelf-led')
    for z in (0.78, 1.26, 1.74, 2.22, 2.70):
        sl.box(S['x0'] + 0.05, S['y0'] + 0.02, z - 0.040, S['x1'] - 0.05, S['y0'] + 0.035, z - 0.036)
    objs.append(sl.object(bpy, emitter(bpy, 'h44-led-warm', '#FFB774', p.get('shelf_led', 6.0))))
    T_ = P.SHOP_TABLE
    tb = Mesh('h44-shop-table'); tb.box(T_['x0'], T_['y0'], T_['h'] - 0.04, T_['x1'], T_['y1'], T_['h'])
    objs.append(tb.object(bpy, oak(bpy, vertical=False, name='oak-table'), bevel=0.004))
    tf = Mesh('h44-shop-table-frame')
    for x in (T_['x0'] + 0.08, T_['x1'] - 0.12):
        tf.box(x, T_['y0'] + 0.08, 0.0, x + 0.04, T_['y1'] - 0.08, T_['h'] - 0.04)
    objs.append(tf.object(bpy, K.blackened_steel(bpy)))
    Wp = P.WINDOW_PLINTH
    wp = Mesh('h44-window-plinth'); wp.box(Wp['x0'], Wp['y0'], 0.0, Wp['x1'], Wp['y1'], Wp['h'])
    objs.append(wp.object(bpy, terrazzo(bpy, 'terrazzo-floor'), bevel=0.004))


def bar(bpy, p, objs):
    C, B = P.COUNTER, P.BACKBAR
    # the counter body: a terrazzo die with the offcut accent, an oak kick, a quartzite top with a soft nosing
    die = Mesh('h44-bar-die'); die.box(C['x0'], C['y0'], 0.12, C['x1'], C['y_work'], 1.03)
    objs.append(die.object(bpy, terrazzo(bpy, 'terrazzo-accent', ground='#4A4743', accent=ACCENT, scale=30.0), bevel=0.006))
    kk = Mesh('h44-bar-kick'); kk.box(C['x0'] + 0.03, C['y0'] + 0.06, 0.0, C['x1'] - 0.03, C['y_work'], 0.12)
    objs.append(kk.object(bpy, K.blackened_steel(bpy)))
    top = Mesh('h44-bar-top')
    top.box(C['x0'] - 0.04, C['edge'], 1.04, C['x1'] + 0.04, C['y_work'] + 0.05, 1.07)
    top.box(C['x0'] - 0.04, P.COUNTER['y0'], P.LOW_END['top_z'] - 0.03, P.LOW_END['x1'], P.COUNTER['y0'] + 0.01, P.LOW_END['top_z'])
    objs.append(top.object(bpy, quartzite(bpy), bevel=0.012, seg=4))
    # the accessible low end: a 60 in run at 34 in, cut into the counter's near end (a lower shelf in quartzite)
    lo = Mesh('h44-bar-low'); lo.box(C['x0'], C['edge'] - 0.10, P.LOW_END['top_z'] - 0.03, P.LOW_END['x1'], C['y0'], P.LOW_END['top_z'])
    objs.append(lo.object(bpy, quartzite(bpy), bevel=0.008))
    fr = Mesh('h44-footrail')
    LK._rod(fr.bm, (P.LOW_END['x1'] + 0.1, C['y0'] - 0.12, 0.22), (C['x1'] - 0.1, C['y0'] - 0.12, 0.22), 0.022, 0.022, seg=16)
    for x in (P.LOW_END['x1'] + 0.2, (P.LOW_END['x1'] + C['x1']) / 2, C['x1'] - 0.2):
        LK._rod(fr.bm, (x, C['y0'] - 0.12, 0.22), (x, C['y0'], 0.22), 0.012, 0.012, seg=10)
    objs.append(fr.object(bpy, K.brass(bpy), smooth=True))
    # the back bar: oak doors under a quartzite work top; three blackened-steel shelves of bottles, lit from beneath
    bb = Mesh('h44-backbar'); bb.box(B['x0'], B['y0'], 0.0, B['x1'], B['y1'], B['h'] - 0.03)
    objs.append(bb.object(bpy, oak(bpy, name='oak-backbar'), bevel=0.004))
    bt = Mesh('h44-backbar-top'); bt.box(B['x0'], B['y0'] - 0.02, B['h'] - 0.03, B['x1'], B['y1'], B['h'])
    objs.append(bt.object(bpy, quartzite(bpy), bevel=0.006))
    sv = Mesh('h44-bb-shelves'); led = Mesh('h44-bb-led')
    zs = (1.45, 1.85, 2.25)
    for z in zs:
        sv.box(B['x0'] + 0.3, W - 0.30, z - 0.02, B['x1'] - 0.3, W, z)
        led.box(B['x0'] + 0.35, W - 0.28, z - 0.024, B['x1'] - 0.35, W - 0.26, z - 0.021)
    objs.append(sv.object(bpy, K.blackened_steel(bpy)))
    objs.append(led.object(bpy, emitter(bpy, 'h44-led-warm', '#FFB774', p.get('shelf_led', 6.0))))
    # bottles: glass with liquid in four warm tones, varied heights
    import kit39
    rnd = random.Random(44)
    gm = kit39._glass(bpy)
    liq = [kit39._liquid(bpy, c, f'h44-liq-{c[1:]}') for c in ('#7A3A12', '#B5651D', '#D9C27A', '#3B1F10')]
    bots = [Mesh(f'h44-bottles') for _ in range(1)][0]
    lm = [Mesh(f'h44-liq{i}') for i in range(4)]
    for z in zs:
        x = B['x0'] + 0.38
        while x < B['x1'] - 0.42:
            r = rnd.choice([0.035, 0.040, 0.045]); h = rnd.choice([0.24, 0.28, 0.30, 0.32])
            y = W - 0.15 + rnd.uniform(-0.04, 0.04)
            _cyl(bots.bm, x, y, z, r, h * 0.72, seg=20); _cyl(bots.bm, x, y, z + h * 0.72, r * 0.35, h * 0.28, seg=12)
            _cyl(lm[rnd.randrange(4)].bm, x, y, z + 0.004, r - 0.004, h * 0.6, seg=20)
            x += 2 * r + rnd.uniform(0.02, 0.08)
    objs.append(bots.object(bpy, gm, smooth=True))
    for i in range(4):
        objs.append(lm[i].object(bpy, liq[i], smooth=True))
    # the kit alcove's gasketed door, flush oak, at the shop end of the back bar
    A = P.KIT_ALCOVE
    kd = Mesh('h44-kit-wall'); kd.box(A['x0'], A['y0'] - 0.10, 0.0, A['x1'], A['y0'], P.CEIL)
    kd.box(A['x1'] - 0.10, A['y0'], 2.20, A['x1'], W, P.CEIL)
    objs.append(kd.object(bpy, D.plaster(bpy, p, name='h44-plaster', colour=p.get('plaster', '#8F877B'))))
    dd = Mesh('h44-kit-door'); dd.box(A['x1'] - 0.08, A['y0'] + 0.25, 0.0, A['x1'] - 0.03, W - 0.20, 2.18)
    objs.append(dd.object(bpy, oak(bpy, name='oak-backbar'), bevel=0.003))
    # stools: oak seat, blackened-steel frame, 30 in high
    ss = Mesh('h44-stool-steel'); so = Mesh('h44-stool-oak')
    for x in P.STOOLS:
        _cyl(ss.bm, x, P.STOOL_Y, 0.0, 0.20, 0.015, seg=32); _cyl(ss.bm, x, P.STOOL_Y, 0.015, 0.025, 0.72, seg=12)
        _cyl(ss.bm, x, P.STOOL_Y, 0.28, 0.17, 0.012, seg=32)
        _cyl(so.bm, x, P.STOOL_Y, 0.735, 0.19, 0.04, seg=40)
    objs.append(ss.object(bpy, K.blackened_steel(bpy), smooth=True))
    objs.append(so.object(bpy, oak(bpy, vertical=False, name='oak-stool'), smooth=True, bevel=0.006))
    # the banquette: oak frame, oxblood leather, its back to the route (a rail at 1.05)
    Bq = P.BANQ
    bq = Mesh('h44-banq-oak'); bq.box(Bq['x0'], Bq['y0'], 0.0, Bq['x1'], Bq['y1'], 0.40)
    bq.box(Bq['x0'], Bq['y0'], 0.40, Bq['x1'], Bq['y0'] + 0.08, Bq['back'])
    objs.append(bq.object(bpy, oak(bpy, name='oak-banq'), bevel=0.004))
    up = Mesh('h44-banq-leather'); up.box(Bq['x0'] + 0.02, Bq['y0'] + 0.08, 0.40, Bq['x1'] - 0.02, Bq['y1'], 0.47)
    up.box(Bq['x0'] + 0.02, Bq['y0'] + 0.08, 0.50, Bq['x1'] - 0.02, Bq['y0'] + 0.16, 0.92)
    objs.append(up.object(bpy, K.leather(bpy, '#4A1E17', name='h44-leather'), bevel=0.02))
    tt = Mesh('h44-banq-tables'); tl = Mesh('h44-banq-table-steel')
    for x in P.BANQ_TABLES:
        y0 = Bq['y1'] + 0.08
        tt.box(x - P.BANQ_TABLE['w'] / 2, y0, 0.72, x + P.BANQ_TABLE['w'] / 2, y0 + P.BANQ_TABLE['d'], 0.75)
        _cyl(tl.bm, x, y0 + 0.30, 0.0, 0.025, 0.72, seg=12); _cyl(tl.bm, x, y0 + 0.30, 0.0, 0.22, 0.012, seg=32)
    objs.append(tt.object(bpy, quartzite(bpy), bevel=0.005))
    objs.append(tl.object(bpy, K.blackened_steel(bpy), smooth=True))


def lantern(bpy, p, objs):
    """The box: a slotted oak baffle on the bar's side, plain oak boards along the route, a band of lit Smoke acrylic
    fins under the ceiling on both seen faces, a lit line under the baffle's foot; the porch; and inside, the room."""
    Lt = P.LANT; x0, x1, y0, y1, h = Lt['x0'], Lt['x1'], Lt['y0'], Lt['y1'], Lt['h']
    bz0, bz1 = P.BAND['z0'], P.BAND['z1']
    oakm = oak(bpy, name='oak-lantern')
    blk = felt(bpy)
    # the outer leaf behind the oak, black (seen through the slots and the fins)
    bk = Mesh('h44-lant-back')
    bk.box(x0 + 0.02, y0 + 0.02, 0.0, x1, y1, bz0 - 0.03)
    bk.box(x0 + 0.08, y0 + 0.08, bz0 - 0.03, x1, y1, h)                     # behind the band's diffuser
    objs.append(bk.object(bpy, blk))
    # the front baffle: 60 mm battens, 12 mm slots, from the lit foot to the band; the porch covers its route end
    bf = Mesh('h44-lant-baffle')
    _battens(bf, 'y', y0, y1, x0 - 0.02, x0 + 0.02, 0.10, bz0 - 0.02, 0.060, 0.012)
    bf.box(x0 - 0.03, y0, bz0 - 0.03, x0 + 0.02, y1, bz0)                      # a top rail under the band
    # the route side: 140 mm boards with a 6 mm shadow, from the foot to the band
    _battens(bf, 'x', x0, x1, y0 - 0.02, y0 + 0.02, 0.10, bz0 - 0.02, 0.140, 0.006)
    bf.box(x0, y0 - 0.03, bz0 - 0.03, x1, y0 + 0.02, bz0)
    objs.append(bf.object(bpy, oakm, bevel=0.002))
    # the band: fins 20 mm thick on a 60 mm pitch, 60 mm deep into the cavity, in the outer cavity; behind them the
    # LED-lit diffuser (white, warm); a steel cap above and a sill below
    fins = Mesh('h44-fins'); diff = Mesh('h44-band-diffuser'); cap = Mesh('h44-band-steel')
    a = y0 + 0.02
    while a < y1 - 0.02:
        fins.box(x0 - 0.02, a, bz0, x0 + 0.04, a + P.BAND['fins'], bz1 - 0.02); a += P.BAND['pitch']
    a = x0 + 0.02
    while a < x1 - 0.02:
        fins.box(a, y0 - 0.02, bz0, a + P.BAND['fins'], y0 + 0.04, bz1 - 0.02); a += P.BAND['pitch']
    diff.box(x0 + 0.06, y0 + 0.06, bz0, x0 + 0.07, y1, bz1 - 0.02)
    diff.box(x0 + 0.06, y0 + 0.06, bz0, x1, y0 + 0.07, bz1 - 0.02)
    cap.box(x0 - 0.035, y0 - 0.035, bz1 - 0.02, x1, y1, bz1)
    cap.box(x0 - 0.035, y0 - 0.035, bz0 - 0.008, x1, y0 + 0.05, bz0)
    cap.box(x0 - 0.035, y0 - 0.035, bz0 - 0.008, x0 + 0.05, y1, bz0)
    objs.append(fins.object(bpy, acrylic(bpy, 'acrylic-smoke-fin', SMOKE_TI)))
    objs.append(diff.object(bpy, emitter(bpy, 'h44-band-led', '#FFB46A', p.get('band_glow', 3.0))))
    objs.append(cap.object(bpy, K.blackened_steel(bpy)))
    # the lit foot: a 100 mm recess with a warm line washing the floor
    ft = Mesh('h44-lant-foot'); ft.box(x0 + 0.04, y0 + 0.04, 0.0, x1, y1, 0.10)
    objs.append(ft.object(bpy, blk))
    fl = Mesh('h44-lant-footled'); fl.box(x0 + 0.045, y0 + 0.045, 0.085, x0 + 0.055, y1, 0.095)
    fl.box(x0 + 0.045, y0 + 0.045, 0.085, x1, y0 + 0.055, 0.095)
    objs.append(fl.object(bpy, emitter(bpy, 'h44-foot-led', '#FFB774', p.get('foot_glow', 4.0))))
    # the porch: a small oak box outside the seal, its door off the route, an acoustic door into the box
    Lk = P.LOCK
    pc = Mesh('h44-porch')
    hp = 2.70
    pc.box(Lk['x0'], Lk['y1'] - 0.12, 0.0, Lk['x1'], Lk['y1'], hp)                       # its bar-side wall
    pc.box(Lk['x0'], Lk['y0'], 0.0, Lk['x0'] + 0.12, Lk['y1'], hp)                       # its shop-side wall
    pc.box(Lk['x0'], Lk['y0'], 0.0, P.LOCK_DOOR1['x'], Lk['y0'] + 0.12, hp)              # the route face, beside door 1
    pc.box(P.LOCK_DOOR1['x'] + P.DOOR, Lk['y0'], 0.0, Lk['x1'], Lk['y0'] + 0.12, hp)
    pc.box(P.LOCK_DOOR1['x'], Lk['y0'], 2.13, P.LOCK_DOOR1['x'] + P.DOOR, Lk['y0'] + 0.12, hp)
    pc.box(Lk['x0'], Lk['y0'], hp - 0.08, Lk['x1'], Lk['y1'], hp)                       # its roof
    objs.append(pc.object(bpy, oakm, bevel=0.003))
    pd = Mesh('h44-porch-door'); pd.box(P.LOCK_DOOR1['x'] + 0.01, Lk['y0'] + 0.03, 0.0, P.LOCK_DOOR1['x'] + P.DOOR - 0.01, Lk['y0'] + 0.08, 2.12)
    objs.append(pd.object(bpy, oak(bpy, vertical=True, name='oak-door', tint='#4E3622'), bevel=0.003))
    pl = Mesh('h44-porch-pull'); pl.box(P.LOCK_DOOR1['x'] + P.DOOR - 0.10, Lk['y0'] + 0.0, 0.85, P.LOCK_DOOR1['x'] + P.DOOR - 0.08, Lk['y0'] + 0.03, 1.25)
    objs.append(pl.object(bpy, K.brass(bpy)))
    # the porch's name in cut brass letters is a later decision; for now a small lit push plate (the power operator)
    pp = Mesh('h44-push'); pp.box(P.LOCK_DOOR1['x'] - 0.25, Lk['y0'] - 0.005, 0.95, P.LOCK_DOOR1['x'] - 0.13, Lk['y0'], 1.07)
    objs.append(pp.object(bpy, principled(bpy, 'h44-push', '#C9C2B6', rough=0.4, metal=0.6)))
    if p.get('interior', True):
        interior(bpy, p, objs)


def interior(bpy, p, objs):
    I = P.INNER; x0, x1, y0, y1, h = I['x0'], I['x1'], I['y0'], I['y1'], I['h']
    import kit43
    oakm = oak(bpy, name='oak-lantern')
    fl = Mesh('h44-in-floor'); fl.box(x0 - 0.3, y0 - 0.3, -0.1, x1 + 0.3, y1 + 0.3, 0.0)
    objs.append(fl.object(bpy, K.end_grain(bpy, name='h44-endgrain', lo='#3A2818', hi='#B08A60')))
    # the inner leaf, black felt behind the slats; the walls 45 mm slats with 15 mm gaps (absorber behind) on 35% of
    # the side walls (the upper part), plain oak boards below to 1.2 m (the seats lean on them)
    bk = Mesh('h44-in-back')
    bk.box(x0 - 0.02, y0 - 0.02, 0.0, x0, y1 + 0.02, h); bk.box(x1, y0 - 0.02, 0.0, x1 + 0.02, y1 + 0.02, h)
    bk.box(x0, y0 - 0.02, 0.0, x1, y0, h); bk.box(x0, y1, 0.0, x1, y1 + 0.02, h)
    objs.append(bk.object(bpy, felt(bpy)))
    sl = Mesh('h44-in-slats')
    for (yy, d) in ((y0, 1), (y1, -1)):
        a, b = sorted((yy, yy + d * 0.03))
        _battens(sl, 'x', x0, P.TRAP['x0'], a, b, 1.20, h, 0.045, 0.015)
        a2, b2 = sorted((yy, yy + d * 0.02))
        sl.box(x0, a2, 0.0, P.TRAP['x0'], b2, 1.20)                                       # the wainscot board
    # the front wall: plain oak boards with the door at the route end, the selector's niche at the far end
    sl.box(x0, y0 + 1.10, 0.0, x0 + 0.02, y1, h)
    objs.append(sl.object(bpy, oakm, bevel=0.0015))
    # the lid: 45 mm slats across the room with 25 mm gaps over the absorber, and two rows of small spots
    ld = Mesh('h44-in-lid')
    _battens(ld, 'x', x0, x1, y0, y1, h - 0.03, h, 0.045, 0.025)
    objs.append(ld.object(bpy, oakm, bevel=0.0015))
    lb = Mesh('h44-in-lid-back'); lb.box(x0, y0, h, x1, y1, h + 0.02)
    objs.append(lb.object(bpy, felt(bpy)))
    # the bass-trap wall at the back: 900 mm deep, its face 60 mm battens with 30 mm slots (wool behind), a bench in it
    T_ = P.TRAP
    tr = Mesh('h44-trap'); _battens(tr, 'y', y0, y1, T_['x0'], T_['x0'] + 0.04, P.BENCH['z'] + 0.05, h - 0.03, 0.060, 0.030)
    tr.box(P.BENCH['x0'], y0, 0.0, T_['x0'], y1, P.BENCH['z'])                          # the bench, solid oak
    objs.append(tr.object(bpy, oakm, bevel=0.002))
    tb = Mesh('h44-trap-back'); tb.box(T_['x0'] + 0.04, y0, 0.0, T_['x1'], y1, h)
    objs.append(tb.object(bpy, felt(bpy)))
    cu = Mesh('h44-bench-cushion'); cu.box(P.BENCH['x0'] + 0.02, y0 + 0.05, P.BENCH['z'], T_['x0'] - 0.02, y1 - 0.05, P.BENCH['z'] + 0.07)
    cu.box(T_['x0'] - 0.10, y0 + 0.05, P.BENCH['z'] + 0.12, T_['x0'] - 0.01, y1 - 0.05, P.BENCH['z'] + 0.50)
    objs.append(cu.object(bpy, K.mohair(bpy, p.get('mohair', '#4A4038'), 'h44-mohair'), bevel=0.02))
    # the lit line under the bench's front (vertical, never trodden on)
    bl = Mesh('h44-bench-led'); bl.box(P.BENCH['x0'] + 0.02, y0, 0.02, P.BENCH['x0'] + 0.03, y1, 0.05)
    objs.append(bl.object(bpy, emitter(bpy, 'h44-foot-led', '#FFB774', p.get('foot_glow', 4.0))))
    # the rug, the chairs (the wheelchair space left clear, beside its companion chair), side tables
    rg = Mesh('h44-rug'); rg.box(P.SWEET[0] - 1.6, y0 + 0.55, 0.0, P.BENCH['x0'] - 0.15, y1 - 0.55, 0.012)
    objs.append(rg.object(bpy, principled(bpy, 'h44-rug', p.get('rug', '#3E3833'), rough=0.97, spec=0.1, bump=(0.004, 0.5, 0.001))))
    stl, wood, uph = Mesh('h44-chair-steel'), Mesh('h44-chair-oak'), Mesh('h44-chair-wool')
    for (x, y, kind) in P.SEATS:
        if kind in ('chair', 'companion'):
            face = math.degrees(math.atan2(P.SWEET[1] - y, (P.STACK_X - 6.0) - x)) if False else 180.0
            kit43._chair(stl, wood, uph, x, y, face)
    objs.append(stl.object(bpy, K.blackened_steel(bpy), smooth=True))
    objs.append(wood.object(bpy, oakm, bevel=0.004))
    objs.append(uph.object(bpy, K.mohair(bpy, p.get('mohair', '#4A4038'), 'h44-mohair'), bevel=0.01))
    # the speakers' plinths: terrazzo, 0.40 high
    pk = Mesh('h44-stack-plinths')
    for (x, y) in P.STACKS:
        pk.box(x - 0.36, y - 0.36, 0.0, x + 0.36, y + 0.36, P.TROPOS['plinth'])
    objs.append(pk.object(bpy, terrazzo(bpy, 'terrazzo-floor'), bevel=0.006))
    # the selector's desk at the front corner: oak, the decks on it, records below
    Sd = P.SELECTOR
    sd = Mesh('h44-selector'); sd.box(Sd['x0'] + 0.05, Sd['y0'], 0.0, Sd['x1'], Sd['y1'] - 0.05, Sd['h'])
    objs.append(sd.object(bpy, oakm, bevel=0.004))
    tt = Mesh('h44-decks')
    for dy in (0.45, 1.25):
        tt.box(Sd['x0'] + 0.18, Sd['y0'] + dy - 0.22, Sd['h'], Sd['x0'] + 0.62, Sd['y0'] + dy + 0.22, Sd['h'] + 0.10)
    objs.append(tt.object(bpy, principled(bpy, 'h44-deck', '#1A1A1A', rough=0.35, metal=0.3), bevel=0.006))
    pl = Mesh('h44-platters')
    for dy in (0.45, 1.25):
        _cyl(pl.bm, Sd['x0'] + 0.40, Sd['y0'] + dy, Sd['h'] + 0.10, 0.15, 0.012, seg=48)
    objs.append(pl.object(bpy, principled(bpy, 'h44-vinyl', '#0B0B0C', rough=0.25), smooth=True))
    # the inner door, at the front's route end (seen closed)
    dd = Mesh('h44-in-door'); dd.box(x0, P.LOCK_DOOR2['y'] + 0.02, 0.0, x0 + 0.06, P.LOCK_DOOR2['y'] + P.DOOR - 0.02, 2.12)
    objs.append(dd.object(bpy, oak(bpy, vertical=True, name='oak-door', tint='#4E3622'), bevel=0.003))


def mother(bpy, p, objs):
    """Mother EARF at 1.25 m on a 0.80 x 0.40 m terrazzo plinth (the acrylic-offcut accent), by kit43ams.globe."""
    import kit43ams
    M = P.MOTHER
    q = {'size': M['d'], 't': 0.025, 'at': [M['x'], M['y']], 'rim': p.get('mother_rim', 0.06), 'rim_par': 1.0,
         'heading': p.get('mother_heading', 30.0), 'base_h': M['plinth_h'], 'post': 0.08, 'base_r': M['plinth_d'] / 2}
    obs = kit43ams.globe(bpy, 'h44-mother', q, None)
    tz = terrazzo(bpy, 'terrazzo-accent', ground='#4A4743', accent=ACCENT, scale=30.0)
    for ob in obs:
        if ob.name.startswith('h44-mother-base'):
            ob.data.materials.clear(); ob.data.materials.append(tz)
    objs.extend(obs)


def house(bpy, name, p, kit):
    objs = []
    shell(bpy, p, objs)
    shopfront(bpy, p, objs)
    shop(bpy, p, objs)
    bar(bpy, p, objs)
    lantern(bpy, p, objs)
    if p.get('mother', True):
        mother(bpy, p, objs)
    if p.get('street', True):
        import kit43
        kit43.street(bpy, kit, p, objs)
    return objs
