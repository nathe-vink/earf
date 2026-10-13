"""The cast horn's sound field by boundary elements (round 12, the owner: "Do 1-3", the first being to check the horn's
acoustics by simulation): its coverage, its loading and its on-axis response from below the 800 Hz crossover to
8 kHz, alone and on its cabinet beside the 15 in woofer, and the two summed through the crossover.

    .venv-fab/bin/python spinoffs/barkhorn/horn_sim.py check               # the solver against a pulsating sphere
    .venv-fab/bin/python spinoffs/barkhorn/horn_sim.py mesh lo             # a band's mesh: its size, and an STL to look at
    .venv-fab/bin/python spinoffs/barkhorn/horn_sim.py solve lo            # -> acoustics/horn-lo.json (also mid, hi, cab)

What is modelled: the horn's surfaces as speaker/horn.py lofts them from product.py's P['horn']['cast'], meshed straight
from the same section formulas: the flare, its rim rounded over a crest, the shell's outside following the flare back
into the round pod, the pod's domed cap. The air path runs on behind the throat through the boss and the adaptor ring
(24 mm, the 2 in bore) to the driver's exit, where a flat piston stands in for the compression driver. Every other
surface is rigid; the posts (10 mm rods) are left out. Each band has its own mesh, at least six elements a wavelength
inside the horn at the band's top, coarser outside and behind it, where little sound goes at those frequencies.
`cab` adds the cabinet (a closed box, its front flat) with the woofer as a second piston of its effective area.
The solver is fab/bem.py's: bempp-cl, Burton-Miller, a direct solve.

Frames: the product's, mm (x across from the cabinet's left, y back from its front, z up from the floor); the horn's
axis points to -y at the height zc, its mouth in the cabinet's front plane. Angles: horizontal positive to the right
seen from the front... from the listener's side, as fab/bem.py's directions(); vertical positive up.
"""
import argparse, gc, json, math, sys, time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / 'fab'))
from bem import consistent_orientation, sphere, device, beamwidth    # noqa: E402

OUT = HERE / 'acoustics'
C_AIR = 343.0

# 1/6 octave, each band meshed for its top frequency: h inside the horn, outside it, behind it (pod, cap), at the
# throat, and along the rim's rounding (mm)
BANDS = dict(
    lo=dict(freqs=[250, 280, 315, 355, 400, 450, 500, 560, 630, 710, 800, 900, 1000, 1120, 1250, 1400, 1600],
            h_in=15.0, h_out=24.0, h_back=34.0, h_throat=6.0, h_rim=3.0),
    mid=dict(freqs=[1800, 2000, 2240, 2500, 2800, 3150, 3550, 4000],
             h_in=10.0, h_out=15.0, h_back=21.0, h_throat=5.0, h_rim=3.0),
    hi=dict(freqs=[4500, 5000, 5600, 6300, 7100, 8000],
            h_in=7.0, h_out=10.5, h_back=14.0, h_throat=4.0, h_rim=2.5),
    cab=dict(freqs=[250, 280, 315, 355, 400, 450, 500, 560, 630, 710, 800, 900, 1000, 1120, 1250, 1400, 1600, 1800, 2000],
             h_in=14.0, h_out=22.0, h_back=30.0, h_throat=6.0, h_rim=3.0, h_box=28.0),
)


def _smax(a, b, k=8.0):
    return (a ** k + b ** k) ** (1.0 / k)


