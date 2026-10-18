#!/usr/bin/env python3
"""Stage an uplight31 image for a fresh, blind critic under critic/PROMPT-promo.md: the image under a neutral name, a
short card (what the frame is for and what is fixed, from card-uplight31.yaml, and the shot's current settings), the
measuring tool, and the message to hand the critic verbatim.

    python3 spinoffs/barkhorn/critic/stage_promo.py IMAGE.png --shot uplight-frame --tag f1 [--stage DIR]
"""
import argparse, json, os, shutil, sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def prompt_text():
    t = (ROOT / 'critic' / 'PROMPT-promo.md').read_text()
    a = t.index('\n---\n') + 5; b = t.index('\n---\n', a)
    return t[a:b].strip()


def settings(sh):
    """The settings worth naming: the camera, the lights, the set's pieces, the haze, the sky, the exposure."""
    L = [f'- camera: {json.dumps(sh.get("camera"))}', f'- frame: {sh.get("size")} px',
         f'- render: exposure {sh["render"].get("exposure")}, view {sh["render"].get("view")}, white balance {sh["render"].get("white_balance_k")} K',
         f'- sky (`sky`): {json.dumps(sh.get("sky"))}', f'- haze (`haze`): {json.dumps(sh.get("haze"))}']
    for n, l in (sh.get('lights') or {}).items():
        L.append(f'- `lights.{n}`: {json.dumps(l)}')
    for i, p in enumerate(sh['set'].get('props', [])):
        L.append(f'- `set.props.{i}`: {json.dumps(p)}')
    L.append('- the speakers (`product.instances.N.position`): ' + json.dumps([i['position'] for i in sh['product']['instances']]))
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('image'); ap.add_argument('--shot', required=True); ap.add_argument('--tag', required=True)
    ap.add_argument('--stage', default=os.environ.get('CLAUDE_SCRATCH', '/tmp') + '/critic-stage')
    a = ap.parse_args()
    d = Path(a.stage); d.mkdir(parents=True, exist_ok=True)
    src = Path(a.image)
    img = d / f'render-{a.tag}{src.suffix}'
    shutil.copy(src, img)
    card = yaml.safe_load((HERE / 'card-uplight31.yaml').read_text())
    sc = card['shots'][a.shot]
    sh = json.loads(src.with_suffix('.shot.json').read_text()) if src.with_suffix('.shot.json').exists() else None
    L = [f'# Card: {sc["title"]}', '', '## The product', '', ' '.join(card['product'].split()), '',
         '## What this frame is for', '', ' '.join(sc['purpose'].split()), '', 'It must show: ' + '; '.join(sc['must_show']) + '.', '',
         '## Fixed', '']
    L += ['- ' + ' '.join(f.split()) for f in card['fixed'] + sc.get('fixed', [])]
    L += ['', '## What may change', '', 'Everything about the set, the light, the camera, the sky, the haze and the finish. Lengths '
          'are metres; z up; the speakers face -y (toward the camera); the wall\'s face is a plane of constant y behind them. The '
          'set\'s pieces are kit pieces: `concrete.wall` (a block `size` [w, t, h] of board-formed concrete, a photographed '
          'texture `texture`, `bump`, `vary` its tone variation), `concrete.paving` (`texture`, `wet` 0 to 1, `puddle_m`), '
          '`concrete.water` (`ripple`, `ripple_m`), boxes and cylinders. The uplights are Cycles spot lamps (power in W, '
          'cone, blend, radius, colour); the view transform is Khronos PBR Neutral.']
    if sh:
        L += ['', '## The shot\'s current settings', ''] + settings(sh)
    (d / f'card-{a.tag}.md').write_text('\n'.join(L) + '\n')
    tool = d / 'measure.py'
    shutil.copy(ROOT / 'critic' / 'measure.py', tool)
    work = d / f'work-{a.tag}'; work.mkdir(exist_ok=True)
    text = prompt_text().replace('TOOL', str(tool)).replace('IMAGE', str(img)).replace('SCRATCH', str(work))
    msg = (f'Image: {img}\nCard (read only in stage 2): {d / f"card-{a.tag}.md"}\nMeasuring tool: {tool} (run it with python3)\n'
           f'Scratch directory for your crops and grids: {work}\n\n{text}\n')
    (d / f'message-{a.tag}.txt').write_text(msg)
    print(d / f'message-{a.tag}.txt')


if __name__ == '__main__':
    main()
