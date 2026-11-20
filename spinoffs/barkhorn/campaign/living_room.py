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

EXT = 'spinoffs/barkhorn/campaign/living/living_ext.py'
LIFE = 'spinoffs/barkhorn/campaign/bar_life/bar_life.py'
LAMPS = 'spinoffs/barkhorn/campaign/stage/stage2_props.py'

# --- the room -----------------------------------------------------------------------------------------------------
W, D, H = 5.4, 6.0, 2.75                        # a living room, 5.4 x 6.0 m, 2.75 m ceiling
CX, CY = 0.0, -1.0                              # its floor's centre: x -2.7..2.7, y -4..2
BACK = CY + D / 2                               # the back wall's face, y = 2.0
LEFT = CX - W / 2                               # the left wall's face, x = -2.7
WIN_BACK = {'wall': 'back', 'along': -1.95, 'sill': 0.42, 'size': [0.85, 1.95], 'mullions': [1, 3]}   # in frame, at the left
WIN_LEFT = {'wall': 'left', 'along': 0.35, 'sill': 0.42, 'size': [1.5, 1.95], 'mullions': [2, 3]}     # out of frame: the sun's way in
WIN_FRONT = {'wall': 'front', 'along': 0.0, 'sill': 0.42, 'size': [2.2, 1.95], 'mullions': [3, 3]}   # behind the lens: the sky from the front
SKY = {'kind': 'hdri', 'polyhaven': 'garden_nook', 'res': '4k', 'rotation_deg': 101.2, 'strength': 1.0}
# (assets.py sun garden_nook: azimuth 54.2 - rotation, elevation 25.9: at 101.2 the sun comes from the front left,
# azimuth -47, through the left window onto the floor at the left speaker's front)

# --- the furniture --------------------------------------------------------------------------------------------------
SPK_X, SPK_GAP, TOE = 1.25, 0.30, 6.0           # the pair 2.5 m apart, 0.3 m off the wall, toed in
TROPOS_D = 0.428
SPK_Y = round(BACK - SPK_GAP - TROPOS_D / 2, 4)
CONSOLE = {'w': 1.5, 'd': 0.45, 'h': 0.64}
CON_Y = round(BACK - 0.06 - CONSOLE['d'] / 2, 4)
TOP = CONSOLE['h']
MANTLE = (-0.24, CON_Y - 0.02, TOP + 0.001, 0.0)
CORE = (0.5, CON_Y - 0.04, TOP)
SOCKETS = (-1.85, 2.1)                          # the two outlets, either side of the pair, in frame
CHAIR = (-0.15, -1.6, 180.0)                    # its back to the lens, across the frame's foot, below the speakers' feet
CAM_A = {'position': [0.1, -3.05, 1.5], 'target': [0.0, 1.6, 1.0], 'lens_mm': 32.0, 'level': True, 'fstop': 8.0,
         'focus': [0.0, 1.3, 0.9]}


def _floor():
    # real oak planks over the room's own floor, a hair above it (Cycles: coplanar faces render black)
    return {'kind': 'kit', 'shape': 'box', 'size': [W - 0.02, D - 0.02, 0.003], 'position': [CX, CY, 0.0005],
            'material': 'pbr', 'texture': 'oak_wood_planks', 'tex_res': '2k', 'gain': 1.0}


def _rug():
    return {'kind': 'kit', 'shape': 'box', 'size': [2.4, 1.7, 0.009], 'position': [0.0, 0.15, 0.0045],
            'material': 'pbr', 'texture': 'poly_wool_herringbone', 'tex_res': '2k', 'tint': '#C8B597', 'tint_mix': 0.6, 'gain': 1.1, 'ease': 0.003}


def _console():
    return {'kind': 'sideboard', 'position': [0.0, CON_Y], 'size': [CONSOLE['w'], CONSOLE['d'], CONSOLE['h']], 'wood': 'veneer',
            'color': '#6E4A32', 'grain': 0.3, 'turntable': False}


def _socket(x):
    # a white duplex outlet on the back wall above the skirting
    return {'kind': 'kit', 'shape': 'box', 'size': [0.07, 0.012, 0.115], 'position': [x, BACK - 0.006, 0.28],
            'material': 'satin', 'color': '#ECEAE4', 'ease': 0.002}


