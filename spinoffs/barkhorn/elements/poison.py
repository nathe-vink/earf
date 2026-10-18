"""Poison, concept A: a redwood rainforest on location (round 31b; poison.md has the concept and the passes).

The floor of a coast redwood forest on a misty morning, in the spirit of Prairie Creek: redwood trunks metres across
rising out of the frame, sword ferns in layers, a fallen log with moss over it and two fly agarics on it, the light
coming down in shafts through the mist. The bottle green speaker stands among the ferns, turned toward the light.
Photographed assets throughout (Poly Haven, CC0): the misty_pines sky, metasequoia (dawn redwood) bark on the trunks,
forest_leaves_02 on the ground, fern_02's ferns, moss_01's moss and dead_tree_trunk for the log.
"""
import math, random

from common import area, asset, camera, finish, ground, piece, portrait_of, shot as frame, sky, sun_from_sky

SKY = 'misty_pines'
SKY2, SKY_ROT = 'mossy_forest', 180.0
BANK = (0.5, 9.0, -0.9, 14.0, 4.0, 2.2)            # a mossy bank behind (x, y, z, half-width, half-depth, half-height)


def bank_z(x, y):
    """The bank's surface height at (x, y), or None off it."""
    bx, by, bz, a, b, c = BANK
    q = 1 - ((x - bx) / a) ** 2 - ((y - by) / b) ** 2
    return bz + c * math.sqrt(q) if q > 0 else None
# redwoods further back, fading into the mist: layers of trunks so the forest reads deep
FAR = [(-9.0, 15.0, 1.4), (-5.5, 20.0, 1.7), (4.5, 16.0, 1.3), (8.5, 18.5, 1.6), (12.0, 13.0, 1.2), (-13.5, 21.0, 1.5),
       (-1.0, 26.0, 1.8), (6.0, 27.0, 1.5), (-7.5, 30.0, 1.6), (13.0, 26.0, 1.7), (-14.0, 11.0, 1.3)]
REDWOOD = '#8A4126'                # the bark's cinnamon red, which the dawn redwood's scan lacks
SUN = {'azimuth_deg': -68.0, 'elevation_deg': 30.0, 'irradiance': 22.0, 'angle_deg': 0.6, 'color': '#FFE6B8'}
CANOPY_Z = 16.0
SUNLIT2 = [(0.0, 0.0, 0.8, 1.1), (-0.5, 6.0, 1.5, 1.2), (3.0, 7.0, 1.5, 1.0), (-4.0, 8.0, 2.0, 1.0)]
SUNLIT = [(0.0, 0.0, 0.85, 0.75), (-1.0, 3.4, 0.0, 0.9), (2.0, 4.6, 0.0, 1.0)]   # where the sun gets through [x, y, z, r]


def gap_for(x, y, z, r, centre):
    """The canopy hole (in the canopy's own plane) through which the sun lands on (x, y): back along the sun."""
    az, el = math.radians(SUN['azimuth_deg']), math.radians(SUN['elevation_deg'])
    d = (CANOPY_Z - z) / math.tan(el)
    gx, gy = x + d * math.sin(az), y - d * math.cos(az)
    return [round(gx - centre[0], 3), round(gy - centre[1], 3), r]
LOG_A, LOG_B = (-4.6, 2.6, 0.3), (-0.75, 1.7, 0.26)
LOG2_A, LOG2_B = (-3.2, 1.9, 0.22), (3.4, 2.3, 0.2)    # A2: the log across behind, its ends behind the trunk and the ferns     # the fallen log's axis: its foot (left) to its broken end


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
    zones = [((-2.6, -1.9, -1.0, -0.6), 4, (1.0, 1.3)), ((1.0, -2.0, 2.8, -0.6), 6, (1.0, 1.3)),     # the corners
             ((-2.8, -0.6, -0.75, 1.3), 7, (1.0, 1.35)), ((0.75, -0.6, 3.0, 1.2), 7, (1.0, 1.35)),   # beside it
             ((-1.4, 0.5, 1.8, 1.6), 10, (1.1, 1.5)),                                                 # just behind
             ((-4.0, 1.2, 4.2, 5.5), 45, (1.1, 1.7)), ((-7.0, 5.5, 7.0, 11.0), 45, (1.3, 1.9))]                                               # the middle distance
    for (x0, y0, x1, y1), n, (s0, s1) in zones:
        k = 0
        while k < n:
            x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
            if x * x + y * y < 0.75 ** 2 or _seg_dist(x, y, LOG2_A, LOG2_B) < 0.5 or math.hypot(x - 1.55, y + 0.55) < 0.25:
                continue
            pl.append([round(x, 3), round(y, 3), 0.0, round(rnd.uniform(s0, s1), 3), round(rnd.uniform(0, 360), 1),
                       rnd.choice([0, 1, 2, 3]), round(rnd.uniform(-12, 12), 1)])
            k += 1
    pl.append([2.0, -2.6, 0.0, 1.2, 200, 2])            # a frond close to the lens at the right edge, in the blur
    return [ext('plants', model='fern_02', place=pl, seed=seed)]


