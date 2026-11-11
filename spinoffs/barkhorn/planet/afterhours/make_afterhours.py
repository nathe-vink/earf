"""AFTER HOURS AT PLANET EARF (the coordinator, 2026-11-11 04:20; the owner's pick for the site's home page): the bar
after closing, lit ONLY by the lamps EARF sells, at their real lumens. The whole family: five Hemisphere pendants in a
row over the counter in the warm tints, Core lamps along it like candles, Mantle on the counter with a record on, the
eight Tropos about the room like guests who stayed.

    python3 spinoffs/barkhorn/planet/afterhours/make_afterhours.py       # writes studio/shots/barkhorn/afterhours/hero.json
    LAMPS_ROOT=<checkout of r32-lamps-final> python3 studio/engine/render.py studio/shots/barkhorn/afterhours/hero.json --out X.png

The room is the bar of round 38 (e7149388, planet38 finals-b/bar-smoke), with every lamp, glow, strip, flame, lit
window, street lamp and sky taken out: the only emitters are the products' LEDs. Everything final as of 2026-11-11:
- Tropos: base A on its own feet (no plinth, no light), horn A polished, black rods (r33-speaker-horn 370de3da's
  product files); the eight tints by shots.py's SITE_TINTS.
- Hemisphere and Core: the lamp lane's own builders (lamps_final.py, r32-lamps-final), LED per tint as finalised:
  Ember 2200 K; Poison, Fog 2700 K; Haze 3000 K; Dust, Acid, Ice, Smoke 4000 K. Core's shells: Dust, Acid, Ice at 1.5
  (3x), Smoke 0.15 (the light grey), the rest 0.5.
- Mantle: Strata Float v3 (r48-mantle-design 450064b8), no light, smoked base.
"""
import copy, json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path[:0] = [os.path.join(HERE, '..', 'tropos-a'), os.path.join(HERE, '..', 'r37'), os.path.join(HERE, '..', 'r36')]
import r37_plan as R                                                   # noqa: E402
from make_listening import tropos, FEET_BAR                            # noqa: E402

SRC = ('e7149388', 'renders/2026-10-20/barkhorn/planet38/finals-b/bar-smoke.shot.json')
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'afterhours', 'hero.json')
TINT = {'ember': ('cloud-red', 'red'), 'dust': ('cloud-orange', 'orange'), 'acid': ('cloud-amber', 'amber'),
        'poison': ('eucalyptus-y2k-green', 'green'), 'ice': ('cloud-blue', 'blue'), 'haze': ('cloud-violet', 'violet'),
        'fog': ('birch-fog-clear', 'ice'), 'smoke': ('cloud-black', 'black')}       # shots.py SITE_TINTS (370de3da)
LED_K = {'red': 2200, 'green': 2700, 'ice': 2700, 'violet': 3000, 'orange': 4000, 'amber': 4000, 'blue': 4000, 'black': 4000}
CORE_LOAD = {'orange': 1.5, 'amber': 1.5, 'blue': 1.5, 'black': 0.15}
HEMI_LM, CORE_LM_OUT = 1000, {'ember': None, 'dust': 12.5, 'acid': 18.3, 'poison': None, 'ice': 6.6, 'haze': None,
                               'fog': None, 'smoke': 12.9}   # Core out of the ball at the final recipe (ae86581b lumens.txt; None: not measured at it)
Y_BAR = (R.COUNTER['y0'] + R.COUNTER['y1']) / 2
TOP = R.COUNTER['top_z']

# the room's own emitters, all off (planet_r36/37's parameters)
DARK = {k: 0.0 for k in ('dome_w', 'dome_glow', 'sphere_w', 'sphere_glow', 'disc_glow', 'disc_lamp', 'name_glow',
                         'niche_strip', 'sink_glow', 'sink_strip', 'sink_w', 'screen_glow', 'etch_glow', 'shade_glow',
                         'flat_glow', 'flame', 'windows_lit', 'counter_strip', 'sconce_w', 'sconce_glow',
                         'spk_niche_strip', 'plinth_bar', 'plinth_listen')}

