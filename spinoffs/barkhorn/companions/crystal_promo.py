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


# the paper's wash per frame, calibrated (calibrate.py in the scratch) so the backdrop renders the page's #EAE4DA: p2's
# backdrops came out lavender-grey near lum 175 (dE 10 to 19), every critic's first note
WASH = {}


def studio(size, cam, props, lights, exposure=0.15, wb=4300, samples=256, depth=1.2, radius=0.5, wash=1.0,
           wash_target=None, wash_k=3800):
    """A pale studio: a paper sweep whose wall stands close enough behind to take the lamps' light (p1: it was far, and
    nothing landed on it), a long soft strip as the key (p1: square softbox windows on every ball), a low fill, and a
    wash on the paper that pools behind the product and falls away (p1: a dead flat field). The balance matches the
    lights, 4300 K (p1: 4600 pushed the paper pink, dE 5 to 6 from the page)."""
    tgt = cam['target']
    L = {'key': {'type': 'area', 'size_m': [3.0, 0.5], 'orbit': {'azimuth_deg': -30, 'elevation_deg': 42, 'distance_m': 2.6},
                 'target': tgt, 'irradiance': 0.6, 'color': 4300},
         'fill': {'type': 'area', 'size_m': [2.5, 2.0], 'orbit': {'azimuth_deg': 30, 'elevation_deg': 12, 'distance_m': 3.0},
                  'target': tgt, 'irradiance': 0.25, 'color': 4300},
         'bgwash': {'type': 'area', 'size_m': [6.0, 4.0], 'position': [tgt[0], -1.2, 3.6],
                    'target': wash_target or [tgt[0], depth, tgt[2]], 'irradiance': wash, 'color': wash_k, 'camera': False,
                    'specular': 0.0},
         **lights}
    # (p4 tried a plaster wall, Poly Haven's painted_plaster_wall: its blotches read as concrete, not the page's paper,
    # and its foot lit to a white band; the paper sweep stays, the place comes from the oak tops and the counter)
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


OAK = '#E9DAC4'                # pale oak (oak_veneer_01): p3, the marble's tile joints ran into the bases


def marble(w, d, x=0.0, y=0.0, h=0.04, z0=0.0):
    """The surface the lamps stand on (named for p1 to p3's marble): a pale oak top, oiled, wide and deep enough that no
    edge is in frame; at z0 a bar counter's top under the pendants."""
    return {'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'oak_veneer_01', 'res': '2k', 'color': OAK,
            'rough_mul': 0.75, 'size': [w, d, h], 'position': [x, y, z0]}


# each tint's glow, relative: the pale and the cool ones blew to white at the warm ones' level (p3: Fog white, Smoke
# lilac-white, Ice clipping blue)
GAIN = {'ember': 1.0, 'dust': 1.0, 'acid': 0.9, 'poison': 0.9, 'ice': 0.75, 'haze': 0.85, 'fog': 0.45, 'smoke': 0.6}


def row(fn, spots, glow, **k):
    """One kit piece per tint, so each tint's glow is set on its own."""
    return [piece(fn, [sp], sp['flavour'], shade_glow=round(glow * GAIN[sp['flavour']], 3), **k) for sp in spots]


def orb_pool(x, y, z, tint, w=1.5):
    """The Orb's own lamp is shut in the ball (hidden from transmission, as every lamp here): one small hidden lamp in
    front of its base, in its tint, stands in for the light it throws forward (p1: two orange lobes at its sides)."""
    return {f'pool{x:+.2f}': {**hidden_point((x, y - 0.075, z + 0.05), w, radius=0.06), 'color': POOL[tint]}}


def dome_hero():
    z = 1.40
    # p4: over a pale oak bar top (p3, both: 'a pool on no surface'); the lamp lower, so the red holds; a bounce under
    # the rim so its edge reads as acrylic, not a grey gasket
    cam = {'position': [-0.12, -1.05, 1.12], 'target': [0.0, 0.0, 1.30], 'lens_mm': 70, 'level': False, 'fstop': 5.6,
           'focus': [0.0, -0.05, 1.40]}
    L = {'rim': {'type': 'area', 'size_m': [0.6, 0.6], 'position': [0.35, 0.22, 1.62], 'target': [0, 0, 1.47],
                 'irradiance': 0.35, 'color': 3600, 'camera': False},
         'rim_l': {'type': 'area', 'size_m': [0.6, 0.6], 'position': [-0.35, 0.22, 1.62], 'target': [0, 0, 1.47],
                   'irradiance': 0.35, 'color': 3600, 'camera': False},
         'hubstrip': {'type': 'area', 'size_m': [1.2, 0.04], 'position': [-0.25, -0.45, 1.75], 'target': [0, 0, 1.5],
                      'irradiance': 1.2, 'color': 3600, 'camera': False},
         'lip': {'type': 'area', 'size_m': [1.0, 0.4], 'position': [0.0, -0.6, 0.9], 'target': [0, 0, 1.4],
                 'irradiance': 0.3, 'color': 3600, 'camera': False}}
    s = studio([1600, 2000], cam, [marble(4.0, 0.7, 0.0, 0.0, 0.05, 0.90),
                                   piece('dome', [[0.0, 0.0, z]], 'ember', shade_glow=0.6, lamp_w=10.0)], L,
               depth=0.6, radius=0.3, wash=1.8)
    s['lights']['key'].update(size_m=[0.8, 0.8], irradiance=0.4)
    return s