class Horn:
    """The cast horn's surfaces as section rings (W, H, n, z): superellipses |x/W|^n + |y/H|^n = 1 in the horn's local
    frame (x across, y up, z from the throat to the mouth), with speaker/horn.py's formulas for the flare, the outside,
    the rim's rounding and the cap. `profile` swaps in another air surface for proposals: a function z -> (w, h, n),
    with its own depth and mouth."""

    def __init__(self, P, profile=None):
        c = P['horn']['cast']
        self.c = c
        self.hw, self.hh, self.depth = c['mouth_w'] / 2, c['mouth_h'] / 2, c['d']
        self.r0, self.wall, self.rim, self.ra = c['r0'], c['wall'], c['rim'], c['round_rim']
        self.nm, self.pod_r, self.pod_back, self.dome = c['n_mouth'], c['pod_r'], c['pod_back'], c['dome']
        self.cable_d = 10.0
        self.zp = -(c['boss']['t'] + c['adaptor']['t'])          # the driver's exit, behind the throat
        self.ta = math.sqrt(max(self.hw ** 2 - self.r0 ** 2, 0.0)) / self.depth
        self.tb = math.sqrt(max(self.hh ** 2 - self.r0 ** 2, 0.0)) / self.depth
        self.za = self.depth - self.ra
        self.crest = (self.hw + self.rim / 2, self.hh + self.rim / 2)
        self.profile = profile
        # where the horn sits (product.waveguide): the throat at y = depth, the axis at zc
        self.cx, self.zc = P['W'] / 2, P['H'] + c['gap'] + self.hh + self.rim

    def flare(self, z):
        if self.profile:
            return self.profile(z)
        d = self.depth
        return (math.sqrt(self.r0 ** 2 + (z * self.ta) ** 2), math.sqrt(self.r0 ** 2 + (z * self.tb) ** 2),
                2.0 + (self.nm - 2.0) * (max(z, 0.0) / d) ** 1.2)

    def outer(self, z):
        if z < 0:
            return self.pod_r, self.pod_r, 2.0
        d = self.depth
        zz = min(z, d)
        w, h, nn = self.flare(zz)
        if self.profile is None:
            nn = 2.0 + (self.nm - 2.0) * (zz / d) ** 1.2
        grow = self.wall + (self.rim - self.wall) * max(0.0, (zz - (d - 25.0)) / 25.0) ** 2
        W, H = _smax(w + grow, self.pod_r), _smax(h + grow, self.pod_r)
        pod = (self.pod_r / max(W, H)) ** 4
        return W, H, nn * (1 - pod) + 2.0 * pod

    def rounding(self, f, s):
        """horn.py's rounding(): from z = za along f's own slope, a quadratic Bezier toward the crest at the mouth's
        plane; s in [0, 1] runs over its five sections (u = 1 - sqrt(1 - k/4) at z = za + k, the last u = 0.82)."""
        za, d = self.za, self.depth
        (w0, h0, n0), (w1, h1, _) = f(za), f(za - 0.5)
        qw, qh = w0 + (w0 - w1) / 0.5 * (d - za), h0 + (h0 - h1) / 0.5 * (d - za)
        u = 1.0 - math.sqrt(1.0 - s) if s <= 0.75 else 0.5 + (s - 0.75) / 0.25 * 0.32
        a, b, cc = (1 - u) ** 2, 2 * u * (1 - u), u * u
        wc, hc = self.crest
        return a * w0 + b * qw + cc * wc, a * h0 + b * qh + cc * hc, n0, za + (d - za) * s

    def cap(self, u):
        z0 = -self.pod_back
        r = max(self.pod_r * math.sqrt(max(1 - u * u, 0.0)), self.cable_d / 2 + self.wall + 2)
        return r, r, 2.0, z0 - self.dome * u

    def segments(self):
        """The body's surface from the piston's centre to the cap's, as segments of densely sampled rings, each
        (region, [(W, H, n, z), ...]); consecutive segments share their end rings."""
        r0, d = self.r0, self.depth
        S = []
        S.append(('piston', [(r, r, 2.0, self.zp) for r in np.linspace(0.0, r0, 40)]))
        S.append(('throat', [(r0, r0, 2.0, z) for z in np.linspace(self.zp, 0.0, 40)]))
        zs = np.concatenate([np.linspace(0.0, 30.0, 120), np.linspace(30.0, self.za, 700)[1:]])
        S.append(('flare', [(*self.flare(z), z) for z in zs]))
        S.append(('rim', [self.rounding(self.flare, s) for s in np.linspace(0, 1, 60)]))
        (wi, hi, ni, _), (wo, ho, no, _) = self.rounding(self.flare, 1.0), self.rounding(self.outer, 1.0)
        S.append(('rim', [(wi + (wo - wi) * t, hi + (ho - hi) * t, ni + (no - ni) * t, d) for t in np.linspace(0, 1, 12)]))
        S.append(('rim', [self.rounding(self.outer, s) for s in np.linspace(1, 0, 60)]))
        S.append(('outer', [(*self.outer(z), z) for z in np.linspace(self.za, 0.0, 800)]))
        S.append(('back', [(self.pod_r, self.pod_r, 2.0, z) for z in np.linspace(0.0, -self.pod_back, 80)]))
        S.append(('back', [self.cap(u) for u in np.linspace(0, 1, 120)]))
        re, _, _, ze = self.cap(1.0)
        S.append(('back', [(r, r, 2.0, ze) for r in np.linspace(re, 0.0, 20)]))
        return S

    def to_product(self, x, y, z):
        """Local (x across, y up, z toward the mouth) to the product frame (mm)."""
        return np.stack([self.cx + x, self.depth - z, self.zc + y], -1)



