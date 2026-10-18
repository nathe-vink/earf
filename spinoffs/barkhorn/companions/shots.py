"""Round 31's companion shots for the engine: each product in the eight Atmosphere colours on the look book's sweep
(lookbook21's sweep colour for each, its key, fill and wash), a hero of each beside a Cloud in the same colour, and a
detail of each. Writes studio/shots/barkhorn/companions/*.json; render them with

    python3 spinoffs/barkhorn/companions/shots.py                     # the shot files
    python3.11 studio/engine/render.py studio/shots/barkhorn/companions/look-turntable-ember.json \
        --out renders/2026-10-18/barkhorn/companions/look-turntable-ember.png

(bpy needs the Python it was installed for: the system's, or python3.11 where the system's is newer).
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import common as C                                                  # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'companions')
TT = 'studio/products/barkhorn-turntable.json'
LAMP = 'studio/products/barkhorn-lamp.json'
CLOUD = 'studio/products/barkhorn-cloud.json'
# the turntable's spindle in the engine's frame (its CAD point less the product file's origin, metres), and the
# platter's top: a record goes there
SPINDLE = (round((218.0 - 241.6) / 1000, 4), round((170.0 - 186.5) / 1000, 4)); PLATTER_TOP = 0.095
LED = 22.0                                                         # the strip's emission when the lamp is on


def orbit(tgt, az, el, dist):
    a, e = math.radians(az), math.radians(el)
    return [round(tgt[0] + dist * math.cos(e) * math.sin(a), 4), round(tgt[1] - dist * math.cos(e) * math.cos(a), 4),
            round(tgt[2] + dist * math.sin(e), 4)]


def lights(tgt, scale=1.0, dist=4.0):
    return {'key': {'type': 'area', 'size_m': [2.5, 2.0], 'orbit': {'azimuth_deg': -35, 'elevation_deg': 40, 'distance_m': dist},
                    'target': tgt, 'irradiance': round(2.2 * scale, 3), 'color': '#FFF3E1'},
            'fill': {'type': 'area', 'size_m': [3.0, 2.5], 'orbit': {'azimuth_deg': 30, 'elevation_deg': 18, 'distance_m': dist},
                     'target': tgt, 'irradiance': round(1.0 * scale, 3), 'color': '#FFF7EA'},
            'wash': {'type': 'area', 'size_m': [5.0, 1.0], 'position': [0.0, -1.0, 2.9], 'target': [0.0, 0.5, 1.2],
                     'irradiance': round(0.8 * scale, 3), 'color': '#FFF7EA'},
            'rim': {'type': 'area', 'size_m': [3.0, 0.8], 'position': [0.5, 1.8, 1.3], 'target': tgt,
                    'irradiance': round(1.2 * scale, 3), 'color': '#FFF7EA'}}


def base(title, size, colour, cam, sweep=None):
    return {'title': title, 'size': size,
            'set': {'kind': 'sweep', 'color': sweep or C.SWEEP[colour], 'width': 9.0, 'front': 5.0, 'depth': 1.5, 'radius': 1.2, 'height': 5.0},
            'camera': cam,
            'sky': {'kind': 'gradient', 'zenith': '#C4C2BE', 'horizon': '#CFCDC8', 'ground': '#5A5650', 'strength': 0.7},
            'render': {'samples': 64, 'adaptive': 0.02, 'denoise': True, 'clamp': 8, 'bounces': 12, 'view': 'Khronos PBR Neutral',
                       'exposure': 0.0, 'white_balance_k': 5600, 'white_balance_tint': 3.0}}


def record(x, y, z, colour):
    """A black LP on the platter, its label in the colour's accent."""
    acc = next(c[4] for c in C.COLOURS if c[0] == colour)
    return [{'kind': 'kit', 'shape': 'cylinder', 'material': 'gloss', 'color': '#0D0D0E', 'radius': 0.1505, 'height': 0.0018,
             'position': [x, y, z], 'segments': 128},
            {'kind': 'kit', 'shape': 'cylinder', 'material': 'paper', 'color': acc, 'radius': 0.05, 'height': 0.0003,
             'position': [x, y, z + 0.0018], 'segments': 96}]


