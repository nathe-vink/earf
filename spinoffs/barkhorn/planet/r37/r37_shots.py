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

DEFAULT = dict(T36.DEFAULT, **dict(config='smoke', colourway='neutral', disc_col='#FFD2A0', disc_glow=0.12,
                                   disc_lamp=4.0, spk_niche_strip=0.8, tt_glow=0.35, sink_glow=0.8))
S.DEFAULT = DEFAULT
KEYS = T36.KEYS + ('chair_leather', 'banq_col', 'sink_deep', 'sink_glow_col', 'decks', 'spk_niche_strip', 'niche_felt')


def room_piece(v):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'planet_r37', 'fn': 'room', **{k: v[k] for k in KEYS if k in v}}


S.room_piece = room_piece


def products(v):
    """Four speakers, one product: the listening pair on the altar, the bar pair in their niches; EARF's players at
    the decks. Each group in its configuration's tint."""
    cfg = RP.CONFIGS[v['config']]
    listen = [{'position': [round(x, 4), round(y, 4), z], 'rotate_z': rot, 'hide': ['cloth-disc']}
              for role, c, x, y, z, rot in RP.speakers()]
    bar = [{'position': [x, y, z], 'rotate_z': rot, 'hide': ['cloth-disc']} for role, x, y, z, rot in RP.bar_speakers()]
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


S.products, S.props = products, props

BAR = {'title': 'the back bar: the bar pair in its niches either side of the decks, the Domes',
       # from a banquette table, across the counter to the back bar, square to it (Ginza's view of its Tannoys): the
       # niches, the record wall and the disc, the decks with EARF's players, the Domes low over the zinc
       # c1: seated at a banquette table the counter hid the pair (their tops alone above the zinc); standing at the
       # counter's customer side, the eye at 1.55, the sight line drops over the zinc onto the cabinets
       'camera': {'position': [6.55, 2.55, 1.55], 'target': [6.95, 6.0, 0.95], 'lens_mm': 26, 'level': True, 'fstop': 4.0,
                  'focus': [6.9, 5.4, 0.9]},
       'settings': {'exposure': 0.6, 'screen_glow': 1.0, 'pendant_w': 170.0, 'pendant_cone': 24.0}}
LISTEN = {'title': 'the listening zone: the listening pair on the altar',
          'camera': {'position': [11.2, 2.75, 1.3], 'target': [16.6, 3.1, 1.0], 'lens_mm': 35, 'level': True,
                     'fstop': 4.0, 'focus': [16.3, 3.1, 0.9]},
          'settings': {'exposure': 1.9, 'wb': 2700, 'screen_glow': 0.35, 'spk_irr': 1.0, 'altar_w': 130.0,
                       'altar_cone': 28.0, 'altar_z': 0.8, 'haze': 0.008, 'sphere_w': 4.0, 'sphere_glow': 0.6,
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
                   'settings': {**T36.VIEWS['street']['settings'], 'config': 'smoke', 'etch_glow': 0.05,
                                'exposure': 1.2, 'disc_glow': 0.3, 'disc_lamp': 10.0}}
VIEWS['sink'] = {'title': 'the sink in Smoke, a detail',
                 'camera': dict(T36.VIEWS['sink']['camera']),
                 'settings': {**T36.VIEWS['sink']['settings'], 'config': 'smoke', 'sink_glow': 1.2}}
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
