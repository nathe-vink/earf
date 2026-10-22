"""Poison G5 (round 31j): G4 made obviously deadly, a deer's remains lying among the death caps.

The owner, 2026-10-21, verbatim: "Poison: green, but more obviously deadly". G4 keeps the poisons green (the troop of
death caps, the arum's green berries), but at a glance it is a green wood with mushrooms in it: nothing says they kill.
The obvious green danger is a green pit viper, and Poison B modelled one; every critique of B called it a rubber toy
(poison_b.md), and it cost B its duel. So the cue here is a real thing, not a model: a deer's bones, the Smithsonian's
scans (CC0; poison_b_el.bones), weathered a season or two.

p1 (a white-tailed deer's skull at the troop's right, 5.5 m off, life size, in the shade): in the frame a pale scrap
about 90 x 30 px that "could pass for a bleached bit of bark or bone"; only a 3x crop showed a skull. p2 (the skull a
big buck's, 1.25 x, forward in front of the speaker's left foot, side on, in the forest's one sun fleck, paler): at
600 px still "a small whitish object ... might be a bone or a small skull ... could just as easily be fungus"; and all
four critics found it placed, not found: "spotless, bone-white and crisp, resting on top of the dirt dead centre in
front of the box, with no staining or moss, no leaf litter over it and no partial burial". Both duels kept G4 (6-7,
6-6), each calling G5 the deadlier. (Two strews of the skull's own, moss and litter round it, had taken p1's proof past
the helpers' 15 GB: each strew on this ground costs about 3 GB at Cycles' start. None here either.)

p3, the deer's remains rather than its skull, found rather than placed:
- what a wolf kill looks like a season on, over about 0.7 m of the open litter in front of the troop, left of the
  speaker, so the bones and the death caps read as one thing and the box's foot stays clear: the spine from the hips
  to the neck, which reaches the caps; the upper side's ribs fallen toward the lens in a row, each on its side (a rib
  on its side rests on its two ends, its curve arched up: an arc the lens sees whole); the lower side's flat under the
  moss; a leg bone dragged off (local looks without the forest: ribs strewn round the skull read as loops of root, a
  row of them off the spine as a ribcage);
- the skull pulled off the neck and turned back along the body, side on to the lens among the caps (its eye socket,
  its long snout), nose down in the litter to its teeth, the jaw upright beside it;
- all of it sunk into the litter, the moss and the bark of G4's own strews over and through it (p2 cleared the litter
  round the skull: it sat on bare dirt), only the branches kept off;
- the bone a dull, stained ivory, darker than p2's, the moss and algae on it heavier; the skull's top the palest;
- the sun fleck across the ribs, not centred on the skull, and a second fleck on the open floor at centre right,
  where the shafts would land (both realism critics: the shafts "land nowhere").
G4 otherwise whole, so the duel against G4 measures the remains.

p3's critics: at 600 px "looks like bleached bones, perhaps the remains of a small animal, though it could also be dead
pale roots"; told the brief ("green, but more obviously deadly"), both duels took p3 over G4 (5 v 6, 5 v 6 for realism):
"the bleached bones next to the pale mushrooms suggest something was poisoned here", but both had the bones "too bright
and clean ... on top of the leaf litter instead of in it: stain, darken and partly bury them". The proof also showed the
jaw run into the back of the skull. Both realism critics also found the skeleton "tidy", "a neat, still-joined
line". So p4: the bone mottled from p3's pale to two steps darker (darker all over, a local look, made the ribs read as
sticks), the stains and pits deeper, mossier; every bone sunk 1-2 cm deeper; the troop's own moss and bark strews (G4's
seeds 300 and 400) moved over the bones and thickened; a vertebra knocked off the line (a rib dragged off the row and dropped flat read as a stick);
the jaw 12 cm clear of the skull.
"""
import copy
import math

import poison as A
import poison_g4 as G4

VIEW = 108.0                    # the lens's heading on the floor (degrees from +x): across the view is 18
BONE = [(0.3, '#C2B79B'), (0.48, '#A69A7C'), (0.6, '#8B8064'), (0.72, '#6E6650')]     # pale to stained: mottled
BRANCH_CLEAR = [(-0.2, -1.66, 0.45)]                                 # no strewn branch through the bones (x, y, r)
FLECKS = [(-0.26, -1.72, 0.02, 0.16), (0.95, -0.7, 0.0, 0.18)]       # canopy holes' spots: across the ribs; open floor
LITTER = {300: ((-0.15, -1.56, 0.6), 6500), 400: ((-0.15, -1.6, 0.62), 140.0)}   # G4's troop strews (seed: within, density),
                                                                    # moved over the bones and thickened


