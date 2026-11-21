"""B1 fixed-7 (the coordinator, 16:09): fixed-6 with real black-fabric grids and skirts on both frontal softboxes, as a
photographer rigs them (living_ext.softbox `skirt` 0.3 m: the box's sides carried forward past the face; `grid` 4 x 3
egg-crate louvers 0.12 m deep), so the light stays on the bays and off the ceiling, the record wall and the left wall.
The far softbox moves to (6.5, 3.4, 2.98) so its skirt stays out of frame (z 2.44-3.37; every corner and edge outside
the frame). Optionally `wall` scales the record-wall heads (a real dimmer).
    python3 gen7.py [WALL]  ->  fixed7.json and fixed7q.json (the quarter test: 800 x 450, 96 samples)"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
wall = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
s = json.load(open(os.path.join(HERE, 'fixed6.json')))
for p in s['set']['props']:
    if p.get('fn') == 'softbox' and p['size'] == [1.2, 0.9]:
        p.update(skirt=0.3, grid=[4, 3], grid_depth=0.12)
        if p['position'][0] < 7:
            p['position'] = [6.5, 3.4, 2.98]
for k, l in s['lights'].items():
    if k.startswith('track-wall'):
        l['irradiance'] = round(l['irradiance'] * wall, 3)
s['title'] = 'B1 fixed-7: Planet EARF bar, the record wall from a seat at the bar (a test, not a final)'
json.dump(s, open(os.path.join(HERE, 'fixed7.json'), 'w'), indent=1)
q = copy.deepcopy(s); q['size'] = [800, 450]; q['render']['samples'] = 96; q['title'] += ', the quarter test'
json.dump(q, open(os.path.join(HERE, 'fixed7q.json'), 'w'), indent=1)
print([(p['position'], p.get('skirt'), p.get('grid')) for p in s['set']['props'] if p.get('fn') == 'softbox'], 'wall x', wall)
