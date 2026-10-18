"""Ice, concept B: Jokulsarlon's Diamond Beach at sunrise. The speaker stands on black volcanic sand above the wash,
among chunks of glacier ice the lagoon has given to the sea; the sun, just up over the North Atlantic, comes through
the ice as it comes through the speaker's blue acrylic. Keeps its cool.

The beach, the sea and the ice are studio/engine/kit_ext/ice_b_el.py; the sky is a photographed sunrise over the sea.
"""
import math
import common as C

SKY = 'umhlanga_sunrise'           # a sunrise over open sea, the sun on the horizon (Poly Haven, CC0)
SUN_AZ = 172.5                     # the sun behind the big chunk, left of the speaker (from +y, a little +x)
SHORE = {'y0': 0.5, 'slope': 0.05, 'wiggle': 0.55, 'freq': 0.45, 'phase': 0.7, 'water_z': -0.09}


def sand_z(x, y, s=SHORE):
    yy = y + s['wiggle'] * math.sin(x * s['freq'] + s['phase'])
    return -s['slope'] * max(0.0, yy - s['y0'])


def sky_sun(az, res='1k'):
    """The sky's rotation that puts its sun at azimuth `az`, and that sun as a lamp's settings. Worked out with
    Cycles' own equirectangular convention (u = -atan2(y, x) / 2 pi + 0.5): assets.hdri_sun assumes atan2(y, -x),
    which puts the lamp somewhere other than the sun the camera sees (round 31b, found on this set's first proof)."""
    import numpy as np
    s = C.assets.hdri_sun(SKY, 0.0, res)                       # its colour, elevation and peak are right; its azimuth is not
    img = C.assets.read_hdr(C.assets.hdri(SKY, res))
    H, W, _ = img.shape
    lum = img @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    k = max(1, int(lum.size * 0.0005))
    idx = np.argpartition(lum.ravel(), -k)[-k:]
    w = lum.ravel()[idx]
    rows, cols = np.unravel_index(idx, lum.shape)
    u = (np.average(cols, weights=w) + 0.5) / W
    phi = math.degrees((0.5 - u) * 2 * math.pi)                # the sun's angle from +x in the map
    want = math.degrees(math.atan2(-math.cos(math.radians(az)), math.sin(math.radians(az))))
    rot = (phi - want) % 360.0                                 # the world is the map turned by -rot
    return round(rot, 2), {'azimuth_deg': az, 'elevation_deg': max(0.5, s['elevation_deg']), 'color': s['color'],
                           'angle_deg': 0.53}


def ext(fn, **k):
    return C.piece('ext', module='ice_b_el', fn=fn, shore=SHORE, **k)


def chunk(x, y, size, seed, kind='clear', sink=0.03, turn=0.0, **k):
    """A chunk of ice bedded `sink` metres into the sand (or the sea floor) where it lies."""
    return ext('ice', position=[x, y, round(sand_z(x, y) - sink, 4)], rotate=[0, 0, turn], size=list(size), seed=seed,
               ice_kind=kind, **k)


ICE = [
    chunk(-0.90, 2.60, (1.15, 0.95, 0.88), 11, 'blue', sink=0.05, turn=20, facets=8, cracks=3),
    chunk(1.95, 4.10, (0.75, 0.62, 0.52), 23, 'clear', sink=0.06, turn=-35, cracks=1),
    chunk(-2.85, 4.00, (0.62, 0.55, 0.42), 31, 'milky', sink=0.05, turn=60, cracks=0),
    chunk(0.65, 1.30, (0.22, 0.18, 0.14), 53, 'clear', sink=0.015, subdiv=4, cracks=0),
    chunk(-2.20, 1.05, (0.28, 0.22, 0.17), 54, 'blue', sink=0.02, subdiv=4, cracks=0),
    chunk(2.00, 2.90, (0.45, 0.38, 0.30), 55, 'clear', sink=0.03, facets=8, cracks=1),
    chunk(0.35, 3.70, (0.30, 0.26, 0.20), 56, 'clear', sink=0.04, subdiv=4, cracks=0),
]


def props():
    return [ext('beach', texture='gravelly_sand', res='4k', displace=0.006, relief=0.04, dark='#0D0D0E', light='#2E2D2C',
                tex_scale=1.25, wet_h=0.07, damp_h=0.1, damp_base=0.0, spec=0.05, bump=1.0, wet_jitter=0.06,
                wet_rough=0.04),
            ext('sea', rough=0.07, chop=0.9, absorb='#2F4A48', density=6.0, lace_w=0.15, crests=[[4.5, 0.16, 0.45, 2.0, 1.0], [11.0, 0.28, 0.8, 3.6, 0.9], [24.0, 0.35, 1.2, 5.5, 0.6],
                         [45.0, 0.35, 2.0, 8.0, 0.35]]),
            *ICE]


def shot(az=SUN_AZ, sun_irr=3.0):
    rot, sun = sky_sun(az)
    sun['irradiance'] = sun_irr
    sk = C.sky(SKY, rotation_deg=rot, strength=1.0, res='4k')
    s = C.shot('ice_b', props(), C.camera(height=0.70, distance=5.2, azimuth=-12.0, lens=50.0, target=(0.0, 0.0, 0.62),
                                          fstop=5.6),
               sk, 'Ice: Diamond Beach at sunrise', sun=sun, rotate_z=10.0, position=(0.0, 0.0, -0.008), exposure=-0.3,
               fin=C.finish(contrast=0.04, clarity=0.04, sharpen=0.25, vignette=0.10),
               haze={'box_m': [-420.0, -12.0, -1.0, 420.0, 420.0, 8.0], 'density': 0.002, 'anisotropy': 0.6,
                     'color': '#F2C9A8'})
    s['render']['volume_bounces'] = 4
    s['render']['bounces'] = 16
    return s


def portrait():
    return C.portrait_of(shot(), position=C.camera(height=0.70, distance=6.0, azimuth=-12.0)['position'], lens_mm=50.0)
