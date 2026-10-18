"""Planet EARF's drawings: the floor plan and the long section at 1:50 on A3, in the fab kit's sheet
(studio/fabkit/drawings.py's Page: its border, title block, type and dimension style), every line from plan.py.

    .venv-fab/bin/python spinoffs/barkhorn/planet/sheets.py     # -> spinoffs/barkhorn/planet/drawings/

Sheet 1, the plan: the shell, the window and the door; the bar and its eight panels in their colours, the back-bar and
the Fog niches; the booths, the stools, the lounge's chairs, the corner pairs and where they aim; the record wall's
cubbies by depth and the DJ desk; the seat counts; and the acoustic treatment, hatched by kind. Sheet 2, the long
section through the room looking at the party wall: the slab, the plenum and the membrane, the bar front's spectrum,
the back-bar's shelves, the Fog pair in their niches, the screens, the corner pairs and the record wall in section.
"""
import math, os, sys
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import plan as P                                                    # noqa: E402
import drawings as DR                                               # noqa: E402

OUT = os.path.join(HERE, 'drawings')
K = 50.0                          # 1:50
MM = 1000.0 / K                   # paper mm per metre
INK = DR.INK
TREAT = {'absorber': '#8E8A99', 'slats': P.COLOURS['haze'], 'diffuser': '#B9A27E', 'membrane': '#C9B8D8'}
SPEAKER = (0.560, 0.428, 1.293)   # an Atmosphere speaker's footprint and height (m)

