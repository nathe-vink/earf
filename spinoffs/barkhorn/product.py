"""barkhorn (a working name): a two-way horn loudspeaker after the owner's reference photograph of Friendly Pressure's
speakers (reference/friendly-pressure-owner-2026-10-10.jpg), in two finishes: birch bark and eucalyptus bark, each
with its waveguide cast in a translucent resin tinted from its bark.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/product.py
    .venv-fab/bin/python spinoffs/barkhorn/product.py            # the bass box's numbers

What the photograph shows, and how it is read here:
- a bass cabinet about 1 : 1.6 (wide to tall), a thin wooden shell (walnut there; bark here) framing a pale front
  panel set back in it;
- a 15 in black paper cone in a wide off-white ring, its centre a little above the cabinet's middle;
- a small square port at the bottom right;
- a frosted, translucent waveguide on top: a rounded rectangle about 1.72 : 1 (measured again in round 4; round 1
  read 2.1 : 1), wider than the cabinet (about 1.12 times), its rim thin, the driver's dark throat near its centre,
  on four slim posts (a wide pair in front, a narrow pair behind), its rim just above the cabinet.
Sizes are scaled from the photograph by its turntable (about 450 wide): the cabinet about 560 x 880; the waveguide
from the cabinet: about 630 x 366, its rim about 37 above the top.

Parts from the horn-speaker research of 2026-10-10 (components.json): FaitalPRO 15PR400-8 woofer (treated paper cone),
BMS 4550-16 compression driver (polyester diaphragm, crossed at 800 Hz or above), a Hypex FusionAmp FA122.
"""
import math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'studio', 'fabkit'))
from kit import *                                                    # noqa: E402,F403
from speaker.drivers import driver_part, place                      # noqa: E402
from speaker.horn import waveguide_shell, waveguide_lens, waveguide_slab, round_horn, tractrix   # noqa: E402

import json  # noqa: E402
LIB = json.load(open(os.path.join(HERE, '..', '..', 'studio', 'fabkit', 'library', 'components.json')))
LIB.update(json.load(open(os.path.join(HERE, 'components.json'))))

P = dict(
    W=560.0, D=420.0, H=880.0, T=18.0,           # the cabinet's shell, outside; it stands on the floor on glides
    # the shell's finish: 'bark' (bark sheet laminated to the plywood), or 'pressed' (round 4: faced in pressed recycled
    # HDPE sheet, `skin` thick, screwed from inside through oversized holes so it can move with the seasons, `gap`
    # between sheets at the corners; the panel faced in `face_t` sheet; pressed.py builds it)
    finish='bark', skin=dict(t=8.0, face_t=5.0, gap=1.5, hole=14.0, stock='recycled-hdpe'),
    inset=24.0,                                  # the front panel set back in the shell (the photograph's frame): deep
                                                 # enough for a cover to clear the cone at twice its Xmax
    woofer='faital-15pr400-8', woofer_z=478.0,   # its centre 45.7 % down from the top, as photographed
    gasket=1.0,
    ring=dict(od=436.0, id=350.0, t=6.0),        # the off-white ring over the frame, 6 mm MDF, standing on the panel
    port=dict(a=100.0, wall=4.0, x=455.0, z=113.0),   # the square port, bottom right, as photographed
    fb=38.0,
    brace_z=200.0, brace_window=(420.0, 300.0),
    amp='hypex-fa122', amp_z=520.0,
    hf='bms-4550-16',
    # the waveguide, a rounded rectangle about 640 x 300 with its mouth filling the face (612 x 272), 170 deep, in one of
    # the forms of the 2026-10-11 study: 'shell' (a thin cast shell following its flare, a pod behind round the driver),
    # 'lens' (thin at its edge, deep only in the middle where it holds the driver), 'slab' (a slim slab, after the
    # photograph's, the rest of the flare in a tail behind), 'pebble' (the slab's soft rolled rim on the lens's smooth
    # back) or 'round' (a round tractrix horn, a rolled lip)
    horn=dict(form='cast', mouth_w=612.0, mouth_h=272.0, d=170.0, r0=12.7, wall=6.0, rim=10.0, n_mouth=4.5,
              pod_r=74.0, pod_back=70.0, dome=45.0, boss=dict(d=130.0, t=12.0, bolt_d=76.2, bolts=2, bolt_hole=6.5),
              # 'cast' (round 4, the owner's second notes of 2026-10-11): the photograph's horn, measured again: about 630 x 366 outside (1.72 : 1, not the
              # 2.1 : 1 read before), a thin shell whose flare runs nearly to its edge, a 10 mm rim rounded right round,
              # squarer corners (about 70 mm), the driver in a round pod behind, closed by a cap; on four posts
              cast=dict(mouth_w=610.0, mouth_h=346.0, d=200.0, wall=6.0, rim=10.0, round_rim=4.0, n_mouth=7.0,
                        pod_r=70.0, pod_back=70.0, dome=30.0, gap=37.0, boss_d=126.0,   # the boss 1 clear inside the pod
                        posts=dict(front=(183.0, 35.0), back=(35.0, 35.0), d=10.0, bore=7.0, pad_d=26.0, pad_h=6.0,
                                   insert_d=13.0, insert_depth=14.0, top_insert=(14.0, 15.0), cable_post=2),
                        # its back: 'shell' (the photograph's: the shell follows the flare to a round pod round the driver)
                        # or 'tub' (the outside runs straight back from the rim to a flat back that hides the driver, the
                        # flare its own skin inside; the back pair of posts wider, under its flat bottom)
                        back='shell',
                        tub=dict(back=76.0, taper=0.08, round=0.25, end=0.6, lid=30.0, seam=0.4, posts_back=(120.0, 20.0))),
              lens=dict(rim=14.0, back=78.0, back_r=84.0, taper=0.55, edge=5.0, pod_r=68.0),
              slab=dict(rim=16.0, slab_t=64.0),
              pebble=dict(rim=30.0, back=78.0, back_r=88.0, taper=0.7, edge=27.0, pod_r=68.0),
              round=dict(fc=400.0, lip=22.0, wall=6.0, rods_front=90.0)),
    gap=80.0, rod_d=10.0, rods_front=(150.0, 40.0),   # the study forms' two front rods: +-x from the centre, y back from the face
    # the front's covers, options (the photograph shows the panel bare), each in the recess in front of the panel, 1.5
    # clear of the shell all round: a cloth grille (an MDF frame, the cloth stretched over it), a slotted grille
    # (lenticels for birch: short horizontal dashes; strips for eucalyptus: long vertical ones), each flush with the
    # shell's front on four pegs into cups in the panel's corners; or the panel faced in bark or cork round the ring
    # and the port
    cover=dict(gap=1.5, cloth_face=1.0, frame_t=6.0, frame_w=30.0, bar_z=205.0, bar_w=24.0,
               grille_t=6.0, border=22.0, slot_w=6.0,
               lenticel=dict(pitch=14.0, length=(22.0, 120.0), gap=(10.0, 34.0), seed=11),
               strips=dict(pitch=16.0, length=(90.0, 260.0), gap=(14.0, 30.0), seed=5),
               face_t=dict(bark=1.0, cork=3.0),
               alternatives=False,             # the round 2 and 3 covers the owner did not pick, back as options
               disc_t=12.0,                    # the cloth disc's frame, over the woofer alone, in front of the ring
               disc_magnet=dict(d=15.0, t=3.0, n=4)),   # its magnet pairs, one in its back and one behind the ring
)


