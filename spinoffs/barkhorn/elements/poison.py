"""Poison, concept A: a redwood rainforest on location (round 31b; poison.md has the concept and the passes).

The floor of a coast redwood forest on a misty morning, in the spirit of Prairie Creek: redwood trunks metres across
rising out of the frame, sword ferns in layers, a fallen log with moss over it and two fly agarics on it, the light
coming down in shafts through the mist. The bottle green speaker stands among the ferns, turned toward the light.
Photographed assets throughout (Poly Haven, CC0): the misty_pines sky, metasequoia (dawn redwood) bark on the trunks,
forest_leaves_02 on the ground, fern_02's ferns, moss_01's moss and dead_tree_trunk for the log.
"""
import math, random

from common import area, asset, camera, finish, ground, piece, portrait_of, shot as frame, sky

SKY = 'misty_pines'
SUN = {'azimuth_deg': -125.0, 'elevation_deg': 40.0, 'irradiance': 10.0, 'angle_deg': 0.6, 'color': '#FFE6B8'}
CANOPY_Z = 16.0
SUNLIT = [(0.0, 0.1, 1.2), (-1.4, 2.6, 0.9), (2.2, 4.2, 1.0)]   # where gaps in the canopy let the sun through [x, y, r]


def gap_for(x, y, r, centre):
    """The canopy hole (in the canopy's own plane) through which the sun lands on (x, y): back along the sun."""
    az, el = math.radians(SUN['azimuth_deg']), math.radians(SUN['elevation_deg'])
    d = CANOPY_Z / math.tan(el)
    gx, gy = x + d * math.sin(az), y - d * math.cos(az)
    return [round(gx - centre[0], 3), round(gy - centre[1], 3), r]
LOG_A, LOG_B = (-3.6, 0.0, 0.3), (-0.75, 2.4, 0.26)     # the fallen log's axis: its foot (left) to its broken end


def ext(fn, position=(0, 0, 0), **k):
    return piece('ext', module='poison_el', fn=fn, position=list(position), **k)


def on_log(t, v=0.0):
    """A point on the log's back, `t` of the way from its foot to its end, `v` metres across it."""
    x = LOG_A[0] + (LOG_B[0] - LOG_A[0]) * t; y = LOG_A[1] + (LOG_B[1] - LOG_A[1]) * t
    z = LOG_A[2] + (LOG_B[2] - LOG_A[2]) * t
    r = 0.42 + (0.36 - 0.42) * t
    return (round(x, 4), round(y + v, 4), round(z + r - 0.01, 4))


