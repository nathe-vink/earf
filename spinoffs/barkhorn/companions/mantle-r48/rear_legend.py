"""The rear plate's legends as a texture (2026-11-20): white on black, the plate seen from behind, at the CAD's own
positions (strata_rear.py's plate(), without the holes and dimensions), 20 px a mm, for v3_day.py --rear-legend.

    .venv-fab/bin/python rear_legend.py      (writes out-strata-v3/render/rear-legend.png)
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import strata_rear as S

X = S.X; X0, X1, PZ0, PZ1 = S.X0, S.X1, S.PZ0, S.PZ1
w, h = X1 - X0, PZ1 - PZ0
fig = plt.figure(figsize=(w / 25.4 * 2, h / 25.4 * 2), dpi=25.4 * 10)   # 20 px a mm
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(X0, X1); ax.set_ylim(PZ0, PZ1); ax.axis('off')
fig.patch.set_facecolor('black')
u = lambda x: X1 + X0 - x
pt = 72 / 25.4   # points a mm
for name, x, z, hole, do, *_ in X.REAR_HW:
    ax.text(u(x), z + (7.5 if z > 45 else -7.5), name, fontsize=2.0 * pt, ha='center', va='center', family='DejaVu Sans', color='w')
for i, line in enumerate(S.RATING):
    ax.text((X0 + X1) / 2, S.b1 - 2.4 - 3.4 * i, line, fontsize=1.6 * pt, ha='center', va='center', family='DejaVu Sans Mono', color='w')
out = os.path.join(S.HERE, 'out-strata-v3', 'render', 'rear-legend.png')
fig.savefig(out, facecolor='black'); print('wrote', out, f'{w:.1f} x {h:.1f} mm')
