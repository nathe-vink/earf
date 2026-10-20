"""Planet EARF's shots, round 37: the bar as a showroom. Round 36's shot builder (r36_shots.py, itself the den's) on
round 37's room (studio/engine/kit_ext/planet_r37.py, its plan r37_plan.py), with a configuration as one parameter:
a tint per product group (the bar pair, the listening pair, the Domes, the Orbs, the record players).

    python3 spinoffs/barkhorn/planet/r37/r37_shots.py [VIEW ...]          # writes studio/shots/barkhorn/planet37/
    python3 studio/engine/render.py studio/shots/barkhorn/planet37/bar-smoke.json --out IMG [--samples N --scale S]

Views: bar-<config> and listening-<config> for each configuration (smoke, ember, ice, mixed); street and sink in Smoke.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r36'))
import r37_plan as RP                                               # noqa: E402
import r36_shots as T36                                             # noqa: E402  (patches the den's builder)

S = T36.S
S.P = RP
S.OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet37')

DEFAULT = dict(T36.DEFAULT, **dict(config='smoke', colourway='neutral', disc_col='#FFD2A0', disc_glow=0.06,
                                   disc_lamp=2.0, spk_niche_strip=3.0, tt_glow=0.05, plinth=1.0, plinth_lamp=1.5, sink_glow=0.8))
S.DEFAULT = DEFAULT
KEYS = T36.KEYS + ('counter_strip', 'sconce_w', 'sconce_glow', 'card_text', 'chair_leather', 'banq_col', 'sink_deep', 'sink_glow_col', 'decks', 'spk_niche_strip', 'niche_felt')


def room_piece(v):
    cfg = RP.CONFIGS[v['config']]
    return {'kind': 'kit', 'shape': 'ext', 'module': 'planet_r37', 'fn': 'room', **{k: v[k] for k in KEYS if k in v},
            'plinth_bar': round(v['plinth'] * RP.PLINTH_GAIN[cfg['bar']], 3), 'plinth_bar_col': RP.PLINTH_COL[cfg['bar']],
            'plinth_listen': round(v['plinth'] * RP.PLINTH_GAIN[cfg['listen']], 3),
            'plinth_listen_col': RP.PLINTH_COL[cfg['listen']]}


S.room_piece = room_piece


def products(v):
    """Four speakers, one product: the listening pair on the altar, the bar pair in their niches; EARF's players at
    the decks. Each group in its configuration's tint."""
    cfg = RP.CONFIGS[v['config']]
    listen = [{'position': [round(x, 4), round(y, 4), z], 'rotate_z': rot, 'hide': ['cloth-disc']}
              for role, c, x, y, z, rot in RP.speakers()]
    bar = [{'position': [x, y, z], 'rotate_z': rot, 'tilt_x': tilt, 'hide': ['cloth-disc']}
           for role, x, y, z, rot, tilt in RP.bar_speakers()]
    C = RP.COUNTER; yd = round(C['y1'] - 0.22, 4)
    tt = [{'position': [round(RP.DJ['x'] + dx, 4), yd, C['top_z']], 'rotate_z': 180.0} for dx in (-0.42, 0.42)]
    return [{'def': S.CLOUD, 'flavour': RP.SPEAKER_FLAVOUR[cfg['listen']], 'instances': listen},
            {'def': S.CLOUD, 'flavour': RP.SPEAKER_FLAVOUR[cfg['bar']], 'instances': bar},
            {'def': RP.TT_DEF, 'flavour': cfg['tt'], 'instances': tt}]


def lamps(v):
    """The owner's Dome over the counter and Orb on every table, each in its group's tint."""
    cfg = RP.CONFIGS[v['config']]
    y = round((RP.COUNTER['y0'] + RP.COUNTER['y1']) / 2, 4)
    noshadow = T36.COVER
    return [{'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'flavour': RP.LAMP_FLAVOUR[cfg['dome']],
             'spots': [[x, y, RP.DOME['rim_z']] for x in RP.DOMES], 'ceiling': RP.CEIL, 'lamp_w': v['dome_w'],
             'lamp_k': 2700, 'shade_glow': v.get('dome_glow_' + cfg['dome'], RP.LAMP_GLOW[cfg['dome']]),
             'noshadow': noshadow},
            {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb', 'flavour': RP.LAMP_FLAVOUR[cfg['orb']],
             'spots': [list(s) for s in RP.sphere_spots()], 'lamp_w': v['sphere_w'], 'lamp_k': 2700,
             'shade_glow': v.get('orb_glow_' + cfg['orb'], RP.LAMP_GLOW[cfg['orb']] * v.get('sphere_glow', 1.1) / 1.1),
             'noshadow': noshadow}]


