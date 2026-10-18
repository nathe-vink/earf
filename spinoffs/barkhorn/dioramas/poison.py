"""Poison: a poison garden, in moss, velvet and clay (round 31; poison.md has the concept and the rounds).

A moss-flocked clearing at night. Velvet toadstools with felt spots, clay nightshade, velvet foxglove spires and a
crooked black tree stand round a glossy green resin swamp that glows from within, glass bubbles rising from it; spores
drift, a low mist lies on the moss, and the bottle green speaker stands at the swamp's edge, lit through from behind
by a cold moon so its acrylic glows and throws green on the moss. A tiny clay skull, the icon, lies in the moss.
"""
import math, os, random

import common as C

from common import finish, kit, mound, point, area, spot, portrait_of, shot as frame, tilt_shift

# the palette: apothecary greens and blacks, foxglove violet the one accent
MOSS, MOSS2 = '#15231A', '#3A5230'
DEEP, DEEP2 = '#0F1A11', '#1B2B1A'
VELVET_CAP = '#22422B'
BLACK_CAP = '#101511'
SPOT = '#E6E2C8'
BARK = '#121412'
FOXGLOVE = '#7E3A70'
RESIN = '#1E6A2E'
GLOW = '#6CFF8A'
SPORE = '#D6FF9C'
SPEAKER = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'waveguide*', 'woofer-*', 'port*', 'rib-*',
           'brace*', 'feet-*', 'grip-*', 'mark-back', 'land-*', 'hf-*', 'lining-*', 'amp-*', 'post-*', 'top-pad']


def ext(fn, position, rotate=(0, 0, 0), scale=1.0, **k):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'poison', 'fn': fn, 'position': list(position),
            'rotate': list(rotate), 'scale': scale, **k}


def toadstool(x, y, h, cap_r, cap_h, stem, color=VELVET_CAP, lean=(0, 0), seed=1, spots=9, turn=0.0, **k):
    return ext('toadstool', (x, y, 0.0), (0, 0, turn), height=h, cap=[cap_r, cap_h], stem=stem, cap_color=color,
               spot_color=SPOT, lean=list(lean), seed=seed, spots=spots, **k)


def foxglove(x, y, h, lean=(0.05, 0.0), side=-110, seed=3, bells=12):
    return ext('foxglove', (x, y, 0.0), height=h, lean=list(lean), side=side, seed=seed, bells=bells,
               bell_color=FOXGLOVE)


def nightshade(x, y, h, lean, seed, berries=4, berry=0.018):
    return ext('nightshade', (x, y, 0.0), height=h, lean=list(lean), seed=seed, berries=berries, berry=berry)


def tree(x, y, seed=7):
    """A crooked tree: a twisting trunk and a few bent branches, black suede over wire."""
    rnd = random.Random(seed)
    trunk = [[0, 0, 0], [0.08, 0.02, 0.5], [-0.06, 0.05, 1.0], [0.1, 0.0, 1.5], [0.02, 0.04, 1.9], [0.18, 0.0, 2.3]]
    out = [kit('tube', 'suede', BARK, points=trunk, radius=[0.13, 0.085, 0.07, 0.055, 0.04, 0.02], position=[x, y, 0])]
    # the roots: short ropes spread on the moss
    for a in range(5):
        th = a * 2 * math.pi / 5 + rnd.uniform(-0.3, 0.3)
        out.append(kit('tube', 'suede', BARK, position=[x, y, 0],
                       points=[[0, 0, 0.18], [math.cos(th) * 0.18, math.sin(th) * 0.18, 0.05], [math.cos(th) * 0.38, math.sin(th) * 0.38, -0.02]],
                       radius=[0.06, 0.04, 0.012]))
    branches = [([0.0, 0.03, 1.05], [-0.45, 0.0, 1.45], [-0.75, 0.05, 1.4], [-1.0, 0.1, 1.62]),
                ([0.08, 0.0, 1.55], [0.45, -0.05, 1.8], [0.6, 0.0, 2.15], [0.9, 0.05, 2.2]),
                ([0.04, 0.03, 1.85], [-0.25, 0.05, 2.15], [-0.35, 0.0, 2.5]),
                ([0.12, 0.0, 0.7], [0.45, 0.02, 0.85], [0.62, 0.1, 1.12])]
    for b in branches:
        n = len(b)
        out.append(kit('tube', 'suede', BARK, points=[list(p) for p in b], position=[x, y, 0],
                       radius=[0.045 * (1 - i / n) + 0.008 for i in range(n)]))
    return out


