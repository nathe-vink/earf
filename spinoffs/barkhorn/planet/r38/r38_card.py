"""The critic's card for a Planet EARF frame, round 38 (round 37's card on round 38's shots): the bar pair raised on
ledges at counter height, EARFcoin (the request column at the decks, the bowl at the door), the lamps' black hardware,
the listening zone's signs of life, the sink as smoked glass. All in Smoke (the owner: "Planet: Smoke, ledge at counter
height").

    python3 spinoffs/barkhorn/planet/r38/r38_card.py VIEW OUT.md [--shot IMG.shot.json] [--scale 0.5]
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r37'))
import r38_shots as S38                                              # noqa: E402  (patches r37's builder)
import r37_card as C                                                 # noqa: E402

C.S.VIEWS.update(S38.VIEWS)
COIN = ('EARFcoin: acrylic coins with the EARF globe on them, one given to each guest at the door, exchanged for a song '
        'request; ')
C.FOR.update({
    'bar': 'the back bar, the room\'s showroom wall, seen across the counter from a counter stool: two of EARF\'s speakers '
           'raised on solid oak ledges at counter height in timber-lined, felt-lined niches either side of the DJ station '
           '(as Ginza Music Bar\'s Tannoys sit in theirs), tilted down and toed in toward the counter, each over a glowing '
           'light plinth, the blackened-steel doors beneath; between them the decks with a pair of EARF\'s own record '
           'players (R3 Float), a rotary mixer, and the request column (EARFcoin, below); a frosted disc in a '
           'floor-to-ceiling record wall; the zinc-topped racetrack counter with a fluted dark-oak front; EARF\'s Dome '
           'pendants low over the zinc, with black anodised hardware. ' + COIN + 'Configuration: {config}.',
    'coins': 'a detail at the bar: ' + COIN + 'at the decks, the request column, a clear tube on a Smoke base where the '
             'coins played wait their turn, the next song at the bottom, lit from an LED in its base, a warm pin spot over '
             'the decks; one of EARF\'s record players beside it. Or, at the door: the bowl of coins in all eight of EARF\'s '
             'tints, waiting on a host stand inside the door, a coin for each guest. Configuration: {config}.',
    'listening': C.FOR['listening'].replace('Configuration:', 'Signs of life: a glass and a record on the middle table, a '
                                            'record sleeve against a plinth, a coat over a chair. Configuration:'),
})
_settings = C.settings


def settings(sh, scale):
    return _settings(sh, scale).replace(
        '- props: rocks glasses and a half-drunk coupe, a record out of its sleeve, a coat over a counter chair, record '
        'sleeves on the panels\' ledges, bottles in the lit niche, candles on the counter',
        '- props: rocks glasses and a half-drunk coupe, a record out of its sleeve, a coat over a counter chair, candles '
        'on the counter; in the zone a record and sleeve, a sleeve against a plinth, a coat over a tub chair; EARFcoins '
        '(the request column at the decks with 24 coins, three fanned on the counter, a brass bowl of 40 at the door)')


C.settings = settings

if __name__ == '__main__':
    C.main()
