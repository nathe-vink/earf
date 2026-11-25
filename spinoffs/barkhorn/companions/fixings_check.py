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
       'tray-screws', 'canopy-studs', 'relief-bracket', 'cord-clamp', 'clamp-screws'}


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
# V11-1(g) (the V10 check): the work done on site, with the canopy tied down below (so the canopy, its grommet and its set
# screws are left out): a screwdriver (Ø6 x 120) along each of the cord clamp's screws from its head, and each lever splice's
# levers opened (WAGO 221-412: 8.2 closed, 15.3 open, so 7.1 more in front of the lever face). Each must hit nothing.
from geom import box as _box, cyl as _cyl
OUT = {'canopy', 'canopy-bushing', 'canopy-screws'}
for top in (None, 'A', 'B'):
    p = dict(C.V3, top=top) if top else dict(C.V3)
    parts = {q.name: q.solid for q in C.north_parts(p) if q.solid is not None}
    tt_ = C.TOP_TIERS['A' if top == 'A' else 'B' if top == 'B' else 'today']
    a0 = tt_.get('cables', C.GRIP['cables'])[0]
    zc = parts['canopy'].bounding_box().min.Z
    turn = (lambda sh: C.at(a0, sh)) if a0 else (lambda sh: sh)
    tools = [(f'screwdriver at the clamp screw z {zs:g}', turn(_cyl('y', (8.0, zc + zs), 6.0, -121.4, -1.45)), {'cord-clamp', 'clamp-screws'})
             for zs in (10.0, 17.0)]
    tools += [(f'splice {k} levers open', turn(_box(x0, 12.85, zc + 28.5, x1, 19.9, zc + 46.8)), {'splices'})
              for k, (x0, x1) in (('A', (-3.05, 10.05)), ('B', (10.55, 23.65)))]
    for label, tool, own in tools:
        hits = []
        for n, sh in parts.items():
            if n in OUT or n in own:
                continue
            i = tool & sh
            v = i.volume if i is not None else 0.0
            if v > 0:
                hits.append(f'{n} {v:.3f} mm3')
        print(f'{top or "today":6} {label}: ' + ('clear' if not hits else 'HITS ' + ', '.join(hits)))
        bad += 1 if hits else 0
print('fixings_check:', 'ok' if not bad else f'{bad} problem(s)')
sys.exit(1 if bad else 0)
