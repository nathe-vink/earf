"""Round 34's renders of Mantle (Float until the owner named it), the record player (turntable_float.py), in the names
the site picks up (renders/2026-10-22/barkhorn/turntable/): for each of the eight colours a studio hero (3:2) on the
speakers' pale paper field, the same at dusk with the base lit, and a phone frame (4:5); in Smoke, the lid open, the
arm and platter, and the motor's pod. The studio rig is the speakers' studio heroes' (studio31's hero-light, rig
1769c6a), brought in to a record player's size; the materials are the speakers' own (common.MATERIALS), so the tints
match.

    .venv-fab/bin/python spinoffs/barkhorn/companions/turntable_float_shots.py --model     # the lid-open model
    python3 spinoffs/barkhorn/companions/turntable_float_shots.py                         # the shot files
    python3.11 spinoffs/barkhorn/companions/turntable_float_shots.py --render [names] [--scale s] [--samples n] [--out dir]
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import common as C                                                 # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'turntable-float')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'turntable')
DEF = 'studio/products/barkhorn-turntable-float.json'
OPEN_DEF = 'spinoffs/barkhorn/companions/out-turntable-float/open/barkhorn-turntable-float-open.json'
ONE = 'smoke'                                   # the colour of the open, detail and pod frames

# the product's frame in metres (its footprint's centre on the shelf): the parts the frames are aimed at
SPINDLE = [-0.025, -0.012]
ARM = [0.170, 0.094]
STYLUS = [0.0945, -0.130]
POD = [-0.161, 0.113]
DAY_HIDE = ['led-strip-edge']                   # by day the edge is the clear acrylic it is


def model():
    """The lid swung open on its hinges, as a render model of its own (never built: the lid is the same five parts)."""
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
    import turntable_float as F
    import render as fk_render
    out = os.path.join(HERE, 'out-turntable-float', 'open')
    prod = copy.copy(F.PRODUCT)
    prod.name = 'barkhorn-turntable-float-open'
    fk_render.write(prod, [p for p in F.parts(F.P, lid_open=True) if p.solid is not None], out, engine_file=os.path.join(ROOT, OPEN_DEF), proof=False)
    print(OPEN_DEF)


def mirror_flag(cam, at, dist=1.3, size=(2.4, 1.4), color='#4A4A4C'):
    """A dark card seen only in reflections, where a level face at `at` mirrors the camera's view: the lid's top
    mirrored the white field and vanished; with this it reads as tinted sheet with a soft dark reflection in it."""
    v = [at[i] - cam[i] for i in range(3)]
    r = [v[0], v[1], -v[2]]
    n = sum(x * x for x in r) ** 0.5
    r = [x / n for x in r]
    return {'center_m': [round(at[i] + dist * r[i], 3) for i in range(3)], 'size_m': list(size),
            'normal': [round(-x, 3) for x in r], 'glossy': True, 'reflect_only': True, 'color': color}


def record():
    """A 12 inch record on the platter (a prop of the set, not a part of the product): black vinyl, a cream label."""
    z = 0.113
    return [{'kind': 'kit', 'shape': 'cylinder', 'radius': 0.1505, 'height': 0.0018, 'position': [SPINDLE[0], SPINDLE[1], z],
             'material': 'gloss', 'color': '#0C0C0D', 'roughness': 0.22},
            {'kind': 'kit', 'shape': 'cylinder', 'radius': 0.050, 'height': 0.0003, 'position': [SPINDLE[0], SPINDLE[1], z + 0.0018],
             'material': 'paper', 'color': '#E6E0D4'}]


def aim(s, at=(0.0, 0.0, 0.194)):
    """The mirror card for the shot's camera, on the lid's top (or a level face at `at`)."""
    s['set']['flags'] = [mirror_flag(s['camera']['position'], at)]
    return s


# the cameras: lid open (the heroes: the arm, the record and the raised lid all read), lid down (the second picture)
CAM_OPEN = {'position': [0.95, -1.75, 0.78], 'target': [0.0, 0.03, 0.15], 'lens_mm': 62.0, 'level': False}
CAM_CLOSED = {'position': [0.80, -1.62, 0.86], 'target': [0.0, 0.0, 0.075], 'lens_mm': 70.0, 'level': False}


def studio(colour, lid='open'):
    """The studio hero: the speakers' bright field (studio31, hero-light), the record player from the front right
    and above; `lid` 'open' (raised on its hinges), 'closed' or 'off'."""
    s = {
        'title': f'Mantle in {C.NAMES[colour]}, studio, lid {lid}',
        'size': [2400, 1600],
        'product': {'def': OPEN_DEF if lid == 'open' else DEF, 'flavour': colour, 'hide': DAY_HIDE + (['lid-*'] if lid == 'off' else []),
                    'instances': [{'position': [0.0, 0.0, 0.0], 'rotate_z': 0.0}]},
        'set': {'kind': 'sweep', 'color': '#F3F1EE', 'width': 52.0, 'front': 20.0, 'depth': 6.0, 'radius': 5.0, 'height': 9.0,
                'contact': {'strength': 0.8, 'distance_m': 0.3, 'core_strength': 0.9, 'core_distance_m': 0.03},
                'props': record()},
        'camera': dict(CAM_OPEN if lid == 'open' else CAM_CLOSED),
        'sky': {'kind': 'gradient', 'zenith': '#F2F1EF', 'horizon': '#EEEDEB', 'ground': '#CFCCC8', 'strength': 0.6, 'visible': False},
        'render': {'samples': 64, 'adaptive': 0.015, 'denoise': True, 'clamp': 4, 'bounces': 16, 'view': 'Khronos PBR Neutral',
                   'exposure': 0.0, 'white_balance_k': 5900, 'white_balance_tint': 7.0},
        'finish': {'enabled': True, 'white_in': 235, 'white_out': 238, 'contrast': 0.1, 'clarity': 0.03, 'sharpen': 0.12,
                   'sharpen_px': 0.7},
        'materials': {'sweep': {'roughness': 0.32}},
        'lights': {
            'bg-left': {'type': 'area', 'size_m': [4.0, 3.0], 'position': [-2.6, 3.2, 3.4], 'target': [-1.5, 6.0, 1.2],
                        'irradiance': 3.6, 'color': '#FFF4E8', 'camera': False, 'specular': 0.0},
            'bg-right': {'type': 'area', 'size_m': [4.0, 3.0], 'position': [2.6, 3.2, 3.4], 'target': [-0.9, 6.0, 1.0],
                         'irradiance': 3.6, 'color': '#FFF4E8', 'camera': False, 'specular': 0.0},
            'scrim': {'type': 'area', 'size_m': [1.4, 1.2], 'position': [0.05, 0.15, 1.5], 'target': [0.0, 0.0, 0.1],
                      'irradiance': 1.6, 'color': '#FFFAF4', 'camera': False},
            'key': {'type': 'area', 'size_m': [0.9, 0.9], 'orbit': {'azimuth_deg': -30, 'elevation_deg': 38, 'distance_m': 2.2},
                    'target': [0.0, 0.0, 0.08], 'irradiance': 4.0, 'color': '#FFFAF4', 'camera': False, 'specular': 1.0},
            'back-top': {'type': 'area', 'size_m': [0.6, 0.6], 'orbit': {'azimuth_deg': 200, 'elevation_deg': 30, 'distance_m': 1.4},
                         'target': [0.0, -0.3, 0.0], 'irradiance': 14.0, 'color': '#FFF8F0', 'camera': False},
            # a low soft bank behind, opposite the camera, at the plinth's height: light through the sheet edge to
            # edge, so the plinth's edges glow in the colour as lit acrylic does, instead of reading black
            'plinth-back': {'type': 'area', 'size_m': [1.0, 0.12], 'position': [-0.40, 0.80, 0.077], 'target': [0.0, 0.0, 0.076],
                            'irradiance': 120.0, 'color': '#FFF8F0', 'camera': False, 'specular': 0.0},
        },
    }
    return aim(s) if lid == 'closed' else aim(s, (0.0, 0.0, 0.115))


def dusk(colour, lid='open'):
    """The same frame at dusk: the paper in blue-grey evening light, the room's lamps down, the base's edge lit."""
    s = studio(colour, lid)
    s['title'] = f'Mantle in {C.NAMES[colour]}, dusk, the base lit'
    s['product']['hide'] = []
    s['set']['color'] = '#B9BCC6'
    s['sky'].update(zenith='#5A6274', horizon='#77808F', ground='#3A3D46', strength=0.25)
    L = s['lights']
    for k in ('bg-left', 'bg-right'):
        L[k].update(irradiance=0.35, color='#9FB0D8')
    L['scrim'].update(irradiance=0.12, color='#B8C6E6')
    L['key'].update(irradiance=0.45, color='#AFC0E4')
    L['back-top'].update(irradiance=1.6, color='#C9D2EA')
    L['plinth-back'].update(irradiance=12.0, color='#C9D2EA')
    s['materials']['glow'] = {'strength': 9.0}
    s['finish'] = {'enabled': True, 'contrast': 0.08, 'clarity': 0.03, 'sharpen': 0.1, 'sharpen_px': 0.7}
    s['render'].update(white_balance_k=5600, white_balance_tint=0.0, exposure=0.3)
    return s


def tall(colour, lid='open'):
    """The phone frame, 4:5: the raised lid over the deck, the float under it, stacked in the tall frame."""
    s = studio(colour, lid)
    s['title'] = f'Mantle in {C.NAMES[colour]}, phone'
    s['size'] = [1600, 2000]
    s['camera'] = {'position': [0.66, -1.22, 0.86], 'target': [0.0, 0.03, 0.17], 'lens_mm': 62.0, 'level': False}
    return aim(s, (0.0, 0.0, 0.115))


def opened():
    """The lid open from the left, lower: the hinges, the lid's edge, the deck under it."""
    s = studio(ONE, 'open')
    s['title'] = f'Mantle in {C.NAMES[ONE]}, the lid open, from the left'
    s['camera'] = {'position': [-1.15, -1.45, 0.55], 'target': [0.0, 0.05, 0.16], 'lens_mm': 62.0, 'level': False}
    s['lights']['key']['orbit'] = {'azimuth_deg': 30, 'elevation_deg': 38, 'distance_m': 2.2}
    s['lights']['plinth-back'].update(position=[0.55, 0.70, 0.077])
    return aim(s, (0.0, 0.0, 0.115))


