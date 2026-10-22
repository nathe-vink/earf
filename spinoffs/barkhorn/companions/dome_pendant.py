"""Hemisphere North (the Dome until round 35), the pendant whose shades swap by hand and fit Hemisphere South too
(crystal.py says what it is and how it is made). The file keeps its old name so nothing downstream breaks.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/dome_pendant.py --out spinoffs/barkhorn/companions/out-dome-pendant
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crystal as C                                                 # noqa: E402

PRODUCT = C.Product('earf-dome-pendant', 'Hemisphere North', 'Pendant in cast acrylic, its shades swapping by hand',
                    params=dict(C.D), parts=lambda P: C.dome_parts(), count=1, materials=C.MATERIALS,
                    variants=C.VARIANTS, notes=C.NOTES_DOME, touching=C.TOUCHING_DOME, drawing_prefix='EDP')