class BellHorn(Horn):
    """A proposal, not built: the same horn with a bell-flared lip. The flare stops `roll_dz` short of the mouth's
    plane, on a smaller mouth, and its last stretch curls outward on an arc in each plane (radius `roll_r` across, the
    radius up and down whatever ends both arcs at the mouth's plane) until it faces straight forward at the same 610 x
    346 mouth; the shell's lip turns over a semicircle of its own thickness and its outside follows the arc back. The
    outside is about the same size as now; the rim reads as a rounded bell, not a thin edge."""

    def __init__(self, P, roll_r=40.0):
        super().__init__(P)
        c, d, r0 = self.c, self.depth, self.r0
        self.roll_r = roll_r
        hw1, hh1 = self.hw - 25.0, self.hh - 18.0
        for _ in range(30):                          # the smaller flare whose curled lip lands on the mouth
            ta, tb = math.sqrt(hw1 ** 2 - r0 ** 2), math.sqrt(hh1 ** 2 - r0 ** 2)
            dz = roll_r * (1 - math.sin(math.atan(ta / (d - 0.0))))
            d1 = d - dz
            th_h, th_v = math.atan(ta / d1), math.atan(tb / d1)
            dz = roll_r * (1 - math.sin(th_h)); d1 = d - dz
            rv = dz / (1 - math.sin(th_v))
            hw1 = self.hw - roll_r * math.cos(th_h); hh1 = self.hh - rv * math.cos(th_v)
        self.d1, self.dz, self.hw1, self.hh1 = d1, dz, hw1, hh1
        self.ta1 = math.sqrt(hw1 ** 2 - r0 ** 2) / d1; self.tb1 = math.sqrt(hh1 ** 2 - r0 ** 2) / d1
        self.th = (math.atan(self.ta1), math.atan(self.tb1))
        self.R = (roll_r, dz / (1 - math.sin(self.th[1])))

    def flare(self, z):
        z = min(z, self.d1)
        return (math.sqrt(self.r0 ** 2 + (z * self.ta1) ** 2), math.sqrt(self.r0 ** 2 + (z * self.tb1) ** 2),
                2.0 + (self.nm - 2.0) * (max(z, 0.0) / self.d1) ** 1.2)

    def _arc(self, k, z, off=0.0):
        """Plane k's (0 across, 1 up) lip at depth z: the radius of the curl (inside, or `off` toward the shell)."""
        th, R = self.th[k], self.R[k]
        r1 = (self.hw1, self.hh1)[k]
        cr, cz = r1 + R * math.cos(th), self.d1 - R * math.sin(th)          # the arc's centre, behind the lip
        rr = R - off
        u = min(max((z - cz) / rr, -1.0), 1.0)
        return cr - rr * math.sqrt(max(1 - u * u, 0.0))

    def outer(self, z):
        if z < 0:
            return self.pod_r, self.pod_r, 2.0
        w, h, nn = self.flare(z)
        zz = min(z, self.d1)
        sw = math.sqrt(1 + (zz * self.ta1 ** 2 / max(w, 1e-9)) ** 2)        # the wall's normal thickness, across
        sh = math.sqrt(1 + (zz * self.tb1 ** 2 / max(h, 1e-9)) ** 2)
        W, H = _smax(w + self.wall * sw, self.pod_r), _smax(h + self.wall * sh, self.pod_r)
        pod = (self.pod_r / max(W, H)) ** 4
        return W, H, nn * (1 - pod) + 2.0 * pod

    def segments(self):
        r0, d, t = self.r0, self.depth, self.wall
        n1 = self.nm
        S = []
        S.append(('piston', [(r, r, 2.0, self.zp) for r in np.linspace(0.0, r0, 40)]))
        S.append(('throat', [(r0, r0, 2.0, z) for z in np.linspace(self.zp, 0.0, 40)]))
        zs = np.concatenate([np.linspace(0.0, 30.0, 120), np.linspace(30.0, self.d1, 700)[1:]])
        S.append(('flare', [(*self.flare(z), z) for z in zs]))
        S.append(('rim', [(self._arc(0, z), self._arc(1, z), n1, z) for z in np.linspace(self.d1, d, 60)]))
        S.append(('rim', [(self.hw + t / 2 * math.sin(a), self.hh + t / 2 * math.sin(a), n1, d - t / 2 + t / 2 * math.cos(a))
                          for a in np.linspace(0, math.pi, 24)]))
        z0 = self.d1 - t * math.sin(self.th[0])
        S.append(('rim', [(self._arc(0, z, t), self._arc(1, z, t), n1, z) for z in np.linspace(d - t, z0, 60)]))
        S.append(('outer', [(*self.outer(z), z) for z in np.linspace(z0, 0.0, 800)]))
        S.append(('back', [(self.pod_r, self.pod_r, 2.0, z) for z in np.linspace(0.0, -self.pod_back, 80)]))
        S.append(('back', [self.cap(u) for u in np.linspace(0, 1, 120)]))
        re, _, _, ze = self.cap(1.0)
        S.append(('back', [(r, r, 2.0, ze) for r in np.linspace(re, 0.0, 20)]))
        return S

