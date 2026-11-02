"""Variants of a study shot for the sheen: `cards` (the reflection-only panels off), `spec` (the horn and fill lights'
specular off, the rim off), `flags` (dark reflection-only cards round the camera, so the polished faces mirror a dark,
warm surround), `rough=R` (the horn's outside satin: horn-lot roughness R, in the shot's def copies)."""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
src, tag, *mods = sys.argv[1:]
s = json.load(open(f'{HERE}/shot-{src}.json'))
L = s['lights']
for m in mods:
    if m == 'cards':
        for n in ('scrim', 'sheen', 'topline', 'sidesheen'):
            if n in L: L[n]['strength'] = 0.0
    elif m == 'spec':
        for n in ('horn', 'fill'):
            if n in L: L[n]['specular'] = 0.0
        if 'rim' in L: L['rim']['power_w'] = 0.0
    elif m == 'soft':
        L['key']['size_m'] = [3.0, 3.0]; L['horn']['size_m'] = [4.0, 3.0]
    elif m == 'flags':
        fl = s['set'].setdefault('flags', [])
        fl += [{'center_m': [0.0, -2.6, 1.9], 'size_m': [3.0, 1.6], 'normal': [0.0, 0.85, -0.5], 'reflect_only': True, 'color': '#16120F'},
               {'center_m': [-1.6, -1.8, 1.3], 'size_m': [1.6, 2.4], 'normal': [0.7, 0.7, 0.0], 'reflect_only': True, 'color': '#16120F'},
               {'center_m': [1.6, -1.8, 1.3], 'size_m': [1.6, 2.4], 'normal': [-0.7, 0.7, 0.0], 'reflect_only': True, 'color': '#16120F'}]
    elif m.startswith('rough='):
        r = float(m[6:])
        for b in s['products']:
            d = json.load(open(b['def']))
            for f in d['flavours'].values():
                if 'horn-lot' in f.get('materials', {}):
                    f['materials']['horn-lot']['roughness'] = r
            if 'horn-lot' in d['materials']:
                d['materials']['horn-lot']['roughness'] = r
            q = b['def'].replace('.json', f'-{tag}.json'); json.dump(d, open(q, 'w')); b['def'] = q
json.dump(s, open(f'{HERE}/shot-{tag}.json', 'w'), indent=1)
print(tag, mods)
