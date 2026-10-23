"""Stitch a final from haze_b_strips' top strips and one lower crop rendered in a single process (so the rubble, which a
separate render process can build differently, is one build): the crop's top rows overlap the last top strip's bottom
rows and are feathered across them; the shot's finish is applied once over the whole frame, as haze_b_strips.stitch does.

    python3.11 spinoffs/barkhorn/elements/stitch_crop.py SHOT STRIPS_DIR N_TOP CROP.png CROP_TOP_ROW OUT.png
"""
import json, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
shot, wd, ntop, crop, ctop, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), sys.argv[6]
s = json.load(open(shot)); W, H = s['size']
acc = np.zeros((H, W, 3)); wsum = np.zeros((H, 1, 1))
pieces = []
for i in range(ntop):
    rows = json.load(open(os.path.join(wd, f'strip{i}.png.done')))['rows']
    pieces.append((rows[0], np.asarray(Image.open(os.path.join(wd, f'strip{i}.png')).convert('RGB')).astype(np.float64)))
cim = np.asarray(Image.open(crop).convert('RGB')).astype(np.float64)
assert cim.shape[1] == W and ctop + cim.shape[0] == H, (cim.shape, ctop, H)
pieces.append((ctop, cim))
for k, (top, im) in enumerate(pieces):
    h = im.shape[0]; w = np.ones(h)
    if k > 0:                                  # feather in over the overlap with the piece above
        ptop, pim = pieces[k - 1]; pend = ptop + pim.shape[0]
        ov = pend - top
        for j in range(min(ov, h)):
            w[j] = (j + 0.5) / ov
    if k < len(pieces) - 1:                    # and out over the overlap with the piece below
        ntop_, nim = pieces[k + 1]; ov = top + h - ntop_
        for j in range(ov):
            w[h - ov + j] = min(w[h - ov + j], 1 - (j + 0.5) / ov)
    acc[top:top + h] += im * w[:, None, None]; wsum[top:top + h] += w[:, None, None]
img = (acc / np.maximum(wsum, 1e-6)).clip(0, 255).round().astype(np.uint8)
raw = out[:-4] + '.raw.png'; Image.fromarray(img).save(raw)
sys.path.insert(0, os.path.join(ROOT, 'studio/engine'))
import finish as Fn
pr = Fn.post(raw, out, s.get('finish'), None, None, None, None, None)
secs = [json.load(open(os.path.join(wd, f'strip{i}.png.done')))['seconds'] for i in range(ntop)]
rep = json.load(open(os.path.join(wd, 'strip0.report.json')))
crep = crop[:-4] + '.report.json'
csec = json.load(open(crep)).get('seconds', {}) if os.path.exists(crep) else {}
rep.update({'shot': shot, 'image': out, 'size': [W, H], 'strips': ntop, 'strip_seconds': secs, 'crop': {'rows': [ctop, H], 'seconds': csec},
            'finish': pr.get('finish'), 'note': f'the top {ntop} strips rendered by haze_b_strips (no rubble in them), the rest in one crop in a '
            'single process (the rubble is one build), feathered across their shared rows and finished once'})
rep.pop('parts_2d', None)
open(out[:-4] + '.report.json', 'w').write(json.dumps(rep, indent=1, default=str) + '\n')
json.dump(s, open(out[:-4] + '.shot.json', 'w'), indent=1)
print(out, 'top strips', ntop, 'crop rows', ctop, H)
