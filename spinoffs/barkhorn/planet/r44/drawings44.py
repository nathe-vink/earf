"""Planet EARF, round 44: the lantern's drawing set, every line from plan44.py.

    python3 spinoffs/barkhorn/planet/r44/drawings44.py              # SVGs into spinoffs/barkhorn/planet/r44/drawings/
    node spinoffs/barkhorn/planet/r44/sheets44.mjs spinoffs/barkhorn/planet/r44/drawings spinoffs/.../drawings/A-*.svg

A-101 floor plan, A-102 reflected ceiling plan, A-201 two sections (long, through the lantern; across, at the sweet
spot), A-301 two elevations (the street; the lantern's face from the bar), A-401 axonometric. ARCH D sheets (36 x 24
in), plans and the long section at 1/4" = 1'-0", the cross section and the elevations at 3/8" = 1'-0".
"""
import json, math, os, sys, base64

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r42'))
import plan44 as P                                                   # noqa: E402
from svg42 import Sheet, Frame, ftin, INK, GREY, LIGHT, PAPER          # noqa: E402

OUT = os.path.join(HERE, 'drawings')
S4 = 1000 / 48.0                  # 1/4" = 1'-0"
S38 = 1000 / 32.0                 # 3/8" = 1'-0"
SHEETS = [('A-101', 'Floor plan'), ('A-102', 'Reflected ceiling plan'), ('A-201', 'Sections'),
          ('A-301', 'Elevations'), ('A-401', 'Axonometric')]
EX = '#2a2927'
NEW = '#77736c'
C = {'route': '#2f6fd0', 'exit': '#1d8a4e', 'oak': '#c9ad86', 'oakd': '#8a6a48', 'band': '#e0a050', 'terr': '#d8d3ca',
     'shop': '#f3ede2', 'lant': '#efe6dc', 'rear': '#efefec', 'felt': '#3a3532', 'glow': '#f6c47e', 'ember': '#b5402c',
     'quartz': '#5a5754'}
W, L = P.W, P.L
I = P.INNER
YC = (I['y0'] + I['y1']) / 2
SITE = ["A typical San Francisco storefront:", "25'-0\" x 80'-0\" inside the party walls", "(2,000 sq ft), 14'-0\" to the joists of",
        'the flats above, a slab on grade,', 'a glazed front and a rear yard.', 'No site chosen: the scheme is drawn',
        'generic and is fitted to the lease.']


def frame(sh, number, title, sub, notes=()):
    tx = sh.frame(number, title, sub, SHEETS, notes=notes, site=SITE)
    sh.el = [e.replace('Round 42 · 31 October 2026 · rev A', 'Round 44 · the lantern · 31 October 2026 · rev A') for e in sh.el]
    return tx


# --- plan ---------------------------------------------------------------------------------------------------------------
def walls(sh, F):
    T = P.WALL
    ex = dict(fill=EX, stroke=INK, sw=0.25)
    F.r(sh, -0.30, -T, L + T, 0, **ex)
    F.r(sh, -0.30, W, L + T, W + T, **ex)
    F.r(sh, L, 0, L + T, P.REAR_EXIT['y0'], **ex); F.r(sh, L, P.REAR_EXIT['y1'], L + T, W, **ex)
    F.door(sh, (L, P.REAR_EXIT['y0']), (0, 1), (1, 0), P.DOOR)
    # the shopfront: the pier at the right, the alcove, the glass on its bulkhead, a mullion
    F.r(sh, -0.30, -T, 0.0, P.ENTRY['y0'], **ex)
    F.r(sh, -0.12, P.GLASS[0], 0.0, W, fill=PAPER, sw=0.2); F.l(sh, -0.06, P.GLASS[0], -0.06, W, sw=0.12)
    F.r(sh, -0.12, (P.GLASS[0] + W) / 2 - 0.03, 0.0, (P.GLASS[0] + W) / 2 + 0.03, fill=INK, sw=0.1)
    V = P.VEST
    F.r(sh, 0.0, V['y1'], V['x1'], V['y1'] + 0.06, fill=PAPER, sw=0.2)        # the vestibule's glass side
    for x in (V['x0'], V['x1']):                                              # its doors, in series
        F.r(sh, x - 0.03, V['y0'], x + 0.03, V['y0'] + 0.20, fill=INK, sw=0.1)
        F.r(sh, x - 0.03, V['y0'] + 0.20 + P.DOOR, x + 0.03, V['y1'], fill=INK, sw=0.1)
        F.door(sh, (x, V['y0'] + 0.20), (0, 1), (-1, 0), P.DOOR)
    # the kit alcove's wall and door
    A = P.KIT_ALCOVE
    nw = dict(fill=NEW, stroke=INK, sw=0.22)
    F.r(sh, A['x0'], A['y0'] - 0.10, A['x1'], A['y0'], **nw)
    F.r(sh, A['x1'] - 0.10, A['y0'], A['x1'], A['y0'] + 0.20, **nw)
    F.door(sh, (A['x1'] - 0.05, A['y0'] + 0.20), (0, 1), (1, 0), 0.85)
    # the rear: the lobby's back wall with three doors, the rooms' walls
    Lb = P.LOBBY
    for i, wc in enumerate(P.WCS):
        d0 = wc['y0'] + 0.20
        F.r(sh, Lb['x1'], wc['y0'], Lb['x1'] + 0.12, d0, **nw)
        F.r(sh, Lb['x1'], d0 + P.DOOR, Lb['x1'] + 0.12, wc['y1'], **nw)
        F.door(sh, (Lb['x1'] + 0.12, d0), (0, 1), (1, 0), P.DOOR)
        if i:
            F.r(sh, Lb['x1'], wc['y0'] - 0.06, L, wc['y0'] + 0.06, **nw)
        F.r(sh, L - 0.45, wc['y1'] - 0.75, L - 0.02, wc['y1'] - 0.35, fill=PAPER, sw=0.2)          # WC, 17 in off the side wall
        F.r(sh, Lb['x1'] + 0.75, wc['y1'] - 0.50, Lb['x1'] + 1.30, wc['y1'] - 0.06, fill=PAPER, sw=0.2)   # lavatory
        F.c(sh, Lb['x1'] + 1.10, (wc['y0'] + wc['y1']) / 2 - 0.15, 0.762, sw=0.12, dash='1.5 1')
        if wc.get('urinal'):
            F.r(sh, L - 0.40, wc['y0'] + 0.10, L - 0.02, wc['y0'] + 0.48, fill=PAPER, sw=0.2)
        F.t(sh, Lb['x1'] + 0.35, (wc['y0'] + wc['y1']) / 2, wc['name'], size=2.4, weight=600)
    F.r(sh, Lb['x0'], P.ROUTE_Y[1], Lb['x0'] + 0.0, W, sw=0.0)


