"""Cumulus, EARF's record player (round 31; the owner: "Record player and lighting for one. All acrylic."), concept T2
of concepts.py, picked: the plinth drawn as the Atmosphere icons are drawn, of circles, one for each thing it holds.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/turntable.py \
        --out spinoffs/barkhorn/companions/out-turntable

- **The plinth** is two 20 mm sheets of the Clouds' tinted cast acrylic, cemented: three circles fused, the platter's
  (340), the arm's (150, on the Rega arm's pivot, 222 from the spindle) and the motor's (136), their meeting corners
  rounded R14 and every edge eased R2, as the cabinets' are.
- **The motor stands apart.** Its circle is a ring round a hole; the motor lives in its own pod of three 20 mm discs,
  standing on its own soft feet on the shelf, 4 mm clear of the plinth all round, so its hum has no path into the
  arm but the belt. It is the plain thing a good belt drive does, made visible: the cloud has a hole in it.
- **The platter** is 25 mm of the same acrylic, 300 across (2.1 kg; with its brass hub 2.4 kg turning), the belt on
  its polished rim, no mat (acrylic is close to vinyl's own impedance, which is why acrylic platters are a thing).
- **The bearing** is turned: a brass housing, flanged into a pocket in the top sheet, through both; two sintered
  bronze bushes; a hardened, ground stainless spindle on a 6 mm carbide ball and a PTFE pad. Brass is what you see
  of it through the plinth.
- **Bought:** Rega's RB330 arm (its lift on its own base), an Ortofon 2M Black, Rega's 24 V motor driven by its Neo
  PSU MK2 (33/45 by a button, trimmed in 0.01 rpm steps), a flat belt, Sorbothane under three levelling feet.

The frame is the kit's: x across from the left seen from the front, y back from the front, z up from the shelf.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
sys.path.insert(0, HERE)
from kit import *                                                   # noqa: E402,F403
import common as C                                                  # noqa: E402

P = dict(
    T=20.0,                       # SPEC (concept): the sheet, the Clouds' own
    platter_d=300.0, platter_t=25.0,
    rim=20.0,                     # the plinth's platter circle stands this far past the platter
    arm_r=222.0,                  # DATASHEET: Rega's spindle to arm hole
    arm_angle=31.1,               # the pivot's bearing from the spindle, degrees from +x (back right)
    arm_circle=150.0, arm_hole=24.0,
    motor_c=(-150.0, 135.0),      # the motor from the spindle
    motor_circle=136.0, pod_d=88.0, gap=4.0,
    fillet=14.0, ease=2.0,        # the circles' meeting corners, every edge
    feet_h=26.0,                  # the pad (6) and the foot (20): the plinth's underside from the shelf
    lift=4.0,                     # the platter's underside above the plinth
    rpm_motor=250.0,              # PROPOSAL: Rega's 24 V motor at 50 Hz from the Neo; set when the motor is in hand
)


def derived(P):
    T = P['T']
    sx = -P['motor_c'][0] + P['motor_circle'] / 2         # the motor circle's left edge at x = 0
    sy = P['platter_d'] / 2 + P['rim']                       # the platter circle's front edge at y = 0
    a = math.radians(P['arm_angle'])
    d = dict(S=(sx, sy), A=(sx + P['arm_r'] * math.cos(a), sy + P['arm_r'] * math.sin(a)),
             M=(sx + P['motor_c'][0], sy + P['motor_c'][1]))
    d['z0'] = P['feet_h']; d['z1'] = d['z0'] + T; d['z2'] = d['z1'] + T          # the plinth's three faces
    d['pz0'] = d['z2'] + P['lift']; d['pz1'] = d['pz0'] + P['platter_t']         # the platter
    d['belt_z'] = (d['pz0'] + d['pz1']) / 2
    r_belt = P['platter_d'] / 2 + 0.3
    d['pulley_d'] = round(2 * r_belt * (100.0 / 3.0) / P['rpm_motor'] - 0.6, 2)    # its belt line 0.3 out
    d['record_z'] = d['pz1'] + 1.8                                               # a 180 g record's top
    return d


D = derived(P)


def sketch_plinth(P, D, hole=True):
    from build123d import BuildSketch, Locations, Circle, Mode, fillet
    S, A, M = D['S'], D['A'], D['M']
    with BuildSketch() as sk:
        with Locations(S):
            Circle(P['platter_d'] / 2 + P['rim'])
        with Locations(A):
            Circle(P['arm_circle'] / 2)
        with Locations(M):
            Circle(P['motor_circle'] / 2)
        fillet(sk.vertices(), P['fillet'])
        if hole:
            with Locations(M):
                Circle(P['pod_d'] / 2 + P['gap'], mode=Mode.SUBTRACT)
    return sk.sketch


def slab(sketch, z0, z1, ease):
    """A sheet part from a plan, its outer edges top and bottom eased."""
    from build123d import Plane, extrude, fillet, Axis
    s = extrude(Plane.XY.offset(z0) * sketch, z1 - z0)
    if ease:
        fs = s.faces().sort_by(Axis.Z)
        s = fillet(fs[0].edges() + fs[-1].edges(), ease)
    return s


def eased_disc(cx, cy, d, z0, z1, ease, bottom=True, top=True):
    from build123d import fillet, Axis
    s = cyl('z', (cx, cy), d, z0, z1)
    fs = s.faces().sort_by(Axis.Z)
    es = (fs[0].edges() if bottom else []) + (fs[-1].edges() if top else [])
    return fillet(es, ease) if es else s


def hull_pts(circles, n=180):
    """The convex hull of circles [(cx, cy, r)], as an outline: the belt's path round the platter and the pulley."""
    pts = sorted({(round(cx + r * math.cos(2 * math.pi * k / n), 4), round(cy + r * math.sin(2 * math.pi * k / n), 4))
                  for cx, cy, r in circles for k in range(n)})
    def half(ps):
        h = []
        for p in ps:
            while len(h) >= 2 and (h[-1][0] - h[-2][0]) * (p[1] - h[-2][1]) - (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0]) <= 0:
                h.pop()
            h.append(p)
        return h
    lo, hi = half(pts), half(list(reversed(pts)))
    return lo[:-1] + hi[:-1]


