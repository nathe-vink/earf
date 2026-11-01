"""Hemisphere, PROPOSAL v3 (2026-11-01, launch/stock-tints-lamps.md; recommended over v2, which is the main build
dome_pendant.py): the tint outside. A 3 mm stock-tint shell, a 6 mm clear structural shell, then the 3 mm opal, seen
directly from below. Everything else is the main build's. For the owner to choose against v2.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/dome_pendant_v3.py --out spinoffs/barkhorn/companions/out-dome-pendant-v3
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crystal as C                                                 # noqa: E402

V3 = dict(C.D, shell=3.0, liner=6.0, skin=3.0, build='v3')         # outside in: tint 3, gap 1, clear 6, gap 1, opal 3

PRODUCT = C.Product('earf-dome-pendant-v3', 'Hemisphere v3 (proposal)', 'Pendant in cast acrylic, the tint outside',
                    params=dict(V3), parts=lambda P: C.north_parts(V3), count=1, materials=C.MATERIALS,
                    variants=C.VARIANTS, notes=C.NOTES_DOME, touching=C.TOUCHING_DOME, drawing_prefix='EDP3')
