"""A2 extra readings: lining slab (every lining-*), deep inside (back, its ribs and bosses), by each frame's own mask."""
import json, sys, numpy as np
from PIL import Image
exec(open(__file__.replace('a2meas.py', 'meas.py')).read().split('rows = [')[0])
print('| frame | lining L* | deep inside L* | deep inside p10 |'); print('|---|---|---|---|')
for arg in sys.argv[1:]:
    name, png = arg.split('='); stem = png[:-4]
    m = json.load(open(stem + '.mask.json')); ids = np.asarray(Image.open(stem + '.mask.png').convert('RGB'))[..., 0].astype(int)
    sel = lambda f: np.isin(ids, [int(k) for k, v in m.items() if f(v)])
    L = lab(np.asarray(Image.open(png).convert('RGB')).astype(float))[0][..., 0]
    lin = sel(lambda v: v.startswith('lining-')); deep = sel(lambda v: v == 'back' or v.startswith('rib-back') or v.startswith('back-boss'))
    print(f'| {name} | {L[lin].mean():.1f} | {L[deep].mean():.1f} | {np.percentile(L[deep], 10):.1f} |')
