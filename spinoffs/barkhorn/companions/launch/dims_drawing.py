"""Dimension drawings for the site (2026-11-20, the coordinator): Hemisphere from the side, Core from the front, line only,
millimeters and inches, from the CAD. Every outline is a part's own silhouette, read from its STL (out-dome-pendant/,
out-orb-table/: the fabkit builds) as its largest radius in each 0.25 mm of height, mirrored about the axis; nothing is
drawn that the CAD does not hold. Core's base skin (the default since 2026-11-11, B in its own colour) is the rig's
BASE_ALL profile, the same numbers the renders use; the dock inside it is drawn hidden (dashed).

Usage: dims_drawing.py OUTDIR   (writes hemisphere-dimensions.svg and core-dimensions.svg; the PNG previews are made
with ImageMagick by the caller)."""
import math, os, struct, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CO = os.path.join(HERE, '..')


def stl(folder, name):
    d = open(os.path.join(CO, folder, 'stl', name + '.stl'), 'rb').read()
    n = struct.unpack('<I', d[80:84])[0]
    a = np.frombuffer(d[84:84 + n * 50], dtype=np.dtype([('n', '<3f4'), ('v', '<9f4'), ('a', '<u2')]))
    return a['v'].reshape(-1, 3, 3).astype(float)


def silhouette(folder, names, step=0.5):
    """[(r, z)] the outer radius per height band, bottom to top, of one part or the union of several (a revolved
    part's side view: only the outside line, nothing inside it). Each triangle is sampled densely and the bands
    filled across the triangle's own height, so a tall side face leaves no gaps."""
    if isinstance(names, str):
        names = [names]
    tri = np.concatenate([stl(folder, n) for n in names])
    zs = tri[..., 2]; z0, z1 = zs.min(), zs.max()
    nb = int(math.ceil((z1 - z0) / step)) + 1
    rmax = np.zeros(nb)
    g = np.linspace(0, 1, 21)
    w = np.array([(a, b, 1 - a - b) for a in g for b in g if a + b <= 1.0 + 1e-9])
    for c in range(0, len(tri), 20000):
        pts = np.einsum('kj,ijl->ikl', w, tri[c:c + 20000]).reshape(-1, 3)
        r = np.hypot(pts[:, 0], pts[:, 1]); bi = np.clip(((pts[:, 2] - z0) / step).round().astype(int), 0, nb - 1)
        np.maximum.at(rmax, bi, r)
    # a band a sample missed takes the larger of its neighbours (no notch narrower than the band)
    rm = rmax.copy()
    for i in range(1, nb - 1):
        if rmax[i] < 0.97 * min(rmax[i - 1], rmax[i + 1]):
            rm[i] = max(rmax[i - 1], rmax[i + 1])
    zz = z0 + np.arange(nb) * step
    keep = rm > 0
    return list(zip(rm[keep], zz[keep]))


class SVG:
    def __init__(self, W, H):
        self.W, self.H, self.el = W, H, []

    def poly(self, pts, dash=False, w=1.2, close=True):
        d = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
        tag = 'polygon' if close else 'polyline'
        self.el.append(f'<{tag} points="{d}" fill="none" stroke="#111" stroke-width="{w}"' +
                       (' stroke-dasharray="5 4"' if dash else '') + ' stroke-linejoin="round"/>')

    def line(self, a, b, w=0.8, dash=False):
        self.el.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="#111" stroke-width="{w}"' +
                       (' stroke-dasharray="5 4"' if dash else '') + '/>')

    def text(self, p, s, anchor='middle', size=15, rot=0):
        tr = f' transform="rotate({rot} {p[0]:.2f} {p[1]:.2f})"' if rot else ''
        self.el.append(f'<text x="{p[0]:.2f}" y="{p[1]:.2f}" font-family="Helvetica, Arial, sans-serif" font-size="{size}" '
                       f'fill="#111" text-anchor="{anchor}"{tr}>{s}</text>')

    def arrow(self, tip, d):
        ux, uy = d; L = 9; Wd = 3.2
        px, py = -uy, ux
        a = (tip[0] - ux * L + px * Wd, tip[1] - uy * L + py * Wd); b = (tip[0] - ux * L - px * Wd, tip[1] - uy * L - py * Wd)
        self.el.append(f'<polygon points="{tip[0]:.2f},{tip[1]:.2f} {a[0]:.2f},{a[1]:.2f} {b[0]:.2f},{b[1]:.2f}" fill="#111"/>')

    def save(self, path):
        open(path, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{self.H}" '
                              f'viewBox="0 0 {self.W} {self.H}">\n<rect width="100%" height="100%" fill="#fff"/>\n' +
                              '\n'.join(self.el) + '\n</svg>\n')


