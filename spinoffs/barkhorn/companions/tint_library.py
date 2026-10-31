"""The Tint Library (a proposal, round 43, 2026-10-31; idea (f) in r47-brand's brandbook/IDEAS.md): EARF's eight tints
as stepped chips in a case, for the designers and architects who specify them, the press mailer, and a first product
that needs no certification. Every number is a proposal until the owner signs it.

Each chip is cut from 3/8" (9.5) cast sheet and stepped, so it shows a tint at the two depths EARF uses:
- the left 45 mm at the sheet's full 9.5 (Hemisphere's shell, Core's ball, Mantle's base);
- the right 35 mm milled down to 3.2 (Hemisphere's skin).

The tint's name, its sheet code and its light transmission at both depths, measured on the lot, are laser-engraved on
the thick part's front and filled white. The eight stand on edge in the spectrum's order in a routed birch tray, under
a hood of 3 mm Smoke acrylic, with a card of the particulars. For now the chips are cut from stock stand-ins
(`launch/stock-colours.md`, R1); the custom tints replace them later, with the same files.

The frame (mm): the tray's footprint centred on the origin, z up from the table; the chips stand along y.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/tint_library.py --out spinoffs/barkhorn/companions/out-tint-library
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
from kit import Part, Product, Sheet, Machined, Bought             # noqa: E402

# the eight, in the spectrum's order, with today's stock stand-ins (R1; Haze's 1020 to confirm as cast)
TINTS = [('Ember', 'TruCast 2423'), ('Dust', '2422 Amber'), ('Acid', '2208 Yellow'), ('Poison', 'TruCast 9093'),
         ('Ice', '2069 Light Blue'), ('Haze', '1020 Purple'), ('Fog', '3030 Glass Green'), ('Smoke', 'TruCast 2064')]

P = dict(
    L=80.0, H=50.0, T=10.0,         # a chip: long, tall (standing), the sheet's thickness (nominal 10; stock 3/8" is 9.5)
    step_x=5.0, thin=3.2,           # the step: from x = 5 to the right end, milled down to 3.2 from the back
    R=4.0,                          # the chip's corners
    pitch=15.0, slot_t=10.1, slot_l=80.6, slot_d=18.0,    # the tray's slots
    tray=(100.0, 144.0, 28.0),      # the tray, x y z
    hood_t=3.0, hood_gap=0.2, hood_clear=1.5,              # the hood over it
)


def chip(x0, y0, z0):
    """One chip standing on its long edge, its face in x-z, its thickness along y (the step at the back, +y)."""
    from build123d import Box, Pos, fillet, Axis
    L, H, T = P['L'], P['H'], P['T']
    c = Pos(x0, y0, z0 + H / 2) * Box(L, T, H)
    c = fillet(c.edges().filter_by(Axis.Y), P['R'])
    cut = Pos(x0 + (P['step_x'] + L / 2) / 2, y0 + T / 2 - (T - P['thin']) / 2 + 0.001, z0 + H / 2) * \
        Box(L / 2 - P['step_x'] + 0.002, T - P['thin'] + 0.002, H + 2)
    return c - cut


def chips():
    n = len(TINTS)
    y_first = -(n - 1) * P['pitch'] / 2
    z0 = P['tray'][2] - P['slot_d']
    return [chip(0.0, y_first + i * P['pitch'], z0) for i in range(n)]


def tray():
    from build123d import Box, Pos
    X, Y, Z = P['tray']
    t = Pos(0, 0, Z / 2) * Box(X, Y, Z)
    n = len(TINTS)
    y_first = -(n - 1) * P['pitch'] / 2
    for i in range(n):
        t -= Pos(0, y_first + i * P['pitch'], Z - P['slot_d'] / 2 + 0.5) * Box(P['slot_l'], P['slot_t'], P['slot_d'] + 1)
    return t


def hood():
    """Five panels of 3 mm Smoke, bonded: the top over the four walls, the walls standing on the table round the tray."""
    from build123d import Box, Pos
    X, Y, _ = P['tray']
    t, g = P['hood_t'], P['hood_gap']
    top_z = P['tray'][2] - P['slot_d'] + P['H'] + P['hood_clear']       # the chips' tops, and a little air
    ix, iy = X + 2 * g, Y + 2 * g                                         # inside
    ox, oy = ix + 2 * t, iy + 2 * t
    h = top_z                                                             # the walls' height, from the table
    return {
        'hood-top': Pos(0, 0, h + t / 2) * Box(ox, oy, t),
        'hood-front': Pos(0, -(iy + t) / 2, h / 2) * Box(ox, t, h),
        'hood-back': Pos(0, (iy + t) / 2, h / 2) * Box(ox, t, h),
        'hood-left': Pos(-(ix + t) / 2, 0, h / 2) * Box(t, iy, h),
        'hood-right': Pos((ix + t) / 2, 0, h / 2) * Box(t, iy, h),
    }


def parts(P_):
    cs = chips()
    out = [Part(f'chip-{i + 1}', s, Sheet('cast-acrylic', 10, face='-y'), finish='chip', group='chips',
                notes=[f'{name}: {code}, 3/8" (9.5) cast sheet; laser-cut 80 x 50, corners R4, edges diamond- or '
                       'flame-polished; the right 35 milled from the back down to 3.2 (a flat-bottomed pocket, its '
                       'floor polished); the front of the thick part engraved: the name, the code, and LT at 9.5 and '
                       'at 3.2, measured on the lot, filled white (Smoke\'s and Fog\'s filled black)'])
           for i, (s, (name, code)) in enumerate(zip(cs, TINTS))]
    out.append(Part('tray', tray(), Machined('birch-hardwood', 'cnc-mill'), finish='birch', group='case',
                    notes=['solid birch 100 x 144 x 28, eight slots 80.6 x 10.1 x 18 at 15 pitch routed from the top; '
                           'edges eased R1; oiled; four felt pads under it']))
    for k, s in hood().items():
        out.append(Part(k, s, Sheet('acrylic', 3), finish='smoke', group='case',
                        notes=['3 mm Smoke cast acrylic, laser-cut, edges polished; bonded into a hood (the top over '
                               'the four walls, front and back over the sides), the joints clear; the top engraved '
                               'THE TINT LIBRARY, filled white'] if k == 'hood-top' else []))
    out += [
        Part('engrave', None, Bought('tint-chip-engrave'), qty=8),
        Part('chip-step', None, Bought('tint-chip-step'), qty=8),
        Part('card', None, Bought('tint-card')),
        Part('felt', None, Bought('tint-felt')),
        Part('sleeve', None, Bought('tint-mailer')),
    ]
    return out


PRODUCT = Product('tint-library', 'The Tint Library', 'EARF\'s eight tints as stepped chips in a case (a proposal)',
                  params=P, parts=parts, count=1, drawing_prefix='ETL', origin=(0, 0, 0),
                  materials={'chip': {'preset': 'acrylic', 'color': '#B23A28'},
                             'birch': {'preset': 'wood', 'color': '#D8C3A0'},
                             'smoke': {'preset': 'acrylic', 'color': '#6E6A66'}},
                  notes=['A proposal (round 43): idea (f), the Tint Library. For designers and architects specifying '
                         'EARF colours, as the press mailer, and as a product that needs no certification.',
                         'Each chip shows its tint at two depths: 9.5 (shell, ball, base) and 3.2 (skin). Its LT at both '
                         'is measured on the lot with a lux meter and engraved, so the card and the chip agree.',
                         'Stock stand-ins now (TruCast 2423, 2422, 2208, 9093, 2069, 1020, 3030, 2064); the custom '
                         'tints later, the same files.'])