def lantern_plan(sh, F):
    Lt = P.LANT
    # the double leaf, in hatch between the outer and inner faces
    lf = sh.hatch('leaf', 45, 0.9, 0.12, INK, '#d9d1c4')
    F.r(sh, Lt['x0'], Lt['y0'], Lt['x1'], Lt['y1'], fill=lf, sw=0.35)
    F.r(sh, I['x0'], I['y0'], I['x1'], I['y1'], fill=C['lant'], sw=0.3)
    # the band above (dashed, outside the outer face on the two seen sides)
    F.p(sh, [(Lt['x1'], Lt['y0'] - 0.05), (Lt['x0'] - 0.05, Lt['y0'] - 0.05), (Lt['x0'] - 0.05, Lt['y1'])], close=False,
        stroke=C['band'], sw=0.6, dash='2 1')
    # the porch: oak walls, door 1 off the route, door 2 through the box's leaves
    Lk = P.LOCK
    ow = dict(fill=C['oakd'], stroke=INK, sw=0.22)
    F.r(sh, Lk['x0'], Lk['y1'] - 0.12, Lk['x1'], Lk['y1'], **ow)
    F.r(sh, Lk['x0'], Lk['y0'], Lk['x0'] + 0.12, Lk['y1'], **ow)
    F.r(sh, Lk['x0'], Lk['y0'], P.LOCK_DOOR1['x'], Lk['y0'] + 0.12, **ow)
    F.r(sh, P.LOCK_DOOR1['x'] + P.DOOR, Lk['y0'], Lk['x1'], Lk['y0'] + 0.12, **ow)
    F.door(sh, (P.LOCK_DOOR1['x'], Lk['y0'] + 0.06), (1, 0), (0, 1), P.DOOR)
    F.r(sh, Lt['x0'], P.LOCK_DOOR2['y'], I['x0'], P.LOCK_DOOR2['y'] + P.DOOR, fill=PAPER, sw=0.2)
    F.door(sh, (I['x0'], P.LOCK_DOOR2['y']), (0, 1), (1, 0), P.DOOR)
    F.c(sh, Lk['x0'] + 0.82, Lk['y0'] + 1.25, 0.762, sw=0.12, dash='1.5 1')
    # inside: the trap (hatched), the bench, the rug, the selector, the plinths and the pair, Mother EARF
    F.r(sh, P.TRAP['x0'], I['y0'], P.TRAP['x1'], I['y1'], fill=sh.hatch('trap', -45, 0.7, 0.1, INK, '#cfc6b8'), sw=0.25)
    F.r(sh, P.BENCH['x0'], I['y0'], P.BENCH['x1'], I['y1'], fill=C['oak'], sw=0.2)
    F.r(sh, P.SWEET[0] - 1.6, I['y0'] + 0.55, P.BENCH['x0'] - 0.15, I['y1'] - 0.55, sw=0.15, dash='1 1')
    Sd = P.SELECTOR
    F.r(sh, Sd['x0'] + 0.05, Sd['y0'], Sd['x1'], Sd['y1'] - 0.05, fill=C['oak'], sw=0.2)
    for dy in (0.45, 1.25):
        F.c(sh, Sd['x0'] + 0.40, Sd['y0'] + dy, 0.15, sw=0.15)
    for (x, y) in P.STACKS:
        F.r(sh, x - 0.36, y - 0.36, x + 0.36, y + 0.36, fill=C['terr'], sw=0.2)
        F.r(sh, x - P.TROPOS['d'] / 2, y - P.TROPOS['w'] / 2, x + P.TROPOS['d'] / 2, y + P.TROPOS['w'] / 2, fill=C['ember'], sw=0.2)
    M = P.MOTHER
    F.c(sh, M['x'], M['y'], M['plinth_d'] / 2, fill=C['terr'], sw=0.25)
    F.c(sh, M['x'], M['y'], M['d'] / 2, sw=0.2, dash='2 1')
    # the listening triangle, dashed
    sx, sy = P.SWEET
    F.p(sh, [P.STACKS[0], P.STACKS[1], (sx, sy)], stroke=GREY, sw=0.12, dash='3 1.5')
    for (x, y, kind) in P.SEATS:
        if kind == 'wheelchair':
            F.r(sh, x - 0.61, y - 0.38, x + 0.61, y + 0.38, fill='#dbe6f7', stroke=C['route'], sw=0.3)
            F.t(sh, x, y - 0.12, 'W', size=2.6, weight=700, anchor='middle', fill=C['route'])
        elif kind == 'bench':
            F.c(sh, x, y, 0.08, fill=GREY, stroke='none')
        else:
            F.r(sh, x - 0.27, y - 0.27, x + 0.27, y + 0.27, fill=PAPER if kind == 'chair' else '#dbe6f7', sw=0.2)


