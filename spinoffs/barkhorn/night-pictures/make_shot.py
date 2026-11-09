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
# gate 2 (the coordinator, 01:47: the centre-line pendant silhouetted the box and read as a dome on the horn): to the
# camera's side and in front of the speaker's face, so its light rakes the cabinet's front and top; higher, so lit wall
# separates its rim from the horn
HEMI = (0.22, -0.48)             # (gate 2's hang, kept for the record)
HEMI_DZ = 0.28
# gate 3 (the coordinator, 17:18, HOLD 0/3: a pendant 27 cm in front of the speaker over bare floor read as a disguised
# spotlight): over a nightstand 0.7 m to the camera's right and forward of the speaker's face, hung over it as a side
# pendant is (its rim 0.45 above the stand's top), so it has a reason to hang there and its light still reaches the
# speaker's face and the wall beside it (against the wall, g3b, it lit only the wall and the speaker's side)
STAND = (0.74, -0.55)            # the nightstand's centre (Poly Haven ClassicNightstand_01: 0.57 x 0.42 x 0.70)
HEMI3 = (0.68, -0.58)
HEMI3_DZ = -0.17                 # its rim 1.15 up, 0.45 over the stand's top (1.32 in its own picture)
# gate 3: the speaker's face needs a source on the camera's side (a 490 lm pendant beside it lights its side and the
# wall, not its face; the night window cannot honestly give 50 lux). A second Hemisphere, a reading pendant over the
# armchair at the front left, hung high, so its light reaches the speaker's face from the front left
CHAIR = (-1.95, 0.05)
HEMI_READ = (-0.95, -1.15)
HEMI_READ_DZ = 0.25              # its rim 1.57 up, over the chair's seat
READING = False                  # tried (g3c): a downlight lights the chair under it, not the speaker; left out
# gate 3, option A (the coordinator, 17:31): a low record console beside the speaker, its near end just forward of the
# speaker's face, and the pendant over that near end, 0.25 m off the speaker's side and 0.35 m in front of its face;
# the pool lands on the console's top. Poly Haven modern_wooden_cabinet (CC0), 2.44 x 0.52 x 0.68, a run of sleeves on it
CONSOLE = (1.72, -0.30)          # its centre: the near end at x 0.52 (0.24 off the speaker's side), its front at y -0.32
HEMI_A = (0.44, -0.36)           # proxy 7: 10 cm right of proxy 6 (horn crops: no horn pixel over L* 90)           # the pendant: over the console's near end, 0.35 in front of the speaker's face
HEMI_A_DZ = 0.15                 # proxy 6: its rim 1.47 up (0.15 over proxy 4), off the horn's top line in frame
# gate 2, point 6: the Hemisphere's mouth is open and its COB sits at the rim, so a camera below the rim sees the bare
# COB (scene_audit: 106 of 113 points from 0.40 m). The camera stands above the rim, at eye height
CAM_Z = 1.70
# proxy 6 (the coordinator, 18:48): the Hemisphere's drawn drop is 600 mm, its rim 776 below the ceiling; a 2.25 m
# ceiling puts the rim at 1.47 with that drop
ROOM = {'x0': -2.6, 'x1': 3.1, 'y_back': 0.78, 'y_front': -6.2, 'height': 2.25}
# the formats (the coordinator's spec, r46-owner-notes 65ec7c5f: night-picture-spec-2026-11-04.md). The speaker with
# its lamp inside the box; the text zones dark; light pools inside the speaker's column. The camera level at the
# middle of speaker-plus-shade (0 to about 1.55 m), its distance set so that height fills the box's height
FORMATS = {
    'wide': {'size': [3840, 2160], 'lens_mm': 35.0, 'box_h': 0.54, 'dz': -0.075},
    'tall': {'size': [1440, 2560], 'lens_mm': 35.0, 'box_h': 0.31, 'dz': -0.02},
}
LAMP_TOP = 1.72                  # (gate 2: the Hemisphere's crown with its rim at 1.60)
# gate 3: the pendant beside the speaker, so the box frames the speaker itself (1.28 tall) with headroom; the frame's
# top then falls below the ceiling (the warm ceiling stripe out)
FRAME_TOP = 1.36
ROTATE = 0.0                     # gate 3: the camera squared to the wall, the speaker square to it too (gate 1 had 10)


def _slim_table(cx, cy, top=0.62, w=0.40, t=0.018, leg=0.022, col='#5E5850'):
    # a slim side table: a thin top on four slender legs (grey oak), not a block
    parts = [{'name': 'side-table-top', 'center': [cx, cy, top - t / 2], 'size': [w, w, t], 'color': col, 'rough': 0.55}]
    o = w / 2 - 0.03
    for i, (dx, dy) in enumerate(((-o, -o), (o, -o), (o, o), (-o, o))):
        parts.append({'name': f'side-table-leg{i}', 'center': [cx + dx, cy + dy, (top - t) / 2], 'size': [leg, leg, top - t],
                      'color': col, 'rough': 0.55})
    return parts


