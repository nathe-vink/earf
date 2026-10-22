"""The critic's card for a Planet EARF frame, round 39: round 38's card (its context, what is fixed, what may change,
the settings as rendered) with what each of round 39's six photographs is for, and Mother EARF where it hangs.

    python3 spinoffs/barkhorn/planet/r39/r39_card.py VIEW OUT.md --shot IMG.shot.json [--scale 0.5]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r38'))
import r38_card as C38                                               # noqa: E402  (patches r37's card)

C = C38.C
COIN = ('EARFcoin: acrylic coins with the EARF globe on them, one given to each guest at the door, exchanged for a song '
        'request. ')
MOTHER = (' Hung low over the middle banquette table: Mother EARF, the brand\'s globe made at architectural scale, '
          '1.25 m across, six slotted discs of 25 mm cast acrylic in Smoke, see-through, under one hard spot that '
          'throws its shadow on the concrete wall: the room\'s centrepiece.')
FOR = {
    'door': 'the hero of the feature: the whole room from just inside the door at night, as a guest first sees it: the '
            'banquette and its frosted screens on the right, the zinc racetrack counter under its Hemisphere North pendants on the '
            'left with the record wall and the bar pair behind it, and at the far end, up a step, the listening room with '
            'EARF\'s pair on its altar. Board-formed concrete, fir beams, blackened steel. ',
    'bar': 'a hero: the bar counter, from the banquette\'s end, along the zinc-topped racetrack counter with its fluted '
           'dark-oak front to the back bar: two of EARF\'s speakers raised on oak ledges at counter height in timber-lined '
           'niches either side of the decks (as Ginza Music Bar\'s Tannoys sit in theirs), EARF\'s Mantle record players, the '
           'record wall with a frosted disc, the Hemisphere North pendants low over the zinc; a night\'s glasses, a candle and a coat '
           'on a chair. ',
    'listening': 'a hero: the listening room, a room within the room up a 200 mm step: low velvet tub chairs and small '
                 'oak tables with EARF\'s Core lamps, all facing the altar, where EARF\'s listening pair stands on solid oak '
                 'plinths in a niche lined in Douglas fir; the shell around it. ',
    'decks': 'a detail at the bar: a drink just poured beside the decks (a coupe, the mixing glass it came from, the bottle '
             'open), the request column (a clear tube on a Smoke base where the coins played wait their turn, lit from '
             'its base), one of EARF\'s Mantle record players beyond. ' + COIN,
    'bowl': 'a detail at the door: the bowl of coins in EARF\'s eight tints on the host stand inside the door, a coin for '
            'each guest, the door and the shopfront beyond. ' + COIN,
    'street': 'a detail: the shopfront at blue hour from across the street: the blackened-steel shopfront, the name etched '
              'in the glass, a frosted lightbox with the fogged silhouette of a woman dancing, the room lit behind the '
              'glass, the flats above. ',
}


def main():
    view = sys.argv[1]; out = sys.argv[2]
    sh = json.load(open(sys.argv[sys.argv.index('--shot') + 1]))
    scale = float(sys.argv[sys.argv.index('--scale') + 1]) if '--scale' in sys.argv else 0.5
    key = view.replace('-mother', '')
    C.SHOT_VIEW[0] = ''
    s = C.settings(sh, scale)
    life = next((p for p in sh['set']['props'] if p.get('fn') == 'life'), {})
    if life:
        s += '\n- round 39 props: ' + ', '.join(f"{len(v)} {k}" for k, v in life.items() if isinstance(v, list))
    m = next((p for p in sh['set']['props'] if p.get('fn') == 'mother'), None)
    if m:
        if m.get('tint'):
            sp = sh['lights'].get('mother-spot', {})
            s += (f"\n- Mother EARF: centre {m['centre']}, {m['size']} m across, every disc cast in Smoke ({m['tint']}, "
                  f"radius {m.get('radius')}), unlit; one hard spot {sp.get('power_w')} W, cone {sp.get('cone_deg')} deg, from "
                  f"{sp.get('position')}, throwing its shadow on the concrete wall")
        else:
            s += (f"\n- Mother EARF: centre {m['centre']}, {m['size']} m across, rim glow {m['rim']} (parallels x{m['rim_par']}), "
                  f"core glow {m['core_glow']}, core lamp {m['core_w']} W")
    txt = (f"# Card: Planet EARF, {sh['title']}\n\n**What the frame is for:** {FOR[key]}Configuration: Smoke (the house "
           f"configuration).{MOTHER if m else ''}\n\n{C.CONTEXT}\n\n{C.FIXED}\n\n{C.MAY}\n\n**Settings now:**\n\n{s}\n")
    open(out, 'w').write(txt)
    print(out)


if __name__ == '__main__':
    main()