def superellipse(W, H, n, N):
    """N points on |x/W|^n + |y/H|^n = 1, evenly spaced along it from (W, 0), counterclockwise (N even keeps the set
    symmetric about both axes)."""
    th = np.linspace(0, 2 * np.pi, 8001)
    c, s = np.cos(th), np.sin(th)
    r = (np.abs(c / W) ** n + np.abs(s / H) ** n) ** (-1.0 / n)
    x, y = r * c, r * s
    cum = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(x), np.diff(y)))])
    t = np.arange(N) * cum[-1] / N
    return np.interp(t, cum, x), np.interp(t, cum, y), cum[-1]


def perimeter(W, H, n):
    return superellipse(W, H, n, 4)[2] if W > 1e-9 else 0.0


def pick_rings(rings, h):
    """Rings along a densely sampled segment, about h apart along its meridian (the steeper of the two half
    dimensions' paths), its end rings kept."""
    R = np.array(rings, float)
    ds = np.maximum(np.hypot(np.diff(R[:, 0]), np.diff(R[:, 3])), np.hypot(np.diff(R[:, 1]), np.diff(R[:, 3])))
    cum = np.concatenate([[0.0], np.cumsum(ds)])
    L = cum[-1]
    m = max(1, int(math.ceil(L / h - 0.15)))
    t = np.linspace(0, L, m + 1)
    return np.stack([np.interp(t, cum, R[:, k]) for k in range(4)], 1)


