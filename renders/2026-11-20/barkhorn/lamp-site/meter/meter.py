"""meter.py MODE IMG... : the lamps lane's measures, rebuilt 2026-11-21 after the container restart.
corners: TL TR ML MR LL BR L*/a*/b* (patches 5 % in, 4 % from top/bottom, 6 % wide, mean; reproduces the old lab.py to 0.1)
base: Core's base (mask base.png): left/right low, bottom band, lip top, the coordinator's boxes cL/cR, centre, share below L* 20
share: the base's body share at 30/45/55/65 deg, row y 1650-1670 (full scale), half-width from the mask
body MASK: lower/middle third and whole L*/C* of a body's mask (ball.png, shade.png)
pair MASK: the LIT pair's two glow masks inside MASK (A: L*>18, C*>45, h 25-50; B: R>100 and L*>25),
  each median and p10/p90 L*; R>=250 in the frame and in MASK; floor patches (Core frames: left, right, front)
glow MASK: red-dominant pixels of a body's mask after a 3x3 median: median L*/C*, R>=250 share; walls TL/TR"""
import sys, os, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from labf import lab
MD = os.path.dirname(os.path.abspath(__file__))
def load(f, med=False):
    im = Image.open(f).convert('RGB')
    if med: im = im.filter(ImageFilter.MedianFilter(3))
    return np.asarray(im).astype(float)
def mask(name, H, W):
    return np.asarray(Image.open(os.path.join(MD, name)).convert('L').resize((W, H))) > 128
def LC(a):
    L, A, B = lab(a); return L, np.hypot(A, B)
def nm(f): return '/'.join(f.split('/')[-2:]).ljust(34)
mode = sys.argv[1]; args = sys.argv[2:]
if mode in ('body', 'glow', 'pair'): mk, args = args[0], args[1:]
for f in args:
    a = load(f, med=(mode == 'glow')); H, W = a.shape[:2]; L, C = LC(a); yy, xx = np.mgrid[:H, :W]
    if mode == 'corners':
        Lb = lab(a)
        def P(x, y):
            cy, cx = int(y * H), int(x * W); h, w = int(0.03 * H), int(0.03 * W)
            return '/'.join(f'{float(np.mean(c[cy - h:cy + h + 1, cx - w:cx + w + 1])):.1f}' for c in Lb)
        print(nm(f), ' '.join(f'{k} {P(x, y)}' for k, (x, y) in
              {'TL': (.05, .04), 'TR': (.95, .04), 'ML': (.05, .5), 'MR': (.95, .5), 'LL': (.05, .96), 'BR': (.95, .96)}.items()))
    elif mode == 'base':
        m = mask('base.png', H, W); ys, xs = np.nonzero(m); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); w, h = x1 - x0, y1 - y0; k = W / 1600
        reg = {'left low': m & (xx < x0 + .2 * w) & (yy > y0 + .5 * h), 'right low': m & (xx > x1 - .2 * w) & (yy > y0 + .5 * h),
               'bottom band': m & (yy > y1 - .12 * h), 'lip top': m & (yy < y0 + .12 * h),
               'cL': m & (xx >= 470 * k) & (xx <= 520 * k) & (yy >= 1630 * k) & (yy <= 1690 * k),
               'cR': m & (xx >= 1150 * k) & (xx <= 1200 * k) & (yy >= 1630 * k) & (yy <= 1690 * k),
               'centre': m & (abs(xx - (x0 + x1) / 2) < .15 * w) & (yy > y0 + .3 * h) & (yy < y1 - .15 * h)}
        print(nm(f), '  '.join(f'{r} {np.median(L[q]):.1f}/{np.median(C[q]):.1f}' for r, q in reg.items()), f' <L20 {100 * (L[m] < 20).mean():.1f}%')
    elif mode == 'share':
        c = a / 255.0; lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4); k = W / 1600
        m = mask('base.png', H, W); y0 = int(1650 * k); y1 = int(1670 * k) + 1
        xs_ = np.nonzero(m[y0])[0]; hw = (xs_.max() - xs_.min()) / 2; cx = (xs_.max() + xs_.min()) / 2
        row = lin[y0:y1].mean(0); cc = row[int(cx - 3 * k):int(cx + 3 * k) + 1].mean(0)
        sol = np.linalg.lstsq(np.stack([cc, np.ones(3)], 1), row.T, rcond=None)[0]
        ang = np.degrees(np.arcsin(np.clip((np.arange(W) - cx) / hw, -1, 1)))
        print(nm(f), 'body share L/R', '  '.join(f'{d}: {sol[0][(ang > -d - 2) & (ang < -d + 2)].mean():.2f}/{sol[0][(ang > d - 2) & (ang < d + 2)].mean():.2f}' for d in (30, 45, 55, 65)))
    elif mode == 'body':
        m = mask(mk, H, W); ys = np.nonzero(m)[0]; t0, t1 = ys.min(), ys.max(); hh = t1 - t0
        parts = {'lower third': m & (yy > t1 - hh / 3), 'middle third': m & (yy > t0 + hh / 3) & (yy <= t1 - hh / 3), 'whole': m}
        print(nm(f), '  '.join(f'{r} {np.median(L[q]):.1f}/{np.median(C[q]):.1f}' for r, q in parts.items()))
    elif mode == 'pair':
        L_, A_, B_ = lab(a); h_ = np.degrees(np.arctan2(B_, A_)) % 360; m = mask(mk, H, W); k = W / 1600
        mA = m & (L_ > 18) & (C > 45) & (h_ >= 25) & (h_ <= 50); mB = m & (a[..., 0] > 100) & (L_ > 25)
        q = lambda v: f'{np.median(v):.1f} ({np.percentile(v, 10):.1f}-{np.percentile(v, 90):.1f})'
        fl = {'left floor': (120, 420, 1480, 1700), 'right floor': (1250, 1500, 1480, 1700), 'front': (550, 1050, 1820, 1960)}
        fs = '  '.join(f'{n_} {np.median(L_[int(y0 * k):int(y1 * k), int(x0 * k):int(x1 * k)]):.1f}' for n_, (x0, x1, y0, y1) in fl.items())
        print(nm(f), f'A {q(L_[mA])} n{mA.sum()}  B {q(L_[mB])} n{mB.sum()}  R>=250 frame {(a[..., 0] >= 250).sum()} px, mask {100 * (a[m][:, 0] >= 250).mean():.2f}%  R=255 {(a[..., 0] >= 255).sum()} px  floors {fs}')
    elif mode == 'glow':
        m = mask(mk, H, W); px = a[m]; g = (px[:, 0] > 30) & (px[:, 0] > 2 * px[:, 1] + 10)
        Lg, Cg = LC(px[g][None]); a0 = load(f); L0 = lab(a0)[0]
        def P(x, y):
            cy, cx = int(y * H), int(x * W); h, w = int(0.03 * H), int(0.03 * W); return float(np.mean(L0[cy - h:cy + h + 1, cx - w:cx + w + 1]))
        print(nm(f), f'glow L {np.median(Lg):.1f} C {np.median(Cg):.1f} R>=250 {100 * (px[g][:, 0] >= 250).mean():.1f}%  walls TL {P(.05, .04):.1f} TR {P(.95, .04):.1f}')
