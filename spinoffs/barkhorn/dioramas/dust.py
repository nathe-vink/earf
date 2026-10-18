"""Dust: golden hour in a suede desert (round 31; dust.md has the concept and the proof rounds).

A sand floor, ribbed corduroy dunes and cut-suede mesas under a big low paper sun on a paper sky. The sun rakes in low
from behind the speaker's right, so the orange acrylic glows and every piece throws a long shadow to the left. Beside
the speaker sits the icon in wool felt (three puffs trailing a flat wedge), with roadrunner footprints running off to
the right from its point: something just went past. Motes hang in the light; a sage corduroy saguaro is the one accent.
"""
import math, random

from common import finish, kit, mound, portrait_of, shot as frame, tilt_shift

SAND, SAND2 = '#E2A46C', '#CF8A55'
APRICOT, RUST, TERRA = '#E8A46E', '#A8482E', '#BF5F3E'
PUFF = '#E8955A'
SUN = '#FFE3B0'
SKY = '#F8C088'
# the sun: low, behind the speaker's left (azimuth 0 is from the front), matched to the paper sun on the sky card
SUN_AZ, SUN_EL = 122.0, 11.0
PAPER_SUN = (0.9, 6.0, 1.05, 0.72)                # x, y, z, radius


def sky():
    """A paper sky card far behind, and the tissue sun on it, lit from within, with two rings of thinner tissue round
    it for its glow."""
    x, y, z, r = PAPER_SUN
    out = [kit('box', 'paper', SKY, size=[18.0, 0.05, 7.0], position=[0.0, y + 0.2, -0.1], shadow=False, emit=0.12)]
    for k, (rr, c, e) in enumerate([(1.7, '#F4B482', 0.18), (1.32, '#F8BE84', 0.4), (1.0, '#FFC77E', 0.8), (0.86, '#FFD496', 1.05)]):
        out.append(kit('cylinder', 'paper', c, radius=r * rr, height=0.01, position=[x, y + 0.12 - 0.03 * k, z],
                       rotate=[90, 0, 0], emit=e, segments=128, shadow=False))
    return out


def mesa(x, y, w, h, colors, seed, squash=0.75):
    """A mesa of stacked suede layers: a flared talus at the foot, then near-vertical cliff bands with a small step at
    each, a flat top."""
    rnd = random.Random(seed)
    out = [kit('lathe', 'suede', colors[0], position=[x, y, -0.02], scale=[1.0, squash, 1.0], segments=72,
               profile=[[0, 0], [w * 1.55, 0], [w * 1.35, h * 0.06], [w * 1.12, h * 0.16], [w * 1.02, h * 0.24], [0, h * 0.24]])]
    z, r = h * 0.22, w
    bands = colors[1:]
    for i, c in enumerate(bands):
        t = (h * 0.78) / len(bands) * rnd.uniform(0.8, 1.2)
        prof = [[0, 0], [r, 0], [r * 0.985, t * 0.92], [r * 0.97, t], [0, t]]
        out.append(kit('lathe', 'suede', c, profile=[[round(a, 4), round(b, 4)] for a, b in prof],
                       position=[x, y, round(z, 4)], scale=[1.0, squash, 1.0], segments=72))
        z += t * 0.99
        r *= rnd.uniform(0.93, 0.985)
    return out


def strata(x, y, r, h, layers, seed, squash=0.7):
    return kit('ext', 'suede', layers[0], module='dust', fn='strata', position=[x, y, 0.0], radius=r, height=h,
               layers=layers, seed=seed, squash=squash, ease=0.004)


def tumbleweed(x, y, r):
    """A raffia tumbleweed mid-roll, lifted a hair off the sand on its bounce, a little dust kicked up behind it."""
    out = [kit('ext', 'paper', '#C79A64', module='dust', fn='tumbleweed', radius=r, count=48, strand=0.0026, seed=5,
               position=[x, y, r + 0.035], rotate=[12, 30, 0])]
    out.append(kit('puffs', 'wool', PUFF, puffs=[[-r * 1.15, r * 0.35, r * 0.42], [-r * 1.75, r * 0.3, r * 0.3],
                                                 [-r * 2.2, r * 0.22, r * 0.2]], depth=0.8, position=[x, y + 0.05, 0.0]))
    return out


