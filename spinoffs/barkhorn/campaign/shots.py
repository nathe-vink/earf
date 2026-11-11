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


def _hero_gate3(s):
    """The deck hero's fixes (the coordinator's blind critics on 67f795ab, 2026-11-03, 3 HOLD): the same family as the
    tall front's, on the same rig. The lower right side face mirrored the lit floor (pale pink, saturation about 0.2), the
    top chamber clipped flat coral, and the lid's front edge read as a neutral grey strip. The tall front's fix carries
    over whole (_siteG_round1: sidesheen and through off, a reflect-only black card where the right face's mirror ray
    goes from this camera, the top light x0.65, the key 5 deg round), and the topline, the panel that put the lid's edge
    line there, comes down to a third, so the edge reads dark red with a glint like the vertical edges."""
    _siteG_round1(s, 'front-off-tall', 'ember')
    if 'topline' in s['lights']:
        s['lights']['topline']['strength'] = round(s['lights']['topline']['strength'] / 3, 3)
    # (its proxy: the side face deep red, 0.58 to 0.83 saturation above, but the top chamber still clipped on 38 % and
    # the lid's strip still grey, 170: from this camera, 0.4 m above the lid, the strip is the lid's top at a grazing
    # angle mirroring the bright sweep behind, about 1.5 m left of the speaker at 2.6 m back. A reflect-only black card
    # there, and the top light down again, to 0.4 of the rig's)
    if 'horn' in s['lights'] and s['lights']['horn'].get('irradiance'):
        s['lights']['horn']['irradiance'] = round(s['lights']['horn']['irradiance'] * 0.6, 3)
    s['set'].setdefault('flags', []).append({'center_m': [-1.2, 2.5, 1.1], 'size_m': [2.6, 1.6], 'normal': [0.46, -0.88, -0.16],
                                             'reflect_only': True, 'color': '#050505'})
    # (the fourth proxy: the lower right face still brownish, saturation 0.45: from 0.4 m down, its mirror rays fall to
    # the floor within a metre behind and right of the speaker, short of the card. A reflect-only black patch there)
    s['set']['flags'].append({'center_m': [0.62, 0.75, 0.004], 'size_m': [0.9, 1.5], 'normal': [0.0, 0.0, 1.0],
                              'reflect_only': True, 'color': '#050505'})
    L = s['lights']
    # (the top chamber, clipped coral on 26 % in a crop with all of the above: the key's light through the front onto the
    # top chamber's linings. Without links (the coordinator, 2026-11-03: no light a real lamp cannot give), crop tests:
    # the key at -60 deg (from -40): (205, 63, 63), 26 % at 250, to (170, 1, 2), 0 %, the woofer 64 to 53; at -52
    # (180, 4, 5); at elevation 10 the clip worse, 64 %; the key at 0.6 with more fill (192, 46, 46), 0 %; AgX no clip
    # but pink, (183, 87, 77). The key goes round to -60 and the fill up from 1.6 to 2.4: (175, 1, 2), the woofer 58)
    if 'key' in L and 'orbit' in L['key']:
        L['key']['orbit']['azimuth_deg'] = -60.0
    if 'fill' in L and L['fill'].get('irradiance'):
        L['fill']['irradiance'] = 2.4
    # (the fifth proxy: the right face deep red, (52, 1, 1) low and (82, 23, 26) high, which shows the `edge` glint as a
    # white bar a little in from its front edge, hidden before under the face's pale reflection: to a third)
    if 'edge' in L and L['edge'].get('power_w'):
        L['edge']['power_w'] = round(L['edge']['power_w'] / 3, 3)
    honest_lights(s)                                       # the owner's rule (horn to specular 1, kick and back unlinked)
    if 'back' in L:                                        # as the site frames: unlinked, it lit the floor the face mirrors
        L['back']['irradiance'] = 0.0
    # (the honest proxy: the lower right face 0.38, mirroring the lit floor right of the speaker, and the lid's strip
    # (101, 93, 87), its top mirroring the sweep at grazing. Staging, as a photographer would (the coordinator, 21:14):
    # the speaker turned 6 deg toward the camera and the camera 0.15 m lower)
    for blk in s['products']:
        for i in blk['instances']:
            i['rotate_z'] = i.get('rotate_z', 0.0) - 6.0
    s['camera']['position'][2] = round(s['camera']['position'][2] - 0.15, 3)
    cards_out_of_frame(s)
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
    else:   # satin, said outright: since the owner's 15:14 call the product files carry 0.05, so satin no longer falls back
        mats['horn-satin'] = {**mats.get('horn-satin', {}), 'roughness': 0.25}
    return s


def deck_row():
    """The deck's Colors slide: the eight in a row on white (studio31's line-up rig), Ember to Smoke, 3328 x 1040."""
    s = strata_lit(load('studio/shots/barkhorn/studio31/lineup.json'), glow=20.0)
    s['title'] = 'Tropos, the eight in a row (Strata on the lit plinth)'
    s['size'] = [3328, 1040]
    s['render']['samples'] = 160
    return s


def _row_gate3(s):
    """The deck row's fixes (the coordinator's blind critics, 2026-11-03, 2 HOLD 1 SHOW): the camera-right side faces
    mirrored the white sweep and the key (Smoke's a silver panel, Ice and Haze milky) and each its neighbour (Poison a blue
    stripe from Ice). A black card behind and right of the row, seen only in reflections (no shadow, no bounce), where the
    side faces' mirror rays go (about +0.75 x, +0.66 y from a face turned -24 deg); the units a little wider apart; and the
    sweep's falloff at the bottom left lifted by a soft lamp on the sweep alone."""
    blk = s['products'][0]
    n = len(blk['instances'])
    for k, i in enumerate(blk['instances']):
        i['position'] = [round((k - (n - 1) / 2) * 1.0, 4)] + list(i['position'][1:])
    for blk2 in s['products'][1:]:
        for k, i in enumerate(blk2['instances']):
            i['position'] = [round((k - (n - 1) / 2) * 1.0, 4)] + list(i['position'][1:])
    s['set'].setdefault('flags', []).append({'center_m': [2.2, 2.6, 0.9], 'size_m': [13.0, 2.6], 'normal': [-0.75, -0.66, 0.0],
                                             'reflect_only': True, 'color': '#050505'})
    s['lights']['sweep-left'] = {'type': 'area', 'size_m': [6.0, 4.0], 'position': [-4.5, -5.0, 4.0], 'target': [-3.5, -2.5, 0.0],
                                 'irradiance': 1.2, 'color': '#FFFFFF', 'receivers': ['sweep']}
    # (its proxy: the glossy sweep at the bottom right mirrors the card, 237 to 215; the same lamp on the right)
    s['lights']['sweep-right'] = {**s['lights']['sweep-left'], 'position': [4.5, -5.0, 4.0], 'target': [3.5, -2.5, 0.0]}
    return s


def _row_turn(s, deg=-12.0):
    """The row without its in-frame card (the coordinator's rule, 20:17): at -24 deg the right sides mirrored the white
    sweep behind the row (Poison 0.84 to 0.25 without the card). The units turned more square to the camera, (a) of the
    four options (the coordinator, 21:06), so the sides show less and mirror further round."""
    for blk in s['products']:
        for i in blk['instances']:
            i['rotate_z'] = deg
    return s


def _row_sweep(s, color='#BDB9B3'):
    """(d) of the row's four options (the coordinator, 21:06): (a), the units at -12 deg, washed the fronts (Ember's
    saturation 0.76 to 0.60) without saving the sides. A darker sweep for the row: what the sides mirror is darker."""
    s['set']['color'] = color
    return s


# (the proxies, 0.3 scale, right-side saturation Ember..Smoke: the in-frame card 0.96 .89 .87 .84 .72 .71 .01 .33; no card
# .94 .80 .69 .25 .33 .19 .01 .05; (a) alone washed the fronts (Ember 0.76 to 0.60); (d) alone, the sides .32 .39 .23 for
# Poison, Ice, Haze; (a) and (d) together .53 .57 .51 .83 .83 .86 .06 .42, the fronts deep (whole Poison .55, Ice .53))
SHOTS['deck-row'] = lambda: cards_out_of_frame(honest_lights(_row_turn(_row_sweep(_row_gate3(deck_row())))))


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
    # (its proxy after the hero's hold, 2026-11-03: Ember, at the left end turned to the camera, mirrored side_l in its
    # front, a pale pink patch on the upper left, (197, 156, 155), 12 % at 250. Its mirror ray from the front reaches
    # x -6 at y -3, z 0.2, inside that lamp's 0.6 x 3 m face. The lamp moves back to y -1.5, off that ray; Smoke's ray
    # at the other end reaches x 7 at about y -4.2, well clear of side_r at y -1. No links: the coordinator's rule)
    if 'side_l' in s['lights']:
        s['lights']['side_l']['position'] = [-6.0, -1.5, 1.4]
    # the owner's rule on light (the coordinator, 19:32 and 19:51): the cover's lamps linked to the panels or the drivers
    # are unlinked, the cyc, top and over lamps light through glass, the fill and face show in reflections. Two lamps
    # were only ever safe because of their links, so they get real controls instead: `smoke`, 80, linked to Smoke's parts
    # alone, gets a honeycomb grid (30 deg) and aims at Smoke, so it does not wash Fog and its neighbours; `strip`, 70,
    # linked to the drivers, lit nothing else, and unlinked at 70 it would light every front at ten times the face lamp:
    # down to the face lamp's level, 6
    L = s['lights']
    # (the coordinator, 23:24: the key was a sun from straight behind the row reaching it through the paper, which cast no
    # shadow. The sweep now casts its shadow (honest_lights), so that sun lights nothing in the set; in its place a small
    # disc softbox behind the row, inside the set and above the frame, on the sun's line and at its irradiance, so the
    # coloured shadows keep their hard edges)
    sun = s.pop('sun', None)
    if sun and sun.get('irradiance'):
        import math
        az, el = math.radians(sun.get('azimuth_deg', 180)), math.radians(sun.get('elevation_deg', 30))
        cx, cy, cz = 0.0, 0.5, 0.6
        dist = 7.0
        hx, hy = math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el)
        L['key-disc'] = {'type': 'area', 'size_m': [0.35, 0.35], 'position': [round(cx + dist * hx, 3), round(cy + dist * hy, 3), round(cz + dist * math.sin(el), 3)],
                         'target': [cx, cy, cz], 'irradiance': sun['irradiance'], 'color': sun.get('color', 5200)}
    honest_lights(s)
    sm = s['products'][0]['instances'][-1]['position']
    if 'smoke' in L:
        L['smoke'].update(target=[sm[0], sm[1], 0.5], spread_deg=30)
    if 'strip' in L:
        L['strip']['irradiance'] = 6.0
    # (its proxy, 0.25 scale: the cyc, top and over lamps through glass, and the side lamps unlinked, lift the fronts by
    # about a third and fill the long shadows; Dust's and Acid's tops clipped on 12 and 11 %. 0.3 stop down: 4 and 6 %,
    # as before the rule, the fronts' saturation within 0.05 of it, the sweep 238)
    s['render']['exposure'] = round(s['render'].get('exposure', 0.0) - 0.3, 2)
    return s


SHOTS['deck-cover'] = deck_cover
# the deck's Home slide: the golden-hour room (754e16a9's scene, covers off) with the pair turned into the final design
def _room_gate3(s):
    """The room's fixes (the coordinator's blind critics on the portrait, 2026-11-03, 2 HOLD 1 SHOW): the low sun raked
    both bottom chambers at floor level, so the bottoms glowed green, the brightest part of each speaker, which reads as
    a base light by day (the owner: no light). The windows get a sill at 0.9 m (their tops stay at 2.75) and the sun
    goes down to 8 deg, so it reaches the left unit only above about 0.77 m and the right above about 0.41 m: the bottom
    40 cm in shade, the light through the upper cabinets and the horns onto the wall behind. AgX in place of PBR
    Neutral so the greens roll off, and 2/3 of a stop down; the left unit turned so its right side shows its green; the
    right a little more, off the woofer's pinwheel shadow. The two leads (one to each unit's own outlet, behind it)
    are kept."""
    for w in s['set'].get('windows', []):
        top = w['sill'] + w['size'][1]
        w['sill'] = 0.9
        w['size'] = [w['size'][0], round(top - 0.9, 3)]
    # (its proof at -1.37: the fronts still dark boxes, the left 11 and the right 22 against the row's Poison front at
    # 48.6. The sun at azimuth -68 reaches the left unit through the window nearest the back wall (along 2.75) and the
    # right through the next (along 1.15), so that one window alone gets a lower sill, 0.55: the sun reaches the left
    # unit from about 0.42 m up, its middle, while the right keeps its 0.41 m and both bottoms stay in shade)
    for w in s['set'].get('windows', []):
        if abs(w.get('along', 0) - 2.75) < 1e-6:
            top = w['sill'] + w['size'][1]
            w['sill'] = 0.55
            w['size'] = [w['size'][0], round(top - 0.55, 3)]
    # (the fix1 portrait's gate, 2026-11-03 21:28, HOLD 3/3: the lower ~40 % of both cabinets near-black (65 % of cabinet
    # pixels under 20), the left unit's face toward the sideboard a beige mirror of the sunlit wall, the left horn's green
    # on the wall running up to the right horn. Both sills come down, so the low sun reaches each cabinet from about a
    # quarter of its height up, the bottom chambers still in shade: the window nearest the back wall to 0.35 (the left
    # unit lit from about 0.22 m), the next to 0.75 (the right from about 0.26 m); the sun 3 deg round, so the green
    # cast moves off the right horn; the left unit turned to -6 deg, its face toward the sideboard mirroring the room)
    for w in s['set'].get('windows', []):
        for along, sill in ((2.75, 0.25), (1.15, 0.6)):
            if abs(w.get('along', 0) - along) < 1e-6:
                top = w['sill'] + w['size'][1]
                w['sill'] = sill
                w['size'] = [w['size'][0], round(top - sill, 3)]
    s['sun']['azimuth_deg'] = s['sun'].get('azimuth_deg', -68.0) - 3.0
    s['sun']['elevation_deg'] = 8.0
    s['render']['view'] = 'AgX'
    # (its proxy: AgX sits about half a stop under PBR Neutral, so -2/3 left the cabinets near black: -2/3 + 1/2)
    s['render']['exposure'] = round(s['render'].get('exposure', 0.0) - 0.17, 2)
    for blk in s['products']:
        for i in blk['instances']:
            x = i['position'][0]
            if x < 0:
                i["rotate_z"] = -14.0
            else:
                i['rotate_z'] = -8.0
    return s


