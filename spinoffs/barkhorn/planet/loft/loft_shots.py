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
    rug_tex='poly_wool_herringbone', rug_tint='#4A4541', rug_mix=0.7, rug_value=0.9, haze=0.008,
    wb=3300, exposure=0.0,
    # AgX, measured against Khronos PBR Neutral on the bar frame (README): crush 0.07 % vs 0.98, no clipping vs 0.3 %,
    # median 27.9 vs 19.4, whites warm-white not orange (b 19 vs 2)
    view='AgX'))
S.DEFAULT = DEFAULT
LOFT_KEYS = ('screen_glow', 'screen_banquette-a', 'screen_banquette-b', 'screen_lounge', 'screen_window', 'inlay_glow',
             'pendant_lamp', 'concrete_tint', 'concrete_mix', 'concrete_tex', 'floor_acg', 'floor_tint', 'floor_mix',
             'floor_coat', 'etch_glow', 'shade_glow', 'niche_glow')
_room_piece = S.room_piece


def room_piece(v):
    out = _room_piece(v)
    out['module'] = 'planet_loft'
    out.update({k: v[k] for k in LOFT_KEYS if k in v})
    return out


S.room_piece = room_piece

VIEWS = {
    'bar': {'title': 'the bar from a stool, close',
            # the den's close corner (the lead's): from a stool at 65 mm, one of the Fog pair in its niche, a frosted
            # pendant over the counter, a glass near
            # (the lead) wider, the frame shifted up so a fir beam and the steel cornice read over the niche
            # after bar-r2 (4.0): a step closer and higher on 35 mm, the niche's speaker larger, a beam still in
            'camera': {'position': [7.6, 3.3, 1.55], 'target': [9.06, 5.9, 1.75], 'lens_mm': 35, 'level': True,
                       'fstop': 4.0, 'focus': [LP.NICHES[1][0] + LP.NICHES[1][1] / 2, LP.BACKBAR_Y + 0.05, 1.3]},
            # after bar-r1 (4.5): the shelf edges warm and lower (kit), the niche softer and graded, its spots grazing;
            # the pendants pooling on the fir; brighter; haze; the near glass in focus at f/4
            'settings': {'exposure': 1.45, 'niche_glow': 0.12, 'spot_niche': 220.0, 'niche_cone': 20.0, 'niche_dy': 0.32,
                         'niche_aim_z': 1.2, 'niche_fill': 6.0, 'pendant_w': 180.0, 'pendant_cone': 24.0, 'haze': 0.02,
                         'concrete_tint': '#A0998F', 'concrete_mix': 0.3}},
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
                               'flame': 60.0, 'candle_w': 1.5, 'haze': 0.02}},
    'street': {'title': 'the shopfront at night, from across the street',
               # after street-r2 (4.5): from the far curb, level and shifted up so the Edwardian bay is in, the right
               # Ember speaker in clear glass beside the name; 1.2 stops brighter, the street lamps up and one low
               # behind the camera grazing the pavement and riser; the lightbox, the name, the pendants and the Ember
               # lamp scaled back for the exposure; more haze; focused 2 m inside
               'camera': {'position': [-9.0, 3.0, 1.6], 'target': [0.0, 3.2, 2.9], 'lens_mm': 35, 'level': True,
                          'fstop': 5.6, 'focus': [2.0, 3.0, 1.5]},
               'settings': {'exposure': 2.1, 'wb': 3300, 'wet': True, 'road_rough': 0.12, 'street_lamp': 260.0,
                            'lamp_k': 3400, 'lamp_z': 6.0, 'lamp_dx': 0.0, 'lamp_cam': 200.0, 'lamp_cam_z': 4.0,
                            'lamp_cam_y': 2.0, 'sign_w': 0.0, 'entry_w': 15.0, 'entry_cone': 100.0,
                            'transom_glow': 0.15, 'spk_irr': 10.0, 'pendant_w': 90.0, 'pendant_glow': 0.4,
                            'inlay_glow': 0.6, 'haze': 0.035, 'siding': '#8E9384', 'sky': 0.03,
                            'sky_zenith': '#1A2440', 'sky_horizon': '#2A3550', 'flat_glow': 0.06,
                            'across_glow': 0.05, 'linen_trans': 0.5, 'etch_glow': 0.25, 'screen_window': 0.24}},
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