def stitch(ia, ib):
    """Triangles joining two rings of vertex indices by their fraction of the way round (either may be one centre
    vertex)."""
    out = []
    if len(ia) == 1 or len(ib) == 1:
        c, ring, flip = (ia[0], ib, False) if len(ia) == 1 else (ib[0], ia, True)
        for j in range(len(ring)):
            t = (c, ring[j], ring[(j + 1) % len(ring)])
            out.append((t[0], t[2], t[1]) if flip else t)
        return out
    Na, Nb = len(ia), len(ib)
    i = j = 0
    while i < Na or j < Nb:
        na = (i + 1) / Na if i < Na else 9.0
        nb = (j + 1) / Nb if j < Nb else 9.0
        if na <= nb:
            out.append((ia[i % Na], ia[(i + 1) % Na], ib[j % Nb])); i += 1
        else:
            out.append((ia[i % Na], ib[(j + 1) % Nb], ib[j % Nb])); j += 1
    return out


def horn_mesh(horn, band):
    """A closed triangle mesh of the horn (product frame, mm): vertices (N, 3), triangles (M, 3), domain (M,): 1 on the
    driver's piston, 0 elsewhere."""
    hm = dict(piston=band['h_throat'], throat=band['h_throat'], flare=band['h_in'], rim=band['h_rim'],
              outer=band['h_out'], back=band['h_back'])
    hp = dict(hm, rim=band['h_in'])                  # along the rings: the rim's rings spaced as the flare's
    V, T, D = [], [], []
    prev = None
    for region, rings in horn.segments():
        picked = pick_rings(rings, hm[region])
        start = 1 if prev is not None else 0         # the first ring is the last segment's
        for k in range(start, len(picked)):
            W, H, n, z = picked[k]
            if W < 1e-6:
                idx = [len(V)]
                V.append(horn.to_product(np.array(0.0), np.array(0.0), np.array(z)))
            else:
                N = max(12, 4 * int(math.ceil(perimeter(W, H, n) / hp[region] / 4)))
                x, y, _ = superellipse(W, H, n, N)
                idx = list(range(len(V), len(V) + N))
                V.extend(horn.to_product(x, y, np.full(N, z)))
            if prev is not None:
                tri = stitch(prev, idx)
                T.extend(tri); D.extend([1 if region == 'piston' else 0] * len(tri))
            prev = idx
    V = np.array(V, float)
    T = np.array(T, int)
    D = np.array(D, np.uint32)
    T = consistent_orientation(V, T)
    return V, T, D


def box_mesh(P, h, woofer=True):
    """The cabinet as a closed box (product frame, mm), its front flat at y = 0, the woofer a disc of its effective
    area (domain 2) at its centre: vertices, triangles, domain."""
    import gmsh
    W, Dp, H = P['W'], P['D'], P['H']
    gmsh.initialize(); gmsh.option.setNumber('General.Terminal', 0)
    gmsh.model.add('box')
    occ = gmsh.model.occ
    box = occ.addBox(0, 0, 0, W, Dp, H)
    disc = None
    if woofer:
        a = math.sqrt(WOOFER_SD_CM2 * 1e2 / math.pi)
        disc = occ.addDisk(0, 0, 0, a, a)              # in the xy plane; turned about x into the front (y = 0)
        occ.rotate([(2, disc)], 0, 0, 0, 1, 0, 0, math.pi / 2)
        occ.translate([(2, disc)], W / 2, 0, P['woofer_z'])
        occ.synchronize()
        occ.fragment([(3, box)], [(2, disc)])
    occ.synchronize()
    gmsh.option.setNumber('Mesh.MeshSizeMin', h * 0.6); gmsh.option.setNumber('Mesh.MeshSizeMax', h)
    gmsh.option.setNumber('Mesh.Algorithm', 6)
    gmsh.model.mesh.generate(2)
    tags, coords, _ = gmsh.model.mesh.getNodes()
    xyz = coords.reshape(-1, 3); idx = {int(t): i for i, t in enumerate(tags)}
    tris, dom = [], []
    a = math.sqrt(WOOFER_SD_CM2 * 1e2 / math.pi)
    for dim, s in gmsh.model.getEntities(2):
        bb = occ.getBoundingBox(2, s)
        is_disc = woofer and abs(bb[1]) < 1e-6 and abs(bb[4]) < 1e-6 and (bb[3] - bb[0]) < 2 * a + 1.0
        et, _, en = gmsh.model.mesh.getElements(2, s)
        for typ, nodes in zip(et, en):
            if typ != 2:
                continue
            for t in np.asarray(nodes).reshape(-1, 3):
                tris.append([idx[int(q)] for q in t]); dom.append(2 if is_disc else 0)
    gmsh.finalize()
    V = xyz.copy()
    T = np.array(tris, int)
    used = np.unique(T)                               # drop the box's inner nodes, if any
    remap = -np.ones(len(V), int); remap[used] = np.arange(len(used))
    V, T = V[used], remap[T]
    return V, consistent_orientation(V, T), np.array(dom, np.uint32)