def props(v):
    return [o for o in T36._props(v) if o.get('module') == 'planet_r37' or o.get('model') == 'street_lamp_01'] + lamps(v)


_lights = S.lights


def lights(v):
    """Round 36's lights; the altar's two spots moved in front of the listening pair and aimed at their faces (p1, both
    critics: the pools fell on the felt above them)."""
    L = _lights(v)
    z = RP.ZONE['z']
    for i, (role, c, x, y, zz, rot) in enumerate(RP.speakers()):
        if f'altar{i}' in L:
            L[f'altar{i}'].update({'position': [round(x - 1.0, 3), y, 2.45], 'target': [x, y, round(z + v.get('altar_z', 0.9), 3)]})
    # the light plinths: under each cabinet a small lamp facing up into its base, light-linked to its own speaker, so
    # the tinted cabinet glows from below; `plinth` scales it with the plinth's glow (0 = off)
    cfg = RP.CONFIGS[v['config']]
    if v.get('plinth', 0) > 0:
        for grp, spk in (('l', [(x, y, zz) for role, c, x, y, zz, rot in RP.speakers()]),
                         ('b', [(x, y, zz) for role, x, y, zz, rot, tilt in RP.bar_speakers()])):
            tint = cfg['listen'] if grp == 'l' else cfg['bar']
            for i, (x, y, zz) in enumerate(spk):
                L[f'plinth{grp}{i}'] = {'type': 'area', 'position': [x, y, round(zz + 0.01, 3)], 'target': [x, y, round(zz + 0.9, 3)],
                                        'size_m': [0.40, 0.30], 'irradiance': round(v['plinth_lamp'] * v['plinth'] * RP.PLINTH_GAIN[tint], 3),
                                        'color': RP.PLINTH_COL[tint], 'camera': False, 'receivers': [f'*#{i}']}
    # the bar pair: a soft spot from the ceiling over the bartender's aisle onto each cabinet's face
    for i, (role, x, y, zz, rot, tilt) in enumerate(RP.bar_speakers()):
        L[f'barspk{i}'] = {'type': 'spot', 'position': [x, round(y - 1.25, 3), RP.CEIL - 0.25],
                           'target': [x, y, round(zz + 0.75, 3)], 'power_w': v.get('barspk_w', 30.0),
                           'cone_deg': v.get('barspk_cone', 26.0), 'blend': 0.8, 'radius_m': 0.03, 'color': 2700,
                           'camera': False}
    return L


S.products, S.props, S.lights = products, props, lights

BAR = {'title': 'the back bar: the bar pair in its niches either side of the decks, the Domes',
       # from a banquette table, across the counter to the back bar, square to it (Ginza's view of its Tannoys): the
       # niches, the record wall and the disc, the decks with EARF's players, the Domes low over the zinc
       # c1: seated at a banquette table the counter hid the pair (their tops alone above the zinc); standing at the
       # counter's customer side, the eye at 1.55, the sight line drops over the zinc onto the cabinets
       # the pair raised (the owner, with a photo of Ginza): seated at the counter's customer side, the eye at 1.35,
       # looking up a little to the cabinets on their ledges
       'camera': {'position': [6.9, 2.75, 1.35], 'target': [6.95, 6.0, 1.6], 'lens_mm': 24, 'level': True, 'fstop': 4.0,
                  'focus': [6.9, 5.6, 1.6]},
       'settings': {'exposure': 0.6, 'screen_glow': 1.0, 'pendant_w': 170.0, 'pendant_cone': 24.0}}
