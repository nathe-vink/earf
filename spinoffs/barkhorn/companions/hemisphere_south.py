"""Hemisphere South, DROPPED (the owner, 2026-10-25: "Get rid of south altogether and just call it hemisphere."). Kept as a record: nothing
in the line builds on it.

Hemisphere South, the bowl: the same shades as Hemisphere North turned opening-up, on a slim rod from the ceiling,
the light at the bottom of the bowl shining up (crystal.py says what it is and how it is made; README, round 35).

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/hemisphere_south.py --out spinoffs/barkhorn/companions/out-hemisphere-south
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crystal as C                                                 # noqa: E402

PRODUCT = C.Product('earf-hemisphere-south', 'Hemisphere South (dropped 2026-10-25)', 'Uplighter bowl on a rod in cast acrylic, its own '
                    'shade, nothing below it', params=dict(C.S), parts=lambda P: C.south_parts(),
                    count=1, materials=C.MATERIALS, variants=C.VARIANTS, notes=C.NOTES_SOUTH,
                    touching=C.TOUCHING_SOUTH, drawing_prefix='EHS',
                    # the origin at the bowl's rim, on its axis, as the model is drawn (the kit reads all-zero as unset)
                    origin=(0.0, 0.0, 1e-6))
