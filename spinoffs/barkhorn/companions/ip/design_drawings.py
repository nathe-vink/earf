"""Design-patent drawing pack (round 43, 2026-10-31; R11 on r46-owner-notes, section A): for each product, the six
orthographic views and one axonometric view from the fab kit's own solids, as black line drawings with hidden lines
removed, no dimensions and no text. Parts the design should not claim (bought parts, the cord, the drive) are drawn in
broken lines. A draftsperson finishes them (surface shading, the oblique lines for transparent surfaces, the FIG.
labels, the sheet margins): see README.md.

    .venv-fab/bin/python spinoffs/barkhorn/companions/ip/design_drawings.py DESIGN [--src CHECKOUT]

DESIGN is hemisphere, core, mantle, tropos-a (the formed horn), tropos-b (the laminated horn, horn-plan-b), globe or
coin. Mantle's product file lives on r32-turntable-final and Tropos's on r33-speaker-horn; pass `--src` to a checkout.
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
# Tropos (r33-speaker-horn, spinoffs/barkhorn/cloud.py): the cabinet, its ports, the horn on its pod and posts claimed;
# the drivers, the amplifier, the cloth disc and its frame, the posts' sockets and sleeves, the feet, the screws, the
# rating plate and the mark in broken lines. Its mains cable is not modelled (README).
_TROPOS = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'woofer-ring', 'port-left', 'port-right',
           'port-frame-left', 'port-frame-right', 'horn-pod', 'waveguide-cap', 'post-1', 'post-2', 'post-3', 'post-4',
           'horn-pads']
_TROPOS_BROKEN = ['woofer', 'amp-plate', 'hf', 'hf-adaptor', 'cloth-disc', 'disc-frame', 'post-sockets',
                  'post-sleeves', 'feet', 'back-screws', 'port-screws', 'rating-plate', 'mark-back']
DESIGNS.update({
    'tropos-a': dict(file='spinoffs/barkhorn/cloud.py', claimed=_TROPOS + ['waveguide', 'horn-throat'],
                     broken=_TROPOS_BROKEN),
    # Plan B in the formed horn's place: horn_options.py builds it at the Cloud's origin
    'tropos-b': dict(file='spinoffs/barkhorn/cloud.py', extra='spinoffs/barkhorn/horn_options.py',
                     claimed=_TROPOS + ['horn-plan-b'], broken=_TROPOS_BROKEN),
    # the six discs and the base; the glow bands, the UV ring and the hue chips left out (inside, or not the object)
    'globe': dict(loader='globe', claimed=['disc-m90', 'disc-m30', 'disc-m150', 'disc-equator', 'disc-north',
                                           'disc-south', 'base'], broken=[]),
    # one coin, design A: the reeded body with the globe engraved in its back and the words in its front
    # 40 mm across: the drawing kit's mesh, raster and stray-line sizes (set for speakers) scaled down with it
    'coin': dict(loader='coin', claimed=['coin'], broken=[], scale=0.08),
})
VIEWS = [('1-perspective', 'iso'), ('2-front', 'front'), ('3-rear', 'back'), ('4-left', 'left'), ('5-right', 'right'),
         ('6-top', 'top'), ('7-bottom', 'bottom')]


def load(path, fabkit):
    sys.path.insert(0, fabkit)
    sys.path.insert(0, os.path.dirname(path))
    spec = importlib.util.spec_from_file_location('product_ip_' + os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def solids(D, src, fabkit):
    """{part name: solid} for one design."""
    if D.get('loader') == 'globe':
        m = load(os.path.join(src, 'spinoffs/barkhorn/globe_colour.py'), fabkit)
        return {p.name: p.solid for p in m.parts() if p.solid is not None}
    if D.get('loader') == 'coin':
        m = load(os.path.join(src, 'spinoffs/barkhorn/companions/earf_coin.py'), fabkit)
        coin = [p for p in m.PRODUCT.parts(m.PRODUCT.params) if p.name == 'coin'][0]
        # the reeded body through hidden-line removal; the engravings (0.2 and 0.12 deep, too fine for its mesh) drawn
        # as their outlines on the face they open to: `face` lines, seen from the side the face looks to
        return {'coin': coin.pieces['body'][0],
                'face': [(coin.pieces['words'][0], +1), (coin.pieces['globe'][0], -1)]}
    P = load(os.path.join(src, D['file']), fabkit).PRODUCT
    out = {p.name: p.solid for p in P.parts(P.params) if p.solid is not None}
    if D.get('extra'):
        X = load(os.path.join(src, D['extra']), fabkit).PRODUCT
        out.update({p.name: p.solid for p in X.parts(X.params) if p.solid is not None})
    return out


def face_lines(items, view, DR):
    """Outlines of thin engravings in a flat face: the edges of each engraving's face nearest that surface, projected
    when the view looks at the face's side (`side` +1: the +z face, -1: the -z face)."""
    import numpy as np
    d = np.array(DR.VIEWS[view][0], float)
    out = []
    for solid, side in items:
        if d[2] * side <= 1e-6:
            continue
        zs = [f.center().Z for f in solid.faces()]
        z = max(zs) if side > 0 else min(zs)
        for f in solid.faces():
            if abs(f.center().Z - z) > 1e-3:
                continue
            for e in f.edges():
                n = 2 if e.geom_type.name == 'LINE' else int(min(400, max(6, e.length / 0.05)))
                pts = [(p.X, p.Y, p.Z) for p in (e.position_at(t) for t in np.linspace(0, 1, n))]
                out.append(DR.to2d(view, pts))
    return out


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
    parts = solids(D, a.src, fabkit)
    import drawings as DR
    DR.VIEWS.setdefault('bottom', ((0, 0, -1), (0, -1, 0)))
    k = D.get('scale', 1.0)
    if k != 1.0:
        for n in ('MESH_MM', 'FOOT_PX', 'NEAR_MM', 'BRIDGE_MM', 'STRAY_MM', 'EASE_MM', 'MEET_MM'):
            setattr(DR, n, getattr(DR, n) * k)
        DR._drop_slivers.__defaults__ = (DR.STRAY_MM, 2.0 * k)
    claimed = [parts[n] for n in D['claimed'] if n in parts]
    broken = [parts[n] for n in D['broken'] if n in parts]
    missing = [n for n in D['claimed'] + D['broken'] if n not in parts]
    if missing:
        print('not in the model:', missing)
    out_dir = os.path.join(HERE, a.design)
    os.makedirs(out_dir, exist_ok=True)
    for name, view in VIEWS:
        everything, _ = DR.hlr(claimed + broken, view) if broken else (None, None)
        mine, _ = DR.hlr(claimed, view)
        s, b = classify(everything, mine) if broken else (mine, [])
        s = s + face_lines(parts.get('face', []), view, DR)
        b = clip(b, s)
        draw(s, b, os.path.join(out_dir, f'{a.design}-{name}'))
        print(a.design, name, len(s), 'solid', len(b), 'broken', flush=True)


if __name__ == '__main__':
    main()
