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
    # p2 (both p1 critics 5.0, converged): Mother EARF into the frame (28 mm, aimed into the room), exposure down, the
    # zinc darker and rougher, the pendants' downlights softer, the record wall in pools, the Cores up a little
    'counter': dict(camera={'position': [10.35, 2.55, 1.42], 'target': [4.6, 3.3, 1.55], 'lens_mm': 24, 'level': True,
                            'fstop': 4.0, 'focus': [7.3, 4.0, 1.15]}, exposure=3.6,
                    lights={'pend': {'power_w': 20.0, 'cone_deg': 24.0}, 'rw': {'power_w': 8.0, 'cone_deg': 16.0, 'color': 2700},
                            'street': {'radius_m': 0.6}},
                    retouch={'darken': {'zinc': 0.25}, 'zinc_rough': [0.30, 0.60]}, orb={'lamp_w': 0.6, 'shade_glow': 0.012}),
    # the listening corner: the altar, the pair, the tub chairs and their Cores
    'listening': dict(camera={'position': [11.25, 2.70, 1.30], 'target': [16.5, 3.05, 1.00], 'lens_mm': 26, 'level': True,
                              'fstop': 4.0, 'focus': [16.0, 3.0, 1.0]}, exposure=4.8),
    # the room at night from the back, the line playing: past the tubs to the counter, the globe and the street
    # p2 (critics 4.5/5.0, converged): forward of the jambs at seated height, 32 mm; the floor's stains calmed; the
    # pendants' downlights softer; the Cores and Mother's rims down, its spot up; the screens dimmer; the speakers lit
    'night': dict(camera={'position': [14.2, 3.0, 1.32], 'target': [2.0, 2.9, 1.25], 'lens_mm': 32, 'level': True,
                          'fstop': 5.6, 'focus': [7.0, 3.0, 1.2]}, exposure=4.2,
                  lights={'pend': {'power_w': 20.0, 'cone_deg': 24.0}, 'spk': {'irradiance': 3.0}, 'barspk': {'power_w': 120.0},
                          'altar': {'power_w': 220.0, 'cone_deg': 24.0}, 'mother-spot': {'power_w': 180.0, 'cone_deg': 24.0},
                          'street': {'radius_m': 0.6}},
                  orb={'lamp_w': 0.15, 'shade_glow': 0.0035}, mother={'rim': 0.015}, room={'screen_glow': 0.015},
                  props=[{'kind': 'kit', 'shape': 'ext', 'path': KIT42, 'fn': 'flatten', 'match': 'Concrete044A', 'contrast': -0.45, 'mean': 0.15}]),
    # the shop wall by the door: everything in the room is on sale, and this is where it waits
    # p2 (critics 5.0/4.5, converged): night exposure (4.2 to 2.9), the Tropos lit to stay the hero, the Domes and the
    # shelf strips down, the Cores grouped over two shelves (two unlit), the cards bigger, seated camera at 32 mm
    'shop': dict(camera={'position': [0.82, 1.84, 1.28], 'target': [2.5, 5.9, 1.18], 'lens_mm': 32, 'level': True,
                         'fstop': 4.0, 'focus': [2.2, 5.7, 1.1]}, exposure=2.9, shop=True,
                 lights={'pend': {'power_w': 20.0, 'cone_deg': 24.0}, 'shop_key': {'irradiance': 0.5}},
                 props=[{'kind': 'kit', 'shape': 'ext', 'path': KIT42, 'fn': 'flatten', 'match': 'Concrete044A', 'contrast': -0.45, 'mean': 0.15}]),
}
FLAVOURS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
SHELF = [0.32, 0.80, 1.28, 1.70]


def shop_props():
    yw = 6.10
    # grouped by hand, not drilled: three and three on the third shelf, two on the top; two of them unlit
    xs = [(0.62, 2), (0.84, 2), (1.06, 2), (1.62, 2), (1.84, 2), (2.06, 2), (0.80, 3), (1.15, 3)]
    cores = [{'position': [x, 5.93, SHELF[k]], 'flavour': f, 'rotate_z': 0.0, **({'lamp': False} if i in (2, 6) else {})}
             for i, ((x, k), f) in enumerate(zip(xs, FLAVOURS))]
    cards = [(0.84, SHELF[2]), (1.84, SHELF[2]), (0.95, SHELF[1]), (1.75, SHELF[1]), (1.9, SHELF[0]), (0.98, SHELF[3])]
    props = [
        {'kind': 'kit', 'shape': 'ext', 'path': KIT42, 'fn': 'shopwall', 'x': [0.45, 2.35], 'wall': yw, 'shelves': SHELF,
         'cards': cards, 'card_size': [0.09, 0.06], 'led': 3.0, 'covers': ['#c8452f', '#e9e4d8'], 'plinth': [2.95, 5.60, 0.62, 0.52, 0.26]},
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb', 'spots': cores, 'cable': False,
         'cartridge': 'none', 'lamp_w': 0.25, 'lamp_k': 2700, 'shade_glow': 0.0067, 'noshadow': 'shell|liner|skin',
         'materials': {'liner': {'glow_color': '#FFA060'}}},
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'ceiling': 3.4, 'lamp_w': 6.0, 'lamp_k': 2700,
         'shade_glow': 0.02, 'noshadow': 'shell|liner|skin',
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
                           'irradiance': 1.2, 'color': 2900, 'spread_deg': 60.0},
              # the Tropos's own light (p2): a soft key from the front-left and a grazing rim from above the plinth
              'shop_spk': {'type': 'area', 'position': [3.7, 4.4, 2.5], 'target': [2.95, 5.6, 0.95], 'size_m': [0.4, 0.4],
                           'irradiance': 2.2, 'color': 2700, 'spread_deg': 50.0},
              'shop_spk_rim': {'type': 'area', 'position': [3.2, 6.0, 2.8], 'target': [2.95, 5.6, 1.2], 'size_m': [0.25, 0.25],
                               'irradiance': 1.5, 'color': 2700, 'spread_deg': 40.0}}
    return props, products, lights


def shot(view):
    s = copy.deepcopy(json.load(open(BASE)))
    v = VIEWS[view]
    s['camera'] = v['camera']
    s['render']['exposure'] = v.get('exposure', s['render']['exposure'])
    s['title'] = f'Planet EARF, round 42: {view}'
    s['set']['props'] += v.get('props', [])
    for pre, kv in v.get('lights', {}).items():
        for name, L in s['lights'].items():
            if name.startswith(pre):
                L.update(kv)
    for q in s['set']['props']:
        if q.get('fn') == 'retouch' and v.get('retouch'):
            q.update(v['retouch'])
        if q.get('fn') == 'orb' and q.get('module') == 'earf_moon' and v.get('orb'):
            q.update(v['orb'])
        if q.get('fn') == 'room' and v.get('room'):
            q.update(v['room'])
        if q.get('fn') == 'mother' and v.get('mother'):
            q.update(v['mother'])
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
