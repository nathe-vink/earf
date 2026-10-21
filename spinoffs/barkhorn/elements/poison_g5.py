"""Poison G5 (round 31j): G4 made obviously deadly, a deer's skull lying among the death caps.

The owner, 2026-10-21, verbatim: "Poison: green, but more obviously deadly". G4 keeps the poisons green (the troop of
death caps, the arum's green berries), but at a glance it is a green wood with mushrooms in it: nothing says they kill.
The obvious green danger is a green pit viper, and Poison B modelled one; every critique of B called it a rubber toy
(poison_b.md), and it cost B its duel. So the cue here is a real thing, not a model: a white-tailed deer's skull, the
Smithsonian's scan (CC0, edanmdm:nmnheducation_15006160; poison_b_el.bones), weathered a season or two: dull ivory,
tannin-stained, darker in its pits, green with algae on top, its teeth sunk in the litter. Seen side on: its long
snout, the eye socket and the tooth row. Nothing strewn on the floor pierces it; the troop's own moss and litter (G3's
strews round the clump) reach it. (Two more strews of its own, moss and litter in a ring round it, took the proof past
the helpers' 15 GB: each strew on this ground costs about 3 GB at Cycles' start. They are out.)

p1 (the skull at the troop's right, 5.5 m off, life size, in the shade, two young caps beside it): in the frame it was
a pale scrap about 90 x 30 px that "could pass for a bleached bit of bark or bone"; only a 3x crop showed a skull. So,
p2:
- the skull a big buck's (1.25 x the scan's doe, 34 cm), forward into the open litter in front of the speaker's left
  foot, 5.0 m off, side on to the lens, its snout pointing into the troop (cap 62 a hand's width ahead of it): about
  1.5 x p1's size in frame;
- the forest's one sun fleck, G4's (which lit open litter no one saw), moved onto it, so bleached bone in sun is the
  brightest small thing in the lower frame, against the dark duff;
- the bone a step paler, the tannin lighter, so that in the sun it reads white;
- p1's two young caps out (the troop's 62 and 64 now flank it).
G4 otherwise whole, so the duel against G4 measures the skull.
"""
import copy

import poison as A
import poison_g4 as G4

SKULL = (0.24, -1.37)           # in the open litter in front of the speaker's left foot; 5.0 m off
SKULL_ROT = [-6, -15, -80]      # side on to the lens, snout to its left (into the troop), crown rolled toward it
SKULL_SCALE = 1.25              # a big buck's
BONE = [(0.32, '#D6CDB4'), (0.5, '#C6BA9D'), (0.62, '#B4A88B'), (0.75, '#A0977F')]   # a step paler than the kit's
AVOID = {'bark_debris_01': 0.2, 'dry_branches_medium_01': 0.2, 'moss_01': 0.11}    # clear of the skull (m)


def shot():
    s = copy.deepcopy(G4.shot())
    props = s['set']['props']
    for p in props:
        if p.get('fn') == 'strew' and p.get('model') in AVOID:      # nothing strewn on the floor grows through it
            p['avoid'] = p.get('avoid', []) + [[SKULL[0], SKULL[1], AVOID[p['model']]]]
        elif p.get('fn') == 'canopy':                                # G4's fleck, the last hole, onto the skull
            p['holes'] = p['holes'][:-1] + [A.gap_for(SKULL[0], SKULL[1], 0.06, 0.15, (0.0, 4.0), A.SUN_A2)]
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'poison_b_el', 'fn': 'bones', 'position': [0, 0, 0],
                  'bone': BONE, 'streaks': 0.4,
                  'items': [{'part': 'skull', 'position': [SKULL[0], SKULL[1], 0.0], 'rotate': SKULL_ROT,
                             'scale': SKULL_SCALE, 'sink': 0.03}]})
    s['title'] = 'barkhorn, Poison G5, the wood\'s poisons green, a deer\'s skull among the death caps'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
