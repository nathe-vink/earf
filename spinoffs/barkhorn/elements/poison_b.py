"""Poison, concept B: the poisonous forest (round 31b; poison_b.md has the concept and the passes).

The owner on concept A (2026-10-18, evening): "Poison isn't reading as poisonous. Needs shrooms around it, or a snake,
or both. Or other poisonous things." So the same redwood rainforest on a damp, misty morning, now with the poisons
themselves at the speaker's feet, modelled to scale (studio/engine/kit_ext/poison_b_el.py): fly agarics at every age,
from the button to the flat torn cap, and olive death caps in the moss and the duff; a green pit viper coiled on the
mossy log beside the speaker, its head raised; a green-and-black dart frog on the moss; foxglove spires and a sprig of
nightshade. Low sun comes through the canopy into a little mist; the bottle green acrylic glows where it falls.
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
SUN_A2 = {'azimuth_deg': -100.0, 'elevation_deg': 42.0, 'irradiance': 32.0, 'angle_deg': 0.6, 'color': '#FFE6B8'}
SUNLIT2 = [(0.0, 0.0, 0.8, 1.1), (1.5, 6.0, 4.0, 0.7), (4.0, 10.0, 5.0, 0.8), (6.5, 14.0, 5.0, 0.7), (2.5, 6.5, 0.8, 0.6),
           (-1.85, 1.6, 2.5, 0.4)]
BACK = [(4.5, 11.0, 1.2), (8.0, 15.0, 1.5), (-4.5, 17.0, 1.4), (4.0, 24.0, 1.6), (10.0, 20.0, 1.3), (-7.0, 26.0, 1.5),
        (1.0, 34.0, 1.6)]
SUNLIT = [(0.0, 0.0, 0.85, 0.75), (-1.0, 3.4, 0.0, 0.9), (2.0, 4.6, 0.0, 1.0)]   # where the sun gets through [x, y, z, r]


def gap_for(x, y, z, r, centre, sun=None):
    """The canopy hole (in the canopy's own plane) through which the sun lands on (x, y): back along the sun."""
    sun = sun or SUN
    az, el = math.radians(sun['azimuth_deg']), math.radians(sun['elevation_deg'])
    d = (CANOPY_Z - z) / math.tan(el)
    gx, gy = x + d * math.sin(az), y - d * math.cos(az)
    return [round(gx - centre[0], 3), round(gy - centre[1], 3), r]
LOG_A, LOG_B = (-4.6, 2.6, 0.3), (-0.75, 1.7, 0.26)
LOG2_A, LOG2_B = (-1.2, 1.55, 0.22), (4.6, 5.4, 0.2)    # A2: the log across behind, its ends behind the trunk and the ferns     # the fallen log's axis: its foot (left) to its broken end


def extb(fn, position=(0, 0, 0), **k):
    return piece('ext', module='poison_b_el', fn=fn, position=list(position), **k)


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
            if x * x + y * y < 0.75 ** 2 or _seg_dist(x, y, LOG2_A, LOG2_B) < 0.5 or math.hypot(x - 0.7, y + 1.4) < 0.4:
                continue
            pl.append([round(x, 3), round(y, 3), 0.0, round(rnd.uniform(s0, s1), 3), round(rnd.uniform(0, 360), 1),
                       rnd.choice([0, 1, 2, 3]), round(rnd.uniform(-12, 12), 1)])
            k += 1
    pl.append([2.0, -2.6, 0.0, 1.2, 200, 2])
    pl.append([-1.3, 1.25, 0.0, 1.5, 40, 1])             # over the log's near end            # a frond close to the lens at the right edge, in the blur
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


LOGB = ((-0.75, 1.1, 0.24), (-2.9, -0.9, 0.24), 0.27, 0.3)
ROCK = (-0.5, -2.05, 0.55)         # the mossy stump in the foreground: x, y, scale of the scan (0.84 x 0.77 x 0.29 m)   # the fallen log: its far end, its near end, radii


def on_logb(t, v=0.0):
    """A point on the B log's top, `t` of the way from its far end to its near end, `v` metres across it."""
    (ax, ay, az), (bx, by, bz), r0, r1 = LOGB
    x, y, z = ax + (bx - ax) * t, ay + (by - ay) * t, az + (bz - az) * t
    dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy)
    return (round(x - dy / L * v, 4), round(y + dx / L * v, 4), round(z + r0 + (r1 - r0) * t - 0.01, 4))


