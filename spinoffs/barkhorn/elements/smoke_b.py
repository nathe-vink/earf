"""Smoke, concept B: high-key. A misty birch wood on a white winter morning: chalk-white trunks receding into the mist,
fresh snow, woodsmoke drifting low from somewhere unseen, soft light from an overcast sky. The smoked-black speaker
stands sharp against the pale mist, black on white, as a fashion editorial would set it, and the light coming through
its acrylic shows its tint. Its line: "Where there's smoke."

The trunks and the smoke are pieces of studio/engine/kit_ext/smoke_b_el.py (Poly Haven has no birch); the snow, the
sky and the bark's micro-relief are Poly Haven's. Notes and critic passes: smoke_b.md.
"""
import math, os, random

import common as C

CONCEPT = os.environ.get('SMOKE_B_CONCEPT', 'sidesun')
SKY = {'overcast': ('snow_field', 200.0, 1.0), 'sun': ('birchwood', 150.0, 1.0), 'sidesun': ('birchwood', 135.0, 1.0)}[CONCEPT]
SPEAKER_X = 0.0
ROT = -18.0                                               # the speaker's turn (degrees)


# a black flag out of frame on the camera's side, as a photographer would stand one: the speaker's front mirrors black,
# not the white wood behind the lens, so the smoked acrylic reads deep; and behind the speaker, a soft glow standing
# for the bright mist there, so light comes through the tint and draws its edges (critic pass 1, c3)
LIGHTS = {'negative': {'type': 'flag', 'size_m': [2.6, 2.0], 'orbit': {'azimuth_deg': -26.0, 'elevation_deg': 1.0,
                                                                     'distance_m': 1.8},
                       'target': [0.0, 0.0, 0.65], 'glossy': True},
          # and overhead, a second flag, keeping the bright sky out of the horn's flare
          'overhead': {'type': 'flag', 'size_m': [2.0, 2.0], 'orbit': {'azimuth_deg': -15.0, 'elevation_deg': 75.0,
                                                                      'distance_m': 1.8},
                       'target': [0.0, 0.0, 1.0], 'glossy': True},
          'mistglow': {**C.area(150.0, 18.0, 2.8, 7.0, color='#F2EEE6', size=(1.6, 2.2), target=(0.0, 0.0, 0.65)),
                       'specular': 0.1,                  # its light, not its mirror image
                       # the cabinet alone: through the horn's resin it blew the horn out white (pass 2; even a
                       # quarter of it, from behind the horn alone, turned it white in pass 3's tests)
                       'receivers': ['left', 'right', 'back', 'top', 'bottom', 'front-panel', 'lining-*', 'rib-*',
                                     'brace*', 'land-*', 'woofer-*', 'port-*']}}


def _trunks():
    """The wood: a few trunks near enough to read, then more and more, receding into the mist."""
    near = [(2.1, 2.6, 0.095, 2.5, 100, 1), (-1.15, 3.2, 0.085, 4.0, 200), (0.45, 6.2, 0.09, 1.5, 80),
            (2.4, 4.4, 0.075, 5.0, 20), (-2.6, 6.5, 0.11, 2.0, 250, 3), (-0.7, 9.5, 0.08, 3.0, 160),
            (3.6, 8.0, 0.10, 3.0, 300), (1.7, 11.5, 0.085, 1.0, 40, 2), (-0.35, 2.4, 0.035, 2.0, 120)]
    rnd = random.Random(31)
    far = []
    while len(far) < 70:
        y = 8.0 + 52.0 * rnd.random() ** 0.8
        x = rnd.uniform(-0.55, 0.55) * (8.0 + y * 1.1)
        if abs(x - SPEAKER_X) < 0.5 and y < 14:                      # nothing growing out of the speaker's head
            continue
        if any((x - a) ** 2 + (y - b) ** 2 < 1.2 ** 2 for a, b, *_ in near + far):
            continue
        far.append((round(x, 2), round(y, 2), round(rnd.uniform(0.05, 0.13), 3), round(rnd.uniform(0, 6), 1),
                    round(rnd.uniform(0, 360)), rnd.choice((1, 1, 1, 2, 3))))
    return [list(t) for t in near + far]


