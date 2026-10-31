"""The proposals' render model alone (the GLB and the engine's product file, studio/products/barkhorn-variants.json),
without fabkit's clash checks, cut files and drawings: the Topo horn's detailed outlines took the full build 78
minutes to export and then out of memory in its checks, sharing the machine with renders. For the design pass's
pictures; the full build (drawings, parts list) runs alone afterwards.

    .venv-fab/bin/python spinoffs/barkhorn/variants/render_model.py
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import build, render                                                 # noqa: E402

P = build.load_product(os.path.join(HERE, 'variants.py'))
parts = [p for p in P.parts(P.params) if p.solid is not None]
glb, pf = render.write(P, parts, os.path.join(HERE, 'out'), proof=False)
print(glb, pf)
