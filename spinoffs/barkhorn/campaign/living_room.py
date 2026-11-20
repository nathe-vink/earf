"""A living room by day for Tropos, Mantle and Core (the coordinator, 20 Nov: the owner, "the speakers should have ... a
listening space image ... Core and mantle should have living space images").

Built from three photographs (looked at 20 Nov, public pages):
- Klipsch, Klipschorn AK7 hero (a pair against the wall, a low console between with the turntable on it, records
  below, the seat's back across the foot of the frame, a plant at the side);
- KEF, Blade Two lifestyle (daylight from a side window raking across a plain wall and a pale floor, a chair cut by the
  frame's edge, a small side table, nothing else);
- Design Within Reach, Panthella 160 (a small lamp on wood beside the bed, the window's sun throwing its shadow on a
  limewash wall).

The room: limewash plaster walls, an oak floor, one wool rug, a walnut console 640 mm high, a mid-century lounge chair
(scanned), a plant (scanned), books and records; the pair 2.5 m apart, 0.3 m off the back wall, toed in 6 degrees; Mantle
on the console, a record on it; a Core switched off at the console's right end; each Tropos's mains lead to a socket,
Mantle's leads to each speaker. Honest light: the sky and its sun (garden_nook, Poly Haven CC0, its own unclipped sun)
through the room's three windows: one in the back wall's left corner (in frame), one in the left wall (out of frame, the
sun's way in), one in the wall behind the lens (out of frame, the sky from the front). No lamp, no card, no fill.

Frame (metres): x across (+ to the right as the camera looks), y into the room (the back wall at y = 2), z up.

    TROPOS_BASE=A LAMPS_ROOT=/home/user/lamps-mix python3 spinoffs/barkhorn/campaign/living_room.py OUTDIR [TINT]
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shots                                    # noqa: E402
import listening_bar as LB                      # noqa: E402  (its turned glass)

EXT = 'spinoffs/barkhorn/campaign/living/living_ext.py'
LIFE = 'spinoffs/barkhorn/campaign/bar_life/bar_life.py'
LAMPS = 'spinoffs/barkhorn/campaign/stage/stage2_props.py'

# --- the room -----------------------------------------------------------------------------------------------------
W, D, H = 5.4, 6.0, 2.75                        # a living room, 5.4 x 6.0 m, 2.75 m ceiling
CX, CY = 0.0, -1.0                              # its floor's centre: x -2.7..2.7, y -4..2
BACK = CY + D / 2                               # the back wall's face, y = 2.0
LEFT = CX - W / 2                               # the left wall's face, x = -2.7
# the window in frame: a steel casement, its frame and bars dark; its bars are set pieces a few mm behind the frame's
# faces (the engine's own bars share the frame's faces, and coplanar faces render black in Cycles: proof 1's notches)
# (test u2: at along -1.95 the garden showed through the left horn and cabinet: further left, clear of the speaker)
WIN_BACK = {'wall': 'back', 'along': -2.22, 'sill': 0.42, 'size': [0.75, 1.95], 'mullions': [1, 1], 'frame_w': 0.055, 'frame_d': 0.06}
# the sun's way in, out of frame: a narrow window in the left wall at the back corner (y 1.55..1.95), so the sun crosses
# the room behind the horns' faces: it grazes the backs of both cabinets' sides (their red light onto the floor and the
# console's ends) and crosses the console's top to Mantle and the Core (test u1: a wider one lit the left horn alone,
# horns L* 41 against 10)
WIN_LEFT = {'wall': 'left', 'along': 2.75, 'sill': 0.3, 'size': [0.4, 2.05], 'mullions': [1, 1], 'frame_w': 0.055, 'frame_d': 0.06}   # (C: its bars our own too)
# the right wall, toward the front, out of frame: more sky into the room
WIN_RIGHT = {'wall': 'right', 'along': 1.6, 'sill': 0.3, 'size': [1.6, 2.15], 'mullions': [2, 2]}
# behind the lens: a long run of windows, the sky from the front, on both speakers alike. (The coordinator, 12:30: the
# fronts paler than the studio's, chroma 44 against 80. Tested: at 2.0 m and 1.2 m the fronts mirror plain wall, and the
# cabinets went darker and no deeper, chroma 42/37 and 36/33. The studio's depth is its 'through' lamp aimed through the
# cabinet; the honest twin here is the sun through the cabinets. Proof 2's run kept.)
WIN_FRONT = {'wall': 'front', 'along': 0.0, 'sill': 0.3, 'size': [4.6, 2.15], 'mullions': [5, 2]}
SKY = {'kind': 'hdri', 'polyhaven': 'garden_nook', 'res': '4k', 'rotation_deg': 144.2, 'strength': 1.0}
# (assets.py sun garden_nook: azimuth 54.2 - rotation, elevation 25.9. Proof 1 (101.2, azimuth -47, from the front
# left) put the sun on the left speaker's front and its cone: the coordinator, 20 Nov 11:58, no sun on a front. At 144.2
# the sun comes from straight left, azimuth -90, parallel to the fronts: through the left window it grazes the left
# cabinet's side (its red light onto the floor and the console's end), lies in stripes on the floor before the pair,
# and crosses the console's top to Mantle and the Core.)
STEEL = '#2C2B29'

# --- the furniture --------------------------------------------------------------------------------------------------
SPK_X, SPK_GAP, TOE = 1.25, 0.30, 15.5          # the pair 2.5 m apart, 0.3 m off the wall, aimed at the seat 4.5 m back (atan 1.25/4.5); (the critics: at 6 degrees the inner sides, seen 14 degrees off edge-on, mirrored the room white; past 14.5 they turn away from the lens)
TROPOS_D = 0.428
SPK_Y = round(BACK - SPK_GAP - TROPOS_D / 2, 4)
# (the critics, 18:41: the cabinets' inner sides read white: at that angle each mirrors the back wall in the gap beside
# the console; at 1.8 m the console's walnut end stands where they look)
CONSOLE = {'w': 1.8, 'd': 0.45, 'h': 0.64}
CON_Y = round(BACK - 0.06 - CONSOLE['d'] / 2, 4)
TOP = CONSOLE['h']
# (proof 2: the sun crosses the console's top in a band at its front; Mantle and the Core moved into it, Mantle turned
# 30 degrees toward the window so its Ember plinth's lit face shows to the lens)
MANTLE = (-0.24, CON_Y - 0.06, TOP + 0.001, -30.0)
CORE = (0.5, CON_Y - 0.155, TOP)           # at the console's front edge: the sun's band on its top is its front 6 cm
SOCKETS = (-1.85, 2.1)                          # the two outlets, either side of the pair, in frame
# (the critics, 20 Nov 18:41: the lounge chair's plywood back read as an oak barrel: an upholstered sofa, sofa_02 (scanned,
# 1.81 x 0.82 m, back 0.71 m high), its back to the lens across the frame's foot)
CHAIR = (0.0, -0.9, 180.0)
# a walnut side table (scanned) by the window in frame, in the sun's band: a book and a glass of water on it in every frame;
# camera C sets the Core on it, switched off (taken off the console for that frame only)
SIDE = (-2.2, 1.5, 0.0)              # (forward, so the Core can stand out of the sun's band)
SIDE_TOP = 0.5507
CORE_C = (-2.31, 1.40, SIDE_TOP)          # (in front of the sun's band, y 1.55 on: in full sun its opal went salmon, L* 75 C* 35)
CAM_A = {'position': [0.1, -3.05, 1.5], 'target': [0.0, 1.6, 1.0], 'lens_mm': 32.0, 'level': True, 'fstop': 8.0,
         'focus': [0.0, 1.3, 0.9]}


def _floor():
    # real oak planks over the room's own floor, a hair above it (Cycles: coplanar faces render black)
    return {'kind': 'kit', 'shape': 'box', 'size': [W - 0.02, D - 0.02, 0.003], 'position': [CX, CY, 0.0005],
            'material': 'pbr', 'texture': 'oak_wood_planks', 'tex_res': '2k', 'gain': 1.0}


def _rug():
    """A wool rug with pile and a bound edge: a herringbone wool field (photographed: its weave and pile in the texture)
    inside an 80 mm border band much darker, 16 mm thick, its edge rounded over (the field 1 mm proud, so no two faces
    lie in one plane). (Proof 2: the kit's wool has a strong sheen, and seen this low it went white and flat.)"""
    # (the critics, 18:41: a flat grey field with a knife-sharp border, no pile: 22 mm thick, the edge rounded 10 mm, the
    # weave twice its size and in relief, the border a shade of the field, not a line)
    wool = {'material': 'pbr', 'texture': 'poly_wool_herringbone', 'tex_res': '2k', 'tex_scale': 0.5, 'bump': 2.5}
    return [{'kind': 'kit', 'shape': 'box', 'size': [2.4, 1.7, 0.022], 'position': [0.0, 0.15, 0.0045], 'ease': 0.01,
             **wool, 'tint': '#6C604F', 'tint_mix': 0.6, 'gain': 0.7},
            {'kind': 'kit', 'shape': 'box', 'size': [2.26, 1.56, 0.0228], 'position': [0.0, 0.15, 0.0045], 'ease': 0.006,
             **wool, 'tint': '#A69680', 'tint_mix': 0.45, 'gain': 0.9}]


# (american_walnut_veneer averages #726E69, a grey: walnut_veneer_02, #A98971, deepened a little toward walnut)
WALNUT = {'material': 'pbr', 'texture': 'walnut_veneer_02', 'tex_res': '4k', 'tint': '#3A2214', 'tint_mix': 0.7, 'gain': 0.5}


def _console():
    """A walnut credenza, 1500 x 450 x 640, as a furniture maker builds one: a case of walnut (top, sides, bottom) round
    a dark inside; across its front a door, a bank of three drawers and a door, 18 mm fronts with 4 mm reveals between
    them and to the case; blackened bar pulls; the case on a walnut base rail and four tapered legs, set in from the
    ends. Grain runs along the top and up the fronts."""
    w, d, h = CONSOLE['w'], CONSOLE['d'], CONSOLE['h']
    yf = CON_Y - d / 2                                  # the front's plane
    z0, t, rv, ft = 0.19, 0.022, 0.004, 0.018           # the case's underside, its boards, the reveals, the fronts
    out = []
    box = lambda size, pos, rz=0.0, **m: {'kind': 'kit', 'shape': 'box', 'size': size, 'position': pos, 'rotate': [0, 0, rz], 'ease': 0.0015, **m}
    # the case: the top (grain along its length), the sides, the bottom; a dark core behind the fronts shows in the reveals
    out.append(box([d, w, t], [0.0, CON_Y, h - t], 90.0, **WALNUT))
    for sx in (-1, 1):
        out.append(box([t, d, h - z0 - t - 0.0005], [sx * (w / 2 - t / 2), CON_Y, z0], **WALNUT))
    out.append(box([w - 2 * t - 0.001, d, t], [0.0, CON_Y, z0], **WALNUT))
    out.append(box([w - 2 * t - 0.002, d - ft - 0.004, h - z0 - 2 * t - 0.002], [0.0, CON_Y + (ft + 0.004) / 2, z0 + t + 0.001],
                   material='clay', color='#1A1411', roughness=0.9))
    # the fronts in the opening x -0.728..0.728, z z0+t..h-t, 4 mm reveals
    x0, x1, za, zb = -w / 2 + t + rv, w / 2 - t - rv, z0 + t + rv, h - t - rv
    door = 0.36
    fy = yf + ft / 2 + 0.0005
    pull = dict(material='foil', color='#2E2925', roughness=0.42)
    for sx in (-1, 1):                                  # the two doors, vertical pulls by their inner edges
        cx = sx * (x1 - door / 2)
        out.append(box([door, ft, zb - za], [cx, fy, za], **WALNUT))
        out.append(box([0.012, 0.014, 0.11], [cx - sx * (door / 2 - 0.035), yf - 0.007, za + (zb - za) * 0.6], **pull))
    dx0, dx1 = x0 + door + rv, x1 - door - rv
    dh = (zb - za - 2 * rv) / 3
    for k in range(3):                                  # the bank of three drawers, a bar pull centred on each
        dz = za + k * (dh + rv)
        out.append(box([dx1 - dx0, ft, dh], [0.0, fy, dz], **WALNUT))
        out.append(box([0.16, 0.014, 0.012], [0.0, yf - 0.007, dz + dh * 0.62], **pull))
    # the base: a rail under the case and four tapered legs, set in from the ends and the front
    out.append(box([w - 0.2, d - 0.1, 0.03], [0.0, CON_Y, z0 - 0.03], **WALNUT))
    for sx in (-1, 1):
        for sy in (-1, 1):
            out.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.012, 'radius_top': 0.02, 'height': z0 - 0.03,
                        'position': [sx * (w / 2 - 0.13), CON_Y + sy * (d / 2 - 0.08), 0.0], **WALNUT})
    return out


