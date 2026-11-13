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
# (20:47: Mantle on the bar between the lens and the near speaker, in its own pool, big enough to read; it sits below
# the speaker's foot in the frame, so it covers none of it)
MANTLE = (8.5, Y_BAR + 0.12, R.COUNTER['top_z'] + 0.001)
MANTLE_RZ = 25.0
# (18:36: no lamp across a speaker, every shade whole, one over Mantle so it sits in a pool: five, between the bays)
HEMIS = [('dust', 6.18, -0.02, 1.80), ('ember', 6.54, 0.12, 1.66), ('acid', 6.92, -0.04, 1.86), ('ember', 7.3, 0.08, 1.74),
         ('dust', 7.66, -0.03, 1.82)]
CORES = [('ember', 6.05, -0.14), ('dust', 7.05, -0.2), ('acid', 7.8, -0.12)]     # (18:36: all three in frame, none before Mantle)
EV, WB = -2.0, 4000          # (20:47: the near Cores pale at -1.5: half a stop down, the room lifted by its declared fill)
TRACK = 3.0                  # the declared track lights' scale (tests 1-4: too dark)
# (20:47: the bays' pools a stop and a half too strong, aim near 1.6x the wall; the room lifted for the half stop down)
WALL, BAY, HOUSE = 1.7, 5.5, 0.6
HORN = 1.5


def _room():
    s = json.loads(subprocess.run(['git', 'show', f'{SRC[0]}:{SRC[1]}'], capture_output=True, check=True, cwd=ROOT).stdout)
    room = copy.deepcopy(s['set']['props'][0])
    room.update(DARK)
    room.update({'street': False, 'tropos_feet': True, 'host_stand': False, 'products_only': True, 'life_glasses': [],
                 'life_sleeves': []})
    return s, room


def _lamps(hemis, cores):
    # (no led_k: the lamps lane's own LED colours; its Core loadings, 0.5 x TINT_LOAD, as CORE_LOAD)
    return {'kind': 'kit', 'shape': 'ext', 'path': LAMPS, 'fn': 'lamps', 'top_z': R.CEIL, 'core_load': shots.CORE_LOAD, 'core_cable': False,
            'hemispheres': [{'tint': shots.KEY[t], 'x': x, 'y': round(Y_BAR + dy, 3), 'rim_z': z} for t, x, dy, z in hemis],
            'cores': [{'tint': shots.KEY[t], 'x': x, 'y': round(Y_BAR + dy, 3), 'floor_z': TOP, 'rot': 0.0} for t, x, dy in cores]}


