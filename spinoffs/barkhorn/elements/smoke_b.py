"""Smoke, concept B: high-key. A misty birch wood on a white winter morning: chalk-white trunks receding into the mist,
fresh snow, woodsmoke drifting low from somewhere unseen, soft light from an overcast sky. The smoked-black speaker
stands sharp against the pale mist, black on white, as a fashion editorial would set it, and the light coming through
its acrylic shows its tint. Its line: "Where there's smoke."

The trunks and the smoke are pieces of studio/engine/kit_ext/smoke_b_el.py (Poly Haven has no birch); the snow, the
sky and the bark's micro-relief are Poly Haven's. Notes and critic passes: smoke_b.md.
"""
import math, os, random

import common as C

CONCEPT = os.environ.get('SMOKE_B_CONCEPT', 'overcast')
SKY = {'overcast': ('snow_field', 200.0, 1.0), 'sun': ('birchwood', 150.0, 1.0)}[CONCEPT]
SPEAKER_X = 0.0


# a black flag out of frame on the camera's side, as a photographer would stand one: the speaker's front mirrors black,
# not the white wood behind the lens, so the smoked acrylic reads deep; and behind the speaker, a soft glow standing
# for the bright mist there, so light comes through the tint and draws its edges (critic pass 1, c3)
LIGHTS = {'negative': {'type': 'flag', 'size_m': [2.0, 1.6], 'orbit': {'azimuth_deg': -26.0, 'elevation_deg': 1.0,
                                                                     'distance_m': 3.2},
                       'target': [0.0, 0.0, 0.65], 'glossy': True},
          'mistglow': {**C.area(165.0, 6.0, 2.8, 2.0, color='#F4F1EC', size=(1.2, 1.8), target=(0.0, 0.0, 0.65)),
                       'specular': 0.1}}                 # its light, not its mirror image on the horn's top


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
                displace=0.015, relief=0.22, res='4k', cells=1500, flat=[0.0, 0.0, 1.2]),
        # last summer's grass, dry through the snow in clumps at the trunks' feet, a few strays between
        *[C.piece('ext', module='smoke_b_el', fn='dry_scatter', models=['grass_medium_01', 'grass_medium_02'], count=n,
                  area=[x - r, y - r, x + r, y + r], avoid=[[0.0, 0.0, 0.9]], scale=[0.4, 1.4], z=-0.04, seed=11 + i,
                  res='1k')
          for i, (x, y, r, n) in enumerate([(-1.15, 3.2, 0.7, 7), (2.1, 2.6, 0.6, 6), (-2.6, 6.5, 0.9, 7),
                                            (2.4, 4.4, 0.5, 4), (0.45, 6.2, 0.6, 4), (0.0, 4.0, 4.0, 7)])],
        C.piece('ext', module='smoke_b_el', fn='birches', trunks=_trunks(), height=17.0, seed=5, bark='bark_willow'),
        # woodsmoke in thin drifting sheets (a thick box averages its wisps away): one just behind the speaker, one
        # deeper in the wood, drifting in from the left, where a fire burns out of frame
        C.piece('ext', module='smoke_b_el', fn='smoke', box=[-6.0, 2.5, 0.0, 3.0, 3.5, 2.5], drift=6.0, height=1.1,
                thickness=0.4, density=14.0, lo=0.4, hi=0.6, scale=[0.35, 0.6, 1.8], distortion=1.4,
                fade_x=[3.0, -2.0], seed=3, color='#B8B2AA', absorb_color='#A09890'),
        C.piece('ext', module='smoke_b_el', fn='smoke', box=[-14.0, 9.0, 0.0, 10.0, 10.8, 4.5], drift=-4.0, height=1.6,
                thickness=0.9, density=6.0, lo=0.4, hi=0.6, scale=[0.3, 0.5, 1.5], distortion=1.4,
                fade_x=[8.0, 0.0], seed=7, color='#9A9FA6', absorb_color='#A09890'),
        C.piece('ext', module='smoke_b_el', fn='mist', box=[-45.0, -14.0, 0.0, 45.0, 95.0, 30.0], clear_y=1.0,
                full_y=26.0, density=0.07, floor=0.06, ground_boost=0.8, ground_h=4.0),
    ]


FIN = C.finish(contrast=0.04, clarity=0.05, sharpen=0.25, vignette=0.06, lift=0.02, lift_color='#1A1612')
FIN['white_in'] = 228


def shot():
    hdri, rot, strength = SKY
    cam = C.camera(height=1.0, distance=7.6, azimuth=-12.0, lens=65.0, target=(SPEAKER_X, 0.0, 0.62), fstop=2.8,
                   shift_x=-0.24)
    sun = C.sun_from_sky(hdri, rot, irradiance=2.5) if CONCEPT == 'sun' else None
    return C.shot('smoke_b', props(), cam, C.sky(hdri, rot, strength, res='4k'), 'Smoke: Where there\'s smoke. (B)',
                  lights=LIGHTS, sun=sun, rotate_z=-18.0, position=(SPEAKER_X, 0.0, -0.025),
                  fin=FIN, exposure=1.55, white_balance=(7000, 10))


def portrait():
    return C.portrait_of(shot(), lens=50.0, shift_x=0.0)