def cactus(x, y, h, color='#8E9A6C'):
    """The one accent: a little saguaro of sage corduroy, its ribs running up, two arms."""
    r = h * 0.11
    out = [kit('tube', 'corduroy', color, points=[[x, y, -0.02], [x, y, h * 0.5], [x, y, h - r]], radius=r, rib='Z',
               grain=0.8, sides=24)]
    out.append(kit('sphere', 'corduroy', color, position=[x, y, h - r], scale=r, rib='Z', grain=0.8))
    for side, z0, top in ((-1, 0.38, 0.72), (1, 0.5, 0.86)):
        pts = [[x, y, h * z0], [x + side * h * 0.17, y, h * (z0 + 0.02)], [x + side * h * 0.22, y, h * (z0 + 0.12)],
               [x + side * h * 0.22, y, h * top]]
        out.append(kit('tube', 'corduroy', color, points=pts, radius=r * 0.68, rib='Z', grain=0.8, sides=20))
        out.append(kit('sphere', 'corduroy', color, position=[x + side * h * 0.22, y, h * top], scale=r * 0.68, rib='Z', grain=0.8))
    return out


def dune(x, y, sx, sy, sz, color, rot=0.0):
    return mound(x, y, -sz * 0.35, sx, sy, sz, color, material='corduroy', rotate=[0, 0, rot], rib='X', grain=2.5)


def streak(x0, y0):
    """The icon: three felt puffs (the Fog cloud's circles, small) at the tall end of a flat felt wedge that thins away
    along the ground; footprints run on from its point."""
    out = []
    s = 0.0021                                       # metres an icon unit
    # the icon's circles (marks.CLOUD at 0.62, moved left 174) and its wedge (-285..356 along the ground, 140 tall)
    circles = [(-179 * 0.62 - 174, 35 * 0.62, 115 * 0.62), (-19 * 0.62 - 174, -67 * 0.62, 173 * 0.62),
               (179 * 0.62 - 174, 19 * 0.62, 131 * 0.62)]
    ground = 121
    puffs = [[round((cx + 285) * s, 4), round((ground - cy) * s, 4), round(r * s, 4)] for cx, cy, r in circles]
    out.append(kit('puffs', 'wool', PUFF, puffs=puffs, depth=0.8, position=[x0, y0, 0.0]))
    # the wedge: a soft felt rope lying on the ground, fat under the puffs and thinning to a point
    L = (356 + 285) * s
    pts, rad = [], []
    for i in range(9):
        t = i / 8
        pts.append([round(x0 + 0.05 + L * t, 4), round(y0 + 0.01 * math.sin(t * 3), 4), round(0.07 * (1 - t) ** 1.2 + 0.004, 4)])
        rad.append(round(0.085 * (1 - t) ** 1.1 + 0.006, 4))
    out.append(kit('tube', 'wool', PUFF, points=pts, radius=rad, flat=0.55, sides=20))
    # footprints: a roadrunner's X, two toes forward and two back, pressed in a line toward the right
    x = x0 + L + 0.18
    for i in range(7):
        side = 0.045 if i % 2 else -0.045
        out.append(kit('extrude', 'suede', '#A85A36', outline=_foot(0.07), depth=0.004, ease=0.001,
                       position=[round(x, 4), round(y0 - 0.02 + side, 4), 0.006], rotate=[90, 0, 0]))
        x += 0.2
    return out


def _foot(L):
    """A roadrunner's footprint: an X, its toes at +-28 degrees off the line of travel, front and back."""
    pts = []
    for a in (28, 152, 208, 332):
        for da, rr in ((-14, 0.18), (0, 1.0), (14, 0.18)):
            if rr < 1:
                pts.append((math.cos(math.radians(a + da * 1.4)) * L * rr, math.sin(math.radians(a + da * 1.4)) * L * rr))
            else:
                pts.append((math.cos(math.radians(a)) * L, math.sin(math.radians(a)) * L))
    # keep the vertices in angular order round the centre
    pts.sort(key=lambda p: math.atan2(p[1], p[0]))
    return [[round(a, 4), round(b, 4)] for a, b in pts]


