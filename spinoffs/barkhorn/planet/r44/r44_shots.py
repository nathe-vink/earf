"""Planet EARF, round 44: the lantern, rendered. The coordinator, 31 October 2026: "3 to 5 photoreal views. Calibrated
acrylic (IOR 1.49, A&C's TruCast transmission), real lenses, caustics where light passes through tint."

    python3 spinoffs/barkhorn/planet/r44/r44_shots.py [VIEW ...]     # writes studio/shots/barkhorn/planet44/VIEW.json

The room is `kit44.house` (plan44's geometry). Views: `street` (from the sidewalk at night: the shop, the bar and the
lantern at the end of the room), `bar` (from the shop table down the bar to the lantern's face), `lantern` (inside, from
the bench: Mother EARF on its plinth between the Tropos pair, its coloured shadow on the end-grain floor).
The products are as they stand (the other lanes' redesigns are proposals): the Ember Tropos pair, Cores, Hemispheres,
Mantle and the coins.
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, HERE)
import plan44 as P                                                   # noqa: E402

BASE = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet42', 'shop.json')
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet44')
KIT = 'spinoffs/barkhorn/planet/r44/kit44.py'
CLOUD = 'studio/products/barkhorn-cloud.json'
MANTLE = 'spinoffs/barkhorn/companions/out-concepts2/r3.json'
FLAVOURS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
H = P.CEIL
I = P.INNER
YC = (I['y0'] + I['y1']) / 2

VIEWS = {
    'street': dict(camera={'position': [-3.4, 5.7, 1.52], 'target': [13.0, 4.2, 1.95], 'lens_mm': 35, 'level': True,
                           'fstop': 4.0, 'focus': [6.0, 4.4, 1.2]}, exposure=3.6, haze=0.003),
    'bar': dict(camera={'position': [4.9, 2.55, 1.45], 'target': [13.0, 4.3, 2.0], 'lens_mm': 28, 'level': True,
                        'fstop': 4.0, 'focus': [11.0, 4.5, 1.6]}, exposure=3.6, haze=0.003),
    'lantern': dict(camera={'position': [P.BENCH['x0'] - 0.25, I['y0'] + 0.75, 1.15], 'target': [P.MOTHER['x'] + 0.2, YC + 0.3, 1.05],
                            'lens_mm': 28, 'level': True, 'fstop': 2.8, 'focus': [P.MOTHER['x'], YC, 1.0]},
                    exposure=4.5, haze=0.002, room={'interior': True}),
}


def _face(x, y, tx, ty):
    """rotate_z for a Tropos at (x, y) to face (tx, ty): at 0 it faces -y, at -90 it faces -x."""
    return round(math.degrees(math.atan2(ty - y, tx - x)) + 90.0, 2)


def spot(pos, tgt, w, cone, k=2700, blend=0.6, radius=0.03):
    return {'type': 'spot', 'position': pos, 'target': tgt, 'power_w': w, 'cone_deg': cone, 'blend': blend,
            'radius_m': radius, 'color': k, 'camera': False}


def scene():
    S = P.SHOP_WALL
    props = [{'kind': 'kit', 'shape': 'ext', 'path': KIT, 'fn': 'house', 'windows_lit': 0.3, 'window_glow': 0.25,
              'glass_gloss': 0.3}]
    shelves = [0.30, 0.78, 1.26, 1.74, 2.22]
    # the Cores along the shop's shelves, in the eight tints, some unlit
    xs = [S['x0'] + 0.35 + 0.30 * i for i in range(8)]
    cores = [{'position': [x, W_ - 0.25, shelves[2]], 'flavour': f, 'rotate_z': 180.0} for x, f in zip(xs, FLAVOURS)]
    cores += [{'position': [x + 2.6, W_ - 0.25, shelves[1]], 'flavour': f, 'rotate_z': 180.0, **({'lamp': False} if i % 2 else {})}
              for i, (x, f) in enumerate(zip(xs, ['smoke', 'fog', 'ember', 'ice', 'acid', 'haze', 'dust', 'poison']))]
    cores += [{'position': [4.0, 3.60, P.SHOP_TABLE['h']], 'flavour': 'ice'}, {'position': [4.5, 3.85, P.SHOP_TABLE['h']], 'flavour': 'ember'}]
    cores += [{'position': [P.WINDOW_PLINTH['x0'] + 0.5, y, P.WINDOW_PLINTH['h']], 'flavour': f}
              for y, f in zip((3.6, 4.4, 5.2, 6.0), ('ember', 'smoke', 'fog', 'haze'))]
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb', 'spots': cores, 'cable': False,
                  'cartridge': 'none', 'lamp_w': 0.20, 'lamp_k': 2700, 'shade_glow': 0.005, 'noshadow': 'shell|liner|skin',
                  'materials': {'liner': {'glow_color': '#FFA060'}}})
    by = (P.COUNTER['edge'] + P.COUNTER['y_work']) / 2
    domes = [{'position': [x, by, 2.05], 'flavour': 'smoke'} for x in (8.6, 10.0, 11.4)]
    domes += [{'position': [x, 3.75, 2.15], 'flavour': f} for x, f in ((4.0, 'haze'), (4.9, 'dust'))]
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'ceiling': H, 'lamp_w': 4.0,
                  'lamp_k': 2700, 'shade_glow': 0.006, 'noshadow': 'shell|liner|skin', 'spots': domes})
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'bowl', 'spots': [[3.75, 3.55, P.SHOP_TABLE['h']]],
                  'n': 30, 'bowl': 'brass', 'd': 200})
    # signs of life: rounds on the bar and the banquette tables
    props.append({'kind': 'kit', 'shape': 'ext', 'path': 'spinoffs/barkhorn/planet/r39/kit39.py', 'fn': 'life',
                  'rocks': [[9.55, by - 0.12, 1.07, 0.03, 1, '#B8641C'], [10.75, by - 0.08, 1.07, 0.02, 2, '#B8641C'],
                            [P.BANQ_TABLES[1], P.BANQ['y1'] + 0.35, 0.75, 0.025, 1, '#B8641C']],
                  'coupes': [[10.15, by - 0.10, 1.07, 0.6, '#B8462A'], [P.BANQ_TABLES[2] + 0.1, P.BANQ['y1'] + 0.32, 0.75, 0.4, '#E8DDB8']],
                  'napkins': [[9.55, by - 0.12, 1.07, 8.0], [10.15, by - 0.10, 1.07, -12.0]],
                  'votives': [], 'matchbooks': [], 'coats': []})
    sweet = P.SWEET
    products = [
        {'def': CLOUD, 'flavour': 'cloud-red', 'instances': [
            {'position': [x, y, P.TROPOS['plinth']], 'rotate_z': _face(x, y, *sweet), 'hide': ['cloth-disc']} for (x, y) in P.STACKS]},
        {'def': MANTLE, 'flavour': 'smoke', 'instances': [{'position': [5.0, 3.55, P.SHOP_TABLE['h']], 'rotate_z': 90.0}]},
    ]
    zc = H - 0.05
    lights = {}
    for i, x in enumerate((1.4, 3.0, 4.6)):                           # the shop wall
        lights[f'shop{i}'] = spot([x, W_ - 1.4, zc], [x, W_ - 0.2, 1.4], 30.0, 34.0)
    lights['table'] = spot([4.3, 3.75, zc], [4.3, 3.75, 0.9], 14.0, 28.0)
    for i, x in enumerate([7.6, 8.4] + P.STOOLS[::2]):                # the counter
        lights[f'ctr{i}'] = spot([x, P.COUNTER['y0'] + 0.25, zc], [x, P.COUNTER['y0'] + 0.05, 1.07], 14.0, 26.0)
    for i, x in enumerate(P.BANQ_TABLES):                             # the banquette tables
        lights[f'bq{i}'] = spot([x, P.BANQ['y1'] + 0.40, zc], [x, P.BANQ['y1'] + 0.35, 0.75], 9.0, 24.0)
    lights['route'] = {'type': 'area', 'position': [8.0, 0.72, H - 0.02], 'target': [8.0, 0.72, 0.0], 'size_m': [10.0, 0.1],
                       'irradiance': 0.3, 'color': 2700, 'camera': False}
    lights['fill'] = {'type': 'area', 'position': [7.0, W_ / 2, H - 0.3], 'target': [7.0, W_ / 2, 0.0], 'size_m': [10.0, 4.0],
                      'irradiance': 0.06, 'color': 2900, 'camera': False}
    # the lantern's face, grazed from the ceiling's edge so the slots read
    lights['baffle'] = {'type': 'area', 'position': [P.LANT['x0'] - 0.45, W_ / 2 + 0.8, H - 0.08],
                        'target': [P.LANT['x0'] - 0.05, W_ / 2 + 0.8, 1.2], 'size_m': [0.15, 5.2], 'irradiance': 0.8,
                        'color': 2600, 'camera': False}
    # inside the lantern: the pair's spots, a hard spot through Mother EARF (its coloured shadow on the floor), the
    # trap's graze, a low fill
    zi = I['h'] - 0.05
    for i, (x, y) in enumerate(P.STACKS):
        lights[f'stack{i}'] = spot([x + 1.0, y + (0.5 if y < YC else -0.5), zi], [x, y, 1.3], 30.0, 20.0, k=2600)
    M = P.MOTHER
    lights['mother'] = spot([M['x'] - 0.25, M['y'] - 0.6, zi], [M['x'] + 0.7, M['y'] + 0.25, 0.0], 60.0, 18.0, k=3000,
                            blend=0.2, radius=0.01)
    lights['trap'] = {'type': 'area', 'position': [P.TRAP['x0'] - 0.25, YC, zi - 0.05], 'target': [P.TRAP['x0'], YC, 1.0],
                      'size_m': [0.15, 4.6], 'irradiance': 0.5, 'color': 2600, 'camera': False}
    lights['infill'] = {'type': 'area', 'position': [(I['x0'] + I['x1']) / 2, YC, zi - 0.1], 'target': [(I['x0'] + I['x1']) / 2, YC, 0.0],
                        'size_m': [5.0, 3.5], 'irradiance': 0.08, 'color': 2700, 'camera': False}
    lights['street'] = {'type': 'area', 'position': [-2.4, 1.0, 6.0], 'target': [-1.5, 3.0, 0.0], 'size_m': [0.6, 0.6],
                        'irradiance': 1.2, 'color': 2200, 'spread_deg': 80.0}
    return props, products, lights


W_ = P.W


def shot(view):
    s = copy.deepcopy(json.load(open(BASE)))
    v = VIEWS[view]
    props, products, lights = scene()
    s['title'] = f'Planet EARF, round 44: the lantern, {view}'
    s['camera'] = v['camera']
    s['set'] = {'kind': 'stage', 'props': props}
    s['products'] = products
    s['lights'] = lights
    s['haze']['density'] = v.get('haze', 0.002)
    s['haze']['box_m'] = [0.05, 0.05, 0.01, P.L - 0.05, P.W - 0.05, H - 0.05]
    s['render']['exposure'] = v.get('exposure', 3.6)
    s['render']['white_balance_k'] = 2800; s['render']['white_balance_tint'] = 1.0
    s['render']['caustics_refractive'] = True                       # light through the tinted discs and fins
    s['render'].update(v.get('render', {}))
    if v.get('room'):
        props[0].update(v['room'])
    for pre, kv in v.get('lights', {}).items():
        for name, L_ in s['lights'].items():
            if name.startswith(pre):
                L_.update(kv)
    return s


def write(names=None):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(VIEWS):
        p = os.path.join(OUT, f'{n}.json')
        json.dump(shot(n), open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    write([a for a in sys.argv[1:] if not a.startswith('--')] or None)
