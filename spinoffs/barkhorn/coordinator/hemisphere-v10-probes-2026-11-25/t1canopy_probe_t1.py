"""T1 canopy probe (read-only): loads one package's BREPs (built by build1.py from the lane's crystal.py at 58e4f5d036),
turns A-with-the-lock back by -105 deg so every package is measured in the canopy's own drawing frame (x on the cables'
line, h = z - 726 above the canopy's underside), and measures:
  1. every overlap between a canopy part and any part (no exemptions, any volume > 0);
  2. gaps between named pairs (the driver body and its leads split out);
  3. tool access (saddle screws, box screws, WAGO levers);
  4. real-part substitutions (ERP's real tab holes, PEM S-M3-1 at its real 6.35 x 1.5, Heyco SB 250-2, WAGO 221-500).
Usage: python -I probe_t1.py <package>    (today | A-lock | A-nolock | B)"""
import os, sys, json, math, itertools
from build123d import import_brep, Box, Cylinder, Pos, Rot, Location, Axis, Solid, Compound

S = '/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/b110/t1canopy'
pkg = sys.argv[1]
d = os.path.join(S, 'brep', pkg)
info = json.load(open(os.path.join(d, 'info.json')))
A0 = 105.0 if pkg == 'A-lock' else 0.0
ZC = 726.0
out = {}

def load(n):
    sh = import_brep(os.path.join(d, n + '.brep'))
    if A0:
        sh = sh.rotate(Axis.Z, -A0)
    return sh

parts = {n: load(n) for n in info}
CAN = [n for n, v in info.items() if v['group'] == 'canopy'] + ['cord', 'suspension']

def H(h):
    return ZC + h

def box(x0, y0, z0, x1, y1, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)

def cyl(axis, c, dia, a0, a1):
    L = a1 - a0
    if axis == 'z':
        return Pos(c[0], c[1], (a0 + a1) / 2) * Cylinder(dia / 2, L)
    if axis == 'x':
        return Pos((a0 + a1) / 2, c[0], c[1]) * (Rot(0, 90, 0) * Cylinder(dia / 2, L))
    if axis == 'y':
        return Pos(c[0], (a0 + a1) / 2, c[1]) * (Rot(90, 0, 0) * Cylinder(dia / 2, L))

def vol(a, b):
    try:
        i = a & b
        return 0.0 if i is None else float(i.volume)
    except Exception as e:  # noqa: BLE001
        return float('nan')

def bbo(a, b, m=0.5):
    A, B = a.bounding_box(), b.bounding_box()
    return not (A.max.X + m < B.min.X or B.max.X + m < A.min.X or A.max.Y + m < B.min.Y or B.max.Y + m < A.min.Y
                or A.max.Z + m < B.min.Z or B.max.Z + m < A.min.Z)

def gap(a, b):
    try:
        return round(float(a.distance_to(b)), 3)
    except Exception as e:  # noqa: BLE001
        return f'err {e}'

# ---- 1. overlaps, no exemptions --------------------------------------------------------------------------------
ov = []
names = sorted(parts)
for a, b in itertools.combinations(names, 2):
    if a not in CAN and b not in CAN:
        continue
    if not bbo(parts[a], parts[b], 0.0):
        continue
    v = vol(parts[a], parts[b])
    if v != 0.0:
        ov.append((a, b, round(v, 4)))
out['overlaps'] = ov

# ---- split the driver into its body and leads -------------------------------------------------------------------
drv = parts['driver']
body_reg = box(-34.0, -51.0, H(7.9), -8.8, 33.0, H(47.9))
body = drv & body_reg
inp = drv & box(-40, 33.0, H(0), 0, 60, H(120))           # the input leads (+y end, up into the box)
led = drv - body_reg - box(-40, 33.0, H(0), 0, 60, H(120))  # the LED leads (-y end, round the tray)
out['driver_split_volumes'] = dict(body=round(body.volume, 1), input_leads=round(inp.volume, 1), led_leads=round(led.volume, 1))

g = {}
def G(k, a, b):
    g[k] = gap(a, b)