def lenticels(x0, z0, x1, z1, w, pitch, length, gap, seed):
    """Birch's lenticels as a grille's slots: rows of short horizontal dashes, their lengths and gaps random (seeded,
    so a rebuild cuts the same panel), most short, a few long, and each row starting at its own offset."""
    rng = random.Random(seed)
    out, z = [], z0 + w / 2
    while z <= z1 - w / 2:
        x = x0 + rng.uniform(0.0, length[0])
        while True:
            L = rng.uniform(*length) if rng.random() < 0.25 else rng.uniform(length[0], (length[0] + length[1]) / 2.5)
            L = min(L, x1 - x)
            if L < length[0]:
                break
            out.append((x + L / 2, z, L, w, False))
            x += L + rng.uniform(*gap)
        z += pitch
    return out


def strips(x0, z0, x1, z1, w, pitch, length, gap, seed):
    """A eucalyptus's strips as a grille's slots: columns of long vertical slots, their lengths and the bridges
    between them random (seeded), so the slats between the columns are tied every 90 to 260."""
    rng = random.Random(seed)
    out, x = [], x0 + w / 2
    while x <= x1 - w / 2:
        z = z0 + rng.uniform(0.0, length[0] * 0.6)
        while True:
            L = min(rng.uniform(*length), z1 - z)
            if L < length[0] * 0.5:
                break
            out.append((x, z + L / 2, L, w, True))
            z += L + rng.uniform(*gap)
        x += pitch
    return out


def port_length(P, net_l):
    """The square port's length tuning `net_l` litres to fb (one end flanged, one free; the end correction of the
    round port of the same area)."""
    c, a = 343.0, P['port']['a'] / 1000
    sp = a * a
    d_eq = 2 * a / math.sqrt(math.pi)
    w = 2 * math.pi * P['fb']
    return (sp * c * c / (w * w * net_l * 1e-3) - 0.732 * d_eq) * 1000


def net_volume(P, port_l=60.0):
    W, D, H, T = P['W'], P['D'], P['H'], P['T']
    inner = (W - 2 * T) * (D - T - (P['inset'] + T)) * (H - 2 * T) / 1e6
    o = P['port']['a'] + 2 * P['port']['wall']
    port = o * o * port_l / 1e6
    brace = ((W - 2 * T) * (D - P['inset'] - 3 * T) - P['brace_window'][0] * P['brace_window'][1]) * T / 1e6
    return inner - 4.5 - 1.3 - port - brace      # woofer (estimated), amplifier module, port, brace


