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
LAMP_STRIP_Z = 0.441                                               # the strip's middle above the lamp's foot
LAMP_W = 14.0                                                     # its light, watts as Cycles counts them (tuned by eye)
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
    s['materials'] = {'led': {'strength': LED * 4 if on else 0.0}}      # x4: round 1's critic on the hero (it read as off)
    return s


def sideboard(x, w=1.0, h=0.56):
    return {'kind': 'sideboard', 'position': [x, 0.0], 'size': [w, 0.45, h], 'wood': 'veneer', 'color': '#6E4B33',
            'turntable': False}


# --- the heroes (round 31b: the lead session and the owner: the companion the subject, 40-50 % of the frame, the speaker
# as context behind it, partly cropped and softer; the setting real, with texture; Bell switched on) ------------------
CAB = (1.25, 0.47)              # Poly Haven's modern_wooden_cabinet (2.44 x 0.52 x 0.68), its centre on the floor
CAB_TOP = 0.68


def room(dusk=False):
    """A living room: oak boards, plaster, a tall window in the left wall the sun comes through (or blue dusk), the
    back wall 0.75 m behind the companions, and the scanned walnut cabinet against it."""
    r = {'kind': 'room', 'size': [5.6, 4.6, 2.8], 'center': [0.4, -1.55],
         'floor': {'plank_w': 0.19, 'plank_l': 1.8, 'base': '#B08A60', 'dark': '#97724A', 'light': '#C49D70', 'plank_contrast': 1.1},
         'wall': {'color': '#EEE9E1'}, 'ceiling': '#F3F0EA', 'skirting': {'h': 0.11, 'color': '#ECE8E1'},
         'windows': [{'wall': 'left', 'along': 0.9, 'sill': 0.45, 'size': [1.5, 2.0], 'mullions': [1, 2]}],
         'props': [{'kind': 'kit', 'shape': 'asset', 'model': 'modern_wooden_cabinet', 'res': '2k',
                    'position': [CAB[0], CAB[1], 0.0], 'rotate': [0, 0, 0]}]}
    return r


def room_shot(title, size, cam):
    return {'title': title, 'size': size, 'camera': cam,
            'render': {'samples': 64, 'adaptive': 0.015, 'denoise': True, 'clamp': 8, 'bounces': 12, 'view': 'Khronos PBR Neutral',
                       'exposure': 0.0, 'white_balance_k': 5600},
            'materials': {'oak': {'grain': 1.0, 'roughness': 0.38}}}


def hero_turntable(colour='ember', speaker=(-0.32, 0.52, 10), cam=(-8, 14, 1.75, 50)):
    """Cumulus on the walnut cabinet in morning sun from the left window, a record on it; the Cloud in its colour
    behind it at the left, out of focus. Promo pass 1 (critic/rounds/2026-10-18/promo-hero-turntable-p1.json, 5.0):
    a softbox key on the record player (it was the darkest thing in the frame), the sun higher and more frontal (its
    long shadow of the horn filled the wall), the speaker further back so its horn reads, the cabinet at 4k, a real
    plaster wall (Poly Haven beige_wall_001), more samples, f/4 focused on the arm and the platter's front."""
    tx, ty = 0.36, 0.42
    h = CAB_TOP
    tgt = [tx, ty - 0.02, h + 0.06]
    az, el, d, lens = cam
    s = room_shot(f'Cumulus beside {C.NAMES[colour]}', [1600, 1100],
                  {'position': orbit(tgt, az, el, d), 'target': tgt, 'lens_mm': lens, 'level': True, 'fstop': 4.0,
                   'focus': [0.42, 0.40, 0.80]})
    s['render']['samples'] = 160
    s['render']['exposure'] = 0.8
    s['set'] = room()
    s['set']['props'][0]['res'] = '4k'
    s['set']['props'].append(WALL)
    s['products'] = [{'def': CLOUD, 'flavour': C.SPEAKER_FLAVOUR[colour], 'instances': [{'position': list(speaker[:2]) + [0], 'rotate_z': speaker[2]}]},
                     {'def': TT, 'flavour': colour, 'instances': [{'position': [tx, ty, h], 'rotate_z': -6}]}]
    rx = tx + SPINDLE[0] * math.cos(math.radians(-6)) - SPINDLE[1] * math.sin(math.radians(-6))
    ry = ty + SPINDLE[0] * math.sin(math.radians(-6)) + SPINDLE[1] * math.cos(math.radians(-6))
    s['set']['props'] += record(round(rx, 4), round(ry, 4), h + PLATTER_TOP, colour)
    s['sky'] = {'kind': 'gradient', 'strength': 9.0, 'zenith': '#9FB8DA', 'horizon': '#D6EAF8', 'ground': '#8A8478'}
    s['sun'] = {'azimuth_deg': -55, 'elevation_deg': 38, 'irradiance': 3.0, 'angle_deg': 0.53, 'color': '#FFF0DC'}
    s['lights'] = {'fill': {'type': 'area', 'size_m': [1.6, 1.2], 'orbit': {'azimuth_deg': 35, 'elevation_deg': 15, 'distance_m': 2.2},
                            'target': tgt, 'irradiance': 0.35, 'color': '#EAF2FF'},
                   'key': {'type': 'area', 'size_m': [1.2, 0.9], 'orbit': {'azimuth_deg': -25, 'elevation_deg': 35, 'distance_m': 1.6},
                           'target': [tx, ty - 0.02, h + 0.09], 'irradiance': 1.6, 'color': '#FFF4E6'}}
    return s


