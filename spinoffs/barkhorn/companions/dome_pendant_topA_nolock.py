"""PROPOSAL 2026-11-24 (crystal.py TOP_TIERS['A'], the even-tier top for the owner's question): Hemisphere (the Dome until round 35, Hemisphere North in rounds 35 to 37), the pendant whose shades swap by hand
(crystal.py says what it is and how it is made). Round 41: round 32f's low top, no fins. Since 2026-11-01 (the owner:
"Hemisphere: color outside"), the shade is v3: a 3 mm stock-tint shell, a 6 mm clear structural shell, then the opal
(launch/stock-tints-lamps.md); v2 is dome_pendant_v2.py. The file keeps its old name so nothing downstream breaks.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/dome_pendant_topA_nolock.py --out spinoffs/barkhorn/companions/out-dome-pendant-topA-nolock
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['HEMI_LOCK_ON'] = '0'                                    # v9: top A without the lock (the owner's other choice)
import crystal as C                                                 # noqa: E402

PRODUCT = C.Product('earf-dome-pendant-topA-nolock', 'Hemisphere, top A without the lock (PROPOSAL)', 'Pendant in cast acrylic, its shades swapping by hand',
                    params=dict(C.V3, top='A'), parts=lambda P: C.dome_parts(dict(C.V3, top='A')), count=1, materials=C.MATERIALS,
                    variants=C.VARIANTS, notes=C.notes_dome('A'), touching=C.TOUCHING_DOME, drawing_prefix='EDP')