def _window_bars():
    """The steel bars of the two windows camera A or C sees, set 6 mm back from their frames' faces (the engine's own
    bars share the frame's faces, and coplanar faces render black in Cycles: proof 1's notches): the back window one
    upright and two cross bars; the left window's narrow light two cross bars. 22 mm bars."""
    out = []
    bar = lambda size, pos: {'kind': 'kit', 'shape': 'box', 'size': size, 'position': pos, 'material': 'foil', 'color': STEEL,
                             'roughness': 0.5, 'ease': 0.001}
    wb = WIN_BACK                                       # in the back wall (y = BACK), outside toward +y
    xc = CX + wb['along']; ww, wh = wb['size']; fw = wb['frame_w']
    xa, xb, za, zb = xc - ww / 2 + fw, xc + ww / 2 - fw, wb['sill'] + fw, wb['sill'] + wh - fw
    y0 = BACK + 0.12 + 0.006; dep = wb['frame_d'] - 0.012
    out.append(bar([0.022, dep, zb - za + 0.02], [xc, y0 + dep / 2, za - 0.01]))
    for k in (1, 2):
        out.append(bar([xb - xa + 0.02, dep, 0.022], [xc, y0 + dep / 2, za + (zb - za) * k / 3 - 0.011]))
    wl = WIN_LEFT                                       # in the left wall (x = LEFT), outside toward -x; along runs to +y
    yc = CY + wl['along']; ww, wh = wl['size']; fw = wl['frame_w']
    ya, yb, za, zb = yc - ww / 2 + fw, yc + ww / 2 - fw, wl['sill'] + fw, wl['sill'] + wh - fw
    x0 = LEFT - 0.12 - 0.006; dep = wl['frame_d'] - 0.012
    for k in (1, 2):
        out.append(bar([dep, yb - ya + 0.02, 0.022], [x0 - dep / 2, yc, za + (zb - za) * k / 3 - 0.011]))
    return out


