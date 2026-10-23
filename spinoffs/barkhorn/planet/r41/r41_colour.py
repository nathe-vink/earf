"""Planet EARF, round 41 (the owner, 2026-10-22: "Bar people: empty rooms, as round 39" and "Bar globe: the site's
multicolour"): round 39's empty door-mother final exactly as rendered (its shot file), with Mother EARF's globe in the
site's multicolour, round 33c's globe as on the site's mother-globe.jpg: the six discs in their speakers' tints (Poison
the meridian facing, Dust and Haze the side meridians, Ember 40 N, Ice the equator, Acid 40 S), each rim glowing its
colour, no core. The same 1.25 m, place, heading, sheet and light; round 39's hard spot and rim spot stay as they were.

    python3 spinoffs/barkhorn/planet/r41/r41_colour.py [--edge]   # writes studio/shots/barkhorn/planet41/door-mother-colour.json

`--edge` adds round 40's edge light (r40/r40_edge.EDGE), only if the colours do not read without it.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
SRC = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'planet39', 'finals', 'door-mother.shot.json')
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet41', 'door-mother-colour.json')
# the site's globe: every rim lit alike (meridians and parallels), no opal core (round 39's p1 variant had one)
COLOUR = dict(core=0.0, rim=0.14, rim_par=1.0, radius=0.07)   # rim 0.22 (round 39's p1) neared clipping at a look


def main():
    s = json.load(open(SRC))
    m = next(p for p in s['set']['props'] if p.get('fn') == 'mother')
    m.pop('tint', None)
    m.update(COLOUR)
    if '--edge' in sys.argv:
        sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r40'))
        from r40_edge import EDGE
        s['lights']['mother-edge'] = dict(EDGE)
    s['title'] = s['title'].replace('(Mother EARF)', "(Mother EARF in the site's multicolour)").replace('(round 39)', '(round 41)')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(s, open(OUT, 'w'), indent=1)
    print(OUT)


if __name__ == '__main__':
    main()