SHOTS['deck-home'] = lambda: dict(_room_gate3(strata_lit(room_off(), glow=20.0)), title='Tropos at home, golden hour, Poison (the final design)')
SHOTS['deck-home-portrait'] = lambda: dict(_room_gate3(strata_lit(room_off_portrait(), glow=20.0)),
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
    _siteG_round1(s, frame, tint)
    if frame == 'hero-light':
        _siteH_round1(s)
    if frame == 'back':
        _siteB_round1(s)
        _siteB_round2(s)
        _siteB_round3(s)
    honest_lights(s)
    if frame in ('front-off-tall', 'front-off-wide', 'side'):
        _siteG_round2(s)
    if frame in ('front-off-tall', 'front-off-wide', 'side') and 'back' in s['lights']:
        # (the honest rig's proxies, tall Ice and Ember: unlinked, the `back` lamp, behind the speaker and aimed through
        # it at the floor, lit the floor beside it (176 to 229), and the lower right face, mirroring it, fell from
        # saturation 0.56 to 0.46 (Ice) and 0.49 to 0.35 (Ember). A reflect-only patch on that floor is not allowed (the
        # camera sees the floor: the coordinator, 20:17). Tests: the kick at half, floor 224, face 0.47; the kick on a
        # 25 deg grid, 244 and 0.43; `back` at half, 215 and 0.49; `back` off, 197 and 0.51 (Ember 195 and 0.42), the
        # front unchanged. `back` goes off)
        s['lights']['back']['irradiance'] = 0.0
        s['lights']['back'].pop('power_w', None)
    if frame == 'front-off-tall':
        # (the veil, tallr3's gate, 2026-11-09: the lower right face, near-grazing to the lens, mirrored lit floor behind
        # and right of the speaker: white over the tint 74-78 levels, saturation 0.16 (Poison) to 0.33 (Haze). Geometry
        # puts the mirror on floor x 0.32-1.08, y -0.12 to 1.9; the floor flag takes a quarter of it, a real black floor
        # card out of frame (the corrected cast, _frame_rays) a sixth more, and the speaker turns 6 deg toward the lens
        # (the face less edge-on); the back-edge card turns with it. Haze crops, lower face rows 800-1060, sat / white:
        # 0.33 / 78; the card + 3 deg 0.50 / 26, + 6 deg 0.61 / 16, + 10 deg 0.64 / 17. Turn only, Ember 6 deg 0.51 / 29,
        # Poison 0.32 / 29. Left: the lowest part of the face mirrors floor beside the speaker that the camera sees)
        for blk in s['products']:
            for i in blk['instances']:
                i['rotate_z'] = i.get('rotate_z', 0) - 6.0
        s.setdefault('set', {}).setdefault('flags', []).append(
            {'center_m': [1.575, 1.775, 0.006], 'size_m': [1.65, 2.45], 'normal': [0.0, 0.0, 1.0], 'color': '#060606',
             'camera': True, 'glossy': True, 'name': 'floor card behind-right'})
    if frame in ('front-off-tall', 'front-off-wide', 'hero-light', 'side'):
        back_edge_card(s, sides=('back', 'left') if frame == 'side' else ('back',),
                       trim_right=0.008 if frame == 'front-off-tall' else 0.0)
    if frame == 'front-off-tall' and 'horn' in s['lights']:
        # (the honest tall's gate, 2026-11-09 19:32/19:41: the horn lamp, slid out of frame and grown 1.8x, lit the floor
        # in front, which the front face mirrored as a milky veil, and mirrored in the front and the horn mouth itself.
        # The same 2.5 x 1.6 m softbox, not grown, at the same irradiance on the horn, raised above the camera clear of
        # the front face's mirror zone (which reaches about 0.8 m up at the camera's distance), with a 25 deg grid, and a
        # black cutter under its lower edge so it stops lighting the foreground floor: all out of frame)
        L = s['lights']['horn']
        # Dust proxy against the passed tall (half size, same pixels): grid 25 and a 1.4 x 0.7 cutter, wall 0.81 / floor
        # 0.94 / front saturation 0.65; grid 15, a 2.0 x 1.0 cutter and the frame -0.15 stop, wall 0.76 (0.77) / floor
        # 0.86 (0.87) / horn L* 50 (54) / front saturation 0.77 (0.70) / centre block 0.80, blue 0.026 linear / bottom
        # batt 0.85. (The horn lamp off moves the wall and floor 0.01: the rest of the lift is the frame's, hence -0.15)
        # Round 2 (the gate held 15931e00 for the backdrop: a hard arched pool edge across the cyc). That edge was the
        # 15 deg grid: Blender's area-light spread is a hard cone from every point of the box, with no penumbra the box's
        # size, an edge no real grid throws (Fog: the cutter off left it, the grid off took it away). So no grid; a
        # larger cutter (2.5 x 1.25) holds the foreground floor; the frame -0.1; the kick 2.5 (1.1) for the right side,
        # which the in-frame lamp used to light; a white fill card camera-right, out of frame. Half size, 64 samples,
        # against the passed talls: the backdrop at x 860 238-239 (240-244) and smooth, 0.0 % at 248+, the upper wall
        # 239, the floor pool's p95 240-242; Dust front saturation 0.82 at V 0.54, horn L* 54 (54); Fog's right face
        # V 0.65 (0.77; 0.60 before the kick)
        L.update(position=[0.9, -2.3, 2.2], size_m=[2.5, 1.6])
        L.pop('orbit', None); L.pop('spread_deg', None)
        s.setdefault('set', {}).setdefault('flags', []).append(
            {'center_m': [0.76, -1.91, 1.47], 'size_m': [2.5, 1.25], 'normal': [0.0, 0.0, 1.0], 'color': '#050505',
             'camera': True, 'glossy': True, 'name': 'horn cutter'})
        s['set'].setdefault('bounces', []).append(
            {'center_m': [1.4, 0.0, 0.6], 'size_m': [1.4, 1.8], 'normal': [-1.0, 0.0, 0.0], 'color': '#F2F2F2',
             'camera': True, 'glossy': True, 'name': 'fill card right'})
        if 'kick' in s['lights']:
            s['lights']['kick']['irradiance'] = 2.5
        s['render']['exposure'] = round((s['render'].get('exposure') or 0.0) - 0.1, 3)
    if frame == 'front-off-wide' and 'horn' in s['lights']:
        # (the honest wide's gate, 2026-11-09: a crisp near-white tapered stroke across 27 % of the horn's lip, read as a
        # logo. Not the key: the key 8 to 24 deg higher and 8 deg toward the lens changed nothing. It is the `horn` lamp,
        # the whole of it drawn into a line by the lip's curve (ray-cast from the stroke: its rays meet the lamp across
        # u 0.01-0.75, v 0-1, so no edge flag can take it), and in this view that lamp lights the horn's shell not at
        # all: shell 223/114/26 with it, 222/114/25 without; the stroke 655 px -> 54. A lamp dimmed as a whole: off)
        s['lights']['horn']['irradiance'] = 0.0
        s['lights']['horn'].pop('power_w', None)
    if frame in ('front-off-tall', 'side'):
        # (the tall gate's glint, 2026-11-09: a faint horizontal line on the right side face at mid-height, near the back
        # edge, on Dust, Fog and Ember. The probe: the face mirrors the floor flag (finals31's, at 1.6, 1.8 on the floor,
        # reaching y 3.0) below that line and the upright black card behind it (1.8, 2.7) above; the upright card runs
        # on a slant and at its left end stands 0.1 m past the floor flag's far edge, so a strip of lit sweep showed
        # between them. Not the cutter, the fill card or the flag's sheen: each off or velvet left the line. The floor
        # flag reaches on under the upright card, y 0.6 to 3.5; still out of frame)
        for f in (s.get('set') or {}).get('flags', []):
            if f.get('center_m') == [1.6, 1.8, 0.005]:
                f['center_m'] = [1.6, 2.05, 0.005]; f['size_m'] = [1.6, 2.9]
        # (the line again, tallr3, 2026-11-09: it stayed, 65 over 16 on Ember at row 701. Lights off in turn only dimmed
        # it; the floor flag off brightened everything below it, the upright card off everything above, so it is their
        # junction. The sweep's cove rises from y 2.7 (depth 5.5 - radius 2.8); the upright card ran on a slant from
        # (0.41, 3.25) to (3.2, 2.15), half of it standing on the rising cove, and the floor flag at z 0.005 goes under
        # the cove past y 2.87: a wedge of lit cove between them. The card 0.6 m forward stands wholly on the flat
        # floor (far end y 2.66), in front of the cove; the line 59 -> 16 on Ember, 56 -> 14 on Haze, field 16 / 14;
        # still 0 % in frame)
        for f in (s.get('set') or {}).get('flags', []):
            if f.get('center_m') == [1.8, 2.7, 1.3]:
                f['center_m'] = [1.8, 2.1, 1.3]
    if frame in ('front-off-tall', 'side'):
        # (the coordinator's 21:34 ruling, withdrawing specular-only sources: a panel at diffuse 0 shows in the glass and
        # lights nothing, which no real lamp does. scrim 0.25, sheen 0.6 and topline 0.9 go; Dust half size: the veil box
        # 78 -> 70 % under 0.5, front saturation 0.83, horn L* 52, the backdrop smooth, nothing at 248+)
        for k in [k for k, L in s['lights'].items() if L.get('type') == 'panel' and float(L.get('diffuse', 1.0) or 0.0) == 0.0]:
            s['lights'].pop(k)
    if frame in ('front-off-tall', 'front-off-wide', 'hero-light', 'side', 'back'):
        realize_hidden(s)
    # a panel at strength 0 still stands in the set: unseen by the camera and casting no shadow, but in the glossy floor's
    # reflections a black rectangle (the wide's critics, 2026-11-09: a straight, nearly horizontal seam on the floor at
    # x 1650-1800, y 780-790 of 1800 x 1200, darker beyond it; the ray-cast puts it on `sidesheen`'s foot, y 2.4 m behind
    # the speaker). An unlit panel is no lamp, whatever its ramp (a fraction of 0): it goes
    for k in [k for k, L in s['lights'].items() if L.get('type') == 'panel' and float(L.get('strength', 1.0)) <= 0.0]:
        s['lights'].pop(k)
    if frame == 'side' and 'kick' in s['lights']:
        # (the tall gates' fold-in (1), 2026-11-09: the lower third of the right side mirrored the floor between the speaker
        # and the black mirror card, which the card rule keeps 2.5 m out, too far to reach the lower face's reflections
        # (they fall 12 to 21 deg and meet the floor first). The probe: 54 % of the right face mirrors the sweep at az 51
        # to 60. In this view the kick lights that floor and next to nothing else: Poison proxy, the face's lower third
        # 19/57/16 sat 0.72 with it, 5/47/4 sat 0.91 without; the upper face 116 to 115 green, the horn 139 to 133; the
        # floor right of the speaker 243 to 201, the left 244 to 231. A lamp dimmed as a whole: the kick goes off here)
        s['lights']['kick']['irradiance'] = 0.0
        s['lights']['kick'].pop('power_w', None)
    cards_out_of_frame(s)
    return s


def back_edge_card(s, gap=0.004, h=0.045, sides=('back',), trim_right=0.0):
    """A black card standing on the floor just behind the speaker's bottom panel (the bottom-edge gate, 2026-11-09).
    The panel is clear and runs the cabinet's full depth, polished at both ends: from the front the camera looks into
    its front edge and along it, by total internal reflection, out of its back edge to the bright studio behind, through
    420 mm of dye: Dust's red bar at the foot, Fog's white streaks, Ice's blue band. Tests on the Dust hero-light base
    crop: each lamp off in turn left the bar (3630 red px; the key off 3430), a card on the floor under the footprint
    changed nothing, the background lamps off dimmed it, and a low black card behind the speaker took it to 0. A real
    set object: seen by the camera and in reflections, casting shadows, no link; the cabinet's width, 45 mm tall, 4 mm
    behind the back face, where the speaker hides it from the front."""
    # `sides`: ('back',) for the front views; the side view (the speaker turned -50) looks into the front edge on a
    # slant, along the panel toward its left end, and out through the left wall: ('back', 'left') there, the left card
    # hidden behind the cabinet from that camera
    import math
    # each card in the speaker's own frame: its centre (x, y), its width, its outward normal (x, y)
    # (the back card's +x end 9 mm short, ending 9 mm inside the right side panel's outer face: the tall gate, 2026-11-09,
    # saw its end as a black nub 2-6 px past the back-right corner at the floor)
    # `trim_right`: that much more off the back card's +x end (the tall turned 6 deg: 3 px of it past the back-right
    # corner by the equipment audit, 2026-11-09)
    defs = {'back': ((-0.0045 - trim_right / 2, 0.2063 + gap), 0.551 - trim_right, (0.0, 1.0)), 'left': ((-0.28 - gap, -0.004), 0.42, (-1.0, 0.0))}
    for blk in s.get('products', []):
        for i in blk['instances']:
            x0, y0, z0 = i.get('position', [0, 0, 0]); r = math.radians(i.get('rotate_z', 0))
            c, sn = math.cos(r), math.sin(r)
            for side in sides:
                (px, py), w, (nx, ny) = defs[side]
                cx, cy = x0 + c * px - sn * py, y0 + sn * px + c * py
                wx, wy = c * nx - sn * ny, sn * nx + c * ny          # the outward normal, turned; the card faces in
                s.setdefault('set', {}).setdefault('flags', []).append(
                    {'center_m': [round(cx, 4), round(cy, 4), round(z0 + h / 2, 4)], 'size_m': [w, h],
                     'normal': [round(-wx, 4), round(-wy, 4), 0.0], 'color': '#050505',
                     'camera': True, 'glossy': True, 'name': f'{side}-edge card'})
        break
    return s


_SET_NAMES = ('sweep', 'floor', 'wall', 'ceiling', 'cyc', 'room')


def _set_only(recv):
    return bool(recv) and all(any(r.startswith(n) for n in _SET_NAMES) for r in recv)


def honest_lights(s, log=None):
    """The owner's rule on light (the coordinator's rulings, 2026-11-03 19:32: "what's technically possible trumps what
    looks cool"): no lamp lights something without also lighting, and showing in, everything else it reaches.
    1. A lamp that lights the scene shows at full in reflections: a `specular` under 1 goes to 1.0, and a lamp held
       off transmission (`transmission: false`) lights through glass again.
    2. A lamp linked to some of the product's parts (receivers) lights everything it reaches: the link goes.
    These stand: background lamps linked to the set alone (the sweep, the floor, a wall), at any specular (a background
    light flagged off the subject, its head out of view); specular-only sources dimmed as a whole (an area lamp with
    diffuse 0, such as `edge`; a panel with diffuse 0, a reflection card); flags. Returns the changes as text."""
    out = []
    for name, L in s.get('lights', {}).items():
        if L.get('off') or L.get('type') == 'flag':
            continue
        recv = L.get('receivers')
        if name.startswith('bg') and not recv and L.get('specular', 1.0) == 0.0:
            # a background lamp lighting everything but showing in nothing: flagged off the subject instead, its light
            # on the sweep alone (which stands), rather than at full in the side faces, which already mirror too much
            out.append(f'{name}: unlinked at specular 0, now on the sweep alone')
            L['receivers'] = ['sweep']
            continue
        spec_only = L.get('diffuse', 1.0) == 0.0
        if _set_only(recv):
            continue
        if L.get('type') == 'panel':
            if recv:     # a reflection card shown in some parts only: a part-link all the same
                out.append(f'{name}: panel receivers {recv} removed')
                del L['receivers']
            if not spec_only and 'specular' in L and L['specular'] != 1.0:   # a lit panel hidden from reflections
                out.append(f"{name}: panel specular {L['specular']} to 1.0")
                L['specular'] = 1.0
            continue
        if spec_only:
            # a specular-only source may be dimmed as a whole, never linked (the coordinator, 23:18)
            if recv:
                out.append(f'{name}: specular-only, receivers {recv[:3]}... removed')
                del L['receivers']
            continue
        if recv:
            out.append(f'{name}: receivers {recv[:3]}{"..." if len(recv) > 3 else ""} removed')
            del L['receivers']
        if 'specular' in L and L['specular'] != 1.0:
            out.append(f"{name}: specular {L['specular']} to 1.0")
            L['specular'] = 1.0
        if L.get('transmission') is False:
            out.append(f'{name}: transmission false removed')
            del L['transmission']
    # every part of a set casts shadows, and light reaches the product only through a real opening (the coordinator,
    # 23:24): no paper that lets a sun through, no cutter only some rays meet, no flag scoped to some lamps, no lamp whose
    # shadow on the set is lightened
    st = s.get('set', {})
    if st.get('cast_shadow') is False:
        out.append('set: cast_shadow false removed (the paper casts its shadow)')
        del st['cast_shadow']
    for fl in st.get('flags', []):
        if fl.get('see_through'):
            out.append(f"flag {fl.get('center_m')}: see_through removed"); del fl['see_through']
    for name, L in s.get('lights', {}).items():
        if L.get('type') == 'flag' and L.get('lights'):
            out.append(f'{name}: flag scoped to {L["lights"]}: scope removed'); del L['lights']
        if L.get('see_through'):
            out.append(f'{name}: see_through removed'); del L['see_through']
        if 'shadow_on_set' in L and L['shadow_on_set'] < 1.0:
            out.append(f'{name}: shadow_on_set {L["shadow_on_set"]} removed'); del L['shadow_on_set']
    if log is not None:
        log.extend(out)
    return s


def _frame_rays(s, nx=96, ny=96):
    """Unit rays through a grid over the camera's frame (lens shift included, padded 3 % past each edge), or over its
    render crop where it has one."""
    import numpy as np
    # as render.py builds the camera (2026-11-09, the veil's floor cards: the cast had fitted the sensor to the larger
    # side and aimed the lens at the target, so a portrait frame read 20 % too narrow and a level camera's frame sat
    # where a tilted one's would; cards cast at 0 % showed at the tall's right edge). The sensor is fitted HORIZONTAL,
    # `sensor_mm` across; a `level` camera looks level and shifts the lens by render.py's formula; with that fit
    # Blender's shift is in sensor widths (checked against bpy's world_to_camera_view on the tall: within 1 px)
    import math
    cam = s['camera']; c = np.array(cam['position'], float); t = np.array(cam.get('target', [0, 0, 0]), float)
    W, H = s['size']; lens = cam['lens_mm']; sw = cam.get('sensor_mm', 36.0)
    hx, hy = sw / 2, sw / 2 * H / W
    span = sw            # a HORIZONTAL fit measures the shift in sensor widths (Blender's own projection, 2026-11-09)
    sx, sy = cam.get('shift_x', 0.0), cam.get('shift_y', 0.0)
    d0 = t - c
    if cam.get('level', True):
        flat = np.array([d0[0], d0[1], 0.0]); tilt = math.atan2(d0[2], np.linalg.norm(flat))
        f = flat / np.linalg.norm(flat)
        sy += math.tan(tilt) * lens / sw * (1.0 if W >= H else W / H)
    else:
        f = d0 / np.linalg.norm(d0)
    r = np.cross(f, [0.0, 0.0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    if cam.get('roll_deg'):
        a = math.radians(cam['roll_deg']); r, u = r * math.cos(a) + u * math.sin(a), u * math.cos(a) - r * math.sin(a)
    # a render crop (fractions of the frame from the top left; the arc's) is the frame that is shown (2026-11-09)
    x0, y0, x1, y1 = ((s.get('render') or {}).get('crop') or [0.0, 0.0, 1.0, 1.0])
    pad = 0.03
    xs = np.linspace(2 * x0 - 1 - pad, 2 * x1 - 1 + pad, nx); ys = np.linspace(1 - 2 * y1 - pad, 1 - 2 * y0 + pad, ny)
    X, Y = np.meshgrid(xs, ys)
    px = X * hx + sx * span; py = Y * hy + sy * span                 # mm on the sensor
    d = f[None, None, :] * lens + px[..., None] * r[None, None, :] + py[..., None] * u[None, None, :]
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    return c, d.reshape(-1, 3)


def card_coverage(s, fl):
    """The share of the frame's rays that hit the card's rectangle in front of the camera (the coordinator's cardcast,
    2026-11-03: a test of corners alone missed a large card whose middle crossed the frame)."""
    import numpy as np, math
    c, d = _frame_rays(s)
    cx, cy, cz = fl['center_m']; w, h = fl['size_m']
    n = np.array(fl['normal'], float); n /= np.linalg.norm(n)
    if abs(n[2]) > 0.9:
        a = np.array([1.0, 0.0, 0.0]); b = np.array([0.0, 1.0, 0.0])
    else:
        L = math.hypot(n[0], n[1]) or 1.0
        a = np.array([-n[1] / L, n[0] / L, 0.0]); b = np.cross(n, a); b /= np.linalg.norm(b)
    o = np.array([cx, cy, cz])
    den = d @ n
    with np.errstate(divide='ignore', invalid='ignore'):
        tt = ((o - c) @ n) / den
    p = c[None, :] + tt[:, None] * d
    q = p - o
    hit = (tt > 0) & np.isfinite(tt) & (np.abs(q @ a) <= w / 2) & (np.abs(q @ b) <= h / 2)
    return float(hit.mean())


def _in_frame(s, fl):
    return card_coverage(s, fl) > 0.0


def _card_points(fl):
    import math
    cx, cy, cz = fl['center_m']; w, h = fl['size_m']; n = fl['normal']
    if abs(n[2]) > 0.9:                                    # on the floor (or a ceiling): its plane is horizontal
        ax, ay, az, bx, by, bz = 1.0, 0.0, 0.0, 0.0, 1.0, 0.0
    else:
        L = math.hypot(n[0], n[1]) or 1.0
        ax, ay, az = -n[1] / L, n[0] / L, 0.0; bx, by, bz = 0.0, 0.0, 1.0
    g = (-1.0, -0.5, 0.0, 0.5, 1.0)
    return [(cx + a * w / 2 * ax + b * h / 2 * bx, cy + a * w / 2 * ay + b * h / 2 * by, cz + a * w / 2 * az + b * h / 2 * bz)
            for a in g for b in g]


def cards_out_of_frame(s, log=None):
    """The coordinator's rule (2026-11-03 20:17): a reflect-only card is an out-of-frame flag or nothing. Each one inside
    the camera's frustum slides away from the speaker along the line through it, growing in proportion so it holds the
    same angle from the speaker, until no part of it is in frame, staying inside the studio (the sweep's depth and
    width, or the room). A card on the floor cannot leave a frame that sees the floor, and goes; so does one that
    cannot get out of frame inside the studio."""
    st = s.get('set', {}); out = []
    i0 = s['products'][0]['instances'][0]['position'] if s.get('products') else [0, 0, 0]
    depth = st.get('depth', 1e9) - 0.2; half_w = st.get('width', 1e9) / 2 - 0.2
    # (the set's reflect-only `bounces`, white cards seen only in reflections, fall under the same rule: removed if in
    # frame; they are not slid out, a bounce card's place is set by what it lights)
    bk = []
    for b in st.get('bounces', []):
        if b.get('reflect_only') and _in_frame(s, b):
            out.append(f"reflect-only bounce at {b['center_m']} in frame: removed")
        else:
            bk.append(b)
    if 'bounces' in st:
        st['bounces'] = bk
    keep = []
    for fl in st.get('flags', []):
        if not fl.get('reflect_only') or not _in_frame(s, fl):
            keep.append(fl); continue
        if abs(fl['normal'][2]) > 0.9:
            out.append(f"floor card at {fl['center_m']} in frame: removed"); continue
        cx, cy, cz = fl['center_m']; rx, ry = cx - i0[0], cy - i0[1]
        done = None
        for k10 in range(11, 81):
            k = k10 / 10
            nc = [round(i0[0] + k * rx, 3), round(i0[1] + k * ry, 3), cz]
            if nc[1] > depth or abs(nc[0]) > half_w:
                break
            cand = {**fl, 'center_m': nc, 'size_m': [round(fl['size_m'][0] * k, 3), round(fl['size_m'][1] * k, 3)]}
            if cand['center_m'][2] - cand['size_m'][1] / 2 < -0.5:   # grown far below the floor: lift it to stand on it
                cand['center_m'][2] = round(cand['size_m'][1] / 2 - 0.5, 3)
            if not _in_frame(s, cand):
                done = cand; break
        if done:
            out.append(f"card at {fl['center_m']} moved to {done['center_m']} at x{round(done['size_m'][0] / fl['size_m'][0], 1)}")
            keep.append(done)
        else:
            out.append(f"card at {fl['center_m']} cannot leave the frame inside the studio: removed")
    st['flags'] = keep
    if log is not None:
        log.extend(out)
    return s


def _slide_out(s, fl, i0, depth, half_w):
    """`fl` slid away from the speaker along the line through it, growing to hold its angle, until no part of it is in
    frame inside the studio (cards_out_of_frame's walk); None if it cannot leave."""
    cx, cy, cz = fl['center_m']; rx, ry = cx - i0[0], cy - i0[1]
    for k10 in range(11, 81):
        k = k10 / 10
        nc = [round(i0[0] + k * rx, 3), round(i0[1] + k * ry, 3), cz]
        if nc[1] > depth or abs(nc[0]) > half_w:
            return None
        cand = {**fl, 'center_m': nc, 'size_m': [round(fl['size_m'][0] * k, 3), round(fl['size_m'][1] * k, 3)]}
        if cand['center_m'][2] - cand['size_m'][1] / 2 < -0.5:
            cand['center_m'][2] = round(cand['size_m'][1] / 2 - 0.5, 3)
        if not _in_frame(s, cand):
            return cand
    return None


def realize_hidden(s, log=None):
    """The coordinator's rule (2026-11-09 18:37): no object in frame hidden from the camera. Every flag and bounce that
    is not reflect-only becomes a real object, seen by the camera and in reflections and casting shadows; one in frame
    slides out of it along the line from the speaker, growing to hold its angle (cards_out_of_frame's walk), or goes if
    it cannot leave the studio or lies on the floor. (A practical's bulb inside its own fitting is the one exception;
    the site rigs have none.)"""
    import math
    st = s.get('set', {}); out = []
    i0 = s['products'][0]['instances'][0]['position'] if s.get('products') else [0, 0, 0]
    depth = st.get('depth', 1e9) - 0.2; half_w = st.get('width', 1e9) / 2 - 0.2
    # a lamp-rig flag (lights.flag: a matte card the camera never sees) becomes a set flag, the camera's to see like any
    # other card, and goes through the same walk below
    import hiddencast as H0
    for k, L in list((s.get('lights') or {}).items()):
        if L.get('type') != 'flag':
            continue
        r = H0._lamp_rect(L)
        if r:
            st.setdefault('flags', []).append({'center_m': [round(x, 3) for x in r['center_m']], 'size_m': list(r['size_m']),
                                               'normal': [round(x, 4) for x in r['normal']], 'color': L.get('color', '#000000'),
                                               'name': k})
            out.append(f"lamp-rig flag {k}: a set flag")
        s['lights'].pop(k)
    for key in ('flags', 'bounces'):
        keep = []
        for fl in st.get(key, []) or []:
            if fl.get('reflect_only') or fl.get('camera'):
                keep.append(fl); continue
            fl = {**fl, 'camera': True, 'glossy': True}
            if not _in_frame(s, fl):
                keep.append(fl); continue
            if abs(fl['normal'][2]) > 0.9:
                out.append(f"{key[:-1]} on the floor at {fl['center_m']}, hidden, in frame: removed"); continue
            done = _slide_out(s, fl, i0, depth, half_w)
            if done:
                out.append(f"{key[:-1]} at {fl['center_m']}, hidden, in frame: made real, moved to {done['center_m']} at "
                           f"x{round(done['size_m'][0] / fl['size_m'][0], 1)}")
                keep.append(done)
            else:
                out.append(f"{key[:-1]} at {fl['center_m']}, hidden, in frame, cannot leave: removed")
        if key in st:
            st[key] = keep
    # lamps: Cycles hides an area lamp from the camera, and a panel is hidden unless it says otherwise; one lit and in
    # frame slides out along the line from its target, its size grown to hold its angle there (an irradiance holds;
    # a lamp given in watts gains k squared; a panel's strength is a radiance and holds)
    import hiddencast as H
    for k, L in list((s.get('lights') or {}).items()):
        if L.get('type') not in ('area', 'panel') or L.get('camera'):
            continue
        if not any(float(L.get(x, 0) or 0) > 0 for x in ('irradiance', 'power_w', 'strength')):
            continue
        r = H._lamp_rect(L)
        if not r or not _in_frame(s, r):
            continue
        t = L.get('target', H.CENTRE)
        moved = None
        for k10 in range(11, 81):
            f = k10 / 10
            if 'orbit' in L:
                cand = {**L, 'orbit': {**L['orbit'], 'distance_m': round(L['orbit'].get('distance_m', 2.0) * f, 3)}}
            else:
                p = L['position']
                cand = {**L, 'position': [round(t[i] + (p[i] - t[i]) * f, 3) for i in range(3)]}
            sz = L.get('size_m', [0.5, 0.5])
            cand['size_m'] = [round(x * f, 3) for x in sz] if isinstance(sz, list) else round(sz * f, 3)
            if 'power_w' in L:
                cand['power_w'] = round(L['power_w'] * f * f, 3)
            rc = H._lamp_rect(cand)
            if rc and not _in_frame(s, rc) and rc['center_m'][1] < depth and abs(rc['center_m'][0]) < half_w:
                moved = cand; break
        if not moved and 'position' in L:
            # cannot leave along its line inside the studio (a lamp behind the speaker, its line running into the cove):
            # raised instead, at its own azimuth round its target, from its elevation up, at 1 to 2 times its distance
            p0 = L['position']; v = [p0[i] - t[i] for i in range(3)]
            d0 = math.sqrt(sum(x * x for x in v)) or 1.0
            el0 = math.degrees(math.asin(max(-1.0, min(1.0, v[2] / d0)))); az0 = math.atan2(v[0], -v[1])
            for el in range(int(el0) + 3, 88, 3):
                for f in (1.0, 1.3, 1.6, 2.0):
                    e = math.radians(el); d = d0 * f
                    cand = {**L, 'position': [round(t[0] + d * math.cos(e) * math.sin(az0), 3),
                                              round(t[1] - d * math.cos(e) * math.cos(az0), 3), round(t[2] + d * math.sin(e), 3)]}
                    sz = L.get('size_m', [0.5, 0.5])
                    cand['size_m'] = [round(x * f, 3) for x in sz] if isinstance(sz, list) else round(sz * f, 3)
                    if 'power_w' in L:
                        cand['power_w'] = round(L['power_w'] * f * f, 3)
                    rc = H._lamp_rect(cand)
                    if rc and not _in_frame(s, rc) and rc['center_m'][1] < depth:
                        moved = cand; break
                if moved:
                    out.append(f"lamp {k}: raised from {round(el0)} to {el} deg at x{f}")
                    break
        if moved:
            s['lights'][k] = moved
            out.append(f"lamp {k}, hidden, in frame: moved out at x{f}")
        else:
            s['lights'].pop(k)
            out.append(f"lamp {k}, hidden, in frame, cannot leave: removed")
    if log is not None:
        log.extend(out)
    return s


def arc_rig(s, bg=0.7, key_grow=2.5, off_deg=20.0, flats=False, bg_spread=None, log=None):
    """The front arc's gate (2026-11-09, wf_a973e665-cb8): 03 and 05's 10 deg side faces read as flat white slabs (Fresnel
    off a sweep lit well over white), and 05's horn corner mirrored the small high key as crisp streaks.
    1. Two matte-black v-flats on the floor behind the speaker, `off_deg` either side of the lens axis, where a face at
       80 deg to the camera sends its reflection; slid out along that line, grown to hold their angle, until out of frame
       (from about 3.5 m behind the speaker at 20 deg): real, seen by the camera and in reflections, casting shadows.
    2. The sweep from blown to just white: the background lamps (linked to the sweep alone) at `bg`.
    3. The key `key_grow` times larger at the same irradiance: a broad soft source for the horn's corner seam to mirror."""
    import math
    out = []
    cam = s['camera']['position']; tgt = s['camera'].get('target', [0, 0, 0.6])
    i0 = s['products'][0]['instances'][0]['position'] if s.get('products') else [0, 0, 0]
    ux, uy = tgt[0] - cam[0], tgt[1] - cam[1]; m = math.hypot(ux, uy); ux, uy = ux / m, uy / m
    st = s.setdefault('set', {}); depth = st.get('depth', 1e9) - 0.2; half_w = st.get('width', 1e9) / 2 - 0.2
    for side, a in ((('left', off_deg), ('right', -off_deg)) if flats else ()):
        c, sn = math.cos(math.radians(a)), math.sin(math.radians(a))
        dx, dy = c * ux - sn * uy, sn * ux + c * uy
        w, h = 1.2, 2.4
        fl = {'center_m': [round(i0[0] + 2.0 * dx, 3), round(i0[1] + 2.0 * dy, 3), h / 2], 'size_m': [w, h],
              'normal': [round(-dx, 4), round(-dy, 4), 0.0], 'color': '#060606', 'camera': True, 'glossy': True,
              'name': f'v-flat {side}'}
        done = fl if not _in_frame(s, fl) else _slide_out(s, fl, i0, depth, half_w)
        if done:
            done['center_m'][2] = round(done['size_m'][1] / 2, 3)          # standing on the floor
            st.setdefault('flags', []).append(done)
            out.append(f"v-flat {side} at {done['center_m']} {done['size_m']}")
        else:
            out.append(f"v-flat {side}: cannot stand out of frame inside the studio")
    for k, L in s['lights'].items():
        if _set_only(L.get('receivers')) and str(k).startswith('bg'):
            for x in ('irradiance', 'power_w'):
                if x in L:
                    L[x] = round(L[x] * bg, 3)
            if bg_spread:
                L['spread_deg'] = bg_spread
    if 'key' in s['lights']:
        sz = s['lights']['key'].get('size_m', [1.0, 1.0])
        s['lights']['key']['size_m'] = [round(v * key_grow, 3) for v in sz] if isinstance(sz, list) else round(sz * key_grow, 3)
    if log is not None:
        log.extend(out)
    return s


def _mirror_card(s, dist=1.2, size=(1.8, 1.3), z=0.5):
    """A reflect-only black card where the right side face's mirror ray goes from this camera, turned with the speaker
    (the first instance), `dist` m beyond the face: the face then shows its own tint, not the white studio."""
    import math
    cam = s['camera']['position']
    i = s['products'][0]['instances'][0]
    a = math.radians(i.get('rotate_z', 0.0))
    nx, ny = math.cos(a), math.sin(a)
    px = i['position'][0] + 0.28 * nx; py = i['position'][1] + 0.28 * ny; pz = 0.45
    dx, dy, dz = px - cam[0], py - cam[1], pz - cam[2]
    m = math.sqrt(dx * dx + dy * dy + dz * dz); dx, dy = dx / m, dy / m
    k = dx * nx + dy * ny
    rx, ry = dx - 2 * k * nx, dy - 2 * k * ny
    h = math.sqrt(rx * rx + ry * ry) or 1.0
    rx, ry = rx / h, ry / h
    s['set'].setdefault('flags', []).append({'center_m': [round(px + dist * rx, 3), round(py + dist * ry, 3), z],
                                             'size_m': list(size), 'normal': [round(-rx, 3), round(-ry, 3), 0.0],
                                             'reflect_only': True, 'color': '#050505'})


def _floor_patch(s, z_lo=0.06, z_hi=0.42, margin=0.15):
    """A reflect-only black patch on the floor where the right side face's lower mirror rays land from this camera
    (turned with the speaker): with the kick and back lamps unlinked (the owner's rule) the floor beside the speaker is
    lit, and the lower face mirrored it pale. None if those rays never reach the floor."""
    import math
    cam = s['camera']['position']
    i = s['products'][0]['instances'][0]
    a = math.radians(i.get('rotate_z', 0.0))
    nx, ny = math.cos(a), math.sin(a)
    tx, ty = -ny, nx                                         # along the face, front to back
    pts = []
    for along in (-0.2, 0.0, 0.2):
        for z in (z_lo, (z_lo + z_hi) / 2, z_hi):
            px = i['position'][0] + 0.28 * nx + along * tx; py = i['position'][1] + 0.28 * ny + along * ty
            dx, dy, dz = px - cam[0], py - cam[1], z - cam[2]
            k = dx * nx + dy * ny
            rx, ry, rz = dx - 2 * k * nx, dy - 2 * k * ny, dz
            if rz >= 0:
                continue
            u = z / -rz
            pts.append((px + u * rx, py + u * ry))
    if not pts:
        return
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    s['set'].setdefault('flags', []).append({'center_m': [round((min(xs) + max(xs)) / 2, 3), round((min(ys) + max(ys)) / 2, 3), 0.004],
                                             'size_m': [round(max(xs) - min(xs) + 2 * margin, 3), round(max(ys) - min(ys) + 2 * margin, 3)],
                                             'normal': [0.0, 0.0, 1.0], 'reflect_only': True, 'color': '#050505'})


def _siteG_round2(s):
    """The fix1 gates (the coordinator's critics, 2026-11-03 22:14 and 22:59). 1. A full-height cool white stripe on the
    right face behind the front corner (wide): `edge`, the specular-only glint lamp; with it off, the stripe is gone.
    Off. 2. A white rounded 'plate' at the floor (wide) and a pale line along the bottom edge (side): the cabinet's own
    bottom panel (hiding the part takes the band from 203 to 26 px at 240; the feet and the lower lining change
    nothing), its polished edge mirroring and piping the light round it. With the floor darker (the row's sweep) the band
    stands further above it; with the key and kick off it still stands 25 levels above the floor. The key and the kick
    raised from about 20 to 40 deg take it down to the floor's own level (0 px more than 25 above it): their lower edges
    no longer sit at the bottom edge's height. 3. For the dark tints: a black card camera-right down to floor level (the
    right face's lower third and front stripe) and one overhead in front (the top front edge), real cards, kept only
    where they fall out of frame (cards_out_of_frame)."""
    L = s['lights']
    if 'edge' in L:
        L['edge']['power_w'] = 0.0
    for k in ('key', 'kick'):
        if k in L and 'orbit' in L[k]:
            L[k]['orbit']['elevation_deg'] = 40.0
    _mirror_card(s, dist=1.2, size=(1.8, 1.0), z=0.3)
    s['set'].setdefault('flags', []).append({'center_m': [0.0, -1.0, 2.2], 'size_m': [2.0, 1.2], 'normal': [0.0, 0.42, -0.91],
                                             'reflect_only': True, 'color': '#050505'})
    return s


def _siteB_round1(s):
    """The back set's gate (the coordinator's critics, 2026-11-03, HOLD 7/7). 1. The horn from behind clipped (Ember 54-93 %
    at 250, pastel): `cab-back`, a 7 W/m2 lamp on the far side of the speaker that lit through the cabinet and the horn,
    hidden from reflections at specular 0. Crop tests on Ember's horn, one lamp off at a time: the key, fill, wash and
    plate strip change nothing; cab-back off, 53 % to 2 %, (206, 106, 104) to (163, 41, 37). Lowered to the cabinet on a
    35 deg grid it still left 11 %; off, the cabinet loses 75 to 72. It goes, and so does `glow` (finals31's, dropped from
    phase 2 for the same reason), and the horn's rim lamp comes down from 3.5 to 1.0. 2. The softbox patch on the back
    panel's upper left was partly cab-back's reflection: its saturation 0.42 to 0.69 with it gone. 3. The lower face
    toward the camera's left mirrored the floor: a reflect-only card on its mirror ray, out of frame."""
    L = s['lights']
    for k in ('glow', 'cab-back'):
        if k in L:
            L[k]['irradiance'] = 0.0
    if 'horn-rim' in L:
        L['horn-rim']['irradiance'] = 1.0
    # (the patch's crop tests on Ember: the key turned to -70 or -40, or grown to 2.4 x 2.0, left it as it was; with
    # `plate-strip` off, the small strip lamp beside the amp plate, it is gone: its reflection, not the key's. It goes;
    # the plate has its own close-up)
    if 'plate-strip' in L:
        L['plate-strip']['irradiance'] = 0.0
    _mirror_card(s)
    return s


def _siteB_round2(s):
    """The honest backs' gate (the coordinator's critics, 2026-11-04 01:15, wf_dfce1fd6-dc4: Ember, Poison, Haze and Acid
    held, the dark colours sunk from behind, back face L* 8-12). The fill is the one lamp that meets the back face
    near its normal (17 deg off; the key 89): x3, 1.3 to 3.9. The key and the sky, which light the sweep but hardly the
    back, come down to hold it: key x0.5 (2.6 to 1.3), sky 0.7 to 0.3. Proxies (0.5 scale, 32 samples, part masks,
    c2): back L* Ember 11.5 to 18.6, Haze 9.0 to 15.4; wall 84.4 to 84.8, floor 74 to 79; no clipping; EARF letters
    on Ember 15.0 on 6.2 to 22.7 on 10.3. Rejected: a brighter or bigger key, a soft side lamp (back +1, sweep up), a
    lamp over the lid (horn clips 4-5 %, floor 95), a soft lamp on the back's axis (mirrored as glare), real black
    flags beside the cabinet (a black slab in the set; the side goes black, not coloured). The lid and the side
    camera-left stay as they are: grazing mirrors of the in-frame floor (the coordinator, 01:48)."""
    L = s['lights']
    L['fill']['irradiance'] = 3.9
    L['key']['irradiance'] = 1.3
    s['sky']['strength'] = 0.3
    return s


def _siteB_round3(s, glow=4.0):
    """The honest backs' gate (2026-11-09, wf_73733377-178, held 1/3): (1) a crisp light edge on the backdrop, the wash's
    narrow 3.6 x 0.72 box close to the wall: twice the size at the same irradiance, a soft edge. (2) The horn's back went
    flat once horn-rim left the frame (sample 132 -> 100): no camera-side lamp (it would show in the polished back and
    top) and no more horn-rim; the photographer's way, bright-field: a lamp linked to the sweep alone, out of frame
    camera-right, on the wall behind the horn, which the horn then shows through as glass does. (3) The amplifier
    plate's green LED off in a frame with nothing on. Dust, half size, 64 samples: the horn sample 100 -> 111 at 2.0,
    122 at 4.0 (the target 120-130; rigB as rendered 133), 131 at 6.0 (the wall 217-225); its hue 25 against the back
    face's 25; the upper wall a smooth column, no 4 px step over 1."""
    L = s['lights']
    if 'wash' in L:
        L['wash']['size_m'] = [round(x * 2, 3) for x in L['wash']['size_m']]
    L['glow-wall'] = {'type': 'area', 'size_m': [1.6, 1.0], 'position': [1.8, 0.6, 2.2], 'target': [0.0, 1.45, 1.2],
                      'irradiance': glow, 'color': '#FFF3E1', 'receivers': ['sweep']}
    s.setdefault('materials', {})['led-on'] = {'strength': 0.0}
    return s


def _siteH_round1(s):
    """hero-light's fixes (the coordinator's blind critics, 2026-11-03: Dust, Acid, Poison and Ice held). Studio31 is
    an all-white surround with no flags. 1. Every right side face mirrored the white floor and cove behind-right (Poison
    grey-green, saturation 0.24-0.31): a reflect-only black card on its mirror ray, turned with the speaker, so the arc's
    turned frames get theirs. 2. The bottom panel's front edge glowed as a saturated bar with a tinted fringe in front:
    `back-top`, a lamp behind and above aimed at the floor in front of the speaker (the tall rig's `through` under
    another name), its light crossing the tinted cabinet, pooling on the floor and running along the bottom panel to its
    polished edge, an underglow by day. Off. No links: the coordinator's rule."""
    L = s['lights']
    if 'back-top' in L:
        L['back-top']['irradiance'] = 0.0
    _mirror_card(s)
    return s


def _siteG_round1(s, frame, tint):
    """The roll-out's gate on front-off-tall (the coordinator's blind critics, 2026-11-03): a hard white reflection over
    the lower half of the right side face in every tint, the owner's "spray painted white". It is `sidesheen`, a
    specular-only panel behind and right of the speaker put there so the side would read; tall, wide and side share it
    (back and hero-light do not). It goes off, and a black card that only reflections see takes its place, where the
    right face's mirror ray goes from this camera, so the face shows its own tint. The top light comes down a little so the
    top batt keeps its tint, the key turns a little so no caustic starts at a foot, and Fog loses the -0.6 its old rig
    carried, to match the other six."""
    import math
    if frame not in ('front-off-tall', 'front-off-wide', 'side'):
        return
    L = s['lights']
    if 'sidesheen' in L:
        L['sidesheen']['strength'] = 0.0
    # (the proxies: with sidesheen off the lower right face still read pale, 226 to 220. The rest was `through`, a small
    # lamp behind the speaker aimed through it at the floor, whose image sat in that face: off, 220 to 156 and the
    # face's saturation 0.47 to 0.58; the floor's coloured light is the key's and stays. Only the tall rig has it)
    if 'through' in L:
        L['through']['irradiance'] = 0.0
    if 'horn' in L and L['horn'].get('irradiance'):
        L['horn']['irradiance'] = round(L['horn']['irradiance'] * 0.65, 3)
    if frame == 'front-off-wide' and 'topline' in L:
        L['topline']['strength'] = round(L['topline']['strength'] * 0.65, 3)
    if 'key' in L and 'orbit' in L['key']:
        L['key']['orbit']['azimuth_deg'] = L['key']['orbit']['azimuth_deg'] - 5.0
    if tint == 'fog':
        s['render']['exposure'] = 0.0
    # the card: from the camera to the middle of the right face, mirrored in the face, 1.2 m on
    cam = s['camera']['position']
    i = s['products'][0]['instances'][0]
    a = math.radians(i.get('rotate_z', 0.0))
    nx, ny = math.cos(a), math.sin(a)                       # the right face's normal, turned with the speaker
    px = i['position'][0] + 0.28 * nx; py = i['position'][1] + 0.28 * ny; pz = 0.45
    dx, dy, dz = px - cam[0], py - cam[1], pz - cam[2]
    m = math.sqrt(dx * dx + dy * dy + dz * dz); dx, dy, dz = dx / m, dy / m, dz / m
    k = dx * nx + dy * ny
    rx, ry, rz = dx - 2 * k * nx, dy - 2 * k * ny, dz
    h = math.sqrt(rx * rx + ry * ry) or 1.0
    rx, ry = rx / h, ry / h
    s['set'].setdefault('flags', []).append({'center_m': [round(px + 1.2 * rx, 3), round(py + 1.2 * ry, 3), 0.5], 'size_m': [1.8, 1.3],
                                             'normal': [round(-rx, 3), round(-ry, 3), 0.0], 'reflect_only': True, 'color': '#050505'})


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


# --- the site's home-page hero (the owner, 2026-11-10: "put the speakers in a studio and have stripes of colors as the
# background and ground behind and under each one that compliments each speakers color") ---------------------------------
HERO_BRAND = {'ember': '#B50404', 'dust': '#D35D17', 'acid': '#C5BC1E', 'poison': '#027614', 'ice': '#1169C1',
              'haze': '#500CB4'}
HERO_ORDER = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
HERO_NEUTRAL = {'v1': {'fog': '#F4F3F1', 'smoke': '#CDCCCA', 'out': '#EFEDEA'},
                'v2': {'fog': '#E2E1DF', 'smoke': '#8E8D8B', 'out': '#D9D6D2'}}


def _toward_white(hx, f):
    """The colour taken `f` of the way to white, in sRGB."""
    c = [int(hx[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(v + f * (255 - v)):02X}' for v in c)


def hero_stripes(variant='v1'):
    """The eight in a row, Ember to Smoke, each on its own seamless paper stripe in its own colour family, edge to edge
    as wide as the speakers' spacing (1 m): v1 pale (two thirds of the way to white), v2 bold (one third). The deck row's
    studio and lamps (its rig, honest), the sweep's lamps on every stripe, 1680 x 700, the top quarter kept clear."""
    s = _approved(SHOTS['deck-row']())
    f = 2 / 3 if variant == 'v1' else 1 / 3
    n = len(HERO_ORDER)
    stripes = []
    for k, t in enumerate(HERO_ORDER):
        col = _toward_white(HERO_BRAND[t], f) if t in HERO_BRAND else HERO_NEUTRAL[variant][t]
        x = (k - (n - 1) / 2) * 1.0
        stripes.append({'x': [round(x - 0.5, 4), round(x + 0.5, 4)], 'color': col, 'tint': t})
    s['set']['stripes'] = stripes
    s['set']['color'] = HERO_NEUTRAL[variant]['out']
    s['materials']['sweep'] = {k: v for k, v in s['materials'].get('sweep', {}).items() if k != 'color'}   # its roughness kept
    for L in s['lights'].values():
        if L.get('receivers') == ['sweep']:
            L['receivers'] = ['sweep*']
    # the 21:34 rule: no specular-only panel (the row's front strip, diffuse 0)
    for k in [k for k, L in s['lights'].items() if L.get('type') == 'panel' and float(L.get('diffuse', 1.0) or 0.0) == 0.0]:
        s['lights'].pop(k)
    # (its first proxy, 2026-11-10: the deck row's cove, 11 m deep on a 9 m radius, put each wall stripe far behind and
    # to the side of its speaker, and the high-key set washed the stripes out; the mask pass ran out of memory on sixteen
    # copies' refined normals). A tight cove so each wall stripe stands behind its speaker, the set's own lamps lower,
    # and the normals unrefined (a few tenths of a millimetre, nothing at this size)
    s['set'].update(depth=2.6, radius=1.0, height=6.0, front=12.0, stripes_fan=-14.0)
    for L in s['lights'].values():
        if L.get('receivers') == ['sweep*']:
            L['irradiance'] = round(float(L.get('irradiance', 1.0)) * (0.55 if float(L.get('irradiance', 1.0)) > 2 else 0.5), 3)
    s['render']['exposure'] = round((s['render'].get('exposure') or 0.0) - 0.3, 3)
    # the background lamps stood behind the new wall: in front of it now, above the frame, aimed down the wall
    for k, x in (('bg-left', -3.0), ('bg-right', 3.0)):
        if k in s['lights']:
            s['lights'][k].update(position=[x, 1.2, 3.6], target=[x, 2.6, 1.0])
    s['size'] = [1680, 700]
    s['title'] = f'Tropos, the eight on their stripes ({variant})'
    # the camera 14 m off, a touch above the cabinets' middle; the frame's top quarter above the horns
    s['camera'].update(position=[0.0, -14.0, 0.85], target=[0.0, 0.0, 0.45], lens_mm=58.0, level=True)
    realize_hidden(s)
    return s


def hero_centres(s, z=0.55):
    """Each speaker's centre (its cabinet's middle, `z` m up) in percent of the frame, as the camera projects it
    (_frame_rays' model: a HORIZONTAL sensor fit, a level camera's shift)."""
    import math, numpy as np
    cam = s['camera']; W, H = s['size']; c = np.array(cam['position'], float); t = np.array(cam['target'], float)
    lens = cam['lens_mm']; sw = cam.get('sensor_mm', 36.0); hx, hy = sw / 2, sw / 2 * H / W
    d0 = t - c; flat = np.array([d0[0], d0[1], 0.0]); f = flat / np.linalg.norm(flat)
    sy = cam.get('shift_y', 0.0) + math.tan(math.atan2(d0[2], np.linalg.norm(flat))) * lens / sw * (1.0 if W >= H else W / H)
    sx = cam.get('shift_x', 0.0)
    r = np.cross(f, [0.0, 0.0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    out = []
    for k, i in enumerate(s['products'][0]['instances']):
        # (fixed 2026-11-11: measured from the speaker's own base, its riser, seat or step, not the floor; a speaker on
        # its side (rotate_y +/-90) at its middle, half its 1.28 m height along x)
        x0, y0, z0 = (list(i['position']) + [0, 0, 0])[:3]
        ry = i.get('rotate_y', 0)
        if abs(abs(ry) - 90) < 1:
            x0 += 0.64 * (1 if ry > 0 else -1); zc = z0
        else:
            zc = z0 + z
        p = np.array([x0, y0, zc]) - c; zz = p @ f
        X = ((p @ r) / zz * lens - sx * sw) / hx; Y = ((p @ u) / zz * lens - sy * sw) / hy
        out.append({'tint': HERO_ORDER[k], 'x': round(float((X + 1) / 2 * 100), 2), 'y': round(float((1 - Y) / 2 * 100), 2),
                    'color': (s['set'].get('stripes') or [{}] * (k + 1))[k].get('color')})
    return out


def hero_room():
    """The owner on the stripes (2026-11-10 16:01): "more like a studio shot where it looks more like they are in a room
    with painted walls and floor". Base A, no plinth, no light (TROPOS_BASE=A, options []), black rods. A room, not paper:
    a flat wall 1.3 m behind the row meeting a flat floor in a crisp corner (a 3 mm radius), matte painted (the paper's
    tooth and mottle as paint's grain); eight stripes in the room's own frame, parallel, hard-edged, each the same paint on
    wall and floor to the frame's front edge, the outer two carried past both frame edges; v2's own-family colours, Fog on
    a soft warm grey. Studio lamps only: a large soft overhead, a soft key high left, a low front fill behind the camera.
    A 50 mm lens at the cabinets' middle height, 8.3 m off so the end speakers keep a little air: about 54 % of the height."""
    assert ROLLOUT['base'] == 'A', 'run with TROPOS_BASE=A'
    s = _approved(SHOTS['deck-row']())
    sp = 0.72
    n = len(HERO_ORDER)
    for blk in s['products']:
        for k, i in enumerate(blk['instances']):
            i['position'] = [round((k - (n - 1) / 2) * sp, 4)] + list(i['position'][1:])
            i['rotate_z'] = -10.0
    cols = {**{t: _toward_white(c, 1 / 3) for t, c in HERO_BRAND.items()}, 'fog': '#CFC8BE', 'smoke': '#8E8D8B'}
    stripes = []
    for k, t in enumerate(HERO_ORDER):
        x = (k - (n - 1) / 2) * sp
        x0 = -30.0 if k == 0 else x - sp / 2
        x1 = 30.0 if k == n - 1 else x + sp / 2
        stripes.append({'x': [round(x0, 4), round(x1, 4)], 'color': cols[t], 'tint': t})
    s['set'] = {'kind': 'sweep', 'color': '#CFC8BE', 'width': 60.0, 'front': 12.0, 'depth': 1.3, 'radius': 0.003,
                'height': 4.0, 'stripes': stripes,
                'contact': {'strength': 0.8, 'distance_m': 0.35, 'core_strength': 1.0, 'core_distance_m': 0.03}}
    s['materials']['sweep'] = {'roughness': 0.85, 'tooth': 0.25, 'mottle': 0.05}
    s['lights'] = {
        'top': {'type': 'area', 'size_m': [5.0, 2.5], 'position': [0.0, -0.8, 3.4], 'target': [0.0, 0.0, 0.0],
                'irradiance': 3.0, 'color': '#FFF8F0'},
        'key': {'type': 'area', 'size_m': [2.0, 2.0], 'position': [-3.4, -3.6, 2.4], 'target': [0.0, 0.0, 0.6],
                'irradiance': 1.6, 'color': '#FFF5E8'},
        'fill': {'type': 'area', 'size_m': [4.0, 1.2], 'position': [0.0, -10.0, 0.7], 'target': [0.0, 0.0, 0.6],
                 'irradiance': 1.0, 'color': '#FFF8F0'}}
    s['camera'] = {'position': [0.0, -8.3, 0.5], 'target': [0.0, 0.0, 0.72], 'lens_mm': 50.0, 'level': True}
    s['size'] = [1680, 700]
    s['render']['samples'] = 64
    s['render']['exposure'] = 0.0
    s['title'] = 'Tropos, the eight in a painted room on their stripes'
    return s


HERO_FAN = [-35.0, -25.0, -15.0, -5.0, 5.0, 15.0, 25.0, 35.0]


def hero_room2(fan=HERO_FAN):
    """The owner on hero-room (2026-11-10 16:25): "wider bands and more space and maybe speakers going from outward facing
    to middle facing back to outward facing across the spectrum". Bands 1.0 m (= the spacing), the row framed with room:
    the speakers about 36 % of the height, a third of wall above the horns, about 30 % floor; the wall 1.7 m behind. Each
    speaker yawed on its own axis, centred on its band, from outward at the ends to straight in the middle (`fan`, Ember
    to Smoke; negative turns the front toward the frame's left). The low front fill is gone (it lit Haze's white lining
    and mirrored in Smoke's front): the soft overhead does the work, the key larger and higher, the contact shadow firmer."""
    s = hero_room()
    sp = 1.0
    n = len(HERO_ORDER)
    for blk in s['products']:
        for k, i in enumerate(blk['instances']):
            i['position'] = [round((k - (n - 1) / 2) * sp, 4)] + list(i['position'][1:])
            i['rotate_z'] = fan[k]
    for k, st in enumerate(s['set']['stripes']):
        x = (k - (n - 1) / 2) * sp
        st['x'] = [-30.0 if k == 0 else round(x - sp / 2, 4), 30.0 if k == n - 1 else round(x + sp / 2, 4)]
    s['set'].update(depth=1.7, contact={'strength': 1.2, 'distance_m': 0.35, 'core_strength': 1.5, 'core_distance_m': 0.03})
    s['lights'] = {
        'top': {'type': 'area', 'size_m': [7.0, 3.0], 'position': [0.0, -1.0, 3.6], 'target': [0.0, 0.2, 0.0],
                'irradiance': 3.2, 'color': '#FFF8F0'},
        'key': {'type': 'area', 'size_m': [3.0, 3.0], 'position': [-4.5, -4.0, 3.4], 'target': [0.0, 0.0, 0.6],
                'irradiance': 1.4, 'color': '#FFF5E8'}}
    s['camera'] = {'position': [0.0, -9.9, 0.9], 'target': [0.0, 0.0, 0.75], 'lens_mm': 40.0, 'level': True}
    s['title'] = 'Tropos, the eight fanned on wide stripes in a painted room'
    return s


def _aim_rot(frm, to):
    """Euler (deg) turning a kit cylinder's +z axis from `frm` toward `to`."""
    import math
    d = [t - f for f, t in zip(frm, to)]; L = math.sqrt(sum(v * v for v in d)); d = [v / L for v in d]
    return [round(math.degrees(math.acos(max(-1, min(1, d[2])))), 2), 0.0, round(math.degrees(math.atan2(d[0], -d[1])), 2)]


def _stand(name, base, head_z, legs=0.45):
    """A period lamp stand: a column and three splayed legs, black."""
    import math
    x, y = base
    out = [{'kind': 'kit', 'shape': 'cylinder', 'radius': 0.016, 'height': head_z, 'position': [x, y, 0.0],
            'material': 'gloss', 'color': '#141414'}]
    for k in range(3):
        a = math.radians(90 + 120 * k)
        out.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.012, 'height': legs,
                    'position': [x, y, 0.30], 'rotate': [118.0, 0.0, round(math.degrees(a) + 90, 1)],
                    'material': 'gloss', 'color': '#141414'})
    return out


def hero_shoot():
    """The owner (2026-11-11 02:10): "an Austin powers spy who shagged me photoshoot vibe ... more editorial". A 1960s mod
    fashion shoot, the eight Tropos the models; the genre evoked (a swinging-sixties studio, op-art target, bold colour),
    no film's set, characters or lettering, no people. A cyclorama painted with one giant target in the six colours and
    cream (0.45 m bands by 3D distance from a point low on the wall); the group in a loose V, Ember the star front and
    centre, five on gloss-cream podiums; in frame, a fresnel on a stand at the left (the hard key, high front-left) and a
    dish on a stand at back right (the rim), each lamp inside its own housing; a broad soft fill behind the camera; a
    camera on its tripod soft in the near right. 26 mm at 0.4 m, 1600 x 800."""
    assert ROLLOUT['base'] == 'A', 'run with TROPOS_BASE=A'
    s = _approved(SHOTS['deck-row']())
    # (tint, x, y, podium height, yaw): the star front and centre, a loose V of mixed depths, heights and angles
    pose = {'ember': (0.0, -0.55, 0.0, 0.0), 'dust': (-0.78, 0.15, 0.30, -18.0), 'acid': (0.80, 0.10, 0.15, 22.0),
            'poison': (-1.55, 0.75, 0.60, -32.0), 'ice': (1.50, 0.80, 0.45, 30.0), 'smoke': (0.30, 1.25, 0.60, 8.0),
            'haze': (-2.30, 1.30, 0.0, -48.0), 'fog': (2.30, 1.30, 0.0, 48.0)}
    for blk in s['products']:
        for k, i in enumerate(blk['instances']):
            x, y, h, yaw = pose[HERO_ORDER[k]]
            i['position'] = [x, y, round(h + i['position'][2], 4)]
            i['rotate_z'] = yaw
    props = []
    for t, (x, y, h, yaw) in pose.items():
        if h > 0:
            props.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.42, 'height': h, 'position': [x, y, 0.0],
                          'material': 'gloss', 'color': '#F1E8D6'})
    # the fresnel (key), high front-left, and the dish (rim), back right: each lamp in its housing
    fr_head, fr_aim = [-1.55, -1.45, 2.05], [0.0, 0.3, 0.7]
    props += _stand('fresnel', fr_head[:2], fr_head[2] - 0.12)
    props.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.14, 'height': 0.30, 'position': fr_head,
                  'rotate': _aim_rot(fr_head, [2 * a - b for a, b in zip(fr_head, fr_aim)]), 'material': 'gloss', 'color': '#161616'})
    dish_head, dish_aim = [2.55, 2.05, 1.85], [0.2, 0.4, 0.9]
    props += _stand('dish', dish_head[:2], dish_head[2] - 0.1)
    props.append({'kind': 'kit', 'shape': 'lathe', 'profile': [[0.06, 0.0], [0.2, 0.05], [0.33, 0.16], [0.34, 0.17]],
                  'position': dish_head, 'rotate': _aim_rot(dish_head, dish_aim), 'material': 'gloss', 'color': '#EDEAE4'})
    # the camera on its tripod, soft in the near right foreground
    props += _stand('tripod', [1.05, -3.2], 0.82, legs=0.9)
    props.append({'kind': 'kit', 'shape': 'box', 'size': [0.16, 0.11, 0.12], 'position': [1.05, -3.2, 0.82],
                  'material': 'gloss', 'color': '#1A1A1A', 'ease': 0.01})
    props.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.035, 'height': 0.09, 'position': [1.05, -3.27, 0.88],
                  'rotate': [90.0, 0.0, 0.0], 'material': 'gloss', 'color': '#111111'})
    rings = ['#F2E8D0', '#B50404', '#D35D17', '#C5BC1E', '#027614', '#1169C1', '#500CB4']
    s['set'] = {'kind': 'sweep', 'color': '#F2E8D0', 'width': 16.0, 'front': 8.0, 'depth': 2.6, 'radius': 1.0,
                'height': 6.0, 'rings': {'center': [0.0, 2.6, 0.55], 'width': 0.45, 'colors': rings}, 'props': props}
    s['materials']['sweep'] = {'roughness': 0.85}
    # the lamps: the fresnel's and the dish's sources sit just inside their housings' mouths (a practical in its
    # fitting); the fill a broad soft source behind the camera, out of frame
    import math
    def ahead(head, aim, d):
        v = [b - a for a, b in zip(head, aim)]; L = math.sqrt(sum(c * c for c in v))
        return [round(a + d * c / L, 3) for a, c in zip(head, v)]
    s['lights'] = {
        'fresnel': {'type': 'area', 'shape': 'DISK', 'size_m': [0.22, 0.22], 'position': ahead(fr_head, fr_aim, 0.02),
                    'target': fr_aim, 'irradiance': 7.0, 'spread_deg': 35, 'color': '#FFF2DE'},
        'dish': {'type': 'area', 'shape': 'DISK', 'size_m': [0.18, 0.18], 'position': ahead(dish_head, dish_aim, 0.12),
                 'target': dish_aim, 'irradiance': 4.5, 'spread_deg': 60, 'color': '#FFF6EC'},
        'fill': {'type': 'area', 'size_m': [5.0, 2.5], 'position': [0.0, -6.8, 1.7], 'target': [0.0, 0.3, 0.8],
                 'irradiance': 1.0, 'color': '#FFF8F0'}}
    s['camera'] = {'position': [0.0, -4.0, 0.4], 'target': [0.0, 0.6, 1.0], 'lens_mm': 26.0, 'level': True}
    s['size'] = [1600, 800]
    s['render'].update(samples=64, exposure=0.0)
    s['title'] = 'Tropos, the shoot: a 1960s fashion studio, the eight as the models'
    return s


