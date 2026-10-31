"""Planet EARF, round 43: the pop-up room (drawing A-401, `r42/popup42.py`) as one kit `ext` piece, by path.

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r43/kit43.py", "fn": "popup", ...}

A vacant downtown storefront, 25 x 50 ft, 13 ft to a dark painted ceiling, and nothing built in: what the pop-up brings
is portable and leaves with the licence. Front to back (x from the glass, y from the right-hand wall, as popup42):
- the window: a Tropos pair on a low black plinth, facing the street;
- the shop: blackened-steel and oak shelving on both walls (the round 42 shop wall, which moves to the flagship), the
  Cores on the right, records, Mantle and the coins; a long walnut table with the till at its end;
- the bar: a 2.4 m portable bar in oak with a zinc top, poured by the licensed partner, and four standing ledges;
- the listening room: charcoal felt drapes on a ceiling track with an opening, a rug, ten chairs in two rows facing a
  Tropos on an oak plinth either side, the decks on a table by the drape;
- the back: a plaster partition with the WC and store door.
The products themselves (Tropos, Core, Hemisphere, Mantle, the coins) are their own models, placed by the shot
(`r43_shots.py`). The materials are the studio's (planet_loft, planet_den, planet_r36), so the pop-up and the flagship
read as one house.
"""
import math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine', 'kit_ext'))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'r42'))
import planet_r36 as K                                               # noqa: E402
import popup42 as Q                                                  # noqa: E402

LK, D, R = K.LK, K.D, K.LK.R
Mesh, principled, emitter, _cyl = R.Mesh, R.principled, R.emitter, R._cyl

SHELF = [0.30, 0.78, 1.26, 1.70, 2.12]                               # shelf tops (m)


def _shelving(bpy, p, objs, name, x0, x1, side, shelves, d=0.40):
    """One run of shelving against a side wall: blackened-steel uprights every ~1.2 m, oiled oak shelves, a warm LED
    under each shelf's front edge (facing down and back), a dark back panel. `side` 'right' (y = 0) or 'left' (y = W)."""
    W = Q.W
    y_wall, sgn = (0.0, 1.0) if side == 'right' else (W, -1.0)
    yf = y_wall + sgn * d                                           # the shelves' front edge
    ya, yb = sorted((y_wall + sgn * 0.012, yf))
    st, oak, bk, led = Mesh(f'{name}-steel'), Mesh(f'{name}-oak'), Mesh(f'{name}-back'), Mesh(f'{name}-led')
    top = shelves[-1] + 0.10
    b0, b1 = sorted((y_wall + sgn * 0.002, y_wall + sgn * 0.012))
    bk.box(x0, b0, 0.0, x1, b1, top)
    n = max(2, int(round((x1 - x0) / 1.2)) + 1)
    for k in range(n):
        xu = x0 + (x1 - x0) * k / (n - 1)
        st.box(xu - 0.02, ya, 0.0, xu + 0.02, yb, top)
    for k, z in enumerate(shelves):
        oak.box(x0 + 0.02, ya, z - 0.03, x1 - 0.02, yb, z)
        if k:
            la, lb = sorted((yf - sgn * 0.03, yf - sgn * 0.045))
            led.box(x0 + 0.05, la, z - 0.037, x1 - 0.05, lb, z - 0.031)
    objs.append(st.object(bpy, K.blackened_steel(bpy)))
    objs.append(oak.object(bpy, K.dark_oak(bpy, name='oak-popup'), bevel=0.003))
    objs.append(bk.object(bpy, principled(bpy, 'popup-shelfback', '#2A2420', rough=0.85)))
    lamp = led.object(bpy, emitter(bpy, f'popup-led-{p.get("led", 3.0)}', '#FFB565', p.get('led', 3.0)))
    lamp.visible_camera = False; lamp.visible_glossy = False
    objs.append(lamp)


def _records(bpy, objs, name, x0, x1, side, z, seed=43, depth=0.31):
    """Sleeves on edge, spines out, in a shelf's bay."""
    W = Q.W
    y_wall, sgn = (0.0, 1.0) if side == 'right' else (W, -1.0)
    rnd = random.Random(seed)
    cols = ['#1d1b19', '#c9bfae', '#8a2f22', '#2f4a5e', '#d8c27a', '#3c3a36', '#e7e2d8', '#6b4a2e', '#24302a']
    meshes = {c: Mesh(f'{name}-{c}') for c in cols}
    ya, yb = sorted((y_wall + sgn * 0.02, y_wall + sgn * (0.02 + depth)))
    x = x0
    while x < x1:
        w = 0.004 + rnd.random() * 0.004
        meshes[rnd.choice(cols)].box(x, ya, z, x + w, yb, z + 0.312 - rnd.random() * 0.004)
        x += w + 0.0015
    for c, m in meshes.items():
        objs.append(m.object(bpy, principled(bpy, f'popup-lp-{c}', c, rough=0.7)))


