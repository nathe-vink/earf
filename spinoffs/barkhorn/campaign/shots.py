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
        if design == 'strata':      # the Strata horn (with its lip), its bronze posts and collars, and the caldera
            for i in inst:          # the pads stay (the posts thread into them); the stainless posts and cups go
                i['hide'] = sorted((set(i['hide']) - {'horn-pads'}) | {'post-*', 'post-sockets', 'post-sleeves'})
            prods.append({'def': VARIANTS, 'flavour': flavour, 'instances': [{**keep(i), 'hide': ['horn-topo']} for i in inst]})
        elif design == 'topo':
            prods.append({'def': VARIANTS, 'flavour': flavour,
                          'instances': [{**keep(i), 'hide': ['caldera-*', 'horn-strata', 'strata-*']} for i in inst]})
        else:                       # topo-clear: the clear layers and their tinted laminae (an option in the product)
            prods.append({'def': VARIANTS, 'flavour': flavour,
                          'instances': [{**keep(i), 'hide': ['caldera-*', 'horn-topo', 'horn-strata', 'strata-*'], 'options': ['Topo Clear']} for i in inst]})
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


def room_off_portrait():
    """The same room, covers off, as a portrait for phones (the site's "At home" band): round 31's phone framing (a
    35 mm lens 3.9 m from the speakers, aimed up at 1.25 m so the wall above takes the heading), adjusted after its
    proof, a little toward the window."""
    s = room_off()
    s['title'] += ', portrait'
    s['size'] = [1600, 2000]
    ty = s['camera']['target'][1]
    # (the proof at 35 mm, 3.9 m, aiming at 1.25: the pair small and a band of ceiling; 40 mm from 4.1 m at 0.95 puts the
    # ceiling line at the frame's top and the pair larger)
    s['camera'] = {'position': [-0.1, ty - 4.1, 1.05], 'target': [-0.1, ty, 0.95], 'lens_mm': 40.0, 'level': True,
                   'fstop': 5.6, 'focus': s['camera'].get('focus', [0.0, ty - 0.21, 0.7])}
    return s