def hero_shoot2():
    """The shoot, second pass (the coordinator, 2026-11-11 02:20, after the owner saw the first): the set black and white
    (op art: the target in alternating warm white and soft black; a spiral would need the paper's unrolled coordinates,
    which the sweep does not carry), so the only colour is the speakers and what is seen through them; the group opened
    up, Ember larger and nearer, Smoke seen, at most one small overlap; the gear in frame and readable: a fresnel upper
    left (the hard key), a white umbrella on its stand at the right (the soft fill, off the fronts' mirror angles), a
    camera on its tripod soft in the near right; the rim a hard lamp back right, out of frame. 30 mm, a little depth of
    field on the star."""
    s = hero_shoot()
    pose = {'ember': (0.0, -1.1, 0.0, 0.0), 'dust': (-1.15, 0.0, 0.30, -15.0), 'acid': (1.15, 0.05, 0.15, 18.0),
            'smoke': (0.95, 1.5, 0.60, 6.0), 'poison': (-2.0, 0.8, 0.60, -28.0), 'ice': (2.0, 0.8, 0.45, 28.0),
            'haze': (-2.6, 1.6, 0.0, -45.0), 'fog': (2.6, 1.6, 0.0, 45.0)}
    black = {'smoke', 'poison'}
    for blk in s['products']:
        for k, i in enumerate(blk['instances']):
            x, y, h, yaw = pose[HERO_ORDER[k]]
            base = 0.0385
            i['position'] = [x, y, round(h + base, 4)]
            i['rotate_z'] = yaw
    props = []
    for t, (x, y, h, yaw) in pose.items():
        if h > 0:
            props.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.42, 'height': h, 'position': [x, y, 0.0],
                          'material': 'gloss', 'color': '#151515' if t in black else '#F4F1EA'})
    fr_head, fr_aim = [-2.15, -0.25, 1.85], [0.0, 0.0, 0.7]
    props += _stand('fresnel', fr_head[:2], fr_head[2] - 0.12)
    props.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.15, 'height': 0.32, 'position': fr_head,
                  'rotate': _aim_rot(fr_head, [2 * a - b for a, b in zip(fr_head, fr_aim)]), 'material': 'gloss', 'color': '#161616'})
    props.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.155, 'height': 0.012,
                  'position': [round(a + 0.01 * (b - a), 3) for a, b in zip(fr_head, fr_aim)],
                  'rotate': _aim_rot(fr_head, fr_aim), 'material': 'frosted', 'color': '#F2EEE6'})
    um_head, um_aim = [2.45, -0.4, 1.75], [0.0, -0.2, 0.8]
    props += _stand('umbrella', um_head[:2], um_head[2] - 0.05)
    props.append({'kind': 'kit', 'shape': 'cone', 'radius': 0.55, 'radius_top': 0.02, 'height': 0.32, 'position': um_head,
                  'rotate': _aim_rot(um_head, [2 * a - b for a, b in zip(um_head, um_aim)]), 'material': 'satin', 'color': '#F6F4F0'})
    props.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.008, 'height': 0.75, 'position': um_head,
                  'rotate': _aim_rot(um_head, um_aim), 'material': 'gloss', 'color': '#141414'})
    props += _stand('tripod', [0.62, -3.05], 0.52, legs=0.6)
    props.append({'kind': 'kit', 'shape': 'box', 'size': [0.16, 0.11, 0.12], 'position': [0.62, -3.05, 0.52],
                  'material': 'gloss', 'color': '#1A1A1A', 'ease': 0.01})
    props.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.035, 'height': 0.09, 'position': [0.62, -3.12, 0.58],
                  'rotate': [90.0, 0.0, 0.0], 'material': 'gloss', 'color': '#111111'})
    s['set'].update(props=props, rings={'center': [0.0, 2.6, 0.55], 'width': 0.38, 'colors': ['#F2EDE4', '#1C1B1A']},
                    color='#F2EDE4')
    import math
    def ahead(head, aim, d):
        v = [b - a for a, b in zip(head, aim)]; L = math.sqrt(sum(c * c for c in v))
        return [round(a + d * c / L, 3) for a, c in zip(head, v)]
    s['lights'] = {
        'fresnel': {'type': 'area', 'shape': 'DISK', 'size_m': [0.22, 0.22], 'position': ahead(fr_head, fr_aim, -0.03),
                    'target': fr_aim, 'irradiance': 7.5, 'spread_deg': 35, 'color': '#FFF2DE'},
        'umbrella': {'type': 'area', 'shape': 'DISK', 'size_m': [0.7, 0.7], 'position': ahead(um_head, um_aim, -0.02),
                     'target': um_aim, 'irradiance': 1.6, 'color': '#FFF8F0'},
        'rim': {'type': 'area', 'shape': 'DISK', 'size_m': [0.35, 0.35], 'position': [4.3, 2.2, 2.6],
                'target': [0.0, 0.3, 1.0], 'irradiance': 5.0, 'spread_deg': 30, 'color': '#F4F7FF'}}
    s['camera'] = {'position': [0.0, -4.2, 0.45], 'target': [0.0, 0.6, 0.95], 'lens_mm': 30.0, 'level': True,
                   'fstop': 4.0, 'focus': [0.0, -1.1, 0.8]}
    s['title'] = 'Tropos, the shoot (second pass): op art in black and white, the eight in colour'
    return s