def arm_solids(P, D):
    """Rega's RB330 as a stand-in drawn from its published geometry (effective length 236.5, offset 21.55 deg) and
    proportioned elsewhere: the base and its nut's pillar, the bearing yoke, the tube to the headshell, the
    counterweight, the lift. Resting: the tube points to the front, the stylus off the platter at its right."""
    from build123d import Pos, Rot
    ax, ay = D['A']
    z = D['z2']
    h = D['record_z'] + 21.0                                            # the tube's axis: the cartridge, the headshell
    L = 236.5
    rest = math.radians(-96.0)                                          # on the lift, a little in from straight ahead
    ex, ey = ax + L * math.cos(rest), ay + L * math.sin(rest)
    ang = math.degrees(rest)
    tube = Pos(ax, ay, h) * Rot(0, 0, ang) * Pos((L - 22) / 2, 0, 0) * Rot(0, 90, 0) * cyl('z', (0, 0), 9.5, -(L - 22) / 2, (L - 22) / 2)
    head = Pos(ex, ey, h) * Rot(0, 0, ang + 21.55) * box(-26, -9, -4.5, 6, 9, 0.5)
    cw = Pos(ax, ay, h) * Rot(0, 0, ang) * Rot(0, 90, 0) * cyl('z', (0, 0), 34, -64, -36)
    stub = Pos(ax, ay, h) * Rot(0, 0, ang) * Rot(0, 90, 0) * cyl('z', (0, 0), 8, -40, -6)
    base = union(cyl('z', (ax, ay), 44, z, z + 8), cyl('z', (ax, ay), 26, z + 8, h - 8),
                 box(ax - 16, ay - 12, h - 9, ax + 16, ay + 12, h + 9))
    lift = union(cyl('z', (ax + 30, ay - 14), 10, z, h - 6), box(ax + 26, ay - 50, h - 10, ax + 34, ay - 14, h - 6))
    cart_c = (ex + 6 * math.cos(rest), ey + 6 * math.sin(rest))
    cart = Pos(cart_c[0], cart_c[1], h - 4.5) * Rot(0, 0, ang + 21.55) * box(-14, -9, -17, 13, 9, 0)
    return union(base, tube, head, cw, stub, lift), cart


