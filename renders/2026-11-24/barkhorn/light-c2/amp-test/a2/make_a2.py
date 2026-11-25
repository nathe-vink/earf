"""The eight amp rig A2 shot files (full size): each tint's ampA file with the changes that turn Ad-ice into A2a-ice
(flag 1 camera on; the strip a real body orbited to azimuth -55) and the turns' path depth (32 total, 16 glossy,
32 transmission).    python3 amp-test/a2/make_a2.py   (from light-c2)"""
import json, copy
TINTS = ('acid', 'dust', 'ember', 'fog', 'haze', 'ice', 'poison', 'smoke')
def diff(a, b, p=()):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b: yield p + (k,), b.get(k, '<del>')
            else: yield from diff(a[k], b[k], p + (k,))
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)): yield from diff(x, y, p + (i,))
    elif a != b: yield p, b
def put(d, p, v):
    for k in p[:-1]: d = d[k]
    if v == '<del>': d.pop(p[-1])
    else: d[p[-1]] = v
ad, a2a = (json.load(open(f'amp-test/a2/{n}-ice.json')) for n in ('Ad', 'A2a'))
changes = [(p, v) for p, v in diff(ad, a2a) if p != ('title',)]
for p, v in changes: print('change', '/'.join(map(str, p)), '->', v)
for t in TINTS:
    s = json.load(open(f'ampA-{t}.json'))
    for p, v in changes: put(s, p, copy.deepcopy(v))
    s['render'].update(bounces=32, glossy_bounces=16, transmission_bounces=32)
    s['title'] = s['title'].replace('amp rig A (', 'amp rig A2 (real strip with a body, moved clear of the key to azimuth -55; flag 1 seen by the camera; path depth 32/16/32; ')
    json.dump(s, open(f'ampA2-{t}.json', 'w'), indent=1); open(f'ampA2-{t}.json', 'a').write('\n')