P = parts
G('body|tray-u (inner wall, bottom)', body, P['tray-u'])
G('body|tray-wall', body, P['tray-wall'])
G('body|strap (plate underside)', body, P['strap'])
G('body|canopy-studs', body, P['canopy-studs'])
G('body|tray-screws', body, P['tray-screws'])
G('body|lead-bushing', body, P['lead-bushing'])
G('input leads|tray-screws (joint screw+nut)', inp, P['tray-screws'])
G('input leads|tray-u (flange, end wall)', inp, P['tray-u'])
G('input leads|tray-wall', inp, P['tray-wall'])
G('input leads|strap (the opening)', inp, P['strap'])
G('input leads|canopy-studs', inp, P['canopy-studs'])
G('input leads|ground-screw', inp, P['ground-screw'])
G('LED leads|lead-bushing', led, P['lead-bushing'])
G('LED leads|tray-u', led, P['tray-u'])
G('LED leads|canopy', led, P['canopy'])
G('LED leads|tray-screws', led, P['tray-screws'])
G('LED leads|splices', led, P['splices'])
G('LED leads|cord-clamp', led, P['cord-clamp'])
G('LED leads|relief-bracket', led, P['relief-bracket'])
G('LED leads|box-screws', led, P['box-screws'])
G('LED leads|cord', led, P['cord'])
G('splices|tray-u', P['splices'], P['tray-u'])
G('splices|strap', P['splices'], P['strap'])
G('splices|relief-bracket', P['splices'], P['relief-bracket'])
G('splices|cord-clamp', P['splices'], P['cord-clamp'])
G('cord|cord-clamp', P['cord'], P['cord-clamp'])
G('cord|relief-bracket', P['cord'], P['relief-bracket'])
G('cord|canopy-bushing', P['cord'], P['canopy-bushing'])
G('cord|tray-u', P['cord'], P['tray-u'])
G('cord|splices', P['cord'], P['splices'])
G('ground-screw|relief-bracket', P['ground-screw'], P['relief-bracket'])
G('ground-screw|canopy-studs', P['ground-screw'], P['canopy-studs'])
G('ground-screw|gripper-brackets', P['ground-screw'], P['gripper-brackets'])
G('ground-screw|splices', P['ground-screw'], P['splices'])
G('ground-screw|cord', P['ground-screw'], P['cord'])
G('ground-screw|box-screws', P['ground-screw'], P['box-screws'])
G('tray-u|gripper-brackets', P['tray-u'], P['gripper-brackets'])
G('tray-wall|gripper-brackets', P['tray-wall'], P['gripper-brackets'])
G('tray-wall|gripper-nuts', P['tray-wall'], P['gripper-nuts'])
G('tray-u|box-screws', P['tray-u'], P['box-screws'])
G('tray-wall|canopy', P['tray-wall'], P['canopy'])
G('tray-u|canopy', P['tray-u'], P['canopy'])
G('tray-u|canopy-bushing', P['tray-u'], P['canopy-bushing'])
G('tray-u|suspension', P['tray-u'], P['suspension'])
G('tray-wall|suspension', P['tray-wall'], P['suspension'])
G('relief-bracket|box-screws', P['relief-bracket'], P['box-screws'])
G('relief-bracket|gripper-brackets', P['relief-bracket'], P['gripper-brackets'])
G('cord-clamp|tray-u', P['cord-clamp'], P['tray-u'])
G('lead-bushing|canopy', P['lead-bushing'], P['canopy'])
G('lead-bushing|tray-wall', P['lead-bushing'], P['tray-wall'])
out['gaps'] = g

# the tray's rim against the plate: the gap between each tray part's top and the plate's underside
zp = H(48.4)
rim = {}
for n in ('tray-wall', 'tray-u'):
    bb = P[n].bounding_box()
    rim[n + ' top z'] = round(bb.max.Z - ZC, 3)
out['rim_vs_plate_underside_h48.4'] = rim

