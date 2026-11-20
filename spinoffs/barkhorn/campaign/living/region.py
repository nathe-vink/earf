"""Join a region rendered with --crop (same shot, more samples) into the frame, feathered over its last `feather` px;
prints the mean and 99th-percentile difference over the feather (noise if the two renders agree).

    python3 region.py FRAME.png REGION.png X0 Y0 OUT.png [FEATHER]
"""
import sys
import numpy as np
from PIL import Image

F = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
R = np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(float)
x0, y0 = int(sys.argv[3]), int(sys.argv[4]); fe = int(sys.argv[6]) if len(sys.argv) > 6 else 16
h, w = R.shape[:2]
yy, xx = np.mgrid[0:h, 0:w]
edge = np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]).astype(float)
wgt = np.clip(edge / fe, 0, 1)[..., None]
sub = F[y0:y0 + h, x0:x0 + w]
ring = (edge < fe)
d = np.abs(sub - R).max(2)[ring]
out = F.copy(); out[y0:y0 + h, x0:x0 + w] = sub * (1 - wgt) + R * wgt
Image.fromarray(np.clip(out.round(), 0, 255).astype(np.uint8)).save(sys.argv[5], optimize=True)
print(f'region {w}x{h} at {x0},{y0}: over the {fe} px feather, mean {d.mean():.2f}, p99 {np.percentile(d, 99):.1f} /255; '
      f'inside, mean change {np.abs(sub - R).max(2)[~ring].mean():.2f}')
