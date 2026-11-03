"""Re-dress a rendered Planet EARF shot with Tropos as the owner set it on 2026-11-03: base A (its own feet: no plinth, no
light from under or inside), horn A polished. The coordinator, 15:58 UTC: the House Book's and the brand book's pictures
that are not in Smoke, a proxy then a final each, the room's own lights kept.

    python3 spinoffs/barkhorn/planet/tropos-a/retropos.py SRC.shot.json OUT.json [--floor Z] [--title TEXT]

- Every `barkhorn-cloud` product becomes the cabinet plus its variant parts, as gate 2's A frames on r33-speaker-horn
  (5295e58): the other horns hidden, no option fitted (make_listening.py's `tropos`).
- Each cabinet is set down on the floor (`--floor`, default 0.0) and levelled (no tilt).
- Lamps named plinth* or uplight* go; the room prop gets `tropos_feet` (its kit then draws no plinth, lit top or wedge)
  and any plinth glow set to 0.
- The horn's outside polished (`horn-satin` at roughness 0.05); every LED and uplight material of the variant parts at
  glow 0 (they are unfitted options in any case).
"""
import argparse, copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_listening import tropos                                     # noqa: E402

GLOW_OFF = ('uplight-edge', 'uplight-panel', 'uplight-wash', 'led', 'builtin-led', 'builtin-led-brace')


def convert(s, floor=0.0, title=None):
    s = copy.deepcopy(s)
    products = []
    for p in s['products']:
        if 'barkhorn-cloud' not in p['def']:
            products.append(p)
            continue
        inst = [{'position': [i['position'][0], i['position'][1], floor], 'rotate_z': i.get('rotate_z', 0.0)}
                for i in p['instances']]
        products += tropos(inst, p.get('flavour'))
    s['products'] = products
    gone = [k for k in s.get('lights', {}) if k.startswith(('plinth', 'uplight'))]
    for k in gone:
        s['lights'].pop(k)
    mats = dict(s.get('materials', {}))
    mats['horn-satin'] = {**mats.get('horn-satin', {}), 'roughness': 0.05}
    for m in GLOW_OFF:
        mats[m] = {**mats.get(m, {}), 'glow': 0.0}
    s['materials'] = mats
    for pr in s['set']['props']:
        if pr.get('fn') in ('room', 'house', 'popup'):
            pr['tropos_feet'] = True
            for k in list(pr):
                if k.startswith('plinth') and isinstance(pr[k], (int, float)):
                    pr[k] = 0.0
    if title:
        s['title'] = title
    return s, gone


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--floor', type=float, default=0.0)
    ap.add_argument('--title')
    a = ap.parse_args()
    s, gone = convert(json.load(open(a.src)), a.floor, a.title)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(s, open(a.out, 'w'), indent=1)
    print(a.out, 'lamps removed:', gone or 'none')
