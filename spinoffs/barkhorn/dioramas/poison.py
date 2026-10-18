"""Poison: a redwood forest floor, in moss, felt, corduroy and velvet (round 31; poison.md has the concept and the rounds).

The owner's direction: "a mossy, ferny redwood forest with a fallen log and poisonous mushrooms", the speaker placed in
its atmosphere of the earth. Corduroy redwood trunks rise out of the frame, flaring at their feet; moss flock lies over
everything, with felt ferns, a fallen log furred in moss and red velvet fly agarics with felt spots on it and round it
(the one accent), pale death caps at its foot. Green-gold light falls through the canopy in shafts into a low mist.
The bottle green speaker stands in the light, its acrylic glowing. Two quiet nods to the witch: a little potion
bottle tucked by the log, and the icon's skull in clay in the moss.
"""
import math, os, random

import common as C

from common import finish, kit, point, area, spot, portrait_of, shot as frame, tilt_shift

# the palette: moss greens and redwood rust, the gold of the light, fly agaric red the one accent
MOSS, MOSS2 = '#1D2E19', '#43592B'
DEEP, DEEP2 = '#16220F', '#2A3A1C'
REDWOOD, REDWOOD_DEEP = '#6E3424', '#4A2219'
AGARIC = '#B8261C'
DEATHCAP = '#CDD3B4'
SPOT = '#EFEBDD'
FERN, FERN2 = '#3B6A27', '#4F7F30'
LIGHT = '#FFE3A2'
MOTE = '#FFE6A0'
SPEAKER = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'waveguide*', 'woofer-*', 'port*', 'rib-*',
           'brace*', 'feet-*', 'grip-*', 'mark-back', 'land-*', 'hf-*', 'lining-*', 'amp-*', 'post-*', 'top-pad']


def ext(fn, position, rotate=(0, 0, 0), scale=1.0, **k):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'poison', 'fn': fn, 'position': list(position),
            'rotate': list(rotate), 'scale': scale, **k}


def agaric(x, y, h, cap_r, cap_h, stem, lean=(0, 0), seed=1, spots=9, turn=0.0, z=0.0, **k):
    """A fly agaric: red velvet cap, felt warts, a cream felt stem with its skirt."""
    return ext('toadstool', (x, y, z), (0, 0, turn), height=h, cap=[cap_r, cap_h], stem=stem, cap_color=AGARIC,
               spot_color=SPOT, stem_color='#ECE4CF', gill_color='#E9DFC6', lean=list(lean), seed=seed, spots=spots, **k)


def deathcap(x, y, h, cap_r, seed, lean=(0, 0), z=0.0):
    """A death cap: pale olive-white, no warts, a skirt."""
    return ext('toadstool', (x, y, z), height=h, cap=[cap_r, cap_r * 0.55], stem=cap_r * 0.18, cap_color=DEATHCAP,
               spot_color=DEATHCAP, stem_color='#E8E8DA', gill_color='#EDEDE0', lean=list(lean), seed=seed, spots=0)


def fern(x, y, length, seed, fronds=9, rise=0.55, turn=0.0):
    return ext('fern', (x, y, 0.0), (0, 0, turn), length=length, fronds=fronds, rise=rise, seed=seed, color=FERN, tint=FERN2)


def trunk(x, y, r, seed, height=12.0, flare=0.7):
    return ext('trunk', (x, y, 0.0), (0, 0, seed * 37 % 360), radius=r, height=height, flare=flare, foot=r * 1.3,
               lobes=5 + seed % 3, seed=seed, color=REDWOOD, material='corduroy', rib='X', grain=3.0)


# the ground: rolling moss, calm where the speaker stands, raised round the trunks' feet and in banks behind
TRUNKS = [(-2.35, 1.5, 0.78, 1), (1.7, 3.5, 0.98, 2), (-0.2, 6.2, 0.7, 3), (3.1, 1.3, 0.62, 4), (-4.3, 4.6, 0.85, 5),
          (4.4, 6.5, 0.9, 6)]