def _records():
    # a run of LP sleeves standing on the console's top toward its far end (31.5 cm square, 4-5 mm thick, muted spines)
    # and a short stack by the pendant: generic boxes, no artwork
    top = 0.68; out = []
    cols = ('#2E2B28', '#4A3F36', '#1F2328', '#5B5249', '#2A2F2A', '#3C3430', '#6A6158', '#26221F')
    x = 2.20
    for i in range(16):
        out.append({'name': f'sleeve{i}', 'center': [x, -0.30, top + 0.1575], 'size': [0.005, 0.315, 0.315],
                    'color': cols[i % len(cols)], 'rough': 0.6})
        x += 0.0062
    for i in range(4):
        # proxy 8: the stack in dark sleeves (the critics: its pale top read as a slab at luma 154 under the lamp)
        out.append({'name': f'stack{i}', 'center': [0.80, -0.32, top + 0.0025 + 0.005 * i], 'size': [0.315, 0.315, 0.005],
                    'color': ('#1E1C1A', '#26221F', '#1F2328', '#2A2622')[i], 'rough': 0.7})
    return out


def _camera(fmt, az_deg=0.0, cam_z=None):     # gate 3: squared to the back wall (the skirting level)
    import math
    F = FORMATS[fmt]; W, H = F['size']
    cam_z = CAM_Z if cam_z is None else cam_z
    # the engine's sensor is 36 mm across the frame's width (sensor_fit HORIZONTAL)
    sensor_h = 36.0 * H / W
    frame_h = FRAME_TOP / F['box_h']                      # metres the frame spans at the speaker
    d = frame_h * F['lens_mm'] / sensor_h
    zc = FRAME_TOP / 2 - 0.01 + F.get('dz', 0.0)      # a little lower, so the speaker sits inside the box
    # the camera level at CAM_Z, the frame moved by lens shift to the speaker-plus-shade's middle (gate 1's wide proxy
    # had it at 0.40 m), so the cabinet's verticals stay vertical
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
        'ceiling': '#E4E2DE',
        # gate 2: a real room. Oak planks with a soft sheen (Poly Haven wood_floor, CC0, tinted toward a neutral dark
        # oak), the wall plaster (beige_wall_001 tinted toward off-white), a dark skirting
        'floor_pbr': 'wood_floor', 'floor_tint': '#2C2824', 'floor_tint_mix': 0.6, 'floor_rough_mul': 0.55,
        # gate 3: a plaster with relief the light can graze (beige_wall_002), toned toward a limewash off-white
        # proxy 7 (the skeptic, 19:54): the wall's paint deeper (a darker limewash, not less light), so the wall above
        # the speaker falls well below its lit batts
        'wall_pbr': 'beige_wall_002', 'wall_tint': '#D2CFC8', 'wall_tint_mix': 0.5, 'wall_value': 0.42,
        'skirting': {'height': 0.15, 'color': '#2A2826'},
        # ruling 4: a real window in the left wall, out of frame, a sheer curtain in it and the evening sky outside;
        # gate 1: dimmer and near-neutral, so the room is not tinted Ice's blue
        # gate 2: the curtain open, a soft cool fill on the speaker's face from the camera's side (a real opening; the
        # night sky on the lamps' scale: about 30 cd/m2 of blue-hour sky, 0.0065 W a lumen, so about 0.6)
        'opening': {'y0': -1.9, 'y1': -0.7, 'z0': 0.80, 'z1': 2.10, 'sky_color': '#AEB8C8', 'sky_strength': 0.6,
                    'curtain': True, 'curtain_open': 0.75},
        # gate 3: the window's cool light as a soft shape on a wall: a streetlight across the road, through the left
        # window's opening and its sheer; proxy 6: cut 1.3 stops (about 1.5 lux, 0.01 W/m2) and about 4000 K, so under the
        # 3000 K balance it reads a faint cool, not blue
        'outside_light': {'direction': [0.62, 0.62, -0.48], 'irradiance': 0.01, 'angle_deg': 3.0, 'color': '#FFCE9F'},
        # gate 1: a living room. A slim side table (the cube read as a second speaker), a rug's edge, a sofa's arm
        # gate 1: a living room (a slim side table, a rug's edge, a sofa's arm) when the Core is in; the singles'
        # formats keep the speaker's surroundings dark (the text zones), so for them the Core and its table are out
        'furniture': (_slim_table(SIDE[0], SIDE[1]) + [
            {'name': 'rug', 'center': [-0.35, -0.95, 0.006], 'size': [3.2, 1.9, 0.012], 'color': '#8E8981', 'rough': 0.95},
            {'name': 'sofa-arm', 'center': [-1.62, -1.05, 0.33], 'size': [0.26, 1.0, 0.66], 'color': '#9A958C', 'rough': 0.9},
            {'name': 'sofa-seat', 'center': [-2.05, -1.05, 0.22], 'size': [0.62, 1.0, 0.44], 'color': '#9A958C', 'rough': 0.9}])
                     if core else _records(),
        # gate 3: the speaker clearly on a wool rug (curly_teddy_natural, CC0: a pile, its own relief), a bound edge,
        # 0.9 m of rug in front of the feet; a nightstand under the pendant and an armchair in shadow at the left edge
        # proxy 8 (the coordinator, 20:49): 3.8 m wide, past the oak at the lower right and the wedge at the lower left
        'rug': None if core else {'pbr': 'curly_teddy_natural', 'tint': '#3A3836', 'tint_mix': 0.9, 'value': 0.014, 'bump': 1.0, 'matte': True, 'tile_m': 0.12,
                                  'center': [0.0, -1.10], 'size': [3.8, 3.30], 'border_w': 0.035, 'border_color': '#24211E'},
        'models': [] if core else [
            {'id': 'modern_wooden_cabinet', 'location': [CONSOLE[0], CONSOLE[1], 0.0], 'rotation_deg': [0, 0, 0], 'name': 'console'},
            {'id': 'ArmChair_01', 'location': [CHAIR[0], CHAIR[1], 0.0], 'rotation_deg': [0, 0, -70], 'name': 'armchair', 'value': 0.3}],
        'lamps': ([
            # the Core on the side table: the lamps lane's honest Core at 26400e7c, its opal core the emitter (their
            # 'nested' build, Core B; the coordinator, 00:44: a real light, a pool, a halo, a little on the cabinet)
            {'blend': os.path.join(lamp_dir, 'core-fog-night-nested.blend'), 'offset': [SIDE[0], SIDE[1], 0.0], 'keep_table': False},
        ] if core else []) + [
            # the Hemisphere on the speaker's centre line between it and the wall, 0.35 higher than in its own picture so
            # (its rim 1.45 up, its cord cut to reach the ceiling): the wall behind the horn and the cabinet the brightest
            {'blend': os.path.join(lamp_dir, 'hemi-fog-night.blend'), 'offset': [HEMI_A[0], HEMI_A[1], HEMI_A_DZ], 'keep_table': False,
             'cord_to_ceiling': True, 'canopy': os.path.join(lamp_dir, 'hemi-canopy.stl'),
             # the coordinator, 18:13: the Vero SE 10's real emitter, an 11 mm disk at the top of the bore
             'honest_cob': 0.011},
        ] + ([] if core or not READING else [
            {'blend': os.path.join(lamp_dir, 'hemi-fog-night.blend'), 'offset': [HEMI_READ[0], HEMI_READ[1], HEMI_READ_DZ],
             'keep_table': False, 'cord_to_ceiling': True, 'canopy': os.path.join(lamp_dir, 'hemi-canopy.stl')}])}}
    out['render'] = dict(s['render'])
    # gate 1: a gentler view (the medium-high look clipped Ice's red to 0), white balance 4300 K, so the 3300 K lamps read a neutral warm white
    # gate 2: the lamp as the lamps lane's file has it (COB 3.2 W, 2700 K), the brightness from exposure (+2 EV), white
    # balance 1000 K above the lamp as before (a neutral warm white); the finish's contrast eased (red off 0)
    out['finish']['contrast'] = 0.05
    # the coordinator, 18:13: more samples for the small source (the honest COB)
    out['render'].update({'samples': 512, 'view': 'AgX', 'look': 'AgX - Base Contrast', 'exposure': 4.3,
                          # gate 3: white balance near the 2700 K lamp, so Ice's batts keep their red (pale blue-white)
                          'white_balance_k': 3000, 'white_balance_tint': 0.0,
                          # the Core's light reaches the room through its own ball, the Hemisphere's through its liner:
                          # refractive caustic paths, as the lamps lane renders them
                          'caustics_refractive': True,
                          # the coordinator, 18:43 (the lamps lane's flux check, r32 5c319549): the floor lit by way of
                          # the polished reflector is a reflective caustic, and the indirect clamp capped the mirrored
                          # COB; both off, so the fitting puts out what it does (the COB stays at 3.2 W)
                          'caustics_reflective': True, 'clamp': 0.0})
    return out


if __name__ == '__main__':
    root, tint, lamp_dir, path = sys.argv[1:5]
    fmt = sys.argv[5] if len(sys.argv) > 5 else 'wide'
    json.dump(shot(root, tint, lamp_dir, fmt, core='--core' in sys.argv), open(path, 'w'), indent=1)
    print(path)