def furniture(sh, F):
    S = P.SHOP_WALL
    F.r(sh, S['x0'], S['y0'], S['x1'], S['y1'], fill=C['oak'], sw=0.2)
    Wp = P.WINDOW_PLINTH; F.r(sh, Wp['x0'], Wp['y0'], Wp['x1'], Wp['y1'], fill=C['terr'], sw=0.2)
    T = P.SHOP_TABLE; F.r(sh, T['x0'], T['y0'], T['x1'], T['y1'], fill=C['oak'], sw=0.25)
    B = P.BACKBAR; F.r(sh, B['x0'], B['y0'], B['x1'], B['y1'], fill=C['oak'], sw=0.2)
    A = P.KIT_ALCOVE
    F.r(sh, A['x0'] + 0.05, A['y1'] - 0.70, A['x1'] - 0.15, A['y1'] - 0.05, fill='#e2e2e0', sw=0.2)
    F.t(sh, (A['x0'] + A['x1']) / 2 - 0.05, A['y1'] - 0.42, 'ICE', size=2.0, anchor='middle')
    F.r(sh, A['x0'] + 0.05, A['y1'] - 1.40, A['x1'] - 0.15, A['y1'] - 0.75, fill='#e2e2e0', sw=0.2)
    F.t(sh, (A['x0'] + A['x1']) / 2 - 0.05, A['y1'] - 1.12, 'GW', size=2.0, anchor='middle')
    Cn = P.COUNTER
    F.r(sh, Cn['x0'], Cn['y0'], Cn['x1'], Cn['y_work'], fill=sh.dots('terr', 1.0, 0.14, '#8a847a', C['terr']), sw=0.25)
    F.r(sh, Cn['x0'] - 0.04, Cn['edge'], Cn['x1'] + 0.04, Cn['y0'], fill=C['quartz'], sw=0.2)
    F.r(sh, P.LOW_END['x0'], Cn['edge'] - 0.10, P.LOW_END['x1'], Cn['y0'], fill='#dbe6f7', stroke=C['route'], sw=0.3)
    for x in P.STOOLS:
        F.c(sh, x, P.STOOL_Y, 0.19, fill=PAPER, sw=0.2)
    for x in P.LOW_SEATS:
        F.r(sh, x - 0.24, P.STOOL_Y - 0.10, x + 0.24, P.STOOL_Y + 0.38, fill=PAPER, sw=0.2)
    Bq = P.BANQ
    F.r(sh, Bq['x0'], Bq['y0'], Bq['x1'], Bq['y1'], fill='#8a3b2c', sw=0.22)
    for x in P.BANQ_TABLES:
        y0 = Bq['y1'] + 0.08
        F.r(sh, x - P.BANQ_TABLE['w'] / 2, y0, x + P.BANQ_TABLE['w'] / 2, y0 + P.BANQ_TABLE['d'], fill=C['quartz'], sw=0.2)
        F.r(sh, x - 0.22, y0 + 0.75, x + 0.22, y0 + 1.17, fill=PAPER, sw=0.2)


def route(sh, F):
    """The accessible route: one straight 64 in band from the door to the rear exit; the exits."""
    F.r(sh, 0.0, 0.02, L, P.ROUTE_Y[1] - 0.02, fill='#2f6fd014', stroke=C['route'], sw=0.25, dash='3 1.5')
    for x in (2.0, 9.0, 17.0):
        a, b = F(x, 0.80); sh.poly([(a + 3, b), (a - 1.5, b - 2.2), (a - 1.5, b + 2.2)], fill=C['route'], sw=0)
    F.t(sh, 9.6, 0.62, "ACCESSIBLE ROUTE AND EXIT ACCESS · 5'-4\" CLEAR", size=2.3, weight=600, fill=C['route'], spacing=0.3)
    for (x, y, lab) in ((-0.4, 0.8, 'EXIT 1'), (L + 0.45, 0.70, 'EXIT 2')):
        a, b = F(x, y); sh.text(a, b, lab, size=2.4, weight=700, fill=C['exit'], anchor='middle', rot=-90)


def labels(sh, F):
    def room(x, y, name, sub=()):
        F.tag(sh, x, y, name, size=3.0)
        for i, s_ in enumerate(sub):
            a, b = F(x, y); sh.text(a, b + 4.2 + i * 3.4, s_, size=2.3, anchor='middle', fill=GREY)
    room(3.0, 5.3, 'Shop', ['oak shelves to 10\'-6"', 'terrazzo floor'])
    room(9.9, 3.25, 'Bar', ['about 24 by CBC 1004.5', 'quartzite top, terrazzo die'])
    room((I['x0'] + P.SWEET[0]) / 2 + 0.5, I['y1'] - 0.45, 'The lantern', ['listening room, 20 seats'])
    room(P.LOCK['x0'] + 0.82, P.LOCK['y1'] - 0.55, 'Porch', ['sound lock'])
    room(P.LOBBY['x0'] + 0.62, P.W - 0.6, 'Lobby', [])
    room(1.9, 1.15, 'Vestibule', [])
    F.t(sh, P.TRAP['x0'] + 0.45, YC, 'BASS TRAP 3\'-0" DEEP', size=2.2, weight=600, anchor='middle', rot=-90)
    a, b = F(P.SWEET[0], P.SWEET[1] - 1.05); sh.text(a, b, 'sweet spot = the wheelchair space', size=2.2, anchor='middle', fill=C['route'])
    a, b = F(P.MOTHER['x'], P.MOTHER['y'] + 0.85); sh.text(a, b, 'Mother EARF', size=2.2, anchor='middle')
    a, b = F(P.LANT['x0'] + 2.4, P.LANT['y0'] - 0.25); sh.text(a, b, 'lit acrylic band above, 3.45–3.90 m', size=2.0, fill='#b07020')


def dims(sh, F):
    F.dim(sh, 0, W + P.WALL, L, W + P.WALL, 12, ftin(L))
    xs = [0, P.SHOP_X1, P.BAR_X[1], P.LANT['x1'], L]
    for a, b in zip(xs, xs[1:]):
        F.dim(sh, a, W + P.WALL, b, W + P.WALL, 6)
    F.dim(sh, -0.30, 0, -0.30, W, 8, ftin(W))
    F.dim(sh, I['x0'], I['y0'] + 0.25, I['x1'], I['y0'] + 0.25, -3, 'inside ' + ftin(I['x1'] - I['x0']))
    F.dim(sh, I['x1'] - 0.2, I['y0'], I['x1'] - 0.2, I['y1'], 3, ftin(I['y1'] - I['y0']))


