"""Moon, the pendant (moon.py says what it is and how it is made).

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/moon_pendant.py --out spinoffs/barkhorn/companions/out-moon-pendant
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moon as M                                                    # noqa: E402

PRODUCT = M.Product('earf-moon-pendant', 'Moon pendant', 'Pendant lamp in cast acrylic, for bars',
                    params=dict(M.P), parts=lambda P: M.pendant_parts(), count=1, materials=M.MATERIALS,
                    variants=M.VARIANTS, notes=M.NOTES_PENDANT, touching=M.TOUCHING_PENDANT, drawing_prefix='EMP')
