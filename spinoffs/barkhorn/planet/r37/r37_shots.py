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
            # the plinths' own surface glow at half the lamp's share: at full it read as a hot line on the plinth tops
            # (listening p2) and was the last red clipping in Ember (r37)
            'plinth_bar': round(0.5 * v['plinth'] * RP.PLINTH_GAIN[cfg['bar']], 3), 'plinth_bar_col': RP.PLINTH_COL[cfg['bar']],
            'plinth_listen': round(0.5 * v['plinth'] * RP.PLINTH_GAIN[cfg['listen']], 3),
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
             'spots': [[x, y, RP.DOME['rim_z']] for x in RP.DOMES], 'ceiling': RP.CEIL,
             'lamp_w': round(v['dome_w'] * RP.LAMP_GAIN[cfg['dome']], 2),
             'lamp_k': 2700, 'shade_glow': v.get('dome_glow_' + cfg['dome'], RP.LAMP_GLOW[cfg['dome']]),
             'noshadow': noshadow},
            {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb', 'flavour': RP.LAMP_FLAVOUR[cfg['orb']],
             'spots': [list(s) for s in RP.sphere_spots()], 'lamp_w': round(v['sphere_w'] * RP.LAMP_GAIN[cfg['orb']], 2),
             'lamp_k': 2700,
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
    # the light on each pair scaled to its tint (a saturated red clips first)
    gl, gb = RP.SPK_GAIN[cfg['listen']], RP.SPK_GAIN[cfg['bar']]
    for k, l in L.items():
        if k.startswith('altar') and 'power_w' in l:
            l['power_w'] = round(l['power_w'] * gl, 2)
        elif k.startswith('spk') and 'irradiance' in l:
            l['irradiance'] = round(l['irradiance'] * gl, 3)
    # and a small spot in each niche's head, down the cabinet's face, so the smoked acrylic's edges and horn catch light
    if v.get('niche_spot_w', 0) > 0:
        for i, (role, x, y, zz, rot, tilt) in enumerate(RP.bar_speakers()):
            x0, x1, yf, yb, z0, z1 = RP.niche_box(x)
            L[f'nichespk{i}'] = {'type': 'spot', 'position': [x, round(yf + 0.08, 3), round(z1 - 0.08, 3)],
                                 'target': [x, y, round(zz + 0.8, 3)], 'power_w': round(v['niche_spot_w'] * gb, 2),
                                 'cone_deg': 30.0, 'blend': 0.8, 'radius_m': 0.02, 'color': 2600, 'camera': False}
    # the bar pair: a soft spot from the ceiling over the bartender's aisle onto each cabinet's face
    for i, (role, x, y, zz, rot, tilt) in enumerate(RP.bar_speakers()):
        L[f'barspk{i}'] = {'type': 'spot', 'position': [x, round(y - 1.25, 3), RP.CEIL - 0.25],
                           'target': [x, y, round(zz + 0.75, 3)], 'power_w': round(v.get('barspk_w', 30.0) * gb, 2),
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
       # p2 (p1 4.5, 4.5: a square elevation with the Domes across the cabinets, the pair dark (36-39), the players'
       # blue the loudest colour, the disc and niche heads cold, the fluted front salmon and the brightest surface):
       # seated and off axis on 28 mm, a chair back in the foreground; the pair's spots 60 W; the Domes calmer and
       # their downlights pooled; the counter strip down; the disc and niche strips warm
       # p3 (p2 5.0, 5.0: the pair still dark (26, 32); the cells round the disc the brightest flat squares; the players'
       # blue (a near-neutral glow under warm white balance: now the configuration's warm colour); the chair back dead
       # centre; a hot line at the niche base): a spot in each niche's head down the cabinet's face; the record wall's
       # spots 14 W at 18 deg; the disc 0.5 with 10 W; the plinths 0.6; a step right so the chair goes to the edge
       'camera': {'position': [6.4, 2.5, 1.22], 'target': [7.1, 6.0, 1.3], 'lens_mm': 28, 'level': True, 'fstop': 4.0,
                  'focus': [7.0, 5.6, 1.5]},
       'settings': {'exposure': 0.6, 'screen_glow': 1.0, 'pendant_w': 140.0, 'pendant_cone': 20.0, 'barspk_w': 60.0,
                    'counter_strip': 1.2, 'disc_glow': 0.5, 'disc_col': '#FFC890', 'disc_lamp': 10.0, 'rw_w': 14.0,
                    'rw_cone': 18.0, 'niche_spot_w': 25.0, 'plinth': 0.6}}
LISTEN = {'title': 'the listening zone: the listening pair on the altar',
          # p2 (p1 4.0, 4.0: the spots lit the felt above the pair, the pair murky, the chairs pink shells, a
          # dead-centre showroom view): seated, off axis, on 40 mm; the spots in front, on the cabinets' faces; the
          # Orbs 2.5 W; a browner velvet
          # p3 (p2 3.5, 3.5: the seated 40 mm framed only the niche, no chairs, Orbs or carpet, the right speaker cut;
          # the horns black; the plinth tops a hot line): on the zone's axis behind a tub chair, 30 mm; the spots
          # 240 W at 30 deg aimed higher; the Orbs 6 W, glow 0.55; the light plinths half; haze 0.012
          'camera': {'position': [11.3, 3.05, 1.2], 'target': [16.4, 3.05, 1.05], 'lens_mm': 30, 'level': True,
                     'fstop': 4.0, 'focus': [16.4, 3.05, 1.0]},
          'settings': {'exposure': 3.0, 'wb': 2700, 'screen_glow': 0.35, 'spk_irr': 0.6, 'altar_w': 240.0,
                       'altar_cone': 30.0, 'altar_z': 1.2, 'haze': 0.012, 'sphere_w': 6.0, 'sphere_glow': 0.55,
                       'niche_strip': 5.0, 'plinth': 0.5}}
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
                   # p3 (p2 4.0, 4.5: the pier dead centre over the altar): on the room's axis through the glass, 35 mm
                   # p4 (p3 5.0, 5.0: the name opaque paint and its E cut; the pair grey and small; the mullion
                   # central; the lightbox a blank flat): back across the pavement on 28 mm, the whole name and the
                   # shopfront in frame; the name 0.05; the altar 650 W at 18 deg; the screens 1.0; haze 0.006
                   'camera': {'position': [-3.8, 3.3, 1.5], 'target': [17.0, 3.2, 1.35], 'lens_mm': 28, 'level': True,
                              'fstop': 8.0, 'focus': [6.0, 3.0, 1.4]},
                   'settings': {**T36.VIEWS['street']['settings'], 'config': 'smoke', 'etch_glow': 0.0,
                                'exposure': 1.6, 'disc_glow': 0.3, 'disc_lamp': 10.0, 'street_lamp': 120.0,
                                'altar_w': 650.0, 'altar_cone': 18.0, 'haze': 0.006, 'screen_glow': 1.0,
                                'screen_rough': 0.6, 'etch_glow': 0.05, 'wb': 2900}}