def detail():
    """The arm at rest beside the record's lead-in, and the platter's edge, close and low from the front right."""
    s = studio(ONE, 'off')
    s['title'] = f'Mantle in {C.NAMES[ONE]}, the arm and the platter'
    s['camera'] = {'position': [0.42, -0.42, 0.24], 'target': [0.07, -0.04, 0.10], 'lens_mm': 85.0, 'level': False,
                   'fstop': 5.6, 'focus': [STYLUS[0], STYLUS[1], 0.11]}
    return aim(s, (0.0, 0.0, 0.115))


def pod():
    """The motor's pod rising from the base through its hole in the floating plinth, from the back left, low."""
    s = studio(ONE, 'off')
    s['title'] = f'Mantle in {C.NAMES[ONE]}, the motor apart'
    s['camera'] = {'position': [-0.62, 0.55, 0.22], 'target': [-0.15, 0.10, 0.07], 'lens_mm': 85.0, 'level': False,
                   'fstop': 5.6, 'focus': [POD[0], POD[1], 0.07]}
    aim(s, (-0.05, 0.0, 0.115))
    s['lights']['key']['orbit'] = {'azimuth_deg': 220, 'elevation_deg': 40, 'distance_m': 2.2}
    s['lights']['back-top']['orbit'] = {'azimuth_deg': -20, 'elevation_deg': 30, 'distance_m': 1.4}
    s['lights']['back-top']['target'] = [0.0, 0.3, 0.0]
    return s


