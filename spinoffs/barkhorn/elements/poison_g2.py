"""Poison G2 (round 31i): G1's green poisons made to look grown, not placed.

G1 p1's critics (realism 5 and 5; the read "pale cream mushrooms, nothing looks poisonous"; the duel against F1b to
F1b): "four almost identical flat pale caps", "the same shape, colour and soft highlight", "clean and waxy", "pin
stems", "no gills, ring or volva", "sit on the moss instead of growing out of it"; the berries "a string of identical
beads", "matte, evenly lit, too bright for its shady spot". So, at the same places as G1's (F1b's) caps:
- each death cap its own: a deeper olive-green, fresh yellow-green on the young ones and bronze-olive on the old,
  darker at the centre with the radial fibrils (placed on the cap's own axis, not the leaned stem's); sizes from the
  egg to a 14 cm cap, every age; tilted on their stems, one far enough back to show its white gills;
- the death cap's own parts, which the fly agaric's model did not have: the ring a thin skirt hanging from the
  stem, its hem uneven; the volva a loose torn sac at the foot, showing above the litter; the button an egg the cap is
  breaking out of;
- weather and wear: soil splashed on the older caps, needles fallen on two, a slug's bite out of one, torn margins;
- the lords-and-ladies' unripe berries glossy, each its own green, deeper than G1's.
F1b's set, sun and grade are otherwise unchanged; no yew, as in G1.
"""
import copy

import poison as A
import poison_f1b as F

# a fresh cap's yellow-green, the common olive, an older cap's bronze-olive: centre to margin
# (G1's pale margins read cream under the forest's warm light; a first, saturated try read lime: so a step darker
# than G1, greener, the chroma between, and the three far enough apart to tell under that light)
FRESH = [(0.1, '#323818'), (0.45, '#4C5524'), (0.85, '#6A7434'), (1.2, '#8E9650')]
OLIVE = [(0.1, '#2E3016'), (0.45, '#454A20'), (0.85, '#5E632E'), (1.2, '#7C8046')]
BRONZE = [(0.1, '#332E18'), (0.45, '#4E4724'), (0.85, '#6B6232'), (1.2, '#8A8048')]
# by F1b's seed (A4's troop 61-65, F1b's two more 91-92, its two at the speaker's foot 81-82): the cap each becomes.
# tilt [about x, about y] degrees: about x negative tips the cap's top away from the lens, its gills toward it
CAPS = {
    61: dict(age='plane', cap=0.072, ramp=OLIVE, lean=[0.012, -0.008], tilt=[-5, 4], needles=3, dirt=0.25, dull=0.1, torn=0.15),
    62: dict(age='convex', cap=0.058, ramp=FRESH, lean=[0.02, 0.01], tilt=[-24, -6], needles=1),
    63: dict(age='plane', cap=0.066, ramp=BRONZE, lean=[-0.02, 0.015], tilt=[6, -8], torn=0.3, bite=[235, 0.016], dirt=0.3, dull=0.3),
    64: dict(age='young', cap=0.046, ramp=FRESH, lean=[0.0, -0.01], tilt=[-4, 6]),
    65: dict(age='button', cap=0.032, ramp=FRESH, lean=[0.0, 0.0]),
    91: dict(age='convex', cap=0.05, ramp=OLIVE, lean=[0.01, 0.0], tilt=[10, -12], dirt=0.15),
    92: dict(age='convex', cap=0.062, ramp=BRONZE, lean=[-0.015, 0.01], tilt=[-8, 5], torn=0.2, dull=0.2),
    81: dict(age='convex', cap=0.045, ramp=OLIVE, lean=[0.008, -0.004], tilt=[-10, 0]),
    82: dict(age='young', cap=0.035, ramp=FRESH, lean=[-0.006, 0.004]),
}
SINK = {'button': -0.012}                                 # the sac's lobes above the litter; deeper than this hides them
# (roughness, coat): a satin sheen at most. Seen this low, at a grazing angle, a glossier cap mirrors the bright haze
# and goes cream; the old ones dry
ROUGH = {61: (0.62, 0.05), 62: (0.56, 0.08), 63: (0.72, 0.0), 64: (0.58, 0.07), 65: (0.62, 0.04), 91: (0.6, 0.06),
         92: (0.7, 0.02), 81: (0.6, 0.06), 82: (0.56, 0.08)}


def shot():
    s = copy.deepcopy(F.shot())
    props = s['set']['props']
    props[:] = [p for p in props if p.get('fn') != 'yew']     # only strews on the ground (prop0) follow it: no index shifts
    for p in props:
        if p.get('fn') == 'amanita':
            c = dict(CAPS[p['seed']])
            for k in ('orange', 'matte', 'wash', 'warts', 'stem', 'height', 'torn', 'dull'):
                p.pop(k, None)
            p.update(species='phalloides', cap_ramp=c.pop('ramp'), dull_to='#3A3A1C', fibrils=0.55, skirt='membrane',
                     sac=True, rest=True)
            p['rough'], p['coat'] = ROUGH[p['seed']]
            p.update(c)
            p['position'][2] = SINK.get(p['age'], -0.022)
        elif p.get('fn') == 'arum':
            p.update(unripe=1.0, green_gloss=True, green_deep='#2E4A10', green='#6E8F22', fallen=0)   # the kit drops ripe ones
    s['title'] = 'barkhorn, Poison G2, the wood\'s poisons green, grown in'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
