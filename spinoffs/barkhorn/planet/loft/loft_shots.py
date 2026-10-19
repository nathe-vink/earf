"""Planet EARF's shots, round 34 (the loft): the den's shot builder (den/den_shots.py) on the loft's room.

    python3 spinoffs/barkhorn/planet/loft/loft_shots.py [VIEW ...] [--final]   # writes studio/shots/barkhorn/planet34/
    python3 studio/engine/render.py studio/shots/barkhorn/planet34/bar.json --out IMG [--samples N --scale S]

The room is the kit piece `planet_loft` (studio/engine/kit_ext/planet_loft.py); the plan is loft_plan.py (the den's
footprint plus the beams, the screens and the acrylic). The light: frosted acrylic pendants over the bar, the back-bar's
edge-lit shelves and the niches' frosted backs, the screens (their images through frosted acrylic), one sconce and Bell
in the listening room, candles, a pinhole on each speaker, the record wall's light; outside, the street lamps.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'den'))
import loft_plan as LP                                              # noqa: E402
import den_shots as S                                               # noqa: E402

S.P = LP                                                            # the den's builder reads the loft's plan
S.OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet34')
S.BELL = 'fog'                                                      # Bell's opal white: no second colour in a frame

DEFAULT = dict(S.DEFAULT, **dict(
    sconce_w=6.0, pendant_w=60.0, pendant_cone=50.0, shelf_glow=1.0, shade_glow=0.4, niche_glow=0.6, pendant_glow=0.25,
    pendant_lamp=2.5,                # (bar-r2: the 4.0s here had overridden the kit's calmer edges and lamps)
    screen_glow=0.8, inlay_glow=0.6, etch_glow=0.05, spot_records=9.0, record_glow=1.0,
    menu_color='#8A6E4E',             # kraft card (bar-r4: white menus glowed like phones)
    rug_tex='poly_wool_herringbone', rug_tint='#4A4541', rug_mix=0.7, rug_value=0.9, haze=0.008,
    wb=3300, exposure=0.0,
    # AgX, measured against Khronos PBR Neutral on the bar frame (README): crush 0.07 % vs 0.98, no clipping vs 0.3 %,
    # median 27.9 vs 19.4, whites warm-white not orange (b 19 vs 2)
    view='AgX'))
S.DEFAULT = DEFAULT
LOFT_KEYS = ('screen_glow', 'screen_banquette-a', 'screen_banquette-b', 'screen_lounge', 'screen_window', 'inlay_glow',
             'pendant_lamp', 'concrete_tint', 'concrete_mix', 'concrete_tex', 'floor_acg', 'floor_tint', 'floor_mix',
             'floor_coat', 'etch_glow', 'shade_glow', 'niche_glow', 'menu_color', 'screen_tint', 'tlamp_glow',
             'tlamp_bulb', 'etch_frost', 'etch_col')
_room_piece = S.room_piece


def room_piece(v):
    out = _room_piece(v)
    out['module'] = 'planet_loft'
    out.update({k: v[k] for k in LOFT_KEYS if k in v})
    return out


S.room_piece = room_piece


def lamp_spots(v):
    """Where the den stood Bell: two banquette tables, the window table, the lounge's side tables, any extra."""
    T = LP.TABLE
    out = [[round(LP.TABLES[i] - 0.17, 4), round(T['y'] - 0.14, 4), T['h']] for i in S.BELL_TABLES]
    out += [[LP.WINDOW_TABLE[0] - 0.12, LP.WINDOW_TABLE[1] + 0.10, T['h']]]
    out += [[x, y, S.SIDE_H] for x, y in LP.SIDE_TABLES[1:]]
    return out + [list(b) for b in v.get('extra_bells', [])]


def room_piece(v, _rp=room_piece):
    out = _rp(v)
    out['table_lamps'] = lamp_spots(v)
    return out


S.room_piece = room_piece
_products = S.products


def products(v):
    """The Ember speakers only: no Bell and no Cumulus in Planet (the lead, 2026-10-19: the owner has not picked their
    second designs); a plain table lamp stands where Bell stood (the kit's table_lamps)."""
    return [g for g in _products(v) if g['def'] == S.CLOUD]


S.products = products
_lights = S.lights


def lights(v):
    """The den's lights with each Bell's three strip lamps replaced by one bulb inside the table lamp's drum."""
    L = {k: l for k, l in _lights(v).items() if not k.startswith('bell')}
    for i, (x, y, z) in enumerate(lamp_spots(v)):
        L[f'tlamp{i}'] = {'type': 'point', 'position': [x, y, round(z + 0.27, 4)], 'power_w': v['bell_w'],
                          'radius_m': 0.02, 'color': v.get('tlamp_k', 2700), 'camera': False}
    return L


S.lights = lights

