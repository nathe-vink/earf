"""Acid: acid rain, in glass and resin (round 31; the notes are in acid.md).

A wool cloud the colour of a sour storm hangs over the speaker and rains on it: lemon resin drops, each the Acid icon's
drop with its two air bubbles, hung on fine threads (the stop-motion way). The ground is a wet chartreuse varnish with
pools of lemon resin, ripple rings where the drops land, and glass bubbles. A low sun behind the rain backlights it, so
the drops and the speaker's golden acrylic glow and throw yellow light forward onto the wet ground.
"""
import math, random

from common import finish, kit, portrait_of, shot as frame, tilt_shift, area, point

LEMON, GROUND, POOL = '#FFE24A', '#6F8A14', '#F0D02A'
CLOUD, BELLY = '#FBF3B0', '#E2DC86'


def ext(fn, **k):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'acid', 'fn': fn, **k}


def wool_cloud(cx, cy, cz, w, seed, color='#DCDDB4', belly='#BFC48A'):
    """A plump wool cloud `w` wide: a row of big puffs on top, a flatter belly below (a little darker, in shade)."""
    rnd = random.Random(seed)
    top, low = [], []
    n = 5
    for i in range(n):
        t = i / (n - 1)
        x = (t - 0.5) * w
        r = w * (0.16 + 0.12 * math.sin(math.pi * t)) * rnd.uniform(0.9, 1.1)
        top.append([round(x, 4), round(r * 0.55 + rnd.uniform(-0.02, 0.02), 4), round(r, 4)])
    for i in range(n + 1):
        t = i / n
        x = (t - 0.5) * w * 1.05
        r = w * 0.13 * rnd.uniform(0.85, 1.1)
        low.append([round(x, 4), round(-r * 0.15, 4), round(r, 4)])
    return [kit('puffs', 'wool', color, puffs=top, depth=0.75, position=[cx, cy, cz], grain=1.6),
            kit('puffs', 'wool', belly, puffs=low, depth=0.8, position=[cx, cy - 0.02, cz], grain=1.6)]


def drops_under(cx, cy, cz, w, n, seed, z0=0.15, z1=None, h=(0.07, 0.12), avoid=None):
    """`n` drops hung under a cloud at (cx, cy, cz) `w` wide, their bottoms between z0 and z1, clear of `avoid`
    ((x, y, r): the speaker's footprint)."""
    rnd = random.Random(seed)
    z1 = z1 if z1 is not None else cz - 0.35
    out = []
    while len(out) < n:
        x = cx + rnd.uniform(-0.45, 0.45) * w
        y = cy + rnd.uniform(-0.25, 0.25) * w * 0.6
        if avoid and math.hypot(x - avoid[0], y - avoid[1]) < avoid[2]:
            continue
        out.append([round(x, 4), round(y, 4), round(rnd.uniform(z0, z1), 4), round(rnd.uniform(*h), 4)])
    return out


def bubbles(spots, seed):
    """Glass bubbles resting on the ground (or on a pool): [(x, y, r, z), ...]."""
    out = []
    for x, y, r, z in spots:
        out.append(kit('sphere', 'glass', '#F6F8E8', position=[x, y, z + r * 0.96], scale=r, segments=48))
    return out


def gumdrop(x, y, r, h, color, seed=0):
    """A resin hill in the distance, a gumdrop: a squashed dome (the backlight comes through it)."""
    return kit('sphere', 'resin', color, position=[x, y, 0.0], scale=[r, r * 0.8, h], segments=48, emit=0.35)


def umbrella(x, y, z):
    """The joke: a paper cocktail umbrella stuck in a pool of acid, open and tilted (the sour, served)."""
    return [ext('umbrella', position=[x, y, z], rotate=[-8, -26, 0], radius=0.2, rise=0.11, height=0.4,
                colors=['#FFE04A', '#FBF6E4'])]


