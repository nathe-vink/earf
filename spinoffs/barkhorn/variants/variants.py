"""Tropos design-pass proposals (2026-10-31, the owner: "nail design, make it realistic, make it cooler"): the new
parts, built apart from the Cloud (its build is at the container's memory limit) in the Cloud's own frame, so a shot
lays them on the current cabinet with the parts they replace hidden. The current design stays the baseline; nothing
here changes the Cloud's CAD.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/variants/variants.py --out spinoffs/barkhorn/variants/out

- **Strata** (variants/STRATA.md): the stepped laminated horn (horn_options.py's horn-plan-b) as the hero, and the
  cabinet answering it: the woofer set in a stepped caldera, three rings of stock 1/2 in sheet in place of the cloth
  disc and its dyed ring, so the horn's contour lines start at the woofer.
- **Topo** (variants/TOPO.md): the laminated horn whose 22 layers' outlines each walk a circle round Mount
  Tamalpais's East Peak at a set distance, the land's relief pushing the edge out (variants/topo/topo.py); the air
  path and the wall unchanged.
"""
import copy, dataclasses, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import cloud                                                         # noqa: E402
import horn_options                                                  # noqa: E402
import product                                                       # noqa: E402
from build123d import Align, Cylinder, Pos, Rot                      # noqa: E402

product.SOLIDS.setdefault('bronze', dict(title='Bronze bar (C93200 bearing bronze or C544), turned', density=8.8,
                                          usd_per_cm3=0.12))   # budget, 2026
P = copy.deepcopy(horn_options.P)
_topo = json.load(open(os.path.join(HERE, 'topo', 'outlines.json')))
P['horn']['cast']['formed']['laminated'].update(topo=[r['points'] for r in _topo['rings']], smooth=False, lamina=3.0,
                                                lip=12.0)   # Strata: the mouth's layer 12 outside the 536 air path, so the stepped horn is 560, flush (the owner, 2026-11-01; 20 before)
# Strata's posts (the critic: a visible mount): the four reviewed post positions kept, each a ø16 bronze rod with a
# turned collar on the top plate and one under the horn's pad, in place of the ø10 stainless tubes and their cups
POSTS = dict(at=[(97.0, 35.0, 929.6), (463.0, 35.0, 929.6), (240.0, 353.0, 998.7), (320.0, 353.0, 998.7)],
             d=16.0, foot=867.0, top_plate=880.0, base_collar=(28.0, 8.0), top_collar=(24.0, 6.0), into_pad=10.0)
# the caldera: rings of stock 1/2 in sheet stacked on the front panel's face round the woofer, the bores stepping out
# toward the room (a short terraced horn of the woofer's own); centre and face from the Cloud (x 280, z 478; face y 24)
CALDERA = dict(centre=(280.0, 478.0), face_y=24.0, layer=12.7, od=500.0, ids=(400.0, 427.0, 454.0))   # 13.5 radial steps: the horn's own at the mouth


# the base (the engineering audit, 2026-11-01, item 1: IEC 62368-1 8.6.2.2 needs the feet about 600 x 600 apart,
# stability/README.md): two proposals for the owner, each an option. The Cloud's frame: the cabinet x 0..560, y 0..420
# (front 0), its bottom at z 0; the centre of mass at about (280, 222). The feet's centres at x -25 / 585 and y -94 / 526.
BASE = dict(feet=[(-25.0, -94.0), (585.0, -94.0), (-25.0, 526.0), (585.0, 526.0)], foot=(40.0, 6.0, 16.0, 6.0))
# A: a stepped plinth in Strata's language, three frames of the cabinet's 1/2 in sheet stepping out to 660 x 670, the
# cabinet bolted down on the top one through its own feet's inserts
PLINTH = dict(layer=12.7, gap=0.1, outer=[(-20.0, -20.0, 580.0, 440.0), (-35.0, -70.0, 595.0, 496.0), (-50.0, -119.0, 610.0, 551.0)],
              inner=(60.0, 60.0, 500.0, 360.0),
              # a 6 mm reveal under the bottom frame's outer 70 was tested and dropped (the coordinator, 2026-11-01;
              # variants/BASES.md, "Tested and not adopted"): set reveal=dict(depth=6.0, width=70.0) to model it
              reveal=None)