SOCKET_Z = 0.28                                  # the plate's foot; its lower receptacle's centre at SOCKET_Z + 0.032


def _socket(x):
    """A white duplex receptacle on the back wall above the skirting: the plate, two receptacle faces standing 3 mm proud,
    each with its two slots and its ground hole (the critics: blank plates read as no outlet)."""
    out = [{'kind': 'kit', 'shape': 'box', 'size': [0.07, 0.006, 0.115], 'position': [x, BACK - 0.003, SOCKET_Z],
            'material': 'clay', 'color': '#ECEAE4', 'roughness': 0.35, 'ease': 0.0015}]
    for zc in (SOCKET_Z + 0.032, SOCKET_Z + 0.083):
        out.append({'kind': 'kit', 'shape': 'box', 'size': [0.034, 0.004, 0.03], 'position': [x, BACK - 0.008, zc - 0.015],
                    'material': 'clay', 'color': '#E6E3DC', 'roughness': 0.3, 'ease': 0.002})
        for dx in (-0.0065, 0.0065):
            out.append({'kind': 'kit', 'shape': 'box', 'size': [0.0022, 0.001, 0.009], 'position': [x + dx, BACK - 0.0101, zc - 0.001],
                        'material': 'clay', 'color': '#1A1918', 'roughness': 0.8})
        out.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.0022, 'height': 0.001, 'position': [x, BACK - 0.0101, zc - 0.009],
                    'rotate': [90.0, 0, 0], 'material': 'clay', 'color': '#1A1918', 'roughness': 0.8})
    return out


