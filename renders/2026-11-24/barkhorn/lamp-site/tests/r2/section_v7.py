"""The hanging in section (v7, the v6 check's (12), 2026-11-24): top A cut through the cables' plane (y = 0) at the canopy
and at the lamp's top, and the canopy cut across it (x = 0) for the set screws and the box's screws. Plain names, the
legend outside the plot, the key sizes marked. Run with the CAD venv: .venv-fab/bin/python .../r2/section_v7.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, *(['..'] * 6))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'companions')); sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import crystal as C
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from build123d import Box, Pos
from build123d import Rot
A0 = C.TOP_TIERS['A'].get('cables', C.GRIP['cables'])[0]       # A's cables at 105/285 deg: turned onto x before the cuts
ps = {q.name: Rot(0, 0, -A0) * q.solid for q in C.north_parts(dict(C.V3, top='A')) if q.solid is not None}
NAME = {'canopy': 'canopy', 'strap': 'mounting plate', 'gripper-brackets': 'gripper brackets', 'grippers': 'grippers + safety nuts',
        'gripper-nuts': 'M10 nuts', 'bracket-rivets': 'rivets', 'canopy-screws': 'set screws + clinch nuts', 'box-screws': 'box screws',
        'enclosure': 'driver enclosure', 'driver': 'driver', 'suspension': 'cables + stop sleeves', 'cord': 'cord', 'hub': 'hub',
        'crown': 'crown', 'gland': 'cap', 'grip': 'cord grip', 'crown-screws': 'crown screws', 'collar': 'collar', 'ring': 'PEEK ring',
        'plunger': 'detent plunger', 'lock': 'lock (GN 617)', 'cap-key': 'cap dowel + magnet', 'white-disc': 'white disc',
        'white-paint': 'white paint', 'clamp': 'clamp ring', 'pins': 'pins'}
COL = dict(zip(NAME, plt.cm.tab20.colors + plt.cm.tab20b.colors))
fig, axs = plt.subplots(1, 4, figsize=(30, 9))
views = (('y', (690, 785, -80, 80), 'the canopy, cut through the cables (their line turned onto x)'),
         ('x', (690, 785, -80, 80), 'the canopy, cut across them (x = 0): the set screws, the box screws'),
         ('y', (55, 132, -45, 45), 'the top, cut through the cables and the lock (at 105 deg, turned onto +x)'))
seen = {}
for ax, (cut, (z0, z1, h0, h1), title) in zip(axs[:3], views):
    slab = Box(400, 0.2, z1 - z0 + 20) if cut == 'y' else Box(0.2, 400, z1 - z0 + 20)
    for n in NAME:
        if n not in ps:
            continue
        sec = ps[n] & (Pos(0, 0, (z0 + z1) / 2) * slab)
        for e in sec.edges():
            pts = [e.position_at(i / 12) for i in range(13)]
            h = [p.X if cut == 'y' else p.Y for p in pts]
            ln, = ax.plot(h, [p.Z for p in pts], color=COL[n], lw=0.9)
            seen[NAME[n]] = ln
    ax.set_xlim(h0, h1); ax.set_ylim(z0, z1); ax.set_aspect('equal'); ax.grid(alpha=.2); ax.set_title(title, fontsize=11)
    ax.set_xlabel(('x' if cut == 'y' else 'y') + ', mm'); ax.set_ylabel('z above the rim, mm')
a0, a1, a2, a3 = axs
a0.annotate('gripper at r 48', (48, 736), (52, 704), arrowprops=dict(arrowstyle='->'), fontsize=9)
a0.annotate('floor 3 thick, Ø3 holes', (-48, 727.5), (-78, 700), arrowprops=dict(arrowstyle='->'), fontsize=9)
a0.annotate('M10 nut, 16 AF', (48, 750), (55, 765), arrowprops=dict(arrowstyle='->'), fontsize=9)
a1.annotate('M4 set screw into clinch nut', (68, 770), (20, 700), arrowprops=dict(arrowstyle='->'), fontsize=9)
a1.annotate('8-32 box screw, y 44.45', (44.45, 773), (-75, 700), arrowprops=dict(arrowstyle='->'), fontsize=9)
a2.annotate('stop sleeve in Ø5.6 x 8 counterbore', (16, 63), (-40, 57.5), arrowprops=dict(arrowstyle='->'), fontsize=9)
a2.annotate('cable Ø1.59 in Ø2.4, r 16', (16, 90), (20, 75), arrowprops=dict(arrowstyle='->'), fontsize=9)
# the plan from above: A's top, the lock's knob at 105 deg, the level views' camera, a hand's path to the knob
import math
from matplotlib.patches import Circle, FancyArrowPatch
for d_, c_ in ((200, '#bbbbbb'), (104, '#666666'), (80, '#333333'), (56, '#222222')):
    a3.add_patch(Circle((0, 0), d_ / 2, fill=False, color=c_, lw=1.0))
la = math.radians(C.GRIP['lock']['angle'])
u = (math.cos(la), math.sin(la)); v = (-u[1], u[0])
for r0, r1, w in ((52, 66, 10), (66, 81.3, 21.1)):
    xs = [r0 * u[0] + w / 2 * v[0], r1 * u[0] + w / 2 * v[0], r1 * u[0] - w / 2 * v[0], r0 * u[0] - w / 2 * v[0]]
    ys = [r0 * u[1] + w / 2 * v[1], r1 * u[1] + w / 2 * v[1], r1 * u[1] - w / 2 * v[1], r0 * u[1] - w / 2 * v[1]]
    a3.fill(xs, ys, color=COL['lock'], alpha=0.9)
ca = math.atan2(-1.442, 0.693)
a3.add_patch(FancyArrowPatch((140 * math.cos(ca), 140 * math.sin(ca)), (105 * math.cos(ca), 105 * math.sin(ca)), arrowstyle='->', mutation_scale=15))
a3.text(140 * math.cos(ca) + 4, 140 * math.sin(ca), 'the level views\' camera', fontsize=9)
hp = [(150 * math.cos(la + 0.5), 150 * math.sin(la + 0.5)), (115 * math.cos(la + 0.15), 115 * math.sin(la + 0.15)), (84 * u[0], 84 * u[1])]
a3.plot([q[0] for q in hp], [q[1] for q in hp], '--', color='#c00000', lw=1.5)
a3.annotate('a hand over the shade from behind: pull the knob 5', hp[-1], (hp[0][0] - 60, hp[0][1] + 8), fontsize=9, color='#c00000',
            arrowprops=dict(arrowstyle='->', color='#c00000'))
a3.set_xlim(-160, 160); a3.set_ylim(-160, 160); a3.set_aspect('equal'); a3.grid(alpha=.2)
a3.set_title('A from above (true angles): the lock\'s knob at 105 deg, the cables at 105/285, the level views\' camera', fontsize=11)
for ca_ in (105, 285):
    a3.plot([16 * math.cos(math.radians(ca_)), 48 * math.cos(math.radians(ca_))], [16 * math.sin(math.radians(ca_)), 48 * math.sin(math.radians(ca_))], color=COL['suspension'], lw=1.2)
a3.set_xlabel('x, mm'); a3.set_ylabel('y, mm')
fig.legend(list(seen.values()), list(seen.keys()), loc='lower center', ncol=9, fontsize=9, frameon=False)
plt.subplots_adjust(bottom=0.14)
out = os.path.join(HERE, 'v7-hanging-section.png'); plt.savefig(out, dpi=80, bbox_inches='tight'); print(out)
