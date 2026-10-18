"""Round 31's dioramas: what every set shares, so the eight read as one campaign (BRIEF.md is the direction).

Each colour's set is a module beside this one, named for the colour (ember.py, dust.py, acid.py, poison.py, ice.py,
haze.py, fog.py, smoke.py), with `shot()` returning its landscape frame and `portrait()` its 4:5 frame; build.py writes
them to studio/shots/barkhorn/diorama31/. The helpers here make the pieces (kit.py's shapes and materials, in
studio/engine), the camera (tilt-shift), the light and the finish.
"""
import copy, json, math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BARK = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(BARK))
sys.path.insert(0, BARK)
import marks as M                                         # noqa: E402

OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'diorama31')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'diorama31')
BASE = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lookbook21', 'look-amber-on.json')
# the colours: module name -> (the speaker's key, its flavour in studio/products/barkhorn-cloud.json, its name)
COLOURS = {'ember': ('red', 'cloud-red', 'Ember'), 'dust': ('orange', 'cloud-orange', 'Dust'),
           'acid': ('amber', 'cloud-amber', 'Acid'), 'poison': ('green', 'eucalyptus-y2k-green', 'Poison'),
           'ice': ('blue', 'cloud-blue', 'Ice'), 'haze': ('violet', 'cloud-violet', 'Haze'),
           'fog': ('ice', 'birch-fog-clear', 'Fog'), 'smoke': ('black', 'cloud-black', 'Smoke')}
FOG = [(x, y, r) for _, x, y, r in M.CLOUD[:3]]          # the Fog icon's three circles (icon units, y down)
SPEAKER_H = 1.293                                        # the speaker's height (m); its front faces -y, it stands at 0
LANDSCAPE, PORTRAIT = (2400, 1600), (1600, 2000)


# --- pieces --------------------------------------------------------------------------------------------------------
def kit(shape, material, color, **k):
    """A kit piece (studio/engine/kit.py documents the shapes and materials)."""
    return {'kind': 'kit', 'shape': shape, 'material': material, 'color': color, **k}


def cloud(cx, cy, cz, s, color='#F3F4F4', material='felt', depth=0.55, threads=True, circles=FOG, top=4.6):
    """A cloud of the icon's circles (`s` metres an icon unit), centred on (cx, cy, cz), hung on two threads to `top`."""
    puffs = [[round(x * s, 4), round(-y * s, 4), round(r * s, 4)] for x, y, r in circles]
    out = [kit('puffs', material, color, puffs=puffs, depth=depth, position=[cx, cy, cz])]
    if threads:
        for x, z, r in (puffs[0], puffs[-1]):
            a = [cx + x * 0.6, cy, cz + z + r * 0.92]
            out.append(kit('thread', 'paper', '#E9E6DF', a=a, b=[a[0], cy, top]))
    return out


def bank(x0, x1, y, z, r0, r1, seed, color='#FAFAF7', material='cotton', depth=0.8):
    """A low bank of puffs along x from x0 to x1 (cotton-wool fog, a snowdrift, a hedge), bigger in the middle."""
    rnd = random.Random(seed)
    n = max(3, int((x1 - x0) / (r1 * 0.9)))
    puffs = []
    for i in range(n + 1):
        t = i / n
        r = r0 + (r1 - r0) * math.sin(math.pi * t)
        puffs.append([round(x0 + (x1 - x0) * t, 4), round(z + r * 0.35 + rnd.uniform(-0.02, 0.02), 4), round(r * rnd.uniform(0.85, 1.1), 4)])
    return [kit('puffs', material, color, puffs=puffs, depth=depth, position=[0, y, 0])]


def mound(x, y, z, sx, sy, sz, color, material='felt', **k):
    """A squashed ball half sunk in the ground: a hill, a dune, a drift."""
    return kit('sphere', material, color, position=[x, y, z], scale=[sx, sy, sz], **k)


# --- camera, light, finish -------------------------------------------------------------------------------------------
def tilt_shift(elevation=24.0, azimuth=-20.0, distance=7.0, lens=65.0, target=(0.0, 0.0, 0.62), focus=None,
               fstop=2.8, miniature=11.0, shift_x=0.0, shift_y=0.0, roll=0.0, blades=0):
    """The campaign's camera: above the speaker looking down `elevation` degrees, from `azimuth` (0 straight on from
    the front, negative from its left), `distance` metres from `target`, a `lens` mm lens, focused through `focus`
    (default the target) with the depth of field of the same f-number on a model at 1:`miniature` (tilt-shift)."""
    az, el = math.radians(azimuth), math.radians(elevation)
    tx, ty, tz = target
    pos = [tx + distance * math.sin(az) * math.cos(el), ty - distance * math.cos(az) * math.cos(el), tz + distance * math.sin(el)]
    cam = {'position': [round(v, 4) for v in pos], 'target': [round(v, 4) for v in target], 'lens_mm': lens,
           'level': False, 'fstop': fstop, 'miniature': miniature, 'focus': list(focus or target), 'blades': blades}
    if shift_x or shift_y:
        cam['shift_x'], cam['shift_y'] = shift_x, shift_y
    if roll:
        cam['roll_deg'] = roll
    return cam


