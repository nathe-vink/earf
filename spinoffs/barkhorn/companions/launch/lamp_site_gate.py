import sys, math, glob, os
from PIL import Image
def lin(c): c/=255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def oklab(p):
    r,g,b=(lin(x) for x in p)
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b; m=0.2119034982*r+0.6806995451*g+0.1073969566*b; s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l,m,s=[x**(1/3) for x in (l,m,s)]
    return (0.2104542553*l+0.7936177850*m-0.0040720468*s, 1.9779984951*l-2.4285922050*m+0.4505937099*s, 0.0259040371*l+0.7827717662*m-0.8086757660*s)
GATE={'red':('Ember',25,32,0.15),'orange':('Dust',40,55,None),'amber':('Acid',70,95,None),'green':('Poison',135,160,0.08),
      'blue':('Ice',200,235,0.09),'violet':('Haze',295,325,0.09),'ice':('Fog',None,None,-0.04),'black':('Smoke',None,None,-0.04)}
FACE={'dome':(0.40,0.25,0.60,0.33),'orb':(0.38,0.40,0.62,0.60)}; PAPER={'dome':(0.05,0.40,0.25,0.60),'orb':(0.05,0.15,0.25,0.35)}
def region(im, box):
    w,h=im.size; return list(im.crop(tuple(int(a*b) for a,b in zip(box,(w,h,w,h)))).getdata())
def stats(px):
    # drop the brightest 3 % as speculars
    px=sorted(px, key=lambda p: sum(p))[:int(len(px)*0.97)]
    labs=[oklab(p) for p in px]; n=len(labs)
    L=sum(x[0] for x in labs)/n; a=sum(x[1] for x in labs)/n; b=sum(x[2] for x in labs)/n
    clip=sum(1 for p in px if max(p)>=255)/n
    return L,a,b,math.hypot(a,b),math.degrees(math.atan2(b,a))%360,clip
kind=sys.argv[1]; d=sys.argv[2]
res={}
for c in ['red','orange','amber','green','blue','violet','ice','black']:
    f=os.path.join(d,f'{kind}-{c}.png')
    if not os.path.exists(f): continue
    im=Image.open(f).convert('RGB')
    L,a,b,C,h,clip=stats(region(im,FACE[kind])); Lp=stats(region(im,PAPER[kind]))[0]
    res[c]=(L,a,b)
    nm,h0,h1,cmin=GATE[c]; ok=[]
    if h0 is not None: ok.append(('h', h0<=h<=h1))
    if cmin is not None: ok.append(('C', C>=cmin if cmin>0 else C<=-cmin))
    ok.append(('clip0', clip==0)); ok.append(('face>paper', L>Lp))
    print(f'{kind}-{c:6s} {nm:6s} L {L:.3f} paper {Lp:.3f} C {C:.3f} h {h:5.1f} clip {clip:.3f}  ' + ' '.join(f"{k}:{'PASS' if v else 'FAIL'}" for k,v in ok))
order=[c for c in ['red','orange','amber','green','blue','violet','ice','black'] if c in res]
for x,y in zip(order,order[1:]):
    dE=math.dist(res[x],res[y]); print(f'  dE {x}-{y} {dE:.3f} {"PASS" if dE>=0.08 else "FAIL"}')
