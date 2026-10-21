"""Stitch horizontal pieces of a frame rendered at arbitrary row ranges (strips from haze_b_strips plus thinner
pieces rendered with render.py --crop), feathering across each whole overlap as haze_b_strips does, then apply the
shot's finish once.

    python3.11 spinoffs/barkhorn/elements/rowstitch.py SHOT OUT.png PIECE.png:TOP [PIECE.png:TOP ...]

TOP is the piece's nominal first row. Each piece is placed by matching its overlap with the piece above it
(+-3 rows), since Blender can round a crop's border by a row. Overlaps must be pairwise: no row may lie in three pieces.
"""
import json, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def main():
    shot, out, specs = sys.argv[1], sys.argv[2], sys.argv[3:]
    s = json.load(open(shot))
    W, H = s['size']
    pieces = []
    for sp in specs:
        p, top = sp.rsplit(':', 1)
        im = np.asarray(Image.open(p).convert('RGB')).astype(np.float64)
        assert im.shape[1] == W, (p, im.shape)
        pieces.append({'top': int(top), 'im': im, 'path': p})
    pieces.sort(key=lambda x: x['top'])
    for k, pc in enumerate(pieces):               # pass 1: place each piece against the one above it
        h = pc['im'].shape[0]
        if k:
            pv = pieces[k - 1]
            best = None
            for d in range(-3, 4):
                t = pc['top'] + d
                lo, hi = max(t, pv['top']), min(t + h, pv['top'] + pv['im'].shape[0])
                if t < 0 or t + h > H or hi - lo < 8:
                    continue
                e = np.mean((pc['im'][lo - t:hi - t] - pv['im'][lo - pv['top']:hi - pv['top']]) ** 2)
                best = (e, t) if best is None or e < best[0] else best
            if best and best[1] != pc['top']:
                print(f"{os.path.basename(pc['path'])}: placed at row {best[1]} (nominal {pc['top']})")
            if best:
                pc['top'] = best[1]
        pc['top'] = max(0, min(pc['top'], H - h))
    acc = np.zeros((H, W, 3)); wsum = np.zeros((H, 1, 1))
    for k, pc in enumerate(pieces):               # pass 2: complementary linear ramps across each overlap
        top, h = pc['top'], pc['im'].shape[0]
        w = np.ones(h)
        if k:
            up = pieces[k - 1]['top'] + pieces[k - 1]['im'].shape[0] - top
            if up > 0:
                w[:up] = np.minimum(w[:up], (np.arange(up) + 0.5) / up)
        if k + 1 < len(pieces):
            dn = top + h - pieces[k + 1]['top']
            if dn > 0:
                w[h - dn:] = np.minimum(w[h - dn:], 1 - (np.arange(dn) + 0.5) / dn)
            if k + 2 < len(pieces):
                assert pieces[k + 2]['top'] >= top + h, f"three pieces overlap at {os.path.basename(pc['path'])}"
        acc[top:top + h] += pc['im'] * w[:, None, None]; wsum[top:top + h] += w[:, None, None]
    ws = wsum[:, 0, 0]
    if (ws < 1e-6).any():
        g = np.where(ws < 1e-6)[0]
        sys.exit(f'rows with no piece: {g[:10]} ... ({len(g)} rows)')
    if np.abs(ws - 1).max() > 1e-6:
        print(f'note: weights not 1 in {(np.abs(ws - 1) > 1e-6).sum()} rows (max dev {np.abs(ws - 1).max():.3f}); normalised')
    img = (acc / wsum).clip(0, 255).round().astype(np.uint8)
    raw = out[:-4] + '.raw.png'
    Image.fromarray(img).save(raw)
    sys.path.insert(0, os.path.join(ROOT, 'studio/engine'))
    import finish as Fn
    pr = Fn.post(raw, out, s.get('finish'), None, None, None, None, None)
    rep = {'shot': shot, 'image': out, 'size': [W, H],
           'pieces': [[os.path.basename(pc['path']), pc['top'], pc['im'].shape[0]] for pc in pieces],
           'finish': pr.get('finish'),
           'note': 'rendered in horizontal pieces (strips, plus thinner pieces where the horizon is slowest), stitched raw with feathered overlaps, finished once'}
    open(out[:-4] + '.report.json', 'w').write(json.dumps(rep, indent=1, default=str) + '\n')
    json.dump(s, open(out[:-4] + '.shot.json', 'w'), indent=1)
    print(out)


if __name__ == '__main__':
    main()