def orb_hero():
    h = 0.04
    # p3 (5.5, 5.5): the ball a flat pink disc, no pool on the stone, the steel crushed, the marble's joints; p4 pale oak
    cam = {'position': [-0.14, -0.62, 0.16], 'target': [0.0, 0.0, 0.11], 'lens_mm': 75, 'level': True, 'fstop': 4.0,
           'focus': [0.0, -0.06, 0.12]}
    L = {'pool+0.00': {**hidden_point((0.0, -0.05, h + 0.06), 3.0, radius=0.05), 'color': POOL['ember']},
         'back': {'type': 'area', 'size_m': [0.4, 0.06], 'position': [-0.25, 0.40, 0.14], 'target': [0, 0, 0.06],
                  'irradiance': 1.2, 'color': 4300, 'camera': False, 'specular': 1.0},
         'strip': {'type': 'area', 'size_m': [0.08, 0.6], 'orbit': {'azimuth_deg': -60, 'elevation_deg': 10, 'distance_m': 0.6},
                   'target': [0, 0, 0.06], 'irradiance': 1.2, 'color': 4300, 'camera': False}}
    s = studio([1600, 2000], cam, [marble(3.0, 3.6, 0.0, 0.5, h),
                                   piece('orb', [[0.0, 0.0, h]], 'ember', shade_glow=0.55, lamp_w=1.2)], L,
               depth=2.2, radius=0.8, wash=1.5)
    s['lights']['key'].update(size_m=[0.6, 1.6], orbit={'azimuth_deg': -35, 'elevation_deg': 45, 'distance_m': 2.6},
                              irradiance=0.35)
    s['lights']['fill'].update(irradiance=0.15)
    return s


def orbs():
    dx = 0.21
    xs = [(i - 3.5) * dx for i in range(8)]
    # p3 (5.0, 5.0): standing on a line, no contact shadows, the pools under the feet, Fog white, the L-shaped glint
    # repeated; p4: on pale oak, seen a little from above, one soft key, each tint's glow its own
    cam = {'position': [0.0, -4.4, 0.66], 'target': [0.0, 0.05, 0.13], 'lens_mm': 90, 'level': False, 'fstop': 5.6,
           'focus': [0.0, 0.0, 0.08]}
    L = {}
    for x, t in zip(xs, TINTS):
        L[f'pool{x:+.2f}'] = {**hidden_point((x, -0.16, 0.09), 0.45, radius=0.05), 'color': POOL[t]}
    spots = [{'position': [x, 0.0, 0.04], 'flavour': t} for x, t in zip(xs, TINTS)]
    # the top lifted 4 cm off the sweep's floor: at z 0 its face sat on the floor's and rendered black
    s = studio([2400, 800], cam, [marble(4.0, 4.0, 0.0, 1.2, 0.04, 0.0)]
               + row('orb', spots, 0.65, lamp_w=1.0, materials={'liner': {'glow_color': '#FFE8D0'}}), L,
               depth=2.2, radius=0.8, wash=1.6)
    s['lights']['key'].update(size_m=[1.6, 0.9], orbit={'azimuth_deg': -35, 'elevation_deg': 55, 'distance_m': 2.6},
                              irradiance=0.6)
    s['lights']['fill'].update(irradiance=0.06)
    return s


def domes():
    z, dx = 1.60, 0.30
    xs = [(i - 3.5) * dx for i in range(8)]
    # p3 (4.5, 4.5): 'a peach smear on no surface', the pale tints white, dark rims; p4: over a pale oak bar top, the
    # plaster wall 0.6 behind, each tint's glow its own, a bounce for the rims
    cam = {'position': [0.0, -4.6, 1.52], 'target': [0.0, 0.0, 1.46], 'lens_mm': 70, 'level': False, 'fstop': 4.0,
           'focus': [0.0, 0.0, 1.55]}
    spots = [{'position': [x, 0.0, z], 'flavour': t} for x, t in zip(xs, TINTS)]
    L = {'rim': {'type': 'area', 'size_m': [3.5, 0.15], 'position': [0, 0.45, 2.0], 'target': [0, -0.2, 1.6],
                 'irradiance': 1.2, 'color': 4300, 'camera': False},
         'bounce': {'type': 'area', 'size_m': [4.0, 1.5], 'position': [0, -1.2, 1.3], 'target': [0, 0, 1.6],
                    'irradiance': 0.8, 'color': 4300, 'camera': False}}
    s = studio([2400, 800], cam, [marble(4.0, 0.7, 0.0, 0.05, 0.05, 1.05)]
               + row('dome', spots, 0.75, lamp_w=4.5, materials={'liner': {'glow_color': '#FFF3E6'}}), L,
               depth=0.6, radius=0.2, wash=2.5)
    s['lights']['key'].update(size_m=[3.0, 0.3], orbit={'azimuth_deg': -30, 'elevation_deg': 30, 'distance_m': 2.6},
                              irradiance=0.9)
    return s


