"""Poison, concept A with its poisons (round 31c): A's redwood floor, made poisonous the realistic way.

The owner, on concept A: "Poison isn't reading as poisonous." B (poison_b.py) put the poisons at the speaker's feet
and lost the duel to A by 1.5-2 points: at that distance modelled snakes and fungi read as props. A2 keeps A's set,
light and camera and adds fewer, smaller poisons further back, where the depth of field and the haze carry them:
- a cluster of four fly agarics at a redwood's foot in the middle distance, half buried in moss and duff, one tilted,
  one bitten, in a shaft of their own so the red reads without shouting;
- three foxglove spikes back in the haze;
- no snake (at any size we can model, it reads as a toy).
And A's own two flaws: the hard diagonal shadow across the woofer ring (a softer sun) and the darker right side (the
card at the right lifted).
"""
import copy, math

import poison as A
from common import piece

CLUSTER = (-1.15, 1.3)              # at the left redwood's foot (outside its buttresses), left of the speaker, ~8 m from the lens
# (dx, dy, cap radius, age, seed, lean, torn)
AGARICS = [(0.0, 0.0, 0.085, 'plane', 61, (0.02, -0.01), 0.0),
           (0.13, -0.08, 0.065, 'convex', 62, (0.05, -0.02), 0.0),       # tilted out of the clump
           (-0.1, -0.1, 0.045, 'young', 63, (-0.01, 0.0), 0.35),          # its margin bitten
           (0.06, -0.18, 0.024, 'button', 64, (0.0, 0.0), 0.0)]
FOXGLOVES = [(-0.43, 4.48, 1.25, 1), (-0.17, 5.41, 1.45, 2), (0.35, 4.31, 1.05, 4)]   # x, y, height, seed: in the haze right of the horn, 10-12 m out


def extb(fn, position=(0, 0, 0), **k):
    return piece('ext', module='poison_b_el', fn=fn, position=list(position), **k)


def _clear(x, y):
    """Keep ferns off the cluster and out of the camera's line to it."""
    cx, cy = CLUSTER
    if math.hypot(x - cx, y - cy) < 0.55:
        return False
    cam = (6.4 * math.sin(math.radians(18.0)), -6.4 * math.cos(math.radians(18.0)))
    if math.hypot(x - cx, y - cy) < 1.6 and A._seg_dist(x, y, (cx, cy), cam) < 0.3:
        return False
    return True


def _renum(on, gone):
    if on.startswith('prop') and on.endswith('-kit') and on[4:-4].isdigit():
        n = int(on[4:-4])
        return f'prop{n - sum(1 for g in gone if g < n)}-kit'
    return on


def shot():
    s = A.shot()
    props = s['set']['props']
    # A's two toadstools out: the cluster at the trunk's foot replaces them
    gone = [k for k, p in enumerate(props) if p.get('fn') == 'toadstool']
    props[:] = [p for p in props if p.get('fn') != 'toadstool']
    for p in props:                                       # a strew names its surface by index: renumber past the gap
        if isinstance(p.get('on'), list):
            p['on'] = [_renum(o, gone) for o in p['on']]
    for p in props:
        if p.get('fn') == 'plants' and p.get('model') == 'fern_02' and p.get('seed') == 3:
            p['place'] = [q for q in p['place'] if _clear(q[0], q[1])]
        if p.get('fn') == 'canopy':
            cx, cy = CLUSTER
            p['holes'] = p['holes'] + [A.gap_for(cx, cy, 0.1, 0.22, (0.0, 4.0), A.SUN_A2)]
    nk = len(props)
    cx, cy = CLUSTER
    for dx, dy, R, age, sd, lean, torn in AGARICS:
        props.append(extb('amanita', (cx + dx, cy + dy, -0.02 if age != 'button' else -0.012), cap=R * 1.3, age=age, seed=sd,
                          lean=list(lean), torn=torn))
    # moss and duff banked round their bases (the ground is prop 0)
    props.append(A.ext('strew', model='moss_01', on=['prop0-kit'], density=6000, up=0.5, scale=[0.7, 1.5], seed=65,
                       patch=0.06, patch_cut=0.25, within=[cx, cy, 0.3]))
    props.append(A.ext('strew', model='bark_debris_01', on=['prop0-kit'], density=40.0, up=0.5, scale=[0.15, 0.3], seed=66,
                       within=[cx, cy, 0.35]))
    for x, y, h, sd in FOXGLOVES:
        z = A.bank_z(x, y)
        props.append(extb('foxglove', (x, y, max(z or 0.0, 0.0) - 0.02), height=h, lean=[0.03 * (sd - 2), 0.0], side=-60,
                          seed=sd, bells=int(14 * h)))
    # A's flaws: a softer sun edge for the horn's shadow across the woofer ring; the right side lifted
    s['sun'] = {**s['sun'], 'angle_deg': 2.0}
    s['lights']['card'] = {**s['lights']['card'], 'irradiance': 1.6}
    s['title'] = 'barkhorn, Poison A2, the redwood floor with its poisons'
    return s


def portrait():
    s = shot()
    p = copy.deepcopy(A.portrait())
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