def shot_misty():
    """Concept A1 (passes 1-3: 5.5, 5.5, 4.5): a deep misty redwood grove of modelled trunks. Superseded."""
    props = [ground('forest_leaves_02', size=(16.0, 18.0), position=(0.0, 5.0, 0.0), displace=0.03, tint='#3A2A1E', tint_mix=0.15, relief=0.12,
                    res='4k', cells=640),
             # the redwoods, metres across, rising out of the frame
             ext('redwood', (-4.3, 3.0, -0.1), radius=1.35, height=30.0, tint=REDWOOD, tint_mix=0.15, tex_scale=0.8, bump=2.4, seed=1, flare=0.7, foot=1.6, turn=20),
             ext('redwood', (5.0, 7.4, -0.1), radius=1.7, height=30.0, tint=REDWOOD, tint_mix=0.15, tex_scale=0.8, bump=2.4, seed=2, flare=0.6, foot=1.8, turn=140),
             ext('redwood', (-4.8, 12.0, -0.1), radius=1.6, height=30.0, tint=REDWOOD, tint_mix=0.15, tex_scale=0.8, bump=2.4, seed=3, turn=60),
             ext('redwood', (-7.6, 8.4, -0.1), radius=1.4, height=30.0, tint=REDWOOD, tint_mix=0.15, tex_scale=0.8, bump=2.4, seed=4, turn=200),
             *[ext('redwood', (x, y, -0.1), radius=r, height=40.0, tint=REDWOOD, tint_mix=0.15, tex_scale=0.8, bump=2.4,
                   seed=10 + k, turn=k * 47) for k, (x, y, r) in enumerate(FAR)],
             ext('redwood', (5.8, 13.0, -0.1), radius=1.5, height=30.0, tint=REDWOOD, tint_mix=0.15, tex_scale=0.8, bump=2.4, seed=5, turn=300),
             # the fallen redwood, furred in moss, two fly agarics on its back
             ext('mossy_log', a=list(LOG_A), b=list(LOG_B), radius=0.42, radius_b=0.36, cover=0.4, res='2k', end_tint='#3A2A20', end_tint_mix=0.7),
             ext('strew', model='moss_01', on=['-moss'], density=2500, up=0.35, scale=[0.9, 2.2], patch=0.3,
                 patch_cut=0.25, seed=3),
             # two fly agarics at the speaker's right, back among the ferns: a mature one and a button
             ext('toadstool', (0.95, -1.05, -0.008), height=0.2, cap=[0.11, 0.045], stem=0.02, lean=[0.012, 0.0], seed=3),
             ext('toadstool', (1.12, -0.95, -0.008), height=0.09, cap=[0.045, 0.04], stem=0.013, lean=[0.0, 0.0], seed=4),
             # the forest's air: mist thick low and thinning upward, torn into wisps, and the canopy that breaks the
             # sun into shafts
             ext('mist', (0.0, 21.0, -0.2), size=[50.0, 41.0, 16.0], density=0.06, top=0.3, wisp=2.5, color='#F4F6EE',
                 anisotropy=0.3),
             ext('canopy', (0.0, 4.0, CANOPY_Z), size=[70.0, 70.0], gap=2.5, open=0.35,
                 holes=[gap_for(x, y, z, r, (0.0, 4.0)) for x, y, z, r in SUNLIT])]
    props += ferns()
    sun = SUN
    # a soft bounce from the camera's side, as a photographer's reflector would give, to open the speaker's face
    lights = {'bounce': area(-20, 5, 3.0, 0.5, '#E6EEDC', (1.0, 1.0), (0.0, 0.0, 0.6)),
              # a big soft reflector at the camera's right, so the horn's mouth mirrors a graded panel, not the dark
              'reflector': area(35, 12, 3.0, 1.2, '#EEF0E0', (2.0, 1.5), (0.0, 0.0, 1.05))}
    cam = camera(height=0.85, distance=6.2, azimuth=10.0, lens=65.0, target=(0.0, 0.0, 0.62), fstop=2.8)
    return frame('poison', props, cam, sky(SKY, rotation_deg=0.0, strength=0.5, res='4k'),
                 'barkhorn, Poison, in a redwood rainforest', lights=lights, sun=sun, rotate_z=-20.0,
                 position=(0.0, 0.0, -0.015), fin=finish(contrast=0.10, clarity=0.08, vignette=0.22, saturation=0.08),
                 white_balance=(5300, 10))


