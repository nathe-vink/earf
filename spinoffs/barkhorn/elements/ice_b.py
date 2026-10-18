"""Ice, concept B: Jokulsarlon's Diamond Beach at sunrise. The speaker stands on black volcanic sand above the wash,
among chunks of glacier ice the lagoon has given to the sea; the sun, just up over the North Atlantic, comes through
the ice as it comes through the speaker's blue acrylic. Keeps its cool.

The beach, the sea and the ice are studio/engine/kit_ext/ice_b_el.py; the sky is a photographed sunrise over the sea.
"""
import math
import common as C

# --- the cave (the concept since pass 3: see ice_b.md) --------------------------------------------------------------
CAVE_SKY = 'snowy_hillside'         # outside: snow under a clear winter sun (Poly Haven, CC0)
CAVE_FLOOR = {'y0': 100.0, 'slope': 0.0, 'wiggle': 0.0, 'freq': 0.0, 'phase': 0.0, 'water_z': -5.0}


def cave_props():
    return [C.piece('ext', module='ice_b_el', fn='cave', y_range=[-6.2, 22.0], width=4.6, height=3.3,
                    bend=[3.0, 9.0], scallop=[0.5, 0.06], thickness=[0.9, 2.2], hole=[13.5, 1.3, 2.6, 1.0],
                    ice={'absorb': '#3E93DC', 'density': 1.2}),
            C.piece('ext', module='ice_b_el', fn='beach', shore=CAVE_FLOOR, texture='gravelly_sand', res='4k',
                    extent=[-6.0, -6.4, 14.0, 23.0], fine=[-3.0, -4.0, 3.0, 6.0], displace=0.006, relief=0.05,
                    dark='#0A0A0B', light='#2A2A2B', tex_scale=1.25, spec=0.05, bump=1.2, wet_h=-1.0, damp_h=-0.5,
                    damp_base=0.0, puddles=[0.45, 0.62], wet_rough=0.03, grain_m=0.003, glint_share=0.02)]


def shot(az=167.0, sun_irr=4.0):
    r0 = C.assets.hdri_sun(CAVE_SKY, 0.0)['azimuth_deg']
    rot = round((r0 - az) % 360.0, 2)
    sun = C.sun_from_sky(CAVE_SKY, rot, irradiance=sun_irr)
    sk = C.sky(CAVE_SKY, rotation_deg=rot, strength=1.0, res='4k')
    # the mouth's daylight, 6 m behind the speaker and just behind the camera: a soft panel where the opening is (the
    # snowfield and sky through it), as a photographer would let it in or bounce it
    mouth = {'type': 'area', 'position': [-0.6, -6.0, 1.5], 'size_m': [3.6, 2.6], 'target': [0.0, 0.0, 0.7],
             'irradiance': 0.85, 'color': '#EAF1FF'}
    s = C.shot('ice_b', cave_props(), C.camera(height=1.0, distance=5.0, azimuth=-15.0, lens=35.0,
                                               target=(0.0, 0.0, 0.75), fstop=4.0),
               sk, 'Ice: in a glacier ice cave', sun=sun, lights={'mouth': mouth}, rotate_z=12.0, position=(0.0, 0.0, -0.01), exposure=1.5,
               fin=C.finish(contrast=0.06, clarity=0.05, sharpen=0.25, vignette=0.15),
               haze={'box_m': [-5.0, -6.0, 0.0, 12.0, 21.5, 4.5], 'density': 0.008, 'anisotropy': 0.55, 'color': '#FFFFFF'})
    s['render']['volume_bounces'] = 4
    s['render']['bounces'] = 16
    return s


def portrait():
    s = shot()
    cam = s['camera']
    return C.portrait_of(s, **C.camera(height=cam['position'][2], distance=6.2, azimuth=-15.0, lens=40.0,
                                       target=tuple(cam['target']), fstop=cam['fstop']))

SKY = 'umhlanga_sunrise'           # a sunrise over open sea, the sun on the horizon (Poly Haven, CC0)
SUN_AZ = 169.5                     # the sun just behind the cabinet's upper left (from +y, a little +x)
SHORE = {'y0': 0.2, 'slope': 0.05, 'wiggle': 0.55, 'freq': 0.45, 'phase': 0.7, 'water_z': -0.09}


def sand_z(x, y, s=SHORE):
    yy = y + s['wiggle'] * math.sin(x * s['freq'] + s['phase'])
    return -s['slope'] * max(0.0, yy - s['y0'])


