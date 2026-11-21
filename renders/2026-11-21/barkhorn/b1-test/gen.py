"""The bar test B1 (the coordinator, 21 Nov): bar-backbar at half size (1600 x 900, its full frame's 256 samples), live
against fixed.
   live:  the site's frame, its committed shot file (renders/2026-11-11/barkhorn/product/planet-bar/bar-backbar.shot.json,
          14 Nov; planet_bar.py's own source commit is not in this shallow clone), size halved
   fixed: 1. the shadow-ray shortcut cut wherever caustics are on (living_ext.no_glass_shadows, last in the set: the
             Tropos acrylic, Mantle's, the Cores'); the frame's refractive caustics stay on
          2. the horn-card panel hidden from transmission (planet_bar.py:256-258; the engine's panel takes the flag
             from 21 Nov)
          3. the two drinks as liquid in contact with the glass at its own IOR (whisky 1.36, living_ext.water_glass),
             the ice at 1.31 cut at the liquid's top (no overlapping volumes); the whisky's tint the kit resin's
             #A65812 at its two interfaces, the ice's roughness the kit frosted's 0.35, so only the optics change
          4. filter_glossy 0
    python3 gen.py"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EXT = 'spinoffs/barkhorn/campaign/living/living_ext.py'
RK = [[0, 0], [0.041, 0], [0.043, 0.006], [0.044, 0.092]]                   # planet_bar._life's rocks glass

live = json.load(open(os.path.join(ROOT, 'renders/2026-11-11/barkhorn/product/planet-bar/bar-backbar.shot.json')))
live['size'] = [1600, 900]
live['title'] = 'B1 live: ' + live['title']
fixed = copy.deepcopy(live)
fixed['title'] = live['title'].replace('B1 live', 'B1 fixed')
fixed['render']['filter_glossy'] = 0.0
fixed['lights']['horn-card']['transmission'] = False
props = fixed['set']['props']
glasses = [pr for pr in props if pr.get('shape') == 'lathe' and pr.get('material') == 'glass' and pr['position'][2] > 1.0]
drinks = []
for g in glasses:
    gx, gy, gz = g['position']
    liq = [pr for pr in props if pr.get('shape') == 'lathe' and pr.get('material') == 'resin' and pr['position'][:2] == [gx, gy]]
    ice = [pr for pr in props if pr.get('shape') == 'box' and pr.get('material') == 'frosted' and abs(pr['position'][0] - gx) < 0.03
           and abs(pr['position'][1] - gy) < 0.03 and abs(pr['position'][2] - gz) < 0.1]
    assert len(liq) == 1 and len(ice) == 2, (g['position'], len(liq), len(ice))
    fill = max(z for _, z in liq[0]['profile'])
    drinks.append({'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'water_glass', 'profile': RK, 'wall': 0.0035, 'base': 0.016,
                   'fill': fill, 'meniscus': 0.0015, 'segments': 128, 'position': [gx, gy, gz + 0.0003], 'ior': 1.36,
                   'color': liq[0]['color'], 'ice_ior': 1.31, 'ice_roughness': 0.35,
                   'ice': [{'size': c['size'], 'position': c['position'], 'rotate': c.get('rotate', [0, 0, 0]), 'ease': c.get('ease', 0)} for c in ice]})
    for pr in [g, liq[0]] + ice:
        props.remove(pr)
    print('drink at', [round(gx, 3), round(gy, 3)], 'fill', fill, 'colour', liq[0]['color'])
assert len(drinks) == 2, len(drinks)
props += drinks
props.append({'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'no_glass_shadows'})
for n, s in (('live', live), ('fixed', fixed)):
    json.dump(s, open(os.path.join(HERE, n + '.json'), 'w'), indent=1)
print('caustics', fixed['render'].get('caustics_refractive'), fixed['render'].get('caustics_reflective'), 'fg', fixed['render']['filter_glossy'])