def _life():
    """People were just here, and the music is on (the owner, 17:36: "anemic in soul"): two drinks mid-evening with ice
    and a twist, a bar cloth, a bowl of citrus (scanned), a book of matches, a folded newspaper; the now-playing sleeve
    standing by Mantle, a small stack waiting, a few sleeves pulled half out of the wall (invented covers); a worn
    runner on the concrete, a plant (scanned); and the one wry detail, a RESERVED card at the foot of the far speaker's bay.
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
    out += [{'kind': 'kit', 'shape': 'box', 'size': [0.22, 0.13, 0.014], 'position': [6.62, Y_BAR + 0.26, T], 'rotate': [0, 0, -14.0],
             'material': 'cotton', 'color': '#CFC6B4', 'ease': 0.004},                                          # a bar cloth
            {'kind': 'kit', 'shape': 'asset', 'model': 'wooden_bowl_01', 'res': '2k', 'position': [6.4, Y_BAR + 0.18, T], 'rotate': [0, 0, 30.0]},
            {'kind': 'kit', 'shape': 'asset', 'model': 'food_lime_01', 'res': '2k', 'position': [6.38, Y_BAR + 0.17, T + 0.03], 'rotate': [0, 20, 0]},
            {'kind': 'kit', 'shape': 'asset', 'model': 'food_lime_01', 'res': '2k', 'position': [6.44, Y_BAR + 0.21, T + 0.032], 'rotate': [30, 0, 90]},
            {'kind': 'kit', 'shape': 'asset', 'model': 'lemon', 'res': '2k', 'position': [6.35, Y_BAR + 0.23, T + 0.035], 'rotate': [0, 70, 20]},
            {'kind': 'kit', 'shape': 'box', 'size': [4.2, 1.6, 0.008], 'position': [6.9, 2.75, 0.001],
             'material': 'pbr', 'texture': 'poly_wool_herringbone', 'tex_res': '2k', 'tint': '#6A4A36', 'tint_mix': 0.55, 'gain': 0.7},   # a runner
            {'kind': 'kit', 'shape': 'asset', 'model': 'potted_plant_02', 'res': '2k', 'position': [8.85, 2.35, 0.0], 'rotate': [0, 0, 40.0]}]
    out.append({'kind': 'kit', 'shape': 'box', 'size': [0.2, 0.05, 0.022], 'position': [MANTLE[0] + 0.42, MANTLE[1] + 0.22, T], 'rotate': [0, 0, 20.0],
                'material': 'pbr', 'texture': 'american_walnut_veneer', 'tex_res': '2k', 'tint': '#5A3824', 'tint_mix': 0.5, 'gain': 0.6, 'ease': 0.003})
    bds = [  # the now-playing sleeve on a small walnut stand by Mantle
           {'image': 'tex/cover-05.png', 'w': 0.18, 'h': 0.18, 'x': MANTLE[0] + 0.42, 'y': MANTLE[1] + 0.21, 'z': T + 0.022, 'rot': [-14.0, 0, 20.0], 'ground': '#EFEBE3', 'rough': 0.85},
           # a small stack waiting, on the bar top's back half
           *[{'image': f'tex/cover-{k:02d}.png', 'w': 0.315, 'h': 0.315, 'x': 8.0 + 0.006 * j, 'y': Y_BAR + 0.05 + 0.004 * j, 'z': T + 0.004 * j,
              'rot': [-90.0, 0, [4.0, -6.0, 9.0, -3.0][j]]} for j, k in enumerate((9, 2, 12, 7))],
           # sleeves pulled half out of the wall's cells, their faces turned a little to the room
           *[{'image': f'tex/cover-{k:02d}.png', 'w': 0.315, 'h': 0.315, 'x': x, 'y': R.RECORD_WALL['y'] - 0.14, 'z': z, 'rot': [-4.0, 0, rz],
              'ground': '#E9E3D6'} for k, x, z, rz in ((3, 4.4, 1.565, 70.0), (10, 9.6, 1.925, -64.0), (14, 6.6, 2.285, 58.0))],
           {'image': 'tex/matches.png', 'w': 0.04, 'h': 0.064, 't': 0.006, 'x': 7.05, 'y': Y_BAR - 0.25, 'z': T, 'rot': [-90.0, 0, 22.0]},
           {'image': 'tex/newspaper.png', 'w': 0.29, 'h': 0.4, 't': 0.006, 'x': 6.6, 'y': Y_BAR - 0.34, 'z': T, 'rot': [-90.0, 0, -11.0],
            'ground': '#E4E0D6', 'rough': 0.85},
           # the wry detail: the speaker's seat is taken
           {'image': 'tex/reserved.png', 'w': 0.1, 'h': 0.05, 't': 0.002, 'x': 5.55, 'y': SPK_Y - 0.27, 'z': FEET_BAR, 'rot': [-18.0, 0, 0.0],
            'ground': '#EFEBE3', 'rough': 0.7}]
    out.append({'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'boards', 'boards': bds})
    # (test 2: the room's old DJ station left a mixer and two records floating where the old players stood: out)
    out.append({'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'remove', 'names': ['dj-plinths', 'dj-knobs', 'dj-records', 'dj-labels', 'screen-panels', 'screen-boxes', 'screen-frames']})
    # cozy (the owner, 17:39: "Soul to me means lived in. Cozy."): a worn leather armchair at the frame's left, books
    # among the records (cloth spines, stacked and leaning, in cells the records left empty)
    out.append({'kind': 'kit', 'shape': 'asset', 'model': 'ArmChair_01', 'res': '2k', 'position': [5.35, 2.05, 0.0], 'rotate': [0, 0, -120.0]})   # foreground, soft
    return out


def _track():
    """Declared, above the frame: a bar's track lights, small gridded heads throwing pools with falloff onto the record
    wall and down onto the bar top; warm."""
    out = {}
    for k, x in enumerate((4.3, 6.2, 7.0, 9.0, 9.8)):        # (20:47: off the bays, so the speakers take only their own pool)
        out[f'track-wall{k}'] = {'type': 'area', 'size_m': [0.12, 0.12], 'position': [x, 4.9, R.CEIL - 0.05], 'target': [x + 0.1, R.RECORD_WALL['y'], 1.7],
                                 'irradiance': round(WALL * TRACK, 3), 'spread_deg': 20, 'color': '#FFD2A0'}
    for k, x in enumerate((5.6, 7.0, 8.4)):
        out[f'track-bar{k}'] = {'type': 'area', 'size_m': [0.12, 0.12], 'position': [x, Y_BAR - 0.6, R.CEIL - 0.05], 'target': [x, Y_BAR, TOP],
                                'irradiance': round(0.35 * TRACK, 3), 'spread_deg': 24, 'color': '#FFD2A0'}
    for k, xc in enumerate(R.SPK_NICHES):                     # (18:36: a pool on each bay, so the whole speaker reads)
        # (18:40: the cabinet glows as on the stage picture, the bay's own back and sides darker: strong, narrow, onto the speaker)
        out[f'track-bay{k}'] = {'type': 'area', 'size_m': [0.14, 0.14], 'position': [xc, SPK_Y - 0.45, R.CEIL - 0.05], 'target': [xc, SPK_Y - 0.05, FEET_BAR + 0.7],   # (20:47: steep, from above: the cone in its cabinet's shade
                                'irradiance': round(BAY * TRACK, 3), 'spread_deg': 14, 'color': '#FFE2C0'}
    out['track-mantle'] = {'type': 'area', 'size_m': [0.1, 0.1], 'position': [MANTLE[0] + 0.4, 3.0, R.CEIL - 0.05],
                           'target': [MANTLE[0], MANTLE[1], MANTLE[2]], 'irradiance': round(3.5 * TRACK, 3), 'spread_deg': 18, 'color': '#FFD8B0'}   # (22:32: the Ember plinth's colour)
    # (18:36: the dark warm, not black: a broad low warm fill from the room behind the camera)
    for k, xc in enumerate(R.SPK_NICHES):                     # (22:32: the horn's shape and throat: a head of its own, from the room side)
        out[f'track-horn{k}'] = {'type': 'area', 'size_m': [0.12, 0.12], 'position': [xc + 0.3, 4.4, R.CEIL - 0.05],
                                 'target': [xc, SPK_Y - 0.15, FEET_BAR + 1.12], 'irradiance': round(HORN * TRACK, 3), 'spread_deg': 12,
                                 'color': '#FFE2C0'}
    out['house'] = {'type': 'area', 'size_m': [1.6, 1.6], 'position': [6.9, 0.6, 2.3], 'target': [6.9, 4.5, 1.0],
                    'irradiance': round(HOUSE * TRACK, 3), 'color': '#FFC890'}
    for v in out.values():                                     # (22:32: round heads, so a gloss shows no hard-edged shape)
        v['shape'] = 'DISK'
    return out


def _base(size, title):
    src, room = _room()
    s = shots._cast_base()
    k = shots.HERO_ORDER.index('acid')                  # (18:40: Acid, the lightest of the warm three, reads against walnut)
    pair = []
    for blk in s['products']:
        i = blk['instances'][k]
        pair.append({**blk, 'instances': [{**copy.deepcopy(i), 'position': [x, SPK_Y, FEET_BAR], 'rotate_z': 0.0} for x in R.SPK_NICHES]})
    s['products'] = pair
    shots._approved(s, order=['acid', 'acid'])
    s['products'].append(shots._mantle(*MANTLE, MANTLE_RZ, tint='ember'))
    RW = R.RECORD_WALL
    fill = {'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'fill_records', 'x0': RW['x0'], 'x1': RW['x1'], 'z0': RW['z0'], 'z1': RW['z1'],
            'cell': RW['cell'], 'y': RW['y'], 'depth': RW['depth'], 'skip': [[xc - 0.42, xc + 0.42, 0.0, 4.0] for xc in R.SPK_NICHES]}
    # (the owner, 15:43: no zinc, no brass; 20:47: the bar top dark, low roughness, carrying soft reflections of the
    # Cores and shades; the niches' felt plain)
    style = {'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'restyle',
             'swap': {'zinc': {'kind': 'stone', 'color': '#1C1916', 'rough': 0.16},
                      'brass': {'kind': 'plain', 'color': '#161616', 'rough': 0.45, 'metal': 0.6},
                      'kit-felt': {'kind': 'plain', 'color': '#1A1918', 'rough': 0.95}}}
    s['set'] = {'kind': 'stage', 'props': [room, fill] + _life() + [style]}
    s.pop('haze', None)                                   # (20:47: no visible beams: no haze)
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
    _raise_flat(s)
    return s


def _raise_flat(s):
    """A flat board's printed face sits at its z with its thickness below it: one lying on the bar top at TOP is coplanar
    with the stone and renders black (the matchbook in round 4; the hero test's boards, 2026-11-13). Each one raised by its
    thickness, in every frame built from here on."""
    for pr in s['set']['props']:
        if pr.get('fn') == 'boards':
            for b in pr['boards']:
                tb = b.get('t', 0.003)
                if b.get('rot', [0])[0] == -90.0 and abs(b.get('z', 0) - TOP) < tb:
                    b['z'] = round(TOP + tb + 0.0005, 4)


def _move_drink(pr, dx, dy):
    """Move one of the two drinks (glass, contents, ice, twist: set at x < 6.5 on the bar top) by dx, dy."""
    if pr.get('shape') == 'lathe' and abs(pr['position'][1] - (Y_BAR - 0.16)) < 0.2 and pr['position'][0] < 6.5:
        pr['position'] = [pr['position'][0] + dx, pr['position'][1] + dy, pr['position'][2]]
    if pr.get('shape') == 'box' and pr.get('material') == 'frosted' and pr['position'][0] < 6.5 and pr['position'][2] > 1.0:
        pr['position'] = [pr['position'][0] + dx, pr['position'][1] + dy, pr['position'][2]]
    if pr.get('shape') == 'tube' and pr['points'][0][0] < 6.5:
        pr['points'] = [[q[0] + dx, q[1] + dy, q[2]] for q in pr['points']]


DRINK_DX = 2.0                                           # the two drinks, just left of Mantle


def bar_backbar():
    """From a seat at the bar, across the bar top to the record wall: both Tropos in their bays, Mantle between,
    Hemispheres above, Cores on the bar; 40 mm, a little off axis, some depth of field."""
    s = _base([1920, 1080], 'Planet EARF bar: the record wall from a seat at the bar')
    s['set']['props'].append(_lamps(HEMIS, CORES))
    # (test 1: the bays cut by the frame: a seat pulled back, 30 mm, a little off axis)
    # (17:39 "cozy": closer and lower, from a stool at the bar at a seated eye, the room wrapping round; 26 mm so both
    # bays stay whole)
    # (18:40: a three-quarter view from a seat near the bar's right end: the near speaker whole, about two thirds of the
    # frame's height, nothing across it; the wall of records running away to the far speaker, whole; the Hemispheres
    # receding over the bar; a Core and the drinks on the bar in front; Mantle further along under its lamp)
    s['camera'] = {'position': [9.3, 3.5, 1.42], 'target': [7.0, 5.7, 1.72], 'lens_mm': 24.0, 'level': True,
                   'fstop': 2.8, 'focus': [8.25, 5.5, 1.7]}
    for pr in s['set']['props']:                                 # (20:47 proof: the now-playing sleeve at the frame's edge, too big: out)
        if pr.get('fn') == 'boards':
            pr['boards'] = [b for b in pr['boards'] if 'cover-05' not in b['image']]
    s['set']['props'] = [pr for pr in s['set']['props'] if not (pr.get('texture') == 'american_walnut_veneer' and pr.get('size') == [0.2, 0.05, 0.022])]
    s['lights'].pop('track-wall0', None)
    # (the audit: from this seat the far bay's head sat in the frame's top, 0.033 %: further toward the room, aimed a
    # little higher so its cone stays in the cabinet's shade)
    s['lights']['track-bay0'] = {**s['lights']['track-bay0'], 'position': [R.SPK_NICHES[0], 4.4, R.CEIL - 0.05],
                                 'target': [R.SPK_NICHES[0], SPK_Y - 0.05, FEET_BAR + 0.95],
                                 'irradiance': round(s['lights']['track-bay0']['irradiance'] * 2.2, 3)}   # (22:32: the far speaker back)
    # (22:32: the top left black, not warm dark: a little declared warm fill there, from out of frame at the left)
    # (round 4 proof: the smaller house disc washed the throw and the near stone; this frame has no ball to reflect it
    # clipped, so its round 3 fill: 3 m, nearer the front wall)
    s['lights']['house'] = {**s['lights']['house'], 'size_m': [3.0, 3.0], 'position': [6.9, 0.2, 2.6]}
    s['lights']['house-left'] = {'type': 'area', 'shape': 'DISK', 'size_m': [2.0, 2.0], 'position': [4.6, 2.2, 3.0],
                                 'target': [4.0, 5.6, 2.6], 'irradiance': round(0.5 * TRACK, 3), 'color': '#FFC890'}
    # (22:32: the near horn's shape: polished, it shows only what it mirrors; a graduated warm card over the bay's front,
    # seen only in reflections, so the flare carries a soft ramp along its curve)
    # (22:32: Mantle's Ember shows in its plinth's layered sides: a low head from behind the seat onto its front face)
    s['lights']['mantle-front'] = {'type': 'area', 'shape': 'DISK', 'size_m': [0.15, 0.15], 'position': [9.7, 3.15, 1.55],
                                   'target': [MANTLE[0], MANTLE[1] - 0.12, MANTLE[2] + 0.04], 'irradiance': round(5.0 * TRACK, 3),
                                   'spread_deg': 14, 'color': '#FFD8B0'}
    # (the plinth is clear Ember acrylic in layers: its colour shows where light passes through, so a low head from just
    # past the frame's right edge, through it from the side)
    s['lights']['mantle-side'] = {'type': 'area', 'shape': 'DISK', 'size_m': [0.2, 0.2], 'position': [9.45, 4.25, 1.2],
                                  'target': [MANTLE[0], MANTLE[1], MANTLE[2] + 0.03], 'irradiance': round(6.0 * TRACK, 3),
                                  'spread_deg': 8, 'color': '#FFD8B0'}   # (round 4 full: wider, it carried past Mantle onto the throw)
    s['lights']['horn-card'] = {'type': 'panel', 'size_m': [1.4, 0.9], 'position': [8.05, 4.9, R.CEIL - 0.06],
                                'target': [R.SPK_NICHES[1], SPK_Y - 0.1, FEET_BAR + 1.1], 'strength': 10.0, 'diffuse': 0.0, 'specular': 1.0,
                                'color': '#FFE2C0', 'ramp': {'axis': 'x', 'at_m': [7.4, 8.05, 8.7], 'values': [0.25, 1.0, 0.25]}}                         # (this view sees that head: the audit, 0.03 %)
    for pr in s['set']['props']:                                 # a Core and the drinks on the bar in front of the seat
        if pr.get('fn') == 'lamps':
            # ember by the throw, dust and acid further along; none before Mantle
            pr['cores'] = [{**c, 'x': x, 'y': y} for c, (x, y) in zip(pr['cores'], ((7.32, Y_BAR - 0.1), (6.05, Y_BAR - 0.08), (6.95, Y_BAR + 0.15)))]
    for pr in s['set']['props']:
        if pr.get('shape') == 'lathe' and abs(pr['position'][1] - (Y_BAR - 0.16)) < 0.2 and pr['position'][0] < 6.5:
            pr['position'] = [pr['position'][0] + DRINK_DX, pr['position'][1] - 0.05, pr['position'][2]]
        if pr.get('shape') in ('box', 'tube') and pr.get('material') in ('frosted', 'clay') and pr.get('position', [0])[0] < 6.5 and pr.get('position', [0, 0, 0])[2] > 1.0:
            pr['position'] = [pr['position'][0] + DRINK_DX, pr['position'][1] - 0.05, pr['position'][2]]
        if pr.get('shape') == 'tube' and pr['points'][0][0] < 6.5:
            pr['points'] = [[q[0] + DRINK_DX, q[1] - 0.05, q[2]] for q in pr['points']]
    # cozy (20:47): a wool throw left folded loosely on the bar by the Ember Core, in the near left
    s['set']['props'].append({'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'fold', 'x': 7.86, 'y': Y_BAR - 0.16, 'z': TOP,
                              'rz': 90.0, 'w': 0.42, 'legs': [0.36, 0.3, 0.22], 'rr': 0.016, 't': 0.01, 'color': '#9C4A26'})
    return s


def core_bar_table():
    """One Core on this bar's top, the record wall soft behind, the ball as a lit lamp (the lamps lane's Core exposure)."""
    s = _base([1920, 1280], 'Planet EARF bar: one Core on the bar top')
    s['set']['props'].append(_lamps([], [('ember', 7.05, -0.1)]))
    # (18:36: the now-playing sleeve out of the close-up; the base given the samples it needs)
    for pr in s['set']['props']:
        if pr.get('fn') == 'boards':
            pr['boards'] = [b for b in pr['boards'] if 'cover-05' not in b['image'] and 'matches' not in b['image']]   # (22:32: the matches, a black square before the base)
    s['render'].update(samples=512, adaptive=0.004)
    s['camera'] = {'position': [7.3, Y_BAR - 1.25, TOP + 0.2], 'target': [7.05, Y_BAR - 0.1, TOP + 0.12], 'lens_mm': 85.0, 'level': True,
                   'fstop': 2.0, 'focus': [7.05, Y_BAR - 0.1, TOP + 0.12]}
    s['render']['exposure'] = -1.0
    s['lights'] = {k: {**v, 'irradiance': round(v['irradiance'] * 2 ** (-1.5 + 1.0), 4)} for k, v in s['lights'].items()}   # (its room as approved)
    return s


def bar_backbar_full():
    """bar-backbar at full size (the coordinator, 00:33: 3200 wide, samples enough that the denoiser paints nothing)."""
    s = bar_backbar()
    s['size'] = [3200, 1800]
    s['render'].update(samples=256, adaptive=0.005)
    return s


def core_bar_table_full():
    s = core_bar_table()
    s['size'] = [3200, 2133]
    return s


def bar_backbar_portrait():
    """For phones, its own framing from the same seat (00:33): the near speaker whole in its bay, Mantle and a Core on
    the bar below it, two Hemispheres at the top (hung higher for this frame, beside the speaker's top, none across it)."""
    s = bar_backbar()
    s['title'] = 'Planet EARF bar: the near speaker from a seat at the bar (portrait)'
    s['size'] = [2400, 3000]
    s['render'].update(samples=224, adaptive=0.005)
    for pr in s['set']['props']:
        if pr.get('fn') == 'lamps':
            # (07:22: no product the blurred foreground shape: the Ember Core back beside Mantle, whole, base and all,
            # at the bar's back where the stack lay, about 1.5 m from the lens)
            pr['cores'] = [{**c, 'x': 8.17, 'y': round(Y_BAR + 0.22, 3)} if c['tint'] == shots.KEY['ember'] else c for c in pr['cores']]   # (proof: at 8.05 a glass hid its base)
            pr['hemispheres'] = pr['hemispheres'] + [{'tint': shots.KEY['acid'], 'x': 8.4, 'y': 4.55, 'rim_z': 2.2},
                                                     {'tint': shots.KEY['ember'], 'x': 7.85, 'y': 4.45, 'rim_z': 2.3}]
        if pr.get('fn') == 'boards':                       # the stack, left out of frame
            pr['boards'] = [{**b, 'x': round(b['x'] - 0.38, 3)} if b.get('rot', [0])[0] == -90.0 and b['w'] == 0.315 and abs(b['x'] - 8.0) < 0.05 else b
                            for b in pr['boards']]
    import math
    a, e = math.radians(126.0), math.radians(3.0)        # (the audit: at 30 mm the horn card and two heads in the top)
    c = [9.3, 3.5, 1.42]
    # (07:22: the Core sharp as well as the speaker: f/5.6, focused between them, 1.95 m; both in the depth of field)
    s['camera'] = {'position': c, 'target': [c[0] + 3 * math.cos(a), c[1] + 3 * math.sin(a), c[2] + 3 * math.tan(e)], 'lens_mm': 35.0,
                   'level': True, 'fstop': 5.6, 'focus': [8.15, 5.07, 1.45]}
    return s


PEND_HEMIS = [('acid', 6.55, 0.06, 1.59), ('ember', 6.75, -0.10, 1.44), ('dust', 6.93, 0.14, 1.70), ('ember', 7.11, -0.04, 1.50),
              ('acid', 7.29, 0.10, 1.63)]


def bar_pendants():
    """Test frame (00:33): the Hemispheres over the bar, close to medium, their pools on the dark stone, a Core and the
    drinks under them, the record wall soft behind."""
    # (proof: from the room side at 35 mm both bays sat cut at the frame's edges: square, 61 mm, the wall's frame
    # between the bays only; three Hemispheres, two Cores and the drinks under them)
    s = _base([1920, 1920], 'Planet EARF bar: the Hemispheres over the bar')
    # (07:22: a real cluster: five close together at staggered heights, each whole with its cap and some cord, hung low
    # over the bar so their pools show on the stone; two Cores under them, their bases showing; the drinks)
    s['set']['props'].append(_lamps(PEND_HEMIS, [('ember', 6.66, -0.12), ('dust', 7.26, -0.06)]))
    for pr in s['set']['props']:
        if pr.get('fn') == 'boards':
            pr['boards'] = [b for b in pr['boards'] if not any(k in b['image'] for k in ('newspaper', 'cover-05', 'matches'))]
        _move_drink(pr, 0.78, 0.0)
    s['set']['props'] = [pr for pr in s['set']['props'] if not (pr.get('texture') == 'american_walnut_veneer' and pr.get('size') == [0.2, 0.05, 0.022])]
    s['render'].update(samples=256, adaptive=0.005)
    # (07:45: the stone stays, so the cluster's light shows on what a bar has under it: the newspaper open flat, a linen
    # napkin, a sleeve face up, the cloth, the bowl of citrus, the drinks with their ice)
    s['set']['props'] += [
        {'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'boards', 'boards': [
            # (proof: a flat board's printed face sits at its z, its thickness below: at TOP it was coplanar with the stone
            # and rendered black, as the matches did in round 4: each one raised by its thickness)
            {'image': 'tex/newspaper.png', 'w': 0.29, 'h': 0.4, 't': 0.006, 'x': 6.97, 'y': round(Y_BAR + 0.16, 3), 'z': TOP + 0.0065, 'rot': [-90.0, 0, 82.0],
             'ground': '#E4E0D6', 'rough': 0.85},
            {'image': 'tex/cover-09.png', 'w': 0.315, 'h': 0.315, 't': 0.003, 'x': 6.41, 'y': round(Y_BAR - 0.14, 3), 'z': TOP + 0.0035, 'rot': [-90.0, 0, 0.0],
             'ground': '#E9E3D6', 'rough': 0.7}]},
        {'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'fold', 'x': 7.24, 'y': round(Y_BAR - 0.26, 3), 'z': TOP, 'rz': -15.0,   # (proof: behind the Dust Core: to its front)
         'w': 0.18, 'legs': [0.12, 0.09, 0.06], 'rr': 0.006, 't': 0.004, 'color': '#D8CCB8', 'seed': 5}]
    for k in [k for k in s['lights'] if k.startswith('track-bar')]:      # (07:22: the pools faint: the bar's own heads off here)
        s['lights'].pop(k)
    s['lights']['house'] = {**s['lights']['house'], 'irradiance': round(s['lights']['house']['irradiance'] * 0.5, 3)}
    # (proof: at 50 mm from 1.75 m the far bay stood cut at the edge: from further back, 100 mm, the wall's span between
    # the bays only, a little above so the bar top shows the pools)
    s['camera'] = {'position': [6.92, 1.0, 2.1], 'target': [6.92, Y_BAR, 1.5], 'lens_mm': 100.0, 'level': True,
                   'fstop': 4.0, 'focus': [6.92, Y_BAR - 0.02, 1.4]}
    return s