def _cables():
    """Each Tropos's mains lead from its back, low, down to the floor and out along the skirting to a socket beside it,
    in frame; Mantle's two signal leads from the console's back, down its ends and across the floor to each speaker's
    back. Points in metres (the cable's position is the origin)."""
    out = []
    by = SPK_Y + TROPOS_D / 2 + 0.03               # just behind each cabinet
    for sx, sock in ((-1, SOCKETS[0]), (1, SOCKETS[1])):
        x = sx * SPK_X
        # (the critics: the cords stopped short of blank plates) from the plug, pushed into the lower receptacle, down and
        # along the skirting to the speaker's back; the plug's moulded head on the first 45 mm
        zr = SOCKET_Z + 0.032
        out.append({'kind': 'cable', 'position': [0, 0], 'd': 0.008, 'color': '#141414',
                    'points': [[sock, BACK - 0.011, zr], [sock, BACK - 0.05, zr - 0.01], [sock, BACK - 0.04, 0.1], [sock - sx * 0.12, BACK - 0.03, 0.004],
                               [x + sx * 0.34, BACK - 0.06, 0.004], [x + sx * 0.16, by + 0.04, 0.004], [x + sx * 0.1, by, 0.14]],
                    'plug': [0.045, 0.018]})
        out += _socket(sock)
        ex = sx * (CONSOLE['w'] / 2 + 0.03)             # down the console's end, against the wall
        out.append({'kind': 'cable', 'position': [0, 0], 'd': 0.005, 'color': '#1A1A1A',
                    'points': [[MANTLE[0] + sx * 0.05, BACK - 0.04, TOP - 0.01], [ex, BACK - 0.03, TOP - 0.05], [ex, BACK - 0.03, 0.2],
                               [ex + sx * 0.04, BACK - 0.06, 0.003], [x - sx * 0.16, by + 0.02, 0.003], [x - sx * 0.1, by, 0.14]]})
    return out


