"""The horn reopened (the owner, 2026-11-02 15:48: "I don't like that the stepped horns are now making an X shape in the
light reflection. The horns also look darker than the speaker. Not sure if I like the stepping anymore."): two horns for
the options study, built apart from the variants so the default horn (Strata's `horn-strata`) is untouched. Both keep
Strata's air path (machined smooth on 5 axes, the profile the simulation approved), its 560 flush mouth and its boss.

- `horn-soft` (option b): Strata's 22 layers of stock 1/2 in, each layer's outline a rounded rectangle whose corner
  radius grows toward the mouth (37 at the throat to about 85 at the mouth), the largest each layer takes with 6 left
  at its corner, so the corners no longer line up on straight diagonals.
- `horn-flat` (option d, "Strata laid flat"): the same horn laminated the other way, 29 horizontal slabs of stock
  1/2 in stacked bottom to top, each CNC-cut to the horn's plan at its inner face, so the outside steps in level
  terraces on the top and the bottom and the bond lines run level across the mouth, like strata in rock: no stacked
  corners, so no X.

    .venv-fab/bin/python spinoffs/barkhorn/variants/horn_study.py      # the render model (GLB and product file) only
"""
import copy, dataclasses, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.dirname(HERE))
import variants                                                      # noqa: E402
import product                                                       # noqa: E402

P = copy.deepcopy(variants.P)
SOFT = dict(corner_wall=6.0, margin=0.9)     # each layer's corner radius: `margin` x the largest that leaves `corner_wall`
FLAT = dict(layer=12.7)


def _envelope(c, lip):
    """The laminated horn's outside, smooth: (half width, half height, exponent) at z, the air path pushed out by the
    wall (the mouth's layer by `lip`), as Strata's layers draw it at their fronts."""
    wl = c['formed']['laminated']['wall']

    def at(z):
        w, h, n = product.flare_section(c, z)
        o = lip if z >= c['d'] - 1e-6 else wl
        return w + o, h + o, max(n, 2.0)
    return at


def _rmax(c, w, h, n, A, B, wall):
    """The largest corner radius of an A x B (half sizes) rounded rectangle that leaves `wall` outside the air path's
    superellipse (w, h, n) at every point."""
    pts = []
    for i in range(720):
        t = 2 * math.pi * i / 720; ct, st = math.cos(t), math.sin(t)
        pts.append((abs(w * abs(ct) ** (2 / n)), abs(h * abs(st) ** (2 / n))))

    def ok(R):
        a, b, r = A - wall, B - wall, max(R - wall, 0.01)
        for x, y in pts:
            if x > a or y > b:
                return False
            if x > a - r and y > b - r and (x - a + r) ** 2 + (y - b + r) ** 2 > r * r:
                return False
        return True
    lo, hi = 0.0, min(A, B)
    for _ in range(40):
        m = (lo + hi) / 2; lo, hi = (m, hi) if ok(m) else (lo, m)
    return lo


def study(P):
    from build123d import Align, Cylinder, Pos, RectangleRounded, extrude, Polyline, make_face
    c = P['horn']['cast']; L_ = c['formed']['laminated']; d = c['d']
    hw, hh = c['mouth_w'] / 2, c['mouth_h'] / 2
    cut = product._loft([product._se_pts(c['r0'], c['r0'], 2.0, -c['boss']['t'] - 2.0)] + product.air_sections(c, 0.0, d))
    boss = lambda: Pos(0, 0, -c['boss']['t']) * Cylinder(c['pod_r'], c['boss']['t'] - 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # b: the softened corners
    nl = max(1, round(d / L_['layer'])); t_ = d / nl
    soft, radii = [], []
    for i in range(nl):
        zz = d - i * t_; za = d - (i + 1) * t_
        w, h, n = product.flare_section(c, zz)
        if i == 0:
            w, h = hw, hh
        o = L_.get('lip', L_['wall']) if i == 0 else L_['wall']
        A, B = w + o, h + o
        R = SOFT['margin'] * _rmax(c, w, h, n, A, B, SOFT['corner_wall'])
        radii.append(R)
        soft.append(Pos(0, 0, za + 0.1) * extrude(RectangleRounded(2 * A, 2 * B, R), amount=t_ - 0.2) - cut)
    soft.append(boss() - cut)
    # d: Strata laid flat
    env = _envelope(c, L_.get('lip', L_['wall']))
    Bm = env(d)[1]
    ns = max(1, round(2 * Bm / FLAT['layer'])); p_ = 2 * Bm / ns
    zs = [d * (k / 60) ** 0.8 for k in range(61)]
    flat = []
    for k in range(ns):
        y0, y1 = -Bm + k * p_, -Bm + (k + 1) * p_
        yi = 0.0 if y0 < 0 < y1 else (y0 if y0 >= 0 else y1)        # the slab's inner face: its plan is the horn's there
        edge = []
        for z in zs:
            W, H, n = env(z)
            if H <= abs(yi):
                continue
            edge.append((z, W * (1 - (abs(yi) / H) ** n) ** (1 / n)))
        if len(edge) < 2:
            continue
        right = [(x, z) for z, x in edge]
        poly = right + [(-x, z) for x, z in reversed(right)]
        if edge[0][0] > 1e-6:                                         # the slab ends short of the throat in a point
            poly = [(0.0, edge[0][0] - 0.5)] + poly
        face = make_face(Polyline(*[(x, y0 + 0.1, z) for x, z in poly], close=True))
        slab = extrude(face, amount=p_ - 0.2, dir=(0, 1, 0))
        flat.append(slab - cut)
    flat.append(boss() - cut)
    return soft, flat, radii, ns


def parts(P):
    from build123d import Compound
    wg = product.waveguide(P)                    # its placement: the laminated horn's local frame onto the speaker
    c = P['horn']['cast']; depth = c['d']; cx = P['W'] / 2
    zc = P['H'] + c['gap'] + c['mouth_h'] / 2 + c['rim']
    pl = lambda s_: product.place(s_, (cx, depth, zc), (0, -1, 0))
    soft, flat, radii, ns = study(P)
    F = P['horn']['cast']['formed']
    return [product.Part('horn-soft', Compound(children=[pl(s) for s in soft]), product._lam_stock(F, soft, False),
                         finish='horn-lot', group='horn',
                         notes=[f'Option b: Strata\'s 22 layers, each a rounded rectangle, its corner radius {radii[-1]:.0f} at the '
                                f'throat to {radii[0]:.0f} at the mouth, so the corners do not line up']),
            product.Part('horn-flat', Compound(children=[pl(s) for s in flat]), product._lam_stock(F, flat, False),
                         finish='horn-lot', group='horn',
                         notes=[f'Option d: {ns} horizontal slabs of stock 1/2 in, bottom to top, each cut to the horn\'s plan at '
                                'its inner face; the air path machined through on 5 axes as Strata\'s'])]


PRODUCT = dataclasses.replace(variants.PRODUCT, name='barkhorn-horn-study', params=P, parts=parts, count=2, touching=[],
                              kind='Tropos horn options study (2026-11-02): softened corners, and Strata laid flat',
                              notes=['An options study; the default horn is variants.py\'s horn-strata.'], drawing_prefix='BHS')

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
    import render                                                    # noqa: E402
    ps = [p for p in parts(P) if p.solid is not None]
    for p in ps:
        print(p.name, p.notes[0], f'{1.19 * p.solid.volume / 1e6:.2f} kg' if hasattr(p.solid, 'volume') else '')
    glb, pf = render.write(PRODUCT, ps, os.path.join(HERE, 'out-horn-study'), proof=False)
    print(glb, pf)
