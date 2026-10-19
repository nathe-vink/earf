"""Round 32c, a shape study for the bar lamps (the owner, 2026-10-19: "I'm not sure I like the white section. Maybe if
we do that for light dispersion it's set within the acrylic. Not sure what shape I like yet."): one treatment in five
shapes, each a cordless table lamp and a matching pendant, blocked out and rendered in Moon's bar frame (moon_shots.py)
in smoked and in Ember.

The treatment: nothing white outside. Every visible surface of the shade is tinted cast acrylic, polished; the
diffuser is a frosted liner (an acid-etched or bead-blasted tube or cup) cast or bonded inside it, and where the
shade is open below (the domes, the cones, the pendants) a 3 mm tinted skin covers the liner's inside too: tint,
frost, tint. So the tint glows evenly from within, the frost is seen only through acrylic, and the source, behind the
frost, is never seen. The light is hidden in every shot as Planet's are; the liner glows by itself.

The shapes:
- s1 dome: Moon's dome on its column, the dome tinted, the liner a frosted cup inside it;
- s2 block: the rounded square, a tinted tube with walls 12, a frosted tube inside;
- s3 column: the cylinder, the same in the round;
- s4 sphere: a tinted ball on a column (the table lamp), a ball open below (the pendant);
- s5 cone: a tinted cone, mouth down, on a column and as the pendant (the classic bar shape, the deepest cut-off).

The pendants are open below, the light up inside them past the liner (cut-offs 20 to 35 degrees from the vertical);
the table lamps are cordless (the foot holds the battery, as Moon's), the light under the dome or the cone or inside
the closed forms, so no LED is seen from a seat.

    .venv-fab/bin/python spinoffs/barkhorn/companions/study.py            # the blockouts and the shots
    PY=python3.11 python3 spinoffs/barkhorn/companions/study.py --render [--scale 0.6] [s1 s2 ...]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import bar_lamps as B                                               # noqa: E402
import moon_shots as MS                                             # noqa: E402

OUT = os.path.join(HERE, 'out-study')
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'study')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'study')
SHAPES = {'s1': 'Dome', 's2': 'Block', 's3': 'Column', 's4': 'Sphere', 's5': 'Cone'}
VIEWS = [('bar', 'smoked'), ('bar', 'ember')]

MATERIALS = dict(B.MATERIALS, liner={'preset': 'frosted', 'color': '#F4F2EE', 'absorb': '#EFE6D8', 'roughness': 0.5,
                                     'radius': 0.02, 'clear': 0.1, 'glow': 0.0, 'glow_color': '#FF9A50'})
GAP, LT = 1.0, 2.5            # the liner: 1 mm in from the shell, 2.5 thick
# the hidden lamps (W, table and pendant): a lamp close inside a closed form burned its liner white
WATTS = {'s2': (6.0, 9.0), 's3': (6.0, 9.0), 's4': (3.0, 5.0)}


def _kit():
    return B._kit()


def cone_shell(K, r0, r1, z0, z1, t):
    """A conical wall, `t` thick across, its outside from radius r0 at z0 to r1 at z1."""
    return K.revolve_profile([(r0 - t, z0), (r0, z0), (r1, z1), (r1 - t, z1)])


def ball(R, t, c, cut_below=None, cut_above=None, hole=None):
    from build123d import Sphere, Pos
    import geom as G
    s = Pos(*c) * (Sphere(R) - Sphere(R - t))
    if cut_below is not None:
        s = s - G.box(-R - 1, -R - 1, c[2] - R - 1, R + 1, R + 1, cut_below)
    if cut_above is not None:
        s = s - G.box(-R - 1, -R - 1, cut_above, R + 1, R + 1, c[2] + R + 1)
    return s


def shape(key):
    """(table parts, its light, pendant parts, its light), mm: z up from the table, or from the pendant's lowest point."""
    K = _kit()
    Part, Bought, Machined = K.Part, K.Bought, K.Machined
    rsq = lambda w, z0, z1, r: B.rsq(K, w, z0, z1, r)
    cyl = lambda d, z0, z1: K.cyl('z', (0, 0), d, z0, z1)
    foot = cyl(120, 0, 22)
    T = [Part('foot', foot, Machined('steel'), finish='steel')]
    P = []
    metal = 'steel'
    if key == 's1':
        T += [Part('column', cyl(40, 22, 187), Machined('cast-acrylic'), finish='body'),
              Part('hub', cyl(52, 187, 205), Machined('brass'), finish='brass')]
        T += [Part('dome', ball(75, 8, (0, 0, 193), cut_below=193), Machined('cast-acrylic'), finish='body'),
              Part('liner', ball(75 - 8 - GAP, LT, (0, 0, 193), cut_below=196), Machined('cast-acrylic'), finish='liner'),
              Part('skin', ball(75 - 8 - 2 * GAP - LT, 3, (0, 0, 193), cut_below=193), Machined('cast-acrylic'), finish='body'),
              Part('finial', cyl(20, 267.5, 277), Machined('brass'), finish='brass')]
        tled = (0, 0, 222)
        R, H = 100, 100
        P += [Part('dome', ball(R, 9, (0, 0, 0), cut_below=0) - cyl(50, R - 30, R + 1), Machined('cast-acrylic'), finish='body'),
              Part('liner', ball(R - 9 - GAP, LT, (0, 0, 0), cut_below=4) - cyl(50, R - 30, R + 1), Machined('cast-acrylic'),
                   finish='liner'),
              Part('skin', ball(R - 9 - 2 * GAP - LT, 3, (0, 0, 0), cut_below=0) - cyl(50, R - 30, R + 1),
                   Machined('cast-acrylic'), finish='body'),
              Part('baffle', cyl(48, 55, R + 6) - cyl(42, 54, R - 8), Machined('brass'), finish='brass')]
        pled = (0, 0, 88)
        metal = 'brass'
    elif key in ('s2', 's3'):
        sq = key == 's2'
        body = (lambda w, z0, z1, r: rsq(w, z0, z1, r)) if sq else (lambda w, z0, z1, r: cyl(w, z0, z1))
        T += [Part('shade', body(110, 22, 262, 16) - body(86, 21, 263, 6), Machined('cast-acrylic'), finish='body'),
              Part('liner', body(84, 26, 258, 5) - body(84 - 2 * LT, 25, 259, 4), Machined('cast-acrylic'), finish='liner'),
              Part('cap', body(110, 262, 272, 16), Machined('steel'), finish='steel')]
        tled = (0, 0, 150)
        H = 170
        P += [Part('shade', body(180, 0, H, 24) - body(152, -1, H + 1, 10), Machined('cast-acrylic'), finish='body'),
              Part('liner', body(150, 8, H - 4, 9) - body(150 - 2 * LT, 7, H - 3, 8), Machined('cast-acrylic'), finish='liner'),
              Part('skin', body(150 - 2 * LT - 2 * GAP, 0, H - 4, 8) - body(150 - 2 * LT - 2 * GAP - 6, -1, H - 3, 6),
                   Machined('cast-acrylic'), finish='body'),
              Part('cap', body(180, H, H + 14, 24), Machined('steel'), finish='steel')]
        pled = (0, 0, 130)
    elif key == 's4':
        c = (0, 0, 180)
        T += [Part('column', cyl(40, 22, 112), Machined('cast-acrylic'), finish='body'),
              Part('collar', cyl(54, 106, 116), Machined('brass'), finish='brass'),
              Part('ball', ball(75, 9, c) - cyl(44, 100, 120), Machined('cast-acrylic'), finish='body'),
              Part('liner', ball(75 - 9 - GAP, LT, c) - cyl(44, 100, 130), Machined('cast-acrylic'), finish='liner')]
        tled = c
        R = 100
        c = (0, 0, R)
        P += [Part('ball', ball(R, 9, c, cut_below=16), Machined('cast-acrylic'), finish='body'),
              Part('liner', ball(R - 9 - GAP, LT, c, cut_below=22), Machined('cast-acrylic'), finish='liner'),
              Part('skin', ball(R - 9 - 2 * GAP - LT, 3, c, cut_below=16), Machined('cast-acrylic'), finish='body')]
        H = 2 * R - 2
        pled = (0, 0, 140)
    else:
        T += [Part('column', cyl(32, 22, 200), Machined('cast-acrylic'), finish='body'),
              Part('shade', cone_shell(K, 85, 32, 175, 265, 8) - cyl(30, 250, 270), Machined('cast-acrylic'), finish='body'),
              Part('liner', cone_shell(K, 85 - 8 - GAP, 32 - 8 - GAP, 181, 259, LT) - cyl(30, 250, 270),
                   Machined('cast-acrylic'), finish='liner'),
              Part('skin', cone_shell(K, 85 - 8 - 2 * GAP - LT, 32 - 8 - 2 * GAP - LT, 175, 255, 3) - cyl(30, 250, 270),
                   Machined('cast-acrylic'), finish='body'),
              Part('cap', cyl(40, 262, 276), Machined('brass'), finish='brass')]
        tled = (0, 0, 228)
        H = 200
        P += [Part('shade', cone_shell(K, 95, 30, 0, H, 9), Machined('cast-acrylic'), finish='body'),
              Part('liner', cone_shell(K, 95 - 9 - GAP, 30 - 9 - GAP, 8, H - 6, LT), Machined('cast-acrylic'), finish='liner'),
              Part('skin', cone_shell(K, 95 - 9 - 2 * GAP - LT, 30 - 9 - 2 * GAP - LT, 0, H - 10, 3), Machined('cast-acrylic'),
                   finish='body'),
              Part('cap', cyl(64, H, H + 12), Machined('brass'), finish='brass')]
        pled = (0, 0, 150)
        metal = 'brass'
    P += [Part('cord', cyl(6, H + 12, H + 600), Bought('x'), finish='cord'),
          Part('canopy', cyl(110, H + 600, H + 640), Machined(metal), finish=metal)]
    return T, tled, P, pled


