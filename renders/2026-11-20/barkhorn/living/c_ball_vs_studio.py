"""The Core's ball and base in the room's C and the lamps lane's studio Core OFF (house7): L*/C*/hue medians."""
import sys, numpy as np
from PIL import Image
def lab(a):
    a=a/255; lin=np.where(a<=0.04045,a/12.92,((a+0.055)/1.055)**2.4)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    X=lin@M.T/np.array([0.95047,1,1.08883]); f=np.where(X>216/24389,np.cbrt(X),(24389/27*X+16)/116)
    A=500*(f[...,0]-f[...,1]); B=200*(f[...,1]-f[...,2]); return 116*f[...,1]-16, np.hypot(A,B), np.degrees(np.arctan2(B,A))
def disc(H,W,cx,cy,r):
    Y,X=np.ogrid[:H,:W]; return (X-cx)**2+(Y-cy)**2<=r*r
def rep(name, path, ball, base_c, base_l, base_r, lower):
    L,C,h=lab(np.asarray(Image.open(path).convert('RGB')).astype(float)); H,W=L.shape
    m=disc(H,W,*ball)
    def med(sel): return f'{np.median(L[sel]):5.1f} / {np.median(C[sel]):5.1f} / {np.median(h[sel]):3.0f}'
    box=lambda b: (slice(b[1],b[3]),slice(b[0],b[2]))
    print(f'{name:10s} ball disc {med(m)} | ball lower {med(box(lower))} | base centre {med(box(base_c))} | flanks {med(box(base_l))}  {med(box(base_r))}')
rep('room C', 'living-c-ember.png', (720,1110,170), (690,1320,750,1380), (565,1320,600,1380), (840,1320,875,1380), (660,1160,780,1230))
rep('studio', 'studio-core-off.png', (822,1045,400), (760,1500,880,1580), (505,1500,545,1560), (1095,1500,1135,1560), (700,1180,940,1320))
