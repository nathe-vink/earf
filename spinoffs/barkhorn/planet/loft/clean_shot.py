"""Re-make an earlier loft shot without Bell or Cumulus (the lead, 2026-10-19: neither in Planet until the owner picks
their second designs): the Ember speakers kept, a plain table lamp (planet_loft.table_lamps) and one bulb wherever Bell
stood, the record player gone. Everything else, the camera and the light, stays as the shot had it.

    python3 spinoffs/barkhorn/planet/loft/clean_shot.py IN.shot.json OUT.json
"""
import json, sys

CLOUD = 'studio/products/barkhorn-cloud.json'
LAMP = 'studio/products/barkhorn-lamp.json'


def clean(s):
    spots = [list(i['position']) for g in s['products'] if g['def'] == LAMP for i in g['instances']]
    s['products'] = [g for g in s['products'] if g['def'] == CLOUD]
    watts = sum(l['power_w'] for k, l in s['lights'].items() if k.startswith('bell')) / max(1, len(spots))
    s['lights'] = {k: l for k, l in s['lights'].items() if not k.startswith('bell')}
    for i, (x, y, z) in enumerate(spots):
        s['lights'][f'tlamp{i}'] = {'type': 'point', 'position': [x, y, round(z + 0.27, 4)], 'power_w': round(watts, 2),
                                    'radius_m': 0.02, 'color': 2700, 'camera': False}
    for p in s['set']['props']:
        if p.get('module') in ('planet_loft', 'planet_den'):
            p['module'] = 'planet_loft'; p['table_lamps'] = spots
    return s


if __name__ == '__main__':
    s = clean(json.load(open(sys.argv[1])))
    json.dump(s, open(sys.argv[2], 'w'), indent=1)
    print(sys.argv[2], len(s['lights']), 'lights')
