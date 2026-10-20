"""Round 33, EARFcoin's frames (coin.py says what it is), placed by Planet's kit piece (studio/engine/kit_ext/earf_coin.py):
the concept proofs (A/B/C x the two edges, and the eight tints of the pick), then the finals: the hero, the eight, and
the request column by an R3 Float.

    python3 spinoffs/barkhorn/companions/coin_shots.py                       # write the shots
    PY=python3.11 python3 spinoffs/barkhorn/companions/coin_shots.py --render [names] [--scale 0.5] [--samples 64]
    python3 spinoffs/barkhorn/companions/coin_shots.py --sheet proof|finals
"""
import json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'coin')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-20', 'barkhorn', 'coin')
SPECTRUM = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
NAMES = {'ember': 'Ember', 'dust': 'Dust', 'acid': 'Acid', 'poison': 'Poison', 'ice': 'Ice', 'haze': 'Haze',
         'fog': 'Fog', 'smoke': 'Smoke'}
FACE = {'engraved': 'A, reverse-engraved', 'printed': 'B, printed in colour', 'cast': 'C, cast in'}
PICK = dict(face='engraved', edge='reeded')        # the recommendation (coin.py, the README)
PAPER = '#ECE8E1'


def piece(fn, spots, **k):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': fn, 'spots': spots, **k}


def studio(title, size, cam, props, key=1.6, fill=0.5, sweep=PAPER, samples=192):
    """The house's pale studio (moon_shots' seamless, closer): a paper sweep, a softbox from the upper left and a fill."""
    tgt = cam['target']
    return {'title': title, 'size': size, 'camera': cam,
            'set': {'kind': 'sweep', 'color': sweep, 'width': 3.0, 'front': 2.0, 'depth': 0.8, 'radius': 0.5, 'height': 2.0,
                    'props': props},
            'sky': {'kind': 'gradient', 'zenith': '#D4D2CE', 'horizon': '#DCDAD5', 'ground': '#6A665F', 'strength': 0.6},
            'lights': {'key': {'type': 'area', 'size_m': [0.9, 0.7], 'orbit': {'azimuth_deg': -40, 'elevation_deg': 50, 'distance_m': 1.2},
                               'target': tgt, 'irradiance': key, 'color': '#FFF3E1'},
                       'fill': {'type': 'area', 'size_m': [1.2, 1.0], 'orbit': {'azimuth_deg': 40, 'elevation_deg': 20, 'distance_m': 1.4},
                                'target': tgt, 'irradiance': fill, 'color': '#FFF7EA'},
                       # behind and above: a rim on the edge, and light through the coin onto the paper
                       'back': {'type': 'area', 'size_m': [0.8, 0.3], 'orbit': {'azimuth_deg': 170, 'elevation_deg': 35, 'distance_m': 1.0},
                                'target': tgt, 'irradiance': 0.8, 'color': '#FFF7EA', 'camera': False}},
            'render': {'samples': samples, 'adaptive': 0.01, 'denoise': True, 'clamp': 10, 'bounces': 16,
                       'view': 'Khronos PBR Neutral', 'exposure': 0.0, 'white_balance_k': 5400}}


def proof(face, edge, flavour):
    """A proof cell: one coin lying face up, one standing on its edge behind it, three-quarters from the front."""
    props = [piece('coin', [{'position': [-0.012, -0.010, 0.0], 'rotate': [0, 0, -8]}], flavour=flavour, face=face, edge=edge),
             piece('coin', [{'position': [0.022, 0.030, 0.0201], 'rotate': [90, 0, -25]}], flavour=flavour, face=face, edge=edge)]
    cam = {'position': [0.03, -0.24, 0.17], 'target': [0.004, 0.008, 0.008], 'lens_mm': 85, 'level': False,
           'fstop': 11.0, 'focus': [0.0, 0.0, 0.004]}
    return studio(f'EARFcoin {FACE[face]}, {edge} edge, {NAMES[flavour]}', [900, 700], cam, props)


def tints(face='engraved', edge='plain'):
    """The eight of the pick, flat, from above: the tint check (each coin's lit hue against its swatch)."""
    props = [piece('coin', [{'position': [-0.161 + 0.046 * i, 0.0, 0.0], 'flavour': f, 'rotate': [0, 0, 0]}
                            for i, f in enumerate(SPECTRUM)], face=face, edge=edge)]
    cam = {'position': [0.0, -0.10, 1.02], 'target': [0.0, 0.0, 0.0], 'lens_mm': 85, 'level': False, 'fstop': 16.0,
           'focus': [0.0, 0.0, 0.0]}
    return studio('EARFcoin, the eight', [1400, 300], cam, props)


def bokeh(points, colour='#FFB060', emit=6.0, r=0.012):
    """Far lamps for the background's out-of-focus circles."""
    return [{'kind': 'kit', 'shape': 'sphere', 'material': 'glow', 'color': colour, 'emit': emit, 'scale': r,
             'position': q, 'shadow': False} for q in points]


