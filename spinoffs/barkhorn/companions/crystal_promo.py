"""Round 32e, Dome and Orb for earf.world (the owner, 2026-10-19: "sick lamps. Add them to the site as well and work
on some product images"). The site is pale paper (#F4F1EC, pictures on #F1EDE8), so every frame stands on a pale,
warm studio ground, dim enough that the glow reads, with no black voids. The lamps are placed by Planet's kit piece
(earf_moon.py, fns "dome" and "orb"), as everywhere else.

    1 dome-hero    4:5  1600 x 2000  the pendant lit, Ember, seen from a little below
    2 orb-hero     4:5  1600 x 2000  the Orb lit, Ember, on pale oak, low
    3 orbs         3:1  2400 x  800  the eight tints in a row, lit, in spectrum order
    4 domes        3:1  2400 x  800  eight pendants at one height, lit, one per tint
    5 catch        3:2  1800 x 1200  the bayonet, the cover 20 mm off the hub
    6 unlit        4:5  1600 x 2000  an Orb and a Dome in Smoke, off

    python3 spinoffs/barkhorn/companions/crystal_promo.py                     # the shots
    PY=python3.11 python3 spinoffs/barkhorn/companions/crystal_promo.py --render [names] [--scale 0.5]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'crystal-promo')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'crystal-promo')
TINTS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
FIXTURE = 'hub|pins|cob|gland|cord|canopy'
MARBLE = '#ECE7DF'            # pale honed marble (marble_01): the Orbs' surface (the plaster slab showed its edges, p1)
# the liner's glow for the site: the lamps are 2700 K, but under the studio's 4300 K balance a 2700 K glow pulled every
# tint orange (p1, both critics on both rows: Ember and Dust merged, Smoke and Fog went peach); this is about 3200 K
WARM = {'liner': {'glow_color': '#FFDCB8'}}
# each tint's light on the ground, sampled from the lit Orbs (p1: every pool was the same orange)
POOL = {'ember': '#FF7A68', 'dust': '#FF9C78', 'acid': '#FFC870', 'poison': '#BCE07A', 'ice': '#86D2FF',
        'haze': '#B496FF', 'fog': '#FFF2E4', 'smoke': '#CDBFAF'}


def piece(fn, spots, flavour, **k):
    k.setdefault('materials', WARM)
    return {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': fn, 'spots': spots, 'flavour': flavour, **k}


def hidden_point(pos, w, k=2500, radius=0.03):
    return {'type': 'point', 'position': [round(v, 4) for v in pos], 'power_w': w, 'radius_m': radius, 'color': k,
            'camera': False, 'transmission': False, 'specular': 0.0}


def studio(size, cam, props, lights, exposure=0.15, wb=4300, samples=256, depth=1.2, radius=0.5, wash=1.0,
           wash_target=None):
    """A pale studio: a paper sweep whose wall stands close enough behind to take the lamps' light (p1: it was far, and
    nothing landed on it), a long soft strip as the key (p1: square softbox windows on every ball), a low fill, and a
    wash on the paper that pools behind the product and falls away (p1: a dead flat field). The balance matches the
    lights, 4300 K (p1: 4600 pushed the paper pink, dE 5 to 6 from the page)."""
    tgt = cam['target']
    L = {'key': {'type': 'area', 'size_m': [3.0, 0.5], 'orbit': {'azimuth_deg': -30, 'elevation_deg': 42, 'distance_m': 2.6},
                 'target': tgt, 'irradiance': 0.6, 'color': 4300},
         'fill': {'type': 'area', 'size_m': [2.5, 2.0], 'orbit': {'azimuth_deg': 30, 'elevation_deg': 12, 'distance_m': 3.0},
                  'target': tgt, 'irradiance': 0.25, 'color': 4300},
         'bgwash': {'type': 'area', 'size_m': [3.5, 1.0], 'position': [tgt[0], -0.4, 3.0],
                    'target': wash_target or [tgt[0], depth, tgt[2]], 'irradiance': wash, 'color': 4300, 'camera': False,
                    'specular': 0.0},
         **lights}
    return {'size': size, 'camera': cam,
            'set': {'kind': 'sweep', 'color': '#EAE4DA', 'width': 10.0, 'front': 6.0, 'depth': depth, 'radius': radius,
                    'height': 4.0, 'props': props},
            # a pale ground: the domes' downward rims saw a dark one and drew a grey ring (p1)
            'sky': {'kind': 'gradient', 'zenith': '#D8D2C8', 'horizon': '#DED8CE', 'ground': '#D6CEC2', 'strength': 0.35},
            'lights': L,
            # a ray through a ball crosses its shell, liner and skin twice: 12 surfaces, past the engine's 8 transmission
            # bounces (the unlit Smoke ball rendered solid black)
            'render': {'samples': samples, 'adaptive': 0.012, 'denoise': True, 'clamp': 8, 'bounces': 24,
                       'transmission_bounces': 20,
                       'view': 'Khronos PBR Neutral', 'exposure': exposure, 'white_balance_k': wb}}


def marble(w, d, x=0.0, y=0.0, h=0.04):
    """The Orbs' surface: a pale honed marble slab, wide and deep enough that no edge is in frame."""
    return {'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'marble_01', 'res': '2k', 'color': MARBLE,
            'rough_mul': 0.6, 'size': [w, d, h], 'position': [x, y, 0.0]}


