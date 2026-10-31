"""Planet EARF, round 43: Mother EARF at 2 m on an Amsterdam quay at night, for the Amsterdam Light Festival entry (a
proposal for the owner: the design as signed is 1.25 m). The coordinator, 31 October 2026: "Render A at 2 m outdoors by a
canal, lit as an artwork: rims glowing in the six tints, plus a hard spot throwing its coloured shadow on the quay."

    python3 spinoffs/barkhorn/planet/r43/r43_ams.py [VIEW ...]     # writes studio/shots/barkhorn/planet43/ams-VIEW.json

The scene is `kit43ams` (the quay, the water, the far houses; the globe on its ballast plinth). Views: `quay` (eye
level along the quay, image 1), `shadow` (from higher, the coloured shadow on the paving and the kerb, image 2),
`water` (low from the canal, the globe and its reflection).
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
BASE = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet42', 'shop.json')
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet43')
KIT = 'spinoffs/barkhorn/planet/r43/kit43ams.py'
G = [0.0, -3.2]                       # the globe's place on the quay

VIEWS = {
    # p2 (p1 judged 4.5/4.5 for the quay and the shadow, converged: only three rims read and the globe barely brighter
    # than the frame; the houses a flat slab with clipped white panes; a saturated blue sky and a sepia ground; flat
    # paving; a crushed black plinth; a lamp glow floating above the globe): the rims 0.03 to 0.12; three warmths of
    # lit room at a fifth of the glow, some curtained; a darker, greyer sky; 3200 K; the plinth satin steel; the lamps'
    # glow at their lanterns; the quay view swung so the lit houses stand behind the globe
    'quay': dict(camera={'position': [5.5, -7.0, 1.60], 'target': [-1.0, 0.5, 1.6], 'lens_mm': 32, 'level': True,
                         'fstop': 4.0, 'focus': [0.0, -3.2, 1.5]}, exposure=3.6),
    'shadow': dict(camera={'position': [3.8, -8.2, 2.60], 'target': [-0.4, -1.8, 0.4], 'lens_mm': 32, 'level': True,
                           'fstop': 5.6, 'focus': [0.0, -2.6, 0.5]}, exposure=3.6),
    'water': dict(camera={'position': [-6.5, 9.0, -0.55], 'target': [0.0, -3.0, 1.2], 'lens_mm': 35, 'level': True,
                          'fstop': 5.6, 'focus': [0.0, -3.2, 1.4]}, exposure=3.6),
}


def spot(pos, tgt, w, cone, k=3000, blend=0.15, radius=0.02):
    return {'type': 'spot', 'position': pos, 'target': tgt, 'power_w': w, 'cone_deg': cone, 'blend': blend,
            'radius_m': radius, 'color': k, 'camera': False}


def shot(view):
    s = copy.deepcopy(json.load(open(BASE)))
    v = VIEWS[view]
    s['title'] = f'Mother EARF at 2 m, Amsterdam (a proposal): {view}'
    s['camera'] = v['camera']
    s['set'] = {'kind': 'stage', 'props': [
        {'kind': 'kit', 'shape': 'ext', 'path': KIT, 'fn': 'canal', 'width': 18.0, 'lit': 0.45, 'window_glow': 0.35},
        {'kind': 'kit', 'shape': 'ext', 'path': KIT, 'fn': 'globe', 'size': 2.0, 't': 0.025, 'at': G,
         'rim': v.get('rim', 0.12), 'rim_par': 1.0, 'heading': 35.0, 'base_h': 0.45, 'post': 0.10},
        {'kind': 'kit', 'shape': 'asset', 'model': 'street_lamp_01', 'res': '1k', 'position': [-9.0, -1.0, 0.0],
         'rotate': [0, 0, 90.0]},
        {'kind': 'kit', 'shape': 'asset', 'model': 'street_lamp_01', 'res': '1k', 'position': [12.0, -1.0, 0.0],
         'rotate': [0, 0, 90.0]},
    ]}
    s['products'] = []
    # the hard spot: on a mast on the land side, high, throwing the globe's coloured shadow across the paving toward
    # the kerb and the water; the street lamps along the quay, sodium-warm
    s['lights'] = {
        'hard': spot([-3.5, -8.0, 8.5], [0.4, -2.2, 0.0], v.get('hard_w', 1800.0), 30.0, k=3600, blend=0.2),
        'lamp-a': {'type': 'point', 'position': [-9.0, -1.0, 3.9], 'power_w': 60.0, 'color': 2200, 'radius_m': 0.12},
        'lamp-b': {'type': 'point', 'position': [12.0, -1.0, 3.9], 'power_w': 60.0, 'color': 2200, 'radius_m': 0.12},
        'far': {'type': 'area', 'position': [0.0, 20.0, 6.0], 'target': [0.0, 23.0, 3.0], 'size_m': [30.0, 1.0],
                'irradiance': 0.15, 'color': 2400, 'camera': False},
    }
    s['sky'] = {'kind': 'gradient', 'zenith': '#040508', 'horizon': '#2A2620', 'ground': '#08080A',
                'strength': v.get('sky', 0.12)}
    s['haze'] = {'box_m': [-20.0, -14.0, -1.1, 20.0, 22.0, 8.0], 'density': v.get('haze', 0.0025), 'anisotropy': 0.4,
                 'color': '#FFFFFF'}
    s['render']['exposure'] = v.get('exposure', 3.6)
    s['render']['white_balance_k'] = v.get('wb', 3200)
    return s


def write(names=None):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(VIEWS):
        p = os.path.join(OUT, f'ams-{n}.json')
        json.dump(shot(n), open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    write([a for a in sys.argv[1:] if not a.startswith('--')] or None)
