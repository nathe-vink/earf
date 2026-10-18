"""Haze B's finals, resumable: the container restarted twice under a two-hour render, so a final renders in horizontal
strips (the finish off), skipping strips already rendered, and the raw strips are stitched (the overlaps aligned and
feathered) and the shot's finish applied once over the whole frame.

    python3 spinoffs/barkhorn/elements/haze_b_strips.py render SHOT WORKDIR [--n 8 --samples 512]
    python3.11 spinoffs/barkhorn/elements/haze_b_strips.py stitch SHOT WORKDIR OUT.png   (the finish needs scipy)
"""
import json, os, subprocess, sys, time
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OV = 32


def bands(H, n):
    h = H // n
    out = []
    for i in range(n):
        a, b = i * h, (H if i == n - 1 else (i + 1) * h)
        out.append((a, b, max(0, a - OV), min(H, b + OV)))
    return out


def render(shot, wd, n=8, samples=512):
    os.makedirs(wd, exist_ok=True)
    s = json.load(open(shot))
    W, H = s['size']
    raw = dict(s); raw['finish'] = dict(s.get('finish') or {}); raw['finish']['enabled'] = False
    rshot = os.path.join(wd, 'raw.shot.json'); json.dump(raw, open(rshot, 'w'))
    for i, (a, b, ra, rb) in enumerate(bands(H, n)):
        png = os.path.join(wd, f'strip{i}.png')
        if os.path.exists(png + '.done'):
            continue
        t = time.time()
        r = subprocess.run([sys.executable, os.path.join(ROOT, 'studio/engine/render.py'), rshot, '--out', png,
                            '--samples', str(samples), '--crop', '0', str(ra / H), '1', str(rb / H)],
                           cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
        open(png + '.done', 'w').write(json.dumps({'seconds': round(time.time() - t, 1), 'rows': [ra, rb]}))
        print(f'strip {i} rows {ra}-{rb}: {time.time() - t:.0f} s', flush=True)


def stitch(shot, wd, out):
    s = json.load(open(shot))
    W, H = s['size']
    n = len([f for f in os.listdir(wd) if f.startswith('strip') and f.endswith('.png')])
    acc = np.zeros((H, W, 3)); wsum = np.zeros((H, 1, 1))
    prev = None
    for i, (a, b, ra, rb) in enumerate(bands(H, n)):
        im = np.asarray(Image.open(os.path.join(wd, f'strip{i}.png')).convert('RGB')).astype(np.float64)
        h = im.shape[0]
        top = ra
        if h != rb - ra:                       # Blender rounds the border; find the strip's true top by its overlap
            best = None
            for d in range(-3, 4):
                t = ra + d
                if t < 0 or t + h > H or prev is None:
                    continue
                pa, pi = prev
                lo, hi = max(t, pa), min(t + h, pa + pi.shape[0])
                if hi - lo < 8:
                    continue
                e = np.mean((im[lo - t:hi - t] - pi[lo - pa:hi - pa]) ** 2)
                best = (e, t) if best is None or e < best[0] else best
            top = best[1] if best else (H - h if i == n - 1 else ra)
        w = np.ones(h)
        for k in range(h):                     # feather over the overlaps
            y = top + k
            if y < a:
                w[k] = (y - (a - OV) + 0.5) / (2 * OV)
            elif y >= b and i < n - 1:
                w[k] = 1 - (y - (b - OV) + 0.5) / (2 * OV)
        w = np.clip(w, 0.0, 1.0)
        acc[top:top + h] += im * w[:, None, None]; wsum[top:top + h] += w[:, None, None]
        prev = (top, im)
    img = (acc / np.maximum(wsum, 1e-6)).clip(0, 255).round().astype(np.uint8)
    raw = out[:-4] + '.raw.png'
    Image.fromarray(img).save(raw)
    sys.path.insert(0, os.path.join(ROOT, 'studio/engine'))
    import finish as Fn
    pr = Fn.post(raw, out, s.get('finish'), None, None, None, None, None)
    secs = [json.load(open(os.path.join(wd, f'strip{i}.png.done')))['seconds'] for i in range(n)]
    rep = json.load(open(os.path.join(wd, 'strip0.report.json')))
    rep.update({'shot': shot, 'image': out, 'size': [W, H], 'strips': n, 'strip_seconds': secs,
                'seconds': {'render_total': round(sum(secs), 1)}, 'finish': pr.get('finish'),
                'note': 'rendered in horizontal strips (resumable across container restarts), stitched raw, finished once'})
    rep.pop('parts_2d', None)
    open(out[:-4] + '.report.json', 'w').write(json.dumps(rep, indent=1, default=str) + '\n')
    json.dump(s, open(out[:-4] + '.shot.json', 'w'), indent=1)
    print(out, sum(secs))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'render':
        args = sys.argv[2:]
        n = int(args[args.index('--n') + 1]) if '--n' in args else 8
        sm = int(args[args.index('--samples') + 1]) if '--samples' in args else 512
        render(args[0], args[1], n, sm)
    else:
        stitch(*sys.argv[2:5])