# the ground: rolling moss, calm where the speaker stands, a bed sunk for the swamp, banks rising behind
SWAMP = (1.12, -0.8, 0.72)
GROUND = {'position': [0.0, 3.0, 0.0], 'size': [22.0, 18.0], 'res': 0.07, 'amp': 0.07, 'feature': 0.9, 'calm': [0.55, 0.45],
          'bumps': [[-2.6, 2.2, 1.6, 1.1, 0.22], [2.9, 2.6, 1.8, 1.2, 0.26], [0.3, 4.4, 3.2, 1.4, 0.3], [-3.6, 0.4, 1.2, 1.0, 0.16],
                    [4.2, 0.8, 1.3, 1.0, 0.2], [-0.8, 1.3, 0.7, 0.5, 0.06], [0.75, 1.55, 0.35, 0.28, 0.12],
                    [-4.5, 7.0, 2.6, 1.6, 1.0], [-1.2, 7.8, 2.4, 2.0, 1.3], [2.0, 7.4, 2.2, 1.8, 1.1], [5.0, 7.0, 2.8, 1.5, 0.9]],
          'dents': [[SWAMP[0], SWAMP[1], SWAMP[2] * 1.12, SWAMP[2] * 0.75, 0.09]], 'waver': 0.16, 'dent_edge': 0.15}


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


def swamp(x, y, r):
    """The swamp: glossy green resin poured into a bed in the moss (its shore where the resin meets the bank), glowing
    from its depth, glass bubbles on its skin and rising from it."""
    out = [kit('cylinder', 'resin', RESIN, radius=r * 1.4, height=0.078, position=[x, y, -0.09], scale=[1.0, 0.7, 1.0],
               roughness=0.16),
           ext('glow_pool', (x, y, -0.035), (90, 0, 0), outline=[[1.2 * r * math.cos(t / 32 * math.pi), 0.8 * r * math.sin(t / 32 * math.pi)]
                                                                for t in range(64)], r=r * 1.2, squash=0.66, emit=1.1, core=0.0,
               fade=1.0, color=GLOW)]
    rnd = random.Random(11)
    # felt lily pads and duckweed floating on it
    for (px, py, pr, turn) in [(-0.45, 0.12, 0.09, 30), (-0.3, 0.28, 0.06, 140), (0.42, 0.2, 0.075, 250), (0.55, -0.1, 0.05, 80),
                               (-0.5, -0.2, 0.055, 200), (0.1, 0.36, 0.045, 10)]:
        pad = [[pr * math.cos(t), pr * math.sin(t)] for t in [0.35 + (2 * math.pi - 0.7) * k / 30 for k in range(31)]] + [[0.0, 0.0]]
        out.append(ext('moss', (x + px * r, y + py * r * 0.66, -0.009), (90, 0, turn), color='#14261A', tint2='#1E3420',
                       outline=pad, depth=0.006, ease=0.002, sheen=0.25, **{'as': 'extrude'}))
    out.append(kit('scatter', 'felt', '#2A3E22', position=[x, y, -0.012], count=60, radius=[0.004, 0.009], seed=13,
                   **{'in': [-r * 0.6, -r * 0.4, 0.0, -r * 0.1, r * 0.35, 0.002]}))
    for i in range(7):
        th = rnd.uniform(0, 6.28); d = r * 0.55 * math.sqrt(rnd.random()); s = rnd.uniform(0.008, 0.02)
        out.append(kit('sphere', 'glass', '#E8FFF0', position=[x + d * math.cos(th), y + 0.6 * d * math.sin(th), -0.025 + s * 0.3], scale=s))
    out.append(kit('scatter', 'glass', '#E8FFF0', position=[x, y, 0.03], count=26, radius=[0.008, 0.032], seed=4,
                   plume={'height': 1.0, 'spread': [0.12, 0.45], 'lean': [0.1, 0.05], 'taper': 0.5, 'power': 1.3}))
    return out


