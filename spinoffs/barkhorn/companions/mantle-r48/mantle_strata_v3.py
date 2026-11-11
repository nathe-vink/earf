"""Mantle, proposal A, v3: STRATA FLOAT, the detail pass (round 48). The coordinator's duels (v2 over v1 3-1; v2 and
Outcrop 2-2, distinctiveness 6.0 to 4.75): every judge named the same details under the float, and v3 answers them;
v2 stays as it was:
1. the base recedes: stock smoked 2064, 12.7 (heavier, against the deck's top-heaviness), the deck's corner radius, the
   same 35 setback on all four sides; the strip's channel is lost in the smoke, and the whole edge glows;
2. solid posts: turned 303 stainless, polished, 30 across; each bonded under the deck in a 2 mm seat (a structural
   methacrylate, Plexus MA310 kind) and held from below by its foot's M8 stud through the base into a tapped hole in
   the post; no fixing shows; the isolation is the foot's Sorbothane pad;
3. the mark is a polished recess, tone on tone, on the deck's back edge.
The shared audit fixes (2026-11-01, STOCK-AND-AUDIT.md 3; proposals until the owner signs): the motor hard-mounted as
Rega fits it; the platter's screws up through the hub into bonded inserts; the bearing on a disc spring, 1.0 ml of
oil, a vented 440C spindle; the pulley for 300 rpm pending the bench test; a 4PDT bypass; no isolation claim for the
feet.
Strata's own audit items (2026-11-01, after the owner picked A; proposals until signed): a brass rear plate on the
base's back edge, under the deck's overhang, carries the line out, the earth post, the 4PDT, the light's switch, the
two DC inlets and the Neo's inlet, with the rating engraved (drawing: strata_rear.py); the light is a 5 mm strip of
5 W/m or less in four straight runs in a 7.4 x 7 slot, on a listed Class 2 adapter of 12 W, with no PWM dimmer inside.
The light up through the acrylic (2026-11-03, the owner: the underglow must not be thrown down onto the floor but cast
through the acrylic, so the piece glows from within; a proposal until signed): the deck is edge-lit as a sign is. The
strip lies in a groove routed into the deck's underside 10 in from its edge, facing up into the slab; the groove's
ceiling is bead-blasted, so the light spreads into the acrylic, which carries it to the satin outer edge. Its black
channel closes the groove below, so nothing falls on the shelf but a faint spill, and nothing bright shows. The base
has no light now; its slot is gone. (A strip on the base's top facing up was tried first: from any normal eye height
it shows through the float's gap as a bright line.)
No light (2026-11-10, the owner: "Forget the lights on mantle"; the coordinator: Mantle has no light of any kind): the
deck's groove, its channel and strip, the adapter, the plate's switch and 24 V inlet, and their wiring are gone. The
deck as signed, the base the signed solid Smoke 2074, the posts satin black; the deck's underside bead-blasted satin
(the day win from the light proposals: it scatters the room's light up through the deck); the bearing's visible parts
(housing, nut, washer) black to match the posts; and (2026-11-11) the platter's hub and its six inserts black too, so no
brass shows anywhere (the rear plate, hidden under the deck, stays brass); and (2026-11-11) every visible piece of
hardware satin black: the arm puck and the pulley black anodized, the feet hot black oxide, the screws, studs and disc
spring black oxide, the cartridge's screws and washers black, the arm's counterweight and trim black (to confirm with
Rega). Bright by necessity: the spindle's tip, the cartridge's cantilever, pins and diamond (and, hidden, the ball and
thrust plate). The light notes above and below are history.

v2's notes follow.

Mantle, proposal A, v2: STRATA FLOAT, the second pass (round 48). The coordinator's blind head-to-head (Strata Float
over Outcrop, 3-1, distinctiveness 6.9 to 3.9: "the floating glass turntable") found the same faults every time, and
this pass fixes them; v1 (mantle_strata.py) stays as it was:
1. one grid of round parts: the feet stand directly under the posts;
2. the base is subordinate: 35 mm in from the deck all round and 9.5 thick, so the deck overhangs it and floats;
3. each tier reads as one slab: the deck is two clear 12.7 sheets with one bond line, flush; the base is one sheet;
4. no screws through the clear posts: each post is bonded at both ends, and the feet's studs go into blind inserts
   drilled up through the base into the posts' feet;
5. the mark is small and etched into the deck's front edge, not printed on its top.
The light's strip sits in a black anodized U-channel in the base's slot, whose closed back hides it from above.

v1's notes follow.

 The baseline's architecture kept (a squared plinth floating over a lit
base, the hinged lid, the record player the owner asked for: "squared, similar to a Debut or Orbit, a clear body and a
matching cover"), every fault the fresh review found fixed, and the plinth and base laminated as strata.

What changes from the baseline (turntable_float.py), and why:
- **The plinth** is laminated from stock sheet, as round 43 found it must be for a prototype anyway: tinted 3 (a ring
  20 wide round a clear inlay) / clear 12.7 / tinted 3 (ring) / clear 5.6 = 24.3. The bond lines become the design: two
  dark contour lines round a clear slab, the interior clear so the bearing and the motor show through it.
- **The float is rigid now.** Each clear post is bonded under the plinth and bolted to the base on a torqued M6 stud
  (the review: on Sorbothane bushings it sat at 25-36 Hz, in the speakers' feedback band). Isolation is in the four
  feet. It still floats to the eye.
- **The motor hangs from the plinth** on Rega's own grommets, in the float's gap (the review: the pod on the shelf
  tipped under the belt, and its pulley's height ran through the feet and the bushings).
- **The base** is clear 12.7 with a tinted 3 ring on it; the light's slot is 6 deep from below, 25 in from the edge, in
  continuous runs round all four sides (the review: 1 mm of acrylic over a 9 mm slot in 10 mm sheet). The black band
  is printed on the clear before lamination, so it is inside the stack and cannot wear.
- **The lid** is 3 mm 2064 (1/8 in stock), 1.1 kg, within the Debut hinges' rating (the review: 2.2 kg was twice it).
- **The bearing** is threaded and clamped (no inserts beside the bore); the platter is laminated on a screwed hub; the
  phono stage keeps its own listed 18 V adapter (no shared supply with the dimmer).

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/mantle-r48/mantle_strata.py \
        --out spinoffs/barkhorn/companions/mantle-r48/out-strata
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mantle_outcrop as B                                             # noqa: E402  (the stock sheets, the arm, the hull)
from mantle_outcrop import *                                           # noqa: E402,F403

P = dict(
    W=450.0, D=360.0, R=4.0,                  # the plinth's top: the baseline's footprint
    step=0.0,
    plinth=(('clear', 12.7), ('clear', 12.7)),
    base=(('tint', 12.7),), base_inset=35.0,
    margin=10.0, Rb=6.0, post_material='stainless',
    feet_h=16.0, gap=40.0,
    posts=((145.0, 75.0), (305.0, 75.0), (145.0, 285.0), (305.0, 285.0)), post_d=30.0,
    spindle=(200.0, 168.0),
    platter_d=300.0, platter_t=21.0, lift=6.0,
    platter_lams=(('tint', 3.0), ('clear', 12.7), ('tint', 5.6)),
    arm_r=222.0, arm_x=395.0, L_eff=236.5, offset=21.55, rest_r=168.0,
    puck_d=84.0, puck_t=12.0,
    motor_d=184.7, motor_x=64.0, motor_pocket=76.0,
    rpm_motor=300.0,                                  # PROPOSAL until benched: the US Neo at 60 Hz (STOCK-AND-AUDIT.md 3.1)
    edge_chamfer=1.0,                                 # edge option C (the owner, 2026-11-11): the outer edges of deck and base, 1 mm, polished
    lid_t=3.0, lid_h=100.0, bumper=5.0,
    housing_d=30.0, flange_d=50.0, flange_t=5.0,
    tint_ring=20.0,
)


def derived(P):
    m = P['margin']
    d = {}
    z = P['feet_h']
    base = []
    for kind, t in P['base']:
        base.append(dict(kind=kind, t=t, z0=z, z1=z + t, inset=0.0)); z += t
    b1 = z
    z0 = b1 + P['gap']
    lams, z, ins = [], z0, 0.0
    for i, (kind, t) in enumerate(P['plinth']):
        lams.append(dict(kind=kind, t=t, z0=z, z1=z + t, inset=ins)); z += t
        if kind == 'clear':
            ins += P['step']
    top = z
    ins_top = lams[-1]['inset']
    # the plinth's frame: its bottom lamina's corner at (m, m); the top lamina inset by ins_top
    W0, D0 = P['W'] + 2 * ins_top, P['D'] + 2 * ins_top
    o = m + ins_top
    S = (o + P['spindle'][0], o + P['spindle'][1])
    ay = math.sqrt(P['arm_r'] ** 2 - (P['arm_x'] - P['spindle'][0]) ** 2)
    A = (o + P['arm_x'], S[1] + ay)
    mx = o + P['motor_x']
    M = (mx, S[1] + math.sqrt(P['motor_d'] ** 2 - (mx - S[0]) ** 2))
    pz0 = top + P['lift']; pz1 = pz0 + P['platter_t']
    r_belt = P['platter_d'] / 2 + 0.3
    d.update(base=base, b0=P['feet_h'], b1=b1, z0=z0, lams=lams, top=top, W0=W0, D0=D0, o=o, S=S, A=A, M=M, pz0=pz0, pz1=pz1,
             belt_z=pz0 + 9.0, record_z=pz1 + 1.8, Wb=W0 - 2 * P['base_inset'], Db=D0 - 2 * P['base_inset'],
             pulley_d=round(2 * r_belt * (100.0 / 3.0) / P['rpm_motor'] - 0.6, 2))
    dx, dy = S[0] - A[0], S[1] - A[1]
    dd = math.hypot(dx, dy); L = P['L_eff']; r = P['rest_r']
    a = (L * L - r * r + dd * dd) / (2 * dd); h = math.sqrt(L * L - a * a)
    bx, by = A[0] + a * dx / dd, A[1] + a * dy / dd
    st = min([(bx + h * dy / dd, by - h * dx / dd), (bx - h * dy / dd, by + h * dx / dd)], key=lambda p: p[1])
    d['stylus'] = st
    d['rest_deg'] = math.degrees(math.atan2(st[1] - A[1], st[0] - A[0]))
    d['lid_z0'] = top + P['bumper']
    # for the render (scene.py reads these names)
    d['W1'], d['D1'] = d['Wb'], d['Db']
    d['cover'], d['cover_top'] = [], []
    d['height'] = top + P['bumper'] + P['lid_h']
    return d


D = derived(P)


def poutline(P, D, inset, extra=0.0):
    m = P['margin']
    return rounded_rect(D['W0'] - 2 * inset + 2 * extra, D['D0'] - 2 * inset + 2 * extra, max(P['R'] + 2 - inset, 2.0) + extra,
                        cx=m + D['W0'] / 2, cy=m + D['D0'] / 2)


# the rear plate's hardware (name, x, z, hole, outside d, outside l, inside d, inside l), in the model frame: x across,
# z up from the shelf, through the plate along y. Upper row: line out, the earth post, the 4PDT; lower row: the S2's
# 18 V inlet (2.1 mm), the Neo's (no light since 2026-11-10: its SPST and 24 V inlet are gone)
REAR_HW = [('OUT L', 322, 52, 6.5, 10, 10, 9, 15), ('OUT R', 340, 52, 6.5, 10, 10, 9, 15), ('EARTH', 360, 52, 4.5, 10, 15, 10, 12),
           ('PHONO / BYPASS', 384, 52, 6.4, 6.4, 16, 13, 14),
           ('18 V', 322, 37, 8.0, 11, 2, 9, 16), ('MOTOR', 370, 37, 12.0, 15, 4, 14, 15)]
REAR_PLATE = dict(x0=308.0, x1=418.0, screws=(318.0, 408.0))


def boutline(P, D, inset=0.0):
    m = P['margin']
    return rounded_rect(D['Wb'] - 2 * inset, D['Db'] - 2 * inset, max(P['Rb'] - inset, 2.0), cx=m + D['W0'] / 2, cy=m + D['D0'] / 2)


def parts(P):
    from build123d import Pos, Rot, Sphere, Cone
    D = derived(P)
    S, A, M = D['S'], D['A'], D['M']
    m, top, b0, b1, z0 = P['margin'], D['top'], D['b0'], D['b1'], D['z0']
    Wb, Db = D['Wb'], D['Db']
    tint = {t: Sheet('trucast-tint', t, face='+z') for t in (3.0, 5.6, 9.5, 12.7)}
    clr = {t: Sheet('trucast-clear', t, face='+z') for t in (3.0, 5.6, 9.5, 12.7)}
    posts = [(m + D['o'] - m + x, m + D['o'] - m + y) for x, y in P['posts']]
    rw = P['tint_ring']

    # ---- the plinth's cuts ----
    cuts = [cyl('z', S, P['housing_d'] + 0.4, z0 - 1, top + 1), cyl('z', S, P['flange_d'] + 0.4, top - P['flange_t'], top + 1)]
    pd, pt = P['puck_d'], P['puck_t']
    cuts += [cyl('z', A, pd + 0.4, top - pt, top + 1), cyl('z', A, 56.0, z0 - 1, top - pt + 0.5)]
    puck_screws = [(A[0] + 35 * math.cos(math.radians(a)), A[1] + 35 * math.sin(math.radians(a))) for a in (90, 210, 330)]
    cuts += [cyl('z', c, 7.0, z0 - 1, top - pt + 0.5) for c in puck_screws]
    # the motor's pocket through the plinth: the plate screwed hard to a shoulder 6 down (Rega's method), the motor below in the gap
    cuts += [cyl('z', M, P['motor_pocket'] + 16, top - 6, top + 1), cyl('z', M, P['motor_pocket'], z0 - 1, top + 1)]
    cuts += [cyl('z', (M[0] + 42 * math.cos(math.radians(a)), M[1] + 42 * math.sin(math.radians(a))), 4.6, top - 14, top - 5.5)
             for a in (30, 150, 270)]   # the plate's three M3 inserts
    cuts += [cyl('z', p, P['post_d'] + 0.3, z0 - 1, z0 + 2.0) for p in posts]          # the posts' 2 mm bonded seats
    hx = [m + 80.0, m + D['W0'] - 80.0]
    cuts += [cyl('y', (x + s_ * 10, (z0 + top) / 2), 6.0, m + D['D0'] - 14, m + D['D0'] + 1) for x in hx for s_ in (-1, 1)]

    def chamf(sol, ends):
        # edge option C (the owner, 2026-11-11): a 1 mm even chamfer on the outer edges, polished; the edge itself as signed
        from build123d import chamfer, Axis
        if not ends:
            return sol
        g = sol.edges().group_by(Axis.Z)
        es = (list(g[0]) if 'bottom' in ends else []) + (list(g[-1]) if 'top' in ends else [])
        return chamfer(es, length=P['edge_chamfer'])

    def cut(s, cs):
        for c in cs:
            s = s - c
        return s

    out = []
    one = []
    for i, l in enumerate(D['lams']):
        ends = (['bottom'] if i == 0 else []) + (['top'] if i == len(D['lams']) - 1 else [])   # the stack's outer edges only
        s = cut(chamf(prism(poutline(P, D, l['inset']), 'z', l['z0'], l['z1']), ends), cuts)
        one.append(chamf(prism(poutline(P, D, l['inset']), 'z', l['z0'], l['z1']), ends))
        if l['kind'] == 'tint':
            band = prism(poutline(P, D, l['inset'] + rw), 'z', l['z0'] - 1, l['z1'] + 1)
            out.append(Part(f'plinth-L{i + 1}', s - band, tint[l['t']], finish='acrylic', group='plinth', render=False,
                            notes=['the plinth: four laminae of stock sheet (tinted 3 ring / clear 12.7 / tinted 3 ring / clear 5.6), each tinted lamina a 20 wide ring round a clear inlay cut from the same file; cemented in one vacuum press with ACRIFIX 2R 0190, annealed, faces fly-cut, the stepped outline finish-routed, edges diamond-polished, holes left satin'] if i == 0 else []))
            out.append(Part(f'plinth-L{i + 1}-inlay', s & band, clr[3.0], finish='clear', group='plinth', render=False))
        else:
            # a plain lamina ('clear' in P: no inlay ring): since the stock line (2026-11-01), the flavor's stock tinted sheet
            out.append(Part(f'plinth-L{i + 1}', s, tint[l['t']], finish='clear', group='plinth', render=False,
                            notes=['the deck: two 12.7 sheets of the line\'s stock tint in the flavor\'s code (a lighter custom pour is an open question for the owner), cemented flush with ACRIFIX 2R 0190 in a vacuum press: one bond line, at mid-edge; annealed, faces fly-cut, the outline finish-routed as one; the outer edges chamfered 1 mm even and the chamfers polished (edge option C, the owner 2026-11-11); the outer edge fine bead-blasted to a satin (round 48\'s duels: a polished thick edge refracts the room in patches, a satin one collects light evenly), the top face left glassy; the underside fine bead-blasted to a satin as the edge (2026-11-10, the day win from the light proposals: it scatters the room\'s light up through the deck; masked round the posts\' seats and the bearing\'s washer)'] if i == 0 else []))
    plinth_one = cut(union(*one), cuts)
    out[0].pieces = {'stack': (plinth_one, 'acrylic-strata')}; out[0].render = True

    # ---- the base: one 12.7 sheet, 35 in from the deck, solid (no light); the feet under the posts ----
    feet = list(posts)
    # each foot's M8 brass insert in a blind hole drilled up through the base into the bonded post's foot (14 deep)
    bcuts = [cyl('z', f, 8.5, b0 - 1, b1 + 1) for f in feet]        # the feet's studs, clear through
    # ---- the rear plate: 2 mm brass on the base's back edge at the back right, under the deck's 35 overhang ----
    yb = m + D['D0'] / 2 + Db / 2                                             # the base's back edge
    zp = (b0 + b1) / 2                                                         # the plate's two M3 screws, into the edge
    RP = dict(x0=REAR_PLATE['x0'], x1=REAR_PLATE['x1'], z0=b0 + 1.0, z1=z0 - 4.0)
    rp_screws = [(x, zp) for x in REAR_PLATE['screws']]
    bcuts += [cyl('y', c, 4.6, yb - 10, yb + 0.5) for c in rp_screws]         # brass M3 inserts, bonded into the edge
    RPH = [h[1:] for h in REAR_HW]
    bl0 = D['base'][0]
    base_c = cut(chamf(prism(boutline(P, D), 'z', bl0['z0'], bl0['z1']), ['top', 'bottom']), bcuts)
    out += [Part('base-L1', base_c, tint[12.7], finish='acrylic', group='base', render=False,
                 pieces={'stack': (base_c, 'acrylic-base')},
                 notes=['the base: one 12.7 sheet of stock Smoke 2074 (Dark Gray) in every flavor (it recedes; the color is the deck\'s), the deck\'s corner radius, 35 in from the deck on all four sides; its outer edge diamond-polished, its outer edges chamfered 1 mm and polished (edge option C, 2026-11-11)',
                        'solid: no light anywhere in Mantle since 2026-11-10 (the owner); two M3 inserts in the back edge for the rear plate',
                        'four 8.5 holes through it under the posts, for the feet\'s M8 studs into the posts']),]
    out[-1].render = True
    # ---- the posts: solid 303 stainless, satin black (hot black oxide, the owner 2026-11-10); bonded into a 2 mm seat under the deck, a tapped M8 x 16 hole from below ----
    for i, p in enumerate(posts):
        out.append(Part(f'post-{i + 1}', cyl('z', p, P['post_d'], b1, z0 + 2.0) - cyl('z', p, 6.8, b1 - 1, b1 + 16), Machined('stainless', 'lathe', stock=(35.0, 35.0, 46.0)),
                        finish='black', group='float', notes=['solid 303 stainless 30 x 42, turned, ends faced; finished satin black (the owner, 2026-11-10: black posts, the lamps\' satin black #18181A): hot black oxide for stainless, satin, oiled (stainless kept for the load and the bond; black oxide over black chrome for its satin, not mirror, finish); tapped M8 x 16 from below; bonded 2 mm up into a seat under the deck with a structural methacrylate (Plexus MA310 kind, which bonds acrylic to stainless); the foot\'s stud holds it to the base from below: nothing shows'] if i == 0 else []))

    # ---- the bearing, platter, hub, spindle (as Outcrop) ----
    hz0 = z0 - 20.0
    ft = P['flange_t']
    housing = (cyl('z', S, P['housing_d'], hz0, top - ft) + cyl('z', S, P['flange_d'], top - ft, top)) - cyl('z', S, 14.0, hz0 + 4, top + 1)
    # under the plinth, down from it: a brass washer 64 x 31 x 3, one DIN 2093 C 63 x 31 x 1.8 disc spring (set about 3.0), the nut
    cwasher = cyl('z', S, 64.0, z0 - 3.0, z0) - cyl('z', S, 31.0, z0 - 4, z0 + 1)
    dspring = cyl('z', S, 63.0, z0 - 6.0, z0 - 3.0) - cyl('z', S, 31.0, z0 - 7, z0 - 2)
    nut = cyl('z', S, 46.0, z0 - 13.5, z0 - 6.0) - cyl('z', S, P['housing_d'] + 0.2, z0 - 14.5, z0 - 5)
    plate = cyl('z', S, 13.8, hz0 + 4, hz0 + 6)
    ball_c = hz0 + 9
    ball = Pos(S[0], S[1], ball_c) * Sphere(3.0)
    bushes = union(cyl('z', S, 14.0, hz0 + 12, hz0 + 24) - cyl('z', S, 10.0, hz0 + 11, hz0 + 25),
                   cyl('z', S, 14.0, top - 16, top - 6) - cyl('z', S, 10.0, top - 17, top - 5))
    pz0, pz1 = D['pz0'], D['pz1']
    hub = (cyl('z', S, 70.0, pz0 - 5, pz0) + cyl('z', S, 40.0, pz0, pz0 + 12)) - cyl('z', S, 10.0, pz0 - 6, pz0 + 13)
    spindle = cyl('z', S, 10.0, ball_c + 3, pz0 + 12) + cyl('z', S, 7.2, pz0 + 12, pz1 + 15)
    hub_screws = [(S[0] + 28 * math.cos(math.radians(60 * k + 30)), S[1] + 28 * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    platter = cyl('z', S, P['platter_d'], pz0, pz1) - cyl('z', S, 40.2, pz0 - 1, pz0 + 12.2) - cyl('z', S, 8.0, pz0, pz1 + 1)
    for c in hub_screws:   # as Outcrop's: up through the hub into bonded brass inserts, no head on acrylic
        platter = platter - cyl('z', c, 5.6, pz0 - 1, pz0 + 8)
        hub = hub - cyl('z', c, 4.5, pz0 - 6, pz0 + 1) - cyl('z', c, 7.8, pz0 - 6, pz0 - 2.6)
    screws = union(*[cyl('z', c, 4.0, pz0 - 2.8, pz0 + 7) + cyl('z', c, 7.4, pz0 - 5.0, pz0 - 2.8) for c in hub_screws])
    pinserts = union(*[cyl('z', c, 5.6, pz0, pz0 + 8) - cyl('z', c, 4.0, pz0 - 1, pz0 + 9) for c in hub_screws])

    # ---- the motor, screwed hard to the plinth (Rega's method), hanging into the gap ----
    bz = D['belt_z']
    mt = top - 3
    mplate = cyl('z', M, P['motor_pocket'] + 14, mt - 3, mt) - cyl('z', M, 26, mt - 4, mt + 1)
    motor = union(cyl('z', M, 50.0, mt - 3 - 30, mt - 3), cyl('z', M, 4.0, mt - 3, bz + 9))
    mscrews = union(*[cyl('z', (M[0] + 42 * math.cos(math.radians(a)), M[1] + 42 * math.sin(math.radians(a))), 3.0, top - 13, mt + 1.6)
                      for a in (30, 150, 270)])
    pdia = D['pulley_d']
    pulley = (cyl('z', M, pdia, bz - 5, bz + 5) + cyl('z', M, pdia + 6, bz + 5, bz + 7)) - cyl('z', M, 4.0, bz - 6, bz + 8)
    R = P['platter_d'] / 2
    belt = prism(B_hull([(S[0], S[1], R + 0.65), (M[0], M[1], pdia / 2 + 0.65)]), 'z', bz - 2.5, bz + 2.5) - \
        prism(B_hull([(S[0], S[1], R + 0.05), (M[0], M[1], pdia / 2 + 0.05)]), 'z', bz - 3, bz + 3)

    puck = cyl('z', A, pd, top - pt, top) - cyl('z', A, 24.0, top - pt - 1, top + 1)
    for c in puck_screws:
        # countersunk 90 deg for M5 ISO 10642 heads (dk 10), flush with the puck's top (2026-11-11; it was a 10 x 3 counterbore)
        puck = puck - cyl('z', c, 5.5, top - pt - 1, top + 1) - Pos(c[0], c[1], top - 0.7) * Cone(2.75, 6.15, 3.4)   # r 2.75 at 2.4 down to 5.15 at the top: 90 deg, 10.3 across
    arm, lift, cart = B.arm_solids(P, D)

    foot = union(*(union(cyl('z', f, 36.0, 4, 12), cyl('z', f, 30.0, 12, b0 - 0.5)) for f in feet))
    pads = union(*(cyl('z', f, 36.0, 0, 4) for f in feet))
    fstuds = union(*(cyl('z', f, 8.0, b0 - 0.5, b1 + 15) for f in feet))

    # ---- the phono stage on the base under the platter's back, its own adapter; the rear box ----
    px0, py0 = m + D['W0'] / 2 - 51.5, m + D['D0'] / 2 + Db / 2 - 125.0
    phono = box(px0, py0, b1 + 1.5, px0 + 103, py0 + 115, b1 + 37.5)
    felts = union(*[cyl('z', (px0 + x, py0 + y), 10.0, b1 + 0.15, b1 + 1.5) for x in (12, 91) for y in (12, 103)])
    # the rear plate and its hardware (its plugs and the S2's project behind the base, under the deck's overhang)
    rplate = box(RP['x0'], yb, RP['z0'], RP['x1'], yb + 2.0, RP['z1'])
    for x, z, hole, *_ in RPH:
        rplate = rplate - cyl('y', (x, z), hole, yb - 1, yb + 3)
    for c in rp_screws:
        rplate = rplate - cyl('y', c, 3.4, yb - 1, yb + 3)
    rhw = union(*[cyl('y', (x, z), do, yb + 2.0, yb + 2.0 + lo) + cyl('y', (x, z), di, yb - li, yb) + cyl('y', (x, z), hole - 0.2, yb - 0.5, yb + 2.5)
                  for x, z, hole, do, lo, di, li in RPH],
                *[cyl('y', c, 3.0, yb - 8, yb + 2.0) + cyl('y', c, 5.6, yb + 2.0, yb + 3.6) for c in rp_screws])

    # ---- the mark: EARF, 18 wide, laser-etched into the deck's front edge, low in its lower sheet, frosted ----
    import turntable as T_
    mk = T_.mark_top(18.0, (0.0, 0.0), 0.0, 0.1)
    mk = Pos(m + 40.0, m + D['D0'] + 0.02, z0 + 3.0) * Rot(0, 0, 180) * Rot(90, 0, 0) * mk
    mark_part = Part('mark', mk, Bought('laser-etch-small'), finish='etch-tone')

    # ---- the lid: 3 mm 2064, a top and four walls cemented, on Pro-Ject's hinges in blocks on the plinth's back ----
    t, lz0 = P['lid_t'], D['lid_z0']
    lz1 = lz0 + P['lid_h']
    x0, y0, x1, y1 = m + 1, m + 1, m + D['W0'] - 1, m + D['D0'] - 1
    lid = {'lid-top': box(x0, y0, lz1 - t, x1, y1, lz1), 'lid-front': box(x0, y0, lz0, x1, y0 + t, lz1 - t),
           'lid-back': box(x0, y1 - t, lz0, x1, y1, lz1 - t), 'lid-left': box(x0, y0 + t, lz0, x0 + t, y1 - t, lz1 - t),
           'lid-right': box(x1 - t, y0 + t, lz0, x1, y1 - t, lz1 - t)}
    blocks = union(*(box(x - 20, m + D['D0'], z0 + 2.5, x + 20, m + D['D0'] + 9.5, top - 2.5) for x in hx))
    hinges = union(*(union(box(x - 15, m + D['D0'], top - 2.5, x + 15, m + D['D0'] + 8, lz0), box(x - 15, y1, lz0, x + 15, m + D['D0'] + 8, lz0 + 22))
                     for x in hx))

    out += [
        Part('platter', platter, Machined('cast-acrylic', 'lathe', stock=(310.0, 310.0, 22.0), setup_usd=80.0), finish='acrylic', group='platter',
             pieces={'disc': (platter, 'acrylic-strata-platter')},
             notes=['tinted 3 / clear 12.7 / tinted 5.6 cemented, annealed, turned to 300 x 21 as Outcrop\'s; six blind 5.6 holes from below for bonded brass M4 inserts, the record side unbroken']),
        Part('platter-hub', hub, Machined('brass-leadfree', 'lathe'), finish='black', group='platter',
             notes=['lead-free brass, turned; black nickel plated, satin, as the bearing (2026-11-11: no brass in sight; it shows through the platter\'s clear lamina), the 10 bore masked']),
        Part('platter-screws', screws, Bought('platter-screws'), finish='black', group='platter',
             notes=['six M4 x 10 up through the hub\'s flange into the inserts, 0.6 N m, no thread-locker near acrylic']),
        Part('platter-inserts', pinserts, Bought('platter-inserts'), finish='black', group='platter',
             notes=['black nickel plated with the hub (2026-11-11), threads masked or chased after']),
        Part('spindle', spindle, Machined('stainless-440c', 'lathe', setup_usd=120.0), finish='steel', group='bearing',
             notes=['as Outcrop\'s: 440C, 58 HRC, ground 10 g5; a vent flat 1.0 x 0.3 along the journals']),
        Part('bearing-housing', housing, Machined('brass-leadfree', 'lathe'), finish='black', group='bearing',
             notes=['as Outcrop\'s: M30 x 1.5, clamped by its nut on a disc spring and a brass washer under the plinth (about 1.5 kN), hanging 20 into the float; its visible parts (housing, nut, washer) black (2026-11-10, to match the posts): brass, black nickel plated, satin; 1.0 ml of oil']),
        Part('bearing-nut', nut, Machined('brass-leadfree', 'lathe'), finish='black', group='bearing'),
        Part('bearing-spring', dspring, Bought('bearing-disc-spring'), finish='black', group='bearing'),
        Part('bearing-washer', cwasher, Machined('brass-leadfree', 'lathe'), finish='black', group='bearing'),
        Part('bushes', bushes, Bought('bearing-bushes-solid'), finish='black', group='bearing', inside=True,
             notes=['bronze, unplated (their bores are the bearing); pressed inside the black housing and never seen: drawn black so no scene shows brass']),
        Part('ball', ball, Bought('carbide-ball'), finish='steel', group='bearing', inside=True),
        Part('thrust-plate', plate, Bought('thrust-plate'), finish='steel', group='bearing', inside=True),
        Part('motor-plate', mplate, Sheet('aluminium', 3, face='+z'), finish='black', group='motor',
             notes=['3 mm 5052, black anodized, 90 across, hard on the shoulder on three M3 screws into inserts, as Rega fits its motor (no grommets)']),
        Part('motor', motor, Bought('rega-24v-motor'), finish='black', group='motor'),
        Part('motor-screws', mscrews, Bought('motor-mount-screws'), finish='black', group='motor'),
        Part('pulley', pulley, Machined('aluminium', 'lathe'), finish='black', group='motor',
             notes=['black anodized after turning (2026-11-11), the belt face sized for the coat (about 0.02 on the diameter)', f'belt face {pdia:.2f} at {P["rpm_motor"]:g} rpm: PROPOSAL, not turned until the bench test (STOCK-AND-AUDIT.md 3.1)']),
        Part('belt', belt, Bought('flat-belt-core'), finish='rubber', group='platter'),
        Part('arm-puck', puck, Machined('aluminium', 'lathe'), finish='black', group='arm', notes=['black anodized after turning, satin (2026-11-11: no bright hardware); its three M5 screws black oxide']),
        Part('arm', union(arm, lift), Bought('rega-rb330'), finish='arm', group='arm'),
        Part('cartridge', cart, Bought('ortofon-2m-black'), finish='cartridge', group='arm'),
        Part('feet', foot, Machined('stainless', 'lathe', stock=(40.0, 40.0, 4 * 18.0)), finish='black', group='feet',
             notes=['four, directly under the posts (one grid), turned 303 stainless, hot black oxide satin with the posts (2026-11-11), 36 x 8 with a 30 neck, on M8 studs through the base into the posts, levelled and locked; Sorbothane under. They locate and level; no isolation is claimed']),
        Part('foot-pads', pads, Bought('foot-sorbothane'), finish='rubber', group='feet'),
        Part('foot-studs', fstuds, Bought('foot-studs'), finish='black', group='feet'),
        Part('phono-stage', phono, Bought('phono-box-s2'), finish='aluminium-dark', group='phono'),
        Part('phono-pads', felts, Bought('phono-felts'), finish='rubber', group='phono'),
        Part('rear-plate', rplate, Sheet('brass-sheet', 2, face='+y') if 'brass-sheet' in SHEETS else Machined('brass-leadfree', 'cnc-mill'), finish='black', group='rear',
             notes=['2 mm lead-free brass, black nickel plated satin with the bearing\'s lot (2026-11-11), legends and rating laser-engraved through to the brass and filled white, 110 x 47.7, on the base\'s back edge at the back right, 35 in from the deck\'s back edge: two M3 button screws into brass inserts bonded in the edge',
                    'upper row: line out L and R, the 4 mm earth post (the star), the 4PDT stage / bypass; lower row: 18 V for the phono stage (2.1 mm), the Neo\'s motor inlet (no light since 2026-11-10)',
                    'the rating engraved along its foot and filled white (strata_rear.py has the text and the wiring and earth drawing)']),
        Part('rear-hardware', rhw, Bought('strata-rear-hardware-nolight'), finish='black', group='rear'),
        Part('hinge-blocks', blocks, Machined('cast-acrylic', 'cnc-mill', stock=(45.0, 15.0, 2 * 29.0)), finish='acrylic', group='lid',
             notes=['two 40 x 9.5 blocks of the color, each with the hinge\'s slot 3.2 x 12 x 18 deep, on two M4 screws into inserts in the plinth\'s back edge (horizontal, in shear)']),
        Part('hinges', hinges, Bought('cover-hinges'), finish='black', group='lid', render=False),
        *[Part(k, s, Sheet('trucast-tint', 3.0), finish='acrylic-lid', group='lid', render=False,
               notes=['3 mm stock sheet in the flavor\'s code (1/8 in), cemented as a box with ACRIFIX 2R 0190; 1.1 kg, within the Debut hinges\' rating; outer edges eased R0.5 and polished'] if k == 'lid-top' else [])
          for k, s in lid.items()],
        mark_part,
        Part('inserts', None, Bought('core-inserts')),
        Part('wiring', None, Bought('core-wiring')),
        Part('neo-psu', None, Bought('rega-neo-psu-mk2')),
        Part('bearing-oil', None, Bought('bearing-oil')),
        Part('cement', None, Bought('acrylic-cement-2r')),
        Part('black-plating', None, Bought('black-nickel-plating')),
        Part('black-hardware', None, Bought('black-hardware-finishes')),
        Part('edge-chamfer', None, Bought('edge-chamfer-pass')),
    ]
    return out


def B_hull(circles, n=360):
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


NOTES = [
    'The deck (as built since v2): two 12.7 sheets of the flavor\'s stock tint, cemented flush with ACRIFIX 2R 0190 in a vacuum press (25.4, '
    'one bond line at mid-edge), annealed, fly-cut, the outline routed as one; the outer edge bead-blasted satin, the faces glassy. '
    '450 x 360, corners R4. (v1\'s tinted-ring / clear-inlay strata, 24.3, are gone.)',
    'The base: one 12.7 sheet of stock Smoke 2074, 380 x 290, corners R6, 35 in from the deck all round; the deck floats 40 over it.',
    'The float: four solid 303 stainless posts bonded into 2 mm seats under the plinth, held to the base by the feet\'s M8 studs: '
    'rigid. The four feet (stainless on Sorbothane, levelled and locked) locate and level it; no isolation is claimed. For isolation, a platform at 3-5 Hz.',
    'No light (2026-11-10, the owner): no strip, channel, groove, adapter, switch or 24 V inlet. The deck\'s underside '
    'bead-blasted satin as its edge (the day win from the light proposals). The phono stage runs from its own listed adapter.',
    'The rear plate: 2 mm brass on the base\'s back edge, under the deck\'s overhang; line out, earth post (the star earth), '
    '4PDT stage / bypass, the S2\'s 18 V inlet and the Neo\'s; the rating engraved. Wiring and earth: strata_rear.py.',
    'The motor: Rega 24 V on its plate, screwed hard to a shoulder in a pocket through the plinth as Rega fits it, below it in the float. '
    'The pulley waits for the motor\'s speed measured on the US Neo (300 rpm expected at 60 Hz).',
    'The bearing, platter, arm puck and phono stage as Outcrop\'s (mantle_outcrop.py): a disc spring under the bearing\'s nut, '
    '1.0 ml of oil, a vented 440C spindle; the platter screwed from below into bonded inserts; a 4PDT bypass.',
    'Before the first sample: with the arm in hand, check its counterweight clears the lid\'s back wall.',
    'The lid: 3 mm 2064, 1.1 kg, on Pro-Ject\'s friction hinges.',
]

# The engine's look (studio/products/mantle-strata-v3.json, written by the build; the room and other lanes drop it into
# their scenes). The line's stock cast tints (2026-11-01): `deep` is the color light has after `radius` m, held per
# stock sheet as scene.py's STOCK_HELD (each code's TruCast TT at 1/2 in, two faces' Fresnel out). The deck, the hinge
# blocks and the lid are through-tinted in the flavor; the platter is tinted 3 / clear 12.7 / tinted 5.6, so its one
# material carries 21 mm at 8.6 mm's tint (radius 0.024); the base is always stock Smoke 2074. The engine has no
# per-face finish, so the deck's satin outer edge and the polished top read as one polished slab here; scene.py draws
# them apart.
CLEAR = {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.010, 'roughness': 0.05}
MATERIALS = dict(B.MATERIALS,
                 acrylic=dict(CLEAR),
                 **{'acrylic-strata': dict(CLEAR),
                    'acrylic-strata-platter': dict(CLEAR, radius=0.024),
                    'acrylic-base': dict(CLEAR, deep='$base'),
                    'acrylic-lid': dict(CLEAR, radius=0.010),
                    'etch-tone': {'preset': 'satin_paint', 'color': '$accent', 'roughness': 0.35, 'specular': 0.5}})

# flavors: the line's stock codes (the first is the engine's default). `accent` is the etched mark's tone, `glow` is
# kept only for the engine's variant format (no light since 2026-11-10), `base` the Smoke 2074 base under every flavor
SMOKE_2074 = '#787B7E'
STOCK = [('poison-2092', '#0DA41C', '#123A16'), ('ember-2423', '#E02B3A', '#4A0E12'), ('smoke-2074', SMOKE_2074, '#1A1B1C'),
         ('haze-2287', '#9C5DE3', '#2E1A4A'), ('ice-2069', '#B4DEFA', '#24557E')]
VARIANTS = {k: {'deep': deep, 'accent': acc, 'glow': '#FF8C40', 'base': SMOKE_2074} for k, deep, acc in STOCK}

PRODUCT = Product('mantle-strata-v3', 'Mantle: Strata Float v3 (proposal A)', 'Belt-drive record player, a tinted deck floating over a smoked base (no light)',
                  params=P, parts=parts, count=1, notes=NOTES, materials=MATERIALS, variants=VARIANTS,
                  touching=[('plinth-L*', 'plinth-L*'), ('base-L*', 'base-L*'), ('post-*', 'plinth-L*'), ('post-*', 'base-L*'), ('foot-studs', 'post-*'), ('foot-studs', 'base-L*'), ('rear-plate', 'base-L*'), ('rear-hardware', 'rear-plate'), ('rear-hardware', 'base-L*'), ('phono-pads', 'phono-stage'), ('bushes', 'bearing-housing'), ('bushes', 'spindle'),
                            ('platter-hub', 'spindle'), ('platter-screws', 'platter*'), ('foot-studs', 'feet'), ('foot-studs', 'base-L*'),
                            ('foot-pads', 'feet'), ('motor-screws', 'motor-plate'), ('motor-screws', 'plinth-L*'), ('motor', 'motor-plate'),
                            ('platter-inserts', 'platter'), ('platter-screws', 'platter-hub'), ('platter-screws', 'platter-inserts'), ('bearing-spring', 'bearing-*'), ('bearing-washer', 'plinth-L*'), ('bearing-spring', 'bearing-washer'),
                            ('bearing-nut', 'bearing-housing'), ('arm', 'arm-puck'), ('lid-*', 'lid-*')],
                  drawing_prefix='MS3')
