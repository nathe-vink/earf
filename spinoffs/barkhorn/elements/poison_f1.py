"""Poison, F1 (round 31h): a European poison wood in autumn, every poison native to the same beech wood.

The owner, 2026-10-20: "For poison, the algae idea is too goofy. What other poisonous plants or animals are there?
You could combine a lot of them into a forest or rainforest biome, alongside the red caps." With the earlier notes:
no purple plants (the foxgloves "look fake"), and shrooms or a snake to read as poison.

Built on A4 (poison_a4.py: its light, its floor, its ferns, the speaker's contact with the duff, its troop of fly
agarics), moved to an autumn beech wood: the photographed wood behind (Poly Haven's autumn_forest_01, beech in
autumn over golden litter and mossy boulders), beech litter underfoot (leaves_forest_ground), smooth grey beech bark
on the trunks (chinese_hackberry_bark). The poisons, all in season together in a European autumn wood:
- fly agarics, a bigger troop than A4's, every age, near the lens;
- death caps (Amanita phalloides), olive, at the foot of the beech;
- lords-and-ladies (Arum maculatum) in berry: bare stalks with clubs of glossy orange-red berries;
- deadly nightshade (Atropa belladonna) sprigs with glossy black berries.
No animals: no CC0 scan of an adder or a fire salamander exists (Poly Haven, ambientCG, Smithsonian 3D searched
2026-10-20), and modelled snakes read as toys (poison_a2.md).
"""
import copy

import poison as A
import poison_a4 as A4
from common import piece, portrait_of, sky

HDRI, ROT = 'autumn_forest_01', 180.0
BEECH = '#8A8B82'                   # the bark's smooth grey

# (x, y, cap radius, age, seed, extra): A4's troop at the left, more caps round it, and a second group at the right
AGARICS2 = [(0.55, -1.55, 0.065, 'plane', 71, dict(lean=[0.01, 0.0], wash=0.05, dull=0.36, torn=0.15, matte=True, orange=True)),
            (0.72, -1.48, 0.04, 'young', 72, dict(lean=[-0.01, 0.0], wash=0.15, dull=0.34, matte=True, orange=True)),
            (0.66, -1.72, 0.022, 'button', 73, dict(warts=260, dull=0.3, matte=True)),
            (-0.62, -1.18, 0.08, 'old', 74, dict(lean=[-0.02, 0.0], wash=0.0, dull=0.46, torn=0.5, matte=True, orange=True)),
            (-0.5, -1.55, 0.05, 'convex', 75, dict(lean=[0.01, -0.01], wash=0.1, dull=0.36, matte=True, orange=True))]
DEATHCAPS = [(-1.05, -0.55, 0.055, 'convex', 81), (-1.2, -0.42, 0.04, 'young', 82), (-0.95, -0.35, 0.03, 'button', 83)]
ARUMS = [(1.15, -0.85, 0.32, 41, [0.02, -0.01]), (1.27, -0.78, 0.26, 42, [-0.015, 0.01]), (1.08, -0.7, 0.22, 43, [0.0, 0.02])]
NIGHTSHADE = [(-1.35, -0.9, 0.42, 51), (-1.5, -0.75, 0.36, 52)]


def extp(fn, position=(0, 0, 0), **k):
    return piece('ext', module='poison_p_el', fn=fn, position=list(position), **k)


def shot():
    s = copy.deepcopy(A4.shot())
    props = s['set']['props']
    props[:] = [p for p in props if p.get('fn') != 'foxglove']           # no purple: the owner's note
    for p in props:
        if p.get('texture') == 'forest_leaves_02':                         # beech litter underfoot
            p['texture'] = 'leaves_forest_ground'; p['tint'] = '#4A3420'; p['tint_mix'] = 0.1
        if p.get('fn') == 'redwood':                                        # beech, not redwood: smooth grey, no buttress
            p['bark'] = 'chinese_hackberry_bark'; p['tint'] = BEECH; p['tint_mix'] = 0.35
            p['radius'] = round(p['radius'] * 0.42, 3); p['flare'] = 0.25; p['foot'] = 0.6; p['tex_scale'] = 1.0
        if p.get('fn') == 'plants' and p.get('model') == 'fern_02':           # a beech wood's floor is open: half the ferns
            p['place'] = p['place'][::2]
    for p in props:                                                         # scarlet, as a fly agaric is: A4 dulled them so
        if p.get('fn') == 'amanita':                                        # they would not out-shout the speaker
            p['dull'] = min(p.get('dull', 0.0), 0.2)
    for x, y, R, age, sd, more in AGARICS2:
        more = dict(more); z = more.pop('z', -0.045 if age != 'button' else -0.02)
        more['dull'] = 0.2
        props.append(A4.extb('amanita', (x, y, z), cap=R, age=age, seed=sd, **more))
    for x, y, R, age, sd in DEATHCAPS:
        props.append(A4.extb('amanita', (x, y, -0.04 if age != 'button' else -0.02), species='phalloides', cap=R, age=age,
                             seed=sd, dull=0.3, matte=True))
    for x, y, H, sd, lean in ARUMS:
        props.append(extp('arum', (x, y, -0.01), height=H, seed=sd, lean=lean, berries=44))
    for x, y, H, sd in NIGHTSHADE:
        props.append(A4.extb('nightshade', (x, y, -0.01), height=H, seed=sd, berries=7))
    s['sky'] = sky(HDRI, ROT, strength=0.3, res='4k')
    s['title'] = 'barkhorn, Poison F1, a European poison wood in autumn'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['sky'], p['title'] = s['set'], s['sun'], s['lights'], s['sky'], s['title'] + ' (4:5)'
    return p
