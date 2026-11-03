import json,sys
d=json.load(sys.stdin)
SUS=('specular','diffuse','receivers','transmission','camera','glossy','visible','keep','scope','only','link','blocks','shadow','volume','lights','see_through')
def lamps(o,path=''):
    # find dicts that look like lamps (have irradiance/power/strength) or flags/cards
    if isinstance(o,dict):
        keys=set(o.keys())
        if keys & {'irradiance','power_w','strength','watts','emit'} or o.get('type') in ('area','spot','point','sun','flag','card','panel','net','glint'):
            flagged={k:v for k,v in o.items() if any(s in k.lower() for s in SUS)}
            core={k:o[k] for k in ('type','irradiance','power_w','strength','spread_deg','size_m','size') if k in o}
            print(path, core, 'FLAGS:' if flagged else '', flagged if flagged else '')
        for k,v in o.items(): lamps(v,path+'.'+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): lamps(v,path+'[%d]'%i)
lamps(d)
# rulings 2-4 checks beyond the lamp list
s=d.get('set') or {}
if s.get('cast_shadow') is False:
    print('RULING (set shadows): set.cast_shadow is False -> the set lets light through (sun:', json.dumps(d.get('sun')), ')')
for n,L in (d.get('lights') or {}).items():
    if isinstance(L,dict):
        if L.get('type')=='flag' and (L.get('lights') or L.get('see_through')):
            print('RULING 2 (scoped flag):', n, {k:L.get(k) for k in ('lights','see_through')})
        if L.get('diffuse',1.0)==0.0 and L.get('receivers'):
            print('RULING 2 (linked spec-only lamp):', n, L.get('receivers'))
        if L.get('transmission') is False:
            print('RULING 3 (hidden through resin):', n)
for fl in (s.get('flags') or []):
    if isinstance(fl,dict) and fl.get('reflect_only'):
        print('CHECK (reflect-only card, must be out of frame):', fl.get('center_m'), fl.get('size_m'))