VIEWS = {
    'bar': {'title': 'the bar, down the room',
            # concept changed after three passes at 4.0 to 4.5 on the close corner (bar-r1 to r3; two critics: a Fog-only
            # frame cannot carry the room's one colour): from the window table down the room's length, the bar and the
            # back-bar on the left, the banquette's frosted screens on the right, the pendants, and an Ember speaker
            # glowing at the far end through the smoked partition
            # after bar-r4 (5.5): 35 mm, the sightline past the chairs to the left Ember speaker; the alcove, the records
            # and the screens calmer; warmer balance; the pendants pooling on the bar, their tubes dim; less haze
            # after bar-r5 (4.5): seated at the banquette's first table on 50 mm, the Ember speaker on the right third;
            # it lit harder (linked); the screens warmer and lower; brighter; the pendants' lamps hidden from the camera
            'camera': {'position': [4.5, 2.4, 1.30], 'target': [16.0, 3.4, 1.0], 'lens_mm': 50, 'level': True,
                       'fstop': 4.0, 'focus': [9.0, 4.5, 1.1]},
            'settings': {'exposure': 1.3, 'wb': 2900, 'shelf_glow': 0.18, 'niche_glow': 0.25, 'spot_niche': 160.0,
                         'niche_cone': 30.0, 'niche_dy': 0.32, 'niche_aim_z': 1.2, 'pendant_w': 180.0,
                         'pendant_cone': 24.0, 'pendant_glow': 0.18, 'pendant_lamp': 1.6, 'haze': 0.015,
                         'screen_glow': 0.12, 'screen_tint': '#FFA060', 'inlay_glow': 1.0, 'floor_coat': 0.3,
                         'spk_irr': 20.0, 'spk_back': 30.0, 'spk_spread': 90.0, 'spk_link': True,
                         'spot_records': 10.0, 'rec_cone': 40.0, 'chair_dye': '#4A3A32'}},
    'listening': {'title': 'the listening room, one of the Ember pair',
                  # after the two critics on p6 (5.5, 5.0; mean 5.25): back and lower on 24 mm shifted up, the speaker
                  # whole on the floor and the beams in; the screen and the records well below the speaker, the
                  # speaker lit harder (linked) with a rim from behind; a neutral warm grey (3000 K); darker; pools
                  'camera': {'position': [14.35, 2.75, 1.05], 'target': [16.3, 4.6, 1.35], 'lens_mm': 24, 'level': True,
                             'fstop': 2.8, 'focus': [16.15, LP.PAIR['y'][1], 0.9]},
                  # after the two critics on p7 (4.5, 4.5: flat, sourceless, no practical in frame): a Bell lamp on the
                  # side table in frame and the candle brighter; the hidden fill out; the speaker's back light up; the
                  # screen lower and warm; the records in pools
                  'settings': {'spk_irr': 12.0, 'spk_spread': 90.0, 'spk_k': 2900, 'spk_back': 34.0, 'sconce_w': 20.0,
                               'exposure': -0.2, 'wb': 3000, 'spot_records': 6.0, 'rec_cone': 12.0, 'rec_aim_z': 1.2,
                               'record_glow': 0.25, 'console_lift': 0.55, 'chair_dye': '#2B2119', 'screen_lounge': 0.08,
                               'screen_tint': '#FFA060', 'flame': 80.0, 'candle_w': 6.0, 'haze': 0.02, 'spk_link': True,
                               'extra_bells': [[LP.LISTEN_TABLE[0] + 0.08, LP.LISTEN_TABLE[1] + 0.10, 0.495]],
                               'bell_w': 18.0}},
    'street': {'title': 'the shopfront window at night, from the kerb',
               # after the two critics on p6 (4.5, 4.5): 35 mm from the kerb, the dancer's lightbox on the left edge and
               # the right-hand Ember speaker seen over the lounge chairs, clear of the bar; the name frosted glass again;
               # the lightbox lower and warm; less haze; a cooler balance; the shelf edges down
               # after the two critics on p7 (5.0, 4.5): the speaker a sliver: the camera 0.5 m right and turned left,
               # the speaker lit harder; the name acid etch (a translucent film), not rough transmission; the haze less;
               # the street lamps 2700 K; the pendants' lamps down, their tubes up; the shelf edges down; the lightbox up
               'camera': {'position': [-3.0, 2.5, 1.6], 'target': [6.85, 5.1, 1.55], 'lens_mm': 35, 'level': True,
                          'fstop': 5.6, 'focus': [0.0, 3.4, 1.6]},
               'settings': {'exposure': 1.7, 'wb': 3200, 'wet': True, 'road_rough': 0.12, 'street_lamp': 120.0,
                            'screen_glow': 0.4, 'screen_window': 0.35, 'screen_tint': '#FFA060', 'spot_niche': 120.0,
                            'spk_link': True, 'lamp_k': 2700, 'lamp_z': 5.0, 'lamp_dx': 0.0, 'lamp_cam': 150.0,
                            'lamp_cam_z': 4.0, 'lamp_cam_y': 2.0, 'sign_w': 0.0, 'entry_w': 15.0, 'entry_cone': 100.0,
                            'transom_glow': 0.15, 'spk_irr': 40.0, 'spk_back': 45.0, 'spk_spread': 90.0,
                            'pendant_w': 90.0, 'pendant_glow': 0.25, 'pendant_lamp': 0.8, 'inlay_glow': 0.6,
                            'haze': 0.004, 'shelf_glow': 0.2, 'siding': '#8E9384', 'sky': 0.03, 'sky_zenith': '#1A2440',
                            'sky_horizon': '#2A3550', 'flat_glow': 0.06, 'across_glow': 0.05, 'linen_trans': 0.5,
                            'etch_glow': 0.03, 'glass_gloss': 3.0, 'chair_dye': '#2B2119'}},
}
S.VIEWS = VIEWS
_shot = S.shot


def shot(view):
    s = _shot(view)
    s['title'] = s['title'].replace('(round 33)', '(round 34)')
    return s


S.shot = shot


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--final']
    S.write(args or None, final='--final' in sys.argv)
