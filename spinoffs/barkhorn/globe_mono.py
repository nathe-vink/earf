"""Round 33b: the mark's one-colour globes as real objects (the owner, 2026-10-20: "Is it possible to actually build the
paper and black globes as well? Those could be cool with light cast on them. Maybe not.").

The one-colour marks (brand/real/earf-real-fill-black.png and -white.png, globe_real.py --flat) are see-through faces
with solid rims. Built as the colour globe is (globe_object.py: six discs, the three parallels and three meridians,
leaning 23.4 degrees, each slotted round those before it, the meridian facing us whole), in three sheets:

- black: the Smoke speaker's own cast acrylic (its cabinet's tint, #8A888E after 25 mm), 8 mm: a face is a smoked
  window, and an edge, seen along the disc, goes dark: the drawing's dark rims.
- paper (i): opal cast acrylic, 8 mm (the lamps' frost, a white that lets light through): durable, and it glows where
  the light falls on it.
- paper (ii): real board, 2 mm cotton museum board, laser-cut and slotted: matte, crisp shadows, fragile, cheap.

A ~300 mm desk object (R 150). Lit by one hard raking spot and a little fill, so the rims cast lines of shadow across
the discs and onto the ground: the globe drawn by its own shadow. On paper and on night.

    .venv-fab/bin/python spinoffs/barkhorn/globe_mono.py                  the models (out-globe-mono/) and the shots
    python3.11 spinoffs/barkhorn/globe_mono.py --render [names] [--scale S] [--samples N]
    python3 spinoffs/barkhorn/globe_mono.py --sheet proof
"""
import json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, 'out-globe-mono')
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'globe-mono')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-20', 'barkhorn', 'globe-mono')

LEAN, ELEV, LAT = 23.44, 16.0, 40.0                      # earth.py's
R = 150.0                                                # the desk globe, 300 across
SHEETS = {'acrylic': 8.0, 'board': 2.0}                  # the discs' sheet (mm): the mark's slab is 0.05 of the radius
GAP = {'acrylic': 0.15, 'board': 0.1}                    # each slot's clearance a side: acrylic cemented, board a push fit
STAND = dict(r_out=40.0, r_in=33.0, h=14.0)              # a blackened-steel ring the globe rests in
GROUNDS = {'paper': '#F2EFEA', 'night': '#121114'}       # earth.PAPER, earth.NIGHT

MATERIALS = {
    'black': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#8A888E', 'radius': 0.025, 'roughness': 0.03},
    'opal': {'preset': 'frosted', 'color': '#F6F4EF', 'absorb': '#F1EBE0', 'roughness': 0.35, 'radius': 0.006,
             'clear': 0.04},
    'board': {'preset': 'paper_cone', 'color': '#F1EEE6', 'roughness': 0.9, 'fibre_strength': 0.06},
    'steel': {'preset': 'black_oxide', 'color': '#2E2D2B'},
}
KINDS = {'black': ('acrylic', 'black'), 'opal': ('acrylic', 'opal'), 'board': ('board', 'board')}
TITLES = {'black': 'Black: Smoke cast acrylic', 'opal': 'Paper (i): opal cast acrylic',
          'board': 'Paper (ii): cotton board'}


def discs(T, gap):
    """The six discs in the globe's frame (axis z, the camera along -y), each slotted round those before it: the
    meridian facing us (longitude 90) whole, and returned as [(name, solid)] with each solid's pieces."""
    from build123d import Cylinder, Rot, Pos
    full = []
    for name, lam in (('m90', 90.0), ('m30', 30.0), ('m150', 150.0)):
        full.append((name, Rot(Z=lam - 90) * Rot(X=90) * Cylinder(R, T), Rot(Z=lam - 90) * Rot(X=90) * Cylinder(R + 1, T + 2 * gap)))
    for name, phi in (('equator', 0.0), ('north', LAT), ('south', -LAT)):
        r, z = R * math.cos(math.radians(phi)), R * math.sin(math.radians(phi))
        full.append((name, Pos(0, 0, z) * Cylinder(r, T), Pos(0, 0, z) * Cylinder(r + 1, T + 2 * gap)))
    out = []
    for i, (name, solid, _) in enumerate(full):
        for _, _, slab in full[:i]:
            solid = solid - slab
        out.append((name, solid))
    return out


def lift():
    return STAND['h'] + math.sqrt(R * R - STAND['r_in'] ** 2)


def build():
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
    from build123d import Cylinder, Pos, Rot
    from model import Part, Product, Machined, Sheet
    import render
    made = {}
    for sheet, T in SHEETS.items():
        z = lift()
        ds = discs(T, GAP[sheet])
        parts = [Part(f'disc-{n}', Pos(0, 0, z) * Rot(Y=LEAN) * s, Machined('cast-acrylic', 'cnc-mill'), finish='disc')
                 for n, s in ds]
        ring = Pos(0, 0, STAND['h'] / 2) * (Cylinder(STAND['r_out'], STAND['h']) - Cylinder(STAND['r_in'], STAND['h'] + 2))
        parts.append(Part('stand', ring, Machined('steel', 'lathe'), finish='steel'))
        flav = ({'black': {'materials': {'disc': MATERIALS['black']}}, 'opal': {'materials': {'disc': MATERIALS['opal']}}}
                if sheet == 'acrylic' else {'board': {'materials': {'disc': MATERIALS['board']}}})
        mats = {'disc': MATERIALS['black' if sheet == 'acrylic' else 'board'], 'steel': MATERIALS['steel']}
        name = f'earf-globe-mono-{sheet}'
        prod = Product(name, f'EARF globe, one colour ({sheet})', 'the mark in one sheet', params={}, parts=lambda p: parts,
                       count=1, materials=mats, variants=flav)
        render.write(prod, parts, os.path.join(OUT, sheet), engine_file=os.path.join(OUT, f'{name}.json'), proof=False)
        pieces = {n: len(s.solids()) for n, s in ds}
        made[sheet] = pieces
    json.dump({'pieces': made, 'R': R, 'sheets': SHEETS, 'gap': GAP}, open(os.path.join(OUT, 'pieces.json'), 'w'), indent=1)
    return made


