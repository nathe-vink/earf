"""Planet EARF's shots, round 36: the den's shot builder (den/den_shots.py) on the round-36 room
(studio/engine/kit_ext/planet_r36.py, its plan r36_plan.py).

    python3 spinoffs/barkhorn/planet/r36/r36_shots.py [VIEW ...]          # writes studio/shots/barkhorn/planet36/
    python3 studio/engine/render.py studio/shots/barkhorn/planet36/bar.json --out IMG [--samples N --scale S]

The views: the bar down the room's axis to the altar; the listening zone in each colourway (bottle green and oxblood);
the street, from the kerb; the sink, a close detail. The light: the Domes over the counter (a downlight in each),
the Spheres on every table, the frosted disc behind the DJ station, the record wall's spots, the altar's soffit spots
and the speakers' own lamps (light-linked), candles on the counter, the sink's glow; outside, the street lamps.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'den'))
import r36_plan as RP                                               # noqa: E402
import den_shots as S                                               # noqa: E402

S.P = RP
S.OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet36')
S.BELL_TABLES = ()

DEFAULT = dict(S.DEFAULT, **dict(
    colourway='green', pendant_w=320.0, pendant_cone=46.0, dome_w=30.0, dome_glow=0.6, sphere_w=6.0, sphere_glow=0.6,
    disc_col='#FF5A3A', disc_glow=0.8, disc_lamp=60.0, name_glow=0.25, niche_strip=4.0, sink_glow=6.0,
    screen_glow=0.5, screen_tint='#FFA060', screen_gap=0.04, screen_rough=0.22, etch_glow=0.01, etch_frost=0.3,
    rw_w=30.0, rw_cone=34.0, altar_w=40.0, altar_cone=40.0, spk_irr=14.0, spk_back=30.0, spk_spread=90.0,
    spk_link=True, spk_k=2900, candle_w=3.0, flame=60.0, haze=0.012, wb=3000, exposure=0.0, view='AgX',
    menu_color='#8A6E4E'))
S.DEFAULT = DEFAULT
KEYS = ('colourway', 'dome_w', 'dome_glow', 'sphere_w', 'sphere_glow', 'lamp_deep', 'disc_col', 'disc_glow',
        'disc_lamp', 'name_glow', 'niche_strip', 'sink_glow', 'sink_w', 'sink_deep', 'sink_radius', 'mohair',
        'banq_col', 'screen_glow', 'screen_banquette-a', 'screen_banquette-b', 'screen_lounge', 'screen_window',
        'screen_tint', 'screen_gap', 'screen_rough', 'etch_glow', 'etch_frost', 'etch_col', 'shade_glow',
        'concrete_tint', 'concrete_mix', 'concrete_tex', 'floor_acg', 'floor_tint', 'floor_mix', 'floor_coat', 'props',
        'street', 'wet', 'road_rough', 'siding', 'neighbour', 'neighbour_plain', 'flat_glow', 'across_glow',
        'linen_trans', 'transom_glow', 'glass_gloss', 'flame', 'windows_lit', 'sign')


def room_piece(v):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'planet_r36', 'fn': 'room', **{k: v[k] for k in KEYS if k in v}}


S.room_piece = room_piece
_products, _props, _lights = S.products, S.props, S.lights


def products(v):
    """The Ember pair alone (the back bar is quiet: no Fog pair; no Bell, no Cumulus)."""
    return [g for g in _products(v) if g['def'] == S.CLOUD]


def props(v):
    """The room and the street lamps; the den's scanned stools and chairs are gone (the kit builds the seats)."""
    return [o for o in _props(v) if o.get('module') == 'planet_r36' or o.get('model') == 'street_lamp_01']