def parts(P):
    from build123d import Pos
    D = derived(P)
    T, e = P['T'], P['ease']
    S, A, M = D['S'], D['A'], D['M']
    z0, z1, z2 = D['z0'], D['z1'], D['z2']
    A20 = Sheet('cast-acrylic', 20, face='+z')
    A25 = Sheet('cast-acrylic', 25, face='+z')

    # the plinth: two sheets, the bearing's housing through both (32.4), its flange in a pocket in the top (56.4 x 6)
    # with three 6 holes 10 deep for its bonded inserts, the arm's hole through both, the feet's inserts in the bottom
    sk = sketch_plinth(P, D)
    feet = [(S[0] - 100, S[1] - 95), (S[0] + 100, S[1] - 95), (S[0] + 80, S[1] + 110)]
    lower = slab(sk, z0, z1, 0) - cyl('z', S, 32.4, z0 - 1, z1 + 1) - cyl('z', A, P['arm_hole'], z0 - 1, z1 + 1)
    for fx, fy in feet:
        lower = lower - cyl('z', (fx, fy), 12.5, z0 - 1, z0 + 15)
    upper = slab(sk, z1, z2, 0) - cyl('z', S, 32.4, z1 - 1, z2 + 1) - cyl('z', S, 56.4, z2 - 6, z2 + 1) - cyl('z', A, P['arm_hole'], z1 - 1, z2 + 1)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        upper = upper - cyl('z', (S[0] + 22 * math.cos(a), S[1] + 22 * math.sin(a)), 6.0, z2 - 16, z2 - 5)
    stack = slab(sk, z0, z2, e) - cyl('z', S, 32.4, z0 - 1, z2 + 1) - cyl('z', S, 56.4, z2 - 6, z2 + 1) - cyl('z', A, P['arm_hole'], z0 - 1, z2 + 1)

    # the bearing: a brass housing (its flange 56 x 6, its body 32 down to 10 above the shelf, a 14 bore for the
    # bushes, a 13.8 floor for the pad), the spindle (10, ground, its top 7.2 for the record, 16 above the platter)
    hz0 = 10.0
    housing = (cyl('z', S, 32.0, hz0, z2 - 6) + cyl('z', S, 56.0, z2 - 6, z2)) - cyl('z', S, 14.0, hz0 + 4, z2 + 1)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        housing = housing - cyl('z', (S[0] + 22 * math.cos(a), S[1] + 22 * math.sin(a)), 4.5, z2 - 7, z2 + 1)
    pad = cyl('z', S, 13.8, hz0 + 4, hz0 + 6)
    ball_c = hz0 + 9
    from build123d import Sphere
    ball = Pos(S[0], S[1], ball_c) * Sphere(3.0)
    bushes = union(cyl('z', S, 14.0, hz0 + 14, hz0 + 26) - cyl('z', S, 10.0, hz0 + 13, hz0 + 27),
                   cyl('z', S, 14.0, z2 - 18, z2 - 6) - cyl('z', S, 10.0, z2 - 19, z2 - 5))
    pz0, pz1 = D['pz0'], D['pz1']
    spindle = cyl('z', S, 10.0, ball_c + 3, pz1) + cyl('z', S, 7.2, pz1, pz1 + 16)
    hub = cyl('z', S, 46.0, pz0, pz1) - cyl('z', S, 10.0, pz0 - 1, pz1 + 1)
    platter = cyl('z', S, P['platter_d'], pz0, pz1) - cyl('z', S, 46.0, pz0 - 1, pz1 + 1)
    platter_soft = eased_disc(S[0], S[1], P['platter_d'], pz0, pz1, e) - cyl('z', S, 46.0, pz0 - 1, pz1 + 1)

    # the motor's pod: three 88 discs on three soft pads, the motor's body in a 56 bore through the upper two, its
    # lead down a 10 hole in the bottom disc and out along a groove under it; the motor on its plate on top
    pz = [6.0, 26.0, 46.0, 66.0]
    pods = []
    for i in range(3):
        d = cyl('z', M, P['pod_d'], pz[i], pz[i + 1])
        if i > 0:
            d = d - cyl('z', M, 56.0, pz[i] - 1, pz[i + 1] + 1)
        else:
            d = d - cyl('z', M, 10.0, pz[0] - 1, pz[1] + 1) - box(M[0] - 5, M[1], pz[0] - 1, M[0] + 5, M[1] + 50, pz[0] + 6)
        pods.append(d)
    pod_stack = eased_disc(M[0], M[1], P['pod_d'], pz[0], pz[3], e) - cyl('z', M, 56.0, pz[1], pz[3] + 1)
    motor = union(cyl('z', M, 50.0, pz[1] + 4, pz[3]), cyl('z', M, 66.0, pz[3], pz[3] + 3), cyl('z', M, 4.0, pz[3] + 3, D['belt_z'] + 9))
    pd = D['pulley_d']
    pulley = (cyl('z', M, pd, D['belt_z'] - 5, D['belt_z'] + 5) + cyl('z', M, pd + 6, D['belt_z'] + 5, D['belt_z'] + 7)) \
        - cyl('z', M, 4.0, D['belt_z'] - 6, D['belt_z'] + 8)
    pads = union(*(cyl('z', (M[0] + 28 * math.cos(math.radians(90 + 120 * k)), M[1] + 28 * math.sin(math.radians(90 + 120 * k))), 25, 0, 6)
                   for k in range(3)))

    # the belt, 5 x 0.6, round the platter's rim and the pulley
    R = P['platter_d'] / 2
    inner = hull_pts([(S[0], S[1], R + 0.05), (M[0], M[1], pd / 2 + 0.05)], n=360)
    outer = hull_pts([(S[0], S[1], R + 0.65), (M[0], M[1], pd / 2 + 0.65)], n=360)
    belt = prism(outer, 'z', D['belt_z'] - 2.5, D['belt_z'] + 2.5) - prism(inner, 'z', D['belt_z'] - 3, D['belt_z'] + 3)

    # the feet: a 50 acrylic disc on each M8 stud, its Sorbothane under it
    foot_parts = [Part(f'foot-{i + 1}', cyl('z', (fx, fy), 50.0, 6.0, z0), A20, finish='acrylic', group='feet',
                       pieces={'disc': (eased_disc(fx, fy, 50.0, 6.0, z0, e), 'acrylic')},
                       notes=['tapped M8 through its centre and turned on its stud to level the platter'])
                  for i, (fx, fy) in enumerate(feet)]
    fpad = union(*(cyl('z', (fx, fy), 44.0, 0.0, 6.0) for fx, fy in feet))

    arm, cart = arm_solids(P, D)

    # EARF, 44 wide, etched in the arm's circle in front of its base and filled with the colour (a hair off the face)
    mark = mark_top(44.0, (A[0] - 4, A[1] - 58), z2 + 0.02, 0.1)

    return [
        Part('plinth-lower', lower, A20, finish='acrylic', group='plinth', pieces={'stack': (stack, 'acrylic')},
             notes=['cemented under the upper with a polymerising acrylic cement, clamped flat; annealed after; the outline\'s edges eased R2 and polished after cementing',
                    'three 12.5 holes 15 deep from below for the feet\'s M8 inserts']),
        Part('plinth-upper', upper, A20, finish='acrylic', group='plinth', render=False,
             notes=['the bearing\'s flange in the 56.4 pocket 6 deep, three 6 holes 11 deep for its M4 inserts']),
        Part('platter', platter, A25, finish='acrylic', group='platter', pieces={'disc': (platter_soft, 'acrylic')},
             notes=['its edges eased R2, its rim polished and crowned 0.2 for the belt; balanced on the hub after bonding (under 2 g mm)']),
        Part('platter-hub', hub, Machined('brass', 'lathe'), finish='brass', group='platter',
             notes=['bonded into the platter with a structural acrylic adhesive; bored after, true to the spindle']),
        Part('spindle', spindle, Machined('stainless', 'lathe', setup_usd=120.0), finish='steel', group='bearing',
             notes=['440C or hardened 416, ground to 10 h5; the record spindle 7.2; a 6 cup at its foot for the ball; '
                    'pressed and bonded into the hub']),
        Part('bearing-housing', housing, Machined('brass', 'lathe'), finish='brass', group='bearing',
             notes=['C360 brass; the bushes pressed in and reamed in line; filled with 2 ml of oil']),
        Part('bushes', bushes, Bought('bearing-bushes'), finish='brass', group='bearing', inside=True),
        Part('ball', ball, Bought('carbide-ball'), finish='steel', group='bearing', inside=True),
        Part('thrust-pad', pad, Bought('thrust-pad'), finish='black', group='bearing', inside=True),
        Part('pod-1', pods[0], A20, finish='acrylic', group='pod', pieces={'stack': (pod_stack, 'acrylic')},
             notes=['the motor\'s lead down the 10 hole and out the 10 groove under it']),
        Part('pod-2', pods[1], A20, finish='acrylic', group='pod', render=False),
        Part('pod-3', pods[2], A20, finish='acrylic', group='pod', render=False),
        Part('motor', motor, Bought('rega-24v-motor'), finish='black', group='pod',
             notes=['on its own rubber mounts on the pod\'s top; the bore waits on the motor in hand']),
        Part('pulley', pulley, Machined('aluminium', 'lathe'), finish='aluminium', group='pod',
             notes=[f'its belt face {D["pulley_d"]:.2f} at {P["rpm_motor"]:g} rpm (Neo, 33.3); turned to the motor\'s '
                    'measured speed; the Neo trims the rest']),
        Part('pod-pads', pads, Bought('sorbothane-pod'), finish='rubber', group='pod'),
        Part('belt', belt, Bought('flat-belt'), finish='rubber', group='platter'),
        *foot_parts,
        Part('foot-pads', fpad, Bought('sorbothane-feet'), finish='rubber', group='feet'),
        Part('arm', arm, Bought('rega-rb330'), finish='arm', group='arm',
             notes=['its nut under the plinth; its height set with Rega\'s spacers to the cartridge\'s VTA']),
        Part('cartridge', cart, Bought('ortofon-2m-black'), finish='cartridge', group='arm'),
        Part('mark', mark, Bought('laser-etch-small'), finish='accent'),
        Part('neo-psu', None, Bought('rega-neo-psu-mk2')),
        Part('feet-studs', None, Bought('feet-studs')),
        Part('bearing-fixings', None, Bought('bearing-fixings')),
        Part('bearing-oil', None, Bought('bearing-oil')),
        Part('cement', None, Bought('acrylic-cement-small')),
    ]