def hero(flavour='acid'):
    """One coin on the bar's zinc, low light raking across it from behind, shallow focus: the globe 6 mm down in the
    tint catching the light, the reeds glinting."""
    zinc = {'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'metal_plate_02', 'res': '2k', 'tint': '#8E949A',
            'tint_mix': 0.55, 'rough_mul': 0.75, 'tex_scale': 0.6, 'size': [2.4, 1.6, 0.03], 'position': [0.0, 0.5, -0.03]}
    props = [zinc, piece('coin', [{'position': [0.0, 0.0, 0.0], 'rotate': [0, 0, -14]}], flavour=flavour, **PICK)]
    # the bar behind, out of focus: its lamps seen in the zinc as soft warm circles, and a low glow along the back bar
    # for the zinc's sheen (a metal shows what it mirrors: at 0.25 sky it rendered black)
    props += bokeh([[-0.50, 1.6, 0.70], [-0.12, 2.0, 0.92], [0.30, 1.8, 0.78], [0.62, 2.3, 1.02], [0.06, 2.5, 1.10],
                    [-0.85, 2.3, 0.92], [0.95, 1.9, 0.80]], emit=40.0, r=0.03)
    props += [{'kind': 'kit', 'shape': 'box', 'material': 'glow', 'color': '#FF9C55', 'emit': 1.2, 'size': [4.0, 0.02, 0.5],
               'position': [0.0, 2.6, 0.75], 'shadow': False}]
    tgt = [0.0, 0.002, 0.004]
    cam = {'position': [0.040, -0.190, 0.105], 'target': tgt, 'lens_mm': 100, 'level': False, 'fstop': 2.8,
           'focus': [0.0, -0.002, 0.004]}
    s = {'title': 'EARFcoin on the zinc', 'size': [1600, 1067], 'camera': cam,
         'set': {'kind': 'stage', 'props': props},        # no sweep: its floor would lie on the zinc's top
         'sky': {'kind': 'gradient', 'zenith': '#1C1B1A', 'horizon': '#2A2622', 'ground': '#141210', 'strength': 0.25},
         'lights': {
             # low and behind on the left: grazes the face, lights the engraving from inside, rims the reeds
             'rake': {'type': 'area', 'size_m': [0.25, 0.08], 'position': [-0.30, 0.28, 0.07], 'target': tgt,
                      'irradiance': 4.0, 'color': 2900, 'camera': False},
             # a soft warm top light, the counter's sheen
             'top': {'type': 'area', 'size_m': [0.6, 0.4], 'position': [0.10, 0.25, 0.55], 'target': tgt,
                     'irradiance': 0.9, 'color': 2700, 'camera': False},
             'fill': {'type': 'area', 'size_m': [0.5, 0.4], 'orbit': {'azimuth_deg': 25, 'elevation_deg': 18, 'distance_m': 0.8},
                      'target': tgt, 'irradiance': 0.12, 'color': 3200, 'camera': False}},
         'render': {'samples': 384, 'adaptive': 0.008, 'denoise': True, 'clamp': 12, 'bounces': 16,
                    'view': 'Khronos PBR Neutral', 'exposure': 0.0, 'white_balance_k': 3600}}
    return s


def eight():
    """The eight in spectrum order, dealt in a fan on paper (each resting on the one before), three-quarters from the
    front in the pale studio."""
    props = [piece('fan', [{'position': [-0.112, 0.012, 0.0], 'heading': -4}], flavours=SPECTRUM, s=30.0, arc=420.0,
                   seed=4, **PICK)]
    tgt = [-0.002, 0.040, 0.006]
    cam = {'position': [0.01, -0.39, 0.33], 'target': tgt, 'lens_mm': 70, 'level': False, 'fstop': 8.0,
           'focus': [-0.002, 0.040, 0.006]}
    s = studio('EARFcoin, the eight', [1600, 1067], cam, props, key=0.9, fill=0.3, samples=256, sweep='#DDD8D0')
    # a low raking strip from the back left draws the frosted globes and the reeds
    s['lights']['rake'] = {'type': 'area', 'size_m': [0.5, 0.06], 'position': [-0.45, 0.35, 0.08], 'target': tgt,
                           'irradiance': 3.0, 'color': '#FFF1DC', 'camera': False}
    return s


