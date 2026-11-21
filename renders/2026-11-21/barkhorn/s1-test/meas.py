"""S1: the tallr7 fronts a / b / c, measured by part (the engine's masks, first hit: the batts are read through the
right side panel) and in six ground patches. L* / C* means.  python3 meas.py ember-a ember-b ..."""
import json, sys, numpy as np
from PIL import Image
def lab(a):
    a=a/255; lin=np.where(a<=0.04045,a/12.92,((a+0.055)/1.055)**2.4)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    X=lin@M.T/np.array([0.95047,1,1.08883]); f=np.where(X>216/24389,np.cbrt(X),(24389/27*X+16)/116)
    return 116*f[...,1]-16, np.hypot(500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2]))
GROUND = {'floor left of the foot': (150, 1080, 250, 1160), 'floor right of the foot': (740, 1030, 840, 1090),
          'floor in front': (380, 1160, 520, 1230), 'floor far left': (20, 1150, 120, 1240),
          'sweep, high left': (80, 80, 220, 200), 'sweep, right': (840, 380, 960, 520)}
def one(stem):
    m = {int(k): n for k, n in json.load(open(stem + '.mask.json')).items()}
    ids = np.asarray(Image.open(stem + '.mask.png').convert('RGB'))[..., 0].astype(int)
    L, C = lab(np.asarray(Image.open(stem + '.png').convert('RGB')).astype(float))
    H, W = ids.shape; Y = np.arange(H)[:, None].repeat(W, 1)
    part = lambda f: np.isin(ids, [k for k, n in m.items() if f(n)])
    out = {}
    rb = part(lambda n: n == 'right')
    ym = np.median(Y[rb]); up, lo = rb & (Y < ym), rb & (Y >= ym)
    out['batts right, upper'] = (L[up].mean(), C[up].mean())
    out['batts right, lower'] = (L[lo].mean(), C[lo].mean())
    au = (slice(610, 880), slice(640, 700))                 # the audit's box (full size x 640-700, y 610-880)
    out["batts right, the audit's box"] = (L[au].mean(), C[au].mean())
    ab = (slice(505, 560), slice(330, 590))                 # the front above the woofer, under the top's edge
    out['front above the woofer'] = (L[ab].mean(), C[ab].mean())
    for nm, f in (('horn (waveguide)', lambda n: n == 'waveguide'), ('throat and pod', lambda n: n in ('horn-throat', 'horn-pod'))):
        s = part(f); out[nm] = (L[s].mean(), C[s].mean())
    for nm, (x0, y0, x1, y1) in GROUND.items():
        r = (slice(y0, y1), slice(x0, x1)); bg = ids[r] == 0
        out['ground: ' + nm] = (L[r][bg].mean(), C[r][bg].mean())
    return out
if __name__ == '__main__':
    stems = sys.argv[1:]; res = {s: one(s) for s in stems}
    print(f"| {'':30s} | " + ' | '.join(f'{s:>13s}' for s in stems) + ' |')
    for k in res[stems[0]]:
        print(f'| {k:30s} | ' + ' | '.join(f'{res[s][k][0]:5.1f} / {res[s][k][1]:5.1f}' for s in stems) + ' |')