LISTEN = {'title': 'the listening zone: the listening pair on the altar',
          # p2 (p1 4.0, 4.0: the spots lit the felt above the pair, the pair murky, the chairs pink shells, a
          # dead-centre showroom view): seated, off axis, on 40 mm; the spots in front, on the cabinets' faces; the
          # Orbs 2.5 W; a browner velvet
          'camera': {'position': [12.4, 2.2, 1.12], 'target': [16.4, 3.4, 0.95], 'lens_mm': 40, 'level': True,
                     'fstop': 2.8, 'focus': [16.5, 1.95, 0.9]},
          'settings': {'exposure': 2.7, 'wb': 2700, 'screen_glow': 0.35, 'spk_irr': 1.0, 'altar_w': 170.0,
                       'altar_cone': 22.0, 'altar_z': 0.9, 'haze': 0.006, 'sphere_w': 2.5, 'sphere_glow': 0.45,
                       'niche_strip': 5.0}}
NAMES = {'smoke': 'Smoke', 'ember': 'Ember', 'ice': 'Ice', 'mixed': 'Mixed'}
VIEWS = {}
for c in RP.CONFIGS:
    for key, base in (('bar', BAR), ('listening', LISTEN)):
        VIEWS[f'{key}-{c}'] = {'title': f"{base['title']} ({NAMES[c]})", 'camera': dict(base['camera']),
                               'settings': {**base['settings'], 'config': c}}
VIEWS['street'] = {'title': 'the shopfront at night, from the kerb (Smoke)',
                   # round 36's best street framing (p2r): the shopfront in frame, the mullion off the altar
                   'camera': {'position': [-3.2, 2.2, 1.5], 'target': [17.0, 3.4, 1.35], 'lens_mm': 32, 'level': True,
                              'fstop': 5.6, 'focus': [0.0, 3.0, 1.6]},
                   # p2 (p1 5.0, 5.0: dark (15), the pair murky, the name opaque vinyl, the sill the brightest plane,
                   # the mullion through the counter): nearer on 40 mm with the altar in a clear pane; exposure 1.6;
                   # the name unlit; the street lamps 60 W; the altar spots 220 W
                   'camera': {'position': [-2.0, 1.6, 1.45], 'target': [17.0, 3.0, 1.3], 'lens_mm': 40, 'level': True,
                              'fstop': 5.6, 'focus': [0.0, 3.0, 1.6]},
                   'settings': {**T36.VIEWS['street']['settings'], 'config': 'smoke', 'etch_glow': 0.0,
                                'exposure': 1.6, 'disc_glow': 0.3, 'disc_lamp': 10.0, 'street_lamp': 60.0,
                                'altar_w': 220.0, 'altar_cone': 30.0, 'haze': 0.006}}
VIEWS['sink'] = {'title': 'the sink in Smoke, a detail',
                 'camera': dict(T36.VIEWS['sink']['camera']),
                 # p2 (p1 3.5, 4.0: no glow through the slab, the boards showing through it, the bowl a flat disc, the
                 # spout cropped, a black band at the left): the glow 4.0, the cast denser, the spot 3 W at 25 deg; the
                 # camera higher and a step right; f/5.6
                 'camera': {'position': [10.3, 1.2, 1.32], 'target': [11.0, 0.33, 0.95], 'lens_mm': 50, 'level': True,
                            'fstop': 5.6, 'focus': [10.98, 0.47, 0.86]},
                 'settings': {**T36.VIEWS['sink']['settings'], 'config': 'smoke', 'sink_glow': 2.0, 'sink_radius': 0.05,
                              'sink_spot': 3.0, 'sink_spot_cone': 25.0, 'exposure': 0.8}}
S.VIEWS = VIEWS
_shot = S.shot


def shot(view):
    s = _shot(view)
    s['title'] = s['title'].replace('(round 36)', '(round 37)').replace('(round 33)', '(round 37)')
    v = {**DEFAULT, **VIEWS[view]['settings']}
    s.setdefault('materials', {})['glow'] = {'strength': v['tt_glow']}       # the players' edges, lit
    return s


S.shot = shot


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--final']
    S.write(args or None, final='--final' in sys.argv)
