"""The Core base in C: L*, C*, hue at its centre and both flanks (boxes in the 1600 x 2000 frame's pixels)."""
import sys, numpy as np
from PIL import Image
def lab(a):
    a=a/255; lin=np.where(a<=0.04045,a/12.92,((a+0.055)/1.055)**2.4)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    X=lin@M.T/np.array([0.95047,1,1.08883]); f=np.where(X>216/24389,np.cbrt(X),(24389/27*X+16)/116)
    A=500*(f[...,0]-f[...,1]); B=200*(f[...,1]-f[...,2]); return 116*f[...,1]-16, np.hypot(A,B), np.degrees(np.arctan2(B,A))
BOX={'left flank':(565,600),'centre':(690,750),'right flank':(840,875)}
for p in sys.argv[1:]:
    L,C,h=lab(np.asarray(Image.open(p).convert('RGB')).astype(float))
    print(p.split('/')[-1], '  '.join(f'{n}: {L[1320:1380,x0:x1].mean():.1f} / {C[1320:1380,x0:x1].mean():.1f} / h {h[1320:1380,x0:x1].mean():.0f}' for n,(x0,x1) in BOX.items()))