GROUND = {'position': [0.0, 3.0, 0.0], 'size': [22.0, 18.0], 'res': 0.07, 'amp': 0.08, 'feature': 0.9, 'calm': [0.55, 0.45],
          'bumps': [[-2.6, 0.9, 1.2, 0.9, 0.12], [2.9, 2.6, 1.8, 1.2, 0.2], [0.3, 4.4, 3.2, 1.4, 0.25], [-3.6, 0.0, 1.2, 1.0, 0.16],
                    [4.2, 0.4, 1.3, 1.0, 0.18]] + [[x, y, r * 2.2, r * 2.2, 0.18] for x, y, r, _ in TRUNKS],
          'dents': []}
LOG = [(-2.5, -0.95, 0.0), (-1.55, -0.5, 0.0), (-0.68, -0.08, 0.0)]     # the fallen log's axis, its foot to its broken end
LOG_R = 0.27


def gz(x, y):
    """The ground's height at (x, y), as the kit's terrain builds it."""
    return round(_kit_ext().ground_z(GROUND, x, y), 4)


_K = []


def _kit_ext():
    """This set's kit pieces (studio/engine/kit_ext/poison.py; the same name as this module, so loaded by path)."""
    if not _K:
        import importlib.util
        import bpy  # noqa: F401  (mathutils comes with it)
        sp = importlib.util.spec_from_file_location('poison_kit', os.path.join(C.ROOT, 'studio', 'engine', 'kit_ext', 'poison.py'))
        _K.append(importlib.util.module_from_spec(sp)); sp.loader.exec_module(_K[0])
    return _K[0]


def on_ground(piece, sink=0.01):
    x, y = piece['position'][:2]
    piece['position'][2] += gz(x, y) - sink
    return piece


def _along(pts, t):
    """A point `t` of the way along the log's two spans."""
    seg = 0 if t < 0.5 else 1; u = (t - 0.5 * seg) * 2
    return [pts[seg][i] + (pts[seg + 1][i] - pts[seg][i]) * u for i in range(3)]


def log():
    """The fallen redwood: a corduroy log on the moss, its broken end a clay face with rings, moss over its back,
    fly agarics standing on it."""
    pts = [[x, y, gz(x, y) + LOG_R * 0.8] for x, y, _ in LOG]
    out = [kit('tube', 'corduroy', REDWOOD_DEEP, points=pts, radius=[LOG_R * 1.05, LOG_R, LOG_R * 0.95], rib='Y', grain=1.0,
               sides=40, position=[0, 0, 0])]
    # the broken end: a clay face with its rings, turned to the log's axis
    (x1, y1, z1), (x0, y0, z0) = pts[-1], pts[-2]
    ax = math.degrees(math.atan2(y1 - y0, x1 - x0))
    for k, (rr, c) in enumerate([(0.93, '#9C5A3C'), (0.7, '#B57450'), (0.45, '#9C5A3C'), (0.2, '#B57450')]):
        out.append(kit('cylinder', 'clay', c, radius=LOG_R * 0.95 * rr, height=0.012 + 0.002 * k, position=[x1, y1, z1],
                       rotate=[0, 90, ax]))
    # moss along its back, in clumps
    rnd = random.Random(31)
    for i in range(46):
        x, y, z = _along(pts, rnd.uniform(0.02, 0.95))
        off = rnd.uniform(-0.6, 0.6); s = rnd.uniform(0.05, 0.11)
        out.append(ext('moss', (x - off * LOG_R * 0.35, y + off * LOG_R, z + LOG_R * math.cos(off) * 0.9), scale=[s * 1.4, s, s * 0.55],
                       color=MOSS2, tint2='#5C7034', **{'as': 'sphere'}))
    # fly agarics on the log
    for (t, h, r, sd) in [(0.62, 0.42, 0.17, 41), (0.7, 0.26, 0.11, 42), (0.55, 0.18, 0.08, 43), (0.35, 0.3, 0.12, 44)]:
        x, y, z = _along(pts, t)
        out.append(agaric(x, y + rnd.uniform(-0.05, 0.05), h, r, r * 0.62, r * 0.17, lean=(rnd.uniform(-0.03, 0.03), -0.02),
                          seed=sd, spots=8, z=z + LOG_R * 0.85 - 0.02))
    return out


