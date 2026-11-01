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
              # the reveal (the coordinator, 2026-11-01, option b): a rebate in the bottom frame's underside from its outside
              # edge in to the diffuser, so the gap at the step's edge is 18 (the feet's 12 and the rebate's 6) and a low eye
              # sees under it, not the diffuser; 6 deep leaves a 6.7 lip in the 1/2 in sheet (a 15 reveal does not fit)
              reveal=dict(depth=6.0, width=70.0))
# B: four outrigger arms of bronze bar, 30 x 20, from under the cabinet's corners (two M8 into its feet's inserts and
# a second insert each) out on the diagonal to the feet
# A, lit (the owner, 2026-11-01: "can we make them light up from underneath? ... I'd go with the one on the left"): a
# 2700 K COB strip in a shallow aluminium channel with a frosted diffuser, routed into the bottom frame's underside
# `inset` in from its outside edge all round, so a soft warm glow falls on the floor round the plinth (variants/BASES.md)
# the plinth light (the coordinator, 2026-11-01: a soft pool on the floor, not a line): the 10 mm COB strip 90 in from the
# bottom frame's edge, behind a 40 wide, 3 mm opal diffuser under the frame, so the step's edge no longer shows the strip
# itself and its light leaves downward; the feet, the footprint and the plinth's outline unchanged (it was 40 in, bare)
# and the seal (the coordinator, 2026-11-01): the light piped through the clear frame and glowed at its edges as a line,
# so the strip and the diffuser ride in a removable black U-channel (1.5 walls), screwed to the frame's underside, light
# tight above and at the sides: only the diffuser's face lights, down onto the floor; the strip replaceable in service
PLINTH_LIGHT = dict(inset=90.0, w=10.0, t=2.0, diffuser_w=40.0, diffuser_t=3.0, channel_wall=1.5)
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
    layers, zp = plinth(PLINTH)
    for k, ring in enumerate(layers):
        out.append(product.Part(f'base-plinth-{k + 1}', ring, product.Machined('stock-cast-sheet', 'cnc-mill', setup_usd=60.0),
                                finish='bark', group='base', option='Plinth',
                                notes=[f'Base A, the stepped plinth (make/engineering-audit.md, stability/README.md): frame {k + 1} of 3 '
                                       'from the top, 1/2 in stock sheet in the cabinet\'s color, its outside edges polished, the three '
                                       'bonded; the cabinet bolted down on it with M8 through its feet\'s inserts']))
    from build123d import Box
    x0, y0, x1, y1 = PLINTH['outer'][-1]; L_ = PLINTH_LIGHT; i_ = L_['inset']
    # what shows and glows is the diffuser (the strip sits in its channel above it, inside the frame's underside)
    W_ = L_['diffuser_w']; cw = L_['channel_wall']
    zc1 = zp - 0.1; zl1 = zc1 - cw - 0.1; zl0 = zl1 - L_['diffuser_t']     # the channel's top, then the diffuser below it
    strip, chan = [], []
    for (ax, ay, bx, by) in ((x0 + i_, y0 + i_, x1 - i_, y0 + i_), (x0 + i_, y1 - i_, x1 - i_, y1 - i_),
                             (x0 + i_, y0 + i_, x0 + i_, y1 - i_), (x1 - i_, y0 + i_, x1 - i_, y1 - i_)):
        lx = abs(bx - ax) + W_; ly = abs(by - ay) + W_
        dx, dy = (lx if lx > W_ else W_), (ly if ly > W_ else W_)
        strip.append(Pos((ax + bx) / 2, (ay + by) / 2, (zl0 + zl1) / 2) * Box(dx, dy, L_['diffuser_t']))
        # the U-channel round it: a top plate and two walls down to the diffuser's face (a frame of the run, its corners
        # closed by the neighbouring runs)
        ox, oy = dx + 2 * cw + 0.2, dy + 2 * cw + 0.2
        u = Pos((ax + bx) / 2, (ay + by) / 2, (zl0 + zc1) / 2) * Box(ox, oy, zc1 - zl0)
        u = u - Pos((ax + bx) / 2, (ay + by) / 2, (zl0 + zl1) / 2 - 0.5) * Box(dx + 0.2, dy + 0.2, L_['diffuser_t'] + 1.0)
        chan.append(u)
    out.append(product.Part('base-plinth-light', _C(children=strip), product.Bought('plinth-led'), finish='led', group='base',
                            option='Plinth light', notes=['Base A, lit: the COB strip in a channel under the bottom frame, '
                                                          f'{i_:g} in from its edge all round, behind a {W_:g} wide, '
                                                          f'{L_["diffuser_t"]:g} mm opal acrylic diffuser, so it throws a soft pool on '
                                                          'the floor, not a line at the step (variants/BASES.md)']))
    out.append(product.Part('base-plinth-channel', _C(children=chan), product.Bought('plinth-channel'), finish='channel', group='base',
                            option='Plinth light', notes=['Base A, lit: the strip and its diffuser ride in a black anodised aluminium '
                                                          f'U-channel ({cw:g} walls), light tight above and at the sides so no light '
                                                          'enters the clear frame; held to the frame\'s underside by M3 stainless screws '
                                                          'into threaded inserts about every 250, not bonded, so the strip can be '
                                                          'replaced (the coordinator, 2026-11-01; variants/BASES.md)']))
    for nm, key in (('base-plinth-supply', 'plinth-supply'), ('base-plinth-controller', 'plinth-controller')):
        out.append(product.Part(nm, None, product.Bought(key), group='base', option='Plinth light'))
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
               'channel': {'preset': 'plastic', 'color': '#111111', 'roughness': 0.55}},
    kind='Tropos design-pass proposals: Strata\'s caldera and the Topo horn',
    notes=['Proposals beside the current design (variants/README.md); the Cloud\'s CAD is unchanged.'],
    origin=(280.0, 213.7, -12.0), drawing_prefix='BHV')
