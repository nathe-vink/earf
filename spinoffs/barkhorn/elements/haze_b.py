"""Haze, concept B: layered hills at blue hour. "Dusk, kept indoors."

Coastal hills recede range after range into violet haze, each paler than the last, and a pale sun sinks into the haze
(the icon: a sun behind three bars of haze). The speaker stands on the near ridge in dry grass, at eye level, the sun
low behind it, so its violet acrylic glows with the last light and its shadow runs long toward the camera.

The set's own pieces are in studio/engine/kit_ext/haze_b_el.py (the ridge, the hill layers, the haze, the sun's disk,
the dried grass). The far ranges stand at a tenth of their size and distance (the camera clips at 300 m).

This is the rig of critic pass 3, which won the blind duels and made the finals. The photographed-ranges version of
passes 4 to 7 (Poly Haven kiara_9_dusk behind a modelled ridge) is in git at b761a8d; haze_b.md has the history.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C                                        # noqa: E402

SKY = 'qwantani_dusk_2_puresky'
SKY_ROT = 247.3                                           # its afterglow behind the speaker (azimuth 174)
SUN_AZ, SUN_EL = 161.5, 1.5                       # the disc in clear sky right of the horn
CAM = dict(height=1.0, distance=10.0, azimuth=-15.0, lens=85.0, fstop=5.6)

RIDGE = {'area': [-10.0, -13.0, 9.0, 7.0], 'cell': 0.02, 'crest_y': 1.4, 'drop': 5.0, 'relief': 0.10, 'flat_r': 0.8,
         'slope_front': 0.02}


# a photographer's bounce from the camera's side (the dusk sky caught in a large reflector), so the speaker's front
# is not lost against the glow behind it
BOUNCE = C.area(-30.0, 10.0, 3.5, 7.0, '#F2DCCB', size=(3.0, 2.0))


STRAW = dict(ground=RIDGE, color='#5A4834', color2='#33291F', tip='#7A6448', value_jitter=0.3)


def GRADE(full, eye=(-2.5882, -9.6593, 1.0)):
    return {'at': [0.0, 0.0], 'r0': 0.4, 'r1': 2.2, 'eye': list(eye), 'full': full, 'clear': 0.02, 'floor': 0.08,
            'dens_min': 0.45}


def ext(fn, **k):
    return C.piece('ext', module='haze_b_el', fn=fn, **k)


def layers(cam_x=-2.6):
    """The ranges: distance of the crest behind the speaker, its height (metres, the camera's eye at 1.0) and rise."""
    spec = [  # d, crest angle below the eye (deg), amp, fuzz (scrub on the crest)
        (25.0, -3.6, 0.9, 0.0), (50.0, -2.3, 1.6, 0.0), (90.0, -1.4, 2.6, 0.0), (150.0, -0.7, 3.4, 0.0),
        (215.0, +0.1, 5.0, 0.0), (255.0, +1.1, 4.0, 0.0)]
    trees = {2: {'models': ['searsia_lucida', 'island_tree_01', 'searsia_burchellii'], 'count': 120, 'scale': [0.1, 0.22],
                 'down': 0.7}}
    import math
    out = []
    for k, (d, a, amp, fz) in enumerate(spec):
        D = d + 10.0
        out.append({'d': d, 'crest': round(1.0 + D * math.tan(math.radians(a)), 3), 'amp': amp, 'front': 0.32 * d,
                    'back': 0.2 * d, 'height': 0.14 * d, 'half_width': 0.62 * D, 'x': round(cam_x + 0.27 * D, 2),
                    'seed': 2.3 + 1.7 * k, 'feature': 0.3 * D, 'fuzz': fz, 'fuzz_feature': 0.5 + 0.02 * d,
                    'nx': 700 if k < 2 else 450, 'ny': 70 if k < 2 else 50})
        if k == 0:                                         # the nearest range: dry grass at its true scale
            out[-1].update(texture='withered_grass', tex_scale=0.4, tint='#5A4C44', tint_mix=0.5, folds=0.35, value=0.4)
        if k in trees:
            out[-1]['trees'] = trees[k]
    return out


def props():
    return [
        ext('ridge', texture='withered_grass', res='4k', displace=0.025, tint='#5E4E48', tint_mix=0.35, value=0.5, **RIDGE),
        ext('hills', layers=layers(), texture='rocky_terrain_02', res='2k', tex_scale=9.0, tint='#3E3A3C',
            tint_mix=0.6, folds=0.25),
        ext('haze', boxes=[{'box': [-160.0, 3.0, -60.0, 220.0, 300.0, 4.0], 'density': 0.0055, 'color': '#E2D4F0',
                            'anisotropy': 0.6},
                           {'box': [-160.0, 3.0, 4.0, 220.0, 300.0, 30.0], 'density': 0.0004, 'color': '#E2D4F0',
                            'anisotropy': 0.8}]),
        ext('sundisk', azimuth=SUN_AZ, elevation=SUN_EL, distance=296.0, eye=[-2.6, -9.7, 1.0], diameter_deg=0.6,
            emit=18.0, color='#FFC296'),
        # the grass grades down toward the speaker's feet, lowest in the corridor toward the camera, like grass
        # trodden on the way in: no cleared ring, and its base and ports in view
        ext('grass', area=[-6.0, -8.5, 6.0, 3.0], avoid=[[0.0, 0.0, 0.36], [-2.6, -9.7, 1.0]], count=7500, children=12,
            length=[0.15, 0.5], **STRAW, seed=3, patchy=0.75, clump=0.3, clump_r=0.05, cell=0.05, grade=GRADE(0.5)),
        ext('grass', area=[-6.0, -8.5, 6.0, 3.0], avoid=[[0.0, 0.0, 0.36], [-2.6, -9.7, 1.0]], count=3000, children=6,
            length=[0.15, 0.45], **STRAW, seed=8, patchy=0.75, root_mm=1.8, tip_mm=0.35, random=0.2, rough=0.05,
            cell=0.05, grade=GRADE(0.45)),
        ext('grass', area=[-1.4, -1.6, 1.4, 1.2], within=[0.0, -0.2, 1.4], avoid=[[0.0, 0.0, 0.36]], count=1200,
            children=10, length=[0.02, 0.07], **STRAW, seed=6, patchy=1.0, cell=0.04),
    ]


def shot():
    cam = C.camera(target=(0.0, 0.0, 1.09), shift_x=-0.16, **CAM)
    sun = {'azimuth_deg': SUN_AZ, 'elevation_deg': SUN_EL, 'irradiance': 24.0, 'angle_deg': 0.6, 'color': '#FFB48C'}
    return C.shot('haze_b', props(), cam, C.sky(SKY, SKY_ROT, 0.75), 'Haze in its element: layered hills at dusk',
                  sun=sun, lights={'bounce': BOUNCE}, white_balance=(5000, 0), rotate_z=10.0, position=(0.0, 0.0, -0.008), exposure=-1.0, look='AgX - Medium High Contrast',
                  fin=C.finish(contrast=0.04, clarity=0.1, sharpen=0.2, vignette=0.12, saturation=0.12, bloom=0.3, bloom_px=40, threshold=0.8))


def portrait():
    """The 4:5 frame, re-framed: a longer lens from closer, so the speaker keeps its share of the taller frame and
    the ranges stack higher behind it; the sun stays a little left of it."""
    s = C.portrait_of(shot())
    s['camera'] = C.camera(height=1.0, distance=7.5, azimuth=-15.0, lens=105.0, fstop=5.6, target=(0.0, 0.0, 1.26),
                           shift_x=-0.12)
    # from this closer camera the horn is wider: the sun and the sky turn 1 deg further so the disc keeps clear sky
    s['sun']['azimuth_deg'] = SUN_AZ - 1.0
    s['sky']['rotation_deg'] = SKY_ROT + 1.0
    for p in s['set']['props']:
        if p.get('fn') == 'sundisk':
            p['eye'] = s['camera']['position']
            p['azimuth'] = SUN_AZ - 1.0
        if p.get('fn') == 'grass':
            p['avoid'] = [a if a[1] > -5 else [*s['camera']['position'][:2], 1.0] for a in p['avoid']]
            if p.get('grade'):
                p['grade'] = GRADE(p['grade']['full'], tuple(s['camera']['position']))
    return s
