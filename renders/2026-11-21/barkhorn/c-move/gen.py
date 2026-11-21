"""C, the ball's back light (the coordinator, 21 Nov 05:58: keep filter_glossy 0 and AgX; take the window's line off
the ball as a photographer would place the lamp). The line from the camera through the ball meets the narrow left
window (the left wall at x -2.7, y 1.55 to 1.95), whose daylight is the ball's back light. The Core cannot leave that
line on the side table (0.55 x 0.45 m), so the table with all it carries (the Core, the glass, the book) and the camera
move together by dy along y: the group keeps its framing and the window passes off the ball. The book also moves
6 cm along +x (the olive disc: its cloth seen through the water). Quarter size, 256 samples.
    python3 gen.py    -> m025.json, m035.json"""
import copy, json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, '..', '..', '..', '2026-11-20', 'barkhorn', 'living', 'living-c-ember.shot.json')))
TABLE = (-2.2, 1.5)
def near(p):                                              # on or of the side table
    return 'position' in p and abs(p['position'][0] - TABLE[0]) < 0.3 and abs(p['position'][1] - TABLE[1]) < 0.25
for dy in (-0.25, -0.35):
    s = copy.deepcopy(C); moved = []
    for p in s['set']['props']:
        if p.get('fn') == 'cores_off':
            for c in p['cores']:
                c['y'] += dy
            moved.append('core')
        elif near(p):
            p['position'][1] += dy; moved.append(p.get('model') or p.get('fn') or p.get('material'))
            if p.get('material') in ('cotton', 'paper') and p.get('fn') is None and p.get('model') is None:
                p['position'][0] += 0.06
    cam = s['camera']
    for k in ('position', 'target', 'focus'):
        cam[k][1] += dy
    s['size'] = [400, 500]
    nm = f'm{abs(round(dy * 100)):03d}'
    json.dump(s, open(os.path.join(HERE, nm + '.json'), 'w'), indent=1)
    cx, cy = s['set']['props'][[i for i, p in enumerate(s['set']['props']) if p.get('fn') == 'cores_off'][0]]['cores'][0]['x'], None
    print(nm, 'moved', moved, 'camera', cam['position'])