# B: four outrigger arms of bronze bar, 30 x 20, from under the cabinet's corners (two M8 into its feet's inserts and
# a second insert each) out on the diagonal to the feet
# A, lit (the owner, 2026-11-01: "can we make them light up from underneath? ... I'd go with the one on the left"): a
# 2700 K COB strip in a shallow aluminium channel with a frosted diffuser, routed into the bottom frame's underside
# `inset` in from its outside edge all round, so a soft warm glow falls on the floor round the plinth (variants/BASES.md)
# the plinth light (the coordinator, 2026-11-01, after the pool tests): the bare COB strip 40 in from the bottom frame's
# edge, as the hero shows it (a thin warm line at the step: glow 20 by day, 40 at dusk); four runs, each broken `brk` short
# of the corner so it clears the foot pads there, joined by short jumpers. The sealed channel (`sealed`, 90 or 40 in) was
# tested and is kept as an alternative (variants/BASES.md)
PLINTH_LIGHT = dict(inset=40.0, w=10.0, t=2.0, brk=30.0,
                    sealed=None)   # dict(inset=90.0, diffuser_w=40.0, diffuser_t=3.0, channel_wall=1.5) for the sealed channel
# the uplight (the owner, 2026-11-02 20:38: "The light in the base is meant to go upward through the speaker ... like in
# the underlit promo images"; variants/BASES.md): in place of the floor line, light aimed up into the cabinet from inside
# its footprint. `edges`: an LED strip in a groove in the top frame under each wall's bottom edge (x0, y0, x1, y1 of its
# line): the sides' own edges, and the front and back panels' edges through the bottom panel they stand on, so each wall
# carries its tint's light up from its foot. `groove` (w, depth) in the top frame; `channel` (w, h) the aluminium
# U-channel on nylon standoffs, clear of the acrylic all round; its frosted lens `gap` under the wall's edge. `panel`: an
# opal diffuser (w, d, t) `panel_under` under the cabinet's bottom, over an LED plate `board_gap` below it, as the uplit
# set's flat panel; it lights the cabinet's inside through the bottom panel round the bottom batt (by the ports)
UPLIGHT = dict(edges=[(10.0, 30.0, 10.0, 390.0), (550.0, 30.0, 550.0, 390.0), (40.0, 34.0, 520.0, 34.0), (40.0, 410.0, 520.0, 410.0)],
               groove=(16.0, 8.0), channel=(12.0, 7.0), wall=1.5, lens_t=1.0, gap=0.6,
               panel=(420.0, 280.0, 3.0), panel_under=10.0, plate_t=2.0, board_gap=8.0, centre=(280.0, 210.0))
# the cabinet wash (a proposal for the owner, 2026-11-02, after the uplight fell short of the underlit promo look): a COB
# strip on the bottom panel at the foot of each side wall and the front panel, inside the cabinet, between the wall and
# its lining, aimed up the wall's inner face so the whole wall and the lining's white voile behind it glow in the tint;
# fed from the plinth's 24 V through a sealed connector in the bottom panel at a foot pad. (x0, y0, x1, y1) of each run
# on the bottom panel's top face (z 20); the back is left out (its land strip and the amplifier's compartment)
WASH = dict(runs=[(24.0, 60.0, 24.0, 370.0), (536.0, 60.0, 536.0, 370.0), (60.0, 48.0, 500.0, 48.0)], w=8.0, t=2.0, z=20.0)
# the built-in light (a proposal for the owner, 2026-11-03, the coordinator: "could the whole uplight live inside the
# speaker, with no plate at all?"): COB strips, 24 V, 20 W/m, 4000 K, in black aluminium U-channels on nylon standoffs,
# aimed straight up, inside the cabinet. `floor`: on the bottom panel's top face (z 20), behind the batt (under the back
# lining, which starts at z 50) and behind each port; `brace`: on the brace's top face (z 220), clear of the side linings,
# the ribs and the back's bosses. (x0, y0, x1, y1) of each run, mm in the cabinet's frame. Fed from an external 24 V plug-in
# supply through a panel connector in the back's cable gland (variants/BASES.md)
BUILTIN = dict(floor=[(60.0, 360.0, 500.0, 360.0), (50.0, 295.0, 160.0, 295.0), (400.0, 295.0, 510.0, 295.0)], z_floor=20.0,
               brace=[(90.0, 250.0, 470.0, 250.0), (90.0, 300.0, 470.0, 300.0)], z_brace=220.0,
               channel=(12.0, 7.0), wall=1.5, lens_t=1.0, lens_down=0.6, standoff=(6.0, 3.0))
