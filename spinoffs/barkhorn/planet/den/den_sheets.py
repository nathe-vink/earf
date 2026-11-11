"""Planet EARF, round 33 (the den): the floor plan and the long section at 1:50 on A3, in the fab kit's sheet
(studio/fabkit/drawings.py's Page: its border, title block, type and dimension style), every line from den_plan.py.

    .venv-fab/bin/python spinoffs/barkhorn/planet/den/den_sheets.py     # -> spinoffs/barkhorn/planet/den/drawings/

Sheet 1, the plan: the shell and the shopfront with its recessed door; the bar, the back-bar and its two niches; the
banquette and its two-tops; the listening room's chairs, the Ember pair and where they aim, the record wall and its
console, the books; the seat counts; the acoustic treatment, by kind; and where each warm lamp stands. Sheet 2, the
long section through the room looking at the bar wall.
"""
import math, os, sys
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import den_plan as P                                                # noqa: E402
import drawings as DR                                               # noqa: E402

OUT = os.path.join(HERE, 'drawings')
K = 50.0
MM = 1000.0 / K
INK = DR.INK
TREAT = {'curtain': '#7A3A36', 'books': '#B9A27E', 'records': '#C8B08A', 'slats': '#8A6440', 'rug': '#D8B8A0',
         'upholstery': '#9A5A50'}
WALNUT = '#6B4A30'
LAMP = '#E8A040'
SPEAKER = (0.560, 0.428, 1.293)

PRODUCT = SimpleNamespace(title='Planet EARF', kind='Listening bar, San Francisco (a proposal, round 33)',
                          name='planet', drawing_prefix='PLE', revision='B', drawing_style={})


def _poly(ax, pts, fc='none', ec=INK, lw=0.35, ls='-', z=3, hatch=None, alpha=1.0):
    from matplotlib.patches import Polygon
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw * DR.PT, ls=ls, zorder=z, hatch=hatch, alpha=alpha))


def _rect(ax, x0, y0, x1, y1, **k):
    _poly(ax, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **k)


def _circle(ax, c, r, fc='none', ec=INK, lw=0.3, z=3):
    from matplotlib.patches import Circle
    ax.add_patch(Circle(c, r, fc=fc, ec=ec, lw=lw * DR.PT, zorder=z))


def _rot(cx, cy, w, d, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return [(cx + c * u - s * v, cy + s * u + c * v) for u, v in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2))]