PRODUCT = SimpleNamespace(title='Planet EARF', kind='Listening bar, Hayes Valley, San Francisco (a proposal)',
                          name='planet', drawing_prefix='PLE', revision='A', drawing_style={})


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
    ax = pg.ax
    ox, oy = 27.0, 75.0                                              # the paper point of the plan's origin
    X = lambda x: ox + x * MM
    Y = lambda y: oy + y * MM
    R = lambda x0, y0, x1, y1, **k: _rect(ax, X(x0), Y(y0), X(x1), Y(y1), **k)
    pg.head('Floor plan, 1:50. Metres in the plan; dimensions in millimetres. North is up the page only as drawn '
            '(the long street at the bottom, the side street at the left). A proposal: every number is a working '
            'assumption (README, "Assumptions") for the owner to overturn.')
    L, D, T = P.L, P.D, P.WALL_T
    W, Dr = P.WINDOW, P.DOOR
    # the walls in poché, the openings left
    wall = dict(fc='#3a3a3a', ec=INK, lw=0.3, z=4)
    R(-T, -T, W['x0'], 0, **wall); R(W['x1'], -T, L + T, 0, **wall)
    R(-T, D, L + T, D + T, **wall); R(L, 0, L + T, D, **wall)
    R(-T, 0, 0, Dr['y0'], **wall); R(-T, Dr['y1'], 0, D, **wall)
    # the window: glass on its line, the mullions
    ax.plot([X(W['x0']), X(W['x1'])], [Y(-0.085)] * 2, color=INK, lw=0.5 * DR.PT, zorder=5)
    ax.plot([X(W['x0']), X(W['x1'])], [Y(-0.2)] * 2, color=INK, lw=0.2 * DR.PT, zorder=5)
    for xm in W['mullions']:
        R(xm - 0.03, -0.12, xm + 0.03, -0.05, fc=INK, z=5)
    # the door and its swing (inward, hinged on the window side)
    import numpy as np
    w = Dr['y1'] - Dr['y0']
    ax.plot([X(0), X(w)], [Y(Dr['y0'])] * 2, color=INK, lw=0.4 * DR.PT, zorder=5)
    a = np.linspace(0, math.pi / 2, 30)
    ax.plot(X(0) + w * MM * np.cos(a), Y(Dr['y0']) + w * MM * np.sin(a), color=INK, lw=0.18 * DR.PT, ls='--', zorder=5)
    pg.text(X(-T) - 1, Y((Dr['y0'] + Dr['y1']) / 2), 'door + neon', ha='right', va='center', size=7.1)
    # the membrane's edge (dashed, above)
    g = P.MEMBRANE_GAP
    R(g, g, L - g, D - g, ec=TREAT['membrane'], lw=0.5, ls=(0, (6, 3)), z=2)
    # the bar: its top (dashed), the eight panels in their colours, the body
    R(P.BAR_X0 - 0.10, P.BAR_FRONT - P.TOP_OVER, P.BAR_X1 + 0.10, P.BAR_FRONT + P.BAR_DEPTH + 0.04, ls='--', lw=0.25)
    R(P.BAR_X0, P.BAR_FRONT, P.BAR_X1, P.BAR_FRONT + P.BAR_DEPTH, lw=0.35)
    for i, c in enumerate(P.PANELS):
        a0 = P.BAR_X0 + i * P.PANEL_W
        R(a0, P.BAR_FRONT, a0 + P.PANEL_W, P.BAR_FRONT + 0.06, fc=P.COLOURS[c] if c != 'fog' else '#E8EAEA', lw=0.2, z=5)
        pg.text(X(a0 + P.PANEL_W / 2), Y(P.BAR_FRONT + 0.25), c.capitalize(), ha='center', va='center', size=7.1)
    ax.plot([X(P.BAR_X0 + 0.1), X(P.BAR_X1 - 0.1)], [Y(P.BAR_FRONT - P.FOOTRAIL['off'])] * 2, color=INK, lw=0.5 * DR.PT,
            zorder=4)
    # the back-bar and the niches
    R(P.BAR_X0 - 0.35, P.BACKBAR_Y, P.BAR_X1 + 0.35, D, fc='#efece6', lw=0.35)
    for nx, nw in P.NICHES:
        R(nx, P.BACKBAR_Y, nx + nw, D, fc='white', lw=0.3)
    pg.text(X((P.BAR_X0 + P.BAR_X1) / 2), Y(D - 0.23), 'back-bar: edge-lit shelves over a 920 counter', ha='center',
            va='center', size=7.1)
    # the stools
    for x, y in P.stools():
        _circle(ax, (X(x), Y(y)), 0.20 * MM)
    # the booths
    for x0 in P.BOOTHS:
        x1 = x0 + P.BOOTH_LEN
        R(x0, 0.10, x0 + P.BENCH_D, P.BOOTH_DEPTH, fc='#d9d2c8', lw=0.3)
        R(x1 - P.BENCH_D, 0.10, x1, P.BOOTH_DEPTH, fc='#d9d2c8', lw=0.3)
        R(x0 + P.BENCH_D + 0.08, 0.15, x1 - P.BENCH_D - 0.08, 0.15 + P.TABLE['d'], lw=0.3)
        _circle(ax, (X(x0 + P.BOOTH_LEN / 2), Y(0.37)), 0.108 * MM, fc=P.COLOURS['ember'], lw=0.2, z=5)
    # the screens
    for ya, yb in ((1.75, P.SCREEN_OPEN[0]), (P.SCREEN_OPEN[1], D - 1.75)) if P.SCREENS else ():
        ys = np.linspace(ya, yb, 40)
        ax.plot(X(P.SCREEN_X + 0.06 * np.sin(2 * math.pi * (ys - ya) / (yb - ya) * 2)), Y(ys), color=INK, lw=0.5 * DR.PT,
                zorder=4)
    # the lounge: rug, chairs, side tables
    R(12.55, 1.70, 15.65, 7.45, ls=':', lw=0.25)
    for x, y, f in P.CHAIRS:
        _poly(ax, [(X(px), Y(py)) for px, py in _rot(x, y, 0.80, 0.82, f - 90)], fc='#e6dccb', lw=0.3)
    for x, y in P.SIDE_TABLES:
        _circle(ax, (X(x), Y(y)), 0.22 * MM)
        _circle(ax, (X(x), Y(y)), 0.108 * MM, fc=P.COLOURS['ember'], lw=0.2, z=5)
    # the speakers: plinth, cabinet, and the axis they aim along
    for role, colour, x, y, z, rot in P.speakers():
        if role != 'backbar':
            _poly(ax, [(X(px), Y(py)) for px, py in _rot(x, y, P.PLINTH['w'], P.PLINTH['d'], rot)], fc='#2a2a2e', lw=0.3)
        fc = P.COLOURS[colour] if colour != 'fog' else '#F0F2F2'
        _poly(ax, [(X(px), Y(py)) for px, py in _rot(x, y, SPEAKER[0], SPEAKER[1], rot)], fc=fc, lw=0.35, z=5)
        a = math.radians(rot); dx, dy = math.sin(a), -math.cos(a)
        ln = 1.2 if role != 'backbar' else 0.9
        ax.annotate('', xy=(X(x + dx * ln), Y(y + dy * ln)), xytext=(X(x + dx * 0.3), Y(y + dy * 0.3)),
                    arrowprops=dict(arrowstyle='-|>', lw=0.2 * DR.PT, color=INK, mutation_scale=5), zorder=6)
    lx, ly = P.LISTEN
    ax.plot([X(lx)], [Y(ly)], marker='+', color=INK, ms=6, zorder=6)
    # the record wall, its cubbies by depth, and the DJ desk
    import random
    rnd = random.Random(7)
    cell = P.REC_CELL; nc = int((P.REC_Y1 - P.REC_Y0) / cell); y0 = (P.REC_Y0 + P.REC_Y1) / 2 - nc * cell / 2
    for ci in range(nc):
        dpt = rnd.choice([0.30, 0.36, 0.42, 0.48, 0.55])
        R(L - dpt, y0 + ci * cell, L, y0 + (ci + 1) * cell, fc=TREAT['diffuser'], lw=0.2, hatch='////' if False else None)
    R(L - P.DJ['desk_d'], P.DJ['y0'], L, P.DJ['y1'], fc='#2a2a2e', lw=0.35, z=5)
    pg.text(X(L - 0.9), Y(D / 2), 'DJ desk\n+ Cumulus', ha='right', va='center', size=7.1)
    # the acoustic treatment: slats over absorber (street wall of the lounge), plain absorber opposite
    S = P.SLATS
    R(S['x0'] - 0.05, 0.0, S['x1'] + 0.05, P.ABSORBER_T, fc=TREAT['absorber'], lw=0.2, z=5)
    x = S['x0']
    while x + S['w'] <= S['x1']:
        R(x, P.ABSORBER_T + S['gap'], x + S['w'], P.ABSORBER_T + S['gap'] + S['t'], fc=TREAT['slats'], ec=TREAT['slats'],
          lw=0.1, z=5)
        x += S['pitch']
    R(P.SCREEN_X + 0.4, D - P.ABSORBER_T, L - 1.4, D, fc=TREAT['absorber'], lw=0.2, z=5)
    # the zones and their seats
    for txt, (x, y) in [(f"BAR  {P.SEATS['bar']} seats", ((P.BAR_X0 + P.BAR_X1) / 2, P.STOOL_Y - 0.55)),
                        (f"BOOTHS  {P.SEATS['booths']} seats (4 x 4)", (6.0, 1.95)),
                        (f"LISTENING LOUNGE  {P.SEATS['lounge']} seats", (15.6, 7.55))]:
        pg.text(X(x), Y(y), txt, ha='center', va='center', size=8, fontweight='bold')
    total = sum(P.SEATS.values())
    pg.text(X(0.3), Y(5.4), f'{total} seats; occupant load {P.CAPACITY}\n(Group B, under 50)', ha='left', va='center', size=7.1)
    # dimensions
    pg.dim((X(0), Y(-T) - 4), (X(L), Y(-T) - 4), -4, f'{L * 1000:.0f}  (60 ft)')
    pg.dim((X(L + T) + 3, Y(0)), (X(L + T) + 3, Y(D)), -4, f'{D * 1000:.0f}  (30 ft)')
    pg.dim((X(P.BAR_X0), Y(D + T) + 3), (X(P.BAR_X1), Y(D + T) + 3), 3, f'bar front {P.BAR_X1 * 1000 - P.BAR_X0 * 1000:.0f}')
    pg.dim((X(W['x0']), Y(-T) - 12), (X(W['x1']), Y(-T) - 12), -3, f'window {(W["x1"] - W["x0"]) * 1000:.0f}')
    # the legend
    lx0, ly0 = 22, 46
    pg.text(lx0, ly0 + 6, 'Acoustic treatment', size=8, fontweight='bold')
    items = [('membrane', 'ceiling: back-lit micro-perforated membrane, 570 plenum with absorber (NRC 0.85), dashed'),
             ('slats', 'tinted Haze slats 75 x 12 at 150, 75 proud of the absorber (street wall of the lounge)'),
             ('absorber', 'dark fabric-faced absorber, 100 (both lounge side walls)'),
             ('diffuser', 'record wall: cubbies 300 to 550 deep, a diffuser')]
    for k, (key, s) in enumerate(items):
        yy = ly0 - k * 5
        _rect(ax, lx0, yy - 1.5, lx0 + 6, yy + 1.5, fc=TREAT[key] if key != 'membrane' else 'none',
              ec=TREAT[key] if key == 'membrane' else INK, lw=0.3, ls=(0, (3, 1.5)) if key == 'membrane' else '-')
        pg.text(lx0 + 8, yy, s, va='center', size=7.1)
    pg.text(lx0, 24.5, 'Products', size=8, fontweight='bold')
    prods = ['Atmosphere pairs on Smoke plinths 120 high: Ember (the lounge\'s front corners), Ice (either side of the record wall);',
             'arrows: each speaker\'s axis, aimed at the listening seat (+). The Fog pair: the back-bar\'s niches, floor 450.',
             'Bell: six Fog pendants over the bar, Ember lamps on the four booth tables and the two lounge side tables. Cumulus (Ice): the DJ desk.']
    for k, s in enumerate(prods):
        pg.text(lx0, 19.8 - k * 4.0, s, va='center', size=7.1)


