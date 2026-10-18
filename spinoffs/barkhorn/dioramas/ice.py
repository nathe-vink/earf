"""Ice: a frozen grotto, in glass and wool (round 31; ice.md has the concept and the rounds).

The speaker stands on a frosted glass lake lit from beneath, in a grotto of cast-glass shards and chunky wool snow. A
ledge of frosted glass crosses the back with glass icicles hanging from it in the icon's rhythm (three from a bar, the
middle longest); cotton-wool drifts bank the lake, paper snowflakes hang on threads, fine snow drifts in the air. One
light idea: the cold blue glow from under the ice, with a silver rim from behind. The joke: a skater's figure of eight
scratched into the lake, ending at the speaker's feet (it keeps its cool).
"""
import math, random

from common import bank, finish, kit, mound, portrait_of, shot as frame, tilt_shift, area, point

ICE = '#BFE3F5'        # ice, lit
DEEP = '#0B1E36'       # the grotto's shadow
SNOW = '#F4F8FB'
WOOL = '#DCE8F1'
PRODUCT = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'rib-*', 'brace*', 'waveguide*', 'port-*']


def icicle(x, y, z_top, length, r, seed, material='glass', color='#EAF6FC'):
    """A glass icicle hanging from z_top, its point at z_top - length: a lathe from the point up, a little wavy."""
    rnd = random.Random(seed)
    prof = [[0.0, 0.0]]
    n = 9
    for i in range(1, n + 1):
        t = i / n
        prof.append([round(r * (t ** 0.85) * (1 + 0.07 * math.sin(t * 11 + rnd.uniform(0, 6))), 5), round(length * t, 5)])
    return kit('lathe', material, color, profile=prof, position=[x, y, z_top - length], segments=40)


def icon_icicles(x, y, z_top, s, seed=0, material='glass', top=4.2, rot=0.0):
    """The icon as a mobile: a frosted glass bar hung on two threads, three glass icicles under it, touching, the middle
    one longest (icons.ice(), `s` m an icon unit)."""
    w, t = 570 * s, 80 * s
    out = [kit('box', 'foil', '#DDE3E8', size=[w, t, t], ease=t * 0.3, position=[x, y, z_top], rotate=[0, 0, rot])]
    c, si = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for dx, L in ((-190, 390), (0, 550), (190, 390)):
        out.append(icicle(x + dx * s * c, y + dx * s * si, z_top + t * 0.4, L * s + t * 0.4, 95 * s, seed + dx, material))
    for dx in (-0.42 * w, 0.42 * w):
        a = [x + dx * c, y + dx * si, z_top + t * 0.95]
        out.append(kit('thread', 'paper', '#E8EEF2', a=a, b=[a[0], a[1], top], radius=0.0015))
    return out


def ceiling(x0, x1, y, z, seed, n=9):
    """Icicles along the grotto's lip above the lens, long and short, out of focus at the frame's top."""
    rnd = random.Random(seed)
    out = [kit('box', 'frosted', '#D6ECF8', size=[x1 - x0 + 0.4, 0.5, 0.25], ease=0.08, position=[(x0 + x1) / 2, y, z + 0.5])]
    for i in range(n):
        xi = x0 + (x1 - x0) * (i + rnd.uniform(-0.3, 0.3)) / (n - 1)
        L = rnd.choice([0.35, 0.5, 0.7, 0.9]) * rnd.uniform(0.8, 1.1) + 0.5
        out.append(icicle(xi, y + rnd.uniform(-0.15, 0.15), z + 0.55, L, rnd.uniform(0.05, 0.09), seed * 10 + i))
    return out


def snowflake(x, y, z, r, rot=0.0, tilt=0.0, top=4.2, seed=0):
    rnd = random.Random(seed)
    br = [[0.40, 0.2 + rnd.uniform(-0.03, 0.03)], [0.64, 0.13 + rnd.uniform(-0.02, 0.02)]]
    out = [kit('ext', 'paper', '#FBFCFD', module='ice', fn='snowflake', radius=r, branches=br, depth=0.006,
               position=[x, y, z], rotate=[tilt, 0, rot])]
    out.append(kit('thread', 'paper', '#E8EEF2', a=[x, y, z + r * 0.98], b=[x, y, top], radius=0.0015))
    return out


def crystal(x, y, w, d, h, seed, material='frosted', color=ICE, rot=0.0):
    return kit('ext', material, color, module='ice', fn='crystal', size=[w, d, h], seed=seed, position=[x, y, -0.02],
               rotate=[0, 0, rot])