def plan_sheet(pg):
    import numpy as np
    ax = pg.ax
    ox, oy = 40.0, 112.0                       # the paper point of the plan's origin; x across the page, y up it
    X = lambda x: ox + x * MM
    Y = lambda y: oy + y * MM
    R = lambda x0, y0, x1, y1, **k: _rect(ax, X(x0), Y(y0), X(x1), Y(y1), **k)
    pg.head('Floor plan, 1:50. Metres in the plan; dimensions in millimetres. The street at the left; the bar along the '
            'top wall. A proposal: every number is a working assumption (README, "Assumptions") for the owner to overturn.')
    W, L, T = P.W, P.L, P.WALL_T
    E, Dr, Wn = P.ENTRY, P.DOOR, P.WINDOW
    wall = dict(fc='#3a3a3a', ec=INK, lw=0.3, z=4)
    R(0, -T, L + T, 0, **wall); R(0, W, L + T, W + T, **wall); R(L, 0, L + T, W, **wall)
    # the shopfront: the piers, the bulkhead and glass, the vestibule and its door
    R(-0.16, -T, 0, E['y0'], **wall); R(-0.16, Wn['y1'], 0, W + T, **wall); R(-0.16, E['y1'], 0, Wn['y0'], **wall)
    ax.plot([X(-0.09)] * 2, [Y(Wn['y0']), Y(Wn['y1'])], color=INK, lw=0.6 * DR.PT, zorder=5)
    ax.plot([X(-0.16)] * 2, [Y(Wn['y0']), Y(Wn['y1'])], color=INK, lw=0.2 * DR.PT, zorder=5)
    R(0, E['y0'] - 0.08, E['depth'], E['y0'], fc=INK, z=5); R(0, E['y1'], E['depth'], E['y1'] + 0.08, fc=INK, z=5)
    R(E['depth'], E['y0'] - 0.08, E['depth'] + 0.10, Dr['y0'], fc=INK, z=5)
    R(E['depth'], Dr['y1'], E['depth'] + 0.10, E['y1'] + 0.08, fc=INK, z=5)
    R(-0.16, E['y0'], E['depth'], E['y1'], fc='#efece6', lw=0.2, z=2, hatch='....')
    w = Dr['y1'] - Dr['y0']; a = np.linspace(0, math.pi / 2, 30)
    hx = E['depth'] + 0.08
    ax.plot([X(hx), X(hx + w)], [Y(Dr['y0'])] * 2, color=INK, lw=0.4 * DR.PT, zorder=5)
    ax.plot(X(hx) + w * MM * np.sin(a), Y(Dr['y0']) + w * MM * np.cos(a), color=INK, lw=0.18 * DR.PT, ls='--', zorder=5)
    ys = np.linspace(0.04, 0.85, 30)                                 # the velvet curtain inside the door
    ax.plot(X(E['depth'] + 0.35 + 0.05 * np.sin(ys * 25)), Y(ys), color=TREAT['curtain'], lw=0.8 * DR.PT, zorder=5)
    pg.text(X(-0.4), Y((E['y0'] + E['y1']) / 2), 'recessed\nentry', ha='right', va='center', size=7.1)
    pg.text(X(-0.4), Y((Wn['y0'] + Wn['y1']) / 2), 'display window,\ncafé curtains,\nname in gold leaf;\ntransom over',
            ha='right', va='center', size=7.1)
    # the bar: its top (dashed), the reeded front, the armrest, the footrail; the back-bar and the niches
    R(P.BAR_X0 - 0.08, P.BAR_FRONT - P.TOP_OVER, P.BAR_X1 + 0.08, P.BAR_FRONT + P.BAR_DEPTH + 0.03, ls='--', lw=0.25)
    R(P.BAR_X0, P.BAR_FRONT, P.BAR_X1, P.BAR_FRONT + P.BAR_DEPTH, fc=WALNUT, lw=0.35, alpha=0.55)
    ax.plot([X(P.BAR_X0 + 0.1), X(P.BAR_X1 - 0.1)], [Y(P.BAR_FRONT - P.FOOTRAIL['off'])] * 2, color='#A07A45',
            lw=0.7 * DR.PT, zorder=4)
    R(P.BAR_X0 - 0.30, P.BACKBAR_Y, P.BAR_X1 + 0.30, W, fc='#d9cbb8', lw=0.35)
    for nx, nw in P.NICHES:
        R(nx, P.BACKBAR_Y, nx + nw, W, fc='white', lw=0.3)
    pg.text(X((P.BAR_X0 + P.BAR_X1) / 2), Y(W - 0.23), 'back-bar: walnut, lit shelves, antique mirror',
            ha='center', va='center', size=7.1)
    pg.text(X((P.BAR_X0 + P.BAR_X1) / 2), Y(P.BAR_FRONT + 0.31), 'reeded walnut bar, walnut top, leather armrest, brass rail',
            ha='center', va='center', size=7.1, color='white')
    for x, y in P.stools():
        _circle(ax, (X(x), Y(y)), 0.20 * MM)
    for x in P.PENDANTS:
        _circle(ax, (X(x), Y(P.BAR_FRONT + 0.18)), 0.18 * MM, ec=LAMP, lw=0.5, z=6)
    # the banquette and the two-tops, their chairs; the window table
    R(P.BANQ_X0, 0.03, P.BANQ_X1, P.BANQ_D, fc=TREAT['upholstery'], lw=0.3)
    TB = P.TABLE
    for cx in P.TABLES:
        R(cx - TB['w'] / 2, TB['y'] - TB['d'] / 2, cx + TB['w'] / 2, TB['y'] + TB['d'] / 2, lw=0.3, fc='#d9cbb8')
        R(cx - 0.22, P.CHAIR_Y - 0.22, cx + 0.22, P.CHAIR_Y + 0.22, lw=0.25)
    wx, wy = P.WINDOW_TABLE
    _circle(ax, (X(wx), Y(wy)), 0.34 * MM, fc='#d9cbb8')
    for dy in (-0.62, 0.62):
        R(wx - 0.22, wy + dy - 0.22, wx + 0.22, wy + dy + 0.22, lw=0.25)
    for x in P.SCONCES_RIGHT:
        _circle(ax, (X(x), Y(0.20)), 0.10 * MM, ec=LAMP, lw=0.5, z=6)
    for x in P.SCONCES_LEFT_LOUNGE:
        _circle(ax, (X(x), Y(W - 0.20)), 0.10 * MM, ec=LAMP, lw=0.5, z=6)
    # the listening room: the cased opening and its curtains, the rug, the chairs, the side tables
    X0 = P.LOUNGE_X0
    R(X0 - 0.10, 0.0, X0 + 0.10, 0.18, fc=WALNUT); R(X0 - 0.10, W - 0.18, X0 + 0.10, W, fc=WALNUT)
    ax.plot([X(X0 - 0.10)] * 2, [Y(0.18), Y(W - 0.18)], color=INK, lw=0.18 * DR.PT, ls='--', zorder=5)
    for ya, yb in ((0.18, 0.18 + P.CURTAIN['w']), (W - 0.18 - P.CURTAIN['w'], W - 0.18)):
        ys = np.linspace(ya, yb, 40)
        ax.plot(X(X0 + 0.22 + 0.055 * np.sin(ys * 24)), Y(ys), color=TREAT['curtain'], lw=0.9 * DR.PT, zorder=5)
    Rg = P.RUG
    R(Rg['x0'], Rg['y0'], Rg['x1'], Rg['y1'], fc=TREAT['rug'], lw=0.25, ls=':', z=2, alpha=0.6)
    for x, y, f in P.CHAIRS:
        _poly(ax, [(X(px), Y(py)) for px, py in _rot(x, y, 0.80, 0.82, f - 90)], fc='#c8a07a', lw=0.3)
    for x, y in P.SIDE_TABLES:
        _circle(ax, (X(x), Y(y)), 0.21 * MM, fc='#d9cbb8')
    # the books (right wall) and the record wall (back wall) with the console
    B = P.BOOKS
    R(B['x0'], 0.0, B['x1'], B['depth'], fc=TREAT['books'], lw=0.3)
    pg.text(X((B['x0'] + B['x1']) / 2), Y(B['depth'] / 2), 'books to 2400 (a diffuser)', ha='center', va='center', size=7.1)
    Rc = P.REC
    R(L - Rc['depth'], Rc['y0'], L, Rc['y1'], fc=TREAT['records'], lw=0.3)
    C = P.CONSOLE
    R(L - C['d'] - 0.02, C['y0'], L - 0.02, C['y1'], fc=WALNUT, lw=0.35, z=5)
    pg.text(X(L - 0.75), Y(W / 2), 'console\n+ Cumulus', ha='right', va='center', size=7.1)
    # the speakers: plinth, cabinet, the axis they aim along
    for role, colour, x, y, z, rot in P.speakers():
        if role == 'lounge':
            _poly(ax, [(X(px), Y(py)) for px, py in _rot(x, y, P.PLINTH['w'], P.PLINTH['d'], rot)], fc=WALNUT, lw=0.3)
        _poly(ax, [(X(px), Y(py)) for px, py in _rot(x, y, SPEAKER[0], SPEAKER[1], rot)], fc=P.COLOURS[colour], lw=0.35, z=5)
        a = math.radians(rot); dx, dy = math.sin(a), -math.cos(a)
        ln = 1.2 if role == 'lounge' else 0.8
        ax.annotate('', xy=(X(x + dx * ln), Y(y + dy * ln)), xytext=(X(x + dx * 0.3), Y(y + dy * 0.3)),
                    arrowprops=dict(arrowstyle='-|>', lw=0.2 * DR.PT, color=INK, mutation_scale=5), zorder=6)
    lx, ly = P.LISTEN
    ax.plot([X(lx)], [Y(ly)], marker='+', color=INK, ms=6, zorder=6)
    # the zones and their seats
    S = P.SEATS
    for txt, (x, y) in [(f"BAR  {S['bar']} seats", ((P.BAR_X0 + P.BAR_X1) / 2, P.STOOL_Y - 0.50)),
                        (f"BANQUETTE  {S['banquette']} seats (5 two-tops)", ((P.BANQ_X0 + P.BANQ_X1) / 2, P.CHAIR_Y + 0.55)),
                        (f"WINDOW  {S['window']}", (wx + 0.55, wy - 0.95)),
                        (f"LISTENING ROOM  {S['lounge']} seats", ((X0 + L) / 2 - 0.4, 0.62))]:
        pg.text(X(x), Y(y), txt, ha='center', va='center', size=8, fontweight='bold')
    pg.text(X(0.25), Y(-T) - 22, f'{sum(S.values())} seats; occupant load {P.CAPACITY} (Group B, under 50)', ha='left',
            va='center', size=7.1)
    pg.dim((X(0), Y(-T) - 5), (X(L), Y(-T) - 5), -4, f'{L * 1000:.0f}  (56 ft)')
    pg.dim((X(L + T) + 3, Y(0)), (X(L + T) + 3, Y(W)), -4, f'{W * 1000:.0f}  (20 ft)')
    pg.dim((X(P.BAR_X0), Y(W + T) + 3), (X(P.BAR_X1), Y(W + T) + 3), 3, f'bar {(P.BAR_X1 - P.BAR_X0) * 1000:.0f}')
    # the legend
    lx0, ly0 = 22, 64
    pg.text(lx0, ly0 + 6, 'Acoustic treatment', size=8, fontweight='bold')
    items = [('curtain', 'oxblood wool velvet: the door curtain and the listening room\'s curtains (drawn, they close it off)'),
             ('books', 'books, floor to 2400, 300 deep: a diffuser on the listening room\'s right wall'),
             ('records', 'the record wall: cubbies of LPs 400 deep, to 2700, a diffuser'),
             ('slats', 'listening room ceiling: walnut slats 45 at 90 over 50 black absorber'),
             ('rug', 'a wool rug under the chairs; leather and velvet throughout'),
             ('upholstery', 'the banquette: oxblood leather, channel-tufted')]
    for k, (key, s) in enumerate(items):
        yy = ly0 - k * 5
        _rect(ax, lx0, yy - 1.5, lx0 + 6, yy + 1.5, fc=TREAT[key], ec=INK, lw=0.3)
        pg.text(lx0 + 8, yy, s, va='center', size=7.1)
    pg.text(lx0 + 200, ly0 + 12, 'Light (warm, 2200 to 2700 K), in pools', size=8, fontweight='bold')
    lights = ['circles in amber: shaded brass sconces at 1720 (six on the right wall, two on the brick);',
              'three spun-brass pendants over the bar, rims 800 over the top;',
              'the back-bar\'s shelves lit from strips under their front edges; a pinhole in each niche;',
              'Bell (Dust) on two two-tops, the window table and two lounge tables; candles on the rest;',
              'a picture light under the record wall\'s cornice; a soft lamp over each Ember speaker.']
    for k, s in enumerate(lights):
        pg.text(lx0 + 200, ly0 + 6 - k * 4.5, s, va='center', size=7.1)
    pg.text(lx0, 26, 'Products', size=8, fontweight='bold')
    prods = ['Atmosphere: the Ember pair either side of the record wall on low walnut plinths, each aimed at the listening seat (+);',
             'the Fog pair in the back-bar\'s two niches, floor 450, the horns at a stool\'s eye. Arrows: each speaker\'s axis.',
             'Bell (Dust): table lamps. Cumulus: a small stand-in on the console while the companions are redesigned.']
    for k, s in enumerate(prods):
        pg.text(lx0, 21.5 - k * 4.0, s, va='center', size=7.1)