def cushions(seed=12, n=520):
    """Cushion moss round the speaker and the swamp, kept off the resin and from under the speaker."""
    rnd = random.Random(seed); pts = []
    sx, sy, sr = SWAMP
    while len(pts) < n:
        x, y = rnd.uniform(-2.6, 3.0), rnd.uniform(-1.6, 1.6)
        if ((x - sx) / (sr * 1.15)) ** 2 + ((y - sy) / (sr * 0.77)) ** 2 < 1.0 or (abs(x) < 0.4 and abs(y) < 0.35):
            continue
        pts.append([round(x, 3), round(y, 3), round(rnd.uniform(0.02, 0.055), 3)])
    # and a thicker lip on the swamp's far bank
    for k in range(70):
        t = rnd.uniform(0, 2 * math.pi)
        rr = rnd.uniform(1.12, 1.3)
        pts.append([round(sx + sr * rr * math.cos(t), 3), round(sy + sr * 0.75 * rr * math.sin(t), 3), round(rnd.uniform(0.03, 0.07), 3)])
    return pts


def garden():
    P = [ext('terrain', GROUND['position'], **{k: v for k, v in GROUND.items() if k != 'position'}, color=MOSS, tint2=MOSS2)]
    P.append(ext('clumps', (0, 0, 0), points=cushions(), ground=GROUND, color=MOSS2, tint2='#4A6E34'))
    # the mist: a low bank torn into wisps over the moss, and a deeper haze behind the garden that the moon lights
    P.append(ext('mist', (0.0, 2.6, -0.05), size=[12.0, 6.0, 0.5], density=0.6, wisp=0.6, wisp_lo=0.48, wisp_hi=0.62,
                 color='#D8EEDD', anisotropy=0.35))
    P.append(ext('mist', (0.0, 6.0, 0.0), size=[16.0, 6.0, 3.5], density=0.12, wisp=1.6, wisp_lo=0.35, wisp_hi=0.7,
                 color='#D4E2E6', anisotropy=0.5))
    P += swamp(*SWAMP)
    G = []
    # toadstools: a tall one beside the speaker, a family in front, a black one far right
    G.append(toadstool(-0.88, 0.2, 1.05, 0.41, 0.26, 0.068, lean=(-0.06, 0.0), seed=1, spots=11, turn=20))
    G.append(toadstool(-0.62, -0.62, 0.34, 0.17, 0.11, 0.03, lean=(0.03, 0.0), seed=2, spots=6))
    G.append(toadstool(-0.5, -0.98, 0.2, 0.1, 0.07, 0.019, lean=(0.02, -0.01), seed=3, spots=5, skirt=False))
    G.append(toadstool(-1.45, -0.35, 0.55, 0.24, 0.15, 0.042, lean=(-0.05, 0.02), seed=4, spots=8, color=BLACK_CAP))
    G.append(toadstool(0.55, 0.5, 0.3, 0.14, 0.09, 0.026, lean=(0.03, 0.0), seed=5, spots=6, color=BLACK_CAP))
    G.append(toadstool(2.45, 0.9, 0.75, 0.32, 0.2, 0.05, lean=(0.05, 0.0), seed=6, spots=9))
    G.append(toadstool(0.42, 1.35, 0.22, 0.1, 0.07, 0.02, lean=(0.02, 0.0), seed=18, spots=5))
    G.append(toadstool(0.3, 1.6, 0.16, 0.075, 0.05, 0.015, lean=(-0.02, 0.0), seed=19, spots=4, skirt=False, color=BLACK_CAP))
    # foxgloves behind, left and right
    G += [foxglove(-1.75, 0.9, 1.7, (0.06, 0.0), -100, 3, 13), foxglove(-1.35, 1.35, 1.35, (-0.05, 0.02), -120, 4, 11),
          foxglove(-2.3, 1.5, 1.95, (0.08, 0.0), -100, 5, 14), foxglove(0.95, 1.1, 1.25, (0.05, 0.0), -110, 6, 10),
          foxglove(-2.0, 2.1, 1.5, (0.04, 0.0), -100, 16, 12), foxglove(1.25, 1.45, 0.95, (0.03, 0.0), -120, 17, 9),
          foxglove(-0.6, 3.6, 1.6, (0.04, 0.0), -110, 15, 12)]
    # nightshade sprigs in the moss
    G += [nightshade(-0.18, -0.72, 0.2, (0.06, -0.02), 7), nightshade(0.53, -0.36, 0.17, (-0.04, -0.05), 8, 3),
          nightshade(2.05, -0.2, 0.24, (-0.05, -0.02), 9, 5, 0.022), nightshade(-1.15, -0.9, 0.18, (0.04, -0.03), 10, 4),
          nightshade(-0.45, 1.0, 0.26, (0.04, 0.0), 20, 5, 0.02),
          nightshade(0.3, -1.8, 0.34, (-0.05, -0.03), 22, 5, 0.03)]       # a sprig near the lens, in the blur
    # the skull, half in the moss under the little toadstools, facing the camera
    G.append(ext('skull', (0.44, -0.44, 0.0), (-10, 0, -18), size=0.08))
    P += [on_ground(g, 0.012) for g in G]
    # the crooked trees behind
    P += [on_ground(t, 0.04) for t in tree(1.9, 1.75) + tree(-3.2, 4.3, seed=9)]
    # spores: a sparse glow drifting
    P.append(kit('scatter', 'glow', SPORE, emit=6.0, count=110, radius=[0.003, 0.009], seed=21, shadow=False,
                 **{'in': [-3.2, -1.6, 0.15, 3.4, 2.6, 2.4]}))
    return P