def look_turntable(colour):
    tgt = [0.0, 0.02, 0.06]
    s = base(f'Cumulus in {C.NAMES[colour]}', [1200, 900], colour,
             {'position': orbit(tgt, -30, 27, 1.32), 'target': tgt, 'lens_mm': 70, 'level': True})
    s['product'] = {'def': TT, 'flavour': colour, 'instances': [{'position': [0, 0, 0], 'rotate_z': 0}]}
    s['lights'] = lights(tgt)
    return s


def look_lamp(colour, on=True):
    tgt = [0.0, 0.0, 0.25]
    s = base(f'Bell in {C.NAMES[colour]}', [960, 1200], colour,
             {'position': orbit(tgt, -24, 7, 1.6), 'target': tgt, 'lens_mm': 70, 'level': True})
    s['product'] = {'def': LAMP, 'flavour': colour, 'instances': [{'position': [0, 0, 0], 'rotate_z': 0}]}
    s['lights'] = lights(tgt)
    s['materials'] = {'led': {'strength': LED if on else 0.0}}
    return s


def sideboard(x, w=1.0, h=0.56):
    return {'kind': 'sideboard', 'position': [x, 0.0], 'size': [w, 0.45, h], 'wood': 'veneer', 'color': '#6E4B33',
            'turntable': False}


def hero_turntable(colour='ember'):
    """Cumulus on a low sideboard beside the Cloud in its colour, a record on it. Round 1's critic
    (critic/rounds/2026-10-18/companions-hero-turntable-e1-r1.json, 4.5): the speaker back 0.41 so the record player
    leads, a longer lens, the dome down to 0.25, a smaller and stronger key, a graded card over the record, a finer
    veneer."""
    tgt = [0.1, 0.0, 0.64]
    sx, h = 0.5, 0.56
    s = base(f'Cumulus beside {C.NAMES[colour]}', [1500, 1050], colour,
             {'position': orbit(tgt, -20, 12, 4.1), 'target': tgt, 'lens_mm': 72, 'level': True})
    s['sky']['strength'] = 0.25
    s['products'] = [{'def': CLOUD, 'flavour': C.SPEAKER_FLAVOUR[colour], 'instances': [{'position': [-0.5, 0.45, 0], 'rotate_z': 0}]},
                     {'def': TT, 'flavour': colour, 'instances': [{'position': [sx, -0.02, h], 'rotate_z': -8}]}]
    rx = sx + SPINDLE[0] * math.cos(math.radians(-8)) - SPINDLE[1] * math.sin(math.radians(-8))
    ry = -0.02 + SPINDLE[0] * math.sin(math.radians(-8)) + SPINDLE[1] * math.cos(math.radians(-8))
    sb = sideboard(sx); sb['figure_m'] = 0.01
    s['set']['props'] = [sb] + record(round(rx, 4), round(ry, 4), h + PLATTER_TOP, colour)
    s['lights'] = lights(tgt, dist=4.5)
    s['lights']['key'].update({'size_m': [1.2, 1.0], 'irradiance': 3.2})
    s['lights']['glow'] = {'type': 'area', 'size_m': [0.7, 0.32], 'position': [-0.5, 1.11, 1.12], 'target': [-0.5, 0.45, 1.1],
                           'irradiance': 1.6, 'color': '#FFF1DC', 'specular': 0, 'transmission': False}
    s['lights']['tt_card'] = {'type': 'panel', 'size_m': [1.0, 0.4], 'position': [0.5, -0.55, 1.25], 'target': [0.5, -0.02, 0.66],
                              'strength': 4.0, 'color': '#FFFFFF', 'ramp': {'axis': 'y', 'at_m': [-0.75, -0.35], 'values': [0, 1]},
                              'diffuse': False}
    return s