def label(mm):
    return f'{mm:.0f} mm ({mm / 25.4:.2f} in)'


class Sheet:
    """Drawing at `k` px per mm, the axis at x = cx, model z = 0 at y = cy (z up)."""
    def __init__(self, W, H, k, cx, cy):
        self.s = SVG(W, H); self.k, self.cx, self.cy = k, cx, cy

    def P(self, r, z):
        return (self.cx + r * self.k, self.cy - z * self.k)

    def part(self, prof, dash=False, close=True):
        pts = [self.P(-r, z) for r, z in prof] + [self.P(r, z) for r, z in prof][::-1] if not close else \
              [self.P(r, z) for r, z in prof] + [self.P(-r, z) for r, z in reversed(prof)]
        self.s.poly(pts, dash=dash, close=close)

    def hdim(self, r0, r1, z, zfrom, text, gap=8):
        """A horizontal dimension from r0 to r1 at height z, extension lines from zfrom."""
        a, b = self.P(r0, z), self.P(r1, z)
        for rr, zz in ((r0, zfrom), (r1, zfrom)):
            e0 = self.P(rr, zz); e1 = self.P(rr, z)
            s = 1 if e1[1] > e0[1] else -1
            self.s.line((e0[0], e0[1] + s * 4), (e1[0], e1[1] + s * gap), w=0.6)
        self.s.line(a, b); self.s.arrow(a, (-1, 0)); self.s.arrow(b, (1, 0))
        self.s.text(((a[0] + b[0]) / 2, a[1] - 7), text)

    def vdim(self, z0, z1, r, rfrom, text, side=1, gap=8, flat=False):
        a, b = self.P(r, z0), self.P(r, z1)
        for zz, rr in ((z0, rfrom[0]), (z1, rfrom[1])):
            e0 = self.P(rr, zz); e1 = self.P(r, zz)
            s = 1 if e1[0] > e0[0] else -1
            self.s.line((e0[0] + s * 4, e0[1]), (e1[0] + s * gap, e1[1]), w=0.6)
        self.s.line(a, b); self.s.arrow(a, (0, 1)); self.s.arrow(b, (0, -1))
        if flat:   # a short span: the words beside it, level
            self.s.text(((a[0] + b[0]) / 2 + side * 10, (a[1] + b[1]) / 2 + 5), text, anchor='start' if side > 0 else 'end')
        else:
            m = ((a[0] + b[0]) / 2 + side * 12, (a[1] + b[1]) / 2)
            self.s.text(m, text, rot=-90 if side < 0 else 90)