def poisons():
    """The poisons at the speaker's feet: fly agarics at every age in a drift from its front left round to its right,
    death caps behind them at the right, the viper on the log, the frog, foxgloves, nightshade."""
    P = []
    # fly agarics in clusters: (x, y, cap radius, age, seed, lean, torn)
    rnd = random.Random(41)
    AG = [  # at the speaker's front left
          (-0.42, -0.45, 0.085, 'convex', 1, (0.01, -0.01), 0.0), (-0.3, -0.56, 0.05, 'young', 2, (0.0, -0.01), 0.0),
          (-0.52, -0.6, 0.03, 'button', 3, (0, 0), 0.0), (-0.62, -0.38, 0.1, 'plane', 5, (-0.015, 0.0), 0.15),
          # at its right
          (0.42, -0.5, 0.07, 'convex', 6, (0.01, -0.005), 0.0), (0.56, -0.38, 0.105, 'old', 7, (0.02, 0.01), 0.55),
          (0.34, -0.66, 0.028, 'button', 8, (0, 0), 0.0),
          # the hero cluster near the lens at the right, big in the frame
          (0.62, -2.05, 0.095, 'convex', 21, (-0.012, -0.01), 0.0), (0.76, -1.95, 0.065, 'young', 22, (0.01, 0.005), 0.0),
          (0.52, -2.2, 0.035, 'button', 23, (0, 0), 0.0), (0.88, -2.15, 0.12, 'plane', 24, (0.02, -0.01), 0.25),
          (0.7, -2.28, 0.045, 'young', 25, (-0.008, -0.012), 0.0), (0.98, -1.85, 0.03, 'button', 26, (0, 0), 0.0),
          (1.1, -2.05, 0.08, 'convex', 27, (0.015, 0.0), 0.0)]
    for x, y, R, age, sd, lean, torn in AG:
        P.append(extb('amanita', (x, y, -0.006), cap=R, age=age, seed=sd, lean=list(lean), torn=torn))
    # death caps, olive, half in the ferns at the right behind the speaker's cluster
    for x, y, R, age, sd in [(0.82, -0.28, 0.055, 'convex', 11), (0.95, -0.45, 0.04, 'young', 12), (0.78, -0.08, 0.065, 'plane', 13),
                              (1.3, -1.75, 0.05, 'convex', 14)]:
        P.append(extb('amanita', (x, y, -0.006), cap=R, age=age, seed=sd, species='phalloides'))
    # a mossy stump (a Poly Haven scan) in the foreground at the left, the viper coiled on its top, its head raised
    # toward the speaker; the frog on the moss at the stump's foot
    rx, ry, rs = ROCK
    P.append(asset('tree_stump_02', (rx, ry, -0.03), rotate=(0, 0, 35), scale=rs, res='2k'))
    P.append(extb('viper', (rx + 0.02, ry + 0.02, 0.3), drop=True, rotate=[0, 0, 20], head=[0.07, -0.1, 0.15], look=-35,
                  girth=0.024, r_out=0.13, r_in=0.05, turns=2.1))
    P.append(extb('dartfrog', (0.3, -2.45, -0.004), rotate=[0, 0, 200], size=0.042))
    # foxglove spires behind at the left, nightshade at the right
    P += [extb('foxglove', (-1.2, 0.5, -0.01), height=1.35, lean=[0.05, 0.0], side=-100, seed=1, bells=24),
          extb('foxglove', (-1.95, 1.4, -0.01), height=1.05, lean=[-0.04, 0.02], side=-90, seed=2, bells=20),
          extb('foxglove', (1.35, 1.25, -0.01), height=1.15, lean=[0.03, 0.0], side=-110, seed=3, bells=22),
          extb('nightshade', (1.0, -0.55, -0.01), height=0.42, lean=[-0.06, -0.03], seed=5, berries=6)]
    return P


def ferns_b(seed=3):
    """Sword ferns round the clearing, kept off the speaker, the log, the mushrooms and the camera's line."""
    rnd = random.Random(seed); pl = []
    zones = [((-3.0, -1.8, -1.0, -0.9), 4, (1.0, 1.3)), ((1.2, -1.9, 3.0, -0.8), 5, (1.0, 1.3)),
             ((-3.2, -0.8, -1.2, 1.6), 6, (1.0, 1.4)), ((1.1, -0.6, 3.2, 1.6), 8, (1.0, 1.4)),
             ((-1.2, 0.7, 1.6, 2.0), 7, (1.1, 1.5)), ((-4.0, 1.6, 4.2, 5.5), 45, (1.1, 1.7)),
             ((-7.0, 5.5, 7.0, 11.0), 45, (1.3, 1.9))]
    for (x0, y0, x1, y1), n, (s0, s1) in zones:
        k = 0
        while k < n:
            x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
            if x * x + y * y < 0.8 ** 2 or (-0.9 < x < 1.1 and -0.8 < y < 0.0) or math.hypot(x - 0.8, y + 2.05) < 0.5 or math.hypot(x - ROCK[0], y - ROCK[1]) < 0.55:
                continue
            pl.append([round(x, 3), round(y, 3), 0.0, round(rnd.uniform(s0, s1), 3), round(rnd.uniform(0, 360), 1),
                       rnd.choice([0, 1, 2, 3]), round(rnd.uniform(-12, 12), 1)])
            k += 1
    return [ext('plants', model='fern_02', place=pl, seed=seed)]


