"""Tropos's campaign stills (2026-10-31): shot files for studio/engine/render.py, built from the rigs that already
passed their critics (room31, studio31), with the model as it stands (round 36's formed horn in its deep lot).

    python3 spinoffs/barkhorn/campaign/shots.py      ->  spinoffs/barkhorn/campaign/shots/*.json

- room: room31's pair at golden hour (Poison), the record player taken off the credenza (its model, a companion's,
  is not built on this branch).
- night: uplight31's facade, lit from below (Ember). inside: finals31's see-into-it view (Ember). corner: studio31's
  polished corner and joint (Ember). above: new, the horn from above in studio31's bright-field rig.
- horn-formed, horn-laminated: studio31's horn macro in Ember, the formed horn and Plan B (make/plan-b.md).
"""
import copy, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.path.join(HERE, 'shots')


def load(path):
    return json.load(open(os.path.join(ROOT, path)))


def room():
    s = load('studio/shots/barkhorn/room31/room.json')
    s['title'] = 'Tropos, a pair at home at golden hour (Poison), round 36 horn'
    s['products'] = [p for p in s['products'] if 'turntable' not in p['def']]
    for p in s['set']['props']:              # with the record player gone, the books and the vase drawn in toward the middle
        if p.get('fn') == 'books':
            p['position'] = [-0.4] + p['position'][1:]
        if p.get('model') == 'ceramic_vase_02':
            p['position'] = [0.42] + p['position'][1:]
    return s


def night():
    s = load('studio/shots/barkhorn/uplight31/facade.json')
    s['title'] = 'Tropos at night, lit from below on a facade (Ember), round 36 horn'
    return s


def inside():
    s = load('studio/shots/barkhorn/finals31/inside-red.json')
    s['title'] = 'Tropos, the see-into-it view (Ember), round 36 horn'
    return s


def corner():
    s = load('studio/shots/barkhorn/studio31/macro-corner-ember.json')
    s['title'] = 'Tropos, a polished corner and its cemented joint, the horn above (Ember)'
    return s


def above():
    """New: the horn from above, in studio31's bright-field rig, the camera high over the front right corner."""
    s = load('studio/shots/barkhorn/studio31/hero-light-ember.json')
    s['title'] = 'Tropos, the horn from above (Ember)'
    s['size'] = [2400, 1600]
    s['camera'] = {'position': [1.45, -2.05, 3.0], 'target': [0.0, 0.06, 1.05], 'lens_mm': 70.0, 'level': False}
    return s


def horn_pair(laminated):
    """Plan B beside the formed horn: studio31's horn macro, in Ember, once each."""
    s = load('studio/shots/barkhorn/studio31/macro-horn-acid.json')
    s['title'] = 'Tropos, the horn ' + ('laminated (Plan B)' if laminated else 'formed') + ' (Ember)'
    s['product']['flavour'] = 'cloud-red'
    for i in s['product']['instances']:
        i['flavour'] = 'cloud-red'
    if laminated:                      # the Cloud without its formed flare, throat and pads; the laminated horn in their place
        cab = s.pop('product')
        for i in cab['instances']:
            i['hide'] = list(i.get('hide', [])) + ['waveguide', 'horn-throat', 'horn-pads']
        lam = {'def': 'studio/products/barkhorn-horn-options.json', 'flavour': 'cloud-red',
               'instances': [{**{k: v for k, v in i.items() if k not in ('hide', 'options')}, 'hide': ['horn-trial-plug', 'horn-trial-base']}
                             for i in cab['instances']]}
        s['products'] = [cab, lam]
    return s


SHOTS = {'room': room, 'night': night, 'inside': inside, 'corner': corner, 'above': above,
         'horn-formed': lambda: horn_pair(False), 'horn-laminated': lambda: horn_pair(True)}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SHOTS.items():
        json.dump(fn(), open(os.path.join(OUT, f'{name}.json'), 'w'), indent=1)
        print(name)