def _seg_dist(x, y, a, b):
    """Distance in plan from (x, y) to the segment a-b."""
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    t = max(0.0, min(1.0, ((x - ax) * (bx - ax) + (y - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2)))
    return math.hypot(x - ax - t * (bx - ax), y - ay - t * (by - ay))


def ferns(seed=3):
    """Sword ferns (fern_02's four, near their scanned size: about a metre across): dense in the foreground's corners,
    a middle layer behind the speaker, clumps toward the trunks; kept off the speaker's footprint and the camera's
    line to it."""
    rnd = random.Random(seed); pl = []
    zones = [((-2.6, -1.9, -1.0, -0.6), 6, (1.2, 1.5)), ((1.0, -2.0, 2.8, -0.6), 6, (1.2, 1.5)),     # the corners
             ((-2.8, -0.6, -0.75, 1.3), 7, (1.0, 1.35)), ((0.75, -0.6, 3.0, 1.2), 7, (1.0, 1.35)),   # beside it
             ((-1.2, 0.5, 1.4, 1.2), 5, (1.0, 1.3)),                                                 # just behind
             ((-3.6, 1.2, 3.8, 5.5), 22, (1.1, 1.5))]                                               # the middle distance
    for (x0, y0, x1, y1), n, (s0, s1) in zones:
        k = 0
        while k < n:
            x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
            if x * x + y * y < 0.75 ** 2 or _seg_dist(x, y, LOG_A, LOG_B) < 0.55 or math.hypot(x - 0.62, y + 0.5) < 0.4:
                continue
            pl.append([round(x, 3), round(y, 3), 0.0, round(rnd.uniform(s0, s1), 3), round(rnd.uniform(0, 360), 1),
                       rnd.choice([1, 2])])
            k += 1
    return [ext('plants', model='fern_02', place=pl, seed=seed)]


def shot():
    props = [ground('forest_leaves_02', size=(16.0, 18.0), position=(0.0, 5.0, 0.0), displace=0.02, relief=0.12,
                    res='4k', cells=640),
             # the redwoods, metres across, rising out of the frame
             ext('redwood', (-2.4, 4.4, -0.1), radius=1.35, height=30.0, seed=1, flare=0.7, foot=1.6, turn=20),
             ext('redwood', (2.9, 6.2, -0.1), radius=1.7, height=30.0, seed=2, flare=0.6, foot=1.8, turn=140),
             ext('redwood', (-0.2, 12.0, -0.1), radius=1.6, height=30.0, seed=3, turn=60),
             ext('redwood', (-5.6, 9.0, -0.1), radius=1.4, height=30.0, seed=4, turn=200),
             ext('redwood', (5.8, 13.0, -0.1), radius=1.5, height=30.0, seed=5, turn=300),
             # the fallen redwood, furred in moss, two fly agarics on its back
             ext('mossy_log', a=list(LOG_A), b=list(LOG_B), radius=0.42, radius_b=0.36, cover=0.5, res='2k'),
             ext('strew', model='moss_01', on=['-moss'], density=6000, up=0.35, scale=[0.8, 1.7], patch=0.3,
                 patch_cut=0.2, seed=3),
             ext('toadstool', on_log(0.78), height=0.15, cap=[0.06, 0.038], stem=0.01, lean=[0.01, 0.0], seed=1),
             ext('toadstool', on_log(0.82, 0.08), height=0.09, cap=[0.036, 0.024], stem=0.0065, lean=[0.008, 0.0], seed=2),
             # and a family on the floor at the speaker's right front, in the light
             ext('toadstool', (0.6, -0.48, -0.005), height=0.22, cap=[0.085, 0.05], stem=0.014, lean=[-0.015, 0.0], seed=3),
             ext('toadstool', (0.74, -0.4, -0.005), height=0.13, cap=[0.05, 0.034], stem=0.009, lean=[0.01, -0.005], seed=4),
             ext('toadstool', (0.52, -0.62, -0.005), height=0.08, cap=[0.032, 0.026], stem=0.007, lean=[0.0, 0.0], seed=5),
             # the forest's air: mist thick low and thinning upward, torn into wisps, and the canopy that breaks the
             # sun into shafts
             ext('mist', (0.0, 9.5, -0.2), size=[30.0, 18.0, 14.0], density=0.15, top=0.25, wisp=3.0, color='#F4F6EE',
                 anisotropy=0.6),
             ext('canopy', (0.0, 4.0, CANOPY_Z), size=[70.0, 70.0], gap=2.5, open=0.22,
                 holes=[gap_for(x, y, r, (0.0, 4.0)) for x, y, r in SUNLIT])]
    props += ferns()
    sun = SUN
    # a soft bounce from the camera's side, as a photographer's reflector would give, to open the speaker's face
    lights = {'bounce': area(-20, 5, 3.0, 0.5, '#E6EEDC', (1.0, 1.0), (0.0, 0.0, 0.6))}
    cam = camera(height=0.95, distance=4.6, azimuth=-14.0, lens=45.0, target=(0.0, 0.0, 0.62), fstop=4.0)
    return frame('poison', props, cam, sky(SKY, rotation_deg=0.0, strength=0.45, res='4k'),
                 'barkhorn, Poison, in a redwood rainforest', lights=lights, sun=sun, rotate_z=18.0,
                 position=(0.0, 0.0, -0.008), fin=finish(contrast=0.06, clarity=0.05, vignette=0.15))


def portrait():
    return portrait_of(shot(), **camera(height=0.95, distance=5.4, azimuth=-14.0, lens=45.0, target=(0.0, 0.0, 0.85),
                                        fstop=4.0))
