"""Amp-plate test (the coordinator, 24 Nov 15:49): which light lights the cabinet's inside round the plate, and the
smallest real change that brings that surround back to about FA123's L* with the plate's L* held.
    python3 gen.py alone            -> alone-acid-<light>.json: Acid with one light on (and `sky` alone), quarter size
    python3 gen.py change TINT...   -> change-<tint>.json, half size (800 x 800): the proposed change (CHANGE below)
    python3 gen.py expo TINT EV...  -> expo-<tint>-<ev>.json, half size: light C as rendered, exposure only"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.dirname(HERE)


def load(t):
    return json.load(open(os.path.join(SRC, f'amp-{t}.json')))


def change(s):
    """The proposed real change; filled in from the light-alone test."""
    return s


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'alone':
        base = load('acid')
        for name in list(base['lights']) + ['sky']:
            s = copy.deepcopy(base)
            for n in s['lights']:
                if n != name:
                    s['lights'][n]['off'] = True
            if name != 'sky':
                s['sky']['strength'] = 0.0
            s['size'] = [400, 400]; s['render']['samples'] = 48
            json.dump(s, open(os.path.join(HERE, f'alone-acid-{name}.json'), 'w'), indent=1)
            print(name)
    elif what == 'change':
        for t in sys.argv[2:]:
            s = change(load(t)); s['size'] = [800, 800]
            json.dump(s, open(os.path.join(HERE, f'change-{t}.json'), 'w'), indent=1)
    elif what == 'expo':
        t = sys.argv[2]
        for ev in sys.argv[3:]:
            s = load(t); s['size'] = [800, 800]; s['render']['exposure'] = float(ev)
            json.dump(s, open(os.path.join(HERE, f'expo-{t}-{ev}.json'), 'w'), indent=1)