def plan_sheet():
    sh = Sheet()
    frame(sh, 'A-101', 'Floor plan', "1/4\" = 1'-0\" · 2,000 sq ft · posted load about 53",
          notes=[('THE IDEA', ['The listening room\'s isolation, a room', 'within the room, is the building\'s one',
                               'object: an oak box on its own floated', 'floor, lit by a band of acrylic fins.']),
                 ('READ WITH', ['A-102 ceiling and services; A-201', 'sections; DESIGN.md for the numbers.'])])
    F = Frame(150.0, 250.0, S4)
    F.r(sh, 0, 0, P.SHOP_X1, W, fill=C['shop'], stroke='none')
    F.r(sh, P.LOBBY['x0'], 0, L, W, fill=C['rear'], stroke='none')
    route(sh, F)
    walls(sh, F)
    furniture(sh, F)
    lantern_plan(sh, F)
    labels(sh, F)
    dims(sh, F)
    # section and elevation marks
    a0, a1 = F(-1.3, YC), F(L + 1.0, YC)
    sh.line(a0[0] + 5, a0[1], a1[0] - 5, a1[1], sw=0.25, dash='6 2 1 2')
    sh.section_mark(a0[0], a0[1], 'A', 'A-201', (0, -1)); sh.section_mark(a1[0], a1[1], 'A', 'A-201', (0, -1))
    b0, b1 = F(P.SWEET[0] + 0.3, -1.2), F(P.SWEET[0] + 0.3, W + 1.6)
    sh.line(b0[0], b0[1] - 5, b1[0], b1[1] + 5, sw=0.25, dash='6 2 1 2')
    sh.section_mark(b0[0], b0[1], 'B', 'A-201', (-1, 0)); sh.section_mark(b1[0], b1[1], 'B', 'A-201', (-1, 0))
    e1 = F(-2.4, W / 2); sh.section_mark(e1[0], e1[1], '1', 'A-301', (1, 0))
    e2 = F(12.3, W / 2 + 0.6); sh.section_mark(e2[0], e2[1], '2', 'A-301', (1, 0))
    sh.scale_bar(150, 300, S4)
    sh.north(330, 300)
    notes = ['1. Two exits (CBC 1006.2.1: over 49 occupants): the front door and the rear door, 24 m apart, joined by',
             "   one straight route 5'-4\" clear (ADA 403; 60 in to pass and turn). The lantern holds 20, under 50: one door.",
             '2. Posted load about 53 by CBC Table 1004.5 (shop 60 gross; bar 15 net; the lantern by its seats). Under 100,',
             '   so CBC 903.2.1.2 does not require sprinklers for the A-2 by its load; the building may still have them.',
             '3. The lantern stands free: a 60 mm gap to the party wall, a 60 mm gap to the ceiling, its floor a 100 mm',
             '   slab on spring mounts (about 7 Hz) in a 175 mm cut in the existing slab, so it finishes flush: no step.',
             '4. The ice machine and the glasswasher sit in a gasketed alcove at the shop end of the back bar, 6.5 m',
             '   from the lantern\'s face. Restroom plumbing stays outside the box.',
             '5. The wheelchair space (30 x 48 in, with its companion seat) is on the sweet spot, row 1, floor level:',
             '   ADA 221.2.1.1 asks one for 4 to 25 seats; 221.2.3.2 Exc. 1 waives vertical dispersion under 300.',
             '6. Three single-user all-gender rooms, one with a urinal: CPC Table 422.1 at a load of about 53 asks',
             '   3 water closets and 1 urinal (to confirm with DBI). Each holds a 60 in turning circle.',
             "7. The bar's accessible run: 60 in at 34 in (CBC 11B-902.3), at its near end."]
    sh.lines_of(150, 340, notes, size=2.6, lead=1.5)
    return sh


# --- RCP --------------------------------------------------------------------------------------------------------------
def rcp_sheet():
    sh = Sheet()
    frame(sh, 'A-102', 'Reflected ceiling plan', "1/4\" = 1'-0\" · ceilings, light, air",
          notes=[('CEILINGS', ["Shop and bar: 13'-0\", acoustic plaster on", 'resilient clips under the joists (a second',
                               'line to the flats), 12 in plenum.', "The lantern's lid: 11'-2\" inside, oak slats",
                               'over wool, carried by its own walls.', "Rear rooms: 8'-6\"; a plant deck above."])])
    F = Frame(150.0, 250.0, S4)
    walls(sh, F)
    Lt = P.LANT
    F.r(sh, Lt['x0'], Lt['y0'], Lt['x1'], Lt['y1'], fill=sh.hatch('leaf', 45, 0.9, 0.12, INK, '#d9d1c4'), sw=0.35)
    F.r(sh, I['x0'], I['y0'], I['x1'], I['y1'], fill=C['lant'], sw=0.3)
    x = I['x0'] + 0.05
    while x < I['x1']:
        F.l(sh, x, I['y0'], x, I['y1'], sw=0.08, stroke=GREY); x += 0.28
    F.p(sh, [(Lt['x1'], Lt['y0'] - 0.05), (Lt['x0'] - 0.05, Lt['y0'] - 0.05), (Lt['x0'] - 0.05, Lt['y1'])], close=False,
        stroke=C['band'], sw=1.2)
    # the slot diffusers, the downlights, the Hemispheres over the counter
    F.r(sh, 1.0, 0.70, P.LANT['x0'] - 1.8, 0.74, fill=INK, sw=0.1)
    F.r(sh, P.SHOP_X1 + 0.5, W - 2.10, P.LANT['x0'] - 0.6, W - 2.06, fill=INK, sw=0.1)
    for x_ in [1.6 + 1.45 * i for i in range(8)]:
        F.c(sh, x_, 3.4, 0.07, fill=PAPER, sw=0.25)
    for x_ in P.STOOLS + [7.6, 8.4]:
        F.c(sh, x_, P.COUNTER['y0'] + 0.25, 0.07, fill=PAPER, sw=0.25)
    by = (P.COUNTER['edge'] + P.COUNTER['y_work']) / 2
    for x_ in (8.6, 10.0, 11.4):
        F.c(sh, x_, by, 0.20, fill='#5a5a60', sw=0.2)
    for x_ in (4.0, 4.9):
        F.c(sh, x_, 3.75, 0.20, fill='#c9c3e0', sw=0.2)
    for i, (x_, y_) in enumerate(P.STACKS):
        F.c(sh, x_ + 1.0, y_ + (0.5 if y_ < YC else -0.5), 0.06, fill=INK, sw=0.1)
    F.c(sh, P.MOTHER['x'] - 0.25, P.MOTHER['y'] - 0.6, 0.06, fill='#d07a20', sw=0.1)
    F.l(sh, P.TRAP['x0'] - 0.25, I['y0'] + 0.3, P.TRAP['x0'] - 0.25, I['y1'] - 0.3, sw=0.6, stroke='#d07a20')
    # the lantern's air: its own fan coil on the plant deck over the rear rooms; supply and return through lined
    # silencers at the back wall, low-velocity linear grilles in the lid
    F.r(sh, P.LOBBY['x1'] + 0.2, 3.0, P.LOBBY['x1'] + 1.6, 5.0, fill='#e8e4dc', sw=0.3, dash='2 1')
    F.t(sh, P.LOBBY['x1'] + 0.9, 4.0, 'FCU', size=2.4, weight=700, anchor='middle')
    for (y_, lab) in ((I['y0'] + 1.0, 'S'), (I['y1'] - 1.0, 'R')):
        F.r(sh, I['x1'] - 0.1, y_ - 0.25, P.LOBBY['x1'] + 0.2, y_ + 0.25, sw=0.25, dash='2 1', fill='#f2efe9')
        F.t(sh, (I['x1'] + P.LOBBY['x1']) / 2, y_ - 0.08, lab + ' silencer', size=2.0, anchor='middle')
        F.r(sh, I['x0'] + 1.0, y_ - 0.04, I['x1'] - 1.0, y_ + 0.04, fill=INK, sw=0.1)
    F.r(sh, P.LOBBY['x0'], P.ROUTE_Y[1], L, W, fill='#efefec80', sw=0.2, dash='1 1')
    legend = ['○  downlight, 2700 K, dimmed (the counter, the tables, the shop)', '●  Hemisphere (the product) over the counter and the shop table',
              '▬  linear slot diffuser (supply), under 2 m/s face velocity', '•  spot inside the lantern: the pair, Mother EARF (its coloured shadow), the trap\'s graze',
              '━  the lantern\'s lit band (amber line), seen from the bar and the route',
              'FCU  the lantern\'s own fan coil on the plant deck; supply and return through lined silencers and flexible',
              '     connectors at the box\'s back wall; grilles in the lid at under 1.5 m/s (NC 15–20 target)']
    sh.lines_of(150, 300, legend, size=2.7, lead=1.6)
    sh.scale_bar(600, 300, S4)
    return sh


