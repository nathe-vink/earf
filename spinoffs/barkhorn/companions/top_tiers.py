"""The top's meshes for the render (2026-11-24, the even-tier PROPOSALS A and B and today's top, with check 3's fixings and
review 2's shade release): builds each with crystal.py (V3) and writes the parts the render loads into
lamp-site-meshes/out-dome-pendant (today) and out-dome-pendant-top{A,B} (stl), with their sizes; the outer silicone ring
also on its own (gasket-out), since the render shows only that one. Run with the CAD venv:
    .venv-fab/bin/python spinoffs/barkhorn/companions/top_tiers.py
lamp_site.py takes A or B with HEMI_TOP; the heat check is hemisphere_thermal.py's last table."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'studio', 'fabkit'))
import crystal as C
from build123d import export_stl, Sphere

NAMES = ('clamp', 'crown', 'gland', 'collar', 'white-disc', 'grip', 'gaskets', 'hub', 'ring', 'suspension', 'crown-screws', 'cord')
for top in (None, 'A', 'B'):
    p = dict(C.V3, top=top) if top else dict(C.V3)
    parts = C.north_parts(p)
    d = os.path.join(HERE, 'lamp-site-meshes', f'out-dome-pendant-top{top}' if top else 'out-dome-pendant', 'stl')
    os.makedirs(d, exist_ok=True)
    for q in parts:
        if q.name in NAMES and q.solid is not None:
            bb = q.solid.bounding_box()
            print(top or 'today', q.name, 'z', round(bb.min.Z, 2), 'to', round(bb.max.Z, 2), 'Ø', round(bb.max.X - bb.min.X, 2),
                  'volume', round(q.solid.volume / 1000, 1), 'cm3')
            # v6: the bowed cord under its own name (the shared cord.stl, which other renders load, stays)
            export_stl(q.solid, os.path.join(d, ('cord-v6' if q.name == 'cord' else q.name) + '.stl'), tolerance=0.02, angular_tolerance=0.1)
            if q.name == 'gaskets':
                R = p['R']
                export_stl(q.solid & (Sphere(R + 3.0) - Sphere(R - 0.5)), os.path.join(d, 'gasket-out.stl'), tolerance=0.02, angular_tolerance=0.1)
