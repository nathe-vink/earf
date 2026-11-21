"""The proof's variants of A: base, pier, cam, back, all (+ water)."""
import copy, json, os, sys
sys.path.insert(0, '/home/user/earf/spinoffs/barkhorn/campaign')
import living_room as L
od = sys.argv[1]
B0 = copy.deepcopy(L.WIN_BACK)
def front_pier(s, pier=1.2):
    out = []
    for w in s['set']['windows']:
        if w['wall'] != 'front':
            out.append(w); continue
        tot = w['size'][0]; each = (tot - pier) / 2
        for sg in (-1, 1):
            out.append({**w, 'along': sg * (pier / 2 + each / 2), 'size': [each, w['size'][1]], 'mullions': [2, 2]})
    s['set']['windows'] = out
def make(name, pier=False, cam=False, back=False, water=False):
    L.WIN_BACK.clear(); L.WIN_BACK.update(B0)
    if back:
        L.WIN_BACK.update({'along': -2.33, 'size': [0.6, 1.95]})
    L.WATER = 0.078 if water else 0.06
    s = L.SHOTS['living-a']('ember')
    if pier: front_pier(s)
    if cam:
        s['camera'] = copy.deepcopy(s['camera']); s['camera']['position'] = [*s['camera']['position'][:2], 1.15]
    s['size'] = [960, 640]
    json.dump(s, open(os.path.join(od, f'{name}.json'), 'w'), indent=1)
    print(name, s['camera']['position'], [ (w['wall'], w.get('along'), w['size']) for w in s['set']['windows']])
make('base'); make('pier', pier=True); make('cam', cam=True); make('back', back=True)
make('all', pier=True, cam=True, back=True, water=True)
