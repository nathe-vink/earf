"""Acid, concept B: acid rain, real. A storm in sulphurous light over a field of wet black lava rock; the light breaks
through low behind the rain, so every streak catches it, the wet rock shines and the puddles mirror the golden speaker.
Rain as a shutter of about 1/60 s records it (streaks a few to 15 cm long, aligned with the fall, scattered through the
depth), with crowns and rings where it lands. No strings. The pieces are studio/engine/kit_ext/acid_rain_el.py.

    python3 spinoffs/barkhorn/elements/build.py acid_b
"""
import os

import common as C

NAME = 'acid_b'
V = os.environ.get('ACID_B_VARIANT', 'a')                 # the concept proofs: a backlit gap, b a side-back sun
SKY = {'a': ('belfast_sunset_puresky', 265.0, 0.24), 'b': ('kloppenheim_01_puresky', -40.0, 0.55)}[V]
# the sun's line from the speaker (azimuth 148): nothing stands on it to shade the speaker
SUN_LINE = [[2.5, 4, 2.5], [4.38, 7, 2.5], [6.25, 10, 2.5], [8.12, 13, 2.5], [10.0, 16, 2.5], [11.88, 19, 2.5], [13.75, 22, 2.5], [15.62, 25, 2.5], [17.5, 28, 2.5], [19.38, 31, 2.5], [21.25, 34, 2.5], [23.12, 37, 2.5]]
SUN_FAR = [[round(0.625 * t, 1), round(t, 1), 6.0 + 0.04 * t] for t in range(45, 160, 8)]
CAM = dict(height=0.85, distance=9.2, azimuth=-12.0, lens=80.0, target=(0.0, 0.0, 0.62), fstop=4.5)


def ext(fn, **k):
    return C.piece('ext', module='acid_rain_el', fn=fn, **k)


def props(cam):
    feet = [0.0, 0.0, 0.5]
    return [
        # the lava field: black rock, wet, broadly undulating so the rain pools in its hollows
        ext('wet_ground', texture='dark_rock', size=[40.0, 44.0], position=[0.0, 14.0, 0.0], cells=1700, displace=0.07,
            relief=False, flat=[0.0, 0.0, 0.7], res='4k', tex_scale=0.8, bump=3.0, rough_mul=0.8, darken=0.55, film=0.3, tint='#1E1D17', tint_mix=0.7,
            film_rough=0.33, film_vary=[0.05, 0.35], lumps=[[2.6, 0.06, 'billow'], [1.1, 0.04, 'fbm'], [0.9, 0.03, 'ridged'], [0.3, 0.02, 'fbm'], [0.12, 0.008, 'fbm'],
                   [9.0, 0.05]],
            dips=[[0.0, 0.0, 1.1, 0.16], [-0.2, -1.2, 1.2, 0.2], [-0.55, -2.7, 1.5, 0.22], [-0.85, -4.1, 1.6, 0.22], [-1.1, -5.4, 1.4, 0.2],
                  [2.6, 2.4, 1.6, 0.18]], seed=2),
        # beyond it, the same field on to the horizon, coarse (it is far and in the haze)
        ext('wet_ground', texture='dark_rock', size=[900.0, 700.0], position=[0.0, 345.0, -0.12], cells=700,
            displace=0.0, relief=False, flat=[0.0, 0.0, 26.0], res='2k', tex_scale=3.0, rough_mul=0.5,
            darken=0.72, film=0.4, film_rough=0.18, tint='#1E1D17', tint_mix=0.7, lumps=[[2.5, 0.3, 'ridged'], [7.0, 0.4, 'billow'], [25.0, 0.5]], seed=3),
        # standing water in the hollows, ringed by the drops
        ext('puddle', size=[40.0, 44.0], position=[0.0, 14.0, 0.0], z=-0.11, ring=0.2, ripple=3.0, keep=1.0, roughness=0.02, ripple_m=0.0012),
        # black boulders: one out of focus close at the left, a couple behind on the field
        ext('rock', model='rock_09', position=[-2.5, -2.4, -0.05], rotate=[0, 0, 40], scale=1.1, darken=0.5,
            film_rough=0.15),
        ext('rock', model='moon_rock_04', position=[4.4, 7.8, -0.1], rotate=[0, 0, 200], scale=1.6, darken=0.8,
            film_rough=0.12),
        ext('rock', model='moon_rock_01', position=[-4.2, 10.0, -0.05], rotate=[0, 0, 70], scale=1.4, darken=0.8,
            film_rough=0.12),
        # loose blocks of lava over the field, thinning toward the hills
        ext('rocks', models=['rock_09', 'moon_rock_01', 'moon_rock_04', 'rock_07'], count=160, area=[-22.0, 3.0, 26.0, 45.0],
            avoid=[[0.0, 0.0, 3.5]] + SUN_LINE, scale=[0.25, 1.4], z=-0.08, seed=8, darken=0.75, film_rough=0.35, tilt_deg=15.0),
        # more blocks on the far field, so their tops break its line
        ext('rocks', models=['rock_09', 'moon_rock_04'], count=40, area=[-30.0, 25.0, 40.0, 80.0],
            scale=[0.8, 2.2], z=-0.2, seed=28, darken=0.75, film_rough=0.5, tilt_deg=15.0, avoid=SUN_FAR + SUN_LINE),
        ext('rocks', models=['rock_09', 'moon_rock_01', 'moon_rock_04'], count=220, area=[-60.0, 45.0, 90.0, 150.0],
            scale=[1.0, 3.0], z=-0.3, seed=18, darken=0.75, film_rough=0.5, tilt_deg=15.0, avoid=SUN_FAR),
        # the rain, and where it lands
        ext('rain', camera=cam, count=90000, near=5.0, far=60.0, length=[0.04, 0.18], radius=[0.0008, 0.0014],
            lean=[0.09, 0.02], z=[0.0, 30.0], opacity=[0.1, 0.6], scatter=0.9, rough=0.25, clear=0.25,
            avoid=[[0.0, 0.0, 0.4]], seed=3),
        # a few drops close to the lens, far out of focus
        ext('rain', camera=cam, count=30, near=1.5, far=4.0, length=[0.04, 0.08], radius=[0.0006, 0.001],
            lean=[0.09, 0.02], z=[0.0, 30.0], opacity=[0.15, 0.35], scatter=0.7, rough=0.25, seed=13),
        # and the curtain beyond, too fine to count
        ext('rain', camera=cam, count=300000, near=15.0, far=120.0, length=[0.06, 0.18], radius=[0.0006, 0.0009],
            lean=[0.09, 0.02], z=[0.0, 30.0], opacity=0.08, scatter=0.9, rough=0.25, clear=0.3, seed=23),
        ext('splashes', area=[-3.0, -7.0, 3.5, 3.0], z=-0.11, count=3000, radius=[0.004, 0.01], opacity=0.25,
            avoid=[[0.0, 0.0, 0.45]], seed=5),
    ]