def _euler(cx, cy, cz):
    """XYZ Euler degrees for the rotation taking a scan's own x, y and z axes to cx, cy, cz."""
    r = [[cx[i], cy[i], cz[i]] for i in range(3)]
    a = math.atan2(r[2][1], r[2][2]); b = math.asin(max(-1.0, min(1.0, -r[2][0]))); c = math.atan2(r[1][0], r[0][0])
    return [round(math.degrees(v), 2) for v in (a, b, c)]


def _cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def _flat(yaw):
    return [math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0.0]


def _tilt(yaw, deg):
    """Up (0, 0, 1) leaned `deg` about the horizontal heading `yaw`."""
    side = _cross(_flat(yaw), [0, 0, 1]); t = math.radians(deg)
    return [math.sin(t) * side[0], math.sin(t) * side[1], math.cos(t)]


def rib(x, y, yaw, lean=0.0, scale=2.0, sink=0.012, mirror=False, **w):
    """A rib on its side along `yaw`, resting on its two ends with its curve arched up, leaned `lean` off upright."""
    u = _flat(yaw); bow = _tilt(yaw, lean)
    return dict(part='rib', position=[x, y, 0.0], rotate=_euler(bow, u, _cross(bow, u)), scale=scale, sink=sink,
                mirror=mirror, **w)


def vertebra(part, x, y, yaw, roll=0.0, scale=1.5, sink=0.02, **w):
    """A vertebra, its body along `yaw`, its spine rolled `roll` off straight up (90: on its side)."""
    u = _flat(yaw); s = _tilt(yaw, roll)
    return dict(part=part, position=[x, y, 0.0], rotate=_euler(_cross(s, u), s, u), scale=scale, sink=sink, **w)


def long_bone(part, x, y, yaw, roll=0.0, scale=1.0, sink=0.015, **w):
    """A leg bone lying along `yaw` (the scan's long axis: y for the foreleg, z for the humerus), rolled `roll`."""
    u = _flat(yaw); up = _tilt(yaw, roll)
    if part == 'humerus':
        cx, cz = up, u
        cy = _cross(cz, cx)
    else:
        cx, cy = up, u
        cz = _cross(cx, cy)
    return dict(part=part, position=[x, y, 0.0], rotate=_euler(cx, cy, cz), scale=scale, sink=sink, **w)


def skull(part, x, y, yaw, roll=0.0, pitch=0.0, scale=1.2, sink=0.03, **w):
    """The skull (or jaw), its snout heading `yaw` and dipped `pitch` (degrees, + nose down), rolled `roll`."""
    f = _flat(yaw); p = math.radians(pitch)
    f = [f[0] * math.cos(p), f[1] * math.cos(p), -math.sin(p)]
    side = _cross(f, [0, 0, 1]); n = math.sqrt(sum(v * v for v in side)); side = [v / n for v in side]
    up = _cross(side, f)
    t = math.radians(roll)
    crown = [math.cos(t) * up[i] + math.sin(t) * side[i] for i in range(3)]
    cy = [-v for v in f]                                             # the scan's snout is to -y
    return dict(part=part, position=[x, y, 0.0], rotate=_euler(_cross(cy, crown), cy, crown), scale=scale, sink=sink,
                **w)


SPINE = ((-0.42, -1.84), (-0.12, -1.52))    # the deer's back, its hips (front left) to its neck, among the death caps


