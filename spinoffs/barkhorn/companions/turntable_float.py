"""Float, EARF's record player, final (round 34). The owner, 2026-10-18: "I want a squared record player similar to a
debut or orbit but with a clear body and matching cover." "The brian eno one and the audio technica hotaru are
acrylic I think and look really cool when backlit, but are way too expensive." And 2026-10-22: "We also need to
finalize the record player." Round 31c's R3 Float, refined; Cumulus's engineering (turntable.py) carried over.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/turntable_float.py \
        --out spinoffs/barkhorn/companions/out-turntable-float

- **The plinth** is one 25 mm sheet of the Clouds' tinted cast acrylic, 450 x 360, its corners R4 and its edges eased
  and polished: the Debut's and the Orbit's squared slab.
- **It floats** 32 mm over a 10 mm base of the same acrylic on four clear posts, each bonded under the plinth and
  standing on a Sorbothane bushing on the base, held down by a stainless M6 bolt through a second bushing under the
  base, so nothing hard joins the plinth to the base and it cannot be tipped off.
- **The base glows round its edge.** A 24 V strip stands in a 3 mm slot routed up into the base's underside 12 mm in
  from its edge, facing out: its light enters the slot's outer wall, stays in the sheet (it meets the faces past the
  critical angle) and leaves at the polished edge. The top stays clear.
- **The motor stands apart**, on the base, in its own pod of acrylic discs on three soft pads, up through a hole in
  the plinth with 4 mm clear all round: the belt is the only thing that touches both.
- **Bought:** Rega's RB330 arm and its lift, an Ortofon 2M Black, Rega's 24 V motor driven by its Neo PSU MK2,
  Pro-Ject's friction hinges for a 6 mm lid in the same tint, the LED strip behind a listed 24 V adapter and an
  in-line dimmer, levelling feet. The bearing is turned, as Cumulus's (no inverted bearing is sold on its own now).

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
    W=450.0, D=360.0, T=25.0, R=4.0,          # PROPOSAL: the plinth, a Debut's or an Orbit's footprint
    margin=10.0, Tb=10.0, Rb=8.0,             # the base: 10 past the plinth all round, 10 thick
    feet_h=14.0,                              # the levelling feet: the base's underside from the shelf
    gap=32.0,                                 # the float: base top to the plinth's underside
    post_d=30.0, post_bore=6.6,               # the clear posts (an M6 bolt through each)
    posts=((135.0, 60.0), (315.0, 60.0), (135.0, 300.0), (315.0, 300.0)),   # in the plinth's own frame
    bush_t=5.6,                               # the Sorbothane bushing under each post (0.22 in)
    spindle=(190.0, 175.0),                   # in the plinth's frame
    platter_d=300.0, platter_t=20.0, lift=4.0,
    arm_r=222.0, arm_x=385.0,                 # DATASHEET: Rega's spindle to arm hole; the pivot's x (plinth frame)
    L_eff=236.5, offset=21.55,                # DATASHEET: RB330's effective length, its headshell's offset
    rest_r=168.0,                             # at rest the stylus sits this far from the spindle, on the arm's arc
    pod=(57.0, 303.0), pod_d=76.0, pod_gap=4.0,
    rpm_motor=250.0,                          # PROPOSAL: Rega's 24 V motor at 50 Hz from the Neo; set when in hand
    slot_in=12.0, slot_w=3.0, slot_h=9.0, strip_end=40.0,   # the light's slot under the base, its runs' ends
    lid_t=6.0, lid_h=100.0, bumper=5.0, open_deg=78.0,      # the lid
    ease=1.5,
)


def derived(P):
    m = P['margin']
    d = {}
    d['ox'] = d['oy'] = m                                  # the plinth's corner in the base's (the product's) frame
    S = (m + P['spindle'][0], m + P['spindle'][1])
    ay = math.sqrt(P['arm_r'] ** 2 - (P['arm_x'] - P['spindle'][0]) ** 2)
    A = (m + P['arm_x'], S[1] + ay)
    M = (m + P['pod'][0], m + P['pod'][1])
    d.update(S=S, A=A, M=M)
    d['b0'] = P['feet_h']; d['b1'] = d['b0'] + P['Tb']                  # the base
    d['z0'] = d['b1'] + P['gap']; d['z1'] = d['z0'] + P['T']            # the plinth
    d['pz0'] = d['z1'] + P['lift']; d['pz1'] = d['pz0'] + P['platter_t']
    d['belt_z'] = (d['pz0'] + d['pz1']) / 2
    d['record_z'] = d['pz1'] + 1.8
    r_belt = P['platter_d'] / 2 + 0.3
    d['pulley_d'] = round(2 * r_belt * (100.0 / 3.0) / P['rpm_motor'] - 0.6, 2)
    # the arm at rest: the stylus on the arm's arc rest_r from the spindle (just off the record's lead-in), the
    # nearer of the arc's two crossings to the front
    dx, dy = S[0] - A[0], S[1] - A[1]
    dd = math.hypot(dx, dy); L = P['L_eff']; r = P['rest_r']
    a = (L * L - r * r + dd * dd) / (2 * dd); h = math.sqrt(L * L - a * a)
    bx, by = A[0] + a * dx / dd, A[1] + a * dy / dd
    cands = [(bx + h * dy / dd, by - h * dx / dd), (bx - h * dy / dd, by + h * dx / dd)]
    st = min(cands, key=lambda p: p[1])
    d['stylus'] = st
    d['rest_deg'] = math.degrees(math.atan2(st[1] - A[1], st[0] - A[0]))
    # the lid's hinge axis: behind the plinth's back edge, a little over its top
    d['lid_z0'] = d['z1'] + P['bumper']
    d['hinge'] = (m + P['D'] + 2.0, d['lid_z0'] + 2.0)
    return d


D = derived(P)


def rr(w, d, r, x0, y0):
    return rounded_rect(w, d, r, cx=x0 + w / 2, cy=y0 + d / 2)


def slab(outline, z0, z1, ease):
    from build123d import fillet, Axis
    s = prism(outline, 'z', z0, z1)
    if ease:
        fs = s.faces().sort_by(Axis.Z)
        s = fillet(fs[0].edges() + fs[-1].edges(), ease)
    return s


def ring_skin(outline_out, outline_in, z0, z1):
    """A thin skin round an edge: what glows."""
    return prism(outline_out, 'z', z0, z1) - prism(outline_in, 'z', z0 - 1, z1 + 1)


def hull_pts(circles, n=180):
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
    """Rega's RB330 as a stand-in from its published geometry (effective length 236.5, offset 21.55 deg), at rest:
    the stylus just off the record's lead-in, the tube in the lift's cradle. Returns the arm (base, yoke, tube,
    counterweight), its lift on its own base on the plinth, and the cartridge."""
    from build123d import Pos, Rot
    ax, ay = D['A']
    z = D['z1']
    h = D['record_z'] + 21.0                                            # the tube's axis
    ang = D['rest_deg']
    u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    L = P['L_eff']
    sx, sy = D['stylus']
    tube_L = L - 30
    tube = Pos(ax, ay, h) * Rot(0, 0, ang) * Pos(tube_L / 2, 0, 0) * Rot(0, 90, 0) * cyl('z', (0, 0), 9.5, -tube_L / 2, tube_L / 2)
    # the headshell: a flat plate turned by the offset, the stylus at its tip's underside
    head = Pos(sx, sy, h) * Rot(0, 0, ang + P['offset']) * box(-34, -9, -4.5, 4, 9, 0.5)
    cw = Pos(ax, ay, h) * Rot(0, 0, ang) * Rot(0, 90, 0) * cyl('z', (0, 0), 34, -66, -38)
    stub = Pos(ax, ay, h) * Rot(0, 0, ang) * Rot(0, 90, 0) * cyl('z', (0, 0), 8, -40, -6)
    yoke = Pos(ax, ay, h) * Rot(0, 0, ang) * box(-16, -12, -9, 16, 12, 9)
    base = union(cyl('z', (ax, ay), 44, z, z + 8), cyl('z', (ax, ay), 26, z + 8, h - 9))
    # the lift, on its own base: a pillar 70 along the tube and 22 to its right (outboard), a cradle across under it
    nx, ny = u[1], -u[0]                                                 # the tube's right hand, seen from the pivot
    lx, ly = ax + 70 * u[0] + 22 * nx, ay + 70 * u[1] + 22 * ny
    lift = union(cyl('z', (lx, ly), 18, z, z + 3), cyl('z', (lx, ly), 9, z + 3, h - 7.5),
                 Pos(lx - 11 * nx, ly - 11 * ny, h - 7.5) * Rot(0, 0, ang + 90) * box(-14, -3, -3, 14, 3, 2.75))
    # the 2M's body under the headshell (18 wide, 15 tall), its stylus housing forward and below, the stylus at x = 0
    cart = Pos(sx, sy, h - 4.5) * Rot(0, 0, ang + P['offset']) * union(box(-21, -9, -15, 1, 9, 0), box(-6, -3.5, -17.5, 1.5, 3.5, -14.5))
    return union(base, yoke, tube, head, cw, stub), lift, cart


def mark_top(width, at, z, t):
    import turntable
    return turntable.mark_top(width, at, z, t)


def parts(P, lid_open=False):
    """The parts; `lid_open` swings the lid up on its hinges (a render model for the open shot, never built)."""
    from build123d import Pos, Rot, Sphere
    D = derived(P)
    W, Dp, T, m, e = P['W'], P['D'], P['T'], P['margin'], P['ease']
    S, A, M = D['S'], D['A'], D['M']
    b0, b1, z0, z1 = D['b0'], D['b1'], D['z0'], D['z1']
    Wb, Db = W + 2 * m, Dp + 2 * m
    A25 = Sheet('cast-acrylic', 25, face='+z')
    A20 = Sheet('cast-acrylic', 20, face='+z')
    A10 = Sheet('cast-acrylic', 10, face='+z')
    A6 = Sheet('cast-acrylic', 6)
    out = rr(W, Dp, P['R'], m, m)
    bout = rr(Wb, Db, P['Rb'], 0, 0)
    posts = [(m + x, m + y) for x, y in P['posts']]

    # -- the plinth: the bearing's housing through it (32.4), its flange in a pocket in the top (56.4 x 6) on three
    # M4 inserts; the arm's hole (24); the pod's hole (84); under it, the four posts' bonded seats (an M6 insert 12
    # deep in each), the lift's foot screw
    def plinth_cuts(s):
        s = s - cyl('z', S, 32.4, z0 - 1, z1 + 1) - cyl('z', S, 56.4, z1 - 6, z1 + 1) - cyl('z', A, 24.0, z0 - 1, z1 + 1)
        s = s - cyl('z', M, P['pod_d'] + 2 * P['pod_gap'], z0 - 1, z1 + 1)
        for k in range(3):
            a = math.radians(90 + 120 * k)
            s = s - cyl('z', (S[0] + 22 * math.cos(a), S[1] + 22 * math.sin(a)), 6.0, z1 - 16, z1 - 5)
        for p in posts:
            s = s - cyl('z', p, 8.0, z0 - 1, z0 + 12)
        return s
    plinth = plinth_cuts(prism(out, 'z', z0, z1))
    plinth_soft = plinth_cuts(slab(out, z0, z1, e))

    # -- the base: the light's slot up from below (3 x 9, 12 in from the edge, four straight runs that stop short
    # of the corners), the four feet's M6 inserts, the four bolts' holes (10, for the bushings' sleeves), the motor's
    # lead down through a 10 hole under the pod and out to the back-left corner in a groove underneath, the arm's
    # lead in a groove on top to the back-right corner, the light's lead out at the back-right corner below
    si, sw, sh, se = P['slot_in'], P['slot_w'], P['slot_h'], P['strip_end']
    runs = [box(se, si, b0 - 1, Wb - se, si + sw, b0 + sh), box(se, Db - si - sw, b0 - 1, Wb - se, Db - si, b0 + sh),
            box(si, se, b0 - 1, si + sw, Db - se, b0 + sh), box(Wb - si - sw, se, b0 - 1, Wb - si, Db - se, b0 + sh)]
    feet = [(35.0, 35.0), (Wb - 35, 35.0), (35.0, Db - 35), (Wb - 35, Db - 35)]

    def groove(p0, p1, wd, za, zb):
        ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        return Pos(p0[0], p0[1], 0) * Rot(0, 0, ang) * box(0, -wd / 2, za, L, wd / 2, zb)

    lead_m = groove(M, (-5.0, Db + 5.0), 8.0, b0 - 1, b0 + 4)
    lead_a = groove((A[0] - 10, A[1] - 10), (Wb + 5.0, Db + 5.0), 8.0, b1 - 4, b1 + 1)

    def base_cuts(s):
        for r_ in runs:
            s = s - r_
        for f in feet:
            s = s - cyl('z', f, 8.0, b0 - 1, b0 + 7)
        for p in posts:
            s = s - cyl('z', p, 10.0, b0 - 1, b1 + 1)
        return s - cyl('z', M, 10.0, b0 - 1, b1 + 1) - lead_m - lead_a
    base = base_cuts(prism(bout, 'z', b0, b1))
    base_soft = base_cuts(slab(bout, b0, b1, e))
    # the strip in its slot, its LEDs facing out; and the polished edge it lights, as a skin a hair outside it
    strip = union(*[box(se + 2, si + sw - 1.6, b0 + 0.5, Wb - se - 2, si + sw - 0.2, b0 + 8.5),
                    box(se + 2, Db - si - sw + 0.2, b0 + 0.5, Wb - se - 2, Db - si - sw + 1.6, b0 + 8.5),
                    box(si + sw - 1.6, se + 2, b0 + 0.5, si + sw - 0.2, Db - se - 2, b0 + 8.5),
                    box(Wb - si - sw + 0.2, se + 2, b0 + 0.5, Wb - si - sw + 1.6, Db - se - 2, b0 + 8.5)])
    edge = ring_skin(rounded_rect(Wb + 0.8, Db + 0.8, P['Rb'] + 0.4, cx=Wb / 2, cy=Db / 2),
                     rounded_rect(Wb + 0.1, Db + 0.1, P['Rb'] + 0.05, cx=Wb / 2, cy=Db / 2), b0 + e, b1 - e)

    # -- the float: each post a clear rod 30 bored 6.6, bonded under the plinth; under it a Sorbothane bushing on the
    # base, a second under the base, a washer and a nut; the M6 bolt up through it all into the plinth's insert
    bt = P['bush_t']
    post_parts, bush_top, bush_bot, bolts = [], [], [], []
    for p in posts:
        post_parts.append(cyl('z', p, P['post_d'], b1 + bt, z0) - cyl('z', p, P['post_bore'], b1 + bt - 1, z0 + 1))
        bush_top.append(cyl('z', p, 18.3, b1, b1 + bt) - cyl('z', p, 7.1, b1 - 1, b1 + bt + 1))
        bush_bot.append(cyl('z', p, 18.3, b0 - bt, b0) - cyl('z', p, 7.1, b0 - bt - 1, b0 + 1))
        bolts.append(union(cyl('z', p, 6.0, b0 - bt - 1.6, z0 + 10), cyl('z', p, 18.0, b0 - bt - 1.6, b0 - bt),
                           cyl('z', p, 11.0, b0 - bt - 6.6, b0 - bt - 1.6)))

    # -- the bearing (turned, as Cumulus's): a brass housing from 10 over the base up through the plinth, flanged
    # into its pocket; two sintered bronze bushes; a ground stainless spindle on a 6 mm carbide ball and a PTFE pad
    hz0 = b1 + 8.0
    housing = (cyl('z', S, 32.0, hz0, z1 - 6) + cyl('z', S, 56.0, z1 - 6, z1)) - cyl('z', S, 14.0, hz0 + 4, z1 + 1)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        housing = housing - cyl('z', (S[0] + 22 * math.cos(a), S[1] + 22 * math.sin(a)), 4.5, z1 - 7, z1 + 1)
    pad = cyl('z', S, 13.8, hz0 + 4, hz0 + 6)
    ball_c = hz0 + 9
    ball = Pos(S[0], S[1], ball_c) * Sphere(3.0)
    bushes = union(cyl('z', S, 14.0, hz0 + 14, hz0 + 26) - cyl('z', S, 10.0, hz0 + 13, hz0 + 27),
                   cyl('z', S, 14.0, z1 - 18, z1 - 6) - cyl('z', S, 10.0, z1 - 19, z1 - 5))
    pz0, pz1 = D['pz0'], D['pz1']
    spindle = cyl('z', S, 10.0, ball_c + 3, pz1) + cyl('z', S, 7.2, pz1, pz1 + 16)
    hub = cyl('z', S, 46.0, pz0, pz1) - cyl('z', S, 10.0, pz0 - 1, pz1 + 1)
    pdisc = cyl('z', S, P['platter_d'], pz0, pz1) - cyl('z', S, 46.0, pz0 - 1, pz1 + 1)
    pdisc_soft = slab(circle_pts(S[0], S[1], P['platter_d'], 128), pz0, pz1, e) - cyl('z', S, 46.0, pz0 - 1, pz1 + 1)

    # -- the motor's pod on the base: two 20 discs and a 10 on three soft pads, the motor's body in a 56 bore
    # through the top two, its lead down a 10 hole; the motor's flange on top, the pulley at the platter's mid-rim
    q = [b1 + 6.0, b1 + 26.0, b1 + 46.0, b1 + 56.0]
    pods = []
    for i in range(3):
        dsk = cyl('z', M, P['pod_d'], q[i], q[i + 1])
        dsk = dsk - (cyl('z', M, 56.0, q[i] - 1, q[i + 1] + 1) if i > 0 else cyl('z', M, 10.0, q[0] - 1, q[1] + 1))
        pods.append(dsk)
    pod_soft = slab(circle_pts(M[0], M[1], P['pod_d'], 96), q[0], q[3], e) - cyl('z', M, 56.0, q[1], q[3] + 1)
    bz = D['belt_z']
    motor = union(cyl('z', M, 50.0, q[1] + 4, q[3]), cyl('z', M, 66.0, q[3], q[3] + 3), cyl('z', M, 4.0, q[3] + 3, bz + 9))
    pd = D['pulley_d']
    pulley = (cyl('z', M, pd, bz - 5, bz + 5) + cyl('z', M, pd + 6, bz + 5, bz + 7)) - cyl('z', M, 4.0, bz - 6, bz + 8)
    pod_pads = union(*(cyl('z', (M[0] + 26 * math.cos(math.radians(90 + 120 * k)), M[1] + 26 * math.sin(math.radians(90 + 120 * k))),
                           25, b1, b1 + 6) for k in range(3)))

    R = P['platter_d'] / 2
    inner = hull_pts([(S[0], S[1], R + 0.05), (M[0], M[1], pd / 2 + 0.05)], n=360)
    outer = hull_pts([(S[0], S[1], R + 0.65), (M[0], M[1], pd / 2 + 0.65)], n=360)
    belt = prism(outer, 'z', bz - 2.5, bz + 2.5) - prism(inner, 'z', bz - 3, bz + 3)

    foot = union(*(union(cyl('z', f, 30.0, 0, 6), cyl('z', f, 22.0, 6, 10), cyl('z', f, 6.0, 10, b0)) for f in feet))

    arm, lift, cart = arm_solids(P, D)

    # -- the lid: 6 mm sheet in the same tint, a top and four walls cemented, standing on six clear bumpers on the
    # plinth, hinged behind on Pro-Ject's two friction hinges, each in a slot in a 20 mm acrylic block screwed to
    # the plinth's back edge on two M4 inserts
    t, lz0 = P['lid_t'], D['lid_z0']
    lz1 = lz0 + P['lid_h']
    x0, y0, x1, y1 = m + 1, m + 1, m + W - 1, m + Dp - 1
    lid = {'lid-top': box(x0, y0, lz1 - t, x1, y1, lz1),
           'lid-front': box(x0, y0, lz0, x1, y0 + t, lz1 - t),
           'lid-back': box(x0, y1 - t, lz0, x1, y1, lz1 - t),
           'lid-left': box(x0, y0 + t, lz0, x0 + t, y1 - t, lz1 - t),
           'lid-right': box(x1 - t, y0 + t, lz0, x1, y1 - t, lz1 - t)}
    hy, hz = D['hinge']

    def opened(s):
        return Pos(0, hy, hz) * Rot(-P['open_deg'], 0, 0) * Pos(0, -hy, -hz) * s
    hx = [m + 80.0, m + W - 80.0]
    blocks = union(*(box(x - 20, m + Dp, z0 + 2.5, x + 20, m + Dp + 9.5, z1 - 2.5) for x in hx))
    hinges = union(*(union(box(x - 15, m + Dp, z1 - 2.5, x + 15, m + Dp + 8, lz0), box(x - 15, y1, lz0, x + 15, m + Dp + 8, lz0 + 22))
                     for x in hx))
    bumps = union(*(Pos(x, y, z1 - 0.5) * Sphere(5.5) for x, y in
                    [(x0 + 3, y0 + 40), (x1 - 3, y0 + 40), (x0 + 3, y1 - 40), (x1 - 3, y1 - 40), ((x0 + x1) / 2, y0 + 3), ((x0 + x1) / 2, y1 - 3)]))
    bumps = bumps - box(0, 0, z1 - 10, Wb, Db, z1)

    mark = mark_top(40.0, (m + W - 40, m + 18), z1 + 0.02, 0.1)

    lid_parts = []
    for k, s in lid.items():
        lid_parts.append(Part(k, opened(s) if lid_open else s, A6, finish='acrylic-lid', group='lid',
                              notes=['6 mm cast acrylic in the colour, cast 3.3 times as dense in the tint (so it reads as the cabinets\' 20 mm); cemented as a box (top over the walls, front and back over the sides), its outer edges eased R1 and polished'] if k == 'lid-top' else []))

    return [
        Part('plinth', plinth, A25, finish='acrylic', group='plinth', pieces={'slab': (plinth_soft, 'acrylic')},
             notes=['25 mm cast acrylic in the colour; edges eased R1.5 and flame- or diamond-polished; annealed after machining (about 80 C, 8 h, cooled slowly)',
                    'under it: four 8 holes 12 deep for the posts\' M6 inserts; on top: the bearing\'s flange pocket 56.4 x 6 and three 6 holes for its M4 inserts']),
        Part('base', base, A10, finish='acrylic', group='base', pieces={'slab': (base_soft, 'acrylic')},
             notes=['10 mm cast acrylic in the colour; the outer edge polished all round (it is the light\'s exit); top and bottom left as cast',
                    'from below: the light\'s slot 3 wide x 9 deep 12 in from the edge, four straight runs; the motor\'s lead groove 8 x 5 to the back-left corner; four 8 holes 7 deep for the feet\'s M6 inserts',
                    'from above: the arm\'s lead groove 8 x 5 to the back-right corner']),
        Part('led-strip', strip, Bought('led-strip-float'), finish='ledstrip', group='base', pieces={'strip': (strip, 'ledstrip'), 'edge': (edge, 'glow')},
             notes=['four straight runs (2 x 386, 2 x 296; 1.36 m) stood in the slot on their 3M tape against the inner wall, the LEDs facing out, joined at the corners with soldered jumpers; 6.5 W at full']),
        *[Part(f'post-{i + 1}', s, Machined('cast-acrylic', 'lathe'), finish='clear', group='float',
               notes=['water-clear cast acrylic rod 30, bored 6.6, faced and polished; cemented under the plinth on a jig'] if i == 0 else [])
          for i, s in enumerate(post_parts)],
        Part('bushings', union(*bush_top, *bush_bot), Bought('float-bushings'), finish='rubber', group='float'),
        Part('float-bolts', union(*bolts), Bought('float-bolts'), finish='steel', group='float',
             notes=['snug only: the nut just touches its washer, so the bushings carry the plinth and the bolt only keeps it down']),
        Part('platter', pdisc, A20, finish='acrylic', group='platter', pieces={'disc': (pdisc_soft, 'acrylic')},
             notes=['20 mm cast acrylic in the colour, 300 across; its edges eased R1.5, its rim polished and crowned 0.2 for the belt; balanced on the hub after bonding (under 2 g mm)']),
        Part('platter-hub', hub, Machined('brass', 'lathe'), finish='brass', group='platter',
             notes=['bonded into the platter with a structural acrylic adhesive; bored after, true to the spindle']),
        Part('spindle', spindle, Machined('stainless', 'lathe', setup_usd=120.0), finish='steel', group='bearing',
             notes=['440C or hardened 416, ground to 10 h5; the record spindle 7.2; a 6 cup at its foot for the ball; pressed and bonded into the hub']),
        Part('bearing-housing', housing, Machined('brass', 'lathe'), finish='brass', group='bearing',
             notes=['C360 brass; the bushes pressed in and reamed in line; filled with 2 ml of oil; hangs 8 over the base']),
        Part('bushes', bushes, Bought('bearing-bushes'), finish='brass', group='bearing', inside=True),
        Part('ball', ball, Bought('carbide-ball'), finish='steel', group='bearing', inside=True),
        Part('thrust-pad', pad, Bought('thrust-pad'), finish='black', group='bearing', inside=True),
        Part('pod-1', pods[0], A20, finish='acrylic', group='pod', pieces={'stack': (pod_soft, 'acrylic')},
             notes=['the motor\'s lead down the 10 hole and through the base']),
        Part('pod-2', pods[1], A20, finish='acrylic', group='pod', render=False),
        Part('pod-3', pods[2], A10, finish='acrylic', group='pod', render=False),
        Part('motor', motor, Bought('rega-24v-motor'), finish='black', group='pod',
             notes=['on its own rubber mounts on the pod\'s top; the bore waits on the motor in hand']),
        Part('pulley', pulley, Machined('aluminium', 'lathe'), finish='aluminium', group='pod',
             notes=[f'its belt face {pd:.2f} at {P["rpm_motor"]:g} rpm (Neo, 33.3); turned to the motor\'s measured speed; the Neo trims the rest']),
        Part('pod-pads', pod_pads, Bought('sorbothane-pod'), finish='rubber', group='pod'),
        Part('belt', belt, Bought('flat-belt'), finish='rubber', group='platter'),
        Part('feet', foot, Bought('levelling-feet'), finish='black', group='base',
             notes=['four M6 levelling feet in bonded brass inserts: level the platter on them before setting the arm']),
        Part('arm', union(arm, lift), Bought('rega-rb330'), finish='arm', group='arm', pieces={'arm': (arm, 'arm'), 'lift': (lift, 'arm')},
             notes=['its nut under the plinth (25 mm), its lead down into the float and back along the base\'s top groove; its height set with Rega\'s spacers to the cartridge\'s VTA',
                    'its own lift and rest on its own base, screwed to the plinth beside it']),
        Part('cartridge', cart, Bought('ortofon-2m-black'), finish='cartridge', group='arm'),
        Part('hinge-blocks', blocks, A20, finish='acrylic', group='lid',
             notes=['two 40 x 20 x 9.5 blocks of the colour (cut from 20 sheet on edge, faced to 9.5), each with the hinge\'s slot, on two M4 screws into inserts in the plinth\'s back edge']),
        Part('hinges', hinges, Bought('cover-hinges'), finish='black', group='lid'),
        Part('fixings', bumps, Bought('float-fixings'), finish='clear', group='lid'),
        *lid_parts,
        Part('mark', mark, Bought('laser-etch-small'), finish='accent'),
        Part('neo-psu', None, Bought('rega-neo-psu-mk2')),
        Part('led-adapter', None, Bought('led-adapter-float')),
        Part('led-dimmer', None, Bought('float-dimmer')),
        Part('bearing-fixings', None, Bought('bearing-fixings')),
        Part('bearing-oil', None, Bought('bearing-oil')),
        Part('cement', None, Bought('acrylic-cement-small')),
    ]


NOTES = [
    'The plinth: one 25 mm sheet of tinted cast acrylic (the Clouds\' own, in the colour), 450 x 360, corners R4, edges '
    'eased and polished, annealed after machining. The base: 10 mm of the same, 470 x 380, R8, its outer edge polished '
    'all round.',
    'The float: four water-clear posts (30 rod, bored 6.6) cemented under the plinth; each stands on a Sorbothane bushing '
    '(30 duro, 18.3 x 7.1 x 5.6) on the base, with a second under the base, a washer and a nyloc nut on an M6 stainless '
    'bolt into a brass insert in the plinth. Snug the nuts by hand: the bushings carry about 1.8 kg each.',
    'The light: a 24 V, 4.8 W/m strip in four straight runs standing in a 3 x 9 slot routed up into the base from below, '
    '12 in from the edge, the LEDs facing out. Behind a listed Mean Well 24 V adapter and an in-line dimmer. 6.5 W at '
    'full; the slot is open below, so the strip breathes into the 14 mm under the base.',
    'The motor stands apart: its pod (two 20 and one 10 discs, 76 across) on three soft Sorbothane pads on the base, up '
    'through an 84 hole in the plinth, 4 mm clear all round. Nothing touches the plinth from the motor but the belt.',
    'The platter: 20 mm of the same acrylic, 300 across; the brass hub bonded in, the spindle pressed and bonded into the '
    'hub, the whole balanced. The belt on its polished rim. No mat.',
    'The bearing: a turned brass housing through the plinth, flanged into a pocket in its top on three M4 screws into '
    'bonded inserts; two sintered bronze bushes; a ground stainless spindle on a 6 mm carbide ball on a PTFE pad. Oiled.',
    'Speed: Rega\'s 24 V motor driven by the Neo PSU MK2 (33/45 by a button, 0.01 rpm trim); the pulley turned to the '
    'motor\'s measured speed.',
    'Arm: Rega RB330 at Rega\'s 222 from the spindle, its nut under the 25 mm plinth; its lift on the plinth beside it; '
    'an Ortofon 2M Black. Level the platter on the four feet before setting the arm.',
    'The lid: 6 mm of the same acrylic, cemented as a box 448 x 358 x 100, on six clear bumpers, on Pro-Ject\'s two '
    'friction hinges in acrylic blocks on the plinth\'s back edge. Open, it leans back about 12 degrees past upright and '
    'needs 100 mm behind the base.',
    'The mark: EARF 40 wide laser-etched at the plinth\'s front right and filled with the colour, deeper.',
]

MATERIALS = dict(C.MATERIALS,
                 clear={'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#F4F6F5', 'radius': 0.05, 'roughness': 0.04},
                 # the lid: 6 mm cast 3.3 times as dense in the tint, so it reads as the cabinets' 20 mm walls do
                 **{'acrylic-lid': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.0075, 'roughness': 0.05}},
                 cartridge={'preset': 'satin_paint', 'color': '#0E0E0F', 'roughness': 0.35, 'specular': 0.5},
                 ledstrip={'preset': 'satin_paint', 'color': '#F2EEE6', 'roughness': 0.5, 'specular': 0.3})

PRODUCT = Product('barkhorn-turntable-float', 'Float', 'Belt-drive record player in tinted cast acrylic, floating over a lit base',
                  params=P, parts=parts, count=1, notes=NOTES, materials=MATERIALS, variants=C.VARIANTS,
                  touching=[('bushes', 'bearing-housing'), ('bushes', 'spindle'), ('float-bolts', 'post-*'),
                            ('float-bolts', 'bushings'), ('led-strip', 'base')], drawing_prefix='EF')

if __name__ == '__main__':
    d = derived(P)
    pm = math.pi * (P['platter_d'] / 2000) ** 2 * P['platter_t'] / 1000 * 1190
    print({k: (tuple(round(x, 1) for x in v) if isinstance(v, tuple) else round(v, 2)) for k, v in d.items()})
    print(f'platter {pm:.2f} kg, I {0.5 * pm * (P["platter_d"] / 2000) ** 2:.4f} kg m2')
    S, M = d['S'], d['M']
    print('pulley to spindle', round(math.hypot(M[0] - S[0], M[1] - S[1]), 1))