def shot(kind, ground, size=(900, 900), samples=128):
    sheet, flavour = KINDS[kind]
    night = ground == 'night'
    zc = lift() / 1000
    c = [0.0, 0.0, zc]
    el, dist = math.radians(ELEV + 6), 1.75
    return {'title': f'{TITLES[kind]}, on {ground}', 'size': list(size),
            'product': {'def': os.path.relpath(os.path.join(OUT, f'earf-globe-mono-{sheet}.json'), ROOT), 'flavour': flavour,
                        'instances': [{'position': [0, 0, 0], 'rotate_z': 0}]},
            'set': {'kind': 'sweep', 'color': GROUNDS[ground], 'width': 6.0, 'front': 3.0, 'depth': 1.6, 'radius': 0.9, 'height': 3.0},
            'camera': {'position': [0.0, -dist * math.cos(el), zc + dist * math.sin(el)], 'target': [0.02, 0.02, zc - 0.035],
                       'lens_mm': 115.0, 'level': False},
            'sky': {'kind': 'gradient', 'zenith': '#C4C2BE', 'horizon': '#CFCDC8', 'ground': '#5A5650',
                    'strength': 0.04 if night else 0.25},
            'lights': {
                # one hard raking spot from the left, low: the rims' shadows run across the discs and onto the ground
                'spot': {'type': 'spot', 'position': [-1.5, 0.35, zc + 0.62], 'target': [0.06, -0.02, 0.10], 'power_w': 700 if not night else 520,
                         'cone_deg': 24, 'blend': 0.35, 'radius_m': 0.003, 'color': 3600, 'camera': False},
                'fill': {'type': 'area', 'size_m': [1.6, 1.2], 'orbit': {'azimuth_deg': 30, 'elevation_deg': 20, 'distance_m': 2.6},
                         'target': c, 'irradiance': 0.04 if night else 0.18, 'color': '#FFF7EA', 'camera': False}},
            'render': {'samples': samples, 'adaptive': 0.012, 'denoise': True, 'clamp': 10, 'bounces': 16,
                       'view': 'Khronos PBR Neutral', 'exposure': 0.0, 'white_balance_k': 4600}}


def final(kind, ground):
    """A final at 1600 x 1067: the globe left of centre, its shadow drawing across the ground to the right; on night a
    low rim from behind draws the far edges."""
    s = shot(kind, ground, size=(1600, 1067), samples=256)
    zc = lift() / 1000
    s['camera'].update(lens_mm=70.0, target=[0.10, 0.06, zc - 0.02])
    s['sky'].update(zenith='#D6D0C6', horizon='#DDD7CD')     # the sweep's wall warm, not the blue-grey of the proofs
    if ground == 'night':
        s['lights']['rim'] = {'type': 'area', 'size_m': [0.6, 0.15], 'position': [0.35, 1.1, zc + 0.35],
                              'target': [0.0, 0.0, zc], 'irradiance': 0.5, 'color': 4200, 'camera': False}
    return s


FRAMES = {f'{k}-{g}': (lambda k=k, g=g: shot(k, g)) for k in KINDS for g in GROUNDS}
FRAMES['final-black-paper'] = lambda: final('black', 'paper')
FRAMES['final-board-night'] = lambda: final('board', 'night')


def write_shots():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in FRAMES.items():
        json.dump(f(), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)


def render_(names, scale, samples):
    os.makedirs(RENDERS, exist_ok=True)
    for n in names:
        cmd = [sys.executable, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
               '--out', os.path.join(RENDERS, n + '.png'), '--scale', str(scale)] + (['--samples', str(samples)] if samples else [])
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-2000:], r.stderr[-2000:]); raise SystemExit(n)
        print(n, flush=True)


def sheet():
    tiles = ' '.join(f"-label '{TITLES[k]}, {g}' {os.path.join(RENDERS, f'{k}-{g}.png')}" for g in GROUNDS for k in KINDS)
    out = os.path.join(RENDERS, 'sheet-proof.png')
    subprocess.run(f"montage {tiles} -tile 3x2 -geometry 560x560+4+4 -pointsize 15 -background '#F2F0EC' -depth 8 {out}",
                   shell=True, check=True)
    print(out)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--sheet' in a:
        sheet()
    elif '--render' in a:
        write_shots()
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        samples = int(a[a.index('--samples') + 1]) if '--samples' in a else None
        render_([x for x in a if x in FRAMES] or [k for k in FRAMES if not k.startswith('final')], scale, samples)
    else:
        print(json.dumps(build()))
        write_shots()
