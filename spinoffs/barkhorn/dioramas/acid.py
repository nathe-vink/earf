"""Acid: acid rain, in glass and resin (round 31; the notes are in acid.md).

Seen level with the speaker: it stands in a pool of lemon resin on a wet chartreuse plain, under a wool cloud that
rains on threads. Each drop is the Acid icon's drop (a ball and the cone tangent to it) cast in lemon resin, with the
icon's two bubbles inside it as air. Behind, a bank of dark sour storm cloud in wool; a low sun between the bank and the
speaker comes through the rain and the speaker's golden acrylic, so the drops glow against the dark and the wet ground
mirrors them. A warm key on the speaker's front. The one nod: a paper cocktail umbrella stuck in a pool of acid.
"""
import math, random

from common import area, finish, kit, portrait_of, shot as frame, tilt_shift

LEMON, GROUND, POOL = '#FFE24A', '#5E7A10', '#F0D02A'
CLOUD, BELLY = '#F3EDB2', '#D4CF86'
STORM = '#3C4612'
FLOOR = 0.012
ROT = 22.0                                    # the speaker turned to show its left side to the camera
CAM = dict(elevation=2.5, azimuth=-6.0, distance=5.6, lens=70.0, target=(-0.08, 0.05, 0.7), focus=(0.0, -0.1, 0.75),
           miniature=6.0)
PCAM = dict(CAM, distance=4.4, lens=70.0, target=(-0.1, 0.05, 0.98))


def ext(fn, **k):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'acid', 'fn': fn, **k}


def cam_pos(c=CAM):
    az, el = math.radians(c['azimuth']), math.radians(c['elevation'])
    tx, ty, tz = c['target']
    d = c['distance']
    return tx + d * math.sin(az) * math.cos(el), ty - d * math.cos(az) * math.cos(el), tz + d * math.sin(el)


def clear_of_speaker(x, y, margin=0.12, cams=None):
    """Whether a drop at (x, y) stays out of the speaker's silhouette from every camera: nothing crosses the hero."""
    for c in cams or [CAM]:
        cx, cy, _ = cam_pos(c)
        a_s = math.atan2(0.0 - cx, 0.0 - cy)
        a_d = math.atan2(x - cx, y - cy)
        half = math.atan2(0.36 + margin, math.hypot(cx, cy))
        if abs(a_d - a_s) < half:
            return False
    return True


def wool_cloud(cx, cy, cz, w, seed, color=CLOUD, belly=BELLY, depth=0.75):
    """A plump wool cloud `w` wide: a row of big puffs on top, a flatter belly below (a little darker, in shade)."""
    rnd = random.Random(seed)
    top, low = [], []
    n = 5
    for i in range(n):
        t = i / (n - 1)
        r = w * (0.16 + 0.12 * math.sin(math.pi * t)) * rnd.uniform(0.9, 1.1)
        top.append([round((t - 0.5) * w, 4), round(r * 0.55 + rnd.uniform(-0.02, 0.02), 4), round(r, 4)])
    for i in range(n + 1):
        t = i / n
        r = w * 0.13 * rnd.uniform(0.85, 1.1)
        low.append([round((t - 0.5) * w * 1.05, 4), round(-r * 0.15, 4), round(r, 4)])
    return [kit('puffs', 'wool', color, puffs=top, depth=depth, position=[cx, cy, cz], grain=1.6),
            kit('puffs', 'wool', belly, puffs=low, depth=depth + 0.05, position=[cx, cy - 0.02, cz], grain=1.6)]


def storm_bank():
    """The backdrop: a long bank of dark wool storm cloud on the horizon, its tops catching the low sun."""
    out = []
    rnd = random.Random(5)
    for y, z0, rr, col, n in [(7.5, 0.55, 0.95, '#4A5616', 11), (8.6, 1.5, 1.2, '#525E1C', 9), (9.8, 2.6, 1.4, STORM, 8)]:
        puffs = []
        for i in range(n):
            x = -7.0 + 14.0 * i / (n - 1) + rnd.uniform(-0.3, 0.3)
            puffs.append([round(x, 3), round(z0 + rnd.uniform(-0.2, 0.25), 3), round(rr * rnd.uniform(0.75, 1.15), 3)])
        out.append(kit('puffs', 'wool', col, puffs=puffs, depth=0.6, position=[0, y, 0], grain=2.5))
    return out


def drops_under(cx, cy, cz, w, n, seed, z0=0.1, z1=None, h=(0.1, 0.17), dy=0.35):
    """`n` drops hung under a cloud, their bottoms between z0 and z1, none crossing the speaker."""
    rnd = random.Random(seed)
    z1 = z1 if z1 is not None else cz - 0.3
    out, tries = [], 0
    while len(out) < n and tries < 5000:
        tries += 1
        x = cx + rnd.uniform(-0.45, 0.45) * w
        y = cy + rnd.uniform(-dy, dy) * w
        if not clear_of_speaker(x, y, cams=[CAM, PCAM]):
            continue
        out.append([round(x, 4), round(y, 4), round(rnd.uniform(z0, z1), 4), round(rnd.uniform(*h), 4)])
    return out


