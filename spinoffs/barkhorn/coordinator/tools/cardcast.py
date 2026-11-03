"""Ray-cast a shot's frame against each reflect-only card's rectangle; print the share of the frame each would block.
usage: python3 cardcast.py shot.json [extra_cards.json]"""
import json, math, sys
def sub(a,b): return [a[i]-b[i] for i in range(3)]
def add(a,b): return [a[i]+b[i] for i in range(3)]
def mul(a,s): return [x*s for x in a]
def dot(a,b): return sum(a[i]*b[i] for i in range(3))
def cross(a,b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def norm(a): n=math.sqrt(dot(a,a)); return [x/n for x in a]
d=json.load(open(sys.argv[1])); cards=[f for f in (d.get('set',{}).get('flags') or []) if f.get('reflect_only')]
if len(sys.argv)>2: cards+=json.load(open(sys.argv[2]))
cam=d['camera']; W,H=d['size']
c=cam['position']; f=norm(sub(cam['target'],c)); r=norm(cross(f,[0,0,1])); u=cross(r,f)
lens=cam['lens_mm']; hx,hy=(18.0,18.0*H/W) if W>=H else (18.0*W/H,18.0)
sx=cam.get('shift_x',0.0); sy=cam.get('shift_y',0.0)
step=max(4,int(max(W,H)/240))
for fl in cards:
    C=fl['center_m']; S=fl['size_m']; n=norm(fl['normal'])
    a=norm(cross(n,[0,0,1])) if abs(n[2])<0.99 else [1.0,0.0,0.0]; b=cross(n,a)
    hit=tot=0; xs=[]; ys=[]
    for py in range(0,H,step):
        for px in range(0,W,step):
            tot+=1
            x=(px+0.5)/W*2-1 + sx*36.0/hx; y=1-(py+0.5)/H*2 + sy*36.0/hy   # Blender shift moves the frame by shift x 36 mm
            dv=norm(add(add(f, mul(r, x*hx/lens)), mul(u, y*hy/lens)))
            den=dot(dv,n)
            if abs(den)<1e-9: continue
            t=dot(sub(C,c),n)/den
            if t<=0: continue
            q=sub(add(c,mul(dv,t)),C)
            if abs(dot(q,a))<=S[0]/2 and abs(dot(q,b))<=S[1]/2:
                hit+=1; xs.append(px); ys.append(py)
    pct=100.0*hit/tot
    print(('IN FRAME ' if hit else 'out      ')+'%5.1f %%' % pct, 'centre', C, 'size', S, 'normal', fl['normal'], ('x %d-%d y %d-%d px' % (min(xs),max(xs),min(ys),max(ys))) if xs else '')