# ---- 3. tool access ---------------------------------------------------------------------------------------------
acc = {}
others = [n for n in names if n not in ('cord-clamp', 'canopy')]   # the canopy is lowered for the cord step
# saddle screws: heads at x 0.2..2.0, axis along x at (y -+8, h 11); a O6 driver shaft from x 0.2 toward -x
for sy in (-8.0, 8.0):
    for L in (10.0, 25.0, 50.0, 120.0):
        shaft = cyl('x', (sy, H(11.0)), 6.0, 0.2 - L, 0.2)
        hits = [(n, round(vol(shaft, P[n]), 2)) for n in others if bbo(shaft, P[n], 0.0) and vol(shaft, P[n]) > 0]
        acc[f'saddle screw y{sy:+.0f}: O6 shaft {L:.0f} long along -x'] = hits
    # how far along -x before the first hit (free length), 0.1 steps
    free = None
    for k in range(1, 200):
        x0 = 0.2 - 0.1 * k
        seg = cyl('x', (sy, H(11.0)), 6.0, x0, 0.2)
        if any(vol(seg, P[n]) > 1e-6 for n in ('tray-u', 'tray-wall', 'splices', 'driver', 'tray-screws')):
            free = round(0.2 - x0, 1); break
    acc[f'saddle screw y{sy:+.0f}: free length along -x for a O6 shaft'] = free
    # tilted in the x-z plane, coming from below (the canopy lowered): smallest tilt that clears 120 of shaft
    best = None
    for ang in range(0, 91, 1):
        shaft = cyl('x', (sy, H(11.0)), 6.0, 0.2 - 120.0, 0.2)
        shaft = shaft.rotate(Axis((0.2, sy, H(11.0)), (0, 1, 0)), -ang)   # tip at the head, handle going down and -x
        hit = [n for n in others if bbo(shaft, P[n], 0.0) and vol(shaft, P[n]) > 1e-6]
        if not hit:
            best = ang; break
    acc[f'saddle screw y{sy:+.0f}: smallest tilt below horizontal that clears a O6 x 120 shaft'] = best
# box screws: a O6 shaft straight down from each head, for the four positions the slots allow
bs = []
for ys in (-44.45, -34.925, 34.925, 44.45):
    shaft = cyl('z', (0.0, ys), 6.0, H(48.4) - 2.4 - 150.0, H(48.4) - 2.4)
    hit = [(n, round(vol(shaft, P[n]), 2)) for n in names if n not in ('box-screws', 'canopy') and bbo(shaft, P[n], 0.0) and vol(shaft, P[n]) > 1e-6]
    bs.append((ys, hit))
acc['box screws: O6 x 150 shaft straight down (canopy lowered)'] = bs
# WAGO 221-412 levers: each lever on the splice's -x face (the base of a 221-412 sits in its carrier), swinging
# open about 90 deg: its tip travels about 13 off the face. Room in front of the -x face:
acc['splices -x face to tray inner wall (lever room)'] = gap(box(-6.7, -13.6, H(28.5), -6.69, 13.6, H(46.8)), P['tray-u'])
lev = box(-6.7 - 13.0, -13.6, H(28.5), -6.7, 13.6, H(46.8))
acc['lever swing zone (13 off the -x face) overlaps'] = [(n, round(vol(lev, P[n]), 1)) for n in names if bbo(lev, P[n], 0.0) and vol(lev, P[n]) > 0]
out['access'] = acc

# ---- 4. real parts ----------------------------------------------------------------------------------------------
real = {}
# ERP: holes 3.5 from the case's ends and sides (fig. 7: 84/77, 40/33); the case at y -51..33, h 7.9..47.9
erp_holes = [(33.0 - 3.5, 47.9 - 3.5), (-51.0 + 3.5, 7.9 + 3.5)]
cad_holes = [(27.7, 44.4), (-49.7, 11.1)]
real['ERP real tab holes (y, h)'] = erp_holes
real['CAD studs (y, h)'] = cad_holes
real['offsets (mm)'] = [round(math.hypot(a[0] - b[0], a[1] - b[1]), 2) for a, b in zip(erp_holes, cad_holes)]
real['CAD pattern (dy, dh)'] = (round(cad_holes[0][0] - cad_holes[1][0], 2), round(cad_holes[0][1] - cad_holes[1][1], 2))
# the real tab: 1.8 at the base (x -34..-32.2) in a corner pocket about 6.5 x 6.5 (fig. 7 at 600 dpi: the case wall
# arcs about 6 to 7 from the ends and sides at the base); its hole O3.2 at the real position
tabs = None
for (hy, hh), (ylo, yhi, hlo, hhi) in zip(erp_holes, ((33.0 - 6.5, 33.0, 47.9 - 6.5, 47.9), (-51.0, -51.0 + 6.5, 7.9, 7.9 + 6.5))):
    t = box(-34.0, ylo, H(hlo), -32.2, yhi, H(hhi)) - cyl('x', (hy, H(hh)), 3.2, -35, -31)
    tabs = t if tabs is None else tabs + t
