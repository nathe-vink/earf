"""C's olive disc (the critics, 21 Nov 04:47): the book's grey-green cloth (#4F6253) seen through the glass of water,
which stands about 17 cm in front of it on the camera's line. Two moves, as wide crops from C's own shot:
   e1-book: the book 6 cm along +x;  e2-glass: the glass 5 cm along -x."""
import copy, json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, '..', '..', '..', '2026-11-20', 'barkhorn', 'living', 'living-c-ember.shot.json')))
P = C['set']['props']
gi = next(i for i, p in enumerate(P) if p.get('fn') == 'water_glass')
gx, gy = P[gi]['position'][:2]
book = [i for i, p in enumerate(P) if p.get('material') in ('cotton', 'paper') and math.hypot(p['position'][0] - gx, p['position'][1] - gy) < 0.35]
assert len(book) == 4, book
s = copy.deepcopy(C)
for i in book:
    s['set']['props'][i]['position'][0] += 0.06
json.dump(s, open(os.path.join(HERE, 'e1-book.json'), 'w'), indent=1)
s = copy.deepcopy(C); s['set']['props'][gi]['position'][0] -= 0.05
json.dump(s, open(os.path.join(HERE, 'e2-glass.json'), 'w'), indent=1)
print('book pieces', book, 'glass', P[gi]['position'])
