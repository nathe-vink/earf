"""New living-room directions (the owner, 24 Nov 04:02: "Room is too barren and midcentury for these speakers. We might
try something 90s with CRT screens and gadgetry, or something more contemporary"; "Core needs a more cozy setup like a
lamp on a table next to a cozy lounge chair"). Proofs only, for the coordinator to show the owner.

Built on living_room.py's room (its 5.4 x 6.0 x 2.75 m shell, windows, the garden_nook sky with its own sun) and its
light model (one HDRI, no lamps, cards or fill; both caustics on, clamp 0, filter_glossy 0, the acrylics' shortcut cut),
with the props replaced. Every prop is a CC0 Poly Haven model or the kit's own geometry.

  r90   a lived-in 1990s room: the Tropos pair either side of a CRT on a black-ash stand, a VCR and a games console under
        it, the gamepad on the carpet, a worn bookshelf with a boombox and a camcorder, a sofa, a coffee table with a
        cassette player and magazines, posters, wall-to-wall carpet
  now   a contemporary room: plaster walls, wide oak floor, the walnut console with Mantle, a deep sofa and an armchair,
        a full bookshelf, a tall plant, one large abstract print, a coffee table with books
  cozy  the Core's corner by evening: the Core lit (its own LED, the lamps lane's code) on a side table beside a worn
        leather armchair with a wool throw, books, a plant; the dusk sky at the window (the HDRI dimmed), nothing else

    python3 spinoffs/barkhorn/campaign/rooms2.py OUTDIR [TINT]  ->  OUTDIR/<room>-<framing>-<tint>.json (proof size)
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shots                                    # noqa: E402
import living_room as LR                        # noqa: E402

EXT = LR.EXT
LIFE = LR.LIFE
PROOF = dict(samples=48, adaptive=0.02)
SIZE = (960, 640)


def asset(model, x, y, rz=0.0, z=0.0, res='2k'):
    return {'kind': 'kit', 'shape': 'asset', 'model': model, 'res': res, 'position': [x, y, z], 'rotate': [0, 0, rz]}


def box(size, pos, rz=0.0, **mat):
    return {'kind': 'kit', 'shape': 'box', 'size': size, 'position': pos, 'rotate': [0, 0, rz], **mat}


def room(tint, wall='#E6E0D5', props=(), floor=None):
    """living_room's base with its props replaced (the pair and Mantle as there; Mantle dropped where not wanted)."""
    s = LR.base(tint, SIZE)
    s['set']['wall'] = {'color': wall}
    keep = [{'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'no_portal', 'windows': ['wall-back', 'wall-left', 'wall-right']}]
    s['set']['props'] = [floor or LR._floor()] + list(props) + keep + \
        [{'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'no_glass_shadows'}]
    s['render'].update(PROOF)
    return s


# ---- (a) the 1990s room -------------------------------------------------------------------------------------------
def r90(tint='ember'):
    B = LR.BACK
    carpet = box([LR.W - 0.02, LR.D - 0.02, 0.012], [LR.CX, LR.CY, 0.006], material='pbr', texture='poly_wool_herringbone',
                 tex_res='2k', tex_scale=0.25, tint='#8C7F6C', tint_mix=0.75, gain=0.8)
    stand_y = B - 0.30
    props = [
        carpet,
        # the TV stand, black ash, with its shelf; the CRT on top; a VCR and the games console on the shelf
        box([1.1, 0.48, 0.03], [0.0, stand_y, 0.47], material='plain', color='#1D1B19', roughness=0.45),
        box([1.1, 0.48, 0.03], [0.0, stand_y, 0.22], material='plain', color='#1D1B19', roughness=0.45),
        box([0.03, 0.48, 0.47], [-0.535, stand_y, 0.0], material='plain', color='#1D1B19', roughness=0.45),
        box([0.03, 0.48, 0.47], [0.535, stand_y, 0.0], material='plain', color='#1D1B19', roughness=0.45),
        asset('Television_01', 0.0, stand_y, 0.0, z=0.50),
        box([0.43, 0.30, 0.09], [-0.22, stand_y, 0.25], material='plain', color='#202020', roughness=0.35),     # the VCR
        asset('gaming_console', 0.25, stand_y, 0.0, z=0.25),
        asset('gamepad', 0.35, -0.55, 35.0, z=0.012),
        # the worn bookshelf on the left wall, books, the boombox and the camcorder on it
        asset('wooden_bookshelf_worn', LR.LEFT + 0.25, 0.2, 90.0),
        {'kind': 'books', 'position': [LR.LEFT + 0.25, 0.2], 'z': 0.95, 'colors': ['#2F3E6B', '#B8352C', '#E3C04A', '#3D6B44', '#D9D2C2'], 'seed': 9},
        asset('boombox', LR.LEFT + 0.27, 0.05, 90.0, z=1.42),
        asset('vintage_video_camera', LR.LEFT + 0.27, 0.55, 70.0, z=0.95),
        # the sofa facing the TV, the coffee table with a cassette player and magazines, throw pillows
        asset('sofa_03', 0.0, -1.35, 180.0),
        asset('CoffeeTable_01', 0.0, -0.35, 0.0),
        asset('portable_cassette_player', -0.25, -0.35, 20.0, z=0.42),
        box([0.21, 0.28, 0.006], [0.18, -0.30, 0.42], -12.0, material='paper', color='#C84B3A'),
        box([0.21, 0.28, 0.006], [0.22, -0.36, 0.426], 8.0, material='paper', color='#2E5C8A'),
        asset('potted_plant_01', LR.LEFT + 0.45, 1.65),
        # posters, a bit crooked, on the back wall either side of the windows' reach
        {'kind': 'frame', 'position': [-1.85, B - 0.012], 'z': 1.55, 'size': [0.5, 0.7],
         'artwork': {'bands': [['#1B2A5C', 0.4], ['#D2452F', 0.25], ['#F0C84A', 0.35]], 'ground': '#121212', 'seed': 4}},
        {'kind': 'frame', 'position': [1.9, B - 0.012], 'z': 1.6, 'size': [0.45, 0.6],
         'artwork': {'bands': [['#3BA59B', 0.5], ['#F2E6D0', 0.2], ['#8E3B8A', 0.3]], 'ground': '#1A1A1A', 'seed': 12}},
    ]
    s = room(tint, wall='#E9E1CF', props=props)
    s['products'] = [b for b in s['products'] if 'asset_blend' not in b]          # no Mantle in this room
    s['title'] = f'Living room, 1990s: the pair either side of the CRT ({tint})'
    s['camera'] = {'position': [0.35, -2.2, 1.55], 'target': [0.0, 1.6, 0.95], 'lens_mm': 26.0, 'level': True, 'fstop': 8.0,
                   'focus': [0.0, 1.3, 0.9]}
    return s


def r90_side(tint='ember'):
    s = r90(tint)
    s['title'] = f'Living room, 1990s: from the sofa\'s end, the CRT, a speaker and the shelf ({tint})'
    s['camera'] = {'position': [1.9, -1.6, 1.25], 'target': [-0.6, 1.4, 0.9], 'lens_mm': 32.0, 'level': True, 'fstop': 8.0,
                   'focus': [0.0, 1.4, 0.9]}
    return s


# ---- (b) the contemporary room ------------------------------------------------------------------------------------
def now(tint='ember'):
    B = LR.BACK
    floor = {'kind': 'kit', 'shape': 'box', 'size': [LR.W - 0.02, LR.D - 0.02, 0.003], 'position': [LR.CX, LR.CY, 0.0005],
             'material': 'pbr', 'texture': 'wood_floor_deck', 'tex_res': '2k', 'gain': 1.0}
    props = [
        *LR._rug(), *LR._console(),
        {'kind': 'books', 'position': [-0.6, LR.CON_Y], 'z': LR.TOP, 'colors': ['#2B3A4A', '#C9B79C', '#8A3B2E', '#E8E2D6'], 'seed': 7},
        asset('sofa_02', 0.0, -1.0, 180.0),
        asset('throw_pillows_01', -0.4, -1.05, 180.0, z=0.42),
        asset('modern_arm_chair_01', -1.65, -0.35, 125.0),
        asset('modern_coffee_table_01', 0.0, -0.15, 0.0),
        {'kind': 'books', 'position': [0.15, -0.15], 'z': 0.36, 'colors': ['#D7CFC0', '#3A3F46'], 'seed': 3},
        asset('Shelf_01', LR.W / 2 - 0.25, 0.4, -90.0),
        {'kind': 'books', 'position': [LR.W / 2 - 0.25, 0.4], 'z': 1.2, 'colors': ['#43505C', '#B59A72', '#7E2F2A', '#E4DED2', '#2E2C2A'], 'seed': 11},
        asset('potted_plant_04', -2.25, 1.55),
        {'kind': 'frame', 'position': [0.0, B - 0.012], 'z': 1.75, 'size': [1.2, 0.8],
         'artwork': {'bands': [['#C9BBA6', 0.35], ['#6E7B73', 0.3], ['#E2D9CB', 0.35]], 'ground': '#EAE4DA', 'seed': 33}},
    ]
    s = room(tint, wall='#DEDAD3', props=props, floor=floor)
    s['title'] = f'Living room, contemporary: the pair and the console ({tint})'
    s['camera'] = {'position': [0.6, -3.1, 1.45], 'target': [0.0, 1.6, 1.0], 'lens_mm': 30.0, 'level': True, 'fstop': 8.0,
                   'focus': [0.0, 1.3, 0.9]}
    return s


def now_side(tint='ember'):
    s = now(tint)
    s['title'] = f'Living room, contemporary: from the armchair, across the room ({tint})'
    s['camera'] = {'position': [-2.0, -2.4, 1.3], 'target': [0.6, 1.5, 0.95], 'lens_mm': 32.0, 'level': True, 'fstop': 8.0,
                   'focus': [0.5, 1.3, 0.9]}
    return s


# ---- (c) the Core's cozy corner -----------------------------------------------------------------------------------
CORNER = (-2.0, 1.2)          # the side table's centre, in the room's back-left corner
CHAIR = (-0.95, 1.05)         # the lounge chair, turned 35 deg toward the room
THROW = (-0.48, 1.25, 0.6)    # hung over the chair's arm (the chair has no ottoman)
LAMP, LAMP_H, LAMP_D = (-1.45, 1.62), 1.55, 0.30
SKY_K, EXPOSURE, LAMP_LM = 0.45, 1.3, 2000
def cozy(tint='ember'):
    x, y = CORNER
    T = 0.5507                # side_table_01's top
    props = [
        *LR._rug(),
        asset('side_table_01', x, y),
        *LR._book(x + 0.12, y + 0.10, T + 0.0005, 18.0, cloth='#6B3A2C'),
        *LR._book(x + 0.13, y + 0.11, T + 0.0285, 6.0, cloth='#2F3D4C'),
        # a deep lounge chair to read in; a knit throw hung over its arm, on the room's side
        asset('mid_century_lounge_chair', *CHAIR, 35.0),
        {'kind': 'kit', 'shape': 'drape', 'orient': 'hang', 'size': [0.5, 0.42], 'folds': 3, 'amplitude': 0.025, 'noise': 0.4,
         'seed': 5, 'position': list(THROW), 'rotate': [0, 0, -55.0], 'material': 'wool', 'color': '#B9A68A'},
        # the room's light: a floor lamp between the table and the chair, its bulb in the lights below
        {'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'floor_lamp', 'x': LAMP[0], 'y': LAMP[1], 'height': LAMP_H,
         'radius': 0.21, 'drum': LAMP_D},
        asset('potted_plant_02', x - 0.35, y - 0.9),
        {'kind': 'books', 'position': [x + 0.25, y + 0.45], 'z': 0.0, 'colors': ['#5C3A2A', '#C2B49A', '#3B4A3E', '#8E2F2A'], 'seed': 2},
        {'kind': 'frame', 'position': [x + 0.6, LR.BACK - 0.012], 'z': 1.5, 'size': [0.45, 0.6],
         'artwork': {'bands': [['#B7A68A', 0.4], ['#5E4A3C', 0.3], ['#D8CBB4', 0.3]], 'ground': '#E3DACB', 'seed': 8}},
        # the Core, lit: the lamps lane's own code and photometry (its 200 lm LED), on the side table
        shots._family(cores=[(tint, x - 0.08, y - 0.05, T, 0.0)]),
    ]
    s = room(tint, wall='#E3D8C6', props=props)
    s['products'] = []                                                   # no speakers in the Core's corner
    # blue hour at the window: a sky with no sun in it, a little light (the coordinator, 04:58: never bright day)
    s['sky'] = {'kind': 'gradient', 'zenith': '#1F2D52', 'horizon': '#5C6F9C', 'ground': '#1C2029', 'strength': SKY_K}
    # the floor lamp's bulb: LAMP_LM warm white at the lamp lane's scale (0.0065 W a lumen), every ray on
    s['lights'] = {'floor-lamp-bulb': {'type': 'point', 'position': [LAMP[0], LAMP[1], LAMP_H - LAMP_D / 2],
                                       'power_w': round(LAMP_LM * 0.0065, 2), 'color': 2700, 'radius_m': 0.03}}
    # Khronos PBR Neutral, not AgX: AgX takes the Core's lit globe to white, Neutral keeps its Ember red (one camera
    # rendering for the frame; the light is unchanged)
    s['render'].update(exposure=EXPOSURE, view='Khronos PBR Neutral', look='None')
    s['title'] = f'The Core\'s corner by evening: lit on a side table by the armchair ({tint})'
    s['camera'] = {'position': [x + 2.35, y - 3.1, 1.3], 'target': [x + 0.6, y, 0.75], 'lens_mm': 32.0, 'level': True, 'fstop': 4.0,
                   'focus': [x, y, T + 0.15]}
    return s


def cozy_close(tint='ember'):
    s = cozy(tint)
    x, y = CORNER
    s['title'] = f'The Core\'s corner by evening: close on the lamp and the chair\'s arm ({tint})'
    s['camera'] = {'position': [x + 0.3, y - 1.35, 0.95], 'target': [x + 0.15, y, 0.65], 'lens_mm': 45.0, 'level': True, 'fstop': 3.2,
                   'focus': [x - 0.08, y - 0.05, 0.75]}
    return s


SHOTS = {'r90-wide': r90, 'r90-side': r90_side, 'now-wide': now, 'now-side': now_side, 'cozy-wide': cozy, 'cozy-close': cozy_close}

if __name__ == '__main__':
    od = sys.argv[1]
    tint = sys.argv[2] if len(sys.argv) > 2 else 'ember'
    os.makedirs(od, exist_ok=True)
    for n, f in SHOTS.items():
        json.dump(f(tint), open(os.path.join(od, f'{n}-{tint}.json'), 'w'), indent=1)
        print(n, tint)