# a real plastered wall over the room's back wall, a hair in front of it (promo pass 1: the plain wall read as CG)
WALL = {'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'beige_wall_001', 'res': '2k', 'color': '#E6E0D6',
        'size': [5.4, 0.008, 2.78], 'position': [0.4, 0.738, 0.005]}


def hero_lamp(colour='haze'):
    """Bell, lit, on the walnut cabinet at dusk: the room lit by it alone but for the blue of the window; the Cloud
    in its colour behind it at the left, out of focus."""
    lx, ly = 0.36, 0.45
    h = CAB_TOP
    tgt = [lx, ly, h + 0.24]
    s = room_shot(f'Bell beside {C.NAMES[colour]}', [1600, 1100],
                  {'position': orbit(tgt, 6, 6, 1.8), 'target': tgt, 'lens_mm': 50, 'level': True, 'fstop': 2.8,
                   'focus': [lx, ly - 0.2, h + 0.3]})
    s['set'] = room(dusk=True)
    s['products'] = [{'def': CLOUD, 'flavour': C.SPEAKER_FLAVOUR[colour], 'instances': [{'position': [-0.36, 0.36, 0], 'rotate_z': 10}]},
                     {'def': LAMP, 'flavour': colour, 'instances': [{'position': [lx, ly, h], 'rotate_z': 0}]}]
    s['sky'] = {'kind': 'gradient', 'strength': 2.5, 'zenith': '#1E2C4A', 'horizon': '#5A6E92', 'ground': '#2A2A30'}
    s['lights'] = {'fill': {'type': 'area', 'size_m': [1.6, 1.2], 'orbit': {'azimuth_deg': 40, 'elevation_deg': 20, 'distance_m': 2.4},
                            'target': tgt, 'irradiance': 0.04, 'color': '#C9D6F0'}}
    # the strip's light: three small lamps just outside the opal sleeve, at the strip's height (the sleeve's subsurface stops shadow rays, so lamps inside it lit only the table) (an
    # emitting strip that thin is all noise to a path tracer; its glow stays on the strip itself)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        s['lights'][f'strip{k}'] = {'type': 'point', 'position': [round(lx + 0.047 * math.cos(a), 4), round(ly + 0.047 * math.sin(a), 4), h + LAMP_STRIP_Z],
                                    'power_w': LAMP_W / 3, 'radius_m': 0.004, 'color': 2700}
    s['materials'] = {'oak': {'grain': 1.0, 'roughness': 0.38}, 'led': {'strength': 60.0}}
    s['render']['white_balance_k'] = 3400
    s['render']['exposure'] = 0.9
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
