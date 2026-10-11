"""barkhorn's comparison sheets: sets of frames, one speaker each under the same light and camera, rendered and set
in a grid with their names.

    python3 spinoffs/barkhorn/frames.py covers|front|study|experiments [--samples 64] [--all | --only NAME ...]

Sets:
- covers: each bark bare, as photographed, then with each front cover (round 2);
- front: the panel faced in bark under a solid colour cloth, two ways: the whole front's grille (the bark shows when it
  comes off) and a disc over the woofer alone (round 3);
- study: the waveguide's forms (P['horn']['form']), three-quarter and from the side; each form's render model is built
  first into out/study/ (`--build` to build them again after a change);
- experiments: material experiments (pressed recycled plastic, strata and terrazzo resin);
- proposal: where the study points: the pebble waveguide in strata resin (eucalyptus) and in terrazzo (birch), on the
  bark face with a cloth disc.

Each frame's shot goes to studio/shots/barkhorn/<set>/ (so any one can be re-rendered or tuned) and its image to
renders/<day>/barkhorn/<set>/, beside the grid <set>.png. Only frames not yet rendered are rendered, unless named with
--only or all are asked for with --all; the grid is set again every run.
"""
import argparse, copy, io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn')
PRODUCT = 'studio/products/barkhorn.json'
STUDY = os.path.join(HERE, 'out', 'study')
DAY = {'covers': '2026-10-10'}                 # where each set's renders live (a set first made that day)

FRONT_CAM = {'position': [-0.78, -2.6, 1.0], 'target': [0.0, 0.0, 0.64], 'lens_mm': 66, 'level': True}
THREE_Q = {'position': [1.45, -2.7, 1.45], 'target': [0.0, 0.08, 0.66], 'lens_mm': 60, 'level': True}
RIGHT_Q = {'position': [1.25, -2.55, 1.2], 'target': [0.0, 0.05, 0.66], 'lens_mm': 60, 'level': True}
SIDE = {'position': [3.2, 0.12, 0.8], 'target': [0.0, 0.12, 0.66], 'lens_mm': 70, 'level': True}
# from behind: the speaker turned round and brought 1.2 m forward of the wall (the room's lamps follow it), seen from
# behind and above
BEHIND = {'position': [-1.0, -3.2, 1.45], 'target': [0.0, -1.2, 0.72], 'lens_mm': 55, 'level': True}
TURNED = dict(position=[0.0, -1.2, 0], rotate_z=180, shift=-1.2)


def F(name, bark, label, options=(), materials=None, product=PRODUCT, camera=None, lights=None, at=None):
    return dict(name=name, bark=bark, label=label, options=list(options), materials=materials or {}, product=product,
                camera=camera, lights=lights or {}, at=at)


def form_product(form):
    return os.path.relpath(os.path.join(STUDY, f'barkhorn-{form}.json'), ROOT)


FORMS = [('shell', 'shell (round 2)'), ('lens', 'lens'), ('slab', 'slab'), ('pebble', 'pebble: slab rim, lens back'),
         ('round', 'round')]
