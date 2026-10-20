"""EARFcoin, a boxed set of eight (coin.py says what it is and how it is made): the house's pick, the globe
reverse-engraved and the edge reeded, one coin in each speaker's tint.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/earf_coin.py --out spinoffs/barkhorn/companions/out-earf-coin
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coin as C                                                    # noqa: E402
from kit import Part, Product, Sheet, Bought                        # noqa: E402  (coin.py puts the kit on the path)

FACE, EDGE = 'engraved', 'reeded'


def parts(P):
    art = C.art_solids()
    return [
        Part('coin', C.disc_blank(), Sheet('cast-acrylic', 6, face='+z'), finish='coin', qty=8,
             pieces={'body': (C.body(EDGE), 'coin'), 'globe': art['globe-engraved'], 'words': art['words']},
             notes=['one in each tint (Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke), 6 mm cast acrylic',
                    'laser-cut 40 across from the sheet; the globe engraved 0.2 deep into the BACK face from the '
                    'mirrored file (the coin face down in the sheet\'s skeleton), the words 0.12 into the FRONT; '
                    'both paint-filled through the masking: the globe black (Smoke\'s white), the words white',
                    'then both edges rounded 1.5 (a roundover cutter) and 100 reeds milled across the edge (a 0.9 ball '
                    'cutter, 0.3 deep), and the edge tumble- or vapour-polished; the faces stay the sheet\'s own']),
        Part('laser', None, Bought('coin-laser'), qty=8),
        Part('edge', None, Bought('coin-edge'), qty=8),
        Part('fill', None, Bought('coin-fill'), qty=8),
        Part('polish', None, Bought('coin-polish'), qty=8),
        Part('box', None, Bought('coin-box')),
    ]


PRODUCT = Product('earf-coin', 'EARFcoin', 'Acrylic song-request tokens, a set of eight in a box', params={},
                  parts=parts, count=1, materials=C.materials(), variants=C.variants(), drawing_prefix='ECN',
                  origin=(0, 0, 0),
                  notes=['A song request at Planet EARF: each guest picks one coin from the bowl at the door and hands '
                         'it over at the decks with a request; it drops into the request column and the queue plays '
                         'from the bottom up. GOOD FOR ONE SONG.',
                         'All numbers are proposals until the owner signs them: 40 x 6, edges 1.5, the globe 25 across, '
                         'the words in a band 15 to 17 from the centre, about 9 g.',
                         'The laser files (laser/, written by coin.py): the cut, the back\'s globe MIRRORED, the front\'s '
                         'words, and a 600 x 400 nest of 104 coins; also B\'s print file and C\'s inlay, the two faces '
                         'not chosen.'])