def remains(dx=0.0, dy=0.0, leg=True):
    """The deer as wolves and a season left it: the spine across the litter from its hips (front left) to its neck,
    which reaches the troop; the ribs of its upper side fallen toward the lens, parallel, on their sides (each arched
    from its head at the spine to its tip in the litter), those of its lower side flat under the moss behind; the
    skull pulled off the neck and turned back along the body, side on to the lens among the caps, its jaw beside it;
    a leg bone dragged off to the front. Headings in degrees on the floor; across the view is 18, toward the lens 288."""
    (x0, y0), (x1, y1) = [(x + dx, y + dy) for x, y in SPINE]
    yaw = math.degrees(math.atan2(y1 - y0, x1 - x0))

    def at(t, off=0.0, side=-90.0):                                 # a point t of the way up the spine, off to a side
        d = _flat(yaw + side)
        return round(x0 + (x1 - x0) * t + d[0] * off, 3), round(y0 + (y1 - y0) * t + d[1] * off, 3)

    out = [vertebra('lumbar', *at(0.06), yaw, roll=70.0, scale=1.45, sink=0.04, seed=1),
           vertebra('thoracic', *at(0.3), yaw + 6.0, roll=40.0, sink=0.035, seed=2),
           vertebra('thoracic', *at(0.46, 0.09, 90.0), yaw - 40.0, roll=85.0, sink=0.035, seed=3),   # knocked off
           vertebra('thoracic', *at(0.62), yaw + 10.0, roll=30.0, sink=0.035, seed=4),
           vertebra('cervical', *at(0.86), yaw - 14.0, roll=60.0, sink=0.035, seed=5)]
    # the upper side's ribs, heads at the spine, tips toward the front right; centre half a rib out from the head
    for k, (t, out_yaw, lean, sc, sink) in enumerate([(0.14, -34.0, 8.0, 1.9, 0.028), (0.26, -31.0, 12.0, 2.1, 0.024),
                                                      (0.38, -28.0, 6.0, 2.2, 0.03), (0.5, -25.0, 10.0, 2.1, 0.024),
                                                      (0.62, -22.0, 4.0, 1.9, 0.028)]):
        d = _flat(out_yaw); half = 0.062 * sc
        hx, hy = at(t, 0.035)
        out.append(rib(round(hx + d[0] * half, 3), round(hy + d[1] * half, 3), out_yaw + 180.0, lean=lean, scale=sc,
                       sink=sink, mirror=bool(k % 2), seed=6 + k))
    # the lower side's, flat and sunk, pointing back left under the moss
    for k, (t, out_yaw, sc) in enumerate([(0.3, 150.0, 2.0), (0.5, 160.0, 2.1)]):
        d = _flat(out_yaw); half = 0.062 * sc
        hx, hy = at(t, 0.035, 90.0)
        out.append(rib(round(hx + d[0] * half, 3), round(hy + d[1] * half, 3), out_yaw + 180.0, lean=86.0, scale=sc,
                       sink=0.016, seed=11 + k))
    out += [skull('skull', x1 + 0.13, y1 + 0.02, VIEW + 90.0 + 15.0, roll=-12.0, pitch=8.0, scale=1.2, sink=0.05,
                  moss=1.6, seed=13),
            skull('jaw', x1 + 0.42, y1 - 0.16, VIEW + 90.0 + 30.0, roll=12.0, scale=1.2, sink=0.03, seed=14),
            long_bone('humerus', x0 - 0.12, y0 - 0.06, -10.0, roll=20.0, scale=1.25, sink=0.03, seed=15)]
    return out if leg else out[:-1]


def shot(dx=0.0, dy=0.0, leg=True):
    """G4 with the remains, moved by (dx, dy) and their fleck with them (the portrait's narrower frame)."""
    s = copy.deepcopy(G4.shot())
    props = s['set']['props']
    for p in props:
        if p.get('fn') == 'strew' and p.get('seed') in LITTER:          # the troop's moss and bark over the bones
            (x, y, r), dens = LITTER[p['seed']]
            p['within'], p['density'] = [x + dx, y + dy, r], dens
        if p.get('fn') == 'strew' and p.get('model') == 'dry_branches_medium_01':
            p['avoid'] = p.get('avoid', []) + [[x + dx, y + dy, r] for x, y, r in BRANCH_CLEAR]
        elif p.get('fn') == 'canopy':                                # G4's fleck, the last hole, onto the ribs; one more
            spots = [(FLECKS[0][0] + dx, FLECKS[0][1] + dy) + FLECKS[0][2:]] + FLECKS[1:]
            p['holes'] = p['holes'][:-1] + [A.gap_for(x, y, z, r, (0.0, 4.0), A.SUN_A2) for x, y, z, r in spots]
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'poison_b_el', 'fn': 'bones', 'position': [0, 0, 0],
                  'bone': BONE, 'streaks': 0.85, 'pits': 0.35, 'algae': 1.0, 'moss': 1.5, 'soil': 0.04,
                  'items': remains(dx, dy, leg)})
    s['title'] = 'barkhorn, Poison G5, the wood\'s poisons green, a deer\'s remains among the death caps'
    return s


def portrait():
    """The 4:5 frame is 1.6 m across where the remains lie: they move 0.3 m right and 0.18 m back into it, the leg bone
    left out, the skull at the speaker's left foot."""
    s = shot(0.3, 0.18, leg=False)
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
