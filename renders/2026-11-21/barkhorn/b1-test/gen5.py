"""B1 fixed-5, a crop test (the coordinator, 12:46): fixed-4 with
   1. horn-card removed (a panel at diffuse 0, specular 1, off transmission: it emitted only into reflections);
   2. ceiling-panel rebuilt as a real light: an engine area lamp (a Cycles AREA light) of the same size, place, aim
      and colour, every ray visibility on (camera too), its light casting shadows as every Cycles lamp's does. Power:
      a panel of strength S lights like an area lamp of about 2.2 x S x area watts (measured 21 Nov on a white floor
      1 m under a 1 m square: emission strength 1 gave 0.277, a 1 W area lamp 0.126), so 2.2 x 8 x 1.28 = 22.5 W.
    python3 gen5.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = json.load(open(os.path.join(HERE, 'fixed4.json')))
s['lights'].pop('horn-card')
p = s['lights'].pop('ceiling-panel')
A = p['size_m'][0] * p['size_m'][1]
s['lights']['ceiling-light'] = {'type': 'area', 'shape': 'RECTANGLE', 'size_m': p['size_m'], 'position': p['position'],
                                'target': p['target'], 'power_w': round(2.2 * p['strength'] * A, 1), 'color': p['color'],
                                'camera': True}
s['title'] = s['title'].replace('B1 fixed-4', 'B1 fixed-5 (no horn card; the ceiling panel a real area light)')
json.dump(s, open(os.path.join(HERE, 'fixed5.json'), 'w'), indent=1)
print(s['lights']['ceiling-light'])
