"""V10 (T1, 2026-11-25): the canopy as it is now built, cut from crystal.py's solids (today's top: its cables lie on x).
Four views: cut across the cables' line through the cord (y = 0); cut along the tray through the driver (x = -21); cut
across the tray at its -y end (y = -55, the LED leads' bushing); from below (the parts' edges in plan). Heights above the
canopy's underside. Writes canopy-v10-section.png here.   .venv-fab/bin/python renders/2026-11-25/barkhorn/lamp-site/v10/section_v10.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, *(['..'] * 5))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'companions')); sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import crystal as C
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from build123d import Box, Pos

NAME = {'canopy': 'canopy', 'strap': 'mounting plate', 'tray-wall': 'tray, outer wall', 'tray-u': 'tray, U', 'driver': 'driver + its leads',
        'cord': 'cord + its conductors', 'cord-clamp': 'cord clamp (saddle, screws, nuts)', 'relief-bracket': 'clamp channel',
        'splices': 'two lever splices + carrier', 'lead-bushing': 'snap bushing (LED leads)', 'canopy-bushing': 'floor grommet',
        'canopy-studs': 'PEM studs + nuts', 'tray-screws': 'tray joint screws', 'box-screws': 'box screws', 'ground-screw': 'green screw',
        'grippers': 'grippers', 'gripper-brackets': 'gripper brackets', 'gripper-nuts': 'M10 nuts', 'bracket-studs': 'bracket studs',
        'suspension': 'cables', 'canopy-screws': 'set screws'}
COL = dict(zip(NAME, plt.cm.tab20.colors + plt.cm.tab20b.colors))
ps = {q.name: q.solid for q in C.north_parts(dict(C.V3)) if q.solid is not None}
cb = ps['canopy'].bounding_box(); zc, zt = cb.min.Z, cb.max.Z
fig, axs2 = plt.subplots(2, 2, figsize=(26, 17)); axs = list(axs2.flat)
seen = {}
VIEWS = (('y', 0.0, 'cut across the cables\' line through the cord (y = 0)'),
         ('x', -21.0, 'cut along the tray through the driver (x = -21)'),
         ('y', -55.0, 'cut across the tray\'s -y end (y = -55): the LED leads\' bushing'))
for ax, (cut, at, title) in zip(axs[:3], VIEWS):
    slab = Pos(0, at, (zc + zt) / 2) * Box(400, 0.2, 200) if cut == 'y' else Pos(at, 0, (zc + zt) / 2) * Box(0.2, 400, 200)
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
            ln, = ax.plot([p.X if cut == 'y' else p.Y for p in pts], [p.Z - zc for p in pts], color=COL[n], lw=1.3)
            seen[NAME[n]] = ln
    ax.set_xlim(-80, 80); ax.set_ylim(-4, 75); ax.set_aspect('equal'); ax.grid(alpha=.2)
    ax.set_title(title, fontsize=13); ax.set_xlabel(('x' if cut == 'y' else 'y') + ', mm'); ax.set_ylabel('z above the canopy\'s underside, mm')
a0 = axs[0]
a0.annotate('cord on the axis, clamped\n(saddle z 7 to 15)', (-3, 11), (-78, 62), arrowprops=dict(arrowstyle='->'), fontsize=10)
a0.annotate('two lever splices,\nz 28.5 to 46.8', (-2, 38), (-40, 68), arrowprops=dict(arrowstyle='->'), fontsize=10)
a0.annotate('driver on edge in its tray\n(120 V inside: tray + plate)', (-20, 30), (5, 62), arrowprops=dict(arrowstyle='->'), fontsize=10)
a0.annotate('green screw\n(in the box)', (20, 52), (40, 62), arrowprops=dict(arrowstyle='->'), fontsize=10)
axs[1].annotate('input leads up through the\nplate\'s Ø8 into the box', (36.5, 52), (-60, 64), arrowprops=dict(arrowstyle='->'), fontsize=10)
ax = axs[3]
for n in ('canopy', 'tray-wall', 'tray-u', 'driver', 'cord', 'relief-bracket', 'splices', 'gripper-brackets', 'strap', 'ground-screw', 'box-screws'):
    if n not in ps:
        continue
    zcut = zc + (2.0 if n == 'canopy' else 49.2 if n in ('strap', 'ground-screw', 'box-screws') else 30.0)
    try:
        sec = ps[n] & (Pos(0, 0, zcut) * Box(400, 400, 0.2))
    except Exception:                              # noqa: BLE001
        continue
    if sec is None:
        continue
    for e in sec.edges():
        pts = [e.position_at(i / 12) for i in range(13)]
        if abs(pts[0].Z - pts[-1].Z) < 0.01:
            ax.plot([p.X for p in pts], [p.Y for p in pts], color=COL[n], lw=1.0)
ax.set_xlim(-80, 80); ax.set_ylim(-80, 80); ax.set_aspect('equal'); ax.grid(alpha=.2)
ax.set_title('plan: the floor at z 2, the inside at z 30, the plate at z 49.2', fontsize=13); ax.set_xlabel('x (the cables\' line), mm'); ax.set_ylabel('y, mm')
fig.legend(list(seen.values()), list(seen.keys()), loc='lower center', ncol=11, fontsize=11, frameon=False)
fig.suptitle('Hemisphere V10: the canopy, 150 x 50, the cord on its axis (T1: the driver on edge in a steel tray beside it). From the CAD\'s solids, today\'s top.', fontsize=15, x=0.01, ha='left')
plt.subplots_adjust(bottom=0.08, top=0.93, hspace=0.25)
out = os.path.join(HERE, 'canopy-v10-section.png'); plt.savefig(out, dpi=60, bbox_inches='tight'); print(out, os.path.getsize(out))
