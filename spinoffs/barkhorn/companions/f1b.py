"""F1b, Block lit low (round 32b, the coordinator: "keep F1 alive; the owner liked the squared one"): F1 Block with a
frosted lower section so it lights the table (bar_lamps.family('f1b')), blocked out and rendered in Moon's two bar frames
(moon_shots.py's set, its third critic round), so the owner can set the square beside the recommended Moon.

    .venv-fab/bin/python spinoffs/barkhorn/companions/f1b.py            # the blockouts and the shots
    PY=python3.11 python3 spinoffs/barkhorn/companions/f1b.py --render
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import bar_lamps as B                                               # noqa: E402
import moon_shots as MS                                             # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'f1b')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'f1b')
VIEWS = [('bar', 'smoked'), ('bar', 'ember')]
LIGHTS = os.path.join(B.OUT, 'f1b-lights.json')


def build():
    K = B._kit()
    import render as fk_render
    table, tled, pend, pled = B.family('f1b')
    for kind, parts in (('table', table), ('pendant', pend)):
        name = f'f1b-{kind}'
        prod = K.Product(name, f'F1b Block {kind}', 'bar lamp blockout', params={}, parts=lambda P, parts=parts: parts,
                         materials=B.MATERIALS, variants=B.VARIANTS)
        fk_render.write(prod, parts, os.path.join(B.OUT, name), engine_file=os.path.join(B.OUT, f'{name}.json'), proof=False)
    json.dump({'table_light_mm': tled, 'pendant_light_mm': pled}, open(LIGHTS, 'w'), indent=1)
    shots()


def shot(where, colour, tled, pled):
    s = MS.shot(where, colour)
    tx, ty, px, py = -0.12, 0.0, 0.26, 0.18
    s['title'] = f'F1b Block in {colour}, {where}'
    s['set']['props'] = [p for p in s['set']['props'] if p.get('module') != 'earf_moon']
    s['products'] = [{'def': 'spinoffs/barkhorn/companions/out-bar/f1b-table.json', 'flavour': colour,
                      'instances': [{'position': [tx, ty, MS.TABLE_Z], 'rotate_z': 12}]},
                     {'def': 'spinoffs/barkhorn/companions/out-bar/f1b-pendant.json', 'flavour': colour,
                      # the block is 170 tall to Moon's 120 at the disc: hung so its mouth sits where Moon's rim does
                      'instances': [{'position': [px, py, MS.PEND_Z], 'rotate_z': 0}]}]
    s['materials'] = {'shade': {'glow': 0.6}, 'edge': {'strength': 2.5}}
    s['lights']['tlamp'] = B.hidden_point((tx + tled[0] / 1000, ty + tled[1] / 1000, MS.TABLE_Z + tled[2] / 1000), 14.0)
    s['lights']['pend'] = B.hidden_point((px + pled[0] / 1000, py + pled[1] / 1000, MS.PEND_Z + pled[2] / 1000), 9.0)
    return s


def shots():
    os.makedirs(SHOTS, exist_ok=True)
    L = json.load(open(LIGHTS))
    for where, colour in VIEWS:
        json.dump(shot(where, colour, L['table_light_mm'], L['pendant_light_mm']),
                  open(os.path.join(SHOTS, f'{where}-{colour}.json'), 'w'), indent=1)
        print(where, colour)


def render():
    py = os.environ.get('PY', 'python3')
    os.makedirs(RENDERS, exist_ok=True)
    for where, colour in VIEWS:
        name = f'{where}-{colour}'
        subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, name + '.json'),
                        '--out', os.path.join(RENDERS, name + '.png'), '--scale', sys.argv[sys.argv.index('--scale') + 1]
                        if '--scale' in sys.argv else '1.0'], check=True)
        print(name, flush=True)


if __name__ == '__main__':
    render() if '--render' in sys.argv else build()