def parts(P):
    W, D, H, T = P['W'], P['D'], P['H'], P['T']
    cx = W / 2
    yb = P['inset']                                   # the front panel's face
    wf = LIB[P['woofer']]['geom']; amp = LIB[P['amp']]['geom']; hf = LIB[P['hf']]['geom']
    pt = P['port']
    plen = round(port_length(P, net_volume(P)), 1)
    ply = lambda grain, face=None: Sheet('baltic-birch', T, face=face, grain=grain)

    # the front panel, set back in the shell: the woofer flush in its rebate, its T-nut holes, the square port
    baffle = box(T, yb, T, W - T, yb + T, H - T)
    wz = P['woofer_z']
    baffle -= cyl('y', (cx, wz), wf['frame_od'] + 1.6, yb - 1, yb + wf['flange_t'] + P['gasket'])
    baffle -= cyl('y', (cx, wz), wf['cutout'], yb - 1, yb + T + 1)
    for k in range(wf['bolts']):
        a = 2 * math.pi * (k + 0.5) / wf['bolts']
        baffle -= cyl('y', (cx + wf['bolt_d'] / 2 * math.cos(a), wz + wf['bolt_d'] / 2 * math.sin(a)), 7.0, yb - 1, yb + T + 1)
    o = pt['a'] + 2 * pt['wall']
    baffle -= box(pt['x'] - o / 2 - 0.2, yb - 1, pt['z'] - o / 2 - 0.2, pt['x'] + o / 2 + 0.2, yb + T + 1, pt['z'] + o / 2 + 0.2)

    back = box(T, D - T, T, W - T, D, H - T)
    az = P['amp_z']
    back -= box(cx - (amp['plate_w'] + 0.5) / 2, D - 4.5, az - (amp['plate_h'] + 0.5) / 2, cx + (amp['plate_w'] + 0.5) / 2, D + 1, az + (amp['plate_h'] + 0.5) / 2)
    back -= box(cx - amp['cutout_w'] / 2, D - T - 1, az - amp['cutout_h'] / 2, cx + amp['cutout_w'] / 2, D, az + amp['cutout_h'] / 2)

    # the top: the cast horn's four posts screw into brass inserts in it (the front pair stand over the front panel's
    # top edge, so nothing can hang below; the HF cable comes down inside one of the rear pair and through a hole under
    # its insert), or the study forms' rods stand in inserts in it, the cable through a gland behind them
    top = box(T, 0, H - T, W - T, D, H)
    hz = P['horn']
    rods = rod_places(P)
    if hz['form'] == 'cast':
        pp = hz['cast']['posts']
        for i, (rx, ry) in enumerate(rods):
            top -= cyl('z', (rx, ry), pp['top_insert'][0], H - pp['top_insert'][1], H + 1)
            if i == pp['cable_post']:
                top -= cyl('z', (rx, ry), pp['bore'] + 1.0, H - T - 1, H)
    else:
        for rx, ry in rods:
            top -= cyl('z', (rx, ry), 12.0, H - 15.0, H + 1)      # M8 threaded inserts, 12 drilled 15 deep
        top -= cyl('z', (cx, D - 70.0), 16.5, H - T - 1, H + 1)
    bottom = box(T, 0, 0, W - T, D, T)
    brace = box(T, yb + T, P['brace_z'], W - T, D - T, P['brace_z'] + T)
    bw, bd = P['brace_window']
    ym = (yb + T + D - T) / 2
    brace -= box(cx - bw / 2, ym - bd / 2, P['brace_z'] - 1, cx + bw / 2, ym + bd / 2, P['brace_z'] + T + 1)

    out = [
        Part('left', box(0, 0, 0, T, D, H), ply('z'), finish='bark', group='cabinet'),
        Part('right', box(W - T, 0, 0, W, D, H), ply('z'), finish='bark', group='cabinet'),
        Part('top', top, ply('x', '+z'), finish='bark', group='cabinet'),
        Part('bottom', bottom, ply('x', '-z'), finish='bark', group='cabinet'),
        Part('front-panel', baffle, ply('z', '-y'), finish='panel', group='cabinet'),
        Part('back', back, ply('z', '+y'), finish='bark', group='cabinet'),
        Part('brace', brace, ply('x', '+z'), finish='raw', group='cabinet', inside=True),
    ]

    # the ring over the woofer's frame, standing on the panel; the square port's tube, printed
    r = P['ring']
    ring = cyl('y', (cx, wz), r['od'], yb - r['t'], yb) - cyl('y', (cx, wz), r['id'], yb - r['t'] - 1, yb + 1)
    for k in range(wf['bolts']):          # pockets behind it for the woofer's screw heads: it lies flat over the frame
        a = 2 * math.pi * (k + 0.5) / wf['bolts']
        ring -= cyl('y', (cx + wf['bolt_d'] / 2 * math.cos(a), wz + wf['bolt_d'] / 2 * math.sin(a)), 14.0, yb - 4.0, yb + 1)
    mg = P['cover']['disc_magnet']
    for mx, mz in disc_magnets(P, cx, wz):  # and for the cloth disc's magnets, behind its face, so the face stays clean
        ring -= cyl('y', (mx, mz), mg['d'] + 0.2, yb - mg['t'] - 0.2, yb + 1)
    out.append(Part('woofer-ring', ring, Sheet('mdf', r['t'], face='-y'), finish='ring', group='cabinet',
                    notes=['sprayed in the ring colour; held by four dots of silicone on the panel; eight pockets behind it '
                           'clear the woofer\'s screw heads; four more take the cloth disc\'s magnets (an option)']))
    tube = box(pt['x'] - o / 2, yb, pt['z'] - o / 2, pt['x'] + o / 2, yb + plen, pt['z'] + o / 2)
    tube -= box(pt['x'] - pt['a'] / 2, yb - 1, pt['z'] - pt['a'] / 2, pt['x'] + pt['a'] / 2, yb + plen + 1, pt['z'] + pt['a'] / 2)
    out.append(Part('port', tube, Printed('asa', orient='on end'), finish='port', group='cabinet',
                    notes=[f'{pt["a"]:g} square, {plen:.0f} long from the panel\'s face: tunes the box to {P["fb"]:g} Hz; print 15 longer and trim to tune']))

    woofer, _ = driver_part('woofer', P['woofer'], wf, centre=(cx, yb, wz))
    out.append(woofer)
    plate = box(cx - amp['plate_w'] / 2, D - 3.0, az - amp['plate_h'] / 2, cx + amp['plate_w'] / 2, D, az + amp['plate_h'] / 2)
    module = box(cx - amp['cutout_w'] / 2 + 4, D - amp['depth'], az - amp['cutout_h'] / 2 + 6, cx + amp['cutout_w'] / 2 - 4, D - 3.0, az + amp['cutout_h'] / 2 - 6)
    out.append(Part('amp-plate', plate.fuse(module), Bought(P['amp']), finish='amp'))

    # the waveguide (the form chosen in P['horn']), its face flush with the cabinet's front and its mouth's lower rim
    # `gap` above the top; it stands on three rods cut to its underside
    wg = waveguide(P)
    shell, zc = wg['shell'], wg['zc']
    out.append(Part('waveguide', shell, Machined('cast-resin', 'cast', setup_usd=900.0), finish='horn', group='horn',
                    notes=wg['notes']))
    if wg['cap'] is not None:
        out.append(Part('waveguide-cap', wg['cap'], Machined('cast-resin', 'cast', setup_usd=250.0), finish='horn', group='horn',
                        notes=[('the tub\'s back, a lid; six M4 screws into inserts round its edge; the cable leaves through a post below'
                                if hz['form'] == 'cast' and hz['cast']['back'] == 'tub' else
                                'closes the pod behind the driver; a spigot locates it, three M4 screws hold it; '
                                + ('the cable leaves through a post below' if hz['form'] == 'cast' else 'the cable leaves through its centre'))]))
    hfp, _ = driver_part('hf', P['hf'], hf, centre=(cx, wg['throat_y'] + hz['boss']['t'], zc))
    out.append(hfp)
    from build123d import Axis
    if hz['form'] == 'cast':
        out += posts(P, rods, shell)
        rods = []                                 # the study forms' rods below
    for i, (rx, ry) in enumerate(rods, 1):
        # where the rod meets the shell's underside: the lowest hit over its axis and its rim, so no edge pokes in
        ztop = 1e9
        for a in [None] + [2 * math.pi * k / 12 for k in range(12)]:
            px, py = (rx, ry) if a is None else (rx + P['rod_d'] / 2 * math.cos(a), ry + P['rod_d'] / 2 * math.sin(a))
            hits = shell.find_intersection_points(Axis((px, py, H + 1.0), (0, 0, 1)))
            ztop = min([ztop] + [h[0].Z for h in hits if h[0].Z > H + 1.0])
        ztop -= 0.2
        out.append(Part(f'rod-{i}', cyl('z', (rx, ry), P['rod_d'], H, ztop), Machined('stainless', 'lathe'), finish='rod',
                        group='horn', notes=[f'{ztop - H:.0f} long; M8 thread 15 deep each end']))

    out += covers(P, wz, o)
    if P['finish'] == 'pressed':
        out += skins(P, rod_places(P), amp)
    else:
        out.append(Part('bark', None, Bought('bark-sheet'), qty=2, notes=['about 1.75 m2 a speaker: the shell\'s sides, top, bottom, back and front edges']))
    out += [
        Part('woofer-fixings', None, Bought('m6-tnut-set'), notes=['the T-nuts hammered in from inside before the glue-up']),
        Part('hf-fixings', None, Bought('m6-hf-screws')),
        *([Part('post-inserts', None, Bought('post-inserts'))] if hz['form'] == 'cast' else []),
        Part('gasket', None, Bought('gasket-foam'), qty=2),
        Part('damping', None, Bought('damping-fill'), qty=2),
        Part('amp-fixings', None, Bought('amp-screws')),
        Part('cable', None, Bought('speaker-cable-1m'), qty=3),
        Part('terminals', None, Bought('push-on-terminal'), qty=4),
        Part('hf-pad', None, Bought('attenuator-l-pad')),
        Part('glides', None, Bought('felt-glides')),
    ]
    return out


