"""Planet EARF's shots, round 38 (prep, while the owner reads round 37's sheet): round 37's builder and room, with
signs of life in the listening zone and the sink's thickness let read. EARFcoin (r31-coin's kit piece) and the
companions' lamp kit come in when their commits land.

    python3 spinoffs/barkhorn/planet/r38/r38_shots.py [VIEW ...]          # writes studio/shots/barkhorn/planet38/
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r37'))
import r37_shots as T37                                             # noqa: E402

S = T37.S
S.OUT = os.path.join(T37.ROOT, 'studio', 'shots', 'barkhorn', 'planet38')
T37.KEYS += ('zone_life', 'sink_under', 'sink_fill')
S.DEFAULT = T37.DEFAULT = dict(T37.DEFAULT, zone_life=True)

VIEWS = {k: v for k, v in T37.VIEWS.items() if k in ('listening-smoke', 'sink')}
# the sink (the lead: its thickness should read, light through the polished edges, the front face about lum 8-12 rather
# than crushed): the cast less dense (0.025 -> 0.08) and a hidden panel under it lighting the cast from below
VIEWS['sink'] = {**VIEWS['sink'], 'settings': {**VIEWS['sink']['settings'], 'sink_radius': 0.08, 'sink_under': 1.2, 'sink_fill': 20.0, 'sink_wash': 15.0}}
# the listening view a step back and to the side, looking down a little more, so the middle table (its Orb, a record,
# a glass) and the near chair (a coat over its back) come into the frame's lower left (round 37's p6 framed the props out)
VIEWS['listening-smoke'] = {**VIEWS['listening-smoke'],
                            'camera': {**VIEWS['listening-smoke']['camera'], 'position': [11.9, 1.6, 1.55],
                                       'target': [16.5, 3.3, 1.0]}}
S.VIEWS = VIEWS

_shot = S.shot


def shot(view):
    s = _shot(view)
    s['title'] = s['title'].replace('(round 37)', '(round 38)')
    return s


S.shot = shot

if __name__ == '__main__':
    S.write(sys.argv[1:] or None)
