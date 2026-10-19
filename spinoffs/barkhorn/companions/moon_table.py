"""Moon, the table (moon.py says what it is and how it is made).

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/moon_table.py --out spinoffs/barkhorn/companions/out-moon-table
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moon as M                                                    # noqa: E402

PRODUCT = M.Product('earf-moon-table', 'Moon table', 'Cordless rechargeable table lamp in cast acrylic, for bars',
                    params=dict(M.T), parts=lambda P: M.table_parts(), count=1, materials=M.MATERIALS,
                    variants=M.VARIANTS, notes=M.NOTES_TABLE, touching=M.TOUCHING_TABLE, drawing_prefix='EMT')
