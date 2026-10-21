"""Poison, F2 (round 31h): a tropical rainforest floor, the alternative to F1.

The owner, 2026-10-20: "...combine a lot of them into a forest or rainforest biome, alongside the red caps." Built on
A4 like F1 (its light, its floor, its ferns, the speaker's contact, its troop of fly agarics), moved to a rainforest:
Poly Haven's rainforest_trail behind, a dark wet floor (mud_forest), and the one toxic aroid there is a CC0 scan of,
anthurium (calcium oxalate, the same poison as dumb cane), in clumps. The red caps are a staged mix here: fly agarics
do not grow in the tropics.
Not built, for want of a believable model: dart frogs and the eyelash viper (no CC0 scan; modelled ones read as
toys, poison_a2.md), angel's trumpet, castor bean, rosary pea.
"""
import copy

import poison as A
import poison_a4 as A4
from common import piece, portrait_of, sky

HDRI, ROT = 'rainforest_trail', 180.0
ANTHURIUM = [(1.2, -0.8, 0.9, 20), (1.45, -0.55, 1.1, 140), (-1.25, -0.7, 1.0, 250), (-1.5, -0.3, 0.9, 80),
             (1.7, 0.4, 1.2, 300), (-1.9, 0.6, 1.3, 30)]


def shot():
    s = copy.deepcopy(A4.shot())
    props = s['set']['props']
    props[:] = [p for p in props if p.get('fn') != 'foxglove']           # no purple: the owner's note
    for p in props:
        if p.get('texture') == 'forest_leaves_02':                         # a dark, wet rainforest floor
            p['texture'] = 'mud_forest'; p['tint'] = '#2A2014'; p['tint_mix'] = 0.15
        if p.get('fn') == 'redwood':                                        # smooth rainforest trunks, not redwood
            p['bark'] = 'japanese_camphor_bark'; p['tint'] = '#6A6A58'; p['tint_mix'] = 0.3
            p['radius'] = round(p['radius'] * 0.5, 3); p['flare'] = 0.5; p['foot'] = 0.9
        if p.get('fn') == 'amanita':
            p['dull'] = min(p.get('dull', 0.0), 0.2)
    for x, y, sc, rz in ANTHURIUM:
        props.append(piece('asset', model='anthurium_botany_01', position=[x, y, 0.0], rotate=[0, 0, rz], scale=sc, res='2k'))
    s['sky'] = sky(HDRI, ROT, strength=0.3, res='4k')
    s['title'] = 'barkhorn, Poison F2, a tropical rainforest floor'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['sky'], p['title'] = s['set'], s['sun'], s['lights'], s['sky'], s['title'] + ' (4:5)'
    return p