WOOFER_SD_CM2 = 805.0          # FaitalPRO 15PR400-8 (components.json)


def watertight(T):
    from collections import Counter
    e = Counter()
    for t in T:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            e[(min(a, b), max(a, b))] += 1
    bad = sum(1 for v in e.values() if v != 2)
    return bad


def quality(V, T):
    a, b, c = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    l = np.stack([np.linalg.norm(b - a, axis=1), np.linalg.norm(c - b, axis=1), np.linalg.norm(a - c, axis=1)], 1)
    area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    # aspect: longest edge over the height on it (1.15 for an equilateral triangle)
    asp = l.max(1) ** 2 / (2 * area + 1e-12)
    return dict(edge_mean=float(l.mean()), edge_max=float(l.max()), area=float(area.sum() / 1e6),
                aspect_p95=float(np.percentile(asp, 95)), aspect_max=float(asp.max()), degenerate=int((area < 1e-6).sum()))


def write_stl(path, V, T):
    with open(path, 'w') as f:
        f.write('solid m\n')
        for t in T:
            a, b, c = V[t[0]], V[t[1]], V[t[2]]
            n = np.cross(b - a, c - a); n = n / (np.linalg.norm(n) + 1e-12)
            f.write(f'facet normal {n[0]:.4f} {n[1]:.4f} {n[2]:.4f}\n outer loop\n')
            for p in (a, b, c):
                f.write(f'  vertex {p[0]:.3f} {p[1]:.3f} {p[2]:.3f}\n')
            f.write(' endloop\nendfacet\n')
        f.write('endsolid m\n')


def arcs(step=5):
    """Unit vectors: the horizontal circle (positive to the listener's right... fab/bem.py's +x) and the vertical
    (positive up), each from -180 to 180 - step degrees, measured from the axis (-y)."""
    a = np.arange(-180, 180, step)
    r = np.radians(a)
    hor = np.stack([np.sin(r), -np.cos(r), np.zeros_like(r)])
    ver = np.stack([np.zeros_like(r), -np.cos(r), np.sin(r)])
    return a, hor, ver


