"""Hemisphere, low top (round 40, a PROPOSAL beside dome_pendant.py): round 32f's profile over the shade, no fins
(crystal.north_low_parts says why it does at 575 lm).

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/dome_pendant_low.py --out spinoffs/barkhorn/companions/out-dome-pendant-low
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crystal as C                                                 # noqa: E402

PRODUCT = C.Product('earf-dome-pendant-low', 'Hemisphere, low top (proposal)',
                    'Pendant in cast acrylic, its shades swapping by hand: round 32f\'s low top, no fins',
                    params=dict(C.N_LOW), parts=lambda P: C.north_low_parts(), count=1, materials=C.MATERIALS,
                    variants=C.VARIANTS, notes=C.NOTES_DOME_LOW, touching=C.TOUCHING_DOME_LOW, drawing_prefix='EDL')
