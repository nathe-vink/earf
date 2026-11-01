import json, sys
from PIL import Image
def lin(c):
    c=c/255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def L(p): r,g,b=p[:3]; return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
spec=json.load(open(sys.argv[1])); A=Image.open(sys.argv[2]).convert('RGB'); B=Image.open(sys.argv[3]).convert('RGB')
blocks=[('header',(spec['header']['x'],spec['header']['y'],spec['header']['x']+spec['header']['w'],spec['header']['y']+spec['header'].get('h',150)))]
for c in spec['callouts']:
    l=c['label']; blocks.append((c['id'],(l['x']-4,l['y']-4,l['x']+l['w']+4,l['y']+l.get('h',112)+4)))
f=spec.get('foot'); 
if f: blocks.append(('foot',(f['x'],f['y']-4,f['x']+f['w'],f['y']+26)))
worst=99
for name,(x0,y0,x1,y1) in blocks:
    glyph=[]
    for y in range(max(0,int(y0)),min(1080,int(y1))):
        for x in range(max(0,int(x0)),min(1920,int(x1))):
            la=L(A.getpixel((x,y))); lb=L(B.getpixel((x,y)))
            if abs(la-lb)>0.08: glyph.append((la,lb))
    if not glyph: print(name,'no glyphs'); continue
    glyph.sort(key=lambda t:-abs(t[0]-t[1]))
    core=glyph[:max(1,len(glyph)//3)]
    light = sum(1 for la,lb in core if la>lb) > len(core)/2
    inks=sorted(la for la,lb in core); bgs=sorted(lb for la,lb in core)
    if light:
        ink=inks[len(inks)//2]; bg=bgs[int(len(bgs)*0.95)-1]; cr=(ink+0.05)/(bg+0.05)
    else:
        ink=inks[len(inks)//2]; bg=bgs[int(len(bgs)*0.05)]; cr=(bg+0.05)/(ink+0.05)
    worst=min(worst,cr)
    print(f"{name:11s} {'light' if light else 'dark '} effective {cr:4.1f}:1  (ink L {ink:.3f}, bg L under glyphs {bg:.3f}, n={len(core)})" + ('' if cr>=4.5 else '  <-- below 4.5'))
print(f'worst effective {worst:.1f}:1')
