"""Hemisphere (the Dome until round 35, Hemisphere North in rounds 35 to 37), the pendant whose shades swap by hand
(crystal.py says what it is and how it is made). Round 41: round 32f's low top, no fins. Since 2026-11-01 (the owner:
"Hemisphere: color outside"), the shade is v3: a 3 mm stock-tint shell, a 6 mm clear structural shell, then the opal
(launch/stock-tints-lamps.md); v2 is dome_pendant_v2.py. The file keeps its old name so nothing downstream breaks.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/dome_pendant.py --out spinoffs/barkhorn/companions/out-dome-pendant
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crystal as C                                                 # noqa: E402

PRODUCT = C.Product('earf-dome-pendant', 'Hemisphere', 'Pendant in cast acrylic, its shades swapping by hand',
                    params=dict(C.V3), parts=lambda P: C.dome_parts(), count=1, materials=C.MATERIALS,
                    variants=C.VARIANTS, notes=C.NOTES_DOME, touching=C.TOUCHING_DOME, drawing_prefix='EDP')
