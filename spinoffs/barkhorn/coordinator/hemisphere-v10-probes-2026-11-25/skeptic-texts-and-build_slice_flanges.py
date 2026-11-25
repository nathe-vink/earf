import os, sys, json
from build123d import import_brep, Plane, Vector, Box, Pos, Align
D = sys.argv[1]
tu = import_brep(os.path.join(D, 'tray-u.brep')); zc = import_brep(os.path.join(D, 'canopy.brep')).bounding_box().min.Z
def box(x0, y0, z0, x1, y1, z1):
    return Pos(min(x0, x1), min(y0, y1), min(z0, z1)) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), align=Align.MIN)
out = {}
# the two joint flanges alone: tray-u within x -34 to -33 (the flanges' layer) and the end walls excluded
for nm, (y0, y1) in (('flange -y', (-57.0, -52.0)), ('flange +y', (35.0, 40.0))):
    f = tu & box(-34.0, y0, zc, -33.0, y1, zc + 50)
    b = f.bounding_box()
    # the material's y extent at the hole's height (z of the hole), by thin slabs
    zs = 22.0 if nm == 'flange -y' else 10.2
    ys = -54.2 if nm == 'flange -y' else 37.0
    prof = []
    k = y0
    while k < y1 - 1e-9:
        s = f & box(-34.0, k, zc + zs - 0.01, -33.0, k + 0.05, zc + zs + 0.01)
        v = sum(x.volume for x in s.solids()) if s is not None else 0.0
        prof.append(1 if v > 1e-6 else 0)
        k += 0.05
    # runs of metal along y at the hole's height
    runs = []; start = None
    for i, m in enumerate(prof + [0]):
        y = y0 + 0.05 * i
        if m and start is None: start = y
        if not m and start is not None: runs.append([round(start, 2), round(y, 2)]); start = None
    out[nm] = dict(vol=round(f.volume, 2), bbox_y=[round(b.min.Y, 2), round(b.max.Y, 2)], bbox_z=[round(b.min.Z - zc, 2), round(b.max.Z - zc, 2)],
                   metal_runs_y_at_hole_height=runs, hole_y=ys)
json.dump(out, open(sys.argv[2], 'w'), indent=1); print(json.dumps(out, indent=1))
