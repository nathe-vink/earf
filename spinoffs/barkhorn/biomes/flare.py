"""Crease contrast on a polished horn: L* p5-p95 on the flare clear of the driver (box per frame, full-res coords)."""
import sys; from PIL import Image, ImageDraw; import numpy as np
def Lstar(a):
    c=a/255; lin=np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4); Y=(lin*[0.2126,0.7152,0.0722]).sum(-1)
    f=np.where(Y>0.008856,np.cbrt(Y),7.787*Y+16/116); return 116*f-16
def span(path, box, out=None):
    im=Image.open(path).convert('RGB'); a=np.asarray(im).astype(float); x0,y0,x1,y1=box
    L=Lstar(a[y0:y1,x0:x1]); v=float(np.percentile(L,95)-np.percentile(L,5))
    if out:
        c=im.crop((x0-120,y0-80,x1+120,y1+80)); d=ImageDraw.Draw(c); d.rectangle((120,80,120+x1-x0,80+y1-y0),outline='yellow',width=3); c.save(out)
    return round(v,1)
if __name__=='__main__':
    print(span(sys.argv[1], tuple(int(x) for x in sys.argv[2:6]), sys.argv[6] if len(sys.argv)>6 else None))
