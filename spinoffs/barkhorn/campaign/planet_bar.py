"""The bar the owner liked (the coordinator, 2026-11-11 17:33: "Would be cooler if the speakers were built into the shelves
like the original bar renders"): the bar lane's Planet EARF bar (planet_r37's room, round 38's bar, e7149388
planet38 finals-b/bar-smoke), ONLY its room: the walnut record wall with its speaker bays, the concrete panels, the
fluted walnut bar, the stools. Every old product and every light in it out (the bar lane's DARK switches and
products_only, as its afterhours scene does); the products are the approved ones:

- a Tropos pair in Dust (shots._approved), each in its own tall bay of the record wall (r37_plan.SPK_NICHES), standing
  at back-counter height (FEET_BAR) so the whole speaker shows above the bar top;
- Mantle in Ember (its asset, checked) on the back counter between them, a record on;
- Hemispheres in Ember, Dust and Acid over the bar; Cores on the bar top (r32-lamps-final 3e38954b, its own LED
  colours and loadings);
- light: the lamps, exposed as the lamps lane exposes them, and declared track lights above the frame throwing pools
  with falloff onto the record wall and the bar.

    TROPOS_BASE=A python3 spinoffs/barkhorn/campaign/planet_bar.py OUTDIR
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
sys.path[:0] = [os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', d) for d in ('r37', 'r36', 'tropos-a')]
import shots                                    # noqa: E402
import r37_plan as R                            # noqa: E402
from make_listening import FEET_BAR             # noqa: E402

import listening_bar as LB                     # noqa: E402  (its turned glass)
SRC = ('e7149388', 'renders/2026-10-20/barkhorn/planet38/finals-b/bar-smoke.shot.json')
LIFE = 'spinoffs/barkhorn/campaign/bar_life/bar_life.py'
LAMPS = 'spinoffs/barkhorn/campaign/stage/stage2_props.py'
DARK = {k: 0.0 for k in ('dome_w', 'dome_glow', 'sphere_w', 'sphere_glow', 'disc_glow', 'disc_lamp', 'name_glow',
                         'niche_strip', 'sink_glow', 'sink_strip', 'sink_w', 'screen_glow', 'etch_glow', 'shade_glow',
                         'flat_glow', 'flame', 'windows_lit', 'counter_strip', 'sconce_w', 'sconce_glow',
                         'spk_niche_strip', 'plinth_bar', 'plinth_listen')}
Y_BAR = (R.COUNTER['y0'] + R.COUNTER['y1']) / 2
TOP = R.COUNTER['top_z']
SPK_Y = R.BACKBAR_Y + 0.0662
MANTLE = (6.9, R.BACKBAR_Y - 0.2, FEET_BAR - 0.02)
HEMIS = [('ember', 5.25, 0.0, 1.70), ('dust', 5.85, 0.06, 1.82), ('acid', 6.5, -0.02, 1.68), ('ember', 7.15, 0.05, 1.78),
         ('dust', 7.8, -0.03, 1.72), ('acid', 8.45, 0.04, 1.84)]
CORES = [('ember', 5.55, -0.12), ('dust', 7.6, -0.18), ('acid', 8.75, -0.1)]     # (test 1: the Dust Core hid Mantle at 6.95)
EV, WB = -1.5, 4000          # the lamps lane's finals: Core -1, Hemisphere -2, white balance 4000 K
TRACK = 2.0                  # the declared track lights' scale (test 1: too dark)


def _room():
    s = json.loads(subprocess.run(['git', 'show', f'{SRC[0]}:{SRC[1]}'], capture_output=True, check=True, cwd=ROOT).stdout)
    room = copy.deepcopy(s['set']['props'][0])
    room.update(DARK)
    room.update({'street': False, 'tropos_feet': True, 'host_stand': False, 'products_only': True, 'life_glasses': [],
                 'life_sleeves': []})
    return s, room


def _lamps(hemis, cores):
    # (no led_k: the lamps lane's own LED colours; its Core loadings, 0.5 x TINT_LOAD, as CORE_LOAD)
    return {'kind': 'kit', 'shape': 'ext', 'path': LAMPS, 'fn': 'lamps', 'top_z': R.CEIL, 'core_load': shots.CORE_LOAD,
            'hemispheres': [{'tint': shots.KEY[t], 'x': x, 'y': round(Y_BAR + dy, 3), 'rim_z': z} for t, x, dy, z in hemis],
            'cores': [{'tint': shots.KEY[t], 'x': x, 'y': round(Y_BAR + dy, 3), 'floor_z': TOP, 'rot': 0.0} for t, x, dy in cores]}


def _life():
    """People were just here, and the music is on (the owner, 17:36: "anemic in soul"): two drinks mid-evening with ice
    and a twist, a bar cloth, a bowl of citrus (scanned), a book of matches, a folded newspaper; the now-playing sleeve
    standing by Mantle, a small stack waiting, a few sleeves pulled half out of the wall (invented covers); a worn
    runner on the concrete, a plant (scanned); and the one wry detail, a RESERVED card at the foot of a speaker's bay.
    Nothing lined up."""
    T, BB = TOP, FEET_BAR - 0.02
    RK = [[0, 0], [0.041, 0], [0.043, 0.006], [0.044, 0.092]]
    out = []
    for (x, y, rz, fill) in ((6.12, Y_BAR - 0.16, 0.0, 0.045), (6.31, Y_BAR - 0.02, 0.0, 0.03)):
        out.append(LB.lathe(LB.shell(RK, 0.0035, 0.016), [x, y, T], 'glass', '#F8F8F6', 64))
        out.append(LB.lathe(LB.contents(RK, fill, 0.0035, 0.016), [x, y, T], 'resin', '#A65812', 64))
        for j, (dx, dy, dz, a) in enumerate(((-0.012, 0.006, 0.02, 12.0), (0.01, -0.008, 0.026, -20.0))):   # ice, a little proud
            out.append({'kind': 'kit', 'shape': 'box', 'size': [0.026, 0.026, 0.024], 'position': [x + dx, y + dy, T + 0.016 + dz],
                        'rotate': [8.0 * j, -6.0, a], 'material': 'frosted', 'color': '#F4F7F8', 'ease': 0.004})
        out.append({'kind': 'kit', 'shape': 'tube', 'points': [[x + 0.02, y - 0.03, T + 0.096], [x + 0.034, y - 0.012, T + 0.1],
                                                                [x + 0.03, y + 0.014, T + 0.094]], 'radius': 0.0035,
                    'material': 'clay', 'color': '#E2861E', 'roughness': 0.45})                                    # a twist of orange
    out += [{'kind': 'kit', 'shape': 'box', 'size': [0.22, 0.13, 0.014], 'position': [7.95, Y_BAR + 0.12, T], 'rotate': [0, 0, -14.0],
             'material': 'cotton', 'color': '#CFC6B4', 'ease': 0.004},                                          # a bar cloth
            {'kind': 'kit', 'shape': 'asset', 'model': 'wooden_bowl_01', 'res': '2k', 'position': [9.3, Y_BAR + 0.05, T], 'rotate': [0, 0, 30.0]},
            {'kind': 'kit', 'shape': 'asset', 'model': 'food_lime_01', 'res': '2k', 'position': [9.28, Y_BAR + 0.04, T + 0.03], 'rotate': [0, 20, 0]},
            {'kind': 'kit', 'shape': 'asset', 'model': 'food_lime_01', 'res': '2k', 'position': [9.34, Y_BAR + 0.08, T + 0.032], 'rotate': [30, 0, 90]},
            {'kind': 'kit', 'shape': 'asset', 'model': 'lemon', 'res': '2k', 'position': [9.25, Y_BAR + 0.1, T + 0.035], 'rotate': [0, 70, 20]},
            {'kind': 'kit', 'shape': 'box', 'size': [5.8, 0.85, 0.008], 'position': [6.9, R.STOOL_Y - 0.25, 0.001],
             'material': 'pbr', 'texture': 'poly_wool_herringbone', 'tex_res': '2k', 'tint': '#6A4A36', 'tint_mix': 0.55, 'gain': 0.7},   # a runner
            {'kind': 'kit', 'shape': 'asset', 'model': 'potted_plant_02', 'res': '2k', 'position': [10.4, R.STOOL_Y + 0.1, 0.0], 'rotate': [0, 0, 40.0]}]
    bds = [  # the now-playing sleeve, standing by Mantle, leaning on the wall's foot
           {'image': 'tex/cover-05.png', 'w': 0.315, 'h': 0.315, 'x': 7.62, 'y': R.BACKBAR_Y - 0.05, 'z': BB, 'rot': [-12.0, 0, -8.0], 'ground': '#EFEBE3'},
           # a small stack waiting
           *[{'image': f'tex/cover-{k:02d}.png', 'w': 0.315, 'h': 0.315, 'x': 6.2 + 0.006 * j, 'y': R.BACKBAR_Y - 0.33 + 0.004 * j, 'z': BB + 0.004 * j,
              'rot': [-90.0, 0, [4.0, -6.0, 9.0, -3.0][j]]} for j, k in enumerate((9, 2, 12, 7))],
           # sleeves pulled half out of the wall's cells, their faces turned a little to the room
           *[{'image': f'tex/cover-{k:02d}.png', 'w': 0.315, 'h': 0.315, 'x': x, 'y': R.RECORD_WALL['y'] - 0.14, 'z': z, 'rot': [-4.0, 0, rz],
              'ground': '#E9E3D6'} for k, x, z, rz in ((3, 4.4, 1.565, 70.0), (10, 9.6, 1.925, -64.0), (14, 6.6, 2.285, 58.0))],
           {'image': 'tex/matches.png', 'w': 0.04, 'h': 0.064, 't': 0.006, 'x': 6.55, 'y': Y_BAR - 0.22, 'z': T, 'rot': [-90.0, 0, 22.0]},
           {'image': 'tex/newspaper.png', 'w': 0.29, 'h': 0.4, 't': 0.006, 'x': 9.0, 'y': Y_BAR - 0.26, 'z': T, 'rot': [-90.0, 0, -11.0],
            'ground': '#E4E0D6', 'rough': 0.85},
           # the wry detail: the speaker's seat is taken
           {'image': 'tex/reserved.png', 'w': 0.1, 'h': 0.05, 't': 0.002, 'x': 8.25, 'y': R.BACKBAR_Y - 0.12, 'z': BB, 'rot': [-18.0, 0, 0.0],
            'ground': '#EFEBE3', 'rough': 0.7}]
    out.append({'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'boards', 'boards': bds})
    # (test 2: the room's old DJ station left a mixer and two records floating where the old players stood: out)
    out.append({'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'remove', 'names': ['dj-plinths', 'dj-knobs', 'dj-records', 'dj-labels']})
    # cozy (the owner, 17:39: "Soul to me means lived in. Cozy."): a worn leather armchair at the frame's left, books
    # among the records (cloth spines, stacked and leaning, in cells the records left empty)
    out.append({'kind': 'kit', 'shape': 'asset', 'model': 'ArmChair_01', 'res': '2k', 'position': [5.15, 3.05, 0.0], 'rotate': [0, 0, -150.0]})
    cloth = ['#5A2A22', '#2E3A2E', '#6E5A3E', '#3A2E26', '#7A6448', '#2A2A30', '#5E4A36']
    cz = [R.RECORD_WALL['z0'] + R.RECORD_WALL['cell'] * k + 0.02 for k in range(5)]
    for n_, (x, zi, lean) in enumerate(((5.05, 1, 0.0), (6.25, 3, 8.0), (7.95, 0, 0.0), (9.4, 2, -6.0), (4.3, 3, 0.0))):
        for j in range(5):
            h = 0.22 + 0.06 * ((j * 7 + n_) % 4) / 3
            out.append({'kind': 'kit', 'shape': 'box', 'size': [0.028 + 0.01 * ((j + n_) % 3), 0.2, h],
                        'position': [round(x + j * 0.04, 3), R.RECORD_WALL['y'] + 0.12, cz[zi]], 'rotate': [0, lean, 0],
                        'material': 'card', 'color': cloth[(j + n_ * 2) % len(cloth)], 'ease': 0.002})
    return out


def _track():
    """Declared, above the frame: a bar's track lights, small gridded heads throwing pools with falloff onto the record
    wall and down onto the bar top; warm."""
    out = {}
    for k, x in enumerate((5.0, 6.2, 7.4, 8.6, 9.6)):
        out[f'track-wall{k}'] = {'type': 'area', 'size_m': [0.12, 0.12], 'position': [x, 4.9, R.CEIL - 0.05], 'target': [x + 0.1, R.RECORD_WALL['y'], 1.7],
                                 'irradiance': round(1.6 * TRACK, 3), 'spread_deg': 28, 'color': '#FFD2A0'}
    for k, x in enumerate((5.6, 7.0, 8.4)):
        out[f'track-bar{k}'] = {'type': 'area', 'size_m': [0.12, 0.12], 'position': [x, Y_BAR - 0.6, R.CEIL - 0.05], 'target': [x, Y_BAR, TOP],
                                'irradiance': round(0.5 * TRACK, 3), 'spread_deg': 24, 'color': '#FFD2A0'}
    out['house'] = {'type': 'area', 'size_m': [3.0, 2.0], 'position': [6.9, 0.6, 2.8], 'target': [6.9, 4.5, 1.2],
                    'irradiance': round(0.02 * TRACK, 3), 'color': '#FFD8B0'}     # (cozy: the room's fill low, its edges warm and dark)
    return out


def _base(size, title):
    src, room = _room()
    s = shots._cast_base()
    k = shots.HERO_ORDER.index('dust')
    pair = []
    for blk in s['products']:
        i = blk['instances'][k]
        pair.append({**blk, 'instances': [{**copy.deepcopy(i), 'position': [x, SPK_Y, FEET_BAR], 'rotate_z': 0.0} for x in R.SPK_NICHES]})
    s['products'] = pair
    shots._approved(s, order=['dust', 'dust'])
    s['products'].append(shots._mantle(*MANTLE, 0.0, tint='ember'))
    s['set'] = {'kind': 'stage', 'props': [room] + _life()}
    s['haze'] = {'box_m': [3.2, 0.5, 0.0, 10.6, 6.1, 3.35], 'density': 0.012, 'anisotropy': 0.5, 'color': '#FFFFFF'}   # declared: a little haze in the pools
    s['materials'] = {**{k: v for k, v in s.get('materials', {}).items() if k != 'sweep'},
                      **{m: {'glow': 0.0} for m in ('uplight-edge', 'uplight-panel', 'uplight-wash', 'led')}, 'glow': {'strength': 0.0}}
    s['sky'] = {**src['sky'], 'strength': 0.0}
    s['lights'] = _track()
    s['size'] = size
    s['render'] = {**s['render'], 'samples': 128, 'adaptive': 0.01, 'denoise': True, 'clamp': 0, 'bounces': 24, 'diffuse_bounces': 8,
                   'glossy_bounces': 12, 'transmission_bounces': 24, 'caustics_refractive': True, 'caustics_reflective': False,
                   'view': 'AgX', 'look': 'AgX - Punchy', 'exposure': EV, 'white_balance_k': WB, 'white_balance_tint': 0.0}
    s.pop('finish', None)
    s['title'] = title
    return s


def bar_backbar():
    """From a seat at the bar, across the bar top to the record wall: both Tropos in their bays, Mantle between,
    Hemispheres above, Cores on the bar; 40 mm, a little off axis, some depth of field."""
    s = _base([1920, 1080], 'Planet EARF bar: the record wall from a seat at the bar')
    s['set']['props'].append(_lamps(HEMIS, CORES))
    # (test 1: the bays cut by the frame: a seat pulled back, 30 mm, a little off axis)
    # (17:39 "cozy": closer and lower, from a stool at the bar at a seated eye, the room wrapping round; 26 mm so both
    # bays stay whole)
    s['camera'] = {'position': [6.6, 3.05, 1.36], 'target': [6.95, 5.6, 1.55], 'lens_mm': 26.0, 'level': True,
                   'fstop': 3.2, 'focus': [6.9, 4.15, 1.12]}
    return s


def core_bar_table():
    """One Core on this bar's top, the record wall soft behind, the ball as a lit lamp (the lamps lane's Core exposure)."""
    s = _base([1920, 1280], 'Planet EARF bar: one Core on the bar top')
    s['set']['props'].append(_lamps([], [('ember', 7.05, -0.1)]))
    s['camera'] = {'position': [7.35, Y_BAR - 1.25, TOP + 0.2], 'target': [7.05, Y_BAR - 0.1, TOP + 0.12], 'lens_mm': 85.0, 'level': True,
                   'fstop': 2.0, 'focus': [7.05, Y_BAR - 0.1, TOP + 0.12]}
    s['render']['exposure'] = -1.0
    s['lights'] = {k: {**v, 'irradiance': round(v['irradiance'] * 2 ** (EV + 1.0), 4)} for k, v in s['lights'].items()}
    return s


SHOTS = {'bar-backbar': bar_backbar, 'core-bar-table': core_bar_table}

if __name__ == '__main__':
    od = sys.argv[1]
    os.makedirs(od, exist_ok=True)
    for n, f in SHOTS.items():
        json.dump(f(), open(os.path.join(od, n + '.json'), 'w'), indent=1)
        print(n)
