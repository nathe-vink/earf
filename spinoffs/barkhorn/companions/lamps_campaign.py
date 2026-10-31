"""The campaign pictures (the coordinator, 2026-10-31, for the site, the deck and the press): Hemisphere over a dining
table at dusk, Core on a bedside at night, Mantle on a credenza with records, all three in one room, and macro
details. Each frame lights its lamp as the brightness study does (hemisphere_brightness.py: a Cycles watt of white
light is 683 lm, EV100 6, so a frame shows the light the fitting would give), and the rooms are dressed with Poly Haven
(CC0) furniture.

    python3 spinoffs/barkhorn/companions/lamps_campaign.py                       # the shots
    python3 spinoffs/barkhorn/companions/lamps_campaign.py --render NAME [...] [--scale 0.3 --samples 32 --out DIR]
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import hemisphere_brightness as HB                                  # noqa: E402
import lamps_final as LF                                            # noqa: E402
import lamps_pdp_r41 as P4                                          # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-campaign')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-31', 'barkhorn', 'lamps-campaign')
LM = 590.0                    # Hemisphere on its driver (round 42: ERP ESS010W-0180-42, 180 mA)
MANTLE = 'spinoffs/barkhorn/companions/out-turntable-float/open/barkhorn-turntable-float-open.json'


def asset(model, pos, rot=0.0, scale=1.0):
    return {'kind': 'kit', 'shape': 'asset', 'model': model, 'position': list(pos), 'rotate': [0, 0, rot], 'scale': scale}


def kit(shape, material, color, pos, **kw):
    return dict({'kind': 'kit', 'shape': shape, 'material': material, 'color': color, 'position': list(pos)}, **kw)


def dining_room(level='575', shade='ember'):
    """The brightness study's room at the design's light, its table swapped for a scanned dining table and chairs, a
    window in the left wall onto dusk."""
    s = HB.shot(level, shade)
    s['lights']['cob']['power_w'] = round(s['lights']['cob']['power_w'] * LM / HB.LEVELS[level], 4)
    st = s['set']
    tx, ty = HB.TABLE
    for p in st['props']:
        if p.get('fn') == 'dome':
            p['shade_glow'] = 0.8                    # the shade lit from inside (1.1 read pink through the red)
            p['materials'] = {'liner': {'glow_color': '#FF4A22'}}
        if p.get('kind') == 'lamp':
            p['off'] = True                           # the floor lamp competed with the pendant
    st['props'] += [asset('dining_chair_02', (tx - 0.42, ty - 0.68, 0.0), 0.0),
                    asset('dining_chair_02', (tx + 0.42, ty - 0.68, 0.0), 0.0),
                    asset('dining_chair_02', (tx - 0.42, ty + 0.68, 0.0), 180.0),
                    asset('dining_chair_02', (tx + 0.42, ty + 0.68, 0.0), 180.0),
                    asset('potted_plant_02', (-2.05, 2.75, 0.0), 30.0)]
    st['windows'] = [{'wall': 'left', 'along': 0.1, 'sill': 0.55, 'size': [1.7, 1.85], 'mullions': [2, 1],
                      'frame': '#2A2724'}]
    st['frame'] = '#2A2724'
    s['sky'] = {'kind': 'hdri', 'polyhaven': 'twilight_sunset', 'rotation_deg': 250.0, 'strength': 0.03, 'res': '4k'}
    s['render']['exposure'] = round(s['render']['exposure'] + 0.8, 3)     # a photographer's dusk, a stop up
    return s


def dining_dusk():
    s = dining_room()
    s['title'] = 'Hemisphere in Ember over a dining table at dusk, at 590 lm (the campaign)'
    s['size'] = [2400, 1600]
    s['lights'].pop('floorlamp', None)
    s['camera'] = {'position': [1.4, -0.65, 1.62], 'target': [-0.2, 1.1, 1.1], 'lens_mm': 32, 'level': True,
                   'fstop': 3.2, 'focus': [0.0, 0.95, 1.3]}
    s['set']['wall'] = {'color': '#8C8476'}
    return s


def box(material, color, size, pos, **kw):
    return kit('box', material, color, pos, size=list(size), **kw)


def bare_room(wall='#8C8476', floor=None):
    """The brightness study's room, emptied: no table, no pendant, no candles, its walls repainted; the sconces off."""
    s = HB.shot('575', 'ember')
    st = s['set']
    st['props'] = [p for p in st['props'] if p.get('kind') in ('frame',)]
    st['wall'] = {'color': wall}
    if floor:
        st['floor'] = floor
    s['lights'] = {}
    return s


