"""barkhorn (a working name): a two-way horn loudspeaker after the owner's reference photograph of Friendly Pressure's
speakers (reference/friendly-pressure-owner-2026-10-10.jpg), in two finishes: birch bark and eucalyptus bark, each
with its waveguide cast in a translucent resin tinted from its bark.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/product.py
    .venv-fab/bin/python spinoffs/barkhorn/product.py            # the bass box's numbers

What the photograph shows, and how it is read here:
- a bass cabinet about 1 : 1.6 (wide to tall), a thin wooden shell (walnut there; bark here) framing a pale front
  panel set back in it;
- a 15 in black paper cone in a wide off-white ring, its centre a little above the cabinet's middle;
- a small square port at the bottom right (round 14, the owner: a round tube behind a square frame);
- a frosted, translucent waveguide on top: a rounded rectangle about 1.72 : 1 (measured again in round 4; round 1
  read 2.1 : 1), wider than the cabinet (about 1.12 times), its rim thin, the driver's dark throat near its centre,
  on four slim posts (a wide pair in front, a narrow pair behind), its rim just above the cabinet.
Sizes are scaled from the photograph by its turntable (about 450 wide): the cabinet about 560 x 880; the waveguide
from the cabinet: about 630 x 366, its rim about 37 above the top.

Parts from the horn-speaker research of 2026-10-10 and 2026-10-12 (components.json): FaitalPRO 15PR400-8 woofer (treated
paper cone), B&C DE1085TN-16 compression driver (2 in exit, 100 mm titanium diaphragm, crossed at 800 Hz or above; round
5, for the owner's bigger throat, in place of round 4's 1 in BMS 4550), a Hypex FusionAmp FA122.
"""
import math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.normpath(os.path.join(HERE, '..', '..', 'studio', 'fabkit', 'fonts'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'studio', 'fabkit'))
from kit import *                                                    # noqa: E402,F403
from speaker.drivers import driver_part, place                      # noqa: E402
from speaker.horn import waveguide_shell, waveguide_lens, waveguide_slab, round_horn, tractrix, twist_lock   # noqa: E402

import json  # noqa: E402
LIB = json.load(open(os.path.join(HERE, '..', '..', 'studio', 'fabkit', 'library', 'components.json')))
LIB.update(json.load(open(os.path.join(HERE, 'components.json'))))

P = dict(
    W=560.0, D=420.0, H=880.0, T=18.0,           # the cabinet's shell, outside; it stands on levelling feet (below)
    stock='baltic-birch',                        # the shell's sheet (pressed.py: recycled HDPE, no wood at all)
    # the shell's finish: 'bark' (bark sheet laminated to the plywood); 'pressed' (round 5, pressed.py: no wood, the
    # shell's own panels pressed recycled HDPE, laid out in the bark's pattern, welded); or 'faced' (round 4: the
    # plywood faced in pressed recycled HDPE sheet, `skin` thick, screwed from inside through oversized holes so it can
    # move with the seasons, `gap` between sheets at the corners; the panel faced in `face_t` sheet)
    finish='bark', skin=dict(t=8.0, face_t=5.0, gap=1.5, hole=14.0, stock='recycled-hdpe'),
    inset=24.0,                                  # the front panel set back in the shell (the photograph's frame): deep
                                                 # enough for a cover to clear the cone at twice its Xmax
    woofer='faital-15pr400-8', woofer_z=478.0,   # its centre 45.7 % down from the top, as photographed
    gasket=1.0,
    woofer_hole=8.0,                             # its eight fixing holes: M6 T-nuts in plywood (pressed.py: 9.0, for inserts for
                                                 # plastics, as their maker's chart for PE gives; round 13, the reality check's r3)
    ring=dict(od=436.0, id=350.0, t=6.0, stock='mdf'),   # the off-white ring over the frame, 6 mm, standing on the panel
    # the ports, one in each bottom corner, as the reference speaker has them (the owner, 2026-10-12: one is cut off in the
    # photograph; round 1 to 5 had the bottom right one only), tuned together. Round 14, the owner: "It's not meant to be
    # a square opening. It's meant to be cylindrical with square framing around the end": a tube `d` across inside (the
    # area of round 6's 100 square), `wall` thick, its front end a square `frame` (corners `frame_r`) `frame_t` thick,
    # printed in one; fitted from the front into a recess in the panel, flush with its face, on a `seal` of foam, four
    # black countersunk screws (`screw`: the hole, the countersink) in the frame's corners. Its centre on the corner's
    # diagonal, 105 in from the side and the bottom, as photographed. `flare`: both mouths rounded on it (0: plain; round
    # 15, the owner's pick: rounded, so the air turns the corner without chuffing). `stock`: None, printed in black ASA;
    # or a sheet stock (cloud.py: the Cloud's own cast acrylic), the tube flared over a mandrel and cemented into a frame
    # cut from `frame_t` sheet
    port=dict(d=113.0, wall=4.0, x=(105.0, 455.0), z=105.0, frame=140.0, frame_r=10.0, frame_t=5.0, seal=1.0, flare=8.0,
              screw=(4.5, 9.0), stock=None),
    # round 15: a pad cut from the shell's own sheet, welded (glued and screwed in plywood) under the top between the
    # rear posts, where the top is too thin under their sockets for the tie rod's insert and the HF lead's gland (the
    # 20 mm sheet, the plywood): `d` front to back, `margin` beyond the posts each way
    top_boss=dict(d=28.0, margin=14.0),
    # the back (round 14, the owner's pick; the reality check's r4): it comes off, the way in to the amplifier, the L-pad
    # and the leads. It closes on a `gasket` against four `land` strips (`land` wide, the shell's thickness deep) fixed
    # inside the shell, `clear` from the shell all round; sixteen M5 button heads (`screw_hole`) through it into inserts
    # (`insert`: the hole across, deep) in the strips, `edge` in from its edges. The amplifier's compartment, the back's
    # ribs and its batts come off with it
    back=dict(land=25.0, gasket=3.0, clear=1.0, edge=12.5, per_side=6, per_end=4, screw_hole=5.5, insert=(8.0, 12.0)),
    # the feet (round 14, the owner's pick; r11): four levelling feet, M8 into inserts in the bottom (`insert`: the hole
    # across, deep), `inset` in from its edges, `lift` under it (a shadow gap): a 1.29 m speaker with 10 kg at its top
    # stands level and cannot rock
    feet=dict(inset=50.0, lift=12.0, d=40.0, base=6.0, insert=(12.5, 15.0)),
    fb=38.0,
    braces=[dict(z=200.0, window=(420.0, 300.0))],   # level braces across the shell, each a frame round its window
    ribs=None,                                   # ribs welded on edge inside the panels (pressed.py: the HDPE shell needs them)
    # the lining (round 13): batts of acoustic-grade polyester (about 30 kg/m3: the light batts sold for walls absorb
    # less in the midrange), recycled PET thermally bonded, `t` thick against the sides, the back,
    # the top and the bottom, a batt to each bay between the ribs and braces, each in a sewn sleeve of white voile. None
    # on the front panel; none beside a port (`port_clear` round its tube; the jet from its inner end left clear to the
    # back's batt); none round the amplifier's module (`amp_clear`); a strip left narrower than `min_strip` beside a
    # keep-out goes with it. `gap`: the air between a batt and any face, so no two faces coincide. `t_top` and
    # `t_bottom` (round 21, the owner: "100 mm now"): the top's and the bottom's batts doubled, as lining.py found those
    # faces the least lined and the modes between them, top to bottom, the least damped
    lining=dict(t=50.0, t_top=100.0, t_bottom=100.0, gap=0.5, port_clear=10.0, amp_clear=20.0, min_strip=40.0,
                stock='polyester-batting', soft=9.0),    # soft: the render's batts' edges rounded, as a sleeved batt's are
    amp='hypex-fa122', amp_z=520.0,
    # the amplifier's sealed compartment (round 13, the reality check's r2: Hypex asks for one, and the box must stay
    # airtight): 1.5 mm aluminium folded and welded, black anodised, `inside` (across, deep, high) round the module, its
    # `flange` screwed to the back's inner face on a `gasket` of EPDM; the L-pad and the driver's capacitor inside it, the
    # leads out through two cable glands (`gland`: across, long) in its front
    amp_box=dict(t=1.5, inside=(125.0, 75.0, 320.0), flange=15.0, gasket=3.0, gland=(19.0, 22.0)),
    hf='bc-de1085tn-16',
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
              # round 5 (the owner's third notes, 2026-10-12): the back flush with the cabinet's (the flare 278 deep, the pod
              # 130 and its cap 12 behind it: 420 in all), and a 2 in throat for the B&C DE1085TN. The driver's M6 holes are
              # blind threads in its front plate, so it screws to an aluminium adaptor ring from the front first, and the ring
              # to brass inserts in the boss on a circle outside the driver (a ball-end key reaches them past it with the cap
              # off), so the pod is 200 across
              cast=dict(mouth_w=610.0, mouth_h=346.0, d=278.0, r0=25.4, wall=6.0, rim=10.0, round_rim=4.0, n_mouth=7.0,
                        pod_r=100.0, pod_back=130.0, dome=12.0, gap=37.0, solid_neck=True,
                        boss=dict(d=184.0, t=14.0, bolt_d=170.0, bolts=4, bolt_hole=7.0),   # 2 clear inside the pod
                        adaptor=dict(t=10.0, od=184.0, driver_holes=6.6, sink=12.5, screw_hole=5.5),
                        posts=dict(front=(183.0, 35.0), back=(40.0, 75.0), d=10.0, bore=7.0, pad_d=26.0, pad_h=6.0,
                                   insert_d=13.0, insert_depth=14.0, front_insert_depth=10.0, socket=(14.7, 15.0),
                                   socket_bore=12.0, sleeve=(12.0, 10.0, 13.0), cable_post=2, tie_post=3,
                                   tie=dict(d=6.0, hole=6.5, insert=(9.0, 10.0, 14.0, 1.5))),
                                   # socket: the brass cup in the top each post's plain foot stands in, knurled to 15 and
                                   # pressed into a 14.7 hole 15 deep (round 13, r3: nothing bonded to HDPE), bored 12 for a
                                   # polyurethane sleeve 12 x 10 x 13 (Shore A 90) that centres the post and stops it
                                   # buzzing (r1). The cable post's floor is holed for the HF lead, an M12 gland under the
                                   # top round it (r2); the tie post's for an M6 rod from inside the pod down to a flanged
                                   # insert (body 9 x 10, flange 14 x 1.5) under the top, which holds the horn down (r1).
                                   # The front pads' inserts 10 deep: a 14 leaves only 3 to 8 of resin under the flare
                        # its back: 'shell' (the photograph's: the shell follows the flare to a round pod round the driver)
                        # or 'tub' (the outside runs straight back from the rim to a flat back that hides the driver, the
                        # flare its own skin inside; the back pair of posts wider, under its flat bottom)
                        back='shell',
                        # round 16, the owner's pick ("Twist-lock"): the cap held by a twist-lock, three lugs on its
                        # spigot in L-slots in the pod's bore, an O-ring beyond them, two finger dimples to turn it by
                        # (speaker.horn.twist_lock); no screw shows
                        lock=dict(lugs=3, turn=45.0),
                        tub=dict(back=142.0, taper=0.08, round=0.25, end=0.6, lid=30.0, seam=0.4, posts_back=(120.0, 20.0))),
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
               disc_t=12.0, disc_stock='mdf',  # the cloth disc's frame, over the woofer alone, in front of the ring
               disc_edge_r=5.0,                # the frame's face edge rounded, and the cloth taken round it
               disc_magnet=dict(d=15.0, t=3.0, n=4, r=207.5, pocket=15.2)),
               # its magnets, on a circle between the woofer's rebate and the ring's edge (round 13, r7: four steel discs in
               # the ring's back over four magnets in the panel hold the ring; the disc's magnets hold to the same discs
               # through the ring, more weakly, so the disc comes away alone); `pocket`: bonded in MDF (pressed.py: 14.85,
               # a press fit, since HDPE holds no bond)
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


def shell_kind(P):
    """What the shell is made of, for its notes and fixings: 'wood' (plywood, bark-faced or faced), 'hdpe' (pressed.py:
    welded, nothing bonds to it) or 'acrylic' (cloud.py: cemented, bonds well, brittle, so nothing is pressed into it)."""
    if P['finish'] != 'pressed':
        return 'wood'
    return 'acrylic' if 'acrylic' in P['stock'] else 'hdpe'


def port_length(P, net_l):
    """The round ports' length tuning `net_l` litres to fb, the ports in parallel (one end flanged, one free)."""
    c, d = 343.0, P['port']['d'] / 1000
    sp = len(P['port']['x']) * math.pi * d * d / 4
    w = 2 * math.pi * P['fb']
    return (sp * c * c / (w * w * net_l * 1e-3) - 0.732 * d) * 1000


def port_reach(P):
    """A port's greatest radius behind the panel: its tube, or its flared inner mouth."""
    pt = P['port']
    return max(pt['d'] / 2 + pt['wall'], pt['d'] / 2 + pt['flare'])


def port_screw_len(P):
    """The ports' screws' length and their holes' depth below the recess's floor (round 15): the longest stock length
    whose hole stops 2 short of the panel's back face (round 14's 15 deep ran through the 20 mm sheet and the plywood)."""
    pt, T = P['port'], P['T']
    head = pt['frame_t'] + pt['seal']
    for L in (25.0, 20.0, 16.0, 14.0, 12.0, 10.0):
        if L - head + 1.0 <= min(15.0, T - head - 2.0):
            return L, L - head + 1.0
    raise ValueError(f'the front panel ({T:g}) is too thin for the ports\' screws')


def top_boss(P):
    """Round 15: the pad under the top between the rear posts, (x0, y0, x1, y1, z0, z1), where the top is too thin
    under their sockets for the tie rod's insert (the 20 mm sheet, the plywood); None where it needs none (the
    Cloud's 25 mm acrylic) or the horn has no posts."""
    hz = P['horn']
    if hz['form'] != 'cast':
        return None
    pp = hz['cast']['posts']
    H, T, b = P['H'], P['T'], P['top_boss']
    if T - pp['socket'][1] >= pp['tie']['insert'][1]:
        return None
    places = rod_places(P)
    (gx, gy), (tx, ty) = places[pp['cable_post']], places[pp['tie_post']]
    yc = (gy + ty) / 2
    return (min(gx, tx) - b['margin'], yc - b['d'] / 2, max(gx, tx) + b['margin'], yc + b['d'] / 2, H - 2 * T, H - T)


def back_edge(P):
    """Where the braces end at the back (round 14): short of the back's ribs and its batts, which come off with it.
    The top's and the bottom's ribs, clear of the back's ribs, end at the batts' face."""
    T, D, L = P['T'], P['D'], P['lining']
    ye = D - T - L['t'] - 2 * L['gap']                      # the back's batts' face, less a gap
    return min(ye, D - T - P['ribs']['depth'] - 1.0) if P['ribs'] else ye, ye


def brace_window(P, b):
    """A brace's window, front to back (y0, y1): its front edge as before, its back edge leaving a member as wide as
    the front one, so each brace is still a closed frame round its window (round 14: the braces end short of the back)."""
    yb, T, D = P['inset'], P['T'], P['D']
    ym = (yb + T + D - T) / 2
    y0 = ym - b['window'][1] / 2
    return y0, min(ym + b['window'][1] / 2, back_edge(P)[0] - (y0 - (yb + T)))


def back_screws(P):
    """The back's sixteen screws' centres (x, z): `per_side` up each side, `per_end` along the top and the bottom (the
    corners shared), on the land strips' centre lines."""
    W, H, T, bk = P['W'], P['H'], P['T'], P['back']
    e = T + bk['land'] / 2
    zs = [e + (H - 2 * e) * k / (bk['per_side'] - 1) for k in range(bk['per_side'])]
    xs = [e + (W - 2 * e) * k / (bk['per_end'] - 1) for k in range(bk['per_end'])]
    return [(x, z) for x in (e, W - e) for z in zs] + [(x, z) for x in xs[1:-1] for z in (e, H - e)]


def tuned(P):
    """The ports' length and the net volume they leave, each found from the other (a long port takes room)."""
    net = net_volume(P)
    for _ in range(3):
        pl = port_length(P, net)
        net = net_volume(P, pl)
    return round(port_length(P, net), 1), net


def rib_spans(P):
    """The heights (z0, z1) between the bottom, the braces and the top where a side's span is long enough to want a
    rib (P['ribs']['min_span']): below the lowest brace and above the highest, the spans are short and already stiff.
    (The back's ribs run its full height, round 14: it comes off, and the braces stop short of it.)"""
    T, H = P['T'], P['H']
    zs = [T] + [z for b in P['braces'] for z in (b['z'], b['z'] + T)] + [H - T]
    return [(zs[i], zs[i + 1]) for i in range(0, len(zs), 2) if zs[i + 1] - zs[i] > P['ribs'].get('min_span', 0.0)]