def _chair(stl, wood, uph, x, y, face):
    """A low lounge chair for the listening rows: a steel sled base, an oak shell seat and back, a wool pad."""
    f = math.radians(face)
    c, s = math.cos(f), math.sin(f)

    def P(u, v, z):                                                 # u along `face` (forward), v across
        return (x + u * c - v * s, y + u * s + v * c, z)
    for v in (-0.24, 0.24):                                         # the sled runners and the legs
        LK._rod(stl.bm, P(-0.26, v, 0.012), P(0.26, v, 0.012), 0.009, 0.009, seg=10)
        LK._rod(stl.bm, P(0.22, v, 0.012), P(0.18, v, 0.38), 0.009, 0.009, seg=10)
        LK._rod(stl.bm, P(-0.22, v, 0.012), P(-0.18, v, 0.38), 0.009, 0.009, seg=10)
    # the seat, its pad and the raked back, as slabs
    seat =[P(u, v, z) for (u, v, z) in ((-0.25, -0.27, 0.38), (0.25, -0.27, 0.38), (0.25, 0.27, 0.38), (-0.25, 0.27, 0.38))]
    _slab(wood, seat, 0.025)
    pad = [P(u, v, z) for (u, v, z) in ((-0.22, -0.24, 0.405), (0.22, -0.24, 0.405), (0.22, 0.24, 0.405), (-0.22, 0.24, 0.405))]
    _slab(uph, pad, 0.05)
    back = [P(-0.25, -0.27, 0.42), P(-0.25, 0.27, 0.42), P(-0.36, 0.27, 0.80), P(-0.36, -0.27, 0.80)]
    _slab(wood, back, 0.022, normal=(c, s))


def _slab(m, pts, t, normal=None):
    """A quad extruded by t: up (z) or along `normal` (a horizontal direction)."""
    nx, ny, nz = (0.0, 0.0, 1.0) if normal is None else (normal[0], normal[1], 0.0)
    a = [m.bm.verts.new(p) for p in pts]
    b = [m.bm.verts.new((p[0] + nx * t, p[1] + ny * t, p[2] + nz * t)) for p in pts]
    m.bm.faces.new(a[::-1]); m.bm.faces.new(b)
    for i in range(4):
        j = (i + 1) % 4
        m.bm.faces.new([a[i], a[j], b[j], b[i]])


def street(bpy, kit, p, objs):
    """Outside the glass: the sidewalk, the kerb and the road, and the building opposite with a few lit windows."""
    sw = Mesh('popup-sidewalk'); sw.box(-3.6, -30.0, -0.15, -0.20, Q.W + 30.0, 0.0)
    objs.append(sw.object(bpy, R._pbr(bpy, kit, 'concrete_pavement', res='2k', tint=p.get('pavement', '#2E2C29'), tint_mix=0.7)))
    rd = Mesh('popup-road'); rd.box(-16.0, -30.0, -0.30, -3.6, Q.W + 30.0, -0.15)
    objs.append(rd.object(bpy, principled(bpy, 'popup-asphalt', '#1C1C1D', rough=0.55, bump=(0.004, 0.3, 0.0004))))
    fa = Mesh('popup-opposite'); fa.box(-17.0, -30.0, -0.30, -16.0, Q.W + 30.0, 14.0)
    objs.append(fa.object(bpy, principled(bpy, 'popup-facade', '#3B3733', rough=0.85)))
    wins = Mesh('popup-opp-windows')
    rnd = random.Random(7)
    for zf in (3.6, 6.6, 9.6):
        for k in range(-8, 12):
            y = k * 2.6
            if rnd.random() < p.get('windows_lit', 0.35):
                wins.box(-16.02, y, zf, -16.0, y + 1.4, zf + 1.6)
    if p.get('windows_lit', 0.35) > 0:
        objs.append(wins.object(bpy, emitter(bpy, 'popup-opp-lit', '#FFC890', p.get('window_glow', 1.2))))
    if p.get('opp_shop_glow', 0.0) > 0:          # (round 43 p1: its reflection read as a hard blue rectangle on the glass)
        shop = Mesh('popup-opp-shop'); shop.box(-16.02, -4.0, 0.2, -16.0, 6.0, 2.8)
        objs.append(shop.object(bpy, emitter(bpy, 'popup-opp-shop', '#FFB070', p['opp_shop_glow'])))