def orb_pool(x, y, z, tint, w=1.5):
    """The Orb's own lamp is shut in the ball (hidden from transmission, as every lamp here): one small hidden lamp in
    front of its base, in its tint, stands in for the light it throws forward (p1: two orange lobes at its sides)."""
    return {f'pool{x:+.2f}': {**hidden_point((x, y - 0.075, z + 0.05), w, radius=0.06), 'color': POOL[tint]}}


def dome_hero():
    z = 1.40
    cam = {'position': [-0.12, -0.95, 1.22], 'target': [0.0, 0.0, 1.46], 'lens_mm': 75, 'level': False, 'fstop': 5.6,
           'focus': [0.0, -0.05, 1.42]}
    return studio([1600, 2000], cam, [piece('dome', [[0.0, 0.0, z]], 'ember', shade_glow=1.4, lamp_w=22.0)],
                  {'rim': {'type': 'area', 'size_m': [0.6, 0.6], 'position': [0.35, 0.22, 1.62], 'target': [0, 0, 1.47],
                           'irradiance': 0.35, 'color': 3600, 'camera': False}},
                  depth=0.55, radius=0.3, wash=0.9, wash_target=[0.0, 0.55, 1.6])


def orb_hero():
    h = 0.04
    cam = {'position': [-0.16, -0.62, 0.15], 'target': [0.0, 0.0, 0.13], 'lens_mm': 75, 'level': True, 'fstop': 5.6,
           'focus': [0.0, -0.06, 0.12]}
    L = orb_pool(0.0, 0.0, h, 'ember', 2.0)
    L['back'] = {'type': 'area', 'size_m': [0.4, 0.06], 'position': [-0.25, 0.40, 0.10], 'target': [0, 0, 0.06],
                 'irradiance': 0.8, 'color': 4300, 'camera': False, 'specular': 0.5}
    return studio([1600, 2000], cam, [marble(3.0, 4.2, 0.0, 0.8, h),
                                      piece('orb', [[0.0, 0.0, h]], 'ember', shade_glow=1.1, lamp_w=3.0)], L,
                  depth=2.2, radius=0.8, wash=0.9, wash_target=[0.0, 2.2, 0.25])


def orbs():
    dx = 0.24
    xs = [(i - 3.5) * dx for i in range(8)]
    # on the paper itself (p1: the shelf cut the banner into stripes), a little higher to show each pool
    cam = {'position': [0.0, -4.2, 0.62], 'target': [0.0, 0.0, 0.09], 'lens_mm': 70, 'level': False, 'fstop': 8.0,
           'focus': [0.0, 0.0, 0.08]}
    L = {}
    for x, t in zip(xs, TINTS):
        L.update(orb_pool(x, 0.0, 0.0, t, 0.9))
    spots = [{'position': [x, 0.0, 0.0], 'flavour': t} for x, t in zip(xs, TINTS)]
    return studio([2400, 800], cam, [piece('orb', spots, 'ember', shade_glow=1.8, lamp_w=4.0)], L,
                  depth=1.0, radius=0.6, wash=0.9, wash_target=[0.0, 1.0, 0.2])


def domes():
    z, dx = 1.60, 0.30
    xs = [(i - 3.5) * dx for i in range(8)]
    # the wall 0.4 behind them, to take each one's light; a little lower, to see into each glowing mouth
    cam = {'position': [0.0, -3.4, 1.48], 'target': [0.0, 0.0, 1.70], 'lens_mm': 50, 'level': False, 'fstop': 8.0,
           'focus': [0.0, 0.0, 1.66]}
    spots = [{'position': [x, 0.0, z], 'flavour': t} for x, t in zip(xs, TINTS)]
    return studio([2400, 800], cam, [piece('dome', spots, 'ember', shade_glow=2.2, lamp_w=12.0)], {},
                  depth=0.4, radius=0.3, wash=1.5, wash_target=[0.0, 0.4, 1.8])