studs_cad = None
for hy, hh in cad_holes:
    s = cyl('x', (hy, H(hh)), 3.0, -35.0, -29.0)
    studs_cad = s if studs_cad is None else studs_cad + s
real['CAD studs through the REAL tabs (mm3)'] = round(vol(studs_cad, tabs), 2)
# PEM edge distances for the studs as drawn and as they should be, in the 1.0 wall (y -58..41, h 6.4..48.4)
def edge(hy, hh):
    return round(min(hy + 58.0, 41.0 - hy, hh - 6.4, 48.4 - hh), 2)
real['FH-M3 C/L-to-edge in the wall, CAD (PEM min 5.6)'] = [edge(*c) for c in cad_holes]
real['FH-M3 C/L-to-edge in the wall, at ERP holes (PEM min 5.6)'] = [edge(*c) for c in erp_holes]
# the plate stud at (-21, 45.5) to the O8 opening's edge at (-21, 36.5)
real['plate FH-M3-8 at (-21,45.5): C/L to the O8 opening edge (PEM min 5.6)'] = round(9.0 - 4.0, 2)
# PEM S-M3-1 at its real size (E 6.35, T 1.5; min C/L to edge 4.8) at the two joint flanges
pem = None
for ys, hs in ((-54.2, 22.0), (37.0, 10.2)):
    n_ = cyl('x', (ys, H(hs)), 6.35, -33.0, -31.5)
    pem = n_ if pem is None else pem + n_
real['real S-M3-1 collars vs tray-u (mm3)'] = round(vol(pem, P['tray-u'] - box(-34.0, -60, H(0), -33.0, 60, H(60))), 3)
real['joint flanges: C/L to edges (y-, y+, h-, h+) -y flange y -57..-52 h 17.5..26.5'] = (round(-54.2 + 57, 2), round(-52 + 54.2, 2), round(22 - 17.5, 2), round(26.5 - 22, 2))
real['joint flanges: C/L to edges +y flange y 35..40 h 7.4..14.7'] = (round(37 - 35, 2), round(40 - 37, 2), round(10.2 - 7.4, 2), round(14.7 - 10.2, 2))
pem_web = None
for sy in (-8.0, 8.0):
    n_ = cyl('x', (sy, H(11.0)), 6.35, 4.6, 6.1)
    pem_web = n_ if pem_web is None else pem_web + n_
real['real S-M3-1 collars in the clamp web vs relief-bracket side flanges (mm3)'] = round(vol(pem_web, P['relief-bracket'] - box(3.0, -12.4, H(0), 4.6, 12.4, H(60))), 3)
# Heyco SB 250-2 (#2000): hole .250, ID .140 (3.6), head O.312 (7.9), overall .312 (7.9); head taken 1.3 thick
sbA = (cyl('y', (-29.0, H(32.0)), 7.9, -59.3, -58.0) + cyl('y', (-29.0, H(32.0)), 6.4, -58.0, -58.0 + 7.9 - 1.3)) - cyl('y', (-29.0, H(32.0)), 3.6, -70, -40)
sbB = (cyl('y', (-29.0, H(32.0)), 7.9, -57.0, -55.7) + cyl('y', (-29.0, H(32.0)), 6.4, -57.0 - (7.9 - 1.3), -57.0)) - cyl('y', (-29.0, H(32.0)), 3.6, -70, -40)
real['SB 250-2 head outside, body inside: vs driver body (mm3)'] = round(vol(sbA, body), 3)
real['SB 250-2 head outside, body inside: gap to driver body'] = gap(sbA, body)
real['SB 250-2 head inside, body outside: gap to canopy wall'] = gap(sbB, P['canopy'])
real['two 18 AWG leads (O2.0 each, 300 V) need a bore of'] = 4.0
real['SB 250-2 bore'] = 3.6
# WAGO 221-500 carrier 77.6 x 25.5 x 17.5 vs the room the CAD gives it (x -7..3 between the tray and the web)
real['221-500 size'] = (77.6, 25.5, 17.5)
real['room between tray inner wall (x -7) and clamp web (x 3)'] = 10.0
out['real'] = real
json.dump(out, open(os.path.join(S, 'out', f'probe-{pkg}.json'), 'w'), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
