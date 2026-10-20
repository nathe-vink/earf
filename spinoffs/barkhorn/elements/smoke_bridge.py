"""Smoke, setting E7: the aftermath on a bridge (the owner, 2026-10-20: "an apocalyptic or riot scene, with cars crashed
and burning on a bridge, billowing black smoke, with the speaker in the foreground").

A concrete highway bridge at blue hour, wet asphalt and lane markings receding between Jersey barriers. Fifteen to twenty-five
metres back, three cars sit crashed at angles across the lanes; two burn inside, and their thick black smoke billows up
and drifts left across the frame, lit orange from within. Firelight lies in the wet road; a few embers rise. The speaker
stands untouched on the deck in the foreground, crisp and lit, the fire behind it. An empty aftermath: no people.
The cars are simple, well-proportioned forms, mostly in silhouette inside the smoke and against the fire.
"""
import math

from common import area, asset, camera, finish, ground, piece, point, shot as frame, portrait_of, sky
from smoke import SHELL, SPEAKER

SKY = 'highway_bridge_sunset'               # a freeway bridge at blue hour (Poly Haven, CC0)
SOOT = '#151515'
# the cars: (x, y, heading in degrees, paint, burning)
CARS = [(-0.6, 15.0, 35.0, '#1A1B1D', True), (4.4, 19.5, -60.0, '#222427', False), (2.2, 26.0, 15.0, '#151617', True)]
SEDAN = [[-2.32, 0.32], [-2.34, 0.72], [-2.05, 0.9], [-1.05, 0.98], [-0.45, 1.4], [0.75, 1.44], [1.35, 1.0],
         [2.2, 0.9], [2.33, 0.62], [2.3, 0.32]]


def car(x, y, heading, paint, burning):
    """A sedan's simple form: its body extruded from a side profile, four wheels, dark glass; a burning one charred."""
    h = math.radians(heading)
    body = '#141210' if burning else paint
    out = [piece('extrude', outline=SEDAN, depth=1.8, position=[x, y, 0.0], rotate=[0.0, 0.0, heading + 90.0],
                 material='gloss' if not burning else 'clay', color=body, ease=0.06)]
    for dx in (-1.45, 1.45):
        for dy in (-0.82, 0.82):
            wx = x + dx * math.cos(h + math.pi / 2) - dy * math.sin(h + math.pi / 2)
            wy = y + dx * math.sin(h + math.pi / 2) + dy * math.cos(h + math.pi / 2)
            out.append(piece('cylinder', radius=0.33, height=0.22, position=[wx, wy, 0.33], rotate=[90.0, 0.0, heading],
                             material='clay', color='#0E0E0E'))
    return out


def fire(x, y, heading, seed):
    """The fire inside a burning car: hot cores deep in its cabin, seen through the smoke rather than as flames drawn
    in the open, and a few embers lifting off it."""
    out = []
    for k, (dx, dz, r) in enumerate([(-0.5, 0.65, 0.25), (0.3, 0.75, 0.32), (1.1, 0.6, 0.22)]):
        h = math.radians(heading + 90.0)
        out.append(piece('sphere', position=[x + dx * math.cos(h), y + dx * math.sin(h), dz], scale=r, material='glow',
                         color='#FF6A1A', emit=18.0))
    out.append(piece('scatter', count=40, radius=[0.006, 0.016], position=[x, y, 1.4], material='glow', color='#FF8A30',
                     emit=30.0, seed=seed, plume={'height': 5.0, 'spread': [0.4, 2.0], 'lean': [-2.0, 0.5], 'taper': 0.7}))
    return out


