"""Poison, P1 (round 31f): the poison cabinet of a Victorian pharmacy, after closing.

The owner, 2026-10-20: "poison's still doesn't communicate poison to me. The purple plants also look fake relative to
everything else." So no plants: glass, which is where the renders are strongest, and Poison's own bottle green. A dark
pharmacy, walnut and brass, worn boards; behind the speaker a wall of antique poison bottles, ribbed and hexagonal, in
bottle green and cobalt, with POISON labels, a skull and crossbones and NOT TO BE TAKEN, a few stoppers out; a brass
scale and an oil lamp on the counter. The speaker stands on the boards among them, its green echoing the bottles.
Lit warm and low by the lamp, with a cold glow from the street at the left.

Scanned (Poly Haven, CC0): vintage_cabinet_01 (the glazed dresser), vintage_oil_lamp, old_wood_floor, dark_paneled_wood,
plastered_wall_04. Modelled here (kit_ext/poison_p_el.py): the bottles and their labels, the shelves, the scale.
"""
import random

from common import area, asset, camera, finish, piece, point, portrait_of, shot as frame, sky

GREEN, COBALT, AMBER, CLEAR = '#3E9A55', '#3D63D0', '#B8742E', '#DDE6DA'
VLABELS = ['v-arsenic', 'v-laudanum', 'v-strychnine', 'v-belladonna', 'v-cyanide', 'v-oxalic', 'v-sublimate', 'v-aconite']
BACK_Y = 1.6                       # the back wall
WALL_X = (-3.2, 3.2)


def ext(fn, position=(0, 0, 0), **k):
    return piece('ext', module='poison_p_el', fn=fn, position=list(position), **k)


def shelf_row(rnd, x0, x1, z, depth_y, n, sizes=(0.13, 0.24), labels=0.7, out=0.12):
    """A shelf's row of bottles from x0 to x1 at height z: mostly green and cobalt poison bottles, hex and ribbed, a
    few clear and amber; most labelled; a few stoppers out."""
    items = []
    xs = sorted(rnd.uniform(x0, x1) for _ in range(n))
    x = x0
    for _ in range(n):
        H = rnd.uniform(*sizes)
        kind = rnd.choices(['hex', 'ribbed', 'round'], [0.5, 0.3, 0.2])[0]
        col = rnd.choices([GREEN, COBALT, AMBER, CLEAR], [0.45, 0.3, 0.15, 0.1])[0]
        R = H * 0.22
        x += R + rnd.uniform(0.008, 0.03)
        if x + R > x1:
            break
        lab = rnd.choice(VLABELS) if rnd.random() < labels else None
        st = 'out' if rnd.random() < out else rnd.choice(['cork', 'glass', 'cork'])
        items.append([round(x, 3), round(depth_y + rnd.uniform(-0.02, 0.02), 3), z, kind, col, round(H, 3), lab, st,
                      round(rnd.uniform(0.3, 0.8), 2) if col in (CLEAR, GREEN) and rnd.random() < 0.6 else None])
        x += R
    return items


