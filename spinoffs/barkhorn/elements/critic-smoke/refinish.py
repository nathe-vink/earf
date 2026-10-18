"""Re-finish a raw frame: neutralise the amber cast, lift the shadows a touch, dodge the speaker, then the shot's own
finish chain (studio/engine/finish.py). Args: RAW MASK SHOT OUT wb_r wb_b shadow_lift dodge_ev"""
import json, sys
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
sys.path.insert(0, '/home/user/earf/studio/engine')
import finish as F

raw, mask, shot, out = sys.argv[1:5]
wb_r, wb_b, lift, dodge = map(float, sys.argv[5:9])
rgb = np.asarray(Image.open(raw).convert('RGB')).astype(np.float64) / 255.0
lin = F.s2l(rgb)
Y = lin @ np.array([0.2126, 0.7152, 0.0722])
# white balance toward neutral, luminance kept
g = np.array([wb_r, 1.0, wb_b]); lin2 = lin * g
Y2 = lin2 @ np.array([0.2126, 0.7152, 0.0722]); lin2 *= (Y / np.maximum(Y2, 1e-6))[..., None]
# the speaker: any part id in the mask, feathered
m = np.asarray(Image.open(mask))
m = (m[..., 0] if m.ndim == 3 else m) > 0
mf = gaussian_filter(m.astype(np.float64), 2.0)
# shadow lift (a toe), and the dodge on the speaker for its darker tones
Y2 = lin2 @ np.array([0.2126, 0.7152, 0.0722])
toe = lift * np.exp(-Y2 / 0.02)                       # adds up to `lift` in linear at black, gone by mid-shadow
gain = 1.0 + toe / np.maximum(Y2, 1e-4) * (Y2 > 0)
gain = np.minimum(gain, 4.0)
dg = 2 ** (dodge * mf * np.clip(1.0 - Y2 / 0.12, 0, 1))
lin3 = lin2 * (gain * dg)[..., None]
srgb = np.clip(F.l2s(np.clip(lin3, 0, 1)), 0, 1)
tmp = out + '.pre.png'
Image.fromarray((srgb * 255 + 0.5).astype(np.uint8)).save(tmp)
fin = json.load(open(shot))['finish']
F.post(tmp, out, fin)
o = np.asarray(Image.open(out).convert('RGB')).astype(np.float64)
L = o @ np.array([0.2126, 0.7152, 0.0722])
print('cabinet mean', round(L[m].mean(), 1), 'ground below', round(L[1300:1600].mean(), 1),
      'cabinet rgb', o[m].mean(0).round(1))
