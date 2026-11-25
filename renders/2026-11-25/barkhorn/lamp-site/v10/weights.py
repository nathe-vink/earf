"""V10 weights (2026-11-25): what hangs from the two cables (every part of the lamp, with the stop sleeves and the cables
inside the lamp, below the cap's top at z 126; not the cord, which carries no load) and what the canopy weighs, for the
four packages, from crystal.py's solids. Densities: made parts from fabkit's SOLIDS; bought parts as listed below; the lock at Ganter's 24 g.
    HEMI_LOCK_ON=0 .venv-fab/bin/python renders/2026-11-25/barkhorn/lamp-site/v10/weights.py   (A without the lock)
    .venv-fab/bin/python renders/2026-11-25/barkhorn/lamp-site/v10/weights.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, *(['..'] * 5))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'companions')); sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import crystal as C
from model import SOLIDS, Machined, Bought
from build123d import Box, Pos
BOUGHT = {'pins': 8.0, 'plunger': 8.0, 'gaskets': 1.2, 'board': 2.7, 'grip': 8.5, 'crown-screws': 8.0, 'cap-key': 7.8,
          'white-paint': 1.5, 'slip-washer': 2.2, 'vent': 1.0, 'lock': 7.8, 'suspension': 8.0, 'grippers': 7.8,
          'gripper-nuts': 7.9, 'bracket-studs': 7.8, 'canopy-screws': 7.8, 'box-screws': 7.8, 'driver': 1.9,
          'tray-screws': 7.8, 'canopy-studs': 7.8, 'lead-bushing': 1.1, 'cord-clamp': 7.8, 'splices': 1.6,
          'canopy-bushing': 2.7, 'ground-screw': 7.8, 'cord': 1.4}
tops = [('today', None), ('A' + (' with the lock' if C.LOCK_ON else ' without the lock'), 'A')] + ([('B', 'B')] if C.LOCK_ON else [])
if not C.LOCK_ON:
    tops = [tops[1]]
for name, top in tops:
    p = dict(C.V3, top=top) if top else dict(C.V3)
    lamp = canopy = 0.0; mx = my = 0.0
    for q in C.north_parts(p):
        if q.solid is None:
            continue
        rho = SOLIDS[q.make.material]['density'] if isinstance(q.make, Machined) else BOUGHT.get(q.name)
        if rho is None:
            print('  no density for', q.name); continue
        if q.group == 'canopy':
            canopy += q.solid.volume / 1000 * rho
            continue
        sh = q.solid
        if q.name in ('suspension', 'cord'):
            if q.name == 'cord':
                continue
            sh = sh & (Pos(0, 0, 63) * Box(400, 400, 126))      # the cables and sleeves inside the lamp
        m = 24.0 if q.name == 'lock' else sh.volume / 1000 * rho      # the lock: Ganter's 24 g (the drawn one is fuller)
        c = sh.center()
        lamp += m; mx += m * c.X; my += m * c.Y
    off = ((mx / lamp) ** 2 + (my / lamp) ** 2) ** 0.5
    print(f'{name}: hangs {lamp:.0f} g ({lamp / 453.6:.2f} lb), its center {off:.2f} off the axis; the canopy and all in it {canopy:.0f} g; together {lamp + canopy:.0f} g')
