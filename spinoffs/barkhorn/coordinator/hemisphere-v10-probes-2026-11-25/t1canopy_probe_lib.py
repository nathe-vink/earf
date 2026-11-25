import os, sys, json, math, itertools
from build123d import import_brep, Box, Cylinder, Pos, Rot, Axis
S = '/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/b110/t1canopy'
pkg = sys.argv[1]
d = os.path.join(S, 'brep', pkg)
info = json.load(open(os.path.join(d, 'info.json')))
A0 = 105.0 if pkg == 'A-lock' else 0.0
ZC = 726.0
def load(n):
    sh = import_brep(os.path.join(d, n + '.brep'))
    return sh.rotate(Axis.Z, -A0) if A0 else sh
P = {n: load(n) for n in info}
names = sorted(P)
def H(h): return ZC + h
def box(x0, y0, z0, x1, y1, z1): return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)
def cyl(axis, c, dia, a0, a1):
    L = a1 - a0
    if axis == 'z': return Pos(c[0], c[1], (a0 + a1) / 2) * Cylinder(dia / 2, L)
    if axis == 'x': return Pos((a0 + a1) / 2, c[0], c[1]) * (Rot(0, 90, 0) * Cylinder(dia / 2, L))
    if axis == 'y': return Pos(c[0], (a0 + a1) / 2, c[1]) * (Rot(90, 0, 0) * Cylinder(dia / 2, L))
def vol(a, b):
    try:
        i = a & b; return 0.0 if i is None else float(i.volume)
    except Exception: return float('nan')
def bbo(a, b, m=0.5):
    A, B = a.bounding_box(), b.bounding_box()
    return not (A.max.X + m < B.min.X or B.max.X + m < A.min.X or A.max.Y + m < B.min.Y or B.max.Y + m < A.min.Y or A.max.Z + m < B.min.Z or B.max.Z + m < A.min.Z)
