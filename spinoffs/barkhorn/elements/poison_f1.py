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
AGARICS2 = [(0.62, -1.62, 0.095, 'plane', 71, dict(lean=[0.02, 0.0], wash=0.05, torn=0.15, height=0.17)),
            (0.82, -1.38, 0.06, 'convex', 72, dict(lean=[-0.01, 0.01], wash=0.1, height=0.13)),
            (0.5, -1.95, 0.03, 'button', 73, dict(warts=260)),
            (-0.7, -1.02, 0.1, 'old', 74, dict(lean=[-0.03, 0.0], wash=0.0, torn=0.5, height=0.19)),
            (-0.48, -1.72, 0.07, 'convex', 75, dict(lean=[0.01, -0.02], wash=0.08, height=0.15)),
            (-0.95, -1.5, 0.05, 'young', 76, dict(lean=[0.0, 0.01], wash=0.12)),
            (0.25, -2.05, 0.085, 'convex', 77, dict(lean=[0.02, -0.01], wash=0.06, height=0.16))]
DEATHCAPS = [(-1.05, -0.55, 0.055, 'convex', 81), (-1.2, -0.42, 0.04, 'young', 82), (-0.95, -0.35, 0.03, 'button', 83)]
ARUMS = [(0.98, -1.65, 0.34, 41, [0.02, -0.01]), (1.1, -1.58, 0.28, 42, [-0.015, 0.01]), (0.9, -1.5, 0.24, 43, [0.0, 0.02]),
         (1.2, -0.85, 0.3, 44, [0.01, 0.0])]
NIGHTSHADE = [(-0.95, -1.75, 0.38, 51), (-1.1, -1.62, 0.32, 52)]


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
    for x, y, R, age, sd, more in AGARICS2:
        more = dict(more); z = more.pop('z', -0.045 if age != 'button' else -0.02)
        props.append(A4.extb('amanita', (x, y, z), cap=R, age=age, seed=sd, **more))
    for x, y, R, age, sd in DEATHCAPS:
        props.append(A4.extb('amanita', (x, y, -0.04 if age != 'button' else -0.02), species='phalloides', cap=R, age=age,
                             seed=sd, dull=0.3, matte=True))
    for x, y, H, sd, lean in ARUMS:
        props.append(extp('arum', (x, y, -0.01), height=H, seed=sd, lean=lean, berries=48, berry=0.0055))
    for x, y, H, sd in NIGHTSHADE:
        props.append(A4.extb('nightshade', (x, y, -0.01), height=H, seed=sd, berries=9, berry=0.0085))
    for p in props:
        if p.get('fn') == 'amanita' and p.get('species', 'muscaria') == 'muscaria' and p['position'][1] > -1.5:
            p['cap'] = round(p['cap'] * 1.35, 3)                              # a bold troop: mature caps 15-20 cm across
    for p in props:                                                         # scarlet and viscid, as a fresh fly agaric is: A4
        if p.get('fn') == 'amanita' and p.get('species', 'muscaria') == 'muscaria':   # dulled and dried them (matte) so they
            p['dull'] = 0.0 if p.get('age') != 'old' else 0.15              # would not out-shout the speaker, and at 600 px
            p['matte'] = False; p['orange'] = False                         # they read as pink 'toadstools'
            p['wash'] = min(p.get('wash', 0.15), 0.08)
    s['sky'] = sky(HDRI, ROT, strength=0.3, res='4k')
    s['title'] = 'barkhorn, Poison F1, a European poison wood in autumn'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['sky'], p['title'] = s['set'], s['sun'], s['lights'], s['sky'], s['title'] + ' (4:5)'
    return p
