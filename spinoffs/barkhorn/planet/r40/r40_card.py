"""The critic's card for a Planet EARF frame, round 40: round 39's card, with the people (blurred by a long exposure,
on purpose: the owner allowed blurred figures, never sharp faces) and the fir's boards listed.

    python3 spinoffs/barkhorn/planet/r40/r40_card.py VIEW OUT.md --shot IMG.shot.json [--scale 0.5]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r39'))
import r39_card as C39                                               # noqa: E402

C39.MOTHER = C39.MOTHER.replace('over the middle banquette table', 'over a banquette table')
PEOPLE = (' People are in the room as a long exposure records them: a quarter-second or so, so whoever moves is a '
          'blur, and no face is ever sharp. That is intended (the owner allowed blurred figures, never sharp faces); '
          'how many and where follow the hour.')


def main():
    view, out = sys.argv[1], sys.argv[2]
    sh = json.load(open(sys.argv[sys.argv.index('--shot') + 1]))
    C39.main()                                  # writes round 39's card to OUT
    txt = open(out).read()
    fig = next((p for p in sh['set']['props'] if p.get('fn') == 'figures'), {})
    ppl = fig.get('people', [])
    poses = {}
    for q in ppl:
        poses[q['pose']] = poses.get(q['pose'], 0) + 1
    names = {'stool': 'at the counter', 'chair': 'at a table', 'bench': 'on the banquette', 'tub': 'in a tub chair',
             'pour': 'the bartender, pouring', 'decks': 'the selector at the decks'}
    txt = txt.replace('Configuration: Smoke (the house configuration).',
                      'Configuration: Smoke (the house configuration).' + (PEOPLE if ppl else ''))
    txt = txt.replace('(round 39)', '(round 40)').replace('round 39 props', 'props')
    extra = ''
    if ppl:
        extra += ('\n- people (fixed in kind; their number, places and blur may change): '
                  + ', '.join(f"{n} {names[k]}" for k, n in poses.items())
                  + f"; shutter {fig.get('shutter', 1.0)} frame; the head's travel {ppl[0]['head'][:3]} m and turn "
                    f"{ppl[0]['head'][3]} deg for a seated guest")
    if any(p.get('fn') == 'boards' for p in sh['set']['props']):
        extra += '\n- the fir: every board its own stretch of the scan, tone +/-10 %, warmth +/-1.5 %'
    open(out, 'w').write(txt.rstrip('\n') + extra + '\n')
    print(out)


if __name__ == '__main__':
    main()
