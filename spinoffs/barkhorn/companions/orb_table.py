"""Core (the Orb until round 35), the table lamp, a crystal ball that works plugged in or not, on its own replaceable
cells (crystal.py says what it is and how it is made). The file keeps its old name so nothing downstream breaks.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/orb_table.py --out spinoffs/barkhorn/companions/out-orb-table
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crystal as C                                                 # noqa: E402

PRODUCT = C.Product('earf-orb-table', 'Core', 'Table lamp in cast acrylic, a crystal ball, plugged in or on its own cells',
                    params=dict(C.O), parts=lambda P: C.orb_parts(), count=1, materials=C.MATERIALS,
                    variants=C.VARIANTS, notes=C.NOTES_ORB, touching=C.TOUCHING_ORB, drawing_prefix='EOT',
                    # the origin on the ball's axis, on the table: the cable (420 back) would move the footprint's centre
                    # (the kit's default origin) 170 behind it; the kit reads an all-zero origin as unset, hence the 1e-6
                    origin=(0.0, 0.0, 1e-6))