def catch():
    """The bayonet, close: at the pins' height, a longer lens, so the 20 mm drop, the slot and its pin read in one line
    (p3: from above the drop foreshortened); a narrow kick on each pin; a soft, broad key (p3: a hard rectangle and its
    ghost on the dome); a low fill into the gap; the lamp low."""
    cam = {'position': [0.12, -0.42, 1.27], 'target': [0.0, 0.0, 1.255], 'lens_mm': 135, 'level': False, 'fstop': 13.0,
           'focus': [0.0, -0.045, 1.265]}
    L = {'rimstrip': {'type': 'area', 'size_m': [0.12, 1.2], 'orbit': {'azimuth_deg': 125, 'elevation_deg': 40, 'distance_m': 0.9},
                      'target': [0, 0, 1.26], 'irradiance': 3.0, 'color': 4300, 'camera': False},
         'domestrip': {'type': 'area', 'size_m': [0.12, 1.2], 'orbit': {'azimuth_deg': 60, 'elevation_deg': 15, 'distance_m': 1.0},
                       'target': [0, 0, 1.22], 'irradiance': 1.8, 'color': 4300, 'camera': False},
         'pinkick': {'type': 'area', 'size_m': [0.04, 0.25], 'orbit': {'azimuth_deg': -20, 'elevation_deg': 15, 'distance_m': 0.5},
                     'target': [0, 0, 1.30], 'irradiance': 2.5, 'color': 4300, 'camera': False}}
    s = studio([1800, 1200], cam, [piece('dome', [[0.0, 0.0, 1.18]], 'acid', cover_drop=0.02, cover_turn=-30,
                                         shade_glow=0.2, lamp_w=5.0)], L,
               depth=0.6, radius=0.3, wash=1.6)
    s['lights']['key'].update(size_m=[0.9, 1.4], orbit={'azimuth_deg': -60, 'elevation_deg': 72, 'distance_m': 2.4},
                              irradiance=1.3)
    s['lights']['fill'].update(size_m=[0.35, 1.4], orbit={'azimuth_deg': 40, 'elevation_deg': -12, 'distance_m': 2.2},
                               irradiance=1.6)
    s['render']['samples'] = 512
    return s


def unlit():
    """Off, as an object: the Orb leads at lower left, the Dome back and right; less light through the ball, so Smoke
    reads deep (p3: milky lilac); the back light higher, so it rims and doesn't flood the floor; both lamps sharp."""
    h = 0.04
    cam = {'position': [-0.05, -1.45, 0.32], 'target': [0.08, 0.0, 0.27], 'lens_mm': 85, 'level': True, 'fstop': 8.0,
           'focus': [0.08, 0.10, 0.25]}
    L = {'back': {'type': 'area', 'size_m': [0.6, 1.2], 'position': [0.35, 1.0, 1.1], 'target': [0.05, 0, 0.3],
                  'irradiance': 0.6, 'color': 4300, 'camera': False},
         'thru_orb': {'type': 'area', 'size_m': [0.16, 0.16], 'position': [0.04, 0.13, 0.14], 'target': [-0.05, -1.45, 0.25],
                      'irradiance': 4.0, 'color': 4300, 'camera': False, 'specular': 0.0},
         'thru_dome': {'type': 'area', 'size_m': [0.3, 0.18], 'position': [0.26, 0.62, 0.57], 'target': [-0.05, -1.45, 0.30],
                       'irradiance': 0.3, 'color': 4300, 'camera': False, 'specular': 0.0},
         'bounce': {'type': 'area', 'size_m': [0.8, 0.5], 'position': [0.0, -0.6, 0.30], 'target': [0.02, 0, 0.10],
                    'irradiance': 0.12, 'color': 5000, 'camera': False}}
    s = studio([1600, 2000], cam, [marble(3.0, 3.6, 0.0, 0.5, h),
                                   piece('orb', [[0.02, 0.0, h]], 'smoke', lamp=False, shade_glow=0.0),
                                   piece('dome', [[0.22, 0.35, 0.50]], 'smoke', lamp=False, shade_glow=0.0)],
               L, depth=2.2, radius=0.8, wash=1.4, exposure=0.0)
    s['lights']['key'].update(size_m=[1.2, 0.6], orbit={'azimuth_deg': -40, 'elevation_deg': 35, 'distance_m': 2.6},
                              irradiance=0.9)
    return s


FRAMES = {'dome-hero': dome_hero, 'orb-hero': orb_hero, 'orbs': orbs, 'domes': domes, 'catch': catch, 'unlit': unlit}


def build():
    os.makedirs(SHOTS, exist_ok=True)
    cal = os.path.join(SHOTS, 'wash.json')
    WASH.update(json.load(open(cal)) if os.path.exists(cal) else {})
    for n, f in FRAMES.items():
        s = f(); s['title'] = f'Dome and Orb for earf.world: {n}'
        if n in WASH:
            s['lights']['bgwash'].update(WASH[n])
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