def rod_places(P):
    """Where the waveguide's supports stand on the top (x, y): the cast horn's four posts, as in the photograph (a wide
    pair under the front of its mouth, a narrow pair under the driver's pod), or the study forms' three rods (two under
    the mouth, one under the back)."""
    hz, cx = P['horn'], P['W'] / 2
    f = hz['form']
    if f == 'cast':
        c, pp = hz['cast'], hz['cast']['posts']
        (fx, fy), (bx, by) = pp['front'], (c['tub']['posts_back'] if c['back'] == 'tub' else pp['back'])
        return [(cx - fx, fy), (cx + fx, fy), (cx - bx, c['d'] + by), (cx + bx, c['d'] + by)]
    fx, fy = (hz['round']['rods_front'], P['rods_front'][1]) if f == 'round' else P['rods_front']
    back = {'lens': hz['lens']['back'], 'pebble': hz['pebble']['back']}.get(f, hz['pod_back'])
    depth = round_profile(P)[-1][0] if f == 'round' else hz['d']
    return [(cx - fx, fy), (cx + fx, fy), (cx, depth + back * 0.5)]


def skins(P, places, amp):
    """The shell faced in pressed recycled plastic sheet (P['finish'] 'pressed'): each side, the top and the back a
    sheet `skin` thick laid on the plywood, strips over the shell's front edges; a gap at each corner, so every sheet can
    move (HDPE grows about 2 to 3.5 mm on 880 over 20 degrees); each screwed from inside through 8 mm holes in the
    plywood (No. 8 pan heads and washers at about 150 centres), so no fixing shows."""
    W, D, H, T = P['W'], P['D'], P['H'], P['T']
    sk = P['skin']; ts, g = sk['t'], sk['gap']
    up = lambda face=None: Sheet(sk['stock'], ts, face=face, grain='z')
    fix = 'screwed from inside through 8 mm holes in the plywood (No. 8 x 25 pan heads, washers, about 150 apart), never glued'
    top = box(g, g, H, W - g, D + ts, H + ts)
    for rx, ry in places:
        top -= cyl('z', (rx, ry), sk['hole'], H - 1, H + ts + 1)       # the posts pass through, the sheet free round them
    back = box(g, D, 0, W - g, D + ts, H - g)
    az = P['amp_z']
    back -= box(W / 2 - (amp['plate_w'] + 1.0) / 2, D - 1, az - (amp['plate_h'] + 1.0) / 2, W / 2 + (amp['plate_w'] + 1.0) / 2, D + ts + 1,
                az + (amp['plate_h'] + 1.0) / 2)
    out = [Part('skin-left', box(-ts, g, 0, 0, D + ts, H + ts), up('-x'), finish='bark', group='cabinet', notes=[fix]),
           Part('skin-right', box(W, g, 0, W + ts, D + ts, H + ts), up('+x'), finish='bark', group='cabinet', notes=[fix]),
           Part('skin-top', top, Sheet(sk['stock'], ts, face='+z', grain='y'), finish='bark', group='cabinet',
                notes=[fix + f'; the posts through {sk["hole"]:g} holes, free of it']),
           Part('skin-back', back, up('+y'), finish='bark', group='cabinet', notes=[fix + '; cut round the amplifier\'s plate']),
           Part('skin-edge-left', box(-ts, -ts, 0, T, 0, H + ts), up('-y'), finish='bark', group='cabinet',
                notes=['over the shell\'s front edge and the side sheet\'s, ' + fix]),
           Part('skin-edge-right', box(W - T, -ts, 0, W + ts, 0, H + ts), up('-y'), finish='bark', group='cabinet',
                notes=['over the shell\'s front edge and the side sheet\'s, ' + fix]),
           Part('skin-edge-top', box(T + g, -ts, H - T, W - T - g, 0, H + ts), Sheet(sk['stock'], ts, face='-y', grain='x'), finish='bark',
                group='cabinet', notes=['over the top\'s front edge and the top sheet\'s, ' + fix]),
           Part('skin-edge-bottom', box(T + g, -ts, 0, W - T - g, 0, T), Sheet(sk['stock'], ts, face='-y', grain='x'), finish='bark',
                group='cabinet', notes=['over the bottom\'s front edge, ' + fix]),
           Part('skin-fixings', None, Bought('skin-fixings'), notes=['about 60 a speaker'])]
    return out


