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

# the room (m; the speaker at the origin, facing -y). Gate 1 (the coordinator, 00:44, HOLD 3/3) moved the pendant onto
# the speaker's centre line between it and the wall, so the brightest wall is seen through the horn and the cabinet;
# a slim side table to the speaker's left with the Core on it; a rug edge and a sofa arm at the frame's left
SIDE = (-0.70, -0.10)            # the side table's centre (0.40 square top, 0.62 high: the Core picture's table height)
HEMI = (0.0, 0.50)               # where the Hemisphere hangs: on the speaker's centre line, 0.28 off the wall
HEMI_DZ = 0.13                   # its rim 1.45 up, its cord cut to the ceiling: the wash's bright core behind the cabinet
ROOM = {'x0': -2.6, 'x1': 2.2, 'y_back': 0.78, 'y_front': -6.2, 'height': 2.40}
# the formats (the coordinator's spec, r46-owner-notes 65ec7c5f: night-picture-spec-2026-11-04.md). The speaker with
# its lamp inside the box; the text zones dark; light pools inside the speaker's column. The camera level at the
# middle of speaker-plus-shade (0 to about 1.55 m), its distance set so that height fills the box's height
FORMATS = {
    'wide': {'size': [3840, 2160], 'lens_mm': 35.0, 'box_h': 0.54, 'dz': -0.05},
    'tall': {'size': [1440, 2560], 'lens_mm': 35.0, 'box_h': 0.31, 'dz': -0.02},
}
LAMP_TOP = 1.56                  # the Hemisphere's crown with its rim at 1.45: the top of 'the speaker with its lamp'
ROTATE = 10.0                    # the speaker turned toward the camera, off the wall's grazing reflection in its side


def _slim_table(cx, cy, top=0.62, w=0.40, t=0.018, leg=0.022, col='#5E5850'):
    # a slim side table: a thin top on four slender legs (grey oak), not a block
    parts = [{'name': 'side-table-top', 'center': [cx, cy, top - t / 2], 'size': [w, w, t], 'color': col, 'rough': 0.55}]
    o = w / 2 - 0.03
    for i, (dx, dy) in enumerate(((-o, -o), (o, -o), (o, o), (-o, o))):
        parts.append({'name': f'side-table-leg{i}', 'center': [cx + dx, cy + dy, (top - t) / 2], 'size': [leg, leg, top - t],
                      'color': col, 'rough': 0.55})
    return parts


def _camera(fmt, az_deg=7.0, cam_z=0.40):
    import math
    F = FORMATS[fmt]; W, H = F['size']
    # the engine's sensor is 36 mm across the frame's width (sensor_fit HORIZONTAL)
    sensor_h = 36.0 * H / W
    frame_h = LAMP_TOP / F['box_h']                       # metres the frame spans at the speaker
    d = frame_h * F['lens_mm'] / sensor_h
    zc = LAMP_TOP / 2 - 0.01 + F.get('dz', 0.0)       # a little lower, so speaker and shade sit inside the box
    # the camera low (0.40 m) and level, the frame raised by lens shift to the speaker-plus-shade's middle: the wall's
    # foot then sits above the lower text zones, and the cabinet's verticals stay vertical
    shift_y = F['lens_mm'] * (zc - cam_z) / d / 36.0
    a = math.radians(az_deg)
    return {'position': [round(d * math.sin(a), 3), round(-d * math.cos(a), 3), cam_z], 'target': [0.0, 0.0, cam_z],
            'lens_mm': F['lens_mm'], 'level': True, 'shift_y': round(shift_y, 4), 'fstop': 5.6, 'focus': [0.0, -0.20, 0.65]}


