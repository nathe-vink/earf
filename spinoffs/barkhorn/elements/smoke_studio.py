"""Smoke, setting E3: the studio take (round E, the coordinator's third setting; a deliberate step outside the series'
locations).

The speaker on black, on a black gloss floor that mirrors it. A sculpted column of smoke rises from behind it and wraps
round it, most of a turn from the floor to above the waveguide, rim-lit from behind on both sides as a fragrance or
whisky campaign lights its smoke: bright edges against the dark, no haze, no source in frame.
"""
import math, random

from common import area, camera, finish, piece, shot as frame, portrait_of
from smoke import SHELL, SPEAKER


def column(seed=5):
    """Two strands, each most of a loose helix round the speaker (radius about 0.6 m), widening as they climb."""
    rnd = random.Random(seed)
    strands = []
    for j, (th0, dens, r0) in enumerate([(math.radians(235), 3.0, 0.62), (math.radians(300), 1.5, 0.7)]):
        pts, rr = [], []
        n = 40
        ph = [rnd.uniform(0, 6.28) for _ in range(3)]
        for i in range(n):
            t = i / (n - 1)
            th = th0 + 2 * math.pi * 0.85 * t + 0.25 * math.sin(5 * t + ph[0])
            r = r0 + 0.08 * math.sin(7 * t + ph[1]) + 0.1 * t
            z = 0.05 + 2.1 * t + 0.05 * math.sin(9 * t + ph[2])
            pts.append([round(r * math.cos(th), 4), round(r * math.sin(th), 4), round(z, 4)])
            rr.append(round(0.03 + 0.3 * t ** 1.2, 4))
        strands.append({'points': pts, 'radii': rr, 'density': dens})
    return piece('ext', module='smoke_el', fn='ribbon', strands=strands, layers=5, scale=0.1, cut=0.4, soft=0.35,
                 rise=2.0, laminar=0.0, laminar_blend=0.05, fade=[1.8, 2.3], color='#DADDE2', anisotropy=0.6,
                 detail=4.0, distortion=0.6, seed=seed, wobble=0.6, wobble_freq=4.0,
                 break_scale=0.5, break_cut=0.4, break_floor=0.1)


def shot():
    props = [piece('box', size=[24.0, 24.0, 0.02], position=[0.0, 0.0, -0.02], material='gloss', color='#060606',
                   roughness=0.12),
             column()]
    cam = camera(height=1.0, distance=6.0, azimuth=-20, lens=65, target=(0.0, 0.0, 0.9), fstop=5.6, shift_x=0.0)
    lights = {
        'skyfill': {**area(-20, 5, 2.4, 0.8, '#C8CCD4', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 2.5, '#C9C4BC', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 30.0, '#F2EEE8', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 22.0, '#F2EEE8', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        # the smoke's rims: two tall strips behind, left and right, flagged off the lens
        'rim_l': {**area(-145, 15, 3.0, 40.0, '#F4F0EA', (0.4, 2.6), (0.0, 0.0, 1.1)), 'specular': 0.0},
        'rim_r': {**area(145, 10, 3.0, 30.0, '#E6ECF4', (0.4, 2.6), (0.0, 0.0, 1.1)), 'specular': 0.0},
        # a soft top so the black floor's gloss shows a horizon of light under the speaker
        'top': {'type': 'area', 'size_m': [2.0, 1.0], 'position': [0.0, 1.6, 3.2], 'target': [0.0, 0.3, 0.0],
                'irradiance': 1.2, 'color': '#E8E6E2'},
    }
    return frame('smoke_studio', props, cam, {'kind': 'none', 'strength': 0.0}, 'barkhorn, Smoke, the studio take',
                 lights=lights, rotate_z=18.0, position=(0.0, 0.0, 0.0), samples=512, exposure=0.0,
                 fin=finish(contrast=0.05, clarity=0.03, bloom=0.03, bloom_px=30, threshold=0.9, vignette=0.15))


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=1.0, distance=5.0, azimuth=-20, lens=65, target=(0.0, 0.0, 0.9), fstop=5.6,
                                    shift_y=0.04))
