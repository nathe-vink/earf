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
    sconce_w=6.0, pendant_w=60.0, pendant_cone=50.0, shelf_glow=4.0, shade_glow=0.4, niche_glow=0.6, pendant_glow=0.35,
    pendant_lamp=4.0, screen_glow=0.8, inlay_glow=0.6, etch_glow=0.05, spot_records=9.0, record_glow=1.0,
    rug_tex='poly_wool_herringbone', rug_tint='#4A4541', rug_mix=0.7, rug_value=0.9, haze=0.008,
    wb=3300, exposure=0.0))
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
            'camera': {'position': [7.5, 3.6, 1.40], 'target': [9.06, 5.9, 1.25], 'lens_mm': 50, 'level': True,
                       'fstop': 2.8, 'focus': [LP.NICHES[1][0] + LP.NICHES[1][1] / 2, LP.BACKBAR_Y + 0.05, 1.3]},
            'settings': {'exposure': 0.6, 'spot_niche': 300.0, 'niche_cone': 40.0, 'niche_dy': 0.30, 'niche_aim_z': 0.9,
                         'niche_fill': 10.0}},
    'listening': {'title': 'the listening room, one of the Ember pair',
                  'camera': {'position': [14.6, 2.0, 0.95], 'target': [16.3, 4.5, 0.75], 'lens_mm': 35, 'level': True,
                             'fstop': 2.8, 'focus': [16.15, LP.PAIR['y'][1], 0.9]},
                  'settings': {'spk_irr': 20.0, 'spk_spread': 30.0, 'spk_k': 3000, 'spk_back': 6.0, 'sconce_w': 4.0,
                               'exposure': -0.3, 'spot_records': 4.0, 'rec_cone': 40.0, 'rec_aim_z': 1.2,
                               'record_glow': 0.3, 'console_lift': 0.55}},
    'street': {'title': 'the shopfront at night, from across the street',
               # three-quarter from up the street on the bar's side, the dancer's lightbox in the window, the Edwardian
               # bay over the shop
               'camera': {'position': [-9.5, 7.5, 1.6], 'target': [0.0, 3.2, 2.2], 'lens_mm': 35, 'level': True,
                          'fstop': 4.0, 'focus': [-0.09, 4.0, 1.8]},
               'settings': {'exposure': 0.9, 'wb': 3300, 'wet': True, 'road_rough': 0.12, 'street_lamp': 150.0,
                            'lamp_k': 3500, 'lamp_dx': 0.0, 'lamp_cam': 200.0, 'sign_w': 0.0, 'entry_w': 30.0,
                            'entry_cone': 100.0, 'transom_glow': 0.4, 'spk_irr': 12.0, 'pendant_w': 90.0,
                            'haze': 0.02, 'siding': '#8E9384', 'sky': 0.05, 'sky_zenith': '#1A2440',
                            'sky_horizon': '#2A3550', 'flat_glow': 0.12, 'across_glow': 0.06, 'linen_trans': 0.5,
                            'etch_glow': 0.15, 'screen_window': 1.4}},
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
