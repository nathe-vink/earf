"""Round 32d, the bar lamps the owner picked from the shape study (2026-10-19: "I like the dome overhead lights,
especially if the acrylic covers are easy to swap out, but I'm also a sucker for the spheres. For the table lamp
though, I'd want the spheres to be squatted rather than raised, like a crystal ball."). Two products, the frost set
within the acrylic as in round 32c (study.py): tint, frost, tint; nothing white outside.

Dome, the pendant. A tinted dome 200 across is a cover that comes off by hand. A brass collar is bonded into its crown,
and three L-slots in the collar take three pins on the fixture's brass hub: a quarter-turn bayonet (30 degrees here).
Lifted 5 mm, turned and lowered, the cover hangs with each pin up in a notch at the end of its slot, so its own weight
locks it. It can't turn out unless it is first pushed up, and a spring plunger in the hub clicks into a dimple in the
collar as a detent. The COB (2700 K, recessed 22 up a 46 bore: a cut-off about 46 deg from the vertical), the hub, the
cord and the driver in the canopy stay on the fixture, so a cover is never a live part and the listing (UL 1598) covers
the fixture with any cover. The covers are sold on their own in every tint.

Orb, the table lamp. A tinted ball 160 across, a crystal ball, sits low in the cup of a short base: a blackened-steel
drum 120 across with a brass ring at its top that is the touch (tap to switch, hold to dim, 2200 to 2700 K). The
battery, the board and the LED stay sealed in the base (IP44, as Moon's foot), and the LED shines up through a sealed
window into a port in the ball's underside. So the ball is a cover too: it lifts off, and Orbs swap colour as the Domes
do. It rests on a silicone ring in the cup, 18 deep, which is enough to stop a nudge rolling it. It charges on the
staff tray through gold rings underneath (or USB-C).

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/dome_pendant.py --out spinoffs/barkhorn/companions/out-dome-pendant
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/orb_table.py --out spinoffs/barkhorn/companions/out-orb-table

The frame: x across, y back, z up from the dome's rim (the pendant) or from the table (the Orb), mm.
"""
import copy, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
sys.path.insert(0, HERE)
from kit import *                                                   # noqa: E402,F403
import bar_lamps as B                                               # noqa: E402

