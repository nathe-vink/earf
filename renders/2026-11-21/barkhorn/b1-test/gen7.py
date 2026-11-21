"""B1 fixed-7 (the coordinator, 16:09): fixed-6 with real black-fabric grids and skirts on both frontal softboxes, as a
photographer rigs them (living_ext.softbox `skirt` 0.3 m: the box's sides carried forward past the face; `grid` 4 x 3
egg-crate louvers 0.12 m deep), so the light stays on the bays and off the ceiling, the record wall and the left wall.
The far softbox moves to (6.5, 3.4, 2.98) so its skirt stays out of frame (z 2.44-3.37; every corner and edge outside
the frame). fixed-7b (the quarter test with grids: the record wall stayed at 45 and the grid cut the batts' light more
than the cone's, ratio 0.38): skirts only, and the ceiling-flush diffuser removed. Optionally `wall` scales the record-wall heads (a real dimmer).
    python3 gen7.py [WALL] [--grid]  ->  fixed7.json and fixed7q.json (the quarter test: 800 x 450, 96 samples)"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
wall = float(next((a for a in sys.argv[1:] if not a.startswith('--')), 1.0))
s = json.load(open(os.path.join(HERE, 'fixed6.json')))
grid = '--grid' in sys.argv
for p in s['set']['props']:
    if p.get('fn') == 'softbox' and p['size'] == [1.2, 0.9]:
        p.update(skirt=0.3)
        if grid:
            p.update(grid=[4, 3], grid_depth=0.12)
        if p['position'][0] < 7:
            p['position'] = [6.5, 3.4, 2.92]        # (its body's top z 3.36: at 2.98 the body reached 3.418)
# (fixed-7b) the diffuser flush under the ceiling over the near bay goes: it was there for the bell (t6), which it did
# not light, and it lit the record wall below it
s['set']['props'] = [p for p in s['set']['props'] if not (p.get('fn') == 'softbox' and p['size'] == [1.4, 0.9])]
for k, l in s['lights'].items():
    if k.startswith('track-wall'):
        l['irradiance'] = round(l['irradiance'] * wall, 3)
s['title'] = 'B1 fixed-7: Planet EARF bar, the record wall from a seat at the bar (a test, not a final)'
json.dump(s, open(os.path.join(HERE, 'fixed7.json'), 'w'), indent=1)
q = copy.deepcopy(s); q['size'] = [800, 450]; q['render']['samples'] = 96; q['title'] += ', the quarter test'
json.dump(q, open(os.path.join(HERE, 'fixed7q.json'), 'w'), indent=1)
print([(p['position'], p.get('skirt'), p.get('grid')) for p in s['set']['props'] if p.get('fn') == 'softbox'], 'wall x', wall)
