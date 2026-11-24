"""Hemisphere's top: every part against every other at zero tolerance (check 4 (20), 2026-11-24).

fabkit's clash check skips overlaps under 1 mm3 and crystal.py's TOUCHING_DOME exempts the fixings from it, so this
checks them on their own. The only overlaps allowed are a thread in its tapped hole (the thread is drawn at its major
diameter, the hole at its tap drill); each is listed with the volume that engagement should give.

    .venv-fab/bin/python spinoffs/barkhorn/companions/fixings_check.py      (exit 1 on any other overlap)
"""
import itertools, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'studio', 'fabkit'))
import crystal as C

FIX = {'crown', 'gland', 'grip', 'crown-screws', 'cap-key', 'suspension', 'tether', 'hub'}


def ring(d, t, L, n=1):                 # a thread's major Ø d in a tap drill Ø t, L engaged, n of them
    return n * math.pi * (d * d - t * t) / 4 * L


# thread pairs: the volume a thread in its tapped hole should overlap, ±40 % (the run-outs and chamfers)
THREADS = {('hub', 'suspension'): ring(6.35, 5.1, 12, 2), ('crown-screws', 'hub'): ring(2.5, 2.05, 6, 3),
           ('hub', 'pins'): ring(3.0, 2.5, 6, 3), ('hub', 'tether'): None, ('grip', 'hub'): None}

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
print('fixings_check:', 'ok' if not bad else f'{bad} problem(s)')
sys.exit(1 if bad else 0)