def cushions(seed=12, n=600):
    """Cushion moss over the floor, kept from under the speaker."""
    rnd = random.Random(seed); pts = []
    while len(pts) < n:
        x, y = rnd.uniform(-3.0, 3.2), rnd.uniform(-1.8, 2.0)
        if abs(x) < 0.4 and abs(y) < 0.35:
            continue
        pts.append([round(x, 3), round(y, 3), round(rnd.uniform(0.02, 0.06), 3)])
    return pts


def garden():
    P = [ext('terrain', GROUND['position'], **{k: v for k, v in GROUND.items() if k != 'position'}, color=MOSS, tint2=MOSS2)]
    P.append(ext('clumps', (0, 0, 0), points=cushions(), ground=GROUND, color=MOSS2, tint2='#5A7234'))
    # the mist: a low bank torn into wisps over the floor behind the speaker
    P.append(ext('mist', (0.0, 3.0, -0.05), size=[14.0, 7.0, 0.6], density=0.5, wisp=0.7, wisp_lo=0.46, wisp_hi=0.64,
                 color='#E6EEDD', anisotropy=0.5))
    # the air of the forest behind the speaker, where the light through the canopy shows as shafts (none in front of
    # the speaker, so it stays crisp)
    P.append(ext('mist', (0.0, 6.6, 0.0), size=[18.0, 9.0, 12.0], density=0.4,
                 color='#F2F2E2', anisotropy=0.55))
    P += log()
    # the redwoods, rising out of the frame
    for x, y, r, sd in TRUNKS:
        P.append(on_ground(trunk(x, y, r, sd), 0.25))
    G = []
    # ferns: one beside the speaker, others at the trunks' feet and in the foreground blur
    G += [fern(0.95, 0.65, 0.85, 1, 11, 0.6), fern(2.35, 0.2, 0.75, 2, 10), fern(-1.35, 1.45, 0.9, 3, 11, 0.65),
          fern(1.05, 2.4, 1.0, 4, 12), fern(-2.9, 1.2, 0.8, 5), fern(-1.5, -1.45, 0.7, 6, 9, 0.5), fern(2.9, -0.9, 0.7, 7, 9),
          fern(-3.4, 3.0, 1.0, 8, 11), fern(3.1, 2.2, 0.9, 9, 10)]
    # fly agarics on the floor: a family right of the speaker, one tall one by the log
    G += [agaric(0.62, -0.22, 0.46, 0.18, 0.11, 0.032, lean=(0.03, 0.0), seed=1, spots=9),
          agaric(0.82, -0.05, 0.26, 0.11, 0.07, 0.022, lean=(0.03, 0.01), seed=2, spots=6),
          agaric(-0.3, -0.8, 0.22, 0.1, 0.065, 0.02, lean=(0.02, -0.01), seed=3, spots=6, skirt=False),
          agaric(-1.15, 0.4, 0.62, 0.24, 0.15, 0.042, lean=(-0.04, 0.0), seed=4, spots=10),
          agaric(2.0, 1.1, 0.5, 0.2, 0.12, 0.036, lean=(0.04, 0.0), seed=5, spots=8)]
    # death caps at the log's foot
    G += [deathcap(1.05, -0.62, 0.24, 0.1, 11, (0.02, -0.02)), deathcap(1.25, -0.72, 0.16, 0.07, 12),
          deathcap(0.92, -0.82, 0.12, 0.055, 13), deathcap(-1.75, -0.08, 0.2, 0.085, 14)]
    # the nods to the witch: the icon's skull in the moss by the speaker's foot, a potion bottle tucked by the log's end
    G.append(ext('skull', (0.42, -0.46, 0.0), (-10, 0, -18), size=0.08))
    G.append(ext('potion', (-0.56, -0.32, 0.0), (0, 6, 0), size=0.1))
    P += [on_ground(g, 0.012) for g in G]
    # motes in the light: a sparse glow drifting
    P.append(kit('scatter', 'glow', MOTE, emit=5.0, count=55, radius=[0.0025, 0.006], seed=21, shadow=False,
                 **{'in': [-2.8, -1.4, 0.2, 2.8, 2.4, 2.6]}))
    return P