def mantle_bar():
    """Test frame (14:33 notes): Mantle in Ember on the bar seen from a seat, three-quarter, the record and the arm from
    above; a Hemisphere hung over it lights the deck and makes the Ember plinth's edges glow; an Ember Core beside it;
    the near speaker soft behind. No declared key: the products light it."""
    s = bar_backbar()
    s['title'] = 'Planet EARF bar: Mantle on the bar'
    s['size'] = [1920, 1280]
    s['render'].update(samples=256, adaptive=0.005)
    life = _life()
    stand = next(pr for pr in life if pr.get('texture') == 'american_walnut_veneer' and pr.get('size') == [0.2, 0.05, 0.022])
    sleeve = next(b for pr in life if pr.get('fn') == 'boards' for b in pr['boards'] if 'cover-05' in b['image'])
    import math
    a = math.radians(MANTLE_RZ)
    fwd = (math.sin(a), -math.cos(a)); right = (math.cos(a), math.sin(a))     # Mantle's front, and its right as one faces it
    # Mantle's middle: the asset's origin is its front left corner, 0.46 wide and 0.42 deep
    cen = (MANTLE[0] + 0.23 * right[0] - 0.21 * fwd[0], MANTLE[1] + 0.23 * right[1] - 0.21 * fwd[1])
    # the now-playing sleeve on its stand behind Mantle's left, muted (07:22)
    sx, sy = cen[0] + 0.36 * right[0] - 0.30 * fwd[0], cen[1] + 0.36 * right[1] - 0.30 * fwd[1]   # (proofs 7, 8: cut at the frame's left: behind its right)
    stand = {**stand, 'position': [sx, sy, TOP], 'rotate': [0, 0, MANTLE_RZ + 10.0]}
    sleeve = {**sleeve, 'image': 'tex/cover-00.png', 'ground': '#1C1B1A', 'rough': 0.8, 'x': sx, 'y': sy - 0.01, 'rot': [-14.0, 0, MANTLE_RZ + 10.0]}
    keep = []
    for pr in s['set']['props']:
        if pr.get('shape') in ('lathe', 'tube') or (pr.get('shape') == 'box' and pr.get('material') == 'frosted'):
            continue                                               # the drinks
        if pr.get('fn') == 'boards':
            pr = {**pr, 'boards': [b for b in pr['boards'] if not (b.get('rot', [0])[0] == -90.0 and b['w'] == 0.315)]}   # the stack
        keep.append(pr)
    s['set']['props'] = keep + [stand, {'kind': 'kit', 'shape': 'ext', 'path': LIFE, 'fn': 'boards', 'boards': [sleeve]}]
    # (14:33: a Hemisphere over Mantle, its light on the deck and through the Ember plinth's edges, as the portrait's left
    # edge; the Ember Core beside it, not behind; posts black: the low heads on Mantle off, the fills down)
    for pr in s['set']['props']:
        if pr.get('fn') == 'lamps':
            # (proofs 7, 8: on the right, the side away from the lens, the plinth's edge showed nothing: on its left, the side
            # the lens sees, close, so its light enters that edge, as the Core beside it does in the portrait)
            pr['cores'] = [{'tint': shots.KEY['ember'], 'x': round(cen[0] - 0.33 * right[0] - 0.08 * fwd[0], 3),
                            'y': round(cen[1] - 0.33 * right[1] - 0.08 * fwd[1], 3), 'floor_z': TOP, 'rot': 0.0}]
            pr['hemispheres'] = [h for h in pr['hemispheres'] if h['x'] < 7.4] + [
                {'tint': shots.KEY['ember'], 'x': round(cen[0], 3), 'y': round(cen[1], 3), 'rim_z': MANTLE_HEMI_Z}]
    for k in ('mantle-front', 'mantle-side', 'track-mantle'):
        s['lights'].pop(k, None)
    for k in ('house', 'house-left'):
        s['lights'][k] = {**s['lights'][k], 'irradiance': round(s['lights'][k]['irradiance'] * 0.25, 3)}
    s['render']['exposure'] = -1.0
    s['lights'] = {k: ({**v, 'irradiance': round(v['irradiance'] * 0.5, 4)} if 'irradiance' in v else {**v, 'strength': v['strength'] * 0.5})
                   for k, v in s['lights'].items()}
    # a seat at the bar, three-quarter from Mantle's front left: the eye 1.38 m, 45 mm, Mantle about half the width
    az = math.radians(MANTLE_CAM_AZ)
    d = MANTLE_CAM_D
    c = [cen[0] + d * (math.cos(az) * fwd[0] - math.sin(az) * right[0]), cen[1] + d * (math.cos(az) * fwd[1] - math.sin(az) * right[1]), 1.38]
    s['camera'] = {'position': [round(v, 4) for v in c], 'target': [cen[0] - 0.12 * right[0], cen[1] - 0.12 * right[1], MANTLE[2] + 0.12], 'lens_mm': 45.0,   # (proof 9: the Core cut at the left) 'level': True,
                   'fstop': 4.0, 'focus': [cen[0], cen[1], MANTLE[2] + 0.1]}
    return s



