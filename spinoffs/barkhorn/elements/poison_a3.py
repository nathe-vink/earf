"""Poison, concept A with its poisons, third try (round 31d): A's redwood floor, made poisonous quietly.

A2 (poison_a2.py) lost every round of its duel against A (by 0.55 on the landscape, 0.5 on the phone frame): its fly
agarics read as toy CG, the reddest thing in the frame; its foxgloves as strings of pink beads; and the 2 deg sun disc
it used to soften the woofer bay's shadow blurred A's shafts, A's main win. A3, per the coordinator's brief:
- A's sun as it was (0.6 deg), so the shafts stay; the woofer bay's shadow answered with fill, not a wider sun;
- two or three agarics, smaller, a duller red, in shadow, half in the litter, in the gap between A's fern stand at
  the trunk's foot and the speaker, no frond across a cap (A's fern stand kept whole: it was A's win, not A2's);
- two foxgloves with real bells: crowded toward the bottom, hanging down on short stalks, buds at the tip, a little
  desaturated;
- no snake.
"""
import math

import poison as A
from common import piece

CLUSTER = (-0.70, 0.50)             # in the shade at the right foot of A's fern stand, by the speaker's left side, ~7 m out
# (dx, dy, cap radius, age, seed, extra amanita settings)
AGARICS = [(0.0, 0.0, 0.072, 'old', 61, dict(lean=[0.012, -0.008], wash=0.05, dull=0.2, needles=2, torn=0.15, height=0.1)),
           (0.11, -0.06, 0.05, 'convex', 62, dict(lean=[0.035, -0.015], wash=0.1, dull=0.2, torn=0.3, height=0.05)),
           (-0.06, -0.1, 0.02, 'button', 64, dict(warts=260, dull=0.2))]
FOXGLOVES = [(-0.17, 5.41, 1.45, 2), (0.35, 4.31, 1.05, 4)]   # x, y, height, seed: in the haze right of the horn


def extb(fn, position=(0, 0, 0), **k):
    return piece('ext', module='poison_b_el', fn=fn, position=list(position), **k)


def _clear(x, y):
    """Only the fern that would lie across a cap goes."""
    return math.hypot(x - CLUSTER[0], y - CLUSTER[1]) >= 0.22


def _renum(on, gone):
    if on.startswith('prop') and on.endswith('-kit') and on[4:-4].isdigit():
        n = int(on[4:-4])
        return f'prop{n - sum(1 for g in gone if g < n)}-kit'
    return on


def shot():
    s = A.shot()
    props = s['set']['props']
    # A's two toadstools out: the agarics at the trunk's foot replace them
    gone = [k for k, p in enumerate(props) if p.get('fn') == 'toadstool']
    props[:] = [p for p in props if p.get('fn') != 'toadstool']
    for p in props:                                       # a strew names its surface by index: renumber past the gap
        if isinstance(p.get('on'), list):
            p['on'] = [_renum(o, gone) for o in p['on']]
    for p in props:
        if p.get('fn') == 'plants' and p.get('model') == 'fern_02' and p.get('seed') == 3:
            p['place'] = [q for q in p['place'] if _clear(q[0], q[1])]
    cx, cy = CLUSTER
    for dx, dy, R, age, sd, more in AGARICS:
        more = dict(more)
        props.append(extb('amanita', (cx + dx, cy + dy, -0.03 if age != 'button' else -0.015), cap=R, age=age, seed=sd,
                          **more))
    # the litter they push up through: moss in broken cushions, bark crumbs and twigs over their bases
    props.append(A.ext('strew', model='moss_01', on=['prop0-kit'], density=4000, up=0.5, scale=[0.6, 1.3], seed=65,
                       patch=0.06, patch_cut=0.3, within=[cx, cy, 0.28]))
    props.append(A.ext('strew', model='bark_debris_01', on=['prop0-kit'], density=60.0, up=0.5, scale=[0.15, 0.32], seed=66,
                       within=[cx, cy, 0.3]))
    for x, y, h, sd in FOXGLOVES:
        z = A.bank_z(x, y)
        props.append(extb('foxglove', (x, y, max(z or 0.0, 0.0) - 0.02), height=h, lean=[0.03 * (sd - 3), 0.0], side=-60,
                          seed=sd, bells=int(30 * h), bell=0.026, droop=0.7, crowd=1.6, pedicel=0.02, buds=9,
                          color='#8C5A84'))
    # the woofer bay: the cabinet's edge throws a hard sun shadow across the lining behind the clear front; A's warm
    # bounce (diffuse only) is turned down onto the bay and lifted, so the shaded half fills instead of the sun widening
    b = s['lights']['bounce']
    s['lights']['bounce'] = {**b, 'irradiance': 3.5, 'target': [0.0, 0.0, 0.6], 'size_m': [2.0, 1.5],
                             'orbit': {**b['orbit'], 'elevation_deg': 25}}
    s['title'] = 'barkhorn, Poison A3, the redwood floor with its poisons, quietly'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