def build():
    K = _kit()
    import render as fk_render
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for key, title in SHAPES.items():
        table, tled, pend, pled = shape(key)
        for kind, parts in (('table', table), ('pendant', pend)):
            name = f'{key}-{kind}'
            prod = K.Product(name, f'{title} {kind}', 'bar lamp study', params={}, parts=lambda P, parts=parts: parts,
                             materials=MATERIALS, variants=B.VARIANTS)
            fk_render.write(prod, parts, os.path.join(OUT, name), engine_file=os.path.join(OUT, f'{name}.json'), proof=False)
        meta[key] = {'table_light_mm': tled, 'pendant_light_mm': pled}
        print(key, title, flush=True)
    json.dump(meta, open(os.path.join(OUT, 'lights.json'), 'w'), indent=1)
    shots()


def shot(key, where, colour, tled, pled):
    s = MS.shot(where, colour)
    tx, ty, px, py = -0.12, 0.0, 0.26, 0.18
    s['title'] = f'{SHAPES[key]} in {colour}, {where} (the liner inside)'
    s['set']['props'] = [p for p in s['set']['props'] if p.get('module') != 'earf_moon']
    rel = 'spinoffs/barkhorn/companions/out-study'
    s['products'] = [{'def': f'{rel}/{key}-table.json', 'flavour': colour,
                      'instances': [{'position': [tx, ty, MS.TABLE_Z], 'rotate_z': 12}]},
                     {'def': f'{rel}/{key}-pendant.json', 'flavour': colour,
                      'instances': [{'position': [px, py, MS.PEND_Z], 'rotate_z': 0}]}]
    # the tint carries the glow: cast at the Clouds' 25 mm depth in these 8 to 12 mm walls, the liner dim behind it
    # (smoked is near black at that depth: cast lighter, so it glows a smoky amber)
    s['materials'] = {'body': {'radius': 0.008 if colour == 'smoked' else 0.005}, 'liner': {'glow': 0.25}}
    tw, pw = WATTS.get(key, (14.0, 9.0))
    s['lights']['tlamp'] = B.hidden_point((tx + tled[0] / 1000, ty + tled[1] / 1000, MS.TABLE_Z + tled[2] / 1000), tw)
    s['lights']['pend'] = B.hidden_point((px + pled[0] / 1000, py + pled[1] / 1000, MS.PEND_Z + pled[2] / 1000), pw)
    return s


