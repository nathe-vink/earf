"""Smoke, setting E5: black smoke on a salt pan (the coordinator, 2026-10-20, after the owner: "it should really be
black smoke"; a location with real black smoke and no forced fire).

A dry salt pan at a low sun, its white crust cracked into plates to the horizon. The speaker stands on the crust with its
long shadow. A few metres off, a little out of focus, a black smoke canister of the kind photographers use lies on its
side; its plume rolls low over the crust behind the speaker, then climbs. Monochrome: white ground, black smoke, the
smoked-black speaker.
"""
import math, random

from common import area, camera, finish, ground, piece, shot as frame, portrait_of, sun_from_sky, sky
from smoke import SHELL, SPEAKER

SKY = 'aarfontein_pan'                      # a real dry lake bed at a low sun (Poly Haven, CC0)
SKY_ROT = 124.0                             # the sky's low sun to the front-left, so the speaker's shadow falls behind it
CAN = (1.9, 1.4)                           # the canister, on the crust right of and behind the speaker


def canister():
    """A smoke canister on its side: a matte black tin with a pull ring, its open end toward the speaker."""
    x, y = CAN
    return [piece('cylinder', radius=0.033, height=0.15, position=[x, y, 0.033], rotate=[0.0, -90.0, 20.0],
                  material='clay', color='#151515', roughness=0.6),
            piece('cylinder', radius=0.034, height=0.012, position=[x + 0.005, y + 0.002, 0.033], rotate=[0.0, -90.0, 20.0],
                  material='foil', color='#5A5A5A', roughness=0.4)]


def plume(seed=9):
    """The canister's smoke: out of its end low over the crust, rolling left behind the speaker, then climbing."""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]
    knots = [(0.0, CAN[0] - 0.15, CAN[1] - 0.05, 0.05), (0.25, 0.9, 1.3, 0.15), (0.5, -0.1, 1.1, 0.35),
             (0.7, -0.7, 0.9, 0.9), (0.85, -0.9, 0.8, 1.6), (1.0, -0.8, 0.8, 2.6)]
    pts, rr = [], []
    n = 56
    for i in range(n):
        t = i / (n - 1)
        j = max(k for k in range(len(knots) - 1) if knots[k][0] <= t)
        (t0, x0, y0, z0), (t1, x1, y1, z1) = knots[j], knots[j + 1]
        f = (t - t0) / (t1 - t0); f = f * f * (3 - 2 * f)
        w = 0.05 * t
        pts.append([round(x0 + (x1 - x0) * f + w * math.sin(9 * t + ph[0]), 4),
                    round(y0 + (y1 - y0) * f + w * math.cos(7 * t + ph[1]), 4),
                    round(max(0.06 + 0.04 * t, z0 + (z1 - z0) * f), 4)])
        rr.append(round(0.07 + 0.25 * t ** 0.9 + 0.25 * max(0.0, t - 0.6), 4))
    return piece('ext', module='smoke_el', fn='ribbon', strands=[{'points': pts, 'radii': rr, 'density': 55.0}], layers=6,
                 scale=0.07, cut=0.38, soft=0.3, rise=1.4, laminar=0.0, laminar_blend=0.05, fade=[2.2, 2.9],
                 color='#0C0C0C', anisotropy=0.3, detail=7.0, distortion=0.8, seed=seed, wobble=0.35, wobble_freq=6.0,
                 break_scale=0.5, break_cut=0.35, break_floor=0.35, grid=True, voxel=0.02)


def shot():
    props = [ground('dry_ground_01', size=(40.0, 40.0), position=(0.0, 14.0, 0.0), displace=0.0, relief=0.05,
                    res='2k', tint='#F0EEEA', tint_mix=0.95),
             plume()] + canister()
    cam = camera(height=0.8, distance=5.6, azimuth=-20, lens=65, target=(0.0, 0.0, 0.85), fstop=4.0, shift_x=0.05)
    lights = {
        'skyfill': {**area(-20, 5, 2.4, 2.0, '#DCE2EA', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 6.0, '#E6E2DA', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 22.0, '#FFE6CC', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 16.0, '#FFE6CC', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
    }
    return frame('smoke_saltflat', props, cam, sky(SKY, rotation_deg=SKY_ROT, strength=1.0),
                 'barkhorn, Smoke, black smoke on a salt pan', sun={**sun_from_sky(SKY, SKY_ROT, irradiance=9.0), 'elevation_deg': 14.0},
                 lights=lights, rotate_z=18.0, position=(0.0, 0.0, -0.01), samples=512, exposure=0.3,
                 fin=finish(contrast=0.05, clarity=0.03, saturation=-0.9, vignette=0.15))


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=0.8, distance=4.6, azimuth=-20, lens=65, target=(0.0, 0.0, 0.85), fstop=4.0,
                                    shift_y=0.05))