def props():
    return [
        C.piece('ext', module='smoke_b_el', fn='snow', texture='snow_02', size=[60.0, 60.0], position=[0.0, 18.0, 0.0],
                displace=0.0, relief=0.5, res='4k', cells=1500, flat=[0.0, 0.0, 1.2],
                procedural_relief=True, relief_bump=1.2),
        # snow banked a little against the speaker's foot (critic pass 1, c2)
        C.piece('ext', module='smoke_b_el', fn='snow_lip', size=[0.56, 0.43], rotate_z=ROT, height=0.03, reach=0.06,
                mat_object='prop0-kit'),
        # (no ground cover: scanned grass sunk in snow showed only rows of dots, and the critics read it as stickers;
        # the low sun's ripples and the trunks' shadows carry the snow's texture instead)
        C.piece('ext', module='smoke_b_el', fn='birches', trunks=_trunks(), height=17.0, seed=5, bark='bark_willow'),
        # woodsmoke in thin drifting sheets (a thick box averages its wisps away): one just behind the speaker, one
        # deeper in the wood, drifting in from the left, where a fire burns out of frame
        C.piece('ext', module='smoke_b_el', fn='smoke', box=[-6.0, 4.6, 0.0, 3.0, 5.6, 2.5], drift=6.0, height=1.5,
                thickness=0.5, density=10.0, lo=0.4, hi=0.6, scale=[0.35, 0.6, 1.8], distortion=1.4,
                fade_x=[3.0, -2.0], seed=3, color='#A9ABAE', absorb_color='#B8BBBE'),
        C.piece('ext', module='smoke_b_el', fn='smoke', box=[-14.0, 9.0, 0.0, 10.0, 10.8, 4.5], drift=-4.0, height=1.6,
                thickness=0.9, density=6.0, lo=0.4, hi=0.6, scale=[0.3, 0.5, 1.5], distortion=1.4,
                fade_x=[8.0, 0.0], seed=7, color='#A9ABAE', absorb_color='#B8BBBE'),
        # and its source: a column of woodsmoke rising behind the clump on the left, bent over toward the speaker
        C.piece('ext', module='smoke_b_el', fn='plume', base=[-2.66, 7.3], height=4.5, lean=3.5, bend=1.6, width=0.5,
                spread=0.35, density=25.0, seed=5, color='#A3A8AF', absorb_color='#B8BBBE'),
        C.piece('ext', module='smoke_b_el', fn='mist', box=[-45.0, -14.0, 0.0, 45.0, 95.0, 30.0], clear_y=1.0,
                full_y=26.0, density=0.05, floor=0.04, ground_boost=0.8, ground_h=4.0),
    ]


FIN = C.finish(contrast=0.12, clarity=0.05, sharpen=0.12, vignette=0.06, lift=0.02, lift_color='#16181A', bloom=0.08,
               bloom_px=30, threshold=0.85)
FIN['white_in'] = 212


def shot():
    hdri, rot, strength = SKY
    cam = C.camera(height=1.0, distance=7.6, azimuth=-12.0, lens=65.0, target=(SPEAKER_X, 0.0, 0.62), fstop=2.8,
                   shift_x=-0.24)
    sun = (C.sun_from_sky(hdri, rot, irradiance=2.5) if CONCEPT == 'sun' else
           dict(C.sun_from_sky(hdri, rot, irradiance=4.0, angle_deg=2.0, color='#FFE6C6'), elevation_deg=14.0)
           if CONCEPT == 'sidesun' else None)
    return C.shot('smoke_b', props(), cam, C.sky(hdri, rot, strength, res='4k'), 'Smoke: Where there\'s smoke. (B)',
                  lights=LIGHTS, sun=sun, rotate_z=ROT, position=(SPEAKER_X, 0.0, -0.09),
                  fin=FIN, exposure=1.3, white_balance=(6800, 10))


def portrait():
    return C.portrait_of(shot(), lens=50.0, shift_x=0.0)
