"""Writes a night picture's shot file for night_room.py (the coordinator, 2026-11-03 23:04).

    python3 spinoffs/barkhorn/night-pictures/make_shot.py ENGINE_ROOT TINT LAMP_DIR OUT.json [--wall]

The speaker block, its materials (the polished horn, the base's lights off) and its render finish come from the
speaker lane's honest gate-2 shot (renders/2026-11-03/barkhorn/base-question/gate2/A-ice-polished-honest.shot.json),
with the flavour swapped for TINT. Its studio is dropped: no lamps (`lights: {}`), a black sky, and the set becomes
the evening room (night_room.night_set), lit by EARF's Core on the side table and a Hemisphere pendant over it, both in
Fog (clear) so the speaker's colour is the only colour, plus a dim evening window behind a curtain.
"""
import copy
import json
import os
import sys

FLAVOUR = {'ember': 'cloud-red', 'dust': 'cloud-orange', 'acid': 'cloud-amber', 'poison': 'eucalyptus-y2k-green',
           'ice': 'cloud-blue', 'haze': 'cloud-violet', 'fog': 'birch-fog-clear', 'smoke': 'cloud-black'}
BASE = 'renders/2026-11-03/barkhorn/base-question/gate2/A-ice-polished-honest.shot.json'

# the room (m; the speaker at the origin, facing -y). A side table to the speaker's left (camera's left) with the Core
# on it and the Hemisphere hung over it; the window on the left wall, behind a curtain
SIDE = (-0.68, -0.12)            # the side table's centre (0.42 square, its top at 0.62, the Core picture's table height)
HEMI = (0.08, 0.40)              # where the Hemisphere hangs
ROOM = {'x0': -2.6, 'x1': 2.2, 'y_back': 0.78, 'y_front': -4.2, 'height': 2.40}


def shot(root, tint, lamp_dir):
    s = json.load(open(os.path.join(root, BASE)))
    fl = FLAVOUR[tint]
    out = {k: copy.deepcopy(s[k]) for k in ('products', 'materials', 'finish')}
    for b in out['products']:
        b['flavour'] = fl
        for i in b['instances']:
            i['flavour'] = fl
    out['title'] = f'Tropos {tint.capitalize()}, base A on its feet, polished horn A: night, lit by EARF lamps only'
    out['size'] = [1800, 1200]
    out['camera'] = {'position': [0.62, -3.20, 0.98], 'target': [-0.20, 0.10, 0.70], 'lens_mm': 35.0, 'level': True,
                     'fstop': 4.0, 'focus': [0.0, -0.22, 0.65]}
    out['sky'] = {'kind': 'none'}
    out['lights'] = {}
    out['set'] = {'kind': 'sweep', 'night': {
        'room': ROOM,
        'floor_pbr': 'american_walnut_veneer', 'floor_rough_mul': 0.9,
        # the lamps lane's dusk curtain, at its own colour and strength (lamp_pictures.py, round 12)
        # ruling 4: a real window in the left wall, out of frame, a sheer curtain in it and the evening sky outside
        'opening': {'y0': -2.2, 'y1': -1.0, 'z0': 0.75, 'z1': 2.15, 'sky_color': '#9FB2D6', 'sky_strength': 6.0,
                    'curtain': True, 'curtain_open': 0.15},
        # a small side table behind the speaker's left (camera's left), its top at the Core picture's table height
        'furniture': [{'name': 'side-table', 'center': [SIDE[0], SIDE[1], 0.31], 'size': [0.42, 0.42, 0.62],
                       'color': '#2A211B', 'rough': 0.35}],
        'lamps': [
            # the Core on the side table, behind the speaker's left: its light comes through the tinted cabinet
            {'blend': os.path.join(lamp_dir, 'core-fog-night.blend'), 'offset': [SIDE[0], SIDE[1], 0.0], 'keep_table': False,
             'led_up': True},
            # the Hemisphere hung behind the speaker's right, 0.35 higher than in its own picture so its cord meets the
            # ceiling (its rim 1.67 up): a pool on the floor behind and a wash on the wall the cabinet stands against
            {'blend': os.path.join(lamp_dir, 'hemi-fog-night.blend'), 'offset': [HEMI[0], HEMI[1], 0.35], 'keep_table': False},
        ]}}
    out['render'] = dict(s['render'])
    out['render'].update({'samples': 256, 'view': 'AgX', 'look': 'AgX - Medium High Contrast', 'exposure': 2.2,
                          'white_balance_k': 3800, 'white_balance_tint': 0.0,
                          # the Core's light reaches the room through its own ball, the Hemisphere's through its liner:
                          # refractive caustic paths, as the lamps lane renders them
                          'caustics_refractive': True})
    return out


if __name__ == '__main__':
    root, tint, lamp_dir, path = sys.argv[1:5]
    json.dump(shot(root, tint, lamp_dir), open(path, 'w'), indent=1)
    print(path)
