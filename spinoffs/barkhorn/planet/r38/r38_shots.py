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
# the coins, close: the request column at the decks from a stool at the counter; the bowl on the host stand at the door
_C = T37.RP.COUNTER; _cx = round(T37.RP.DJ['x'] + 0.80, 3); _cy = round(_C['y1'] - 0.30, 3); _zt = _C['top_z']
VIEWS['coins-decks'] = {'title': 'EARFcoin: the request column at the decks (Smoke)',
                        'camera': {'position': [_cx - 0.55, round(_C['y0'] - 0.45, 3), round(_zt + 0.30, 3)],
                                   'target': [_cx - 0.10, _cy, round(_zt + 0.06, 3)], 'lens_mm': 50, 'level': True,
                                   'fstop': 4.0, 'focus': [_cx, _cy, round(_zt + 0.05, 3)]},
                        'settings': {**T37.VIEWS['bar-smoke']['settings'], 'config': 'smoke', 'exposure': -0.3}}
_H = T37.RP.HOST
VIEWS['coins-door'] = {'title': 'EARFcoin: the bowl at the door (Smoke)',
                       'camera': {'position': [_H['x'] + 0.75, _H['y'] + 0.45, 1.70],
                                  'target': [_H['x'], _H['y'], _H['top'] + 0.03], 'lens_mm': 50, 'level': True,
                                  'fstop': 4.0, 'focus': [_H['x'], _H['y'], _H['top'] + 0.03]},
                       'settings': {**T37.VIEWS['bar-smoke']['settings'], 'config': 'smoke', 'exposure': 2.1, 'host_w': 30.0}}
S.VIEWS = VIEWS
T37.VIEWS.update(VIEWS)                                            # r37's shot() reads its own VIEWS

# --- EARFcoin (r31-coin 3cf191f, studio/engine/kit_ext/earf_coin.py; the owner: "Acrylic coins with the EARF globe on
# them that can be exchanged for a song request. Each guest gets one."): the request column at the decks where the
# no-requests card stood, a few coins fanned on the counter by a glass, the bowl of all eight tints at the door
_props = S.props


def props(v):
    out = _props(v)
    if not v.get('coins'):
        return out
    RP = T37.RP; C = RP.COUNTER; zt = C['top_z']
    # the request column, lit from inside (the lead, 2026-10-20; r31-coin 2fc994c then 410356d: the LED disc in its Smoke base and a
    # bead-blasted back half of the tube glowing behind the queue)
    out.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'column',
                'spots': [[round(RP.DJ['x'] + 0.80, 4), round(C['y1'] - 0.30, 4), zt]], 'rotate_z': 0.0,
                # a busy night (the lead, 2026-10-20: change what's in it, not the light): 24 coins, all eight tints, the
                # light ones spread through, two Smoke at most, never two alike together, a clear Fog every five or six
                # carrying the base's light out to its rim
                'coins': ['acid', 'ember', 'poison', 'ice', 'dust', 'fog', 'haze', 'acid', 'ember', 'dust', 'poison', 'fog',
                          'smoke', 'acid', 'ice', 'dust', 'haze', 'fog', 'poison', 'ember', 'acid', 'ice', 'smoke', 'dust'], 'out': 6.0, 'base_glow': 1.0, 'back_glow': 1.0})   # r31-coin 410356d, tuned from this stool
    out.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'fan',
                'spots': [[4.35, round(C['y0'] + 0.16, 4), zt]], 'flavours': ['dust', 'fog', 'poison'], 'heading': 15.0})
    H = RP.HOST
    out.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'bowl', 'spots': [[H['x'], H['y'], H['top']]],
                'n': 40, 'bowl': v.get('coin_bowl', 'brass'), 'd': 220})
    return out


S.props = props
T37.props = props

_lights = S.lights


def lights(v):
    L = _lights(v)
    if v.get('coins'):
        H = T37.RP.HOST                                 # a pinhole downlight over the host stand, onto the bowl
        L['host'] = {'type': 'spot', 'position': [H['x'], H['y'], T37.RP.CEIL - 0.05], 'target': [H['x'], H['y'], H['top']],
                     'power_w': v.get('host_w', 40.0), 'cone_deg': v.get('host_cone', 6.0), 'blend': 0.6, 'radius_m': 0.02, 'color': 2700,
                     'camera': False}
        C = T37.RP.COUNTER                              # a warm pin spot over the decks, from above and in front (below
        # the Domes' line: from the ceiling over the aisle it lit nothing at the column, by eye and measure; a Cycles spot's
        # watts are for the whole sphere, so a narrow cone needs hundreds to read), grazing
        # the request column's front so the coins' polished edges catch it (the lead: as any listening bar lights its decks)
        cx, cy = round(T37.RP.DJ['x'] + 0.80, 3), round(C['y1'] - 0.30, 3)
        L['decks-pin'] = {'type': 'spot', 'position': [round(cx + 0.15, 3), round(cy - 0.75, 3), 2.55],
                          'target': [cx, cy, round(C['top_z'] + 0.08, 3)], 'power_w': v.get('decks_pin', 300.0),
                          'cone_deg': 9.0, 'blend': 0.5, 'radius_m': 0.015, 'color': 2700, 'camera': False}
    return L


S.lights = lights
T37.lights = lights

_shot = S.shot


def shot(view):
    s = _shot(view)
    s['title'] = s['title'].replace('(round 37)', '(round 38)')
    return s


S.shot = shot

if __name__ == '__main__':
    S.write(sys.argv[1:] or None)
