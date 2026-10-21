"""Smoke, setting E3: the studio take (round E, the coordinator's third setting; a deliberate step outside the series'
locations).

The speaker on black, on a black gloss floor that mirrors it. A column of smoke rises behind and left of it (its
source unseen, a studio convention), climbs beside it and rolls over above the waveguide, never in front: rim-lit from behind on both sides as a fragrance or
whisky campaign lights its smoke: bright edges against the dark, no haze, no source in frame.
"""
import math, random

from common import area, camera, finish, piece, shot as frame, portrait_of
from smoke import SHELL, SPEAKER


def column(seed=5, color='#DADDE2', density=7.0, cut=0.44, fade_in=(0.12, 1.0)):
    """One column, rising out of the dark behind and left of the speaker (its source unseen), crossing behind the
    waveguide so the horn stands against it, then rolling up and away to the right as it widens, billows and thins.
    Nothing crosses the front or touches the shell, and it never seems to come out of the speaker."""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]
    # the column's spine: (t, x, y) knots from the floor (t 0) to the top of the frame (t 1)
    knots = [(0.0, -1.1, 0.85), (0.35, -1.0, 0.85), (0.6, -0.55, 0.9), (0.8, 0.05, 0.8), (1.0, 0.55, 0.5)]
    pts, rr = [], []
    n = 48
    for i in range(n):
        t = i / (n - 1)
        j = max(k for k in range(len(knots) - 1) if knots[k][0] <= t)
        (t0, x0, y0), (t1, x1, y1) = knots[j], knots[j + 1]
        f = (t - t0) / (t1 - t0); f = f * f * (3 - 2 * f)
        w = 0.04 * t
        x = x0 + (x1 - x0) * f + w * math.sin(11 * t + ph[0])
        y = y0 + (y1 - y0) * f + w * math.cos(9 * t + ph[1])
        z = 0.12 + 2.45 * t
        pts.append([round(x, 4), round(y, 4), round(z, 4)])
        rr.append(round(0.1 + 0.3 * t ** 1.1 + 0.2 * max(0.0, t - 0.5), 4))
    return piece('ext', module='smoke_el', fn='ribbon', strands=[{'points': pts, 'radii': rr, 'density': density}], layers=6,
                 scale=0.07, cut=cut, soft=0.3, rise=1.6, laminar=0.0, laminar_blend=0.05, fade=[1.9, 2.4],
                 color=color, anisotropy=0.6, detail=7.0, distortion=0.8, seed=seed, wobble=0.35, wobble_freq=6.0,
                 break_scale=0.45, break_cut=0.35, break_floor=0.15, fade_in=list(fade_in), grid=True, voxel=0.012)


def shot():
    props = [piece('box', size=[24.0, 24.0, 0.02], position=[0.0, 0.0, -0.02], material='gloss', color='#0B0B0B',
                   roughness=0.15),
             column(),
             # a dark backdrop far behind the speaker, its edges out of frame, lit in a soft pool so the black cabinet
             # has a graded ground to stand against
             piece('box', size=[14.0, 0.05, 7.0], position=[0.5, 5.5, 0.0], material='clay', color='#2A2826')]
    cam = camera(height=0.6, distance=5.2, azimuth=-20, lens=65, target=(0.0, 0.0, 0.9), fstop=5.6, shift_x=0.0,
                 shift_y=-0.05)
    lights = {
        'skyfill': {**area(-20, 5, 2.4, 4.0, '#C8CCD4', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 10.0, '#C9C4BC', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 26.0, '#F2EEE8', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 18.0, '#F2EEE8', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        # the smoke's rims: two tall strips behind, left and right, high enough that the gloss floor's mirror image of
        # them falls out of frame (seen through the smoke, a low one showed as a lit card on the floor)
        'rim_l': {**area(-145, 40, 3.0, 40.0, '#F4F0EA', (0.4, 2.6), (0.0, 0.0, 1.1)), 'specular': 0.0},
        'rim_r': {**area(145, 40, 3.0, 30.0, '#E6ECF4', (0.4, 2.6), (0.0, 0.0, 1.1)), 'specular': 0.0},
        # a soft top so the black floor's gloss shows a horizon of light under the speaker
        'top': {'type': 'area', 'size_m': [2.0, 1.0], 'position': [0.0, 1.6, 3.2], 'target': [0.0, 0.3, 0.0],
                'irradiance': 3.0, 'color': '#E8E6E2', 'specular': 0.25},
        # the pool on the backdrop: a soft spot from high behind the camera, on the card alone
        'pool': {'type': 'spot', 'position': [-1.0, -3.0, 4.0], 'target': [0.4, 5.5, 0.8], 'power_w': 3500,
                 'cone_deg': 22.0, 'blend': 1.0, 'color': '#D8D4CE', 'radius_m': 0.3},
    }
    return frame('smoke_studio', props, cam, {'kind': 'none', 'strength': 0.0}, 'barkhorn, Smoke, the studio take',
                 lights=lights, rotate_z=18.0, position=(0.0, 0.0, 0.0), samples=512, exposure=0.0,
                 fin=finish(contrast=0.05, clarity=0.03, bloom=0.03, bloom_px=30, threshold=0.9, vignette=0.15))


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=0.6, distance=5.0, azimuth=-20, lens=65, target=(0.0, 0.0, 0.9), fstop=5.6,
                                    shift_y=0.04))