def core_pool(s, x, y, z, flavour_light='#FF8A60', lm=200.0):
    for i, dx in enumerate((-0.095, 0.095)):
        s['lights'][f'corepool{i}'] = {'type': 'point', 'position': [x + dx, y - 0.02, z + 0.06],
                                       'power_w': round(lm * 0.25 / HB.LM_PER_W, 4), 'radius_m': 0.03,
                                       'color': flavour_light, 'camera': False, 'transmission': False, 'specular': 0.0}
    s['lights']['coreup'] = {'type': 'point', 'position': [x, y, z + 0.30], 'power_w': round(lm * 0.35 / HB.LM_PER_W, 4),
                             'radius_m': 0.08, 'color': flavour_light, 'camera': False, 'transmission': False,
                             'specular': 0.0}


def core_bedside():
    """Core in Ember on a bedside table at night: the only light in the room but a cool window."""
    s = bare_room(wall='#3C4250')
    st = s['set']
    bx, by = 0.55, 2.05                      # the bed's centre: its head at the back wall (y 3.15)
    st['props'] = [
        box('gloss', '#3A2A1E', (1.72, 2.1, 0.30), (bx, by, 0.0), roughness=0.55),
        box('cotton', '#ECE8E0', (1.62, 2.0, 0.22), (bx, by, 0.30)),
        box('wool', '#7F8794', (1.66, 1.45, 0.07), (bx, by - 0.3, 0.50)),
        box('cotton', '#F2EFE9', (0.62, 0.40, 0.15), (bx - 0.38, 2.86, 0.52), rotate_z=4),
        box('cotton', '#F2EFE9', (0.62, 0.40, 0.15), (bx + 0.38, 2.86, 0.52), rotate_z=-3),
        box('gloss', '#3A2A1E', (1.84, 0.06, 1.05), (bx, 3.10, 0.0), roughness=0.55),
        asset('side_table_01', (-0.62, 2.82, 0.0), 0.0),
        box('paper', '#2B3A4A', (0.17, 0.24, 0.025), (-0.70, 2.80, 0.55), rotate_z=8),
        box('paper', '#B8873C', (0.16, 0.23, 0.02), (-0.70, 2.80, 0.575), rotate_z=-4),
        kit('lathe', 'glass', '#F4F2EE', (-0.47, 2.70, 0.55),
            profile=[[0, 0], [0.032, 0], [0.034, 0.11], [0.0, 0.11]]),
        LF.core_piece(-0.62, 2.85, 0.55, 'ember', glow=0.35, rotate_z=-30),
        {'kind': 'frame', 'position': [bx, 3.15], 'z': 1.55, 'size': [0.9, 0.6], 'art': '#2E3C52'},
    ]
    st['windows'] = [{'wall': 'left', 'along': -0.4, 'sill': 0.75, 'size': [1.1, 1.5], 'mullions': [1, 1],
                      'frame': '#1E2024'}]
    s['sky'] = {'kind': 'gradient', 'zenith': '#1A2A48', 'horizon': '#3A4A6A', 'ground': '#141820', 'strength': 0.006}
    core_pool(s, -0.62, 2.85, 0.55)
    s['render']['exposure'] = round(s['render']['exposure'] + 1.0, 3)
    s['render']['white_balance_k'] = 3300
    s['title'] = 'Core in Ember on a bedside table at night (the campaign)'
    s['size'] = [2400, 1600]
    s['camera'] = {'position': [-1.55, 0.95, 1.05], 'target': [-0.45, 2.75, 0.70], 'lens_mm': 38, 'level': True,
                   'fstop': 2.8, 'focus': [-0.62, 2.85, 0.68]}
    return s


