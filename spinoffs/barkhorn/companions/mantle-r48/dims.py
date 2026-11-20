"""Mantle's dimension drawing (the coordinator, 2026-11-20): line only, top and front, millimeters and inches, from the
CAD's own solids (out-strata-v3/stl, the files the current build wrote). Each view is a visible-line drawing: every
part group's silhouette is rasterized at 0.2 mm, the nearest group wins each pixel, and the boundaries between groups
are traced back to lines. Nothing is drawn that is not in the CAD (no record, no label).

    .venv-fab/bin/python dims.py        (writes drawings/mantle-dimensions.svg and .png)
"""
import glob, os, struct
import numpy as np
from PIL import Image, ImageDraw
import contourpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
STL = os.path.join(HERE, 'out-strata-v3', 'stl')
OUT = os.path.join(HERE, 'drawings')
RES = 0.2   # mm a pixel
# groups that read as one piece; the old lid, hinge and light files the build no longer writes are left out by date
GROUPS = [('deck', ('plinth-',)), ('base', ('base-',)), ('post', ('post-',)), ('feet', ('feet', 'foot-pads')),
          ('platter', ('platter', 'platter-hub', 'platter-screws')), ('spindle', ('spindle',)),
          ('arm', ('arm', 'cartridge')), ('puck', ('arm-puck',)), ('motor', ('pulley', 'motor', 'belt', 'motor-plate')),
          ('rear', ('rear-plate', 'rear-hardware')), ('cover', ('cover-top', 'cover-front', 'cover-back', 'cover-left', 'cover-right')),
          ('cover-feet', ('cover-feet',))]


def load(f):
    d = open(f, 'rb').read(); n = struct.unpack('<I', d[80:84])[0]
    a = np.frombuffer(d[84:84 + 50 * n], dtype=np.dtype([('n', '<3f4'), ('v', '<9f4'), ('a', '<u2')]))
    return a['v'].reshape(-1, 3, 3).astype(float)


fresh = os.path.getmtime(os.path.join(STL, 'plinth-L1.stl')) - 120
parts = {os.path.basename(f)[:-4]: load(f) for f in glob.glob(os.path.join(STL, '*.stl')) if os.path.getmtime(f) >= fresh}
tris = {}
for g, names in GROUPS:
    ts = [parts[n] for n in parts if any(n == p or (p.endswith('-') and n.startswith(p)) for p in names)]
    if ts: tris[g] = np.concatenate(ts)
allv = np.concatenate([t.reshape(-1, 3) for t in tris.values()])
LO = allv.min(0)
for g in tris: tris[g] = tris[g] - LO     # x from the deck's left edge, y from its front, z from the shelf


def view(groups, ax_u, ax_v, depth, near_high):
    """rasterize: u, v the drawing's axes (indices into xyz), depth the axis toward the viewer"""
    vs = np.concatenate([tris[g].reshape(-1, 3) for g in groups])
    W = int(np.ceil(vs[:, ax_u].max() / RES)) + 4; H = int(np.ceil(vs[:, ax_v].max() / RES)) + 4
    lab = np.zeros((H, W), np.int16); zb = np.full((H, W), -1e9)
    for i, g in enumerate(groups, 1):
        t = tris[g]; m = Image.new('L', (W, H)); dr = ImageDraw.Draw(m)
        for tri in t:
            dr.polygon([(p[ax_u] / RES + 2, H - (p[ax_v] / RES + 2)) for p in tri], fill=255)
        mk = np.asarray(m) > 0
        z = t[:, :, depth].max() if near_high else -t[:, :, depth].min()
        w = mk & (z > zb); lab[w] = i; zb[w] = z
    lines = []
    for i in range(1, len(groups) + 1):
        cg = contourpy.contour_generator(z=(lab == i).astype(float))
        for c in cg.lines(0.5):
            if len(c) > 3:
                lines.append(np.column_stack(((c[:, 0] - 2) * RES, (H - 1 - c[:, 1] - 2) * RES)))
    return lines, W * RES, H * RES


def mm_in(v):
    return f'{v:.0f} mm ({v / 25.4:.1f} in)'   # whole millimeters: 160.9 reads 161, 196.3 reads 196