def mark_top(width, at, z, t):
    """EARF's wordmark `width` wide on a top face, read from the front: `at` its foot's middle (x, y), z its face."""
    sys.path.insert(0, os.path.dirname(HERE))
    import marks as M
    s = width / M.WORDMARK_W
    sol = []
    circ = lambda cx, cy, r: [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in (2 * math.pi * k / 72 for k in range(72))]
    on = lambda pts: [(at[0] - width / 2 + x * s, at[1] + (300 - y) * s) for x, y in pts]
    for p in M.WORDMARK:
        holes = []
        if p[0] == 'rect':
            x0, y0, x1, y1 = p[1:5]; pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        elif p[0] == 'circle':
            pts = circ(p[1], p[2], p[3])
        elif p[0] == 'ring':
            pts, holes = circ(p[1], p[2], p[3]), [circ(p[1], p[2], p[4])]
        else:
            pts = list(p[1:])
        sh = prism(on(pts), 'z', z, z + t)
        for h in holes:
            sh = sh - prism(on(h), 'z', z - 0.01, z + t + 0.01)
        sol.append(sh)
    return union(*sol)


NOTES = [
    'The plinth: two 20 mm sheets of tinted cast acrylic (the Clouds\' own, in the colour), CNC cut as one outline of '
    'three circles, its corners R14 and its edges eased R2 and polished, cemented with a two-part polymerising acrylic '
    'cement (Acrifix 1R 0192 kind) on a flat table, annealed after (about 80 C, an hour for each 3 mm, cooled slowly).',
    'The motor stands apart: its pod (three 88 discs cemented) on three soft Sorbothane discs on the shelf, 4 mm clear '
    'of the plinth all round. Nothing touches the plinth from the motor but the belt.',
    'The platter: 25 mm of the same acrylic, 300 across, its rim polished and crowned; the brass hub bonded in, the '
    'spindle pressed and bonded into the hub, the whole balanced. No mat.',
    'The bearing: a turned brass housing through both sheets, flanged into a pocket in the top on three M4 screws into '
    'bonded inserts; two sintered bronze bushes; a ground stainless spindle on a 6 mm carbide ball on a PTFE pad. Oiled.',
    'Speed: Rega\'s 24 V motor driven by the Neo PSU MK2 (33/45 by a button, 0.01 rpm trim); the pulley turned to the '
    'motor\'s measured speed so the Neo trims from the middle of its range; a flat belt on the platter\'s rim.',
    'Arm: Rega RB330, 222 from the spindle (Rega geometry), its nut under the plinth through a 24 hole; an Ortofon 2M '
    'Black. Level the platter on the three feet (each turns on its M8 stud) before setting the arm.',
    'The mark: EARF 44 wide laser-etched in the arm\'s circle in front of the arm and filled with the colour, deeper.',
]

PRODUCT = Product('barkhorn-turntable', 'Cumulus', 'Belt-drive record player in tinted cast acrylic, the motor apart',
                  params=P, parts=parts, count=1, notes=NOTES, materials=C.MATERIALS, variants=C.VARIANTS,
                  touching=[('bushes', 'bearing-housing'), ('bushes', 'spindle')], drawing_prefix='EC')

if __name__ == '__main__':
    d = derived(P)
    m = math.pi * (P['platter_d'] / 2000) ** 2 * P['platter_t'] / 1000 * 1190
    print({k: (tuple(round(x, 1) for x in v) if isinstance(v, tuple) else round(v, 2)) for k, v in d.items()})
    print(f'platter {m:.2f} kg, I {0.5 * m * (P["platter_d"] / 2000) ** 2:.4f} kg m2')
