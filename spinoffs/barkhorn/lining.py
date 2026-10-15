"""Does the Cloud's cabinet want more lining? (round 18, the owner: "Should there be more insulation on the bottom of the
cabinet or elsewhere, or are we good there?")

The box's own resonances, its standing waves, reach the listener through the woofer's cone and out of the ports, and
the woofer plays up to the horn's crossover at 800 Hz. This finds them in the Cloud's cabinet (inside: its 20 mm sheet
off each face, the front panel set back), how hard the woofer drives each one (the mode's shape averaged over its cone)
and how much of it each port's inner end picks up, and how well the lining damps it: each batt's admittance by Miki's
model of a porous layer on a rigid wall (polyester at about 30 kg/m3, an airflow resistivity of about 12,000 Pa s/m2),
summed over the batts the build cut (their sizes and places read from out-cloud/stl) as each mode's shape weights them,
gives the mode's decay and so its Q. The cone, the ports and the acrylic damp the modes too, so the Qs are the lining's
share alone, an upper bound; they compare the linings fairly. A Q under about 5 is well damped; 20 rings.

    python3 spinoffs/barkhorn/lining.py            (after the Cloud's build, for out-cloud/stl)
"""
import csv, math, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cloud                                              # noqa: E402
import product as pr                                      # noqa: E402

RHO, C = 1.204, 343.0
SIGMA = 12000.0                                           # Pa s/m2: polyester batt, about 30 kg/m3
F_TOP = 800.0                                             # the horn's crossover


def miki(f, d, sigma=SIGMA):
    """The surface impedance (Pa s/m) of a porous layer `d` (m) thick on a rigid wall at normal incidence, Miki 1990
    (e^{j w t}), and its absorption coefficient."""
    x = f / sigma
    zc = RHO * C * complex(1 + 0.0699 * x ** -0.632, -0.1071 * x ** -0.632)
    k = (2 * math.pi * f / C) * complex(1 + 0.1093 * x ** -0.618, -0.1597 * x ** -0.618)
    kd = k * d
    zs = -1j * zc * (complex(math.cos(kd.real) * math.cosh(kd.imag), -math.sin(kd.real) * math.sinh(kd.imag))
                     / complex(math.sin(kd.real) * math.cosh(kd.imag), math.cos(kd.real) * math.sinh(kd.imag)))   # cot(kd)
    r = (zs - RHO * C) / (zs + RHO * C)
    return zs, 1 - abs(r) ** 2


def stl_box(path):
    """A binary STL's bounding box (mm) and volume (mm3)."""
    data = open(path, 'rb').read()
    n = struct.unpack('<I', data[80:84])[0]
    lo, hi, vol = [1e9] * 3, [-1e9] * 3, 0.0
    for i in range(n):
        v = struct.unpack('<9f', data[84 + 50 * i + 12: 84 + 50 * i + 48])
        a, b, c = v[0:3], v[3:6], v[6:9]
        for p in (a, b, c):
            lo = [min(lo[j], p[j]) for j in range(3)]; hi = [max(hi[j], p[j]) for j in range(3)]
        vol += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6
    return lo, hi, abs(vol)


def batts(out_dir):
    """The batts the build cut (the parts list's names: stale files of earlier builds are skipped), each as its wall,
    its face's rectangle on the inside box's coordinates (m, from the inside corner at the front panel, bottom, left)
    and the share of that rectangle it fills (a batt notched round a keep-out fills less)."""
    names = []
    for row in csv.reader(open(os.path.join(out_dir, 'bom.csv'))):
        if row and 'lining-' in row[0] and row[1] == 'cut':
            names += [n.strip() for n in row[0].split(',')]
    P = cloud.P
    x0, y0, z0 = P['T'], P['inset'] + P['T'], P['T']
    out = []
    for n in names:
        lo, hi, vol = stl_box(os.path.join(out_dir, 'stl', f'{n}.stl'))
        wall = n.split('-')[1]
        ax = {'left': 0, 'right': 0, 'back': 1, 'top': 2, 'bottom': 2}[wall]
        t = hi[ax] - lo[ax]
        rect = [((lo[j] - o) / 1000, (hi[j] - o) / 1000) for j, o in enumerate((x0, y0, z0)) if j != ax]
        span = [hi[j] - lo[j] for j in range(3) if j != ax]
        fill = vol / t / (span[0] * span[1])
        out.append(dict(name=n, wall=wall, t=t / 1000, rect=rect, fill=min(fill, 1.0), area=vol / t / 1e6))
    return out


def inside():
    """The inside box (m): across, front (the front panel's back) to back, bottom to top."""
    P = cloud.P
    return ((P['W'] - 2 * P['T']) / 1000, (P['D'] - 2 * P['T'] - P['inset']) / 1000, (P['H'] - 2 * P['T']) / 1000)


def modes(L, f_max=F_TOP):
    Lx, Ly, Lz = L
    out = []
    for nx in range(0, 6):
        for ny in range(0, 6):
            for nz in range(0, 6):
                if nx == ny == nz == 0:
                    continue
                f = C / 2 * math.sqrt((nx / Lx) ** 2 + (ny / Ly) ** 2 + (nz / Lz) ** 2)
                if f <= f_max:
                    out.append((f, (nx, ny, nz)))
    return sorted(out)