def catch():
    """The bayonet, close. The cover turned back, so the slot's entry stands under the pin facing the camera (p1: the
    pin floated over plain collar); level with the 20 mm gap, so it reads as air; the lamp on, low, so the tint glows."""
    cam = {'position': [0.16, -0.48, 1.255], 'target': [0.0, 0.0, 1.255], 'lens_mm': 100, 'level': True, 'fstop': 11.0,
           'focus': [0.0, -0.04, 1.26]}
    L = {'rimstrip': {'type': 'area', 'size_m': [0.25, 1.2], 'orbit': {'azimuth_deg': 145, 'elevation_deg': 20, 'distance_m': 1.2},
                      'target': [0, 0, 1.26], 'irradiance': 0.8, 'color': 4300, 'camera': False}}
    s = studio([1800, 1200], cam, [piece('dome', [[0.0, 0.0, 1.18]], 'acid', cover_drop=0.02, cover_turn=-30,
                                         shade_glow=0.5, lamp_w=4.0)], L,
               depth=0.6, radius=0.3, wash=1.1, wash_target=[-0.1, 0.6, 1.3])
    s['lights']['key'].update(size_m=[0.3, 1.6], irradiance=1.3)               # one crisp line per brass cylinder
    s['lights']['fill'].update(irradiance=0.6, orbit={'azimuth_deg': 25, 'elevation_deg': 0, 'distance_m': 3.0})
    return s


def unlit():
    """Off, as an object: one group, the Dome hanging just above and right of the Orb; panels behind each on the camera's
    line, so light crosses the acrylic (about 24 mm of Smoke and two frosts) and the frost core shows."""
    h = 0.04
    cam = {'position': [-0.05, -1.45, 0.32], 'target': [0.06, 0.0, 0.25], 'lens_mm': 85, 'level': True, 'fstop': 5.6,
           'focus': [0.02, 0.0, 0.14]}
    L = {'back': {'type': 'area', 'size_m': [1.4, 1.0], 'position': [0.1, 1.6, 0.9], 'target': [0.05, 0, 0.3],
                  'irradiance': 0.7, 'color': 4300, 'camera': False},
         'thru_orb': {'type': 'area', 'size_m': [0.35, 0.35], 'position': [0.04, 0.26, 0.135], 'target': [-0.05, -1.45, 0.25],
                      'irradiance': 40.0, 'color': 4300, 'camera': False, 'specular': 0.0},
         'thru_dome': {'type': 'area', 'size_m': [0.3, 0.18], 'position': [0.13, 0.42, 0.47], 'target': [-0.05, -1.45, 0.30],
                       'irradiance': 3.5, 'color': 4300, 'camera': False, 'specular': 0.0},
         'bounce': {'type': 'area', 'size_m': [0.4, 0.3], 'position': [-0.35, -0.3, 0.08], 'target': [0.02, 0, 0.06],
                    'irradiance': 0.6, 'color': 4300, 'camera': False}}
    return studio([1600, 2000], cam, [marble(3.0, 4.2, 0.0, 0.8, h),
                                      piece('orb', [[0.02, 0.0, h]], 'smoke', lamp=False, shade_glow=0.0),
                                      piece('dome', [[0.10, 0.10, 0.40]], 'smoke', lamp=False, shade_glow=0.0)],
                  L, depth=2.2, radius=0.8, wash=0.9, wash_target=[0.1, 2.2, 0.3])


FRAMES = {'dome-hero': dome_hero, 'orb-hero': orb_hero, 'orbs': orbs, 'domes': domes, 'catch': catch, 'unlit': unlit}


def build():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in FRAMES.items():
        s = f(); s['title'] = f'Dome and Orb for earf.world: {n}'
        json.dump(s, open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
        print(n)


def render(names, scale, out=RENDERS):
    py = os.environ.get('PY', 'python3')
    os.makedirs(out, exist_ok=True)
    for n in names:
        subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                        '--out', os.path.join(out, n + '.png'), '--scale', str(scale)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(n, flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--render' in a:
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        out = a[a.index('--out') + 1] if '--out' in a else RENDERS
        render([x for x in a if x in FRAMES] or list(FRAMES), scale, out)
    else:
        build()
