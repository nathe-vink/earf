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

SRC = ('e7149388', 'renders/2026-10-20/barkhorn/planet38/finals-b/bar-smoke.shot.json')
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
CORES = [('ember', 5.6, -0.12), ('dust', 6.95, -0.15), ('acid', 8.1, -0.1)]
EV, WB = -1.5, 4000          # the lamps lane's finals: Core -1, Hemisphere -2, white balance 4000 K
TRACK = 1.0                  # the declared track lights' scale


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
                    'irradiance': round(0.05 * TRACK, 3), 'color': '#FFE0C0'}
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
    s['set'] = {'kind': 'stage', 'props': [room]}
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
    s['camera'] = {'position': [6.45, 1.95, 1.22], 'target': [6.95, 5.6, 1.6], 'lens_mm': 32.0, 'level': True,
                   'fstop': 4.0, 'focus': [6.9, 4.2, 1.2]}
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
