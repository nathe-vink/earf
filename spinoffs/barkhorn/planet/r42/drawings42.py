"""Planet EARF, round 42: the drawing set, every line from plan42.py.

    python3 spinoffs/barkhorn/planet/r42/drawings42.py           # SVGs into spinoffs/barkhorn/planet/r42/drawings/
    node spinoffs/barkhorn/planet/r42/sheets42.mjs spinoffs/barkhorn/planet/r42/drawings spinoffs/.../drawings/A-*.svg

A-000 the house in numbers (areas, occupant load, seats, the code's thresholds), A-101 the floor plan, A-102 the
reflected ceiling plan and the lamps, A-201 two sections. ARCH D sheets (36 x 24 in), plans and the long section at
1/4" = 1'-0", the cross section at 3/8" = 1'-0".
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan42 as P                                                   # noqa: E402
from svg42 import Sheet, Frame, ftin, INK, GREY, LIGHT, PAPER          # noqa: E402

OUT = os.path.join(HERE, 'drawings')
S4 = 1000 / 48.0                  # 1/4" = 1'-0": paper mm per metre
S38 = 1000 / 32.0                 # 3/8" = 1'-0"
PLAN_O = (112.0, 300.0)           # the paper point of the plan's origin (x = 0 at the glass, y = 0 the right wall)
SHEETS = [('A-000', 'The house in numbers'), ('A-101', 'Floor plan'), ('A-102', 'Reflected ceiling plan'),
          ('A-201', 'Sections'), ('A-301', 'Axonometric')]
EXISTING = '#2a2927'
NEW = '#77736c'
TINT = {'smoke': '#4a4a50', 'tropos': '#3f3e44', 'fog': '#e9e7e2', 'ember': '#c8452f', 'zinc': '#b8b6b0',
        'oak': '#b89c78', 'leather': '#6b3a2a', 'mohair': '#5b4a3c', 'felt': '#3a3532', 'route': '#2f6fd0',
        'exit': '#1d8a4e', 'shop': '#f3ede2', 'boh': '#efefec', 'listen': '#efe9e4'}
W, L = P.W, P.L


# --- shared: the shell -------------------------------------------------------------------------------------------------
def shell(sh, F, light=False):
    """Existing walls in poché, the shopfront, the new partitions; the doors and their swings."""
    ex = dict(fill=LIGHT if light else EXISTING, stroke=INK, sw=0.25)
    nw = dict(fill=PAPER if light else NEW, stroke=INK, sw=0.25)
    T = P.WALL
    F.r(sh, 0, -T, L + T, 0, **ex)                                   # right party wall
    F.r(sh, 0, W, L + T, W + T, **ex)                                # left party wall
    F.r(sh, L, 0, L + T, P.REAR_EXIT_Y, **ex)                        # back wall, the rear exit's opening left
    F.r(sh, L, P.REAR_EXIT_Y + P.DOOR_W, L + T, W, **ex)
    # the shopfront: a bulkhead and glass to the alcove, the pier beyond it
    F.r(sh, -0.30, -T, 0, 0.0, **ex)
    F.r(sh, -0.10, 0, 0, P.GLASS[1], fill=PAPER, sw=0.2)
    F.l(sh, -0.05, 0, -0.05, P.GLASS[1], sw=0.12)
    for y in (1.85, 3.70, 5.55):
        F.r(sh, -0.12, y - 0.03, 0.02, y + 0.03, fill=INK, sw=0.1)
    F.r(sh, -0.30, P.GLASS[1], 0.0, P.VEST['y0'] - 0.12, **ex)
    F.r(sh, -0.30, P.VEST['y1'] + 0.12, 0, W + T, **ex)
    # the vestibule: steel and glass walls 120 thick, felt-lined; the outer door at x0, the inner door at x1
    V = P.VEST
    F.r(sh, 0, V['y0'] - 0.12, V['x1'] + 0.12, V['y0'], **nw)
    F.r(sh, 0, V['y1'], V['x1'] + 0.12, V['y1'] + 0.12, **nw)
    F.r(sh, V['x0'] - 0.06, V['y0'], V['x0'], P.OUTER_DOOR_Y, fill=PAPER, sw=0.2)
    F.r(sh, V['x0'] - 0.06, P.OUTER_DOOR_Y + P.DOOR_W, V['x0'], V['y1'], fill=PAPER, sw=0.2)
    F.r(sh, V['x1'], V['y0'], V['x1'] + 0.12, P.INNER_DOOR_Y, **nw)
    F.r(sh, V['x1'], P.INNER_DOOR_Y + P.DOOR_W, V['x1'] + 0.12, V['y1'], **nw)
    F.door(sh, (V['x0'] - 0.03, P.OUTER_DOOR_Y), (0, 1), (-1, 0), P.DOOR_W)
    F.door(sh, (V['x1'], P.INNER_DOOR_Y), (0, 1), (-1, 0), P.DOOR_W)
    # the coat closet between the vestibule and the left wall, open to the front room
    F.r(sh, V['x1'] + 0.12 - 0.12, V['y1'] + 0.12, V['x1'] + 0.12, W, **nw) if False else None
    # the listening room: its front partition (double stud, 300), the wall to the corridor, the lobby
    Pt = P.PARTITION
    F.r(sh, Pt['x0'], Pt['y0'], Pt['x1'], P.LISTEN_DOOR1_Y, **nw)
    F.r(sh, Pt['x0'], P.LISTEN_DOOR1_Y + P.DOOR_W, Pt['x1'], W, **nw)
    F.r(sh, Pt['x0'], P.CORRIDOR['y1'], L, P.LISTEN['y0'], **nw)
    Lb = P.LOBBY
    F.r(sh, Lb['x1'], Lb['y0'], Lb['x1'] + 0.12, P.LISTEN_DOOR2_Y, **nw)
    F.r(sh, Lb['x1'], P.LISTEN_DOOR2_Y + P.DOOR_W, Lb['x1'] + 0.12, Lb['y1'] + 0.12, **nw)
    F.r(sh, Lb['x0'], Lb['y1'], Lb['x1'] + 0.12, Lb['y1'] + 0.12, **nw)
    F.door(sh, (Pt['x0'], P.LISTEN_DOOR1_Y), (0, 1), (-1, 0), P.DOOR_W)
    F.door(sh, (Lb['x1'], P.LISTEN_DOOR2_Y), (0, 1), (-1, 0), P.DOOR_W)
    # back of house: the corridor wall with a door to each room, the rooms' walls, the wall to the bar room
    B = P.BOH
    F.r(sh, B['x0'] - 0.12, 0, B['x0'], P.CORRIDOR['y0'], **nw)
    xs = [r[0] for r in P.ROOMS] + [L]
    for i, (x0, x1, name) in enumerate(P.ROOMS):
        d0 = x0 + 0.25 if i else x0 + 0.20
        F.r(sh, x0 if i == 0 else x0 + 0.06, B['y1'], d0, P.CORRIDOR['y0'], **nw)
        F.r(sh, d0 + P.DOOR_W, B['y1'], x1 - 0.06 if x1 < L else L, P.CORRIDOR['y0'], **nw)
        F.door(sh, (d0, B['y1'] + 0.06), (1, 0), (0, -1), P.DOOR_W)
        if i:
            F.r(sh, x0 - 0.06, 0, x0 + 0.06, B['y1'], **nw)
    F.door(sh, (L, P.REAR_EXIT_Y), (0, 1), (1, 0), P.DOOR_W)          # the rear exit swings out


def plan_sheet():
    sh = Sheet()
    tx = sh.frame('A-101', 'Floor plan', "1/4\" = 1'-0\" · 2,800 sq ft · 55 seats",
                  SHEETS, notes=[('READ WITH', ['A-000 for the occupant load and the code', 'thresholds; A-102 for the lamps.'])])
    F = Frame(PLAN_O[0], PLAN_O[1], S4)
    # zone tints under everything
    F.r(sh, 0.9, 0, P.SHOP_WALL['x1'] + 0.2, 3.40, fill=TINT['shop'], stroke='none')
    F.r(sh, P.LISTEN['x0'], P.LISTEN['y0'], L, W, fill=TINT['listen'], stroke='none')
    F.r(sh, P.BOH['x0'], 0, L, P.LISTEN['y0'] - 0.3, fill=TINT['boh'], stroke='none')
    shell(sh, F)
    furniture(sh, F)
    route_and_exits(sh, F)
    plan_labels(sh, F)
    plan_dims(sh, F)
    # section marks: A along y = 6.80 looking toward the left wall; B at x = 11.40 looking toward the back
    a0, a1 = F(-1.6, 6.80), F(L + 1.3, 6.80)
    sh.line(a0[0] + 5, a0[1], a1[0] - 5, a1[1], sw=0.25, dash='6 2 1 2')
    sh.section_mark(a0[0], a0[1], 'A', 'A-201', (0, -1))
    sh.section_mark(a1[0], a1[1], 'A', 'A-201', (0, -1))
    b0, b1 = F(11.40, -1.5), F(11.40, W + 1.5)
    sh.line(b0[0], b0[1] - 5, b1[0], b1[1] + 5, sw=0.25, dash='6 2 1 2')
    sh.section_mark(b0[0], b0[1], 'B', 'A-201', (1, 0))
    sh.section_mark(b1[0], b1[1], 'B', 'A-201', (1, 0))
    sh.north(PLAN_O[0] + 140, 352, rot=0)
    sh.text(PLAN_O[0] + 150, 353, 'Plan north; no site yet', size=2.3, fill=GREY)
    sh.scale_bar(PLAN_O[0], 352, S4)
    legend(sh, PLAN_O[0], 380)
    plan_notes(sh, PLAN_O[0], 470)
    return sh


def furniture(sh, F):
    k = dict(sw=0.18)
    # --- the shop wall and the front room
    SW = P.SHOP_WALL
    F.r(sh, SW['x0'], 0, SW['x1'], SW['d'], fill='#f7f4ee', sw=0.25)
    for x0, x1, what in P.SHOP_BAYS:
        F.l(sh, x1, 0, x1, SW['d'], sw=0.18)
        F.l(sh, x0 + 0.05, SW['d'] - 0.12, x1 - 0.05, SW['d'] - 0.12, sw=0.1, dash='1 0.6')
    for x, y, what in P.SHOP_PLINTHS:
        if what == 'Tropos':
            F.r(sh, x - 0.40, y - 0.33, x + 0.40, y + 0.33, fill='#d8d4cc', sw=0.2)
            F.r(sh, x - P.TROPOS['w'] / 2, y - P.TROPOS['d'] / 2, x + P.TROPOS['w'] / 2, y + P.TROPOS['d'] / 2,
                fill=TINT['tropos'], sw=0.2)
        else:
            F.r(sh, x - 0.40, y - 0.30, x + 0.40, y + 0.30, fill='#d8d4cc', sw=0.2)
            F.c(sh, x, y, 0.16, fill='#cfc8bc', sw=0.15)                  # Mantle's platter
    T = P.SHOP_TABLE
    F.r(sh, T['x0'], T['y0'], T['x1'], T['y1'], fill='#ece6da', sw=0.25)
    for i in range(8):                                                   # the eight Cores on the table's end
        F.c(sh, T['x0'] + 0.25 + i * 0.13, T['y1'] - 0.18, 0.05, fill=['#c8452f', '#d27a3a', '#d9b43c', '#5d8a4a',
                                                                      '#6fa8c8', '#8b6fb0', '#e9e7e2', '#4a4a50'][i], sw=0.08)
    LC = P.LOUNGE_CHAIR
    for x, y in P.LOUNGE:
        F.c(sh, x, y, 0.33, fill='#e4ded2', sw=0.2)
        for s in (-1, 1):
            cy = y + s * LC['gap']
            F.r(sh, x - LC['w'] / 2, cy - 0.36, x + LC['w'] / 2, cy + 0.36, rx=1.6, fill='#d8cbb8', sw=0.2)
            F.l(sh, x - LC['w'] / 2 + 0.06, cy + s * 0.26, x + LC['w'] / 2 - 0.06, cy + s * 0.26, sw=0.4)
    H = P.HOST
    F.r(sh, H['x0'], H['y0'], H['x1'], H['y1'], fill='#d8d4cc', sw=0.2)
    F.c(sh, (H['x0'] + H['x1']) / 2, (H['y0'] + H['y1']) / 2, 0.13, sw=0.15)     # the coin bowl
    # the coat closet: a rail in the slot between the vestibule and the left wall
    F.l(sh, 0.4, (P.VEST['y1'] + 0.12 + W) / 2, 3.3, (P.VEST['y1'] + 0.12 + W) / 2, sw=0.25, dash='2 0.8')
    # --- the bar
    B, C = P.BACKBAR, P.COUNTER
    F.r(sh, B['x0'], B['y0'], B['x1'], B['y1'], fill='#e2ddd3', sw=0.25)
    for x0, x1, what in P.BAR_FIXTURES:
        F.l(sh, x1, B['y0'], x1, B['y1'], sw=0.12)
    F.r(sh, C['x0'], C['y0'], C['x1'], C['y_work'], rx=2.2, fill=TINT['oak'], sw=0.25)            # the fluted body
    F.r(sh, C['x0'] - 0.04, C['edge'], C['x1'] + 0.04, C['y_work'] + 0.03, rx=4.0, sw=0.2, dash='2.4 1')   # the top
    F.r(sh, P.LOW_END['x0'], C['y0'] + 0.05, P.LOW_END['x1'], C['y0'] + 0.20, fill=TINT['route'], stroke='none',
        opacity=0.35)
    F.l(sh, C['x0'] + 0.2, C['y0'] - 0.16, C['x1'] - 0.2, C['y0'] - 0.16, sw=0.45, stroke='#8a6a3a')     # the foot rail
    for x, kind in P.SINKS:
        w = 0.30 if kind == 'hand' else (0.90 if kind == '3-comp' else 0.40)
        F.r(sh, x - w / 2, C['y_work'] - 0.30, x + w / 2, C['y_work'] - 0.06, fill=PAPER, sw=0.15)
    for x in P.STOOLS:
        F.c(sh, x, P.STOOL_Y, 0.21, fill=TINT['leather'], sw=0.18)
        sh.path(arc_d(F, x, P.STOOL_Y, 0.21, 200, 340), sw=0.6)
    for x in P.LOW_SEATS:
        chair(sh, F, x, P.STOOL_Y + 0.05, 90)
    # the booth: the desk, its glass, the decks; the record wall behind
    Bo = P.BOOTH
    F.r(sh, Bo['desk'][0], Bo['y0'] + 0.08, Bo['desk'][1], C['y_work'], fill='#4a4844', sw=0.25)
    F.r(sh, Bo['x0'], Bo['y0'], Bo['x1'], Bo['y0'] + 0.08, fill=PAPER, sw=0.25)         # the low wall and its glass
    for dy in (0.45, 1.05):
        F.c(sh, Bo['desk'][0] + 0.30, Bo['y0'] + dy, 0.17, fill='#2b2a28', sw=0.12)
    F.r(sh, Bo['desk'][0] + 0.12, Bo['y0'] + 0.62, Bo['desk'][0] + 0.48, Bo['y0'] + 0.88, fill='#6a6862', sw=0.1)
    R = P.RECORD_WALL
    F.r(sh, R['x0'], R['y0'], R['x1'], R['y1'], fill='#d9cdb8', sw=0.25)
    n = int((R['y1'] - R['y0']) / R['cell'])
    for i in range(1, n):
        y = R['y0'] + i * (R['y1'] - R['y0']) / n
        F.l(sh, R['x0'], y, R['x1'], y, sw=0.1)
    F.l(sh, R['x0'] - 0.10, R['y0'] + 0.1, R['x0'] - 0.10, R['y1'] - 0.1, sw=0.2, dash='3 1')    # the ladder's rail
    # --- the banquette, its tables and chairs; the communal table
    Q = P.BANQ
    F.r(sh, Q['x0'], Q['y0'], Q['x1'], Q['y1'], rx=1.0, fill=TINT['mohair'], sw=0.25)
    F.r(sh, Q['x0'] + 0.03, Q['y0'] + 0.03, Q['x1'] - 0.03, Q['y0'] + 0.22, fill='#3f3329', sw=0.12)
    for i in range(1, 13):
        x = Q['x0'] + i * (Q['x1'] - Q['x0']) / 13
        F.l(sh, x, Q['y0'] + 0.22, x, Q['y1'], sw=0.08, stroke='#2a221b')
    BT = P.BANQ_TABLE
    for x in P.BANQ_TABLES:
        F.r(sh, x - BT['w'] / 2, BT['y0'], x + BT['w'] / 2, BT['y0'] + BT['d'], fill='#5a4636', sw=0.2)
        chair(sh, F, x, P.BANQ_CHAIR_Y, -90)
    Cm = P.COMMUNAL
    F.r(sh, Cm['x0'], Cm['y0'], Cm['x1'], Cm['y1'], rx=1.0, fill='#5a4636', sw=0.25)
    for x in P.COMMUNAL_CHAIRS:
        chair(sh, F, x, P.COMMUNAL_CHAIR_Y[0], 90)
        chair(sh, F, x, P.COMMUNAL_CHAIR_Y[1], -90)
    M = P.MOTHER
    F.c(sh, M['x'], M['y'], M['d'] / 2, sw=0.25, dash='2 1')
    F.l(sh, M['x'] - M['d'] / 2, M['y'], M['x'] + M['d'] / 2, M['y'], sw=0.1, dash='1 1')
    F.l(sh, M['x'], M['y'] - M['d'] / 2, M['x'], M['y'] + M['d'] / 2, sw=0.1, dash='1 1')
    # --- Core on every table (a small tinted dot)
    for x, y in P.CORE_ON:
        F.c(sh, x, y, 0.06, fill='#d9b43c', sw=0.1)
    # --- the listening room
    for x, y in P.STACKS:
        F.r(sh, x - 0.43, y - 0.36, x + 0.43, y + 0.36, fill='#2b2a28', sw=0.2)                  # the plinth
        ang = math.degrees(math.atan2(P.SWEET[1] - y, P.SWEET[0] - x))
        rot_rect(sh, F, x, y, P.TROPOS['d'], P.TROPOS['w'], ang, fill=TINT['tropos'], sw=0.2)
        F.l(sh, x, y, P.SWEET[0], P.SWEET[1], sw=0.15, dash='1.2 1.2', stroke=GREY)
    F.c(sh, P.SWEET[0], P.SWEET[1], 0.08, fill=INK, stroke='none')
    A = P.ALTAR
    F.r(sh, A['x0'], A['y0'], A['x1'], A['y1'], fill=sh.hatch('endgrain', 45, 0.9, 0.1, '#5a4636', '#d3c3a8'), sw=0.25)
    for x, y in P.TUBS:
        ang = math.degrees(math.atan2(P.SWEET[1] - y, (L - 1.0) - x))
        tub(sh, F, x, y, ang)
    for x, y in P.SIDE_TABLES:
        F.c(sh, x, y, 0.22, fill='#5a4636', sw=0.18)
    for x0, x1 in P.PANELS_L:
        F.r(sh, x0, W - 0.10, x1, W, fill=sh.hatch('absorb', -45, 0.8, 0.1, INK, '#cfc8c0'), sw=0.2)
        F.r(sh, x0 + 1.2, P.LISTEN['y0'], x1, P.LISTEN['y0'] + 0.10, fill=sh.hatch('absorb', -45, 0.8, 0.1), sw=0.2)
    for i in range(14):                                                   # the slotted diffuser round the altar
        y = P.LISTEN['y0'] + 0.35 + i * 0.40
        if A['y0'] - 0.1 < y < A['y1'] + 0.1:
            continue
        F.r(sh, L - 0.12, y, L, y + 0.22, fill='#b89c78', sw=0.1)
    # --- back of house
    for i, (x0, x1, name) in enumerate(P.ROOMS[:3]):
        cx = (x0 + x1) / 2
        F.ellipse = None
        x, y = F(x0 + 0.42, 0.33)
        sh.ellipse(x, y, 0.20 * S4, 0.30 * S4, fill=PAPER, sw=0.2)                 # the water closet
        F.r(sh, x0 + 0.24, 0.02, x0 + 0.60, 0.12, fill=PAPER, sw=0.2)               # its tank
        F.r(sh, x1 - 0.62, 0.0, x1 - 0.12, 0.45, rx=1.0, fill=PAPER, sw=0.2)        # the lavatory
        F.l(sh, x0 + 0.08, 0.30, x0 + 0.08, 1.37, sw=0.5)                           # grab bars
        F.l(sh, x0 + 0.15, 0.05, x0 + 1.05, 0.05, sw=0.5)
        F.c(sh, cx + 0.05, 1.45, 0.76, sw=0.12, dash='1.5 1', stroke=TINT['route'])  # the 60 in turning circle
    x0, x1, _ = P.ROOMS[3]
    F.r(sh, x0 + 0.10, 0.0, x1 - 0.05, 0.45, fill='#e2ddd3', sw=0.2)              # shelving
    F.r(sh, x0 + 0.10, 1.90, x0 + 1.30, 2.50, fill='#e2ddd3', sw=0.2)             # the desk
    F.r(sh, x1 - 0.70, 2.30, x1 - 0.05, 2.95, fill=PAPER, sw=0.2)                 # the mop sink
    F.r(sh, x1 - 0.15, 0.80, x1 - 0.02, 1.80, fill=INK, sw=0.1)                   # the panels


def arc_d(F, x, y, r, a0, a1):
    p = F(x + r * math.cos(math.radians(a0)), y + r * math.sin(math.radians(a0)))
    q = F(x + r * math.cos(math.radians(a1)), y + r * math.sin(math.radians(a1)))
    R = r * F.S
    return f'M{p[0]:.2f},{p[1]:.2f} A{R:.2f},{R:.2f} 0 0 0 {q[0]:.2f},{q[1]:.2f}'


def rot_rect(sh, F, x, y, a, b, deg, **k):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    pts = [(x + c * u - s * v, y + s * u + c * v) for u, v in ((-a / 2, -b / 2), (a / 2, -b / 2), (a / 2, b / 2), (-a / 2, b / 2))]
    F.p(sh, pts, **k)


def chair(sh, F, x, y, facing):
    """A chair seen from above, its back away from `facing` (degrees: the direction the sitter looks)."""
    rot_rect(sh, F, x, y, 0.46, 0.46, facing, fill='#cdbfa9', sw=0.18)
    t = math.radians(facing)
    bx, by = x - 0.20 * math.cos(t), y - 0.20 * math.sin(t)
    rot_rect(sh, F, bx, by, 0.07, 0.44, facing, fill='#6b5a48', sw=0.1)


def tub(sh, F, x, y, facing):
    """A low tub chair: a disc, its back a thick arc away from where it faces."""
    F.c(sh, x, y, P.TUB_R, fill='#7b3b2c', sw=0.2)
    F.c(sh, x, y, P.TUB_R * 0.62, fill='#93503c', sw=0.12)
    a0, a1 = facing + 125, facing + 235
    sh.path(arc_d(F, x, y, P.TUB_R * 0.84, a0, a1).replace(' 0 0 0 ', ' 0 0 1 '), sw=1.4, stroke='#4a2219')


def route_and_exits(sh, F):
    """The accessible route (blue: the street to every kind of seat and the WCs) and the two exit paths (green)."""
    ln = dict(close=False, sw=0.45, stroke=TINT['route'], dash='3 1.5', cap='round', join='round')
    F.p(sh, [(-0.6, 8.76), (4.6, 8.76), (4.6, 6.75), (15.3, 6.75), (15.3, 5.20), (17.3, 5.40), (18.3, 5.40)], **ln)
    F.p(sh, [(8.70, 6.75), (8.70, 7.35)], **ln)                          # the counter's low end
    F.p(sh, [(13.6, 6.75), (13.6, 4.65)], **ln)                          # the communal table's end
    F.p(sh, [(4.6, 6.75), (4.6, 3.75), (6.4, 3.75), (6.4, 2.85), (15.4, 2.85), (15.4, 3.70), (20.8, 3.70)], **ln)
    F.p(sh, [(4.6, 3.75), (2.9, 3.75), (2.9, 4.55)], **ln)               # the lounge and the shop
    ex = dict(close=False, sw=0.32, stroke=TINT['exit'], dash='0.8 1.2', cap='round', join='round')
    for path in ([(20.0, 5.45), (17.3, 5.65), (15.6, 5.65), (15.6, 3.55), (L + 0.6, 3.55)],
                 [(13.0, 6.55), (4.35, 6.55), (4.35, 8.55), (-0.9, 8.55)]):
        F.p(sh, path, **ex)
        (x0, y0), (x1, y1) = F(*path[-2]), F(*path[-1])
        a = math.atan2(y1 - y0, x1 - x0)
        sh.poly([(x1, y1), (x1 - 2.6 * math.cos(a - 0.4), y1 - 2.6 * math.sin(a - 0.4)),
                 (x1 - 2.6 * math.cos(a + 0.4), y1 - 2.6 * math.sin(a + 0.4))], fill=TINT['exit'], stroke='none')
    F.tag(sh, -1.0, 9.35, 'Exit 1', size=2.6, fill=TINT['exit'], spacing=0.4)
    F.tag(sh, L + 1.25, P.REAR_EXIT_Y - 0.55, 'Exit 2', size=2.6, fill=TINT['exit'], spacing=0.4)


def plan_labels(sh, F):
    def room(x, y, name, sub=()):
        F.tag(sh, x, y, name, size=3.0, weight=700, spacing=0.8)
        for i, s in enumerate(sub):
            F.t(sh, x, y - 0.0 - (i + 1) * 0.25, s, size=2.3, anchor='middle', fill='#55524c')
    room(4.10, 4.80, 'Shop and window lounge', ['the street at the glass'])
    room(11.40, 6.35, 'Bar room')
    room(21.0, 10.05, 'Listening room', ['11 seats · quiet at the line'])
    room(19.0, 3.86, 'Corridor', ["3'-10\" clear"])
    F.t(sh, 2.12, 8.95, 'Vestibule', size=2.4, anchor='middle', weight=600)
    F.t(sh, 2.12, 8.55, 'sound lock', size=2.2, anchor='middle', fill=GREY)
    F.t(sh, 1.6, 10.42, 'Coats', size=2.2, anchor='middle', fill=GREY)
    F.t(sh, -0.55, 6.1, 'Display glass', size=2.2, anchor='middle', rot=-90, fill=GREY)
    for x0, x1, what in P.SHOP_BAYS:
        F.t(sh, (x0 + x1) / 2, 0.23, what, size=2.3, anchor='middle', weight=600)
    F.t(sh, (P.SHOP_TABLE['x0'] + P.SHOP_TABLE['x1']) / 2, P.SHOP_TABLE['y0'] + 0.35, 'Shop table · till', size=2.3,
        anchor='middle')
    F.t(sh, 4.1, 6.62, 'Host · coin bowl', size=2.2, anchor='middle')
    F.t(sh, 11.05, 10.30, 'Back bar: ice · glasswasher · reach-ins · keg · bottles above', size=2.2, anchor='middle')
    F.t(sh, 11.05, 9.48, "Bartenders' aisle 3'-1\"", size=2.2, anchor='middle', fill='#55524c')
    F.t(sh, 11.60, 8.50, 'Counter: zinc on fluted oak, 3\'-6"', size=2.3, anchor='middle', fill=INK, weight=600)
    F.t(sh, 8.70, 8.20 - 0.68, 'Low end 2\'-10" (11B-902.3)', size=2.1, anchor='middle', fill=TINT['route'])
    F.t(sh, 14.70, 8.20, 'Booth', size=2.4, anchor='middle', weight=700, fill=PAPER, rot=-90)
    F.t(sh, 15.32, 9.55, 'Selector', size=2.1, anchor='middle', fill=GREY, rot=-90)
    F.t(sh, 15.82, 7.6, 'Record wall · ~9,000 LPs to 14\'', size=2.2, anchor='middle', rot=-90)
    F.t(sh, 11.40, 0.42, 'Banquette', size=2.3, anchor='middle', fill=PAPER, weight=600)
    F.t(sh, 11.40, 5.45 - 0.75, 'Communal table', size=2.2, anchor='middle', fill=PAPER)
    F.t(sh, P.MOTHER['x'] + 0.85, P.MOTHER['y'] + 0.62, 'Mother EARF over', size=2.1, anchor='start', fill=GREY)
    F.t(sh, 17.0, 5.75, 'Lobby', size=2.3, anchor='middle', weight=600)
    F.t(sh, P.SWEET[0] + 0.15, P.SWEET[1] - 0.95, 'the seat', size=2.1, anchor='start', fill=GREY)
    for x, y in P.STACKS:
        F.t(sh, x, y + (0.52 if y > 7 else -0.62), 'Tropos on a 16" plinth', size=2.1, anchor='middle')
    F.t(sh, P.ALTAR['x0'] - 0.1, 7.6, 'End-grain altar', size=2.1, anchor='middle', rot=-90)
    F.t(sh, 19.8, W - 0.38, 'Absorber in steel frames', size=2.1, anchor='middle')
    for x0, x1, name in P.ROOMS:
        if name.startswith('All'):
            F.t(sh, (x0 + x1) / 2 + 0.05, 2.35, name.replace('All-gender ', ''), size=2.4, anchor='middle', weight=600)
            F.t(sh, (x0 + x1) / 2 + 0.05, 2.05, 'all-gender, accessible', size=2.0, anchor='middle', fill=GREY)
        else:
            F.t(sh, (x0 + x1) / 2, 1.35, 'Stock · office', size=2.4, anchor='middle', weight=600)
            F.t(sh, (x0 + x1) / 2, 1.05, 'mop sink · panels', size=2.0, anchor='middle', fill=GREY)


def plan_dims(sh, F):
    T = P.WALL
    F.dim(sh, 0, W + T, L, W + T, 14)                                         # overall length, along the top
    F.dim(sh, 0, W + T, P.FRONT_X1, W + T, 7)
    F.dim(sh, P.FRONT_X1, W + T, P.PARTITION['x0'], W + T, 7)
    F.dim(sh, P.PARTITION['x0'], W + T, L, W + T, 7)
    F.dim(sh, L + T, 0, L + T, W, -16)                                         # overall width, on the right
    F.dim(sh, L + T, 0, L + T, P.BOH['y1'], -9)
    F.dim(sh, L + T, P.BOH['y1'], L + T, P.LISTEN['y0'], -9)
    F.dim(sh, L + T, P.LISTEN['y0'], L + T, W, -9)
    # clearances in the bar room
    F.dim(sh, 13.75, P.COMMUNAL_CHAIR_Y[1] + 0.30, 13.75, P.STOOL_Y - 0.25, -3.0)
    F.dim(sh, 14.85, P.BANQ_CHAIR_Y + 0.25, 14.85, P.COMMUNAL_CHAIR_Y[0] - 0.30, -3.0)
    F.dim(sh, P.VEST['x0'], P.VEST['y0'] + 0.25, P.VEST['x1'], P.VEST['y0'] + 0.25, 3.0)
    F.dim(sh, -0.30, -T - 0.0, 0.0, -T, 0) if False else None


def legend(sh, x, y):
    sh.text(x, y, 'LEGEND', size=2.4, weight=700, spacing=0.6)
    rows = [('poche', EXISTING, 'Existing walls (assumed)'), ('poche', NEW, 'New partitions; the listening room double stud'),
            ('line', TINT['route'], 'Accessible route (36 in min; 44 in on the main aisle)'),
            ('line', TINT['exit'], 'Exit path; two exits, panic hardware'),
            ('dot', '#d9b43c', 'Core on the table'), ('fill', TINT['tropos'], 'Tropos'),
            ('dash', INK, 'Above: the counter top, Mother EARF')]
    for i, (kind, c, s) in enumerate(rows):
        yy = y + 6 + i * 5.2
        if kind in ('poche', 'fill'):
            sh.rect(x, yy - 2.4, x + 7, yy + 0.6, fill=c, sw=0.2)
        elif kind == 'line':
            sh.line(x, yy - 0.9, x + 7, yy - 0.9, sw=0.5, stroke=c, dash='3 1.5')
        elif kind == 'dot':
            sh.circle(x + 3.5, yy - 0.9, 1.2, fill=c, sw=0.1)
        else:
            sh.line(x, yy - 0.9, x + 7, yy - 0.9, sw=0.25, dash='2 1')
        sh.text(x + 10, yy, s, size=2.5)
    # the seat count
    xs = x + 150
    sh.text(xs, y, 'SEATS', size=2.4, weight=700, spacing=0.6)
    yy = y + 6
    for k, v in P.seats().items():
        sh.text(xs, yy, k, size=2.5); sh.text(xs + 82, yy, str(v), size=2.5, anchor='end', weight=600); yy += 5.2
    sh.line(xs, yy - 3.4, xs + 82, yy - 3.4, sw=0.2)
    sh.text(xs, yy + 0.6, 'Seats in all', size=2.5, weight=700)
    sh.text(xs + 82, yy + 0.6, str(sum(P.seats().values())), size=2.5, weight=700, anchor='end')
    # the occupant load, short (A-000 has it in full)
    xo = xs + 105
    rows, total = P.occupant_load()
    sh.text(xo, y, 'OCCUPANT LOAD (CBC TABLE 1004.5)', size=2.4, weight=700, spacing=0.6)
    yy = y + 6
    for k, sf, f, how, n in rows:
        sh.text(xo, yy, k, size=2.4)
        sh.text(xo + 118, yy, f'{sf:,} sf', size=2.4, anchor='end', fill=GREY)
        sh.text(xo + 142, yy, ('/ ' + str(f) + ' ' + how) if f else 'by seat', size=2.4, anchor='end', fill=GREY)
        sh.text(xo + 156, yy, str(n), size=2.4, anchor='end', weight=600)
        yy += 4.8
    sh.line(xo, yy - 3.2, xo + 156, yy - 3.2, sw=0.2)
    sh.text(xo, yy + 0.8, 'Occupant load: Group A-2, sprinklered (100 and over)', size=2.5, weight=700)
    sh.text(xo + 156, yy + 0.8, str(total), size=2.5, weight=700, anchor='end')



PLAN_NOTES = [
    'The shell is assumed: an existing concrete or masonry ground floor, sprinklered or able to be. A site visit decides it.',
    'Two exits for an occupant load over 49 (CBC 1006.2): the street door through the vestibule and the rear door to the yard and side passage, more than a third of the diagonal apart (sprinklered). Both swing outward with panic hardware (CBC 1010.2.9).',
    'The vestibule is a sound lock: two doors in series 8 ft apart, felt-lined, so the line stays inside when guests come and go (Police Code Art. 29).',
    'The listening room is a room within the room: double-stud walls on isolated clips, its own ceiling at 12 ft, a lobby with two doors. Its stacks face the front, away from the party walls.',
    'Accessible: one level throughout, 36 in routes, 44 in on the main aisle; the counter drops to 34 in for its first 5 ft 3 in (CBC 11B-902.3); 5% of table seats at 30 in (11B-226); three single-user all-gender WCs, each with a 60 in turning circle.',
    'Behind the bar: a hand sink at each end, a three-compartment sink and a dump sink in the underbar; ice, a glasswasher, reach-ins and a keg box under the back bar (DPH plan check).',
    'Everything on the floor is on sale: each piece carries a card. The shop wall holds stock and the pieces not in use.',
]


def plan_notes(sh, x, y):
    sh.text(x, y, 'PLAN NOTES', size=2.4, weight=700, spacing=0.6)
    yy = y + 6
    for i, n in enumerate(PLAN_NOTES):
        import textwrap
        rows = textwrap.wrap(n, 150)
        sh.text(x, yy, f'{i + 1}', size=2.5, weight=700)
        yy = sh.lines_of(x + 5, yy, rows, size=2.5, lead=1.4) + 1.6


# --- A-102: the reflected ceiling plan -------------------------------------------------------------------------------
HEMI = '#2b2a28'
RCP_LEGEND = [('hemi', 'Hemisphere, pendant: 575 lm, 2700 K, dimmed; rim 26 in over the counter'),
              ('mother', 'Mother EARF: the 1 m globe in multicolour, hung from the joists, its own spot'),
              ('spot', 'Adjustable spot, 2700 K, 15 to 25 degrees, on a ceiling track or the beams'),
              ('linear', 'Linear LED in the shelves: the back bar, the shop wall, the record wall'),
              ('core', 'Core, on the tables (for reference: not on the ceiling)'),
              ('exit', 'Exit sign, with the emergency lights on its circuit'),
              ('spk', 'Sprinkler head, pendent: schematic, by the fire protection contractor'),
              ('cloud', 'Acoustic cloud, 2 in mineral wool in fabric, hung 12 in under the listening ceiling')]


def rcp_symbol(sh, F, kind, x, y):
    if kind == 'hemi':
        F.c(sh, x, y, 0.21, fill=HEMI, sw=0.2); F.c(sh, x, y, 0.09, fill='#e7a24a', sw=0.1)
    elif kind == 'mother':
        F.c(sh, x, y, 0.50, fill='none', sw=0.35)
        for a in range(0, 180, 30):
            t = math.radians(a)
            F.l(sh, x - 0.5 * math.cos(t), y - 0.5 * math.sin(t), x + 0.5 * math.cos(t), y + 0.5 * math.sin(t), sw=0.12)
    elif kind == 'spot':
        F.c(sh, x, y, 0.09, fill=PAPER, sw=0.25); F.c(sh, x, y, 0.035, fill=INK, stroke='none')
    elif kind == 'core':
        F.c(sh, x, y, 0.07, fill='#d9b43c', sw=0.1, opacity=0.55)
    elif kind == 'exit':
        X, Y = F(x, y)
        sh.rect(X - 3.2, Y - 1.6, X + 3.2, Y + 1.6, fill=PAPER, stroke=TINT['exit'], sw=0.3)
        sh.text(X, Y + 0.9, 'EXIT', size=2.0, weight=700, anchor='middle', fill=TINT['exit'])
    elif kind == 'spk':
        F.c(sh, x, y, 0.05, fill=PAPER, stroke='#c0392b', sw=0.18)
    elif kind == 'linear':
        F.l(sh, x - 0.4, y, x + 0.4, y, sw=0.8, stroke='#e7a24a')
    elif kind == 'cloud':
        F.r(sh, x - 0.6, y - 0.3, x + 0.6, y + 0.3, fill=sh.dots('wool', 1.0, 0.14, '#7a746a', '#ece7df'), sw=0.2)


def rcp_sheet():
    sh = Sheet()
    sh.frame('A-102', 'Reflected ceiling plan', "1/4\" = 1'-0\" · lamps and ceilings", SHEETS,
             notes=[('LIGHT', ['Warm and low: 2700 K everywhere, 2200 K', 'on the dimmed Hemispheres late. No',
                               'light source visible from a seat. Five', 'dimming zones on one scene controller', '(the colour clock).']),
                    ('CEILINGS', ['Bar and shop: open to the joists, the', 'fir beams exposed, spray acoustic', 'cellulose on the deck between them,',
                                  'black (NRC 0.75 to 0.95 at 1 in).', 'Listening room: isolated gypsum on', 'clips at 12 ft, clouds under it.',
                                  'Back of house: gypsum at 9 ft.'])])
    F = Frame(PLAN_O[0], PLAN_O[1], S4)
    # ceiling zones
    F.r(sh, 0, 0, P.PARTITION['x0'], W, fill=sh.dots('cellulose', 1.6, 0.12, '#9a958c', '#f4f2ee'), stroke='none')
    F.r(sh, P.LISTEN['x0'], P.LISTEN['y0'], L, W, fill='#f7f5f1', stroke='none')
    F.r(sh, P.BOH['x0'], 0, L, P.LISTEN['y0'] - 0.3, fill=sh.hatch('gyp', 0, 2.4, 0.08, '#b6b1a8', '#fbfaf8'), stroke='none')
    shell(sh, F, light=True)
    # the beams across the room (in the listening room and back of house they are above the ceilings: dashed)
    for x in P.BEAMS:
        if x < P.PARTITION['x0']:
            F.r(sh, x - P.BEAM_W / 2, 0, x + P.BEAM_W / 2, W, fill='#b89c78', sw=0.25)
        else:
            F.r(sh, x - P.BEAM_W / 2, 0, x + P.BEAM_W / 2, W, fill='none', sw=0.18, dash='2 1')
    F.r(sh, P.VEST['x0'], P.VEST['y0'], P.VEST['x1'], P.VEST['y1'], fill='#f7f5f1', sw=0.15)
    # the counter and the record wall as a ghost, so the lamps can be read against them
    C = P.COUNTER
    F.r(sh, C['x0'], C['edge'], C['x1'], C['y_work'], rx=4.0, sw=0.15, dash='1.5 1', stroke=GREY)
    F.r(sh, P.COMMUNAL['x0'], P.COMMUNAL['y0'], P.COMMUNAL['x1'], P.COMMUNAL['y1'], sw=0.15, dash='1.5 1', stroke=GREY)
    for x in P.BANQ_TABLES:
        F.r(sh, x - 0.375, 1.12, x + 0.375, 1.72, sw=0.12, dash='1.5 1', stroke=GREY)
    for x, y in P.STACKS:
        F.r(sh, x - 0.43, y - 0.36, x + 0.43, y + 0.36, sw=0.15, dash='1.5 1', stroke=GREY)
    # clouds in the listening room
    for x in (17.6, 19.4, 21.2):
        for y in (5.9, 7.6, 9.3):
            rcp_symbol(sh, F, 'cloud', x, y)
    # lamps
    for x in P.HEMI_COUNTER:
        rcp_symbol(sh, F, 'hemi', x, P.HEMI_COUNTER_Y)
    for x, y in P.HEMI_SHOP + P.HEMI_LOUNGE:
        rcp_symbol(sh, F, 'hemi', x, y)
    rcp_symbol(sh, F, 'mother', P.MOTHER['x'], P.MOTHER['y'])
    for x, y in P.SPOTS:
        rcp_symbol(sh, F, 'spot', x, y)
    for x, y in P.CORE_ON:
        rcp_symbol(sh, F, 'core', x, y)
    for x0 in range(8, 14):
        rcp_symbol(sh, F, 'linear', x0 + 0.5, W - 0.25)
    for x in (1.2, 2.4, 3.6, 4.8, 6.0):
        rcp_symbol(sh, F, 'linear', x + 0.45, 0.25)
    for y in (6.4, 7.4, 8.4, 9.4, 10.2):
        F.l(sh, 15.58, y - 0.4, 15.58, y + 0.4, sw=0.8, stroke='#e7a24a')
    for x, y in ((3.0, 8.75), (L - 0.55, 3.71), (15.2, 3.71), (16.55, 5.21), (5.0, 6.6)):
        rcp_symbol(sh, F, 'exit', x, y)
    # sprinklers: a schematic grid, at most 15 ft apart and 130 sq ft each (NFPA 13 light hazard)
    g = P.SPRINKLER_GRID
    for i in range(int(L / g) + 1):
        for j in range(4):
            x, y = g / 2 + i * g, 1.33 + j * 2.67
            if x < L:
                rcp_symbol(sh, F, 'spk', x + 0.5, y)
    # labels and zones
    def zl(x, y, s, sub):
        F.tag(sh, x, y, s, size=2.8, weight=700, spacing=0.6)
        F.t(sh, x, y - 0.32, sub, size=2.2, anchor='middle', fill='#55524c')
    zl(4.4, 5.2, 'Shop and lounge', "open to the joists 15'-9\"  ·  zone C")
    zl(11.4, 6.6, 'Bar room', "open to the joists 15'-9\", beams 14'-9\"  ·  zones A, B, E")
    zl(20.2, 10.2, 'Listening room', "isolated ceiling 12'-0\"  ·  zone D")
    zl(20.0, 3.95, 'Back of house', "gypsum 9'-0\"")
    F.t(sh, P.MOTHER['x'] + 0.65, P.MOTHER['y'] - 0.95, 'Mother EARF, 3 ft 3 in, centre 8 ft 4 in up', size=2.2)
    F.t(sh, 11.2, P.HEMI_COUNTER_Y + 0.42, 'Six Hemispheres, rims 5 ft 8 in up (26 in over the zinc)', size=2.2, anchor='middle')
    F.t(sh, 3.3, 1.75, 'Three Hemispheres hung low, for sale', size=2.2, anchor='middle')
    F.t(sh, 22.0, 4.85, 'Pin spots on the stacks and the altar', size=2.2, anchor='middle')
    F.dim(sh, 0, W + P.WALL, L, W + P.WALL, 10)
    for x0, x1 in zip([0] + P.BEAMS[:-1], P.BEAMS):
        F.dim(sh, x0, W + P.WALL, x1, W + P.WALL, 4.5)
    sh.scale_bar(PLAN_O[0], 352, S4)
    # legend and the lamp schedule
    x, y = PLAN_O[0], 380
    sh.text(x, y, 'LEGEND', size=2.4, weight=700, spacing=0.6)
    for i, (k, t) in enumerate(RCP_LEGEND):
        yy = y + 7 + i * 6
        rcp_symbol(sh, Frame(x + 4, yy - 1.0, S4 if k not in ('mother', 'cloud') else 5.0), k, 0, 0)
        sh.text(x + 12, yy, t, size=2.5)
    xs = x + 175
    sh.text(xs, y, 'LAMP SCHEDULE', size=2.4, weight=700, spacing=0.6)
    rows = [('Hemisphere', 'counter, shop, lounge', len(P.HEMI_COUNTER) + len(P.HEMI_SHOP) + len(P.HEMI_LOUNGE), 'A, C'),
            ('Mother EARF', 'over the communal table', 1, 'E'),
            ('Spots', 'tables, stacks, altar, shop', len(P.SPOTS), 'B, C, D'),
            ('Core', 'every table, the shop', len(P.CORE_ON), 'on the table'),
            ('Linear LED', 'shelves (ft)', 60, 'A, C'),
            ('Exit signs', 'battery-backed', 5, 'life safety')]
    yy = y + 7
    for r in rows:
        sh.text(xs, yy, r[0], size=2.5, weight=600); sh.text(xs + 26, yy, r[1], size=2.5)
        sh.text(xs + 82, yy, str(r[2]), size=2.5, anchor='end', weight=600); sh.text(xs + 88, yy, r[3], size=2.5, fill=GREY)
        yy += 5.6
    sh.text(xs, yy + 3, 'Zones: A counter · B tables · C shop and lounge · D listening · E Mother EARF', size=2.4, fill=GREY)
    sh.text(xs, yy + 8, 'Load: about 0.5 W per sq ft in the public rooms (Title 24 allows about 1.0 for a bar).', size=2.4, fill=GREY)
    return sh


# --- A-201: sections -------------------------------------------------------------------------------------------------
def slab_and_deck(sh, F, a0, a1, cut_walls):
    F.r(sh, a0, -0.25, a1, 0, fill=sh.hatch('conc', 45, 1.4, 0.12, INK, '#d9d6cf'), sw=0.25)
    F.r(sh, a0, P.JOISTS, a1, P.JOISTS + 0.30, fill=sh.hatch('deck', -45, 1.4, 0.12, INK, '#e4ded2'), sw=0.25)
    for a, b in cut_walls:
        F.r(sh, a, -0.25, b, P.JOISTS + 0.30, fill=EXISTING, sw=0.25)


def section_a():
    """Section A: along the room at y = 6.80, looking toward the left wall (+y): x to the right, z up."""
    sh_items = []
    return sh_items


def sections_sheet():
    sh = Sheet()
    sh.frame('A-201', 'Sections', "A at 1/4\", B at 3/8\" = 1'-0\"", SHEETS,
             notes=[('HEIGHTS', ["Floor 0'-0\" · counter 3'-6\" · low end", "2'-10\" · Hemisphere rims 5'-8\" ·",
                                 "Mother EARF 8'-4\" · listening ceiling", "12'-0\" · beams 14'-9\" · joists 15'-9\""]),
                    ('SOUND', ['The stacks fire toward the front, on', 'mass-loaded plinths on the slab; the',
                               'listening room floats on its own walls', 'and ceiling, 2 layers of gypsum each',
                               'side, insulation between (STC 60+).'])])
    # --- section A
    F = Frame(PLAN_O[0], 160.0, S4)
    y = 6.80
    T = P.WALL
    slab_and_deck(sh, F, -0.30, L + T, [(L, L + T)])
    # the shopfront in section: bulkhead, glass, transom, fascia
    F.r(sh, -0.30, 0, 0, 0.45, fill=EXISTING, sw=0.2)
    F.r(sh, -0.10, 0.45, 0, 3.35, fill='#dfe8ea', sw=0.25)
    F.r(sh, -0.10, 3.35, 0, 4.20, fill='#dfe8ea', sw=0.25)
    F.l(sh, -0.10, 3.35, 0, 3.35, sw=0.6)
    F.r(sh, -0.30, 4.20, 0, P.JOISTS + 0.30, fill=EXISTING, sw=0.2)
    # beyond the cut (y > 6.8): the vestibule's side, the coat wall, the host stand
    F.r(sh, 0, 0, P.VEST['x1'] + 0.12, 2.75, fill='#ebe7e0', sw=0.2)
    F.l(sh, P.VEST['x0'], 0, P.VEST['x0'], 2.75, sw=0.15)
    F.t(sh, (P.VEST['x0'] + P.VEST['x1']) / 2, 1.4, 'Vestibule (beyond)', size=2.2, anchor='middle', fill=GREY)
    F.r(sh, P.HOST['x0'], 0, P.HOST['x1'], 1.07, fill='#d8d4cc', sw=0.2)
    # lounge chair cut near y 7.07
    F.r(sh, 1.36, 0, 2.14, 0.42, fill='#d8cbb8', sw=0.2); F.r(sh, 1.36, 0.42, 2.14, 0.78, fill='#d8cbb8', sw=0.2)
    # the back bar elevation on the left wall: base, shelves of bottles to 2.6, the concrete above
    B = P.BACKBAR
    F.r(sh, B['x0'], 0, B['x1'], B['h'], fill='#3a3836', sw=0.25)
    for z in (1.35, 1.75, 2.15, 2.55):
        F.r(sh, B['x0'], z, B['x1'], z + 0.03, fill='#f2d9a8', sw=0.15)
        n = int((B['x1'] - B['x0']) / 0.11)
        for i in range(n):
            if (i * 7) % 11 < 8:
                bx = B['x0'] + 0.06 + i * 0.11; h = 0.26 + 0.06 * ((i * 5) % 3)
                F.r(sh, bx - 0.035, z + 0.03, bx + 0.035, z + 0.03 + h, fill='#7a5a3a' if i % 3 else '#4b6a52', sw=0.08)
    # the counter in elevation: the fluted front, the zinc top, the low end, the foot rail; the stools in front
    C = P.COUNTER
    F.r(sh, P.LOW_END['x1'], 0.10, C['x1'], C['top_z'] - 0.06, fill=TINT['oak'], sw=0.25)
    F.r(sh, C['x0'], 0.10, P.LOW_END['x1'], P.LOW_END['top_z'] - 0.05, fill=TINT['oak'], sw=0.25)
    for xx in [C['x0'] + 0.06 + 0.06 * i for i in range(int((C['x1'] - C['x0']) / 0.06))]:
        top = P.LOW_END['top_z'] - 0.05 if xx < P.LOW_END['x1'] else C['top_z'] - 0.06
        F.l(sh, xx, 0.12, xx, top - 0.02, sw=0.08, stroke='#7d6548')
    F.r(sh, C['x0'], 0, C['x1'], 0.10, fill='#2b2a28', sw=0.15)
    F.r(sh, P.LOW_END['x1'], C['top_z'] - 0.06, C['x1'] + 0.04, C['top_z'], fill=TINT['zinc'], sw=0.25)
    F.r(sh, C['x0'] - 0.04, P.LOW_END['top_z'] - 0.05, P.LOW_END['x1'], P.LOW_END['top_z'], fill=TINT['zinc'], sw=0.25)
    F.l(sh, P.LOW_END['x1'] + 0.1, 0.22, C['x1'] - 0.1, 0.22, sw=0.6, stroke='#8a6a3a')
    for x in P.STOOLS:
        F.r(sh, x - 0.21, 0.70, x + 0.21, 0.78, fill=TINT['leather'], sw=0.15)
        F.r(sh, x - 0.18, 0.78, x + 0.18, 0.98, fill=TINT['leather'], sw=0.15)
        for d in (-0.15, 0.15):
            F.l(sh, x + d * 0.6, 0.70, x + d, 0.0, sw=0.35, stroke='#2b2a28')
        F.l(sh, x - 0.14, 0.30, x + 0.14, 0.30, sw=0.3, stroke='#8a6a3a')
    for x in P.LOW_SEATS:
        F.r(sh, x - 0.22, 0.42, x + 0.22, 0.47, fill='#cdbfa9', sw=0.15)
        F.l(sh, x - 0.2, 0.42, x - 0.2, 0, sw=0.3); F.l(sh, x + 0.2, 0.42, x + 0.2, 0, sw=0.3)
    # Hemisphere over the counter: cords from the joists, the shade, the rim at top_z + 0.66
    for x in P.HEMI_COUNTER:
        rim = C['top_z'] + 0.66
        F.l(sh, x, P.JOISTS, x, rim + 0.17, sw=0.12)
        X, Y = F(x, rim)
        r = 0.21 * S4
        sh.path(f'M{X - r:.2f},{Y:.2f} A{r:.2f},{r * 0.75:.2f} 0 0 1 {X + r:.2f},{Y:.2f} Z', fill=HEMI, sw=0.2)
        sh.ellipse(X, Y + 0.6, r * 0.5, 0.6, fill='#e7a24a', stroke='none', opacity=0.8)
    # the booth: desk, glass, the selector's lamp; the record wall cut (the partition and the cubbies)
    Bo = P.BOOTH
    F.r(sh, Bo['x0'], 0, Bo['desk'][1], Bo['h'], fill='#4a4844', sw=0.25)
    F.r(sh, Bo['x0'], Bo['h'], Bo['x0'] + 0.02, 1.55, fill='#dfe8ea', sw=0.2)
    R = P.RECORD_WALL
    F.r(sh, R['x0'], 0, R['x1'], R['z1'], fill='#d9cdb8', sw=0.25)
    for k in range(1, int(R['z1'] / R['cell'])):
        z = k * R['cell']
        F.l(sh, R['x0'], z, R['x1'], z, sw=0.12)
        F.r(sh, R['x0'] + 0.03, z - R['cell'] + 0.03, R['x1'] - 0.06, z - 0.03, fill=sh.hatch('lp', 90, 0.5, 0.08, '#3a3532', '#cdbb9d'), stroke='none')
    F.r(sh, P.PARTITION['x0'], 0, P.PARTITION['x1'], P.JOISTS, fill=sh.hatch('stud', 45, 1.0, 0.1, INK, '#cfcac2'), sw=0.25)
    # the listening room: its own ceiling and clouds; the stack beyond (y 9.40), the altar cut, the tubs cut
    LC = P.LISTEN_CEIL
    F.r(sh, P.PARTITION['x1'], LC, L, LC + 0.12, fill=sh.hatch('stud', 45, 1.0, 0.1, INK, '#cfcac2'), sw=0.25)
    for x in (17.6, 19.4, 21.2):
        F.r(sh, x - 0.6, LC - 0.35, x + 0.6, LC - 0.30, fill='#9a948a', sw=0.15)
        F.l(sh, x - 0.5, LC - 0.30, x - 0.5, LC, sw=0.1); F.l(sh, x + 0.5, LC - 0.30, x + 0.5, LC, sw=0.1)
    for x, yy in P.STACKS[1:]:
        F.r(sh, x - 0.43, 0, x + 0.43, P.TROPOS['plinth'], fill='#2b2a28', sw=0.25)
        F.r(sh, x - 0.28, P.TROPOS['plinth'], x + 0.28, P.TROPOS['plinth'] + P.TROPOS['h'], fill=TINT['tropos'], sw=0.25)
        # the horn mouth near seated ear height
        X, Y = F(x, P.TROPOS['plinth'] + P.TROPOS['h'] - 0.30)
        sh.circle(X, Y, 0.17 * S4, fill='#5a5a62', sw=0.2)
        F.t(sh, x, P.TROPOS['plinth'] + P.TROPOS['h'] + 0.18, 'Tropos (beyond)', size=2.2, anchor='middle')
    A = P.ALTAR
    F.r(sh, A['x0'], 0, A['x1'], A['z1'], fill=sh.hatch('endgrain', 45, 0.9, 0.1, '#5a4636', '#d3c3a8'), sw=0.25)
    for x in (17.75, 19.05, 20.30):
        F.r(sh, x - 0.40, 0, x + 0.40, 0.38, fill='#7b3b2c', sw=0.2)
        F.r(sh, x - 0.40, 0.38, x - 0.26, 0.66, fill='#7b3b2c', sw=0.2)
    F.l(sh, 17.0, 1.10, P.SWEET[0], 1.10, sw=0.12, dash='1 1', stroke=GREY)
    F.t(sh, 17.05, 1.18, 'seated ear 3\'-7"', size=2.1, fill=GREY)
    # the beams cut (they run across the room)
    for x in P.BEAMS:
        top = P.JOISTS if x < P.PARTITION['x0'] else P.JOISTS
        F.r(sh, x - P.BEAM_W / 2, P.BEAM_Z, x + P.BEAM_W / 2, top, fill=sh.hatch('fir', 0, 0.7, 0.1, '#5a4636', '#c9a77c'), sw=0.25)
    # back of house is beyond the listening room's wall: not seen. Heights and labels
    for z, s in ((0, "0'-0\""), (C['top_z'], "3'-6\""), (P.LISTEN_CEIL, "12'-0\""), (P.BEAM_Z, "14'-9\""), (P.JOISTS, "15'-9\"")):
        X, Y = F(L + T, z)
        sh.line(X + 2, Y, X + 14, Y, sw=0.15)
        sh.poly([(X + 14, Y), (X + 12.4, Y - 1.4), (X + 15.6, Y - 1.4)], fill=INK, sw=0.1)
        sh.text(X + 17, Y + 0.9, s, size=2.5)
    for x, s in ((3.7, 'Shop and lounge'), (11.0, 'Bar room'), (15.0, 'Booth'), (20.2, 'Listening room')):
        F.tag(sh, x, -0.75, s, size=2.6, weight=700, spacing=0.5)
    sh.text(PLAN_O[0], 40, 'A  ·  SECTION ALONG THE HOUSE, LOOKING AT THE LEFT WALL', size=3.2, weight=700, spacing=0.6)
    sh.text(PLAN_O[0], 45.5, "1/4\" = 1'-0\"  ·  cut at 22'-4\" from the right wall (A-101)", size=2.5, fill=GREY)
    F.dim(sh, 0, -0.25, L, -0.25, -14)

    # --- section B: across the bar room at x = 11.40, looking toward the back; u = W - y from the left wall
    G = Frame(PLAN_O[0], 465.0, S38)
    u = lambda yy: W - yy
    slab_and_deck(sh, G, -T, W + T, [(-T, 0), (W, W + T)])
    # beyond: the beam at 14.63 seen, the record wall and booth, the partition, the corridor opening, WC 1's wall
    G.r(sh, 0, P.BEAM_Z, W, P.JOISTS, fill='#c9a77c', sw=0.2)
    G.r(sh, u(W), 0, u(P.RECORD_WALL['y0']), P.RECORD_WALL['z1'], fill='#d9cdb8', sw=0.2)
    for k in range(1, int(P.RECORD_WALL['z1'] / P.RECORD_WALL['cell'])):
        z = k * P.RECORD_WALL['cell']
        G.l(sh, 0, z, u(P.RECORD_WALL['y0']), z, sw=0.1)
    for k in range(1, int((W - P.RECORD_WALL['y0']) / 0.33)):
        G.l(sh, k * 0.33, 0, k * 0.33, P.RECORD_WALL['z1'], sw=0.1)
    G.r(sh, u(P.RECORD_WALL['y0']), 0, u(P.PARTITION['y0']), P.JOISTS, fill='#cfcac2', sw=0.2)
    G.r(sh, u(P.LISTEN_DOOR1_Y + P.DOOR_W), 0, u(P.LISTEN_DOOR1_Y), 2.13, fill='#4a3a2e', sw=0.25)
    G.r(sh, u(P.CORRIDOR['y1']), 0, u(P.CORRIDOR['y0']), 2.74, fill='#3c3b39', sw=0.2)
    G.t(sh, u((P.CORRIDOR['y0'] + P.CORRIDOR['y1']) / 2), 1.4, 'to the WCs', size=2.2, anchor='middle', fill=PAPER)
    G.r(sh, u(P.CORRIDOR['y0']), 0, u(0), P.JOISTS, fill='#e6e2db', sw=0.2)
    # the booth beyond, its glass and desk
    G.r(sh, u(W), 0, u(P.BOOTH['y0']), P.BOOTH['h'], fill='#4a4844', sw=0.2)
    G.r(sh, u(W - 0.05), P.BOOTH['h'], u(P.BOOTH['y0']), 1.55, fill='#dfe8ea', sw=0.15, opacity=0.8)
    # cut: the back bar, the aisle, the counter, the stools; the communal table and Mother EARF; the banquette
    B = P.BACKBAR
    G.r(sh, u(W), 0, u(B['y0']), B['h'], fill='#3a3836', sw=0.3)
    for z in (1.35, 1.75, 2.15, 2.55):
        G.r(sh, u(W), z, u(B['y0']) - 0.05, z + 0.03, fill='#f2d9a8', sw=0.15)
        for k in range(3):
            G.r(sh, u(W) + 0.10 + k * 0.16, z + 0.03, u(W) + 0.17 + k * 0.16, z + 0.33, fill='#7a5a3a', sw=0.1)
    G.r(sh, u(C['y_work']), 0.10, u(C['y0']), C['top_z'] - 0.06, fill=TINT['oak'], sw=0.3)
    G.r(sh, u(C['y_work']) - 0.03, C['top_z'] - 0.06, u(C['edge']), C['top_z'], fill=TINT['zinc'], sw=0.3)
    G.r(sh, u(C['y_work']) + 0.06, 0.85, u(C['y_work']) + 0.40, 0.95, fill=PAPER, sw=0.2)        # the underbar
    G.r(sh, u(C['y_work']), 0, u(C['y0']), 0.10, fill='#2b2a28', sw=0.2)
    sx = u(P.STOOL_Y)
    G.r(sh, sx - 0.21, 0.70, sx + 0.21, 0.78, fill=TINT['leather'], sw=0.2)
    G.r(sh, sx + 0.12, 0.78, sx + 0.21, 0.98, fill=TINT['leather'], sw=0.2)
    G.l(sh, sx - 0.12, 0.70, sx - 0.17, 0, sw=0.4); G.l(sh, sx + 0.12, 0.70, sx + 0.17, 0, sw=0.4)
    rim = C['top_z'] + 0.66
    hx = u(P.HEMI_COUNTER_Y)
    G.l(sh, hx, P.JOISTS, hx, rim + 0.17, sw=0.12)
    X, Y = G(hx, rim); r = 0.21 * S38
    sh.path(f'M{X - r:.2f},{Y:.2f} A{r:.2f},{r * 0.75:.2f} 0 0 1 {X + r:.2f},{Y:.2f} Z', fill=HEMI, sw=0.2)
    sh.ellipse(X, Y + 0.8, r * 0.5, 0.8, fill='#e7a24a', stroke='none', opacity=0.8)
    Cm = P.COMMUNAL
    G.r(sh, u(Cm['y1']), Cm['h'] - 0.04, u(Cm['y0']), Cm['h'], fill='#5a4636', sw=0.3)
    G.r(sh, u((Cm['y0'] + Cm['y1']) / 2) - 0.05, 0, u((Cm['y0'] + Cm['y1']) / 2) + 0.05, Cm['h'] - 0.04, fill='#2b2a28', sw=0.2)
    for cy, s in ((P.COMMUNAL_CHAIR_Y[0], 1), (P.COMMUNAL_CHAIR_Y[1], -1)):
        cx = u(cy)
        G.r(sh, cx - 0.22, 0.43, cx + 0.22, 0.48, fill='#cdbfa9', sw=0.2)
        G.r(sh, cx + s * 0.20 - 0.025, 0.48, cx + s * 0.20 + 0.025, 0.86, fill='#6b5a48', sw=0.15)
        G.l(sh, cx - 0.2, 0.43, cx - 0.2, 0, sw=0.3); G.l(sh, cx + 0.2, 0.43, cx + 0.2, 0, sw=0.3)
    M = P.MOTHER
    mx = u(M['y'])
    G.l(sh, mx, P.JOISTS, mx, M['z'] + M['d'] / 2, sw=0.15)
    G.c(sh, mx, M['z'], M['d'] / 2, fill='#ebe4f2', sw=0.35)
    X, Y = G(mx, M['z'])
    R_ = M['d'] / 2 * S38
    for a in (0.35, 0.7):
        sh.ellipse(X, Y, R_ * a, R_, sw=0.15)
    sh.line(X - R_, Y, X + R_, Y, sw=0.15)
    G.l(sh, mx + 0.9, P.BEAM_Z, mx + 0.1, Cm['h'] + 0.02, sw=0.12, dash='1.5 1', stroke='#e7a24a')
    G.t(sh, mx + 0.62, M['z'] + 0.62, 'Mother EARF', size=2.4, weight=600)
    BQ = P.BANQ
    G.r(sh, u(BQ['y1']), 0, u(0), BQ['seat'], fill=TINT['mohair'], sw=0.3)
    G.r(sh, u(0.22), BQ['seat'], u(0), BQ['back'], fill=TINT['mohair'], sw=0.3)
    bt = P.BANQ_TABLE
    G.r(sh, u(bt['y0'] + bt['d']), bt['h'] - 0.04, u(bt['y0']), bt['h'], fill='#5a4636', sw=0.2)
    G.l(sh, u(bt['y0'] + bt['d'] / 2), 0, u(bt['y0'] + bt['d'] / 2), bt['h'] - 0.04, sw=0.4)
    for z, s in ((0, "0'-0\""), (C['top_z'], "3'-6\""), (rim, "5'-8\""), (M['z'], "8'-4\""), (P.BEAM_Z, "14'-9\""),
                 (P.JOISTS, "15'-9\"")):
        X, Y = G(W + T, z)
        sh.line(X + 2, Y, X + 14, Y, sw=0.15)
        sh.poly([(X + 14, Y), (X + 12.4, Y - 1.4), (X + 15.6, Y - 1.4)], fill=INK, sw=0.1)
        sh.text(X + 17, Y + 0.9, s, size=2.5)
    for yy, s in ((W - 0.3, 'Back bar'), (P.COUNTER['y0'] + 0.3, 'Counter'), (P.STOOL_Y, 'Counter chair'),
                  (P.MOTHER['y'], 'Communal table'), (1.4, 'Banquette')):
        G.tag(sh, u(yy), -0.55, s, size=2.4, weight=700, spacing=0.4)
    G.t(sh, u(10.0), 2.95, 'Record wall and booth (beyond)', size=2.3)
    G.t(sh, u(5.1), 2.25, 'Listening room door', size=2.2, anchor='middle')
    G.t(sh, u(1.5), 3.2, 'WC 1 wall (beyond)', size=2.2, anchor='middle', fill=GREY)
    G.dim(sh, u(W), -0.25, u(0), -0.25, -12)
    G.dim(sh, u(C['y_work']), C['top_z'] + 0.02, u(B['y0']), C['top_z'] + 0.02, 0, text="3'-1\"")
    sh.text(PLAN_O[0], 290, 'B  ·  SECTION ACROSS THE BAR ROOM, LOOKING TOWARD THE BACK', size=3.2, weight=700, spacing=0.6)
    sh.text(PLAN_O[0], 295.5, "3/8\" = 1'-0\"  ·  cut through the communal table and Mother EARF (A-101)", size=2.5, fill=GREY)
    sh.scale_bar(PLAN_O[0] + 330, 530, S38, label="3/8\" = 1'-0\"")
    sh.scale_bar(PLAN_O[0], 212, S4)
    return sh


def axo_uri(w=2400):
    import base64, subprocess
    j = os.path.join(OUT, '.axo-embed.jpg')
    subprocess.run(['convert', os.path.join(OUT, 'axo.png'), '-resize', f'{w}x', '-quality', '88', j], check=True)
    d = base64.b64encode(open(j, 'rb').read()).decode()
    os.remove(j)
    return 'data:image/jpeg;base64,' + d


def axo_sheet():
    import json
    sh = Sheet()
    sh.frame('A-301', 'Axonometric', 'the plan built as a model', SHEETS,
             notes=[('HOW IT WAS MADE', ['The plan (plan42.py) built in Blender as a', 'cutaway: the far walls cut at 8 ft 6 in,',
                                         'the near wall at 3 ft 3 in, the back of', 'house at 4 ft 3 in. The products as', 'simple solids in their colours.'])])
    x, y, w, h = 30, 40, 760, 506.7
    sh.image(x, y, w, h, axo_uri(3000))
    an = os.path.join(OUT, 'axo.anchors.json')
    if os.path.exists(an):
        A = json.load(open(an))
        for i, (k, (u, v)) in enumerate(sorted(A.items(), key=lambda kv: kv[1][0])):
            px, py = x + u * w, y + v * h
            sh.circle(px, py, 3.2, fill=INK, stroke=PAPER, sw=0.4)
            sh.text(px, py + 1.1, str(i + 1), size=2.8, weight=700, anchor='middle', fill=PAPER)
            col, row = divmod(i, 6)
            lx, ly = x + 8 + col * 150, y + h + 14 + row * 5.4
            sh.text(lx, ly, f'{i + 1}', size=2.8, weight=700)
            sh.text(lx + 7, ly, k, size=2.8)
    sh.text(x, y - 8, 'AXONOMETRIC FROM THE STREET CORNER, THE WALLS CUT AWAY', size=3.2, weight=700, spacing=0.6)
    return sh


# --- A-000: the house in numbers -------------------------------------------------------------------------------------
def cover_sheet():
    sh = Sheet()
    sh.frame('A-000', 'The house in numbers', 'areas, load, code', SHEETS)
    x = 40
    sh.text(x, 52, 'PLANET EARF', size=22, weight=700, spacing=3.0)
    sh.text(x, 66, 'A listening bar for San Francisco. One floor, 2,800 sq ft, 55 seats.', size=7.0)
    sh.text(x, 76, 'The shop and the window lounge at the street; the bar room under Mother EARF; the selector in a wall of '
            'records; the listening room behind it, its Tropos stacks facing the front.', size=3.4, fill='#55524c')
    if os.path.exists(os.path.join(OUT, 'axo.png')):
        sh.image(330, 100, 460, 307, axo_uri())
    # key plan: the zones only, small
    F = Frame(x, 215, 1000 / 96)
    zones = [((0, 0, P.FRONT_X1, W), '#efe6d6', 'Shop + lounge'), ((P.FRONT_X1, 0, P.PARTITION['x0'], W), '#e6dccb', 'Bar room'),
             ((P.LISTEN['x0'], P.LISTEN['y0'], L, W), '#d9c9c2', 'Listening'), ((P.BOH['x0'], 0, L, P.LISTEN['y0']), '#e9e9e6', 'Back of house')]
    for (a0, b0, a1, b1), c, s in zones:
        F.r(sh, a0, b0, a1, b1, fill=c, sw=0.3)
        F.t(sh, (a0 + a1) / 2, (b0 + b1) / 2 - 0.15, s, size=3.0, anchor='middle', weight=600)
    F.r(sh, 0, 0, L, W, sw=0.8)
    sh.text(x, 99, "KEY PLAN  ·  1/8\" = 1'-0\"", size=2.6, weight=700, spacing=0.5)
    # areas
    y = 240
    sh.text(x, y, 'AREAS', size=2.8, weight=700, spacing=0.6)
    rows = [('Shop and window lounge', P.FRONT_X1 * W), ('Bar room, the booth, the record wall', (P.PARTITION['x0'] - P.FRONT_X1) * W),
            ('Listening room and lobby', (L - P.LISTEN['x0']) * (W - P.LISTEN['y0'])),
            ('Back of house: three WCs, stock and office, the corridor', (L - P.BOH['x0']) * P.LISTEN['y0']),
            ('Partitions and the lobby walls', W * L - P.FRONT_X1 * W - (P.PARTITION['x0'] - P.FRONT_X1) * W - (L - P.LISTEN['x0']) * (W - P.LISTEN['y0']) - (L - P.BOH['x0']) * P.LISTEN['y0']), ('', 0)]
    yy = y + 8
    tot = 0
    for k, a in rows[:-1]:
        sh.text(x, yy, k, size=3.0); sh.text(x + 150, yy, f'{a * P.SQFT:,.0f} sq ft', size=3.0, anchor='end'); yy += 6; tot += a
    sh.line(x, yy - 4, x + 150, yy - 4, sw=0.3)
    sh.text(x, yy + 1, 'Inside the walls', size=3.0, weight=700)
    sh.text(x + 150, yy + 1, f'{tot * P.SQFT:,.0f} sq ft', size=3.0, anchor='end', weight=700)
    # occupant load
    x2 = x
    y = 292
    sh.text(x2, y, 'OCCUPANT LOAD  ·  CBC 2022 TABLE 1004.5', size=2.8, weight=700, spacing=0.6)
    rows, total = P.occupant_load()
    yy = y + 8
    for k, sf, f, how, n in rows:
        sh.text(x2, yy, k, size=3.0)
        sh.text(x2 + 140, yy, f'{sf:,} sf', size=3.0, anchor='end', fill=GREY)
        sh.text(x2 + 172, yy, f'/ {f} {how}' if f else 'by seat', size=3.0, anchor='end', fill=GREY)
        sh.text(x2 + 185, yy, str(n), size=3.0, anchor='end', weight=600)
        yy += 6
    sh.line(x2, yy - 4, x2 + 185, yy - 4, sw=0.3)
    sh.text(x2, yy + 1, 'Occupant load', size=3.0, weight=700)
    sh.text(x2 + 185, yy + 1, str(total), size=3.0, anchor='end', weight=700)
    sh.text(x2, yy + 8, 'Seats 55 · standing room at the counter and the shop. Post the load at the door (CBC 1004.9).', size=2.7, fill='#55524c')
    ro, to = P.occupant_load_option()
    sh.text(x2, yy + 15, f'OPTION: {to} OCCUPANTS, NO SPRINKLER REQUIREMENT', size=2.6, weight=700, spacing=0.5)
    sh.lines_of(x2, yy + 20.5, ['Count the front room as the shop it is (mercantile, 60 sq ft gross a person: 15) and fix the',
                                'listening chairs to the floor (11 seats): ' + f'{to} in all. Ask the building official before relying on it.'],
                size=2.7, fill='#55524c')
    # code thresholds
    y = 395
    sh.text(x, y, 'WHAT THE LOAD TRIGGERS (CALIFORNIA BUILDING AND PLUMBING CODES, 2022; SF AMENDMENTS)', size=2.8, weight=700, spacing=0.6)
    T = [('Group', 'A-2 (a bar, 50 or more). Under 50 it would be a B, with no Place of Assembly permit: not possible at this size and seat count.'),
         ('Exits', 'Two (more than 49): the street door and the rear door, a third of the diagonal apart (sprinklered). Doors swing out with panic hardware.'),
         ('Sprinklers', 'Required for A-2 at 100 or more (CBC 903.2.1.2). Check the building: many SF shells have them; else a deferred submittal.'),
         ('Fire alarm', 'Not required for A-2 under 300 (CBC 907.2.1). Emergency lights and lit exit signs are.'),
         ('Place of Assembly', 'SF Fire Department permit for 50 or more, with the load posted.'),
         ('Egress width', '0.2 in per occupant for doors (sprinklered): 27 in needed, 32 in clear at each door.'),
         ('Plumbing', 'CPC Table 422.1 for A-2; three single-user all-gender WCs, each accessible, counted for either sex (CPC 422.2). Confirm the count against the plumbing official\'s load.'),
         ('Accessibility', 'CBC 11B: one level, 36 in routes, the counter\'s 60 in low end at 34 in, 5% of dining seats accessible, accessible WCs.'),
         ('Energy', 'Title 24 Part 6 lighting allowance for the space types; dimming and controls throughout.')]
    yy = y + 8
    import textwrap
    for k, t in T:
        sh.text(x, yy, k, size=3.0, weight=700)
        yy = sh.lines_of(x + 40, yy, textwrap.wrap(t, 105), size=3.0, lead=1.35) + 2.2
    sh.text(x, yy + 4, 'All proposals. The building official sets the load; an architect and the city\'s plan check confirm every line '
            'before anything is built. Sources and the permit path: spinoffs/barkhorn/planet/r42/RULES.md.', size=2.7, fill=GREY)
    return sh


def main():
    os.makedirs(OUT, exist_ok=True)
    built = {'A-000': cover_sheet(), 'A-101': plan_sheet(), 'A-102': rcp_sheet(), 'A-201': sections_sheet(), 'A-301': axo_sheet()}
    for n, sh in built.items():
        open(os.path.join(OUT, f'{n}.svg'), 'w').write(sh.svg())
        print(os.path.join(OUT, f'{n}.svg'))


if __name__ == '__main__':
    main()
