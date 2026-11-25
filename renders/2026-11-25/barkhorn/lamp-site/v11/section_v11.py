"""V11 (V11-1(f)): the canopy's new cord corner cut from crystal.py's solids (today's top: its cables lie on x), with the room
the site work needs drawn in: the screwdriver (Ø6 x 120) along each strap screw, from the front (-y), and each lever splice's
levers opened (15.3 tall, so 7.1 in front of the lever face). Heights above the canopy's underside; the canopy is tied 10 to
15 cm below during this work, so it is drawn but not in the way. Writes canopy-v11-section.png here.
    .venv-fab/bin/python renders/2026-11-25/barkhorn/lamp-site/v11/section_v11.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, *(['..'] * 5))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'companions')); sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import crystal as C
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from build123d import Box, Pos

NAME = {'canopy': 'canopy', 'strap': 'mounting plate', 'tray-wall': 'tray, outer wall', 'tray-u': 'tray, U', 'driver': 'driver + its leads',
        'cord': 'cord + its conductors', 'cord-clamp': 'the two straps', 'clamp-screws': 'strap screws', 'relief-bracket': 'clamp channel (+ its PEM nuts)',
        'splices': 'two WAGO 221-412', 'canopy-bushing': 'floor grommet', 'canopy-studs': 'PEM studs, nuts, driver screws',
        'tray-screws': 'tray joint screws', 'box-screws': 'box screws', 'ground-screw': 'green screw', 'grippers': 'grippers',
        'gripper-brackets': 'gripper brackets', 'suspension': 'cables'}
COL = dict(zip(NAME, plt.cm.tab20.colors + plt.cm.tab20b.colors))
ps = {q.name: q.solid for q in C.north_parts(dict(C.V3)) if q.solid is not None}
zc = ps['canopy'].bounding_box().min.Z
fig, axs2 = plt.subplots(2, 2, figsize=(26, 18)); axs = list(axs2.flat)
seen = {}
def cut(ax, axis, at, xr, zr, title, plan=False):
    if plan:
        slab = Pos(0, 0, zc + at) * Box(400, 400, 0.2)
    else:
        slab = Pos(0, at, zc + 40) * Box(400, 0.2, 200) if axis == 'y' else Pos(at, 0, zc + 40) * Box(0.2, 400, 200)
    for n in NAME:
        if n not in ps:
            continue
        try:
            sec = ps[n] & slab
        except Exception:                          # noqa: BLE001
            continue
        if sec is None:
            continue
        for e in sec.edges():
            pts = [e.position_at(i / 12) for i in range(13)]
            if plan:
                if abs(pts[0].Z - pts[-1].Z) > 0.01:
                    continue
                xs, ys = [p.X for p in pts], [p.Y for p in pts]
            else:
                xs, ys = [p.X if axis == 'y' else p.Y for p in pts], [p.Z - zc for p in pts]
            ln, = ax.plot(xs, ys, color=COL[n], lw=1.4); seen[NAME[n]] = ln
    ax.set_xlim(*xr); ax.set_ylim(*zr); ax.set_aspect('equal'); ax.grid(alpha=.2); ax.set_title(title, fontsize=13)
def room(ax, x0, y0, w, h, label, c='#d62728'):
    ax.add_patch(Rectangle((x0, y0), w, h, fc=c, alpha=0.15, ec=c, lw=1.2, ls='--'))
    ax.text(x0 + 1, y0 + h + 1, label, color=c, fontsize=10)
# 1: plan at z 17 (the upper strap's screw): the screwdriver's path along y from the front
a = axs[0]; cut(a, None, 17.0, (-80, 80), (-80, 80), 'plan at z 17 (the upper strap): the screwdriver from the front (-y)', plan=True)
room(a, 5.0, -121.4 + 60, 6.0, 60.0 - 1.45, 'screwdriver Ø6 (120 long; drawn to y -61)')
a.set_xlabel('x (the cables\' line), mm'); a.set_ylabel('y, mm')
# 2: cut at x 8 along y: the straps' screws, their nuts in the web, the screwdriver
a = axs[1]; cut(a, 'x', 8.0, (-70, 40), (-4, 56), 'cut at x 8 (through the strap screws): the screwdriver along each, from y -1.4')
for zs in (10.0, 17.0):
    room(a, -61.0, zs - 3.0, 61.0 - 1.45, 6.0, f'screwdriver at z {zs:g}' if zs == 17.0 else '')
a.set_xlabel('y, mm'); a.set_ylabel('z above the canopy\'s underside, mm')
# 3: cut at x 3.5 along y: splice A, its lever's swing, the ledge, the top flange
a = axs[2]; cut(a, 'x', 3.5, (-20, 40), (-4, 56), 'cut at x 3.5 (splice A): its levers opened, 7.1 in front of the lever face')
room(a, 12.85, 28.5, 19.9 - 12.85, 46.8 - 28.5, 'lever swing (15.3 open)', c='#1f77b4')
a.set_xlabel('y, mm'); a.set_ylabel('z above the canopy\'s underside, mm')
# 4: cut at y 8.7 along x: the splices standing on the ledge, the conductors and LED leads up through its notches
a = axs[3]; cut(a, 'y', 8.7, (-45, 45), (-4, 56), 'cut at y 8.7 (through the splices\' entries): A (-) and B (+) on the ledge')
a.set_xlabel('x, mm'); a.set_ylabel('z above the canopy\'s underside, mm')
fig.legend(list(seen.values()), list(seen.keys()), loc='lower center', ncol=9, fontsize=11, frameon=False)
fig.suptitle('Hemisphere V11: the cord corner (two straps, two lever splices in the clamp\'s channel), cut from the CAD\'s solids, with the site work\'s room', fontsize=15, x=0.01, ha='left')
plt.subplots_adjust(bottom=0.07, top=0.93, hspace=0.22)
out = os.path.join(HERE, 'canopy-v11-section.png'); plt.savefig(out, dpi=60, bbox_inches='tight'); print(out, os.path.getsize(out))
