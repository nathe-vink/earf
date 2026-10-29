"""Moon, EARF's bar lamps (round 32, family F3 of bar_lamps.py, recommended): a cordless table lamp and a pendant in the
line's tints (the eight Tropos colours, and clear, frosted and smoked), for Planet EARF and for sale.

The table lamp: a frosted dome turned from cast acrylic over a solid tinted column, on a weighted blackened-steel
foot. The light is a warm-dim LED board on a brass hub at the column's top, facing up into the dome, so a seated guest
looking down on it sees only the lit frost; a small ring of LEDs in the foot lights the column from below, so its
polished top glows (the signature: light carried through thick acrylic). The battery and the board are sealed in the
foot; it charges on a staff tray through two gold rings underneath (or USB-C); a touch on the brass finial dims it,
2200 to 2700 K. 120 across, 273 tall, about 1.9 kg.

The pendant: a frosted dome 200 across, turned from cast acrylic, hung mouth down under a 20 mm tinted disc whose
polished edge glows, a brass hub between them holding a COB recessed for a cut-off, the driver in a brass canopy.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/moon_table.py --out spinoffs/barkhorn/companions/out-moon-table
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/moon_pendant.py --out spinoffs/barkhorn/companions/out-moon-pendant

The frame: x across, y back, z up from the table (the table lamp) or from the dome's rim (the pendant), mm.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
sys.path.insert(0, HERE)
from kit import *                                                   # noqa: E402,F403
import bar_lamps as B                                               # noqa: E402

MATERIALS = dict(B.MATERIALS, led={'preset': 'emit', 'color': '#FFC890', 'strength': 0.0},
                 silicone={'preset': 'rubber', 'color': '#1A1A1A'}, gold={'preset': 'metal', 'color': '#D8B45A', 'roughness': 0.2})
VARIANTS = B.VARIANTS

T = dict(foot=(120.0, 22.0), col=(40.0, 8.0), col_top=187.0, hub=(52.0, 26.0), dome_r=75.0, dome_t=6.0, finial=(22.0, 10.0))
P = dict(dome_r=100.0, dome_t=7.0, disc=(220.0, 20.0), hub=(80.0, 34.0), canopy=(150.0, 50.0), drop=600.0)

# where each lamp's light sits (mm, in its own frame): the shots and Planet's kit piece put a hidden lamp there
TABLE_LIGHT = (0.0, 0.0, 222.0)
PENDANT_LIGHT = (0.0, 0.0, 70.0)


def eased(d, z0, z1, e, top=True, bottom=True):
    from build123d import fillet, Axis
    s = cyl('z', (0, 0), d, z0, z1)
    fs = s.faces().sort_by(Axis.Z)
    es = (fs[0].edges() if bottom else []) + (fs[-1].edges() if top else [])
    return fillet(es, e) if es else s


def dome_shell(R, t, z_rim, up=True):
    """A hemispherical shell R outside, t thick, its rim at z_rim, crown up (mouth down), its rim rounded."""
    from build123d import Sphere, Pos
    s = (Sphere(R) - Sphere(R - t)) - box(-R - 1, -R - 1, -R - 1, R + 1, R + 1, 0)
    return Pos(0, 0, z_rim) * s


def table_parts(p=T):
    from build123d import Pos
    fd, fh = p['foot']
    cd, cb = p['col']
    zt = p['col_top']
    hd, hh = p['hub']
    R, t = p['dome_r'], p['dome_t']
    z_rim = zt + 6.0                                    # the dome's rim just above the hub's base
    # the foot: blackened steel, a pocket 100 x 14 from the top for the battery and the board, the column's socket 24
    # deep, a 2 mm recess underneath for the silicone ring and the two gold contact rings
    foot = eased(fd, 0, fh, 3.0) - cyl('z', (0, 0), 100, 6, fh + 1) \
        - (cyl('z', (0, 0), 112, -1, 2) - cyl('z', (0, 0), 106, -2, 3)) - (cyl('z', (0, 0), 61, -1, 2) - cyl('z', (0, 0), 53, -2, 3))
    lid = cyl('z', (0, 0), 100, fh - 4, fh) - cyl('z', (0, 0), cd + 0.2, fh - 5, fh + 1)
    pack = box(-34, -19, 7, 34, 19, 16.5)                # two 18650s side by side
    board = cyl('z', (0, 0), 92, 16.6, 18.0) - cyl('z', (0, 0), 30, 16, 19)
    col = eased(cd, fh - 4, zt, 1.5, bottom=False) - cyl('z', (0, 0), cb, fh - 5, zt + 1)
    hub = eased(hd, zt, zt + hh, 2.0, bottom=False) - cyl('z', (0, 0), cb, zt - 1, zt + 6)
    led = cyl('z', (0, 0), 30, zt + hh, zt + hh + 1.6)
    rod = cyl('z', (0, 0), 6, zt + hh + 1.6, z_rim + R - t)
    dome = dome_shell(R, t, z_rim)
    fin_d, fin_h = p['finial']
    finial = eased(fin_d, z_rim + R - 0.5, z_rim + R - 0.5 + fin_h, 2.5, bottom=False)
    ring = cyl('z', (0, 0), 111.6, 0.2, 2) - cyl('z', (0, 0), 106.4, 0, 3)
    contacts = cyl('z', (0, 0), 60, 0.4, 1.6) - cyl('z', (0, 0), 54, 0, 2)
    return [
        Part('foot', foot, Machined('steel', 'lathe'), finish='steel', group='foot',
             notes=['mild steel, blackened (hot-blackened and waxed, or black e-coat for wiping); its weight keeps the lamp '
                    'down: about 1.5 kg']),
        Part('lid', lid, Machined('steel', 'lathe'), finish='steel', group='foot', inside=True,
             notes=['closes the pocket on an O-ring; the column passes through it']),
        Part('battery', pack, Bought('moon-battery'), finish='steel', group='foot', inside=True, render=False),
        Part('board', board, Bought('moon-board'), finish='steel', group='foot', inside=True, render=False),
        Part('column', col, Machined('cast-acrylic', 'lathe'), finish='body', group='column',
             notes=['cast acrylic rod 40 in the colour, turned, its 8 bore reamed and its outside and top polished; lit '
                    'from below by four LEDs in the lid, so its polished top edge glows']),
        Part('hub', hub, Machined('brass', 'lathe'), finish='brass', group='light',
             notes=['brass, satin; the LED board on its top face, facing up into the dome, its heat into the brass']),
        Part('led', led, Bought('moon-led-table'), finish='led', group='light'),
        Part('rod', rod, Machined('brass', 'lathe'), finish='brass', group='light', inside=True,
             notes=['M6 brass, the dome screwed down on it by the finial; the touch electrode']),
        Part('dome', dome, Machined('cast-acrylic', 'lathe', setup_usd=120.0), finish='shade', group='shade',
             notes=['turned from cast block in the colour, 6 wall, its inside bead-blasted satin and its outside honed: a '
                    'frosted dome; its rim polished and eased']),
        Part('finial', finial, Machined('brass', 'lathe'), finish='brass', group='shade',
             notes=['the touch: tap to switch, hold to dim']),
        Part('foot-ring', ring, Bought('moon-seals'), finish='silicone', group='foot'),
        Part('contacts', contacts, Bought('moon-contacts'), finish='gold', group='foot'),
    ]


def pendant_parts(p=P):
    R, t = p['dome_r'], p['dome_t']
    dd, dt = p['disc']
    hd, hh = p['hub']
    cd, ch = p['canopy']
    z_top = R                                            # the dome's crown, under the disc
    dome = dome_shell(R, t, 0.0) - cyl('z', (0, 0), hd + 0.4, R - 30, R + 1)
    disc = eased(dd, z_top, z_top + dt, 2.0) - cyl('z', (0, 0), 12, z_top - 1, z_top + dt + 1)
    hub = cyl('z', (0, 0), hd, z_top - hh, z_top) - cyl('z', (0, 0), 46, z_top - hh - 1, z_top - hh + 22)
    cob = cyl('z', (0, 0), 28, z_top - hh + 20, z_top - hh + 22)
    cap = eased(40, z_top + dt, z_top + dt + 14, 2.0, bottom=False)
    cord = cyl('z', (0, 0), 6, z_top + dt + 14, z_top + dt + p['drop'])
    canopy = eased(cd, z_top + dt + p['drop'], z_top + dt + p['drop'] + ch, 3.0, top=False) \
        - cyl('z', (0, 0), cd - 6, z_top + dt + p['drop'] + 3, z_top + dt + p['drop'] + ch + 1)
    driver = box(-42, -28.5, z_top + dt + p['drop'] + 6, 42, 28.5, z_top + dt + p['drop'] + 6 + 29.5)
    return [
        Part('dome', dome, Machined('cast-acrylic', 'lathe', setup_usd=160.0), finish='shade', group='shade',
             notes=['turned from cast block in the colour, 7 wall, frosted inside and out, its rim polished and eased']),
        Part('disc', disc, Sheet('cast-acrylic', 20), finish='body', group='shade',
             notes=['20 mm cast sheet in the colour, its edge eased R2 and polished: lit from the dome below through its '
                    'polished underside, it glows at its edge']),
        Part('hub', hub, Machined('brass', 'lathe'), finish='brass', group='light',
             notes=['brass, satin, its 46 bore 22 deep a baffle: the COB sits 22 up inside it, so from below a seated '
                    'guest sees the frost, not the source (cut-off about 46 deg from the vertical)']),
        Part('cob', cob, Bought('moon-cob'), finish='led', group='light', inside=True),
        Part('cap', cap, Machined('brass', 'lathe'), finish='brass', group='light',
             notes=['clamps the disc to the hub through its 12 hole; the cord grip']),
        Part('cord', cord, Bought('moon-cord'), finish='cord'),
        Part('canopy', canopy, Machined('brass', 'lathe'), finish='brass', group='canopy',
             notes=['150 x 50, brass, satin (or blackened steel); holds the driver and the junction box strap']),
        Part('driver', driver, Bought('moon-driver'), finish='steel', group='canopy', inside=True, render=False),
        Part('listing', None, Bought('moon-listing')),
    ]


NOTES_TABLE = [
    'Cordless: two 18650 cells (25 Wh) sealed in the foot; about 12 hours at the bar setting (2 W), 6 at full; charged '
    'on the staff tray through two gold rings underneath, or by USB-C (its plug rubber-sealed).',
    'No LED in sight: the board faces up inside the frosted dome, under a seated guest\'s eye line; a touch on the '
    'brass finial switches it, holding dims it, 2200 to 2700 K as it dims (two channels mixed).',
    'Splash-proof (IP44): the foot sealed by the lid\'s O-ring and the column\'s; nothing on top where a drink can pool '
    '(the dome sheds, the finial is round). Wipe with a damp cloth; no solvents on the acrylic.',
    'The acrylic: the column a 40 rod and the dome turned from cast block, both in the colour (the eight Tropos '
    'tints, clear, frosted, smoked); polished where it shows an edge, the dome frosted; never thin sheet.',
]
NOTES_PENDANT = [
    'Mains: a Mean Well PCD-16-700B (phase-cut dimmable, UL8750 Class 2) in the canopy driving a 2700 K CRI 90 COB in '
    'the brass hub; the whole to be listed (UL 1598) as a fixture.',
    'Cut-off: the COB sits 22 mm up a 46 bore in the hub, so seated guests see the lit frost, not the source.',
    'Hang over a bar at 750 to 900 mm centres, the dome\'s rim 700 to 800 above the counter; over a booth, one per '
    'table, the rim about 650 above it.',
]
TOUCHING_TABLE = [('finial', 'dome'), ('rod', 'hub'), ('rod', 'finial')]
TOUCHING_PENDANT = [('cap', 'disc')]