# --- sections ------------------------------------------------------------------------------------------------------------
def section_a(sh, F):
    """Long section at y = YC through the lantern, looking toward the left-hand wall."""
    ex = dict(fill=EX, stroke=INK, sw=0.25)
    F.r(sh, -0.3, -0.30, L + 0.3, 0.0, fill=sh.hatch('earth', 45, 1.2, 0.1, INK, '#e9e5de'), sw=0.25)
    F.r(sh, P.LANT['x0'], -P.FLOAT['depth'], P.LANT['x1'], 0.0, fill=PAPER, sw=0.2)               # the cut
    F.r(sh, I['x0'], -0.10, I['x1'], 0.0, fill='#cfc7ba', sw=0.25)                                 # the floated slab
    x = I['x0'] + 0.4
    while x < I['x1'] - 0.2:
        F.c(sh, x, -0.135, 0.03, sw=0.15); x += 0.9                                                 # spring mounts
    F.r(sh, -0.3, P.JOISTS, L + 0.3, P.JOISTS + 0.30, fill=sh.hatch('joist', 0, 1.0, 0.1, INK, '#f1ede6'), sw=0.25)
    F.r(sh, -0.3, P.JOISTS + 0.30, L + 0.3, P.JOISTS + 0.33, fill=EX, sw=0.1)
    F.t(sh, 3.0, P.JOISTS + 0.45, 'FLATS ABOVE', size=2.6, weight=600, fill=GREY)
    F.l(sh, 0.0, P.CEIL, P.LANT['x0'] - 0.0, P.CEIL, sw=0.5); F.l(sh, P.LANT['x1'], P.CEIL, P.LOBBY['x0'], P.CEIL, sw=0.5)
    F.l(sh, P.LANT['x0'], P.CEIL, P.LANT['x1'], P.CEIL, sw=0.5)
    # the shopfront
    F.r(sh, -0.12, 0.0, 0.0, P.BULKHEAD, fill=C['terr'], sw=0.2)
    F.r(sh, -0.08, P.BULKHEAD, -0.04, 3.30, fill='#cfe0ea', sw=0.15)
    F.r(sh, -0.30, 3.30, 0.0, P.JOISTS, **ex)
    # beyond: the back bar's shelves and the counter, light
    lg = dict(stroke=GREY, sw=0.15)
    F.r(sh, P.BACKBAR['x0'], 0, P.BACKBAR['x1'], P.BACKBAR['h'], fill='none', **lg)
    for z in (1.45, 1.85, 2.25):
        F.l(sh, P.BACKBAR['x0'] + 0.3, z, P.BACKBAR['x1'] - 0.3, z, **lg)
    F.r(sh, P.COUNTER['x0'], 0, P.COUNTER['x1'], 1.07, fill='#f2efea', **lg)
    F.r(sh, P.SHOP_WALL['x0'], 0, P.SHOP_WALL['x1'], P.SHOP_WALL['z1'], fill='none', **lg)
    # the lantern cut: the two leaves at each end, the lid, the band; inside, Mother EARF cut, the pair beyond
    lf = sh.hatch('leaf', 45, 0.9, 0.12, INK, '#d9d1c4')
    Lt = P.LANT
    F.r(sh, Lt['x0'], 0.0, I['x0'], Lt['h'], fill=lf, sw=0.3)
    F.r(sh, I['x1'], 0.0, Lt['x1'], Lt['h'], fill=lf, sw=0.3)
    F.r(sh, I['x0'], I['h'], I['x1'], I['h'] + P.LID, fill=sh.hatch('lid', -45, 0.9, 0.12, INK, '#e3dccf'), sw=0.3)
    F.r(sh, Lt['x0'] - 0.02, P.BAND['z0'], Lt['x0'] + 0.06, P.BAND['z1'], fill=C['band'], sw=0.2)
    F.r(sh, P.TRAP['x0'], 0.0, P.TRAP['x1'], I['h'], fill=sh.hatch('trap', -45, 0.7, 0.1, INK, '#cfc6b8'), sw=0.25)
    F.r(sh, P.BENCH['x0'], 0.0, P.BENCH['x1'], P.BENCH['z'], fill=C['oak'], sw=0.2)
    M = P.MOTHER
    cz = M['plinth_h'] + 0.08 + M['d'] / 2 * 0.94
    F.r(sh, M['x'] - M['plinth_d'] / 2, 0.0, M['x'] + M['plinth_d'] / 2, M['plinth_h'], fill=C['terr'], sw=0.25)
    F.c(sh, M['x'], cz, M['d'] / 2, sw=0.3, stroke='#7a4fa0')
    F.l(sh, M['x'] - math.sin(math.radians(23.4)) * 0.62, cz - math.cos(math.radians(23.4)) * 0.62,
        M['x'] + math.sin(math.radians(23.4)) * 0.62, cz + math.cos(math.radians(23.4)) * 0.62, sw=0.2, stroke='#7a4fa0')
    x, y = P.STACKS[1]
    F.r(sh, x - 0.36, 0.0, x + 0.36, P.TROPOS['plinth'], fill='none', stroke=GREY, sw=0.2)
    F.r(sh, x - P.TROPOS['d'] / 2, P.TROPOS['plinth'], x + P.TROPOS['d'] / 2, P.TROPOS['plinth'] + P.TROPOS['h'], fill='none', stroke=C['ember'], sw=0.3)
    F.l(sh, x, 1.10, P.SWEET[0], 1.10, sw=0.12, dash='2 1', stroke=GREY)
    F.t(sh, (x + P.SWEET[0]) / 2, 1.18, 'ears at 1.10 m, seated', size=2.0, anchor='middle', fill=GREY)
    # the rear rooms' ceiling and the plant deck with the fan coil, its duct to the lantern through silencers
    F.r(sh, P.LOBBY['x0'], P.CEIL_REAR, L, P.CEIL_REAR + 0.15, fill=sh.hatch('lid', -45, 0.9, 0.12), sw=0.25)
    F.r(sh, P.LOBBY['x1'] + 0.2, P.CEIL_REAR + 0.15, P.LOBBY['x1'] + 1.6, P.CEIL_REAR + 0.85, fill='#e8e4dc', sw=0.3)
    F.t(sh, P.LOBBY['x1'] + 0.9, P.CEIL_REAR + 0.42, 'FCU', size=2.2, weight=700, anchor='middle')
    F.r(sh, I['x1'] - 0.1, 3.05, P.LOBBY['x1'] + 0.2, 3.30, sw=0.25, dash='2 1', fill='#f2efe9')
    F.r(sh, P.LOBBY['x1'] - 0.06, 0.0, P.LOBBY['x1'] + 0.06, P.CEIL_REAR, fill=NEW, sw=0.2)
    F.r(sh, L, -0.3, L + 0.3, P.JOISTS + 0.33, **ex)
    # dimensions
    F.dim(sh, -0.5, 0.0, -0.5, P.JOISTS, 8, ftin(P.JOISTS))
    F.dim(sh, I['x0'] + 0.3, 0.0, I['x0'] + 0.3, I['h'], -4, 'inside ' + ftin(I['h']))
    F.dim(sh, Lt['x0'] - 0.3, P.BAND['z0'], Lt['x0'] - 0.3, P.BAND['z1'], 4, 'band 1\'-6"')
    for (x_, s_) in ((3.0, 'SHOP'), (9.6, 'BAR'), (17.0, 'THE LANTERN'), (22.7, 'REAR')):
        F.tag(sh, x_, -0.75, s_, size=2.6)