def smoke_column(x, y, seed):
    """Thick black smoke out of a burning car: dense and low over the fire, billowing up and drifting left."""
    out = []
    for k in range(7):
        t = k / 6
        w = 3.0 + 11.0 * t ** 1.2
        out.append(piece('ext', module='smoke_el', fn='woodsmoke', position=[x - 9.0 * t ** 1.5, y + 2.0 * t, 0.6 + 2.6 * k],
                         size=[w, w, 3.4], density=4.5 * 0.78 ** k, seed=seed + k, scale=0.9 + 1.6 * t, cut=0.42, soft=0.3,
                         anisotropy=0.3, fade=[0.35, 0.35, 0.4], floor=0.0, rise=1.5, color=SOOT, detail_scale=0.3 + 0.4 * t,
                         detail_weight=0.5))
    return out


def deck():
    """The bridge: wet asphalt, lane markings, Jersey barriers each side and a steel railing beyond the right one."""
    out = [ground('asphalt_02', size=(14.0, 90.0), position=(0.0, 35.0, 0.0), displace=0.004, relief=False, res='2k',
                  tint='#2E2E30', tint_mix=0.3, rough_mul=0.35)]
    for k in range(10):
        y = -4.0 + 9.0 * k
        for x in (-1.85, 1.85):
            out.append(piece('box', size=[0.14, 3.0, 0.004], position=[x, y, 0.0], material='clay', color='#CFCDC6'))
    # Jersey barriers each side: the classic profile, cast concrete, one long run
    jersey = [[-0.3, 0.0], [0.3, 0.0], [0.3, 0.08], [0.1, 0.3], [0.08, 0.81], [-0.08, 0.81], [-0.1, 0.3], [-0.3, 0.08]]
    for x in (-6.2, 6.2):
        out.append(piece('extrude', outline=jersey, depth=90.0, position=[x, 39.0, 0.0], material='pbr',
                         texture='concrete_wall_008', tex_scale=2.0, tint='#8C8A86', tint_mix=0.3, ease=0.01))
    for k in range(30):
        out.append(piece('box', size=[0.08, 0.08, 1.2], position=[6.9, -6.0 + 3.0 * k, 0.0], material='foil',
                         color='#55585C', roughness=0.5))
    out.append(piece('box', size=[0.06, 90.0, 0.1], position=[6.9, 39.0, 1.15], material='foil', color='#55585C',
                     roughness=0.5))
    return out


def shot():
    props = deck()
    lights = {
        'skyfill': {**area(-20, 5, 2.4, 1.6, '#AEB8C8', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 4.0, '#C9BBA8', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 30.0, '#FF9A50', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 22.0, '#FF9A50', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
    }
    for i, (x, y, heading, paint, burning) in enumerate(CARS):
        props += car(x, y, heading, paint, burning)
        if burning:
            props += fire(x, y, heading, 50 + i) + smoke_column(x, y, 60 + 10 * i)
            lights[f'fire{i}'] = point([x, y, 1.4], 6000.0, '#FF7A28', 0.8)
    # the smoke pooled low round the wrecks, so they sit in it as silhouettes
    props.append(piece('ext', module='smoke_el', fn='woodsmoke', position=[1.5, 21.0, -0.2], size=[16.0, 16.0, 3.0],
                       density=0.9, seed=77, scale=1.2, cut=0.45, soft=0.3, anisotropy=0.3, fade=[0.3, 0.3, 0.5], floor=0.05,
                       rise=1.2, color=SOOT, detail_scale=0.3, detail_weight=0.5))
    cam = camera(height=0.9, distance=5.0, azimuth=-12, lens=40, target=(0.0, 0.0, 0.85), fstop=4.0, shift_x=0.0,
                 shift_y=0.1)
    return frame('smoke_bridge', props, cam, sky(SKY, rotation_deg=0.0, strength=0.35),
                 'barkhorn, Smoke, the aftermath on a bridge', lights=lights, rotate_z=18.0, position=(0.0, 0.0, 0.0),
                 samples=512, exposure=0.0,
                 fin=finish(contrast=0.06, clarity=0.04, bloom=0.06, bloom_px=40, threshold=0.85, vignette=0.25))


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=0.9, distance=4.2, azimuth=-12, lens=40, target=(0.0, 0.0, 0.85), fstop=4.0,
                                    shift_y=0.12))