def solve(V, T, D, freqs, radiators=(1,), log=print):
    """Each radiator's far field (complex, on the two circles and a sphere of 600 directions) and the mean pressure on
    its own face, for a unit normal velocity... a unit normal derivative of the pressure on it (dp/dn = i w rho v)."""
    import bempp_cl.api as bempp
    from scipy.linalg import lu_factor, lu_solve
    bempp.DEFAULT_PRECISION = 'single'
    bempp.DEFAULT_DEVICE_INTERFACE = device()
    grid = bempp.Grid(V.T / 1000.0, T.T.astype(np.uint32), D.astype(np.uint32))
    P1 = bempp.function_space(grid, 'P', 1)
    sp = {r: bempp.function_space(grid, 'DP', 0, segments=[r]) for r in radiators}
    g = {r: bempp.GridFunction(sp[r], coefficients=np.ones(sp[r].global_dof_count, dtype=np.complex128)) for r in radiators}
    ang, hor, ver = arcs()
    sph = sphere(600)
    pts = np.concatenate([hor, ver, sph], 1)
    nh, nv = hor.shape[1], ver.shape[1]
    area = {r: float(np.real(g[r].projections(sp[r]).sum())) for r in radiators}    # each radiator's face, m^2
    out = []
    for f in freqs:
        t0 = time.time(); k = 2 * np.pi * f / C_AIR
        eta = 1j / k
        # D - I/2 + eta H, built in one Fortran-ordered single-precision array: each operator assembled alone and
        # dropped before the next (the sum operator's own assembly held four dense copies at once, and the 8 kHz
        # mesh's 14,400 unknowns ran the container out of memory)
        A = np.array(bempp.operators.boundary.helmholtz.double_layer(P1, P1, P1, k).weak_form().to_dense(),
                     dtype=np.complex64, order='F')
        gc.collect()
        Hd = bempp.operators.boundary.helmholtz.hypersingular(P1, P1, P1, k).weak_form().to_dense()
        np.multiply(Hd, np.complex64(eta), out=Hd)
        A += Hd
        del Hd; gc.collect()
        Isp = bempp.operators.boundary.sparse.identity(P1, P1, P1).weak_form().A.tocoo()
        np.add.at(A, (Isp.row, Isp.col), (-0.5 * Isp.data).astype(np.complex64))
        lu = lu_factor(A, overwrite_a=True, check_finite=False)
        del A; gc.collect()
        DLf = bempp.operators.far_field.helmholtz.double_layer(P1, pts, k)
        res = dict(f=f, k=k)
        for r in radiators:
            Ig = bempp.operators.boundary.sparse.identity(sp[r], P1, P1)
            Sg = bempp.operators.boundary.helmholtz.single_layer(sp[r], P1, P1, k)
            Dpg = bempp.operators.boundary.helmholtz.adjoint_double_layer(sp[r], P1, P1, k)
            b = ((Sg - eta * (0.5 * Ig + Dpg)) * g[r]).projections(P1)
            coeffs = lu_solve(lu, b, check_finite=False)
            p = bempp.GridFunction(P1, coefficients=coeffs)
            SLf = bempp.operators.far_field.helmholtz.single_layer(sp[r], pts, k)
            pf = (DLf * p - SLf * g[r]).ravel()
            pm = complex(p.projections(sp[r]).sum()) / area[r]     # the mean pressure on its face
            res[str(r)] = dict(h=[[float(z.real), float(z.imag)] for z in pf[:nh]],
                               v=[[float(z.real), float(z.imag)] for z in pf[nh:nh + nv]],
                               power=float(np.mean(np.abs(pf[nh + nv:]) ** 2)),
                               p_face=[pm.real, pm.imag])
        res['seconds'] = round(time.time() - t0, 1)
        out.append(res)
        del lu, DLf; gc.collect()
        log(f'{f:7.0f} Hz  {res["seconds"]:7.1f} s', flush=True)
    return dict(angles=ang.tolist(), results=out)


def icosphere(R=100.0, level=4):
    t = (1 + 5 ** 0.5) / 2
    V = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
         (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    F = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6),
         (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7),
         (9, 8, 1)]
    V = [np.array(v, float) / np.linalg.norm(v) for v in V]
    for _ in range(level):
        mid = {}
        def m(i, j):
            key = (min(i, j), max(i, j))
            if key not in mid:
                v = V[i] + V[j]; V.append(v / np.linalg.norm(v)); mid[key] = len(V) - 1
            return mid[key]
        F = [f for a, b, c in F for f in ((a, m(a, b), m(c, a)), (b, m(b, c), m(a, b)), (c, m(c, a), m(b, c)), (m(a, b), m(b, c), m(c, a)))]
    return np.array(V) * R, np.array(F, int)