def disc_magnets(P, cx, wz):
    """The cloth disc's magnet pairs' centres (x, z): on the ring's mid-radius, between the woofer's screws."""
    r, n = P['ring'], P['cover']['disc_magnet']['n']
    rm = (r['od'] + r['id']) / 4
    return [(cx + rm * math.cos(2 * math.pi * k / n), wz + rm * math.sin(2 * math.pi * k / n)) for k in range(n)]


def posts(P, places, shell):
    """The cast horn's four posts: stainless lamp tube threaded M10 x 1 at both ends, each screwed into a brass insert
    bonded in a pad under the horn and into another in the top; the HF cable comes down inside one of them."""
    from build123d import Axis
    H, T = P['H'], P['T']
    c = P['horn']['cast']; pp = c['posts']
    out = []
    for i, (rx, ry) in enumerate(places, 1):
        foot = 1e9                                # the pad's flat foot: rays just outside the insert's hole
        for k in range(8):
            a = 2 * math.pi * k / 8
            rr = (pp['insert_d'] / 2 + pp['pad_d'] / 2) / 2
            hits = shell.find_intersection_points(Axis((rx + rr * math.cos(a), ry + rr * math.sin(a), H + 1.0), (0, 0, 1)))
            foot = min([foot] + [h[0].Z for h in hits if h[0].Z > H + 1.0])
        z0, z1 = H - pp['top_insert'][1] + 2.0, foot + pp['insert_depth'] - 2.0
        tube = cyl('z', (rx, ry), pp['d'], z0, z1) - cyl('z', (rx, ry), pp['bore'], z0 - 1, z1 + 1)
        cable = i == pp['cable_post'] + 1
        out.append(Part(f'post-{i}', tube, Machined('stainless', 'lathe'), finish='rod', group='horn',
                        notes=[f'{z1 - z0:.0f} long ({foot - H:.0f} showing): stainless tube {pp["d"]:g} x {pp["bore"]:g}, threaded M10 x 1 '
                               f'{pp["insert_depth"] - 2:g} at the top and {pp["top_insert"][1] - 2:g} at the foot, each end into a brass insert'
                               + ('; the HF cable runs down inside it' if cable else '')]))
    return out


def round_profile(P):
    return tractrix(P['horn']['round']['fc'], P['horn']['r0'])