def lights(v):
    L = {k: l for k, l in _lights(v).items() if not k.startswith(('bell', 'tlamp', 'rec', 'niche', 'sconce', 'fill'))}
    z = RP.ZONE['z']
    for k, l in L.items():
        if k.startswith('spk') and not k.startswith('spkb'):
            l['target'] = [l['target'][0], l['target'][1], z + 0.8]
        if k.startswith(('pend', 'entry')):
            l['camera'] = False
    for k, (role, c, x, y, zz, rot) in enumerate(RP.speakers()):     # the back light: behind the cabinet, in the niche
        if f'spkb{k}' in L:
            L[f'spkb{k}'].update({'position': [RP.L - 0.12, y, z + 0.55], 'target': [x, y, z + 0.8]})
    # the record wall: three soft spots from under the beams, raking the spines
    for i, x in enumerate((4.6, 6.0, 8.0, 9.6)):
        L[f'rw{i}'] = {'type': 'spot', 'position': [x, RP.W - 0.95, RP.CEIL - 0.32], 'target': [x, RP.W - 0.05, 2.0],
                       'power_w': v['rw_w'], 'cone_deg': v['rw_cone'], 'blend': 0.8, 'radius_m': 0.03, 'color': 2600,
                       'camera': False}
    # the altar: two spots in the niche's soffit, washing down the end grain and the cabinets
    for i, y in enumerate((RP.YC - 1.0, RP.YC + 1.0)):
        L[f'altar{i}'] = {'type': 'spot', 'position': [RP.L - 0.25, y, RP.ALTAR['z1'] - 0.04],
                          'target': [RP.L - 0.05, y, z + 0.6], 'power_w': v['altar_w'], 'cone_deg': v['altar_cone'],
                          'blend': 0.9, 'radius_m': 0.03, 'color': 2500, 'camera': False}
    # the sink: a pinhole downlight in the alcove's head
    L['sink'] = {'type': 'spot', 'position': [RP.SINK['x'], 0.30, RP.ALCOVE['z1'] - 0.02],
                 'target': [RP.SINK['x'], 0.28, RP.SINK['top']], 'power_w': v.get('sink_spot', 18.0), 'cone_deg': 30,
                 'blend': 0.7, 'radius_m': 0.02, 'color': 2700, 'camera': False}
    return L


S.products, S.props, S.lights = products, props, lights

VIEWS = {
    'bar': {'title': 'the bar, down the room to the altar',
            # down the room's axis: the racetrack counter and the record wall on the left, the banquette and its screens
            # on the right, the Domes low over the zinc, the Ember pair on its altar at the far end, framed by the
            # partition's opening
            'camera': {'position': [1.4, 2.75, 1.45], 'target': [17.0, 3.15, 1.15], 'lens_mm': 30, 'level': True,
                       'fstop': 5.6, 'focus': [8.0, 3.2, 1.1]},
            'settings': {'exposure': 0.6}},
    'listening-green': {'title': 'the listening zone, bottle green',
                        'camera': {'position': [12.15, 2.85, 1.45], 'target': [16.6, 3.05, 1.1], 'lens_mm': 35,
                                   'level': True, 'fstop': 4.0, 'focus': [16.5, 3.05, 1.1]},
                        'settings': {'colourway': 'green', 'exposure': 0.2}},
    'listening-oxblood': {'title': 'the listening zone, oxblood',
                          'camera': {'position': [12.15, 2.85, 1.45], 'target': [16.6, 3.05, 1.1], 'lens_mm': 35,
                                     'level': True, 'fstop': 4.0, 'focus': [16.5, 3.05, 1.1]},
                          'settings': {'colourway': 'oxblood', 'exposure': 0.2}},
    'street': {'title': 'the shopfront at night, from the kerb',
               'camera': {'position': [-2.6, 3.0, 1.55], 'target': [7.4, 4.3, 1.4], 'lens_mm': 35, 'level': True,
                          'fstop': 5.6, 'focus': [0.0, 3.4, 1.6]},
               'settings': {'exposure': 1.7, 'wb': 3200, 'wet': True, 'road_rough': 0.12, 'street_lamp': 200.0,
                            'screen_window': 0.45, 'lamp_k': 3000, 'lamp_z': 5.0, 'lamp_dx': 0.0, 'lamp_cam': 120.0,
                            'lamp_cam_z': 4.0, 'lamp_cam_y': 2.0, 'sign_w': 0.0, 'entry_w': 45.0, 'entry_cone': 100.0,
                            'transom_glow': 0.15, 'siding': '#8E9384', 'sky': 0.03, 'sky_zenith': '#1A2440',
                            'sky_horizon': '#2A3550', 'flat_glow': 0.06, 'across_glow': 0.05, 'linen_trans': 0.5,
                            'glass_gloss': 3.0, 'haze': 0.008}},
    'sink': {'title': 'the sink, a detail',
             'camera': {'position': [10.25, 1.55, 1.38], 'target': [11.02, 0.26, 0.82], 'lens_mm': 65, 'level': True,
                        'fstop': 2.8, 'focus': [11.02, 0.27, 0.84]},
             'settings': {'exposure': 0.4, 'haze': 0.0}},
}
S.VIEWS = VIEWS
_shot = S.shot


def shot(view):
    s = _shot(view)
    s['title'] = s['title'].replace('(round 33)', '(round 36)')
    return s


S.shot = shot


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--final']
    S.write(args or None, final='--final' in sys.argv)