SHOTS = {'room': room, 'room-final': lambda: room(critic_round=3),   # round 3's look (7.0): the final
         'room-final-off': room_off, 'room-final-off-portrait': lambda: room_off_portrait(), 'night': night, 'inside': inside, 'corner': corner, 'above': above,
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
        # (its first proof, from the front right, showed the woofer and only a sliver of the steps: from further round,
        # so the caldera's terraces carry the frame)
        s['camera'] = {'position': [0.92, -0.78, 0.6], 'target': [0.02, -0.02, 0.47], 'lens_mm': 85.0, 'level': False,
                       'fstop': 6.3, 'focus': [0.2, -0.02, 0.47]}
    else:                           # the horn's terraces, from the front right, a little above
        s['camera'] = {'position': [0.75, -1.2, 1.32], 'target': [0.05, 0.05, 1.07], 'lens_mm': 85.0, 'level': False,
                       'fstop': 5.6, 'focus': [0.2, -0.05, 1.07]}
    return s


BASES = {'plinth': ('Plinth', 0.0385), 'outriggers': ('Outriggers', 0.0202)}   # the option, and how far it lifts the cabinet (m)


def base(which, view='hero'):
    """Strata on a base for the stability test (the engineering audit, 2026-11-01; variants/variants.py PLINTH, OUTRIG):
    'plinth' (A, stepped frames of 1/2 in sheet), 'outriggers' (B, bronze arms), or 'today' (the Cloud's own feet, for
    reference). The studio hero's frame, or a higher three-quarter view so the footprint reads."""
    s = proposal('strata')
    s['title'] = f'Tropos Strata on {which}' + (', three-quarter' if view == 'three-quarter' else '')
    if which != 'today':
        opt, lift = BASES[which]
        for blk in s['products']:
            for i in blk['instances']:
                i['position'] = [i['position'][0], i['position'][1], lift]
                if 'cloud' in blk['def']:
                    i['hide'] = sorted(set(i['hide']) | {'feet-base', 'feet-stem'})
                else:
                    i['options'] = [opt]
    if view == 'three-quarter':          # from higher and further round, so the base's footprint reads; whole speaker
        # (its first proof at 50 mm saw past the studio's sweep at the top left, the speaker small: a longer lens)
        # (and at 72 mm the base cut at the bottom: further back, on 85 mm)
        s['camera'] = {'position': [2.85, -3.1, 1.75], 'target': [0.0, 0.04, 0.6], 'lens_mm': 85.0, 'level': True,
                       'fstop': 6.3, 'focus': [0.25, -0.2, 0.5]}
    return s


def base_lit(view='hero', glow=None):
    """Strata on the stepped plinth lit from underneath (the owner, 2026-11-01): the studio frame, or 'dusk', the same
    frame with the studio's lamps brought down to about a tenth and cooled, so the plinth's warm glow on the floor
    carries the picture. The whole speaker, cover off."""
    s = base('plinth', 'three-quarter' if view == 'three-quarter' else 'hero')
    s['title'] = 'Tropos Strata on the lit plinth' + {'hero': '', 'dusk': ', dusk', 'three-quarter': ', three-quarter'}[view]
    for blk in s['products']:
        if 'variants' in blk['def']:
            for i in blk['instances']:
                i['options'] = ['Plinth', 'Plinth light']
    if view == 'dusk':
        for L in s['lights'].values():
            if 'irradiance' in L:
                L['irradiance'] = round(L['irradiance'] * 0.1, 3)
            L['color'] = '#C9D3E8'
        # (the first dusk proof: the right side read pale silver, the side face mirroring the kick light at a grazing
        # angle, not the batts; at dusk there is no kick)
        if 'kick' in s['lights']:
            s['lights']['kick']['irradiance'] = 0.0
        s['render']['exposure'] = s['render'].get('exposure', 0.0) + 1.3
        s['render']['white_balance_k'] = 4800
    if glow is not None:
        s.setdefault('materials', {})['led'] = {'glow': glow}
    return s


# the deck's LED level (the coordinator, 2026-11-01): 20 by day, 40 at dusk; every deck frame is a daylight frame
def deck_hero():
    """The deck's Tropos slide (the owner's final design, 2026-11-01): Strata in Ember on the lit plinth, the studio,
    2:3 portrait (shown at 720 x 1080, object-fit cover), the glow subtle but visible."""
    s = base_lit('hero', glow=20.0)
    s['title'] = 'Tropos, the deck hero (Strata, flush horn, lit plinth, Ember)'
    s['size'] = [1440, 2160]
    s['render']['samples'] = 192
    return s


SHOTS['deck-hero'] = deck_hero


# the two open answers (the coordinator, 2026-11-03): the base (A, its own feet and no light; D, the lantern built in;
# 'plinth', the lit plinth every shot so far has used) and the horn's outside (satin, the owner's spec; polished).
# rollout.py sets them for a whole set; the default keeps every existing shot as it was rendered
ROLLOUT = {'base': os.environ.get('TROPOS_BASE', 'plinth'), 'horn': os.environ.get('TROPOS_HORN', 'satin')}
D_OPTIONS = ['Built-in light', 'Built-in floor', 'Floor film']
# D's light as gate 3 passed it (gate2/D-night-ice-v2.png): the floor runs about 13 W/m, the brace 30 W/m, 4000 K
D_GLOW = {'builtin-led': 450.0, 'builtin-led-brace': 1020.0}


def strata_lit(s, glow=None, horn='smooth'):
    """Any shot's Tropos instances turned into the owner's final design, everything lifted onto the stepped plinth:
    since 2026-11-03 (the owner: "Horn: A, smooth"; polished outside since 15:14) the Cloud's formed horn on Strata's bronze
    posts, with the caldera, and the plinth's uplight (the owner, 2026-11-02: the light goes up through the speaker);
    `horn='stepped'` gives Strata's stepped horn, the documented alternative. `glow` keeps the old shots' meaning: 20 (by
    day) leaves the uplight at its default 50 %, 40 (at dusk) runs it at full."""
    blk = s.pop('product') if 'product' in s else s.pop('products')[0]
    on_feet = ROLLOUT['base'] in ('A', 'D')            # the cabinet on its own swivel feet, no plinth
    lift = 0.0 if on_feet else BASES['plinth'][1]
    hidden = {'cloth-disc', 'woofer-ring', 'post-*', 'post-sockets', 'post-sleeves'} | (set() if on_feet else {'feet-base', 'feet-stem'})
    if horn == 'stepped':
        hidden |= set(HORN_PARTS) - {'horn-pads'}
    inst = []
    for i in blk['instances']:
        x, y, z = (list(i.get('position', [0, 0, 0])) + [0, 0, 0])[:3]
        inst.append({**i, 'position': [x, y, z + lift], 'hide': sorted(set(i.get('hide', [])) | hidden)})
    keep = lambda i: {k: v for k, v in i.items() if k not in ('hide', 'options')}
    vhide = ['horn-topo*', 'base-out*'] + (['horn-strata'] if horn == 'smooth' else [])
    opts = {'A': [], 'D': D_OPTIONS}.get(ROLLOUT['base'], ['Plinth', 'Plinth uplight'])
    s['products'] = [{**blk, 'instances': inst},
                     {'def': VARIANTS, 'flavour': blk.get('flavour', 'cloud-red'),
                      'instances': [{**keep(i), 'hide': vhide, 'options': opts} for i in inst]}]
    mats = s.setdefault('materials', {})
    if ROLLOUT['base'] == 'plinth':
        if glow is not None and glow >= 40:
            mats.update({'uplight-edge': {'glow': 375.0}, 'uplight-panel': {'glow': 105.0}})
    else:                                              # A has no light; D's is off by day (the owner: off in day frames)
        night = glow is not None and glow >= 40 and ROLLOUT['base'] == 'D'
        mats.update({k: {'glow': (v if night else 0.0)} for k, v in D_GLOW.items()})
    if ROLLOUT['horn'] == 'polished':                  # the waveguide's outside as formed, not bead-blasted (asset/README.md)
        mats['horn-satin'] = {**mats.get('horn-satin', {}), 'roughness': 0.05}
    return s


def deck_row():
    """The deck's Colors slide: the eight in a row on white (studio31's line-up rig), Ember to Smoke, 3328 x 1040."""
    s = strata_lit(load('studio/shots/barkhorn/studio31/lineup.json'), glow=20.0)
    s['title'] = 'Tropos, the eight in a row (Strata on the lit plinth)'
    s['size'] = [3328, 1040]
    s['render']['samples'] = 160
    return s


SHOTS['deck-row'] = deck_row


def deck_cover():
    """The deck's cover (shown 1920 x 680 across the slide's bottom): the eight on one gentle curve in hero31's studio,
    each turned to the camera, the plinths glowing faintly; a calm, wide frame, 3840 x 1360, its top third clear for the
    headline."""
    import math
    s = load('studio/shots/barkhorn/hero31/hero.json')
    blk = s['product'] if 'product' in s else s['products'][0]
    order = ['cloud-red', 'cloud-orange', 'cloud-amber', 'eucalyptus-y2k-green', 'cloud-blue', 'cloud-violet', 'birch-fog-clear', 'cloud-black']
    cam_y = -15.0
    inst = []
    for k, fl in enumerate(order):
        x = (k - 3.5) * 0.98
        y = 0.9 - 0.055 * x * x                      # the ends a little forward, a gentle curve
        rz = math.degrees(math.atan2(x, y - cam_y))   # each turned to face the camera
        inst.append({'position': [round(x, 4), round(y, 4), 0.0], 'rotate_z': round(rz, 2), 'flavour': fl, 'hide': ['cloth-disc']})
    blk['instances'] = inst
    s = strata_lit(s, glow=20.0)
    s['title'] = 'Tropos, the deck cover: the eight on a curve (Strata on the lit plinth)'
    s['size'] = [3840, 1360]
    # (its first test at eye level with a 0.11 shift: the bases cut and no curve; a little higher, less shift)
    s['camera'] = {'position': [0.0, cam_y, 2.3], 'target': [0.0, 0.5, 0.62], 'lens_mm': 56.0, 'level': True,
                   'shift_y': 0.05, 'fstop': 5.6, 'focus': [0.0, 0.3, 0.7]}
    s['render']['samples'] = 128
    return s


SHOTS['deck-cover'] = deck_cover
# the deck's Home slide: the golden-hour room (754e16a9's scene, covers off) with the pair turned into the final design
SHOTS['deck-home'] = lambda: dict(strata_lit(room_off(), glow=20.0), title='Tropos at home, golden hour, Poison (the final design)')
SHOTS['deck-home-portrait'] = lambda: dict(strata_lit(room_off_portrait(), glow=20.0),
                                           title='Tropos at home, golden hour, Poison, portrait (the final design)')


# --- the site set in the final design (2026-11-01; SITE-SET-PLAN.md) ---------------------------------------------------
# tint: (flavour, the key of today's rigs). finals31 names Ice's frames 'blue' and Fog's 'ice'; studio31 uses the tint names.
SITE_TINTS = {'ember': ('cloud-red', 'red'), 'dust': ('cloud-orange', 'orange'), 'acid': ('cloud-amber', 'amber'),
              'poison': ('eucalyptus-y2k-green', 'green'), 'ice': ('cloud-blue', 'blue'), 'haze': ('cloud-violet', 'violet'),
              'fog': ('birch-fog-clear', 'ice'), 'smoke': ('cloud-black', 'black')}
SITE_FRAMES = {     # frame: (today's rig, size, the glow: 20 in daylight, 40 at dusk, the coordinator 2026-11-01)
    'front-off-tall': ('studio/shots/barkhorn/finals31/front-off-tall-{key}.json', [1000, 1250], 20.0),
    'front-off-wide': ('studio/shots/barkhorn/finals31/front-off-wide-{key}.json', [1800, 1200], 20.0),
    'hero-light':     ('studio/shots/barkhorn/studio31/hero-light-{tint}.json', [2400, 1350], 20.0),
    'side':           ('studio/shots/barkhorn/finals31/front-off-tall-{key}.json', [1000, 1250], 20.0),
    'back':           ('studio/shots/barkhorn/finals31/back-{key}.json', [880, 1100], 20.0),
}


def site(frame, tint):
    """One frame of the site set in the owner's final design (Strata, the flush horn, the lit plinth, cover off, the line's
    stock tints): today's rig for that frame and tint, at the site's size, 96 samples. 'side' is new: the tall front's
    studio seen from the speaker's right, a little forward of square, so the stepped horn's profile and the plinth's
    steps read; the whole speaker in frame."""
    fl, key = SITE_TINTS[tint]
    rig, size, glow = SITE_FRAMES[frame]
    s = load(rig.format(key=key, tint=tint))
    blk = s['product'] if 'product' in s else s['products'][0]
    blk['flavour'] = fl
    for i in blk['instances']:
        i['flavour'] = fl
        i['hide'] = sorted(set(i.get('hide', [])) | {'cloth-disc'})
    s = strata_lit(s, glow=glow)
    s['title'] = f'Tropos, {frame}, {tint} (the final design)'
    s['size'] = size
    s['render']['samples'] = 96
    if frame == 'side':
        # (its first proof moved the camera round to the speaker's side and saw past the sweep's edge: the camera stays
        # in the studio's frame and the speaker turns, its right side to the camera, a little of the front showing)
        for blk in s['products']:
            for i in blk['instances']:
                i['rotate_z'] = i.get('rotate_z', 0) - 50.0
    if frame == 'back':
        # (its first proof put the plinth's near corner on the frame's bottom edge: a little wider)
        s['camera']['lens_mm'] = round(s['camera']['lens_mm'] * 0.9, 1)
        # finals31's back rig had no finish block, so the backs skipped the finish the other frames get (the
        # coordinator caught it on Ice's back final, 2026-11-02): the same pass
        s['finish'] = {'enabled': True, 'white_in': 236, 'white_out': 236, 'contrast': 0.2, 'clarity': 0.05,
                       'sharpen': 0.3, 'sharpen_px': 0.7, 'grain': 1.5, 'grain_px': 1.0}
    _site_round1(s, frame)
    _site_round2(s, frame)
    _site_round3(s, frame)
    _siteF_round1(s, frame)
    _siteF_round2(s, frame)
    _siteF_round3(s, frame)
    # horn A (the owner, 2026-11-03): the rim lamp that lit the formed horn's shell from behind made it read flat, a sign
    # rather than a cone (renders/2026-11-02/barkhorn/horn-study/deep/README.md): off; the rest of the rig as it was
    if 'rim' in s.get('lights', {}):
        s['lights']['rim']['power_w'] = 0.0
    return s


def _siteF_round3(s, frame):
    """The fresh gate's round 3 (2026-11-02; CRITIC.md), carried into the finals (no further critic round): the
    clipped light through the side view's horn pulled back, the cabinets' fronts off clipping, the contact denser, the
    backgrounds evened. The deep horn's contrast stays (the coordinator: the design)."""
    L = s['lights']; c = s['set'].setdefault('contact', {})
    if frame == 'front-off-tall':
        L['key']['irradiance'] = 2.9; L['topline']['strength'] = 0.9         # the front off clipping (pale cyan)
        L['horn'].update(irradiance=8.0, position=[0.5, -1.4, 1.45])
        s['set']['flags'].append({'center_m': [1.9, -0.6, 1.2], 'size_m': [2.0, 2.5], 'normal': [-0.9, 0.4, 0.0], 'color': '#060606'})
        L['through'].update(size_m=[0.12, 0.12], irradiance=4.5)
        L['bg-left']['irradiance'] = 1.8; L['wall_left']['irradiance'] = 2.2; L['kick']['irradiance'] = 1.1
    elif frame == 'front-off-wide':
        c.update(strength=5.0, distance_m=0.30, core_strength=10.0, core_distance_m=0.025); L['wash']['irradiance'] = 0.15
        L['scrim'].update(strength=0.7); L['scrim']['ramp'] = {**L['scrim']['ramp'], 'values': [1.0, 0.6]}
        L['floor'].update(irradiance=0.35, position=[-1.6, -2.4, 4.5])     # the grey wedge front-left
        L['kick'].update(irradiance=1.8, size_m=[1.6, 2.4])
        L['topline']['strength'] = 1.8
        s['finish'].update(sharpen=0.04, clarity=0.02)
    elif frame == 'hero-light':
        c.update(strength=7.0, distance_m=0.25, core_strength=30.0, core_distance_m=0.012)
        L['key'].update(size_m=[3.0, 3.0]); L['key']['orbit']['elevation_deg'] = 60   # the blue cast pools near the plinth
        L['bg-left']['irradiance'] = 1.8; L['bg-right']['irradiance'] = 0.9
        L['scrim'].update(position=[0.1, -0.5, 2.6], irradiance=4.2)
        s['render']['white_balance_tint'] = -0.5
    elif frame == 'side':
        L['horn'].update(irradiance=3.0, specular=0.6); L['rim']['power_w'] = 120     # the blown white wedge in the throat
        L['sidesheen'].update(strength=2.2, position=[2.0, -1.6, 0.8])
        L['sidesheen']['ramp'] = {**L['sidesheen']['ramp'], 'values': [0.2, 1.0]}
        c.update(strength=1.8, distance_m=0.4, core_strength=3.6, core_distance_m=0.025)
        L['bg-right']['irradiance'] = 0.45
        L['fill'].update(irradiance=1.6); L['fill']['orbit'].update(azimuth_deg=20, elevation_deg=18)
        L['topline'].update(strength=0.7, size_m=[2.4, 0.8]); L['scrim']['strength'] = 0.6
        # The backdrop up to the set's level (the coordinator, 2026-11-02: 166 against the tall's 215): the sweep's own
        # lights x2.1, the speaker's untouched (proxies: x1.6 gives 195, x2.0 gives 211)
        for n in ('bg-left', 'bg-right', 'wall_left'):
            L[n]['irradiance'] = round(L[n]['irradiance'] * 2.1, 3)
    elif frame == 'back':
        L['cab-back'].update(irradiance=7.0, position=[-0.25, 0.6, 1.0]); L['fill']['irradiance'] = 1.3
        c.update(distance_m=0.3); L['key']['size_m'] = [1.6, 1.2]; L['key']['orbit']['elevation_deg'] = 22
        L['etch-rake'].update(irradiance=5.0, position=[0.32, -0.12, 0.84], size_m=[0.6, 0.03])
        # The mark test (2026-11-02, variant A, the coordinator's pick): the etch rake off, so the R no longer
        # reads as a B; the plate strip lowered so its glare clears the mark panel.
        L['etch-rake']['irradiance'] = 0.0
        L['plate-strip'].update(position=[0.35, -0.9, 0.55], target=[0.1, -0.17, 0.45])
        s['set']['flags'][-2].update(center_m=[-0.8, 0.3, 0.9], size_m=[1.6, 2.2])


def _siteF_round2(s, frame):
    """The fresh gate in colors F, round 2 (2026-11-02; CRITIC.md): the horn still a navy block, the lining clipping
    through the walls, the speakers still light on the floor. Light, set and camera only (not caustics, the LED, or a
    darker backdrop: the coordinator's)."""
    L = s['lights']; c = s['set'].setdefault('contact', {})
    if frame == 'front-off-tall':
        L['rim'].update(position=[0.0, 0.7, 1.35], power_w=260, size_m=[1.2, 0.8], target=[0.05, -0.05, 1.12])
        L['key'].update(irradiance=3.8, size_m=[1.4, 1.8])                  # the lining burnt through the walls
        c.update(strength=1.7, distance_m=0.4, core_strength=2.2); L['floor']['irradiance'] = 0.0
        L['through'] = {'type': 'area', 'size_m': [0.25, 0.25], 'orbit': {'azimuth_deg': 165, 'elevation_deg': 28, 'distance_m': 2.2},
                        'target': [0.0, -0.35, 0.0], 'irradiance': 3.0, 'color': '#FFF8F0'}   # blue light onto the floor
        L['wall_left']['irradiance'] = 2.6; L['bg-high']['irradiance'] = 0.6
        L['fill']['specular'] = 1.0; L['fill']['orbit'].update(azimuth_deg=15, elevation_deg=40)
    elif frame == 'side':
        L['rim'].update(power_w=240, position=[0.3, 0.6, 1.25]); L['back']['irradiance'] = 6.0
        L['sidesheen']['strength'] = 1.1; L['sidesheen']['ramp'] = {**L['sidesheen']['ramp'], 'values': [0.45, 0.8]}
        L['kick'].update(target=[0.28, 0.0, 0.35], irradiance=3.4)
        L['bg-left']['irradiance'] = 0.6; L['wall_left']['irradiance'] = 1.1; L['floor']['irradiance'] = 0.15
        L['horn'].update(position=[1.2, -0.9, 1.3], irradiance=6.0)
    elif frame == 'back':
        L['glow']['irradiance'] = 9.0
        L['cab-back'] = {'type': 'area', 'size_m': [0.6, 1.0], 'position': [-0.35, 0.55, 0.7], 'target': [0.0, 0.0, 0.6],
                         'irradiance': 4.0, 'color': '#FFF1DC', 'specular': 0.0, 'transmission': True}   # through the cabinet
        L['d-wall']['irradiance'] = 0.0
        L['wash'].update(irradiance=0.35, position=[0.0, 1.2, 1.4], target=[0.0, 1.5, 0.3])
        L['key'].update(size_m=[1.0, 0.8], irradiance=2.6); L['key']['orbit'].update(azimuth_deg=-55, elevation_deg=28)
        L['etch-rake'].update(irradiance=2.8, position=[0.30, -0.20, 0.86])
        L['plate-strip'] = {'type': 'area', 'size_m': [0.6, 0.08], 'position': [0.35, -0.9, 0.9], 'target': [0.1, -0.17, 0.55],
                            'irradiance': 1.0, 'color': '#FFF3E1'}
        s['render']['exposure'] = -0.5
    elif frame == 'front-off-wide':
        L['floor']['irradiance'] = 0.2; L['wash']['irradiance'] = 0.3
        c.update(strength=4.0, distance_m=0.45, core_strength=7.0, core_distance_m=0.015)
        L['back'].update(size_m=[0.5, 0.4], irradiance=5.0); L['back']['orbit']['elevation_deg'] = 24
        L['paper']['power_w'] = 12.0
        L['bg-left']['irradiance'] = 0.6; L['bg-right']['irradiance'] = 0.9; L['bg-high']['irradiance'] = 0.2
        L['key']['irradiance'] = 4.2; L['topline']['strength'] = 1.2
        L['rim'].update(size_m=[1.4, 0.8], power_w=22)
        s['finish'].update(contrast=0.28, white_in=240)
    elif frame == 'hero-light':
        c.update(strength=4.5, distance_m=0.35, core_strength=14.0, core_distance_m=0.02)
        L['key'].update(irradiance=6.5, size_m=[2.4, 2.4]); L['key']['orbit']['elevation_deg'] = 46
        L['bg-left'].update(irradiance=2.6, target=[-2.6, 6.0, 0.6]); L['bg-right'].update(irradiance=0.7, target=[3.5, 6.0, 0.8])
        s['set']['bounces'][0]['reflect_only'] = False
        L['scrim']['irradiance'] = 2.8; s['render']['white_balance_tint'] = 0.5


def _siteF_round1(s, frame):
    """The fresh gate in colors F, round 1 (2026-11-02; renders/2026-11-02/barkhorn/site-strata-F/CRITIC.md): still light
    on the floor; Ice's deep horn a dark mass beside the paler cabinet (three critics), so a light behind the horn
    through its layers; the sweeps flat or uneven. Light, set and camera only."""
    L = s['lights']; c = s['set'].setdefault('contact', {})
    if frame == 'front-off-tall':
        L['rim'].update(position=[0.0, 0.6, 1.6], target=[0.05, 0.0, 1.15], power_w=80, size_m=[1.0, 0.6])
        L['horn']['size_m'] = [2.5, 1.6]
        c.update(strength=1.0, distance_m=0.25, core_strength=1.6, core_distance_m=0.012); L['pool']['irradiance'] = 0.0
        L['bg-right']['irradiance'] = 0.35; L['bg-left']['irradiance'] = 1.4; L['wall_left']['irradiance'] = 3.8
        L['scrim']['strength'] = 0.25; L['topline']['strength'] = 1.6
        L['kick']['irradiance'] = 1.6; L['kick']['orbit'].update(azimuth_deg=75, elevation_deg=40)
    elif frame == 'side':
        c.update(strength=1.4, core_strength=2.6, core_distance_m=0.05)
        L['pool']['irradiance'] = 0.2; L['floor']['irradiance'] = 0.08
        L['horn']['irradiance'] = 5.5; L['rim'].update(power_w=95, position=[0.5, 0.4, 1.5])
        L['bg-right']['irradiance'] = 0.2; L['wall_left']['irradiance'] = 1.5; L['bg-left']['irradiance'] = 0.85
        L['topline']['strength'] = 1.2; L['sidesheen']['strength'] = 1.6
    elif frame == 'back':
        L['d-floor']['irradiance'] = 0.0; L['d-wall'].update(irradiance=0.10, target=[0.0, 1.5, 1.2])
        s['set']['color'] = '#EDE6DC'
        c.update(strength=1.0, distance_m=0.12); L['key']['size_m'] = [1.6, 1.2]
        L['etch-rake'] = {'type': 'area', 'size_m': [0.8, 0.05], 'position': [0.165, -0.236, 0.95], 'target': [0.12, -0.17, 0.80],
                          'irradiance': 1.2, 'color': '#FFF3E1'}          # the etched mark, at a grazing angle
        L['horn-rim'].update(irradiance=3.5, position=[0.0, 0.7, 1.35], size_m=[1.0, 0.4])
        L['fill'].update(irradiance=2.2, size_m=[1.2, 1.6]); L['fill']['orbit'].update(azimuth_deg=5, elevation_deg=25)
        s['render'].update(exposure=-0.35, clamp=6)
        s['set']['flags'].append({'center_m': [1.2, 0.3, 0.9], 'size_m': [1.0, 2.0], 'normal': [-0.97, -0.24, 0.0],
                                  'reflect_only': True, 'color': '#060606'})
        s['camera'].update(lens_mm=62.0, target=[s['camera']['target'][0], s['camera']['target'][1], 0.55])
    elif frame == 'front-off-wide':
        c.update(strength=2.6, distance_m=0.30, core_strength=5.0, core_distance_m=0.012)
        L['cove_far']['target'] = [-7.0, 3.5, 0.3]; L['floor'].update(size_m=[10.0, 6.0], position=[-1.0, -2.0, 4.5])
        s['set']['radius'] = 3.6
        L['back'].update(irradiance=3.0); L['back']['orbit']['elevation_deg'] = 38
        L['back']['receivers'] = L['back']['receivers'] + ['sweep']    # the blue through the cabinet onto the floor
        L['bg-left']['irradiance'] = 0.9; L['wash'].update(irradiance=0.6, position=[0.8, -1.4, 3.0])
        L['sidesheen'].update(strength=0.9, size_m=[1.4, 2.4]); s['finish']['sharpen'] = 0.08
    elif frame == 'hero-light':
        c.update(strength=3.0, distance_m=0.30, core_strength=6.0, core_distance_m=0.035)
        s['render'].update(white_balance_k=5900, white_balance_tint=2.0)  # the set read cool against its #F3F1EE
        L['bg-right']['irradiance'] = 1.0; L['bg-left']['irradiance'] = 2.9
        L['key']['irradiance'] = 6.0; L['key']['orbit'].update(azimuth_deg=-20, elevation_deg=32)
        L['front-strip']['strength'] = 6.0; L['front-strip']['orbit']['azimuth_deg'] = -32
        L['back-top']['irradiance'] = 26.0; L['back-top']['orbit']['azimuth_deg'] = 140
        s['materials']['sweep']['roughness'] = 0.25; L['scrim']['irradiance'] = 4.0; s['finish']['clarity'] = 0.0


def _site_round3(s, frame):
    """The Ice gate's third round (2026-11-01, renders/2026-11-01/barkhorn/site-strata/CRITIC.md): its notes, logged but
    not applied then, carried into the fresh gate in colors F (the coordinator, 2026-11-02). Light, set and camera only."""
    L = s['lights']; c = s['set'].setdefault('contact', {})
    if frame == 'front-off-tall':
        L['edge']['power_w'] = 0.3                                            # the front-right edge a flat white bar
        L['kick']['irradiance'] = 1.3; L['kick']['orbit']['elevation_deg'] = 35
        L['horn'].update(size_m=[2.0, 1.2], irradiance=6.5, specular=0.6, position=[0.6, -1.5, 1.7])
        c.update(strength=0.8, distance_m=0.35, core_strength=1.0, core_distance_m=0.025)
        L['fill'].update(irradiance=1.6, specular=0.5); L['fill']['orbit'].update(azimuth_deg=25, elevation_deg=30)
        L['bg-left'].update(irradiance=1.2, target=[-1.5, 4.5, 0.6])      # the dark band on the left sweep
        L['scrim']['strength'] = 0.5
    elif frame == 'front-off-wide':
        c.update(strength=1.6, core_strength=2.5, core_distance_m=0.025, distance_m=0.22)
        L['pool']['irradiance'] = 0.15; L['floor']['irradiance'] = 0.45
        L['cove_far'].update(irradiance=4.2, target=[-8.0, 4.5, 1.4]); L['wall_left']['irradiance'] = 3.2   # the cove band
        L['horn'].update(irradiance=2.6, spread_deg=25, position=[1.1, -1.0, 1.6]); L['rim']['power_w'] = 30
        L['edge']['power_w'] = 0.8; L['sidesheen']['strength'] = 1.4
        L['bg-right']['irradiance'] = 1.4; L['bg-high']['irradiance'] = 0.4
        L['scrim']['strength'] = 0.4; L['topline']['strength'] = 1.8
    elif frame == 'hero-light':
        L['bg-left']['irradiance'] = 2.6; L['bg-right'].update(irradiance=1.6, target=[3.5, 6.0, 2.0])
        c.update(strength=2.0, distance_m=0.35, core_strength=3.2, core_distance_m=0.02)
        L['back-top']['irradiance'] = 22.0; L['back-top']['orbit'].update(azimuth_deg=160, elevation_deg=55)   # the floor streak
        s['render'].update(white_balance_tint=0.0, white_balance_k=5600)      # the plinth violet from a magenta tint
        L['key'].update(irradiance=5.5, size_m=[1.8, 1.8]); L['key']['orbit'].update(azimuth_deg=-40, elevation_deg=30)
        L['scrim']['irradiance'] = 4.5
        s['finish'].update(white_in=245, contrast=0.15)
    elif frame == 'side':
        L['sidesheen']['strength'] = 2.2; L['rim']['power_w'] = 55
        c.update(core_distance_m=0.03, core_strength=1.4)
        L['floor']['irradiance'] = 0.15; L['wall_left']['irradiance'] = 2.1
    elif frame == 'back':
        # the left side and the top mirrored the bright sweep: a black card off the left face, out of frame
        s['set'].setdefault('flags', []).append({'center_m': [-1.0, 0.75, 0.9], 'size_m': [1.2, 2.0], 'normal': [0.66, -0.76, 0.0],
                                                  'reflect_only': True, 'color': '#060606'})
        L['key']['orbit'].update(azimuth_deg=-35, elevation_deg=40)
        L['d-wall'].update(irradiance=0.15, target=[0.0, 1.5, 0.2])
        L['wash'].update(irradiance=0.15, position=[0.0, 0.8, 2.9], size_m=[3.0, 0.6])
        s['render']['exposure'] = s['render'].get('exposure', 0.0) - 0.2
        c.update(strength=0.9, distance_m=0.06); L['d-floor']['irradiance'] = 0.08
        L['fill'].update(irradiance=1.8, size_m=[2.0, 2.0]); L['fill']['orbit'].update(azimuth_deg=20, elevation_deg=18)
        L['horn-rim'] = {'type': 'area', 'size_m': [1.2, 0.15], 'position': [-0.3, 0.6, 1.6], 'target': [0.0, 0.0, 1.2],
                         'irradiance': 1.5, 'color': '#FFF3E1'}           # the horn's layer edges


def _site_round2(s, frame):
    """The Ice proofs' second critic round (2026-11-01; all five at 5.5): the speaker still light on the floor, the horn
    and the side faces dark, the backdrops uneven. Light, set and camera only (CRITIC.md)."""
    L = s['lights']; c = s['set'].setdefault('contact', {})
    if frame == 'front-off-tall':
        L['floor']['irradiance'] = 0.15; L['wash']['irradiance'] = 0.0; L['pool']['irradiance'] = 0.2
        c['core_distance_m'] = 0.06
        L['key']['size_m'] = [1.0, 1.3]; L['key']['orbit']['distance_m'] = 2.2      # a smaller key, set back: a shadow
        L['horn']['irradiance'] = 5.0; L['rim']['power_w'] = 30
        L['wall_left']['irradiance'] = 3.0; L['bg-left']['irradiance'] = 0.9
        L['edge']['power_w'] = 1.0; L['sidesheen']['strength'] = 0.9
    elif frame == 'front-off-wide':
        L['cove_far']['irradiance'] = 3.0; L['floor'].update(irradiance=0.6, spread_deg=80)   # the banded floor
        c.update(core_strength=1.0, core_distance_m=0.05, distance_m=0.30); L['scrim']['strength'] = 0.6
        L['wash']['irradiance'] = 0.45
        L['bg-right'].update(irradiance=1.1, target=[1.0, 6.0, 1.6])
        L['sidesheen']['strength'] = 1.0; L['kick']['irradiance'] = 2.6
        L['topline'].update(strength=2.2, position=[-1.0, -2.1, 1.1])
    elif frame == 'side':
        # the side face mirrors the sidesheen panel: moved to its mirror position about the face, from the camera
        L['sidesheen'].update(position=[2.2, -1.2, 0.7], target=[0.28, -0.1, 0.55], size_m=[0.9, 2.2], strength=1.4)
        L['sidesheen']['ramp'] = {**L['sidesheen']['ramp'], 'values': [0.05, 1.0]}
        L['back'].update(target=[0.05, 0.0, 1.12], irradiance=4.0, size_m=[1.0, 0.8])
        L['back']['orbit'].update(azimuth_deg=150, elevation_deg=30, distance_m=1.6)     # through the horn's layers
        L['rim'].update(position=[0.7, -0.6, 1.6], target=[0.15, 0.0, 1.12], power_w=30)
        L['rim']['receivers'] = L['rim']['receivers'] + ['hf-*']
        L['wall_left']['irradiance'] = 2.6; L['bg-right']['irradiance'] = 0.5; L['floor']['irradiance'] = 0.25
        s['render'].update(white_balance_k=5900, white_balance_tint=0.0)
        c.update(core_strength=1.0, core_distance_m=0.015, distance_m=0.35)
        L['key']['size_m'] = [1.4, 1.8]; L['key']['orbit'].update(azimuth_deg=-45, elevation_deg=28)
        # (round 3: the black reflect-only flag at [1.6, -1.2, 1.2] stood between the side face and the moved sidesheen,
        # so the face still mirrored black; the coordinator, 2026-11-01: take it out)
        s['set']['flags'] = [f for f in s['set'].get('flags', []) if f.get('center_m') != [1.6, -1.2, 1.2]]
    elif frame == 'back':
        L['wash']['irradiance'] = 0.3                                                   # the side and top mirrored it
        L['glow'].update(irradiance=5.0, transmission=True, size_m=[0.9, 0.5])
        L['fill'].update(irradiance=1.1, size_m=[1.5, 1.5]); L['fill']['orbit'].update(azimuth_deg=10, elevation_deg=10)
        c.update(strength=0.6, distance_m=0.12)
        L['d-wall']['irradiance'] = 0.25
    elif frame == 'hero-light':
        c.update(strength=1.4, distance_m=0.5, core_strength=2.2, core_distance_m=0.025)
        L['back-top']['irradiance'] = 45.0; L['back-top']['orbit'].update(azimuth_deg=190, elevation_deg=35)
        L['scrim']['irradiance'] = 3.6
        L['bg-left'].update(position=[-3.6, 3.0, 3.6], target=[-2.6, 6.0, 1.2], irradiance=3.4)   # the grey top-left
        s['materials']['sweep']['roughness'] = 0.35


def _site_round1(s, frame):
    """The Ice proofs' first critic round (2026-11-01, framing and light only; renders/2026-11-01/barkhorn/site-strata/
    CRITIC.md): every frame floated (no contact shadow, the floor fills as bright as the open floor) on a flat ground.
    Material notes (the tints, the lining, the plinth's glow) and sample counts are set aside."""
    L = s['lights']; c = s['set'].setdefault('contact', {})
    if frame in ('front-off-tall', 'front-off-wide', 'side'):          # finals31's studio
        L['floor']['irradiance'] = 0.35; L['wash']['irradiance'] = 0.2; L['pool']['irradiance'] = 0.4
        c.update(strength=1.0, distance_m=0.45, core_distance_m=0.03)
        L['bg-right']['irradiance'] = 0.8; L['bg-high']['irradiance'] = 0.0; L['wall_left']['irradiance'] = 3.6
        L['horn']['irradiance'] = 3.2; L['rim']['power_w'] = 18              # the horn's shaded terraces crushed
        if frame == 'front-off-tall':
            L['back']['irradiance'] = 1.6                                     # the lower interior too busy
            L['topline']['strength'] = 2.6                                    # the bronze posts read as metal
        if frame == 'front-off-wide':                                         # 32 mm leaned the verticals: 50 mm, further back
            s['camera'].update(position=[1.86, -3.87, 0.95], lens_mm=50.0)
            s['finish']['sharpen'] = 0.15
        if frame == 'side':                                                   # the side panel a dead slab: rake it
            L['kick'].update(irradiance=2.8); L['kick']['orbit'].update(azimuth_deg=75, elevation_deg=25)
    elif frame == 'back':                                                     # finals31's back rig
        L['d-floor']['irradiance'] = 0.0; L['fill']['irradiance'] = 0.6
        L['d-wall'].update(irradiance=0.2, position=[0.0, -0.5, 1.6], target=[0.0, 1.5, 0.6])
        L['key']['irradiance'] = 2.6; L['key']['orbit'].update(azimuth_deg=-60, elevation_deg=32)   # the amplifier's plate
        L['glow'].update(irradiance=2.4, position=[0.0, 0.55, 1.35])        # the horn from behind
        s['camera']['target'] = [s['camera']['target'][0], s['camera']['target'][1], 0.52]
    elif frame == 'hero-light':                                               # studio31's light hero
        c.update(strength=1.0, core_strength=1.0, core_distance_m=0.04)
        L['scrim']['irradiance'] = 2.6
        L['bg-left'].update(irradiance=2.8, target=[-1.5, 6.0, 0.6]); L['bg-right'].update(irradiance=2.8, target=[0.9, 6.0, 0.6])
        L['back-top']['irradiance'] = 30.0; L['back-top']['orbit']['elevation_deg'] = 45
        s['camera']['target'] = [-0.55] + s['camera']['target'][1:]          # the speaker to the right third, room for the heading
        s.setdefault('materials', {}).setdefault('sweep', {})['roughness'] = 0.6


for _f in SITE_FRAMES:
    for _t in SITE_TINTS:
        SHOTS[f'site-{_f}-{_t}'] = (lambda f=_f, t=_t: site(f, t))

for _v in ('hero', 'dusk', 'three-quarter'):
    SHOTS['base-plinth-lit' + {'hero': '', 'dusk': '-dusk', 'three-quarter': '-34'}[_v]] = (lambda v=_v: base_lit(v))


for _b in ('plinth', 'outriggers', 'today'):
    for _v in ('hero', 'three-quarter'):
        SHOTS[f'base-{_b}' + ('' if _v == 'hero' else '-34')] = (lambda b=_b, v=_v: base(b, v))


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