def section_b(sh, F):
    """Across at the sweet spot, looking toward the speakers: the route, the box in its shell."""
    ex = dict(fill=EX, stroke=INK, sw=0.25)
    F.r(sh, -0.3, -0.30, W + 0.3, 0.0, fill=sh.hatch('earth', 45, 1.2, 0.1, INK, '#e9e5de'), sw=0.25)
    F.r(sh, P.LANT['y0'], -P.FLOAT['depth'], P.LANT['y1'], 0.0, fill=PAPER, sw=0.2)
    F.r(sh, I['y0'], -0.10, I['y1'], 0.0, fill='#cfc7ba', sw=0.25)
    y = I['y0'] + 0.3
    while y < I['y1'] - 0.1:
        F.c(sh, y, -0.135, 0.03, sw=0.15); y += 0.8
    F.r(sh, -0.30, -0.3, 0.0, P.JOISTS + 0.33, **ex); F.r(sh, W, -0.3, W + 0.30, P.JOISTS + 0.33, **ex)
    F.r(sh, -0.3, P.JOISTS, W + 0.3, P.JOISTS + 0.30, fill=sh.hatch('joist', 0, 1.0, 0.1, INK, '#f1ede6'), sw=0.25)
    F.t(sh, 0.4, P.JOISTS + 0.6, 'FLATS ABOVE', size=2.6, weight=600, fill=GREY)
    F.l(sh, 0.0, P.CEIL, P.LANT['y0'], P.CEIL, sw=0.5); F.l(sh, P.LANT['y0'], P.CEIL, W, P.CEIL, sw=0.5)
    for y_ in (0.4, 1.2):
        F.l(sh, y_, P.CEIL, y_, P.JOISTS, sw=0.12, dash='1 0.8')                                  # resilient hangers
    lf = sh.hatch('leaf', 45, 0.9, 0.12, INK, '#d9d1c4')
    Lt = P.LANT
    F.r(sh, Lt['y0'], 0.0, I['y0'], Lt['h'], fill=lf, sw=0.3)
    F.r(sh, I['y1'], 0.0, Lt['y1'], Lt['h'], fill=lf, sw=0.3)
    F.r(sh, I['y0'], I['h'], I['y1'], I['h'] + P.LID, fill=sh.hatch('lid', -45, 0.9, 0.12, INK, '#e3dccf'), sw=0.3)
    F.r(sh, Lt['y0'] - 0.02, P.BAND['z0'], Lt['y0'] + 0.06, P.BAND['z1'], fill=C['band'], sw=0.2)
    # beyond: the pair on their plinths and Mother EARF between them
    for (x, y) in P.STACKS:
        F.r(sh, y - 0.36, 0.0, y + 0.36, P.TROPOS['plinth'], fill='#f2efea', stroke=GREY, sw=0.2)
        F.r(sh, y - P.TROPOS['w'] / 2, P.TROPOS['plinth'], y + P.TROPOS['w'] / 2, P.TROPOS['plinth'] + P.TROPOS['h'], fill='#f3dcd6', stroke=C['ember'], sw=0.3)
    M = P.MOTHER
    cz = M['plinth_h'] + 0.08 + M['d'] / 2 * 0.94
    F.r(sh, M['y'] - M['plinth_d'] / 2, 0.0, M['y'] + M['plinth_d'] / 2, M['plinth_h'], fill='#f2efea', stroke=GREY, sw=0.2)
    F.c(sh, M['y'], cz, M['d'] / 2, sw=0.3, stroke='#7a4fa0')
    # cut: the wheelchair space and the companion seat on the sweet spot
    F.r(sh, P.SWEET[1] - 0.55 - 0.38, 0.0, P.SWEET[1] - 0.55 + 0.38, 0.05, fill='#dbe6f7', stroke=C['route'], sw=0.3)
    F.t(sh, P.SWEET[1] - 0.55, 0.15, 'W', size=2.6, weight=700, anchor='middle', fill=C['route'])
    F.t(sh, 0.81, 1.0, 'ROUTE', size=2.4, weight=600, anchor='middle', fill=C['route'])
    F.dim(sh, 0.0, -0.6, P.ROUTE_Y[1], -0.6, -4, "5'-4\"")
    F.dim(sh, I['y0'], -0.6, I['y1'], -0.6, -4, 'inside ' + ftin(I['y1'] - I['y0']))
    F.dim(sh, W + 0.5, 0.0, W + 0.5, I['h'], -8, 'inside ' + ftin(I['h']))
    F.dim(sh, W + 0.5, I['h'] + P.LID, W + 0.5, P.CEIL, -8, '2 in gap')


