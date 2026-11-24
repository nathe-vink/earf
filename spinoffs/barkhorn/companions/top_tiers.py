"""The top's even tiers (2026-11-24, PROPOSALS A and B, crystal.py TOP_TIERS; the owner's question): builds the clamp
ring, the crown and the gland of each with the shade's main build (V3) and writes their STLs beside the render's other
meshes (lamp-site-meshes/out-dome-pendant-top{A,B}/stl), with their sizes. Run with the CAD venv:
    .venv-fab/bin/python spinoffs/barkhorn/companions/top_tiers.py
lamp_site.py takes them with HEMI_TOP=A or B; the heat check is hemisphere_thermal.py's last table."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'studio', 'fabkit'))
import crystal as C
from build123d import export_stl

for top in (None, 'A', 'B'):
    parts = C.north_parts(dict(C.V3, top=top, white_split=True) if top else C.V3)
    d = os.path.join(HERE, 'lamp-site-meshes', f'out-dome-pendant-top{top}', 'stl')
    for p in parts:
        if p.name in ('clamp', 'crown', 'gland', 'collar', 'white-disc', 'grip', 'gaskets', 'hub', 'ring', 'suspension') and p.solid is not None:
            bb = p.solid.bounding_box()
            print(top or 'today', p.name, 'z', round(bb.min.Z, 2), 'to', round(bb.max.Z, 2), 'Ø', round(bb.max.X - bb.min.X, 2),
                  'volume', round(p.solid.volume / 1000, 1), 'cm3')
            if top:
                os.makedirs(d, exist_ok=True)
                export_stl(p.solid, os.path.join(d, p.name + '.stl'), tolerance=0.02, angular_tolerance=0.1)