def lining(P, plen, ribs):
    """The lining's batts, (name, solid) each. The sides', the top's and the bottom's sit in the zones between the
    bottom, the braces and the top: the sides' run from the front panel to the back's land strips, the top's and the
    bottom's between them, up to the back's ribs (or its batts). The back's (round 14) run its full height between its
    land strips, on the back between its ribs, so they come off with it. A zone holding a port has none on its sides
    (the ports stand 20 from them). Every batt keeps clear of each port's tube, of the jet from its inner end (up to the
    back's batts), of the amplifier's compartment, and (the cast horn) of the HF lead's gland and the tie rod's insert
    under the top. The ribs cut a wall's batt into one a bay; a batt is named for its wall, its zone (1 the lowest; the
    back's have none) and, where the ribs or a keep-out cut it, its piece (a, b, ... front to back, left to right, bottom
    to top)."""
    W, D, H, T = P['W'], P['D'], P['H'], P['T']
    L = P['lining']; t, g, ms = L['t'], L['gap'], L['min_strip']
    t_top, t_bot = L.get('t_top', t), L.get('t_bottom', t)  # the top's and the bottom's (round 21)
    bk = P['back']; lw = bk['land']
    x0, x1, y0, y1 = T, W - T, P['inset'] + T, D - T        # the inside faces: the sides, the front panel's back, the back
    yback = y1 - g - t                                       # the back's batts' face
    yland = y1 - bk['gasket'] - T                            # the back's land strips' front face
    ytb = (min(yback, y1 - P['ribs']['depth']) if P['ribs'] else yback) - g    # where the top's and the bottom's end
    zs = [T] + [z for b in P['braces'] for z in (b['z'], b['z'] + T)] + [H - T]
    zones = [(zs[i], zs[i + 1]) for i in range(0, len(zs), 2)]
    pt = P['port']
    pw = port_reach(P) + L['port_clear']                     # half a port's keep-out
    az, cx = P['amp_z'], W / 2
    ab = P['amp_box']; (iw, idp, ih), ac = ab['inside'], L['amp_clear']
    aw, ah = iw / 2 + ab['t'] + ab['flange'] + ac, ih / 2 + ab['t'] + ab['flange'] + ac   # the compartment, with room
    under_top = []                                            # (x0, x1, z0, z1, y0, y1) cut out of the batts under the top
    if P['horn']['form'] == 'cast':
        pp = P['horn']['cast']['posts']; places = rod_places(P)
        (gx, gy), (tx, ty) = places[pp['cable_post']], places[pp['tie_post']]
        under_top += [(gx - 20, gx + 20, H - T - max(60, t_top + 10), H - T + 1, gy - 12, y1 + 1),   # the HF lead's gland and its way in
                      (tx - 10, tx + 10, H - T - t_top - g - 2, H - T + 1, min(ty - 9, yback - g), y1 + 1)]   # the tie rod's anchor
        tb = top_boss(P)
        if tb:                                                # round 15: the pad under the top
            under_top.append((tb[0] - g, tb[2] + g, tb[4] - g, H - T + 1, tb[1] - g, tb[3] + g))
    if 'grips' in (P.get('lift') or []):                      # round 21's recessed grips: the side batts cut round the cups
        (gy0, gy1, gz0, gz1), dep = grip_boxes(P)
        for xa, xb in ((-1.0, T + dep + 3.0 + g), (W - T - dep - 3.0 - g, W + 1.0)):
            under_top.append((xa, xb, gz0 - 3.0 - g, gz1 + 3.0 + g, gy0 - 3.0 - g, gy1 + 3.0 + g))

    def keep_out(xa, xb, za, zb, ya, yb_, zone, stops):
        """A keep-out box, run on to a wall, a rib or a zone's end where it leaves a strip narrower than `min_strip`."""
        lo_ = [v for v in stops if v <= xa]; hi_ = [v for v in stops if v >= xb]
        xa = max(lo_) - 1 if lo_ and xa - max(lo_) < ms else xa; xb = min(hi_) + 1 if hi_ and min(hi_) - xb < ms else xb
        za = zone[0] - 1 if za - zone[0] < ms else za; zb = zone[1] + 1 if zone[1] - zb < ms else zb
        return box(xa, ya, za, xb, yb_, zb)

    grown = lambda r: box(*(v - g for v in r.bounding_box().min), *(v + g for v in r.bounding_box().max))
    mid = lambda b, i: getattr(b.bounding_box().center(), 'XYZ'[i])

    def named(wall, k, s, axes):
        bits = sorted(s.solids(), key=lambda b: tuple(round(mid(b, i)) for i in axes))
        return [(f'lining-{wall}' + (f'-{k}' if k else '') + (('' if k else '-') + chr(ord('a') + j) if len(bits) > 1 else ''), b)
                for j, b in enumerate(bits)]

    out = []
    for k, zone in enumerate(zones):
        za, zb = zone
        lo, hi = za + g, zb - g
        ports = [px for px in pt['x'] if za < pt['z'] < zb]
        sides = not ports
        xi0, xi1 = (x0 + 2 * g + t, x1 - 2 * g - t) if sides else (x0 + g, x1 - g)
        slabs = ([('left', box(x0 + g, y0 + g, lo, x0 + g + t, yland - g, hi)),
                  ('right', box(x1 - g - t, y0 + g, lo, x1 - g, yland - g, hi))] if sides else [])
        if k == len(zones) - 1:
            slabs.append(('top', box(xi0, y0 + g, hi - t_top, xi1, ytb, hi)))
        if k == 0:
            slabs.append(('bottom', box(xi0, y0 + g, lo, xi1, ytb, lo + t_bot)))
        cut = [grown(r) for _, r in ribs]
        stops = [x0, x1, xi0, xi1]
        for px in ports:
            cut.append(keep_out(px - pw, px + pw, pt['z'] - pw, pt['z'] + pw, -1.0, yback - g, zone, stops))
        for ux0, ux1, uz0, uz1, uy0, uy1 in under_top:
            if uz0 < zb and uz1 > za:
                cut.append(box(ux0, uy0, uz0, ux1, uy1, uz1))
        for wall, s in slabs:
            for r in cut:
                s = s - r
            out += named(wall, k + 1, s, (1, 0) if wall in ('left', 'right') else (0, 1))
    # the back's: its full height between its land strips, inside the sides' batts, cut by its ribs, round the
    # amplifier's compartment and under the top
    zone = (T + lw, H - T - lw)
    xb0, xb1 = x0 + 2 * g + t, x1 - 2 * g - t
    s = box(xb0, yback, zone[0] + g, xb1, y1 - g, zone[1] - g)
    backs = [r for n, r in ribs if n.startswith('rib-back')]
    stops = [xb0, xb1] + [v for r in backs for v in (r.bounding_box().min.X - g, r.bounding_box().max.X + g)]
    cut = [grown(r) for r in backs] + [keep_out(cx - aw, cx + aw, az - ah, az + ah, yback - 1, D + 1, zone, stops)]
    cut += [box(ux0, uy0, uz0, ux1, uy1, uz1) for ux0, ux1, uz0, uz1, uy0, uy1 in under_top]
    for r in cut:
        s = s - r
    out += named('back', 0, s, (0, 2))
    return out


def batt_t(P, name):
    """A batt's thickness, by its name: the top's and the bottom's their own (round 21), the others `t`."""
    L = P['lining']
    return (L.get('t_top', L['t']) if name.startswith('lining-top') else
            L.get('t_bottom', L['t']) if name.startswith('lining-bottom') else L['t'])


def soft(s, r):
    """A batt as the render shows it: its edges rounded on `r`, as a batt sewn into a sleeve and pressed into a bay is
    (the cut files and the checks keep the square prism it is cut as)."""
    for rr in (r, r * 0.6, r * 0.35):
        try:
            return s.fillet(rr, s.edges())
        except Exception:
            continue
    return s


def net_volume(P, port_l=60.0):
    W, D, H, T = P['W'], P['D'], P['H'], P['T']
    yb = P['inset']
    inner = (W - 2 * T) * (D - T - (yb + T)) * (H - 2 * T) / 1e6
    pt = P['port']
    port = len(pt['x']) * math.pi * (pt['d'] / 2 + pt['wall']) ** 2 * port_l / 1e6
    ye, ytr = back_edge(P)
    brace = sum(((W - 2 * T) * (ye - yb - T) - b['window'][0] * (lambda w: w[1] - w[0])(brace_window(P, b))) * T / 1e6
                for b in P['braces'])
    rb = P.get('ribs')
    ribs = (2 * len(rb.get('side') or (0,)) * sum(z1 - z0 for z0, z1 in rib_spans(P))
            + len(rb['back']) * (H - 2 * T - 2 * P['back']['land'] - 1.0)
            + 2 * len(rb.get('top') or (0,)) * (ytr - yb - T)) * rb['t'] * rb['depth'] / 1e6 if rb else 0.0
    bk = P['back']; lw = bk['land']
    land = (2 * (H - 2 * T) + 2 * (W - 2 * T - 2 * lw)) * lw * (T + bk['gasket']) / 1e6     # the strips and the gasket on them
    ab = P['amp_box']; (iw, idp, ih) = ab['inside']
    amp = (iw + 2 * ab['t'] + 2 * ab['flange']) * (ih + 2 * ab['t'] + 2 * ab['flange']) * (ab['gasket'] + ab['t']) / 1e6 + \
        (iw + 2 * ab['t']) * (ih + 2 * ab['t']) * (idp + ab['t'] - ab['gasket']) / 1e6
    tb = top_boss(P)
    pad = (tb[2] - tb[0]) * (tb[3] - tb[1]) * (tb[5] - tb[4]) / 1e6 if tb else 0.0
    return inner - 4.5 - amp - port - brace - ribs - land - pad   # woofer (estimated), compartment, ports, braces, ribs, lands, pad


def parts(P):
    W, D, H, T = P['W'], P['D'], P['H'], P['T']
    cx = W / 2
    yb = P['inset']                                   # the front panel's face
    wf = LIB[P['woofer']]['geom']; amp = LIB[P['amp']]['geom']; hf = LIB[P['hf']]['geom']
    pt = P['port']
    plen, _ = tuned(P)
    ply = lambda grain, face=None: Sheet(P['stock'], T, face=face, grain=grain)
    kind = shell_kind(P)
    wood = kind == 'wood'                             # pressed and cloud: no wood anywhere (pressed.py, cloud.py)

    # the front panel, set back in the shell: the woofer flush in its rebate, its T-nut holes, the square port
    baffle = box(T, yb, T, W - T, yb + T, H - T)
    wz = P['woofer_z']
    baffle -= cyl('y', (cx, wz), wf['frame_od'] + 1.6, yb - 1, yb + wf['flange_t'] + P['gasket'])
    baffle -= cyl('y', (cx, wz), wf['cutout'], yb - 1, yb + T + 1)
    for k in range(wf['bolts']):
        a = 2 * math.pi * (k + 0.5) / wf['bolts']
        baffle -= cyl('y', (cx + wf['bolt_d'] / 2 * math.cos(a), wz + wf['bolt_d'] / 2 * math.sin(a)), P['woofer_hole'], yb - 1, yb + T + 1)
    fr, ft, sl = pt['frame'], pt['frame_t'], pt['seal']
    _, sdep = port_screw_len(P)
    for px in pt['x']:                                # each port's frame in a recess, flush with the face; its tube through
        baffle -= prism(rounded_rect(fr + 0.5, fr + 0.5, pt['frame_r'] + 0.25, cx=px, cy=pt['z']), 'y', yb - 1, yb + ft + sl)
        baffle -= cyl('y', (px, pt['z']), 2 * port_reach(P) + 1.0, yb + ft + sl - 0.5, yb + T + 1)
        for sx, sz in port_screws(P, px):             # pilot holes (tapped M4 in acrylic), 2 short of the panel's back
            baffle -= cyl('y', (sx, sz), 3.3 if kind == 'acrylic' else 3.5, yb + ft + sl - 0.5, yb + ft + sl + sdep)
    mg = P['cover']['disc_magnet']
    for mx, mz in disc_magnets(P, cx, wz):            # round 13 (r7): the magnets that hold the ring, under its steel discs
        baffle -= cyl('y', (mx, mz), mg['pocket'], yb - 1, yb + mg['t'] + 0.2)

    # the back (round 14): it comes off, `clear` from the shell all round, on its gasket against the land strips inside
    # the shell, sixteen M5 button heads through it
    bk = P['back']
    back = box(T + bk['clear'], D - T, T + bk['clear'], W - T - bk['clear'], D, H - T - bk['clear'])
    for sx, sz in back_screws(P):
        back -= cyl('y', (sx, sz), bk['screw_hole'], D - T - 1, D + 1)
    az = P['amp_z']
    back -= box(cx - (amp['plate_w'] + 0.5) / 2, D - 4.5, az - (amp['plate_h'] + 0.5) / 2, cx + (amp['plate_w'] + 0.5) / 2, D + 1, az + (amp['plate_h'] + 0.5) / 2)
    back -= box(cx - amp['cutout_w'] / 2, D - T - 1, az - amp['cutout_h'] / 2, cx + amp['cutout_w'] / 2, D, az + amp['cutout_h'] / 2)

    # the top: the cast horn's four posts stand in brass sockets pressed into it (round 11, the owner: "go with the sockets
    # and the thin wire"; the front pair stand over the front panel's top edge, so nothing can hang below; the HF lead
    # comes down inside one of the rear pair and through a gland under its socket; round 13, the reality check's r1 and
    # r2: a rod down the other holds the horn down, into an insert under the top), or the study forms' rods stand in
    # inserts in it, the cable through a gland behind them
    top = box(T, 0, H - T, W - T, D, H)
    hz = P['horn']
    rods = rod_places(P)
    if hz['form'] == 'cast':
        pp = hz['cast']['posts']
        for i, (rx, ry) in enumerate(rods):
            top -= cyl('z', (rx, ry), pp['socket'][0], H - pp['socket'][1], H + 1)
            if i == pp['cable_post']:
                top -= cyl('z', (rx, ry), 10.5, H - T - 1, H)              # tapped M12 for the HF lead's gland below
            if i == pp['tie_post']:                  # the rod's insert (or, in plywood too thin for one, its hole to a nut below)
                ti = pp['tie']['insert']
                top -= cyl('z', (rx, ry), ti[0] if T - pp['socket'][1] >= ti[1] else pp['tie']['hole'], H - T - 1, H - pp['socket'][1] + 0.5)
    else:
        for rx, ry in rods:
            top -= cyl('z', (rx, ry), 12.0, H - 15.0, H + 1)      # M8 threaded inserts, 12 drilled 15 deep
        top -= cyl('z', (cx, D - 70.0), 16.5, H - T - 1, H + 1)
    bottom = box(T, 0, 0, W - T, D, T)
    for x, y in feet_places(P):                       # round 14: the levelling feet's inserts
        bottom -= cyl('z', (x, y), P['feet']['insert'][0], -1, P['feet']['insert'][1])
    braces = []
    ym = (yb + T + D - T) / 2
    ye, ytr = back_edge(P)                            # round 14: the braces stop short of the back, which comes off
    for b in P['braces']:
        brace = box(T, yb + T, b['z'], W - T, ye, b['z'] + T)
        (bw, _), (wy0, wy1) = b['window'], brace_window(P, b)
        braces.append(brace - box(cx - bw / 2, wy0, b['z'] - 1, cx + bw / 2, wy1, b['z'] + T + 1))
    ribs = []
    if P['ribs']:
        # ribs on edge inside the shell (the cabinet without wood): one up each side at mid-depth, in lengths between the
        # braces, and one front to back under the top and over the bottom; a pair up the back, welded to it, its full
        # height between the land strips, so they come off with it (round 14)
        rb = P['ribs']; rt, rd = rb['t'], rb['depth']
        ys, xs = rb.get('side') or (ym,), rb.get('top') or (cx,)     # the sides' ribs (y), the top's and the bottom's (x)
        for k, (z0, z1) in enumerate(rib_spans(P), 1):
            for j, y in enumerate(ys):
                n = f'{k}' + (chr(ord('a') + j) if len(ys) > 1 else '')
                ribs.append((f'rib-left-{n}', box(T, y - rt / 2, z0, T + rd, y + rt / 2, z1)))
                ribs.append((f'rib-right-{n}', box(W - T - rd, y - rt / 2, z0, W - T, y + rt / 2, z1)))
        for j, x in enumerate(rb['back'], 1):
            ribs.append((f'rib-back-{j}', box(x - rt / 2, D - T - rd, T + bk['land'] + 0.5, x + rt / 2, D - T, H - T - bk['land'] - 0.5)))
        pad = top_boss(P)
        for j, x in enumerate(xs, 1):
            n = f'-{j}' if len(xs) > 1 else ''
            yt = min(ytr, pad[1] - 1.0) if pad and x + rt / 2 > pad[0] and x - rt / 2 < pad[2] else ytr   # round 15: short of the pad
            ribs.append((f'rib-top{n}', box(x - rt / 2, yb + T, H - T - rd, x + rt / 2, yt, H - T)))
            ribs.append((f'rib-bottom{n}', box(x - rt / 2, yb + T, T, x + rt / 2, ytr, T + rd)))

    shell = [Part('left', box(0, 0, 0, T, D, H), ply('z'), finish='bark', group='cabinet'),
             Part('right', box(W - T, 0, 0, W, D, H), ply('z'), finish='bark', group='cabinet'),
             Part('top', top, ply('x', '+z'), finish='bark', group='cabinet'),
             Part('bottom', bottom, ply('x', '-z'), finish='bark', group='cabinet')]
    if P.get('roto'):
        shell = [roto_shell(P, [p.solid for p in shell])]
    out = shell + [
        Part('front-panel', baffle, ply('z', '-y'), finish='panel' if wood else 'bark', group='cabinet'),
        Part('back', back, ply('z', '+y'), finish='bark', group='cabinet'),
    ] + [Part('brace' if i == 0 else f'brace-{i + 1}', b, ply('x', '+z'), finish='raw' if wood else 'bark', group='cabinet', inside=True)
         for i, b in enumerate(braces)] + [Part(n, r, ply('z'), finish='bark', group='cabinet', inside=True,
                                                notes=[f'{P["ribs"]["depth"]:g} on edge, '
                                                       + {'hdpe': 'extrusion welded', 'acrylic': 'cemented', 'wood': 'glued'}[kind] + ' to '
                                                       + ('the back both sides: it comes off with the back' if n.startswith('rib-back') else
                                                          'the panel both sides')])
                                           for n, r in ribs]
    batts = [Part(n, s, Sheet(P['lining']['stock'], batt_t(P, n)), finish='lining', group='lining', inside=True,
                 pieces={'web': (soft(s, P['lining']['soft']), 'lining')},
                 notes=['cut 10 full each way, sewn into its voile sleeve and pressed into its bay; '
                        + ('stapled through the sleeve\'s edge to the panel' if wood else 'four dots of tape hold it flat on the wall')])
            for n, s in lining(P, plen, ribs)]

    # the ring over the woofer's frame, standing on the panel; the square port's tube, printed
    r = P['ring']
    ring = cyl('y', (cx, wz), r['od'], yb - r['t'], yb) - cyl('y', (cx, wz), r['id'], yb - r['t'] - 1, yb + 1)
    for k in range(wf['bolts']):          # pockets behind it for the woofer's screw heads: it lies flat over the frame
        a = 2 * math.pi * (k + 0.5) / wf['bolts']
        ring -= cyl('y', (cx + wf['bolt_d'] / 2 * math.cos(a), wz + wf['bolt_d'] / 2 * math.sin(a)), 14.0, yb - 4.0, yb + 1)
    for mx, mz in disc_magnets(P, cx, wz):  # and four for steel discs, behind its face, so the face stays clean (round 13)
        ring -= cyl('y', (mx, mz), mg['pocket'], yb - mg['t'] - 0.2, yb + 1)
    out.append(Part('woofer-ring', ring, Sheet(r['stock'], r['t'], face='-y'), finish='ring', group='cabinet',
                    notes=[('sprayed in the ring colour' if r['stock'] == 'mdf' else 'cast acrylic, tinted opaque in the ring colour'
                            if 'acrylic' in r['stock'] else 'pressed in the ring colour, one colour of flake')
                           + '; eight pockets behind it clear the woofer\'s screw heads; four more hold steel discs '
                           f'({mg["d"]:g} x {mg["t"]:g}), {"pressed" if mg["pocket"] < mg["d"] else "bonded"} in: the magnets under them in the panel '
                           'hold the ring, and the cloth disc\'s hold to them through it, more weakly, so the disc comes away alone']))
    tune = ((f'the {len(pt["x"])} together tune' if len(pt['x']) > 1 else 'it tunes') + f' the box to {P["fb"]:g} Hz; '
            + ('its length found on the first sample (three made 10 apart, the one whose impedance minimum falls at fb kept) '
               'and the rest made to it: its rounded ends cannot be trimmed' if pt['flare'] else 'print 15 longer and trim to tune with the back off'))
    fit = (f'fitted from the front, the frame flush in a {ft + sl:g} recess on a {sl:g} closed-cell PE foam gasket, four black countersunk '
           + {'wood': 'wood screws', 'hdpe': 'thread-forming screws for plastics', 'acrylic': 'M4 screws into threads tapped in the panel'}[kind]
           + ' in its corners')
    for px in pt['x']:
        side = '' if len(pt['x']) == 1 else ('-left' if px < cx else '-right')
        if pt['stock']:
            # round 15, the owner's pick for the Cloud: the port in the cabinet's own acrylic, a tube flared over a mandrel and
            # cemented into a frame cut from sheet (the frame holds the whole front flare, so no joint shows in the mouth)
            frame, tube = port_solid(P, px, plen, split=True)
            out.append(Part('port' + side, tube, Machined(pt['stock'], 'formed', setup_usd=250.0), finish='bark', group='cabinet',
                            notes=[f'cast acrylic tube {pt["d"] + 2 * pt["wall"]:g} x {pt["wall"]:g} ({pt["d"]:g} bore, polished), '
                                   f'{plen - ft:.0f} long behind its frame, its inner end flared to R{pt["flare"]:g} over a heated mandrel '
                                   f'and annealed; cemented square into its frame\'s back face; {tune}']))
            out.append(Part('port-frame' + side, frame, Sheet(pt['stock'], ft, face='-y'), finish='bark', group='cabinet',
                            notes=[f'{fr:g} square, corners R{pt["frame_r"]:g}, its bore {pt["d"]:g}, the mouth rounded over R{pt["flare"]:g} '
                                   'on the router and flame polished, the edges polished; four holes countersunk for M4; ' + fit]))
        else:
            out.append(Part('port' + side, port_solid(P, px, plen), Printed('asa', orient='on its frame'), finish='port', group='cabinet',
                            notes=[f'{pt["d"]:g} across inside, {plen:.0f} long from the panel\'s face, its {fr:g} square frame '
                                   f'(corners R{pt["frame_r"]:g}) printed in one'
                                   + (f', both mouths rounded on R{pt["flare"]:g}' if pt['flare'] else '') + f': {tune}; {fit}']))

    # round 31: the screws in the slots the panel's holes are under, the gasket in the rebate, the terminals on the lower
    # spoke where the lead ends (its depth behind the flange, and the posts' base radius), the spokes so one runs down
    woofer, _ = driver_part('woofer', P['woofer'], dict(wf, bolt_phase=0.5, spoke_phase=0.5, gasket_t=P['gasket'], terminals=(68.0, 119.0)),
                            centre=(cx, yb, wz))
    out.append(woofer)
    plate = box(cx - amp['plate_w'] / 2, D - 3.0, az - amp['plate_h'] / 2, cx + amp['plate_w'] / 2, D, az + amp['plate_h'] / 2)
    module = box(cx - amp['cutout_w'] / 2 + 4, D - amp['depth'], az - amp['cutout_h'] / 2 + 6, cx + amp['cutout_w'] / 2 - 4, D - 3.0, az + amp['cutout_h'] / 2 - 6)
    out.append(Part('amp-plate', plate.fuse(module), Bought(P['amp']), finish='amp', pieces=amp_plate_pieces(amp, cx, D, az)))
    later = amp_compartment(P, ribs, wz, wood)       # round 13's parts, numbered after the ones the drawings have long had

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
                                (('closes the pod behind the driver on a twist-lock: three lugs cast on its spigot go into L-slots '
                                  f'in the pod\'s bore and an eighth of a turn ({hz["cast"]["lock"]["turn"]:g} degrees, clockwise from '
                                  'behind) locks them, a small bump in each slot clicking them home; an O-ring on the spigot, '
                                  'beyond the lugs, seals it and stops it rattling; two shallow finger dimples to turn it by; '
                                  'no screw shows; ') if hz['form'] == 'cast' and hz['cast'].get('lock') else
                                 'closes the pod behind the driver; a spigot locates it, three M4 screws hold it; ')
                                + ('the HF pair leaves through a post below; unplugged here, the horn lifts off its sockets'
                                   if hz['form'] == 'cast' else 'the cable leaves through its centre'))]))
        if wg.get('ring') is not None:
            later.append(Part('cap-o-ring', wg['ring'], Bought('cap-o-ring'), finish='sleeve', group='horn', inside=True,
                              notes=['in the groove on the cap\'s spigot, beyond the lugs; a smear of silicone grease so it turns']))
    hfp, _ = driver_part('hf', P['hf'], hf, centre=(cx, wg['driver_y'], zc))
    out.append(hfp)
    if hz['form'] == 'cast':
        out.append(adaptor_ring(P, wg, hf))
    from build123d import Axis
    if hz['form'] == 'cast':
        out += posts(P, rods, shell)
        later += fittings(P, rods, shell)
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

    out += covers(P, wz)
    if P['finish'] == 'faced':
        out += skins(P, rod_places(P), amp)
    elif P['finish'] == 'bark':
        out.append(Part('bark', None, Bought('bark-sheet'), qty=2, notes=['about 1.75 m2 a speaker: the shell\'s sides, top, bottom, back and front edges']))
    later += back_and_feet(P, kind) + [port_screws_part(P, kind)]     # round 14's
    tb = top_boss(P)
    if tb:                                            # round 15's: the pad under the top for the rear posts' fixings
        pp = hz['cast']['posts']; (gx, gy), (tx, ty) = rod_places(P)[pp['cable_post']], rod_places(P)[pp['tie_post']]
        ti = pp['tie']['insert']
        pad = box(tb[0], tb[1], tb[4], tb[2], tb[3], tb[5])
        pad -= cyl('z', (gx, gy), 10.5, tb[4] - 1, tb[5] + 1)                  # tapped M12 for the HF lead's gland
        pad -= cyl('z', (tx, ty), ti[0], tb[4] - 1, tb[4] + ti[1])             # the tie rod's insert, from below
        pad -= cyl('z', (tx, ty), pp['tie']['hole'], tb[4], tb[5] + 1)
        later.append(Part('top-pad', pad, ply('x', '-z'), finish='raw' if wood else 'bark', group='cabinet', inside=True,
                          notes=[f'{tb[2] - tb[0]:g} x {tb[3] - tb[1]:g}, cut from the shell\'s own sheet, '
                                 + {'wood': 'glued and screwed', 'hdpe': 'extrusion welded round its edges', 'acrylic': 'cemented'}[kind]
                                 + ' under the top between the rear posts, so the tie rod\'s insert and the HF lead\'s gland have '
                                 f'{T - pp["socket"][1] + T:g} to hold in under the sockets; tapped M12 through for the gland']))
    out += later + batts                          # after the parts the drawings have numbered since round 5
    out += [
        (Part('woofer-fixings', None, Bought('m6-tnut-set'), notes=['the T-nuts hammered in from inside before the glue-up']) if wood else
         Part('woofer-fixings', None, Bought('m6-plastic-inserts'),
              notes=[f'the inserts screwed into the panel from the front, in {P["woofer_hole"]:g} holes; the screws\' torque checked again '
                     'after 48 hours (HDPE creeps)']) if kind == 'hdpe' else
         Part('woofer-fixings', None, Bought('m6-acrylic-inserts'),
              notes=[f'the inserts bonded into the panel with epoxy, in {P["woofer_hole"]:g} holes, flush with its face'])),
        Part('hf-fixings', None, Bought('hf-mount-screws' if hz['form'] == 'cast' else 'm6-hf-screws')),
        *({'hdpe': [Part('weld-rod', None, Bought('hdpe-weld-rod'))], 'acrylic': [Part('cement', None, Bought('acrylic-cement'))]}.get(kind, [])),
        Part('gasket', None, Bought('gasket-foam'), qty=2),
        Part('lining-sleeves', None, Bought('voile-sleeves')),
        *({'hdpe': [Part('lining-tape', None, Bought('lse-tape-dots'))], 'acrylic': [Part('lining-tape', None, Bought('vhb-clear-dots'))]}.get(kind, [])),
        Part('amp-fixings', None, Bought('amp-screws')),
        Part('amp-box-fixings', None, Bought('amp-box-screws')),
        *([] if hz['form'] == 'cast' else [Part('hf-cable', None, Bought('speaker-cable-1m'))]),
        Part('hf-capacitor', None, Bought('hf-protect-cap'), notes=['in series ahead of the L-pad: the driver safe from low frequencies '
                                                                    'even if the amplifier\'s preset is lost (a first-order high-pass at '
                                                                    'about 300 Hz into 16 ohm)']),
        Part('loom', None, Bought('loom-set')),
        Part('terminals', None, Bought('push-on-terminal'), qty=4),
        Part('back-inserts', None, Bought({'wood': 'm5-inserts-wood', 'hdpe': 'm5-inserts-plastic', 'acrylic': 'm5-inserts-acrylic'}[kind])),
        Part('feet-inserts', None, Bought({'wood': 'm8-inserts-wood', 'hdpe': 'm8-inserts-plastic', 'acrylic': 'm8-inserts-acrylic'}[kind])),
    ]
    return extras(P, out)