def shot(concept='A'):
    st = {'kind': 'stage', 'kit_scale': 11.0, 'props': garden()}
    moon = {**area(145, 42, 5.0, 2.0, '#DCEFE4', (1.6, 1.2), (0.0, 0.1, 0.9)), 'specular': 0.0}
    key = area(-42, 40, 5.5, 0.85, '#D2DCE0', (2.6, 2.0), (0.0, 0.0, 0.8))
    swamp_l = {**point((SWAMP[0], SWAMP[1], 0.25), 35, GLOW, 0.3), 'specular': 0.0}
    # the moon's rim on the speaker alone, so its acrylic glows above a garden left in the dark
    rim = {**area(172, 55, 4.0, 16.0, '#E2F4E8', (1.4, 1.0), (0.0, 0.1, 1.0)), 'receivers': SPEAKER}
    # the swamp's glow on the speaker's face, low from the front right: the lining lights up behind the green
    glow = {**area(48, 12, 3.0, 6.0, '#B8F5C8', (1.6, 0.8), (0.0, 0.0, 0.5)), 'receivers': SPEAKER}
    # the moon low behind the garden, lighting the haze there so the tree and the spires stand against it
    back = {**area(178, 12, 9.0, 3.0, '#C9DCE8', (6.0, 2.0), (0.0, 3.0, 0.8)), 'specular': 0.0}
    # the green the speaker throws on the moss at its feet (the light through its acrylic)
    spill = {**point((0.05, -0.5, 0.35), 14, '#5EE07A', 0.25), 'specular': 0.0}
    lights = {'spill': spill, 'back': back, 'moon': moon, 'key': key, 'swamp': swamp_l, 'rim': rim, 'glow': glow}
    cam = tilt_shift(elevation=24, azimuth=-20, distance=7.3, lens=65, target=(0.42, 0.1, 0.7), focus=(0.0, -0.25, 0.7),
                     fstop=2.8, miniature=11.0)
    sky = {'kind': 'gradient', 'zenith': '#050B07', 'horizon': '#14261A', 'ground': '#0A140D', 'strength': 0.5}
    hz = {'box_m': [-12, -12, -0.1, 12, 12, 0.28], 'density': 0.3, 'anisotropy': 0.4, 'color': '#C4DCCB'}
    return frame('poison', st, lights, cam, 'barkhorn, Poison, a poison garden', sky=sky,
                 fin=finish(bloom=0.3, bloom_px=40, threshold=0.7, saturation=0.12, lift=0.02, lift_color='#0A1A12',
                            vignette=0.25, contrast=0.14))


def portrait():
    # the 4:5 frame: the camera a little further round and higher, the speaker on the centre line, the swamp below it
    # to the right, the tree's crown above
    cam = tilt_shift(elevation=21, azimuth=-18, distance=8.0, lens=105, target=(0.22, -0.2, 0.86), focus=(0.0, -0.25, 0.7),
                     fstop=2.8, miniature=11.0)
    return portrait_of(shot(), **cam)
