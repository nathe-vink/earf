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
Pass 5 (the lead's notes): the poisons grouped as they grow (a death cap cluster at the speaker's foot, a clump of
lords-and-ladies, a straggly nightshade bush, a yew's bough with red arils over the top-right corner), the troop varied
(one fallen, one old and cupped), the beech wood let in (copper litter on the bank, a low golden backlight).
No animals: no CC0 scan of an adder or a fire salamander exists (Poly Haven, ambientCG, Smithsonian 3D searched
2026-10-20), modelled snakes read as toys (poison_a2.md), and a modelled fire salamander (poison_p_el.salamander)
was judged a toy on a close crop (2026-10-20).
"""
import copy

import poison as A
import poison_a4 as A4
from common import area, piece, portrait_of, sky

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
# pass 5 (the lead): the poisons grouped as they grow. Death caps in a cluster at the speaker's foot, left
DEATHCAPS = [(0.38, -0.5, 0.06, 'convex', 81), (0.5, -0.42, 0.045, 'young', 82), (0.3, -0.62, 0.03, 'button', 83),
             (0.56, -0.55, 0.052, 'convex', 84), (0.44, -0.66, 0.025, 'button', 85)]
# lords-and-ladies in one clump, as they come up from a patch of corms (uneven heights, leaning apart)
ARUMS = [(1.02, -1.6, 0.36, 41, [0.03, -0.01], 50), (1.1, -1.55, 0.24, 42, [0.035, 0.02], 32), (0.96, -1.52, 0.29, 43, [-0.02, 0.03], 44),
         (1.07, -1.68, 0.31, 44, [0.01, -0.035], 40), (0.93, -1.64, 0.2, 45, [-0.035, -0.01], 26), (1.14, -1.62, 0.27, 46, [0.04, -0.02], 36)]
# deadly nightshade: a straggly bush mid-right, behind the berries' clump
NIGHTSHADE = [(1.12 + dx, 0.3 + dy, h * 0.7, 51 + k) for k, (dx, dy, h) in enumerate(
    ((0.0, 0.0, 0.75), (0.12, 0.08, 0.62), (-0.1, 0.1, 0.68), (0.06, -0.1, 0.55), (-0.14, -0.05, 0.5), (0.18, -0.04, 0.48),
     (-0.04, 0.18, 0.8), (0.1, 0.2, 0.58), (-0.2, 0.12, 0.44), (0.22, 0.12, 0.66)))]
# the yew's bough hanging into the top-right corner, near the lens and soft
YEW = dict(position=[1.5, -1.55, 1.3], rotate=[168, 0, 200], scale=0.4)
# the low golden sun of an autumn morning, through the beeches behind and right: the backlight
SUN = {'azimuth_deg': 150.0, 'elevation_deg': 16.0, 'irradiance': 26.0, 'angle_deg': 0.6, 'color': '#FFC47A'}
SUNLIT = [(0.0, 0.0, 0.8, 1.1), (-0.2, -1.35, 0.0, 0.7), (0.6, -1.7, 0.0, 0.5), (-0.5, -0.4, 0.0, 0.4), (1.5, 0.5, 0.4, 0.5),
          (2.5, 6.5, 0.8, 0.8), (-2.0, 7.0, 1.0, 0.8)]


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
        props.append(A4.extb('nightshade', (x, y, -0.01), height=H, seed=sd, berries=9, berry=0.0085, leaves=1,
                             lean=[0.08 * ((sd % 3) - 1), 0.06 * ((sd % 2) * 2 - 1)]))
    props.append(extp('yew', arils=50, aril=0.006, seed=9, value=0.75, **YEW))
    # the troop's variety: one old cap gone flat and cupped at the back (a fallen one read as a ball, so none)
    props.append(A4.extb('amanita', (-0.35, -0.95, -0.05), cap=0.085, age='old', seed=79, torn=0.4, matte=True, dull=0.3, wash=0.0))
    # the beech wood shows: the bank behind in copper beech litter, a third of its ferns
    for p in props:
        if p.get('texture') == 'acg:Moss001':
            p['texture'] = 'leaves_forest_ground'; p['tint'] = '#5A3A1E'; p['tint_mix'] = 0.15; p['tex_scale'] = 0.6
        if p.get('fn') == 'plants' and p.get('model') == 'fern_02' and p.get('seed') == 17:
            p['place'] = p['place'][::3]
        if p.get('fn') == 'canopy':                                         # the canopy's gaps along the new sun
            p['holes'] = [A.gap_for(x, y, z, r, (0.0, 4.0), SUN) for x, y, z, r in SUNLIT]
    s['sun'] = SUN
    # a cool fill from the camera side, so the speaker's green stays true against the warm backlight
    s['lights']['cool'] = {**area(-25, 15, 3.0, 1.2, '#DCE6EE', (1.5, 1.5), (0.0, 0.0, 0.7)), 'specular': 0.1}
    for p in props:
        if p.get('fn') == 'amanita' and p.get('species', 'muscaria') == 'muscaria' and p['position'][1] > -1.5:
            p['cap'] = round(p['cap'] * 1.35, 3)                              # a bold troop: mature caps 15-20 cm across
    for p in props:                                                         # scarlet and viscid, as a fresh fly agaric is: A4
        if p.get('fn') == 'amanita' and p.get('species', 'muscaria') == 'muscaria':   # dulled and dried them (matte) so they
            p.setdefault('dull', 0.0); p['dull'] = min(p['dull'], 0.25) if p.get('age') == 'old' else min(p['dull'], 0.12)
            p['matte'] = p.get('age') == 'old'                              # would not out-shout the speaker, and at 600 px
            p['orange'] = False                                             # they read as pink 'toadstools'
            p['wash'] = min(p.get('wash', 0.15), 0.12)
            # pass 6 (proof 5's critics: "copies of one plastic model, stamped dots, clean stems"): each cap weathered
            # its own way: dried (no viscid gloss, soil up the stem), litter on the cap, the rain's wash uneven
            k = p.get('seed', 1)
            p['matte'] = True; p['dull'] = max(p['dull'], 0.04 + 0.03 * (k % 4))
            p['needles'] = 1 + k % 4; p['ragged'] = 0.04 + 0.02 * (k % 3)
            p['wash'] = [0.0, 0.05, 0.12, 0.25, 0.4][k % 5]
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