def wordmark_outlines(width):
    """EARF's wordmark (marks.py's shapes) as closed outlines [(u, v), ...] in mm, each with its holes' (round 29: the
    R's bowl a ring): [(outline, [hole, ...]), ...], u across from its left, v up from its foot, `width` wide."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import marks as M
    s = width / M.WORDMARK_W
    circle = lambda cx, cy, r: [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in (2 * math.pi * k / 72 for k in range(72))]
    mm = lambda pts: [(x * s, (300 - y) * s) for x, y in pts]
    out = []
    for p in M.WORDMARK:
        holes = []
        if p[0] == 'rect':
            x0, y0, x1, y1 = p[1:5]
            pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        elif p[0] == 'circle':
            pts = circle(p[1], p[2], p[3])
        elif p[0] == 'ring':
            pts, holes = circle(p[1], p[2], p[3]), [circle(p[1], p[2], p[4])]
        else:
            pts = list(p[1:])
        out.append((mm(pts), [mm(h) for h in holes]))
    return out


def wordmark_height(width):
    """The wordmark's height when it is `width` wide (its cap height, 300, of marks.py's WORDMARK_W: round 26's narrower
    A made it 980, not 1020)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import marks as M
    return width * 300 / M.WORDMARK_W


def mark_solid(width, at, face, t):
    """The wordmark `width` wide as a solid `t` deep on a face of the cabinet: `face` '-y' (a front face, read from in
    front) or '+y' (a back face, read from behind, so drawn mirrored), `at` = (x of its middle, y of the face, z of its
    foot)."""
    xm, yf, z0 = at
    on = (lambda q: [(xm - width / 2 + u, z0 + v) for u, v in q]) if face == '-y' else \
         (lambda q: [(xm + width / 2 - u, z0 + v) for u, v in q])
    y0, y1 = (yf - t, yf) if face == '-y' else (yf, yf + t)
    sol = []
    for o, holes in wordmark_outlines(width):
        s = prism(on(o), 'y', y0, y1)
        for h in holes:                                  # cut a little past both faces, so no skin is left
            s = s - prism(on(h), 'y', y0 - 0.01, y1 + 0.01)
        sol.append(s)
    return union(*sol)


def _globe():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brand', 'earth-outlines.json')))


def globe_outlines(style):
    """Round 24 (24b): the globe (earth.py's outlines, brand/earth-outlines.json): `style` 'discs' (seamed, for one
    colour), 'flush' (for colour), 'base' (round 24b's ball gaps at the rim; empty since round 25, the globe its discs
    alone) or 'lines': [(ring, exterior, holes)] on the unit globe, y up."""
    return [tuple(q) for q in _globe()[style]]


def globe_colours():
    """Round 25: the rings' colours and the ring that fills the ball (earth.py's RING and ATMOS, by way of the
    outlines file, so a print follows the brand when its colours move)."""
    G = _globe()
    return G['ring'], G['atmos']


def globe_solid(d, at, face, t, style, rings=None):
    """The globe `d` across as a solid `t` deep on a face of the cabinet (as mark_solid): `at` = (x of its centre, y of
    the face, z of its centre); `rings` the rings whose shapes to keep (None for all)."""
    xc, yf, zc = at
    r, sx = d / 2, (1 if face == '-y' else -1)               # read from behind, mirrored
    y0, y1 = (yf - t, yf) if face == '-y' else (yf, yf + t)
    flat = lambda pts: [(xc + sx * r * u, zc + r * v) for u, v in pts]
    sol = []
    for k, ext, holes in globe_outlines(style):
        if rings is not None and k not in rings:
            continue
        s = prism(flat(ext), 'y', y0, y1)
        for h in holes:
            s = s - prism(flat(h), 'y', y0 - 0.05, y1 + 0.05)
        sol.append(s)
    return union(*sol)


def grip_boxes(P):
    """Round 21's recessed grips: each side's opening (y0, y1, z0, z1) and how deep its cup reaches in. P['grip_w'] the
    opening's length (round 23: 240 takes both hands, 124 one)."""
    g = dict(w=P.get('grip_w', 124.0), h=42.0, depth=40.0, below=92.0)
    y0, z1 = P['D'] / 2 - g['w'] / 2, P['H'] - g['below']
    return (y0, y0 + g['w'], z1 - g['h'], z1), g['depth']


def extras(P, out):
    """Round 21's options, none unless P asks. P['mark'] (the owner, of where EARF's mark goes on the speaker: "I'd
    like to see options"), any of: 'plate', laser-marked on the rating plate beside the amplifier; 'back', cut from 3 mm
    white acrylic and cemented high on the back; 'corner', laser-etched into the front panel's top right corner; 'edge',
    etched into the bottom's front edge, under the front panel; 'cap', etched into the horn's twist-lock cap; 'disc',
    printed low on the cloth disc. The mark is the wordmark: the globe is not chosen yet. P['lift'] (the owner, of
    lifting a 72 kg speaker: "Open to ideas"), any of: 'handles', a removable bar handle each side, screwed into two M8
    inserts bonded in the side near the top; 'castors', four castors screwed into the feet's M8 inserts in place of the
    feet; 'grips', a recessed grip in each side near the top, a cup of 3 mm acrylic cemented behind the opening, the
    side's batt cut round it.

    Round 23 (the owner: "either the front corner or high on the back, etched in the speakers own tint or uncolored"):
    the back's mark etched too, 140 wide, and P['mark_finish'] for the back's and the corner's: 'etch' (frosted,
    uncoloured) or 'tint' (the etch filled with the speaker's own colour, deeper: its cover's and ring's). And of the
    grips ("only if it would help ergonomically"): P['grip_w'], their length, 240 for two hands (grip_boxes).

    Round 24 (the owner: "I'm thinking logo in the corner, depending on what it looks like. Name on back own color"):
    'globe', the globe in the front panel's top right corner, P['globe'] = dict(d=its diameter, style='discs' (the
    facets, the seams clear) or 'lines' (the rings at one weight), finish='etch' (frosted), 'tint' (the etch filled
    with the speaker's own colour) or 'print' (UV-printed in the six colours on a white underprint: round 24b, flush,
    no seams and no outline, the ball violet where no disc reaches its rim)). The Cloud carries the back's name in its
    own colour and the 240 grips as standard (cloud.py)."""
    import dataclasses
    from build123d import Compound, Pos
    marks, lifts = P.get('mark') or [], P.get('lift') or []
    if not marks and not lifts:
        return out
    W, D, H, T = P['W'], P['D'], P['H'], P['T']
    by = {p.name: p for p in out}
    bb = lambda n: by[n].solid.bounding_box()
    add = []
    etched = 'laser-etched, frosted, about 0.1 deep'
    tint = P.get('mark_finish', 'etch') == 'tint'
    face_finish = 'mark-tint' if tint else 'etch'
    how = etched + (', the etch filled with the speaker\'s own colour, deeper' if tint else '')
    for m in marks:
        if m == 'plate':
            b = bb('rating-plate')
            add.append(Part('mark-plate', mark_solid(46.0, ((b.min.X + b.max.X) / 2, b.max.Y, b.max.Z - 8.0 - wordmark_height(46.0)), '+y', 0.1),
                            Bought('rating-plate'), finish='etch', notes=['EARF laser-marked across the rating plate\'s top, 46 wide']))
        elif m == 'back':
            add.append(Part('mark-back', mark_solid(140.0, (W / 2, D, H - 72.0 - wordmark_height(140.0)), '+y', 0.1),
                            Bought('laser-etch'), finish=face_finish,
                            notes=[f'EARF {how}, 140 wide, high on the back, centred']))
        elif m == 'corner':
            b = bb('front-panel'); w = 60.0
            add.append(Part('mark-corner', mark_solid(w, (b.max.X - 24.0 - w / 2, b.min.Y, b.max.Z - 24.0 - wordmark_height(w)), '-y', 0.1),
                            Bought('laser-etch'), finish=face_finish, notes=[f'EARF {how}, 60 wide, into the front panel\'s top right corner']))
        elif m == 'edge':
            w = 52.0
            add.append(Part('mark-edge', mark_solid(w, (W / 2, 0.0, (T - wordmark_height(w)) / 2), '-y', 0.1), Bought('laser-etch'),
                            finish='etch', notes=[f'EARF {etched}, 52 wide, centred in the bottom\'s front edge']))
        elif m == 'cap':
            cap = by['waveguide-cap'].solid; b = cap.bounding_box(); w = 64.0
            plate = mark_solid(w, ((b.min.X + b.max.X) / 2, b.max.Y - 4.0, (b.min.Z + b.max.Z) / 2 - wordmark_height(w) / 2), '+y', 4.12)
            skin = Pos(0, 0.12, 0) * cap - cap                    # a skin 0.12 deep on the cap's faces that look back
            add.append(Part('mark-cap', plate & skin, Bought('laser-etch'), finish='etch',
                            notes=[f'EARF {etched}, 64 wide, across the middle of the horn\'s cap, between its finger dimples']))
        elif m == 'globe':
            b = bb('front-panel'); g = P.get('globe') or {}
            d, style, fin = g.get('d', 48.0), g.get('style', 'discs'), g.get('finish', 'etch')
            c = (b.max.X - 24.0 - d / 2, b.min.Y, b.max.Z - 24.0 - d / 2)
            where = f'{d:g} across, its centre {24 + d / 2:g} in from the front panel\'s top and right edges'
            if fin == 'print':                           # in colour: flush, the discs alone (round 25: no ball filled)
                for k in range(6):
                    sol = globe_solid(d, c, '-y', 0.1, 'flush', rings=[k])
                    add.append(Part(f'mark-globe-{k}', sol, Bought('uv-print'), finish=f'print-{k}',
                                    notes=[f'the globe\'s ring {k + 1} of six, UV-printed in its colour, flush with the next; {where}']))
            else:
                add.append(Part('mark-globe', globe_solid(d, c, '-y', 0.1, style), Bought('laser-etch'),
                                finish='mark-tint' if fin == 'tint' else 'etch',
                                notes=[f'the globe ({style}) {etched}' + (', the etch filled with the speaker\'s own colour, deeper'
                                                                         if fin == 'tint' else '') + f'; {where}']))
        elif m == 'disc':
            b = bb('cloth-disc'); w = 64.0
            add.append(Part('mark-disc', mark_solid(w, ((b.min.X + b.max.X) / 2, b.min.Y, b.min.Z + 34.0), '-y', 0.1), Bought('cloth-print'),
                            finish='print', option=by['cloth-disc'].option, notes=['EARF printed in white on the cloth, 64 wide, low on the disc']))
    if 'handles' in lifts:
        yc, zc = D / 2, H - 110.0
        for side, x0, sgn in (('left', 0.0, -1), ('right', W, 1)):
            legs = [cyl('x', (y, zc), 18.0, x0, x0 + sgn * 44.0) for y in (yc - 62.0, yc + 62.0)]
            bar = cyl('y', (x0 + sgn * 35.0, zc), 22.0, yc - 76.0, yc + 76.0)
            add.append(Part(f'handle-{side}', union(*legs, bar), Bought('lift-handles'), finish='rod',
                            notes=['a stainless bar handle, 150 between its legs, screwed into two M8 inserts bonded in the side; '
                                   'off when the speaker is in place, the inserts left as two small brass rings']))
    if 'castors' in lifts:
        out = [p for p in out if p.name != 'feet']
        hubs, wheels = [], []
        for x, y in feet_places(P):
            hubs.append(cyl('z', (x, y), 42.0, -14.0, 0.0).fuse(box(x - 15.0, y - 26.0, -46.0, x + 15.0, y + 8.0, -14.0)))
            for dx in (-15.5, 3.5):
                wheels.append(cyl('x', (y - 9.0, -37.0), 50.0, x + dx, x + dx + 12.0))
        add.append(Part('castors', Compound(children=hubs), Bought('castors-m8'), finish='amp',
                        notes=['four twin-wheel swivel castors, 50 wheels, M8 stems screwed into the feet\'s inserts in place of '
                               'the feet to move the speaker, the feet back in to stand it']))
        add.append(Part('castor-wheels', Compound(children=wheels), Bought('castors-m8'), finish='sleeve'))
    if 'grips' in lifts:
        (y0, y1, z0, z1), dep = grip_boxes(P)
        hole = lambda x_a, x_b: prism(rounded_rect(y1 - y0, z1 - z0, 14.0, cx=(y0 + y1) / 2, cy=(z0 + z1) / 2), 'x', x_a, x_b)
        for side, (xa, xb), (ca, cb) in (('left', (-1.0, T + 1.0), (T, T + dep)), ('right', (W - T - 1.0, W + 1.0), (W - T - dep, W - T))):
            p = by[side]
            out = [dataclasses.replace(q, solid=q.solid - hole(xa, xb)) if q.name == side else q for q in out]
            cup = box(ca, y0 - 3.0, z0 - 3.0, cb, y1 + 3.0, z1 + 3.0) - hole(*((T - 1.0, T + dep - 3.0) if side == 'left' else (W - T - dep + 3.0, W - T + 1.0)))
            # round 24: the cup drape-formed from 3 mm sheet over a buck (a box with rounded corners is not a flat part)
            add.append(Part(f'grip-{side}', cup, Machined('cast-acrylic-formed', 'formed', setup_usd=120.0), finish='bark', inside=True,
                            notes=[f'a hand grip {y1 - y0:g} x {z1 - z0:g}, its corners rounded on 14, cut through the side; a cup '
                                   f'drape-formed from 3 mm acrylic in the side\'s tint over a buck, {dep:g} deep, its flange '
                                   f'trimmed and cemented behind the opening, so the box stays sealed']))
    return out + add


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
    """The ring's and the cloth disc's magnets' centres (x, z), between the woofer's screws: on the circle `r` between
    the woofer's rebate and the ring's edge (round 13), so the panel's magnets sit in the panel, clear of the rebate."""
    mg = P['cover']['disc_magnet']
    rm, n = mg['r'], mg['n']
    rebate = (LIB[P['woofer']]['geom']['frame_od'] + 1.6) / 2
    assert rm - mg['d'] / 2 > rebate + 1.0 and rm + mg['d'] / 2 < P['ring']['od'] / 2 - 1.0, 'the magnets must sit between the rebate and the ring\'s edge'
    return [(cx + rm * math.cos(2 * math.pi * k / n), wz + rm * math.sin(2 * math.pi * k / n)) for k in range(n)]