def popup(bpy, name, p, kit):
    W, L, H = Q.W, Q.L, Q.CEIL
    T = 0.20
    objs = []
    # --- the shell -------------------------------------------------------------------------------------------------
    fl = Mesh('popup-floor'); fl.box(-0.2, 0.0, -0.1, L, W, 0.0)
    objs.append(fl.object(bpy, LK.floor_mat(bpy, {'floor_tint': p.get('floor_tint', '#6A645D'), 'floor_mix': 0.75,
                                                  'floor_coat': p.get('floor_coat', 0.3)})))
    wl = Mesh('popup-walls')
    wl.box(-0.2, -T, 0.0, L + T, 0.0, H)                               # the right wall
    wl.box(-0.2, W, 0.0, L + T, W + T, H)                              # the left wall
    wl.box(L, 0.0, 0.0, L + T, W, H)                                   # the back wall
    # the back-of-house partition, its door to the store and the WC's door
    xb = Q.BACK['x0']
    for (y0, y1) in ((0.0, 0.25), (1.20, 2.55), (3.50, W)):
        wl.box(xb, y0, 0.0, xb + 0.12, y1, H)
    for (y0, y1) in ((0.25, 1.20), (2.55, 3.50)):
        wl.box(xb, y0, 2.10, xb + 0.12, y1, H)
    objs.append(wl.object(bpy, D.plaster(bpy, p, name='popup-plaster', colour=p.get('plaster', '#BDB4A6'))))
    dr = Mesh('popup-doors')
    for (y0, y1) in ((0.25, 1.20), (2.55, 3.50)):
        dr.box(xb + 0.03, y0 + 0.01, 0.0, xb + 0.07, y1 - 0.01, 2.09)
    objs.append(dr.object(bpy, principled(bpy, 'popup-door', '#2B2926', rough=0.6)))
    ce = Mesh('popup-ceiling'); ce.box(-0.2, -T, H, L + T, W + T, H + 0.05)
    objs.append(ce.object(bpy, principled(bpy, 'popup-ceiling', p.get('ceiling', '#1E1D1C'), rough=0.92)))
    bm_ = Mesh('popup-beams')                                          # the steel beams and a run of duct, painted out
    for x in (3.8, 7.6, 11.4):
        bm_.box(x - 0.10, 0.0, H - 0.36, x + 0.10, W, H)
    _cyl(bm_.bm, 0.0, W * 0.62, H - 0.62, 0.22, L, seg=32, axis='x')
    objs.append(bm_.object(bpy, principled(bpy, 'popup-paintout', '#1A1918', rough=0.7)))
    # --- the storefront: blackened steel, one big pane each side of the door, a transom ---------------------------
    sf = Mesh('popup-storefront'); gl = Mesh('popup-glass')
    head, tr = 3.05, H
    d0, d1 = Q.DOOR['y0'], Q.DOOR['y0'] + Q.DOOR['w']
    for (a, b) in ((-T, 0.04), (d0 - 0.05, d0), (d1, d1 + 0.05), (W - 0.04, W + T)):
        sf.box(-0.12, a, 0.0, 0.0, b, tr)                                # the mullions
    sf.box(-0.12, -T, 0.0, 0.0, d0, 0.30)                                # the bulkhead
    sf.box(-0.12, d1, 0.0, 0.0, W + T, 0.30)
    sf.box(-0.14, -T, head - 0.04, 0.0, W + T, head + 0.04)              # the transom bar
    sf.box(-0.12, d0, 2.30, 0.0, d1, head)                               # the door's head
    objs.append(sf.object(bpy, K.blackened_steel(bpy), bevel=0.003))
    for (a, b, z0, z1) in ((0.04, d0 - 0.05, 0.30, head - 0.04),
                           (d1 + 0.05, W - 0.04, 0.30, head - 0.04), (0.04, W - 0.04, head + 0.04, tr - 0.02)):
        gl.box(-0.07, a, z0, -0.06, b, z1)
    if not p.get('no_glass'):
        objs.append(gl.object(bpy, R.thin_glass(bpy, p.get('glass_gloss', 1.0))))
    # the name, frosted on the glass over the window
    if p.get('wordmark', False):              # a plain glowing bar, not letters (p0 look): off until it is lettering
        nm = Mesh('popup-name'); nm.box(-0.058, 1.55, 2.55, -0.056, 4.25, 2.72)
        objs.append(nm.object(bpy, principled(bpy, 'popup-name-frost', '#E9E4DA', rough=0.5, alpha=0.55,
                                               emit='#FFD8A8', strength=p.get('name_glow', 0.15))))
    # the window plinth
    Pw = Q.WINDOW_PLINTH
    pl = Mesh('popup-plinths')
    pl.box(Pw['x'] - Pw['d'] / 2, Pw['y'] - Pw['w'] / 2, 0.0, Pw['x'] + Pw['d'] / 2, Pw['y'] + Pw['w'] / 2, Pw['h'])
    objs.append(pl.object(bpy, principled(bpy, 'popup-plinth', '#1E1D1B', rough=0.55), bevel=0.004))
    # the shop's own Tropos, on a low oak plinth at the end of the right wall's shelves
    if p.get('shop_plinth', True):
        sp = Mesh('popup-shop-plinth'); sp.box(5.58, 0.45, 0.0, 6.22, 1.05, 0.26)
        objs.append(sp.object(bpy, K.dark_oak(bpy, name='oak-popup-shop-plinth'), bevel=0.005))
    # --- the shop ----------------------------------------------------------------------------------------------------
    _shelving(bpy, p, objs, 'popup-shelf-r', Q.WALL_R['x0'], Q.WALL_R['x1'], 'right', SHELF)
    _shelving(bpy, p, objs, 'popup-shelf-l', Q.WALL_L['x0'], Q.WALL_L['x1'], 'left', SHELF[:1] + SHELF[2:])
    _records(bpy, objs, 'popup-lp-r', Q.WALL_R['x0'] + 2.75, Q.WALL_R['x1'] - 0.08, 'right', SHELF[0])
    _records(bpy, objs, 'popup-lp-l', Q.WALL_L['x0'] + 0.06, Q.WALL_L['x1'] - 0.08, 'left', SHELF[0], seed=44)
    # sleeves face out on the left wall's top shelf
    covers = Mesh('popup-covers'); rnd = random.Random(5)
    cc = ['#c8452f', '#e9e4d8', '#1d1b19', '#2f4a5e', '#d8c27a', '#e7e2d8']
    for i in range(6):
        xc = Q.WALL_L['x0'] + 0.25 + i * 0.66
        m = Mesh(f'popup-cover{i}'); m.box(xc, W - 0.07, SHELF[-1], xc + 0.315, W - 0.064, SHELF[-1] + 0.315)
        ob = m.object(bpy, principled(bpy, f'popup-cover-{cc[i]}', cc[i], rough=0.6)); ob.rotation_euler[0] = math.radians(6)
        objs.append(ob)
    # sleeves face out on the upper shelves of both walls (round 43 p1: "nearly empty, an unopened fit-out")
    fo = [(x, z, 'right') for (x, z) in p.get('faceout_r', [])] + [(x, z, 'left') for (x, z) in p.get('faceout_l', [])]
    for i, (x, z, side) in enumerate(fo):
        c = cc[i % len(cc)] if i % 3 else '#2a2622'
        y0, y1 = (0.10, 0.106) if side == 'right' else (W - 0.106, W - 0.10)
        m = Mesh(f'popup-fo{i}'); m.box(x, y0, z, x + 0.315, y1, z + 0.315)
        ob = m.object(bpy, principled(bpy, f'popup-cover-{c}', c, rough=0.6))
        objs.append(ob)
    # the price cards, leaning at the shelf fronts
    card = Mesh('popup-cards')
    for (x, z, side) in p.get('cards', []):
        yf = 0.40 - 0.015 if side == 'right' else W - 0.40 + 0.013
        card.box(x - 0.045, yf, z, x + 0.045, yf + 0.002, z + 0.06)
    if p.get('cards'):
        objs.append(card.object(bpy, principled(bpy, 'popup-card', '#EFE9DE', rough=0.8)))
    # the shop table: walnut on a blackened-steel frame
    Tb = Q.TABLE
    tb = Mesh('popup-table'); tb.box(Tb['x0'], Tb['y0'], 0.86, Tb['x1'], Tb['y1'], 0.90)
    objs.append(tb.object(bpy, D.walnut(bpy, coat=0.4, name='-popup-table'), bevel=0.004))
    tf = Mesh('popup-table-frame')
    for x in (Tb['x0'] + 0.10, Tb['x1'] - 0.14):
        tf.box(x, Tb['y0'] + 0.08, 0.0, x + 0.04, Tb['y1'] - 0.08, 0.86)
    objs.append(tf.object(bpy, K.blackened_steel(bpy)))
    # --- the bar: oak front, zinc top, a back table on the wall ------------------------------------------------------
    B = Q.BAR
    bf = Mesh('popup-bar'); bf.box(B['x0'], B['y0'], 0.0, B['x1'], B['y1'], 1.03)
    objs.append(bf.object(bpy, K.dark_oak(bpy, vertical=True, name='oak-popup-bar'), bevel=0.006))
    bt = Mesh('popup-bar-top'); bt.box(B['x0'] - 0.03, B['y0'] - 0.04, 1.03, B['x1'] + 0.03, B['y1'] + 0.02, 1.07)
    objs.append(bt.object(bpy, K.zinc(bpy), bevel=0.008))
    bb = Mesh('popup-backtable'); bb.box(B['x0'] + 0.2, W - 0.55, 0.0, B['x1'] - 0.2, W - 0.05, 0.90)
    objs.append(bb.object(bpy, principled(bpy, 'popup-backtable', '#232120', rough=0.6), bevel=0.004))
    # standing ledges: a round oak top on a steel post and base
    sl = Mesh('popup-ledge-steel'); so = Mesh('popup-ledge-oak')
    for (x, y) in Q.STAND:
        _cyl(sl.bm, x, y, 0.0, 0.22, 0.02, seg=40); _cyl(sl.bm, x, y, 0.02, 0.03, 1.03, seg=16)
        _cyl(so.bm, x, y, 1.03, 0.30, 0.035, seg=48)
    objs.append(sl.object(bpy, K.blackened_steel(bpy), smooth=True))
    objs.append(so.object(bpy, K.dark_oak(bpy, name='oak-popup-ledge'), smooth=True, bevel=0.004))
    # --- the listening room: felt drapes on a track, a rug, chairs, plinths, the decks -----------------------------
    xl = Q.LISTEN['x0']
    cv = Mesh('popup-drapes')
    o0, o1 = Q.DRAPE_OPEN
    LK.D._curtain(cv, xl, 0.0, o0, H - 0.08, folds=0.05, n=20, seed=0.4)
    LK.D._curtain(cv, xl, o1, W, H - 0.08, folds=0.05, n=110, seed=1.1)
    # felt across the back wall too (round 43 p0 look: the store's door sat in the middle of the view), on its own track,
    # drawn back to the WC's door
    if p.get('back_drape', True):
        LK.D._curtain(cv, Q.LISTEN['x1'] - 0.10, 1.30, W, H - 0.08, folds=0.05, n=120, seed=2.3)
    # a plain dense wool felt (the velour scan's sheen read the charcoal as lilac grey in the p0 look)
    objs.append(cv.object(bpy, principled(bpy, 'popup-felt', p.get('felt', '#1F1E1D'), rough=0.97, spec=0.15,
                                          sheen=0.25), smooth=True))
    tk = Mesh('popup-track'); tk.box(xl - 0.03, 0.0, H - 0.08, xl + 0.03, W, H - 0.04)
    objs.append(tk.object(bpy, K.blackened_steel(bpy)))
    rg = Mesh('popup-rug'); rg.box(xl + 0.25, 0.6, 0.0, Q.LISTEN['x1'] - 0.15, W - 0.4, 0.012)
    objs.append(rg.object(bpy, LK.wool(bpy, p.get('rug', '#4E4238'), name='popup-rug')))
    stl, wood, uph = Mesh('popup-chair-steel'), Mesh('popup-chair-oak'), Mesh('popup-chair-wool')
    for (x, y) in Q.SEATS:
        _chair(stl, wood, uph, x, y, 0.0)
    objs.append(stl.object(bpy, K.blackened_steel(bpy), smooth=True))
    objs.append(wood.object(bpy, K.dark_oak(bpy, name='oak-popup-chair'), bevel=0.004))
    objs.append(uph.object(bpy, LK.wool(bpy, p.get('chair_wool', '#6B5444'), name='popup-chair-wool'), bevel=0.01))
    pk = Mesh('popup-stack-plinths')
    for (x, y) in Q.STACKS:
        pk.box(x - 0.36, y - 0.36, 0.0, x + 0.36, y + 0.36, 0.40)
    objs.append(pk.object(bpy, K.dark_oak(bpy, name='oak-popup-plinth'), bevel=0.005))
    Dk = Q.DECKS
    dk = Mesh('popup-decks'); dk.box(Dk['x0'], Dk['y0'], 0.0, Dk['x1'], Dk['y1'], 0.86)
    objs.append(dk.object(bpy, principled(bpy, 'popup-decks', '#1F1E1C', rough=0.55), bevel=0.004))
    if p.get('street', True):
        street(bpy, kit, p, objs)
    return objs