def area(azimuth, elevation, distance, irradiance, color='#FFFFFF', size=(2.0, 2.0), target=(0.0, 0.0, 0.7)):
    """An area lamp on an orbit round the speaker (azimuth 0: from the front), lighting `target` at `irradiance`."""
    return {'type': 'area', 'size_m': list(size), 'orbit': {'azimuth_deg': azimuth, 'elevation_deg': elevation, 'distance_m': distance},
            'target': list(target), 'irradiance': irradiance, 'color': color}


def point(position, power_w, color='#FFB070', radius=0.05):
    return {'type': 'point', 'position': list(position), 'power_w': power_w, 'color': color, 'radius_m': radius}


def spot(position, target, power_w, cone=30.0, blend=0.4, color='#FFFFFF', radius=0.05):
    return {'type': 'spot', 'position': list(position), 'target': list(target), 'power_w': power_w, 'cone_deg': cone,
            'blend': blend, 'color': color, 'radius_m': radius}


def soft(key=3.2, fill=0.9, rim=1.4, warm='#FFF2E2', cool='#EAF0FF'):
    """A soft key from the front left, a cool fill from the right, a warm rim from behind: a daylight start."""
    return {'key': area(-38, 38, 5.5, key, warm, (2.6, 2.0), (0.0, 0.3, 1.0)),
            'fill': area(48, 14, 6.0, fill, cool, (3.0, 2.0), (0.0, 0.3, 0.9)),
            'rim': area(165, 30, 4.5, rim, warm, (2.0, 1.0), (0.0, 0.5, 1.6))}


def finish(bloom=0.25, bloom_px=40, threshold=0.78, saturation=0.15, lift=0.03, lift_color='#000000', vignette=0.2,
           contrast=0.08, clarity=0.05, sharpen=0.3):
    """The campaign's post (studio/engine/finish.py): no white-point gain, a little contrast and clarity, the dream
    (bloom on the light sources, a vibrance, the shadows lifted in the world's own shadow colour, a vignette)."""
    return {'enabled': True, 'white_in': 236, 'white_out': 236, 'contrast': contrast, 'clarity': clarity,
            'sharpen': sharpen, 'sharpen_px': 0.7,
            'dream': {'bloom': bloom, 'bloom_px': bloom_px, 'bloom_threshold': threshold, 'saturation': saturation,
                      'lift': lift, 'lift_color': lift_color, 'vignette': vignette}}


def shot(name, set_spec, lights, camera, title, sky=None, size=LANDSCAPE, samples=256, fin=None, haze=None,
         rotate_z=-14.0, position=(0.0, 0.0, 0.0), view='Khronos PBR Neutral', look=None, exposure=0.0, cover=False):
    """A diorama's frame: the speaker in `name`'s colour at `position`, turned `rotate_z`, cover off unless `cover`, in
    `set_spec` (a sweep or a stage, with its props), lit by `lights`, seen by `camera`."""
    key, flavour, _ = COLOURS[name]
    s = copy.deepcopy(json.load(open(BASE)))
    inst = {'flavour': flavour, 'position': list(position), 'rotate_z': rotate_z}
    if not cover:
        inst['hide'] = ['cloth-disc']
    s['product'] = {'def': 'studio/products/barkhorn-cloud.json', 'flavour': flavour, 'instances': [inst]}
    s['set'] = set_spec
    s['lights'] = lights
    s['camera'] = camera
    s['size'] = list(size)
    s['title'] = title
    s['sky'] = sky or {'kind': 'gradient', 'zenith': '#2A2A2E', 'horizon': '#3A3A3E', 'ground': '#1A1A1C', 'strength': 0.2}
    s['render'] = {**s['render'], 'samples': samples, 'exposure': exposure, 'clamp': 6, 'view': view}
    if look:
        s['render']['look'] = look
    s['finish'] = fin or finish()
    if haze:
        s['haze'] = haze
    return s


def portrait_of(landscape, **camera):
    """The 4:5 frame of a landscape shot: the same set, light and finish, the camera changed by `camera`'s keys."""
    s = copy.deepcopy(landscape)
    s['size'] = list(PORTRAIT)
    s['camera'].update(camera)
    s['title'] = s['title'] + ' (4:5)'
    return s
