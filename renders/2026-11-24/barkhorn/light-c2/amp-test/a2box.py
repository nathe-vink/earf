"""A2 box readings, in fractions of the frame (the back is clear, so the mask calls everything behind it 'back'):
lining slab = the felt slab at the left, deep inside = the dark gap between it and the plate."""
import sys, numpy as np
from PIL import Image
exec(open(__file__.replace('a2box.py', 'meas.py')).read().split('rows = [')[0])
B = {'lining slab': (0.09, 0.20, 0.15, 0.75), 'deep inside': (0.26, 0.34, 0.30, 0.80)}
print('| frame | ' + ' | '.join(B) + ' | clipped >= 251 |'); print('|---' * (len(B) + 2) + '|')
for arg in sys.argv[1:]:
    name, png = arg.split('='); a = np.asarray(Image.open(png).convert('RGB')).astype(float); h, w = a.shape[:2]
    L = lab(a)[0][..., 0]
    v = [L[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)].mean() for x0, x1, y0, y1 in B.values()]
    print(f'| {name} | ' + ' | '.join(f'{x:.1f}' for x in v) + f' | {(a.max(-1) >= 251).mean() * 100:.1f} % |')
