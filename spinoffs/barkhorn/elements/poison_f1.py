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
# no 'plane' caps (proof 3's critics: "flat, table-like"): domed, every age, uneven heights, a couple leaning hard
AGARICS2 = [(0.62, -1.62, 0.085, 'convex', 71, dict(lean=[0.035, 0.0], wash=0.05, torn=0.15, height=0.14)),
            (0.82, -1.38, 0.055, 'young', 72, dict(lean=[-0.02, 0.01], wash=0.12, height=0.11)),
            (0.5, -1.95, 0.03, 'button', 73, dict(warts=260)),
            (-0.7, -1.02, 0.09, 'old', 74, dict(lean=[-0.04, 0.0], wash=0.0, torn=0.55, height=0.16, matte=True, dull=0.25)),
            (-0.48, -1.72, 0.065, 'convex', 75, dict(lean=[0.01, -0.03], wash=0.1, height=0.12)),
            (-0.95, -1.5, 0.045, 'young', 76, dict(lean=[0.0, 0.01], wash=0.15, height=0.08)),
            (0.25, -2.05, 0.075, 'convex', 77, dict(lean=[0.04, -0.01], wash=0.06, height=0.15, dull=0.12))]
DEATHCAPS = [(-1.05, -0.55, 0.055, 'convex', 81), (-1.2, -0.42, 0.04, 'young', 82), (-0.95, -0.35, 0.03, 'button', 83)]
ARUMS = [(0.98, -1.65, 0.38, 41, [0.04, -0.01], 52), (1.1, -1.58, 0.22, 42, [-0.03, 0.015], 30), (0.9, -1.5, 0.29, 43, [0.0, 0.035], 44),
         (1.2, -0.85, 0.33, 44, [0.02, 0.0], 38)]
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
    for x, y, H, sd, lean, n in ARUMS:
        props.append(extp('arum', (x, y, -0.01), height=H, seed=sd, lean=lean, berries=n, berry=0.0055, club=0.22 + n / 400))
    for x, y, H, sd in NIGHTSHADE:
        props.append(A4.extb('nightshade', (x, y, -0.01), height=H, seed=sd, berries=9, berry=0.0085))
    for p in props:
        if p.get('fn') == 'amanita' and p.get('species', 'muscaria') == 'muscaria' and p['position'][1] > -1.5:
            p['cap'] = round(p['cap'] * 1.35, 3)                              # a bold troop: mature caps 15-20 cm across
    for p in props:                                                         # scarlet and viscid, as a fresh fly agaric is: A4
        if p.get('fn') == 'amanita' and p.get('species', 'muscaria') == 'muscaria':   # dulled and dried them (matte) so they
            p.setdefault('dull', 0.0); p['dull'] = min(p['dull'], 0.25) if p.get('age') == 'old' else min(p['dull'], 0.12)
            p['matte'] = p.get('age') == 'old'                              # would not out-shout the speaker, and at 600 px
            p['orange'] = False                                             # they read as pink 'toadstools'
            p['wash'] = min(p.get('wash', 0.15), 0.12)
            p['position'][2] -= 0.015                                       # stems rise out of the duff, not stand on it
            if p.get('age') in ('old', 'plane'):                            # flat old caps read as tables at this angle:
                p['age'] = 'convex'; p['torn'] = max(p.get('torn', 0.0), 0.45)   # the old ones domed still, but torn
    # the litter they push up through: moss in broken cushions, bark crumbs and twigs over their bases (A4's, for every
    # group, not only its first)
    for cx, cy, r in ((0.55, -1.7, 0.45), (-0.75, -1.3, 0.45), (-1.05, -0.45, 0.3)):
        props.append(A.ext('strew', model='moss_01', on=['prop0-kit'], density=4000, up=0.5, scale=[0.6, 1.3], seed=int(90 + cx * 10),
                           patch=0.06, patch_cut=0.3, within=[cx, cy, r]))
        props.append(A.ext('strew', model='bark_debris_01', on=['prop0-kit'], density=60.0, up=0.5, scale=[0.15, 0.32],
                           seed=int(95 + cx * 10), within=[cx, cy, r + 0.05]))
    s['sky'] = sky(HDRI, ROT, strength=0.3, res='4k')
    s['title'] = 'barkhorn, Poison F1, a European poison wood in autumn'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['sky'], p['title'] = s['set'], s['sun'], s['lights'], s['sky'], s['title'] + ' (4:5)'
    return p