def hemisphere(out):
    F = 'out-dome-pendant'
    body = silhouette(F, ['rim', 'shell', 'collar', 'clamp', 'crown', 'gland'])      # the shade and its fitting, one outline
    can = silhouette(F, 'canopy')
    k = 0.75; W, H = 820, 860
    sh = Sheet(W, H, k, 400, 760)                    # z 0 (the rim) at y 760; the ceiling (776) at y 178
    sh.part(body); sh.part(can)
    for z0_, z1_ in ((126.0, 300.0), (560.0, 726.0)):  # the cord, drawn broken
        sh.s.poly([sh.P(3, z0_), sh.P(3, z1_)], close=False); sh.s.poly([sh.P(-3, z0_), sh.P(-3, z1_)], close=False)
    for zb in (300.0, 560.0):
        sh.s.line(sh.P(-14, zb - 4), sh.P(14, zb + 4), w=0.9)
    sh.s.text(sh.P(14, 430), 'cord, cut to the drop', anchor='start', size=13)
    sh.s.line(sh.P(-340, 776), sh.P(260, 776), w=1.0)
    sh.s.text(sh.P(-335, 782), 'ceiling', anchor='start', size=13)
    rmax = max(r for r, _ in body)
    sh.hdim(-rmax, rmax, -36, 0, label(2 * rmax))
    sh.vdim(0.0, 100.0, 150, (rmax, 58.0), 'shade ' + label(100.0))
    sh.vdim(0.0, 126.0, -118, (-96.8, -20.0), label(126.0), side=-1)
    sh.vdim(126.0, 726.0, -175, (-20.0, -75.0), 'standard drop ' + label(600.0), side=-1)
    cr = max(r for r, _ in can)
    sh.hdim(-cr, cr, 815, 776, 'canopy ' + label(2 * cr))
    sh.vdim(726.0, 776.0, 110, (cr, cr), label(50.0), flat=True)
    sh.vdim(0.0, 776.0, -265, (-96.8, -75.0), label(776.0) + ', ceiling to rim, as supplied', side=-1)
    sh.s.text((W / 2, 36), 'Hemisphere, from the side', size=20)
    sh.s.text((W / 2, 58), 'Shade 200 across, 100 deep; 126 from the rim to the top of the cap. The cord is cut to the drop at install (600 standard).', size=13)
    sh.s.text((W / 2, H - 16), 'From the CAD (out-dome-pendant). Millimeters, inches in brackets.', size=12)
    sh.s.save(os.path.join(out, 'hemisphere-dimensions.svg'))


def core(out):
    F = 'out-orb-table'
    import ast
    src = open(os.path.join(CO, 'lamp_site.py')).read()
    base_all = ast.literal_eval(src.split('BASE_ALL = ', 1)[1].split('\n', 1)[0].split('   #')[0])
    shell = silhouette(F, 'shell'); dock = silhouette(F, 'dock')
    k = 2.6; W, H = 760, 760
    sh = Sheet(W, H, k, 380, 620)     # z 0 the base's foot; the table at z -6.5 (the skirt's edge and the dock's underside)
    zl = base_all[-1][1]
    sh.part([(r, z) for r, z in shell if z >= zl], close=False)      # the ball, above the skin's lip
    sh.part(base_all[1:][::-1], close=False)                         # the base's skin, its lip to the skirt's edge
    sh.s.line(sh.P(-75.0, -6.5), sh.P(75.0, -6.5), w=1.2)
    sh.part(dock, dash=True)
    sh.s.line(sh.P(-140, -6.5), sh.P(140, -6.5), w=0.6)
    rb = max(r for r, _ in shell); zt = max(z for _, z in shell)
    sh.hdim(-rb, rb, zt + 18, zt - 40, 'ball ' + label(2 * rb))
    sh.hdim(-75.0, 75.0, -30, -6.5, 'base ' + label(150.0))
    sh.vdim(-6.5, zt, 120, (75.0, 20.0), label(zt + 6.5) + ', on its dock or off it')
    sh.s.text(sh.P(0, 12), 'dock 136 across, inside the skirt (dashed)', size=12)
    sh.s.text((W / 2, 36), 'Core, from the front', size=20)
    sh.s.text((W / 2, 58), 'The dock sits inside the base\'s skirt, so the lamp stands the same height on it or off it.', size=13)
    sh.s.text((W / 2, H - 16), 'From the CAD (out-orb-table; base B in its own colour, the default). Millimeters, inches in brackets.', size=12)
    sh.s.save(os.path.join(out, 'core-dimensions.svg'))


if __name__ == '__main__':
    o = sys.argv[1]; os.makedirs(o, exist_ok=True)
    hemisphere(o); core(o)