def mantle_bar_full():
    """mantle-bar at full size (the coordinator, 22:17: Acid did not read, so the Ember three-quarter at 2400 x 1600)."""
    s = mantle_bar()
    s['size'] = [2400, 1600]
    return s


MANTLE_HEMI_Z = 1.50           # the Hemisphere's rim over Mantle (the deck at about 1.23)
MANTLE_CAM_AZ, MANTLE_CAM_D = 35.0, 1.05


HERO_MANTLE_TINT = 'ember'      # Mantle's tint in the hero: the last Mantle test decides (the coordinator, 22:17)
HERO_CORES = [('acid', 5.95, 0.04), ('ember', 6.3, -0.12), ('dust', 7.65, -0.14)]   # (proof 1: 4.62 and 9.25 out of frame)


def bar_hero():
    """The line's hero from the bar (the owner, 23:48: "the bar pictures have been looking good"; the coordinator: one
    small test, 1600 x 900): the room from its best seat, wide and fairly frontal; both Tropos whole in their bays, Mantle
    on the bar between them with a record on, the Hemisphere cluster over it, Cores along the bar, the drinks, the
    newspaper and the citrus; nothing in front of a speaker; a calm darker area in the upper left third for a headline.
    Lit as the passed frames: the products' own lamps and the declared track heads out of frame."""
    s = _base(HERO_SIZE, 'Planet EARF bar: the line from the best seat')
    # (proof 2: the bar's long row hung two shades before the horns: the passed pendants' cluster instead, between the
    # bays, 0.15 higher so Mantle reads under it)
    s['set']['props'].append(_lamps([(t_, x_, dy_, z_ + 0.15) for t_, x_, dy_, z_ in PEND_HEMIS], HERO_CORES))
    # Mantle between the bays under the cluster (at 8.5 it stood on the bar before the right speaker's feet), a little
    # turned to the seat so the record reads; the asset's origin is its front left corner, 0.46 wide, 0.42 deep
    import math
    rz = 10.0; a = math.radians(rz)
    fwd = (math.sin(a), -math.cos(a)); right = (math.cos(a), math.sin(a))
    cx, cy = 6.92, Y_BAR + 0.08
    ox, oy = cx - 0.23 * right[0] + 0.21 * fwd[0], cy - 0.23 * right[1] + 0.21 * fwd[1]
    s['products'] = [b for b in s['products'] if 'Mantle' not in b.get('collection', '')] + \
        [shots._mantle(round(ox, 4), round(oy, 4), MANTLE[2], rz, tint=HERO_MANTLE_TINT)]
    s['lights']['track-mantle'] = {**s['lights']['track-mantle'], 'position': [cx + 0.4, 3.0, R.CEIL - 0.05], 'target': [cx, cy, MANTLE[2]]}
    # the upper left third calm and dark for the headline: no wall head there
    s['lights'].pop('track-wall0', None)
    # the frame: from a stool at the bar's middle, centred between the bays (proof 1, from across the room at y 0.95:
    # everything small, the stools across the foot); the eye 1.6 m, so the Cores and Mantle on the bar stay under the
    # line to the speakers' feet
    s['camera'] = {'position': [6.9, HERO_EYE_Y, 1.6], 'target': [6.9, 5.7, HERO_AIM_Z], 'lens_mm': HERO_LENS, 'level': True,   # (proof 2: the Cores cut at the foot)
                   'fstop': 5.6, 'focus': [6.9, 5.2, 1.6]}
    # (test 2, proof 1: at 21 mm from y 2.5 the bays' tops stood at 14 % from the top, inside the headline's band: the
    # stool 0.3 back and the view shifted up (level, so the verticals stay), the bays' tops under the top quarter; the
    # two wall heads between the bays aimed lower, so their pools stay off the upper shelves; no light added)
    for k_ in ('track-wall1', 'track-wall2'):
        if k_ in s['lights']:
            tg = list(s['lights'][k_]['target']); tg[2] = HERO_WALL_AIM_Z
            s['lights'][k_] = {**s['lights'][k_], 'target': tg}
    # (proof 2: with the view shifted up the ceiling shows at the top from y 4.99 back to the wall, and the two bay
    # heads at y 5.27 were in frame (the audit): moved forward on the track to y HERO_BAY_HEAD_Y, the same targets)
    for k_ in ('track-bay0', 'track-bay1'):
        if k_ in s['lights']:
            ps = list(s['lights'][k_]['position']); ps[1] = HERO_BAY_HEAD_Y
            s['lights'][k_] = {**s['lights'][k_], 'position': ps, 'irradiance': HERO_BAY_IRR[k_]}
    # (the coordinator, 03:46, full size: from 4.7 the heads washed the linings, 6-9 % of each cabinet clipped; lower,
    # to test 1's level. Nothing but shelves cut by the side edges: the room's own glasses (a coupe at the left edge, a
    # rocks glass at the right) out, and the now-playing sleeve and its stand, cut by the right edge, out as in the
    # other frames)
    for pr in s['set']['props']:
        if pr.get('fn') == 'remove':
            pr['names'] = pr['names'] + ['glasses-r36', 'pours-r36']
        if pr.get('fn') == 'boards':
            pr['boards'] = [b for b in pr['boards'] if 'cover-05' not in b['image']]
    s['set']['props'] = [pr for pr in s['set']['props'] if not (pr.get('texture') == 'american_walnut_veneer' and pr.get('size') == [0.2, 0.05, 0.022])]
    # (the coordinator, 01:54, test 2: a calm dark top band for the headline; the newspaper the brightest thing in the
    # picture: a dark-covered magazine in its place; the sleeve pulled out high on the wall, the triangle, down to the
    # lowest row)
    for pr in s['set']['props']:
        if pr.get('fn') == 'boards':
            for b_ in pr['boards']:
                if b_['image'] == 'tex/newspaper.png':
                    b_.update(image='tex/cover-08.png', w=0.23, h=0.3, t=0.004, ground='#1E1C1A', rough=0.6)
                    b_['z'] = round(TOP + 0.0045, 4)
                if b_['image'] == 'tex/cover-14.png' and b_['z'] > 2.0:
                    b_['z'] = 1.565
                if b_['image'] == 'tex/cover-10.png':     # (full size: the face-out sleeve on the wall cut by the right edge: in)
                    b_['x'] = HERO_COVER10_X
    return s


