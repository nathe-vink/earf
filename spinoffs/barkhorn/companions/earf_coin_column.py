"""EARFcoin's request column, at the decks (coin.py says what it is): a water-clear tube the coins drop into, standing
in a Smoke acrylic base; the lowest coin is pushed out through a slot at the front, so the queue plays from the bottom up.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/earf_coin_column.py --out spinoffs/barkhorn/companions/out-earf-coin-column
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coin as C                                                    # noqa: E402
from kit import Product                                             # noqa: E402

PRODUCT = Product('earf-coin-column', 'EARFcoin request column', 'A coin column for song requests, at the decks',
                  params=dict(C.COL), parts=lambda P: C.column_parts(P)[0], count=1, materials=C.materials(),
                  variants=C.variants(), drawing_prefix='ECC', touching=[('tube', 'base'), ('ring', 'tube')],
                  notes=['Coins handed over with a request drop in at the top and stack; the queue shows as a column '
                         'of colours. To play the next: a finger through the notch at the back pushes the lowest coin '
                         'out of the slot at the front, and the stack drops one.',
                         'The slot is 6.8 tall, so one 6 mm coin passes and the next is held by the tube\'s wall; '
                         'the tube holds 33.',
                         'The tube is bonded into the base\'s socket and the ring onto the tube (Acrifix 1R 0192 or '
                         'Weld-On 16 for the acrylic, a clear epoxy for the brass).'])