def roto_shell(P, panels):
    """The rotomoulded shell (a study, round 14: the production route the pressed sheet's suppliers point to): the
    sides, the top and the bottom moulded as one hollow part, a double wall `skin` thick each side round a hollow core,
    its outside edges rounded on `r`, the front's inside edge on `r_in`. Moulded, the bark's laid-out pattern turns
    to speckle."""
    W, D, H, T = P['W'], P['D'], P['H'], P['T']
    ro = P['roto']; r, sk = ro['r'], ro['skin']
    shell = panels[0]
    for s in panels[1:]:
        shell = shell.fuse(s)
    shell = shell.clean()

    def edges(solid, x0, x1, y0, y1, z0, z1, inner=None):
        """The edges round a box's outside: along y at its corners, and round its front and back faces."""
        on = lambda v, vals: any(abs(v - q) < 0.01 for q in vals)
        out = []
        for e in solid.edges():
            b = e.bounding_box()
            fx, fy, fz = b.max.X - b.min.X < 0.01, b.max.Y - b.min.Y < 0.01, b.max.Z - b.min.Z < 0.01
            if fx and fz and on(b.min.X, (x0, x1)) and on(b.min.Z, (z0, z1)):
                out.append(e)
            elif fy and on(b.min.Y, (y0, y1)) and ((fx and on(b.min.X, (x0, x1))) or (fz and on(b.min.Z, (z0, z1)))):
                out.append(e)
        return out
    shell = shell.fillet(r, edges(shell, 0, W, 0, D, 0, H))
    inner = [e for e in shell.edges() if (lambda b: b.max.Y - b.min.Y < 0.01 and abs(b.min.Y) < 0.01 and
                                         ((b.max.X - b.min.X < 0.01 and any(abs(b.min.X - q) < 0.01 for q in (T, W - T))) or
                                          (b.max.Z - b.min.Z < 0.01 and any(abs(b.min.Z - q) < 0.01 for q in (T, H - T)))))(e.bounding_box())]
    if inner and ro.get('r_in'):
        shell = shell.fillet(ro['r_in'], inner)
    core = box(sk, sk, sk, W - sk, D - sk, H - sk)
    core = core.fillet(r - sk, edges(core, sk, W - sk, sk, D - sk, sk, H - sk))
    core -= box(T - sk, -1, T - sk, W - T + sk, D + 1, H - T + sk)
    shell -= core
    return Part('shell', shell, Machined('rotomoulded-pe', 'rotomoulded', setup_usd=12000.0), finish='bark', group='cabinet',
                notes=[f'the sides, the top and the bottom rotomoulded as one in recycled PE, a double wall ({sk:g} skins round a '
                       f'hollow core), its outside edges rounded on R{r:g}; the bark\'s colours as speckle'])


def port_screws(P, px):
    """A port's frame's four screws' centres (x, z), 12 in from its edges."""
    pt = P['port']; e = pt['frame'] / 2 - 12.0
    return [(px + sx * e, pt['z'] + sz * e) for sx in (-1, 1) for sz in (-1, 1)]


def cone_y(c, d0, d1, y0, y1):
    """A cone's frustum along y through (x, z) = c: d0 across at y0, d1 at y1."""
    return revolve_profile([(0.0, 0.0), (d0 / 2, 0.0), (d1 / 2, y1 - y0), (0.0, y1 - y0)], 'y', (c[0], y0, c[1]))


def port_solid(P, px, plen, split=False):
    """A port as printed (round 14): its tube, `plen` long from the panel's face, and its square frame in one, the
    frame's corners countersunk for its screws; with `flare`, both mouths rounded on it, the inner one a bell. Each
    profile (r, h) runs along the port from the panel's face. `split`: (the frame, the tube) apart, the tube from the
    frame's back face (round 15: the Cloud's, cemented together)."""
    pt = P['port']; yb = P['inset']
    ri, ro, R, ft, pz = pt['d'] / 2, pt['d'] / 2 + pt['wall'], pt['flare'], pt['frame_t'], pt['z']

    def arc(c, r, a0, a1, n=24):
        return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / n)))
                for k in range(n + 1)]
    c = (px, yb, pz)
    frame = prism(rounded_rect(pt['frame'], pt['frame'], pt['frame_r'], cx=px, cy=pz), 'y', yb, yb + ft)
    if R:
        # the tube's wall as one section from the frame's back face (no boolean between two revolutions that meet at the
        # bell's rim: OCC returns the first unchanged): the front flare's last part, the bore, the bell rolled out to
        # its rim, and back down its outside. The arcs are polylines of 24 (a spline's surface of revolution fails in
        # the frame's cut, silently, and leaves the frame whole)
        if ft < R:
            ra = ri + R - math.sqrt(R * R - (R - ft) ** 2)
            front = arc((ri + R, R), R, math.degrees(math.atan2(ft - R, ra - ri - R)) % 360, 180)
        else:
            front = [(ri, ft)]
        wall = [(ro, ft)] + front + arc((ri + R, plen - R), R, 180, 90) + arc((ri + R, plen - R), R - pt['wall'], 90, 180)
        tube = revolve_profile(wall, 'y', c)
        mouth = [(0.0, -1.0), (ri + R, -1.0)] + arc((ri + R, R), R, 270, 180) + [(ri, max(R, ft) + 1.0), (0.0, max(R, ft) + 1.0)]
        frame = frame - revolve_profile(mouth, 'y', c)
    else:
        tube = revolve_profile([(ri, ft), (ro, ft), (ro, plen), (ri, plen)], 'y', c)
        frame = frame - cyl('y', (px, pz), 2 * ri, yb - 1, yb + ft + 1)
    sh, sk = pt['screw']
    for sx, sz in port_screws(P, px):
        frame -= cyl('y', (sx, sz), sh, yb - 1, yb + ft + 1)
        frame -= cone_y((sx, sz), sk, sh, yb, yb + (sk - sh) / 2)               # a 90 degree countersink
    return (frame, tube) if split else frame.fuse(tube)


def port_screws_part(P, kind):
    """The ports' screws (round 14): four black countersunk screws through each frame's corners into the panel, their
    heads flush with the frame's face."""
    from build123d import Compound
    pt, yb = P['port'], P['inset']
    sh, sk = pt['screw']
    L, dep = port_screw_len(P)
    d0, d1 = sk - 0.2, sh - 0.2
    yh = yb + 0.1 + (d0 - d1) / 2
    heads = [cone_y((sx, sz), d0, d1, yb + 0.1, yh).fuse(cyl('y', (sx, sz), 3.2, yh - 0.1, yb + L))     # the thread's core
             for px in pt['x'] for sx, sz in port_screws(P, px)]
    return Part('port-screws', Compound(children=heads), Bought('port-fixings'), finish='screw', group='cabinet',
                notes=[f'{len(heads)} black countersunk ' + {'wood': f'wood screws 4 x {L:g} into 3.5 pilot holes',
                                                             'hdpe': f'thread-forming screws for plastics (EJOT PT K40 x {L:g} kind) into 3.5 pilot holes',
                                                             'acrylic': f'M4 x {L:g} screws into threads tapped (3.3 drill)'}[kind]
                       + f' {dep:g} deep in the recess\'s floor, four through each port\'s frame, on the foam gasket'])


def feet_places(P):
    """The levelling feet's centres (x, y) under the bottom, `inset` in from its edges."""
    i = P['feet']['inset']
    return [(x, y) for x in (i, P['W'] - i) for y in (i, P['D'] - i)]


def back_and_feet(P, kind):
    """Round 14, the owner's picks (the reality check's r4 and r11). The back comes off: it closes on an EPDM gasket
    against four land strips fixed inside the shell (welded in HDPE; cleats glued and screwed in plywood), sixteen M5
    button heads through it into inserts in the strips. The amplifier's compartment, the back's ribs and its batts come
    off with it; the leads unplug at the compartment. Four levelling feet in inserts in the bottom lift the cabinet
    `lift` and level it."""
    from build123d import Compound
    W, D, H, T = P['W'], P['D'], P['H'], P['T']
    bk = P['back']; lw, gk, bc = bk['land'], bk['gasket'], bk['clear']
    yl1 = D - T - gk; yl0 = yl1 - T                  # the strips' back face (the gasket on it) and their front
    screws = back_screws(P)
    hd, hl = bk['insert']
    wood = kind == 'wood'
    fix = {'hdpe': 'extrusion welded to the shell along both edges', 'acrylic': 'cemented to the shell along both edges',
           'wood': 'a cleat glued and screwed to the shell'}[kind]
    ins = {'wood': 'for wood', 'hdpe': 'for plastics', 'acrylic': 'bonded with epoxy'}[kind]
    out = []
    for n, s in (('land-left', box(T, yl0, T, T + lw, yl1, H - T)), ('land-right', box(W - T - lw, yl0, T, W - T, yl1, H - T)),
                 ('land-top', box(T + lw, yl0, H - T - lw, W - T - lw, yl1, H - T)),
                 ('land-bottom', box(T + lw, yl0, T, W - T - lw, yl1, T + lw))):
        bb, k = s.bounding_box(), 0
        for sx, sz in screws:
            if bb.min.X < sx < bb.max.X and bb.min.Z < sz < bb.max.Z:
                s -= cyl('y', (sx, sz), hd, yl1 - hl, yl1 + 1); k += 1
        out.append(Part(n, s, Sheet(P['stock'], T, face='+y', grain='z' if n in ('land-left', 'land-right') else 'x'),
                        finish='raw' if wood else 'bark', group='cabinet', inside=True,
                        notes=[f'{lw:g} x {T:g}, {fix}, its back face {gk + T:g} in from the shell\'s back edge; {k} M5 inserts '
                               + ins + f' in {hd:g} holes {hl:g} deep take the back\'s screws']))
    gasket = box(T + bc, yl1, T + bc, W - T - bc, D - T, H - T - bc) - box(T + lw, yl1 - 1, T + lw, W - T - lw, D - T + 1, H - T - lw)
    for sx, sz in screws:
        gasket -= cyl('y', (sx, sz), 6.0, yl1 - 1, D - T + 1)
    out.append(Part('back-gasket', gasket, Bought('back-gasket'), finish='sleeve', group='cabinet', inside=True,
                    notes=[f'{lw - bc:g} wide, {gk:g} thick, on the land strips under the back\'s edge, punched for the screws, which '
                           'locate it' + (' (no adhesive: HDPE holds none)' if kind == 'hdpe' else '') + '; at full output the box runs at '
                           'about 1 kPa inside, so it must seal all round']))
    heads = []
    for sx, sz in screws:
        h = cyl('y', (sx, sz), 9.5, D, D + 2.8)
        try:
            h = h.fillet(1.4, [e for e in h.edges() if abs(e.center().Y - (D + 2.8)) < 0.01])
        except Exception:
            pass
        heads.append(h.fuse(cyl('y', (sx, sz), 4.8, yl1 - hl + 2.0, D)))
    out.append(Part('back-screws', Compound(children=heads), Bought('back-screws'), finish='screw', group='cabinet',
                    notes=[f'{len(screws)} M5 x {round(T + gk + hl - 2, -1):g} button heads (ISO 7380, A2, black: round 16) on black nylon washers, '
                           f'{bk["edge"]:g} in from the back\'s edges, into the inserts in the land strips; tightened evenly '
                           'round the back, by hand, to compress the gasket without crushing it']))
    f = P['feet']
    bases = [cyl('z', (x, y), f['d'], -f['lift'], -f['lift'] + f['base']) for x, y in feet_places(P)]
    stems = [cyl('z', (x, y), 13.0, -5.0, 0.0).fuse(cyl('z', (x, y), 7.8, -f['lift'] + f['base'] - 0.5, f['insert'][1] - 1.0))
             for x, y in feet_places(P)]
    out.append(Part('feet', Compound(children=[b.fuse(t) for b, t in zip(bases, stems)]), Bought('levelling-feet'), finish='foot',
                    group='cabinet', pieces={'base': (Compound(children=bases), 'foot'), 'stem': (Compound(children=stems), 'rod')},
                    notes=[f'4 levelling feet, M8, a {f["d"]:g} swivel base on a rubber pad, in M8 inserts '
                           + ins + f' ({f["insert"][0]:g} holes {f["insert"][1]:g} deep) '
                           f'{f["inset"]:g} in from the bottom\'s edges; set to {f["lift"]:g} and levelled, then locked by their nuts']))
    return out


def insert_depth(pp, ry, depth):
    """A pad's insert's depth: the front pair's shorter (round 13, r1: a 14 left only 3 to 8 of resin under the flare)."""
    return pp['front_insert_depth'] if ry < depth / 2 else pp['insert_depth']


def posts(P, places, shell):
    """The cast horn's four posts: stainless lamp tube threaded M10 x 1 at its top, screwed into a brass insert bonded in
    a pad under the horn, its plain foot standing in a polyurethane sleeve in a brass socket pressed into the top (round
    11: a post threaded into fixed inserts at both ends cannot be screwed home, so the horn and its posts lift off as one;
    round 13: the sleeve, and a rod down the free rear post holds them down); the HF lead comes down inside one of them."""
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
        idep = insert_depth(pp, ry, P['horn']['cast']['d'])
        z0, z1 = H - pp['socket'][1] + 2.0, foot + idep - 2.0
        tube = cyl('z', (rx, ry), pp['d'], z0, z1) - cyl('z', (rx, ry), pp['bore'], z0 - 1, z1 + 1)
        cable, tie = i == pp['cable_post'] + 1, i == pp['tie_post'] + 1
        out.append(Part(f'post-{i}', tube, Machined('stainless', 'lathe'), finish='rod', group='horn',
                        notes=[f'{z1 - z0:.0f} long ({foot - H:.0f} showing): stainless tube {pp["d"]:g} x {pp["bore"]:g}, threaded M10 x 1 '
                               f'{idep - 2:g} at the top into the brass insert in its pad; its foot plain, standing '
                               f'{pp["socket"][1] - 2:g} deep in a polyurethane sleeve in a brass socket in the top; its bore deburred'
                               + ('; the HF lead runs down inside it' if cable else '') + ('; the tie rod runs down inside it' if tie else '')]))
    return out



def tube_along(pts, d):
    """A cable: a tube `d` across through the points (straight runs, rounded at each bend)."""
    from build123d import Plane, Pos, Solid, Vector
    out = None
    for a, b in zip(pts, pts[1:]):
        va, vb = Vector(*a), Vector(*b)
        seg = Solid.make_cylinder(d / 2, (vb - va).length, Plane(origin=va, z_dir=vb - va))
        out = seg if out is None else out.fuse(seg)
    for q in pts[1:-1]:
        out = out.fuse(Pos(*q) * Solid.make_sphere(d / 2))
    return out


def rating_plate_pieces(cx, D, az, pw):
    """The rating plate beside the amplifier (round 13's part: 70 x 40 x 1, black anodised aluminium, two M3 screws),
    laser-marked, for the render only (round 31: the finals showed it as a blank grey tile, which read as a fault). In
    white, left to right as one faces the back: the maker; the product; its model and serial number; the ratings, the
    FA122's own (its plate's); where it was designed; and the marks, CE, UKCA, FCC and the WEEE bin. Its two black pan
    heads either end. Returns {piece: (solid, finish)}, as amp_plate_pieces does."""
    from build123d import Align, Compound, Plane, Text, extrude
    FONT, BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    rx, rz, y = cx + pw + 55.0, az + 80.0, D + 1.0          # the plate's middle on the back's outer face; +u to one's left
    prn = []

    def text(st, u, v, size=1.7, bold=False, wmax=50.0):
        """Print from (u, v) rightward as one reads it, `size` mm tall (smaller if it would pass `wmax`)."""
        fp = BOLD if bold else FONT
        w = Text(st, font_size=size, font_path=fp).bounding_box().size.X
        if w > wmax:
            size *= wmax / w
        sk = Text(st, font_size=size, font_path=fp, align=(Align.MIN, Align.CENTER))
        return extrude(Plane(origin=(rx + u, y, rz + v), x_dir=(-1, 0, 0), z_dir=(0, 1, 0)) * sk, amount=0.05)

    def bar(u0, v0, u1, v1, wd=0.4):
        """A printed stroke between two points."""
        L = math.hypot(u1 - u0, v1 - v0); nu, nv = -(v1 - v0) / L * wd / 2, (u1 - u0) / L * wd / 2
        return prism([(rx + u0 + nu, rz + v0 + nv), (rx + u1 + nu, rz + v1 + nv), (rx + u1 - nu, rz + v1 - nv),
                      (rx + u0 - nu, rz + v0 - nv)], 'y', y, y + 0.05)
    L = 25.0                                               # the text's left edge, clear of the left screw
    prn.append(text('EARF', L, 13.2, size=4.2, bold=True))
    prn.append(text('ATMOSPHERE  ·  HORN LOUDSPEAKER, ACTIVE', L, 7.4))
    prn.append(text('MODEL AT-1        S/N  AT1-26-000127', L, 4.1))
    prn.append(text('100-120V~ / 200-240V~    50-60 Hz    350 W MAX', L, 0.8))
    prn.append(text('DESIGNED IN SAN FRANCISCO, CALIFORNIA', L, -2.5))
    prn.append(bar(L, -5.6, -25.0, -5.6, 0.25))
    prn.append(text('CE', L, -11.4, size=4.0))
    prn.append(text('UKCA', L - 9.0, -11.4, size=3.0, bold=True))
    prn.append(text('FCC', L - 21.0, -11.4, size=3.4, bold=True))
    u0, v0 = -10.6, -11.2                                  # the WEEE bin: its body, lid and wheel, crossed out, a bar under
    prn += [bar(u0 + 1.8, v0 + 2.2, u0 + 1.4, v0 - 2.4), bar(u0 - 1.8, v0 + 2.2, u0 - 1.4, v0 - 2.4), bar(u0 + 1.4, v0 - 2.4, u0 - 1.4, v0 - 2.4),
            bar(u0 + 2.3, v0 + 2.3, u0 - 2.3, v0 + 2.3), bar(u0 + 0.6, v0 + 2.9, u0 - 0.6, v0 + 2.9),
            bar(u0 + 2.7, v0 + 3.3, u0 - 2.7, v0 - 3.3), bar(u0 - 2.7, v0 + 3.3, u0 + 2.7, v0 - 3.3), bar(u0 + 2.4, v0 - 4.4, u0 - 2.4, v0 - 4.4, 0.8)]
    plate = box(rx - 35.0, D, rz - 20.0, rx + 35.0, y, rz + 20.0)
    heads = [cyl('y', (rx + u, rz), 5.6, y, y + 1.6) for u in (31.0, -31.0)]
    for u in (31.0, -31.0):
        plate -= cyl('y', (rx + u, rz), 3.2, D - 1, y + 1)
    C = lambda xs: Compound(children=xs)
    return {'plate': (plate, 'amp'), 'print': (C(prn), 'print'), 'screws': (C(heads), 'screw')}