def psi(n, L, p):
    return math.prod(math.cos(n[j] * math.pi * p[j] / L[j]) for j in range(3))


def mean_sq(n, L, axis_ranges):
    """The mean of psi^2 over a box of ranges [(a, b), ...] on the axes it spans (the others held), per axis."""
    m = 1.0
    for j, (a, b) in axis_ranges.items():
        k = n[j] * math.pi / L[j]
        if n[j] == 0 or b <= a:
            continue
        m *= 0.5 + (math.sin(2 * k * b) - math.sin(2 * k * a)) / (4 * k * (b - a))
    return m


def q_factor(f, n, L, lining, thick=None):
    """The mode's Q from the lining alone: delta = c / (2 V Lambda) * sum Re(beta) * integral psi^2 over each batt's face
    (Kuttruff's small-admittance result), Q = omega / (2 delta). `thick` maps a wall to a batt thickness in place of the
    built one."""
    V = L[0] * L[1] * L[2]
    lam = math.prod(0.5 if k else 1.0 for k in n)
    total = 0.0
    for b in lining:
        d = (thick or {}).get(b['wall'], b['t'])
        zs, _ = miki(f, d)
        beta = (RHO * C / zs).real
        ax = {'left': 0, 'right': 0, 'back': 1, 'top': 2, 'bottom': 2}[b['wall']]
        pos = {'left': 0.0, 'right': L[0], 'back': L[1], 'top': L[2], 'bottom': 0.0}[b['wall']]
        face = math.cos(n[ax] * math.pi * pos / L[ax]) ** 2
        others = [j for j in range(3) if j != ax]
        ms = mean_sq(n, L, {others[0]: b['rect'][0], others[1]: b['rect'][1]})
        total += beta * face * ms * b['area']
    delta = C / (2 * V * lam) * total
    return (2 * math.pi * f) / (2 * delta) if delta > 0 else float('inf')


def cone_coupling(n, L, centre, a, steps=60):
    """psi averaged over the cone's disc on the front face (y = 0): 1 drives a mode as hard as it can be driven."""
    s, k = 0.0, 0
    for i in range(steps):
        for j in range(steps):
            u, v = -a + 2 * a * (i + 0.5) / steps, -a + 2 * a * (j + 0.5) / steps
            if u * u + v * v <= a * a:
                s += psi(n, L, (centre[0] + u, 0.0, centre[1] + v)); k += 1
    return s / k


def main():
    P = cloud.P
    L = inside()
    out_dir = os.path.join(HERE, 'out-cloud')
    lining = batts(out_dir)
    plen, net = pr.tuned(P)
    a = math.sqrt(pr.LIB[P['woofer']]['ts']['Sd_cm2'] / 1e4 / math.pi)
    wc = ((P['W'] / 2 - P['T']) / 1000, (P['woofer_z'] - P['T']) / 1000)
    port = ((P['port']['x'][0] - P['T']) / 1000, (plen - P['T']) / 1000, (P['port']['z'] - P['T']) / 1000)   # an inner end:
                                                                     # the tube runs plen from the panel's face
    print(f'inside {L[0] * 1000:.0f} x {L[1] * 1000:.0f} x {L[2] * 1000:.0f} mm; ports {plen:.0f} long, their inner ends '
          f'{port[1] * 1000:.0f} back, {port[2] * 1000:.0f} up; the cone {a * 2000:.0f} across, its centre '
          f'{wc[1] * 1000:.0f} up ({wc[1] / L[2]:.0%} of the height)')
    walls = {}
    for b in lining:
        walls.setdefault(b['wall'], []).append(b)
    face = {'left': L[1] * L[2], 'right': L[1] * L[2], 'back': L[0] * L[2], 'top': L[0] * L[1], 'bottom': L[0] * L[1]}
    print('lined:', ', '.join(f'{w} {sum(b["area"] for b in bs) / face[w]:.0%}' for w, bs in walls.items()))
    for d in (0.05, 0.10):
        print(f'absorption, {d * 1000:.0f} mm:', ', '.join(f'{f:.0f} Hz {miki(f, d)[1]:.2f}' for f in (100, 200, 300, 400, 600, 800)))
    rows = []
    print(f'\n{"mode":>9} {"Hz":>5} {"woofer":>7} {"port":>6} {"Q now":>6} {"Q, top+bottom 100":>18} {"Q, all 100":>11}')
    for f, n in modes(L):
        cw = cone_coupling(n, L, wc, a)
        cp = psi(n, L, port)
        q0 = q_factor(f, n, L, lining)
        q1 = q_factor(f, n, L, lining, {'top': 0.10, 'bottom': 0.10})
        q2 = q_factor(f, n, L, lining, {w: 0.10 for w in face})
        rows.append((n, f, cw, cp, q0, q1, q2))
        print(f'{str(n):>9} {f:5.0f} {cw:7.2f} {cp:6.2f} {q0:6.1f} {q1:18.1f} {q2:11.1f}')
    return rows


if __name__ == '__main__':
    main()