def shot():
    st = {'kind': 'stage', 'kit_scale': 11.0, 'props': garden()}
    # the light through the canopy: a broad shaft from high behind on the left onto the speaker, a smaller one beyond
    sun = spot((-5.2, -0.6, 10.5), (0.05, -0.1, 0.3), 32000, 11.0, 0.6, LIGHT, 0.3)
    sun2 = spot((-3.0, 7.5, 11.0), (2.4, 1.2, 0.0), 14000, 6.0, 0.6, LIGHT, 0.3)
    canopy = {**area(0, 85, 6.0, 0.6, '#B6D3A2', (6.0, 6.0), (0.0, 1.0, 0.0)), 'specular': 0.0}
    key = area(-42, 30, 5.5, 0.6, '#D8E4D2', (2.6, 2.0), (0.0, 0.0, 0.8))
    # the speaker's own: a warm rim from behind, the forest's green-gold low on its face, its green on the moss
    rim = {**area(160, 55, 4.0, 12.0, '#FFEFC8', (1.4, 1.0), (0.0, 0.1, 1.0)), 'receivers': SPEAKER}
    glow = {**area(40, 14, 3.0, 4.5, '#D6F2C0', (1.6, 0.8), (0.0, 0.0, 0.5)), 'receivers': SPEAKER}
    spill = {**point((0.05, -0.5, 0.35), 12, '#5EE07A', 0.25), 'specular': 0.0}
    # more shafts, parallel to the first, falling between the trunks behind
    shafts = {f'shaft{i}': spot((-5.2 + dx, 2.0 + dy, 10.5), (0.05 + dx, -0.1 + dy, 0.0), pw, cone, 0.5, LIGHT, 0.2)
              for i, (dx, dy, pw, cone) in enumerate([(0.8, 2.6, 16000, 6.0), (2.4, 4.2, 14000, 5.0), (-0.4, 5.0, 16000, 6.5)])}
    lights = {**shafts, 'sun': sun, 'sun2': sun2, 'canopy': canopy, 'key': key, 'rim': rim, 'glow': glow, 'spill': spill}
    cam = tilt_shift(elevation=22, azimuth=-20, distance=7.3, lens=60, target=(0.15, 0.3, 0.85), focus=(0.0, -0.25, 0.7),
                     fstop=2.8, miniature=11.0)
    sky = {'kind': 'gradient', 'zenith': '#2C3A22', 'horizon': '#3E4E30', 'ground': '#141C10', 'strength': 0.6}
    hz = {'box_m': [-12, -12, -0.3, 12, 12, 12], 'density': 0.03, 'anisotropy': 0.55, 'color': '#EEF2E2'}
    return frame('poison', st, lights, cam, 'barkhorn, Poison, a redwood forest floor', sky=sky,
                 fin=finish(bloom=0.28, bloom_px=44, threshold=0.72, saturation=0.14, lift=0.03, lift_color='#141E10',
                            vignette=0.22, contrast=0.12))


def portrait():
    # the 4:5 frame: a longer lens, the speaker on the centre line, the log at the left, the trunks rising above
    cam = tilt_shift(elevation=20, azimuth=-18, distance=8.0, lens=106, target=(0.1, -0.12, 0.9), focus=(0.0, -0.25, 0.7),
                     fstop=2.8, miniature=11.0)
    return portrait_of(shot(), **cam)
