"""Poison G5 (round 31j): G4 made obviously deadly, a deer's skull lying among the death caps.

The owner, 2026-10-21, verbatim: "Poison: green, but more obviously deadly". G4 keeps the poisons green (the troop of
death caps, the arum's green berries), but at a glance it is a green wood with mushrooms in it: nothing says they kill.
The obvious green danger is a green pit viper, and Poison B modelled one; every critique of B called it a rubber toy
(poison_b.md), and it cost B its duel. So the cue here is a real thing, not a model: a white-tailed deer's skull, the
Smithsonian's scan (CC0, edanmdm:nmnheducation_15006160; poison_b_el.bones), lying on the litter at the troop's right,
its snout toward the caps, weathered a season or two: dull ivory, tannin-stained, darker in its pits, green with algae
on top, its teeth sunk in the moss. Seen side on (its long snout, the eye socket and the tooth row read as a skull at
600 px). A young death cap comes up at its snout and another behind it. Nothing strewn on the floor pierces it; the
troop's own moss and litter (G3's strews round the clump) already reach it. Two more strews of its own, moss and
litter in a ring round it, took the proof render past the helpers' 15 GB (14 GB at Cycles' start, against G4's 4.8),
so they are out.
G4 otherwise whole, its light included, so the duel against G4 measures the skull.
"""
import copy

import poison as A
import poison_g4 as G4

SKULL = (-0.05, -1.03)          # right of the troop, between the clump and cap 64; 5.5 m from the lens, inside f/2.8
SKULL_ROT = [-6, -15, -65]      # snout to the camera's left (at the caps), crown rolled a little toward the lens
CAPS = {                        # new by seed: (x, y), age, cap radius, stem height over the radius, extras
    93: ((-0.23, -1.07), 'young', 0.03, 1.5, dict(lean=[-0.01, -0.006], tilt=[-5, 7])),     # clear of its snout
    94: ((0.12, -0.9), 'young', 0.024, 1.35, dict(lean=[0.006, 0.004], tilt=[6, -4])),      # and of its crown
}
SINK = {'young': -0.016}
AVOID = {'bark_debris_01': 0.16, 'dry_branches_medium_01': 0.16, 'moss_01': 0.09}   # clear of the skull (m)


def shot():
    s = copy.deepcopy(G4.shot())
    props = s['set']['props']
    young = next(p for p in props if p.get('fn') == 'amanita' and p.get('seed') == 92)
    for p in props:                                   # nothing strewn on the floor grows through the skull
        if p.get('fn') == 'strew' and p.get('model') in AVOID:
            p['avoid'] = p.get('avoid', []) + [[SKULL[0], SKULL[1], AVOID[p['model']]]]
    for seed, ((x, y), age, R, hr, more) in CAPS.items():
        c = copy.deepcopy(young)
        for k in ('lean', 'tilt', 'height', 'stem'):
            c.pop(k, None)
        c.update(seed=seed, age=age, cap=R, position=[x, y, SINK[age]], **more)
        if hr:
            c['height'] = round(hr * R, 4); c['stem'] = round(0.2 * R, 4)
        props.append(c)
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'poison_b_el', 'fn': 'bones', 'position': [0, 0, 0],
                  'items': [{'part': 'skull', 'position': [SKULL[0], SKULL[1], 0.0], 'rotate': SKULL_ROT,
                             'sink': 0.025}]})
    s['title'] = 'barkhorn, Poison G5, the wood\'s poisons green, a deer\'s skull among the death caps'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