def waveguide(P):
    """The waveguide in the form P['horn']['form'], placed: {'shell', 'cap' (or None), 'zc' (its axis's height),
    'throat_y' (where the driver's face meets it), 'notes'}."""
    hz, cx, H = P['horn'], P['W'] / 2, P['H']
    f = hz['form']
    cast = ('cast in tinted translucent polyurethane in a two-part silicone mould from a CNC-cut plug, bead-blasted to '
            'frost; M8 inserts bonded into pads inside its underside take the rods')
    cap = None
    if f == 'cast':
        c, pp = hz['cast'], hz['cast']['posts']
        depth, half_h = c['d'], c['mouth_h'] / 2 + c['rim']
        pads = [dict(x=rx - cx, z=depth - ry, d=pp['pad_d'], h=pp['pad_h'], bore=pp['insert_d'], bore_depth=pp['insert_depth'],
                     cable=(pp['bore'] if i == pp['cable_post'] else 0.0)) for i, (rx, ry) in enumerate(rod_places(P))]
        shell, cap = waveguide_shell(c['mouth_w'], c['mouth_h'], depth, r0=hz['r0'], wall=c['wall'], rim=c['rim'], n_mouth=c['n_mouth'],
                                     pod_r=c['pod_r'], pod_back=c['pod_back'], dome=c['dome'], boss={**hz['boss'], 'd': c['boss_d']},
                                     round_rim=c['round_rim'], pads=pads, cap_hole=False, solid_neck=True,
                                     tub=c['tub'] if c['back'] == 'tub' else None)
        outside = (f'the outside a tub running straight back from the rim to a flat back {c["tub"]["back"]:g} behind the throat, hiding the '
                   f'driver, the flare its own {c["wall"]:g} skin inside it (the space between filled with damping foam); the back a lid, '
                   f'six M4 screws round its edge') if c['back'] == 'tub' else \
                  (f'a shell {c["wall"]:g} thick following its flare; the driver in a pod {2 * c["pod_r"]:g} across behind, closed by a cap')
        bb = shell.bounding_box()                 # outside, as built: the rounded rim draws in a little from mouth + rim
        notes = [f'mouth {c["mouth_w"]:g} x {c["mouth_h"]:g}, {depth:g} deep, 1 in throat; a {c["rim"]:g} rim rounded right round, '
                 f'{bb.max.X - bb.min.X:.0f} x {2 * bb.max.Y:.0f} outside; {outside}; four pads under it take the posts\' '
                 f'brass inserts; {cast}'.replace('; M8 inserts bonded into pads inside its underside take the rods', '')]
        zc = H + c['gap'] + half_h
        shell = place(shell, (cx, depth, zc), (0, -1, 0))
        cap = place(cap, (cx, depth, zc), (0, -1, 0))
        return dict(shell=shell, cap=cap, zc=zc, throat_y=depth, notes=notes)
    if f == 'shell':
        shell, cap = waveguide_shell(hz['mouth_w'], hz['mouth_h'], hz['d'], r0=hz['r0'], wall=hz['wall'], rim=hz['rim'],
                                     n_mouth=hz['n_mouth'], pod_r=hz['pod_r'], pod_back=hz['pod_back'], dome=hz['dome'], boss=hz['boss'])
        depth, half_h = hz['d'], hz['mouth_h'] / 2 + hz['rim']
        notes = [f'mouth {hz["mouth_w"]:g} x {hz["mouth_h"]:g}, {hz["d"]:g} deep, 1 in throat; a shell {hz["wall"]:g} thick following '
                 f'its flare, {hz["rim"]:g} at the rim, and a pod {2 * hz["pod_r"]:g} across behind it round the driver; {cast}']
    elif f in ('lens', 'pebble'):
        L = hz[f]
        shell = waveguide_lens(hz['mouth_w'], hz['mouth_h'], hz['d'], r0=hz['r0'], rim=L['rim'], n_mouth=hz['n_mouth'], back=L['back'],
                               back_r=L['back_r'], taper=L['taper'], edge=L['edge'], pod_r=L['pod_r'], boss=hz['boss'])
        depth, half_h = hz['d'], hz['mouth_h'] / 2 + L['rim'] - L['edge']
        notes = [f'mouth {hz["mouth_w"]:g} x {hz["mouth_h"]:g}, {hz["d"]:g} deep, 1 in throat; a lens: a {L["rim"]:g} face round the mouth, '
                 f'the body curving back to a round back {2 * L["back_r"]:g} across, {hz["d"] + L["back"]:g} deep in all, the driver in a pod '
                 f'inside it; cast hollow (a 7 mm skin) in production, {cast}']
    elif f == 'slab':
        S = hz['slab']
        shell = waveguide_slab(hz['mouth_w'], hz['mouth_h'], hz['d'], r0=hz['r0'], rim=S['rim'], n_mouth=hz['n_mouth'], slab_t=S['slab_t'],
                               wall=hz['wall'], pod_r=hz['pod_r'], pod_back=hz['pod_back'] + 6.0, boss=hz['boss'])
        depth, half_h = hz['d'], hz['mouth_h'] / 2 + S['rim']
        notes = [f'mouth {hz["mouth_w"]:g} x {hz["mouth_h"]:g}, {hz["d"]:g} deep, 1 in throat; a slab {S["slab_t"]:g} thick, its edges '
                 f'rounded right round, the rest of the flare in a tail behind running into a pod round the driver; {cast}']
    else:
        R = hz['round']
        prof = round_profile(P)
        shell = round_horn(prof, wall=R['wall'], lip=R['lip'])
        from build123d import Pos, Cylinder, Align
        pod = Pos(0, 0, -hz['pod_back']) * (Cylinder(hz['pod_r'], hz['pod_back'], align=(Align.CENTER, Align.CENTER, Align.MIN)) -
                                           Pos(0, 0, R['wall']) * Cylinder(hz['pod_r'] - R['wall'], hz['pod_back'] - 2 * R['wall'],
                                                                          align=(Align.CENTER, Align.CENTER, Align.MIN)))   # closed: a can round the driver
        pod -= Cylinder(hz['r0'], 2 * R['wall'], align=(Align.CENTER, Align.CENTER, Align.CENTER))
        shell = shell + pod
        depth = prof[-1][0]
        b = shell.bounding_box()
        half_h = max(b.max.X, b.max.Y)
        notes = [f'a round tractrix horn for {R["fc"]:g} Hz: mouth {2 * prof[-1][1]:.0f} across, {depth:.0f} long, its lip rolled back on '
                 f'{R["lip"]:g}, {R["wall"]:g} thick; the driver in a round pod behind its throat; {cast}']
    zc = H + P['gap'] + half_h
    shell = place(shell, (cx, depth, zc), (0, -1, 0))
    if cap is not None:
        cap = place(cap, (cx, depth, zc), (0, -1, 0))
    return dict(shell=shell, cap=cap, zc=zc, throat_y=depth, notes=notes)


def covers(P, wz, port_o):
    """The front: the panel faced in bark under a cloth disc over the woofer (the owner's pick, 2026-10-11). With
    P['cover']['alternatives'] the covers of rounds 2 and 3 come back as options beside them (a cloth grille, the
    slotted grilles, a cork face; the disc and the bark face then options too), each in the recess in front of the panel
    (y 0 to 12), 1.5 clear of the shell."""
    W, H, T = P['W'], P['H'], P['T']
    cv, r, pt = P['cover'], P['ring'], P['port']
    cx, yb = W / 2, P['inset']
    x0, x1, z0, z1 = T + cv['gap'], W - T - cv['gap'], T + cv['gap'], H - T - cv['gap']
    alt = cv['alternatives']
    out = []
    if alt:
        out += alternative_covers(P, x0, x1, z0, z1)
    out += disc_and_face(P, wz, port_o, alt)
    return out