def check():
    """The pulsating sphere (radius 0.1 m, every triangle the radiator): the mean surface pressure against the exact
    a / (i k a - 1) for dp/dn = 1, and the normalised radiation impedance i k p against ((ka)^2 - i ka) / (1 + (ka)^2)."""
    V, T = icosphere(100.0, 4)
    T = consistent_orientation(V, T)
    D = np.ones(len(T), np.uint32)
    a = 0.1
    freqs = [C_AIR * ka / (2 * np.pi * a) for ka in (0.5, 1.0, 2.0, np.pi)]
    r = solve(V, T, D, freqs, radiators=(1,))
    for res in r['results']:
        k = res['k']; ka = k * a
        pm = complex(*res['1']['p_face']); exact = a / (1j * ka - 1)
        z = 1j * k * pm; ze = ((ka) ** 2 - 1j * ka) / (1 + ka ** 2)
        print(f'ka {ka:5.3f}: p {pm.real:+.5f}{pm.imag:+.5f}i exact {exact.real:+.5f}{exact.imag:+.5f}i   '
              f'z {z.real:.4f}{z.imag:+.4f}i exact {ze.real:.4f}{ze.imag:+.4f}i')


def build(band_name, P=None, profile=None, bell=None):
    import product
    P = P or product.P
    band = BANDS[band_name]
    horn = BellHorn(P, bell) if bell else Horn(P, profile)
    V, T, D = horn_mesh(horn, band)
    radiators = (1,)
    if band_name == 'cab':
        Vb, Tb, Db = box_mesh(P, band['h_box'])
        T = np.concatenate([T, Tb + len(V)]); V = np.concatenate([V, Vb]); D = np.concatenate([D, Db])
        radiators = (1, 2)
    return horn, V, T, D, radiators


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['check', 'mesh', 'solve'])
    ap.add_argument('band', nargs='?', default='lo')
    ap.add_argument('--name', default='horn', help='the run\'s name: acoustics/<name>-<band>.json')
    ap.add_argument('--freqs', nargs='+', type=float, default=None)
    ap.add_argument('--bell', type=float, default=None, help='the proposal: a bell-flared lip of this radius across (mm)')
    a = ap.parse_args()
    if a.cmd == 'check':
        return check()
    horn, V, T, D, radiators = build(a.band, bell=a.bell)
    if a.bell:
        print(f'bell: the flare to {horn.d1:.1f} on a {2 * horn.hw1:.0f} x {2 * horn.hh1:.0f} mouth, its walls at {math.degrees(horn.th[0]):.1f} '
              f'and {math.degrees(horn.th[1]):.1f} deg, curled on {horn.R[0]:.0f} and {horn.R[1]:.0f} mm to {2 * horn.hw:.0f} x {2 * horn.hh:.0f}')
    q = quality(V, T)
    print(f'{a.band}: {len(V)} vertices, {len(T)} triangles ({int((D == 1).sum())} on the piston, {int((D == 2).sum())} on the woofer); '
          f'open edges {watertight(T)}; area {q["area"]:.3f} m2; edges mean {q["edge_mean"]:.1f} max {q["edge_max"]:.1f} mm; '
          f'aspect p95 {q["aspect_p95"]:.2f} max {q["aspect_max"]:.1f}; degenerate {q["degenerate"]}', flush=True)
    OUT.mkdir(exist_ok=True)
    if a.cmd == 'mesh':
        write_stl(OUT / f'{a.name}-{a.band}.stl', V, T)
        return
    freqs = a.freqs or BANDS[a.band]['freqs']
    r = solve(V, T, D, freqs, radiators)
    r['meta'] = dict(band=a.band, mesh=dict(vertices=len(V), triangles=len(T), **{k: v for k, v in BANDS[a.band].items() if k != 'freqs'}),
                     axis=dict(cx=horn.cx, zc=horn.zc), radiators=list(radiators))
    (OUT / f'{a.name}-{a.band}.json').write_text(json.dumps(r))


if __name__ == '__main__':
    main()
