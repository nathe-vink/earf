"""The critic's card for round 41's door frame: round 40's card, with Mother EARF described in the site's multicolour.

    python3 spinoffs/barkhorn/planet/r41/r41_card.py VIEW OUT.md --shot IMG.shot.json [--scale 0.5]
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r40'))
import r40_card as C40                                               # noqa: E402

C40.C39.MOTHER = (" Hung low over a banquette table: Mother EARF, the brand's globe made at architectural scale, 1.25 m "
                  "across, six slotted discs of 25 mm cast acrylic, each in one of EARF's tints (red, orange, yellow, "
                  "green, blue and violet), each polished rim glowing its own colour as the brand's globe does on its "
                  "site, under one hard spot that throws its coloured shadow on the concrete wall: the room's "
                  "centrepiece. The owner chose these colours.")

if __name__ == '__main__':
    C40.main()