def snowman(x, y, s=1.0, turn=0.0):
    """The joke: a felt snowman in earmuffs, beside a loudspeaker. Three balls, coal eyes, a carrot, the muffs."""
    c, si = math.cos(math.radians(turn)), math.sin(math.radians(turn))
    def at(dx, dy, z):                                  # in the snowman's frame: +y toward what he faces
        return [round(x + dx * c - dy * si, 4), round(y + dx * si + dy * c, 4), round(z, 4)]
    r0, r1, r2 = 0.12 * s, 0.085 * s, 0.062 * s
    z0, z1 = r0 * 0.85, r0 * 0.85 + r0 * 0.8 + r1 * 0.75
    z2 = z1 + r1 * 0.8 + r2 * 0.8
    out = [kit('sphere', 'felt', SNOW, position=at(0, 0, z0), scale=[r0, r0, r0 * 0.92], grain=2.5),
           kit('sphere', 'felt', SNOW, position=at(0, 0, z1), scale=r1, grain=2.5),
           kit('sphere', 'felt', SNOW, position=at(0, 0, z2), scale=r2, grain=2.5)]
    for ex in (-0.022 * s, 0.022 * s):
        out.append(kit('sphere', 'clay', '#15181C', position=at(ex, r2 * 0.9, z2 + r2 * 0.25), scale=0.008 * s))
    nose = kit('cone', 'clay', '#E9772E', radius=0.011 * s, height=0.06 * s, position=at(0, r2 * 0.85, z2), segments=16)
    nose['rotate'] = [-90, 0, turn]
    out.append(nose)
    for side in (-1, 1):                                # the muffs: two fluffy pads on a silver band
        out.append(kit('sphere', 'wool', '#8FC6EA', position=at(side * r2 * 0.98, 0, z2 + r2 * 0.1), scale=[0.02 * s, 0.03 * s, 0.03 * s]))
    band = [at(side * r2 * 0.95 * math.cos(t), 0, z2 + r2 * 0.1 + r2 * 1.02 * math.sin(t))
            for side, t in [(1, 0.0), (1, 0.6), (1, 1.2), (0, 0), (-1, 1.2), (-1, 0.6), (-1, 0.0)]]
    band[3] = at(0, 0, z2 + r2 * 1.12)
    out.append(kit('tube', 'foil', '#DCE2E8', points=band, radius=0.005 * s, sides=10))
    return out


def drift(x, y, w, d, h, seed, color=SNOW, material='cotton', count=None, radius=(0.06, 0.17)):
    return kit('ext', material, color, module='ice', fn='drift', size=[w, d, h], seed=seed, radius=list(radius),
               count=count or int(60 + 90 * w * d), position=[x, y, -0.03])


def grotto():
    props = []
    # the ground: a navy felt bed, the glow under the ice (brightest under the speaker), the frosted glass lake
    props.append(kit('box', 'felt', DEEP, size=[30.0, 30.0, 0.02], position=[0, 2.0, -0.6]))
    props.append(kit('ext', 'glow', '#9EDBFF', module='ice', fn='pool', radius=4.2, emit=6.0, power=1.1, edge='#1F5A9C',
                     position=[0.3, 0.9, -0.25]))
    props.append(kit('ext', 'glass', '#BFDFF2', module='ice', fn='lake', size=[12.0, 9.0, 0.06], position=[0, 0.8, -0.001],
                     patch=0.7, rough=[0.05, 0.42]))
    props += snowman(-0.85, 0.5, 1.35, turn=-135)

    # the back wall: shards of frosted and clear glass, lit through by the lake and a lamp behind
    rnd = random.Random(31)
    shards = [(-3.6, 2.6, 1.2, 2.1), (-2.7, 3.1, 1.0, 2.7), (-1.9, 2.4, 0.6, 1.2), (-1.2, 3.4, 1.1, 2.0),
              (-0.3, 3.7, 1.3, 2.6), (0.7, 3.3, 0.9, 1.6), (1.5, 3.6, 1.2, 2.8), (2.3, 2.6, 0.6, 1.1),
              (3.0, 3.0, 1.1, 2.3), (3.9, 2.5, 1.2, 1.7), (-4.5, 2.0, 1.2, 1.6), (4.6, 2.0, 1.2, 1.8),
              (-2.9, 1.9, 0.5, 0.7), (2.9, 1.9, 0.6, 0.6), (0.2, 2.9, 0.5, 0.8), (-0.9, 2.7, 0.4, 0.55)]
    for i, (x, y, w, h) in enumerate(shards):
        k = crystal(x, y, w, w * 0.8, h, 100 + i, 'glass' if i % 3 == 0 else 'frosted',
                    '#CFEAF8' if i % 2 else '#A9D4EE', rot=rnd.uniform(0, 90))
        k['rotate'] = [rnd.uniform(-8, 8), rnd.uniform(-10, 10), k['rotate'][2]]
        props.append(k)
    # the ledge across the grotto and its icicles: the icon's rhythm, a big three right of the speaker, smaller threes
    props += icon_icicles(1.5, 0.35, 1.5, 0.0013, seed=1, rot=-25, top=3.2)
    props += icon_icicles(-1.7, 2.0, 2.0, 0.0008, seed=2, rot=8)

    # cotton-wool drifts banking the lake, wool heaps at the wall's foot
    props.append(drift(-2.4, -1.3, 2.4, 1.2, 0.42, 1))
    props.append(drift(2.3, -0.6, 2.0, 1.0, 0.36, 2))
    props.append(drift(-2.4, 1.6, 2.6, 1.0, 0.5, 3, WOOL, 'wool'))
    props.append(drift(2.4, 1.9, 2.8, 1.0, 0.55, 4, WOOL, 'wool'))
    props.append(drift(0.0, 2.6, 2.4, 0.9, 0.4, 5, WOOL, 'wool'))
    props.append(drift(-1.6, -2.7, 2.2, 1.0, 0.45, 6, radius=(0.06, 0.2)))
    props.append(drift(1.3, 0.8, 0.7, 0.4, 0.14, 7, radius=(0.02, 0.07)))
    props.append(drift(-1.75, -1.0, 1.4, 0.8, 0.3, 8))                 # the foreground, soft
    props.append(drift(1.25, -1.55, 1.6, 0.8, 0.28, 9))

    # paper snowflakes on threads, at three depths
    props += snowflake(-1.6, 0.5, 1.2, 0.26, rot=35, seed=1)
    props += snowflake(1.55, -0.2, 0.95, 0.2, rot=-20, seed=2)
    props += snowflake(-0.95, 1.2, 1.55, 0.12, rot=10, seed=3)
    props += snowflake(-2.6, -1.8, 1.9, 0.3, rot=40, seed=5)          # near the lens: soft

    # fine snow in the air
    props.append(kit('scatter', 'cotton', '#FFFFFF', count=900, radius=[0.004, 0.011], seed=7,
                     **{'in': [-3.5, -2.5, 0.05, 3.5, 3.0, 2.8]}, emit=0.6, emit_color='#EAF6FF'))
    return {'kind': 'stage', 'kit_scale': 11.0, 'props': props}