def alternative_covers(P, x0, x1, z0, z1):
    """The covers of rounds 2 and 3 the owner did not pick, as options: a cloth grille and the slotted grilles."""
    cv = P['cover']
    out = []
    # the cloth grille: a 6 mm MDF frame (a border and a bar between the ring and the port) under acoustically
    # transparent cloth, stretched over its face and round its edges and glued behind; its face 1 back from the
    # shell's front; four pegs behind its corners
    yf = cv['cloth_face'] + 0.5
    fw, ft = cv['frame_w'], cv['frame_t']
    frame = box(x0 + 0.5, yf, z0 + 0.5, x1 - 0.5, yf + ft, z1 - 0.5) - box(x0 + fw, yf - 1, z0 + fw, x1 - fw, yf + ft + 1, z1 - fw)
    frame += box(x0 + fw - 1, yf, cv['bar_z'] - cv['bar_w'] / 2, x1 - fw + 1, yf + ft, cv['bar_z'] + cv['bar_w'] / 2)
    out.append(Part('cloth-frame', frame, Sheet('mdf', ft), finish='black', option='cloth', render=False,
                    notes=['sprayed black so it cannot show through the cloth; its face edges rounded so they cannot cut it; a peg '
                           'glued into each corner (25 in from its edges) meets a cup in the panel']))
    cloth = box(x0, cv['cloth_face'], z0, x1, yf + ft + 0.5, z1)
    out.append(Part('grille-cloth', cloth, Bought('grille-cloth'), finish='cloth', option='cloth',
                    notes=['stretched over the frame\'s face and round its edges, stapled or glued behind; the weave square to the frame']))
    out.append(Part('grille-pegs', None, Bought('grille-pegs'), option='cloth',
                    notes=['the cups in four 10 mm holes 12 deep in the panel\'s corners, 25 in from the recess\'s edges']))

    # the slotted grilles: 6 mm plywood, flush with the shell's front, on pegs as the cloth grille; the woofer plays
    # below 800 Hz only, so an open area about a quarter of the face costs it nothing audible (the air behind the grille
    # resonates in its slots near 1.9 kHz, over an octave above the crossover)
    t, b, sw = cv['grille_t'], cv['border'], cv['slot_w']
    for name, opt, fn, stock, fin in (('lenticel', 'lenticel-grille', lenticels, 'baltic-birch', 'grille-paint'),
                                      ('strips', 'strip-grille', strips, 'spotted-gum-ply', 'grille-timber')):
        g = cv[name]
        cuts = fn(x0 + b, z0 + b, x1 - b, z1 - b, sw, g['pitch'], g['length'], g['gap'], g['seed'])
        panel = slotted_panel(x0, z0, x1, z1, 0.0, t, cuts)
        open_pc = 100 * sum((L - sw) * sw + math.pi * sw * sw / 4 for _, _, L, _, _ in cuts) / ((x1 - x0) * (z1 - z0))
        out.append(Part(f'grille-{name}', panel, Sheet(stock, t, face='-y'), finish=fin, option=opt,
                        notes=[f'{len(cuts)} slots {sw:g} wide, round-ended (a {sw:g} mm bit), {open_pc:.0f} % open; '
                               + ('sprayed in the panel\'s colour' if name == 'lenticel' else 'oiled')
                               + '; pegs in its corners as the cloth grille\'s']))
        out.append(Part(f'grille-{name}-pegs', None, Bought('grille-pegs'), option=opt))
    return out


def disc_and_face(P, wz, port_o, alt):
    """The front as picked: a cloth disc over the woofer on its ring, and the panel faced in bark round the ring and the
    port (with the alternatives, both options, and a cork face as a third)."""
    W, H, T = P['W'], P['H'], P['T']
    cv, r, pt = P['cover'], P['ring'], P['port']
    cx, yb = W / 2, P['inset']
    disc_opt = 'cloth-disc' if alt else ''
    out = []
    # the cloth disc: the woofer alone covered, a solid colour circle on the panel (or on its bark face): a 12 mm MDF ring
    # frame on the woofer's ring, in front of it, the cloth across its face and round its edge; magnets hold it
    dt = cv['disc_t']
    yr = yb - r['t']                                  # the ring's front
    dframe = cyl('y', (cx, wz), r['od'], yr - dt, yr) - cyl('y', (cx, wz), r['id'], yr - dt - 1, yr + 1)
    mg = cv['disc_magnet']
    for mx, mz in disc_magnets(P, cx, wz):
        dframe -= cyl('y', (mx, mz), mg['d'] + 0.2, yr - mg['t'] - 0.2, yr + 1)
    out.append(Part('disc-frame', dframe, Sheet('mdf', dt), finish='black', option=disc_opt, render=False,
                    notes=[f'sprayed black; its face edge rounded; {mg["n"]} magnets ({mg["d"]:g} x {mg["t"]:g}) bonded in the pockets '
                           f'behind it, each attracting its partner in a pocket behind the ring through {r["t"] - mg["t"] - 0.2:g} of MDF']))
    out.append(Part('cloth-disc', cyl('y', (cx, wz), r['od'] + 1.0, yr - dt - 0.5, yr), Bought('grille-cloth'), finish='disc',
                    option=disc_opt, notes=[f'Ø{r["od"] + 1:g}: stretched across the frame\'s face and round its edge, glued behind; '
                                                f'its face {yr - dt - 0.5:g} back from the shell\'s front']))
    out.append(Part('cloth-disc-magnets', None, Bought('grille-magnets'), option=disc_opt))

    # the facings: bark (1 mm; or cork, 3 mm, with the alternatives) laid on the panel round the ring and the port
    # before the ring goes on
    holes = [('circle', cx, wz, r['od'] + 1.0), ('rect', pt['x'], pt['z'], port_o + 0.4, port_o + 0.4)]
    if P['finish'] == 'pressed':
        faces = [('pressed', Sheet(P['skin']['stock'], P['skin']['face_t'], face='-y', grain='z'), 'bark')]
    else:
        faces = [('bark', Bought('bark-sheet'), 'bark')] + ([('cork', Sheet('cork', cv['face_t']['cork'], face='-y'), 'cork')] if alt else [])
    for name, make, fin in faces:
        ft = P['skin']['face_t'] if name == 'pressed' else cv['face_t'][name]
        face = slotted_panel(T + 0.5, T + 0.5, W - T - 0.5, H - T - 0.5, yb - ft, yb, holes=holes)
        out.append(Part(f'{name}-face', face, make, finish=fin, option=f'{name}-face' if alt else '',
                        notes=[f'{ft:g} thick, cut round the ring (Ø{r["od"] + 1:g}) and the port; laminated to the panel before the ring goes on']))
    return out


# each waveguide from its bark, cast in translucent resin (round 4: as the photograph's, milky where thin, deepening
# where thick or seen edge-on): birch's milk with a honey depth, faintly clouded, on a pale panel and an off-white ring
# as photographed; eucalyptus's cream clouded with amber (the photograph's own, which takes up the gum's ochre), on a
# sage-grey panel and a cream ring. The discs: charcoal on birch, rust on eucalyptus (the owner's pick of round 3's
# recommendations)
VARIANTS = dict(
    birch={'bark': 'birch_bark', 'panel': '#D8D5CD', 'ring': '#EEEAE2', 'horn': '#F2EEE6', 'horn_deep': '#D9AE6E',
           'horn_cloud': 0.3, 'horn_preset': 'cast_resin', 'cloth': '#DCD6C8', 'cork': '#3B2F28', 'disc': '#2E2C2A'},
    eucalyptus={'bark': 'eucalyptus_bark', 'panel': '#CBCFC4', 'ring': '#E8E2D4', 'horn': '#EFE5D0', 'horn_deep': '#D6A04E',
                'horn_cloud': 0.6, 'horn_preset': 'cast_resin', 'cloth': '#6F7F66', 'cork': '#3B2F28', 'disc': '#9A4526'})
