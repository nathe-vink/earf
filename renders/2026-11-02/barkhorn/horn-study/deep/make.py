"""Horn-study shots: front-off-tall of a tint with option a (Strata), b (horn-soft), c (the formed horn), d (horn-flat),
the horn-lot deep given as a hex or as `f` x the stock 1/2 in sheet's absorbance (f 1: the stock sheet)."""
import json, math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
srgb = lambda x: 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
T = {'ice': 'cloud-blue', 'ember': 'cloud-red'}
TR = json.load(open('spinoffs/barkhorn/asset/tints-trucast.json'))
STOCK = {e['flavour']: e['strata_horn_deep'] for e in TR.values()}
def scaled(hexc, f):
    return '#' + ''.join(f'{round(255 * srgb(math.exp(f * math.log(max(1e-5, lin(int(hexc[i:i + 2], 16) / 255)))))):02X}' for i in (1, 3, 5))
DEFS = {'v': 'studio/products/barkhorn-variants.json', 'c': 'studio/products/barkhorn-cloud.json', 's': 'studio/products/barkhorn-horn-study.json'}
def make(tag, tint, opt, deep=None, f=None, scale=None):
    fl = T[tint]
    if f is not None:
        deep = scaled(STOCK[fl], f)
    s = json.load(open(f'spinoffs/barkhorn/campaign/shots/site-{os.environ.get("FRAME", "front-off-tall")}-{tint}.json'))
    paths = {}
    for k, p in DEFS.items():
        d = json.load(open(p))
        if k == 'c' and opt in ('e', 'f'):        # e: c with the pod and its cap in black stock cast sheet, the pads and saddle turned bronze
            d['materials']['pod-black'] = {'preset': 'plastic', 'color': '#0C0C0D', 'roughness': 0.12}
            for a in d['assign']:
                if a['material'] == 'horn-lot':
                    a['match'] = 'waveguide' if opt == 'f' else 'waveguide|horn-throat'
            d['assign'] = [{'match': 'horn-pod|waveguide-cap' + ('|horn-throat' if opt == 'f' else ''), 'material': 'pod-black'},
                           {'match': 'horn-pads|horn-saddle', 'material': 'brass'}] + d['assign']
        if deep:
            d['flavours'][fl]['materials']['horn-lot'] = {**d['flavours'][fl]['materials']['horn-lot'], 'deep': deep}
        q = f'{HERE}/def-{tag}-{k}.json'; json.dump(d, open(q, 'w')); paths[p] = q
    blocks = s['products']
    inst0 = json.loads(json.dumps(blocks[1]['instances'][0]))
    for b in blocks:
        i = b['instances'][0]
        if b['def'].endswith('barkhorn-cloud.json') and opt in ('c', 'e', 'f'):
            i['hide'] = [h for h in i['hide'] if h not in ('waveguide', 'horn-throat')]
            if opt == 'f':                 # Strata's build runs the HF lead and the tie rod inside its rear bronze posts
                i['hide'] = i['hide'] + ['lead-hf', 'tie-rod*']
        if b['def'].endswith('barkhorn-variants.json') and opt != 'a':
            i['hide'] = i['hide'] + ['horn-strata']
    if opt in ('b', 'd'):
        i = {k: v for k, v in inst0.items() if k != 'options'}
        i['hide'] = ['horn-flat'] if opt == 'b' else ['horn-soft']
        blocks.append({'def': DEFS['s'], 'flavour': fl, 'instances': [i]})
    for b in blocks:
        b['def'] = paths[b['def']]
    s['title'] = f'Tropos horn study: option {opt}, {tint}, horn {deep or "as the model"}'
    json.dump(s, open(f'{HERE}/shot-{tag}.json', 'w'), indent=1)
    print(tag, tint, opt, deep)
for a in sys.argv[1:]:
    tag, tint, opt, v = a.split(':')
    if v == '-':
        make(tag, tint, opt)
    elif v.startswith('#'):
        make(tag, tint, opt, deep=v)
    else:
        make(tag, tint, opt, f=float(v))