# the slim light plate (the coordinator, 2026-11-03, for the owner's question about the footing: "a separate base that
# people can optionally purchase"): the cabinet's own footprint, `h` tall to the cabinet's bottom; a top frame of the
# cabinet's 1/2 in sheet carrying the uplight's grooves and the centre panel's opening (as the plinth's top frame), over a
# black anodised aluminium tray (`tray_t` walls) holding the centre panel's board and heat sink, vented to the floor; four
# levelling feet `feet_in` from its corners. Under IEC 62368-1 Tropos passes on its own feet (stability/standard-2018.md)
LPLATE = dict(h=50.0, frame=12.7, tray_t=2.0, feet_in=20.0, foot=(40.0, 6.0, 16.0, 6.0))
OUTRIG = dict(w=30.0, h=20.0, inner=[(95.0, 80.0), (465.0, 80.0), (95.0, 340.0), (465.0, 340.0)])


def foot(x, y, z_top):
    """A levelling foot under z_top: a stem and a 40 pad (the Cloud's own kind)."""
    d, t, sd, sh = BASE['foot']
    stem = Pos(x, y, z_top - sh) * Cylinder(sd / 2, sh - 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))
    pad = Pos(x, y, z_top - sh - t) * Cylinder(d / 2, t - 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return stem, pad


def plinth(Q):
    from build123d import Box
    out, z = [], 0.0
    for k, (x0, y0, x1, y1) in enumerate(Q['outer']):
        z1 = z - Q['gap']; z0 = z1 - Q['layer']
        ring = Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)
        ix0, iy0, ix1, iy1 = Q['inner']
        ring = ring - Pos((ix0 + ix1) / 2, (iy0 + iy1) / 2, (z0 + z1) / 2) * Box(ix1 - ix0, iy1 - iy0, z1 - z0 + 2)
        rv = Q.get('reveal')
        if rv and k == len(Q['outer']) - 1:          # the bottom frame: its underside's outer band rebated
            w_, d_ = rv['width'], rv['depth']
            band = Pos((x0 + x1) / 2, (y0 + y1) / 2, z0 + d_ / 2 - 1) * Box(x1 - x0 + 2, y1 - y0 + 2, d_ + 2)
            band = band - Pos((x0 + x1) / 2, (y0 + y1) / 2, z0 + d_ / 2 - 1) * Box(x1 - x0 - 2 * w_, y1 - y0 - 2 * w_, d_ + 4)
            ring = ring - band
        out.append(ring); z = z0
    return out, z


def outriggers(Q):
    from build123d import Box
    arms = []
    z1 = -0.1; z0 = z1 - Q['h']
    for (xi, yi), (xo, yo) in zip(Q['inner'], BASE['feet']):
        L = math.hypot(xo - xi, yo - yi); ang = math.degrees(math.atan2(yo - yi, xo - xi))
        bar = Pos((xi + xo) / 2, (yi + yo) / 2, (z0 + z1) / 2) * Rot(0, 0, ang) * Box(L, Q['w'], Q['h'])
        for (x, y) in ((xi, yi), (xo, yo)):              # rounded ends
            bar = bar + Pos(x, y, z0) * Cylinder(Q['w'] / 2, Q['h'], align=(Align.CENTER, Align.CENTER, Align.MIN))
        arms.append(bar)
    return arms, z0


def caldera(C):
    out = []
    for k, idia in enumerate(C['ids']):
        y1 = C['face_y'] - k * C['layer'] - 0.1; y0 = C['face_y'] - (k + 1) * C['layer'] + 0.1
        ring = Cylinder(C['od'] / 2, y1 - y0) - Cylinder(idia / 2, y1 - y0 + 2)
        out.append(Pos(C['centre'][0], (y0 + y1) / 2, C['centre'][1]) * Rot(90, 0, 0) * ring)
    return out


