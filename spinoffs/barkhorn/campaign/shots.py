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


def room(critic_round=4):
    s = load('studio/shots/barkhorn/room31/room.json')
    s['title'] = 'Tropos, a pair at home at golden hour (Poison), round 36 horn'
    s['products'] = [p for p in s['products'] if 'turntable' not in p['def']]
    for p in s['set']['props']:              # with the record player gone, the books and the vase drawn in toward the middle
        if p.get('fn') == 'books':
            p['position'] = [-0.4] + p['position'][1:]
        if p.get('model') == 'ceramic_vase_02':
            p['position'] = [0.42] + p['position'][1:]
    if critic_round >= 2:                    # the critic's round 1 (tropos-campaign/critic/room-r1.json): c1 to c4, c6, c7
        L = s['lights']
        L['north'].update(irradiance=0.9, position=[-0.4] + L['north']['position'][1:])
        L['bounce']['irradiance'] = 0.25
        L['floorbounce']['irradiance'] = 0.0
        s['render']['exposure'] = -1.2
        s['sun']['elevation_deg'] = 11.0
        s['camera'].update(position=[-0.45] + s['camera']['position'][1:], target=[-0.45] + s['camera']['target'][1:])
        for p in s['set']['props']:
            if p.get('model') == 'ceramic_vase_02':
                p['position'] = [0.55, 0.78, 0.56]
            if p.get('fn') == 'rug':
                p.update(off=False, position=[0.0, -0.9], size=[2.4, 1.5])
    if critic_round >= 3:                    # round 2 (room-r2.json): c1, c2, c3 (the same texture, tinted), c4 to c7
        L = s['lights']
        L['north']['irradiance'] = 0.45
        L['bounce']['irradiance'] = 0.4
        s['sun'].update(elevation_deg=17.0, angle_deg=1.0)
        s['camera'].update(position=[-0.25] + s['camera']['position'][1:], target=[-0.25] + s['camera']['target'][1:])
        for p in s['set']['props']:
            if p.get('fn') == 'rug':
                p.update(value=0.6, tex_scale=1.0, displace=0.006, tint='#8A7A64', tint_mix=1.0)
            if p.get('fn') == 'sheer' and p.get('seed') == 12:
                p['open'] = 0.6
    if critic_round >= 4:                    # look 2 (the coordinator, after round 3's 7.0): round 3's changes (room-r3.json).
        L = s['lights']                      # The rug's tint did take; it read neutral because the scan is pale (value is
        L['north']['irradiance'] = 0.8       # a linear multiply) and PBR Neutral desaturates near-white; so darker, as c1
        L['bounce'].update(position=[0.4, -3.6, 1.0], irradiance=0.55)
        s['sun'].update(azimuth_deg=-60.0, elevation_deg=15.0)
        for p in s['set']['props']:
            if p.get('fn') == 'rug':
                p.update(value=0.32, tint='#7E6C56', pile=0.022, displace=0.009)
            if p.get('fn') == 'sheer' and p.get('seed') == 11:
                p.update(color='#DDD3C4', open=0.45, folds=3)
            if p.get('fn') == 'floor':
                p.update(coat=0.25, coat_rough=0.22)
            if p.get('model') == 'ceramic_vase_02':
                p['rotate'] = [0, 0, 200]
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