def column(coins=('ice', 'ember', 'acid', 'haze', 'poison', 'dust', 'smoke', 'ember', 'fog', 'ice', 'acid', 'haze',
                  'poison', 'ember', 'dust', 'ice', 'fog', 'haze')):
    """The request column by an R3 Float (its lid off), the queue a column of colours, the next song's coin pushed out
    of the slot; two coins waiting on the plinth beside it."""
    z = 0.04            # the walnut top stands on the sweep (a top flush with its floor rendered black)
    r3 = {'def': 'spinoffs/barkhorn/companions/out-concepts2/r3.json', 'flavour': 'fog', 'hide': ['cover'],
          'instances': [{'position': [-0.215, 0.10, z], 'rotate_z': 0}]}
    wood = {'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'wood_table_001', 'res': '2k', 'color': '#8A6040',
            'rough_mul': 0.5, 'size': [2.4, 1.2, z], 'position': [0.0, 0.25, 0.0]}
    props = [wood, piece('column', [{'position': [0.135, 0.02, z], 'rotate_z': 8}], coins=list(coins), out=12.0, **PICK),
             piece('coin', [{'position': [0.215, -0.06, z], 'flavour': 'acid', 'rotate': [0, 0, 30]},
                            {'position': [0.248, -0.032, z], 'flavour': 'haze', 'rotate': [0, 0, 70]}], **PICK)]
    tgt = [0.0, 0.06, 0.09 + z]
    cam = {'position': [0.30, -0.85, 0.42], 'target': tgt, 'lens_mm': 55, 'level': True, 'fstop': 5.6,
           'focus': [0.135, 0.02, 0.10]}
    s = studio('EARFcoin: the request column', [1200, 800], cam, props, key=1.4, fill=0.4, sweep='#D8D2C8', samples=256)
    s['products'] = [r3]
    s['lights']['rake'] = {'type': 'area', 'size_m': [0.08, 0.5], 'position': [-0.05, 0.45, 0.25], 'target': [0.135, 0.02, 0.12],
                           'irradiance': 1.2, 'color': '#FFF1DC', 'camera': False}
    s['camera']['position'][2] += z; s['camera']['focus'][2] += z
    return s


FRAMES = {f'proof-{f[0]}-{e}': (lambda f=f, e=e, c=c: proof(f, e, c))
          for f, c in (('engraved', 'ice'), ('printed', 'fog'), ('cast', 'ember')) for e in ('plain', 'reeded')}
FRAMES['proof-e-smoke'] = lambda: proof('engraved', 'reeded', 'smoke')
FRAMES['tints'] = lambda: tints()
FRAMES['hero'] = lambda: hero()
FRAMES['eight'] = eight
FRAMES['column'] = lambda: column()


def sheet(kind):
    """The concept sheet (A/B/C x the two edges, Smoke's check and the eight of the pick), or the finals'."""
    R = lambda n: os.path.join(RENDERS, n + '.png')
    if kind == 'proof':
        cells = [(f'proof-{f[0]}-{e}', f'{FACE[f]}, {e} edge ({NAMES[c]})') for f, c in
                 (('engraved', 'ice'), ('printed', 'fog'), ('cast', 'ember')) for e in ('plain', 'reeded')]
        cells.append(('proof-e-smoke', 'A in Smoke (cast lighter), reeded: the check'))
        tiles = ' '.join(f"-label '{t}' {R(n)}" for n, t in cells)
        top = os.path.join(RENDERS, 'sheet-proof-top.png')
        subprocess.run(f"montage {tiles} -tile 4x2 -geometry 450x350+4+4 -pointsize 15 -background '#F2F0EC' -depth 8 {top}",
                       shell=True, check=True)
        out = os.path.join(RENDERS, 'sheet-proof.png')
        subprocess.run(f"convert {top} \\( {R('tints')} -resize 1832x -background '#F2F0EC' -gravity south -splice 0x22 "
                       f"-pointsize 15 -annotate +0+2 'A, the eight (the tint check: each hue within 5 deg of its swatch)' \\) "
                       f"-background '#F2F0EC' -gravity center -append -depth 8 {out}", shell=True, check=True)
        os.remove(top)
    else:
        tiles = ' '.join(f"-label '{t}' {R(n)}" for n, t in (('hero', 'The hero, on the zinc'), ('eight', 'The eight'),
                                                              ('column', 'The request column')))
        out = os.path.join(RENDERS, 'sheet-finals.png')
        subprocess.run(f"montage {tiles} -tile 3x1 -geometry 600x400+4+4 -pointsize 15 -background '#F2F0EC' -depth 8 {out}",
                       shell=True, check=True)
    print(out)


def build():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in FRAMES.items():
        json.dump(f(), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
        print(n)


def render(names, scale, samples=None):
    py = os.environ.get('PY', 'python3')
    os.makedirs(RENDERS, exist_ok=True)
    for n in names:
        cmd = [py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
               '--out', os.path.join(RENDERS, n + '.png'), '--scale', str(scale)]
        if samples:
            cmd += ['--samples', str(samples)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-3000:], r.stderr[-3000:])
            raise SystemExit(n)
        print(n, flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--sheet' in a:
        sheet(a[a.index('--sheet') + 1])
    elif '--render' in a:
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        samples = int(a[a.index('--samples') + 1]) if '--samples' in a else None
        render([x for x in a if x in FRAMES] or list(FRAMES), scale, samples)
    else:
        build()