def sections_sheet():
    sh = Sheet()
    frame(sh, 'A-201', 'Sections', "A long, 1/4\" = 1'-0\" · B across, 3/8\" = 1'-0\"",
          notes=[('ISOLATION', ['Box in box: the lantern\'s floor, walls', 'and lid touch the building only through',
                                'its springs. Targets for the acoustician:', 'music in the flats under 45 dBC at night',
                                '(Police Code 2909, ambient floor 45 dBC);', 'NC 15–20 inside the box.'])])
    FA = Frame(80.0, 165.0, S4)
    section_a(sh, FA)
    sh.text(80, 42, 'A   LONG SECTION THROUGH THE LANTERN', size=3.4, weight=700)
    FB = Frame(560.0, 420.0, S38)
    section_b(sh, FB)
    sh.text(560, 260, 'B   CROSS SECTION AT THE SWEET SPOT', size=3.4, weight=700)
    notes = ['The lantern\'s wall, outside in: oak skin 20 mm; the band\'s cavity 60 mm (fins in it, LED and drivers serviced',
             'from the route through removable outer fin panels, never through the seal); outer leaf, 2 x 5/8 in gypsum on',
             '3-5/8 in studs; 50 mm air; inner leaf, 2 x 5/8 in gypsum on 2-1/2 in studs with 50 mm wool; oak slats inside.',
             'The lid: CLT 200 + 2 x 5/8 in gypsum + 100 mm wool + oak slats, spanning wall to wall, never hung from the joists.',
             'The floor: 100 mm concrete on spring jack-up mounts (about 7 Hz), end-grain oak on top, in a 175 mm cut.',
             'Every service enters through a flexible connector; the two doors are gasketed sets with drop seals.',
             'Demountable: the oak, the leaves and the lid are bolted panels, numbered, so the box can leave with the lease.']
    sh.lines_of(80, 300, notes, size=2.6, lead=1.55)
    return sh


# --- elevations ------------------------------------------------------------------------------------------------------------
def elevation_street(sh, F):
    """From the street: a = W - y (the entry at the right), z up; the flats above, indicative."""
    ex = dict(fill='#d9d4cb', stroke=INK, sw=0.25)
    T = P.WALL
    F.r(sh, -T, -0.15, W + T, 10.6, fill='#ece8e1', sw=0.3)                                     # the building's face
    for zf in (5.0, 8.0):
        for a in (1.2, 3.4, 5.6):
            F.r(sh, a, zf, a + 1.1, zf + 1.9, fill='#f7f5f1', stroke=GREY, sw=0.2)
    F.r(sh, -T, 4.30, W + T, 4.60, fill='#c9c3b8', sw=0.2)                                      # the belt course
    F.r(sh, -T, 3.38, W + T, 4.30, fill='#2a2826', sw=0.25)                                     # the fascia
    F.t(sh, W / 2, 3.66, 'E A R F', size=9.0, weight=700, anchor='middle', fill='#c9a46a', spacing=3)
    F.r(sh, -T, 0.0, 0.0, 3.38, **ex); F.r(sh, W - P.ENTRY['y0'], 0.0, W + T, 3.38, **ex)
    a0, a1 = W - P.GLASS[1], W - P.GLASS[0]
    F.r(sh, a0, 0.0, a1, P.BULKHEAD, fill=C['terr'], sw=0.25)
    F.r(sh, a0, P.BULKHEAD, a1, 3.30, fill='#cfdfe6', sw=0.25)
    F.r(sh, (a0 + a1) / 2 - 0.03, P.BULKHEAD, (a0 + a1) / 2 + 0.03, 3.30, fill=INK, sw=0.1)
    F.r(sh, -T, 3.30, W + T, 3.38, fill=INK, sw=0.1)
    # through the glass, 80 ft in: the lantern's band
    F.r(sh, W - P.LANT['y1'], 2.55, W - P.LANT['y0'], 2.68, fill=C['band'], stroke='none')
    F.t(sh, (a0 + a1) / 2, 2.30, "the lantern's band, 43 ft in, seen through the glass", size=2.2, anchor='middle', fill='#8a5a20')
    # the entry alcove and its door
    e0, e1 = W - P.ENTRY['y1'], W - P.ENTRY['y0']
    F.r(sh, e0, 0.0, e1, 3.30, fill='#bfb8ad', sw=0.25)
    F.r(sh, e0 + 0.20, 0.0, e0 + 0.20 + P.DOOR, 2.40, fill='#cfdfe6', sw=0.3)
    F.r(sh, e0 + 0.20 + P.DOOR - 0.12, 0.85, e0 + 0.20 + P.DOOR - 0.09, 1.25, fill='#b08a40', sw=0.1)
    F.l(sh, -1.0, 0.0, W + 1.0, 0.0, sw=0.5)
    F.dim(sh, -T, -0.6, W + T, -0.6, -4, "25'-0\" + walls")
    F.dim(sh, W + 0.8, 0.0, W + 0.8, P.BULKHEAD, -6, '18"')
    F.dim(sh, W + 0.8, P.BULKHEAD, W + 0.8, 3.30, -6)