def shot():
    rnd = random.Random(31)
    props = [
        # the room: worn boards, walnut panelling to dado height, old plaster above, a dark ceiling
        piece('box', size=[6.4, 4.6, 0.04], position=[0.0, -0.7, -0.04], material='pbr', texture='old_wood_floor',
              tex_scale=2.6, tint='#3A2414', tint_mix=0.3),
        piece('box', size=[6.4, 0.06, 1.05], position=[0.0, BACK_Y + 0.03, 0.0], material='pbr', texture='dark_paneled_wood',
              tex_scale=1.0, tint='#2A170C', tint_mix=0.3),
        piece('box', size=[6.4, 0.06, 2.6], position=[0.0, BACK_Y + 0.06, 1.05], material='pbr', texture='plastered_wall_04',
              tex_scale=2.0, tint='#1C140C', tint_mix=0.82),
        piece('box', size=[0.06, 4.6, 3.6], position=[WALL_X[0], -0.7, 0.0], material='pbr', texture='plastered_wall_04',
              tex_scale=2.0, tint='#1C140C', tint_mix=0.8),
        piece('box', size=[0.06, 4.6, 3.6], position=[WALL_X[1], -0.7, 0.0], material='pbr', texture='plastered_wall_04',
              tex_scale=2.0, tint='#1C140C', tint_mix=0.8),
        piece('box', size=[6.4, 4.6, 0.05], position=[0.0, -0.7, 3.4], material='card', color='#1A120C'),
        # the poison wall behind the speaker: deep walnut shelves, five rows of bottles
        ext('shelves', [0.35, BACK_Y - 0.17, 0.0], size=[2.9, 0.3, 3.3], rows=[0.0, 0.62, 1.0, 1.36, 1.72, 2.08, 2.44, 2.8, 3.27], board=0.03,
            uprights=[-0.48, 0.48], texture='dark_wood', tex_scale=1.0, tint='#2E1A0C', tint_mix=0.4, lip=True),
        asset('vintage_cabinet_01', (-2.05, BACK_Y - 0.36, 0.0), rotate=(0, 0, 0), scale=1.0),
    ]
    rows = []
    for z, sizes, n in ((0.625, (0.22, 0.32), 26), (1.005, (0.2, 0.3), 26), (1.365, (0.17, 0.27), 30),
                        (1.725, (0.15, 0.24), 32), (2.085, (0.13, 0.2), 34), (2.445, (0.13, 0.2), 34), (2.805, (0.12, 0.19), 36)):
        rows += shelf_row(rnd, -1.05, 1.75, z, BACK_Y - 0.24, n, sizes, labels=0.85)
    props.append(ext('bottles', items=rows, seed=31))
    # the counter at the right: a walnut slab, the brass scale, the oil lamp, a few bottles and a ledger
    props += [piece('box', size=[1.3, 0.55, 0.86], position=[1.95, 0.35, 0.0], material='pbr', texture='dark_paneled_wood',
                    tex_scale=1.2, tint='#2A170C', tint_mix=0.35),
              piece('box', size=[1.38, 0.62, 0.045], position=[1.95, 0.35, 0.86], material='pbr', texture='dark_wood',
                    tex_scale=1.0, tint='#2A170C', tint_mix=0.3),
              ext('scale', [1.65, 0.3, 0.905], size=0.36, rotate=[0, 0, -15]),
              asset('vintage_oil_lamp', (2.3, 0.45, 0.905), rotate=(0, 0, 30), scale=0.85),
              ext('bottles', [1.85, 0.28, 0.905], items=[[0.18, -0.08, 0, 'hex', GREEN, 0.2, 'v-arsenic', 'out', None],
                                                        [0.33, 0.04, 0, 'ribbed', COBALT, 0.17, 'v-strychnine', 'cork', None]], seed=4),
              piece('box', size=[0.24, 0.32, 0.03], position=[1.35, 0.25, 0.905], material='card', color='#3A1E12',
                    rotate=[0, 0, 12])]
    # at the speaker's feet: a crate of bottles, one on the boards
    props += [ext('bottles', [0.62, -0.75, 0.0], items=[[0, 0, 0, 'hex', GREEN, 0.34, 'v-arsenic', 'cork', 0.55],
                                                        [0.2, 0.1, 0, 'hex', COBALT, 0.27, 'v-cyanide', 'glass', None],
                                                        [0.1, -0.16, 0, 'ribbed', GREEN, 0.2, 'v-strychnine', 'out', None]], seed=5)]
    # the light: the oil lamp (warm, low, the key), a cold street glow through the left (a window off frame), a soft
    # warm fill from the camera side so the speaker's face opens, a rim from behind-right
    lights = {'lamp': point((2.3, 0.45, 1.35), 220.0, '#FFB060', 0.04),
              'street': {**area(-80, 25, 3.0, 2.0, '#9AB4D8', (1.2, 2.0), (0.0, 0.3, 1.0)), 'specular': 0.6},
              'fill': {**area(-15, 15, 3.5, 1.2, '#FFD8A8', (2.0, 1.4), (-0.35, -0.2, 0.7)), 'specular': 0.0},
              'rim': {**area(150, 30, 2.0, 0.8, '#FFC080', (0.6, 1.6), (0.0, 0.0, 1.0)), 'specular': 0.4},
              'shelf': {**area(25, 35, 2.4, 1.6, '#FFC890', (2.4, 0.6), (0.25, BACK_Y - 0.2, 1.4)), 'specular': 0.5},
              'glow': point((0.25, BACK_Y - 0.08, 1.2), 40.0, '#FFB070', 0.3)}
    cam = camera(height=0.9, distance=4.5, azimuth=8.0, lens=38.0, target=(0.3, 0.1, 1.05), fstop=5.6)
    return frame('poison', props, cam, sky('abandoned_workshop', rotation_deg=0.0, strength=0.05, res='2k'),
                 'barkhorn, Poison P1, the poison cabinet', lights=lights, rotate_z=-16.0, position=(-0.25, -0.35, 0.0),
                 fin=finish(contrast=0.08, clarity=0.06, vignette=0.18))


def portrait():
    return portrait_of(shot(), **camera(height=0.85, distance=4.6, azimuth=12.0, lens=45.0, target=(0.1, 0.3, 1.0), fstop=4.0))