def _cast_base():
    """The eight as rollout.py builds them (_approved: base A, polished horn, black rods, the site's render settings): the
    deck row's products, re-posed by the caller with `_pose`."""
    assert ROLLOUT['base'] == 'A', 'run with TROPOS_BASE=A'
    s = _approved(SHOTS['deck-row']())
    s['materials'] = {k: v for k, v in s.get('materials', {}).items() if k != 'sweep'}
    return s


def _pose(s, pose):
    """pose: tint -> (x, y, z, yaw, tilt_x, tilt_y) for every product block's matching instance."""
    for blk in s['products']:
        for k, i in enumerate(blk['instances']):
            x, y, z, yaw, tx, ty = pose[HERO_ORDER[k]]
            i['position'] = [x, y, z]; i['rotate_z'] = yaw
            if tx: i['rotate_x'] = tx
            if ty: i['rotate_y'] = ty


def hero_hollywood():
    """The owner picked "the Hollywood issue" (2026-11-11 04:20): a gatefold group portrait of the cast as if they were
    people. A painted canvas backdrop (mottled warm grey-olive), a long velvet sofa in charcoal, a muted rug, a heavy
    drape at the left, a step behind the sofa; three standing behind it, two seated, Haze reclining along it as the
    diva, Acid on the floor leaning back on its front, Fog perched on the arm; Ember the star, a little left of centre.
    Lamps out of frame: a very large soft key from 45 deg left, a soft fill right, a kicker from behind and above."""
    s = _cast_base()
    seat, arm, step = 0.42, 0.62, 0.45
    _pose(s, {'ember': (-0.35, 0.0, seat, 8.0, 0, 0), 'dust': (-0.95, 0.02, seat, 14.0, 0, 0),
              'haze': (0.12, 0.05, seat + 0.28, -4.0, 0, 90.0), 'acid': (0.95, -0.78, 0.0, -14.0, -9.0, 0),
              'fog': (-1.47, 0.0, arm, 28.0, 0, 0), 'poison': (-0.85, 0.78, step, 10.0, 0, 0),
              'smoke': (0.05, 0.80, step, 0.0, 0, 0), 'ice': (0.95, 0.78, step, -10.0, 0, 0)})
    velvet, dark = 'velvet', '#2E2B29'
    props = [
        {'kind': 'kit', 'shape': 'box', 'size': [2.7, 0.9, 0.42], 'position': [0.0, 0.0, 0.0], 'material': velvet, 'color': dark, 'ease': 0.04},
        {'kind': 'kit', 'shape': 'box', 'size': [2.7, 0.22, 0.85], 'position': [0.0, 0.45, 0.0], 'material': velvet, 'color': dark, 'ease': 0.05},
        {'kind': 'kit', 'shape': 'box', 'size': [0.24, 0.9, 0.62], 'position': [-1.47, 0.0, 0.0], 'material': velvet, 'color': dark, 'ease': 0.06},
        {'kind': 'kit', 'shape': 'box', 'size': [0.24, 0.9, 0.62], 'position': [1.47, 0.0, 0.0], 'material': velvet, 'color': dark, 'ease': 0.06},
        {'kind': 'kit', 'shape': 'box', 'size': [3.0, 0.6, step], 'position': [0.0, 0.85, 0.0], 'material': 'clay', 'color': '#4A443C'},
        {'kind': 'kit', 'shape': 'box', 'size': [4.6, 3.0, 0.012], 'position': [0.0, -0.3, 0.0], 'material': 'wool', 'color': '#5B5046'},
        {'kind': 'kit', 'shape': 'box', 'size': [0.5, 0.32, 0.2], 'position': [1.6, -0.9, 0.0], 'material': 'clay', 'color': '#8A6A48'},
        {'kind': 'kit', 'shape': 'drape', 'size': [1.6, 3.6], 'position': [-2.9, 0.9, 3.6], 'folds': 9, 'amplitude': 0.12,
         'material': velvet, 'color': '#3B2E29'}]
    s['set'] = {'kind': 'sweep', 'color': '#6E6A58', 'width': 14.0, 'front': 10.0, 'depth': 2.0, 'radius': 0.6, 'height': 5.0,
                'contact': {'strength': 0.9, 'distance_m': 0.3, 'core_strength': 1.2, 'core_distance_m': 0.03}, 'props': props}
    s['materials']['sweep'] = {'roughness': 0.92, 'mottle': 0.35, 'mottle_m': 0.7, 'tooth': 0.2}
    s['lights'] = {
        'key': {'type': 'area', 'size_m': [4.0, 4.0], 'position': [-6.2, -5.4, 3.6], 'target': [0.0, 0.3, 0.9],
                'irradiance': 3.0, 'color': '#FFF4E6'},
        'fill': {'type': 'area', 'size_m': [4.0, 3.0], 'position': [5.5, -8.5, 2.0], 'target': [0.0, 0.2, 0.8],
                 'irradiance': 0.8, 'color': '#FFF8F0'},
        'kicker': {'type': 'area', 'size_m': [2.5, 1.0], 'position': [2.0, 1.6, 3.4], 'target': [0.0, 0.3, 1.0],
                   'irradiance': 3.0, 'spread_deg': 70, 'color': '#FFF6EA'}}
    s['camera'] = {'position': [0.15, -10.0, 1.05], 'target': [0.15, 0.0, 1.2], 'lens_mm': 60.0, 'level': True}
    s['size'] = [1920, 800]
    s['render'].update(samples=64, exposure=0.0)
    s['title'] = 'Tropos, the Hollywood issue: the cast as a gatefold group portrait'
    return s


