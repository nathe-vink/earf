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
    colourway='green', pendant_w=320.0, pendant_cone=46.0, dome_w=9.0, dome_glow=1.1, sphere_w=3.0, sphere_glow=1.1,
    disc_col='#FF5A3A', disc_glow=0.8, disc_lamp=60.0, name_glow=0.25, niche_strip=4.0, sink_glow=6.0,
    screen_glow=1.0, screen_tint='#FFA060', screen_gap=0.04, screen_rough=0.22, etch_glow=0.01, etch_frost=0.3,
    rw_w=14.0, rw_cone=22.0, altar_w=70.0, altar_cone=28.0, spk_irr=5.0, spk_back=40.0, spk_spread=90.0,
    spk_link=True, spk_k=2900, candle_w=3.0, flame=60.0, haze=0.005, wb=3000, exposure=0.0, view='AgX',
    look='AgX - Medium High Contrast',
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


def lamps(v):
    """The owner's lamps (companions, r31-companions 2ea12b9): the Dome pendant low over the counter, the Orb on every
    table; smoked, so the Ember pair stays the hero; an Ember Orb only where a frame asks for one (`orb_ember`)."""
    y = round((RP.COUNTER['y0'] + RP.COUNTER['y1']) / 2, 4)
    orbs = [{'position': list(s), 'flavour': 'ember' if i in v.get('orb_ember', ()) else v.get('lamp_flavour', 'smoked')}
            for i, s in enumerate(RP.sphere_spots())]
    return [{'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'flavour': v.get('lamp_flavour', 'smoked'),
             'spots': [[x, y, RP.DOME['rim_z']] for x in RP.DOMES], 'ceiling': RP.CEIL, 'lamp_w': v['dome_w'],
             'lamp_k': 2700, 'shade_glow': v['dome_glow']},
            {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb', 'spots': orbs, 'lamp_w': v['sphere_w'],
             'lamp_k': 2700, 'shade_glow': v['sphere_glow']}]


def props(v):
    """The room, the lamps and the street lamps; the den's scanned stools and chairs are gone (the kit builds the seats)."""
    return [o for o in _props(v) if o.get('module') == 'planet_r36' or o.get('model') == 'street_lamp_01'] + lamps(v)


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
            # after the two critics on p1 (4.5, 4.5): one orange wood everywhere, the ceiling over the floor under a haze
            # veil, the record wall the brightest, the lamps dull (placeholders then), the altar small: nearer on 35 mm;
            # less haze; a higher-contrast look; the oak darker; the record wall's spots down; the screens up
            'camera': {'position': [4.5, 2.7, 1.35], 'target': [17.0, 3.1, 1.15], 'lens_mm': 35, 'level': True,
                       'fstop': 5.6, 'focus': [12.0, 3.1, 1.1]},
            'settings': {'exposure': -0.3}},
    'listening-green': {'title': 'the listening zone, bottle green',
                        'camera': {'position': [11.25, 2.45, 1.35], 'target': [16.6, 3.25, 1.2], 'lens_mm': 28,
                                   'level': True, 'fstop': 4.0, 'focus': [16.5, 3.05, 1.1]},
                        'settings': {'colourway': 'green', 'exposure': 0.35, 'wb': 2700}},
    'listening-oxblood': {'title': 'the listening zone, oxblood',
                          'camera': {'position': [11.25, 2.45, 1.35], 'target': [16.6, 3.25, 1.2], 'lens_mm': 28,
                                     'level': True, 'fstop': 4.0, 'focus': [16.5, 3.05, 1.1]},
                          'settings': {'colourway': 'oxblood', 'exposure': 0.35, 'wb': 2700}},
    'street': {'title': 'the shopfront at night, from the kerb',
               # after the two critics on p1 (5.0, 5.0): over-exposed under a veil, the mullion through the altar, the
               # etched name a beige square, the lightbox too bright, no reflections: 32 mm with the mullion on a third,
               # exposure down, the etch unlit, the lightbox down, a lamp behind the camera for the glass
               'camera': {'position': [-3.2, 2.2, 1.5], 'target': [17.0, 3.4, 1.35], 'lens_mm': 32, 'level': True,
                          'fstop': 5.6, 'focus': [0.0, 3.0, 1.6]},
               'settings': {'exposure': 1.2, 'etch_glow': 0.0, 'wb': 3200, 'wet': True, 'road_rough': 0.12, 'street_lamp': 200.0,
                            'screen_window': 0.27, 'lamp_k': 3000, 'lamp_z': 5.0, 'lamp_dx': 0.0, 'lamp_cam': 300.0,
                            'lamp_cam_z': 4.0, 'lamp_cam_y': 2.0, 'sign_w': 0.0, 'entry_w': 45.0, 'entry_cone': 100.0,
                            'transom_glow': 0.15, 'siding': '#8E9384', 'sky': 0.03, 'sky_zenith': '#1A2440',
                            'sky_horizon': '#2A3550', 'flat_glow': 0.06, 'across_glow': 0.05, 'linen_trans': 0.5,
                            'glass_gloss': 3.0, 'haze': 0.003}},
    'sink': {'title': 'the sink, a detail',
             # after the two critics on p1 (3.0, 4.0): the trough a black box with a red lid, the wall lit instead,
             # a dead black strip at the left: a glowing core cast inside it; the boards darker and varied; turned right
             'camera': {'position': [9.85, 2.05, 1.42], 'target': [11.02, 0.15, 0.86], 'lens_mm': 65, 'level': True,
                        'fstop': 2.8, 'focus': [11.02, 0.27, 0.84]},
             'settings': {'exposure': 0.2, 'haze': 0.0, 'sink_glow': 6.0, 'sink_spot': 28.0, 'wb': 2800}},
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