def posts(Q):
    out = []
    for x, y, top in Q['at']:
        rod = Pos(x, y, Q['foot']) * Cylinder(Q['d'] / 2, top - Q['foot'], align=(Align.CENTER, Align.CENTER, Align.MIN))
        bc = Pos(x, y, Q['top_plate'] + 0.1) * (Cylinder(Q['base_collar'][0] / 2, Q['base_collar'][1], align=(Align.CENTER, Align.CENTER, Align.MIN))
                                                 - Cylinder(Q['d'] / 2 + 0.2, Q['base_collar'][1] + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        pad = top - Q['into_pad']
        tc = Pos(x, y, pad - Q['top_collar'][1] - 0.1) * (Cylinder(Q['top_collar'][0] / 2, Q['top_collar'][1], align=(Align.CENTER, Align.CENTER, Align.MIN))
                                                           - Cylinder(Q['d'] / 2 + 0.2, Q['top_collar'][1] + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        out.append((rod, bc, tc))
    return out


def parts(P):
    wg = product.waveguide(P)
    fm = wg['formed']
    out = []
    if fm.get('laminated_topo'):
        from build123d import Compound
        out.append(product.Part('horn-topo', Compound(children=fm['laminated_topo']), product._lam_stock(P['horn']['cast']['formed'], fm['laminated_topo'], False),
                                finish='horn-lot', group='horn',
                                notes=['Topo (variants/TOPO.md): the laminated horn, 22 layers of stock 1/2 in and the boss, each '
                                       'layer\'s outline the air path plus the wall pushed out 8 to 45 mm by the elevation along a '
                                       'circle round Mount Tamalpais\'s East Peak (from 2.4 km at the mouth to 150 m at the throat); '
                                       'CNC-cut from the DXF of each layer, bonded and machined as horn-plan-b']))
    if fm.get('laminated_lines'):            # Topo Clear (the Mantle lane's idea): clear layers, a 3 mm tinted lamina each
        from build123d import Compound
        clear, lines = fm['laminated_lines']
        F = P['horn']['cast']['formed']
        out.append(product.Part('horn-topo-clear', Compound(children=clear), product._lam_stock(F, clear, False), finish='clear-cast',
                                group='horn', option='Topo Clear',
                                notes=['Topo Clear: the Topo horn\'s 22 layers in clear cast sheet (9.6 mm each, from 3/8 in faced), '
                                       'and the boss']))
        out.append(product.Part('horn-topo-lines', Compound(children=lines), product.Machined('stock-cast-sheet', 'cnc-mill', setup_usd=300.0),
                                finish='horn-lot', group='horn', option='Topo Clear',
                                notes=['Topo Clear: a 3 mm lamina of the horn\'s tint (stock 1/8 in sheet, e.g. 2423 or 2074) '
                                       'bonded on each clear layer\'s front face, cut to the same outline: the color reads as a '
                                       'contour line at every step\'s edge']))
    if fm.get('laminated'):                  # Strata's horn: the stepped laminated horn with its even front lip
        from build123d import Compound
        out.append(product.Part('horn-strata', Compound(children=fm['laminated']), product._lam_stock(P['horn']['cast']['formed'], fm['laminated'], False),
                                finish='horn-lot', group='horn',
                                notes=['Strata (variants/STRATA.md): the stepped laminated horn, 22 layers of stock 1/2 in and the '
                                       'boss, the mouth\'s layer 20 outside the air path (10 on the others), its front face and every '
                                       'layer\'s edge polished before bonding']))
    from build123d import Compound
    ps = posts(POSTS)
    out.append(product.Part('strata-posts', Compound(children=[r for r, _, _ in ps]), product.Machined('bronze', 'lathe', setup_usd=60.0),
                            finish='brass', group='horn',
                            notes=['Strata: four ø16 bronze rods (C93200 or C544), threaded M12 at the top into inserts in the horn\'s '
                                   'pads, at the four reviewed post positions. The engineering audit (2026-11-01): the front pair\'s feet are '
                                   'turned heads (14 across, 4 thick, on an 8 neck) hooked under keyhole sockets bonded through the top into '
                                   'the front panel\'s edge; the rear pair seated in sleeved sockets, the tie rod in rear post 3 at 2 N m; '
                                   'held at three points, the horn cannot lift (make/engineering-audit.md)']))
    out.append(product.Part('strata-collars', Compound(children=[c for _, b, t in ps for c in (b, t)]), product.Machined('bronze', 'lathe', setup_usd=40.0),
                            finish='brass', group='horn',
                            notes=['Strata: a turned bronze collar on the top plate at each post (ø28 x 8) and one under each pad '
                                   '(ø24 x 6), so the horn reads as mounted, not hovering']))
    from build123d import Compound as _C
    from build123d import Box
    layers, zp = plinth(PLINTH)
    U = UPLIGHT; gw, gd = U['groove']
    seg = lambda ax, ay, bx, by, w, z0, z1: Pos((ax + bx) / 2, (ay + by) / 2, (z0 + z1) / 2) * Box(max(abs(bx - ax) + w, w), max(abs(by - ay) + w, w), z1 - z0)
    for (ax, ay, bx, by) in U['edges']:              # the uplight's grooves in the top frame, under the walls
        layers[0] = layers[0] - seg(ax, ay, bx, by, gw, -gd - 0.1, 1.0)
    for k, ring in enumerate(layers):
        out.append(product.Part(f'base-plinth-{k + 1}', ring, product.Machined('stock-cast-sheet', 'cnc-mill', setup_usd=60.0),
                                finish='bark', group='base', option='Plinth',
                                notes=[f'Base A, the stepped plinth (make/engineering-audit.md, stability/README.md): frame {k + 1} of 3 '
                                       'from the top, 1/2 in stock sheet in the cabinet\'s color, its outside edges polished, the three '
                                       'bonded; the cabinet bolted down on it with M8 through its feet\'s inserts']))
    from build123d import Box
    x0, y0, x1, y1 = PLINTH['outer'][-1]; L_ = PLINTH_LIGHT; S_ = L_.get('sealed')
    if not S_:
        # the bare strip, four runs broken short of the corners (the foot pads), on the frame's underside
        i_, b_ = L_['inset'], L_['brk']; zl1 = zp - 0.1; zl0 = zl1 - L_['t']
        strip = []
        for (ax, ay, bx, by) in ((x0 + i_ + b_, y0 + i_, x1 - i_ - b_, y0 + i_), (x0 + i_ + b_, y1 - i_, x1 - i_ - b_, y1 - i_),
                                 (x0 + i_, y0 + i_ + b_, x0 + i_, y1 - i_ - b_), (x1 - i_, y0 + i_ + b_, x1 - i_, y1 - i_ - b_)):
            strip.append(Pos((ax + bx) / 2, (ay + by) / 2, (zl0 + zl1) / 2) * Box(max(abs(bx - ax), L_['w']), max(abs(by - ay), L_['w']), L_['t']))
        out.append(product.Part('base-plinth-light', _C(children=strip), product.Bought('plinth-led'), finish='led', group='base',
                                option='Plinth light', notes=['Base A, lit: the COB strip in a shallow channel with a frosted diffuser, '
                                                              f'in a groove in the bottom frame\'s underside {i_:g} in from its edge; four runs, '
                                                              f'each stopped {b_:g} short of the corner to clear the foot pads, joined by short '
                                                              'soldered jumpers (variants/BASES.md)']))
    else:
        # the tested alternative: the strip and an opal diffuser in a removable, light-tight black U-channel
        i_ = S_['inset']; W_ = S_['diffuser_w']; cw = S_['channel_wall']
        zc1 = zp - 0.1; zl1 = zc1 - cw - 0.1; zl0 = zl1 - S_['diffuser_t']
        strip, chan = [], []
        for (ax, ay, bx, by) in ((x0 + i_, y0 + i_, x1 - i_, y0 + i_), (x0 + i_, y1 - i_, x1 - i_, y1 - i_),
                                 (x0 + i_, y0 + i_, x0 + i_, y1 - i_), (x1 - i_, y0 + i_, x1 - i_, y1 - i_)):
            dx, dy = max(abs(bx - ax) + W_, W_), max(abs(by - ay) + W_, W_)
            strip.append(Pos((ax + bx) / 2, (ay + by) / 2, (zl0 + zl1) / 2) * Box(dx, dy, S_['diffuser_t']))
            u = Pos((ax + bx) / 2, (ay + by) / 2, (zl0 + zc1) / 2) * Box(dx + 2 * cw + 0.2, dy + 2 * cw + 0.2, zc1 - zl0)
            u = u - Pos((ax + bx) / 2, (ay + by) / 2, (zl0 + zl1) / 2 - 0.5) * Box(dx + 0.2, dy + 0.2, S_['diffuser_t'] + 1.0)
            chan.append(u)
        out.append(product.Part('base-plinth-light', _C(children=strip), product.Bought('plinth-led'), finish='led', group='base',
                                option='Plinth light', notes=['Base A, lit (the sealed alternative): the strip behind an opal diffuser, '
                                                              f'{i_:g} in (variants/BASES.md)']))
        out.append(product.Part('base-plinth-channel', _C(children=chan), product.Bought('plinth-channel'), finish='channel', group='base',
                                option='Plinth light', notes=['the sealed alternative\'s black U-channel, screwed, not bonded (variants/BASES.md)']))
    for nm, key in (('base-plinth-supply', 'plinth-supply'), ('base-plinth-controller', 'plinth-controller')):
        out.append(product.Part(nm, None, product.Bought(key), group='base', option='Plinth light'))
    # the uplight: the strips' lenses and channels in the grooves, the centre panel and its LED plate in the opening
    cw, ch = U['channel']; t_ = U['wall']; zl1 = -U['gap']; zl0 = zl1 - U['lens_t']; zc0 = zl1 - ch
    lens, chan = [], []
    for (ax, ay, bx, by) in U['edges']:
        lens.append(seg(ax, ay, bx, by, cw - 2 * t_ - 0.2, zl0, zl1))
        u = seg(ax, ay, bx, by, cw, zc0, zl1)
        chan.append(u - seg(ax, ay, bx, by, cw - 2 * t_, zc0 + t_, zl1 + 1.0))
    pw, pd, pt = U['panel']; cx, cy = U['centre']; zp1 = -U['panel_under']; zp0 = zp1 - pt
    panel = Pos(cx, cy, (zp0 + zp1) / 2) * Box(pw, pd, pt)
    zb1 = zp0 - U['board_gap']; plate = Pos(cx, cy, zb1 - U['plate_t'] / 2) * Box(pw + 14.0, pd + 14.0, U['plate_t'])
    out.append(product.Part('base-uplight-edge', _C(children=lens), product.Bought('uplight-strip'), finish='uplight-edge', group='base',
                            option='Plinth uplight',
                            notes=['the uplight\'s edge strips: COB, 24 V, 4000 K, under each wall\'s bottom edge in a groove in the top '
                                   f'frame ({gw:g} x {gd:g}), in an aluminium channel on nylon standoffs clear of the acrylic, its frosted '
                                   f'lens {U["gap"]:g} under the wall (variants/BASES.md)']))
    out.append(product.Part('base-uplight-channel', _C(children=chan), product.Bought('uplight-channel'), finish='channel', group='base',
                            option='Plinth uplight', notes=['the edge strips\' aluminium U-channels, on nylon standoffs in the grooves']))
    out.append(product.Part('base-uplight-panel', panel, product.Bought('uplight-panel'), finish='uplight-panel', group='base',
                            option='Plinth uplight',
                            notes=[f'the uplight\'s centre panel: an opal PMMA diffuser {pw:g} x {pd:g} x {pt:g}, {U["panel_under"]:g} under the '
                                   'cabinet\'s bottom, lit from an aluminium-core LED plate below it (4000 K)']))
    out.append(product.Part('base-uplight-plate', plate, product.Bought('uplight-panel'), finish='channel', group='base',
                            option='Plinth uplight', notes=['the centre panel\'s LED plate, black anodised aluminium, on brackets in the opening']))
    B_ = BUILTIN; bcw, bch = B_['channel']; bt = B_['wall']; sw, sh = B_['standoff']
    for key, z0 in (('floor', B_['z_floor']), ('brace', B_['z_brace'])):
        bl, bc, bs = [], [], []
        zc0 = z0 + sh; zc1 = zc0 + bch; zl1 = zc1 - B_['lens_down']; zl0 = zl1 - B_['lens_t']
        for (ax, ay, bx, by) in B_[key]:
            bl.append(seg(ax, ay, bx, by, bcw - 2 * bt - 0.2, zl0, zl1))
            bc.append(seg(ax, ay, bx, by, bcw, zc0, zc1) - seg(ax, ay, bx, by, bcw - 2 * bt, zc0 + bt, zc1 + 1.0))
            for f in (0.08, 0.5, 0.92):           # three nylon standoffs a run
                x, y = ax + f * (bx - ax), ay + f * (by - ay)
                bs.append(Pos(x, y, z0 + sh / 2 + 0.05) * Box(sw, sw, sh - 0.1))
        out.append(product.Part(f'builtin-{key}-led', _C(children=bl), product.Bought('builtin-strip'), finish='builtin-led' if key == 'floor' else 'builtin-led-brace', group='base',
                                option='Built-in light',
                                notes=[f'the built-in light ({key}): COB strip, 24 V, 20 W/m, 4000 K, its frosted lens in a black U-channel, '
                                       'aimed straight up inside the cabinet (a proposal; variants/BASES.md)']))
        out.append(product.Part(f'builtin-{key}-channel', _C(children=bc), product.Bought('uplight-channel'), finish='channel', group='base',
                                option='Built-in light', notes=[f'the built-in light\'s {key} channels: aluminium U, 12 x 7, black anodised']))
        out.append(product.Part(f'builtin-{key}-standoffs', _C(children=bs), product.Bought('builtin-standoffs'), finish='foot', group='base',
                                option='Built-in light', notes=[f'nylon standoffs, M3, screwed into inserts bonded in the {key}, three a run']))
    wash = [seg(ax, ay, bx, by, WASH['w'], WASH['z'] + 0.1, WASH['z'] + 0.1 + WASH['t']) for (ax, ay, bx, by) in WASH['runs']]
    out.append(product.Part('cabinet-wash', _C(children=wash), product.Bought('cabinet-wash'), finish='uplight-wash', group='base',
                            option='Cabinet wash',
                            notes=['the cabinet wash (a proposal): COB strips on the bottom panel at the foot of each side wall and the front '
                                   'panel, between the wall and its lining, aimed up the wall; fed from the plinth through a sealed connector '
                                   'at a foot pad (variants/BASES.md)']))
    # the slim light plate (option 'Light plate'; the uplight's parts are the plinth's, in the same places)
    L = LPLATE; zf = -L['frame'] - 0.1; d_ = L['foot'][1] + L['foot'][3]; zb = -L['h'] + d_
    frame = Pos(280.0, 210.0, zf / 2) * Box(560.0, 420.0, -zf - 0.1) - Pos(280.0, 210.0, zf / 2) * Box(440.0, 300.0, -zf + 2)
    for (ax, ay, bx, by) in U['edges']:
        frame = frame - seg(ax, ay, bx, by, gw, -gd - 0.1, 1.0)
    tw = L['tray_t']
    tray = Pos(280.0, 210.0, (zb + zf - 0.1) / 2) * Box(560.0, 420.0, zf - 0.1 - zb) - \
        Pos(280.0, 210.0, (zb + zf) / 2 + tw) * Box(560.0 - 2 * tw, 420.0 - 2 * tw, zf - zb)
    out.append(product.Part('base-lplate-frame', frame, product.Machined('stock-cast-sheet', 'cnc-mill', setup_usd=60.0), finish='bark',
                            group='base', option='Light plate',
                            notes=['the slim light plate\'s top frame: 1/2 in stock sheet in the cabinet\'s colour, 560 x 420 round a 440 x 300 '
                                   'opening, grooved for the uplight\'s edge strips under the walls, its edges polished']))
    out.append(product.Part('base-lplate-tray', tray, product.Machined('aluminium', 'cnc-mill', setup_usd=80.0), finish='channel',
                            group='base', option='Light plate',
                            notes=[f'the plate\'s tray: {tw:g} mm aluminium, folded and welded, black anodised, holding the centre panel\'s board '
                                   'and heat sink on nylon brackets, slotted round its floor\'s edge to vent; the frame screwed to it']))
    fi = L['feet_in']
    lf = [foot(x, y, zb - 0.1) for x, y in ((fi, fi), (560 - fi, fi), (fi, 420 - fi), (560 - fi, 420 - fi))]
    out.append(product.Part('base-lplate-feet', _C(children=[c for f in lf for c in f]), product.Bought('levelling-feet'),
                            finish='foot', group='base', option='Light plate', notes=['four M8 levelling feet under the plate\'s corners']))
    pf = [foot(x, y, zp - 0.1) for x, y in BASE['feet']]
    out.append(product.Part('base-plinth-feet', _C(children=[c for f in pf for c in f]), product.Bought('levelling-feet'),
                            finish='foot', group='base', option='Plinth', notes=['four M8 levelling feet under the plinth\'s corners']))
    arms, zo = outriggers(OUTRIG)
    out.append(product.Part('base-outriggers', _C(children=arms), product.Machined('bronze', 'cnc-mill', setup_usd=120.0),
                            finish='brass', group='base', option='Outriggers',
                            notes=['Base B, outrigger feet (make/engineering-audit.md): four arms of bronze bar 30 x 20 (C93200 or '
                                   'C544), from under the cabinet\'s corners out on the diagonal to the feet, each held by two M8 '
                                   'into inserts in the bottom (its foot\'s own and a second)']))
    of = [foot(x, y, zo - 0.1) for x, y in BASE['feet']]
    out.append(product.Part('base-outrigger-feet', _C(children=[c for f in of for c in f]), product.Bought('levelling-feet'),
                            finish='foot', group='base', option='Outriggers', notes=['four M8 levelling feet under the arms\' ends']))
    for k, ring in enumerate(caldera(CALDERA)):
        out.append(product.Part(f'caldera-{k + 1}', ring, product.Machined('stock-cast-sheet', 'cnc-mill', stock=(CALDERA['od'] + 10, CALDERA['od'] + 10, CALDERA['layer']), setup_usd=60.0),
                                finish='bark', group='cabinet',
                                notes=[f'Strata (variants/STRATA.md): the woofer\'s caldera, ring {k + 1} of 3 from the panel: '
                                       f'Ø{CALDERA["od"]:g} outside, Ø{CALDERA["ids"][k]:g} bore, 1/2 in stock sheet in the '
                                       'cabinet\'s colour, faced, its bore and outside edges polished; bonded to the front panel '
                                       '(ring 1) and to each other with polymerising cement, before the woofer goes in']))
    return out


PRODUCT = dataclasses.replace(
    cloud.PRODUCT, name='barkhorn-variants', params=P, parts=parts, count=2,
    touching=[('horn-topo', 'horn-topo-clear'), ('horn-topo', 'horn-topo-lines')],      # alternatives in one place
    materials={**cloud.PRODUCT.materials,                # Topo Clear's body: water-clear cast sheet, a faint cool cast
               'clear-cast': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#EEF2EF', 'radius': 0.05, 'roughness': 0.03},
               # the plinth light's diffuser: frosted, lit from within at 2700 K (a shot may turn `glow` up or down)
               'led': {'preset': 'frosted', 'color': '#FFF1E0', 'absorb': '#FFE9D2', 'glow': 40.0, 'glow_color': '#FFB46B'},
               # the plinth light's channel: black anodised aluminium, light tight
               'channel': {'preset': 'plastic', 'color': '#111111', 'roughness': 0.55},
               # the uplight (variants/BASES.md): 4000 K, so each tint shows its own colour; `glow` W/m2 of emitting face
               # at the default 50 %: the strips about 3 W/m of light (10 W/m electrical) through an 8 mm lens at full,
               # 375 W/m2; the panel about 12 W of light (40 W electrical, 2026-11-03; 16 W before) over 0.118 m2 at full, 105 W/m2
               'uplight-edge': {'preset': 'frosted', 'color': '#F4F2EE', 'absorb': '#F0EEEA', 'glow': 188.0, 'glow_color': '#FFCEA6'},
               'uplight-wash': {'preset': 'frosted', 'color': '#F4F2EE', 'absorb': '#F0EEEA', 'glow': 188.0, 'glow_color': '#FFCEA6'},
               'uplight-panel': {'preset': 'frosted', 'color': '#F4F2EE', 'absorb': '#F0EEEA', 'glow': 52.0, 'glow_color': '#FFCEA6'},
               # the built-in light: 20 W/m electrical, about 6 W/m of light through an 8.6 mm lens, 680 W/m2 at full
               'builtin-led': {'preset': 'frosted', 'color': '#F4F2EE', 'absorb': '#F0EEEA', 'glow': 680.0, 'glow_color': '#FFCEA6'},
               'builtin-led-brace': {'preset': 'frosted', 'color': '#F4F2EE', 'absorb': '#F0EEEA', 'glow': 680.0, 'glow_color': '#FFCEA6'}},
    kind='Tropos design-pass proposals: Strata\'s caldera and the Topo horn',
    notes=['Proposals beside the current design (variants/README.md); the Cloud\'s CAD is unchanged.'],
    origin=(280.0, 213.7, -12.0), drawing_prefix='BHV')
