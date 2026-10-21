"""Poison G3 (round 31i): G2's death caps as a troop that grew there.

G2 p1 beat the live F1b in both duels (6 v 5 and 7 v 6: "the red caps look like toy CG props"; "the death caps a
quieter, grown-up nod to Poison"), but its realism critics (5 and 4) and one duel against G1 saw the same thing in the
caps: "one model copied many times", "the same size, the same flat cap, the same pale colour, the same straight
white stem", "evenly spaced in a row, all standing straight up", "the stems as bright under the cap as at the base",
"the low caps flat discs laid on the ground", "no rim of the light from behind"; and both: "the shafts land nowhere".
So, G2 otherwise whole:
- the troop re-laid as one grows: a clump of three and an egg at its foot, their stems fanning out from one spot,
  and three singles at other depths; sizes from 3 to 15 cm across, stems from 3 to 15 cm tall and thicker, every one
  leaning or tilted, one tipped back far enough to show its gills;
- three caps far apart in colour: a fresh yellow-green, the common olive, an old dark bronze-olive gone dull, with
  soil on the older caps and needles on three;
- the stems in the caps' shadow toward the top and soil-stained higher (amanita `shade`);
- A4's sun fleck back by the troop (F1b took it off because the scarlet washed to salmon in it), landing on the litter
  just behind the clump, so one of the shafts lands on something and the caps get a rim of light from behind.
"""
import copy

import poison as A
import poison_g2 as G

DARK = [(0.1, '#2A2814'), (0.45, '#403C1E'), (0.85, '#5A5530'), (1.2, '#77714A')]     # an old cap gone bronze-dark
CLUMP = (-0.29, -1.26)                                    # where the clump's stems meet; the sun fleck lands here
# by F1b's seed: (x, y), age, cap radius, stem height over the radius, stem radius over the cap's, ramp, extras
CAPS = {
    61: ((-0.30, -1.21), 'plane', 0.075, 2.05, 0.16, G.OLIVE, dict(lean=[-0.028, 0.012], tilt=[5, -9], torn=0.3, needles=4, dirt=0.3, dull=0.12)),
    63: ((-0.24, -1.26), 'convex', 0.058, 1.45, 0.17, DARK, dict(lean=[0.048, -0.012], tilt=[9, 16], bite=[235, 0.016], dirt=0.35, dull=0.3)),
    92: ((-0.35, -1.29), 'young', 0.038, 1.2, 0.2, G.FRESH, dict(lean=[-0.03, -0.012], tilt=[-6, -12])),
    65: ((-0.27, -1.34), 'button', 0.03, None, None, G.FRESH, dict()),
    62: ((-0.03, -1.48), 'convex', 0.052, 1.6, 0.17, G.OLIVE, dict(lean=[0.006, -0.022], tilt=[-30, 4], needles=1)),
    64: ((0.23, -1.15), 'plane', 0.062, 1.8, 0.16, G.BRONZE, dict(lean=[0.012, 0.01], tilt=[-4, 8], torn=0.45, dirt=0.35, dull=0.35, needles=2)),
    91: ((-0.62, -1.5), 'young', 0.032, 1.3, 0.2, G.FRESH, dict(lean=[-0.01, 0.0], tilt=[4, -6])),
    81: ((0.42, -0.5), 'convex', 0.05, 1.6, 0.17, G.OLIVE, dict(lean=[0.01, -0.006], tilt=[-12, 4])),
    82: ((0.5, -0.43), 'button', 0.028, None, None, G.FRESH, dict()),
}
SINK = {'button': -0.012, 'young': -0.028}
ROUGH = {61: (0.62, 0.05), 63: (0.74, 0.0), 92: (0.56, 0.08), 65: (0.62, 0.04), 62: (0.58, 0.07), 64: (0.72, 0.02),
         91: (0.56, 0.08), 81: (0.6, 0.06), 82: (0.6, 0.05)}


def shot():
    s = copy.deepcopy(G.shot())
    props = s['set']['props']
    for p in props:
        if p.get('fn') == 'amanita':
            (x, y), age, R, hr, sr, ramp, more = CAPS[p['seed']]
            for k in ('lean', 'tilt', 'torn', 'needles', 'dirt', 'dull', 'bite', 'height', 'stem'):
                p.pop(k, None)
            p.update(age=age, cap=R, cap_ramp=ramp, shade=0.8, **more)
            if hr:
                p['height'] = round(hr * R, 4)
                p['stem'] = round(sr * R, 4)
            p['rough'], p['coat'] = ROUGH[p['seed']]
            p['position'] = [x, y, SINK.get(age, -0.022)]
        elif p.get('fn') == 'canopy':
            # A4's fleck by the troop, back (F1b's realism pass took it off for the scarlet's sake), landing on the
            # litter just behind the clump: square on the caps it washed them cream (proof 0), behind them it rims
            # them and sets them against lit ground
            p['holes'] = p['holes'] + [A.gap_for(CLUMP[0] + 0.06, CLUMP[1] + 0.3, 0.05, 0.2, (0.0, 4.0), A.SUN_A2)]
    s['title'] = 'barkhorn, Poison G3, the wood\'s poisons green, a troop that grew there'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