def hero_orchestra(tiers=None, seats=None, cam_z=1.55):
    """The owner picked "the orchestra" (2026-11-11 04:20): the official portrait of an orchestra whose every player is
    a horn. A concert stage: three curved tiers about the conductor's podium, warm wood behind and underfoot, a black
    music stand before each player; the podium front and centre with its stand, back to the camera. The eight face
    the podium, by tier, symmetrical. Warm stage lamps above the frame's top; a little fill from the hall."""
    import math
    s = _cast_base()
    P = (0.0, -1.0)
    tiers = tiers or {0: (2.1, 0.0), 1: (3.0, 0.30), 2: (3.9, 0.60)}
    seats = seats or {'dust': (0, -40), 'ember': (0, 0), 'acid': (0, 40), 'poison': (1, -22), 'ice': (1, 22),
                      'haze': (2, -48), 'smoke': (2, 0), 'fog': (2, 48)}
    pose, stands = {}, []
    for t, (tier, th) in seats.items():
        r, z = tiers[tier]; a = math.radians(th)
        x, y = P[0] + r * math.sin(a), P[1] + r * math.cos(a)
        pose[t] = (round(x, 3), round(y, 3), z, -th, 0, 0)
        sx, sy = P[0] + (r - 0.62) * math.sin(a), P[1] + (r - 0.62) * math.cos(a)
        stands.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.012, 'height': 0.95, 'position': [round(sx, 3), round(sy, 3), z],
                       'material': 'gloss', 'color': '#111111'})
        stands.append({'kind': 'kit', 'shape': 'box', 'size': [0.46, 0.02, 0.32], 'position': [round(sx, 3), round(sy, 3), z + 0.88],
                       'rotate': [-25.0, 0.0, -th], 'material': 'gloss', 'color': '#111111'})
    _pose(s, pose)
    props = list(stands)
    for tier in (1, 2):
        r, z = tiers[tier]
        for th in range(-70, 71, 14):
            a = math.radians(th)
            props.append({'kind': 'kit', 'shape': 'box', 'size': [0.8, 1.0, z], 'position': [round(P[0] + r * math.sin(a), 3), round(P[1] + r * math.cos(a), 3), 0.0],
                          'rotate': [0.0, 0.0, -th], 'material': 'clay', 'color': '#5E3A20'})
    props += [{'kind': 'kit', 'shape': 'box', 'size': [0.7, 0.7, 0.22], 'position': [P[0], P[1], 0.0], 'material': 'clay', 'color': '#3A2618'},
              {'kind': 'kit', 'shape': 'cylinder', 'radius': 0.014, 'height': 1.1, 'position': [P[0], P[1] + 0.2, 0.22], 'material': 'gloss', 'color': '#111111'},
              {'kind': 'kit', 'shape': 'box', 'size': [0.5, 0.02, 0.36], 'position': [P[0], P[1] + 0.2, 1.24], 'rotate': [25.0, 0.0, 0.0], 'material': 'gloss', 'color': '#111111'}]
    s['set'] = {'kind': 'sweep', 'color': '#7A4A28', 'width': 16.0, 'front': 10.0, 'depth': 3.6, 'radius': 0.04, 'height': 6.0,
                'contact': {'strength': 0.8, 'distance_m': 0.3, 'core_strength': 1.0, 'core_distance_m': 0.03}, 'props': props}
    s['materials']['sweep'] = {'roughness': 0.45, 'mottle': 0.25, 'mottle_m': 0.25, 'tooth': 0.1}
    s['lights'] = {f'stage{k}': {'type': 'area', 'shape': 'DISK', 'size_m': [0.5, 0.5], 'position': [x, 1.0, 4.6],
                                 'target': [x * 0.6, 1.2, 0.6], 'irradiance': 2.6, 'spread_deg': 55, 'color': '#FFE0B4'}
                   for k, x in enumerate((-2.6, 0.0, 2.6))}
    s['lights']['hall'] = {'type': 'area', 'size_m': [3.0, 2.0], 'position': [0.0, -9.0, 3.2], 'target': [0.0, 1.0, 0.8],
                           'irradiance': 0.5, 'color': '#FFF0DC'}
    s['camera'] = {'position': [0.0, -7.6, cam_z], 'target': [0.0, 1.2, 0.95], 'lens_mm': 40.0, 'level': True}
    s['size'] = [1600, 800]
    s['render'].update(samples=64, exposure=0.0)
    s['title'] = 'Tropos, the orchestra: every player a horn'
    return s