body = [g for g, _ in GROUPS if g in tris and not g.startswith('cover')]
top, _, _ = view(body, 0, 1, 2, True)
front, _, _ = view(body, 0, 2, 1, False)
frontc, _, _ = view(body + ['cover', 'cover-feet'], 0, 2, 1, False)
deck = tris['deck'].reshape(-1, 3); W_, D_ = deck[:, 0].max() - deck[:, 0].min(), deck[:, 1].max() - deck[:, 1].min()
Hb = max(tris[g][:, :, 2].max() for g in body); Hc = tris['cover'][:, :, 2].max()
print(f'dims: deck {W_:.1f} x {D_:.1f}; height {Hb:.1f} to the arm, {Hc:.1f} with the cover')

fig = plt.figure(figsize=(16.5, 11.7))   # A3 landscape
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1650); ax.set_ylim(0, 1170); ax.set_aspect('equal'); ax.axis('off')
K = dict(color='black', lw=0.7, solid_capstyle='round')
T = dict(fontsize=9, family='DejaVu Sans', color='black')


def draw(lines, ox, oy):
    for l in lines:
        ax.plot(l[:, 0] + ox, l[:, 1] + oy, **K)


def dim_h(x0, x1, y, ox, oy, text, off=-40):
    yy = oy + y + off
    ax.plot([ox + x0, ox + x0], [oy + y, yy - 6], color='black', lw=0.4); ax.plot([ox + x1, ox + x1], [oy + y, yy - 6], color='black', lw=0.4)
    ax.annotate('', (ox + x0, yy), (ox + x1, yy), arrowprops=dict(arrowstyle='<->', lw=0.5, shrinkA=0, shrinkB=0))
    ax.text(ox + (x0 + x1) / 2, yy - 16, text, ha='center', va='center', **T)


def dim_v(y0, y1, x, ox, oy, text, off=40):
    xx = ox + x + off
    ax.plot([ox + x, xx + 6], [oy + y0, oy + y0], color='black', lw=0.4); ax.plot([ox + x, xx + 6], [oy + y1, oy + y1], color='black', lw=0.4)
    ax.annotate('', (xx, oy + y0), (xx, oy + y1), arrowprops=dict(arrowstyle='<->', lw=0.5, shrinkA=0, shrinkB=0))
    ax.text(xx + 10, oy + (y0 + y1) / 2, text, ha='left', va='center', rotation=90, **T)


# top view, front at the bottom
ox, oy = 90, 560
draw(top, ox, oy); dim_h(0, W_, 0, ox, oy, mm_in(W_)); dim_v(0, D_, W_, ox, oy, mm_in(D_))
ax.text(ox, oy + D_ + 30, 'TOP (cover off)', **dict(T, fontsize=11, weight='bold'))
# front views
ox2, oy2 = 90, 140
draw(front, ox2, oy2); dim_h(0, W_, 0, ox2, oy2, mm_in(W_)); dim_v(0, Hb, W_, ox2, oy2, mm_in(Hb))
ax.text(ox2, oy2 + Hc + 30, 'FRONT (cover off)', **dict(T, fontsize=11, weight='bold'))
ox3 = 900
draw(frontc, ox3, oy2); dim_h(0, W_, 0, ox3, oy2, mm_in(W_)); dim_v(0, Hc, W_, ox3, oy2, mm_in(Hc))
ax.text(ox3, oy2 + Hc + 30, 'FRONT (cover on)', **dict(T, fontsize=11, weight='bold'))
ax.text(900, 1000, 'Mantle (Strata Float v3)', **dict(T, fontsize=14, weight='bold'))
ax.text(900, 975, 'Dimensions from the CAD (out-strata-v3). Scale 1:1 on A3 at 1 mm = 1 unit.', **T)
ax.text(900, 955, 'Deck 450 x 360 mm (17.7 x 14.2 in). Lift-off cover 448 x 358 x 100 mm on 2.2 mm feet.', **T)
ax.text(900, 935, 'Height 161 mm (6.3 in) to the top of the arm; 196 mm (7.7 in) with the cover on.', **T)
ax.text(900, 915, 'Millimeters rounded to 1 mm, inches to 0.1 in. No record or label drawn: only designed parts.', **T)
os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, 'mantle-dimensions.svg'))
fig.savefig(os.path.join(OUT, 'mantle-dimensions.png'), dpi=100)
print('wrote', os.path.join(OUT, 'mantle-dimensions.svg'), 'and .png')
