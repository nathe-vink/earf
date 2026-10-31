"""Design-patent drawing pack (round 43, 2026-10-31; R11 on r46-owner-notes, section A): for each product, the six
orthographic views and one axonometric view from the fab kit's own solids, as black line drawings with hidden lines
removed, no dimensions and no text. Parts the design should not claim (bought parts, the cord, the drive) are drawn in
broken lines. A draftsperson finishes them (surface shading, the oblique lines for transparent surfaces, the FIG.
labels, the sheet margins): see README.md.

    .venv-fab/bin/python spinoffs/barkhorn/companions/ip/design_drawings.py hemisphere|core|mantle [--fabkit DIR]

Mantle's product file lives on r32-turntable-final; pass `--src` to a checkout of it.
"""
import argparse, importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))

# claimed in solid lines; disclaimed in broken lines; everything else (inside, or too small to read) left out
DESIGNS = {
    'hemisphere': dict(
        file='spinoffs/barkhorn/companions/dome_pendant.py', options=['suspension'],
        claimed=['shell', 'skin', 'rim', 'collar', 'clamp', 'hub', 'crown', 'gland', 'pins'],
        broken=['cord', 'suspension']),          # the canopy left out: from above it hid the whole design
    'core': dict(
        file='spinoffs/barkhorn/companions/orb_table.py', options=[],
        claimed=['shell', 'grommet', 'base', 'ring', 'window', 'hatch', 'seat', 'foot-ring'],
        broken=['cable']),
    'mantle': dict(
        file='spinoffs/barkhorn/companions/turntable_float.py', options=[],
        claimed=['plinth', 'base', 'post-1', 'post-2', 'post-3', 'post-4', 'platter', 'platter-hub', 'spindle',
                 'bearing-housing', 'pod-ring-1', 'pod-ring-2', 'pod-ring-3', 'pod-ring-4', 'pod-core', 'pod-mat',
                 'pulley'],    # the lid left out: drawn opaque it hid the whole design (see README)
        broken=['arm', 'cartridge', 'motor', 'belt', 'feet', 'phono-stage', 'rear-box', 'hinges', 'led-strip',
                'slot-mask', 'mark']),
}
VIEWS = [('1-perspective', 'iso'), ('2-front', 'front'), ('3-rear', 'back'), ('4-left', 'left'), ('5-right', 'right'),
         ('6-top', 'top'), ('7-bottom', 'bottom')]


def load(path, fabkit):
    sys.path.insert(0, fabkit)
    spec = importlib.util.spec_from_file_location('product_ip', path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.PRODUCT


def classify(all_lines, claimed_lines, tol=1.0):
    """A line of the whole drawing is solid if most of it lies on a line of the claimed parts' own drawing."""
    import numpy as np
    if not claimed_lines:
        return [], all_lines
    C = np.vstack([np.asarray(q, float) for q in claimed_lines])
    solid, broken = [], []
    for q in all_lines:
        q = np.asarray(q, float)
        s = q[::max(1, len(q) // 10)]
        d = np.sqrt(((s[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)).min(axis=1)
        (solid if (d < tol).mean() >= 0.6 else broken).append(q)
    return solid, broken


def clip(broken, solid, frac=0.3):
    """Broken lines cut to a margin round the claimed outline (a cord shown as a stub, as patent drawings do)."""
    import numpy as np
    if not solid:
        return broken
    S = np.vstack([np.asarray(q, float) for q in solid])
    lo, hi = S.min(axis=0), S.max(axis=0)
    m = frac * float((hi - lo).max())
    lo, hi = lo - m, hi + m
    out = []
    for q in broken:
        q = np.asarray(q, float)
        inside = np.all((q >= lo) & (q <= hi), axis=1)
        run = []
        for p, ok in zip(q, inside):
            if ok:
                run.append(p)
            elif len(run) > 1:
                out.append(np.array(run)); run = []
            else:
                run = []
        if len(run) > 1:
            out.append(np.array(run))
    return out


def draw(solid, broken, out, size_in=7.0):
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    pts = np.vstack([np.asarray(q, float) for q in solid + broken])
    (x0, y0), (x1, y1) = pts.min(axis=0), pts.max(axis=0)
    w, h = x1 - x0, y1 - y0
    k = size_in / max(w, h)
    fig = plt.figure(figsize=(w * k + 0.4, h * k + 0.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off(); ax.set_aspect('equal')
    for q in solid:
        q = np.asarray(q, float); ax.plot(q[:, 0], q[:, 1], color='black', lw=0.7, solid_capstyle='round')
    for q in broken:
        q = np.asarray(q, float); ax.plot(q[:, 0], q[:, 1], color='black', lw=0.5, dashes=(4, 2.5))
    m = 0.2 / k
    ax.set_xlim(x0 - m, x1 + m); ax.set_ylim(y0 - m, y1 + m)
    for ext in ('svg', 'png'):
        fig.savefig(f'{out}.{ext}', dpi=300, facecolor='white')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('design', choices=list(DESIGNS))
    ap.add_argument('--src', default=ROOT, help='the checkout holding the product file (Mantle: r32-turntable-final)')
    a = ap.parse_args()
    D = DESIGNS[a.design]
    fabkit = os.path.join(a.src, 'studio', 'fabkit')
    P = load(os.path.join(a.src, D['file']), fabkit)
    import drawings as DR
    DR.VIEWS.setdefault('bottom', ((0, 0, -1), (0, -1, 0)))
    parts = {p.name: p for p in P.parts(P.params) if p.solid is not None}
    claimed = [parts[n].solid for n in D['claimed'] if n in parts]
    broken = [parts[n].solid for n in D['broken'] if n in parts]
    missing = [n for n in D['claimed'] + D['broken'] if n not in parts]
    if missing:
        print('not in the model:', missing)
    out_dir = os.path.join(HERE, a.design)
    os.makedirs(out_dir, exist_ok=True)
    for name, view in VIEWS:
        everything, _ = DR.hlr(claimed + broken, view)
        mine, _ = DR.hlr(claimed, view)
        s, b = classify(everything, mine)
        b = clip(b, s)
        draw(s, b, os.path.join(out_dir, f'{a.design}-{name}'))
        print(a.design, name, len(s), 'solid', len(b), 'broken', flush=True)


if __name__ == '__main__':
    main()