def section_sheet(pg):
    ax = pg.ax
    ox, oy = 40.0, 110.0
    X = lambda x: ox + x * MM
    Z = lambda z: oy + z * MM
    R = lambda x0, z0, x1, z1, **k: _rect(ax, X(x0), Z(z0), X(x1), Z(z1), **k)
    yc = P.STOOL_Y - 0.6
    pg.head(f'Long section A-A, 1:50, cut along the room {yc * 1000:.0f} from the right-hand wall, looking at the bar wall: '
            'what is cut is drawn heavy, what lies beyond light. Heights in millimetres above the finished floor.')
    L, H = P.L, P.CEIL
    cut = dict(fc='#3a3a3a', ec=INK, lw=0.35, z=5)
    R(-0.16, -0.25, L + P.WALL_T, 0.0, **cut)
    R(-0.16, H, L + P.WALL_T, H + 0.30, **cut)
    R(L, 0, L + P.WALL_T, H, **cut)
    # the shopfront, cut: bulkhead, glass, transom, fascia
    Wn, Tr = P.WINDOW, P.TRANSOM
    R(-0.16, 0, 0, Wn['sill'], **cut); R(-0.16, Wn['head'], 0, Tr['z0'], **cut); R(-0.16, Tr['z1'], 0, H, **cut)
    ax.plot([X(-0.09)] * 2, [Z(Wn['sill']), Z(Wn['head'])], color=INK, lw=0.6 * DR.PT, zorder=6)
    ax.plot([X(-0.09)] * 2, [Z(Tr['z0']), Z(Tr['z1'])], color=INK, lw=0.6 * DR.PT, zorder=6)
    R(0.04, P.CAFE['z0'], 0.08, P.CAFE['z1'], fc='#E6D8BE', lw=0.2, z=6)
    # the wainscot beyond (where the back-bar is not), the plaster, the brick in the listening room
    R(0, 0, P.BAR_X0 - 0.2, P.WAINSCOT, fc=WALNUT, lw=0.2, alpha=0.35, z=2)
    R(P.BAR_X1 + 0.2, 0, P.LOUNGE_X0, P.WAINSCOT, fc=WALNUT, lw=0.2, alpha=0.35, z=2)
    R(P.LOUNGE_X0, 0, L, H, fc='#B0705A', lw=0.2, alpha=0.25, z=1, hatch='----')
    # beyond: the back-bar, its shelves and niches, the Fog pair
    bx0, bx1 = P.BAR_X0 - 0.30, P.BAR_X1 + 0.30
    R(bx0, 0, bx1, P.BASE_H, fc='#d9cbb8', lw=0.25)
    R(bx0, P.BASE_H, bx1, P.BACKBAR_TOP + 0.2, lw=0.25)
    for z in P.SHELVES_Z:
        ax.plot([X(bx0), X(bx1)], [Z(z)] * 2, color=WALNUT, lw=0.8 * DR.PT, zorder=3)
        ax.plot([X(bx0), X(bx1)], [Z(z - 0.04)] * 2, color=LAMP, lw=0.4 * DR.PT, zorder=3)
    for role, colour, x, y, z, rot in P.speakers():
        if role == 'backbar':
            R(x - 0.36, P.NICHE_Z0, x + 0.36, P.NICHE_Z0 + P.NICHE_H, fc='#F2E6D0', lw=0.3, z=4)
            R(x - SPEAKER[0] / 2, P.BAR_TOP_Z + P.TOP_T, x + SPEAKER[0] / 2, z + SPEAKER[2], fc=P.COLOURS[colour], lw=0.35, z=7)
            R(x - SPEAKER[0] / 2, z, x + SPEAKER[0] / 2, z + SPEAKER[2], ec=INK, lw=0.25, ls='--', z=5)
    # the bar beyond the stools: the reeded front (hatched), the top and armrest
    R(P.BAR_X0, P.KICK['h'], P.BAR_X1, P.BAR_TOP_Z, fc=WALNUT, lw=0.25, z=6, hatch='||||', alpha=0.8)
    R(P.BAR_X0, 0, P.BAR_X1, P.KICK['h'], fc='#A07A45', lw=0.25, z=6)
    R(P.BAR_X0 - 0.08, P.BAR_TOP_Z, P.BAR_X1 + 0.08, P.BAR_TOP_Z + P.TOP_T + 0.05, fc=WALNUT, lw=0.3, z=6)
    for x in P.PENDANTS:
        z0 = P.PENDANT_RIM
        ax.plot([X(x), X(x)], [Z(z0 + 0.26), Z(H)], color=INK, lw=0.15 * DR.PT, zorder=6)
        _poly(ax, [(X(x - 0.18), Z(z0)), (X(x + 0.18), Z(z0)), (X(x + 0.06), Z(z0 + 0.18)), (X(x - 0.06), Z(z0 + 0.18))],
              fc='#A07A45', lw=0.3, z=6)
    for x, y in P.stools():
        R(x - 0.2, 0.0, x + 0.2, 0.76, lw=0.3, z=8, fc='white')
    # the listening room: the header and the curtain, the slat ceiling, the Ember pair, the chairs, the record wall
    X0 = P.LOUNGE_X0
    R(X0 - 0.10, P.HEADER_Z, X0 + 0.10, H, **cut)
    R(X0 + 0.15, 0, X0 + 0.30, P.HEADER_Z, fc=TREAT['curtain'], lw=0.25, z=6)
    R(X0 + 0.12, H - 0.13, L, H - 0.01, fc=TREAT['slats'], lw=0.2, z=6, hatch='||||')
    for role, colour, x, y, z, rot in P.speakers():
        if role == 'lounge' and y > P.W / 2:
            R(x - P.PLINTH['w'] / 2, 0, x + P.PLINTH['w'] / 2, P.PLINTH['h'], fc=WALNUT, lw=0.3, z=6)
            R(x - SPEAKER[0] / 2, z, x + SPEAKER[0] / 2, z + SPEAKER[2], fc=P.COLOURS[colour], lw=0.35, z=6)
            pg.text(X(x), Z(z + SPEAKER[2]) + 2, 'Atmosphere Ember', ha='center', size=7.1)
    for x, y, f in P.CHAIRS:
        if y > 2.0:
            R(x - 0.4, 0.0, x + 0.4, 0.80, lw=0.25, z=7, fc='#c8a07a')
    Rc = P.REC
    R(L - Rc['depth'], 0, L, Rc['z1'], fc=TREAT['records'], lw=0.3, z=4)
    R(L - P.CONSOLE['d'] - 0.02, 0, L - 0.02, P.CONSOLE['h'], fc=WALNUT, lw=0.35, z=5)
    for z, s in ((P.BAR_TOP_Z, 'bar top 1070'), (P.NICHE_Z0, 'niche floor 450'),                  (P.SCONCE_Z, 'sconces 1720'), (P.HEADER_Z, 'header 2550'), (H, 'ceiling 3400')):
        ax.plot([X(P.BAR_X1 + 0.32), X(P.BAR_X1 + 0.5)], [Z(z)] * 2, color=INK, lw=0.18 * DR.PT, zorder=7)
        pg.text(X(P.BAR_X1 + 0.52), Z(z), s, ha='left', va='center', size=7.1, zorder=7, bbox=dict(fc='white', ec='none', pad=0.2))
    pg.dim((X(0), Z(-0.25) - 5), (X(L), Z(-0.25) - 5), -4, f'{L * 1000:.0f}')
    for txt, x in (('FRONT', 1.6), ('BAR (stools in front, the back-bar beyond)', (P.BAR_X0 + P.BAR_X1) / 2),
                   ('LISTENING ROOM', (X0 + L) / 2)):
        pg.text(X(x), Z(-0.25) - 17, txt, ha='center', size=8, fontweight='bold')
    pg.text(22, 40, 'Light, by source, all warm (2200 to 2700 K) and in pools: sconces, the bar\'s three pendants, the back-bar\'s '
            'shelf strips and niche pinholes,', size=7.1)
    pg.text(22, 35.5, 'Bell and candles on the tables, the record wall\'s picture light, a soft lamp over each Ember speaker. '
            'No coloured light but the speakers\' own.', size=7.1)


def _retitle(pg):
    from matplotlib.patches import Rectangle
    x0 = DR.A3[0] - 10 - 190
    pg.ax.add_patch(Rectangle((x0 + 1, 11), 144, 6, fc='white', ec='none', zorder=10))
    pg.ax.text(x0 + 3, 14.0, 'Set out from the shell\'s inside faces; joinery to +-2, the shell +-10', fontsize=DR.MIN_PT,
               va='center', zorder=11)


def write():
    from matplotlib.backends.backend_pdf import PdfPages
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'planet-earf-den-sheets.pdf')
    with PdfPages(path) as pdf:
        pg = DR.Page(PRODUCT, 1, 2, 'Floor plan'); plan_sheet(pg); _retitle(pg); pg.save(pdf, OUT)
        pg = DR.Page(PRODUCT, 2, 2, 'Long section A-A'); section_sheet(pg); _retitle(pg); pg.save(pdf, OUT)
    print(path)


if __name__ == '__main__':
    write()