PENDANTS = [(9.05, 'acid'), (7.85, 'ember'), (6.65, 'dust'), (5.45, 'fog'), (4.25, 'ember')]     # near to far
CORES = [(9.55, 'ice'), (8.45, 'poison'), (7.25, 'haze'), (5.95, 'smoke'), (4.85, 'dust'), (3.85, 'ember')]
MANTLE = (6.95, Y_BAR, TOP)
BOOTH_PENDANTS = [(8.52, 'dust'), (6.56, 'acid'), (4.6, 'ember')]          # over the booths' tables (a second row)
BOOTH_Y, BOOTH_RIM = 0.40, 1.50
GUESTS = [   # (x, y, z, facing deg (0 faces -y; 90 faces +x), tint)
    (3.15, 3.45, 0.0, 70.0, 'ember'), (3.15, 5.0, 0.0, 110.0, 'acid'),          # the pair at the counter's far end
    (5.55, R.BACKBAR_Y + 0.0662, FEET_BAR, 0.0, 'smoke'), (8.25, R.BACKBAR_Y + 0.0662, FEET_BAR, 0.0, 'fog'),   # the back bar's niches
    (9.35, 3.42, 0.0, 60.0, 'dust'), (6.15, 3.42, 0.0, 75.0, 'poison'),         # along the counter's front
    (7.54, 1.45, 0.0, 115.0, 'haze'), (5.58, 1.45, 0.0, 100.0, 'ice')]          # by the booths and the window wall


def shot():
    s = json.loads(subprocess.run(['git', 'show', f'{SRC[0]}:{SRC[1]}'], capture_output=True, check=True, cwd=ROOT).stdout)
    s = copy.deepcopy(s)
    s['title'] = 'AFTER HOURS AT PLANET EARF: the bar after closing, lit only by the lamps EARF sells (test, 2026-11-11)'
    s['size'] = [1600, 900]
    s['lights'] = {}                                                  # no lamp but the products' own
    s['sky']['strength'] = 0.0
    s['materials'] = {'glow': {'strength': 0.0},
                      'horn-satin': {'roughness': 0.05},
                      **{m: {'glow': 0.0} for m in ('uplight-edge', 'uplight-panel', 'uplight-wash', 'led', 'builtin-led', 'builtin-led-brace')}}
    room = s['set']['props'][0]
    room.update(DARK); room['street'] = False; room['tropos_feet'] = True; room['host_stand'] = False
    # keep the room and its life; drop the old lamps, the coin column's glow, the street lamps and the fan
    keep = []
    for pr in s['set']['props']:
        if pr is room or pr.get('fn') == 'bowl':
            keep.append(pr)
    keep.append({'kind': 'kit', 'shape': 'ext', 'path': 'spinoffs/barkhorn/planet/afterhours/lamps_final.py', 'fn': 'place',
                 'led_k': LED_K, 'core_load': CORE_LOAD,
                 'hemispheres': [{'tint': TINT[t][1], 'x': x, 'y': Y_BAR, 'rim_z': 1.82} for x, t in PENDANTS] +
                                [{'tint': TINT[t][1], 'x': x, 'y': BOOTH_Y, 'rim_z': BOOTH_RIM} for x, t in BOOTH_PENDANTS],
                 'cores': [{'tint': TINT[t][1], 'x': x, 'y': Y_BAR - 0.17, 'floor_z': TOP, 'rot': 200.0} for x, t in CORES]})
    s['set']['props'] = keep
    prods = []
    for x, y, z, rz, t in GUESTS:
        prods += tropos([{'position': [x, y, z], 'rotate_z': rz}], TINT[t][0])
    prods.append({'def': 'studio/products/mantle-strata-v3.json', 'flavour': 'smoke-2074',
                  'instances': [{'position': list(MANTLE), 'rotate_z': 0.0}]})
    s['products'] = prods
    s['camera'] = {'position': [11.35, 3.25, 1.10], 'target': [2.6, 4.05, 1.30], 'lens_mm': 30, 'level': True,
                   'fstop': 2.8, 'focus': [7.0, 4.0, 1.3]}
    # the lamp lane's own settings for these lamps (lamp_site.py): no clamp (the LEDs are tiny and very bright; a clamp
    # throws away the light the opal scatters), refractive and reflective caustics (the light leaves through clear
    # acrylic), 32 bounces of each kind (the opal cavities)
    s['render'] = {**s['render'], 'samples': 64, 'denoise': True, 'clamp': 0, 'exposure': 5.5, 'white_balance_k': 3000,
                   'bounces': 64, 'diffuse_bounces': 32, 'glossy_bounces': 32, 'transmission_bounces': 32,
                   'caustics_refractive': True, 'caustics_reflective': True}
    s['afterhours'] = {'pendants': PENDANTS, 'booth_pendants': BOOTH_PENDANTS, 'cores': CORES, 'mantle': MANTLE, 'guests': GUESTS, 'led_k': LED_K,
                       'core_load': CORE_LOAD, 'hemisphere_lm': HEMI_LM, 'core_lm_out': CORE_LM_OUT}
    return s


if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(shot(), open(OUT, 'w'), indent=1)
    print(OUT)
