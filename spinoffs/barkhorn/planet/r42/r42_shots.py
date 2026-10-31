"""Planet EARF, round 42: new interior views of the bar as rendered (round 41 p3, the door hero's room, its look and
light unchanged), from new cameras: the counter, the listening corner, the room at night from the back, the shop wall.

    python3 spinoffs/barkhorn/planet/r42/r42_shots.py [VIEW ...]     # writes studio/shots/barkhorn/planet42/VIEW.json

The rendered room is the round 36 to 41 model (20 ft wide, 56 ft deep). The round 42 plan (plan42.py) is the bigger
house the drawings show; these views show its materials, its light and the products, not its exact layout.
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
BASE = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet41', 'door-mother-colour-p3.json')
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet42')
KIT42 = 'spinoffs/barkhorn/planet/r42/kit42.py'

VIEWS = {
    # along the counter from its far end: the zinc, the Hemispheres, the back bar and the record wall, the decks
    'counter': dict(camera={'position': [10.35, 2.55, 1.42], 'target': [4.6, 4.55, 1.30], 'lens_mm': 32, 'level': True,
                            'fstop': 4.0, 'focus': [7.3, 4.1, 1.15]}, exposure=4.0),
    # the listening corner: the altar, the pair, the tub chairs and their Cores
    'listening': dict(camera={'position': [11.25, 2.70, 1.30], 'target': [16.5, 3.05, 1.00], 'lens_mm': 26, 'level': True,
                              'fstop': 4.0, 'focus': [16.0, 3.0, 1.0]}, exposure=4.8),
    # the room at night from the back, the line playing: past the tubs to the counter, the globe and the street
    'night': dict(camera={'position': [14.9, 3.35, 1.68], 'target': [2.0, 2.7, 1.40], 'lens_mm': 28, 'level': True,
                          'fstop': 5.6, 'focus': [7.0, 3.0, 1.2]}, exposure=4.4),
    # the shop wall by the door: everything in the room is on sale, and this is where it waits
    'shop': dict(camera={'position': [0.80, 1.85, 1.40], 'target': [2.35, 5.95, 1.12], 'lens_mm': 28, 'level': True,
                         'fstop': 4.0, 'focus': [2.0, 5.7, 1.1]}, exposure=4.2, shop=True),
}
FLAVOURS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
SHELF = [0.32, 0.80, 1.28, 1.70]


def shop_props():
    yw = 6.10
    cores = [{'position': [0.62 + 0.235 * i, 5.93, SHELF[2]], 'flavour': f, 'rotate_z': 0.0} for i, f in enumerate(FLAVOURS)]
    cards = [(c['position'][0], SHELF[2]) for c in cores[::2]] + [(0.95, SHELF[1]), (1.75, SHELF[1]), (1.9, SHELF[0])]
    props = [
        {'kind': 'kit', 'shape': 'ext', 'path': KIT42, 'fn': 'shopwall', 'x': [0.45, 2.35], 'wall': yw, 'shelves': SHELF,
         'cards': cards, 'plinth': [2.95, 5.60, 0.62, 0.52, 0.26]},
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb', 'spots': cores, 'cable': False,
         'cartridge': 'none', 'lamp_w': 0.25, 'lamp_k': 2700, 'shade_glow': 0.0067, 'noshadow': 'shell|liner|skin',
         'materials': {'liner': {'glow_color': '#FFA060'}}},
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'ceiling': 3.4, 'lamp_w': 12.0, 'lamp_k': 2700,
         'shade_glow': 0.05, 'noshadow': 'shell|liner|skin',
         'spots': [{'position': [0.80, 5.40, 2.05], 'flavour': 'ember'}, {'position': [1.45, 5.30, 2.22], 'flavour': 'ice'},
                   {'position': [2.10, 5.40, 1.98], 'flavour': 'smoke'}]},
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'fan', 'spots': [[1.80, 5.90, SHELF[1]]],
         'flavours': ['ember', 'ice', 'acid', 'fog', 'poison'], 'heading': 10.0},
    ]
    products = [
        {'def': 'spinoffs/barkhorn/companions/out-concepts2/r3.json', 'flavour': 'smoke',
         'instances': [{'position': [0.95, 5.92, SHELF[1]], 'rotate_z': 0.0}]},
        {'def': 'studio/products/barkhorn-cloud.json', 'flavour': 'cloud-red',
         'instances': [{'position': [2.95, 5.60, 0.26], 'rotate_z': -35.0, 'hide': ['cloth-disc']}]},
    ]
    lights = {'shop_key': {'type': 'area', 'position': [1.9, 4.3, 3.30], 'target': [1.5, 6.0, 1.0], 'size_m': [0.3, 0.3],
                           'irradiance': 1.2, 'color': 2900, 'spread_deg': 60.0}}
    return props, products, lights


def shot(view):
    s = copy.deepcopy(json.load(open(BASE)))
    v = VIEWS[view]
    s['camera'] = v['camera']
    s['render']['exposure'] = v.get('exposure', s['render']['exposure'])
    s['title'] = f'Planet EARF, round 42: {view}'
    s['set']['props'] += v.get('props', [])
    if v.get('shop'):
        props, products, lights = shop_props()
        s['set']['props'] += props
        s['products'] += products
        s['lights'].update(lights)
    return s


def write(names=None):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(VIEWS):
        p = os.path.join(OUT, f'{n}.json')
        json.dump(shot(n), open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    write([a for a in sys.argv[1:] if not a.startswith('--')] or None)