def _cables():
    """Each Tropos's mains lead from its back, low, down to the floor and out along the skirting to a socket beside it,
    in frame; Mantle's two signal leads from the console's back, down its ends and across the floor to each speaker's
    back. Points in metres (the cable's position is the origin)."""
    out = []
    by = SPK_Y + TROPOS_D / 2 + 0.03               # just behind each cabinet
    for sx, sock in ((-1, SOCKETS[0]), (1, SOCKETS[1])):
        x = sx * SPK_X
        out.append({'kind': 'cable', 'position': [0, 0], 'd': 0.008, 'color': '#141414',
                    'points': [[x + sx * 0.1, by, 0.14], [x + sx * 0.16, by + 0.04, 0.004], [x + sx * 0.34, BACK - 0.06, 0.004],
                               [sock - sx * 0.12, BACK - 0.03, 0.004], [sock, BACK - 0.03, 0.12], [sock, BACK - 0.014, 0.25]],
                    'plug': [0.05, 0.016]})
        out.append(_socket(sock))
        ex = sx * (CONSOLE['w'] / 2 + 0.03)             # down the console's end, against the wall
        out.append({'kind': 'cable', 'position': [0, 0], 'd': 0.005, 'color': '#1A1A1A',
                    'points': [[MANTLE[0] + sx * 0.05, BACK - 0.04, TOP - 0.01], [ex, BACK - 0.03, TOP - 0.05], [ex, BACK - 0.03, 0.2],
                               [ex + sx * 0.04, BACK - 0.06, 0.003], [x - sx * 0.16, by + 0.02, 0.003], [x - sx * 0.1, by, 0.14]]})
    return out


def _life():
    """Books on the console's left end, a stack of records leaning at its right side on the floor, a plant in the
    window's corner, the chair."""
    sleeves = [{'image': f'tex/cover-{k:02d}.png', 'w': 0.315, 'h': 0.315, 't': 0.004, 'x': CONSOLE['w'] / 2 + 0.06 + 0.012 * j,
                'y': CON_Y - 0.1 + 0.02 * j, 'z': 0.0, 'rot': [-12.0 + 3 * j, 0, 90.0 + 4 * j], 'ground': '#E9E3D6', 'rough': 0.7}
               for j, k in enumerate((3, 11, 6, 13))]
    return [
        # one quiet print above the console, hung at eye height over it (muted, so the pair keeps the colour)
        {'kind': 'frame', 'position': [0.05, BACK - 0.012], 'z': 1.58, 'size': [0.62, 0.78],
         'artwork': {'bands': [['#D8D0C2', 0.45], ['#9C9384', 0.3], ['#CBC2B2', 0.25]], 'ground': '#E8E2D7', 'seed': 21}},
        {'kind': 'books', 'position': [-0.6, CON_Y], 'z': TOP, 'colors': ['#3E4A5C', '#B9A27A', '#7A2E2A', '#D8D2C4'], 'seed': 5},
        {'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'boards', 'boards': sleeves},
        {'kind': 'kit', 'shape': 'asset', 'model': 'potted_plant_02', 'res': '2k', 'position': [-2.38, 1.45, 0.0], 'rotate': [0, 0, 20.0]},
        {'kind': 'kit', 'shape': 'asset', 'model': 'mid_century_lounge_chair', 'res': '2k', 'position': [CHAIR[0], CHAIR[1], 0.0],
         'rotate': [0, 0, CHAIR[2]]},
    ]


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
                'wall': {'color': '#E6E0D5'}, 'ceiling': '#EFECE6', 'skirting': {'h': 0.09, 'color': '#E3DED4'},
                'windows': [WIN_BACK, WIN_LEFT, WIN_FRONT],
                'props': [_floor(), _rug(), _console()] + _cables() + _life() + [_cores(tint),
                          {'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'no_portal', 'windows': ['wall-back']}]}
    s.pop('haze', None)
    s.pop('sun', None)
    s['sky'] = dict(SKY)
    s['lights'] = {}
    s['materials'] = {k: v for k, v in s.get('materials', {}).items() if k != 'sweep'}
    s['size'] = list(size)
    s['render'] = {**s['render'], 'samples': 128, 'adaptive': 0.01, 'denoise': True, 'clamp': 0, 'view': 'AgX', 'look': 'AgX - Base Contrast',
                   'exposure': 2.8, 'white_balance_k': 5600, 'white_balance_tint': 0.0}
    s.pop('finish', None)
    return s


def living_a(tint='ember', size=(2400, 1600)):
    """Camera A, wide, from the listening seat: the pair, the console and Mantle between, the Core off at its end, the
    chair's back at the foot, the corner window at the left."""
    s = base(tint, size)
    s['title'] = f'Living room by day: the pair from the listening seat ({tint})'
    s['camera'] = dict(CAM_A)
    return s


def proof_a(tint='ember'):
    s = living_a(tint, (1500, 1000))
    s['render'].update(samples=48, adaptive=0.02)
    return s


SHOTS = {'living-a-proof': proof_a, 'living-a': living_a}

if __name__ == '__main__':
    od = sys.argv[1]
    tint = sys.argv[2] if len(sys.argv) > 2 else 'ember'
    os.makedirs(od, exist_ok=True)
    for n, f in SHOTS.items():
        json.dump(f(tint), open(os.path.join(od, f'{n}-{tint}.json'), 'w'), indent=1)
        print(n, tint)