def set_spec(variant='a'):
    props = []
    # the ground: a wet chartreuse varnish, wide enough that it melts into the distance (its top at FLOOR)
    props.append(kit('box', 'gloss', GROUND, size=[60.0, 60.0, FLOOR], position=[0, 10.0, 0.0], roughness=0.14))
    # gumdrop hills of resin in the distance, backlit
    for x, y, r, h, c in [(-3.6, 5.0, 1.2, 0.75, '#F2E24C'), (-1.5, 6.0, 1.5, 1.0, '#D8E24A'), (1.5, 5.4, 1.1, 0.7, '#FFE04A'),
                          (3.7, 6.4, 1.7, 1.1, '#CFE04A'), (0.3, 7.8, 2.2, 1.4, '#E8EA5A'), (-5.0, 7.6, 2.0, 1.2, '#E2E450')]:
        props.append(gumdrop(x, y, r, h, c))
    # pools of lemon resin (candy-gloss), ripples where drops landed, a big one under the speaker
    pools = [(0.1, -0.12, 0.62, 0.42, 2), (-1.3, -0.15, 0.58, 0.33, 5), (1.15, -1.35, 0.36, 0.22, 7),
             (1.25, 1.0, 0.55, 0.28, 9), (-1.55, -1.55, 0.32, 0.2, 11), (-0.4, 1.6, 0.5, 0.25, 13)]
    for x, y, rx, ry, s in pools:
        props.append(ext('puddle', material='resin', color=POOL, size=[rx, ry], height=0.014, dome=0.8, wobble=0.14,
                         seed=s, position=[x, y, FLOOR], emit=0.5))
    rings = []
    for (x, y, rx, ry, s), (dx, dy, radii) in zip(pools, [(0.3, -0.12, ()), (0.05, 0.0, (0.08, 0.16, 0.25)), (-0.02, 0.0, (0.07, 0.14)),
                                                          (-0.05, 0.0, (0.1, 0.19)), (0.0, 0.0, (0.09,)), (0.1, 0.05, (0.08, 0.15))]):
        for r in radii:
            u = min(1.0, r / min(rx, ry))
            rings.append([x + dx, y + dy, r, 0.014 * 0.8 * (1 - u * u) - 0.003])   # on the dome
    props.append(ext('ripples', material='resin', color='#F7D63A', rings=rings,
                     width=0.009, height=0.006, position=[0, 0, FLOOR + 0.014], emit=0.15))
    props += umbrella(-1.05, -0.32, FLOOR + 0.016)
    # the wet: beads of acid standing on the varnish, half sunk
    props.append(kit('scatter', 'resin', '#FFE24A', count=380, radius=[0.006, 0.015], seed=21, emit=0.8,
                     **{'in': [-3.2, -2.6, 0.0, 2.6, 2.4, 0.0]}, position=[0, 0, FLOOR - 0.002], scale=[1.0, 1.0, 1.0]))
    # glass bubbles, of three sizes; a big one in the near corner, out of focus
    props += bubbles([(-0.85, -0.9, 0.07, FLOOR), (-0.98, -0.82, 0.04, FLOOR), (0.85, -0.6, 0.05, FLOOR + 0.012),
                      (-2.0, -0.4, 0.1, FLOOR), (1.9, 0.3, 0.09, FLOOR), (0.45, -1.4, 0.035, FLOOR),
                      (1.7, -2.4, 0.16, FLOOR)], 1)
    # the clouds and their rain: a big one over the pool on the speaker's left, more behind
    clouds = [(-1.2, 0.05, 1.66, 1.05, 1, 24), (1.35, 1.3, 2.15, 1.2, 2, 18), (-0.1, 2.6, 2.45, 1.6, 3, 22),
              (-3.0, 1.8, 2.2, 1.3, 4, 16), (3.2, 3.0, 2.5, 1.5, 6, 16)]
    drops = []
    for cx, cy, cz, w, s, n in clouds:
        props += wool_cloud(cx, cy, cz, w, s, color=CLOUD, belly=BELLY)
        drops += [d + [cz - 0.05] for d in drops_under(cx, cy, cz, w, n, s + 10, z0=0.12, z1=cz - 0.45,
                                                       h=(0.11, 0.19), avoid=(0.0, 0.0, 0.42))]
    # a few strings of drops close to the lens, out of focus, framing the near corners
    near = [[-0.3, -3.05, 2.1, 0.22], [-0.4, -3.2, 2.65, 0.2], [-0.22, -2.9, 1.62, 0.24]]
    drops += [d + [4.0] for d in near]
    props.append(ext('rain', color=LEMON, drops=[d[:4] for d in drops], tops=[d[4] for d in drops], bubbles=True,
                     thread_color='#F4F5DC', position=[0, 0, 0]))
    return {'kind': 'stage', 'kit_scale': 11.0, 'props': props}


FLOOR = 0.012


def lights():
    sun = area(162, 15, 4.4, 22.0, '#FFE070', (2.4, 2.4), (0.0, 0.0, 0.7))
    sun['shape'] = 'DISK'
    sun['specular'] = 0.6                                 # its glare on the wet ground, a halo, not a hole
    return {'sun': sun,
            'front': area(-25, 64, 6.0, 4.0, '#FFF8E0', (3.0, 2.4), (0.0, 0.0, 0.7)),
            'rim': area(125, 35, 5.0, 3.0, '#FFF2B0', (1.6, 1.2), (0.0, 0.3, 1.2))}


def shot():
    cam = tilt_shift(elevation=24, azimuth=-18, distance=7.2, lens=64, target=(-0.5, 0.2, 0.92), focus=(0.0, -0.08, 0.9),
                     miniature=10.0)
    return frame('acid', set_spec(), lights(), cam, 'barkhorn, Acid, acid rain',
                 sky={'kind': 'gradient', 'zenith': '#D6DC7A', 'horizon': '#F4EBA8', 'ground': '#7E8E22', 'strength': 0.6},
                 fin=finish(bloom=0.3, saturation=0.16, lift=0.04, lift_color='#3E4A0C', vignette=0.25),
                 position=(0.0, 0.0, FLOOR))


def portrait():
    """The 4:5 frame: the same set and light, a longer lens from the same place, the speaker and the cloud stacked."""
    cam = tilt_shift(elevation=24, azimuth=-18, distance=7.2, lens=94, target=(-0.42, 0.1, 1.1), focus=(0.0, -0.08, 0.9),
                     miniature=10.0)
    return portrait_of(shot(), **cam)