def hero_orchestra2():
    """The orchestra, second pass (the coordinator, 2026-11-11 06:10): a pale hall (blond maple panelling, risers and
    floor) lit like a modern concert hall, the back tier as bright as the front; music desks no higher than the
    cabinets' tops, beside each player; the podium low, its stand short; the sections closer and nearer the camera."""
    import math
    s = _cast_base()
    P = (0.0, -0.8)
    tiers = {0: (1.75, 0.0), 1: (2.5, 0.28), 2: (3.25, 0.56)}
    seats = {'dust': (0, -36), 'ember': (0, 0), 'acid': (0, 36), 'poison': (1, -19), 'ice': (1, 19),
             'haze': (2, -40), 'smoke': (2, 0), 'fog': (2, 40)}
    pose, props = {}, []
    for t, (tier, th) in seats.items():
        r, z = tiers[tier]; a = math.radians(th)
        x, y = P[0] + r * math.sin(a), P[1] + r * math.cos(a)
        pose[t] = (round(x, 3), round(y, 3), z, -th, 0, 0)
        side = 1 if th <= 0 else -1                     # each desk on the player's inner side, toward the centre line
        tx, ty = math.cos(a), -math.sin(a)              # the tier's tangent at the player
        sx, sy = x + side * 0.40 * tx - 0.25 * math.sin(a), y + side * 0.40 * ty - 0.25 * math.cos(a)
        props.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.011, 'height': 0.62, 'position': [round(sx, 3), round(sy, 3), z],
                      'material': 'gloss', 'color': '#111111'})
        props.append({'kind': 'kit', 'shape': 'box', 'size': [0.40, 0.02, 0.28], 'position': [round(sx, 3), round(sy, 3), z + 0.58],
                      'rotate': [-25.0, 0.0, -th], 'material': 'gloss', 'color': '#111111'})
    _pose(s, pose)
    wood = '#D8C39C'
    for tier in (1, 2):
        r, z = tiers[tier]
        for th in range(-60, 61, 12):
            a = math.radians(th)
            props.append({'kind': 'kit', 'shape': 'box', 'size': [0.62, 0.8, z], 'position': [round(P[0] + r * math.sin(a), 3), round(P[1] + r * math.cos(a), 3), 0.0],
                          'rotate': [0.0, 0.0, -th], 'material': 'clay', 'color': '#E3CFA8'})
    props += [{'kind': 'kit', 'shape': 'box', 'size': [0.62, 0.62, 0.14], 'position': [P[0], P[1] - 0.2, 0.0], 'material': 'clay', 'color': '#3A2C22'},
              {'kind': 'kit', 'shape': 'cylinder', 'radius': 0.012, 'height': 0.42, 'position': [P[0] + 0.18, P[1] - 0.02, 0.14], 'material': 'gloss', 'color': '#111111'},
              {'kind': 'kit', 'shape': 'box', 'size': [0.36, 0.02, 0.24], 'position': [P[0] + 0.18, P[1] - 0.02, 0.54], 'rotate': [25.0, 0.0, 0.0], 'material': 'gloss', 'color': '#111111'}]
    s['set'] = {'kind': 'sweep', 'color': wood, 'width': 16.0, 'front': 10.0, 'depth': 3.2, 'radius': 0.04, 'height': 6.0,
                'contact': {'strength': 0.7, 'distance_m': 0.3, 'core_strength': 1.0, 'core_distance_m': 0.03}, 'props': props}
    s['materials']['sweep'] = {'roughness': 0.5, 'mottle': 0.12, 'mottle_m': 0.3, 'tooth': 0.08}
    s['lights'] = {f'stage{k}': {'type': 'area', 'size_m': [2.0, 1.2], 'position': [x, 0.6 + 0.8 * abs(k - 1), 4.4],
                                 'target': [x * 0.7, 1.0, 0.6], 'irradiance': 3.2, 'spread_deg': 75, 'color': '#FFEBD0'}
                   for k, x in enumerate((-2.4, 0.0, 2.4))}
    s['lights']['back'] = {'type': 'area', 'size_m': [5.0, 1.0], 'position': [0.0, 1.0, 4.6], 'target': [0.0, 2.3, 0.6],
                           'irradiance': 2.0, 'color': '#FFEBD0'}
    s['lights']['hall'] = {'type': 'area', 'size_m': [5.0, 2.5], 'position': [0.0, -9.0, 3.4], 'target': [0.0, 0.8, 0.8],
                           'irradiance': 1.0, 'color': '#FFF4E6'}
    s['camera'] = {'position': [0.0, -5.6, 1.45], 'target': [0.0, 1.0, 0.95], 'lens_mm': 40.0, 'level': True}
    s['size'] = [1600, 800]
    s['render'].update(samples=64, exposure=0.3)
    s['title'] = 'Tropos, the orchestra (second pass): a pale hall'
    return s


