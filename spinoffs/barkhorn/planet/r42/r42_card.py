"""The critic's card for round 42's new views of the bar (counter, listening, night, shop): round 41's card with what
each new photograph is for.

    python3 spinoffs/barkhorn/planet/r42/r42_card.py VIEW OUT.md --shot IMG.shot.json [--scale 0.5]
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r41'))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r40'))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r39'))
import r41_card                                                       # noqa: E402,F401  (sets the multicolour Mother)
import r40_card as C40                                                # noqa: E402

C40.C39.FOR.update({
    'counter': 'a hero: the counter, from its far end, along the zinc-topped racetrack counter with its fluted dark-oak '
               'front, the Hemisphere pendants low over the zinc, the back bar, the decks and the record wall, toward the '
               'shopfront and the street at night. ',
    'listening': 'a hero: the listening room, a room within the room up a 200 mm step, seen from behind the low velvet '
                 'tub chairs: EARF\'s Tropos pair on oak plinths in a niche lined in Douglas fir, the altar, the Core '
                 'lamps on the small tables. ',
    'night': 'the hero of the house at night: the whole room from the back of the listening room toward the street, the '
             'line playing: the tub chairs, the step, the banquette and its Core lamps, Mother EARF in colour, the counter '
             'under its pendants and the record wall, the shopfront glass and the street beyond. ',
    'shop': 'a hero for the shop wall: everything in the room is for sale, and this is where it waits, by the door: oiled '
            'oak shelves on blackened steel with the eight Core table lamps in EARF\'s tints, a Mantle record player, '
            'records, a price card at every piece; three Hemisphere pendants hung low in front; a Tropos speaker in Ember '
            'on an oak plinth beside it; the window table, the counter\'s end and the record wall. ',
})

if __name__ == '__main__':
    C40.main()
