# Measurements on the V10 canopy solids (A without the lock), in the canopy's frame (z above its underside).
import os, sys, json, math
from build123d import import_brep, Box, Cylinder, Pos, Rot, Align, Plane, Compound, Location
D = sys.argv[1]
P = {f[:-5]: import_brep(os.path.join(D, f)) for f in os.listdir(D) if f.endswith('.brep')}
can = P['canopy']; zc = can.bounding_box().min.Z
def H(h): return zc + h
def box(x0, y0, z0, x1, y1, z1):
    return Pos(min(x0, x1), min(y0, y1), min(z0, z1)) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), align=Align.MIN)
def cylx(y, z, d, x0, x1):
    lo, L = min(x0, x1), abs(x1 - x0)
    return Pos(lo, y, z) * Rot(0, 90, 0) * Cylinder(d / 2, L, align=(Align.CENTER, Align.CENTER, Align.MIN))
def vol(a, b):
    try:
        i = a & b
        return round(sum(s.volume for s in i.solids()), 3) if i is not None else 0.0
    except Exception as e:
        return 'err ' + str(e)
def dist(a, b):
    return round(a.distance_to(b), 3)
out = {'zc': round(zc, 3)}
bb = lambda s: [round(v, 2) for v in (s.bounding_box().min.X, s.bounding_box().min.Y, s.bounding_box().min.Z - zc,
                                      s.bounding_box().max.X, s.bounding_box().max.Y, s.bounding_box().max.Z - zc)]
for n in ('tray-u', 'tray-wall', 'splices', 'cord-clamp', 'relief-bracket', 'driver', 'tray-screws', 'lead-bushing', 'cord'):
    out['bbox ' + n] = bb(P[n])
# 1. the splices' lever faces against the tray's inner wall
out['dist splices-trayU'] = dist(P['splices'], P['tray-u'])
# 2. a screwdriver (shaft Ø5) on each saddle screw's axis from its head toward -x, 80 long: what it meets
for sy in (-8.0, 8.0):
    sd = cylx(sy, H(11.0), 5.0, 0.15, -80.0)
    out[f'screwdriver y{sy:+.0f}'] = {n: vol(sd, P[n]) for n in ('tray-u', 'tray-wall', 'driver', 'splices', 'cord', 'cord-clamp', 'gripper-brackets', 'canopy')}
    # the clear run from the head to the first obstacle
    clear = None
    for k in range(1, 81):
        seg = cylx(sy, H(11.0), 5.0, 0.15, 0.15 - k)
        if any(vol(seg, P[n]) not in (0.0,) for n in ('tray-u', 'tray-wall', 'driver')):
            clear = k - 1; break
    out[f'screwdriver clear run y{sy:+.0f}'] = clear
# 3. a real ERP case (84 x 40 x 25.2, tabs at the base, holes 77 x 33 apart, 3.5 from the ends and sides) centred on the
#    drawn studs' midpoint (27.7, 44.4) and (-49.7, 11.1): what it meets
ym, zm = (27.7 - 49.7) / 2, (44.4 + 11.1) / 2
real = box(-34.0, ym - 42, H(zm - 20), -8.8, ym + 42, H(zm + 20))
# keep ERP's corner pockets clear as the CAD draws them (relative to the holes): +y top pocket from 4.2 short of the hole
# to the end, -y bottom pocket likewise (generous: 7 x 7.5 around each hole, above the 1.8 tab)
hy1, hz1 = ym + 38.5, zm + 16.5     # ERP hole near +y, high z
hy2, hz2 = ym - 38.5, zm - 16.5     # ERP hole near -y, low z
real = real - box(-32.2, hy1 - 4.5, H(hz1 - 4.0), -8.0, ym + 43, H(zm + 21)) - box(-32.2, ym - 43, H(zm - 21), -8.0, hy2 + 4.5, H(hz2 + 4.0))
out['real case y'] = [round(ym - 42, 2), round(ym + 42, 2)]; out['real case z'] = [round(zm - 20, 2), round(zm + 20, 2)]
out['real case meets'] = {n: vol(real, P[n]) for n in ('tray-u', 'tray-wall', 'tray-screws', 'canopy-studs', 'lead-bushing', 'cord-clamp', 'splices')}
out['drawn case meets'] = {n: vol(P['driver'], P[n]) for n in ('tray-u', 'tray-wall', 'tray-screws', 'lead-bushing')}
# 4. the saddle squeeze: the cord against the saddle and the web
out['dist cord-cordclamp'] = dist(P['cord'], P['cord-clamp']); out['dist cord-reliefbracket'] = dist(P['cord'], P['relief-bracket'])
out['vol cord&cordclamp'] = vol(P['cord'], P['cord-clamp']); out['vol cord&reliefbracket'] = vol(P['cord'], P['relief-bracket'])
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps(out, indent=1))