def shot():
    """Concept A2: the forest itself photographed (Poly Haven's mossy_forest, a lush mossy rainforest, out of focus
    behind), a modelled foreground in front of it: a redwood's buttress at the left, the mossy log, sword ferns, the
    duff, two fly agarics; the sky's own sun, dappled."""
    props = [ground('forest_leaves_02', size=(30.0, 30.0), position=(0.0, 8.0, 0.0), displace=0.03, tint='#3A2A1E',
                    tint_mix=0.15, relief=0.15, res='4k', cells=900),
             ext('redwood', (-2.9, 2.6, -0.1), radius=1.25, height=30.0, tint=REDWOOD, tint_mix=0.3, tex_scale=0.6,
                 bump=1.6, displace=0.035, segments=420, rings=220, seed=1, flare=0.75, foot=1.5, turn=20),
             ext('mossy_log', a=list(LOG2_A), b=list(LOG2_B), radius=0.42, radius_b=0.36, cover=0.55, res='2k',
                 end='acg:TreeEnd003', end_tint='#3A2A20', end_tint_mix=0.7),
             ext('strew', model='moss_01', on=['-moss'], density=3500, up=0.2, scale=[0.9, 2.2], patch=0.3,
                 patch_cut=0.2, seed=3),
             # one fly agaric, small, at the fern edge to the right: the quiet accent
             ext('toadstool', (1.55, -0.55, -0.008), height=0.14, cap=[0.07, 0.035], stem=0.014, lean=[0.012, 0.0], seed=3),
             # the light: one gap in the canopy over the speaker, a few over the bank behind; light mist from 3 m back
             ext('canopy', (0.0, 4.0, CANOPY_Z), size=[70.0, 70.0], gap=2.0, open=0.04,
                 holes=[gap_for(x, y, z, r, (0.0, 4.0)) for x, y, z, r in SUNLIT2]),
             ext('mist', (0.0, 22.0, -0.2), size=[50.0, 38.0, 16.0], density=0.025, top=0.4, wisp=2.5, color='#F2F4EA',
                 anisotropy=0.4)]
    props += ferns()
    # the bank behind: a mound of the same duff, ferns over its face, so the ground rises into the photographed forest
    bx, by, bz, ba, bb, bc = BANK
    nb = len(props)
    props.append(piece('sphere', material='pbr', texture='acg:Moss001', tex_scale=0.12, res='2k', position=[bx, by, bz],
                       scale=[ba, bb, bc], segments=160))
    props.append(ext('strew', model='moss_01', on=[f'prop{nb}-kit'], density=1500, up=0.3, scale=[1.5, 3.0], patch=0.8,
                     patch_cut=0.3, seed=21))
    rnd = random.Random(17); pl = []
    while len(pl) < 170:
        x, y = rnd.uniform(-9, 10), rnd.uniform(5.2, 9.5)
        z = bank_z(x, y)
        if z is None or z < 0.0:
            continue
        pl.append([round(x, 3), round(y, 3), round(z - 0.03, 3), round(rnd.uniform(1.3, 2.0), 3), round(rnd.uniform(0, 360), 1),
                   rnd.choice([0, 1, 2, 3]), round(rnd.uniform(-15, 15), 1)])
    props.append(ext('plants', model='fern_02', place=pl, seed=17))
    rot = SKY_ROT
    lights = {'reflector': area(35, 12, 3.0, 1.2, '#EEF0E0', (2.0, 1.5), (0.0, 0.0, 1.05)),
              'card': area(60, 45, 2.5, 1.2, '#F0F2E6', (1.0, 1.0), (0.0, 0.0, 1.1))}
    cam = camera(height=0.8, distance=6.4, azimuth=18.0, lens=75.0, target=(0.0, 0.0, 0.64), fstop=2.8)
    return frame('poison', props, cam, sky(SKY2, rotation_deg=rot, strength=0.45, res='4k'),
                 'barkhorn, Poison, in a redwood rainforest', lights=lights,
                 sun=SUN, rotate_z=-20.0,
                 position=(0.0, 0.0, -0.022), fin=finish(contrast=0.08, clarity=0.06, vignette=0.2))


def portrait():
    return portrait_of(shot(), **camera(height=0.95, distance=5.4, azimuth=-14.0, lens=45.0, target=(0.0, 0.0, 0.85),
                                        fstop=4.0))