def shot(root, tint, lamp_dir, fmt='wide', core=False):
    s = json.load(open(os.path.join(root, BASE)))
    fl = FLAVOUR[tint]
    out = {k: copy.deepcopy(s[k]) for k in ('products', 'materials', 'finish')}
    for b in out['products']:
        b['flavour'] = fl
        for i in b['instances']:
            i['flavour'] = fl
            i['rotate_z'] = ROTATE
    out['title'] = f'Tropos {tint.capitalize()}, base A on its feet, polished horn A: night, lit by EARF lamps only'
    out['size'] = FORMATS[fmt]['size']
    out['camera'] = _camera(fmt)
    out['sky'] = {'kind': 'none'}
    out['lights'] = {}
    out['set'] = {'kind': 'sweep', 'night': {
        'room': ROOM,
        # gate 1: a neutral room, so Ice is the only colour: an off-white wall and ceiling, a grey oak floor
        'wall_plain': True, 'wall': '#D6D4CF', 'ceiling': '#E4E2DE',
        # (the formats: a dark oak, so the pendant's pool falls under the text zones' limit outside the column)
        'floor_plain': True, 'floor': '#3F3B36', 'floor_rough': 0.6,
        'skirting': {'height': 0.15, 'color': '#2A2826'},
        # ruling 4: a real window in the left wall, out of frame, a sheer curtain in it and the evening sky outside;
        # gate 1: dimmer and near-neutral, so the room is not tinted Ice's blue
        'opening': {'y0': -2.2, 'y1': -1.0, 'z0': 0.75, 'z1': 2.15, 'sky_color': '#C2C2BF', 'sky_strength': 1.0,
                    'curtain': True, 'curtain_open': 0.15},
        # gate 1: a living room. A slim side table (the cube read as a second speaker), a rug's edge, a sofa's arm
        # gate 1: a living room (a slim side table, a rug's edge, a sofa's arm) when the Core is in; the singles'
        # formats keep the speaker's surroundings dark (the text zones), so for them the Core and its table are out
        'furniture': (_slim_table(SIDE[0], SIDE[1]) + [
            {'name': 'rug', 'center': [-0.35, -0.95, 0.006], 'size': [3.2, 1.9, 0.012], 'color': '#8E8981', 'rough': 0.95},
            {'name': 'sofa-arm', 'center': [-1.62, -1.05, 0.33], 'size': [0.26, 1.0, 0.66], 'color': '#9A958C', 'rough': 0.9},
            {'name': 'sofa-seat', 'center': [-2.05, -1.05, 0.22], 'size': [0.62, 1.0, 0.44], 'color': '#9A958C', 'rough': 0.9}])
                     if core else [],
        'lamps': ([
            # the Core on the side table: the lamps lane's honest Core at 26400e7c, its opal core the emitter (their
            # 'nested' build, Core B; the coordinator, 00:44: a real light, a pool, a halo, a little on the cabinet)
            {'blend': os.path.join(lamp_dir, 'v4-core-fog-night-nested.blend'), 'offset': [SIDE[0], SIDE[1], 0.0], 'keep_table': False},
        ] if core else []) + [
            # the Hemisphere on the speaker's centre line between it and the wall, 0.35 higher than in its own picture so
            # (its rim 1.45 up, its cord cut to reach the ceiling): the wall behind the horn and the cabinet the brightest
            {'blend': os.path.join(lamp_dir, 'v4-hemi-fog-night.blend'), 'offset': [HEMI[0], HEMI[1], HEMI_DZ], 'keep_table': False,
             'cord_to_ceiling': True},
        ]}}
    out['render'] = dict(s['render'])
    # gate 1: a gentler view (the medium-high look clipped Ice's red to 0), white balance 4300 K, so the 3300 K lamps read a neutral warm white
    out['render'].update({'samples': 256, 'view': 'AgX', 'look': 'AgX - Base Contrast', 'exposure': 0.6,
                          'white_balance_k': 4300, 'white_balance_tint': 0.0,
                          # the Core's light reaches the room through its own ball, the Hemisphere's through its liner:
                          # refractive caustic paths, as the lamps lane renders them
                          'caustics_refractive': True})
    return out


if __name__ == '__main__':
    root, tint, lamp_dir, path = sys.argv[1:5]
    fmt = sys.argv[5] if len(sys.argv) > 5 else 'wide'
    json.dump(shot(root, tint, lamp_dir, fmt, core='--core' in sys.argv), open(path, 'w'), indent=1)
    print(path)
