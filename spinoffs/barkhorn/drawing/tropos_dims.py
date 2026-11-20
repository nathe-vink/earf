"""Tropos, front and side, line only, in millimeters and inches (the coordinator, 20 Nov: "a dimension drawing of
Tropos from the CAD ... Draw only what is designed").

What is drawn is what the site's pictures show (shots._approved: base A, horn A polished, the black rods): the Cloud's
parts (out-cloud/render/barkhorn-cloud.glb) less the ones the approved look hides (the cloth disc, the woofer ring, the
Cloud's own posts), and the variants' parts it adds (variants/out/render/barkhorn-variants.glb: the Strata posts and
collars, the caldera, the horn lead), each placed by its own node, in the CAD frame (mm; x across, y front to back, z up,
the feet's pads at z -12). Inside parts that no view can see (linings, braces, the driver's back, the amplifier module,
leads) and flat prints are left out.

Visible lines, not a sketch: each view paints every triangle of every part far to near into a part map at 0.5 mm a
pixel, and each part's visible outline is traced from that map, so a line is drawn only where a part meets another
part or the air.

    .venv-fab/bin/python spinoffs/barkhorn/drawing/tropos_dims.py OUTDIR
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import glbparts as G                                    # noqa: E402

BH = os.path.dirname(HERE)
CLOUD = os.path.join(BH, 'out-cloud', 'render', 'barkhorn-cloud.glb')
VARIANTS = os.path.join(BH, 'variants', 'out', 'render', 'barkhorn-variants.glb')
CLOUD_SHOWN = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'port-frame-left', 'port-frame-right', 'port-left',
               'port-right', 'woofer-screws', 'woofer-gasket', 'woofer-surround', 'woofer-cone', 'woofer-cap',
               'waveguide', 'horn-throat', 'horn-pod', 'waveguide-cap', 'horn-pads', 'horn-saddle', 'tie-rod-rod',
               'feet-base', 'feet-stem', 'amp-plate-plate', 'amp-plate-housings', 'amp-plate-metal', 'amp-plate-gold',
               'amp-plate-screws', 'amp-plate-rca-white', 'amp-plate-rca-red', 'amp-plate-rca-orange', 'back-screws']
VARIANTS_SHOWN = ['strata-posts', 'strata-collars', 'lead-hf-pod', 'caldera-1', 'caldera-2', 'caldera-3']
PX = 0.5                                                # mm a pixel
IN = 25.4


def model():
    c, v = G.parts(CLOUD), G.parts(VARIANTS)
    return [(k, *c[k]) for k in CLOUD_SHOWN] + [(k, *v[k]) for k in VARIANTS_SHOWN]


def view(parts, axes, depth_axis, depth_sign):
    """The part map of one view: axes (h, v) of the CAD frame drawn across and up; depth along depth_axis, nearer
    the viewer where depth_sign * coordinate is smaller."""
    allV = np.vstack([V for _, V, _ in parts])
    lo = allV[:, axes].min(0) - 4; hi = allV[:, axes].max(0) + 4
    W, H = (np.ceil((hi - lo) / PX)).astype(int) + 1
    tris = []
    for pid, (_, V, F) in enumerate(parts, start=1):
        T = V[F]                                        # (m, 3, 3)
        d = depth_sign * T[:, :, depth_axis].mean(1)
        uv = (T[:, :, axes] - lo) / PX
        uv[:, :, 1] = H - 1 - uv[:, :, 1]
        tris.append((d, uv, np.full(len(F), pid)))
    d = np.concatenate([t[0] for t in tris]); uv = np.concatenate([t[1] for t in tris]); ids = np.concatenate([t[2] for t in tris])
    order = np.argsort(-d)                              # far first
    img = Image.new('I', (W, H), 0); dr = ImageDraw.Draw(img)
    for k in order:
        dr.polygon([tuple(p) for p in uv[k]], fill=int(ids[k]))
    return np.asarray(img), lo, (W, H)


def outlines(idmap, lo, shape):
    """Each part's visible outline as polylines in mm (h, v)."""
    W, H = shape
    xs = lo[0] + np.arange(W) * PX
    zs = lo[1] + (H - 1 - np.arange(H)) * PX
    fig = plt.figure(); ax = fig.add_subplot()
    lines = []
    for pid in np.unique(idmap):
        if pid == 0:
            continue
        m = (idmap == pid).astype(float)
        if m.sum() < 6:
            continue
        cs = ax.contour(xs, zs, m, levels=[0.5])
        for seg in cs.allsegs[0]:
            if len(seg) > 3:
                lines.append(seg)
    plt.close(fig)
    return lines