def section_sheet(pg):
    ax = pg.ax
    ox, oy = 27.0, 100.0
    X = lambda x: ox + x * MM
    Z = lambda z: oy + z * MM
    R = lambda x0, z0, x1, z1, **k: _rect(ax, X(x0), Z(z0), X(x1), Z(z1), **k)
    yc = P.BAR_FRONT - 1.40
    pg.head(f'Long section A-A, 1:50, cut along the room {yc * 1000:.0f} from the street wall, looking at the party wall: '
            'what is cut is drawn heavy, what lies beyond it light. Heights in millimetres above the finished floor.')
    L, H, T = P.L, P.SLAB, P.WALL_T
    cut = dict(fc='#3a3a3a', ec=INK, lw=0.35, z=5)
    R(-T, -0.25, L + T, 0.0, **cut)                                  # the slab on grade
    R(-T, H, L + T, H + 0.25, **cut)                                 # the slab above
    R(-T, 0, 0, H, **cut); R(L, 0, L + T, H, **cut)                  # the end walls
    R(-T, 0, 0, P.DOOR['h'], fc='white', ec=INK, lw=0.3, z=6)        # the door, in the side street's wall
    # the plenum and the membrane
    R(0, P.MEMBRANE + 0.03, L, H, fc='none', ec=TREAT['absorber'], lw=0.2, hatch='xxxx', z=2)
    ax.plot([X(P.MEMBRANE_GAP), X(L - P.MEMBRANE_GAP)], [Z(P.MEMBRANE)] * 2, color=TREAT['membrane'], lw=1.6 * DR.PT, zorder=6)
    pg.text(X(L / 2) + 40, Z(P.MEMBRANE) - 3.5, 'back-lit acoustic membrane: the colour clock', ha='center', size=7.1)
    pg.text(X(L / 2), Z((P.MEMBRANE + H) / 2), 'plenum: absorber over the membrane, the LEDs', ha='center', va='center',
            size=7.1, bbox=dict(fc='white', ec='none', pad=0.3))
    # beyond: the back-bar (counter, shelves, niches, head)
    bx0, bx1 = P.BAR_X0 - 0.35, P.BAR_X1 + 0.35
    R(bx0, 0, bx1, P.BASE_H, lw=0.25)
    R(bx0, P.BASE_H, bx1, P.SHELF_TOP_Z + 0.12, lw=0.25)
    for z in P.SHELVES_Z:
        ax.plot([X(bx0), X(bx1)], [Z(z)] * 2, color='#c8a15a', lw=0.5 * DR.PT, zorder=3)
    for role, colour, x, y, z, rot in P.speakers():
        if role == 'backbar':
            n0 = x - 0.37
            R(n0, P.NICHE_Z0, n0 + 0.74, P.NICHE_Z0 + P.NICHE_H, fc='white', lw=0.3, z=4)
    # the bar, cut: the panels' line is beyond the cut (drawn as the elevation of the panels, coloured)
    for i, c in enumerate(P.PANELS):
        a0 = P.BAR_X0 + i * P.PANEL_W
        R(a0, P.KICK, a0 + P.PANEL_W, P.BAR_TOP_Z, fc=P.COLOURS[c] if c != 'fog' else '#EDEFEF', lw=0.25, z=6)
    R(P.BAR_X0 - 0.1, P.BAR_TOP_Z, P.BAR_X1 + 0.1, P.BAR_TOP_Z + P.TOP_T, fc='#222', lw=0.25, z=6)
    # the Fog pair beyond the bar, above its top only (the rest hidden behind the bar front)
    for role, colour, x, y, z, rot in P.speakers():
        if role == 'backbar':
            R(x - SPEAKER[0] / 2, z, x + SPEAKER[0] / 2, z + SPEAKER[2], ec=INK, lw=0.25, ls='--', z=5)
            R(x - SPEAKER[0] / 2, P.BAR_TOP_Z + P.TOP_T, x + SPEAKER[0] / 2, z + SPEAKER[2], fc='#F4F5F5', lw=0.35, z=7)
    # the pendants and the stools
    for x in [P.BAR_X0 + 0.7 + 1.4 * i for i in range(6)]:
        z0 = P.BAR_TOP_Z + P.TOP_T + 0.78
        ax.plot([X(x), X(x)], [Z(z0 + 0.2), Z(P.MEMBRANE)], color=INK, lw=0.15 * DR.PT, zorder=6)
        _poly(ax, [(X(x - 0.216), Z(z0)), (X(x + 0.216), Z(z0)), (X(x + 0.05), Z(z0 + 0.19)), (X(x - 0.05), Z(z0 + 0.19))],
              fc='#F4F5F5', lw=0.3, z=6)
    for x, y in P.stools():
        R(x - 0.2, 0.0, x + 0.2, 0.76, lw=0.3, z=8, fc='white')
    # the screens (cut), the lounge beyond, the corner pairs on their plinths, the chairs
    if P.SCREENS:
        R(P.SCREEN_X - 0.01, 0, P.SCREEN_X + 0.01, P.SCREEN_H, fc=INK, lw=0.3, z=8)
    for role, colour, x, y, z, rot in P.speakers():
        if role in ('front', 'back') and y > P.D / 2:
            R(x - P.PLINTH['w'] / 2, 0, x + P.PLINTH['w'] / 2, P.PLINTH['h'], fc='#2a2a2e', lw=0.3, z=5)
            R(x - SPEAKER[0] / 2, z, x + SPEAKER[0] / 2, z + SPEAKER[2], fc=P.COLOURS[colour], lw=0.35, z=5)
            pg.text(X(x), Z(z + SPEAKER[2]) + 2, f'Atmosphere {colour.capitalize()}', ha='center', size=7.1)
    for x, y, f in P.CHAIRS:
        if 2.0 < y < 7.0:
            R(x - 0.4, 0.0, x + 0.4, 0.80, lw=0.25, z=7, fc='#e6dccb')
    # the record wall: cubbies to the membrane, the DJ desk (cut at the middle of the wall)
    for k in range(int((P.REC_Z1 - 0.05) / P.REC_CELL) + 1):
        z = 0.05 + k * P.REC_CELL
        if z < P.DJ['recess_z']:
            continue
        ax.plot([X(L - 0.55), X(L)], [Z(z)] * 2, color=INK, lw=0.2 * DR.PT, zorder=5)
    R(L - 0.55, P.DJ['recess_z'], L, P.REC_Z1, fc=TREAT['diffuser'], lw=0.3, z=4)
    R(L - P.DJ['desk_d'], 0, L, P.DJ['desk_z'], fc='#2a2a2e', lw=0.35, z=6)
    R(L - 0.65, P.DJ['desk_z'], L - 0.17, P.DJ['desk_z'] + 0.135, fc='#B5D9EE', lw=0.3, z=6)
    pg.text(X(L - 0.9), Z(P.DJ['desk_z']) + 2, 'Cumulus', ha='right', size=7.1)
    # heights
    for z, s in ((P.BAR_TOP_Z, 'bar top 1070'), (P.NICHE_Z0, 'niche floor 450'), (P.MEMBRANE, 'membrane 3700'),
                 (H, 'slab 4267'), (P.SHELF_TOP_Z, 'back-bar head 3300')):
        ax.plot([X(0.05), X(0.35)], [Z(z)] * 2, color=INK, lw=0.18 * DR.PT, zorder=7)
        pg.text(X(0.38), Z(z), s, ha='left', va='center', size=7.1, zorder=7, bbox=dict(fc='white', ec='none', pad=0.2))
    pg.dim((X(0), Z(-0.25) - 5), (X(L), Z(-0.25) - 5), -4, f'{L * 1000:.0f}')
    # the zone names under the floor
    for txt, x in (('ENTRY', 1.0), ('BAR (stools in front, the back-bar beyond)', 6.15), ('LISTENING LOUNGE', 14.7)):
        pg.text(X(x), Z(-0.25) - 17, txt, ha='center', size=8, fontweight='bold')
    pg.text(22, 40, 'Light, by source: the membrane (the colour clock); the bar\'s eight panels, back-lit through a white liner '
            'from LEDs in a 75 cavity;', size=7.1)
    pg.text(22, 35.5, 'the back-bar\'s light-guide shelves and Fog-white back panel; the niches; the slats\' LED in their gap; '
            'Bell; pinhole spots on', size=7.1)
    pg.text(22, 31, 'each corner pair, the bar top and the DJ desk. Section cut drawn heavy; beyond, light.', size=7.1)


def _retitle(pg):
    """The kit's title block names a product's tolerances; a room's are a builder's."""
    from matplotlib.patches import Rectangle
    x0 = DR.A3[0] - 10 - 190
    pg.ax.add_patch(Rectangle((x0 + 1, 11), 144, 6, fc='white', ec='none', zorder=10))
    pg.ax.text(x0 + 3, 14.0, 'Set out from the shell\'s inside faces; built to +-5, panels and shelves +-1', fontsize=DR.MIN_PT,
               va='center', zorder=11)


def write():
    from matplotlib.backends.backend_pdf import PdfPages
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'planet-earf-sheets.pdf')
    with PdfPages(path) as pdf:
        pg = DR.Page(PRODUCT, 1, 3, 'Floor plan'); plan_sheet(pg); _retitle(pg); pg.save(pdf, OUT)
        pg = DR.Page(PRODUCT, 2, 3, 'Long section A-A'); section_sheet(pg); _retitle(pg); pg.save(pdf, OUT)
    print(path)


if __name__ == '__main__':
    write()