SUN_B = {'azimuth_deg': -105.0, 'elevation_deg': 32.0, 'irradiance': 30.0, 'angle_deg': 0.6, 'color': '#FFE2AE'}
SUNLIT_B = [(0.0, 0.0, 0.7, 1.0), (-0.1, -0.55, 0.05, 0.75), (0.8, -2.05, 0.12, 0.5), (-0.5, -2.05, 0.35, 0.45), (-2.0, 7.0, 4.0, 0.6),
            (-3.5, 10.0, 5.0, 0.6), (1.0, 12.0, 5.0, 0.55), (2.5, 6.5, 0.8, 0.5)]


def shot():
    props = [ground('forest_leaves_02', size=(30.0, 30.0), position=(0.0, 8.0, 0.0), displace=0.03, tint='#3A2A1E',
                    tint_mix=0.15, relief=0.15, res='4k', cells=900),
             ext('redwood', (-3.4, 3.6, -0.1), radius=1.25, height=30.0, tint=REDWOOD, tint_mix=0.3, tex_scale=1.4,
                 bump=1.6, displace=0.12, segments=420, rings=220, seed=1, flare=0.75, foot=1.5, turn=20),
             # the floor in 3D near the speaker: bark crumbs, twigs and moss in irregular cushions
             ext('strew', model='bark_debris_01', on=['prop0-kit'], density=2.0, up=0.5, scale=[0.22, 0.4], seed=31,
                 within=[0.0, -0.3, 3.2], avoid=[[0.0, 0.0, 0.33], [0.0, -0.55, 0.5]]),
             ext('darken', on=['prop0-kit'], value=0.68, rough=0.85),
             ext('canopy', (0.0, 4.0, CANOPY_Z), size=[220.0, 220.0], gap=1.2, open=0.05,
                 holes=[gap_for(x, y, z, r, (0.0, 4.0), SUN_B) for x, y, z, r in SUNLIT_B]),
             ext('mist', (0.0, 21.0, -0.2), size=[50.0, 37.0, 18.0], density=0.07, top=0.5, wisp=2.5, color='#F2F4EA',
                 anisotropy=0.65),
             *[ext('redwood', (x, y, -0.1), radius=r, height=40.0, tint=REDWOOD, tint_mix=0.3, tex_scale=1.4, bump=1.6,
                   seed=30 + k, turn=k * 61) for k, (x, y, r) in enumerate(BACK)]]
    props += ferns_b()
    props += poisons()
    bx, by, bz, ba, bb, bc = BANK
    nb = len(props)
    props.append(piece('sphere', material='pbr', texture='acg:Moss001', tex_scale=0.12, res='2k', position=[bx, by, bz],
                       scale=[ba, bb, bc], segments=160, tint='#4E6B2A', tint_mix=0.4, rough_mul=1.3))
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
    # bounces a photographer would set: a reflector low at the camera's left (diffuse only), a dim scrim the horn
    # mirrors, a warm strip behind-right for the body's right edge
    lights = {'reflector': {**area(-35, 8, 2.5, 3.5, '#EEF0E0', (2.0, 1.2), (0.0, -0.3, 0.5)), 'specular': 0.0},
              'scrim': {**area(-10, 30, 3.5, 0.5, '#D8DCC8', (4.0, 2.5), (0.0, 0.0, 1.15)), 'diffuse': 0.0},
              'rim': {**area(140, 10, 2.0, 1.5, '#FFE6B8', (0.6, 1.4), (0.0, 0.0, 1.0)), 'specular': 0.4}}
    cam = camera(height=0.42, distance=3.9, azimuth=4.0, lens=35.0, target=(0.0, -0.3, 0.62), focus=(0.0, -0.45, 0.5),
                 fstop=8.0)
    return frame('poison', props, cam, sky(SKY2, rotation_deg=SKY_ROT, strength=0.3, res='4k'),
                 'barkhorn, Poison B, the poisonous forest', lights=lights, sun=SUN_B, rotate_z=-18.0,
                 position=(0.0, 0.0, -0.022), fin=finish(contrast=0.08, clarity=0.06, vignette=0.2))


def portrait():
    return portrait_of(shot(), **camera(height=0.55, distance=4.6, azimuth=8.0, lens=60.0, target=(-0.1, -0.1, 0.62),
                                        focus=(0.0, -0.45, 0.4), fstop=5.6, shift_y=0.08))
