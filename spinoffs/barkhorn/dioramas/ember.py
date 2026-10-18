"""Ember: the depths of hell, in fabric (round 31; BRIEF.md, ember.md for the notes).

A cavern of hanging velvet and satin in crimson, oxblood and black, its folds like rock strata; a black velvet floor with
rivers of glowing orange satin in fissures; the Ember icon's campfire cut from layered felt; embers billowing up in plumes
from the fissures; the red speaker on a velvet ledge over a bed of coals, lit through from below.
"""
import math

from common import area, finish, kit, point, spot, portrait_of, shot as frame, tilt_shift

BLACK, OXBLOOD, CRIMSON, SCARLET = '#140507', '#4A0A12', '#7E0F1C', '#A3141E'
LAVA, EMBER, GOLD = '#FF6A08', '#FF7A1A', '#FFB547'
SPEAKER = (0.2, 0.2)
RISE = 0.1                                   # the island's top, the speaker's feet: above the floor's ripples


def drape(x, y, top, w, h, color, material='velvet', rz=0.0, folds=8, amp=0.12, seed=0, noise=0.35):
    """A hanging sheet: its top edge at height `top`, centred on (x, y), turned rz about z."""
    return kit('drape', material, color, size=[w, h], position=[x, y, top], rotate=[0, 0, rz], folds=folds,
               amplitude=amp, noise=noise, seed=seed, thickness=0.01, res=120)


