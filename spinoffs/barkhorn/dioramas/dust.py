"""Dust: golden hour in a suede desert (round 31; dust.md has the concept and the proof rounds).

A sand floor, ribbed corduroy dunes and stacked suede mesas under a big low tissue-paper sun on a paper sky. The sun
rakes in low from behind the speaker's left, so the orange acrylic glows and throws its colour on the sand. Beside the
speaker, a felt dust cloud in the icon's shape (three puffs trailing a flat wedge) and a line of roadrunner footprints
running off to the right: something just went past. Motes hang in the light.
"""
import math, random

from common import finish, kit, mound, portrait_of, shot as frame, tilt_shift

SAND, SAND2 = '#E2A46C', '#CF8A55'
APRICOT, RUST, TERRA = '#E8A46E', '#A8482E', '#BF5F3E'
PUFF = '#F4D2AE'
SUN = '#FFE3B0'
SKY = '#F2B888'
# the sun: low, behind the speaker's left (azimuth 0 is from the front), matched to the paper sun on the sky card
SUN_AZ, SUN_EL = -150.0, 13.0
PAPER_SUN = (-2.0, 4.6, 1.15, 1.25)                # x, y, z, radius


def sky():
    """A paper sky card far behind, and the tissue sun on it, lit from within."""
    x, y, z, r = PAPER_SUN
    out = [kit('box', 'paper', SKY, size=[16.0, 0.05, 6.0], position=[0.0, y + 0.12, -0.1])]
    out.append(kit('cylinder', 'tissue', SUN, radius=r, height=0.02, position=[x, y, z], rotate=[90, 0, 0],
                   emit=5.0, segments=96))
    out.append(kit('cylinder', 'tissue', '#FFF0D0', radius=r * 0.82, height=0.02, position=[x, y - 0.03, z],
                   rotate=[90, 0, 0], emit=7.0, segments=96))
    return out


def mesa(x, y, w, h, colors, seed, squash=0.8):
    """A butte of stacked suede layers, each a turned slab a little narrower than the one below."""
    rnd = random.Random(seed)
    out, z, r = [], -0.02, w
    n = len(colors)
    for i, c in enumerate(colors):
        t = h / n * rnd.uniform(0.85, 1.15)
        r1 = r * (0.93 if i < n - 1 else 0.9)
        prof = [[0, 0], [r, 0], [r * 0.99, t * 0.3], [r1 * 1.01, t * 0.85], [r1 * 0.97, t], [0, t]]
        out.append(kit('lathe', 'suede', c, profile=[[round(a, 4), round(b, 4)] for a, b in prof],
                       position=[x, y, z], scale=[1.0, squash, 1.0], segments=72))
        z += t * 0.98
        r = r1 * rnd.uniform(0.94, 0.99)
    return out


def dune(x, y, sx, sy, sz, color, rot=0.0):
    return mound(x, y, -sz * 0.35, sx, sy, sz, color, material='corduroy', rotate=[0, 0, rot], rib='X')


