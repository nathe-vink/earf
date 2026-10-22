"""Poison G4 (round 31i): G3 with its low caps standing up.

G3 p1 beat F1b (7 v 5, 6 v 5) and G2 (7 v 6, 6 v 5) in both orders, its realism critics 5 and 5; what they still saw
in the troop was its low caps: "several lie on the soil as flat ovals that look stuck on", "a few of its flat disc caps
look slightly off". Those were the two eggs (a white sac with the cap's top in it, a pale oval at this distance), the cap
tipped back to show its gills (at 960 px its underside reads as a disc on the ground, not as gills) and the young caps
sunk to their caps in the moss. Both critics also saw the caps "glow faintly, brighter than the shaded ground": the
photographer's reflector at the lens lights them as it lights the speaker, and pale caps on white stems take it more
than the dark litter does. And no one saw the sun fleck behind the clump. So, G3 otherwise whole:
- the eggs become young caps on short stems, the tipped cap tilts a little, and every young cap shows its stem;
- the caps a step darker and the stems' albedo down a fifth (amanita `stem_tone`), so the fill does not lift them;
- the fleck lands on the open litter in front of the clump, where the lens sees it.
"""
import copy

import poison as A
import poison_g3 as G3

CAPS = dict(G3.CAPS)
(x, y), age, R, hr, sr, ramp, more = CAPS[62]
CAPS[62] = ((x, -1.42), age, R, 1.85, sr, ramp, dict(more, tilt=[-10, 4]))
CAPS[65] = ((-0.26, -1.35), 'young', 0.031, 1.55, 0.2, G3.G.FRESH, dict(lean=[0.012, -0.01], tilt=[6, 8]))
CAPS[82] = ((0.5, -0.43), 'young', 0.029, 1.5, 0.2, G3.G.FRESH, dict(lean=[-0.006, 0.004], tilt=[-5, 6]))
for k, h in ((92, 1.55), (91, 1.65)):
    (x, y), age, R, hr, sr, ramp, more = CAPS[k]
    CAPS[k] = ((x, y), age, R, h, sr, ramp, more)
SINK = {'button': -0.012, 'young': -0.016}


def _darker(ramp, f=0.86):
    """A cap ramp a step darker: each stop's sRGB scaled by f."""
    return [(t, '#' + ''.join(f'{round(int(h[i:i + 2], 16) * f):02X}' for i in (1, 3, 5))) for t, h in ramp]
FLECK = (G3.CLUMP[0] + 0.1, G3.CLUMP[1] - 0.22)            # on the litter in front of the clump, right of 62's stem


def shot():
    s = copy.deepcopy(G3.shot())
    props = s['set']['props']
    for p in props:
        if p.get('fn') == 'amanita':
            (x, y), age, R, hr, sr, ramp, more = CAPS[p['seed']]
            for k in ('lean', 'tilt', 'torn', 'needles', 'dirt', 'dull', 'bite', 'height', 'stem', 'age', 'cap'):
                p.pop(k, None)
            p.update(age=age, cap=R, cap_ramp=_darker(ramp), stem_tone=0.8, **more)
            p['height'] = round(hr * R, 4)
            p['stem'] = round(sr * R, 4)
            p['position'] = [x, y, SINK.get(age, -0.022)]
        elif p.get('fn') == 'canopy':
            p['holes'] = p['holes'][:-1] + [A.gap_for(FLECK[0], FLECK[1], 0.02, 0.2, (0.0, 4.0), A.SUN_A2)]
    s['title'] = 'barkhorn, Poison G4, the wood\'s poisons green, a troop standing up'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