def amp_plate_pieces(amp, cx, D, az):
    """The FA122's plate as it is (round 31: Hypex's drawing and photographs, read once hypex.nl could be reached; round
    30 had placed the connectors provisionally, the XLRs mirrored), for the render only: the part's solid stays the
    plain plate and module, for the drawings and the checks. The black anodised plate, 120 x 315 x 3, R3 corners, ten
    4.5 holes 5 in from its edges (110 apart across; 77.5, 75, 75, 77.5 down), each with its pan head into the back.
    From the top: five vent slots; the XLRs in two rows, the analogue in (a socket, its PUSH latch above) and its link
    out, the AES in and its link out below them turned half round (the latch below); beside them the RCAs in a column
    (the unbalanced left and right in, the S/PDIF in and out), the mini-USB and the Toslink, and the four status lights
    and the Select button with their labels on the slant; the grey label strips between the rows; Ncore's mark; the
    screws that hold the module; Hypex's name and FA122; the safety marks and the caution; the rating sticker and a
    blank field; five more vent slots; and the mains entry, the IEC C14 inlet turned on its side beside its rocker, the
    ratings under it. Every place is measured off Hypex's photograph of the plate square on (3.25 px a mm, its outline
    and holes agreeing with the drawing to 0.3), as (u, v) from the plate's middle: u = 60 - x and v = 157.5 - y, x and
    y in from its top left as one faces it (so +u is to one's left: the plate faces the back, +y). Returns {piece:
    (solid, finish)}."""
    from build123d import Align, Compound, Plane, Text, extrude
    FONT, BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    at = lambda u, v: (cx + u, az + v)
    rr = lambda w, h, r, u, v: rounded_rect(w, h, r, cx=cx + u, cy=az + v)
    slab = lambda outline, y0, y1: prism(outline, 'y', y0, y1)
    hole = lambda u, v, d, y0, y1: cyl('y', at(u, v), d, y0, y1)
    face = lambda y: Plane(origin=(0, y, 0), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))

    def text(s, u, v, w=None, size=2.4, rot=0.0, bold=False, y0=D, h=0.05, align=(Align.CENTER, Align.CENTER)):
        """Print on the plate's face, read from behind: centred on (u, v) unless `align` says otherwise, `w` wide (the
        size fitted to it) or `size` mm tall, turned `rot` degrees as one reads it."""
        fp = BOLD if bold else FONT
        if w:
            probe = Text(s, font_size=10.0, font_path=fp)
            size = 10.0 * w / probe.bounding_box().size.X
        sk = Text(s, font_size=size, font_path=fp, align=align, rotation=rot)
        pl = Plane(origin=(cx + u, y0, az + v), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
        return extrude(pl * sk, amount=h)

    def line(points, wd, y0=D, h=0.05):
        """A printed stroke `wd` wide through [(u, v), ...]."""
        out = []
        for (u0, v0), (u1, v1) in zip(points, points[1:]):
            L = math.hypot(u1 - u0, v1 - v0); nu, nv = -(v1 - v0) / L * wd / 2, (u1 - u0) / L * wd / 2
            out.append(slab([(cx + u0 + nu, az + v0 + nv), (cx + u1 + nu, az + v1 + nv),
                             (cx + u1 - nu, az + v1 - nv), (cx + u0 - nu, az + v0 - nv)], y0, y0 + h))
        return out

    def ring(u, v, d, wd, y0=D, h=0.05):
        return hole(u, v, d, y0, y0 + h) - hole(u, v, d - 2 * wd, y0 - 1, y0 + h + 1)

    def frame(w, ht, r, u, v, wd, y0=D, h=0.05):
        return slab(rr(w, ht, r, u, v), y0, y0 + h) - slab(rr(w - 2 * wd, ht - 2 * wd, max(r - wd, 0.2), u, v), y0 - 1, y0 + h + 1)

    pw, ph = amp['plate_w'], amp['plate_h']            # 120 x 315
    XLR = [(32.9, 121.15, 'f', 0), (9.8, 121.15, 'm', 0), (32.9, 85.75, 'f', 180), (9.8, 85.75, 'm', 180)]
    RCA = [(-13.85, 128.4, 'rca-white'), (-13.85, 115.8, 'rca-red'), (-13.85, 91.7, 'rca-orange'), (-13.85, 77.5, 'rca-orange')]
    USB, OPT, SELECT = (-26.5, 110.8), (-28.8, 92.5), (-41.9, 112.0)
    LEDS = [(-34.2, 126.5, 'led-red'), (-34.2, 121.5, 'led-on'), (-34.2, 116.2, 'led-green'), (-34.2, 111.2, 'led-green')]
    VENTS = [(u, v) for v in (139.9, -109.1) for u in (35.4, 17.7, 0.0, -17.7, -35.4)]
    MOUNT = [(u, v) for u in (55.0, -55.0) for v in (152.5, 75.0, 0.0, -75.0, -152.5)]
    TORX = [(-22.7, 121.9), (-4.6, 85.2), (-28.8, 82.1), (39.3, 62.2), (-39.0, 62.2), (-17.0, 31.7), (39.3, 0.2), (-39.0, 1.1),
            (3.2, -32.5), (-39.0, -40.0), (39.3, -45.1), (39.2, -100.9), (-39.2, -100.9), (17.7, -129.2)]
    PEM, C14, ROCKER = (-22.9, -129.2), (-13.85, -128.9), (-32.9, -129.55)

    # the plate, its holes and slots
    plate = slab(rr(pw, ph, 3.0, 0, 0), D - 3.0, D)
    for u, v in MOUNT:
        plate -= hole(u, v, 4.5, D - 4, D + 1)
    for u, v in VENTS:
        plate -= slab(rr(16.2, 3.8, 1.9, u, v), D - 4, D + 1)
    for u, v, _, _ in XLR:
        plate -= hole(u, v, 22.0, D - 4, D + 1)
    for u, v, _ in RCA:
        plate -= hole(u, v, 10.0, D - 4, D + 1)
    for (w, h), (u, v) in (((9.6, 8.8), OPT), ((7.2, 3.8), USB), ((41.2, 29.8), PEM)):
        plate -= slab(rr(w, h, 0.8, u, v), D - 4, D + 1)
    for u, v, _ in LEDS:
        plate -= hole(u, v, 3.2, D - 4, D + 1)
    plate -= hole(*SELECT, 4.4, D - 4, D + 1)
    module = box(cx - amp['cutout_w'] / 2 + 4, D - amp['depth'], az - amp['cutout_h'] / 2 + 6,
                 cx + amp['cutout_w'] / 2 - 4, D - 3.0, az + amp['cutout_h'] / 2 - 6)
    # behind every opening a pocket in the module, so a connector's insert and pins show and a slot reads dark and deep
    for u, v, _, _ in XLR:
        module -= hole(u, v, 22.6, D - 16, D - 2.9)
    for u, v, _ in RCA:
        module -= hole(u, v, 10.6, D - 8, D - 2.9)
    for u, v in VENTS:
        module -= slab(rr(16.2, 3.8, 1.9, u, v), D - 9, D - 2.9)
    for (w, h), (u, v) in (((9.8, 9.0), OPT), ((7.4, 4.0), USB), ((39.2, 28.0), PEM)):
        module -= slab(rr(w, h, 0.8, u, v), D - 24, D - 2.9)

    P = {k: [] for k in ('black', 'metal', 'ring', 'gold', 'screws', 'print', 'label', 'ink', 'foil', 'led-on', 'led-green', 'led-red',
                         'rca-white', 'rca-red', 'rca-orange')}

    def pan(u, v, d, y0, recess='cross'):
        """A screw head: a dome-ish pan `d` across standing on y0, its recess cut."""
        s = hole(u, v, d, y0, y0 + d * 0.22).fuse(hole(u, v, d * 0.8, y0 + d * 0.22, y0 + d * 0.32))
        top = y0 + d * 0.32
        if recess == 'cross':
            for a, b in ((d * 0.28, 0.45), (0.45, d * 0.28)):
                s -= box(cx + u - a, top - 0.7, az + v - b, cx + u + a, top + 0.1, az + v + b)
        else:                                          # a six-lobed socket, drawn as a small hexagon
            hx = [(cx + u + d * 0.2 * math.cos(math.radians(60 * k)), az + v + d * 0.2 * math.sin(math.radians(60 * k))) for k in range(6)]
            s -= slab(hx, top - 0.9, top + 0.1)
        return s

    for u, v in MOUNT:                                 # the plate's ten into the back, M4 pan heads
        P['screws'].append(pan(u, v, 7.6, D))
    for u, v in TORX:                                  # the module's, each in a ring of bare metal where it was turned home
        P['screws'].append(pan(u, v, 5.6, D, 'torx'))
        P['ring'].append(ring(u, v, 6.6, 0.45, D, 0.06))

    PINS = [(-4.8, 2.0), (4.8, 2.0), (0.0, -5.2)]      # an XLR's three, as one faces it, latch up
    for u, v, sex, turn in XLR:
        k = -1 if turn else 1                          # the lower row turned half round
        for su, sv in ((9.8, 9.95), (-9.8, -9.95)):    # two M3 heads on the diagonal, the same corners for all four
            P['screws'].append(pan(u + su, v + sv, 5.0, D, 'torx'))
        P['metal'].append(ring(u, v, 22.6, 0.9, D, 0.4))                      # the connector's bright front ring
        if sex == 'f':
            ins = hole(u, v, 21.8, D - 6, D - 1.6)
            for pu, pv in PINS:
                ins -= hole(u + pu, v + k * pv, 3.4, D - 5, D - 1.5)
                P['metal'].append(hole(u + pu, v + k * pv, 2.2, D - 5.4, D - 4.6))   # the contact inside each hole
            ins -= box(cx + u - 1.6, D - 5, az + v + k * 7.4 - 1.2, cx + u + 1.6, D - 1.5, az + v + k * 7.4 + 1.2)  # the key
            P['black'].append(ins)
            lu, lv = u - 0.2, v + k * 13.35                                    # the PUSH latch, a bright tab in a black boss
            P['black'].append(slab(rr(10.0, 6.4, 2.6, lu, lv), D, D + 1.2))
            P['metal'].append(slab(rr(7.6, 4.2, 1.6, lu, lv), D + 1.2, D + 1.9))
            P['ink'].append(text('PUSH', lu, lv - k * 0.3, w=5.6, rot=0 if k > 0 else 180, bold=True, y0=D + 1.9, h=0.08))
        else:
            P['metal'].append(hole(u, v, 21.0, D - 10, D + 0.6) - hole(u, v, 19.0, D - 11, D + 0.7))   # the shell's mouth
            P['metal'].append(box(cx + u - 1.4, D - 9, az + v + k * 9.0 - 0.6, cx + u + 1.4, D + 0.4, az + v + k * 9.0 + 0.9 * k))
            P['black'].append(hole(u, v, 19.0, D - 12, D - 10))
            for pu, pv in PINS:
                P['gold'].append(hole(u + pu, v + k * pv, 1.6, D - 10, D - 3.0))
    hexagon = lambda u, v, af: [(cx + u + af / math.sqrt(3) * math.cos(math.radians(30 + 60 * j)),
                                 az + v + af / math.sqrt(3) * math.sin(math.radians(30 + 60 * j))) for j in range(6)]
    for u, v, col in RCA:                              # nickel nuts and barrels, the insulator's colour at the mouth, gold inside
        P['metal'].append(slab(hexagon(u, v, 10.4), D, D + 1.6) - hole(u, v, 8.2, D - 1, D + 2))
        P['metal'].append(hole(u, v, 8.4, D - 2, D + 7.5) - hole(u, v, 6.8, D - 3, D + 7.6))
        P[col].append(hole(u, v, 6.7, D - 2, D + 7.2) - hole(u, v, 3.6, D + 3.5, D + 7.3))
        P['gold'].append(hole(u, v, 3.4, D + 3.8, D + 6.9) - hole(u, v, 1.9, D + 3.7, D + 7.0))
    u, v = OPT                                         # Toslink: a square housing, its keyed mouth and shutter
    P['black'].append(slab(rr(9.4, 8.6, 0.6, u, v), D - 6, D + 0.6)
                      - slab([(cx + u + 2.6, az + v + 2.2), (cx + u - 2.6, az + v + 2.2), (cx + u - 2.6, az + v - 1.0),
                              (cx + u - 1.6, az + v - 2.2), (cx + u + 1.6, az + v - 2.2), (cx + u + 2.6, az + v - 1.0)], D - 3, D + 0.7))
    P['black'].append(slab(rr(5.0, 4.2, 0.5, u, v), D - 3.4, D - 3.0))
    u, v = USB                                         # mini-B: its shell set back, the tongue in it
    trap = lambda w, h: [(cx + u + w / 2, az + v + h / 2), (cx + u - w / 2, az + v + h / 2),
                         (cx + u - w / 2 + 0.9, az + v - h / 2), (cx + u + w / 2 - 0.9, az + v - h / 2)]
    P['metal'].append(slab(trap(7.0, 3.6), D - 7, D - 0.6) - slab(trap(6.2, 2.9), D - 6, D - 0.5))
    P['black'].append(box(cx + u - 2.3, D - 6, az + v - 0.1, cx + u + 2.3, D - 2.2, az + v + 0.7))
    P['black'].append(slab(rr(7.2, 3.8, 0.6, u, v), D - 8, D - 7))
    for u, v, fin in LEDS:                             # 3 mm lenses: Prot red, P1 lit, P2 and P3 green and dark
        P[fin].append(hole(u, v, 3.0, D - 2, D + 0.4).fuse(cyl('y', at(u, v), 2.4, D + 0.4, D + 0.8)))
    P['black'].append(hole(*SELECT, 4.2, D - 3, D + 0.9))                    # the Select button
    u, v = PEM                                         # the mains entry: a bezel, the C14 inlet on its side, the rocker
    P['black'].append(slab(rr(41.2, 29.8, 2.4, u, v), D, D + 2.4).fuse(slab(rr(39.0, 27.6, 2.0, u, v), D - 22, D))
                      - slab(rr(18.6, 26.8, 1.2, C14[0], C14[1]), D - 1, D + 2.5)
                      - slab(rr(16.6, 22.6, 1.0, ROCKER[0], ROCKER[1]), D + 0.6, D + 2.5))
    cu, cv = C14
    mouth = [(cx + cu - 8.25, az + cv - 12.45), (cx + cu + 4.25, az + cv - 12.45), (cx + cu + 8.25, az + cv - 8.45),
             (cx + cu + 8.25, az + cv + 8.45), (cx + cu + 4.25, az + cv + 12.45), (cx + cu - 8.25, az + cv + 12.45)]
    P['black'].append(slab(rr(18.6, 26.8, 1.2, cu, cv), D - 9, D + 1.0) - slab(mouth, D - 8, D + 1.1))
    for (bu, bv), (w, h) in (((-1.15, 7.0), (4.0, 2.0)), ((-1.15, -7.0), (4.0, 2.0)), ((5.35, 0.0), (2.0, 4.0))):
        P['metal'].append(box(cx + cu + bu - w / 2, D - 8, az + cv + bv - h / 2, cx + cu + bu + w / 2, D - 1.2, az + cv + bv + h / 2))
    ru, rv = ROCKER                                    # the rocker in its bezel, rocked to I (its lower half proud)
    P['black'].append(slab(rr(15.0, 20.9, 1.2, ru, rv), D + 0.6, D + 2.4) - slab(rr(11.4, 15.1, 0.8, ru, rv), D, D + 2.5))
    P['black'].append(prism([(D + 0.8, az + rv + 7.15), (D + 1.6, az + rv + 7.15), (D + 3.8, az + rv - 7.15), (D + 0.8, az + rv - 7.15)],
                            'x', cx + ru - 5.3, cx + ru + 5.3))
    P['print'].append(box(cx + ru - 0.35, D + 1.9, az + rv + 2.6, cx + ru + 0.35, D + 2.45, az + rv + 5.0))       # I
    P['print'].append(cyl('y', at(ru, rv - 3.6), 2.6, D + 3.2, D + 3.62) - cyl('y', at(ru, rv - 3.6), 1.6, D + 3.1, D + 3.7))  # O

    # the grey strips and their words, the white print
    for (u, w), (v, ht), word in [((34.6, 25.4), (105.65, 3.5), 'analogue in'), ((9.45, 21.3), (105.65, 3.5), 'through'),
                                  ((-13.85, 13.1), (105.65, 3.5), 'unbal'), ((-27.3, 10.0), (105.65, 3.5), None),
                                  ((34.6, 25.4), (100.9, 3.8), 'AES in'), ((9.45, 21.3), (100.9, 3.8), 'through'),
                                  ((-13.85, 13.1), (100.9, 3.8), 'S/PDIF'), ((-28.95, 12.9), (100.9, 3.8), 'optical')]:
        P['label'].append(slab(rr(w, ht, 0.8, u, v), D, D + 0.05))
        if word:
            P['ink'].append(text(word, u, v, size=2.6, y0=D + 0.05, h=0.05))
    u, v = -27.3, 105.65                               # the USB trident
    P['ink'] += line([(u + 3.0, v), (u - 2.6, v)], 0.45, D + 0.05)
    P['ink'] += line([(u + 1.2, v), (u + 0.2, v + 1.0), (u - 1.0, v + 1.0)], 0.4, D + 0.05)
    P['ink'] += line([(u + 0.6, v), (u - 0.4, v - 0.9), (u - 1.4, v - 0.9)], 0.4, D + 0.05)
    P['ink'].append(hole(u + 3.1, v, 1.2, D + 0.05, D + 0.1))
    P['ink'].append(slab([(cx + u - 2.6, az + v + 0.8), (cx + u - 3.6, az + v), (cx + u - 2.6, az + v - 0.8)], D + 0.05, D + 0.1))
    for (u, v), word, rot in (((-16.7, 135.2), 'left', -30), ((-18.0, 120.8), 'right', -45),
                              ((-18.3, 86.7), 'input', 45), ((-17.7, 73.0), 'output', 45)):
        P['print'].append(text(word, u, v, size=2.2, rot=rot))
    for (u, v, _), word in zip(LEDS + [(SELECT[0], SELECT[1], None)], ('Prot', 'P1 / Left', 'P2 / Right', 'P3 / L+R', 'Select')):
        a = math.radians(52)
        P['print'] += line([(u - 1.9, v + 0.4), (u - 1.9 - 3.4 * math.cos(a), v + 0.4 + 3.4 * math.sin(a))], 0.3)
        P['print'].append(text(word, u - 1.9 - 3.9 * math.cos(a), v + 0.4 + 3.9 * math.sin(a), size=2.1, rot=52,
                               align=(Align.MIN, Align.CENTER)))
    P['print'].append(cyl('y', at(-28.15, 74.2), 5.6, D, D + 0.05))          # Ncore's mark: an N in a disc, then core
    P['ink'].append(text('N', -28.15, 74.2, size=3.4, bold=True, y0=D + 0.05))
    P['print'].append(text('core', -39.6, 74.6, w=16.0))
    P['print'].append(text('audio power conversion', -37.2, 70.3, w=22.0))
    # Hypex's wave and name, and FA122 (1, 2, 2 in white discs)
    for j in range(7):
        pts = []
        for i in range(41):
            t = i / 40
            pts.append((13.9 - 28.7 * t, 21.2 + (1.5 + 5.5 * t ** 2.2) * math.sin(2 * math.pi * (1.6 * t + 0.07 * j)) + (j - 3) * 0.35 * t))
        P['print'] += line(pts, 0.28)
    P['print'].append(text('hypex', 9.8, 12.2, w=25.4))
    P['print'].append(text('electronics', -13.45, 10.9, w=18.9))
    P['print'].append(text('www.hypex.nl', -11.5, 7.9, w=13.8, bold=True))
    P['print'].append(text('FA', 15.9, -17.6, w=13.4, bold=True))
    for u, dg in ((3.3, '1'), (-7.4, '2'), (-18.1, '2')):
        P['print'].append(cyl('y', at(u, -17.6), 9.5, D, D + 0.05))
        P['ink'].append(text(dg, u, -17.6, size=6.4, bold=True, y0=D + 0.05))
    # the safety marks (outlines), the caution, the sticker and its blank twin, the ratings
    u0, v0 = 25.3, -78.2
    P['print'].append(ring(u0, v0, 6.6, 0.45))
    P['print'] += line([(u0 + 2.0, v0 - 1.2), (u0 + 0.8, v0 + 1.4), (u0, v0 - 0.2), (u0 - 0.9, v0 + 1.5), (u0 - 2.2, v0 - 1.2)], 0.4)
    for u0 in (15.0, 4.8):
        tri = [(u0 + 3.4, v0 - 2.9), (u0 - 3.4, v0 - 2.9), (u0, v0 + 3.1), (u0 + 3.4, v0 - 2.9)]
        P['print'] += line(tri, 0.5)
    P['print'] += line([(15.0, -79.9), (15.0, -77.0)], 0.6); P['print'].append(hole(15.0, -80.9, 0.7, D, D + 0.05))
    P['print'] += line([(5.4, -76.6), (4.2, -78.6), (5.6, -78.4), (4.4, -80.6)], 0.45)
    u0 = -5.3
    P['print'].append(frame(4.6, 5.4, 0.4, u0, v0 + 0.6, 0.45)); P['print'] += line([(u0 + 3.2, v0 + 3.6), (u0 - 3.2, v0 - 2.6)], 0.45)
    P['print'] += line([(u0 - 3.2, v0 + 3.6), (u0 + 3.2, v0 - 2.6)], 0.45); P['print'].append(slab(rr(5.0, 0.8, 0.1, u0, v0 - 3.4), D, D + 0.05))
    P['print'].append(text('CE', -15.6, -78.2, w=6.4))
    P['print'].append(frame(6.2, 5.6, 0.4, -25.9, -78.2, 0.45)); P['print'] += line([(-25.9, -75.6), (-25.9, -80.8)], 0.45)
    P['print'].append(text('CAUTION - RISK OF ELECTRIC SHOCK - DO NOT OPEN', -0.7, -85.3, w=58.6, bold=True))
    P['print'].append(text('PRECAUTION - RISQUE DE CHOC ÉLECTRIQUE - NE PAS OUVRIR', -0.8, -88.0, w=70.0, bold=True))
    P['foil'].append(slab(rr(28.0, 13.8, 0.8, 15.2, -98.6), D, D + 0.12))
    for j in range(5):                                 # the sticker's QR square and its lines, in ink
        for i in range(5):
            if (i * 7 + j * 3) % 5 < 3 or i in (0, 4) and j in (0, 4):
                P['ink'].append(box(cx + 28.4 - i * 1.4, D + 0.12, az - 101.0 + j * 1.4, cx + 27.2 - i * 1.4, D + 0.17, az - 99.8 + j * 1.4))
    for j, wd in enumerate((17.0, 14.0, 9.0, 18.0, 11.0)):
        P['ink'].append(box(cx + 20.5, D + 0.12, az - 93.6 - j * 2.0, cx + 20.5 - wd, D + 0.17, az - 94.4 - j * 2.0))
    P['print'].append(frame(28.2, 14.1, 1.4, -16.8, -98.55, 0.5))
    P['print'].append(text('100 - 120V~ / 200 - 240V~', -21.0, -149.1, w=35.0))
    P['print'].append(text('350W Max. / 50Hz - 60Hz', -20.9, -152.3, w=31.2))

    C = lambda xs: Compound(children=xs)
    out = {'plate': (plate, 'amp'), 'module': (module, 'amp'), 'housings': (C(P['black']), 'gland'),
           'metal': (C(P['metal']), 'rod'), 'gold': (C(P['gold']), 'brass'), 'screws': (C(P['screws']), 'screw'),
           'print': (C(P['print']), 'print'), 'labels': (C(P['label']), 'amp-label'), 'ink': (C(P['ink']), 'amp'),
           'sticker': (C(P['foil']), 'amp-foil'), 'rings': (C(P['ring']), 'amp-ring')}
    for k in ('led-on', 'led-green', 'led-red', 'rca-white', 'rca-red', 'rca-orange'):
        if P[k]:
            out[k] = (C(P[k]), k)
    return out


def amp_compartment(P, ribs, wz, wood):
    """Round 13 (the reality check's r2, r5, r8 and r12). The amplifier in a sealed compartment of its own, as Hypex
    asks, so the box stays airtight and the mains electronics are enclosed in metal: a pan of 1.5 mm aluminium round the
    module, its flange screwed to the back's inner face on an EPDM gasket. Inside it the L-pad's two resistors on a
    3 mm aluminium plate and the HF driver's capacitor. The leads leave through two cable glands in its front: the HF
    lead up the back rib (the back's batts, without ribs) and through brace-2's window to a gland under the top at the
    cable post; the woofer's lead to the woofer's terminals. A rating plate outside, beside the amplifier."""
    from build123d import Compound
    W, D, H, T = P['W'], P['D'], P['H'], P['T']
    cx, az, yb = W / 2, P['amp_z'], P['inset']
    amp = LIB[P['amp']]['geom']
    ab = P['amp_box']; tb, (iw, idp, ih), fl, (gd, gl) = ab['t'], ab['inside'], ab['flange'], ab['gland']
    yi = D - T; yf = yi - ab['gasket']; yfr = yi - idp       # the back's inner face, the flange's back, the pan's inside front
    hole = lambda ya, yb_: box(cx - iw / 2, ya, az - ih / 2, cx + iw / 2, yb_, az + ih / 2)
    pan = box(cx - iw / 2 - tb, yfr - tb, az - ih / 2 - tb, cx + iw / 2 + tb, yf, az + ih / 2 + tb) - hole(yfr, yf + 1)
    rim = box(cx - iw / 2 - tb - fl, yf - tb, az - ih / 2 - tb - fl, cx + iw / 2 + tb + fl, yf, az + ih / 2 + tb + fl) - hole(yf - tb - 1, yf + 1)
    seal = box(cx - iw / 2 - tb - fl, yf, az - ih / 2 - tb - fl, cx + iw / 2 + tb + fl, yi, az + ih / 2 + tb + fl) - hole(yf - 1, yi + 1)
    pad = box(cx - 50, yfr, az - 70, cx + 50, yfr + 3, az + 70)     # the plate on the pan's front, inside
    for dx in (-25, 25):                                            # two aluminium-housed resistors
        pad = pad.fuse(box(cx + dx - 15, yfr + 3, az - 62, cx + dx + 15, yfr + 18, az - 32))
    pad = pad.fuse(cyl('x', (yfr + 3 + 17.5, az + 35), 35.0, cx - 29, cx + 29))   # the capacitor
    g_hf, g_lf = (cx - 30, az + ih / 2 - 30), (cx + 30, az - ih / 2 + 30)
    glands = [cyl('y', g, gd, yfr - tb - gl, yfr - tb) for g in (g_hf, g_lf)]
    tip = lambda g: (g[0], yfr - tb - gl, g[1])
    blank = (iw + 2 * idp + 2 * fl, ih + 2 * idp + 2 * fl, tb)     # the sheet it is folded from
    out = [Part('amp-box', pan.fuse(rim), Machined('aluminium', 'sheet metal', stock=blank, setup_usd=150.0), finish='amp', inside=True,
                notes=[f'{iw:g} x {ih:g} inside, {idp:g} deep from the back: {tb:g} aluminium folded, its corners welded, black '
                       f'anodised; a {fl:g} flange round its open side, on a {ab["gasket"]:g} EPDM gasket on the back\'s inner face, '
                       'ten screws through it, so the box stays airtight and the mains electronics are enclosed in metal; two M12 '
                       'cable glands in its front; the ports\' length found with it fitted (it takes volume)']),
           Part('amp-box-gasket', seal, Bought('epdm-gasket'), finish='sleeve', inside=True),
           Part('hf-pad', pad, Bought('attenuator-l-pad'), finish='amp', inside=True, render=False,
                notes=['on a 3 mm aluminium plate screwed to the compartment\'s front, inside, with thermal compound under the '
                       'resistors; the capacitor beside them; crimped, insulated 6.3 mm receptacles'])]
    # the leads (round 14: they stay in the cabinet when the back comes off, each unplugged at its connector at the
    # compartment): the HF lead straight up from its gland, through brace-2's window, in under the top's batts to its
    # gland at the cable post; the woofer's under the motor to the basket's lower spoke
    Lc = P['lining']
    top_glands = []
    if P['horn']['form'] == 'cast':
        pp = P['horn']['cast']['posts']; gx, gy = rod_places(P)[pp['cable_post']]
        pad = top_boss(P); zg = pad[4] if pad else H - T          # the gland screws into the top, or the pad under it
        top_glands = [cyl('z', (gx, gy), gd, zg - gl, zg)]
        t0 = tip(g_hf); zt = H - T - Lc.get('t_top', Lc['t']) - Lc['gap']     # the top's batts' underside
        hf_path = [t0, (t0[0], t0[1] - 7, t0[2] + 4), (t0[0] - 4, t0[1] - 2, t0[2] + 22), (gx, t0[1] + 9.5, zt - 20),
                   (gx, gy - 13, zt - 6), (gx, gy, min(zt + 8, zg - gl - 6)), (gx, gy, zg - gl)]
        out.append(Part('lead-hf', tube_along(hf_path, 5.0), Bought('hf-pair'), finish='cable', inside=True,
                        notes=['from its connector at the compartment\'s upper gland straight up'
                               + (', through brace-2\'s window (on a screw-mount tie base on its back member)' if len(P['braces']) > 1 else '')
                               + ', through the gland under the top and up the cable post (7 bore) into the pod; it stays in the '
                               'cabinet when the back comes off; a 50 service loop at each end; silicone sleeving where it meets the '
                               'post\'s cut ends']))
    t1, end = tip(g_lf), (cx + 5.0, yb + 68.0, wz - 122.0)
    lerp = lambda f, dz: tuple(a + (b - a) * f for a, b in zip(t1, end))[:2] + (t1[2] + (end[2] - t1[2]) * f + dz,)
    out.append(Part('lead-woofer', tube_along([t1, lerp(0.3, -12.0), lerp(0.65, -8.0), end], 7.0), Bought('speaker-cable-1m'),
                    finish='cable', inside=True, notes=['from its connector at the compartment\'s lower gland to the woofer\'s terminals, under the '
                                                        'motor, tied to the basket\'s lower spoke, clear of the cone\'s travel']))
    out.append(Part('cable-glands', Compound(children=glands + top_glands), Bought('cable-glands'), finish='gland', inside=True))
    pw = amp['plate_w'] / 2
    out.append(Part('rating-plate', box(cx + pw + 20, D, az + 60, cx + pw + 90, D + 1.0, az + 100), Bought('rating-plate'), finish='amp',
                    pieces=rating_plate_pieces(cx, D, az, pw),
                    notes=['beside the amplifier, 70 x 40: the model, the serial number, the ratings, the marks (CE, UKCA, FCC, the '
                           'WEEE bin) and the maker\'s address, laser-marked; two M3 screws into inserts']))
    return out


def fittings(P, places, shell):
    """Round 13 (the reality check's r1 and r3). Each post's foot stands in a polyurethane sleeve in a brass socket, the
    socket knurled and pressed into the top (no bond to HDPE): the sleeve takes up the castings' scatter and stops the
    post buzzing. An M6 rod down the free rear post, from a thumb nut on a washer inside the pod to a flanged insert
    under the top, holds the horn down; with the cap off and the nut undone, the horn and its posts still lift off."""
    from build123d import Axis, Compound
    H, T = P['H'], P['T']
    pp = P['horn']['cast']['posts']; (sd, sdep), sb, (so, si, sl) = pp['socket'], pp['socket_bore'], pp['sleeve']
    cups, sleeves = [], []
    for i, (rx, ry) in enumerate(places):
        cup = cyl('z', (rx, ry), sd, H - sdep, H) - cyl('z', (rx, ry), sb, H - sdep + 2.0, H + 1)
        if i in (pp['cable_post'], pp['tie_post']):
            cup -= cyl('z', (rx, ry), pp['bore'] if i == pp['cable_post'] else pp['tie']['hole'], H - sdep - 1, H)
        cups.append(cup)
        sleeves.append(cyl('z', (rx, ry), so, H - sl, H) - cyl('z', (rx, ry), si, H - sl - 1, H + 1))
    tx, ty = places[pp['tie_post']]
    d, (bi, bl, fd, ft) = pp['tie']['d'], pp['tie']['insert']
    floor = []                                      # the pod's floor inside, round the washer: it sits on the highest
    for k in range(8):
        a = 2 * math.pi * k / 8
        hits = sorted(h[0].Z for h in shell.find_intersection_points(Axis((tx + 8.5 * math.cos(a), ty + 8.5 * math.sin(a), H + 1.0), (0, 0, 1)))
                      if h[0].Z > H + 1.0)
        if len(hits) > 1:
            floor.append(hits[1])
    zf = max(floor) + 0.3
    kind, tb = shell_kind(P), top_boss(P)
    zi = tb[4] if tb else H - T                      # a flanged insert in the top's underside, or (round 15) in the pad under it
    z0 = zi + 1.0
    insert = (cyl('z', (tx, ty), bi, zi, zi + bl) + cyl('z', (tx, ty), fd, zi - ft, zi)) - cyl('z', (tx, ty), d, zi - ft - 1, zi + bl + 1)
    anchor = (f'a flanged M6 insert {"bonded into" if kind == "acrylic" else "for wood in" if kind == "wood" else "for plastics in"} '
              + ('the pad under the top' if tb else 'the top\'s underside'))
    rod = cyl('z', (tx, ty), d, z0, zf + 14.0)
    nut = (cyl('z', (tx, ty), 16.0, zf, zf + 1.6) + cyl('z', (tx, ty), 16.0, zf + 1.6, zf + 9.6)) - cyl('z', (tx, ty), d, zf - 1, zf + 11)
    tie = rod.fuse(nut)
    return [Part('post-sockets', Compound(children=cups), Bought('post-fixings'), finish='brass', group='cabinet',
                 notes=[f'{len(places)} brass cups, ' + ('bonded with epoxy into' if shell_kind(P) == 'acrylic' else 'knurled to 15 and pressed into')
                        + f' {sd:g} holes {sdep:g} deep in the top, bored {sb:g} '
                        '13 deep on a 2 floor; the cable post\'s floor holed 7 for the HF lead, the tie post\'s 6.5 for the rod']),
            Part('post-sleeves', Compound(children=sleeves), Bought('post-sleeves'), finish='sleeve', group='cabinet',
                 notes=[f'polyurethane, Shore A 90, {so:g} x {si:g} x {sl:g}, pressed into the sockets: they centre the posts, take up '
                        'about 0.3 of the castings\' scatter and stop them buzzing']),
            Part('tie-rod', Compound(children=[tie, insert]), Bought('tie-rod-set'), group='horn', inside=True,
                 pieces={'rod': (tie, 'rod'), 'insert': (insert, 'brass')},
                 notes=[f'M6 A2, {zf + 14.0 - z0:.0f} long, down the free rear post from a knurled thumb nut on a washer inside the pod '
                        f'(on a flat cast in its floor) to {anchor}, fitted before the top goes on; undone by hand with the cap off'])]

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
        pads = [dict(x=rx - cx, z=depth - ry, d=pp['pad_d'], h=pp['pad_h'], bore=pp['insert_d'], bore_depth=insert_depth(pp, ry, depth),
                     cable=(pp['bore'] if i in (pp['cable_post'], pp['tie_post']) else 0.0)) for i, (rx, ry) in enumerate(rod_places(P))]
        shell, cap = waveguide_shell(c['mouth_w'], c['mouth_h'], depth, r0=c['r0'], wall=c['wall'], rim=c['rim'], n_mouth=c['n_mouth'],
                                     pod_r=c['pod_r'], pod_back=c['pod_back'], dome=c['dome'], boss=c['boss'],
                                     round_rim=c['round_rim'], pads=pads, cap_hole=False, solid_neck=c['solid_neck'],
                                     tub=c['tub'] if c['back'] == 'tub' else None)
        outside = (f'the outside a tub running straight back from the rim to a flat back {c["tub"]["back"]:g} behind the throat, hiding the '
                   f'driver, the flare its own {c["wall"]:g} skin inside it (the space between filled with damping foam); the back a lid, '
                   f'six M4 screws round its edge') if c['back'] == 'tub' else \
                  (f'a shell {c["wall"]:g} thick following its flare; the driver in a pod {2 * c["pod_r"]:g} across behind, closed by a cap')
        bb = shell.bounding_box()                 # outside, as built: the rounded rim draws in a little from mouth + rim
        notes = [f'mouth {c["mouth_w"]:g} x {c["mouth_h"]:g}, {depth:g} deep, {2 * c["r0"] / 25.4:g} in throat; a {c["rim"]:g} rim rounded right round, '
                 f'{bb.max.X - bb.min.X:.0f} x {2 * bb.max.Y:.0f} outside; {outside}; four pads under it take the posts\' '
                 f'brass inserts; cast in tinted clear resin in a two-part silicone mould from a CNC-cut plug, its faces polished '
                 f'satin (a slow deep-pour resin: the neck round the throat is solid, {shell.volume / 1e6:.1f} L in all), or '
                 f'pigmented the same way for the opaque and marbled finishes']
        ring = None
        if c.get('lock') and c['back'] == 'shell':
            shell, cap, ring = twist_lock(shell, cap, c['pod_r'], c['wall'], c['pod_back'], c['dome'], **c['lock'])
        zc = H + c['gap'] + half_h
        shell = place(shell, (cx, depth, zc), (0, -1, 0))
        cap = place(cap, (cx, depth, zc), (0, -1, 0))
        ring = place(ring, (cx, depth, zc), (0, -1, 0)) if ring is not None else None
        return dict(shell=shell, cap=cap, ring=ring, zc=zc, throat_y=depth, driver_y=depth + c['boss']['t'] + c['adaptor']['t'], notes=notes)
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
    return dict(shell=shell, cap=cap, zc=zc, throat_y=depth, driver_y=depth + hz['boss']['t'], notes=notes)


def adaptor_ring(P, wg, hf):
    """The 2 in driver's adaptor ring (the cast horn): aluminium, between the horn's boss and the driver. The driver screws
    to it first, from the front (countersunk M6 into the blind threads in its front plate, on its bolt circle); then the
    ring screws to brass inserts in the boss, M5 socket caps on the boss's circle, outside the driver's flange, at 45
    degrees to the driver's screws."""
    c = P['horn']['cast']; a, b = c['adaptor'], c['boss']
    cx, zc = P['W'] / 2, wg['zc']
    y0 = wg['throat_y'] + b['t']; y1 = y0 + a['t']
    ring = cyl('y', (cx, zc), a['od'], y0, y1) - cyl('y', (cx, zc), 2 * c['r0'], y0 - 1, y1 + 1)
    for k in range(hf['bolts']):
        t = 2 * math.pi * k / hf['bolts']
        x, z = cx + hf['bolt_d'] / 2 * math.cos(t), zc + hf['bolt_d'] / 2 * math.sin(t)
        ring -= cyl('y', (x, z), a['driver_holes'], y0 - 1, y1 + 1)
        ring -= cyl('y', (x, z), a['sink'], y0 - 1, y0 + 3.5)            # the countersinks, toward the boss
    for k in range(b['bolts']):
        t = 2 * math.pi * (k + 0.5) / b['bolts']
        ring -= cyl('y', (cx + b['bolt_d'] / 2 * math.cos(t), zc + b['bolt_d'] / 2 * math.sin(t)), a['screw_hole'], y0 - 1, y1 + 1)
    return Part('hf-adaptor', ring, Machined('aluminium', 'lathe'), finish='driver-frame', group='horn',
                notes=[f'{a["od"]:g} across, {a["t"]:g} thick, bored {2 * c["r0"]:g} (the throat); {hf["bolts"]} countersunk M6 on '
                       f'{hf["bolt_d"]:g} take the driver from the front; {b["bolts"]} x {a["screw_hole"]:g} on {b["bolt_d"]:g} (at 45 degrees '
                       'to them) take M5 socket caps into the brass inserts in the horn\'s boss; black anodised'])


def covers(P, wz):
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
    out += disc_and_face(P, wz, alt)
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


def disc_and_face(P, wz, alt):
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
        dframe -= cyl('y', (mx, mz), mg['pocket'], yr - mg['t'] - 0.2, yr + 1)
    ds = cv['disc_stock']
    fixed = 'pressed' if 'hdpe' in ds else 'bonded'   # round 13 (r3): HDPE holds no bond
    out.append(Part('disc-frame', dframe, Sheet(ds, dt), finish='black', option=disc_opt, render=False,
                    notes=[f'{"sprayed black" if ds == "mdf" else "cast acrylic, black" if "acrylic" in ds else "pressed black"}; its face edge rounded; {mg["n"]} magnets ({mg["d"]:g} x '
                           f'{mg["t"]:g}) {fixed} into the pockets behind it, each holding to a steel disc in the ring\'s back through '
                           f'{r["t"] - mg["t"] - 0.2:g} of {"MDF" if r["stock"] == "mdf" else "the ring"}']))
    # the cloth as it lies: flat across the face and rolled round the frame's rounded edge (a sharp-edged cylinder read as
    # a placeholder in round 31's duels)
    cloth = cyl('y', (cx, wz), r['od'] + 1.0, yr - dt - 0.5, yr)
    if cv.get('disc_edge_r'):
        cloth = cloth.fillet(cv['disc_edge_r'], [e for e in cloth.edges() if abs(e.center().Y - (yr - dt - 0.5)) < 0.01])
    out.append(Part('cloth-disc', cloth, Bought('grille-cloth'), finish='disc',
                    option=disc_opt, notes=[f'Ø{r["od"] + 1:g}: stretched across the frame\'s face and round its edge, '
                                                + ('glued behind' if 'hdpe' not in ds else 'held behind on an adhesive transfer tape made for '
                                                   'low-surface-energy plastics (3M 300LSE kind)')
                                                + f'; its face {yr - dt - 0.5:g} back from the shell\'s front']))
    out.append(Part('cloth-disc-magnets', None, Bought('grille-magnets'), option=disc_opt))

    # the facings: bark (1 mm; or cork, 3 mm, with the alternatives) laid on the panel round the ring and the port
    # before the ring goes on
    holes = [('circle', cx, wz, r['od'] + 1.0)] + [('rrect', px, pt['z'], pt['frame'] + 1.0, pt['frame'] + 1.0, pt['frame_r'] + 0.5)
                                                   for px in pt['x']]
    if P['finish'] == 'pressed':                      # the panel's own sheet carries the pattern: nothing laid on it
        faces = []
    elif P['finish'] == 'faced':
        faces = [('pressed', Sheet(P['skin']['stock'], P['skin']['face_t'], face='-y', grain='z'), 'bark')]
    else:
        faces = [('bark', Bought('bark-sheet'), 'bark')] + ([('cork', Sheet('cork', cv['face_t']['cork'], face='-y'), 'cork')] if alt else [])
    for name, make, fin in faces:
        ft = P['skin']['face_t'] if name == 'pressed' else cv['face_t'][name]
        face = slotted_panel(T + 0.5, T + 0.5, W - T - 0.5, H - T - 0.5, yb - ft, yb, holes=holes)
        out.append(Part(f'{name}-face', face, make, finish=fin, option=f'{name}-face' if alt else '',
                        notes=[f'{ft:g} thick, cut round the ring (Ø{r["od"] + 1:g}) and the ports\' frames; laminated to the panel before the ring goes on']))
    return out


# each bark's colours: a pale panel and an off-white ring on birch, as photographed; a sage-grey panel and a cream ring on
# eucalyptus. The discs (round 7, the owner: "more neutral colors, depending on the cabinet, will help the cabinet and
# horn pop more"; rounds 4 to 6 had charcoal on birch and rust on eucalyptus): a neutral that steps back into the
# cabinet, oat on birch's pale ground, graphite on eucalyptus's busy one (black from round 11, below), so the cabinet and
# the horn carry the colour;
# pewter on the frosted ice (the frost reads mid grey over the dark inside), mist on the cobalt marble's cool white. The
# woofer's ring takes the disc's colour (round 7, the owner: "That white ring around the driver when there's no cover is
# a little much"; off-white on birch and cream on eucalyptus before), so with the cover off the cone sits in the same
# quiet circle
OAT, GRAPHITE, CHARCOAL, PEWTER, MIST = '#CFC8BA', '#4B4844', '#2E2C2A', '#7A807E', '#C8CACA'
# round 11, the owner: "I don't like the graphite discs on eucalyptus or manzanita. I think we can do something closer
# to the bark color for each, or black"; then, of a test of each beside black: "Black on eucalyptus is preferred. Makes
# the cabinet pop more"
BLACK = '#1E1C1A'
BIRCH = {'bark': 'birch_bark', 'panel': '#D8D5CD', 'cloth': '#DCD6C8', 'cork': '#3B2F28', 'disc': OAT}
EUCALYPTUS = {'bark': 'eucalyptus_bark', 'panel': '#CBCFC4', 'cloth': '#6F7F66', 'cork': '#3B2F28', 'disc': BLACK}
# the waveguide's resin (round 5, the owner's third notes: "something semitransparent", "or something entirely darker,
# like black on birch and green on eucalyptus", "or more obvious texture if not monochromatic"). Each is a set of the
# horn material's tokens, plus settings of its own ('materials'). The first of each bark is the proposal and both
# notes at once: clear resin tinted dark, so the horn is dark in the room and the driver shows through it against the
# light. The others are options: lightly tinted clear, opaque (black, deep green), marbled with the bark's colours, a
# second colour swirled through clear, and round 4's milky resins
HORNS = dict(
    birch={
        'smoked': {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#5A5854', 'horn_cloud': 0.0},
        'clear': {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#EAE6DA', 'horn_cloud': 0.0,
                  'materials': {'horn': {'roughness': 0.1}}},
        'black': {'horn_preset': 'dark_resin', 'horn': '#1C1C1B', 'horn_deep': '#3A3936', 'horn_cloud': 0.08},
        'marble': {'horn_preset': 'marbled_resin', 'horn': '#EEEBE4', 'horn_deep': '#1E1C1A', 'horn_cloud': 0.0,
                   'materials': {'horn': {'stops': [[0.0, '#EEEBE4'], [0.47, '#EEEBE4'], [0.5, '#3A3734'], [0.53, '#1E1C1A'],
                                                    [0.56, '#9C9890'], [0.6, '#EEEBE4'], [1.0, '#EEEBE4']], 'vein_m': 0.32, 'warp': 0.9}}},
        'swirl': {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#E2E0DA', 'horn_cloud': 1.0,
                  'materials': {'horn': {'vein': '#55524D', 'cloud_m': 0.2}}},
        'milk': {'horn_preset': 'cast_resin', 'horn': '#F2EEE6', 'horn_deep': '#D9AE6E', 'horn_cloud': 0.3},
        # round 7, the owner: "try a yellow for the horn on birch to showcase what the tree looks like in the fall": the
        # birch's autumn leaves, a clear horn tinted golden yellow (seen against blue it turns green, so it is shot warm)
        'autumn': {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#F2B705', 'horn_cloud': 0.0,
                   'materials': {'horn': {'roughness': 0.08}}}},
    eucalyptus={
        'bottle': {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#4C6A36', 'horn_cloud': 0.0},
        'clear': {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#BCCB9A', 'horn_cloud': 0.0,
                  'materials': {'horn': {'roughness': 0.1}}},
        'green': {'horn_preset': 'dark_resin', 'horn': '#2C3A26', 'horn_deep': '#2C3A26', 'horn_cloud': 0.08},
        'marble': {'horn_preset': 'marbled_resin', 'horn': '#4A6428', 'horn_deep': '#4A6428', 'horn_cloud': 0.0,
                   'materials': {'horn': {'stops': [[0.0, '#7F7A70'], [0.3, '#7F7A70'], [0.36, '#A65230'], [0.42, '#4A6428'],
                                                    [0.58, '#4A6428'], [0.64, '#B79A48'], [0.7, '#E0D5B6'], [1.0, '#E0D5B6']],
                                          'vein_m': 0.26, 'warp': 1.0}}},
        'swirl': {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#DCCB98', 'horn_cloud': 1.0,
                  'materials': {'horn': {'vein': '#3F5E1C', 'cloud_m': 0.2}}},
        'amber': {'horn_preset': 'cast_resin', 'horn': '#EFE5D0', 'horn_deep': '#D6A04E', 'horn_cloud': 0.6},
        # the bark's own pattern cast into clear resin (round 7's decision for a patterned horn; drawn as round 6's
        # printed horn, which shows the same artwork)
        'cast': {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#E8EBDD', 'horn_cloud': 0.0,
                 'materials': {'horn': {'print': 'eucalyptus_bark', 'print_strength': 0.85, 'roughness': 0.1}}}})
# the line's horns (round 11, the owner: "the cast-in pattern should be used for eucalyptus and the yellow gold can be
# used for birch everywhere"; smoked resin on birch and bottle green on eucalyptus before, round 6)
VARIANTS = dict(birch={**BIRCH, **HORNS['birch']['autumn']}, eucalyptus={**EUCALYPTUS, **HORNS['eucalyptus']['cast']})
for bark, base_ in (('birch', BIRCH), ('eucalyptus', EUCALYPTUS)):
    VARIANTS.update({f'{bark}-{k}': {**base_, **v} for k, v in HORNS[bark].items()})
VARIANTS.update({
    # the cabinet without wood (pressed.py): the sheets laid out in each bark's own pattern (round 5); round 4's sheets
    # (the eucalyptus's colours in vertical strips, the birch's black dashes on milk) kept to compare
    'eucalyptus-pressed': {**VARIANTS['eucalyptus'], 'bark': 'pressed_eucalyptus_bark'},
    'birch-pressed': {**VARIANTS['birch'], 'bark': 'pressed_birch_bark'},
    'eucalyptus-strips': {**VARIANTS['eucalyptus'], 'bark': 'pressed_eucalyptus_sheet'},
    'birch-dashes': {**VARIANTS['birch'], 'bark': 'pressed_birch_sheet'},
    'birch-autumn-pressed': {**VARIANTS['birch-autumn'], 'bark': 'pressed_birch_bark'},
    # the material experiments of 2026-10-11: the waveguide in resin poured in layers (strata) or with recycled plastic
    # chips cast through it (terrazzo), in round 3's colours
    'eucalyptus-strata': {**EUCALYPTUS, 'horn_preset': 'frosted_strata', 'horn': '#DEE6D4', 'horn_deep': '#B9C9A9', 'horn_cloud': 0.0},
    'birch-terrazzo': {**BIRCH, 'horn_preset': 'frosted_terrazzo', 'horn': '#F5F2EC', 'horn_deep': '#EFE5D3', 'horn_cloud': 0.0},
})
# black veins through white, thinner than the study's bold marble, for a speaker marbled all over
VEINED = {'stops': [[0.0, '#EEEBE4'], [0.44, '#EEEBE4'], [0.47, '#8E8B85'], [0.49, '#1E1C1A'], [0.51, '#1E1C1A'], [0.53, '#8E8B85'],
                    [0.56, '#EEEBE4'], [1.0, '#EEEBE4']], 'warp': 1.0}
VARIANTS.update({
    # round 6, the owner's notes of 2026-10-12 (evening). The horn printed with its bark's pattern in translucent inks,
    # over clear resin and over a light tint, on the cabinet without wood
    'birch-printed': {**VARIANTS['birch-pressed'], 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#EEECE6', 'horn_cloud': 0.0,
                      'materials': {'horn': {'print': 'birch_bark', 'print_strength': 0.9, 'roughness': 0.1}}},
    'birch-printed-smoke': {**VARIANTS['birch-pressed'], 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#9C9A95', 'horn_cloud': 0.0,
                            'materials': {'horn': {'print': 'birch_bark', 'print_strength': 0.9, 'roughness': 0.1}}},
    'eucalyptus-printed': {**VARIANTS['eucalyptus-pressed'], 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#E8EBDD',
                           'horn_cloud': 0.0, 'materials': {'horn': {'print': 'eucalyptus_bark', 'print_strength': 0.85, 'roughness': 0.1}}},
    'eucalyptus-printed-green': {**VARIANTS['eucalyptus-pressed'], 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#A3B88A',
                                 'horn_cloud': 0.0, 'materials': {'horn': {'print': 'eucalyptus_bark', 'print_strength': 0.85, 'roughness': 0.1}}},
    # (round 13: the smoke's tint made neutral, #C9C7C2 before; seen through two walls and lit through several, the
    # lining took its warmth up to olive)
    # the cabinet in other plastics, still without wood: translucent cast acrylic as late-90s electronics were (smoke,
    # green, frosted ice), stone looks (terrazzo, cultured marble, a translucent green onyx), and whole speakers
    # marbled or swirled, the horn and the cabinet alike. 'bark' is the cabinet's material
    'birch-y2k-smoke': {**BIRCH, **HORNS['birch']['smoked'], 'bark': 'clear_resin', 'disc': CHARCOAL,
                        'materials': {'bark': {'deep': '#C7C7C5', 'radius': 0.025, 'roughness': 0.05}}},
    # Poison (round 10, the owner: "Poison should have a matching green cover and frame around the driver"): the cover
    # and the ring (which follows the disc) in the acrylic's own green, as Smoke's and Fog's follow theirs
    'eucalyptus-y2k-green': {**EUCALYPTUS, **HORNS['eucalyptus']['bottle'], 'bark': 'clear_resin', 'disc': '#2E4A2C',
                             'materials': {'bark': {'deep': '#B2C9A2', 'radius': 0.025, 'roughness': 0.05}}},
    'birch-y2k-ice': {**BIRCH, **HORNS['birch']['clear'], 'bark': 'clear_resin', 'disc': PEWTER,
                      'materials': {'horn': {'roughness': 0.1}, 'bark': {'deep': '#E4E9EB', 'radius': 0.025, 'roughness': 0.35, 'milk': 0.15}}},
    'birch-stone-terrazzo': {**BIRCH, **HORNS['birch']['smoked'], 'bark': 'terrazzo'},
    'birch-stone-marble': {**BIRCH, **HORNS['birch']['smoked'], 'bark': 'marbled_resin',
                           'materials': {'bark': {'stops': [[0.0, '#F1EFEA'], [0.4, '#ECE9E3'], [0.46, '#C9C6BF'], [0.49, '#5C5955'],
                                                            [0.5, '#2A2826'], [0.52, '#8E8B85'], [0.58, '#E9E6E0'], [1.0, '#F3F1EC']],
                                                  'vein_m': 0.5, 'warp': 1.1, 'stretch': 1.6, 'roughness': 0.3}}},
    'eucalyptus-stone-onyx': {**EUCALYPTUS, **HORNS['eucalyptus']['bottle'], 'bark': 'clear_resin',
                              'materials': {'bark': {'deep': '#DCDFB8', 'radius': 0.025, 'roughness': 0.1, 'milk': 0.12, 'cloud': 1.0,
                                                     'cloud_m': 0.13, 'cloud_edge': [0.47, 0.6], 'vein': '#3F4A1E'}}},
    'birch-marbled': {**BIRCH, **HORNS['birch']['marble'], 'bark': 'marbled_resin',
                      'materials': {'horn': {**VEINED, 'vein_m': 0.32}, 'bark': {**VEINED, 'vein_m': 0.5}}},
    'eucalyptus-marbled': {**EUCALYPTUS, **HORNS['eucalyptus']['marble'], 'bark': 'marbled_resin',
                           'materials': {'horn': HORNS['eucalyptus']['marble']['materials']['horn'],
                                         'bark': {**HORNS['eucalyptus']['marble']['materials']['horn'], 'vein_m': 0.4}}},
    'birch-swirled': {**BIRCH, **HORNS['birch']['swirl'], 'bark': 'clear_resin', 'disc': CHARCOAL,
                      'materials': {'horn': HORNS['birch']['swirl']['materials']['horn'],
                                    'bark': {'deep': '#D9D8D3', 'radius': 0.025, 'roughness': 0.06, 'cloud': 1.0, 'vein': '#5E5B56', 'cloud_m': 0.3}}},
    'eucalyptus-swirled': {**EUCALYPTUS, **HORNS['eucalyptus']['swirl'], 'bark': 'clear_resin',
                           'materials': {'horn': HORNS['eucalyptus']['swirl']['materials']['horn'],
                                         'bark': {'deep': '#E2D6AE', 'radius': 0.025, 'roughness': 0.06, 'cloud': 1.0, 'vein': '#4F6A2C',
                                                  'cloud_m': 0.3}}},
})
# round 7, the look book (the owner: "make the marble a white and cobalt instead of white and black"): the marbled
# speaker's veins in cobalt through a cool white, the horn and the cabinet alike, and a mist disc
COBALT = {'stops': [[0.0, '#F2F3F1'], [0.44, '#F2F3F1'], [0.47, '#9DB0DD'], [0.49, '#1D3C9A'], [0.51, '#1D3C9A'], [0.53, '#9DB0DD'],
                    [0.56, '#F2F3F1'], [1.0, '#F2F3F1']], 'warp': 1.0}
VARIANTS['birch-marbled-cobalt'] = {**BIRCH, **HORNS['birch']['marble'], 'horn': '#F2F3F1', 'horn_deep': '#1D3C9A', 'bark': 'marbled_resin',
                                    'disc': MIST,
                                    'materials': {'horn': {**COBALT, 'vein_m': 0.32}, 'bark': {**COBALT, 'vein_m': 0.5}}}
# round 7, the owner: "We should also do a manzanita". Its smooth bark, deep red and polished, peeling in thin curls to a
# fresh underbark of green, tan and orange (manzanita_bark, the eucalyptus's shader retuned). Its horn wears the bark's
# pattern cast in, as the bark pair's do in the look book; or clear resin tinted ember red. The disc: graphite (the
# ground is a deep red, mid-dark), the ring with it
MANZANITA = {'bark': 'manzanita_bark', 'panel': '#D3C6B8', 'cloth': '#5B2B22', 'cork': '#3B2F28',
             'disc': '#5B2B22'}      # its bark's deep red-brown (round 11, in place of graphite)
HORNS['manzanita'] = {
    'cast': {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#EFE6DF', 'horn_cloud': 0.0,
             'materials': {'horn': {'print': 'manzanita_bark', 'print_strength': 0.85, 'roughness': 0.1}}},
    'ember': {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#8A3F2C', 'horn_cloud': 0.0}}
VARIANTS.update({
    'manzanita': {**MANZANITA, **HORNS['manzanita']['cast']},
    'manzanita-ember': {**MANZANITA, **HORNS['manzanita']['ember']},
    'manzanita-pressed': {**MANZANITA, **HORNS['manzanita']['cast'], 'bark': 'pressed_manzanita_bark'},
})
# round 7, the owner's photos of snakebark maples ("Lots of cool barks we can work with"): a striped maple ('Joe Witt',
# chalk white with green pinstripes), its pattern cast into the horn, and a mist disc on its cool white. Round 8, the
# owner: "Remove Phoenix, red vein, cherry": the coral snakebark, the redvein maple and the Tibetan cherry are gone from
# the line (their bark presets stay in the engine's library)
SNAKEBARK_WHITE = {'bark': 'snakebark_white', 'panel': '#DCE0D8', 'cloth': '#6B784A', 'cork': '#3B2F28', 'disc': MIST}


def cast_horn(preset, deep):
    """A clear horn with a bark's pattern cast into it."""
    return {'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': deep, 'horn_cloud': 0.0,
            'materials': {'horn': {'print': preset, 'print_strength': 0.85, 'roughness': 0.1}}}


VARIANTS.update({
    'snakebark-white': {**SNAKEBARK_WHITE, **cast_horn('snakebark_white', '#EEF0EA')},
    'snakebark-white-pressed': {**SNAKEBARK_WHITE, **cast_horn('snakebark_white', '#EEF0EA'), 'bark': 'pressed_snakebark_white'},
})


# round 8, the owner: "bark is more of a product style/line. Y2K another. Crag another, which would include marble and
# such ... Let's explore some more stone/crag options. Malachite maybe." The Crag line wears a stone's pattern on the horn
# and the cabinet alike (as the cobalt marble does): malachite, lapis lazuli and turquoise (the engine's stone presets).
# Round 10, the owner: "the stone aren't going to be cast stone, they'll be plastic and resin. I imagine cast stone would
# be way too expensive and heavy": the cabinet pressed recycled plastic, the horn cast resin with the pattern cast in. Each is
# one colour, so its cover takes the stone's own colour (the owner, round 7: "I like when the driver covers are the same
# color for the monochromatic options"). Round 10, the owner: "The travertine is boring and the rhodochrosite is too
# much like a pink malachite. Let's replace the two of them with one more interesting rock. Something that will pop,
# that is a different color than the other options": spiderweb turquoise, sky blue-green in a dark web (their presets
# stay in the engine's library)
def crag(stone, cover, deep=None, bands=None, milk=0.0, horn=None):
    """A speaker in one stone's pattern, horn and cabinet, with a cover of the stone's colour: the cabinet pressed
    recycled plastic in the stone's pattern; the horn cast resin with the pattern cast in (round 10), opaque, the
    stone's pigment through it, `horn` its own settings (the pattern drawn out down its walls, below). With `deep` the
    resin clear instead, the pattern through it and `milk` a white haze in it (tried in round 11; the owner prefers
    the opaque horns). `bands`: the stone's colours changed."""
    over = {'bands': bands} if bands else {}
    own = {**over, **(horn or {})}
    h = ({'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': deep, 'horn_cloud': 0.0,
          'materials': {'horn': {'print': stone, 'print_params': over, 'print_strength': 0.9, 'roughness': 0.08, 'milk': milk},
                        **({'bark': over} if over else {})}} if deep else
         {'horn_preset': stone, 'horn': '#FFFFFF', 'horn_deep': '#FFFFFF', 'horn_cloud': 0.0,
          **({'materials': {'horn': own, **({'bark': over} if over else {})}} if own else {})})
    return {'bark': stone, 'panel': cover, 'cloth': cover, 'cork': '#3B2F28', 'disc': cover, **h}


# lapis lazuli without its white calcite (round 11: the critic read a wisp of it on the cabinet's corner as a smudge,
# and the owner's words for it are "deep blue, flecked with gold"): the pale stops blue
LAPIS_BANDS = [[0.0, '#0B1648'], [0.22, '#0F1D5A'], [0.42, '#16286E'], [0.58, '#0E1B55'], [0.72, '#1B3282'], [0.83, '#24408F'],
               [0.86, '#2B4898'], [0.895, '#3552A3'], [0.925, '#284391'], [0.96, '#16286E'], [1.0, '#0F1D5A']]
# the Crag horns opaque, like stone (round 11, the owner: "i kind of prefer the opaque waveguides for the stone
# options"), the pattern drawn out down the walls into the throat as a pour runs down a mould, so the flare reads (the
# critic of the look book: the opaque horns' mouths "read as solid blocks with a dot"): the malachite's bands become
# rings following the horn in, the turquoise's web drawn in with them; the lapis's deep blue and gold flecks read as is
DOWN = {'stretch': 4.0, 'stretch_axis': 1}
VARIANTS.update({
    'crag-malachite': crag('malachite', '#1F4C34', horn=DOWN),
    'crag-lapis': crag('lapis', '#1D2D6B', bands=LAPIS_BANDS),
    'crag-turquoise': crag('turquoise', '#3597A2', horn={**DOWN, 'web_stretch': 2.5}),
})
# the cobalt marble's horn stays opaque marbled resin (cast in, the white goes clear and the cobalt veins grey), polished,
# its veins drawn out down the walls into the throat as a pour runs down a mould, so the flare reads (the critic: the
# Crag horns' mouths "read as solid blocks with a dot"); the Cloud horns polished too (the critic: Poison's and Smoke's
# throats "smeared": a satin face blurs the dark pod behind it)
_cob = VARIANTS['birch-marbled-cobalt']
VARIANTS['birch-marbled-cobalt'] = {**_cob, 'materials': {**_cob['materials'],
                                                          'horn': {**_cob['materials']['horn'], 'roughness': 0.15, 'coat': 0.6,
                                                                   'vein_m': 0.22, 'stretch': 6.0, 'stretch_axis': 1}}}
for _k in ('birch-y2k-smoke', 'eucalyptus-y2k-green'):
    VARIANTS[_k] = {**VARIANTS[_k], 'materials': {**VARIANTS[_k]['materials'], 'horn': {'roughness': 0.03}}}
# round 17 (the owner: "Let's put a pause on bark and crag. The cloud line I think is the strongest aesthetically";
# "Let's add some other colors to the mix, like the autumn color from the birch horn. Not sure what I'd call a yellow
# cloud though. Acid maybe. Purple could be cool too"): two more Cloud speakers made as Poison is, the cabinet in
# tinted cast acrylic lined in white, the horn polished clear resin tinted to match, the cover and the ring in the
# colour, deeper. Amber takes the autumn birch's horn as it is; violet goes about as deep as Poison's bottle green
VARIANTS.update({
    'cloud-amber': {**BIRCH, 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#F2B705', 'horn_cloud': 0.0,
                    'bark': 'clear_resin', 'disc': '#9A6A12',
                    'materials': {'bark': {'deep': '#F2D06B', 'radius': 0.025, 'roughness': 0.05}, 'horn': {'roughness': 0.03}}},
    'cloud-violet': {**BIRCH, 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#5E3F8F', 'horn_cloud': 0.0,
                     'bark': 'clear_resin', 'disc': '#3F2A5E',
                     'materials': {'bark': {'deep': '#BEADD8', 'radius': 0.025, 'roughness': 0.05}, 'horn': {'roughness': 0.03}}},
    # round 18 (the owner: "Can we do dust in an orange color, and ice in a blue color?"): orange (Dust) and a clear blue
    # (Ice; the key is blue, as 'ice' has been Fog's, the frosted one, since round 8)
    'cloud-orange': {**BIRCH, 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#E0661C', 'horn_cloud': 0.0,
                     'bark': 'clear_resin', 'disc': '#8C3B14',
                     'materials': {'bark': {'deep': '#F2B184', 'radius': 0.025, 'roughness': 0.05}, 'horn': {'roughness': 0.03}}},
    'cloud-blue': {**BIRCH, 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#3C86C2', 'horn_cloud': 0.0,
                   'bark': 'clear_resin', 'disc': '#24557E',
                   'materials': {'bark': {'deep': '#B5D9EE', 'radius': 0.025, 'roughness': 0.05}, 'horn': {'roughness': 0.03}}},
    # round 19 (the owner: "What if we did a full spectrum, red orange yellow green blue purple white and black"): a red
    # one (Ember; Flare from round 21 until round 30) and Smoke made black ("Smoke was meant to be the black one"), a deep smoked tint the
    # lining still shows faintly through (round 10's grey, birch-y2k-smoke, retired from the line)
    'cloud-red': {**BIRCH, 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#C8262B', 'horn_cloud': 0.0,
                  'bark': 'clear_resin', 'disc': '#7A1A1C',
                  'materials': {'bark': {'deep': '#F2A29C', 'radius': 0.025, 'roughness': 0.05}, 'horn': {'roughness': 0.03}}},
    'cloud-black': {**BIRCH, 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#2A292C', 'horn_cloud': 0.0,
                    'bark': 'clear_resin', 'disc': '#141316',
                    'materials': {'bark': {'deep': '#8A888E', 'radius': 0.025, 'roughness': 0.05}, 'horn': {'roughness': 0.03}}},
})
# round 22 (the owner: "Should we redo the fog to be more clear white the same way we redid smoke"): Fog made the white
# one as Smoke was made the black: polished, not frosted, cast acrylic, near colourless with a faint opal haze, so the
# white lining reads through it clear and white rather than frosted pale blue; the horn polished water-clear, the cover
# and the ring white. (Tested: milk 0.3 turned it a matt grey box; none at all, plain glass with dark green edges.) The
# key stays 'birch-y2k-ice' (Fog's since round 8; frosted ice-blue until round 22)
VARIANTS['birch-y2k-ice'] = {**BIRCH, 'horn_preset': 'clear_resin', 'horn': '#FFFFFF', 'horn_deep': '#F1F1EE', 'horn_cloud': 0.0,
                             'bark': 'clear_resin', 'disc': '#E7E6E1',
                             'materials': {'bark': {'deep': '#F7F8F7', 'radius': 0.025, 'roughness': 0.05, 'milk': 0.0},
                                           'horn': {'roughness': 0.03}}}
# round 24 (the owner, of round 23's two: "Water-clear"): Fog is water-clear, as the other seven are clear: no haze
# (milk 0, round 22's 0.05), the deep a touch whiter, as round 23's 'birch-fog-clear' (kept below with the opal)
# round 23 (the owner: "Are all of the others not hazy? If so this one could be not hazy for consistency. Completely
# clear like the old phones, or semi opaque like the old gameboy. It would be good to compare options"): the colours
# and Smoke are clear, no haze in them, so two candidates for Fog to set beside round 22's faint haze: water-clear (as
# the colours, the lining seen sharp through it) and semi-opaque (milk 0.18: the lining and the fittings seen as soft
# shapes, as through a translucent Game Boy). A frosted body (the engine's frosted preset, glossy) was tried and read
# as opaque white plastic. (Named birch- as Fog's is, so frames.py takes the same base shot.)
VARIANTS['birch-fog-clear'] = {**VARIANTS['birch-y2k-ice'],
                         'materials': {**VARIANTS['birch-y2k-ice']['materials'],
                                       'bark': {'deep': '#F7F8F7', 'radius': 0.025, 'roughness': 0.05, 'milk': 0.0}}}
VARIANTS['birch-fog-opal'] = {**VARIANTS['birch-y2k-ice'],
                        'materials': {**VARIANTS['birch-y2k-ice']['materials'],
                                      'bark': {'deep': '#F5F6F5', 'radius': 0.025, 'roughness': 0.05, 'milk': 0.18}}}


PRODUCT = Product(
    'barkhorn', 'barkhorn', 'Two-way horn loudspeaker after Friendly Pressure, in birch bark or eucalyptus bark', params=P, parts=parts,
    notes=['Bark on the shell (sides, top, bottom and back): real birch bark sheet (Betula papyrifera, from fallen or felled trees) laminated to the plywood with PVA in a vacuum bag and sealed with a matt waterborne lacquer, wrapped round the shell\'s front edges; for eucalyptus, the shed bark of a smooth-barked gum (spotted or snow gum) pressed flat and laminated the same way, or a UV-printed veneer of it. Approve a sample board first.',
           'Glue-up: sides to the bottom, the brace, then the front panel (set back 24 mm), the top, and the back\'s four cleats, their back faces 21 in from the shell\'s back edge; the back screws on last, on its gasket, and comes off.',
           'The woofer flush in its rebate on a gasket, on eight M6 T-nuts from inside; the ring over its frame, held by four magnets in the panel under steel discs in its back; each port, printed in one with its square frame, fitted from the front, the frame flush in a recess on a foam gasket, four black wood screws in its corners; its length found on the first sample (its rounded ends cannot be trimmed).',
           'The waveguide stands on four posts, stainless lamp tube 10 x 7, each threaded M10 x 1 at its top into a brass insert bonded in a pad cast under the horn (drilled after casting, through a jig taken off the top\'s sockets), its plain foot standing in a polyurethane sleeve in a brass socket pressed into the top, so the horn and its posts lift off as one. An M6 rod down the free rear post, from a thumb nut inside the pod to an insert under the top, holds them down. The cap closing the pod is held by a twist-lock (round 16): three lugs on its spigot in L-slots in the pod\'s bore, locked by an eighth of a turn, an O-ring beyond them; no screw shows. The HF lead, a round silicone cable 5 across, runs from its connector at the amplifier\'s compartment straight up, through a gland under the top and up inside a rear post into the pod, where it plugs into the driver\'s leads. To lift the horn off: the cap off, the nut undone and the lead unplugged.',
           'The front: the panel faced in bark (1 mm) round the ring and the port, and a cloth disc over the woofer, its MDF frame standing on the ring on four magnet pairs, its face 18.5 clear of the cone at rest.',
           'The FA122 crosses at about 800 Hz (LR4: B&C asks 12 dB/oct or steeper there) with the HF channel about 9 dB down (108 dB at 2.83 V against the woofer\'s 99), part of it in the passive L-pad after the amplifier, so its hiss stays inaudible: two 25 W aluminium-housed resistors on a plate in the compartment, behind a 33 uF film capacitor that keeps low frequencies off the driver if the preset is ever lost.',
           'The amplifier\'s preset, stored before the speaker ships: the crossover; a 4th-order Butterworth high-pass at 28 Hz on the woofer (below the ports\' tuning the box no longer holds the cone, which would pass Xmax below about 30 Hz at full output, and a record\'s warp drives it there); limiters set to the woofer\'s Xmax and the driver\'s rating; a notch at the ports\' pipe resonance (about 540 Hz in the pressed cabinet, 560 in the Cloud\'s, 600 in the plywood one), measured in each port\'s near field.',
           'The amplifier in a sealed compartment of its own, as Hypex asks: 1.5 mm aluminium, black anodised, on an EPDM gasket on the back\'s inner face, so the box stays airtight and the mains electronics are enclosed in metal. The leads leave it through cable glands. A rating plate beside the amplifier carries the model, the serial number, the ratings, the marks and the maker\'s address; the finished speaker needs an EMC pre-scan and an IEC 62368-1 assessment.',
           'The lining: polyester batts (thermally bonded, recycled PET), 50 mm on the sides and 100 mm on the top and the bottom (round 21), one to each bay between the braces (and the ribs), and 50 mm on the back, its full height between its ribs, so they come off with it; each cut 10 full each way and sewn into a sleeve of white voile; none on the front panel, none beside the ports (10 clear of each tube, nothing between its inner end and the back\'s batts) and none within 20 of the amplifier\'s compartment.',
           'The back comes off (round 14): it closes on a 3 mm EPDM gasket against four land strips inside the shell, sixteen M5 button heads through it into inserts in them. The amplifier\'s compartment, the back\'s ribs and its batts come off with it and the leads unplug at the compartment, so the amplifier, the L-pad and the leads can be reached.',
           'Four levelling feet (M8, 40 swivel bases on rubber pads) in inserts in the bottom, 50 in from its edges, lift the cabinet 12 mm: set them so it stands level and cannot rock under the horn, and lock their nuts.'],
    touching=[('grille-cloth', 'cloth-frame'), ('cloth-disc', 'disc-frame'),      # the cloth wraps its frame
              ('lead-hf', 'cable-glands'), ('lead-woofer', 'cable-glands')],        # and the leads pass through their glands
    # the shell's edges broken on 1 (round 15): no sheet's edge is sharp once welded and planed, cemented and polished, or
    # wrapped in bark, and the light's catch on it shows where one panel meets the next
    materials={'bark': {'preset': '$bark', 'bevel_mm': 1.0}, 'raw': {'preset': 'birch'},
               'cloth': {'preset': 'cloth', 'color': '$cloth'}, 'disc': {'preset': 'cloth', 'color': '$disc'},
               'grille-paint': {'preset': 'satin_paint', 'color': '$panel', 'roughness': 0.6, 'specular': 0.3},
               'grille-timber': {'preset': 'birch', 'color': '#8E6E4E', 'roughness': 0.55},
               'cork': {'preset': 'cork', 'color': '$cork'},
               'panel': {'preset': 'satin_paint', 'color': '$panel', 'roughness': 0.6, 'specular': 0.3},
               # the disc's colour; round 31: cast acrylic tinted opaque and polished, as the notes say, not a paint
               'ring': {'preset': 'opaque_acrylic', 'color': '$disc'},
               'horn': {'preset': '$horn_preset', 'color': '$horn', 'absorb': '$horn_deep', 'deep': '$horn_deep', 'cloud': '$horn_cloud',
                        'cloud_m': 0.12},
               'rod': {'preset': 'metal', 'color': '#C9C9C6', 'roughness': 0.3},
               # the ports printed in black ASA: a satin face, its edges catching the light, so the round bore reads in its
               # square frame (round 14)
               'port': {'preset': 'satin_paint', 'color': '#1C1B1A', 'roughness': 0.45, 'specular': 0.5, 'bevel_mm': 0.8},
               'amp': {'preset': 'satin_paint', 'color': '#303033', 'roughness': 0.4, 'specular': 0.5},   # black anodised plate
               # round 31 (spinoffs/barkhorn/drivers31.md): the drivers as FaitalPRO and B&C make them. Treated paper with
               # its fibre and streaks, the doped cloth surround, the cap doped glossier; the baskets and bodies die-cast in
               # black e-coat; the screws black oxide; the motor's steel in black, its neodymium nickel-plated
               'driver-frame': {'preset': 'ecoat', 'color': '#1B1B1C'}, 'driver-cone': {'preset': 'treated_paper', 'color': '#2A2826'},
               'driver-surround': {'preset': 'doped_cloth', 'color': '#1E1D1C'},
               'driver-cap': {'preset': 'treated_paper', 'color': '#262422', 'roughness': 0.5, 'coat': 0.3, 'coat_roughness': 0.3,
                              'streaks': 0.04},
               'driver-motor': {'preset': 'ecoat', 'color': '#1D1D1E', 'roughness': 0.34},
               'driver-magnet': {'preset': 'metal', 'color': '#B9B6AE', 'roughness': 0.3},
               'driver-coil': {'preset': 'metal', 'color': '#B87333'}, 'driver-spider': {'preset': 'rubber', 'color': '#C8B88A'},
               'driver-plug': {'preset': 'ecoat', 'color': '#202022', 'roughness': 0.3, 'grain': 0.08},
               'driver-screw': {'preset': 'black_oxide'}, 'driver-gasket': {'preset': 'rubber', 'color': '#121212', 'roughness': 0.85},
               'driver-terminal': {'preset': 'metal', 'color': '#D4D4D2', 'roughness': 0.15},
               'driver-bright': {'preset': 'metal', 'color': '#C9CACB', 'roughness': 0.22, 'anisotropic': 0.5},
               'lining': {'preset': 'batting'},
               # round 21's marks: laser-etched (frosted) acrylic or laser-marked anodising, white acrylic, a print on cloth
               'etch': {'preset': 'satin_paint', 'color': '#ECEBE7', 'roughness': 0.85, 'specular': 0.15},
               'mark-tint': {'preset': 'satin_paint', 'color': '$disc', 'roughness': 0.6, 'specular': 0.25},   # round 23
               'mark': {'preset': 'satin_paint', 'color': '#F3F2EE', 'roughness': 0.3, 'specular': 0.45},
               'print': {'preset': 'satin_paint', 'color': '#EDEBE5', 'roughness': 0.9, 'specular': 0.05},
               # round 24: the globe UV-printed in the corner, each ring's colour (round 25: read from earth.py's RING by
               # way of brand/earth-outlines.json, so the print follows the brand)
               **{f'print-{k}': {'preset': 'satin_paint', 'color': c, 'roughness': 0.55, 'specular': 0.3}
                  for k, c in enumerate(globe_colours()[0])},
               # round 13: the fittings a photograph shows (through the Cloud's acrylic, most of all)
               'brass': {'preset': 'metal', 'color': '#C9A660', 'roughness': 0.3},
               'sleeve': {'preset': 'rubber', 'color': '#1B1B1B'},
               'cable': {'preset': 'rubber', 'color': '#141414', 'roughness': 0.5},
               'gland': {'preset': 'plastic', 'color': '#1A1A1A', 'roughness': 0.5},
               # round 31: the FA122's plate as it is, its grey label strips, the rating sticker's foil, the status lights
               # (P1 lit) and the RCAs' coloured insulators
               'amp-label': {'preset': 'satin_paint', 'color': '#C4C6C5', 'roughness': 0.5, 'specular': 0.3},
               'amp-foil': {'preset': 'metal', 'color': '#BEC0C1', 'roughness': 0.35},
               'amp-ring': {'preset': 'metal', 'color': '#8E8E8C', 'roughness': 0.45},
               'led-on': {'preset': 'emit', 'color': '#4CF07A', 'strength': 6.0},
               'led-green': {'preset': 'gloss_plastic', 'color': '#0F3A1E', 'roughness': 0.15},
               'led-red': {'preset': 'gloss_plastic', 'color': '#4A0E10', 'roughness': 0.15},
               'rca-white': {'preset': 'plastic', 'color': '#E8E6E0', 'roughness': 0.35},
               'rca-red': {'preset': 'plastic', 'color': '#B3121A', 'roughness': 0.35},
               'rca-orange': {'preset': 'plastic', 'color': '#C8742A', 'roughness': 0.35},
               # round 14: the ports' black screws, and the feet
               'screw': {'preset': 'metal', 'color': '#262626', 'roughness': 0.4},
               'foot': {'preset': 'plastic', 'color': '#1C1C1C', 'roughness': 0.6}},
    variants=VARIANTS,
    drawing_style={'face': os.path.join(FONTS, 'IBMPlexMono-Regular.ttf'), 'face_bold': os.path.join(FONTS, 'IBMPlexMono-SemiBold.ttf'),
                   'label_pt': 11, 'dim_pt': 10, 'balloon_pt': 11, 'balloon_r': 4.4},    # the look book's mono, read off a slide
)


if __name__ == '__main__':
    from speaker.box import vented, suggest_vented
    ts = LIB[P['woofer']]['ts']
    pl, net = tuned(P)
    n = len(P['port']['x'])
    print(f"QB3 start: {suggest_vented(ts)} (L, Hz)")
    print(f"net {net:.1f} L, {n} x {P['port']['d']:g} mm round ports {pl:.0f} long for {P['fb']:g} Hz")
    for fb in (32.0, 35.0, 38.0):
        r = vented(ts, net, fb, bore_mm=P['port']['d'] * math.sqrt(n))
        print(fb, {k: r[k] for k in ('f3', 'ref_db', 'max_spl_db', 'port_air_m_s_at_max')})
