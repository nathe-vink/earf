"""Planet EARF's shots, round 33 (the den): one room, one model, every view.

    python3 spinoffs/barkhorn/planet/den/den_shots.py [VIEW ...] [--final]   # writes studio/shots/barkhorn/planet33/
    python3 studio/engine/render.py studio/shots/barkhorn/planet33/bar.json --out IMG [--samples N --scale S]

The room is the kit piece `planet_den` (studio/engine/kit_ext/planet_den.py), built from den_plan.py; the products
come from their own CAD: the Atmosphere speakers (barkhorn-cloud), Bell (barkhorn-lamp) and Cumulus
(barkhorn-turntable; a small stand-in, out of focus, while the companions are redesigned). The light is the room's own,
in pools: shaded sconces, three brass pendants, the back-bar's shelf strips, Bell on the tables, candles, a picture
light on the record wall, a soft lamp on each Ember speaker, a pinhole in each niche; outside, the street lamps.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, HERE)
import den_plan as P                                                # noqa: E402

OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet33')
CLOUD = 'studio/products/barkhorn-cloud.json'
TT = 'studio/products/barkhorn-turntable.json'
LAMP = 'studio/products/barkhorn-lamp.json'
LAMP_STRIP_Z = 0.441             # Bell's strip above its foot (companions/shots.py)
SIDE_H = 0.50                    # the lounge's side tables' tops

DEFAULT = dict(
    sconce_w=10.0, pendant_w=45.0, pendant_cone=75.0, shelf_glow=10.0, shade_glow=0.12, niche_glow=0.9, pendant_glow=0.5, flame=25.0,
    candle_w=0.6, bell_w=22.0, spk_irr=3.0, spot_niche=220.0, record_glow=2.0, spot_records=18.0, vu=2.0,
    street_lamp=500.0, windows_lit=0.5, haze=0.006, street=True, neighbour_plain=True, flat_glow=0.06,
    exposure=0.0, wb=3200, wb_tint=0.0, view='Khronos PBR Neutral', look='None', samples=256,
)
WARM = 2400                      # the room's lamps (K)


def room_piece(v):
    keys = ('shelf_glow', 'shade_glow', 'pendant_glow', 'flame', 'record_glow', 'vu', 'street', 'windows_lit', 'wet',
            'road_rough', 'floor_tex', 'floor_tint', 'floor_mix', 'floor_coat', 'plaster', 'plaster_mix', 'ceiling',
            'brick_tint', 'rug_tex', 'rug_tint', 'rug_mix', 'rug_value', 'props', 'sign', 'cafe', 'no_glass',
            'glass_gloss', 'siding', 'neighbour', 'neighbour_plain', 'niche_glow', 'gold_glow', 'brick_scale', 'brick_mix', 'across_glow', 'flat_glow', 'shelf_color',
            'niche_rim', 'console_lift', 'storefront_paint', 'linen_trans', 'brick_tex', 'brick_bump', 'rug_displace', 'rug_cell', 'transom_glow')
    return {'kind': 'kit', 'shape': 'ext', 'module': 'planet_den', 'fn': 'room', **{k: v[k] for k in keys if k in v}}


def props(v):
    out = [room_piece(v)]
    for i, (x, y) in enumerate(P.stools()):                           # the bar stools (Poly Haven, CC0)
        out.append({'kind': 'kit', 'shape': 'asset', 'model': 'bar_chair_round_01', 'res': '1k',
                    'position': [round(x, 3), round(y, 3), 0.0], 'rotate': [0, 0, (i * 37) % 23 - 11]})
    for i, cx in enumerate(P.TABLES):                                 # a chair at each two-top, facing the banquette
        out.append({'kind': 'kit', 'shape': 'asset', 'model': v.get('chair_model', 'dining_chair_02'), 'res': '1k',
                    'position': [round(cx + (i % 3 - 1) * 0.04, 3), round(P.CHAIR_Y, 3), 0.0],
                    'rotate': [0, 0, v.get('dining_rot0', 180.0) + (i * 23) % 9 - 4]})
    wx, wy = P.WINDOW_TABLE                                           # and two at the window table
    for k, (dy, a) in enumerate(((-0.62, 0.0), (0.62, 180.0))):
        out.append({'kind': 'kit', 'shape': 'asset', 'model': v.get('chair_model', 'dining_chair_02'), 'res': '1k',
                    'position': [wx, wy + dy, 0.0], 'rotate': [0, 0, v.get('dining_rot0', 180.0) + a + 90 + 6 * k]})
    for x, y, f in P.CHAIRS:                                          # the lounge's low leather chairs, as scanned
        out.append({'kind': 'kit', 'shape': 'asset', 'model': 'mid_century_lounge_chair', 'res': '1k',
                    'position': [x, y, 0.008],
                    'rotate': [0, 0, -90.0 + f + ((int(x * 10) * 7 + int(y * 10) * 3) % 7 - 3)]})
    if v['street']:                                                   # the street lamps along the curb (CC0)
        for y in STREET_LAMPS:
            out.append({'kind': 'kit', 'shape': 'asset', 'model': 'street_lamp_01', 'res': '1k',
                        'position': [CURB_X + 0.4, y, 0.0], 'rotate': [0, 0, v.get('lamp_rot', 90.0)]})
    return out


def products(v):
    spk = [{'flavour': P.FLAVOUR[c], 'position': [round(x, 4), round(y, 4), z], 'rotate_z': rot, 'hide': ['cloth-disc']}
           for role, c, x, y, z, rot in P.speakers()]
    T = P.TABLE
    lamps = [{'flavour': BELL, 'position': [round(P.TABLES[i] - 0.17, 4), round(T['y'] - 0.14, 4), T['h']], 'rotate_z': 0.0}
             for i in BELL_TABLES]
    lamps += [{'flavour': BELL, 'position': [P.WINDOW_TABLE[0] - 0.12, P.WINDOW_TABLE[1] + 0.10, T['h']], 'rotate_z': 0.0}]
    lamps += [{'flavour': BELL, 'position': [x, y, SIDE_H], 'rotate_z': 0.0} for x, y in P.SIDE_TABLES[1:]]
    tt = [{'flavour': 'smoke', 'position': [round(P.L - 0.30, 4), round(P.W / 2 - 0.30, 4), P.CONSOLE['h']], 'rotate_z': -90.0}]
    return [{'def': CLOUD, 'flavour': spk[0]['flavour'], 'instances': spk},
            {'def': LAMP, 'flavour': BELL, 'instances': lamps},
            {'def': TT, 'flavour': 'smoke', 'instances': tt}]


def lights(v):
    L = {}
    # a soft warm lamp from the ceiling onto each Ember speaker; a pinhole in each niche's head onto the back-bar pair
    for k, (role, c, x, y, z, rot) in enumerate(P.speakers()):
        if role == 'lounge':
            fx, fy = math.sin(math.radians(rot)), -math.cos(math.radians(rot))
            L[f'spk{k}'] = {'type': 'area', 'position': [round(x + 0.9 * fx, 3), round(y + 0.9 * fy, 3), P.CEIL - 0.2],
                            'target': [x, y, 0.75], 'size_m': [0.35, 0.35], 'irradiance': v['spk_irr'],
                            'color': v.get('spk_k', 2700), 'spread_deg': v.get('spk_spread', 180)}
            if v.get('spk_back', 0) > 0:                              # low behind the cabinet, lighting through it
                L[f'spkb{k}'] = {'type': 'area', 'position': [round(x - 0.55 * fx, 3), round(y - 0.55 * fy, 3), 0.35],
                                 'target': [x, y, 0.65], 'size_m': [0.3, 0.3], 'irradiance': v['spk_back'],
                                 'color': v.get('spk_k', 2700), 'camera': False}
        else:
            if v.get('niche_fill', 0) > 0:                            # a fill at the niche floor's front lip, up the cabinet
                L[f'nfill{k}'] = {'type': 'area', 'position': [x, y - 0.33, P.NICHE_Z0 + 0.03], 'target': [x, y, z + 0.5],
                                  'size_m': [0.3, 0.05], 'power_w': v['niche_fill'], 'color': 2600, 'camera': False}
            L[f'niche{k}'] = {'type': 'spot', 'position': [x, y - v.get('niche_dy', 0.10), P.NICHE_Z0 + P.NICHE_H - 0.04],
                              'target': [x, y - 0.22, z + v.get('niche_aim_z', 0.6)], 'power_w': v['spot_niche'],
                              'cone_deg': v.get('niche_cone', 45), 'blend': 0.8,
                              'radius_m': 0.02, 'color': 2600}
    # the sconces: a lamp inside each shade
    for i, x in enumerate(P.SCONCES_RIGHT):
        L[f'sconceR{i}'] = {'type': 'point', 'position': [x, 0.22, P.SCONCE_Z + 0.06], 'power_w': v['sconce_w'],
                            'radius_m': 0.03, 'color': WARM, 'camera': False}
    for i, x in enumerate(P.SCONCES_LEFT_LOUNGE):
        L[f'sconceL{i}'] = {'type': 'point', 'position': [x, P.W - 0.20, P.SCONCE_Z + 0.06], 'power_w': v['sconce_w'],
                            'radius_m': 0.03, 'color': WARM, 'camera': False}
    # the pendants: a downlight in each dome onto the bar top
    for i, x in enumerate(P.PENDANTS):
        L[f'pend{i}'] = {'type': 'spot', 'position': [x, P.BAR_FRONT + 0.18, P.PENDANT_RIM + 0.10],
                         'target': [x, P.BAR_FRONT + 0.05, P.BAR_TOP_Z], 'power_w': v['pendant_w'],
                         'cone_deg': v['pendant_cone'], 'blend': 0.6, 'radius_m': 0.04, 'color': WARM}
    # the record wall's picture light: three soft spots from under its cornice
    if v.get('spot_records', 0) > 0:
        for k, yy in enumerate((P.W / 2 - 1.0, P.W / 2, P.W / 2 + 1.0)):
            L[f'rec{k}'] = {'type': 'spot', 'position': [P.L - P.REC['depth'] - 0.06, yy, P.REC['z1'] - 0.03],
                            'target': [P.L - 0.2, yy, v.get('rec_aim_z', 0.6)], 'power_w': v['spot_records'],
                            'cone_deg': v.get('rec_cone', 60), 'blend': 0.9,
                            'radius_m': 0.03, 'color': 2500}
    # candles: a tiny warm point at each flame
    for k, (x, y, z) in enumerate(P.candle_spots()):
        L[f'candle{k}'] = {'type': 'point', 'position': [x, y, z + 0.035], 'power_w': v['candle_w'], 'radius_m': 0.006,
                           'color': 1900, 'camera': False}
    # Bell: three small lamps just outside each lamp's opal sleeve (companions/shots.py's bell_lights)
    def bell(lx, ly, h, watts, tag):
        for k in range(3):
            a = math.radians(90 + 120 * k)
            L[f'{tag}{k}'] = {'type': 'point', 'position': [round(lx + 0.047 * math.cos(a), 4), round(ly + 0.047 * math.sin(a), 4),
                                                             round(h + LAMP_STRIP_Z, 4)],
                              'power_w': watts / 3, 'radius_m': 0.04, 'color': 2500, 'camera': False,
                              'transmission': False, 'specular': 0.0}
    T = P.TABLE
    for i in BELL_TABLES:
        bell(P.TABLES[i] - 0.17, T['y'] - 0.14, T['h'], v['bell_w'], f'bellT{i}-')
    bell(P.WINDOW_TABLE[0] - 0.12, P.WINDOW_TABLE[1] + 0.10, T['h'], v['bell_w'], 'bellW-')
    for i, (x, y) in enumerate(P.SIDE_TABLES[1:]):
        bell(x, y, SIDE_H, v['bell_w'], f'bellS{i}-')
    if v.get('bounce', 0) > 0:                                        # a low warm bounce by the window table (bar-r1 c4)
        L['bounce'] = {'type': 'area', 'position': [2.4, 3.2, 0.25], 'target': [5.0, 3.9, 0.5], 'size_m': [1.0, 0.5],
                       'power_w': v['bounce'], 'color': 2500, 'camera': False}
    if v['street']:
        for k, y in enumerate(STREET_LAMPS):
            L[f'street{k}'] = {'type': 'point', 'position': [CURB_X + 0.4 + v.get('lamp_dx', 0.9), y, v.get('lamp_z', 5.6)],
                               'power_w': v['street_lamp'], 'radius_m': 0.15, 'color': v.get('lamp_k', 2700)}
        if v.get('lamp_cam', 0) > 0:                                  # a lamp across the street, behind the camera
            L['street-cam'] = {'type': 'point', 'position': [CURB_X - 12.4, 1.0, 5.6], 'power_w': v['lamp_cam'],
                               'radius_m': 0.15, 'color': v.get('lamp_k', 2700)}
        E = P.ENTRY                                                    # the vestibule's downlight, the sign's lamp
        if v.get('entry_w', 0) > 0:
            L['entry'] = {'type': 'spot', 'position': [0.6, (E['y0'] + E['y1']) / 2, P.TRANSOM['z0'] - 0.08],
                          'target': [0.6, (E['y0'] + E['y1']) / 2, 0.0], 'power_w': v['entry_w'], 'cone_deg': v.get('entry_cone', 70),
                          'blend': 0.8, 'radius_m': 0.03, 'color': 2400}
        if v.get('sign_w', 0) > 0:
            yc = (P.WINDOW['y0'] + P.WINDOW['y1']) / 2
            L['sign'] = {'type': 'spot', 'position': [-0.45, yc, P.TRANSOM['z0'] + 0.08], 'target': [-0.09, yc, P.SIGN['z']],
                         'power_w': v['sign_w'], 'cone_deg': 25, 'blend': 0.6, 'radius_m': 0.02, 'color': 2700}
    return L


def shot(view):
    vw = VIEWS[view]
    v = {**DEFAULT, **vw.get('settings', {})}
    return {
        'title': f'Planet EARF, {vw["title"]} (round 33)',
        'size': vw.get('size', [2400, 1600]),
        'camera': vw['camera'],
        'products': products(v),
        'set': {'kind': 'stage', 'props': props(v)},
        'sky': {'kind': 'gradient', 'zenith': v.get('sky_zenith', '#05070C'), 'horizon': v.get('sky_horizon', '#141824'),
                'ground': '#08080A', 'strength': v.get('sky', 0.0)},
        'lights': lights(v),
        'haze': {'box_m': [0.05, 0.05, 0.01, P.L - 0.05, P.W - 0.05, P.CEIL - 0.08], 'density': v['haze'], 'anisotropy': 0.3,
                 'color': '#FFFFFF'} if v['haze'] > 0 else {},
        'render': {'samples': v['samples'], 'adaptive': 0.02, 'denoise': True, 'clamp': 10, 'bounces': 10,
                   'view': v['view'], 'look': v['look'], 'exposure': v['exposure'], 'white_balance_k': v['wb'],
                   'white_balance_tint': v['wb_tint']},
    }


BELL = 'dust'                    # Bell's colour throughout: a warm amber opal
BELL_TABLES = (1, 3)             # Bell on two of the banquette's tables, candles on the others
CURB_X = -0.16 - 3.4             # the curb's face (the kit's street)
STREET_LAMPS = (-6.0, P.W + 9.0)
VIEWS = {
    'street': {'title': 'the shopfront at night, from across the street',
               # three-quarter from across the street and up it, so the bays read as bays; the shopfront the subject
               # after street-r1 (3.5): closer on 50 mm, the shopfront filling the frame and the view running down the
               # room; the room brighter, the street lamps cooler and off the facades, a dusk-blue sky, the name gilded
               # and lit, the vestibule and transoms lit, blinds in the windows, haze in the room
               # after street-r2 (4.5): looking down the room so one Ember speaker glows over the café curtains on the
               # right third; the street lamps up, one raking from behind the camera; gilt without glow; the transom
               # soft; the vestibule lit wider; a bottle-green shopfront (the warm room's cool counter-note)
               # after street-r3 (4.5): three-quarter from up the street on the bar's side, 40 mm f/2.8 on the glass,
               # pavement in front, the line of sight through the window to the right-hand Ember speaker; the gilt
               # brighter, the café curtains translucent, the lamps softer, the records down, the pendants up
               'camera': {'position': [-9.5, 7.5, 1.6], 'target': [0.0, 3.2, 2.0], 'lens_mm': 40, 'level': True,
                          'fstop': 2.8, 'focus': [-0.09, 3.6, 1.8]},
               'settings': {'exposure': 0.9, 'wb': 3200, 'wet': True, 'road_rough': 0.12, 'street_lamp': 120.0,
                            'lamp_k': 3500, 'lamp_dx': 0.0, 'lamp_cam': 200.0, 'gold_glow': 0.4, 'sign_w': 15.0,
                            'linen_trans': 0.5, 'spot_records': 9.0, 'record_glow': 1.0,
                            'entry_w': 30.0, 'entry_cone': 100.0, 'transom_glow': 0.5, 'spk_irr': 12.0, 'pendant_w': 130.0,
                            'storefront_paint': '#1F2B24', 'sconce_w': 25.0, 'haze': 0.04,
                            'siding': '#8E9384', 'sky': 0.05, 'sky_zenith': '#1A2440', 'sky_horizon': '#2A3550',
                            'flat_glow': 0.12, 'across_glow': 0.06}},
    'bar': {'title': 'the bar, from the window table',
            # bar-r2: the niche a soft glow, not a lightbox; the pinhole from the niche's front edge onto the face and
            # horn; a fill up the cabinet; the rim strip down; pendants pooling harder; the grade lifted and warmer
            'settings': {'exposure': 1.1, 'wb': 2650, 'niche_glow': 0.3, 'spot_niche': 450.0, 'niche_cone': 40.0,
                         'niche_dy': 0.30, 'niche_aim_z': 0.9, 'niche_fill': 15.0, 'niche_rim': 0.5,
                         'pendant_w': 220.0, 'pendant_cone': 45.0,
                         'pendant_glow': 2.0, 'bounce': 15.0, 'spot_records': 9.0, 'record_glow': 1.0, 'haze': 0.012,
                         'shelf_glow': 5.0},
            # after bar-r1 (5.0): into the room on 40 mm, the right-hand Smoke speaker the hero, the other out of frame;
            # its niche darker behind it with a rim, a stronger pinhole; pendants pooling on the top; the far room down
            # (p5: from 3.4, 3.4 the bar top filled the frame and the speaker sat small at 6 m) from a stool's side,
            # 3.7 m off the speaker, the far room out of frame
            # after bar-r2 (4.5): back and wider, the pendants in the top quarter, the niche near the centre
            'camera': {'position': [5.9, 3.0, 1.30], 'target': [9.06, 5.9, 1.55], 'lens_mm': 32, 'level': True,
                       'fstop': 4.0, 'focus': [P.NICHES[1][0] + P.NICHES[1][1] / 2, P.BACKBAR_Y + 0.05, 1.3]}},
    'listening': {'title': 'the listening room, one of the Ember pair',
                  # after listening-r1 (4.5): 40 mm from further back and lower, the speaker on the left third; the
                  # speaker lit harder and from behind, the sconce and the records down, the grade less orange
                  # after listening-r2 (5.5): back and lower on 35 mm so the plinth stands on floor and a chair reads
                  # (p6: from 14.1, 2.3 the camera stood behind a front-row chair) clear of the chairs, the one by the
                  # brick a foreground layer
                  'camera': {'position': [14.6, 2.0, 0.95], 'target': [16.3, 4.5, 0.75], 'lens_mm': 35, 'level': True,
                             'fstop': 2.8, 'focus': [16.15, P.PAIR['y'][1], 0.9]},
                  # (p7: 28 W/m2 in 0.025 haze veiled the frame milky) the lamp on each speaker held to a 30 deg
                  # spread so it lights the cabinet, not the room; the haze back to 0.008
                  'settings': {'spk_irr': 20.0, 'spk_spread': 30.0, 'spk_k': 3000, 'spk_back': 6.0, 'sconce_w': 4.0,
                               'shade_glow': 0.02, 'wb': 2900, 'exposure': -0.8, 'spot_records': 4.0, 'rec_cone': 40.0,
                               'rec_aim_z': 1.2, 'record_glow': 0.3, 'haze': 0.008, 'console_lift': 0.55,
                               # the lead: red acrylic on red brick is a hue clash; the brick much darker and aged, so
                               # the speaker's own light separates it
                               'brick_tint': '#3A2C25', 'brick_mix': 0.65}},
}

FINISH = {'enabled': True, 'white_in': 236, 'white_out': 240, 'contrast': 0.10, 'clarity': 0.06, 'sharpen': 0.3,
          'sharpen_px': 0.7}


def write(names=None, final=False):
    out = os.path.join(OUT, 'final') if final else OUT
    os.makedirs(out, exist_ok=True)
    for n in names or VIEWS:
        s = shot(n)
        if final:
            s['render'].update({'samples': 256, 'adaptive': 0.01})
            s['finish'] = dict(FINISH)
        p = os.path.join(out, f'{n}.json')
        json.dump(s, open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--final']
    write(args or None, final='--final' in sys.argv)