def streak(x0, y0):
    """The icon: three felt puffs (the Fog cloud's circles, small) at the tall end of a flat felt wedge that thins away
    along the ground; footprints run on from its point."""
    out = []
    s = 0.0012                                       # metres an icon unit
    # the icon's circles (marks.CLOUD at 0.62, moved left 174) and its wedge (-285..356 along the ground, 140 tall)
    circles = [(-179 * 0.62 - 174, 35 * 0.62, 115 * 0.62), (-19 * 0.62 - 174, -67 * 0.62, 173 * 0.62),
               (179 * 0.62 - 174, 19 * 0.62, 131 * 0.62)]
    ground = 121
    puffs = [[round((cx + 285) * s, 4), round((ground - cy) * s, 4), round(r * s, 4)] for cx, cy, r in circles]
    out.append(kit('puffs', 'felt', PUFF, puffs=puffs, depth=0.8, position=[x0, y0, 0.0]))
    # the wedge: a soft felt rope lying on the ground, fat under the puffs and thinning to a point
    L = (356 + 285) * s
    pts, rad = [], []
    for i in range(9):
        t = i / 8
        pts.append([round(x0 + 0.05 + L * t, 4), round(y0 + 0.01 * math.sin(t * 3), 4), round(0.07 * (1 - t) ** 1.2 + 0.004, 4)])
        rad.append(round(0.085 * (1 - t) ** 1.1 + 0.006, 4))
    out.append(kit('tube', 'felt', PUFF, points=pts, radius=rad, flat=0.55, sides=20))
    # footprints: a roadrunner's X, two toes forward and two back, pressed in a line toward the right
    x = x0 + L + 0.18
    for i in range(7):
        side = 0.045 if i % 2 else -0.045
        out.append(kit('extrude', 'suede', '#B86A42', outline=_foot(0.055), depth=0.004, ease=0.001,
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
    return [kit('scatter', 'glow', '#FFD9A0', emit=2.5, count=160, radius=[0.003, 0.008], seed=7,
                **{'in': [-1.6, -0.9, 0.15, 1.8, 1.4, 1.9]}, shadow=False)]


def props():
    out = [kit('box', 'sand', SAND, tint2=SAND2, size=[16.0, 14.0, 0.04], position=[0.0, -2.0, -0.04])]
    out += sky()
    # the mesas, far: rust and terracotta strata, the sun sinking behind the left one
    out += mesa(-1.2, 3.6, 1.15, 1.25, [RUST, TERRA, '#B4553A', RUST, '#9E4330'], 1)
    out += mesa(2.6, 3.4, 1.5, 0.9, [TERRA, '#C96A44', RUST, TERRA], 2, squash=0.7)
    out += mesa(0.9, 4.1, 0.7, 0.55, ['#C86B45', TERRA, '#D07A4E'], 3)
    # corduroy dunes, middle distance and a soft lip in the foreground
    out += [dune(-2.6, 1.6, 1.8, 0.9, 0.5, '#D3814C', 12), dune(1.9, 1.8, 2.2, 1.0, 0.42, '#DB8E58', -8),
            dune(0.2, 2.6, 2.4, 0.8, 0.38, '#C9744A', 4), dune(-0.9, -2.9, 2.6, 0.9, 0.36, '#E19A63', 6),
            dune(3.2, -1.6, 1.4, 0.8, 0.3, '#D8894F', -20)]
    out += streak(0.55, -0.35)
    out += motes()
    return out


def lights():
    return {
        # warm bounce off the sand and sky into the front, so the face reads against the light
        'fill': {'type': 'area', 'size_m': [3.0, 2.0], 'orbit': {'azimuth_deg': -25, 'elevation_deg': 18, 'distance_m': 5.0},
                 'target': [0.0, 0.0, 0.7], 'irradiance': 0.7, 'color': '#FFD2A8'},
        # the paper sun's own glow from behind, on the speaker's back edges
        'rim': {'type': 'area', 'size_m': [2.0, 1.2], 'orbit': {'azimuth_deg': SUN_AZ + 10, 'elevation_deg': 20, 'distance_m': 4.5},
                'target': [0.0, 0.0, 0.9], 'irradiance': 1.2, 'color': '#FFC080'},
    }


def shot():
    st = {'kind': 'stage', 'kit_scale': 11.0, 'props': props()}
    s = frame('dust', st, lights(),
              tilt_shift(elevation=22, azimuth=-20, distance=8.0, lens=65, target=(0.35, 0.3, 0.7),
                         focus=(0.0, -0.15, 0.7), miniature=11),
              'barkhorn, Dust, golden hour in a suede desert',
              sky={'kind': 'gradient', 'zenith': '#F0B488', 'horizon': '#F6C899', 'ground': '#B8683F', 'strength': 0.35},
              fin=finish(bloom=0.3, saturation=0.18, lift=0.04, lift_color='#5C2A1C', vignette=0.22),
              rotate_z=-14.0)
    s['sun'] = {'irradiance': 4.5, 'azimuth_deg': SUN_AZ, 'elevation_deg': SUN_EL, 'angle_deg': 2.0, 'color': '#FFB574'}
    return s


def portrait():
    return portrait_of(shot(), lens=55)
