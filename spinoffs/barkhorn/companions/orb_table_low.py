"""Core on the 30 base (round 40, a PROPOSAL beside orb_table.py): round 32f's 120 x 30 drum, three 18650 cells round
the LED (crystal.orb_low_parts).

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/orb_table_low.py --out spinoffs/barkhorn/companions/out-orb-table-low
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crystal as C                                                 # noqa: E402

PRODUCT = C.Product('earf-orb-table-low', 'Core, 30 base (proposal)',
                    'Table lamp in cast acrylic, a crystal ball, plugged in or on its own cells: round 32f\'s 30 base',
                    params=dict(C.O_LOW), parts=lambda P: C.orb_low_parts(), count=1, materials=C.MATERIALS,
                    variants=C.VARIANTS, notes=C.NOTES_ORB_LOW, touching=C.TOUCHING_ORB_LOW, drawing_prefix='EOL',
                    origin=(0.0, 0.0, 1e-6))
