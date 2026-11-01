"""Mantle, proposal B: OUTCROP (round 48). A record player cut from one stack of bonded stock sheet.

The baseline (turntable_float.py: a squared plinth floating over a lit base, a hinged box lid) stays the baseline. This
is a proposal beside it, built to the same fab kit, never overwriting it.

The idea in one line: closed, it is a block of strata, a core sample of the Earth's layers; lift the top strata off and
the record player is excavated inside it. The lifted strata stand on their long edge and frame the sleeve that is
playing.

- **The deck** is seven laminae of stock cell-cast sheet, cemented with a polymerising cement (index-matched, so the
  joints nearly vanish) and stepped like a contour map: tinted 3 / clear 12.7 / tinted 3 / clear 12.7 / tinted 3 /
  clear 12.7, 47.1 tall. Each tinted lamina with the clear one on it steps in 3 mm from the pair below, so every
  terrace is a clear stratum on a dark contour line, and the deck's top is clear: you look down into it. Why thin tint in clear and not the reverse: stock
  2064 Gray passes 29.3 % at 1/8 in (TruCast's chart, Fresnel included), so by Beer-Lambert 12.7 mm of it passes
  about 1 % and reads black; three millimeters pass about a third. Thick clear strata keep the light passing and the
  bearing, the motor and the phono stage visible inside, like a watch's caseback; the thin laminae carry the color.
- **The cover** is the same stack continued upward: five clear rings 10 wide with a tinted lamina on each, stepping
  in 3 mm a ring, and a clear 5.6 top under a tinted 3. Closed, the strata run unbroken from the shelf to the top. It
  lifts off (two dowels locate it; no hinges to sag), and stood on its back edge it frames the sleeve playing.
- **Rigid on three feet** (the review of the baseline: the float sat at 25-36 Hz, in the feedback band). The block is
  heavy and stiff. Three feet (turned stainless on a Sorbothane puck, levelled on M8 studs) locate and level it; they
  do not isolate it (the audit: they sit at 50 Hz or more, above the feedback band). Isolation, if wanted, is a platform.
- **The motor is hard-mounted in the block**, as Rega fits it: its mount screwed to an aluminum plate, the plate on
  three M3 screws into inserts on the pocket's shoulder; the belt decouples it. So the pulley's height is fixed to the platter's by solid acrylic (the review: the pod on the shelf tipped under the belt).
- **The platter** is three laminae of its own (tinted 3 / clear 12.7 / tinted 5.6, faced to 21), turned, on a flanged
  brass hub shrunk onto the spindle, held by six M4 screws up through the hub's flange into brass inserts bonded in
  the platter from below: the bond carries nothing, and no screw head bears on acrylic. The belt runs on the clear
  stratum's rim, between the two dark lines.
- **The arm** stands on an aluminum arm-board puck (Rega's three-point mount into it), replaceable for another arm.
- **The phono stage** (Pro-Ject's Phono Box S2, whole) slides into a tunnel from the back; a brass plate closes it and
  carries the line out, the bypass toggle, the earth post, the 18 V inlet and the rating.

The frame is the kit's: x across from the left seen from the front, y back from the front, z up from the shelf.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/mantle-r48/mantle_outcrop.py \
        --out spinoffs/barkhorn/companions/mantle-r48/out-outcrop
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(COMP)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
sys.path.insert(0, COMP)
from kit import *                                                   # noqa: E402,F403
import common as C                                                  # noqa: E402

# stock cell-cast sheet as AC Plastics / Canal sell it (round 43's stock-colors.md): 1/8 (3.0), 1/4 (5.6), 3/8 (9.5),
# 1/2 (12.7). Priced a square meter a millimeter from the 4 x 8 ft listings of 2026-10-31: 2064 Gray 1/2 $495 (Canal)
# = 13.1, 3/8 $375 = 13.3; 2423 Red 1/2 $835.80 (AC) = 22.2; clear 1/8 about $110 = 11.7. The tinted rate is the
# dearer of the two first colors, so a budget never undershoots.
SHEETS['trucast-tint'] = dict(title='Cell-cast acrylic sheet, stock tint (TruCast 2064 Gray or 2423 Red), 4 x 8 ft',
                              density=1.19, sheet=(2440.0, 1220.0), usd_per_m2_mm=22.0, thicknesses=(3.0, 5.6, 9.5, 12.7))
SHEETS['trucast-clear'] = dict(title='Cell-cast acrylic sheet, water-clear, 4 x 8 ft', density=1.19,
                               sheet=(2440.0, 1220.0), usd_per_m2_mm=12.0, thicknesses=(3.0, 5.6, 9.5, 12.7))

P = dict(
    W=460.0, D=370.0, R=6.0,                  # PROPOSAL: the deck's top lamina (the baseline plinth's footprint)
    step=3.0,                                 # each tinted lamina steps in this much from the one below
    deck=(('tint', 3.0), ('clear', 12.7), ('tint', 3.0), ('clear', 12.7), ('tint', 3.0), ('clear', 12.7)),
    cover_rings=5, ring_w=10.0, ring_t=12.7, cover_top=5.6,
    feet_h=18.0,                              # the feet: the deck's underside from the shelf
    spindle=(200.0, 168.0),                   # in the top lamina's frame (as the baseline's plinth)
    platter_d=300.0, platter_t=21.0, lift=6.0,
    platter_lams=(('tint', 3.0), ('clear', 12.7), ('tint', 5.6)),   # 21.3, faced to 21
    arm_r=222.0, arm_x=395.0,                 # DATASHEET: Rega's spindle to arm hole; the pivot's x (top frame)
    L_eff=236.5, offset=21.55,                # DATASHEET: RB330
    rest_r=168.0,
    puck_d=84.0, puck_t=12.0, puck_access=56.0,
    motor_d=180.0, motor_x=75.0,              # the pulley 180 from the spindle, at x 75 in the top frame
    motor_pocket=76.0, motor_depth=40.0,
    rpm_motor=300.0,                          # PROPOSAL until benched: Rega's 24 V synchronous motor on the US Neo at 60 Hz (STOCK-AND-AUDIT.md 3.1)
    tunnel=(110.0, 38.0, 131.0),              # the phono stage's tunnel: wide, tall, deep from the back notch
    notch=(146.0, 46.0, 12.0),                # the back notch the brass plate sits in: wide, tall, deep
    housing_d=30.0, flange_d=50.0, flange_t=5.0,
    ease=1.0,
    tint_ring=20.0,                           # PROPOSAL: the tinted laminae as rings this wide round clear inlays
)


def derived(P):
    s = P['step']
    zs, z = [], P['feet_h']
    inset, lams = 0.0, []
    for i, (kind, t) in enumerate(P['deck']):
        if kind == 'tint' and i > 0:
            inset += s
        lams.append(dict(kind=kind, t=t, z0=z, z1=z + t, inset=inset))
        z += t
    o = inset                                               # the top lamina's corner in the bottom lamina's frame
    W1, D1 = P['W'] + 2 * o, P['D'] + 2 * o
    top = z
    S = (o + P['spindle'][0], o + P['spindle'][1])
    ay = math.sqrt(P['arm_r'] ** 2 - (P['arm_x'] - P['spindle'][0]) ** 2)
    A = (o + P['arm_x'], S[1] + ay)
    mx = o + P['motor_x']
    M = (mx, S[1] + math.sqrt(P['motor_d'] ** 2 - (mx - S[0]) ** 2))
    pz0 = top + P['lift']; pz1 = pz0 + P['platter_t']
    r_belt = P['platter_d'] / 2 + 0.3
    d = dict(lams=lams, o=o, W1=W1, D1=D1, top=top, S=S, A=A, M=M, pz0=pz0, pz1=pz1,
             belt_z=pz0 + 9.0, record_z=pz1 + 1.8,
             pulley_d=round(2 * r_belt * (100.0 / 3.0) / P['rpm_motor'] - 0.6, 2))
    # the arm at rest (as the baseline): the stylus on the arm's arc rest_r from the spindle
    dx, dy = S[0] - A[0], S[1] - A[1]
    dd = math.hypot(dx, dy); L = P['L_eff']; r = P['rest_r']
    a = (L * L - r * r + dd * dd) / (2 * dd); h = math.sqrt(L * L - a * a)
    bx, by = A[0] + a * dx / dd, A[1] + a * dy / dd
    st = min([(bx + h * dy / dd, by - h * dx / dd), (bx - h * dy / dd, by + h * dx / dd)], key=lambda p: p[1])
    d['stylus'] = st
    d['rest_deg'] = math.degrees(math.atan2(st[1] - A[1], st[0] - A[0]))
    # the cover's rings: each tinted ring steps in s from the lamina under it, a clear lamina on each
    rings, z, ins = [], top, inset
    for k in range(P['cover_rings']):
        ins += s
        rings.append(dict(kind='clear', t=P['ring_t'], z0=z, z1=z + P['ring_t'], inset=ins)); z += P['ring_t']
        rings.append(dict(kind='tint', t=3.0, z0=z, z1=z + 3.0, inset=ins)); z += 3.0
    ins += s
    d['cover'] = rings
    d['cover_top'] = [dict(kind='clear', t=P['cover_top'], z0=z, z1=z + P['cover_top'], inset=ins),
                      dict(kind='tint', t=3.0, z0=z + P['cover_top'], z1=z + P['cover_top'] + 3.0, inset=ins)]
    d['height'] = z + P['cover_top'] + 3.0
    return d


D = derived(P)


def outline(P, D, inset, extra=0.0):
    W1, D1 = D['W1'], D['D1']
    r = max(P['R'] + (D['o'] - inset), 3.0) + extra
    return rounded_rect(W1 - 2 * inset + 2 * extra, D1 - 2 * inset + 2 * extra, r, cx=W1 / 2, cy=D1 / 2)


def arm_solids(P, D):
    """Rega's RB330 as an envelope from its published geometry, at rest, for the drawings and the clash check (the
    render builds a fuller model of it)."""
    from build123d import Pos, Rot
    ax, ay = D['A']
    z = D['top']
    h = D['record_z'] + 21.0
    ang = D['rest_deg']
    L = P['L_eff']
    sx, sy = D['stylus']
    tube_L = L - 30
    tube = Pos(ax, ay, h) * Rot(0, 0, ang) * Pos(tube_L / 2, 0, 0) * Rot(0, 90, 0) * cyl('z', (0, 0), 9.5, -tube_L / 2, tube_L / 2)
    head = Pos(sx, sy, h) * Rot(0, 0, ang + P['offset']) * box(-34, -9, -4.5, 4, 9, 0.5)
    cw = Pos(ax, ay, h) * Rot(0, 0, ang) * Rot(0, 90, 0) * cyl('z', (0, 0), 34, -66, -38)
    stub = Pos(ax, ay, h) * Rot(0, 0, ang) * Rot(0, 90, 0) * cyl('z', (0, 0), 8, -40, -6)
    yoke = Pos(ax, ay, h) * Rot(0, 0, ang) * box(-16, -12, -9, 16, 12, 9)
    base = union(cyl('z', (ax, ay), 44, z, z + 8), cyl('z', (ax, ay), 26, z + 8, h - 9))
    u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    nx, ny = u[1], -u[0]
    lx, ly = ax + 55 * u[0] + 18 * nx, ay + 55 * u[1] + 18 * ny
    lift = union(cyl('z', (lx, ly), 9, z, h - 7.5),
                 Pos(lx - 11 * nx, ly - 11 * ny, h - 7.5) * Rot(0, 0, ang + 90) * box(-14, -3, -3, 14, 3, 2.75))
    cart = Pos(sx, sy, h - 4.5) * Rot(0, 0, ang + P['offset']) * union(box(-21, -9, -15, 1, 9, 0), box(-6, -3.5, -17.5, 1.5, 3.5, -14.5))
    return union(base, yoke, tube, head, cw, stub), lift, cart


def parts(P):
    from build123d import Pos, Sphere
    D = derived(P)
    S, A, M = D['S'], D['A'], D['M']
    W1, D1, top, o = D['W1'], D['D1'], D['top'], D['o']
    b0 = P['feet_h']
    tint = {t: Sheet('trucast-tint', t, face='+z') for t in (3.0, 5.6, 9.5, 12.7)}
    clr = {t: Sheet('trucast-clear', t, face='+z') for t in (3.0, 5.6, 9.5, 12.7)}

    # ---- what is cut through the deck's stack (each lamina takes the cuts that cross it) ----
    cuts = []
    # the bearing: its housing's body (M30 x 1.5, 30) through, its flange (50 x 5) in a pocket in the top, the nut
    # under the deck in a 66 counterbore 14 deep from below, on a disc spring and a brass washer (the audit: the
    # clamp's preload over temperature). No insert near the bore (the review: 2.8 mm webs crack).
    cuts += [cyl('z', S, P['housing_d'] + 0.4, b0 - 1, top + 1), cyl('z', S, P['flange_d'] + 0.4, top - P['flange_t'], top + 1),
             cyl('z', S, 66.0, b0 - 1, b0 + 14)]
    # the arm-board puck (84 x 12) in a counterbore from the top, three M5 inserts in the shoulder under it at r 35; a
    # 56 bore from below to the puck for the arm's nut, its three-point screws and its lead
    pd, pt = P['puck_d'], P['puck_t']
    cuts += [cyl('z', A, pd + 0.4, top - pt, top + 1), cyl('z', A, P['puck_access'], b0 - 1, top - pt + 0.5)]
    puck_screws = [(A[0] + 35 * math.cos(math.radians(a)), A[1] + 35 * math.sin(math.radians(a))) for a in (90, 210, 330)]
    cuts += [cyl('z', c, 7.0, top - pt - 14, top - pt + 0.5) for c in puck_screws]
    # the motor's pocket from the top (76 x 40): its plate screwed down on a 4 shoulder 6 from the top (Rega's method);
    # a 12 hole under it for the lead, a groove under the deck to the back notch
    cuts += [cyl('z', M, P['motor_pocket'] + 16, top - 6, top + 1), cyl('z', M, P['motor_pocket'], top - P['motor_depth'], top + 1),
             cyl('z', M, 12.0, b0 - 1, top - P['motor_depth'] + 1)]
    cuts += [cyl('z', (M[0] + 42 * math.cos(math.radians(a)), M[1] + 42 * math.sin(math.radians(a))), 4.6, top - 14, top - 5.5)
             for a in (30, 150, 270)]   # the plate's three M3 inserts

    def groove(p0, p1, wd, za, zb):
        from build123d import Rot
        ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        Lg = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        return Pos(p0[0], p0[1], 0) * Rot(0, 0, ang) * box(-wd / 2, -wd / 2, za, Lg + wd / 2, wd / 2, zb)
    # the phono stage's tunnel from the back: S2 (103 x 115 x 36) on two felt runners, its switches reached by
    # sliding it out; the back notch (146 x 46 x 12) that the brass plate closes
    tw, th, tdp = P['tunnel']
    nw, nh, nd = P['notch']
    tx0 = S[0] - tw / 2 + 5.0
    tz0 = b0 + 4.0
    cuts.append(box(tx0, D1 - tdp, tz0, tx0 + tw, D1 + 1, tz0 + th))
    nx0 = tx0 + tw / 2 - nw / 2
    cuts.append(box(nx0, D1 - nd, b0 + 1.5, nx0 + nw, D1 + 1, b0 + 1.5 + nh))
    # the leads under the deck, 8 x 6 grooves: the arm's from its bore to the tunnel, the motor's to the notch
    cuts.append(groove(A, (tx0 + tw - 4, D1 - tdp + 20), 8.0, b0 - 1, b0 + 6))
    cuts.append(groove(M, (nx0 + 6, D1 - nd - 2), 8.0, b0 - 1, b0 + 6))
    # three feet: M8 inserts (12 long, through L1 into L2/L3), two at the front, one at the back's middle
    feet = [(48.0, 48.0), (W1 - 48.0, 48.0), (W1 - 150.0, D1 - 42.0)]
    cuts += [cyl('z', f, 11.0, b0 - 1, b0 + 13) for f in feet]
    # the brass plate's four M3 inserts, into the notch's back face
    plate_y = D1 - nd
    plate_holes = [(nx0 + 7, b0 + 6.5), (nx0 + nw - 7, b0 + 6.5), (nx0 + 7, b0 + nh - 3.5), (nx0 + nw - 7, b0 + nh - 3.5)]
    cuts += [cyl('y', h, 5.0, plate_y - 10, plate_y + 1) for h in plate_holes]
    # the cover's two dowels (5 x 12 stainless, pressed into the deck's top lamina near the back corners)
    dowels = [(o + 40.0, o + P['D'] - 7.0), (o + P['W'] - 40.0, o + P['D'] - 7.0)]
    cuts += [cyl('z', c, 5.0, top - 8, top + 1) for c in dowels]

    def cut(s):
        for c in cuts:
            s = s - c
        return s

    lam_parts, solids = [], []
    for i, l in enumerate(D['lams']):
        s = cut(prism(outline(P, D, l['inset']), 'z', l['z0'], l['z1']))
        solids.append(s)
        make = clr[l['t']] if l['kind'] == 'clear' else tint[l['t']]
        notes = []
        if i == 0:
            notes = ['the deck: seven laminae cut from stock cell-cast sheet (tinted 3 / clear 12.7 / tinted 3 / clear 12.7 / tinted 3 / clear 12.7), each CNC-routed oversize by 1.5 on its outline with its through-holes, then cemented in one press with ACRIFIX 2R 0190 (index-matched, so a joint shows as a faint line, not a glue line) on dowel pins through two tooling holes in the waste, under vacuum, and annealed (80 C, 10 h, cooled at 5 C/h)',
                     'after annealing: the top and bottom faces fly-cut flat (0.3 off each), the terraced outline finish-routed on a 3-axis router in one setup, each terrace nose eased R1, every outer face diamond-polished; holes, pockets, the tunnel and the grooves are left as machined (satin)',
                     'cast sheet varies in thickness (about +-10 % at 12.7): the stack is 47.1 nominal, measured before the faces are cut; the record height is set by Rega spacers on the first sample']
        if l['kind'] == 'tint' and P['tint_ring']:
            # the tinted lamina is a ring (tint_ring wide) round a clear inlay cut to fit from 3 mm clear sheet: the
            # color stays at the edges as a contour line, and the interior stays clear, so the mechanism shows
            band = prism(outline(P, D, l['inset'] + P['tint_ring']), 'z', l['z0'] - 1, l['z1'] + 1)
            ring_s, inlay_s = s - band, s & band
            lam_parts.append(Part(f'deck-L{i + 1}', ring_s, make, finish='acrylic', group='deck', render=False, notes=notes + (
                [f'each tinted lamina is a ring {P["tint_ring"]:g} wide (laser-cut) round a clear inlay laser-cut from the same file with the kerf taken up (0.1 clearance), the two cemented edge to edge in the press with the rest: inside, the butt joint reads as a fine refracting line'] if i == 0 else [])))
            lam_parts.append(Part(f'deck-L{i + 1}-inlay', inlay_s, clr[3.0], finish='clear', group='deck', render=False))
        else:
            lam_parts.append(Part(f'deck-L{i + 1}', s, make, finish='acrylic' if l['kind'] == 'tint' else 'clear',
                                  group='deck', render=False, notes=notes))
    # the render's deck: the laminae as one solid (coplanar faces of touching solids render black), its strata painted
    # by height in the render's material
    deck_one = cut(union(*[prism(outline(P, D, l['inset']), 'z', l['z0'], l['z1']) for l in D['lams']]))
    lam_parts[0].pieces = {'stack': (deck_one, 'acrylic-strata')}
    lam_parts[0].render = True

    # ---- the cover: the strata continued; clear rings 10 wide, a tinted lamina on each, a clear 5.6 top under a tinted 3 ----
    cov, cov_solids = [], []
    for k, l in enumerate(D['cover']):
        out_ = outline(P, D, l['inset'])
        inn = outline(P, D, l['inset'] + P['ring_w'])
        s = prism(out_, 'z', l['z0'], l['z1']) - prism(inn, 'z', l['z0'] - 1, l['z1'] + 1)
        if k == 0:
            s = s - union(*[cyl('z', c, 5.4, l['z0'] - 1, l['z0'] + 8) for c in dowels])
        cov_solids.append(s)
        make = clr[l['t']] if l['kind'] == 'clear' else tint[l['t']]
        cov.append(Part(f'cover-C{k + 1}', s, make, finish='acrylic' if l['kind'] == 'tint' else 'clear', group='cover', render=False,
                        notes=['the cover: ten rings (five clear 12.7, five tinted 3) cut from the deck laminae\'s own sheets (the platter blanks and the puck\'s ring nest inside them) and a 5.6 top, cemented and annealed as the deck; outer faces diamond-polished, inner faces as cut',
                               'two 5.4 holes 8 deep under the first ring take the deck\'s dowels; three clear bumpers (3M SJ5302) under it, so acrylic never sits on acrylic'] if k == 0 else []))
    ct, ct2 = D['cover_top']
    top_s = prism(outline(P, D, ct['inset']), 'z', ct['z0'], ct['z1'])
    top_t = prism(outline(P, D, ct2['inset']), 'z', ct2['z0'], ct2['z1'])
    cov.append(Part('cover-top', top_s, clr[5.6], finish='clear', group='cover', render=False))
    cov.append(Part('cover-top-tint', top_t, tint[3.0], finish='acrylic', group='cover', render=False))
    cover_one = union(*cov_solids, top_s, top_t)
    cov[0].pieces = {'stack': (cover_one, 'acrylic-strata')}
    cov[0].render = True

    # ---- the bearing: a turned brass housing, threaded M30 x 1.5 and clamped under the deck by a brass nut ----
    hz0 = b0 + 0.5
    ft = P['flange_t']
    housing = (cyl('z', S, P['housing_d'], hz0, top - ft) + cyl('z', S, P['flange_d'], top - ft, top)) - cyl('z', S, 14.0, hz0 + 4, top + 1)
    # under the deck, up from the nut: the nut (46 x 7.5), one DIN 2093 C 63 x 31 x 1.8 disc spring (set about 3.0 high),
    # a brass washer 64 x 31 x 3 on the acrylic
    nut = cyl('z', S, 46.0, b0 + 0.5, b0 + 8.0) - cyl('z', S, P['housing_d'] + 0.2, b0, b0 + 9)
    dspring = cyl('z', S, 63.0, b0 + 8.0, b0 + 11.0) - cyl('z', S, 31.0, b0 + 7, b0 + 12)
    cwasher = cyl('z', S, 64.0, b0 + 11.0, b0 + 14.0) - cyl('z', S, 31.0, b0 + 10, b0 + 15)
    plate = cyl('z', S, 13.8, hz0 + 4, hz0 + 6)
    ball_c = hz0 + 9
    ball = Pos(S[0], S[1], ball_c) * Sphere(3.0)
    bushes = union(cyl('z', S, 14.0, hz0 + 12, hz0 + 24) - cyl('z', S, 10.0, hz0 + 11, hz0 + 25),
                   cyl('z', S, 14.0, top - 16, top - 4) - cyl('z', S, 10.0, top - 17, top - 3))
    pz0, pz1 = D['pz0'], D['pz1']
    # the hub: a brass flange (70 x 5) under the platter, a 40 spigot into its bore, shrunk onto the spindle
    hub = (cyl('z', S, 70.0, pz0 - 5, pz0) + cyl('z', S, 40.0, pz0, pz0 + 12)) - cyl('z', S, 10.0, pz0 - 6, pz0 + 13)
    spindle = cyl('z', S, 10.0, ball_c + 3, pz0 + 12) + cyl('z', S, 7.2, pz0 + 12, pz1 + 15)
    hub_screws = [(S[0] + 28 * math.cos(math.radians(60 * k + 30)), S[1] + 28 * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    platter = cyl('z', S, P['platter_d'], pz0, pz1) - cyl('z', S, 40.2, pz0 - 1, pz0 + 12.2) - cyl('z', S, 8.0, pz0, pz1 + 1)
    # six M4 screws up through the hub's flange (heads in 7.8 x 2.4 counterbores under it) into brass inserts bonded
    # into the platter from below (5.6 x 8): no head bears on acrylic, and the record side has no holes
    for c in hub_screws:
        platter = platter - cyl('z', c, 5.6, pz0 - 1, pz0 + 8)
        hub = hub - cyl('z', c, 4.5, pz0 - 6, pz0 + 1) - cyl('z', c, 7.8, pz0 - 6, pz0 - 2.6)
    screws = union(*[cyl('z', c, 4.0, pz0 - 2.8, pz0 + 7) + cyl('z', c, 7.4, pz0 - 5.0, pz0 - 2.8) for c in hub_screws])
    pinserts = union(*[cyl('z', c, 5.6, pz0, pz0 + 8) - cyl('z', c, 4.0, pz0 - 1, pz0 + 9) for c in hub_screws])

    # ---- the motor: Rega's 24 V motor on its plate, the plate screwed to the pocket's shoulder (Rega's hard mount) ----
    bz = D['belt_z']
    mt = top - 3
    mplate = cyl('z', M, P['motor_pocket'] + 14, mt - 3, mt) - cyl('z', M, 26, mt - 4, mt + 1)
    motor = union(cyl('z', M, 50.0, mt - 3 - 30, mt - 3), cyl('z', M, 4.0, mt - 3, bz + 9))
    mscrews = union(*[cyl('z', (M[0] + 42 * math.cos(math.radians(a)), M[1] + 42 * math.sin(math.radians(a))), 3.0, top - 13, mt + 1.6)
                      for a in (30, 150, 270)])
    pdia = D['pulley_d']
    pulley = (cyl('z', M, pdia, bz - 5, bz + 5) + cyl('z', M, pdia + 6, bz + 5, bz + 7)) - cyl('z', M, 4.0, bz - 6, bz + 8)
    R = P['platter_d'] / 2

    def hull(circles, n=360):
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
    belt = prism(hull([(S[0], S[1], R + 0.65), (M[0], M[1], pdia / 2 + 0.65)]), 'z', bz - 2.5, bz + 2.5) - \
        prism(hull([(S[0], S[1], R + 0.05), (M[0], M[1], pdia / 2 + 0.05)]), 'z', bz - 3, bz + 3)
    belt_len = sum(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(hull([(S[0], S[1], R + 0.3), (M[0], M[1], pdia / 2 + 0.3)]),
                                                                       hull([(S[0], S[1], R + 0.3), (M[0], M[1], pdia / 2 + 0.3)])[1:]))

    # ---- the arm-board puck and the arm ----
    puck = cyl('z', A, pd, top - pt, top) - cyl('z', A, 24.0, top - pt - 1, top + 1)
    for c in puck_screws:
        puck = puck - cyl('z', c, 5.5, top - pt - 1, top + 1) - cyl('z', c, 10.0, top - 3, top + 1)
    arm, lift, cart = arm_solids(P, D)

    # ---- the feet: turned stainless, 40 x 14, a Sorbothane puck 40 x 4 under, on an M8 stud; levelled by turning ----
    foot = union(*(union(cyl('z', f, 40.0, 0, 4), cyl('z', f, 40.0, 4, 16) , cyl('z', f, 30.0, 16, b0 - 0.5), cyl('z', f, 8.0, b0 - 0.5, b0 + 12))
                   for f in feet))
    pads = union(*(cyl('z', f, 40.0, 0, 4) for f in feet))
    brass_feet = union(*(union(cyl('z', f, 40.0, 4, 16), cyl('z', f, 30.0, 16, b0 - 0.5)) for f in feet))
    studs = union(*(cyl('z', f, 8.0, b0 - 0.5, b0 + 12) for f in feet))

    # ---- the phono stage in its tunnel, and the brass plate ----
    sx0 = tx0 + (tw - 103) / 2
    phono = box(sx0, D1 - nd - 117, tz0 + 1.5, sx0 + 103, D1 - nd - 2, tz0 + 37.5)
    runners = union(box(sx0 + 8, D1 - nd - 117, tz0, sx0 + 18, D1 - nd - 2, tz0 + 1.5), box(sx0 + 85, D1 - nd - 117, tz0, sx0 + 95, D1 - nd - 2, tz0 + 1.5))
    bplate = box(nx0 + 1, plate_y, b0 + 2.0, nx0 + nw - 1, plate_y + 2.0, b0 + nh + 1.0)
    jacks = [(nx0 + 22, 'rca'), (nx0 + 40, 'rca'), (nx0 + 60, 'earth'), (nx0 + 80, 'toggle'), (nx0 + 100, 'dc')]
    jz = b0 + 1.5 + nh * 0.42
    for x, kind in jacks:
        bplate = bplate - cyl('y', (x, jz), {'rca': 8.2, 'earth': 6.5, 'toggle': 6.4, 'dc': 8.0}[kind], plate_y - 1, plate_y + 3)
    for h in plate_holes:
        bplate = bplate - cyl('y', h, 3.4, plate_y - 1, plate_y + 3)
    hardware = union(*[cyl('y', (x, jz), {'rca': 10.0, 'earth': 9.0, 'toggle': 9.0, 'dc': 10.0}[k], plate_y + 2, plate_y + 2 + {'rca': 9, 'earth': 12, 'toggle': 5, 'dc': 4}[k])
                       for x, k in jacks],
                     box(nx0 + 80 - 1.5, plate_y + 7, jz - 1.5, nx0 + 80 + 1.5, plate_y + 11, jz + 1.5))

    mark = None
    try:
        import turntable
        mark = turntable.mark_top(36.0, (o + P['W'] - 42, o + 16), top + 0.02, 0.1)
    except Exception:
        pass

    out = lam_parts + [
        Part('platter', platter, Machined('cast-acrylic', 'lathe', stock=(310.0, 310.0, 22.0), setup_usd=80.0), finish='acrylic', group='platter',
             pieces={'disc': (platter, 'acrylic-strata-platter')},
             notes=['three laminae (tinted 3 / clear 12.7 / tinted 5.6) cut as 312 discs from the cover rings\' offcuts, cemented and annealed, then turned: rough to 302, annealed again, both faces faced to 21.0, the rim finish-turned to 300 and polished, the clear stratum\'s rim crowned 0.2 for the belt',
                    'the bore 40.2 H7 for the hub\'s spigot; six blind 5.6 holes 8.5 deep on r 28 from below for brass M4 inserts (epoxy-bonded, no thread-locker near the acrylic): the screws come up through the hub, so no head bears on acrylic, and the record side is unbroken; the bond between the laminae carries no torque',
                    'flatness and run-out 0.05 or less; balance after fitting to the hub (5 g mm is ample at 0.56 Hz)']),
        Part('platter-hub', hub, Machined('brass-leadfree', 'lathe'), finish='brass', group='platter',
             notes=['lead-free brass: a 70 x 5 flange, a 40 h6 spigot 12 long, six 4.5 holes on r 28 counterbored 7.8 x 2.4 from below for the screws\' heads; shrunk onto the spindle (heated to 200 C) and finish-turned true to it after']),
        Part('platter-screws', screws, Bought('platter-screws'), finish='steel', group='platter',
             notes=['six M4 x 10 up through the hub into the platter\'s inserts, 0.6 N m; the acrylic bears on the 70 flange (under 2 MPa at six times 750 N), not on screw heads (13-42 MPa before: the audit)']),
        Part('platter-inserts', pinserts, Bought('platter-inserts'), finish='brass', group='platter'),
        Part('spindle', spindle, Machined('stainless-440c', 'lathe', setup_usd=120.0), finish='steel', group='bearing',
             notes=['440C hardened to 58 HRC, ground to 10 g5 at the journals, Ra 0.1 (the drawing and the parts list now agree: not 304, which galls in bronze); the record spindle 7.2; a 6 cup at its foot for the ball',
                    'a vent flat ground along it, 1.0 wide x 0.3 deep over the journals\' length, so air leaves the blind bore as the spindle goes in and the oil is not pumped out']),
        Part('bearing-housing', housing, Machined('brass-leadfree', 'lathe'), finish='brass', group='bearing',
             notes=['lead-free brass, threaded M30 x 1.5 for 30 from its foot, a 50 x 5 flange; the bushes pressed in and line-reamed or honed to 10 H6 (8-12 um running clearance on the g5 journal)',
                    'clamped under the deck by its nut on one disc spring and a brass washer, set to about 1.5 kN by angle (no insert near the bore); 1.0 ml of oil (the space is about 1.2 ml), to about 10 under the upper bush']),
        Part('bearing-nut', nut, Machined('brass-leadfree', 'lathe'), finish='brass', group='bearing'),
        Part('bearing-spring', dspring, Bought('bearing-disc-spring'), finish='steel', group='bearing',
             notes=['DIN 2093 C 63 x 31 x 1.8 (about 1.9 kN flat at 0.75 h0; confirm in the maker\'s table): about 1 kN/mm in series with the acrylic, so 20 K moves the preload about 0.05 kN, not about 3 kN']),
        Part('bearing-washer', cwasher, Machined('brass-leadfree', 'lathe'), finish='brass', group='bearing',
             notes=['64 x 31 x 3, faced flat: spreads 1.5 kN over 2,460 mm2 of acrylic, 0.6 MPa']),
        Part('bushes', bushes, Bought('bearing-bushes-solid'), finish='brass', group='bearing', inside=True),
        Part('ball', ball, Bought('carbide-ball'), finish='steel', group='bearing', inside=True),
        Part('thrust-plate', plate, Bought('thrust-plate'), finish='steel', group='bearing', inside=True),
        Part('motor-plate', mplate, Sheet('aluminium', 3, face='+z'), finish='aluminium', group='motor',
             notes=['3 mm 5052, black anodized, 90 across: on the pocket\'s shoulder on three M3 screws into brass inserts, hard, as Rega fits its motor (no grommets: the audit); the motor screwed under it on Rega\'s mount']),
        Part('motor', motor, Bought('rega-24v-motor'), finish='black', group='motor'),
        Part('motor-screws', mscrews, Bought('motor-mount-screws'), finish='steel', group='motor'),
        Part('pulley', pulley, Machined('aluminium', 'lathe'), finish='aluminium', group='motor',
             notes=[f'belt face {pdia:.2f} at {P["rpm_motor"]:g} rpm for 33.3 (the Neo switches 45 electrically; trim 0.01 rpm); two M3 grub screws on a flat',
                    'PROPOSAL: not turned until the bench test (STOCK-AND-AUDIT.md 3.1) has measured the motor on the US Neo; a test pulley in aluminum first']),
        Part('belt', belt, Bought('flat-belt-core'), finish='rubber', group='platter',
             notes=[f'path {belt_len:.0f} round the 300 rim and the pulley; a belt about {belt_len * 0.95:.0f} long (5 % stretch)']),
        Part('arm-puck', puck, Machined('aluminium', 'lathe'), finish='aluminium', group='arm',
             notes=['6061, 84 x 12, bead-blasted and clear anodised: Rega\'s 24 hole and three-point fixing (holes per Rega\'s template, UNCONFIRMED here); three M5 countersunk screws into brass inserts in the deck\'s shoulder. Another arm takes another puck']),
        Part('arm', union(arm, lift), Bought('rega-rb330'), finish='arm', group='arm'),
        Part('cartridge', cart, Bought('ortofon-2m-black'), finish='cartridge', group='arm'),
        Part('feet', brass_feet, Machined('stainless', 'lathe', stock=(45.0, 45.0, 3 * 24.0)), finish='steel', group='feet',
             notes=['three, turned 303 stainless, bead-blasted, 40 x 12 with a 30 neck, a tapped M8 bore (brass read as amber through the tint: round 48\'s critics); each on a stud in the deck\'s M8 insert, a stainless lock nut over it: level the platter by turning them, then lock',
                    'they locate and level; no isolation is claimed (on pads this small they sit at 50 Hz or more, above the feedback band)']),
        Part('foot-pads', pads, Bought('foot-sorbothane'), finish='rubber', group='feet'),
        Part('foot-studs', studs, Bought('foot-studs'), finish='steel', group='feet'),
        Part('phono-stage', phono, Bought('phono-box-s2'), finish='aluminium-dark', group='phono',
             notes=['Pro-Ject Phono Box S2 whole, on two felt runners in its tunnel; set MM, 40 dB, 47k / 100 pF; slides out from the back for its switches']),
        Part('phono-runners', runners, Bought('phono-felts'), finish='rubber', group='phono'),
        Part('back-plate', bplate, Sheet('brass-sheet', 2, face='+y') if 'brass-sheet' in SHEETS else Machined('brass-leadfree', 'cnc-mill'), finish='brass', group='phono',
             notes=['2 mm lead-free brass, brushed: line out (two RCA), earth post, a 4PDT bypass toggle (in bypass it switches the S2\'s input as well as its output, so the cartridge sees one 47k load), the 18 V inlet; the rating engraved under them; four M3 screws into inserts in the notch']),
        Part('back-hardware', hardware, Bought('back-hardware'), finish='steel', group='phono'),
        Part('cover-bumpers', None, Bought('cover-bumpers')),
        Part('dowels', union(*[cyl('z', c, 5.0, top - 8, top + 4) for c in dowels]), Bought('cover-dowels'), finish='steel', group='cover'),
        Part('inserts', None, Bought('core-inserts')),
        Part('wiring', None, Bought('core-wiring')),
        Part('neo-psu', None, Bought('rega-neo-psu-mk2')),
        Part('bearing-oil', None, Bought('bearing-oil')),
        Part('cement', None, Bought('acrylic-cement-2r')),
        *cov,
    ]
    if mark is not None:
        out.append(Part('mark', mark, Bought('laser-etch-small'), finish='etch'))
    return out


SOLIDS.setdefault('stainless-440c', dict(title='Stainless steel 440C, hardened 58 HRC and ground', density=7.8, usd_per_cm3=0.06))

SHEETS.setdefault('brass-sheet', dict(title='Lead-free brass sheet (C26000 / C27450), brushed', density=8.5, sheet=(610.0, 305.0),
                                      usd_per_m2=320.0, thicknesses=(1.5, 2, 3)))

NOTES = [
    'The deck: seven laminae of stock cell-cast sheet (clear 12.7 strata, tinted 3 contour lines), cemented in one press with ACRIFIX 2R 0190 under vacuum and '
    'annealed (80 C, 10 h, 5 C/h down); faces fly-cut, the terraced outline finish-routed, noses eased R1, outer faces '
    'diamond-polished. Holes and pockets satin, as machined.',
    'The cover: five clear rings with a tinted lamina on each and a clear 5.6 top under a tinted 3, cemented and annealed as the deck; it lifts '
    'off on two stainless dowels, on three clear bumpers. Stood on its back edge it frames the sleeve playing.',
    'The bearing: brass housing M30 x 1.5 clamped by its nut under the deck (10 N m on a PTFE washer); two C932 bronze '
    'bushes honed to 10 H6 on a 10 g5 440C spindle (8-12 um, a vent flat along it); a 6 carbide ball on a lapped 52100 plate; 1.0 ml ISO VG 32. '
    'The nut bears on one DIN 2093 disc spring and a brass washer, set to about 1.5 kN, so the preload holds over temperature. '
    'Shipping: platter off, the spindle in, a nitrile cap over the housing.',
    'The platter: three laminae, turned, on a brass hub shrunk onto the spindle, six M4 screws up through the hub into bonded brass inserts, 0.6 N m, no thread-locker. No mat (acrylic is close '
    'to vinyl in acoustic impedance); a carbon-fibre brush and an earthed housing for static.',
    'The motor: Rega 24 V on its plate, screwed hard to the pocket\'s shoulder as Rega fits it (no grommets); the Neo PSU MK2 beside '
    'the record player switches 33/45 and trims speed. The pulley is turned to the motor\'s speed as measured on the bench (300 rpm expected at 60 Hz).',
    'The arm: Rega RB330 on an aluminum puck (Rega three-point) at 222 from the spindle; Rega spacers set the height '
    'to the record (28.8 over the deck\'s top, set on the first sample with the tube level).',
    'The phono stage: Pro-Ject Phono Box S2 in a tunnel from the back, on felt runners; the brass plate closes it and '
    'carries line out, earth, a 4PDT bypass toggle and the 18 V inlet (Pro-Ject\'s own listed adapter). The arm\'s lead runs '
    'in a groove under the deck to it.',
    'Feet: three, turned stainless on Sorbothane, on M8 studs into brass inserts; level the platter, then lock the nuts. They locate and level; '
    'no isolation is claimed. For isolation, a platform at 3-5 Hz under the record player.',
    'Before the first sample: bench the motor on the US Neo (STOCK-AND-AUDIT.md 3.1); with the arm in hand, check its counterweight clears the cover\'s top rings.',
    'First-sample checks: speed and wow (under 0.1 % weighted) with a test record; a tap test on the deck with the stylus '
    'on a still record; the bond lines checked against a light table for bubbles before the outline is finish-routed.',
]

MATERIALS = dict(C.MATERIALS,
                 clear={'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#F4F6F5', 'radius': 0.05, 'roughness': 0.04},
                 **{'acrylic-strata': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.025, 'roughness': 0.05}},
                 **{'acrylic-strata-platter': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.025, 'roughness': 0.05}},
                 **{'aluminium-dark': {'preset': 'metal', 'color': '#2A2A2C', 'roughness': 0.45}},
                 cartridge={'preset': 'satin_paint', 'color': '#0E0E0F', 'roughness': 0.35, 'specular': 0.5})

PRODUCT = Product('mantle-outcrop', 'Mantle: Outcrop (proposal B)', 'Belt-drive record player cut from a stack of bonded cast sheet, with a lift-off strata cover',
                  params=P, parts=parts, count=1, notes=NOTES, materials=MATERIALS, variants=C.VARIANTS,
                  touching=[('deck-L*', 'deck-L*'), ('deck-L*-inlay', 'deck-L*'), ('cover-C*', 'cover-C*'), ('cover-C*', 'cover-top*'), ('cover-top', 'cover-top-tint'), ('phono-runners', 'phono-stage'),
                            ('bushes', 'bearing-housing'), ('bushes', 'spindle'), ('platter-hub', 'spindle'), ('platter-screws', 'platter*'),
                            ('foot-studs', 'feet'), ('foot-studs', 'deck-L*'), ('foot-pads', 'feet'), ('dowels', 'deck-L*'), ('dowels', 'cover-C*'),
                            ('back-hardware', 'back-plate'), ('motor-screws', 'motor-plate'), ('motor-screws', 'deck-L*'), ('motor', 'motor-plate'),
                            ('platter-inserts', 'platter'), ('platter-screws', 'platter-hub'), ('platter-screws', 'platter-inserts'), ('bearing-spring', 'bearing-*'), ('bearing-washer', 'deck-L*'), ('bearing-spring', 'bearing-washer'),
                            ('bearing-nut', 'bearing-housing'), ('arm', 'arm-puck')],
                  drawing_prefix='MO')

if __name__ == '__main__':
    d = derived(P)
    print({k: (tuple(round(x, 1) for x in v) if isinstance(v, tuple) else v) for k, v in d.items() if k not in ('lams', 'cover', 'cover_top')})
    for l in d['lams'] + d['cover'] + d['cover_top']:
        print(l)