HERO_COVER10_X = 9.35      # (from 9.6)
HERO_SIZE = [3200, 1800]   # (the coordinator, 03:46: full size; test 2 was 1600 x 900)
HERO_LENS = 21.0     # (the coordinator, 01:54: option (b), both bays whole and smaller, more wall above them)
HERO_EYE_Y = 2.2     # (test 2: from 2.5)
HERO_AIM_Z = 1.85    # (test 2: from 1.55; with 'level' the engine shifts rather than tilts)
HERO_WALL_AIM_Z = 1.45   # (test 2: from 1.7)
HERO_BAY_HEAD_Y = 4.7    # (test 2: from 5.27, out of frame)
HERO_BAY_IRR = {'track-bay0': 2.0, 'track-bay1': 0.8}   # (full size: from 16.5, W/m2 at the target; proofed on crops: 8 still
#   washed the linings; off, they read 53 / 0.77 / 0.28; the right lining, seen more from the front, takes less for the same look)


SHOTS = {'bar-backbar': bar_backbar_full, 'core-bar-table': core_bar_table_full, 'bar-backbar-portrait': bar_backbar_portrait,
         'bar-pendants': bar_pendants, 'mantle-bar': mantle_bar_full, 'bar-hero': bar_hero}

if __name__ == '__main__':
    od = sys.argv[1]
    os.makedirs(od, exist_ok=True)
    for n, f in SHOTS.items():
        json.dump(f(), open(os.path.join(od, n + '.json'), 'w'), indent=1)
        print(n)
