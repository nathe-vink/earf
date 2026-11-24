"""Amp-plate test (the coordinator, 24 Nov 15:49): which light lights the cabinet's inside round the plate, and the
smallest real change that brings that surround back to about FA123's L* with the plate's L* held.
    python3 gen.py alone            -> alone-acid-<light>.json: Acid with one light on (and `sky` alone), quarter size
    python3 gen.py change TINT...   -> change-<tint>.json, half size (800 x 800): the proposed change (CHANGE below)
    python3 gen.py expo TINT EV...  -> expo-<tint>-<ev>.json, half size: light C as rendered, exposure only
    python3 gen.py v2 TINT...       -> (the coordinator, 17:38) half size, on the S4b-fixed amp rig (light_c's
                                       real_bounces_and_panels + buildable: the bounce card and the front strip real,
                                       flag 1 out of the cove): v2bt-<tint> back-top at half irradiance, exposure -0.1
                                       (the plate face near FA123's 35.5 on Acid); v2ev-<tint> exposure -0.75 only"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.dirname(HERE)


def load(t):
    return json.load(open(os.path.join(SRC, f'amp-{t}.json')))


def change(s):
    """The real change: back-top off (the light that puts the most into the surround, 40 % of it at quarter size). No real
    change tried held the plate while the surround fell: side and top cards, a snooted spot on the plate and a panel at
    the plate's mirror each moved plate and surround together (README.md here)."""
    s['lights']['back-top']['off'] = True
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
    elif what == 'v2':
        sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..', '..', 'spinoffs', 'barkhorn', 'campaign'))
        import light_c
        for t in sys.argv[2:]:
            for name, bt, ev in (('v2bt', 0.5, -0.1), ('v2ev', 1.0, -0.75)):
                s = load(t); light_c.real_bounces_and_panels(s); light_c.buildable(s)
                s['lights']['back-top']['irradiance'] *= bt; s['render']['exposure'] = ev; s['size'] = [800, 800]
                json.dump(s, open(os.path.join(HERE, f'{name}-{t}.json'), 'w'), indent=1)
    elif what == 'expo':
        t = sys.argv[2]
        for ev in sys.argv[3:]:
            s = load(t); s['size'] = [800, 800]; s['render']['exposure'] = float(ev)
            json.dump(s, open(os.path.join(HERE, f'expo-{t}-{ev}.json'), 'w'), indent=1)