def mantle_product(x, y, z, flavour='ember', rot=0.0):
    return {'def': MANTLE, 'flavour': flavour, 'hide': [], 'instances': [{'position': [x, y, z], 'rotate_z': rot}]}


def record(x, y, z):
    """A record on the platter (as Mantle's finals: the disc and its label)."""
    return [kit('cylinder', 'gloss', '#0C0C0D', (x - 0.025, y - 0.012, z + 0.113), radius=0.1505, height=0.0018,
                roughness=0.22),
            kit('cylinder', 'paper', '#C8402A', (x - 0.025, y - 0.012, z + 0.1148), radius=0.05, height=0.0003)]


def sleeves(x, y, z, n=9, seed=3):
    import random
    rnd = random.Random(seed)
    cols = ['#D8D2C4', '#1E1E22', '#B23A28', '#2C4A6A', '#E0B040', '#5A6E4A', '#E8E4DC', '#7A3A5A', '#3A3A3A']
    out = [box('gloss', '#3A2A1E', (0.34, 0.36, 0.012), (x, y, z), roughness=0.5)]
    for i in range(n):
        out.append(box('card', cols[i % len(cols)], (0.315, 0.004, 0.315), (x, y - 0.15 + i * 0.033, z + 0.012),
                       rotate_x=rnd.uniform(-7, -2)))
    return out


CRED = (0.25, 2.79, 0.68)          # the credenza's top centre (modern_wooden_cabinet, 2.44 x 0.68 x 0.68)


def credenza_props():
    cx, cy, cz = CRED
    return [asset('modern_wooden_cabinet', (cx, cy, 0.0), 0.0),
            asset('potted_plant_02', (cx + 1.55, cy - 0.05, 0.0), 20.0),
            asset('ceramic_vase_01', (cx + 0.95, cy + 0.05, cz), 0.0),
            {'kind': 'frame', 'position': [cx - 0.1, 3.15], 'z': 1.62, 'size': [1.0, 0.7], 'art': '#B4432E'},
            *sleeves(cx + 0.55, cy - 0.02, cz)]


def mantle_credenza():
    """Mantle in Ember on a walnut credenza in the evening, a record on, a crate of sleeves beside it, its base lit."""
    s = bare_room(wall='#857B6C')
    cx, cy, cz = CRED
    mx = cx - 0.45
    s['set']['props'] = credenza_props() + record(mx, cy, cz)
    s['product'] = mantle_product(mx, cy - 0.02, cz)
    s['materials'] = {'glow': {'strength': 9.0}}
    s['set']['windows'] = [{'wall': 'left', 'along': 0.6, 'sill': 0.6, 'size': [1.4, 1.8], 'mullions': [2, 1],
                            'frame': '#2A2724'}]
    s['sky'] = {'kind': 'hdri', 'polyhaven': 'twilight_sunset', 'rotation_deg': 250.0, 'strength': 0.03, 'res': '4k'}
    s['lights'] = {
        'key': {'type': 'area', 'size_m': [1.2, 1.2], 'position': [-1.2, 1.0, 2.2], 'target': [mx, cy, cz + 0.1],
                'power_w': round(450 / HB.LM_PER_W, 4), 'color': 2900, 'camera': False},
        'sconce': {'type': 'point', 'position': [1.6, 3.0, 1.7], 'power_w': 0.18, 'radius_m': 0.03, 'color': 2400,
                   'camera': False},
        'fill': {'type': 'area', 'size_m': [2.0, 1.0], 'position': [0.4, -0.8, 1.6], 'target': [mx, cy, cz],
                 'power_w': round(120 / HB.LM_PER_W, 4), 'color': 3400, 'camera': False, 'specular': 0.3},
    }
    s['render']['exposure'] = round(s['render']['exposure'] + 0.6, 3)
    s['title'] = 'Mantle in Ember on a credenza in the evening, a record on (the campaign)'
    s['size'] = [2400, 1600]
    s['camera'] = {'position': [mx + 0.85, cy - 1.75, 1.32], 'target': [mx + 0.1, cy, cz + 0.12], 'lens_mm': 40,
                   'level': True, 'fstop': 4.0, 'focus': [mx, cy, cz + 0.1]}
    return s