def horn_choice(route, colour, macro=False):
    """The owner's choice of horn (2026-10-31, later): formed, laminated stepped or laminated smooth, in the stock colours
    (stock_colours.json), each in studio31's horn macro rig and light, the speaker turned so the camera sees the mouth
    from the front three-quarter. `macro`: the terraces close up, the speaker side-on as in the first comparison."""
    s = load('studio/shots/barkhorn/studio31/macro-horn-acid.json')
    fl = 'stock-' + colour
    s['title'] = f'Tropos, the horn {route} in stock {colour}' + (', the terraces close' if macro else ', front three-quarter')
    cab = s.pop('product')
    cab['flavour'] = fl
    for i in cab['instances']:
        i['flavour'] = fl
        i['rotate_z'] = 80.0 if macro else 57.0
    if route != 'formed':
        for i in cab['instances']:
            i['hide'] = list(i.get('hide', [])) + ['waveguide', 'horn-throat', 'horn-pads']
        other = 'horn-plan-b' if route == 'smooth' else 'horn-plan-b-smooth'
        lam = {'def': 'studio/products/barkhorn-horn-options.json', 'flavour': fl,
               'instances': [{**{k: v for k, v in i.items() if k not in ('hide', 'options')},
                              'hide': ['horn-trial-plug', 'horn-trial-base', other]} for i in cab['instances']]}
        s['products'] = [cab, lam]
    else:
        s['products'] = [cab]
    if macro:                          # closer, on the flank where the terraces step, a longer lens
        s['camera'] = {'position': [0.62, -1.15, 1.30], 'target': [0.06, 0.0, 1.10], 'lens_mm': 135.0, 'level': False}
    return s


def lineup():
    """The site's tints beside the stock pair's (2026-10-31): Ember as on the site, Ember in stock sheet, Smoke as on the
    site, Smoke in stock sheet; the stock two with the laminated horn (the January pair), the site's with the formed one.
    studio31's line-up rig, the camera brought in for four."""
    s = load('studio/shots/barkhorn/studio31/lineup.json')
    s['title'] = 'Tropos: the site\'s Ember and Smoke beside the stock-sheet pair\'s (laminated horn)'
    s['size'] = [2400, 1350]
    s['camera'] = {'position': [0.0, -8.4, 0.95], 'target': [0.0, 0.0, 0.66], 'lens_mm': 58.0, 'level': True}
    cab = s.pop('product')
    xs = [-1.5, -0.5, 0.5, 1.5]; fls = ['cloud-red', 'stock-ember', 'cloud-black', 'stock-smoke']
    base = cab['instances'][0]
    cab['instances'] = []
    lam = {'def': 'studio/products/barkhorn-horn-options.json', 'flavour': 'stock-ember', 'instances': []}
    for x, fl in zip(xs, fls):
        i = {**{k: v for k, v in base.items() if k not in ('position', 'flavour', 'hide')}, 'position': [x, 0, 0], 'flavour': fl}
        if fl.startswith('stock'):
            i['hide'] = list(base.get('hide', [])) + ['waveguide', 'horn-throat', 'horn-pads']
            lam['instances'].append({**{k: v for k, v in i.items() if k not in ('hide', 'options')},
                                     'hide': ['horn-trial-plug', 'horn-trial-base', 'horn-plan-b-smooth']})
        elif base.get('hide'):
            i['hide'] = list(base['hide'])
        cab['instances'].append(i)
    s['products'] = [cab, lam]
    return s


HORN_PARTS = ['waveguide', 'horn-throat', 'horn-pads']
OPTIONS = 'studio/products/barkhorn-horn-options.json'
VARIANTS = 'studio/products/barkhorn-variants.json'