def hero_lamp(colour='haze'):
    """Bell, lit, on the sideboard beside the Cloud in its colour, the studio turned down so the lamp carries. Round
    1's critic (critic/rounds/2026-10-18/companions-hero-lamp-e1-r1.json, 4.5): a 50 mm lens so the speaker stands
    whole, the strip four times brighter, the dome down to 0.25 and the key up, a warm pool on the wall behind the
    shade, a warm grey sweep so the violet separates, the veneer's grain up, contact shadows."""
    tgt = [0.1, 0.0, 0.7]
    sx, h = 0.55, 0.56
    s = base(f'Bell beside {C.NAMES[colour]}', [1500, 1050], colour,
             {'position': orbit(tgt, -18, 9, 3.9), 'target': tgt, 'lens_mm': 50, 'level': True}, sweep='#D8D2CA')
    s['sky']['strength'] = 0.25
    s['products'] = [{'def': CLOUD, 'flavour': C.SPEAKER_FLAVOUR[colour], 'instances': [{'position': [-0.42, 0.04, 0], 'rotate_z': 0}]},
                     {'def': LAMP, 'flavour': colour, 'instances': [{'position': [sx, 0.0, h], 'rotate_z': 0}]}]
    sb = sideboard(sx, 0.9); sb['grain'] = 0.45
    s['set']['props'] = [sb]
    s['lights'] = lights(tgt, scale=0.6, dist=4.5)
    s['lights']['key']['irradiance'] = 1.9
    s['lights']['wallglow'] = {'type': 'area', 'size_m': [0.4, 0.4], 'position': [0.55, 0.4, 1.05], 'target': [0.55, 2.7, 1.1],
                               'irradiance': 0.9, 'color': 2900, 'receivers': ['sweep']}
    s['materials'] = {'led': {'strength': round(LED * 1.6 * 4, 1)}, 'sweep': {'contact': 0.6}}
    s['render']['exposure'] = 0.2
    return s


def detail_turntable(colour='ice'):
    """The cloud's hole: the motor's pod standing apart in its ring, the belt to the platter's rim, low and close."""
    pod = [(68.0 - 241.6) / 1000, (305.0 - 186.5) / 1000]
    tgt = [round(pod[0] + 0.05, 4), round(pod[1] - 0.04, 4), 0.06]
    s = base(f'Cumulus in {C.NAMES[colour]}, the motor apart', [1200, 900], colour,
             {'position': orbit(tgt, -58, 16, 0.62), 'target': tgt, 'lens_mm': 100, 'level': True, 'fstop': 5.6,
              'focus': [round(pod[0], 4), round(pod[1], 4), 0.07]})
    s['product'] = {'def': TT, 'flavour': colour, 'instances': [{'position': [0, 0, 0], 'rotate_z': 0}]}
    s['lights'] = lights(tgt, dist=3.0)
    return s


def detail_lamp(colour='acid'):
    """Under the bell: the opal sleeve lit round the hub, the collar clamped by the cap, the flare deepening to its
    rim, seen from below the rim."""
    tgt = [0.0, 0.0, 0.40]
    s = base(f'Bell in {C.NAMES[colour]}, under the shade', [960, 1200], colour,
             {'position': [-0.17, -0.42, 0.2], 'target': tgt, 'lens_mm': 50, 'level': False, 'fstop': 4.0,
              'focus': [0.0, 0.0, 0.42]})
    s['product'] = {'def': LAMP, 'flavour': colour, 'instances': [{'position': [0, 0, 0], 'rotate_z': 0}]}
    s['lights'] = lights(tgt, scale=0.6, dist=3.0)
    s['materials'] = {'led': {'strength': LED}}
    return s


def all_shots():
    out = {}
    for k in C.KEYS:
        out[f'look-turntable-{k}'] = look_turntable(k)
        out[f'look-lamp-{k}'] = look_lamp(k)
    out['hero-turntable'] = hero_turntable()
    out['hero-lamp'] = hero_lamp()
    out['detail-turntable'] = detail_turntable()
    out['detail-lamp'] = detail_lamp()
    return out


if __name__ == '__main__':
    os.makedirs(SHOTS, exist_ok=True)
    for name, s in all_shots().items():
        json.dump(s, open(os.path.join(SHOTS, f'{name}.json'), 'w'), indent=1)
    print(len(all_shots()), 'shots in', os.path.relpath(SHOTS, ROOT))
