"""Flat-panel blotch (meas.py's measure) in one window of the 1600 x 1600 amp frame, so a crop render and a full frame
(FA123's, or light C's) are compared on the same pixels, with a full frame's mask of the same camera cut to the window.
    python3 blotch_crop.py MASKSTEM X0 Y0 W H NAME=PNG ...
A PNG of size W x H is taken as the crop itself; a 1600 x 1600 PNG is cut to the window."""
import importlib.util, json, os, sys
import numpy as np
from PIL import Image

spec = importlib.util.spec_from_file_location('meas_src', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meas.py'))
ns = {}
exec(open(spec.origin).read().split('rows = [')[0], ns)          # meas.py's lab(), blotch() and PANELS, not its loop

stem, x0, y0, w, h = sys.argv[1], *(int(v) for v in sys.argv[2:6])
m = json.load(open(stem + '.mask.json'))
ids = np.asarray(Image.open(stem + '.mask.png').convert('RGB'))[..., 0].astype(int)
pan = np.isin(ids, [int(k) for k, v in m.items() if v in ns['PANELS']])[y0:y0 + h, x0:x0 + w]
for arg in sys.argv[6:]:
    name, png = arg.split('=')
    rgb = np.asarray(Image.open(png).convert('RGB')).astype(float)
    if rgb.shape[:2] == (1600, 1600):
        rgb = rgb[y0:y0 + h, x0:x0 + w]
    if rgb.shape[:2] != (h, w):
        print(f'{name}: size {rgb.shape[1]}x{rgb.shape[0]} is neither the window nor the full frame'); continue
    L, _ = ns['lab'](rgb)
    print(f'{name}: flat-panel blotch L* RMS {ns["blotch"](L[..., 0], pan, 1.0):.2f}  (mean L* {L[..., 0][pan].mean():.1f})')
