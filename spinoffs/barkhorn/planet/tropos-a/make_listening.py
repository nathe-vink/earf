"""The bar's listening zone again with Tropos as the owner set it on 2026-11-03: base A (its own feet, no plinth, no light)
and horn A polished. The coordinator, 15:25 UTC: re-render bar-listening.jpg from planet38 finals-b/listening-smoke,
with the pair on its own feet, the four lamps aimed up under the pairs and their pedestals gone, the room's own lights
kept.

    python3 spinoffs/barkhorn/planet/tropos-a/make_listening.py      # writes studio/shots/barkhorn/planet-tropos-a/listening-smoke.json

The source shot is read from git (e7149388, r33-planet-world), so this always starts from the frame the brand book used.
Tropos is two models, as on r33-speaker-horn at 5295e58 (spinoffs/barkhorn/campaign/rollout/HELPERS.md builds them): the
cabinet (studio/products/barkhorn-cloud.json) and its variant parts (barkhorn-variants.json, horn A and the bases), shown
as base A by hiding the other horns and fitting no option. The horn's outside polished is `horn-satin` at roughness 0.05
(rollout.py's `--horn polished`); the base's uplight parts are off (glow 0).
"""
import copy, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path[:0] = [os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', d) for d in ('r37', 'r36')]
import r37_plan as R                                                   # noqa: E402

SRC = ('e7149388', 'renders/2026-10-20/barkhorn/planet38/finals-b/listening-smoke.shot.json')
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet-tropos-a', 'listening-smoke.json')
CLOUD, VARIANTS = 'studio/products/barkhorn-cloud.json', 'studio/products/barkhorn-variants.json'
HIDE_CLOUD = ['cloth-disc', 'post-*', 'post-sleeves', 'post-sockets', 'woofer-ring']     # as gate 2's A frames
HIDE_VARIANTS = ['horn-topo*', 'base-out*', 'horn-strata']                               # horn A only; no option fitted
FEET_ZONE = R.ZONE['z']                                               # the listening pair on the zone's floor
FEET_BAR = round(R.SPK_LEDGE['top'] + R.SPK_NICHE['floor'], 4)        # the bar pair on its niche's floor, level
GONE = ('plinthl0', 'plinthl1', 'plinthb0', 'plinthb1')               # the lamps aimed up under the pairs


def tropos(instances, flavour):
    return [{'def': CLOUD, 'flavour': flavour, 'instances': [{**i, 'hide': HIDE_CLOUD} for i in instances]},
            {'def': VARIANTS, 'flavour': flavour, 'instances': [{**i, 'hide': HIDE_VARIANTS, 'options': []} for i in instances]}]


def shot():
    s = json.loads(subprocess.run(['git', 'show', f'{SRC[0]}:{SRC[1]}'], capture_output=True, check=True, cwd=ROOT).stdout)
    s = copy.deepcopy(s)
    s['title'] = 'Planet EARF, the listening zone (Smoke): Tropos on its own feet, horn A polished (2026-11-03)'
    products = []
    for p in s['products']:
        if 'barkhorn-cloud' not in p['def']:
            products.append(p)
            continue
        inst = []
        for i in p['instances']:
            x, y, z = i['position']
            z = FEET_ZONE if z < 0.8 else FEET_BAR                    # the altar pair and the back bar's pair
            inst.append({'position': [x, y, z], 'rotate_z': i['rotate_z']})   # level: no tilt without the wedge
        products += tropos(inst, p['flavour'])
    s['products'] = products
    for k in GONE:
        s['lights'].pop(k)
    # the pair's back kicks (speaker-only lamps behind each cabinet, 0.29 m above its old base): kept as back light, but
    # moved up to the cabinet's middle and aimed level, so nothing rises from below now that the cabinet stands lower
    for k in ('spkb0', 'spkb1'):
        L = s['lights'][k]
        zc = FEET_ZONE + 0.65
        L['position'][2] = zc; L['target'][2] = zc
    s['materials'] = {**s.get('materials', {}), 'horn-satin': {'roughness': 0.05},
                      'uplight-edge': {'glow': 0.0}, 'uplight-panel': {'glow': 0.0},   # option parts, unfitted: off twice over
                      'uplight-wash': {'glow': 0.0}, 'led': {'glow': 0.0}, 'builtin-led': {'glow': 0.0},
                      'builtin-led-brace': {'glow': 0.0}}
    room = s['set']['props'][0]
    room['tropos_feet'] = True                                        # no altar plinths, no lit tops, no lit wedges
    room['plinth_bar'] = 0.0; room['plinth_listen'] = 0.0
    return s


if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(shot(), open(OUT, 'w'), indent=1)
    print(OUT)
