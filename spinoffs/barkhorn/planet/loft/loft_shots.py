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
             'floor_coat', 'etch_glow', 'shade_glow', 'niche_glow', 'menu_color')
_room_piece = S.room_piece


def room_piece(v):
    out = _room_piece(v)
    out['module'] = 'planet_loft'
    out.update({k: v[k] for k in LOFT_KEYS if k in v})
    return out


S.room_piece = room_piece

VIEWS = {
    'bar': {'title': 'the bar, down the room',
            # concept changed after three passes at 4.0 to 4.5 on the close corner (bar-r1 to r3; two critics: a Fog-only
            # frame cannot carry the room's one colour): from the window table down the room's length, the bar and the
            # back-bar on the left, the banquette's frosted screens on the right, the pendants, and an Ember speaker
            # glowing at the far end through the smoked partition
            # after bar-r4 (5.5): 35 mm, the sightline past the chairs to the left Ember speaker; the alcove, the records
            # and the screens calmer; warmer balance; the pendants pooling on the bar, their tubes dim; less haze
            'camera': {'position': [1.6, 2.0, 1.45], 'target': [17.0, 3.9, 1.0], 'lens_mm': 35, 'level': True,
                       'fstop': 5.6, 'focus': [7.0, 3.3, 1.2]},
            'settings': {'exposure': 1.0, 'wb': 2900, 'shelf_glow': 0.35, 'niche_glow': 0.12, 'spot_niche': 160.0,
                         'niche_cone': 30.0, 'niche_dy': 0.32, 'niche_aim_z': 1.2, 'pendant_w': 180.0,
                         'pendant_cone': 24.0, 'pendant_glow': 0.06, 'haze': 0.008, 'screen_glow': 0.2,
                         'spk_irr': 9.0, 'spk_back': 18.0, 'spk_spread': 90.0, 'spk_link': True,
                         'spot_records': 5.0, 'rec_cone': 40.0, 'chair_dye': '#4A3A32'}},
    'listening': {'title': 'the listening room, one of the Ember pair',
                  # after listening-r1 (5.5): 28 mm from a little back and higher, the beams in, the speaker on the left third
                  # (p2: from 14.3, 1.8 a lounge chair filled the foreground) clear of the chairs
                  'camera': {'position': [14.75, 2.6, 1.15], 'target': [16.3, 4.6, 1.2], 'lens_mm': 28, 'level': True,
                             'fstop': 2.8, 'focus': [16.15, LP.PAIR['y'][1], 0.9]},
                  # listening-r1: the speaker's front lamp soft and low, the light mostly from behind through the acrylic;
                  # the chairs espresso; the record wall up; warmer and lower overall
                  # after listening-r2 (5.5): a stop darker, the screen dimmed below the speaker, the speaker lit three
                  # times harder from front and behind, the candle up, the records lower and grazed, haze
                  'settings': {'spk_irr': 18.0, 'spk_spread': 90.0, 'spk_k': 2900, 'spk_back': 36.0, 'sconce_w': 4.0,
                               'exposure': -1.5, 'wb': 3800, 'spot_records': 8.0, 'rec_cone': 25.0, 'rec_aim_z': 1.2,
                               'record_glow': 0.4, 'console_lift': 0.55, 'chair_dye': '#4A3A32', 'screen_lounge': 0.3,
                               'flame': 60.0, 'candle_w': 1.5, 'haze': 0.01,
                               # (p4: the tripled lamps flooded the corner, median 81 at -1.5) light-linked to the speaker
                               'spk_link': True}},
    'street': {'title': 'the shopfront window at night, from the kerb',
               # concept changed after three passes at 3.5 to 4.5 on the whole facade (street-r1 to r3): the lead's
               # fallback, tight on the lit window from the kerb at 50 mm: the dancer's lightbox, the frosted name, the
               # glass and its reflections, and through a clear pane the right-hand Ember speaker, the frame's one colour
               # after street-r4 (4.5): closer, lined up so the right-hand Ember speaker stands in a clear pane
               'camera': {'position': [-4.0, 2.6, 1.65], 'target': [0.0, 3.5, 1.65], 'lens_mm': 50, 'level': True,
                          'fstop': 5.6, 'focus': [-0.09, 3.6, 1.6]},
               'settings': {'exposure': 1.7, 'wb': 3700, 'wet': True, 'road_rough': 0.12, 'street_lamp': 120.0,
                            'screen_glow': 0.4, 'spot_niche': 120.0, 'spk_link': True,
                            'lamp_k': 3000, 'lamp_z': 5.0, 'lamp_dx': 0.0, 'lamp_cam': 60.0, 'lamp_cam_z': 4.0,
                            'lamp_cam_y': 2.0, 'sign_w': 0.0, 'entry_w': 15.0, 'entry_cone': 100.0,
                            'transom_glow': 0.15, 'spk_irr': 9.0, 'spk_back': 18.0, 'spk_spread': 90.0,
                            'pendant_w': 90.0, 'pendant_glow': 0.3, 'inlay_glow': 0.6, 'haze': 0.025,
                            'siding': '#8E9384', 'sky': 0.03, 'sky_zenith': '#1A2440', 'sky_horizon': '#2A3550',
                            'flat_glow': 0.06, 'across_glow': 0.05, 'linen_trans': 0.5, 'etch_glow': 0.0,
                            'screen_window': 0.35, 'glass_gloss': 3.0, 'chair_dye': '#4A3A32'}},
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
