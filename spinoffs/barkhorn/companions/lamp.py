"""Bell, EARF's lamp (round 31; the owner: "Record player and lighting for one. All acrylic."), concept L3b of
concepts.py, picked: the Clouds' horn flare hung mouth down over a table, the light at its throat where the speaker's
compression driver sits. The speaker plays sound out of its horn; this one plays light.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/lamp.py \
        --out spinoffs/barkhorn/companions/out-lamp

- **The shade** is formed from 5 mm sheet of the Clouds' cast acrylic, tinted four times as dense so that 5 mm
  reads as the cabinets' 20 mm do, over a turned buck (vacuum or drape
  formed, about 160 C), a flat collar at its crown and the flare opening late to a rolled rim 420 across, as the
  waveguide's does. Light crosses its wall at a slant, so it glows in its colour and deepens toward the rim.
- **The light** is 0.4 m of 24 V, 95 CRI LED strip that dims warm (2700 K to about 2000 K), two turns round a turned
  aluminium hub that is also its heat sink, behind an opal acrylic sleeve: about 600 lm at full, 6 W or so. Low
  voltage throughout: a listed 24 V wall adapter, a clear cord, a PWM dimmer in the foot.
- **The foot** is two 20 mm discs, 230 and 200, cemented; the dimmer's board in a pocket through the lower, closed by
  a 6 mm cover; its knob, turned from the deeper colour, on top at the front: turned like a volume knob, which it
  nearly is.
- **The stem** is a cast acrylic tube 30 x 3, the cord showing up it.

The frame is the kit's: x across, y back from the front, z up from the table.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
sys.path.insert(0, HERE)
from kit import *                                                   # noqa: E402,F403
import common as C                                                  # noqa: E402

P = dict(
    T=20.0,
    foot=(230.0, 200.0), bumpon=5.0,
    stem=(30.0, 24.0),                 # the tube, outside and bore
    top=480.0,                         # the cap's top above the table
    cap=(104.0, 8.0), flange=(100.0, 6.0), hub=(64.0, 40.0),
    collar=(20.0, 62.0),               # the shade's flat collar, inner and outer radius
    shade_t=5.0, mouth_r=210.0, drop=180.0, m=2.6, corner=10.0,
    sleeve=(84.0, 78.0, 55.0),         # opal tube: outside, bore, length below the flange
    pocket=(50.0, 96.0), knob=(28.0, 16.0), knob_y=-62.0,
)


def eased_disc(cx, cy, d, z0, z1, ease, bottom=True, top=True):
    from build123d import fillet, Axis
    s = cyl('z', (cx, cy), d, z0, z1)
    fs = s.faces().sort_by(Axis.Z)
    es = (fs[0].edges() if bottom else []) + (fs[-1].edges() if top else [])
    return fillet(es, ease) if es else s


def shade_curve(P, zc):
    """The shade's inner face as (r, z): the collar's underside out from its hole, a R10 corner, the flare down to
    the mouth."""
    r_in, r_out = P['collar']
    rc = P['corner']
    pts = [(r_in, zc), (r_out - rc, zc)]
    fl = C.flare(r_out, P['mouth_r'], P['drop'], n=26, m=P['m'])
    a_end = math.atan2(fl[1][0] - fl[0][0], fl[1][1] - fl[0][1])          # the flare's start, off vertical
    turn = math.pi / 2 - abs(a_end)
    corner = [(r_out - rc + rc * math.sin(turn * k / 4), zc - rc + rc * math.cos(turn * k / 4)) for k in range(1, 5)]
    z_top = corner[-1][1]
    r_shift = corner[-1][0] - r_out
    flare = [(r + r_shift, z_top - h) for r, h in fl[1:]]
    return pts + corner + flare, 1


def parts(P):
    from build123d import Pos
    c = (P['mouth_r'] + 6.0, P['mouth_r'] + 6.0)
    T, b = P['T'], P['bumpon']
    za, zb, zc0 = b, b + T, b + 2 * T                                     # the foot's faces
    so, si = P['stem']
    top = P['top']
    cap_d, cap_t = P['cap']; fl_d, fl_t = P['flange']; hub_d, hub_h = P['hub']
    z_collar_top = top - cap_t
    zc = z_collar_top - P['shade_t']                                       # the collar's underside: the flange's top
    z_fl0 = zc - fl_t
    z_hub0 = z_fl0 - hub_h
    pw, pl = P['pocket']
    ky = c[1] + P['knob_y']

    # the foot: the lower disc with the pocket through it (its corners R6) and the cover's recess (140 x 6) and the
    # cord's groove (10 x 6 to the back) from below; the upper with the stem's socket (12 deep), the cord's hole down
    # to the pocket, the pocket's top 8 deep from below and the knob's shaft hole
    from build123d import BuildSketch, RectangleRounded, Locations, Plane, extrude
    def rrect_z(cx, cy, w, l, r, z0, z1):
        with BuildSketch() as sk:
            with Locations((cx, cy)):
                RectangleRounded(w, l, r)
        return extrude(Plane.XY.offset(z0) * sk.sketch, z1 - z0)
    pcy = c[1] + (P['knob_y'] - 18 + 16) / 2                                  # the pocket from under the knob to past the stem
    lower = cyl('z', c, P['foot'][0], za, zb) - rrect_z(c[0], pcy, pw, pl, 6, za - 1, zb + 1) \
        - cyl('z', c, 140.0, za - 1, za + 6) - box(c[0] - 5, pcy, za - 1, c[0] + 5, c[1] + P['foot'][0] / 2 + 1, za + 11)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        lower = lower - cyl('z', (c[0] + 60 * math.cos(a), c[1] + 60 * math.sin(a)), 4.5, za + 6 - 0.01, za + 14)
    upper = cyl('z', c, P['foot'][1], zb, zc0) - cyl('z', c, so + 0.4, zc0 - 12, zc0 + 1) - cyl('z', c, 10.0, zb - 1, zc0) \
        - rrect_z(c[0], pcy, pw, pl, 6, zb - 1, zb + 8) - cyl('z', (c[0], ky), 7.0, zb - 1, zc0 + 1)
    stack = eased_disc(c[0], c[1], P['foot'][0], za, zb, 2.0, top=False) + eased_disc(c[0], c[1], P['foot'][1], zb, zc0, 2.0, bottom=False)
    stack = stack - cyl('z', c, so + 0.4, zc0 - 12, zc0 + 1) - rrect_z(c[0], pcy, pw, pl, 6, za - 1, zb + 8) - cyl('z', c, 140.0, za - 1, za + 6)
    cover = cyl('z', c, 139.6, za, za + 6)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        cover = cover - cyl('z', (c[0] + 60 * math.cos(a), c[1] + 60 * math.sin(a)), 3.4, za - 1, za + 7)

    stem_z0, stem_z1 = zc0 - 12, z_hub0 + 15
    stem = cyl('z', c, so, stem_z0, stem_z1) - cyl('z', c, si, stem_z0 - 1, stem_z1 + 1)

    # the hub: the band the strip wraps (64), the flange the collar sits on (100 x 6) with its locating spigot (38 x 5)
    # up through the collar's hole, the stem's bore (30.4 x 15) and the cord's way up; three M4 holes for the cap
    hub = cyl('z', c, hub_d, z_hub0, z_fl0) + cyl('z', c, fl_d, z_fl0, zc) + cyl('z', c, 2 * P['collar'][0] - 0.4, zc, zc + P['shade_t'])
    hub = hub - cyl('z', c, so + 0.4, z_hub0 - 1, z_hub0 + 15) - cyl('z', c, 8.0, z_hub0 + 14, z_fl0 - 6)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        hub = hub - cyl('z', (c[0] + 44 * math.cos(a), c[1] + 44 * math.sin(a)), 3.3, z_fl0 - 4, zc + 0.01)
    cap = eased_disc(c[0], c[1], cap_d, z_collar_top, top, 2.5, bottom=False)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        cap = cap - cyl('z', (c[0] + 44 * math.cos(a), c[1] + 44 * math.sin(a)), 4.5, z_collar_top - 1, top + 1) \
            - cyl('z', (c[0] + 44 * math.cos(a), c[1] + 44 * math.sin(a)), 8.0, top - 3, top + 1)

    curve, _ = shade_curve(P, zc)
    pts, sm = C.shell_profile(curve, -P['shade_t'])
    shade = revolve_profile(pts, axis='z', centre=(c[0], c[1], 0), smooth=[(1, len(curve) - 1), (sm[1][0], sm[1][1] - 1)])
    for k in range(3):
        a = math.radians(90 + 120 * k)
        shade = shade - cyl('z', (c[0] + 44 * math.cos(a), c[1] + 44 * math.sin(a)), 4.5, zc - 1, z_collar_top + 1)

    so_, si_, sl = P['sleeve']
    sleeve = cyl('z', c, so_, z_fl0 - sl, z_fl0) - cyl('z', c, si_, z_fl0 - sl - 1, z_fl0 + 1)
    strip = cyl('z', c, hub_d + 3.0, z_fl0 - 32, z_fl0 - 8) - cyl('z', c, hub_d, z_fl0 - 33, z_fl0 - 7)

    # the knob on its pot's shaft, the dimmer's board in the pocket, the cord up the stem
    kd, kh = P['knob']
    knob = eased_disc(c[0], ky, kd, zc0 + 1.0, zc0 + 1.0 + kh, 2.0, bottom=False) - cyl('z', (c[0], ky), 6.0, zc0, zc0 + kh - 4)
    board = box(c[0] - 18, ky - 16, za + 7, c[0] + 18, ky + 22, za + 9) + cyl('z', (c[0], ky), 16.0, za + 9, za + 18) \
        + cyl('z', (c[0], ky), 6.0, za + 18, zc0 + kh - 4)
    cord = cyl('z', c, 5.0, zb - 8, z_hub0 + 14) + box(c[0] - 4, c[1] - 2.5, za + 7, c[0] + 4, c[1] + P['foot'][0] / 2 - 2, za + 10.5) \
        + cyl('z', c, 5.0, za + 7, zb)
    bumps = union(*(cyl('z', (c[0] + 95 * math.cos(math.radians(60 * k)), c[1] + 95 * math.sin(math.radians(60 * k))), 11.0, 0.0, b)
                    for k in range(6)))

    A20 = Sheet('cast-acrylic', 20, face='+z')
    return [
        Part('foot-lower', lower, A20, finish='acrylic', group='foot', pieces={'stack': (stack, 'acrylic')},
             notes=['its outer edge eased R2 and polished; the pocket 50 x 96 R6 through; from below the cover\'s recess '
                    '140 x 6, the cord\'s groove 10 x 11 to the back, four 4.5 holes for the cover\'s M3 inserts']),
        Part('foot-upper', upper, A20, finish='acrylic', group='foot', render=False,
             notes=['cemented on the lower, its edge eased R2; the stem\'s socket 30.4 x 12, the pocket\'s top 8 deep from below']),
        Part('cover', cover, Sheet('cast-acrylic', 6, face='-z'), finish='acrylic-satin', group='foot',
             notes=['four M3 x 8 into the inserts; the cord runs over it in the groove to a clear strain-relief bush at the back']),
        Part('stem', stem, Machined('cast-acrylic', 'lathe'), finish='acrylic', group='stem',
             notes=['cast acrylic tube 30 x 3, cut square and its ends polished; bonded into the foot\'s socket and the hub\'s bore']),
        Part('hub', hub, Machined('aluminium', 'lathe'), finish='aluminium', group='light',
             notes=['6061, bead blasted, clear anodised: the strip\'s heat sink; three M4 tapped in its flange']),
        Part('cap', cap, Machined('aluminium', 'lathe'), finish='aluminium', group='light',
             notes=['clamps the shade\'s collar on the hub\'s flange, three M4 button heads counterbored']),
        Part('shade', shade, Machined('cast-acrylic-formed', 'formed', setup_usd=90.0), finish='acrylic-dense', group='shade',
             notes=['the buck about $900, a tenth on each of a first run of ten (the setup here)',
                    'formed from 5 mm cast sheet tinted four times as dense as the cabinets\' 20 mm, so it reads the same, '
                    'over a turned buck (about 160 C), annealed; its rim trimmed and '
                    'rolled R2.5, its collar machined flat and drilled for three M4']),
        Part('sleeve', sleeve, Machined('cast-acrylic', 'lathe'), finish='opal', group='light',
             notes=['opal (white diffusing) cast acrylic tube 84 x 3, bonded to the flange\'s underside']),
        Part('strip', strip, Bought('centric-warm-strip'), finish='led', group='light'),
        Part('knob', knob, Machined('cast-acrylic', 'lathe'), finish='accent', group='foot',
             notes=['turned from rod in the colour, deeper; its edge eased; a 6 bore for the pot\'s shaft, set screw from below']),
        Part('dimmer', board, Bought('rotary-dimmer'), finish='pcb', group='foot', inside=True),
        Part('cord', cord, Bought('clear-cord'), finish='cord', group='stem'),
        Part('bumpons', bumps, Bought('bumpons-clear'), finish='rubber', group='foot'),
        Part('adapter', None, Bought('meanwell-gst25u24')),
        Part('dc-socket', None, Bought('dc-socket')),
        Part('cord-grip', None, Bought('cord-grip')),
        Part('fixings', None, Bought('lamp-fixings')),
        Part('thermal', None, Bought('thermal-tape')),
        Part('collar-gasket', None, Bought('felt-pad-ring')),
        Part('cement', None, Bought('acrylic-cement-small')),
    ]


NOTES = [
    'The shade: 5 mm tinted cast acrylic (the Clouds\' own) formed over a turned buck, about 160 C, annealed after; '
    'its rim trimmed and rolled, its collar machined flat. It hangs from its collar, clamped between the hub\'s flange '
    'and the cap on a silicone ring, three M4 screws: nothing presses on the formed wall.',
    'The light: 0.4 m of 24 V LED strip, 95 CRI, dimming from 2700 K toward 2000 K, wound twice round the hub on its '
    'own adhesive; the hub (aluminium, clear anodised) is its heat sink; an opal acrylic sleeve round it so no dot '
    'shows. About 600 lm at full, 6 W or so (confirm on the strip\'s datasheet).',
    'Power: a listed 24 V DC wall adapter (Mean Well GST25U24), a 2.1 mm in-line socket on a clear 18/2 cord into the '
    'foot\'s back; the dimmer (12-24 V PWM, its switch at the end of the turn) in the foot\'s pocket; the cord on up '
    'the stem to the hub. Nothing in the lamp is at mains voltage.',
    'The foot: two 20 mm discs, 230 and 200, cemented and annealed, the edges eased R2 and polished; the pocket '
    'through the lower closed by a 6 mm cover on four M3 screws into bonded inserts; six clear bumpers under it.',
    'The stem: cast acrylic tube 30 x 3 bonded into the foot\'s socket and the hub\'s bore with a structural acrylic '
    'adhesive.',
    'Stability: about 1.7 kg in the foot and 1.6 kg in the head; it tips past about 28 degrees, as a table lamp of its '
    'size should.',
]

PRODUCT = Product('barkhorn-lamp', 'Bell', 'Table lamp in tinted cast acrylic: the horn\'s flare as its shade',
                  params=P, parts=parts, count=1, notes=NOTES, materials=C.MATERIALS, variants=C.VARIANTS,
                  touching=[('cord', 'stem'), ('cord', 'hub'), ('dimmer', 'knob')], drawing_prefix='EL')