def motes():
    return [kit('scatter', 'glow', '#FFD9A0', emit=1.5, count=55, radius=[0.002, 0.005], seed=7,
                **{'in': [-0.6, -0.2, 0.2, 1.6, 1.2, 1.6]}, shadow=False)]


def props():
    out = [kit('box', 'sand', SAND, tint2=SAND2, size=[16.0, 14.0, 0.04], position=[0.0, -2.0, -0.04])]
    out += sky()
    # the mesas, far: rust and terracotta strata, the sun sinking behind the left one
    # the plateaus: broad, flat-topped, sheer-sided, Monument Valley in cut suede, receding into the warm haze
    out += [strata(-2.6, 5.5, 1.9, 1.05, ['#C8714A', RUST, '#B5563A', TERRA, '#A94B31'], 1, squash=0.38),
            strata(1.75, 5.0, 0.42, 1.15, ['#CD7A50', TERRA, RUST, '#C06041', RUST], 2, squash=0.85),
            strata(4.1, 5.9, 1.15, 0.85, ['#C86B45', RUST, TERRA, '#B0502F'], 3, squash=0.4),
            strata(-0.2, 5.85, 0.9, 0.55, ['#D08058', '#C46A47', '#BE6142'], 4, squash=0.45)]
    out += tumbleweed(-1.25, 0.5, 0.28)
    out += cactus(2.55, 2.5, 0.7)
    out += [kit('ext', 'corduroy', '#D68650', module='dust', fn='dunes', size=[14.0, 3.4], position=[0.5, 2.9, 0.0],
                ridges=[[-0.9, 0.32, 0.55], [0.1, 0.42, 0.6], [1.0, 0.5, 0.6]], seed=4, rib='Y', grain=2.0),
            kit('ext', 'corduroy', '#E09A62', module='dust', fn='dunes', size=[12.0, 1.8], position=[-0.5, -2.7, 0.0],
                ridges=[[0.0, 0.3, 0.45]], seed=9, rib='Y', grain=2.0)]
    out += streak(0.75, 0.15)
    out += motes()
    return out


def lights():
    return {
        # warm bounce off the sand and sky into the front, so the face reads against the light
        'fill': {'type': 'area', 'size_m': [3.0, 2.0], 'orbit': {'azimuth_deg': 10, 'elevation_deg': 18, 'distance_m': 5.0},
                 'target': [0.0, 0.0, 0.7], 'irradiance': 1.3, 'color': '#FFD2A8'},
        # the paper sun's own glow from behind, on the speaker's back edges
        'rim': {'type': 'area', 'size_m': [2.0, 1.2], 'orbit': {'azimuth_deg': SUN_AZ + 10, 'elevation_deg': 20, 'distance_m': 4.5},
                'target': [0.0, 0.0, 0.9], 'irradiance': 2.6, 'color': '#FFB070'},
    }


def shot():
    st = {'kind': 'stage', 'kit_scale': 11.0, 'props': props()}
    s = frame('dust', st, lights(),
              tilt_shift(elevation=19, azimuth=20, distance=8.2, lens=62, target=(0.75, 0.6, 0.85),
                         focus=(0.0, -0.15, 0.7), miniature=11),
              'barkhorn, Dust, golden hour in a suede desert',
              sky={'kind': 'gradient', 'zenith': '#F0B488', 'horizon': '#F6C899', 'ground': '#B8683F', 'strength': 0.35},
              fin=finish(bloom=0.3, saturation=0.18, lift=0.04, lift_color='#5C2A1C', vignette=0.22),
              rotate_z=16.0, haze={'box_m': [-9.0, 0.9, -0.1, 9.0, 6.0, 7.0], 'density': 0.012, 'anisotropy': 0.6,
                                    'color': '#FFD8B0'})
    s['sun'] = {'irradiance': 8.0, 'azimuth_deg': SUN_AZ, 'elevation_deg': SUN_EL, 'angle_deg': 2.0, 'color': '#FFB574'}
    return s


def portrait():
    """The 4:5 frame: the same set from the same side, nearer the speaker's axis, the sun above it and the streak and
    footprints running out to the lower right."""
    return portrait_of(shot(), **tilt_shift(elevation=20, azimuth=8, distance=6.4, lens=72, target=(-0.17, 0.6, 0.98),
                                             focus=(0.0, -0.15, 0.7), miniature=11))