def shot():
    hdri, rot, strength = SKY
    cam = C.camera(**CAM)
    cam['clip_end_m'] = 1500.0
    sun = C.sun_from_sky(hdri, rot, irradiance=11.0, angle_deg=2.0, color='#E8DC7A')
    lights = {
        # a photographer's soft bounce from the camera's side, low: it lifts the speaker's shaded front a little
        'bounce': C.area(-35, 10, 3.5, 0.9, '#F1E6B8', size=(2.0, 2.0)),
        # a small card low in front, as a photographer would hold one, into the horn's throat
        'throat': C.area(-8, 4, 2.2, 0.5, '#F1E6B8', size=(0.5, 0.4), target=(0.0, 0.0, 1.15)),
        'fill': C.area(30, 8, 3.5, 0.2, '#F1E6B8', size=(1.2, 1.2)),
    }
    s = C.shot(NAME, props(cam), cam, C.sky(hdri, rot, strength=strength, res='4k'), 'barkhorn Acid, acid rain',
               lights=lights, sun=sun, white_balance=(6200, -18.0), rotate_z=16.0, position=(0.0, 0.0, -0.09), exposure=-0.35, look='AgX - Medium High Contrast',
               haze={'density': 0.0012, 'anisotropy': 0.5, 'color': '#C8CC6A', 'box_m': [-400, -15, -2, 400, 400, 15]},
               fin=C.finish(contrast=0.22, clarity=0.07, sharpen=0.35, vignette=0.14))
    return s


def portrait():
    s = shot()
    p = C.portrait_of(s)
    cam = C.camera(**{**CAM, 'distance': 6.0, 'lens': 85.0})
    cam['clip_end_m'] = 1500.0
    p['camera'] = cam
    for pr in p['set']['props']:
        if pr.get('fn') == 'rain':
            pr['camera'] = cam
            pr['frame_h'] = 36.0 * 2000 / 1600
    return p