SETS = {
    'covers': dict(title='barkhorn: front covers (options)', camera=FRONT_CAM, rows={
        'birch': [F('birch-bare', 'birch', 'bare, as photographed'), F('birch-cloth', 'birch', 'cloth grille', ['cloth']),
                  F('birch-lenticel-grille', 'birch', 'lenticel grille', ['lenticel-grille']),
                  F('birch-bark-face', 'birch', 'bark face', ['bark-face']), F('birch-cork-face', 'birch', 'cork face', ['cork-face'])],
        'eucalyptus': [F('eucalyptus-bare', 'eucalyptus', 'bare, as photographed'),
                       F('eucalyptus-cloth', 'eucalyptus', 'cloth grille', ['cloth']),
                       F('eucalyptus-strip-grille', 'eucalyptus', 'strip grille', ['strip-grille']),
                       F('eucalyptus-bark-face', 'eucalyptus', 'bark face', ['bark-face']),
                       F('eucalyptus-cork-face', 'eucalyptus', 'cork face', ['cork-face'])]}),
    'front': dict(title='barkhorn: the bark face under a solid colour cloth', camera=FRONT_CAM, rows={
        'birch': [F('birch-grille-charcoal', 'birch', 'grille, charcoal', ['bark-face', 'cloth'], {'cloth': {'color': '#2E2C2A'}}),
                  F('birch-disc-charcoal', 'birch', 'disc, charcoal', ['bark-face', 'cloth-disc'], {'disc': {'color': '#2E2C2A'}}),
                  F('birch-disc-apricot', 'birch', 'disc, apricot', ['bark-face', 'cloth-disc'], {'disc': {'color': '#C98F64'}}),
                  F('birch-disc-oxblood', 'birch', 'disc, oxblood', ['bark-face', 'cloth-disc'], {'disc': {'color': '#6B2B26'}})],
        'eucalyptus': [F('eucalyptus-grille-forest', 'eucalyptus', 'grille, forest green', ['bark-face', 'cloth'],
                         {'cloth': {'color': '#3F4F3A'}}),
                       F('eucalyptus-disc-rust', 'eucalyptus', 'disc, rust', ['bark-face', 'cloth-disc'], {'disc': {'color': '#9A4526'}}),
                       F('eucalyptus-disc-leaf', 'eucalyptus', 'disc, leaf green', ['bark-face', 'cloth-disc'], {'disc': {'color': '#5E6E4F'}}),
                       F('eucalyptus-disc-cream', 'eucalyptus', 'disc, cream', ['bark-face', 'cloth-disc'], {'disc': {'color': '#E4D9BF'}})]}),
    'study': dict(title='barkhorn: waveguide study (eucalyptus, bark face, rust disc)', rows={
        'three-quarter': [F(f'{f}-3q', 'eucalyptus', label, ['bark-face', 'cloth-disc'], product=form_product(f), camera=THREE_Q)
                          for f, label in FORMS],
        'side': [F(f'{f}-side', 'eucalyptus', label, ['bark-face', 'cloth-disc'], product=form_product(f), camera=SIDE)
                 for f, label in FORMS],
        'behind': [F(f'{f}-behind', 'eucalyptus', label, ['bark-face', 'cloth-disc'], product=form_product(f), camera=BEHIND,
                     at=TURNED) for f, label in FORMS]}),
    'proposal': dict(title='barkhorn: where the study points (round 3)', camera=RIGHT_Q, rows={
        'the proposal': [F('pebble-strata-eucalyptus', 'eucalyptus-strata', 'eucalyptus: pebble in strata resin, rust disc',
                           ['bark-face', 'cloth-disc'], product=form_product('pebble')),
                         F('pebble-terrazzo-birch', 'birch-terrazzo', 'birch: pebble in terrazzo resin, charcoal disc',
                           ['bark-face', 'cloth-disc'], product=form_product('pebble'))]}),
    'experiments': dict(title='barkhorn: material experiments', camera=RIGHT_Q, rows={
        'cabinet': [F('pressed-eucalyptus', 'eucalyptus-pressed', 'pressed recycled plastic, eucalyptus', ['bark-face', 'cloth-disc']),
                    F('pressed-birch', 'birch-pressed', 'pressed recycled plastic, birch', ['bark-face', 'cloth-disc'])],
        'waveguide': [F('strata-eucalyptus', 'eucalyptus-strata', 'strata resin waveguide', ['bark-face', 'cloth-disc']),
                      F('terrazzo-birch', 'birch-terrazzo', 'terrazzo resin waveguide', ['bark-face', 'cloth-disc'])]}),
}


def shot_for(frame, set_camera):
    bark = frame['bark'].split('-')[0]
    s = copy.deepcopy(json.load(open(os.path.join(SHOTS, f'{bark}.json'))))
    at = frame['at'] or {}
    inst = {'position': at.get('position', [0, 0, 0]), 'rotate_z': at.get('rotate_z', 0), 'flavour': frame['bark']}
    for L in s['lights'].values():          # the lamps follow a speaker brought forward
        for k in ('target', 'position'):
            if k in L:
                L[k] = [L[k][0], L[k][1] + at.get('shift', 0.0), L[k][2]]
    if frame['options']:
        inst['options'] = frame['options']
    s['product'] = {'def': frame['product'], 'flavour': frame['bark'], 'instances': [inst]}
    s['camera'] = copy.deepcopy(frame['camera'] or set_camera)
    s['size'] = [760, 1000]
    s['title'] = f"barkhorn, {frame['label']}"
    if frame['materials']:
        s.setdefault('materials', {}).update(frame['materials'])
    s['lights'].update(copy.deepcopy(frame['lights']))
    return s