def _life():
    """Books on the console's left end, a stack of records leaning at its right side on the floor, a plant in the
    window's corner, the chair."""
    # (at 1.8 m the console's end is 7 cm from the speaker: the records lean against its front, at the right door)
    # (the coordinator, 22:03: the invented covers (03, 11, 06, 13) put a second strong colour beside the pair: plain
    # card sleeves, unprinted kraft and dark matte, in the same stack)
    sleeves = [{'card': col, 'w': 0.315, 'h': 0.315, 't': 0.004, 'x': 0.58 - 0.015 * j,
                'y': CON_Y - CONSOLE['d'] / 2 - 0.075 + 0.012 * j, 'z': 0.0, 'rot': [12.0 - 2.5 * j, 0, 3.0 * j - 2.0], 'rough': 0.8}
               for j, col in enumerate(('#CDBB9C', '#26221F', '#BFA987', '#1F1D1B'))]
    # (the A critics: Mantle's polished top, seen nearly edge-on, mirrored the white wall behind it and read grey, C* 6:
    # two dark sleeves leaning on the wall behind it, on the console, where its top looks; their faces the darkest covers)
    # (the light-model test: covers 08 and 12 carry bright graphics, busy behind Mantle and only half dark: plain dark
    # card sleeves instead, matte)
    # (the A critics, round 2: they read as one flat board, no card edge, no lit top, and swallowed the deck's back edge:
    # card sleeves, their edges rounded 1.5 mm so the top catches the light, a paper grain; the right one 6 cm further
    # right, clear of the deck)
    dark = [{'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'plain_sleeves',
             'boards': [{'card': col, 'w': 0.315, 'h': 0.315, 't': 0.004, 'ease': 0.0015, 'grain': 0.4, 'rough': 0.8,
                         'x': MANTLE[0] + dx, 'y': BACK - 0.077, 'z': TOP + 0.0005, 'rot': [-8.0, 0, rz]}
                        for dx, rz, col in ((-0.17, -3.0, '#1F1D1B'), (0.20, 2.0, '#26221F'))]}]
    return [
        # one quiet print above the console, hung at eye height over it (muted, so the pair keeps the colour)
        {'kind': 'frame', 'position': [0.05, BACK - 0.012], 'z': 1.58, 'size': [0.62, 0.78],
         'artwork': {'bands': [['#D8D0C2', 0.45], ['#9C9384', 0.3], ['#CBC2B2', 0.25]], 'ground': '#E8E2D7', 'seed': 21}},
        {'kind': 'books', 'position': [-0.6, CON_Y], 'z': TOP, 'colors': ['#3E4A5C', '#B9A27A', '#7A2E2A', '#D8D2C4'], 'seed': 5},
        {'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'plain_sleeves', 'boards': sleeves}, *dark,
        {'kind': 'kit', 'shape': 'asset', 'model': 'potted_plant_02', 'res': '2k', 'position': [-2.3, 0.45, 0.0], 'rotate': [0, 0, 20.0]},
        {'kind': 'kit', 'shape': 'asset', 'model': 'sofa_02', 'res': '2k', 'position': [CHAIR[0], CHAIR[1], 0.0],
         'rotate': [0, 0, CHAIR[2]]},
    ]


WATER = 0.06                                    # the water's height in the 92 mm glass (the A critics, round 2: it read empty)


def _side_table():
    """The side table, a book (cloth boards) and a rocks glass of water on it."""
    x, y, _ = SIDE; T = SIDE_TOP
    RK = [[0, 0], [0.041, 0], [0.043, 0.006], [0.044, 0.092]]
    return [{'kind': 'kit', 'shape': 'asset', 'model': 'side_table_01', 'res': '2k', 'position': [x, y, 0.0], 'rotate': [0, 0, 0.0]},
            *_book(x + 0.1, y + 0.07, T + 0.0005, 14.0),
            LB.lathe(LB.shell(RK, 0.0035, 0.016), [x + 0.13, y - 0.1, T + 0.0005], 'glass', '#F8F8F6', 64),
            LB.lathe(LB.contents(RK, WATER, 0.0035, 0.016), [x + 0.13, y - 0.1, T + 0.0005], 'glass', '#EEF3F4', 64)]


def _book(x, y, z, rz, w=0.155, d=0.235, h=0.028, cloth='#4F6253'):
    """A clothbound book lying flat: two boards 2.5 mm, the spine along its left edge, and the page block between
    them, cream, set in 3 mm at the head, the tail and the fore-edge (the critics: a solid box had no pages)."""
    import math
    c, s_ = math.cos(math.radians(rz)), math.sin(math.radians(rz))
    at = lambda u, v: [round(x + u * c - v * s_, 5), round(y + u * s_ + v * c, 5)]
    cl = {'material': 'cotton', 'color': cloth}
    t = 0.0025
    return [{'kind': 'kit', 'shape': 'box', 'size': [w, d, t], 'position': [*at(0, 0), z], 'rotate': [0, 0, rz], 'ease': 0.0008, **cl},
            {'kind': 'kit', 'shape': 'box', 'size': [w - 0.004, d - 0.006, h - 2 * t - 0.0004], 'position': [*at(-0.001, 0), z + t + 0.0002],
             'rotate': [0, 0, rz], 'material': 'paper', 'color': '#EFE8D6', 'ease': 0.0005},
            {'kind': 'kit', 'shape': 'box', 'size': [w, d, t], 'position': [*at(0, 0), z + h - t], 'rotate': [0, 0, rz], 'ease': 0.0008, **cl},
            {'kind': 'kit', 'shape': 'box', 'size': [0.004, d, h - 0.0002], 'position': [*at(-w / 2 + 0.002, 0), z + 0.0001],
             'rotate': [0, 0, rz], 'ease': 0.0015, **cl}]


def _sleeve_plain():
    """Camera B: a plain sleeve (unprinted kraft card) leaning against the wall on the console, right of Mantle."""
    return {'kind': 'kit', 'shape': 'box', 'size': [0.315, 0.004, 0.315], 'position': [MANTLE[0] + 0.42, CON_Y + 0.165, TOP + 0.0005],
            'rotate': [-10.0, 0, 0], 'material': 'paper', 'color': '#CDBB9C', 'ease': 0.001}


def _cores(tint):
    return {'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'cores_off', 'core_load': shots.CORE_LOAD, 'core_cable': False,
            'cores': [{'tint': shots.KEY[tint], 'x': CORE[0], 'y': CORE[1], 'floor_z': CORE[2], 'rot': 0.0}]}


def base(tint='ember', size=(2400, 1600)):
    s = shots._cast_base()
    k = shots.HERO_ORDER.index(tint)
    pair = []
    for blk in s['products']:
        i = blk['instances'][k]
        pair.append({**blk, 'instances': [{**copy.deepcopy(i), 'position': [sx * SPK_X, SPK_Y, 0.0], 'rotate_z': -sx * TOE}
                                          for sx in (-1, 1)]})
    s['products'] = pair
    shots._approved(s, order=[tint, tint])
    s['products'].append(shots._mantle(MANTLE[0], MANTLE[1], MANTLE[2], MANTLE[3], tint=tint))
    s['set'] = {'kind': 'room', 'size': [W, D, H], 'center': [CX, CY],
                'wall': {'color': '#E6E0D5'}, 'ceiling': '#EFECE6', 'frame': STEEL, 'skirting': {'h': 0.09, 'color': '#E3DED4'},
                'windows': [WIN_BACK, WIN_LEFT, WIN_FRONT, WIN_RIGHT],
                'props': [_floor()] + _rug() + _console() + _window_bars() + _cables() + _life() + _side_table() + [_cores(tint),
                          {'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'no_portal', 'windows': ['wall-back']},
                          # (the A critics, round 2: the sofa read as rubber, its outline faceted: subdivided, a sheen, a nap)
                          {'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'soft_fabric', 'prefixes': ['sofa_02'], 'levels': 2,
                           'sheen': 0.3, 'sheen_rough': 0.5, 'sheen_tint': 0.45, 'weave_mm': 0.8, 'weave_depth': 0.2},
                          # (the coordinator, 19:45: one light model: caustics on, the acrylics' glass-shadow shortcut off)
                          {'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'no_glass_shadows'}]}
    s.pop('haze', None)
    s.pop('sun', None)
    s['sky'] = dict(SKY)
    s['lights'] = {}
    s['materials'] = {k: v for k, v in s.get('materials', {}).items() if k != 'sweep'}
    s['size'] = list(size)
    # (the critics, 18:41: the Core read as a dark mirror ball, its opal core unseen. Daylight reaches the opal only by
    # refracting through the tinted shell, a caustic path; off by the engine's default, on in every lamps-lane frame.
    # On: the opal shows, and the cabinets' fronts deepen, C* 38.7 to 50.0 in a region test)
    s['render'] = {**s['render'], 'caustics_refractive': True, 'caustics_reflective': True,
                   'samples': 128, 'adaptive': 0.01, 'denoise': True, 'clamp': 0, 'view': 'AgX', 'look': 'AgX - Base Contrast',
                   'exposure': 5.35, 'white_balance_k': 5600, 'white_balance_tint': 0.0}
    s.pop('finish', None)
    return s


def living_a(tint='ember', size=(2400, 1600)):
    """Camera A, wide, from the listening seat: the pair, the console and Mantle between, the Core off at its end, the
    chair's back at the foot, the corner window at the left."""
    s = base(tint, size)
    s['title'] = f'Living room by day: the pair from the listening seat ({tint})'
    s['camera'] = dict(CAM_A)
    return s


def living_b(tint='ember', size=(1600, 2000)):
    """Camera B, close on the console: Mantle whole and in focus, a record on, a plain sleeve leaning beside it; its
    plinth in the sun's band from the window's edge. 4:5."""
    s = base(tint, size)
    s['title'] = f'Living room by day: Mantle on the console ({tint})'
    s['set']['props'].append(_sleeve_plain())
    for pr in s['set']['props']:                        # (test 2: the Core half cut by the right edge: 15 cm right, out of frame)
        if pr.get('fn') == 'cores_off':
            pr['cores'] = [{**pr['cores'][0], 'x': CORE[0] + 0.15}]
    # (test: Mantle's origin is not its middle; at x +0.06 it ran 130 px past the right edge: aimed 0.19 m right, wider)
    tgt = [MANTLE[0] + 0.25, MANTLE[1], TOP + 0.09]
    s['camera'] = {'position': [0.5, 0.3, 1.02], 'target': tgt, 'lens_mm': 48.0, 'level': True, 'fstop': 5.6, 'focus': tgt}
    return s


def living_c(tint='ember', size=(1600, 2000)):
    """Camera C: the Core switched off on the side table by the window, beside a book and a glass, the sun from the
    left and the window behind it, so it reads as glass. 4:5."""
    s = base(tint, size)
    s['title'] = f'Living room by day: Core on the side table, switched off ({tint})'
    for pr in s['set']['props']:
        if pr.get('fn') == 'cores_off':
            pr['cores'] = [{**pr['cores'][0], 'x': CORE_C[0], 'y': CORE_C[1], 'floor_z': CORE_C[2]}]
    for pr in s['set']['props']:                        # (final C: the left window is in this frame: no portal in it either)
        if pr.get('fn') == 'no_portal':
            pr['windows'] = ['wall-back', 'wall-left']
    tgt = [CORE_C[0] + 0.05, CORE_C[1], SIDE_TOP + 0.1]
    s['camera'] = {'position': [-1.45, 0.6, 0.98], 'target': tgt, 'lens_mm': 60.0, 'level': True, 'fstop': 4.0, 'focus': [CORE_C[0], CORE_C[1], SIDE_TOP + 0.08]}
    return s


FINAL = dict(samples=256, adaptive=0.005)     # (the coordinator, 12:30: crisp insides; a crop at 128 and 384 both crisp)


def _final(f):
    def g(tint='ember'):
        s = f(tint); s['render'].update(FINAL); return s
    return g


def _small(f, size):
    def g(tint='ember'):
        s = f(tint, size); s['render'].update(samples=48, adaptive=0.02); return s
    return g


def proof_a(tint='ember'):
    s = living_a(tint, (1500, 1000))
    s['render'].update(samples=48, adaptive=0.02)
    return s


SHOTS = {'living-a-proof': proof_a, 'living-a': _final(living_a), 'living-b': _final(living_b), 'living-c': _final(living_c),
         'living-b-test': _small(living_b, (800, 1000)), 'living-c-test': _small(living_c, (800, 1000))}

if __name__ == '__main__':
    od = sys.argv[1]
    tint = sys.argv[2] if len(sys.argv) > 2 else 'ember'
    os.makedirs(od, exist_ok=True)
    for n, f in SHOTS.items():
        json.dump(f(tint), open(os.path.join(od, f'{n}-{tint}.json'), 'w'), indent=1)
        print(n, tint)
