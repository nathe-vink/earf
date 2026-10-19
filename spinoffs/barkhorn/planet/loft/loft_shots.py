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
S.BELL_TABLES = ()                                                  # no Bell (the loft's own lamps)
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
             'tlamp_bulb', 'etch_frost', 'etch_col', 'screen_gap', 'screen_rough')
_room_piece = S.room_piece


def room_piece(v):
    out = _room_piece(v)
    out['module'] = 'planet_loft'
    out.update({k: v[k] for k in LOFT_KEYS if k in v})
    return out


S.room_piece = room_piece


def lamp_spots(v):
    """The table lamps: one at the wall end of each booth's table, the window table, the lounge's side tables, any
    extra."""
    T = LP.TABLE
    out = [[round(cx + 0.15, 4), round(LP.BOOTH['table_y0'] + 0.24, 4), T['h']] for cx in LP.BOOTHS_X]   # each booth
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
_props = S.props


def props(v):
    """The den's props without its scanned bar stools and its banquette's chairs: the kit builds the booths and the
    stools and chairs after Fyrn (the owner, 2026-10-19)."""
    return [o for o in _props(v) if o.get('model') not in ('bar_chair_round_01', v.get('chair_model', 'dining_chair_02'))]


S.props = props
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
            # the owner's seating (booths, stools after Fyrn) from p8. After the two critics on p9 (4.5, 4.5): the
            # speaker a small red smudge: closer, by the stools on 40 mm, aimed at it, and lit harder; the screen out-
            # shone it, cool: dimmer and warm; the shelf edges and the inlay read as LED strips and phone screens: down;
            # the near booth crushed: its lamp up; the pendants clipped: their lamps down
            'camera': {'position': [5.5, 2.5, 1.30], 'target': [16.15, 4.6, 0.95], 'lens_mm': 40, 'level': True,
                       'fstop': 4.0, 'focus': [16.15, 4.85, 0.8]},
            'settings': {'exposure': 1.0, 'wb': 3000, 'shelf_glow': 0.35, 'niche_glow': 0.3, 'spot_niche': 400.0,
                         'niche_cone': 30.0, 'niche_dy': 0.32, 'niche_aim_z': 1.2, 'pendant_w': 700.0,
                         'pendant_cone': 40.0, 'pendant_glow': 0.15, 'pendant_lamp': 1.5, 'shade_glow': 0.6,
                         'inlay_glow': 1.0, 'haze': 0.015, 'screen_glow': 0.2, 'screen_tint': '#FFA060',
                         'screen_gap': 0.04, 'screen_rough': 0.22, 'bell_w': 200.0, 'sconce_w': 25.0,
                         'spot_records': 6.0, 'rec_cone': 40.0, 'record_glow': 0.3, 'candle_w': 2.4, 'tlamp_glow': 0.2,
                         'spk_irr': 50.0, 'spk_back': 90.0, 'spk_spread': 90.0, 'spk_link': True,
                         'chair_dye': '#4A3A32',
                         'chair_move': {'1': [0.0, -0.25, 0.0], '4': [0.0, 0.30, 0.0], '6': [0.30, 0.25, 0.0]}}},
    'listening': {'title': 'the listening room, one of the Ember pair',
                  # p6's frame again (5.25 at proof size, 5.5 at 1200 x 800: the best yet), with only the changes its four
                  # critics shared. p7 and p8 (back and lower on 24 mm, a Bell lamp in frame: 4.5, 4.5) put the side table
                  # across the speaker; the listener's-seat concept (p9c, p9d, composition checks) lost both speakers
                  # behind the chairs. Shared: the screen well below the speaker (81 vs 39), the speaker lit harder, a
                  # stop darker, less orange, the records in pools, the sconce up, more haze, the base and a beam in
                  'camera': {'position': [14.6, 2.5, 1.2], 'target': [16.3, 4.6, 1.15], 'lens_mm': 26, 'level': True,
                             'fstop': 2.8, 'focus': [16.15, LP.PAIR['y'][1], 0.9]},
                  'settings': {'spk_irr': 12.0, 'spk_spread': 90.0, 'spk_k': 2900, 'spk_back': 20.0, 'sconce_w': 25.0,
                               'exposure': 0.0, 'wb': 3100, 'spot_records': 20.0, 'rec_cone': 18.0, 'rec_aim_z': 1.2,
                               'fill_w': 40.0, 'fill_pos': [14.6, 3.2, 3.0], 'fill_target': [15.2, 3.4, 0.0],
                               'record_glow': 0.1, 'console_lift': 0.55, 'chair_dye': '#4A3A32', 'screen_lounge': 0.12,
                               'screen_tint': '#FFA060', 'flame': 60.0, 'candle_w': 1.5, 'haze': 0.025, 'spk_link': True}},
    'street': {'title': 'the shopfront window at night, from the kerb',
               # p7's light (4.75, the best street) with the review's lifted sources (pendants, lamps, records, candles
               # x3.6, the sconce x4.8, the entry x3, the niches x2.4, the speaker x2.4, the shelf edges x0.5), p10's
               # camera, the name acid etch; and the speaker in frame (the lead: present and lit in every frame): the
               # two lounge chairs on the sightline to the left Ember speaker moved aside, as a stylist would
               # (p11: the bar's far end hides the left Ember speaker from any kerb position that keeps the lightbox;
               # now the right-hand one, down the aisle through the lounge's opening, its two chairs moved aside)
               'camera': {'position': [-3.0, 3.6, 1.6], 'target': [6.85, 4.4, 1.5], 'lens_mm': 35, 'level': True,
                          'fstop': 5.6, 'focus': [0.0, 3.4, 1.6]},
               'settings': {'exposure': 1.7, 'wb': 3200, 'wet': True, 'road_rough': 0.12, 'street_lamp': 120.0,
                            'screen_glow': 0.4, 'screen_window': 0.22, 'screen_tint': '#FFA060', 'spot_niche': 288.0,
                            'spk_link': True, 'lamp_k': 3000, 'lamp_z': 5.0, 'lamp_dx': 0.0, 'lamp_cam': 90.0,
                            'lamp_cam_z': 4.0, 'lamp_cam_y': 2.0, 'sign_w': 0.0, 'entry_w': 45.0, 'entry_cone': 100.0,
                            'transom_glow': 0.15, 'spk_irr': 43.0, 'spk_back': 72.0, 'spk_spread': 90.0,
                            'pendant_w': 324.0, 'pendant_glow': 0.32, 'pendant_lamp': 1.6, 'inlay_glow': 1.08,
                            'bell_w': 79.0, 'sconce_w': 29.0, 'spot_records': 32.0, 'candle_w': 2.2, 'tlamp_glow': 0.14,
                            'tlamp_bulb': 1.0, 'haze': 0.01, 'shelf_glow': 0.25, 'siding': '#8E9384', 'sky': 0.03,
                            'sky_zenith': '#1A2440', 'sky_horizon': '#2A3550', 'flat_glow': 0.06, 'across_glow': 0.05,
                            'linen_trans': 0.5, 'etch_glow': 0.03, 'glass_gloss': 3.0, 'chair_dye': '#2B2119',
                            'screen_gap': 0.06, 'screen_rough': 0.3,
                            'chair_move': {'2': [0.0, -0.5, 0.0], '5': [-0.5, -0.35, 0.0]}}},
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
