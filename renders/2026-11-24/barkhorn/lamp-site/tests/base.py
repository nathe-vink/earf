"""The Core base and floor meter (the lamps lane, 2026-11-21): the base box x 520-1110, y 1530-1740 (full-scale px), the
floor at the left (x 0-400, y 1450-1700) and front (y 1800-2000); median RGB and L*/C*."""
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/meter'); from labf import lab
for f in sys.argv[1:]:
    a=np.asarray(Image.open(f).convert('RGB'),float); H,W=a.shape[:2]; k=W/1600
    def box(x0,x1,y0,y1): return a[int(y0*k):int(y1*k), int(x0*k):int(x1*k)]
    b=box(520,1110,1530,1740); L,A,B=lab(b); C=np.hypot(A,B)
    med=lambda q: np.median(q.reshape(-1,3),0).round(1)
    Lf=lab(box(0,400,1450,1700))[0]; Lr=lab(box(0,1600,1800,2000))[0]; bot=box(0,1600,1960,2000)
    print(f.split('/')[-1].ljust(28),'base RGB',med(b),'L*',round(float(np.median(L)),1),'C*',round(float(np.median(C)),1),
          '| floor left',round(float(np.median(Lf)),1),'front',round(float(np.median(Lr)),1),'| bottom rows max',bot.max(axis=(0,1)))
