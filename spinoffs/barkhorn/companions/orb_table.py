"""Orb, the cordless table lamp, a crystal ball (crystal.py says what it is and how it is made).

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/orb_table.py --out spinoffs/barkhorn/companions/out-orb-table
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crystal as C                                                 # noqa: E402

PRODUCT = C.Product('earf-orb-table', 'Orb table lamp', 'Cordless rechargeable table lamp in cast acrylic for bars, a crystal ball',
                    params=dict(C.O), parts=lambda P: C.orb_parts(), count=1, materials=C.MATERIALS,
                    variants=C.VARIANTS, notes=C.NOTES_ORB, touching=C.TOUCHING_ORB, drawing_prefix='EOT')