VIEWS['sink'] = {'title': 'the sink in Smoke, a detail',
                 'camera': dict(T36.VIEWS['sink']['camera']),
                 # p2 (p1 3.5, 4.0: no glow through the slab, the boards showing through it, the bowl a flat disc, the
                 # spout cropped, a black band at the left): the glow 4.0, the cast denser, the spot 3 W at 25 deg; the
                 # camera higher and a step right; f/5.6
                 # p3 (p2 4.5, 4.5: the basin a clipped white oval (35 %), the slab's face flat, no thickness; the black
                 # band left): the glow 0.6 in amber; the spot 6 W at 35 deg; lower, nearer the slab's level
                 'camera': {'position': [10.25, 1.35, 1.08], 'target': [11.0, 0.40, 0.90], 'lens_mm': 50, 'level': True,
                            'fstop': 5.6, 'focus': [10.98, 0.47, 0.86]},
                 'settings': {**T36.VIEWS['sink']['settings'], 'config': 'smoke', 'sink_glow': 0.6, 'sink_radius': 0.05,
                              'sink_glow_col': '#FF9A4A', 'sink_spot': 6.0, 'sink_spot_cone': 35.0, 'exposure': 0.8}}
S.VIEWS = VIEWS
_shot = S.shot


def shot(view):
    s = _shot(view)
    s['title'] = s['title'].replace('(round 36)', '(round 37)').replace('(round 33)', '(round 37)')
    v = {**DEFAULT, **VIEWS[view]['settings']}
    # the players' edges, lit, in the configuration's warm light colour (their own Smoke glow, a near-neutral lavender,
    # read electric blue under the room's 2700-3000 K white balance: bar p2)
    tint = RP.CONFIGS[v['config']]['tt']
    s.setdefault('materials', {})['glow'] = {'strength': v['tt_glow'], 'color': RP.PLINTH_COL[tint]}
    return s


S.shot = shot


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--final']
    S.write(args or None, final='--final' in sys.argv)