def build_forms():
    """Each waveguide form's render model and engine file into out/study/ (the speaker the same, the waveguide not)."""
    venv = os.path.join(ROOT, '.venv-fab', 'bin', 'python')
    code = f'''
import copy, dataclasses, os, sys
sys.path.insert(0, {os.path.join(ROOT, 'studio', 'fabkit')!r})
import build, render
P0 = build.load_product({os.path.join(HERE, 'product.py')!r})
os.makedirs({STUDY!r}, exist_ok=True)
for form in {[f for f, _ in FORMS]!r}:
    params = copy.deepcopy(P0.params); params['horn']['form'] = form
    prod = dataclasses.replace(P0, name='barkhorn-' + form, params=params)
    parts = [p for p in prod.parts(params) if p.solid is not None]
    glb, pf = render.write(prod, parts, {STUDY!r}, engine_file=os.path.join({STUDY!r}, 'barkhorn-' + form + '.json'), proof=False)
    print('built', form, os.path.relpath(glb, {ROOT!r}))
'''
    subprocess.run([venv, '-c', code], check=True, cwd=ROOT)


def font(size, bold=False):
    from fontTools.ttLib import TTFont
    from PIL import ImageFont
    tt = TTFont(os.path.join(ROOT, 'render', 'fonts', 'Archivo-Bold.woff' if bold else 'Archivo-Regular.woff'))
    tt.flavor = None
    buf = io.BytesIO(); tt.save(buf); buf.seek(0)
    return ImageFont.truetype(buf, size)


def grid(title, cells, out, cell_w=480):
    """cells: {row: [(png, label), ...]} -> one image, each row under its name, each frame's name under it; each frame
    `cell_w` wide."""
    from PIL import Image, ImageDraw
    rows = list(cells)
    w0, h0 = Image.open(cells[rows[0]][0][0]).size
    w, h = cell_w, round(cell_w * h0 / w0)
    pad, lab, head, rowhead = 20, 40, 64, 40
    ncol = max(len(v) for v in cells.values())
    W = pad + ncol * (w + pad)
    H = head + len(rows) * (rowhead + h + lab) + pad
    sheet = Image.new('RGB', (W, H), (246, 244, 239))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 20), title, font=font(28, True), fill=(30, 28, 26))
    for r, row in enumerate(rows):
        y = head + r * (rowhead + h + lab)
        d.text((pad, y + 4), row, font=font(24, True), fill=(30, 28, 26))
        y += rowhead
        for c, (png, label) in enumerate(cells[row]):
            x = pad + c * (w + pad)
            sheet.paste(Image.open(png).convert('RGB').resize((w, h), Image.LANCZOS), (x, y))
            d.text((x, y + h + 8), label, font=font(20), fill=(60, 56, 52))
    sheet.save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('set', choices=list(SETS))
    ap.add_argument('--samples', type=int, default=64)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--day', default='2026-10-11')
    ap.add_argument('--only', nargs='*', default=[], help='frame names to render again (e.g. birch-disc-charcoal)')
    ap.add_argument('--all', action='store_true', help='render every frame again')
    ap.add_argument('--build', action='store_true', help='build the study\'s render models again')
    a = ap.parse_args()
    S = SETS[a.set]
    if a.set == 'study' and (a.build or not all(os.path.exists(os.path.join(STUDY, f'barkhorn-{f}.json')) for f, _ in FORMS)):
        build_forms()
    sd = os.path.join(SHOTS, a.set); os.makedirs(sd, exist_ok=True)
    rd = os.path.join(ROOT, 'renders', DAY.get(a.set, a.day), 'barkhorn')
    od = os.path.join(rd, a.set); os.makedirs(od, exist_ok=True)
    cells = {}
    for row, frames in S['rows'].items():
        cells[row] = []
        for fr in frames:
            path = os.path.join(sd, f"{fr['name']}.json")
            json.dump(shot_for(fr, S.get('camera')), open(path, 'w'), indent=1)
            png = os.path.join(od, f"{fr['name']}.png")
            if a.all or fr['name'] in a.only or not os.path.exists(png):
                print('render', fr['name'], flush=True)
                subprocess.run([sys.executable, os.path.join(ROOT, 'studio', 'engine', 'render.py'), path, '--out', png,
                                '--samples', str(a.samples), '--scale', str(a.scale)], check=True, cwd=ROOT,
                               stdout=subprocess.DEVNULL)
            cells[row].append((png, fr['label']))
    print(grid(S['title'], cells, os.path.join(rd, f'{a.set}.png')))


if __name__ == '__main__':
    main()
