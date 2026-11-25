"""Hemisphere's top: every part against every other at zero tolerance (check 4 (20), 2026-11-24), and (V11) the site work's tool room.

fabkit's clash check skips overlaps under 1 mm3, so this checks the fixings on their own. v6 (the v5 check's (10)): the
tapped holes are drawn at the thread's major diameter and TOUCHING_DOME exempts no fixing, so no overlap is allowed at
all: any is a failure.

    .venv-fab/bin/python spinoffs/barkhorn/companions/fixings_check.py      (exit 1 on any other overlap)
"""
import itertools, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'studio', 'fabkit'))
import crystal as C

FIX = {'crown', 'gland', 'grip', 'crown-screws', 'cap-key', 'suspension', 'hub', 'grippers', 'gripper-brackets', 'cord',
       'canopy', 'strap', 'slip-washer', 'collar', 'pins', 'plunger', 'ring', 'gripper-nuts', 'bracket-studs', 'canopy-screws',
       'box-screws', 'white-paint', 'driver', 'lock', 'clamp', 'canopy-bushing', 'ground-screw', 'splices', 'tray-wall', 'tray-u',
       'tray-screws', 'canopy-studs', 'relief-bracket', 'cord-clamp', 'clamp-screws', 'splice-shelf', 'ties',
       'lead-sleeve'}


THREADS = {}

bad = 0
for top in (None, 'A', 'B'):
    p = dict(C.V3, top=top) if top else dict(C.V3)
    parts = {q.name: q.solid for q in C.north_parts(p) if q.solid is not None}
    for a, b in itertools.combinations(sorted(parts), 2):
        if not ({a, b} & FIX):
            continue
        try:
            i = parts[a] & parts[b]
            v = i.volume if i is not None else 0.0
        except Exception as e:                      # noqa: BLE001
            print(top or 'today', a, b, 'error', e); bad += 1; continue
        if v <= 0:
            continue
        exp = THREADS.get((a, b), 'no')
        if exp == 'no':
            print(f'{top or "today":6} CLASH {a}/{b} {v:.4f} mm3'); bad += 1
        else:
            ok = exp is None or 0.6 * exp <= v <= 1.4 * exp
            print(f'{top or "today":6} thread {a}/{b} {v:.1f} mm3' + ('' if exp is None else f' (expected {exp:.1f})')
                  + ('' if ok else '  OUT OF RANGE'))
            bad += 0 if ok else 1
# The site work's tool room (V11-1(g); V12-10). What this proves, and no more: solids drawn at the bought parts' datasheet
# sizes (WAGO 221-412 at WAGO's 2023 13.2 x 8.6 x 18.8; the stud nuts' Ø8 flanges) leave these volumes empty, with the
# canopy tied down below (so the canopy, its grommet and its set screws are left out):
#  - the named screwdriver (PH1, ISO 7045 M3; a Ø6 shaft 75 long, a Ø32 handle 100 long) on each strap screw's axis from
#    its head, worked from -y, tipped 5 deg handle-down at the upper screw, and a hand round its handle (Ø72 x 90);
#  - a ceiling at the plate's top (z 50) outside a 4 in box's Ø101.6 opening;
#  - each splice's levers opened: WAGO's sheet gives 17 overall open (K007's outline 15.3), so a box from the lever face
#    to 17 + 2 from the splice's back, its whole width and height (the tie round them cut first);
#  - room under each splice's lever noses in front of the shelf (4 below, 4.4 out), for a nail or a small blade;
#  - each conductor's straight run, Ø2.4, the last 4 up into its entry.
# It does not prove a hand reaches, a lever's real sweep (WAGO's 3D model is not in the repo) or a blind insertion:
# those are the hand mock-up's (prototype list).
from geom import box as _box, cyl as _cyl
from build123d import Solid, Plane, Vector
def _rod(p0, p1, d):
    a, b = Vector(*p0), Vector(*p1)
    return Solid.make_cylinder(d / 2, (b - a).length, Plane(origin=a, z_dir=(b - a)))
OUT = {'canopy', 'canopy-bushing', 'canopy-screws'}
for top in (None, 'A', 'B'):
    p = dict(C.V3, top=top) if top else dict(C.V3)
    parts = {q.name: q.solid for q in C.north_parts(p) if q.solid is not None}
    tt_ = C.TOP_TIERS['A' if top == 'A' else 'B' if top == 'B' else 'today']
    a0 = tt_.get('cables', C.GRIP['cables'])[0]
    zc = parts['canopy'].bounding_box().min.Z
    turn = (lambda sh: C.at(a0, sh)) if a0 else (lambda sh: sh)
    LZ, EY = 27.6, 8.9
    tools = []
    for zs, tip in ((10.0, 0.0), (17.0, 5.0)):
        t_ = math.radians(tip); h0 = (8.0, -1.45, zc + zs)
        pt = lambda d: (8.0, -1.45 - d * math.cos(t_), zc + zs - d * math.sin(t_))
        sd = _rod(h0, pt(75.0), 6.0) + _rod(pt(75.0), pt(175.0), 32.0)
        hand = _rod(pt(85.0), pt(175.0), 72.0)
        tools.append((f'PH1 screwdriver at the strap screw z {zs:g} (tipped {tip:g})', turn(sd), {'cord-clamp', 'clamp-screws'}))
        tools.append((f'hand on its handle, z {zs:g}', turn(hand), set()))
    ceil = _cyl('z', (0, 0), 800.0, zc + 50.0, zc + 60.0) - _cyl('z', (0, 0), 101.6, zc + 49, zc + 61)
    for (k, (x0, x1), ents) in (('A', (-1.1, 12.1), (2.25, 8.75)), ('B', (12.5, 25.7), (15.85, 22.35))):
        tools.append((f'splice {k} levers open (to 17 + 2)', turn(_box(x0, 13.2, zc + LZ, x1, 4.6 + 17.0 + 2.0, zc + LZ + 18.8)), {'splices', 'ties'}))
        tools.append((f'splice {k} noses (under, in front of the shelf)', turn(_box(x0 + 0.5, 10.8, zc + LZ - 4.0, x1 - 0.5, 15.2, zc + LZ)), set()))
        for xe in ents:
            tools.append((f'splice {k} entry x {xe:g}: straight run', turn(_cyl('z', (xe, EY), 2.4, zc + LZ - 4.0, zc + LZ)), {'cord', 'driver'}))
    hands = [t for t in tools if t[0].startswith('hand')]
    for label, tool, own in tools:
        hits = []
        for n, sh in parts.items():
            if n in OUT or n in own:
                continue
            i = tool & sh
            v = i.volume if i is not None else 0.0
            if v > 0:
                hits.append(f'{n} {v:.3f} mm3')
        if label.startswith('hand') or label.startswith('PH1'):
            i = tool & ceil
            if i is not None and i.volume > 0:
                hits.append(f'the ceiling {i.volume:.3f} mm3')
        print(f'{top or "today":6} {label}: ' + ('clear' if not hits else 'HITS ' + ', '.join(hits)))
        bad += 1 if hits else 0
print('fixings_check:', 'ok' if not bad else f'{bad} problem(s)')
sys.exit(1 if bad else 0)
