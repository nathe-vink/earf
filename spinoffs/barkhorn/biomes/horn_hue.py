"""Horn against cabinet: each tint's transmitted colour (white light, OKLCH) through two cabinet walls (40 mm, the view
through the box) and one horn sheet (12.7 mm), from the Strata asset's own absorption (r48-biomes, 2026-11-04).

    python3.11 spinoffs/barkhorn/biomes/horn_hue.py
"""
bpy.ops.wm.open_mainfile(filepath='spinoffs/barkhorn/biomes/assets/hornA3/tropos-strata.blend')
def oklch(rgb_lin):
    r,g,b=rgb_lin
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b; m=0.2119034982*r+0.6806995451*g+0.1073969566*b; s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l,m,s=[x**(1/3) for x in (l,m,s)]
    L=0.2104542553*l+0.7936177850*m-0.0040720468*s; a=1.9779984951*l-2.4285922050*m+0.4505937099*s; bb=0.0259040371*l+0.7827717662*m-0.8086757660*s
    return L, math.hypot(a,bb), math.degrees(math.atan2(bb,a))%360
def trans(m,t):
    n=[x for x in m.node_tree.nodes if x.type=='VOLUME_ABSORPTION'][0]; c=n.inputs['Color'].default_value; D=n.inputs['Density'].default_value
    return [math.exp(-(1-c[i])*D*t) for i in range(3)]
for tint in ('Haze','Ice','Dust','Ember','Poison','Acid'):
    col=bpy.data.collections['Tropos Strata '+tint]
    mats={sl.material.name.split('@')[0]:sl.material for o in col.all_objects for sl in o.material_slots if sl.material}
    cab=trans(mats['bark'],0.040); horn=trans(mats['horn-satin'],0.0127)
    cl,cc,ch=oklch(cab); hl,hc,hh=oklch(horn)
    Y=lambda t:0.2126*t[0]+0.7152*t[1]+0.0722*t[2]
    print(f'{tint:7s} cabinet 40mm  OKLCH L {cl:.3f} C {cc:.3f} h {ch:5.1f}  Y {Y(cab):.3f} | horn 12.7mm L {hl:.3f} C {hc:.3f} h {hh:5.1f}  Y {Y(horn):.3f} | dh {((hh-ch+180)%360)-180:+.1f}  horn/cab Y {Y(horn)/Y(cab):.2f}  C {hc/cc:.2f}')