def _chair(x, y, yaw, seat=0.46, w=0.64, d=0.52, color='#2A1E18'):
    """An upholstered dark chair: four turned legs, a seat, a tall back with a rail; its back toward +y turned by `yaw`."""
    import math
    a = math.radians(yaw); c, sn = math.cos(a), math.sin(a)
    def at(dx, dy):
        return [round(x + c * dx - sn * dy, 3), round(y + sn * dx + c * dy, 3)]
    out = []
    for dx in (-w / 2 + 0.04, w / 2 - 0.04):
        for dy in (-d / 2 + 0.04, d / 2 - 0.04):
            out.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.022, 'radius_top': 0.016, 'height': seat,
                        'position': at(dx, dy) + [0.0], 'material': 'gloss', 'color': color})
    out.append({'kind': 'kit', 'shape': 'box', 'size': [w, d, 0.07], 'position': at(0, 0) + [seat - 0.02], 'rotate': [0, 0, yaw],
                'material': 'velvet', 'color': '#3B2A24', 'ease': 0.02})
    for dx in (-w / 2 + 0.03, w / 2 - 0.03):
        out.append({'kind': 'kit', 'shape': 'cylinder', 'radius': 0.02, 'height': 0.62, 'position': at(dx, d / 2 - 0.02) + [seat],
                    'material': 'gloss', 'color': color})
    out.append({'kind': 'kit', 'shape': 'box', 'size': [w, 0.04, 0.10], 'position': at(0, d / 2 - 0.02) + [seat + 0.56], 'rotate': [0, 0, yaw],
                'material': 'gloss', 'color': color, 'ease': 0.015})
    return out


def hero_hollywood2():
    """The Hollywood issue, second pass (the coordinator, 2026-11-11 06:10): no lounging (rigid boxes cannot lounge); a
    formal cast portrait. Four seated, each on its own dark upholstered chair, angled a little toward the centre; four
    standing behind on low steps of different heights, in the gaps; a muted rug under the front row, the drape at the
    left, the painted backdrop as before. The light a little brighter, the kicker making the bodies glow."""
    s = hero_hollywood()
    seat = 0.46 + 0.05
    front = {'dust': (-1.38, 12.0), 'ember': (-0.46, 5.0), 'acid': (0.46, -5.0), 'ice': (1.38, -12.0)}
    back = {'poison': (-0.92, 0.30), 'haze': (0.0, 0.48), 'smoke': (0.92, 0.30), 'fog': (1.88, 0.15)}
    pose, props = {}, []
    for blk in s['products']:                           # the first pass's recline and lean go
        for i in blk['instances']:
            i.pop('rotate_x', None); i.pop('rotate_y', None)
    for t, (x, yaw) in front.items():
        pose[t] = (x, 0.0, seat, yaw, 0, 0)
        props += _chair(x, 0.0, yaw)
    for t, (x, h) in back.items():
        pose[t] = (x, 0.85, h, 0.0, 0, 0)
        props.append({'kind': 'kit', 'shape': 'box', 'size': [0.8, 0.62, h], 'position': [x, 0.85, 0.0], 'material': 'clay', 'color': '#4A443C'})
    _pose(s, pose)
    props += [p for p in s['set']['props'] if p.get('shape') == 'drape']
    props.append({'kind': 'kit', 'shape': 'box', 'size': [4.4, 2.2, 0.012], 'position': [0.2, -0.3, 0.0], 'material': 'wool', 'color': '#6A5C50'})
    s['set']['props'] = props
    s['lights']['key']['irradiance'] = 3.6
    s['lights']['fill']['irradiance'] = 1.0
    s['lights']['kicker'].update(irradiance=4.2, position=[1.0, 2.0, 3.6], target=[0.2, 0.5, 1.1])
    s['camera'] = {'position': [0.25, -11.4, 1.1], 'target': [0.25, 0.0, 1.2], 'lens_mm': 60.0, 'level': True}
    s['title'] = 'Tropos, the Hollywood issue (second pass): a formal cast portrait'
    return s


# --- the third passes (the coordinator, 2026-11-11 06:50 and 07:05; the owner: "I actually like the first passes more
# than the second"; the horns "more satin than the product shots on the site") -------------------------------------------
# Why the horns were satin: the hero scenes were built with TROPOS_BASE=A but not TROPOS_HORN, so ROLLOUT['horn'] fell
# back to 'satin' and strata_lit wrote horn-satin roughness 0.25 (the site's A-polished fronts carry 0.05). The rest of
# what a scene built outside rollout.py took by default: the deck row's render settings (clamp 4, 16 bounces, no glossy
# or transmission bounce counts; the site's frames run clamp 8, 32 / 16 / 32, so the polished horn's and the clear
# shells' highlights were cut), and normals_refine false (the waveguide's facets not refined onto its true surface,
# which _cast_base set to spare the mask pass's memory). _approved closes all three, and checks every product block
# against rollout.py's own build of the site's tall front for that tint, so no other default can differ unseen.
SITE_RENDER_KEYS = ('clamp', 'bounces', 'glossy_bounces', 'transmission_bounces')


def _approved(s, order=None):
    """The eight exactly as rollout.py builds the site's fronts (A-polished, tallr7): base A, polished horn, black rods,
    the approved tints and linings; the site's render quality. Asserts each instance's product, flavour, hides and
    options against site('front-off-tall', tint) built the same way."""
    assert ROLLOUT['base'] == 'A', 'run with TROPOS_BASE=A'
    order = order or HERO_ORDER
    mats = s.setdefault('materials', {})
    mats['horn-satin'] = {**mats.get('horn-satin', {}), 'roughness': 0.05}       # polished, as rollout --horn polished
    for blk in s['products']:
        blk.pop('normals_refine', None)
    keep = ROLLOUT['horn']
    ROLLOUT['horn'] = 'polished'
    try:
        refs = {t: site('front-off-tall', t) for t in set(order)}
    finally:
        ROLLOUT['horn'] = keep
    ref0 = refs[order[0]]
    s['render'].update({k: ref0['render'][k] for k in SITE_RENDER_KEYS if k in ref0['render']})
    assert ref0['materials']['horn-satin']['roughness'] == mats['horn-satin']['roughness']
    sig = lambda b, i: (b['def'], i.get('flavour', b.get('flavour')), tuple(sorted(i.get('hide', []))), tuple(i.get('options') or []),
                        b.get('normals_refine', True))
    tropos = [b for b in s['products'] if 'barkhorn' in b['def']]
    for blk in tropos:
        for k, i in enumerate(blk['instances']):
            ref = next(b for b in refs[order[k]]['products'] if b['def'] == blk['def'])
            assert sig(blk, i) == sig(ref, ref['instances'][0]), (blk['def'], order[k], sig(blk, i), sig(ref, ref['instances'][0]))
    return s


LED_K = {'red': 2200, 'green': 2700, 'ice': 2700, 'violet': 3000, 'orange': 4000, 'amber': 4000, 'blue': 4000, 'black': 4000}
CORE_LOAD = {'orange': 1.5, 'amber': 1.5, 'blue': 1.5, 'black': 0.15}       # Dust, Acid, Ice at 3x (ae86581b); Smoke light grey
LAMPS_MODULE = 'spinoffs/barkhorn/planet/afterhours/lamps_final.py'          # the bar lane's embed (r33-planet-world 92db2b2d)
MANTLE_DEF = 'studio/products/mantle-strata-v3.json'                         # r48-mantle-design 450064b8, unchanged
KEY = {t: k for t, (_, k) in SITE_TINTS.items()}                             # tint -> the lamps' key (ember -> red)


def _family(hemis=(), cores=()):
    """The lamps as a set prop: Hemisphere [(tint, x, y, rim_z)], Core [(tint, x, y, floor_z, rot)]; lit only by their
    own LEDs at the lamp lane's lumens (LAMPS_ROOT: a checkout of r32-lamps-final)."""
    return {'kind': 'kit', 'shape': 'ext', 'path': LAMPS_MODULE, 'fn': 'place', 'led_k': LED_K, 'core_load': CORE_LOAD,
            'hemispheres': [{'tint': KEY[t], 'x': x, 'y': y, 'rim_z': z} for t, x, y, z in hemis],
            'cores': [{'tint': KEY[t], 'x': x, 'y': y, 'floor_z': z, 'rot': r} for t, x, y, z, r in cores]}


def _mantle(x, y, z, rz=0.0, flavour='smoke-2074'):
    return {'def': MANTLE_DEF, 'flavour': flavour, 'instances': [{'position': [x, y, z], 'rotate_z': rz}]}


