"""V12 (V12-1(k)): the splice corner as redrawn, cut from crystal.py's solids (today's top: its cables lie on x), with the
room the site work needs, as fixings_check.py tests it: the PH1 screwdriver (Ø6 shaft 75, Ø32 handle 100) and a hand (Ø72)
on each strap screw from the front (-y), tipped 5 deg at the upper one, under the ceiling (z 50 outside the box's Ø101.6);
each splice's levers opened (17 overall + 2); the room under the levers' noses over the shelf's edge; each conductor's path
up into its entry. Heights above the canopy's underside; the canopy is tied 10 to 15 cm below during this work, so it is
drawn but not in the way. Writes canopy-v12-section.png here.
    .venv-fab/bin/python renders/2026-11-25/barkhorn/lamp-site/v12/section_v12.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, *(['..'] * 5))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'companions')); sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import crystal as C
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from build123d import Box, Pos

NAME = {'canopy': 'canopy', 'strap': 'mounting plate', 'tray-wall': 'tray, outer wall', 'tray-u': 'tray, U', 'driver': 'driver + its leads',
        'cord': 'cord + its conductors', 'cord-clamp': 'the two straps', 'clamp-screws': 'strap screws', 'relief-bracket': 'clamp channel (+ its PEM nuts)',
        'splices': 'two WAGO 221-412 (13.2 x 8.6 x 18.8)', 'splice-shelf': 'the shelf (welded)', 'ties': 'ties', 'lead-sleeve': 'glass-fibre sleeve', 'canopy-bushing': 'floor grommet', 'canopy-studs': 'PEM studs, Ø8 serrated nuts, driver screws',
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
from matplotlib.patches import Polygon
import math
def tool(ax, zs, tip, label=True):
    t = math.radians(tip)
    def P(d, off):                                  # a point d along the tool from the head, off across it (in the y-z plane)
        return (-1.45 - d * math.cos(t) - off * math.sin(t), zs - d * math.sin(t) + off * math.cos(t))
    for d0, d1, r, c, lab in ((0, 75, 3, '#d62728', 'PH1 shaft Ø6 x 75'), (75, 175, 16, '#9467bd', 'handle Ø32'), (85, 175, 36, '#8c564b', 'hand Ø72')):
        ax.add_patch(Polygon([P(d0, -r), P(d1, -r), P(d1, r), P(d0, r)], closed=True, fc=c, alpha=0.12, ec=c, ls='--', lw=1.1))
        if label:
            x_, y_ = P((d0 + d1) / 2, r + 2); ax.text(x_, y_, lab + f' (z {zs:g}, tipped {tip:g})', color=c, fontsize=9, ha='center')
def ceiling(ax):
    ax.add_patch(Rectangle((-400, 50), 400 - 50.8, 8, fc='#7f7f7f', alpha=0.35, ec='none'))
    ax.text(-178, 52, 'ceiling (z 50, outside the box\'s Ø101.6)', fontsize=10)
# 1: cut at x 8 along y: the strap screws, the screwdriver, its handle and a hand, the ceiling
a = axs[0]; cut(a, 'x', 8.0, (-185, 30), (-30, 62), 'cut at x 8 (the strap screws): PH1 from the front, its handle and a hand, under the ceiling')
tool(a, 10.0, 0.0, label=False); tool(a, 17.0, 5.0); ceiling(a)
a.set_xlabel('y, mm'); a.set_ylabel('z above the canopy\'s underside, mm')
# 2: cut at x 1.4 along y: splice A, the + conductor's fold behind the web, the shelf, the levers' room, the noses
a = axs[1]; cut(a, 'x', 1.4, (-20, 32), (14, 52), 'cut at x 1.4 (splice A): the levers\' room (17 + 2), the noses over the shelf\'s edge, the conductor\'s fold')
room(a, 13.2, 27.6, 4.6 + 19.0 - 13.2, 18.8, 'levers open: 17 overall + 2', c='#1f77b4')
room(a, 10.8, 23.6, 4.4, 4.0, 'under the noses', c='#2ca02c')
a.set_xlabel('y, mm'); a.set_ylabel('z above the canopy\'s underside, mm')
# 3: cut at y 8.9 along x: the splices on the shelf, each conductor and LED lead straight up into its entry
a = axs[2]; cut(a, 'y', 8.9, (-12, 36), (14, 52), 'cut at y 8.9 (the entries): A (-) and B (+) on the shelf; each wire straight up into its entry')
for xe in (2.25, 8.75, 15.85, 22.35):
    room(a, xe - 1.2, 23.6, 2.4, 4.0, '', c='#2ca02c')
a.text(-11, 21.5, 'green: each wire\'s last 4 straight up into its entry (inner: the cord; outer: the LED leads)', color='#2ca02c', fontsize=10)
a.set_xlabel('x, mm'); a.set_ylabel('z above the canopy\'s underside, mm')
# 4: plan at z 37.6 (the ties): the splices' tie through the web, the LED leads' slack loops tied through the lip
a = axs[3]; cut(a, None, 37.6, (-20, 40), (-25, 25), 'plan at z 37.6: the splices\' tie through the web; the LED leads\' slack loops tied through the lip', plan=True)
a.set_xlabel('x (the cables\' line), mm'); a.set_ylabel('y, mm')
fig.legend(list(seen.values()), list(seen.keys()), loc='lower center', ncol=8, fontsize=11, frameon=False)
fig.suptitle('Hemisphere V12: the splice corner redrawn (the shelf, the studs behind the cord, the splices tied), cut from the CAD\'s solids, with the site work\'s room', fontsize=15, x=0.01, ha='left')
plt.subplots_adjust(bottom=0.07, top=0.93, hspace=0.22)
out = os.path.join(HERE, 'canopy-v12-section.png'); plt.savefig(out, dpi=60, bbox_inches='tight'); print(out, os.path.getsize(out))