def proposal(design, base='studio/shots/barkhorn/lookbook31/look-red-off-tall.json', flavour='cloud-red'):
    """A design-pass proposal (spinoffs/barkhorn/variants) in a shot that already shows the whole speaker, cover off
    (the owner, 2026-10-31): 'current' (the baseline), 'strata' (the stepped laminated horn and the woofer's caldera)
    or 'topo' (the Topo horn). The Cloud stays the cabinet; the proposals' parts come from their own product files,
    in the Cloud's frame, with the parts they replace hidden."""
    s = load(base)
    s['title'] = f'Tropos, {design} (design pass), {flavour}'
    blk = s.pop('product') if 'product' in s else s.pop('products')[0]
    blk['flavour'] = flavour
    inst = [{**i, 'flavour': flavour} for i in blk['instances']]
    for i in inst:
        i['hide'] = sorted(set(i.get('hide', [])) | {'cloth-disc'})
    blk['instances'] = inst
    prods = [blk]
    if design in ('strata', 'topo', 'topo-clear'):
        for i in inst:
            i['hide'] = sorted(set(i['hide']) | set(HORN_PARTS) | ({'woofer-ring'} if design == 'strata' else set()))
        keep = lambda i: {k: v for k, v in i.items() if k not in ('hide', 'options')}
        if design == 'strata':
            prods.append({'def': OPTIONS, 'flavour': flavour,
                          'instances': [{**keep(i), 'hide': ['horn-trial-plug', 'horn-trial-base', 'horn-plan-b-smooth']} for i in inst]})
            prods.append({'def': VARIANTS, 'flavour': flavour, 'instances': [{**keep(i), 'hide': ['horn-topo']} for i in inst]})
        elif design == 'topo':
            prods.append({'def': VARIANTS, 'flavour': flavour, 'instances': [{**keep(i), 'hide': ['caldera-*']} for i in inst]})
        else:                       # topo-clear: the clear layers and their tinted laminae (an option in the product)
            prods.append({'def': VARIANTS, 'flavour': flavour,
                          'instances': [{**keep(i), 'hide': ['caldera-*', 'horn-topo'], 'options': ['Topo Clear']} for i in inst]})
    s['products'] = prods
    return s


def room_off():
    """The room final (round 3's look) with the covers off (the owner, 2026-10-31: product images without the cover)."""
    s = room(critic_round=3)
    s['title'] += ', covers off'
    for blk in s.get('products', []):
        for i in blk.get('instances', []):
            i['hide'] = sorted(set(i.get('hide', [])) | {'cloth-disc'})
    return s


SHOTS = {'room': room, 'room-final': lambda: room(critic_round=3),   # round 3's look (7.0): the final
         'room-final-off': room_off, 'night': night, 'inside': inside, 'corner': corner, 'above': above,
         'horn-formed': lambda: horn_pair(False), 'horn-laminated': lambda: horn_pair(True), 'lineup-stock': lineup}
for _c in ('ember', 'smoke'):
    for _r in ('formed', 'stepped', 'smooth'):
        SHOTS[f'choice-{_r}-{_c}'] = (lambda r=_r, c=_c: horn_choice(r, c))
SHOTS['choice-terraces-ember'] = lambda: horn_choice('stepped', 'ember', macro=True)
for _d in ('current', 'strata', 'topo', 'topo-clear'):
    SHOTS[f'design-{_d}'] = (lambda d=_d: proposal(d))


def _macro(design):
    s = proposal(design)
    s['title'] += ', macro'
    s['size'] = [1600, 1600]
    if design == 'strata':          # the caldera and the woofer, from the front right, low
        s['camera'] = {'position': [0.62, -1.05, 0.58], 'target': [0.0, -0.02, 0.47], 'lens_mm': 85.0, 'level': False,
                       'fstop': 5.6, 'focus': [0.12, -0.03, 0.47]}
    else:                           # the horn's terraces, from the front right, a little above
        s['camera'] = {'position': [0.75, -1.2, 1.32], 'target': [0.05, 0.05, 1.07], 'lens_mm': 85.0, 'level': False,
                       'fstop': 5.6, 'focus': [0.2, -0.05, 1.07]}
    return s


def _in_use(design):
    s = proposal(design, base='spinoffs/barkhorn/campaign/shots/room-final.json', flavour='eucalyptus-y2k-green')
    s['title'] = f'Tropos, {design} (design pass), at home at golden hour, Poison'
    return s


for _d in ('strata', 'topo', 'topo-clear'):
    SHOTS[f'design-{_d}-macro'] = (lambda d=_d: _macro(d))
    SHOTS[f'design-{_d}-room'] = (lambda d=_d: _in_use(d))
SHOTS['design-current-room'] = lambda: _in_use('current')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SHOTS.items():
        json.dump(fn(), open(os.path.join(OUT, f'{name}.json'), 'w'), indent=1)
        print(name)
