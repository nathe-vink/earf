"""The v6 hanging in section (the v5 check, 2026-11-24): top A cut through the cables' plane (y = 0), the canopy and the
lamp's top, each part in its own colour. Run with the CAD venv: .venv-fab/bin/python .../r2/section_v6.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, *(['..'] * 6))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'companions')); sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import crystal as C
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from build123d import Box, Pos
ps = {q.name: q.solid for q in C.north_parts(dict(C.V3, top='A')) if q.solid is not None}
col = {'canopy': '#444444', 'strap': '#cc6600', 'gripper-brackets': '#cc6600', 'grippers': '#0066cc', 'enclosure': '#008800',
       'driver': '#88aa88', 'suspension': '#dd0000', 'cord': '#aa00aa', 'hub': '#555555', 'crown': '#333333', 'gland': '#222222',
       'grip': '#bb8800', 'collar': '#777777', 'tether': '#00aaaa', 'cap-key': '#ff00ff', 'white-disc': '#999999', 'ring': '#aa5500',
       'clamp': '#666666'}
fig, axs = plt.subplots(1, 2, figsize=(16, 8.5))
for ax, (z0, z1, x0, x1) in zip(axs, ((690, 780, -80, 80), (55, 130, -45, 45))):
    for n, c in col.items():
        if n not in ps:
            continue
        sec = ps[n] & (Pos(0, 0, (z0 + z1) / 2) * Box(400, 0.2, z1 - z0 + 20))
        first = True
        for e in sec.edges():
            pts = [e.position_at(i / 12) for i in range(13)]
            ax.plot([p.X for p in pts], [p.Z for p in pts], color=c, lw=0.8, label=n if first else None); first = False
    ax.set_xlim(x0, x1); ax.set_ylim(z0, z1); ax.set_aspect('equal'); ax.grid(alpha=.2)
    ax.set_xlabel('x, mm'); ax.set_ylabel('z above the rim, mm')
axs[0].set_title('the canopy: grippers (blue) on brackets under the strap, plungers 1 above the floor\'s holes')
axs[1].set_title('the top: stop sleeves in the hub\'s counterbores, the cables up through hub, crown and cap')
axs[1].legend(loc='lower center', fontsize=7, ncol=4)
out = os.path.join(HERE, 'v6-hanging-section.png'); plt.savefig(out, dpi=90, bbox_inches='tight'); print(out)
