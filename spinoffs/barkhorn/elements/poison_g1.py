"""Poison G1 (round 31i): the wood's poisons green (the owner, 2026-10-21: "It's a little odd that the poisonous things
are red and not green").

F1b whole (poison_f1b.py: A4's redwood floor, its sun and canopy gaps, the ferns and sorrel, the litter and moss), its
poisons turned green, each still a real poison of the wood:
- the troop of fly agarics becomes a troop of death caps (Amanita phalloides), the deadliest mushroom there is, at the
  same places and sizes, from buttons to opened caps: the yellow-green to olive of a fresh cap, darker at the centre,
  the white skirt and the cup at the foot;
- the lords-and-ladies' berries unripe, the glossy green they are for months before they turn, and as poisonous;
- no yew: its red arils were the last red in the frame.
"""
import copy

import poison as A
import poison_f1b as F

# a fresh death cap: olive at the centre to yellow-green at the margin, greener than the kit's bronze-olive default
DEATHCAP = [(0.1, '#34401A'), (0.45, '#55642C'), (0.85, '#7A8746'), (1.2, '#A8AD74')]


def shot():
    s = copy.deepcopy(F.shot())
    props = s['set']['props']
    props[:] = [p for p in props if p.get('fn') != 'yew']
    for p in props:
        if p.get('fn') == 'amanita':
            p['species'] = 'phalloides'
            p.pop('orange', None)
            p['cap'] = min(p['cap'], 0.07)                   # F1b sized its fly agarics up; a big death cap is 14 cm across
            p['cap_ramp'] = DEATHCAP
            p['dull_to'] = '#3A3A1C'                         # weathering toward a dark olive-brown, not the red's brown
            p['fibrils'] = 0.55                              # the dark radial fibrils that mark a death cap
            if p.get('age') == 'old':                        # a flat, upturned old cap is the fly agaric's; a death cap opens plane
                p['age'] = 'plane'
        elif p.get('fn') == 'arum':
            p['unripe'] = 1.0
    s['title'] = 'barkhorn, Poison G1, the wood\'s poisons green'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