# the tint carries the glow (study.py): cast denser than the Clouds' 25 mm, as these walls are 9 to 15 mm; smoked
# lighter, or it goes black
MATERIALS = dict(B.MATERIALS,
                 body={'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.005, 'roughness': 0.04},
                 # mostly rough transmission (clear 0.85): bead-blasted acrylic 2.5 thick passes most light diffusely; at
                 # the preset's 0.1 it rendered as opal and turned the unlit Smoke ball solid black (round 32e)
                 liner={'preset': 'frosted', 'color': '#F4F2EE', 'absorb': '#EFE6D8', 'roughness': 0.5, 'radius': 0.02,
                        'clear': 0.85, 'glow': 0.25, 'glow_color': '#FF9A50'},
                 led={'preset': 'emit', 'color': '#FFC890', 'strength': 0.0},
                 window={'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#F4F2EE', 'radius': 0.05, 'roughness': 0.2},
                 silicone={'preset': 'rubber', 'color': '#1A1A1A'},
                 gold={'preset': 'metal', 'color': '#D8B45A', 'roughness': 0.2})
VARIANTS = copy.deepcopy(B.VARIANTS)
VARIANTS['smoked'].setdefault('materials', {})['body'] = {'radius': 0.0055}     # 0.008 read cream, not smoke (critic p2)
VARIANTS['smoke'].setdefault('materials', {})['body'] = {'radius': 0.012}       # Smoke at 0.005 read black (round 32e)

GAP, LT, SKIN = 1.0, 2.5, 3.0          # the liner 1 mm in from the shell, 2.5 thick; the inner skin 3

D = dict(R=100.0, shell=9.0, collar=(92.4, 82.0, 70.0, 104.0), hub=(80.0, 62.0, 112.0), bore=(46.0, 84.0),
         pin_z=97.0, turn=30.0, drop=600.0, canopy=(150.0, 50.0))
O = dict(R=80.0, shell=9.0, base=(120.0, 30.0), ring=8.0, rim_r=50.0, port=40.0)

DOME_LIGHT = (0.0, 0.0, 74.0)
ORB_LIGHT = None                       # set below from the ball's centre


def ball(R, t, c, cut_below=None):
    """A spherical shell R outside, t thick, centred at c, cut flat below z = cut_below."""
    from build123d import Sphere, Pos
    s = Pos(*c) * (Sphere(R) - Sphere(R - t))
    if cut_below is not None:
        s = s - box(-R - 1, -R - 1, c[2] - R - 1, R + 1, R + 1, cut_below)
    return s


def at(deg, solid):
    from build123d import Rot
    return Rot(0, 0, deg) * solid


def sector(r0, r1, a0, a1, z0, z1, n=12):
    """An annular sector, radii r0..r1, from a0 to a1 degrees, z0..z1."""
    pts = [(r1 * math.cos(math.radians(a0 + (a1 - a0) * i / n)), r1 * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
           for i in range(n + 1)]
    pts += [(r0 * math.cos(math.radians(a1 - (a1 - a0) * i / n)), r0 * math.sin(math.radians(a1 - (a1 - a0) * i / n)))
            for i in range(n + 1)]
    return prism(pts, 'z', z0, z1)


# --- Dome, the pendant ---------------------------------------------------------------------------------------------
def dome_parts(p=D):
    R, t = p['R'], p['shell']
    co, ci, cz0, cz1 = p['collar']
    hd, hz0, hz1 = p['hub']
    bd, bz = p['bore']
    cd, ch = p['canopy']
    r_shell_in = R - t
    r_liner = r_shell_in - GAP
    r_skin = r_liner - LT - GAP
    hole = cyl('z', (0, 0), co, cz0 - 20, R + 5)
    shell = ball(R, t, (0, 0, 0), cut_below=0) - hole
    liner = ball(r_liner, LT, (0, 0, 0), cut_below=4) - hole
    skin = ball(r_skin, SKIN, (0, 0, 0), cut_below=0) - hole
    rim = cyl('z', (0, 0), 2 * (r_shell_in - 0.2), 0, 3.8) - cyl('z', (0, 0), 2 * (r_skin + 0.2), -1, 5)
    # the collar: bonded into the crown; three L-slots (down from its top, round 30 deg, up into a notch)
    collar = cyl('z', (0, 0), co - 0.4, cz0, cz1) - cyl('z', (0, 0), ci, cz0 - 1, cz1 + 1)
    pz, w = p['pin_z'], 5.0
    for a in (0, 120, 240):
        collar = collar - at(a, box(ci / 2 - 2, -w / 2, pz - 10.5, co / 2 + 2, w / 2, cz1 + 1))          # the entry
        collar = collar - sector(ci / 2 - 2, co / 2 + 2, a, a + p['turn'], pz - 10.5, pz - 5.5)          # the turn
        collar = collar - at(a + p['turn'], box(ci / 2 - 2, -w / 2, pz - 10.5, co / 2 + 2, w / 2, pz + 2.5))  # the notch
    hub = cyl('z', (0, 0), hd, hz0, hz1) - cyl('z', (0, 0), bd, hz0 - 1, bz)
    pins = None
    for a in (0, 120, 240):
        pin = at(a + p['turn'], cyl('x', (0, pz), 4.0, hd / 2 - 1, ci / 2 + 2.5))
        pins = pin if pins is None else pins + pin
    cob = cyl('z', (0, 0), 28, bz - 2, bz)
    gland = cyl('z', (0, 0), 40, hz1, hz1 + 14)
    z_cord = hz1 + 14
    cord = cyl('z', (0, 0), 6, z_cord, z_cord + p['drop'])
    zc = z_cord + p['drop']
    canopy = cyl('z', (0, 0), cd, zc, zc + ch) - cyl('z', (0, 0), cd - 6, zc - 1, zc + ch - 3)
    driver = box(-42, -28.5, zc + 6, 42, 28.5, zc + 6 + 29.5)
    return [
        Part('shell', shell, Machined('cast-acrylic', 'lathe', setup_usd=160.0), finish='body', group='cover',
             notes=['the cover\'s outside: turned from cast block in the tint, 9 wall, polished inside and out']),
        Part('liner', liner, Machined('cast-acrylic', 'lathe', setup_usd=120.0), finish='liner', group='cover', inside=True,
             notes=['the diffuser: a 2.5 cup turned in clear, bead-blasted both faces, bonded between the shell and the '
                    'skin (or cast into the block: ask the caster)']),
        Part('skin', skin, Machined('cast-acrylic', 'lathe', setup_usd=120.0), finish='body', group='cover',
             notes=['the cover\'s inside: a 3 cup in the tint, polished, so the frost is seen only through acrylic']),
        Part('rim', rim, Machined('cast-acrylic', 'lathe'), finish='body', group='cover',
             notes=['closes the three layers at the mouth, bonded and polished with them']),
        Part('collar', collar, Machined('brass', 'mill'), finish='brass', group='cover',
             notes=['brass, satin: bonded into the crown; three L-slots, a quarter-turn bayonet (30 deg); the cover lifts '
                    '5, turns and drops, its weight holding each pin up in its notch']),
        Part('hub', hub, Machined('brass', 'lathe'), finish='brass', group='fixture',
             notes=['brass, satin: the COB 22 up its 46 bore (the cut-off), the pins pressed in, the spring plunger '
                    'the detent; the heat into the brass']),
        Part('pins', pins, Bought('dome-pins'), finish='brass', group='fixture'),
        Part('cob', cob, Bought('moon-cob'), finish='led', group='fixture', inside=True),
        Part('gland', gland, Machined('brass', 'lathe'), finish='brass', group='fixture',
             notes=['the cord grip and strain relief, screwed into the hub']),
        Part('cord', cord, Bought('moon-cord'), finish='cord', group='fixture'),
        Part('canopy', canopy, Machined('brass', 'lathe'), finish='brass', group='canopy',
             notes=['150 x 50, brass (or blackened steel): the driver and the junction-box strap']),
        Part('driver', driver, Bought('moon-driver'), finish='steel', group='canopy', inside=True, render=False),
        Part('plunger', None, Bought('dome-plunger')),
        Part('listing', None, Bought('moon-listing')),
    ]


# --- Orb, the table lamp -------------------------------------------------------------------------------------------
def orb_geometry(p=O):
    R = p['R']
    bd, bh = p['base']
    z_top = bh + p['ring']
    zc = z_top + math.sqrt(R * R - p['rim_r'] ** 2)          # the ball rests at the cup's rim radius
    return R, bd, bh, z_top, zc


def orb_parts(p=O):
    from build123d import Sphere, Pos
    R, bd, bh, z_top, zc = orb_geometry(p)
    cup = Pos(0, 0, zc) * Sphere(R + 0.5)
    t = p['shell']
    r_liner = R - t - GAP
    r_skin = r_liner - LT - GAP
    port = cyl('z', (0, 0), p['port'], zc - R - 5, zc - R + 25)
    shell = ball(R, t, (0, 0, zc)) - port
    liner = ball(r_liner, LT, (0, 0, zc)) - cyl('z', (0, 0), p['port'] + 8, zc - R - 5, zc - R + 25)
    skin = ball(r_skin, SKIN, (0, 0, zc)) - port
    # the ring that lines the port and closes the layers there: brass, bonded
    gz0 = zc - math.sqrt(R ** 2 - (p['port'] / 2) ** 2)
    gz1 = zc - math.sqrt((r_skin - SKIN) ** 2 - (p['port'] / 2) ** 2)
    grommet = cyl('z', (0, 0), p['port'] - 0.4, gz0, gz1) - cyl('z', (0, 0), p['port'] - 6, gz0 - 1, gz1 + 1)
    # the base: a blackened-steel drum, its pocket (the battery and the board) closed from below by a plate; the cup's
    # floor carries a sealed window over the LED; a brass touch ring on top, the cup through both
    base = eased(bd, 0, bh, 3.0, top=False) - cyl('z', (0, 0), 100, -1, 16) - cup - cyl('z', (0, 0), 30, 15, bh)
    plate = cyl('z', (0, 0), 99.6, 0.4, 4) \
        - (cyl('z', (0, 0), 61, -1, 2) - cyl('z', (0, 0), 53, -2, 3))
    ring = eased(bd, bh, z_top, 2.0, bottom=False) - cup
    window = cyl('z', (0, 0), 29.6, 16.2, zc - math.sqrt((R + 0.5) ** 2 - 15 ** 2) - 0.3)
    pack = box(-34, -19, 4.2, 34, 19, 13.5)
    board = cyl('z', (0, 0), 92, 13.6, 15.0) - cyl('z', (0, 0), 34, 13, 16)
    led = cyl('z', (0, 0), 26, 14.0, 15.6)
    # the seat: a silicone ring in the cup under the ball (its top just under the ball's surface)
    zs = zc - math.sqrt(R ** 2 - 42 ** 2) - 0.3
    seat = cyl('z', (0, 0), 92, zs - 1.5, zs) - cyl('z', (0, 0), 84, zs - 2, zs + 1)
    contacts = cyl('z', (0, 0), 60, 0.4, 1.6) - cyl('z', (0, 0), 54, 0, 2)
    foot = cyl('z', (0, 0), 111.6, 0.2, 2) - cyl('z', (0, 0), 106.4, 0, 3)
    base = base - (cyl('z', (0, 0), 112, -1, 2) - cyl('z', (0, 0), 106, -2, 3)) - cyl('z', (0, 0), 92.4, zs - 2, zs + 0.01)
    ring = ring - (cyl('z', (0, 0), 92.4, zs - 2, zs + 0.01) - cyl('z', (0, 0), 83.6, zs - 3, zs + 1))     # the seat's groove
    return [
        Part('shell', shell, Machined('cast-acrylic', 'lathe', setup_usd=160.0), finish='body', group='ball',
             notes=['the ball\'s outside: two hemispheres turned from cast block in the tint, 9 wall, bonded at the equator '
                    'and polished (or rotationally cast: ask the caster); a 40 port at its underside']),
        Part('liner', liner, Machined('cast-acrylic', 'lathe', setup_usd=120.0), finish='liner', group='ball', inside=True,
             notes=['the diffuser: a 2.5 ball in clear, bead-blasted, in two halves inside the shell']),
        Part('skin', skin, Machined('cast-acrylic', 'lathe', setup_usd=120.0), finish='body', group='ball', inside=True,
             notes=['a 3 ball in the tint inside the liner: seen through the port, the frost is still behind acrylic']),
        Part('grommet', grommet, Machined('brass', 'lathe'), finish='brass', group='ball',
             notes=['lines the port and closes the three layers there, bonded']),
        Part('base', base, Machined('steel', 'lathe'), finish='steel', group='base',
             notes=['mild steel, blackened and waxed (or black e-coat): 120 x 30, its weight with the ball\'s about 3.2 kg; '
                    'the cup turned in it and the ring together']),
        Part('ring', ring, Machined('brass', 'lathe'), finish='brass', group='base',
             notes=['brass, satin, insulated from the base: the touch (tap to switch, hold to dim, 2200 to 2700 K)']),
        Part('window', window, Machined('cast-acrylic', 'lathe'), finish='window', group='base',
             notes=['a clear acrylic plug, sealed with an O-ring: the LED under it, the base IP44 with the ball off']),
        Part('plate', plate, Machined('steel', 'lathe'), finish='steel', group='base', inside=True,
             notes=['closes the pocket from below on an O-ring; the gold contact rings on it']),
        Part('battery', pack, Bought('moon-battery'), finish='steel', group='base', inside=True, render=False),
        Part('board', board, Bought('moon-board'), finish='steel', group='base', inside=True, render=False),
        Part('led', led, Bought('moon-led-table'), finish='led', group='base', inside=True),
        Part('seat', seat, Bought('orb-seat'), finish='silicone', group='base'),
        Part('foot-ring', foot, Bought('moon-seals'), finish='silicone', group='base'),
        Part('contacts', contacts, Bought('moon-contacts'), finish='gold', group='base'),
    ]


def eased(d, z0, z1, e, top=True, bottom=True):
    from build123d import fillet, Axis
    s = cyl('z', (0, 0), d, z0, z1)
    fs = s.faces().sort_by(Axis.Z)
    es = (fs[0].edges() if bottom else []) + (fs[-1].edges() if top else [])
    return fillet(es, e) if es else s


_R, _bd, _bh, _zt, _zc = orb_geometry()
ORB_LIGHT = (0.0, 0.0, round(_zc, 1))           # at the centre: 30 below drew a crescent in the frost (critic p2)
ORB_SIZE = dict(ball=2 * _R, height=round(_zc + _R, 1), base=_bd)

NOTES_DOME = [
    'The covers swap by hand: lift the dome 5 mm, turn it 30 degrees and lower it off. To fit one, line up the three '
    'slots, push up, turn until the plunger clicks, and let go: its weight holds each pin up in its notch, so a knock '
    'cannot turn it off. No tools, and the cover is never live (the COB, hub and driver stay up).',
    'The wall is tint, frost, tint: a 9 mm tinted shell, a 2.5 mm frosted liner, a 3 mm tinted skin, closed at the '
    'mouth by a tinted rim. Nothing white is seen, from any side.',
    'Mains: Mean Well PCD-16-700B (phase-cut dimmable, UL8750 Class 2) in the canopy, a 2700 K CRI 90 COB 22 mm up the '
    'hub\'s 46 bore (cut-off about 46 deg); the fixture listed to UL 1598 with any cover.',
    'Hang over a bar at 750 to 900 centres, the rim 700 to 800 above the counter; over a booth, one a table, about 650.',
]
NOTES_ORB = [
    'A crystal ball: a 160 tinted ball, low in the cup of a 120 x 38 base. The ball lifts off: the LED is under a '
    'sealed window in the base, so balls swap colour by hand, as the Dome\'s covers do.',
    'Cordless: two 18650 cells (25 Wh) sealed in the base, about 12 hours at the bar setting; it charges on the staff '
    'tray through two gold rings underneath, or by USB-C. Touch the brass ring: tap to switch, hold to dim, 2200 to '
    '2700 K as it dims.',
    'IP44: the base sealed by the window\'s and the plate\'s O-rings; with the ball on or off. Wipe with a damp cloth.',
    'The ball\'s wall is tint, frost, tint, as the Dome\'s: the port underneath is lined in brass, and through it the '
    'frost is still behind acrylic.',
]
TOUCHING_DOME = [('collar', 'shell'), ('collar', 'liner'), ('collar', 'skin'), ('pins', 'hub'), ('pins', 'collar'),
                 ('cob', 'hub'), ('gland', 'hub'), ('rim', 'shell'), ('rim', 'skin'), ('rim', 'liner')]
TOUCHING_ORB = [('grommet', 'shell'), ('grommet', 'liner'), ('grommet', 'skin'), ('window', 'base'),
                ('seat', 'base'), ('ring', 'base'), ('led', 'board')]
