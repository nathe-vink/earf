"""Proof 2 of A, measured by part: the engine's part masks (a-*.mask.png) pick each part's visible pixels; CIELAB L* and C* (D65).
Each cell: L*, C*, pixels (the throat: L* p95, its eye)."""
import json,numpy as np,sys
from PIL import Image
def lab(a):
    a=a/255; lin=np.where(a<=0.04045,a/12.92,((a+0.055)/1.055)**2.4)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    X=lin@M.T/np.array([0.95047,1,1.08883]); f=np.where(X>216/24389,np.cbrt(X),(24389/27*X+16)/116)
    return 116*f[...,1]-16, np.hypot(500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2]))
rows={}
for v in ['a-p15','a-p125','a-p115s']:
    m={int(k):n for k,n in json.load(open(v+'.mask.json')).items()}
    ids=np.asarray(Image.open(v+'.mask.png').convert('RGB'))[...,0].astype(int)
    L,C=lab(np.asarray(Image.open(v+'.png').convert('RGB')).astype(float))
    H,W=ids.shape; X=np.arange(W)[None,:].repeat(H,0); Y=np.arange(H)[:,None].repeat(W,1)
    def part(name): 
        ks=[k for k,n in m.items() if n==name]; return np.isin(ids,ks)
    out={}
    # speaker halves by the cabinet's own columns
    for side,sel in (('L',X<480),('R',X>=480)):
        sel=sel&(X>150)&(X<820)
        t=part('top')&sel; out['top '+side]=(L[t].mean(),C[t].mean(),t.sum())
        th=part('horn-throat')&sel; out['throat p95 '+side]=(np.percentile(L[th],95),C[th].mean(),th.sum())
        hp=part('hf-plug')&sel; out['plug '+side]=(L[hp].mean(),L[hp].max(),hp.sum())
        cn=part('woofer-cone')&sel; out['cone '+side]=(L[cn].mean(),C[cn].mean(),cn.sum())
        fp=part('front-panel')&sel
        wy=Y[(part('woofer-frame')|part('woofer-surround'))&sel]
        above=fp&(Y<wy.min()); below=fp&(Y>wy.max())
        out['front above woofer '+side]=(L[above].mean(),C[above].mean(),above.sum())
        out['front below woofer (ports) '+side]=(L[below].mean(),C[below].mean(),below.sum())
    room=ids==0
    w=room&(Y>60)&(Y<240)&(X>600)&(X<640); out['wall']=(L[w].mean(),C[w].mean(),w.sum())
    fl=room&(Y>500)&(Y<520)&(X>330)&(X<620); out['floor before console']=(L[fl].mean(),C[fl].mean(),fl.sum())
    rows[v]=out
for k in rows['a-p15']:
    print(f'{k:34s}', ' | '.join(f'{rows[v][k][0]:6.1f} {rows[v][k][1]:6.1f} n{rows[v][k][2]}' for v in rows))
