"""Poison, concept A with its poisons, fourth try (round 31e): one real-looking group the eye meets on its way in.

A3 (poison_a3.py) beat A (+0.45 landscape, +0.1 phone) and went up, but its poisons did not read at the site's sizes:
three small dull caps at the cabinet's foot (where they fought the product) and two foxgloves, a few pixels each at
600 px. A4 keeps A3's wins (A's 0.6 deg sun and its shafts, the brighter cabinet, A's fern stand whole) and moves
the poison to where the eye travels: a group of fly agarics at true scale (caps 8-15 cm across, every age, one broken,
weathered so they are not the reddest thing in the frame) in a dapple of their own on the open duff at the left of
the foreground, and a stand of foxgloves in the haze behind and to the right, one caught in a shaft.
"""
import math

import poison as A
from common import piece

CLUSTER = (-0.22, -1.34)            # on the open duff at the left of the foreground, ~5.2 m from the lens
# (dx, dy, cap radius, age, seed, extra amanita settings): caps 8-15 cm across, every age, one broken
AGARICS = [(0.0, 0.0, 0.07, 'convex', 61, dict(lean=[0.015, -0.01], wash=0.05, dull=0.15, needles=2, torn=0.2)),
           (0.16, 0.05, 0.06, 'convex', 62, dict(lean=[0.03, 0.01], wash=0.1, dull=0.12)),
           (-0.12, 0.1, 0.075, 'old', 63, dict(lean=[-0.02, 0.015], wash=0.0, dull=0.25, torn=0.4)),      # broken, rim torn
           (0.07, -0.12, 0.045, 'young', 64, dict(lean=[0.0, -0.01], wash=0.2, dull=0.2)),
           (-0.05, -0.16, 0.025, 'button', 65, dict(warts=280, dull=0.15)),
           (0.25, -0.08, 0.05, 'convex', 66, dict(rotate=[0, 95, 200], height=0.03, wash=0.1, dull=0.35, z=0.04))]  # fallen
# a stand of foxgloves in the haze behind and right of the horn, 10-12 m out; the first caught in a shaft
FOXGLOVES = [(0.1, 4.9, 1.5, 7), (-0.17, 5.41, 1.4, 2), (0.35, 4.31, 1.1, 4), (0.62, 5.15, 1.25, 8), (-0.45, 4.7, 0.95, 9)]


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
        more = dict(more); z = more.pop('z', -0.03 if age != 'button' else -0.015)
        props.append(extb('amanita', (cx + dx, cy + dy, z), cap=R, age=age, seed=sd, **more))
    # their own dapple, and a shaft through the haze onto the first foxglove
    for p in props:
        if p.get('fn') == 'canopy':
            fx, fy = FOXGLOVES[0][:2]
            p['holes'] = p['holes'] + [A.gap_for(cx, cy, 0.1, 0.26, (0.0, 4.0), A.SUN_A2),
                                       A.gap_for(fx, fy, 1.0, 0.3, (0.0, 4.0), A.SUN_A2)]
    # the litter they push up through: moss in broken cushions, bark crumbs and twigs over their bases
    props.append(A.ext('strew', model='moss_01', on=['prop0-kit'], density=4000, up=0.5, scale=[0.6, 1.3], seed=65,
                       patch=0.06, patch_cut=0.3, within=[cx, cy, 0.38]))
    props.append(A.ext('strew', model='bark_debris_01', on=['prop0-kit'], density=60.0, up=0.5, scale=[0.15, 0.32], seed=66,
                       within=[cx, cy, 0.42]))
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
    s['title'] = 'barkhorn, Poison A4, the redwood floor with its poisons where the eye meets them'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
