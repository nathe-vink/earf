"""The bar's Mantle back on the counter (2026-11-25, the owner via the coordinator: it hung off the back edge).

The asset's origin is the plinth's front-left corner, not its middle (mantle-strata.blend at fa0c3a65: the plinth spans
x 0.01-0.46 and y 0.01-0.37 from it, the feet x 0.137-0.333 and y 0.067-0.313); planet_bar.MANTLE put that corner at
y 4.32, so at rotate_z 25 the plinth's middle stood at y 4.591 and its back-right corner at y 4.83, on and past the
counter's back edge (flat to about 4.562). The fix moves Mantle by DY along y, nothing else about it: at origin y 3.98
the turned plinth spans y 3.993-4.510, 5 cm inside the flat top's back edge and about 15 cm from its front.

The shots planet_bar.py made can no longer be rebuilt from it (its room comes from e7149388, which this clone lacks), so
this moves Mantle and everything placed by it in each frame's own rendered shot file: the product instance, the lights
aimed at it (track-mantle, mantle-front, mantle-side), and in mantle-bar its camera, its Hemisphere and the sleeve on
its stand; nothing else changes.

    python3 spinoffs/barkhorn/campaign/bar_mantle_move.py OUTDIR [FRAME ...]
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SRC = os.path.join(ROOT, 'renders', '2026-11-11', 'barkhorn', 'product', 'planet-bar')
OLD = (8.5, 4.32)
NEW = (8.5, 3.98)
DX, DY = NEW[0] - OLD[0], NEW[1] - OLD[1]
FRAMES = ('bar-backbar-portrait', 'bar-backbar', 'mantle-bar', 'bar-pendants', 'core-bar-table')
NEAR = 0.9          # in mantle-bar, what stands within this of Mantle's old middle moved with it (its stand, its sleeve)


def _mv(v):
    return [round(v[0] + DX, 4), round(v[1] + DY, 4)] + list(v[2:])


def move(s, name):
    s = copy.deepcopy(s)
    log = []
    for b in s.get('products', []):
        if 'Mantle' in (b.get('collection') or ''):
            for inst in b['instances']:
                assert abs(inst['position'][0] - OLD[0]) < 1e-6 and abs(inst['position'][1] - OLD[1]) < 1e-6, inst
                inst['position'] = _mv(inst['position']); log.append(f'product {b["collection"]}')
    for k, L in s.get('lights', {}).items():
        if k in ('track-mantle', 'mantle-front', 'mantle-side') and 'target' in L:
            L['target'] = _mv(L['target']); log.append(f'light {k} target')
    if name == 'mantle-bar':
        # its camera and focus follow Mantle; so do the props placed by it (the stand and sleeve) and its Hemisphere
        cam = s['camera']
        for k in ('position', 'target', 'focus'):
            if k in cam:
                cam[k] = _mv(cam[k])
        log.append('camera')
        c0 = (OLD[0] + 0.133, OLD[1] + 0.271)          # the plinth's old middle (rotate_z 25)
        for i, p in enumerate(s['set'].get('props', [])):
            if not p:
                continue
            if p.get('position') and math.hypot(p['position'][0] - c0[0], p['position'][1] - c0[1]) < NEAR:
                p['position'] = _mv(p['position']); log.append(f'prop {i} ({p.get("shape")})')
            for bd in p.get('boards', []) or []:
                if 'x' in bd and math.hypot(bd['x'] - c0[0], bd['y'] - c0[1]) < NEAR:
                    bd['x'] = round(bd['x'] + DX, 4); bd['y'] = round(bd['y'] + DY, 4); log.append(f'prop {i} board {bd.get("image")}')
            for h in p.get('hemispheres', []) or []:
                if math.hypot(h['x'] - c0[0], h['y'] - c0[1]) < NEAR:
                    h['x'] = round(h['x'] + DX, 4); h['y'] = round(h['y'] + DY, 4); log.append(f'prop {i} hemisphere {h.get("tint")}')
    return s, log


if __name__ == '__main__':
    od = sys.argv[1]
    os.makedirs(od, exist_ok=True)
    for n in (sys.argv[2:] or FRAMES):
        s, log = move(json.load(open(os.path.join(SRC, n + '.shot.json'))), n)
        json.dump(s, open(os.path.join(od, n + '.json'), 'w'), indent=1)
        print(n, '; '.join(log))