def bubble(x, y, r, z=FLOOR):
    return kit('sphere', 'glass', '#F6F8E8', position=[x, y, z + r * 0.96], scale=r, segments=64)


def set_spec():
    props = []
    # the plain: a wet chartreuse varnish that runs to the storm
    props.append(kit('box', 'gloss', GROUND, size=[40.0, 30.0, FLOOR], position=[0, 8.0, 0.0], roughness=0.07))
    props += storm_bank()
    # pools of lemon resin, domed by their surface tension; the speaker stands in the big one
    pools = [(0.05, -0.05, 0.75, 0.55, 2), (-1.05, 0.35, 0.62, 0.36, 5), (1.45, 1.4, 0.8, 0.35, 9), (-0.9, 2.6, 1.0, 0.4, 13)]
    for x, y, rx, ry, s in pools:
        props.append(ext('puddle', material='resin', color=POOL, size=[rx, ry], height=0.014, dome=0.8, wobble=0.14,
                         seed=s, position=[x, y, FLOOR], emit=0.5))
    rings = []
    for (x, y, rx, ry, s), radii in zip(pools[1:], [(0.09, 0.18, 0.28), (0.1, 0.2), (0.12, 0.24)]):
        for r in radii:
            u = min(1.0, r / min(rx, ry) * 0.7)
            rings.append([x, y, r, 0.014 * 0.8 * (1 - u * u) - 0.003])          # on the dome
    props.append(ext('ripples', material='resin', color='#F7D63A', rings=rings, width=0.01, height=0.006,
                     position=[0, 0, FLOOR + 0.014], emit=0.15))
    # the nod: a cocktail umbrella in the pool on the left
    props.append(ext('umbrella', position=[-1.2, 0.3, FLOOR + 0.016], rotate=[-6, -22, 0], radius=0.2, rise=0.11,
                     height=0.42, colors=['#FFE04A', '#FBF6E4']))
    # glass bubbles: two big ones near the lens at the edges, one by the speaker's foot
    props += [bubble(-1.35, -2.1, 0.17), bubble(1.05, -1.7, 0.12), bubble(0.62, -0.42, 0.06)]
    # the clouds and their rain: the hero cloud over the left pool, more behind to the right and far back
    clouds = [(-1.3, 0.6, 1.5, 1.4, 1, 28), (1.6, 1.6, 1.85, 1.5, 2, 26), (-0.2, 3.2, 2.1, 2.0, 3, 26),
              (-3.0, 2.6, 2.3, 1.6, 4, 18), (3.4, 3.4, 2.4, 1.8, 6, 18)]
    drops = []
    for cx, cy, cz, w, s, n in clouds:
        props += wool_cloud(cx, cy, cz, w, s)
        drops += [d + [cz - 0.05] for d in drops_under(cx, cy, cz, w, n, s + 10)]
    # near the lens, at the frame's edges, out of focus
    near = [[1.05, -2.6, 1.25, 0.2], [1.12, -2.45, 0.75, 0.18]]
    drops += [d + [4.0] for d in near]
    props.append(ext('rain', color=LEMON, drops=[d[:4] for d in drops], tops=[d[4] for d in drops], bubbles=True,
                     thread_color='#F4F5DC', position=[0, 0, 0]))
    return {'kind': 'stage', 'kit_scale': 6.0, 'props': props}


def lights():
    sun = area(180 + CAM['azimuth'] + 32, 9, 3.4, 22.0, '#FFDF6A', (2.2, 2.2), (0.0, 0.0, 0.7))   # low, behind, unseen
    sun['shape'] = 'DISK'
    sun['specular'] = 0.7
    return {'sun': sun,
            'key': area(-38, 22, 4.5, 3.2, '#FFF4DA', (1.6, 1.6), (0.0, -0.1, 0.75)),
            'top': area(10, 70, 5.0, 1.4, '#F4F6D6', (3.0, 3.0), (0.0, 0.5, 0.8)),
            'rim': area(140, 22, 4.0, 4.0, '#FFF0A0', (1.2, 1.6), (0.0, 0.2, 0.9))}


def shot():
    return frame('acid', set_spec(), lights(), tilt_shift(**CAM), 'barkhorn, Acid, acid rain',
                 sky={'kind': 'gradient', 'zenith': '#2C340C', 'horizon': '#9A9A2E', 'ground': '#2E3A0A', 'strength': 0.35},
                 fin=finish(bloom=0.3, saturation=0.16, lift=0.04, lift_color='#2E380A', vignette=0.25),
                 position=(0.0, 0.0, FLOOR), rotate_z=ROT)


def portrait():
    """The 4:5 frame: the same set and light, the camera nearer, the clouds over the speaker."""
    return portrait_of(shot(), **tilt_shift(**PCAM))