def shots():
    os.makedirs(SHOTS, exist_ok=True)
    meta = json.load(open(os.path.join(OUT, 'lights.json')))
    for key in SHAPES:
        for where, colour in VIEWS:
            json.dump(shot(key, where, colour, meta[key]['table_light_mm'], meta[key]['pendant_light_mm']),
                      open(os.path.join(SHOTS, f'{key}-{where}-{colour}.json'), 'w'), indent=1)


def render():
    py = os.environ.get('PY', 'python3')
    a = sys.argv[2:]
    scale = a[a.index('--scale') + 1] if '--scale' in a else '0.6'
    only = [k for k in a if k in SHAPES] or list(SHAPES)
    os.makedirs(RENDERS, exist_ok=True)
    for key in only:
        for where, colour in VIEWS:
            name = f'{key}-{where}-{colour}'
            subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, name + '.json'),
                            '--out', os.path.join(RENDERS, name + '.png'), '--scale', scale], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(name, flush=True)


def sheet():
    tiles = ' '.join(f"-label '{SHAPES[k]}, {c}' {os.path.join(RENDERS, f'{k}-bar-{c}.png')}"
                     for c in ('smoked', 'ember') for k in SHAPES)
    out = os.path.join(RENDERS, 'sheet.png')
    subprocess.run(f"montage {tiles} -tile {len(SHAPES)}x2 -geometry 360x400+4+4 -pointsize 15 -background '#F2F0EC' "
                   f"-depth 8 {out}", shell=True, check=True)
    print(out)


if __name__ == '__main__':
    if '--render' in sys.argv:
        render()
    elif '--sheet' in sys.argv:
        sheet()
    else:
        build()
