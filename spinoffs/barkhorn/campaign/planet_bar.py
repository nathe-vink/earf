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
# (test 3, by ray cast: behind the bar is the bartender's aisle, floor to the wall; the original's players stood on the
# bar top's back half, the DJ station, between the bays: Mantle there, where the room's left player stood)
DECK_Y = R.COUNTER['y1'] - 0.22
MANTLE = (R.DJ['x'] - 0.38, DECK_Y, R.COUNTER['top_z'] + 0.001)
# (18:36: no lamp across a speaker, every shade whole, one over Mantle so it sits in a pool: five, between the bays)
HEMIS = [('dust', 6.18, -0.02, 1.80), ('ember', 6.54, 0.12, 1.66), ('acid', 6.92, -0.04, 1.86), ('ember', 7.3, 0.08, 1.74),
         ('dust', 7.66, -0.03, 1.82)]
CORES = [('ember', 6.05, -0.14), ('dust', 7.05, -0.2), ('acid', 7.8, -0.12)]     # (18:36: all three in frame, none before Mantle)
EV, WB = -1.5, 4000          # the lamps lane's finals: Core -1, Hemisphere -2, white balance 4000 K
TRACK = 3.0                  # the declared track lights' scale (tests 1-4: too dark)


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
            {'kind': 'kit', 'shape': 'box', 'size': [4.2, 1.6, 0.008], 'position': [6.9, 2.75, 0.001],
             'material': 'pbr', 'texture': 'poly_wool_herringbone', 'tex_res': '2k', 'tint': '#6A4A36', 'tint_mix': 0.55, 'gain': 0.7},   # a runner
            {'kind': 'kit', 'shape': 'asset', 'model': 'potted_plant_02', 'res': '2k', 'position': [8.85, 2.35, 0.0], 'rotate': [0, 0, 40.0]}]
    out.append({'kind': 'kit', 'shape': 'box', 'size': [0.2, 0.05, 0.022], 'position': [6.86, DECK_Y + 0.09, T],
                'material': 'pbr', 'texture': 'american_walnut_veneer', 'tex_res': '2k', 'tint': '#5A3824', 'tint_mix': 0.5, 'gain': 0.6, 'ease': 0.003})
    bds = [  # the now-playing sleeve on a small walnut stand by Mantle
           {'image': 'tex/cover-05.png', 'w': 0.18, 'h': 0.18, 'x': 6.86, 'y': DECK_Y + 0.08, 'z': T + 0.022, 'rot': [-14.0, 0, -10.0], 'ground': '#EFEBE3', 'rough': 0.85},
           # a small stack waiting, on the bar top's back half
           *[{'image': f'tex/cover-{k:02d}.png', 'w': 0.315, 'h': 0.315, 'x': 7.62 + 0.006 * j, 'y': DECK_Y + 0.16 + 0.004 * j, 'z': T + 0.004 * j,
              'rot': [-90.0, 0, [4.0, -6.0, 9.0, -3.0][j]]} for j, k in enumerate((9, 2, 12, 7))],
           # sleeves pulled half out of the wall's cells, their faces turned a little to the room
           *[{'image': f'tex/cover-{k:02d}.png', 'w': 0.315, 'h': 0.315, 'x': x, 'y': R.RECORD_WALL['y'] - 0.14, 'z': z, 'rot': [-4.0, 0, rz],
              'ground': '#E9E3D6'} for k, x, z, rz in ((3, 4.4, 1.565, 70.0), (10, 9.6, 1.925, -64.0), (14, 6.6, 2.285, 58.0))],
           {'image': 'tex/matches.png', 'w': 0.04, 'h': 0.064, 't': 0.006, 'x': 6.55, 'y': Y_BAR - 0.22, 'z': T, 'rot': [-90.0, 0, 22.0]},
           {'image': 'tex/newspaper.png', 'w': 0.29, 'h': 0.4, 't': 0.006, 'x': 9.0, 'y': Y_BAR - 0.26, 'z': T, 'rot': [-90.0, 0, -11.0],
            'ground': '#E4E0D6', 'rough': 0.85},
           # the wry detail: the speaker's seat is taken
           {'image': 'tex/reserved.png', 'w': 0.1, 'h': 0.05, 't': 0.002, 'x': 8.25, 'y': SPK_Y - 0.27, 'z': FEET_BAR, 'rot': [-18.0, 0, 0.0],
            'ground': '#EFEBE3', 'rough': 0.7}]
    out.append({'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'boards', 'boards': bds})
    # (test 2: the room's old DJ station left a mixer and two records floating where the old players stood: out)
    out.append({'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'remove', 'names': ['dj-plinths', 'dj-knobs', 'dj-records', 'dj-labels']})
    # cozy (the owner, 17:39: "Soul to me means lived in. Cozy."): a worn leather armchair at the frame's left, books
    # among the records (cloth spines, stacked and leaning, in cells the records left empty)
    out.append({'kind': 'kit', 'shape': 'asset', 'model': 'ArmChair_01', 'res': '2k', 'position': [5.35, 2.05, 0.0], 'rotate': [0, 0, -120.0]})   # foreground, soft
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
    for k, xc in enumerate(R.SPK_NICHES):                     # (18:36: a pool on each bay, so the whole speaker reads)
        out[f'track-bay{k}'] = {'type': 'area', 'size_m': [0.14, 0.14], 'position': [xc, 3.9, R.CEIL - 0.05], 'target': [xc, SPK_Y, FEET_BAR + 0.75],
                                'irradiance': round(1.4 * TRACK, 3), 'spread_deg': 22, 'color': '#FFD8B0'}
    out['track-mantle'] = {'type': 'area', 'size_m': [0.1, 0.1], 'position': [MANTLE[0], MANTLE[1] - 0.5, R.CEIL - 0.05],
                           'target': [MANTLE[0], MANTLE[1], MANTLE[2]], 'irradiance': round(0.6 * TRACK, 3), 'spread_deg': 16, 'color': '#FFD8B0'}
    # (18:36: the dark warm, not black: a broad low warm fill from the room behind the camera)
    out['house'] = {'type': 'area', 'size_m': [4.0, 2.0], 'position': [6.9, 0.2, 2.6], 'target': [6.9, 4.5, 1.0],
                    'irradiance': round(0.05 * TRACK, 3), 'color': '#FFC890'}
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
    RW = R.RECORD_WALL
    fill = {'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'fill_records', 'x0': RW['x0'], 'x1': RW['x1'], 'z0': RW['z0'], 'z1': RW['z1'],
            'cell': RW['cell'], 'y': RW['y'], 'depth': RW['depth'], 'skip': [[xc - 0.42, xc + 0.42, 0.0, 4.0] for xc in R.SPK_NICHES]}
    s['set'] = {'kind': 'stage', 'props': [room, fill] + _life()}
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
    # (18:36: both bays whole with air, every shade whole, all three Cores in: from a lounge seat further back, 24 mm)
    s['camera'] = {'position': [6.55, 1.55, 1.3], 'target': [6.92, 5.6, 1.72], 'lens_mm': 24.0, 'level': True,
                   'fstop': 2.8, 'focus': [6.9, 4.2, 1.2]}
    return s


def core_bar_table():
    """One Core on this bar's top, the record wall soft behind, the ball as a lit lamp (the lamps lane's Core exposure)."""
    s = _base([1920, 1280], 'Planet EARF bar: one Core on the bar top')
    s['set']['props'].append(_lamps([], [('ember', 7.05, -0.1)]))
    # (18:36: the now-playing sleeve out of the close-up; the base given the samples it needs)
    for pr in s['set']['props']:
        if pr.get('fn') == 'boards':
            pr['boards'] = [b for b in pr['boards'] if 'cover-05' not in b['image']]
    s['render'].update(samples=512, adaptive=0.004)
    s['camera'] = {'position': [7.3, Y_BAR - 1.25, TOP + 0.2], 'target': [7.05, Y_BAR - 0.1, TOP + 0.12], 'lens_mm': 85.0, 'level': True,
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
