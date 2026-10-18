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
SKY = {'a': ('belfast_sunset_puresky', 83.0, 0.4), 'b': ('kloppenheim_01_puresky', -40.0, 0.55)}[V]
CAM = dict(height=0.85, distance=9.2, azimuth=-12.0, lens=80.0, target=(0.0, 0.0, 0.62), fstop=3.5)


def ext(fn, **k):
    return C.piece('ext', module='acid_rain_el', fn=fn, **k)


def props(cam):
    feet = [0.0, 0.0, 0.5]
    return [
        # the lava field: black rock, wet, broadly undulating so the rain pools in its hollows
        ext('wet_ground', texture='dark_rock', size=[40.0, 44.0], position=[0.0, 14.0, 0.0], cells=1700, displace=0.03,
            relief=False, flat=[0.0, 0.0, 0.7], res='4k', tex_scale=1.4, bump=2.0, rough_mul=0.8, darken=0.5, film=0.5, tint='#2B2721', tint_mix=0.55,
            film_rough=0.28, lumps=[[2.6, 0.12, 'billow'], [0.9, 0.03, 'ridged'], [0.35, 0.025, 'fbm'], [0.12, 0.008, 'fbm'], [9.0, 0.14]],
            dips=[[-0.2, -1.2, 1.2, 0.2], [-0.55, -2.7, 1.5, 0.22], [-0.85, -4.1, 1.6, 0.22], [-1.1, -5.4, 1.4, 0.2],
                  [2.6, 2.4, 1.6, 0.18]], seed=2),
        # beyond it, the same field on toward the hills, coarse (it is far and in the haze)
        ext('wet_ground', texture='dark_rock_02', size=[560.0, 230.0], position=[0.0, 125.0, -0.12], cells=600,
            displace=0.0, relief=False, flat=[0.0, 0.0, 26.0], res='2k', tex_scale=5.0, rough_mul=0.5,
            darken=0.5, film=0.6, film_rough=0.2, tint='#2B2721', tint_mix=0.55, lumps=[[2.5, 0.35, 'ridged'], [7.0, 0.5, 'billow'], [25.0, 1.2]], seed=3),
        # standing water in the hollows, ringed by the drops
        ext('puddle', size=[40.0, 44.0], position=[0.0, 14.0, 0.0], z=-0.11, ring=0.14, ripple=0.6, ripple_m=0.0012),
        # black boulders: one out of focus close at the left, a couple behind on the field
        ext('rock', model='rock_09', position=[-2.5, -2.4, -0.05], rotate=[0, 0, 40], scale=1.1, darken=0.5,
            film_rough=0.15),
        ext('rock', model='moon_rock_04', position=[4.4, 7.8, -0.1], rotate=[0, 0, 200], scale=1.6, darken=0.8,
            film_rough=0.12),
        ext('rock', model='moon_rock_01', position=[-4.2, 10.0, -0.05], rotate=[0, 0, 70], scale=1.4, darken=0.8,
            film_rough=0.12),
        # loose blocks of lava over the field, thinning toward the hills
        ext('rocks', models=['rock_09', 'moon_rock_01', 'moon_rock_04', 'rock_07'], count=160, area=[-22.0, 3.0, 26.0, 45.0],
            avoid=[[0.0, 0.0, 3.5]], scale=[0.25, 1.4], z=-0.08, seed=8, darken=0.75, film_rough=0.14, tilt_deg=15.0),
        # low volcanic hills far off, in the rain
        ext('ridge', position=[0.0, 170.0, -1.0], width=520.0, depth=58.0, height=11.0, spacing=150.0, seed=21,
            film=0.2, film_rough=0.45),
        # the rain, and where it lands
        ext('rain', camera=cam, count=70000, near=1.0, far=60.0, length=[0.05, 0.16], radius=[0.0006, 0.0012],
            lean=[0.09, 0.02], z=[0.0, 14.0], opacity=0.55, scatter=0.7, avoid=[[0.0, 0.0, 0.4]], seed=3),
        ext('splashes', area=[-3.5, -3.0, 3.5, 6.0], z=-0.11, count=160, radius=[0.004, 0.011], opacity=0.6,
            avoid=[[0.0, 0.0, 0.45]], seed=5),
    ]


def shot():
    hdri, rot, strength = SKY
    cam = C.camera(**CAM)
    sun = C.sun_from_sky(hdri, rot, irradiance=3.0, angle_deg=2.0, color='#F4D98A')
    lights = {
        # a photographer's soft bounce from the camera's side, low: it lifts the speaker's shaded front a little
        'bounce': C.area(-30, 8, 3.5, 0.25, '#E9E2C4', size=(1.2, 1.2)),
    }
    s = C.shot(NAME, props(cam), cam, C.sky(hdri, rot, strength=strength, res='4k'), 'barkhorn Acid, acid rain',
               lights=lights, sun=sun, rotate_z=16.0, exposure=-0.55,
               haze={'density': 0.005, 'anisotropy': 0.6, 'color': '#DCDD9A', 'box_m': [-300, -15, -2, 300, 232, 50]},
               fin=C.finish(contrast=0.1, clarity=0.07, sharpen=0.25, vignette=0.14))
    s['render']['white_balance_k'] = 6400
    s['render']['white_balance_tint'] = -6.0
    return s


def portrait():
    s = shot()
    p = C.portrait_of(s)
    cam = C.camera(**{**CAM, 'distance': 5.0, 'lens': 45.0})
    p['camera'] = cam
    for pr in p['set']['props']:
        if pr.get('fn') == 'rain':
            pr['camera'] = cam
            pr['frame_h'] = 36.0 * 2000 / 1600
    return p