def strata(a, b, z0, bands, colors, step=0.1, seed=0):
    """A cliff from a to b (xy) of fabric bands laid one above the next, their folds running level like rock strata: each
    band a drape turned on its side (its width standing up), from z0 up, each stepped back `step` from the one below
    (back: to the left of a -> b)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy); rz = math.degrees(math.atan2(dy, dx)); nx, ny = -dy / L, dx / L
    out, z = [], z0
    for i, (h, col) in enumerate(zip(bands, colors)):
        mat = 'satin' if i % 3 == 1 else 'velvet'
        out.append(kit('drape', mat, col, size=[h * 1.25, L], position=[b[0] + nx * step * i, b[1] + ny * step * i, z + h / 2],
                       rotate=[0, 90, rz], folds=max(2, int(h / 0.22)), amplitude=0.06 + 0.04 * (i % 2), noise=0.5,
                       seed=seed + i, thickness=0.01, res=140))
        z += h
    return out


def plume(x, y, z, seed, height=2.6, spread=(0.12, 0.9), lean=(0.3, 0.2), count=70, r=(0.004, 0.014), emit=9.0,
          color=EMBER):
    return kit('scatter', 'glow', color, position=[x, y, z], count=count, radius=list(r), seed=seed, emit=emit,
               plume={'height': height, 'spread': list(spread), 'lean': list(lean), 'taper': 0.55, 'power': 1.4},
               shadow=False)


def fissure(points, widths, emit=1.0, lip=1.0):
    """A river of lava: glowing orange satin lying in a fissure, rolls of black and oxblood velvet along its lips."""
    # a tube's `radius` is its section's half-height and `flat` its width over that: flat > 1 lies flat
    out = [kit('tube', 'satin', LAVA, points=[[x, y, z - 0.005] for x, y, z in points], radius=[w / 8 for w in widths], flat=8, emit=emit,
                emit_color=LAVA, roughness=0.45, sides=20, res=10)]
    for side, col in ((1, BLACK), (-1, OXBLOOD)):
        pts = []
        for i, (x, y, z) in enumerate(points):
            a, b = points[max(i - 1, 0)], points[min(i + 1, len(points) - 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy)
            o = widths[i] * 0.85 + 0.04 * lip
            pts.append([x - dy / n * o * side, y + dx / n * o * side, 0.0])
        out.append(kit('tube', 'velvet', col, points=pts, radius=[(w * 0.3 + 0.035) * lip for w in widths], flat=1.7, sides=20, res=10))
    return out


# the river comes down from the back left, runs behind the campfire and the speaker (it backlights the acrylic) and
# away to the back right
RIVER = [[-2.7, 3.3, 0.0], [-2.25, 2.1, 0.0], [-1.75, 1.1, 0.0], [-0.8, 0.95, 0.0], [0.0, 1.2, 0.0], [1.1, 1.4, 0.0],
         [2.0, 2.05, 0.0], [2.7, 3.3, 0.0]]
RIVER_W = [0.14, 0.15, 0.14, 0.12, 0.13, 0.14, 0.15, 0.16]


def props():
    sx, sy = SPEAKER
    P = []
    # the floor: black velvet, rumpled, its ripples just below the speaker's feet
    P.append(kit('drape', 'velvet', '#2C050B', size=[14.0, 11.0], position=[0.0, 0.8, -0.13], orient='lay', folds=9,
                 amplitude=0.045, noise=0.7, seed=3, thickness=0.01, res=200))
    P += fissure(RIVER, RIVER_W, 0.6, lip=0.8)
    # the ledge the speaker stands on: a velvet cushion of rock, and a bed of coals at its foot
    P.append(kit('lathe', 'velvet', OXBLOOD, profile=[[0.0, 0.0], [0.42, 0.0], [0.5, -0.025], [0.56, -0.07], [0.6, -0.15]],
                 position=[sx, sy, RISE], scale=[1.0, 0.85, 1.0]))
    # a ring of coals round the speaker's feet on the ledge, felt balls, some glowing and some burnt out: they light its
    # acrylic from the bottom edge up
    for k, (dx, dy) in enumerate([(-0.34, 0.0), (0.34, 0.0), (0.0, -0.31), (0.0, 0.31)]):
        box = [-0.045, -0.24, 0.0, 0.045, 0.24, 0.015] if dx else [-0.3, -0.045, 0.0, 0.3, 0.045, 0.015]
        for seed, col, emit in ((40, '#E8500C', 0.22), (50, '#2A0A08', 0.0)):
            P.append(kit('scatter', 'felt', col, position=[sx + dx, sy + dy, RISE], rotate=[0, 0, -14], scale=[1, 1, 0.75],
                         **{'in': box}, count=8, radius=[0.018, 0.034], seed=seed + k, emit=emit, emit_color='#FF7A18', subdiv=2))
    # the walls: hanging velvet and satin, layered like strata, darker toward the back
    P += strata((-6.5, 3.3), (6.5, 3.3), -0.1, [0.55, 0.7, 0.5, 0.8, 0.6, 0.9, 0.8],
                [OXBLOOD, CRIMSON, BLACK, OXBLOOD, SCARLET, BLACK, OXBLOOD], seed=1)
    P += strata((-3.1, 1.7), (-2.3, 3.3), -0.1, [0.4, 0.6, 0.45, 0.7, 0.6, 0.8], [BLACK, CRIMSON, OXBLOOD, BLACK, CRIMSON, OXBLOOD], seed=11)
    P += strata((2.5, 3.3), (3.3, 0.6), -0.1, [0.45, 0.55, 0.7, 0.5, 0.8, 0.7], [OXBLOOD, BLACK, CRIMSON, OXBLOOD, BLACK, CRIMSON], seed=21)
    # the campfire (the icon, in layered felt) on the far bank, and the devil's toasting fork by it
    P.append(kit('ext', 'felt', SCARLET, module='ember', fn='campfire', size=0.7, position=[-1.05, 0.35, 0.0],
                 rotate=[0, 0, 10], emit=0.12, log='#2A0B09'))
    P.append(kit('ext', 'card', BLACK, module='ember', fn='fork', length=0.95, position=[-0.35, -0.05, 0.02],
                 rotate=[0, -28, 150]))
    P.append(kit('ext', 'felt', SCARLET, module='ember', fn='campfire', size=0.36, position=[2.0, 2.3, 0.0],
                 rotate=[0, 0, -12], emit=0.12))
    # stalactites: velvet cones hanging from the cavern's roof, catching the glow on their tips
    for k, (x, y, top, L, r) in enumerate([(-1.9, 2.4, 3.2, 1.3, 0.2), (-1.3, 2.9, 3.2, 0.9, 0.14), (-0.4, 2.6, 3.2, 1.4, 0.22),
                                           (0.7, 2.9, 3.2, 1.0, 0.15), (1.5, 2.3, 3.2, 1.3, 0.2), (2.3, 2.7, 3.2, 0.85, 0.14)]):
        P.append(kit('lathe', 'velvet', (OXBLOOD, CRIMSON, BLACK)[k % 3], position=[x, y, top],
                     profile=[[0.0, -L], [r * 0.25, -L * 0.93], [r * 0.6, -L * 0.6], [r * 0.9, -L * 0.25], [r, 0.0], [0.0, 0.0]]))
    # a little campfire near the lens, out of focus: the foreground's warmth
    P.append(kit('ext', 'felt', SCARLET, module='ember', fn='campfire', size=0.45, position=[1.5, -0.85, 0.0],
                 rotate=[0, 0, -20], emit=0.25))
    # a velvet boulder in the near left corner, out of focus: the near edge of the cavern
    P.append(kit('sphere', 'velvet', OXBLOOD, position=[-2.0, -1.7, -0.12], scale=[0.75, 0.55, 0.42], rotate=[0, 0, 20]))
    # embers billowing up from the fissures and the coals, drifting right
    P += [plume(-1.75, 1.1, 0.02, 11, count=45, spread=(0.08, 0.6), lean=(-0.6, 0.3)),
          plume(-2.0, 2.4, 0.02, 13, height=3.0, count=60, lean=(0.3, 0.3)), plume(1.6, 1.6, 0.02, 14, count=50, lean=(0.7, 0.2)),
          plume(-1.05, 0.35, 0.55, 15, height=1.8, spread=(0.05, 0.5), count=40, lean=(0.2, 0.2)),
          plume(sx + 0.75, sy - 0.4, 0.03, 16, height=2.4, spread=(0.1, 0.6), count=35, lean=(0.9, 0.4))]
    for seed, box in ((21, [-2.4, -3.4, 0.4, -1.5, -2.6, 2.0]), (22, [1.2, -3.4, 0.4, 2.2, -2.6, 2.0])):
        P.append(kit('scatter', 'glow', EMBER, position=[0, 0, 0], **{'in': box}, count=3, radius=[0.008, 0.014],
                     seed=seed, emit=15.0, shadow=False))
    return P


def lights():
    sx, sy = SPEAKER
    L = {}
    for i, (x, y, w) in enumerate([(-2.2, 2.1, 40), (-1.6, 1.1, 45), (-0.8, 0.95, 35),
                                   (0.1, 1.25, 40), (1.5, 1.6, 40), (2.6, 2.3, 40)]):
        L[f'lava{i}'] = point([x, y, 0.12], w * 0.7, '#FF7A28', 0.08)
    L['fire'] = point([-1.05, 0.7, 0.3], 25, '#FF7A28', 0.1)
    L['hearth'] = point([-0.95, 0.05, 0.14], 6, '#FF8A30', 0.06)          # the campfire's glow on its own log
    L['glow'] = spot([sx - 0.9, sy - 2.6, 0.15], [sx, sy, 1.1], 260, 9.0, 0.6, '#FF6A24', 0.2)   # the coals' glow up the horn
    L['back'] = point([sx + 0.2, sy + 0.95, 0.5], 60, '#FF4A14', 0.15)        # the river behind
    L['horn'] = spot([sx + 0.15, sy + 0.75, 0.55], [sx, sy - 0.1, 1.15], 120, 30.0, 0.7, '#FF6A24', 0.1)   # up through the horn
    for k, (dx, dy) in enumerate([(-0.36, 0.0), (0.36, 0.0), (0.0, -0.33), (0.0, 0.33)]):   # the ring's light
        L[f'edge{k}'] = point([sx + dx * 1.1, sy + dy * 1.1, RISE + 0.07], 10, '#FF7A28', 0.09)
    L['top'] = area(-20, 70, 6.0, 0.05, '#9A2A3A', (3.0, 3.0))
    return L


def shot():
    st = {'kind': 'stage', 'kit_scale': 11.0, 'props': props()}
    cam = tilt_shift(elevation=19, azimuth=-16, distance=6.1, lens=50, target=(0.15, 0.4, 0.72), focus=(0.15, -0.05, 0.7),
                     miniature=11.0)
    return frame('ember', st, lights(), cam, 'barkhorn, Ember, the depths of hell in fabric', sky={'kind': 'none'},
                 position=(*SPEAKER, RISE), exposure=0.0,
                 fin=finish(bloom=0.35, bloom_px=46, threshold=0.7, saturation=0.15, lift=0.025, lift_color='#36060F',
                            vignette=0.25))


def portrait():
    cam = tilt_shift(elevation=17, azimuth=-12, distance=5.0, lens=58, target=(0.0, 0.4, 0.75), focus=(0.15, -0.05, 0.7),
                     miniature=11.0, shift_y=0.1)
    return portrait_of(shot(), **cam)
