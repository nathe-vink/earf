"""Mantle, proposal A: STRATA FLOAT (round 48). The baseline's architecture kept (a squared plinth floating over a lit
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
import mantle_core as B                                             # noqa: E402  (the stock sheets, the arm, the hull)
from mantle_core import *                                           # noqa: E402,F403

P = dict(
    W=450.0, D=360.0, R=4.0,                  # the plinth's top: the baseline's footprint
    step=2.0,
    plinth=(('tint', 3.0), ('clear', 12.7), ('tint', 3.0), ('clear', 5.6)),
    base=(('clear', 12.7), ('tint', 3.0)),
    margin=10.0, Rb=8.0,
    feet_h=16.0, gap=40.0,
    posts=((145.0, 60.0), (305.0, 60.0), (145.0, 300.0), (305.0, 300.0)), post_d=30.0,
    spindle=(200.0, 168.0),
    platter_d=300.0, platter_t=21.0, lift=6.0,
    platter_lams=(('tint', 3.0), ('clear', 12.7), ('tint', 5.6)),
    arm_r=222.0, arm_x=395.0, L_eff=236.5, offset=21.55, rest_r=168.0,
    puck_d=84.0, puck_t=12.0,
    motor_d=184.7, motor_x=64.0, motor_pocket=76.0,
    rpm_motor=250.0,
    slot_in=25.0, slot_w=3.0, slot_h=6.0,
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
             belt_z=pz0 + 9.0, record_z=pz1 + 1.8, Wb=W0 + 2 * m, Db=D0 + 2 * m,
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


def boutline(P, D, inset=0.0):
    return rounded_rect(D['Wb'] - 2 * inset, D['Db'] - 2 * inset, max(P['Rb'] - inset, 2.0), cx=D['Wb'] / 2, cy=D['Db'] / 2)


def parts(P):
    from build123d import Pos, Rot, Sphere
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
    # the motor's pocket through the plinth: the plate hangs on grommets on a shoulder 6 down, the motor below in the gap
    cuts += [cyl('z', M, P['motor_pocket'] + 8, top - 6, top + 1), cyl('z', M, P['motor_pocket'], z0 - 1, top + 1)]
    cuts += [cyl('z', p, 8.0, z0 - 1, z0 + 12) for p in posts]          # the posts' M6 inserts
    hx = [m + 80.0, m + D['W0'] - 80.0]
    cuts += [cyl('y', (x + s_ * 10, (z0 + top) / 2), 6.0, m + D['D0'] - 14, m + D['D0'] + 1) for x in hx for s_ in (-1, 1)]

    def cut(s, cs):
        for c in cs:
            s = s - c
        return s

    out = []
    one = []
    for i, l in enumerate(D['lams']):
        s = cut(prism(poutline(P, D, l['inset']), 'z', l['z0'], l['z1']), cuts)
        one.append(prism(poutline(P, D, l['inset']), 'z', l['z0'], l['z1']))
        if l['kind'] == 'tint':
            band = prism(poutline(P, D, l['inset'] + rw), 'z', l['z0'] - 1, l['z1'] + 1)
            out.append(Part(f'plinth-L{i + 1}', s - band, tint[l['t']], finish='acrylic', group='plinth', render=False,
                            notes=['the plinth: four laminae of stock sheet (tinted 3 ring / clear 12.7 / tinted 3 ring / clear 5.6), each tinted lamina a 20 wide ring round a clear inlay cut from the same file; cemented in one vacuum press with ACRIFIX 2R 0190, annealed, faces fly-cut, the stepped outline finish-routed, edges diamond-polished, holes left satin'] if i == 0 else []))
            out.append(Part(f'plinth-L{i + 1}-inlay', s & band, clr[3.0], finish='clear', group='plinth', render=False))
        else:
            out.append(Part(f'plinth-L{i + 1}', s, clr[l['t']], finish='clear', group='plinth', render=False))
    plinth_one = cut(union(*one), cuts)
    out[0].pieces = {'stack': (plinth_one, 'acrylic-strata')}; out[0].render = True

    # ---- the base: clear 12.7 with the light's slot from below, a tinted 3 ring on it, the band printed between ----
    si, sw, sh = P['slot_in'], P['slot_w'], P['slot_h']
    slot = prism(boutline(P, D, si), 'z', b0 - 1, b0 + sh) - prism(boutline(P, D, si + sw), 'z', b0 - 2, b0 + sh + 1)
    feet = [(35.0, 35.0), (Wb - 35, 35.0), (35.0, Db - 35), (Wb - 35, Db - 35)]
    bcuts = [slot] + [cyl('z', f, 11.0, b0 - 1, b0 + 10) for f in feet] + [cyl('z', p, 8.0, b0 - 1, b1 + 1) for p in posts]
    bl0, bl1 = D['base']
    base_c = cut(prism(boutline(P, D), 'z', bl0['z0'], bl0['z1']), bcuts)
    base_t = prism(boutline(P, D), 'z', bl1['z0'], bl1['z1'])
    band = prism(boutline(P, D, rw), 'z', bl1['z0'] - 1, bl1['z1'] + 1)
    base_t = cut(base_t, bcuts)
    out += [Part('base-L1', base_c, clr[12.7], finish='clear', group='base', render=False,
                 pieces={'stack': (cut(union(prism(boutline(P, D), 'z', bl0['z0'], bl0['z1']), prism(boutline(P, D), 'z', bl1['z0'], bl1['z1'])), bcuts), 'acrylic-base')},
                 notes=['the base: clear 12.7 with the light\'s slot routed from below (3 x 6, 25 in from the edge, one closed loop round all four sides), its outer edge diamond-polished; on it a tinted 3 ring 20 wide round a clear inlay; an opaque black band 11 wide screen-printed on the clear\'s top over the slot before the two are cemented, so it is inside the stack']),
            Part('base-L2', base_t - band, tint[3.0], finish='acrylic', group='base', render=False),
            Part('base-L2-inlay', base_t & band, clr[3.0], finish='clear', group='base', render=False)]
    out[-3].render = True
    strip = prism(boutline(P, D, si + 0.4), 'z', b0 + 0.2, b0 + 5.8) - prism(boutline(P, D, si + 1.6), 'z', b0, b0 + 6)
    out.append(Part('led-strip', strip, Bought('led-strip-cob'), finish='ledstrip', group='base',
                    notes=['a 24 V COB strip (dotless) on its back in the slot, its light facing out, one closed loop of about 1.48 m: 4.4 W at 3 W/m']))

    # ---- the posts: clear rod, bonded under the plinth, M6 studs torqued into inserts top and bottom ----
    for i, p in enumerate(posts):
        out.append(Part(f'post-{i + 1}', cyl('z', p, P['post_d'], b1, z0) - cyl('z', p, 6.6, b1 - 1, z0 + 1), Machined('cast-acrylic', 'lathe'),
                        finish='clear', group='float', notes=['water-clear rod 30, bored 6.6, faced and polished; cemented under the plinth on a jig; an M6 stud through it, torqued 4 N m into the inserts top and bottom: rigid'] if i == 0 else []))
    out.append(Part('studs', union(*[cyl('z', p, 6.0, b0 + 1, z0 + 10) for p in posts]), Bought('float-studs'), finish='steel', group='float'))

    # ---- the bearing, platter, hub, spindle (as Core) ----
    hz0 = z0 - 20.0
    ft = P['flange_t']
    housing = (cyl('z', S, P['housing_d'], hz0, top - ft) + cyl('z', S, P['flange_d'], top - ft, top)) - cyl('z', S, 14.0, hz0 + 4, top + 1)
    nut = cyl('z', S, 46.0, z0 - 7, z0) - cyl('z', S, P['housing_d'] + 0.2, z0 - 8, z0 + 1)
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
    for c in hub_screws:
        platter = platter - cyl('z', c, 4.5, pz0 - 1, pz1 + 1) - cyl('z', c, 8.0, pz1 - 4, pz1 + 1)
    screws = union(*[cyl('z', c, 4.0, pz0 - 4, pz1 - 4) + cyl('z', c, 7.4, pz1 - 4, pz1 - 0.5) for c in hub_screws])

    # ---- the motor, hung from the plinth into the gap ----
    bz = D['belt_z']
    mt = top - 2
    mplate = cyl('z', M, P['motor_pocket'] + 6, mt - 3, mt) - cyl('z', M, 26, mt - 4, mt + 1)
    motor = union(cyl('z', M, 50.0, mt - 3 - 30, mt - 3), cyl('z', M, 4.0, mt - 3, bz + 9))
    grommets = union(*[cyl('z', (M[0] + 36 * math.cos(math.radians(a)), M[1] + 36 * math.sin(math.radians(a))), 8.0, top - 6, mt + 1.5)
                       for a in (0, 120, 240)])
    pdia = D['pulley_d']
    pulley = (cyl('z', M, pdia, bz - 5, bz + 5) + cyl('z', M, pdia + 6, bz + 5, bz + 7)) - cyl('z', M, 4.0, bz - 6, bz + 8)
    R = P['platter_d'] / 2
    belt = prism(B_hull([(S[0], S[1], R + 0.65), (M[0], M[1], pdia / 2 + 0.65)]), 'z', bz - 2.5, bz + 2.5) - \
        prism(B_hull([(S[0], S[1], R + 0.05), (M[0], M[1], pdia / 2 + 0.05)]), 'z', bz - 3, bz + 3)

    puck = cyl('z', A, pd, top - pt, top) - cyl('z', A, 24.0, top - pt - 1, top + 1)
    for c in puck_screws:
        puck = puck - cyl('z', c, 5.5, top - pt - 1, top + 1) - cyl('z', c, 10.0, top - 3, top + 1)
    arm, lift, cart = B.arm_solids(P, D)

    foot = union(*(union(cyl('z', f, 40.0, 4, 14), cyl('z', f, 30.0, 14, b0 - 0.5)) for f in feet))
    pads = union(*(cyl('z', f, 40.0, 0, 4) for f in feet))
    fstuds = union(*(cyl('z', f, 8.0, b0 - 0.5, b0 + 9) for f in feet))

    # ---- the phono stage on the base under the platter's back, its own adapter; the rear box ----
    px0, py0 = Wb / 2 - 51.5, Db - 140.0
    phono = box(px0, py0, b1 + 1.5, px0 + 103, py0 + 115, b1 + 37.5)
    felts = union(*[cyl('z', (px0 + x, py0 + y), 10.0, b1 + 0.15, b1 + 1.5) for x in (12, 91) for y in (12, 103)])

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
             notes=['tinted 3 / clear 12.7 / tinted 5.6 cemented, annealed, turned to 300 x 21 as Core\'s; on a screwed brass hub']),
        Part('platter-hub', hub, Machined('brass-leadfree', 'lathe'), finish='brass', group='platter'),
        Part('platter-screws', screws, Bought('platter-screws'), finish='steel', group='platter'),
        Part('spindle', spindle, Machined('stainless', 'lathe', setup_usd=120.0), finish='steel', group='bearing'),
        Part('bearing-housing', housing, Machined('brass-leadfree', 'lathe'), finish='brass', group='bearing',
             notes=['as Core\'s: M30 x 1.5, clamped by its nut under the plinth, hanging 20 into the float where its brass shows']),
        Part('bearing-nut', nut, Machined('brass-leadfree', 'lathe'), finish='brass', group='bearing'),
        Part('bushes', bushes, Bought('bearing-bushes-solid'), finish='brass', group='bearing', inside=True),
        Part('ball', ball, Bought('carbide-ball'), finish='steel', group='bearing', inside=True),
        Part('thrust-plate', plate, Bought('thrust-plate'), finish='steel', group='bearing', inside=True),
        Part('motor-plate', mplate, Sheet('aluminium', 3, face='+z'), finish='aluminium', group='motor'),
        Part('motor', motor, Bought('rega-24v-motor'), finish='black', group='motor'),
        Part('motor-grommets', grommets, Bought('rega-grommets'), finish='rubber', group='motor'),
        Part('pulley', pulley, Machined('aluminium', 'lathe'), finish='aluminium', group='motor'),
        Part('belt', belt, Bought('flat-belt-core'), finish='rubber', group='platter'),
        Part('arm-puck', puck, Machined('aluminium', 'lathe'), finish='aluminium', group='arm'),
        Part('arm', union(arm, lift), Bought('rega-rb330'), finish='arm', group='arm'),
        Part('cartridge', cart, Bought('ortofon-2m-black'), finish='cartridge', group='arm'),
        Part('feet', foot, Machined('brass-leadfree', 'lathe'), finish='brass', group='feet',
             notes=['four, 40 x 10 with a 30 neck, on M8 studs in the base\'s inserts, levelled and locked; Sorbothane under']),
        Part('foot-pads', pads, Bought('foot-sorbothane'), finish='rubber', group='feet'),
        Part('foot-studs', fstuds, Bought('foot-studs'), finish='steel', group='feet'),
        Part('phono-stage', phono, Bought('phono-box-s2'), finish='aluminium-dark', group='phono'),
        Part('phono-pads', felts, Bought('phono-felts'), finish='rubber', group='phono'),
        Part('back-hardware', None, Bought('back-hardware')),
        Part('hinge-blocks', blocks, tint[9.5] if False else Machined('cast-acrylic', 'cnc-mill'), finish='acrylic', group='lid',
             notes=['two 40 x 9.5 blocks of the color, each with the hinge\'s slot 3.2 x 12 x 18 deep, on two M4 screws into inserts in the plinth\'s back edge (horizontal, in shear)']),
        Part('hinges', hinges, Bought('cover-hinges'), finish='black', group='lid'),
        *[Part(k, s, Sheet('trucast-tint', 3.0), finish='acrylic-lid', group='lid',
               notes=['3 mm 2064 (1/8 in stock), cemented as a box with ACRIFIX 2R 0190; 1.1 kg, within the Debut hinges\' rating; outer edges eased R0.5 and polished'] if k == 'lid-top' else [])
          for k, s in lid.items()],
        Part('led-adapter', None, Bought('led-adapter-float')),
        Part('led-dimmer', None, Bought('float-dimmer-hf')),
        Part('inserts', None, Bought('core-inserts')),
        Part('wiring', None, Bought('core-wiring')),
        Part('neo-psu', None, Bought('rega-neo-psu-mk2')),
        Part('bearing-oil', None, Bought('bearing-oil')),
        Part('cement', None, Bought('acrylic-cement-2r')),
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
    'The plinth: tinted 3 ring / clear 12.7 / tinted 3 ring / clear 5.6 (24.3), each tinted ring 20 wide round a clear inlay, '
    'cemented with ACRIFIX 2R 0190 in one vacuum press, annealed, fly-cut, stepped 2 mm a stratum, diamond-polished.',
    'The float: four clear posts bonded under the plinth, M6 studs torqued 4 N m into inserts in the plinth and the base: '
    'rigid. Isolation in the four feet (brass on Sorbothane, on M8 studs, levelled and locked).',
    'The light: a dotless 24 V COB strip, 3 W/m, one closed loop in a 3 x 6 slot routed from below 25 in from the base\'s '
    'edge; the black band printed on the clear before lamination; Mean Well listed adapter and the 25 kHz dimmer. The '
    'phono stage runs from its own listed adapter.',
    'The motor: Rega 24 V on its plate, hung on Rega\'s grommets in a pocket through the plinth, below it in the float.',
    'The bearing, platter, arm puck and phono stage as Core\'s (mantle_core.py).',
    'The lid: 3 mm 2064, 1.1 kg, on Pro-Ject\'s friction hinges.',
]

MATERIALS = dict(B.MATERIALS, **{'acrylic-base': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.025, 'roughness': 0.05}},
                 ledstrip={'preset': 'satin_paint', 'color': '#EDEAE4', 'roughness': 0.5, 'specular': 0.3})

PRODUCT = Product('mantle-strata', 'Mantle: Strata Float (proposal A)', 'Belt-drive record player, a laminated plinth floating over a lit laminated base',
                  params=P, parts=parts, count=1, notes=NOTES, materials=MATERIALS, variants=B.C.VARIANTS,
                  touching=[('plinth-L*', 'plinth-L*'), ('base-L*', 'base-L*'), ('led-strip', 'base-L*'), ('studs', 'post-*'), ('studs', 'plinth-L*'),
                            ('studs', 'base-L*'), ('phono-pads', 'phono-stage'), ('bushes', 'bearing-housing'), ('bushes', 'spindle'),
                            ('platter-hub', 'spindle'), ('platter-screws', 'platter*'), ('foot-studs', 'feet'), ('foot-studs', 'base-L*'),
                            ('foot-pads', 'feet'), ('motor-grommets', 'motor-plate'), ('motor-grommets', 'plinth-L*'), ('motor', 'motor-plate'),
                            ('bearing-nut', 'bearing-housing'), ('arm', 'arm-puck'), ('lid-*', 'lid-*')],
                  drawing_prefix='MS')