def all_shots():
    out = {}
    for c in C.KEYS:
        out[f'studio-{c}'] = studio(c)
        out[f'studio-{c}-closed'] = studio(c, 'closed')
        out[f'dusk-{c}'] = dusk(c)
        out[f'tall-{c}'] = tall(c)
    out['open'] = opened()
    out['detail'] = detail()
    out['pod'] = pod()
    return out


def build():
    os.makedirs(SHOTS, exist_ok=True)
    for n, s in all_shots().items():
        json.dump(s, open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
    print(len(all_shots()), 'shots in', os.path.relpath(SHOTS, ROOT))


def render(names, extra, out):
    py = os.environ.get('PY', 'python3.11')
    os.makedirs(out, exist_ok=True)
    for n in names:
        subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                        '--out', os.path.join(out, n + '.png')] + extra, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        raw = os.path.join(out, n + '.raw.png')
        if os.path.exists(raw):
            os.remove(raw)                      # the site keeps the png, its shot and its report only
        print(n, flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--model' in a:
        model()
    elif '--render' in a:
        extra = []
        for k in ('--scale', '--samples'):
            if k in a:
                extra += [k, a[a.index(k) + 1]]
        out = a[a.index('--out') + 1] if '--out' in a else RENDERS
        render([x for x in a if x in all_shots()] or list(all_shots()), extra, out)
    else:
        build()
