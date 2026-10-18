"""Fog, concept B: San Francisco's fog. A Marin headland at dawn: the clear speaker stands in the headland's dry grass
near its brow; beyond, the fog fills the valleys below and pours through a saddle in the hills across the water, lit
from behind by a sun just up. Its line: "Now you see it."

The clear acrylic disappears against white, so the frame keeps the horn against the dark, backlit ridge across the
water and the cabinet against the grass; the fog's glow sits beside it, under the sun. The land and the fog are
studio/engine/kit_ext/fog_b_el.py; the near ground, the grass and the rock are Poly Haven scans.
"""
import math

import common as C

SKY = 'syferfontein_6d_clear_puresky'

# the view: the camera's place and the compass direction it looks along (the engine's azimuth: 0 from -y, 90 from +x)
CAM = dict(height=1.15, distance=9.5, azimuth=-15.0, lens=85.0)
LOOK = 180.0 + CAM['azimuth']


def at(bearing, dist, look=LOOK):
    """A point `dist` metres off along `bearing` degrees right of the view's centre (from the origin: at a kilometre
    the camera's few metres do not matter)."""
    az = math.radians(look - bearing)
    return round(dist * math.sin(az), 1), round(-dist * math.cos(az), 1)


FLOOR = -140.0
# the hills across the water: [x, y, height above the floor, half-width along, across, turn]
def hills():
    a = at(-6.0, 950.0); b = at(17.0, 1250.0); c = at(-26.0, 2600.0); d = at(33.0, 2300.0); e = at(8.0, 1500.0)
    look = LOOK - 180.0
    return [[*a, 152.0, 520.0, 190.0, look + 8.0],      # the ridge behind the speaker's horn
            [*b, 145.0, 430.0, 210.0, look - 12.0],     # the ridge right of the sun
            [*e, 118.0, 260.0, 160.0, look],            # the saddle between them, low, the fog pours over it
            [*c, 205.0, 900.0, 420.0, look + 20.0],     # far hills, hazy
            [*d, 185.0, 800.0, 380.0, look - 25.0]]


def pours():
    s, a, b = at(8.0, 1400.0), at(-12.0, 880.0), at(21.0, 1180.0)
    return [[*s, 220.0, 320.0, LOOK - 180.0, 45.0],    # through the saddle
            [*a, 160.0, 240.0, LOOK - 180.0, 30.0],    # over the ridge behind the speaker
            [*b, 140.0, 220.0, LOOK - 180.0, 26.0]]


def sky_rot(sun_bearing):
    """The sky's turn that puts its sun `sun_bearing` degrees right of the view's centre."""
    az0 = C.assets.hdri_sun(SKY, 0.0)['azimuth_deg']              # turning the sky by r moves its sun to az0 - r
    return round((az0 - (LOOK - sun_bearing)) % 360.0, 1)


import os
SUN_BEARING = float(os.environ.get('FOG_B_SUN', -35.0))


def props():
    H = hills()
    return [
        # the headland's near ground: dry coastal grass, level where the speaker stands
        C.ground('sparse_grass', size=(26.0, 16.0), position=(0.0, -6.1, 0.0), displace=0.02, relief=0.12,
                 res='2k', tint='#8A7B55', tint_mix=0.2, cells=900),
        # the headland beyond, falling to the fog; the hills across the water
        C.piece('ext', module='fog_b_el', fn='terrain', hills=H, grass='#7A6C4A', scrub='#23281C', floor=FLOOR, brow=1.95, steep=10.0, drop=110.0, wide=50.0,
                y_range=[1.0, 6500.0], x_spread=[0.55, 1.05], x_margin=40.0, cols=560, row_ratio=0.004, min_row=0.3,
                relief=0.15, relief_far=0.008, gullies=[18.0, 170.0]),
        # the fog: a sea of it below, pouring through the saddle, a thin haze above
        C.piece('ext', module='fog_b_el', fn='fog', hills=H, floor=FLOOR, pours=pours(), top=-48.0, heave=8.0,
                billows=[[160.0, 12.0], [50.0, 5.0], [15.0, 1.5]], bank=34.0, bank_size=200.0, rise=[1000.0, 1800.0, 44.0],
                soft=5.0, density=0.06, anisotropy=0.65, billow_size=30.0, billow_cut=0.2, haze=0.00025, haze_height=170.0,
                box=[-3500.0, 3.0, -170.0, 4500.0, 7000.0, 320.0]),
        # wisps rising up the cliff just behind the brow
        C.piece('ext', module='fog_b_el', fn='fog', top=0.5, heave=4.0, billows=[[22.0, 5.0], [7.0, 1.5]],
                soft=4.0, density=0.035, anisotropy=0.6, billow_size=6.0, billow_cut=0.42, billow_gain=3.0,
                box=[-45.0, 2.6, -40.0, 70.0, 90.0, 4.0]),
        # grass tufts round the speaker and along the brow
        C.scatter(['grass_medium_02', 'grass_medium_01'], 1100, [-9.0, -13.0, 10.0, 1.5], avoid=((0.0, 0.0, 0.6),),
                  scale=(0.7, 1.4), seed=3),
        C.scatter(['grass_medium_02'], 40, [-8.0, 1.4, 12.0, 1.95], scale=(1.0, 1.6), seed=5),
        C.piece('ext', module='fog_b_el', fn='gulls', birds=[[*at(4.0, 160.0), 6.0, 1.3, 20, 0.8],
                                                               [*at(6.5, 190.0), 9.0, 1.3, -30, 0.2],
                                                               [*at(-2.0, 230.0), 13.0, 1.3, 50, 0.6]]),
    ]


def shot():
    cam = C.camera(**CAM, fstop=5.6, shift_x=0.15)
    cam['clip_end_m'] = 12000.0
    rot = sky_rot(SUN_BEARING)
    return C.shot('fog_b', props(), cam, C.sky(SKY, rotation_deg=rot, strength=1.0, res='4k'),
                  'barkhorn, Fog: San Francisco fog over a Marin headland at dawn',
                  sun=C.sun_from_sky(SKY, rot, irradiance=3.0), rotate_z=10.0, position=(0.0, 0.0, -0.008),
                  samples=512, fin=C.finish(vignette=0.15))


def portrait():
    return C.portrait_of(shot(), lens=40.0, shift_x=0.0)