def one_room():
    """All three in one room at dusk: Hemisphere over the dining table, Mantle and Core on the credenza behind it."""
    s = dining_room()
    cx, cy, cz = CRED
    st = s['set']
    st['props'] = [p for p in st['props'] if p.get('kind') not in ('sideboard', 'frame') and
                   not (p.get('material') == 'glow' or (p.get('position') or [0, 0, 0])[1] > 2.5 and p.get('kind') == 'kit'
                        and p.get('shape') == 'cylinder')]
    mx = cx - 0.55
    st['props'] += credenza_props() + record(mx, cy, cz) + [LF.core_piece(cx + 0.98, cy - 0.02, cz, 'smoke', glow=0.3,
                                                                          rotate_z=-20)]
    s['product'] = mantle_product(mx, cy - 0.02, cz)
    s['materials'] = {'glow': {'strength': 9.0}}
    for k in ('sconce1', 'sconce2', 'candle1', 'candle2'):
        s['lights'].pop(k, None)
    core_pool(s, cx + 0.98, cy - 0.02, cz, flavour_light='#E8D8C8')
    s['title'] = 'Hemisphere, Core and Mantle in one room at dusk (the campaign)'
    s['size'] = [2400, 1600]
    s['camera'] = {'position': [1.75, -1.45, 1.45], 'target': [-0.15, 1.75, 1.0], 'lens_mm': 28, 'level': True,
                   'fstop': 5.6, 'focus': [0.0, 1.4, 1.0]}
    return s


def macro_dome():
    """Hemisphere's low top, close: the clamp ring, the crown, the cap, the tint's edge."""
    s = P4.dome('ember')
    z = s['product']['instances'][0]['position'][2]
    s['title'] = 'Hemisphere in Ember, the low top close (the campaign)'
    s['size'] = [2000, 1600]
    s['camera'] = {'position': [0.30, -0.42, z + 0.22], 'target': [0.0, 0.0, z + 0.09], 'lens_mm': 100, 'level': False,
                   'fstop': 5.6, 'focus': [0.0, -0.06, z + 0.10]}
    return s


def macro_core():
    """Core in Ember, close at its base: the touch ring, the ball in its cup, the polished black base."""
    s = P4.orb('ember')
    z = s['product']['instances'][0]['position'][2]
    s['title'] = 'Core in Ember, its base close (the campaign)'
    s['size'] = [2000, 1600]
    s['camera'] = {'position': [0.20, -0.36, z + 0.10], 'target': [0.0, 0.0, z + 0.05], 'lens_mm': 100, 'level': False,
                   'fstop': 5.6, 'focus': [0.0, -0.06, z + 0.04]}
    return s


BUILD = {'dining-dusk': dining_dusk, 'core-bedside': core_bedside, 'mantle-credenza': mantle_credenza,
         'one-room': one_room, 'macro-hemisphere': macro_dome, 'macro-core': macro_core}


def main():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in BUILD.items():
        json.dump(f(), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
    print(len(BUILD), 'shots in', os.path.relpath(SHOTS, ROOT), flush=True)
    if '--render' in sys.argv:
        a = sys.argv[sys.argv.index('--render') + 1:]
        want = [x for x in a if x in BUILD] or list(BUILD)
        out = a[a.index('--out') + 1] if '--out' in a else RENDERS
        extra = []
        for k in ('--scale', '--samples'):
            if k in a:
                extra += [k, a[a.index(k) + 1]]
        os.makedirs(out, exist_ok=True)
        for n in want:
            subprocess.run(['python3', os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                            '--out', os.path.join(out, n + '.png')] + extra, cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('rendered', n, flush=True)


if __name__ == '__main__':
    main()
