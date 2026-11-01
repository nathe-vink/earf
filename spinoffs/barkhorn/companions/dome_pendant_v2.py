"""Hemisphere v2, the alternative (2026-11-01): the 9 mm outer shell clear (TruCast 0000), only the 3 mm inner skin in
stock tint. It glows lit but reads as a white opal dome unlit; the owner signed v3 (dome_pendant.py) instead.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/dome_pendant_v2.py --out spinoffs/barkhorn/companions/out-dome-pendant-v2
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crystal as C                                                 # noqa: E402

PRODUCT = C.Product('earf-dome-pendant-v2', 'Hemisphere v2 (alternative)', 'Pendant in cast acrylic, the tint inside',
                    params=dict(C.D), parts=lambda P: C.north_parts(C.D), count=1, materials=C.MATERIALS,
                    variants=C.VARIANTS, notes=C.NOTES_DOME, touching=C.TOUCHING_DOME, drawing_prefix='EDP2')