def sky_sun(az):
    """The sky's rotation that puts its sun at azimuth `az`, and the engine's sun lamp for it."""
    r0 = C.assets.hdri_sun(SKY, 0.0)['azimuth_deg']
    rot = round((r0 - az) % 360.0, 2)                         # turning the sky by +rot turns its sun by -rot
    return rot, C.sun_from_sky(SKY, rot)


def ext(fn, **k):
    return C.piece('ext', module='ice_b_el', fn=fn, shore=SHORE, **k)


def chunk(x, y, size, seed, kind='clear', sink=0.03, turn=0.0, **k):
    """A chunk of ice bedded `sink` metres into the sand (or the sea floor) where it lies."""
    return ext('ice', position=[x, y, round(sand_z(x, y) - sink, 4)], rotate=[0, 0, turn], size=list(size), seed=seed,
               ice_kind=kind, **k)


ICE = [
    chunk(-0.50, 3.40, (1.15, 0.95, 0.88), 11, 'blue', sink=0.05, turn=20, facets=8, cracks=3),
    chunk(1.95, 4.10, (0.75, 0.62, 0.52), 23, 'clear', sink=0.06, turn=-35, cracks=1),
    chunk(-2.85, 4.00, (0.62, 0.55, 0.42), 31, 'milky', sink=0.05, turn=60, cracks=0),
    chunk(2.00, 2.90, (0.45, 0.38, 0.30), 55, 'clear', sink=0.03, facets=8, cracks=1),
    # stranded on the sand in front: one in the sun's strip, two either side, nearer the lens
    chunk(-1.20, -1.70, (0.48, 0.40, 0.34), 61, 'clear', sink=0.03, turn=35, facets=9, cracks=1),
    chunk(1.30, -0.90, (0.30, 0.25, 0.21), 62, 'blue', sink=0.025, turn=-20, facets=9, cracks=1),
    chunk(2.25, -1.90, (0.36, 0.30, 0.24), 63, 'clear', sink=0.025, turn=70, facets=10, cracks=0),
]


def props():
    return [ext('beach', texture='gravelly_sand', res='4k', displace=0.006, relief=0.06, dark='#0A0A0B', light='#232324',
                tex_scale=1.25, wet_h=0.07, damp_h=0.1, damp_base=0.0, spec=0.05, reach=[-0.7, 0.25],
                grain_m=0.003, glint_share=0.02, bump=1.0, wet_jitter=0.06,
                wet_rough=0.02),
            ext('sea', rough=0.07, chop=0.9, absorb='#1E3533', density=10.0, lace_w=0.3, crests=[[4.0, 0.14, 0.45, 2.0, 1.0, 0.02], [10.5, 0.24, 0.8, 3.2, 0.85, -0.04]],
                ocean={'layers': [{'size': 53.0, 'scale': 0.9, 'seed': 3}, {'size': 131.0, 'scale': 0.7, 'seed': 9}],
                       'shoal_m': 7.0, 'foam_coverage': 0.4}, **{'break': 1.6}),
            *ICE]


def beach_shot(az=SUN_AZ, sun_irr=3.0):
    rot, sun = sky_sun(az)
    sun['irradiance'] = sun_irr
    sk = C.sky(SKY, rotation_deg=rot, strength=1.0, res='4k')
    s = C.shot('ice_b', props(), C.camera(height=0.65, distance=6.5, azimuth=-12.0, lens=65.0, target=(0.0, 0.0, 0.62),
                                          fstop=4.0),
               sk, 'Ice: Diamond Beach at sunrise', sun=sun, rotate_z=10.0, position=(0.0, 0.0, -0.015), exposure=-0.6, look='AgX - Medium High Contrast',
               fin=C.finish(contrast=0.10, clarity=0.04, sharpen=0.25, vignette=0.18),
               haze={'box_m': [-420.0, -12.0, -1.0, 420.0, 420.0, 8.0], 'density': 0.0008, 'anisotropy': 0.6,
                     'color': '#F2C9A8'})
    s['render']['volume_bounces'] = 4
    s['render']['bounces'] = 16
    return s


def beach_portrait():
    s = beach_shot()
    cam = s['camera']
    return C.portrait_of(s, **C.camera(height=cam['position'][2], distance=4.6, azimuth=-12.0, lens=70.0,
                                       target=tuple(cam['target']), fstop=cam['fstop'], shift_y=-0.06))