def elevation_lantern(sh, F):
    """The lantern's face from the bar: a = W - y, z up; the porch in front at the right, the route beyond it."""
    Lt = P.LANT
    F.r(sh, -0.3, 0.0, W + 0.3, 0.0, sw=0.5)
    F.l(sh, -0.3, P.CEIL, W + 0.3, P.CEIL, sw=0.4)
    F.r(sh, -0.3, P.CEIL, W + 0.3, P.JOISTS, fill=sh.hatch('joist', 0, 1.0, 0.1, INK, '#f1ede6'), sw=0.2)
    a0, a1 = W - Lt['y1'], W - Lt['y0']
    F.r(sh, a0, 0.10, a1, P.BAND['z0'], fill=C['oak'], sw=0.3)
    a = a0
    while a < a1 - 0.03:
        F.l(sh, a, 0.10, a, P.BAND['z0'] - 0.02, sw=0.09, stroke=C['oakd']); a += P.BAFFLE_SLOTS['pitch']
    F.r(sh, a0, P.BAND['z0'], a1, P.BAND['z1'], fill='#f0b866', sw=0.3)
    a = a0
    while a < a1:
        F.l(sh, a, P.BAND['z0'], a, P.BAND['z1'] - 0.02, sw=0.1, stroke='#b5752a'); a += P.BAND['pitch'] * 2
    F.r(sh, a0, 0.0, a1, 0.10, fill=C['glow'], sw=0.2)
    # the porch (in front), the route beyond
    Lk = P.LOCK
    F.r(sh, W - Lk['y1'], 0.0, W - Lk['y0'], 2.70, fill='#b99a72', sw=0.35)
    F.t(sh, W - (Lk['y0'] + Lk['y1']) / 2, 1.45, 'PORCH', size=2.6, weight=600, anchor='middle')
    F.t(sh, W - (Lk['y0'] + Lk['y1']) / 2, 1.20, 'door 1 off the route, at its side', size=2.0, anchor='middle', fill=GREY)
    F.t(sh, W - 0.81, 1.2, 'ROUTE', size=2.4, weight=600, anchor='middle', fill=C['route'], rot=-90)
    F.r(sh, W - 0.60, 2.15, W - 0.20, 2.30, fill=C['exit'], sw=0.1)
    # the back bar's end at the left
    F.r(sh, 0.0, 0.0, 0.60, P.BACKBAR['h'], fill=C['oak'], sw=0.25)
    F.dim(sh, a1 + 0.5, 0.0, a1 + 0.5, P.BAND['z0'], -6)
    F.dim(sh, a1 + 0.5, P.BAND['z0'], a1 + 0.5, P.BAND['z1'], -6, '1\'-6"')
    F.dim(sh, a0, -0.5, a1, -0.5, -4, ftin(a1 - a0))
    F.t(sh, (a0 + a1) / 2 - 0.6, 1.9, 'SLOTTED OAK BAFFLE', size=2.6, weight=700, anchor='middle')
    F.t(sh, (a0 + a1) / 2 - 0.6, 1.65, '60 mm battens, 12 mm slots, wool behind', size=2.1, anchor='middle')
    F.t(sh, (a0 + a1) / 2, P.BAND['z1'] + 0.12, 'LIT BAND: CAST SMOKE ACRYLIC FINS, 20 mm ON 28 mm, LED BEHIND', size=2.1,
        weight=600, anchor='middle', fill='#8a5a20')
    F.t(sh, (a0 + a1) / 2, -0.25, 'a warm line at the foot, 100 mm recess', size=2.0, anchor='middle', fill='#8a5a20')


def elevations_sheet():
    sh = Sheet()
    frame(sh, 'A-301', 'Elevations', "3/8\" = 1'-0\" · 1 the street · 2 the lantern from the bar",
          notes=[('MATERIALS', ['Floors: honed epoxy terrazzo (marble', 'and glass chips); end-grain oak inside', 'the lantern.',
                                'Bar top: honed quartzite. Die and', 'plinths: terrazzo with 15% acrylic',
                                'offcut chips (no wear there).', 'Oak: oiled white oak, fumed a shade.',
                                'Acrylic: the band only, behind the oak line.'])])
    F1 = Frame(70.0, 420.0, S38)
    elevation_street(sh, F1)
    sh.text(70, 60, '1   THE STREET', size=3.4, weight=700)
    F2 = Frame(420.0, 420.0, S38)
    elevation_lantern(sh, F2)
    sh.text(420, 270, '2   THE LANTERN FROM THE BAR', size=3.4, weight=700)
    return sh


def axo_sheet():
    sh = Sheet()
    frame(sh, 'A-401', 'Axonometric', 'the model, cut at 8\'-6"; the lantern whole',
          notes=[('WHAT IT SHOWS', ['The render model itself (kit44), cut so', 'the plan reads from above; the lantern',
                                    'stays whole: the one object.'])])
    img = os.path.join(OUT, 'axo.png')
    if os.path.exists(img):
        uri = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(OUT, 'axo.jpg'), 'rb').read()).decode() \
            if os.path.exists(os.path.join(OUT, 'axo.jpg')) else 'axo.png'
        x0, y0, w, h = 20.0, 20.0, 780.0, 520.0
        sh.image(x0, y0, w, h, uri)
        an = os.path.join(OUT, 'axo.anchors.json')
        if os.path.exists(an):
            for k, (u, v) in json.load(open(an)).items():
                px, py = x0 + u * w, y0 + v * h
                sh.circle(px, py, 0.9, fill=INK, sw=0.1)
                tx = px + (14 if u < 0.6 else -14); ty = py - 10
                sh.line(px, py, tx, ty, sw=0.18)
                sh.text(tx + (1 if u < 0.6 else -1), ty - 1, k, size=2.6, weight=600, anchor='start' if u < 0.6 else 'end')
    return sh


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('A-101', plan_sheet), ('A-102', rcp_sheet), ('A-201', sections_sheet), ('A-301', elevations_sheet),
                     ('A-401', axo_sheet)):
        open(os.path.join(OUT, f'{name}.svg'), 'w').write(fn().svg())
        print(os.path.join(OUT, f'{name}.svg'))


if __name__ == '__main__':
    main()