def family_centres(s):
    """hero_centres' projection for the lamps and Mantle: each one's middle in percent of the frame."""
    import math, numpy as np
    cam = s['camera']; W, H = s['size']; c = np.array(cam['position'], float); t = np.array(cam['target'], float)
    lens = cam['lens_mm']; sw = cam.get('sensor_mm', 36.0); hx, hy = sw / 2, sw / 2 * H / W
    d0 = t - c; flat = np.array([d0[0], d0[1], 0.0]); f = flat / np.linalg.norm(flat)
    sy = cam.get('shift_y', 0.0) + math.tan(math.atan2(d0[2], np.linalg.norm(flat))) * lens / sw * (1.0 if W >= H else W / H)
    r = np.cross(f, [0.0, 0.0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)

    def pr(x, y, z):
        p = np.array([x, y, z]) - c; zz = p @ f
        X = ((p @ r) / zz * lens) / hx; Y = ((p @ u) / zz * lens - sy * sw) / hy
        return round(float((X + 1) / 2 * 100), 2), round(float((1 - Y) / 2 * 100), 2)
    out = []
    for p in s['set'].get('props', []):
        if p.get('path') == LAMPS_MODULE:
            inv = {v: k for k, v in KEY.items()}
            for h in p['hemispheres']:
                out.append({'product': 'hemisphere', 'tint': inv[h['tint']], **dict(zip('xy', pr(h['x'], h['y'], h['rim_z'] + 0.1)))})
            for c_ in p['cores']:
                out.append({'product': 'core', 'tint': inv[c_['tint']], **dict(zip('xy', pr(c_['x'], c_['y'], c_['floor_z'] + 0.12)))})
    for b in s['products']:
        if b['def'] == MANTLE_DEF:
            x, y, z = b['instances'][0]['position']
            out.append({'product': 'mantle', 'flavour': b['flavour'], **dict(zip('xy', pr(x, y, z + 0.08)))})
    return out


def _wood(tex, tint=None, mix=0.0, rough=1.0, gain=1.0):
    return {'material': 'pbr', 'texture': tex, 'tex_res': '2k', **({'tint': tint, 'tint_mix': mix} if tint else {}), 'rough_mul': rough, 'gain': gain}


def hero_orchestra3(family=True):
    """The orchestra, third pass (the owner prefers the first; the coordinator, 07:05): the first pass's hall, light and
    camera, with no music stands and no podium; the warm light carried onto the back tier so all eight read, Smoke
    included; the polished horn (_approved); the wood real (Poly Haven scans: old_wooden_floor_01 on the stage floor,
    oak_wood_planks on the risers, cherry_veneer panelling on the back wall). The family, if in: Hemisphere pendants in a
    row above the ensemble, Core lamps along the stage's front edge like footlights, Mantle on a low block at the front
    right corner."""
    # every player in the clear (a projection of each one's box against those nearer, the first layout's Smoke half
    # behind Ember): front +/-30 deg, middle +/-12 deg at 0.62 m, back +/-40 deg and centre at 1.25 m (a choir's risers),
    # the camera 0.35 m higher; Smoke 0 % covered, Poison and Ice 2 %
    s = _approved(hero_orchestra(tiers={0: (2.1, 0.0), 1: (3.0, 0.62), 2: (3.9, 1.25)},
                                 seats={'dust': (0, -30), 'ember': (0, 0), 'acid': (0, 30), 'poison': (1, -12), 'ice': (1, 12),
                                        'haze': (2, -40), 'smoke': (2, 0), 'fog': (2, 40)}, cam_z=1.9))
    F = 0.005                                                     # the stage floor's boards' top (laid 1 mm above the set's floor)
    props = []
    for p in s['set']['props']:
        if p.get('material') == 'gloss':                          # the music stands and the podium's stand
            continue
        if p.get('shape') == 'box' and p.get('size') == [0.7, 0.7, 0.22]:   # the podium
            continue
        sz = p['size'][:2] + [p['size'][2] + 0.001]               # sunk 1 mm into the boards: no coplanar faces
        props.append({**p, 'size': sz, 'position': [p['position'][0], p['position'][1], F - 0.001], **_wood('oak_wood_planks', '#4A2A16', 0.55, 0.9, 0.45)})
    props.append({'kind': 'kit', 'shape': 'box', 'size': [16.0, 13.0, F - 0.001], 'position': [0.0, -3.0, 0.001], **_wood('old_wooden_floor_01', '#5A3418', 0.5, 1.0, 0.55)})
    props.append({'kind': 'kit', 'shape': 'box', 'size': [16.0, 0.05, 6.0], 'position': [0.0, 3.5, F - 0.001], **_wood('cherry_veneer', '#3A2212', 0.75, 0.8, 0.3)})
    for blk in s['products']:
        for i in blk['instances']:
            i['position'][2] = round(i['position'][2] + F, 4)
    # the warm light on the back tier too: two more of the same stage lamps, over the back tier, aimed at its players
    for k, x in enumerate((-2.2, 2.2)):
        s['lights'][f'stageback{k}'] = {**s['lights']['stage1'], 'position': [x, 2.2, 4.8], 'target': [x * 1.05, 2.8, 1.8], 'irradiance': 1.6}
    s['lights']['stageback-c'] = {**s['lights']['stage1'], 'position': [0.0, 2.3, 4.8], 'target': [0.0, 2.9, 1.8], 'irradiance': 1.8}
    if family:
        hemis = [(t, x, 1.0, 2.8) for t, x in (('acid', -2.6), ('ember', -1.3), ('dust', 0.0), ('ember', 1.3), ('fog', 2.6))]
        cores = [(t, round(x, 3), -0.9, F, 200.0) for t, x in zip(('ice', 'poison', 'haze', 'smoke', 'dust', 'ember'), [-2.4 + 0.76 * k for k in range(6)])]
        props.append(_family(hemis, cores))
        props.append({'kind': 'kit', 'shape': 'box', 'size': [0.62, 0.52, 0.301], 'position': [2.45, -0.75, F - 0.001], **_wood('oak_wood_planks', '#6A3E22', 0.35, 0.9)})
        s['products'].append(_mantle(2.45, -0.75, F + 0.301, -20.0))
    s['set']['props'] = props
    s['camera']['target'][2] = 1.2                               # the frame's top over the pendants, the footlights' bases in
    s['title'] = 'Tropos, the orchestra (third pass): the first hall, no stands, the warm light on every player' + (', the family in' if family else '')
    return s


def hero_hollywood3(family=True):
    """The Hollywood issue, third pass (the owner prefers the first; the coordinator, 07:05): the first pass's staging,
    backdrop, drape and light; a real scanned sofa (Poly Haven sofa_03, a Victorian tufted leather sofa, 2.73 m, its seat
    at 0.55 m) for the black box; Haze still lying on its side along the seat (the series' joke); each of the eight
    readable: the group opened, the back three on a plywood riser 0.9 m high in the gaps, Poison clearly seen; a real
    muted rug (quatrefoil_jacquard_fabric, muted). The family, if in: Mantle on a real side table (side_table_01) at the
    left edge, a Core beside it, two Hemisphere pendants hanging in."""
    s = _approved(hero_hollywood())
    seat, arm, step = 0.555, 0.835, 0.9
    _pose(s, {'haze': (-0.93, -0.12, seat + 0.28, 0.0, 0, 90.0),             # on its side along the seat, horn toward Ember
              'ember': (0.62, -0.14, seat, -6.0, 0, 0),                        # the star, on the seat's right
              'fog': (-1.17, -0.06, arm, 14.0, 0, 0),                          # perched on the left arm
              'dust': (1.17, -0.06, arm, -14.0, 0, 0),                         # and the right
              'acid': (2.4, -0.9, 0.0, -22.0, -9.0, 0),                      # on the floor, leaning back on the front
              'poison': (-0.72, 0.85, step, 6.0, 0, 0), 'smoke': (-0.05, 0.85, step, 0.0, 0, 0), 'ice': (2.05, 0.55, 0.30, -10.0, 0, 0)})
    props = [p for p in s['set']['props'] if p.get('shape') == 'drape']
    props += [{'kind': 'kit', 'shape': 'asset', 'model': 'sofa_03', 'res': '2k', 'position': [0.0, 0.0, 0.0]},
              {'kind': 'kit', 'shape': 'box', 'size': [1.8, 0.6, step], 'position': [-0.4, 0.85, 0.0], **_wood('plywood')},
              {'kind': 'kit', 'shape': 'box', 'size': [0.7, 0.6, 0.30], 'position': [2.05, 0.55, 0.0], **_wood('plywood')},
              {'kind': 'kit', 'shape': 'box', 'size': [3.8, 2.6, 0.008], 'position': [0.0, -0.55, 0.001],
               **_wood('quatrefoil_jacquard_fabric', '#6B5A4E', 0.3, 1.0, 0.7)}]      # (full 1: muted 0.55 at 0.6 m a tile read flat salmon: its own scale, less tint, a darker stain)
    s['set']['props'] = props
    if family:
        props.append({'kind': 'kit', 'shape': 'asset', 'model': 'side_table_01', 'res': '2k', 'position': [-2.15, -0.15, 0.0]})
        s['products'].append(_mantle(-2.15, -0.15, 0.549, 15.0))
        props.append(_family(hemis=[('acid', -1.7, 0.2, 2.05), ('dust', 1.4, 0.3, 2.15)], cores=[('ember', -2.45, -0.55, 0.0, 200.0)]))
    # (proof 2: the floor at the frame's foot cut the Core and hid the rug, Acid cut at the right: a little lower, a little wider)
    s['camera'].update(target=[0.15, 0.0, 1.0], lens_mm=55.0)
    s['title'] = 'Tropos, the Hollywood issue (third pass): the first staging on a real sofa, Haze lying down' + (', the family in' if family else '')
    return s


# --- THE STAGE (the owner, 2026-11-11 12:45: "a stage image where each speaker has its hemisphere as a spotlight above
# it, some cutout prop near it, like a white cutout cloud on the ground for fog, a cutout of grass for poison, etc, and
# the spectrum of core at the front of the stage like the old bulbs"; the coordinator's brief, one test frame) ---------
STAGE_Z = 0.9                       # the stage's boards above the stalls' floor
CUTOUTS = 'spinoffs/barkhorn/campaign/stage/cutout_props.py'


def hero_stage(wash=0.02):
    """A small theatre stage dressed for a school play: red velvet curtains drawn to both sides and a valance, one
    continuous floor of scanned planks (Poly Haven old_planks_02... see STAGE_FLOOR), a flat painted night-blue
    backdrop. The eight in spectrum order in a shallow arc, staggered; over each its own Hemisphere in its own tint,
    0.6 m above the horn, hung from a black batten at the canopy's height; a plywood cutout of its icon beside each
    (cutouts.json); the eight Cores as footlights along the front edge, each below its speaker; Mantle on a low block
    at the front right. Haze lies on its side in its own pool. Lit by the lamps alone; `wash` (W/m2 at the stage) adds
    one faint stage wash from the house, out of frame (on by default: the lamps alone did not carry it)."""
    s = _cast_base()
    Z = STAGE_Z
    sp, n = 0.9, len(HERO_ORDER)
    pose, cut, hemis, cores = {}, [], [], []
    rim = Z + 1.283 + 0.6
    for k, t in enumerate(HERO_ORDER):
        x = round((k - (n - 1) / 2) * sp, 3)
        y = round(-0.30 * (x / 3.3) ** 2 + (0.28 if k % 2 else 0.0), 3)        # a shallow arc, every other one back
        if t == 'haze':
            pose[t] = (x - 0.64, y - 0.25, Z + 0.28, 0.0, 0, 90.0)            # on its side, its middle at x
        else:
            pose[t] = (x, y, Z, round(-x * 2.5, 1), 0, 0)                     # each turned a little toward the middle
        hemis.append((t, x, BATTEN_Y, rim))                                  # all hung from the one batten
        cores.append((t, x, -1.78, Z, 200.0))
    _pose(s, pose)
    # the cutouts: each in the gap on its left (in front, so it reads as a flat), Ember's outside on the left, Smoke's
    # on the right, Haze's sun standing behind it (Haze lies low); Poison's grass with its skull sign on a stake
    xs = {t: round((k - (n - 1) / 2) * sp, 3) for k, t in enumerate(HERO_ORDER)}
    ys = {t: pose[t][1] for t in HERO_ORDER}
    gap = lambda a, b: round((xs[a] + xs[b]) / 2, 3)
    place = {'ember': (xs['ember'] - 0.5, 0.62), 'dust': (gap('ember', 'dust'), 0.56), 'acid': (gap('dust', 'acid'), 0.6),
             'poison': (gap('acid', 'poison'), 0.55), 'ice': (gap('poison', 'ice'), 0.6), 'fog': (gap('fog', 'smoke'), 0.56),
             'smoke': (xs['smoke'] + 0.5, 0.6)}
    for t, (x, h) in place.items():
        cut.append({'key': t, 'x': x, 'y': round(min(ys.values()) - 0.36, 3), 'z': Z, 'height': h, 'yaw': round(-x * 2.0, 1)})
    # Haze lies low and would hide a sun stood behind it: the sun is flown in over it on two wires from the batten, as a
    # theatre flies a piece of scenery (proof 3)
    sun_z, sun_h, sun_y = Z + 0.82, 0.62, BATTEN_Y + 0.06
    cut.append({'key': 'haze', 'x': xs['haze'], 'y': sun_y, 'z': sun_z, 'height': sun_h, 'brace': False})
    cut.append({'key': 'poison-sign', 'x': gap('acid', 'poison') + 0.16, 'y': round(min(ys.values()) - 0.30, 3), 'z': Z,
                'height': 0.2, 'stake': 0.42})
    W, D0, D1 = 11.0, -1.95, 2.7                                  # the stage: width, its front edge, the backdrop
    props = [
        {'kind': 'kit', 'shape': 'box', 'size': [W, D1 - D0 + 0.1, Z - 0.001], 'position': [0.0, (D0 + D1) / 2, 0.001],
         'material': 'clay', 'color': '#141210'},                               # the stage's body, its front painted black
        {'kind': 'kit', 'shape': 'box', 'size': [W, D1 - D0 + 0.1, 0.006], 'position': [0.0, (D0 + D1) / 2, Z - 0.001],
         **_wood(STAGE_FLOOR, '#7A6048', 0.25, 1.0, 1.0)},                      # one continuous floor of boards
        {'kind': 'kit', 'shape': 'box', 'size': [W + 2, 0.06, 7.0], 'position': [0.0, D1 + 0.03, 0.001],
         'material': 'paper', 'color': '#16244A', 'roughness': 0.9},           # the painted night backdrop
        {'kind': 'kit', 'shape': 'drape', 'size': [2.4, 4.6], 'position': [-4.65, -1.55, Z + 4.6], 'folds': 13, 'amplitude': 0.09,
         'material': 'velvet', 'color': '#7A0E14', 'seed': 3},
        {'kind': 'kit', 'shape': 'drape', 'size': [2.4, 4.6], 'position': [4.65, -1.55, Z + 4.6], 'folds': 13, 'amplitude': 0.09,
         'material': 'velvet', 'color': '#7A0E14', 'seed': 5},
        {'kind': 'kit', 'shape': 'drape', 'size': [W + 1.0, 0.95], 'position': [0.0, -1.75, Z + 3.85], 'folds': 34, 'amplitude': 0.05,
         'material': 'velvet', 'color': '#6E0C12', 'seed': 7},
        # the proscenium: black flats outside the curtains and a header above the valance
        {'kind': 'kit', 'shape': 'box', 'size': [1.4, 0.2, 6.0], 'position': [-6.25, -1.9, 0.0], 'material': 'clay', 'color': '#0C0B0B'},
        {'kind': 'kit', 'shape': 'box', 'size': [1.4, 0.2, 6.0], 'position': [6.25, -1.9, 0.0], 'material': 'clay', 'color': '#0C0B0B'},
        {'kind': 'kit', 'shape': 'box', 'size': [W + 3.0, 0.2, 1.5], 'position': [0.0, -1.9, Z + 3.7], 'material': 'clay', 'color': '#0C0B0B'},
        # the lighting batten the pendants hang from (their canopies 0.776 m over the rim: hemi_mounting.py)
        {'kind': 'kit', 'shape': 'cylinder', 'radius': 0.024, 'height': 8.6, 'position': [-4.3, BATTEN_Y, rim + 0.776 + 0.024], 'rotate': [0.0, 90.0, 0.0],
         'material': 'gloss', 'color': '#0E0E0E'},
        {'kind': 'kit', 'shape': 'box', 'size': [0.7, 0.55, 0.22], 'position': [4.1, -1.25, Z - 0.001], 'material': 'clay', 'color': '#2A2522'},
        {'kind': 'kit', 'shape': 'ext', 'path': CUTOUTS, 'fn': 'place', 'cutouts': cut},
        *[{'kind': 'kit', 'shape': 'thread', 'a': [xs['haze'] + dx, sun_y + 0.0075, sun_z + sun_h * 0.62], 'b': [xs['haze'] + dx, BATTEN_Y, rim + 0.776],
           'radius': 0.0012, 'material': 'gloss', 'color': '#1A1A1A'} for dx in (-0.2, 0.2)],
        _family(hemis, cores)]
    s['products'].append(_mantle(4.1, -1.25, Z + 0.22, -25.0))
    s['set'] = {'kind': 'sweep', 'color': '#0E0D0C', 'width': 30.0, 'front': 16.0, 'depth': 4.0, 'radius': 0.05, 'height': 9.0,
                'contact': {'strength': 0.8, 'distance_m': 0.3, 'core_strength': 1.0, 'core_distance_m': 0.03}, 'props': props}
    s['materials'].pop('sweep', None)
    s['lights'] = {}
    if wash:
        # (proofs 1-2: the lamps alone left the speakers black and no pools on the floor at any clean exposure: the
        # Hemispheres glow but throw little onto what is 1.9 m below. One faint warm wash from the house, declared)
        s['lights']['house-wash'] = {'type': 'area', 'size_m': [3.0, 1.5], 'position': [0.0, -9.0, 5.5], 'target': [0.0, 0.0, Z + 1.4],
                                     'irradiance': wash, 'color': '#FFE6C8', 'spread_deg': 60}
    s['sky']['strength'] = 0.0                                    # no world light: the lamps (and the wash) only
    # (proof 1: the cast small and low in a dark frame, the curtains barely in: 1.3 m closer, the curtains drawn in)
    s['camera'] = {'position': [0.0, -10.2, 1.7], 'target': [0.0, 0.0, 2.5], 'lens_mm': 40.0, 'level': True}
    s['size'] = [1920, 880]
    # the lamp lane's own settings for these lamps (lamp_site.py, afterhours): no clamp, caustics, deep bounces; denoised
    s['render'].update({'samples': 256, 'denoise': True, 'clamp': 0, 'exposure': 6.3, 'white_balance_k': 3200, 'white_balance_tint': 0.0,
                        'bounces': 48, 'diffuse_bounces': 16, 'glossy_bounces': 24, 'transmission_bounces': 32,
                        'caustics_refractive': True, 'caustics_reflective': True})
    s.pop('finish', None)
    s['title'] = 'Tropos, THE STAGE: each one under its own Hemisphere, its cutout beside it, the Cores as footlights'
    return s


STAGE_FLOOR = 'oak_wood_planks'
BATTEN_Y = 0.12
