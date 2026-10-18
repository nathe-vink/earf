"""Fog, concept C: San Francisco you can name (the owner, 2026-10-18: "a classic foggy SF setting, overlooking the
golden gate and the city from marin headlands"). The clear speaker stands in the coastal grass of a Marin headland
about 110 m above the water. Below it the fog pours through the Gate under the bridge's deck, the two towers standing
out of it in a low sun. Beyond is the city, massed on its hills, and the wall of fog rolls over Twin Peaks and Sutro
Tower to the west.

The bridge, the city, Sutro and the fog are studio/engine/kit_ext/fog_c_el.py (procedural, at real scale); the
headland is fog_b_el's; the near ground, the grass and the rock are Poly Haven scans.
"""
import math, os

import common as C

SKY = 'syferfontein_6d_clear_puresky'
WATER = -110.0                       # the water, below the camera's ground (m)
CAM = dict(height=1.1, distance=5.5, azimuth=0.0, lens=50.0)
LOOK = 180.0 + CAM['azimuth']        # the view looks along +y
SUN_BEARING = float(os.environ.get('FOG_C_SUN', 62.0))


def at(b, d):
    return round(d * math.sin(math.radians(b)), 1), round(d * math.cos(math.radians(b)), 1)


def towers(n_bearing=13.0, n_dist=900.0, s_bearing=25.0):
    """The north tower at `n_bearing`, `n_dist`; the south tower 1280 m on, seen at `s_bearing`."""
    g = math.radians(s_bearing - n_bearing)
    d = n_dist * math.cos(g) + math.sqrt(1280.0 ** 2 - (n_dist * math.sin(g)) ** 2)
    return at(n_bearing, n_dist), at(s_bearing, d)


# the far shore: the distance to the water's edge along each bearing, and the hills the city stands on
LAND = dict(water=WATER, ground=30.0, coast=220.0,
            shore=[[-60.0, 5600.0], [-40.0, 5400.0], [-25.0, 5000.0], [-10.0, 4300.0], [0.0, 3600.0], [10.0, 3000.0],
                   [20.0, 2500.0], [26.0, 2350.0], [32.0, 2600.0], [38.0, 3300.0], [42.0, 1e9]],
            peaks=[[18.0, 3200.0, 80.0, 700.0], [2.0, 4800.0, 110.0, 900.0], [-8.0, 6000.0, 100.0, 600.0],
                   [14.0, 8500.0, 250.0, 1200.0], [18.0, 7600.0, 230.0, 700.0], [-25.0, 7500.0, 60.0, 1500.0]])


def sky_rot(sun_bearing):
    az0 = C.assets.hdri_sun(SKY, 0.0)['azimuth_deg']
    return round((az0 - (LOOK - sun_bearing)) % 360.0, 1)


def props():
    north, south = towers()
    return [
        # the headland: coastal grass, level where the speaker stands, falling to the water behind it
        C.ground('sparse_grass', size=(26.0, 18.6), position=(0.0, -5.7, 0.0), displace=0.02, relief=0.12,
                 res='2k', tint='#5F5A3A', tint_mix=0.3, cells=900),
        C.piece('ext', module='fog_b_el', fn='terrain', hills=[[*at(-6.0, 620.0), 96.0, 400.0, 200.0, 12.0], [*at(-32.0, 480.0), 105.0, 300.0, 220.0, 40.0]],
                grass='#5F5E40', scrub='#2A3320', floor=WATER - 5.0, brow=3.6, steep=10.0, drop=120.0, wide=60.0,
                y_range=[2.6, 1500.0], x_spread=[0.9, 1.1], x_margin=60.0, cols=400, row_ratio=0.006, min_row=0.3,
                relief=0.15, relief_far=0.01, gullies=[10.0, 120.0]),
        # the water, the far shore and its hills, the city, Sutro Tower
        C.piece('ext', module='fog_c_el', fn='water', water=WATER),
        C.piece('ext', module='fog_c_el', fn='land', **LAND, bearings=[-60.0, 45.0], d_range=[1800.0, 14000.0],
                cols=700, row_ratio=0.004),
        C.piece('ext', module='fog_c_el', fn='city', land=LAND, water=WATER, seed=4, grid_deg=12.0,
                houses=[-55.0, 40.0, 2500.0, 12000.0, 4500], downtown=[-5.0, 6800.0, 700.0, 170],
                salesforce=[-2.0, 7200.0], transamerica=[-7.0, 6500.0]),
        C.piece('ext', module='fog_c_el', fn='sutro', land=LAND, at=[18.0, 7600.0]),
        # the Golden Gate
        C.piece('ext', module='fog_c_el', fn='bridge', north=list(north), south=list(south), water=WATER,
                north_approach=700.0, south_approach=900.0),
        # the fog: under the deck in the Gate, higher over the ocean, a wall rolling over Twin Peaks; haze above
        C.piece('ext', module='fog_c_el', fn='fog', top=WATER + 50.0, heave=8.0,
                billows=[[220.0, 18.0], [70.0, 8.0], [20.0, 3.0]], wall=[16.0, 7800.0, 230.0, 14.0, 2500.0],
                ocean=[6.0, 90.0, 1100.0], ocean_width=20.0, soft=6.0, density=0.03, anisotropy=0.7, billow_size=40.0, billow_cut=0.25,
                haze=0.00012, haze_height=300.0, box=[-11000.0, 150.0, WATER - 5.0, 11000.0, 15000.0, 700.0]),
        # grass round the speaker
        C.scatter(['grass_medium_02', 'grass_medium_01'], 3000, [-9.0, -14.5, 11.0, 3.2],
                  avoid=((0.0, 0.0, 3.2),), scale=(0.4, 1.6), seed=3),
        C.scatter(['grass_medium_02', 'grass_medium_01'], 900, [-3.2, -3.2, 3.2, 3.2], avoid=((0.0, 0.0, 1.0),),
                  scale=(0.4, 0.9), seed=11),
        C.scatter(['grass_medium_02'], 60, [-1.1, -1.1, 1.1, 1.1], avoid=((0.0, 0.0, 0.42),), scale=(0.2, 0.35), seed=7),
    ]


def shot():
    cam = C.camera(**CAM, fstop=5.6, shift_x=0.23)
    cam['clip_end'] = 20000.0
    rot = sky_rot(SUN_BEARING)
    s = C.shot('fog_c', props(), cam, C.sky(SKY, rotation_deg=rot, strength=1.0, res='4k'),
               'barkhorn, Fog: over the Golden Gate from the Marin Headlands',
               sun=C.sun_from_sky(SKY, rot, irradiance=4.0), rotate_z=25.0, position=(0.0, 0.0, -0.015),
               samples=512, fin=C.finish(contrast=0.10, clarity=0.06, saturation=0.06, vignette=0.15))
    return s


def portrait():
    cam = C.camera(**{**CAM, 'distance': 4.6}, fstop=5.6, shift_y=0.05)
    cam['clip_end'] = 20000.0
    s = C.portrait_of(shot())
    s['camera'] = cam
    return s
