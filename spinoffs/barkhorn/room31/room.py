"""Room 31: a pair of Poison at home, photographed as a design magazine would shoot it (the coordinator's brief,
2026-10-18; NOTES.md logs every pass).

    python3 spinoffs/barkhorn/room31/room.py            # writes studio/shots/barkhorn/room31/room.json, room-portrait.json
    python3 studio/engine/render.py studio/shots/barkhorn/room31/room.json --out IMG [--samples N --scale S]

One light idea: late-afternoon sun low through the tall glazing of the left wall, from in front of the pair, so it
crosses the floor, falls on both speakers alike, passes through their tinted acrylic and lays their green shadows on
the plaster behind; a sun-free window off to the right (out of frame) fills the shade side. The view out of the glazing
is a photographed place (an exterior plate the camera sees and the room is not lit by). The surfaces are photographed:
oak boards, plaster, a deep-pile wool rug, a scanned lounge chair; the credenza is walnut veneer, bookmatched, built
here (pieces.py); the record player is EARF's own, Cumulus, in Fog.

The frame is the engine's: metres, z up, the speakers' fronts toward -y, the back wall at y = BACK.
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'room31')
PIECES = os.path.relpath(os.path.join(HERE, 'pieces.py'), ROOT)

# --- the room ------------------------------------------------------------------------------------------------------
BACK = 0.95                      # the back wall's face (y)
LEFT = -2.05                     # the glazed left wall's face (x)
RIGHT = 3.75
DEPTH = 7.0
HEIGHT = 2.9
PX = 0.0
SPK_X, SPK_Y, TOE = 1.2, 0.30, 6.0          # the pair: centres at +-x, toe-in (deg)
CAB = dict(x=-0.0, w=1.62, d=0.44, h=0.56)  # the credenza (back to the wall)


def ext(fn, **k):
    return {'kind': 'kit', 'shape': 'ext', 'path': PIECES, 'fn': fn, **k}


def kit(shape, **k):
    return {'kind': 'kit', 'shape': shape, **k}


def _rot(p, deg):
    a = math.radians(deg); x, y = p
    return (x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a))


def lead(side, socket_x, socket_z=0.30):
    """A speaker's mains lead: out of its amp box (on its back, 419 mm up), down behind it to the floor, along the foot
    of the back wall and up into the plug at the socket. side -1 left, +1 right."""
    cx, toe = PX + side * SPK_X, -side * TOE
    def L(lx, ly, z):                                         # a point in the speaker's own frame -> world
        dx, dy = _rot((lx, ly), toe)
        return [round(cx + dx, 4), round(SPK_Y + dy, 4), z]
    yw = BACK - 0.012                                         # along the skirting's foot
    sx = socket_x
    pts = [[sx, BACK - 0.037, socket_z - 0.03], [sx, BACK - 0.04, socket_z - 0.09], [sx, yw - 0.004, 0.06],
           [sx, yw - 0.006, 0.0036]]
    run_to = cx + side * 0.06
    pts += [[round((sx + run_to) / 2, 4), yw - 0.008, 0.0036], [run_to, yw - 0.012, 0.0036],
            [cx, BACK - 0.12, 0.0036]]
    pts += [L(0.0, 0.33, 0.0036), L(0.0, 0.282, 0.06), L(0.0, 0.272, 0.26), L(0.0, 0.258, 0.40), L(0.0, 0.2097, 0.419)]
    return {'kind': 'cable', 'position': [0.0, 0.0], 'points': pts, 'd': 0.0075, 'plug': [0.05, 0.024], 'per': 10}


def room_set(v):
    w = RIGHT - LEFT; cx = (RIGHT + LEFT) / 2; cy = BACK - DEPTH / 2
    # the left wall runs front (y = BACK - DEPTH) to back; `along` is from its centre
    def along(y):
        return round(y - cy, 3)
    # a run of tall French windows down the left wall, piers between, glass to 15 cm under the ceiling
    wins = [{'wall': 'left', 'along': along(yc), 'sill': 0.04, 'size': [1.45, 2.71], 'mullions': m,
             'frame': v.get('frame', '#5A5650')}
            for yc, m in zip(v.get('win_y', (0.2, -1.4, -3.45)), v.get('win_mullions', ([1, 1], [2, 1], [2, 1])))]
    props = [
        ext('floor', rect=[LEFT, BACK - DEPTH, RIGHT, BACK], texture=v['floor'], res='4k', rotate_deg=v['floor_rot'],
            rough_mul=v.get('floor_rough', 1.0), coat=v.get('floor_coat', 0.35), coat_rough=0.35, value=v.get('floor_value', 1.0),
            offset=[0.37, 0.11, 0.0]),
        ext('plaster', texture=v['plaster'], res='4k', color=v['wall'], tint_mix=v.get('wall_tint', 0.85),
            value=v.get('wall_value', 1.0), bump=v.get('wall_bump', 1.0), tex_scale=v.get('wall_tex_scale')),
        ext('credenza', position=[PX + CAB['x'], BACK - CAB['d'] / 2 - 0.012], size=[CAB['w'], CAB['d'], CAB['h']], doors=v.get('doors', 3),
            texture=v.get('veneer', 'walnut_veneer'), lift=v.get('veneer_lift', 1.3), grain_rot=v.get('grain_rot', 90.0)),
        ext('rug', off=v.get('rug_off', False), position=v['rug_pos'], size=v['rug_size'], pile=v.get('rug_pile', 0.018), texture=v.get('rug', 'curly_teddy_natural'),
            tint=v.get('rug_tint', '#E4DCCB'), tint_mix=v.get('rug_tint_mix', 0.5), displace=v.get('rug_displace', 0.006), res=v.get('rug_res', '2k'), value=v.get('rug_value', 1.0),
            tex_scale=v.get('rug_tex_scale')),
        ext('socket', position=[PX - v['socket_x'], BACK, 0.30]),
        ext('socket', position=[PX + v['socket_x'], BACK, 0.30]),
        lead(-1, PX - v['socket_x']), lead(1, PX + v['socket_x']),
        ext('books', position=[PX + v.get('books_x', 0.35), BACK - 0.24, CAB['h']], seed=4, books=[
            # invented titles and imprints (no real books or publishers on a campaign prop)
            [0.31, 0.24, 0.032, '#3E4A57', '#D9D2C2', 'ROOMS IN LATE LIGHT', 'HALDEN'],
            [0.27, 0.21, 0.026, '#C9BBA2', '#3A332C', 'On Listening', 'NORTH PRESS'],
            [0.24, 0.19, 0.022, '#7A3A2C', '#E8DCC8', 'The Shape of Sound', 'ESSAYS'],
        ]),
        kit('asset', model=v.get('vase', 'ceramic_vase_02'), position=[PX + v.get('vase_x', 0.58), BACK - 0.20, CAB['h']], rotate=[0, 0, 20],
            scale=v.get('vase_scale', 1.0)),
        # the lounge chair, its black leather re-dyed cognac so it sits with the walnut and not against the pair
        ext('recolour', off=v.get('chair_off', False), model=v.get('chair', 'modern_arm_chair_01'), position=v['chair_pos'], rotate=[0, 0, v['chair_rot']],
            match=['pillow'], color=v.get('leather', '#7A4A2C'), blend='MIX', mix=v.get('leather_mix', 0.8)),
        # linen sheers drawn across the glazing (concept B): the sun through them becomes a broad soft source
        *[ext('sheer', position=[LEFT + 0.1, yc, HEIGHT - 0.05], rotate=[0, 0, 90], size=[w, HEIGHT - 0.07], folds=int(w * 9),
              amplitude=0.045, noise=0.35, seed=11 + i, res=140, open=(v.get('sheer_opens') or [v.get('sheer_open', 0.25)] * 9)[i], color='#F3EEE4')
          for i, (yc, w) in enumerate(v.get('sheers', []))],
        # a linen sheer, half drawn, at the back of the glazing: the sun comes through it
        kit('drape', off=v.get('drape_off', False), position=[LEFT + 0.09, BACK - 0.33, HEIGHT - 0.06], rotate=[0, 0, 90], size=[0.55, HEIGHT - 0.08],
            folds=9, amplitude=0.035, noise=0.35, thickness=0.0, material='organza', color='#F1ECE2',
            alpha=v.get('sheer_alpha', 0.55), seed=5, res=120),
        ext('exterior', hdri=v['hdri'], rotation_deg=v['hdri_rot'], strength=v['ext_strength'], res='8k',
            centre=[LEFT - 1.0, -1.0, 1.4], radius=60.0, blur=v.get('ext_blur', 0.004), tint=v.get('ext_tint')),
    ]
    return {'kind': 'room', 'size': [w, DEPTH, HEIGHT], 'center': [cx, cy],
            'floor': {'base': '#B89B78'}, 'wall': {'color': v['wall']}, 'ceiling': '#F2EFEA',
            'skirting': {'h': 0.09, 'color': v['wall'], 't': 0.014}, 'frame': v.get('frame', '#5A5650'), 'windows': wins, 'props': props}


DEFAULT = dict(
    floor='wood_floor', floor_coat=0.15, floor_rot=90.0, plaster='beige_wall_001', wall='#E8E2D8', wall_value=0.88, wall_bump=2.0,
    wall_tint=0.5, wall_tex_scale=1.6, socket_x=1.78,
    veneer='walnut_veneer_02', veneer_lift=0.75, grain_rot=90.0,
    rug='poly_wool_herringbone', rug_tex_scale=0.25, rug_tint='#8A7A64', rug_tint_mix=1.0, rug_pos=[0.45, -1.25],
    rug_size=[2.6, 1.6], rug_displace=0.004, rug_pile=0.016, rug_res='4k', rug_value=0.75,
    chair='modern_arm_chair_01', chair_pos=[-1.68, -0.5, 0.0], chair_rot=235.0, leather='#8A7460',
    hdri='autumn_forest_04', hdri_rot=100.0, ext_strength=4.0, ext_blur=0.0008, ext_tint='#FFE9D2',
    # concept C (pass r10): the window corner. The camera, still squared to the back wall, stands toward the glazing, so
    # the left wall recedes in the frame with its view out and the lounge chair by the glass; the pair, moved 0.35 m
    # clear of the window, stands in the low sun (az -76, el 11) through the open back bays; linen sheers over the
    # front bays soften the rest
    sheers=[(-0.66, 0.22), (-2.73, 2.95)], sheer_opens=[0.15, 0.35], drape_off=True, sheer_open=0.15, tt_x=0.0, books_x=-0.55, vase_x=0.62,
    sun=dict(azimuth_deg=-68.0, elevation_deg=14.0, irradiance=48.0, angle_deg=0.5, color='#FFE4C8'),
    sky_strength=1.0, fill=2.2, fill_color='#DCE4EE', fill_pos=[1.6, -3.6, 2.2], bounce=0.7, bounce_pos=[-0.6, -3.6, 1.35],
    bounce_size=[2.4, 1.2], floor_bounce=0.55, fb_pos=[0.0, -0.6, 0.08], rug_off=True, chair_off=True,
    exposure=-1.0, wb=5200, cam_x=0.0, cam_d=5.06, pair_x=0.0, lens=40, cam_tz=0.855, wb_tint=0.0,
)


# the portrait (for phones): the same room, the pair brought in round a two-door credenza so it fills a 4:5 frame
PORTRAIT = dict(spk_x=0.92, cab_w=1.1, doors=2, socket_x=1.46, tt_x=0.08, books_x=0.38, vase_x=-0.4, port_d=4.1,
                port_lens=50, port_tz=0.62,
                # the sun a little further round for this pair, and the sheers' gaps where its beams come in
                sun=dict(azimuth_deg=-66.0, elevation_deg=18.0, irradiance=48.0, angle_deg=0.5, color='#FFE4C8'),
                sheers=[(-0.62, 0.38), (-2.7, 3.0)])     # the gaps where the beams to the pair (now +-0.92) come in


def shot(v=None, portrait=False):
    global SPK_X, PX
    v = {**DEFAULT, **(PORTRAIT if portrait else {}), **(v or {})}
    PX = v.get('pair_x', 0.0)                                 # the pair's and the credenza's centre (x)
    SPK_X = v.get('spk_x', 1.2)                               # the pair's spacing (the portrait brings them in)
    CAB['w'] = v.get('cab_w', 1.62)
    s = {
        'title': 'barkhorn, Poison, at home (room 31)',
        'products': [
            {'def': 'studio/products/barkhorn-cloud.json', 'flavour': 'eucalyptus-y2k-green',
             'instances': [{'flavour': 'eucalyptus-y2k-green', 'position': [PX - SPK_X, SPK_Y, 0.0], 'rotate_z': TOE},
                           {'flavour': 'eucalyptus-y2k-green', 'position': [PX + SPK_X, SPK_Y, 0.0], 'rotate_z': -TOE}]},
            {'def': 'studio/products/barkhorn-turntable.json', 'flavour': v.get('tt_flavour', 'fog'),
             'instances': [{'flavour': v.get('tt_flavour', 'fog'), 'position': [PX + v.get('tt_x', -0.15), BACK - 0.012 - CAB['d'] / 2 - 0.01, CAB['h']],
                            'rotate_z': 0.0}]},
        ],
        'set': room_set(v),
        'sun': dict(v['sun']),
        'sky': {'kind': 'physical', 'strength': v['sky_strength'], 'air': 1.0, 'dust': 1.5},
        'lights': {
            'key': {'off': True}, 'fill': {'off': True}, 'wash': {'off': True},
            # the sun-free window off to the right, out of frame: the shade side's soft light
            'north': {'type': 'area', 'size_m': [2.2, 2.4], 'position': v.get('fill_pos', [RIGHT - 0.55, -2.2, 1.6]),
                      'target': [0.0, 0.2, 0.9], 'irradiance': v['fill'], 'color': v.get('fill_color', '#EEF2F8')},
            # a warm bounce card beside the camera, as an interiors photographer would set one, so the horns' throats
            # read as resin and not as holes
            'bounce': {'type': 'area', 'position': v.get('bounce_pos', [0.0, SPK_Y - 4.6, 1.5]), 'size_m': v.get('bounce_size', [1.6, 1.2]),
                       'target': [0.0, 0.3, 1.15], 'irradiance': v.get('bounce', 0.35), 'color': '#FFF0DE'},
            # a kicker hidden behind each speaker, as an interiors photographer would hide one (and what the sunlit plaster
            # behind would bounce): it lights the batts through the acrylic, so the cabinets glow as the material does
            **{f'kick{k}': {'type': 'area', 'size_m': [0.42, 0.7], 'position': [PX + sx * SPK_X, SPK_Y + 0.32, 0.62],
                            'target': [PX + sx * SPK_X, SPK_Y - 1.0, 0.62], 'irradiance': v.get('kick', 0.0), 'color': '#FFF2E0',
                            'specular': 0, 'transmission': False}
               for k, sx in (('L', -1), ('R', 1)) if v.get('kick', 0) > 0},
            # light the floor bounces up under the credenza (a real room's toe-kick is never a black hole)
            'floorbounce': {'type': 'area', 'size_m': [0.8, 0.3], 'position': v.get('fb_pos', [0.0, -1.0, 0.1]), 'target': [PX, 0.8, 0.04],
                            'irradiance': v.get('floor_bounce', 0.0), 'color': '#FFE8CC'},
        },
        'render': {'samples': 128, 'adaptive': 0.02, 'denoise': True, 'clamp': 10, 'bounces': 12,
                   'view': 'Khronos PBR Neutral', 'exposure': v['exposure'], 'white_balance_k': v.get('wb', 5600),
                   'white_balance_tint': v.get('wb_tint', 4.0)},
    }
    if not portrait:
        s['size'] = [2880, 1620]
        cx, d = v.get('cam_x', 0.0), v.get('cam_d', 5.06)
        s['camera'] = {'position': [cx, SPK_Y - d, 1.05], 'target': [cx, SPK_Y, v.get('cam_tz', 0.855)],
                       'lens_mm': v.get('lens', 40), 'level': True, 'fstop': v.get('fstop', 5.6),
                       'focus': [PX + SPK_X * 0.5, SPK_Y - 0.21, 0.7]}
    else:
        s['size'] = [1600, 2000]
        # for phones: the pair across the frame, the wall above for the heading, the floor and rug below
        s['camera'] = {'position': [0.0, SPK_Y - v.get('port_d', 3.9), 1.05], 'target': [0.0, SPK_Y, v.get('port_tz', 1.25)],
                       'lens_mm': v.get('port_lens', 35), 'level': True,
                       'fstop': 5.6, 'focus': [0.0, SPK_Y - 0.21, 0.7]}
    return s


def write(v=None, tag=''):
    os.makedirs(OUT, exist_ok=True)
    for name, port in (('room', False), ('room-portrait', True)):
        p = os.path.join(OUT, f'{name}{tag}.json')
        json.dump(shot(v, port), open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    write()
