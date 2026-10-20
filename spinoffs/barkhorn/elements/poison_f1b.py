"""Poison, F1 pass 7 (round 31h): A4 whole, with more of the wood's poisons, kept quiet.

The duel of proof 6 against the live A4 (poison_f.md): A4 6.53, F1 5.0, all four judges. They marked F1 down for its
oversized, repeated caps crowding the foreground, its flat backlit speaker, its billboard beech and murky bank, and
the clutter of berries and nightshade; they credited A4's sun and shafts, its redwood, its fern bank and its quiet
troop of small caps. So this keeps A4 as it is (poison_a4.py: the set, the sky, the sun and its canopy gaps, the
cards, the troop) and adds, small and set into the ferns where they grow:
- a few more fly agarics round A4's troop, at its scale;
- death caps at the speaker's foot (olive, white skirt, volva);
- one clump of lords-and-ladies in berry, half in the ferns at the right;
- a yew's red arils as a soft accent far back on the right.
Nothing purple: A4's foxgloves go (the owner: "purple plants (foxgloves) look fake").
"""
import copy

import poison as A
import poison_a4 as A4
from common import piece

MORE_CAPS = [(0.32, -1.45, 0.05, 'young', 91, dict(lean=[0.01, 0.0], wash=0.1, dull=0.3, matte=True, orange=True)),
             (-0.55, -1.2, 0.06, 'convex', 92, dict(lean=[-0.015, 0.01], wash=0.05, dull=0.36, matte=True, orange=True, torn=0.2)),
             (0.48, -1.32, 0.022, 'button', 93, dict(warts=260, dull=0.3, matte=True))]
DEATHCAPS = [(0.4, -0.48, 0.045, 'convex', 81), (0.5, -0.4, 0.035, 'young', 82), (0.33, -0.58, 0.022, 'button', 83)]
ARUMS = [(1.3, -0.6, 0.34, 41, [0.02, -0.01], 50), (1.37, -0.55, 0.25, 42, [0.03, 0.015], 36), (1.25, -0.52, 0.29, 43, [-0.02, 0.025], 44),
         (1.33, -0.68, 0.22, 44, [0.0, -0.03], 30)]
YEW = dict(position=[2.6, 3.0, 1.6], rotate=[168, 0, 200], scale=0.5)


def extp(fn, position=(0, 0, 0), **k):
    return piece('ext', module='poison_p_el', fn=fn, position=list(position), **k)


def shot():
    s = copy.deepcopy(A4.shot())
    props = s['set']['props']
    props[:] = [p for p in props if p.get('fn') != 'foxglove']           # no purple: the owner's note
    for x, y, R, age, sd, more in MORE_CAPS:
        more = dict(more); z = -0.045 if age != 'button' else -0.02
        props.append(A4.extb('amanita', (x, y, z), cap=R, age=age, seed=sd, **more))
    for x, y, R, age, sd in DEATHCAPS:
        props.append(A4.extb('amanita', (x, y, -0.04 if age != 'button' else -0.02), species='phalloides', cap=R, age=age,
                             seed=sd, dull=0.3, matte=True))
    for x, y, H, sd, lean, n in ARUMS:
        props.append(extp('arum', (x, y, -0.01), height=H, seed=sd, lean=lean, berries=n, berry=0.006, club=0.22 + n / 400))
    props.append(extp('yew', arils=40, aril=0.007, seed=9, value=0.7, **YEW))
    # the read (proof 7's judges: "orange mushrooms"): A4 dulled its caps toward brown and dried them so they would not
    # out-shout the speaker; scarlet with white warts they read as fly agarics (F1 p3 on), still at A4's size
    for p in props:
        if p.get('fn') == 'amanita' and p.get('species', 'muscaria') == 'muscaria':
            p['orange'] = False; p['dull'] = 0.15 if p.get('age') == 'old' else 0.04
            p['matte'] = p.get('age') == 'old'; p['wash'] = min(p.get('wash', 0.15), 0.1)
    s['title'] = 'barkhorn, Poison F1b, A4 with more of the wood\'s poisons'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