# the material experiments of 2026-10-11 (frames.py experiments): the shell in pressed recycled plastic, the waveguide
# in resin poured in layers (strata) or with recycled plastic chips cast through it (terrazzo), in round 3's colours
VARIANTS.update({
    'eucalyptus-pressed': {**VARIANTS['eucalyptus'], 'bark': 'pressed_eucalyptus_sheet'},     # round 4's sheets
    'birch-pressed': {**VARIANTS['birch'], 'bark': 'pressed_birch_sheet'},
    'eucalyptus-strata': {**VARIANTS['eucalyptus'], 'horn_preset': 'frosted_strata', 'horn': '#DEE6D4', 'horn_deep': '#B9C9A9'},
    'birch-terrazzo': {**VARIANTS['birch'], 'horn_preset': 'frosted_terrazzo', 'horn': '#F5F2EC', 'horn_deep': '#EFE5D3'},
})


PRODUCT = Product(
    'barkhorn', 'barkhorn', 'Two-way horn loudspeaker after Friendly Pressure, in birch bark or eucalyptus bark', params=P, parts=parts,
    notes=['Bark on the shell (sides, top, bottom and back): real birch bark sheet (Betula papyrifera, from fallen or felled trees) laminated to the plywood with PVA in a vacuum bag and sealed with a matt waterborne lacquer, wrapped round the shell\'s front edges; for eucalyptus, the shed bark of a smooth-barked gum (spotted or snow gum) pressed flat and laminated the same way, or a UV-printed veneer of it. Approve a sample board first.',
           'Glue-up: sides to the bottom, the brace, then the front panel (set back 24 mm), the back, then the top.',
           'The woofer flush in its rebate on a gasket, eight M6 T-nuts from inside, the ring over its frame; the port pushed in dry, trimmed to tune (impedance minimum at fb), then bonded.',
           'The waveguide stands on four posts, stainless lamp tube 10 x 7 threaded M10 x 1 at both ends, screwed into brass inserts bonded in pads cast under it and into inserts in the top; the HF cable runs down inside a rear post.',
           'The front: the panel faced in bark (1 mm) round the ring and the port, and a cloth disc over the woofer, its MDF frame standing on the ring on four magnet pairs, its face 18.5 clear of the cone at rest.',
           'The FA122 crosses at about 800 Hz (LR4) with the HF channel about 14 dB down, part of it in the passive L-pad after the amplifier, so its hiss stays inaudible through a 113 dB driver.',
           'Hypex advises a sealed box round the amplifier module (left out here, as in the kit\'s example).'],
    touching=[('grille-cloth', 'cloth-frame'), ('cloth-disc', 'disc-frame')],     # the cloth wraps its frame
    materials={'bark': {'preset': '$bark'}, 'raw': {'preset': 'birch'},
               'cloth': {'preset': 'cloth', 'color': '$cloth'}, 'disc': {'preset': 'cloth', 'color': '$disc'},
               'grille-paint': {'preset': 'satin_paint', 'color': '$panel', 'roughness': 0.6, 'specular': 0.3},
               'grille-timber': {'preset': 'birch', 'color': '#8E6E4E', 'roughness': 0.55},
               'cork': {'preset': 'cork', 'color': '$cork'},
               'panel': {'preset': 'satin_paint', 'color': '$panel', 'roughness': 0.6, 'specular': 0.3},
               'ring': {'preset': 'satin_paint', 'color': '$ring', 'roughness': 0.45, 'specular': 0.4},
               'horn': {'preset': '$horn_preset', 'color': '$horn', 'absorb': '$horn_deep', 'deep': '$horn_deep', 'cloud': '$horn_cloud',
                        'cloud_m': 0.12},
               'rod': {'preset': 'metal', 'color': '#C9C9C6', 'roughness': 0.3},
               'port': {'preset': 'satin_paint', 'color': '#1A1817', 'roughness': 0.7},
               'amp': {'preset': 'satin_paint', 'color': '#303033', 'roughness': 0.4, 'specular': 0.5},   # black anodised plate
               'driver-frame': {'preset': 'satin_paint', 'color': '#1E1E1E'}, 'driver-cone': {'preset': 'paper_cone', 'color': '#1D1B1A'},
               'driver-surround': {'preset': 'rubber', 'color': '#151515'}, 'driver-cap': {'preset': 'paper_cone', 'color': '#1D1B1A'},
               'driver-motor': {'preset': 'metal', 'color': '#3A3A3A'}, 'driver-magnet': {'preset': 'satin_paint', 'color': '#2B2B2B'},
               'driver-coil': {'preset': 'metal', 'color': '#B87333'}, 'driver-spider': {'preset': 'rubber', 'color': '#C8B88A'},
               'driver-plug': {'preset': 'satin_paint', 'color': '#111111'}},
    variants=VARIANTS,
)


if __name__ == '__main__':
    from speaker.box import vented, suggest_vented
    ts = LIB[P['woofer']]['ts']
    net = net_volume(P)
    pl = port_length(P, net)
    net = net_volume(P, pl)
    pl = port_length(P, net)
    print(f"QB3 start: {suggest_vented(ts)} (L, Hz)")
    print(f"net {net:.1f} L, a {P['port']['a']:g} mm square port {pl:.0f} long for {P['fb']:g} Hz")
    for fb in (32.0, 35.0, 38.0):
        r = vented(ts, net, fb, bore_mm=2 * P['port']['a'] / math.sqrt(math.pi))
        print(fb, {k: r[k] for k in ('f3', 'ref_db', 'max_spl_db', 'port_air_m_s_at_max')})
