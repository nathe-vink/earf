"""Room 31: a pair of Poison at home, photographed as a design magazine would shoot it (the coordinator's brief,
2026-10-18; NOTES.md logs every pass).

    python3 spinoffs/barkhorn/room31/room.py            # writes studio/shots/barkhorn/room31/room.json, room-portrait.json
    python3 studio/engine/render.py studio/shots/barkhorn/room31/room.json --out IMG [--samples N --scale S]

One light idea: late-afternoon sun low through the tall glazing of the left wall, from in front of the pair, so it
crosses the floor, falls on both speakers alike, passes through their tinted acrylic and lays their green shadows on
the plaster behind; a sun-free window off to the right (out of frame) fills the shade side. The view out of the glazing
is a photographed place (an exterior plate the camera sees and the room is not lit by). The surfaces are photographed:
oak boards, plaster, a deep-pile wool rug, a scanned lounge chair; the credenza is walnut veneer, bookmatched, built
here (pieces.py); the record player is EARF's own, Cumulus, in Fog.

The frame is the engine's: metres, z up, the speakers' fronts toward -y, the back wall at y = BACK.
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'room31')
PIECES = os.path.relpath(os.path.join(HERE, 'pieces.py'), ROOT)

# --- the room ------------------------------------------------------------------------------------------------------
BACK = 0.95                      # the back wall's face (y)
LEFT = -2.05                     # the glazed left wall's face (x)
RIGHT = 3.75
DEPTH = 7.0
HEIGHT = 2.9
SPK_X, SPK_Y, TOE = 1.2, 0.30, 4.0          # the pair: centres at +-x, toe-in (deg)
CAB = dict(x=-0.0, w=1.62, d=0.44, h=0.56)  # the credenza (back to the wall)


def ext(fn, **k):
    return {'kind': 'kit', 'shape': 'ext', 'path': PIECES, 'fn': fn, **k}


def kit(shape, **k):
    return {'kind': 'kit', 'shape': shape, **k}


def _rot(p, deg):
    a = math.radians(deg); x, y = p
    return (x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a))


def lead(side, socket_x, socket_z=0.30):
    """A speaker's mains lead: out of its amp box (on its back, 419 mm up), down behind it to the floor, along the foot
    of the back wall and up into the plug at the socket. side -1 left, +1 right."""
    cx, toe = side * SPK_X, -side * TOE
    def L(lx, ly, z):                                         # a point in the speaker's own frame -> world
        dx, dy = _rot((lx, ly), toe)
        return [round(cx + dx, 4), round(SPK_Y + dy, 4), z]
    yw = BACK - 0.012                                         # along the skirting's foot
    sx = socket_x
    pts = [[sx, BACK - 0.037, socket_z - 0.03], [sx, BACK - 0.04, socket_z - 0.09], [sx, yw - 0.004, 0.06],
           [sx, yw - 0.006, 0.0036]]
    run_to = cx + side * 0.06
    pts += [[round((sx + run_to) / 2, 4), yw - 0.008, 0.0036], [run_to, yw - 0.012, 0.0036],
            [cx, BACK - 0.12, 0.0036]]
    pts += [L(0.0, 0.33, 0.0036), L(0.0, 0.282, 0.06), L(0.0, 0.272, 0.26), L(0.0, 0.258, 0.40), L(0.0, 0.2097, 0.419)]
    return {'kind': 'cable', 'position': [0.0, 0.0], 'points': pts, 'd': 0.0075, 'plug': [0.05, 0.024], 'per': 10}


def room_set(v):
    w = RIGHT - LEFT; cx = (RIGHT + LEFT) / 2; cy = BACK - DEPTH / 2
    # the left wall runs front (y = BACK - DEPTH) to back; `along` is from its centre
    def along(y):
        return round(y - cy, 3)
    # a run of tall French windows down the left wall, piers between, glass to 15 cm under the ceiling
    wins = [{'wall': 'left', 'along': along(yc), 'sill': 0.04, 'size': [1.45, 2.71], 'mullions': [2, 1], 'frame': '#2B2926'}
            for yc in v.get('win_y', (0.0, -1.6, -3.2))]
    props = [
        ext('floor', rect=[LEFT, BACK - DEPTH, RIGHT, BACK], texture=v['floor'], res='4k', rotate_deg=v['floor_rot'],
            rough_mul=v.get('floor_rough', 1.0), coat=v.get('floor_coat', 0.35), coat_rough=0.35, value=v.get('floor_value', 1.0),
            offset=[0.37, 0.11, 0.0]),
        ext('plaster', texture=v['plaster'], res='4k', color=v['wall'], tint_mix=v.get('wall_tint', 0.85),
            value=v.get('wall_value', 1.0), bump=v.get('wall_bump', 1.0)),
        ext('credenza', position=[CAB['x'], BACK - CAB['d'] / 2 - 0.012], size=[CAB['w'], CAB['d'], CAB['h']], doors=3,
            texture=v.get('veneer', 'walnut_veneer'), lift=v.get('veneer_lift', 1.3)),
        ext('rug', position=[0.0, -1.55], size=[3.0, 2.3], pile=0.018, texture=v.get('rug', 'curly_teddy_natural'),
            tint=v.get('rug_tint', '#E4DCCB'), tint_mix=v.get('rug_tint_mix', 0.5), displace=0.006, res='2k'),
        ext('socket', position=[-v['socket_x'], BACK, 0.30]),
        ext('socket', position=[v['socket_x'], BACK, 0.30]),
        lead(-1, -v['socket_x']), lead(1, v['socket_x']),
        ext('books', position=[0.42, BACK - 0.24, CAB['h']], seed=4, books=[
            # invented titles and imprints (no real books or publishers on a campaign prop)
            [0.31, 0.24, 0.032, '#3E4A57', '#D9D2C2', 'ROOMS IN LATE LIGHT', 'HALDEN'],
            [0.27, 0.21, 0.026, '#C9BBA2', '#3A332C', 'On Listening', 'NORTH PRESS'],
            [0.24, 0.19, 0.022, '#7A3A2C', '#E8DCC8', 'The Shape of Sound', 'ESSAYS'],
        ]),
        kit('asset', model=v.get('vase', 'ceramic_vase_02'), position=[0.60, BACK - 0.20, CAB['h']], rotate=[0, 0, 20],
            scale=v.get('vase_scale', 1.0)),
        kit('asset', model=v.get('chair', 'modern_arm_chair_01'), position=v['chair_pos'], rotate=[0, 0, v['chair_rot']],
            scale=1.0),
        ext('exterior', hdri=v['hdri'], rotation_deg=v['hdri_rot'], strength=v['ext_strength'], res='8k',
            centre=[LEFT - 1.0, -1.0, 1.4], radius=60.0, blur=v.get('ext_blur', 0.004)),
    ]
    return {'kind': 'room', 'size': [w, DEPTH, HEIGHT], 'center': [cx, cy],
            'floor': {'base': '#B89B78'}, 'wall': {'color': v['wall']}, 'ceiling': '#F2EFEA',
            'skirting': {'h': 0.09, 'color': v['wall'], 't': 0.014}, 'frame': '#2B2926', 'windows': wins, 'props': props}


DEFAULT = dict(
    floor='laminate_floor_02', floor_rot=90.0, plaster='beige_wall_001', wall='#E8E2D8', wall_value=1.3, socket_x=1.78,
    veneer_lift=0.85, rug_tint='#CFC2A8', rug_tint_mix=0.7,
    chair='modern_arm_chair_01', chair_pos=[1.85, -1.05, 0.0], chair_rot=200.0,
    hdri='autumn_forest_04', hdri_rot=0.0, ext_strength=2.2,
    sun=dict(azimuth_deg=-58.0, elevation_deg=18.0, irradiance=14.0, angle_deg=0.6, color='#FFE6C4'),
    sky_strength=0.6, fill=0.6, exposure=-0.2,
)


def shot(v=None, portrait=False):
    v = {**DEFAULT, **(v or {})}
    s = {
        'title': 'barkhorn, Poison, at home (room 31)',
        'products': [
            {'def': 'studio/products/barkhorn-cloud.json', 'flavour': 'eucalyptus-y2k-green',
             'instances': [{'flavour': 'eucalyptus-y2k-green', 'position': [-SPK_X, SPK_Y, 0.0], 'rotate_z': TOE},
                           {'flavour': 'eucalyptus-y2k-green', 'position': [SPK_X, SPK_Y, 0.0], 'rotate_z': -TOE}]},
            {'def': 'studio/products/barkhorn-turntable.json', 'flavour': v.get('tt_flavour', 'fog'),
             'instances': [{'flavour': v.get('tt_flavour', 'fog'), 'position': [-0.30, BACK - 0.012 - CAB['d'] / 2 - 0.01, CAB['h']],
                            'rotate_z': 0.0}]},
        ],
        'set': room_set(v),
        'sun': dict(v['sun']),
        'sky': {'kind': 'physical', 'strength': v['sky_strength'], 'air': 1.0, 'dust': 1.5},
        'lights': {
            'key': {'off': True}, 'fill': {'off': True}, 'wash': {'off': True},
            # the sun-free window off to the right, out of frame: the shade side's soft light
            'north': {'type': 'area', 'size_m': [2.2, 2.4], 'position': [RIGHT - 0.05, -1.2, 1.4],
                      'target': [0.0, 0.2, 0.9], 'irradiance': v['fill'], 'color': '#EEF2F8'},
        },
        'render': {'samples': 128, 'adaptive': 0.02, 'denoise': True, 'clamp': 10, 'bounces': 12,
                   'view': 'Khronos PBR Neutral', 'exposure': v['exposure'], 'white_balance_k': v.get('wb', 5600),
                   'white_balance_tint': v.get('wb_tint', 4.0)},
    }
    if not portrait:
        s['size'] = [2880, 1620]
        s['camera'] = {'position': [0.0, SPK_Y - 5.06, 1.05], 'target': [0.0, SPK_Y, 0.855], 'lens_mm': 40, 'level': True,
                       'fstop': 5.6, 'focus': [0.0, SPK_Y - 0.21, 0.7]}
    else:
        s['size'] = [1600, 2000]
        s['camera'] = {'position': [0.0, SPK_Y - 6.2, 1.05], 'target': [0.0, SPK_Y, 1.05], 'lens_mm': 40, 'level': True,
                       'fstop': 5.6, 'focus': [0.0, SPK_Y - 0.21, 0.7]}
    return s


def write(v=None, tag=''):
    os.makedirs(OUT, exist_ok=True)
    for name, port in (('room', False), ('room-portrait', True)):
        p = os.path.join(OUT, f'{name}{tag}.json')
        json.dump(shot(v, port), open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    write()