def lights():
    return {
        # skylight from above the grotto's mouth, front left: soft, cold
        'key': area(-40, 50, 5.0, 0.6, '#E6F1FF', (2.4, 2.0), (0.0, 0.0, 0.8)),
        # moonlight down through the grotto's mouth, on the snow alone (the speaker keeps its own light)
        'moon': {'type': 'area', 'size_m': [3.0, 3.0], 'position': [-1.0, -0.5, 5.5], 'target': [0.0, 0.5, 0.0],
                 'irradiance': 1.4, 'color': '#EEF5FF', 'receivers': ['prop*']},
        # the silver rims from behind, on the speaker's edges and the shards' tops
        'rim': {**area(165, 28, 4.0, 5.0, '#F2F8FF', (2.0, 0.8), (0.0, 0.2, 1.1)), 'receivers': PRODUCT},
        'rim_set': {**area(175, 48, 6.5, 2.6, '#E8F3FF', (4.0, 2.0), (0.0, 1.0, 0.3)), 'receivers': ['prop*']},
        'rim2': {**area(-145, 20, 4.0, 2.4, '#CFE8FF', (1.0, 1.4), (0.0, 0.2, 0.9)), 'receivers': PRODUCT},
        # behind the shards, low: light through the glass wall
        'wall': {'type': 'area', 'size_m': [9.0, 1.5], 'position': [0.0, 4.8, 0.8], 'target': [0.0, 0.0, 1.0],
                 'irradiance': 0.7, 'color': '#9FD8FF'},
        # the lake's light on the speaker from below the front (the glow, helped)
        'under': area(-5, 4, 2.8, 1.0, '#9ED6FA', (2.4, 0.3), (0.0, 0.0, 0.5)),
        # right behind the speaker, low, shining through its acrylic toward the lens
        'through': {'type': 'area', 'size_m': [0.9, 1.1], 'position': [0.3, 1.1, 0.45], 'target': [-0.6, -2.0, 0.55],
                    'irradiance': 6.0, 'color': '#CDEBFF',
                    'receivers': PRODUCT},
    }


def shot():
    cam = tilt_shift(elevation=24, azimuth=-30, distance=7.0, lens=60, target=(0.15, 0.35, 0.85), focus=(0.0, -0.2, 0.7),
                     miniature=11, fstop=3.5)
    return frame('ice', grotto(), lights(), cam, 'barkhorn, Ice, a frozen grotto', rotate_z=-10,
                 sky={'kind': 'gradient', 'zenith': '#0A1A30', 'horizon': '#123052', 'ground': '#081424', 'strength': 0.4},
                 fin=finish(bloom=0.3, bloom_px=45, threshold=0.75, saturation=0.15, lift=0.04, lift_color='#14304F',
                            vignette=0.22))


def portrait():
    land = shot()
    t = [0.45, 0.2, 0.98]
    # the same camera position, aimed a little right and up so the snowman and the icon both stay in the tall frame
    return portrait_of(land, lens_mm=80, target=t)
