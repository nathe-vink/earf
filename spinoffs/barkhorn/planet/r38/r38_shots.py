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
T37.KEYS += ('zone_life', 'sink_under', 'sink_fill', 'sink_rake', 'host_stand')
S.DEFAULT = T37.DEFAULT = dict(T37.DEFAULT, zone_life=True, host_stand=True, coins=True)

VIEWS = {k: v for k, v in T37.VIEWS.items() if k in ('listening-smoke', 'sink', 'bar-smoke', 'street')}
# the sink (the lead: its thickness should read, light through the polished edges, the front face about lum 8-12 rather
# than crushed): the cast less dense (0.025 -> 0.08) and a hidden panel under it lighting the cast from below
VIEWS['sink'] = {**VIEWS['sink'], 'settings': {**VIEWS['sink']['settings'], 'sink_radius': 0.08, 'sink_under': 1.2, 'sink_fill': 20.0, 'sink_wash': 15.0}}
# p2 (the lead, 2026-10-20: p1 still read as lacquer or stone; do both): a narrow line raked along the polished arrises;
# the sink's Smoke lightened to the transparent grey r31-coin settled on for its Smoke coin (L about 18, like Perspex
# 9T20), for the sink only, a proposal to the owner
VIEWS['sink']['settings'].update(sink_deep='#A9A7AA', sink_radius=0.10, sink_rake=4.0, sink_under=0.25, sink_spot=15.0)
# the listening view a step back and to the side, looking down a little more, so the middle table (its Orb, a record,
# a glass) and the near chair (a coat over its back) come into the frame's lower left (round 37's p6 framed the props out)
VIEWS['listening-smoke'] = {**VIEWS['listening-smoke'],
                            'camera': {**VIEWS['listening-smoke']['camera'], 'position': [11.9, 1.6, 1.55],
                                       'target': [16.5, 3.3, 1.0]}}
S.VIEWS = VIEWS

# --- EARFcoin (r31-coin 3cf191f, studio/engine/kit_ext/earf_coin.py; the owner: "Acrylic coins with the EARF globe on
# them that can be exchanged for a song request. Each guest gets one."): the request column at the decks where the
# no-requests card stood, a few coins fanned on the counter by a glass, the bowl of all eight tints at the door
_props = S.props


def props(v):
    out = _props(v)
    if not v.get('coins'):
        return out
    RP = T37.RP; C = RP.COUNTER; zt = C['top_z']
    out.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'column',
                'spots': [[round(RP.DJ['x'] + 0.80, 4), round(C['y1'] - 0.30, 4), zt]], 'rotate_z': 0.0,
                'coins': ['ice', 'ember', 'acid', 'smoke', 'haze'], 'out': 6.0})
    out.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'fan',
                'spots': [[4.35, round(C['y0'] + 0.16, 4), zt]], 'flavours': ['dust', 'fog', 'poison'], 'heading': 15.0})
    H = RP.HOST
    out.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'bowl', 'spots': [[H['x'], H['y'], H['top']]],
                'n': 40, 'bowl': 'smoke', 'd': 220})
    return out


S.props = props
T37.props = props

_shot = S.shot


def shot(view):
    s = _shot(view)
    s['title'] = s['title'].replace('(round 37)', '(round 38)')
    return s


S.shot = shot

if __name__ == '__main__':
    S.write(sys.argv[1:] or None)