def _dim(ax, a, b, off, text, vertical, lw=0.5, fs=7.5):
    """A dimension between a and b (mm along the view), its line offset `off` from the part."""
    if vertical:
        x = off
        ax.annotate('', xy=(x, a), xytext=(x, b), arrowprops=dict(arrowstyle='<|-|>', lw=lw, color='k', shrinkA=0, shrinkB=0, mutation_scale=7))
        ax.text(x + (8 if off > 0 else -8), (a + b) / 2, text, rotation=90, ha='left' if off > 0 else 'right', va='center', fontsize=fs)
    else:
        y = off
        ax.annotate('', xy=(a, y), xytext=(b, y), arrowprops=dict(arrowstyle='<|-|>', lw=lw, color='k', shrinkA=0, shrinkB=0, mutation_scale=7))
        ax.text((a + b) / 2, y - 10, text, ha='center', va='top', fontsize=fs)


def _ext(ax, pts, lw=0.3):
    for (x0, y0, x1, y1) in pts:
        ax.plot([x0, x1], [y0, y1], color='k', lw=lw)


def fmt(mm):
    return f'{mm:.0f} mm ({mm / IN:.1f} in)'


def main(od):
    os.makedirs(od, exist_ok=True)
    P = model()
    allV = np.vstack([V for _, V, _ in P])
    lo, hi = allV.min(0), allV.max(0)
    print('extents mm', lo.round(1), hi.round(1), (hi - lo).round(1))
    front = view(P, [0, 2], 1, 1.0)                     # from the front: across x, up z; nearer = smaller y
    side = view(P, [1, 2], 0, -1.0)                     # from the right: across y (the front at the left), up z; nearer = larger x
    lf, ls = outlines(*front), outlines(*side)
    floor = lo[2]
    H = hi[2] - floor; Wd = hi[0] - lo[0]; Dp = hi[1] - lo[1]
    cab_top = 880.0 - floor                             # the cabinet's top above the floor (the feet's pads)
    gap = 260.0                                         # between the views
    sx = hi[0] + gap - lo[1]                            # the side view's shift across
    fig = plt.figure(figsize=(11.0, 8.5)); ax = fig.add_axes([0.04, 0.06, 0.92, 0.84])
    for seg in lf:
        ax.plot(seg[:, 0], seg[:, 1] - floor, color='k', lw=0.45, solid_joinstyle='round')
    for seg in ls:
        ax.plot(seg[:, 0] + sx, seg[:, 1] - floor, color='k', lw=0.45, solid_joinstyle='round')
    ax.plot([lo[0] - 60, hi[1] + sx + 60], [0, 0], color='k', lw=0.3, ls=(0, (6, 3)))
    # the front's dimensions: overall width under it, overall height at its left, the cabinet's top
    _ext(ax, [(lo[0], -6, lo[0], -70), (hi[0], -6, hi[0], -70)])
    _dim(ax, lo[0], hi[0], -60, fmt(Wd), False)
    _ext(ax, [(lo[0] - 6, H, lo[0] - 90, H)])
    _dim(ax, 0, H, lo[0] - 80, fmt(H), True)
    _ext(ax, [(lo[0] - 6, cab_top, lo[0] - 40, cab_top)])
    _dim(ax, 0, cab_top, lo[0] - 30, fmt(cab_top), True, fs=6.5)
    # the side's: overall depth under it, the cabinet's depth above the floor line
    _ext(ax, [(lo[1] + sx, -6, lo[1] + sx, -70), (hi[1] + sx, -6, hi[1] + sx, -70)])
    _dim(ax, lo[1] + sx, hi[1] + sx, -60, fmt(Dp), False)
    _ext(ax, [(sx + 0.0, -72, sx + 0.0, -125), (sx + 420.0, -72, sx + 420.0, -125)])
    _dim(ax, sx + 0.0, sx + 420.0, -115, 'cabinet ' + fmt(420.0), False, fs=6.5)
    ax.text((lo[0] + hi[0]) / 2, -195, 'FRONT', ha='center', fontsize=9, weight='bold')
    ax.text(sx + (lo[1] + hi[1]) / 2, -195, 'SIDE (from the right)', ha='center', fontsize=9, weight='bold')
    fig.text(0.04, 0.95, 'TROPOS', fontsize=13, weight='bold')
    fig.text(0.04, 0.925, 'Overall dimensions, millimeters (inches). Base A on its own feet, horn A. Drawn from the CAD.', fontsize=8)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(lo[0] - 200, hi[1] + sx + 140); ax.set_ylim(-235, H + 60)
    for ext in ('svg', 'png'):
        fig.savefig(os.path.join(od, f'tropos-dims.{ext}'), dpi=200 if ext == 'png' else None, facecolor='white')
    plt.close(fig)
    print('wrote', od, {'height': round(H, 1), 'width': round(Wd, 1), 'depth': round(Dp, 1), 'cabinet_top': cab_top,
                        'lines_front': len(lf), 'lines_side': len(ls)})


if __name__ == '__main__':
    main(sys.argv[1])
