"""Poison, P2 (round 31f): a chemist's poison store, now.

The owner, 2026-10-20: "poison's still doesn't communicate poison to me. The purple plants also look fake relative to
everything else." The modern take on P1: a concrete store room, steel racks of amber and green chemical bottles with
GHS skull pictograms, DANGER and their UN numbers, hazard tape on the floor, a fume cupboard glowing faintly at the far
end under cold strip light. The speaker stands in the aisle.

Scanned (Poly Haven, CC0): worn_metal_rack, chemistry_set, concrete_floor_worn_001, concrete_block_wall. Modelled here
(kit_ext/poison_p_el.py): the bottles and their labels, the racks, the tape.
"""
import random

from common import area, asset, camera, finish, piece, point, portrait_of, shot as frame, sky

AMBER, GREEN, BROWN, CLEAR = '#B8742E', '#3E9A55', '#6A3A10', '#DDE6DA'
GLABELS = ['g-cyanide', 'g-arsenic', 'g-mercury', 'g-paraquat', 'g-thallium', 'g-strychnine']
RACK_X = 1.05                     # the racks' fronts either side of the aisle
ROWS = [0.12, 0.62, 1.12, 1.62]   # shelf heights


def ext(fn, position=(0, 0, 0), **k):
    return piece('ext', module='poison_p_el', fn=fn, position=list(position), **k)


def rack_row(rnd, y0, y1, z, x, n, side):
    """A shelf's row of chemical bottles along y (the aisle), at height z, their labels turned to the aisle."""
    items = []
    y = y0
    for _ in range(n):
        H = rnd.uniform(0.2, 0.34)
        kind = rnd.choice(['square', 'square', 'round'])
        col = rnd.choices([AMBER, BROWN, GREEN, CLEAR], [0.45, 0.2, 0.25, 0.1])[0]
        R = H * 0.24
        y += R + rnd.uniform(0.01, 0.04)
        if y + R > y1:
            break
        items.append([round(x + rnd.uniform(-0.03, 0.03), 3), round(y, 3), z, kind, col, round(H, 3),
                      rnd.choice(GLABELS) if rnd.random() < 0.9 else None, 'cap', round(rnd.uniform(0.3, 0.85), 2),
                      65.0 if side < 0 else -65.0])                 # the label to the aisle, a little toward the lens
        y += R
    return items


def shot():
    rnd = random.Random(32)
    props = [
        piece('box', size=[5.0, 9.0, 0.04], position=[0.0, 2.5, -0.04], material='pbr', texture='concrete_floor_worn_001',
              tex_scale=2.0),
        piece('box', size=[0.1, 9.0, 3.2], position=[-2.0, 2.5, 0.0], material='pbr', texture='concrete_block_wall',
              tex_scale=1.0, tint='#6A6C68', tint_mix=0.3),
        piece('box', size=[0.1, 9.0, 3.2], position=[2.0, 2.5, 0.0], material='pbr', texture='concrete_block_wall',
              tex_scale=1.0, tint='#6A6C68', tint_mix=0.3),
        piece('box', size=[4.0, 0.1, 3.2], position=[0.0, 6.6, 0.0], material='pbr', texture='concrete_block_wall',
              tex_scale=1.0, tint='#6A6C68', tint_mix=0.3),
        piece('box', size=[5.0, 9.0, 0.05], position=[0.0, 2.5, 3.0], material='card', color='#2A2C2C'),
    ]
    # the racks, green steel, either side of the aisle, and the scanned one at the far end
    for sx in (-1, 1):
        props.append(ext('shelves', [sx * (RACK_X + 0.3), 2.0, 0.0], rotate=[0, 0, 90], size=[6.0, 0.6, 1.95],
                         rows=[z - 0.02 for z in ROWS] + [1.93], uprights=[-2.0, -1.0, 0.0, 1.0, 2.0], board=0.02,
                         back=False, color='#3E4A38', roughness=0.55, metal=0.35))
    props.append(asset('worn_metal_rack', (-0.9, 6.15, 0.0), rotate=(0, 0, 0), scale=1.0))
    items = []
    for sx in (-1, 1):
        for z in ROWS:
            items += rack_row(rnd, -0.9, 4.9, z + 0.005, sx * (RACK_X + 0.12), 30, sx)
    props.append(ext('bottles', items=items, seed=32))
    # the fume cupboard at the far right: a steel body, a glass sash, a cold light inside
    props += [piece('box', size=[1.2, 0.75, 0.9], position=[0.95, 6.15, 0.0], material='card', color='#C8CCCC'),
              piece('box', size=[1.2, 0.75, 1.2], position=[0.95, 6.15, 0.9], material='card', color='#B8BCBC'),
              piece('box', size=[1.0, 0.02, 0.9], position=[0.95, 5.76, 1.0], material='glass', color='#E6F0F0'),
              asset('chemistry_set', (0.95, 6.2, 0.9), rotate=(0, 0, 180), scale=0.9)]
    # hazard tape along both sides of the aisle, and across it in front of the fume cupboard
    props += [ext('tape', [-0.72, -1.2, 0.002], length=7.0, width=0.06, angle=90),
              ext('tape', [0.72, -1.2, 0.002], length=7.0, width=0.06, angle=90),
              ext('tape', [-0.72, 5.4, 0.002], length=1.44, width=0.06, angle=0)]
    # the light: cold strips overhead down the aisle, the fume cupboard's glow, a soft fill from the camera
    lights = {f'strip{k}': {**area(0, 90, 0.1, 6.0, '#DDE8F0', (0.12, 1.4), (0.0, y, 0.0), centre=(0.0, y, 2.85)), 'specular': 0.6}
              for k, y in enumerate((-1.6, 0.6, 2.8, 5.0))}
    lights.update({'fume': point((0.95, 6.15, 1.45), 60.0, '#CFE6F0', 0.3),
                   'fill': {**area(-10, 12, 3.5, 2.2, '#E6EEF2', (2.0, 1.4), (0.0, 0.0, 0.7)), 'specular': 0.0},
                   'key': {**area(-30, 25, 2.6, 1.6, '#E8F0F4', (1.0, 1.4), (0.0, 0.0, 0.8)), 'specular': 0.2}})
    cam = camera(height=0.95, distance=3.8, azimuth=0.0, lens=32.0, target=(0.0, 0.6, 1.0), fstop=5.6)
    return frame('poison', props, cam, sky('abandoned_workshop', rotation_deg=0.0, strength=0.05, res='2k'),
                 'barkhorn, Poison P2, the poison store', lights=lights, rotate_z=-18.0, position=(0.0, 0.0, 0.0),
                 fin=finish(contrast=0.08, clarity=0.06, vignette=0.15))


def portrait():
    return portrait_of(shot(), **camera(height=0.95, distance=4.0, azimuth=0.0, lens=38.0, target=(0.0, 0.6, 1.05), fstop=5.6))
