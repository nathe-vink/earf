"""Round 32's bar lamps (the owner, 2026-10-19: "We need to design an acrylic table lamp and hanging lamp that will work
well in a bar setting and that we can sell."), for Planet EARF and for sale beside the speakers. Three families, each a
cordless table lamp and a matching pendant, blocked out in the line's tints (the eight Tropos colours, and clear,
frosted and smoked), rendered in a bar (board-formed concrete, fir, blackened steel, 2700 K) and on a seamless.

What a bar asks (the coordinator's brief): the table lamp cordless and rechargeable on a staff tray, a base of 130 mm
or less, 250 to 300 mm tall, weighted, no LED seen from a seated guest's eye, warm-dim 2200 to 2700 K on a touch
dimmer, IP44 and wipeable; the pendant 150 to 200 mm across, a shielded source with a cut-off, 2700 K dimmable, its
driver in the canopy, listable; acrylic that does not look cheap: thick cast sections, crisp polished edges, satin-frosted
diffusers, edge glow as the signature, metal to anchor it; shapes from EARF's circle, square and rounded square.

- F1 Block (the rounded square of the cabinet): a 14 mm-walled rounded-square shade, milled from cast block, its
  outside polished and its inside satin, on a blackened-steel base that holds the battery; the light under a steel cap
  shines down into it. The pendant: the same shade, 180 square, its source recessed above a frosted diffuser.
- F2 Column (the circle): a 12 mm-walled cast tube on a brass foot, a frosted disc under its brass cap; the pendant the
  same tube, 170 across, its diffuser 50 mm up inside for the cut-off.
- F3 Moon (the circle, domed): a frosted dome turned from cast block on a solid tinted column that is lit from the base
  so its polished top and edges glow; the pendant a frosted dome under a 20 mm tinted disc whose polished edge glows.

Each light source is hidden from the camera and from transmission and the frosted parts carry their own glow
(`materials.frosted` glow, Planet's f7c99a4): Cycles passes a lamp's light through rough acrylic only as caustics.

    .venv-fab/bin/python spinoffs/barkhorn/companions/bar_lamps.py                # the models and their shots
    PY=python3.11 python3 spinoffs/barkhorn/companions/bar_lamps.py --render       # render and make the sheet
"""
import json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import common as C                                                 # noqa: E402

OUT = os.path.join(HERE, 'out-bar')
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'barlamps')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'barlamps')

# the line's tints: the eight colours, and clear, frosted and smoked (Planet's acrylic is only those three)
NEUTRAL = {'clear': ('#F4F6F5', '#F6F4F0', '#FF9A40'), 'frosted': ('#F2F2EF', '#F4F2EE', '#FF9A40'),
           'smoked': ('#6E655C', '#8E867E', '#FF8A30')}      # the glows amber: a 3000 K balance whitens a pale one
VARIANTS = {k: {'deep': deep, 'frost': deep, 'glow': C.GLOW[k], 'shade_glow': deep} for k, _, _, deep, _, _ in C.COLOURS}
for k, (deep, frost, glow) in NEUTRAL.items():
    VARIANTS[k] = {'deep': deep, 'frost': frost, 'glow': glow, 'shade_glow': '#FF9A50'}   # warm ivory at 2700 K (the coordinator: #FFB878 read lavender-white)
VARIANTS['frosted']['materials'] = {'body': {'preset': 'frosted', 'color': '#F4F2EE', 'absorb': '#EFE6D8', 'roughness': 0.5}}

MATERIALS = {
    'body': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.025, 'roughness': 0.04},
    'shade': {'preset': 'frosted', 'color': '$frost', 'absorb': '$deep', 'roughness': 0.5, 'radius': 0.02, 'clear': 0.1,
              'glow': 0.0, 'glow_color': '$shade_glow'},
    'edge': {'preset': 'emit', 'color': '$glow', 'strength': 0.0},
    'steel': {'preset': 'gunmetal', 'color': '#232120'},
    'brass': {'preset': 'metal', 'color': '#B8945A', 'roughness': 0.32},
    'cord': {'preset': 'rubber', 'color': '#151413'},
}


def _kit():
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
    import kit
    return kit


def rsq(K, w, z0, z1, r):
    return K.prism(K.rounded_rect(w, w, r), 'z', z0, z1)


def ring(K, solid_outer, solid_inner):
    return solid_outer - solid_inner


def family(key):
    """The family's table lamp and pendant as parts lists (mm, centred on the axis, z up from the table or from the
    pendant's lowest point), and where each one's light sits (mm)."""
    K = _kit()
    Part, Sheet, Bought, Machined = K.Part, K.Sheet, K.Bought, K.Machined
    from build123d import Sphere, Pos
    if key == 'f1':
        # table: steel base 120 sq x 30 (battery, charger contacts below), shade 110 sq 30..250, walls 14, cap 12
        base = rsq(K, 120, 0, 30, 18)
        shade = rsq(K, 110, 30, 250, 16) - rsq(K, 82, 29, 251, 4)
        edge_top = rsq(K, 110.6, 249, 250.6, 16.3) - rsq(K, 81.4, 248, 252, 3.7)
        cap = rsq(K, 110, 250, 262, 16) - rsq(K, 70, 249, 255, 6)
        diff = rsq(K, 81, 236, 240, 3.5)
        table = [Part('base', base, Machined('steel'), finish='steel'), Part('shade', shade, Machined('cast-acrylic'), finish='body'),
                 Part('edge-top', edge_top, Bought('x'), finish='edge'), Part('cap', cap, Machined('steel'), finish='steel'),
                 Part('diffuser', diff, Sheet('cast-acrylic', 4), finish='shade')]
        tled = (0, 0, 245)
        # pendant: 180 sq x 170 shade, walls 14, a frosted diffuser 50 up inside, steel cap, cord to a steel canopy
        H = 170
        pshade = rsq(K, 180, 0, H, 24) - rsq(K, 152, -1, H + 1, 10)
        pedge = rsq(K, 180.6, -0.6, 1.0, 24.3) - rsq(K, 151.4, -2, 2, 9.7)
        pdiff = rsq(K, 151, 50, 54, 9.5)
        pcap = rsq(K, 180, H, H + 14, 24)
        pled = (0, 0, H - 20)
    elif key == 'f1b':
        # F1 with a frosted lower section that lights the table (round 32, kept alive for the owner, who liked the
        # square): a steel base 120 sq x 22; a frosted rounded-square sleeve 110 sq, 22..130, walls 6, glowing with the
        # light inside it at 110 (hidden); a 4 mm steel shadow line; the tinted block above, 134..250, walls 14, its
        # polished top edge lit from below; a steel cap.
        base = rsq(K, 120, 0, 22, 18)
        low = rsq(K, 110, 22, 130, 16) - rsq(K, 98, 21, 131, 10)
        line = rsq(K, 106, 130, 134, 14) - rsq(K, 90, 129, 135, 6)
        shade = rsq(K, 110, 134, 250, 16) - rsq(K, 82, 133, 251, 4)
        edge_top = rsq(K, 110.6, 249, 250.6, 16.3) - rsq(K, 81.4, 248, 252, 3.7)
        cap = rsq(K, 110, 250, 262, 16) - rsq(K, 70, 249, 255, 6)
        table = [Part('base', base, Machined('steel'), finish='steel'), Part('lower', low, Machined('cast-acrylic'), finish='shade'),
                 Part('line', line, Machined('steel'), finish='steel'), Part('shade', shade, Machined('cast-acrylic'), finish='body'),
                 Part('edge-top', edge_top, Bought('x'), finish='edge'), Part('cap', cap, Machined('steel'), finish='steel')]
        tled = (0, 0, 100)
        # pendant: the 180 sq block, a frosted band 0..60 at its mouth, a steel shadow line, the tinted block 64..170;
        # open below, the light 120 up inside (cut-off about 32 deg from the vertical)
        H = 170
        pshade = rsq(K, 180, 64, H, 24) - rsq(K, 152, 63, H + 1, 10)
        pedge = rsq(K, 180, 0, 60, 24) - rsq(K, 168, -1, 61, 18)          # the frosted band (finish shade)
        pdiff = rsq(K, 176, 60, 64, 22) - rsq(K, 156, 59, 65, 12)         # the steel shadow line
        pcap = rsq(K, 180, H, H + 14, 24)
        pled = (0, 0, 120)
    elif key == 'f2':
        base = K.cyl('z', (0, 0), 120, 0, 28)
        shade = K.cyl('z', (0, 0), 110, 28, 228) - K.cyl('z', (0, 0), 86, 27, 229)
        edge_top = K.cyl('z', (0, 0), 110.6, 227, 228.6) - K.cyl('z', (0, 0), 85.4, 226, 230)
        cap = K.cyl('z', (0, 0), 110, 228, 242)
        diff = K.cyl('z', (0, 0), 85, 214, 218)
        table = [Part('base', base, Machined('brass'), finish='brass'), Part('shade', shade, Machined('cast-acrylic'), finish='body'),
                 Part('edge-top', edge_top, Bought('x'), finish='edge'), Part('cap', cap, Machined('brass'), finish='brass'),
                 Part('diffuser', diff, Sheet('cast-acrylic', 4), finish='shade')]
        tled = (0, 0, 224)
        H = 190
        pshade = K.cyl('z', (0, 0), 170, 0, H) - K.cyl('z', (0, 0), 146, -1, H + 1)
        pedge = K.cyl('z', (0, 0), 170.6, -0.6, 1.0) - K.cyl('z', (0, 0), 145.4, -2, 2)
        pdiff = K.cyl('z', (0, 0), 145, 50, 54)
        pcap = K.cyl('z', (0, 0), 170, H, H + 14)
        pled = (0, 0, H - 20)
    else:
        # table: steel base 120 x 24, a 40 solid tinted column lit from below, a frosted dome 150 on a brass ring
        base = K.cyl('z', (0, 0), 120, 0, 24)
        col = K.cyl('z', (0, 0), 40, 24, 190)
        col_edge = K.cyl('z', (0, 0), 40.6, 189, 190.8) - K.cyl('z', (0, 0), 30, 188, 192)
        ringb = K.cyl('z', (0, 0), 60, 190, 198)
        dome = (Pos(0, 0, 198) * Sphere(75)) - (Pos(0, 0, 198) * Sphere(67)) - K.box(-80, -80, 120, 80, 80, 198)
        table = [Part('base', base, Machined('steel'), finish='steel'), Part('column', col, Machined('cast-acrylic'), finish='body'),
                 Part('edge-top', col_edge, Bought('x'), finish='edge'), Part('ring', ringb, Machined('brass'), finish='brass'),
                 Part('dome', dome, Machined('cast-acrylic'), finish='shade')]
        tled = (0, 0, 230)
        # pendant: a frosted dome 200 under a 20 mm tinted disc 220 whose edge glows, a brass canopy
        R = 100
        # the dome hangs mouth down: the upper half of a 7 mm shell, its open rim at z = 0, its crown at z = R
        pdome = (Sphere(R) - Sphere(R - 7)) - K.box(-110, -110, -110, 110, 110, 0)
        pshade = pdome
        pdiff = K.cyl('z', (0, 0), 220, R, R + 20)
        pedge = K.cyl('z', (0, 0), 220.6, R + 0.5, R + 19.5) - K.cyl('z', (0, 0), 218, R, R + 20)
        pcap = K.cyl('z', (0, 0), 70, R + 20, R + 32)
        pled = (0, 0, R - 25)
        H = R + 20
    cord = K.cyl('z', (0, 0), 6, H + 14, H + 600)
    canopy = (rsq(K, 110, H + 600, H + 640, 14) if key in ('f1', 'f1b') else K.cyl('z', (0, 0), 110, H + 600, H + 640))
    metal = 'steel' if key in ('f1', 'f1b', 'f3') else 'brass'
    if key == 'f1b':
        return table, tled, [Part('shade', pshade, Machined('cast-acrylic'), finish='body'),
                             Part('lower', pedge, Machined('cast-acrylic'), finish='shade'),
                             Part('line', pdiff, Machined('steel'), finish='steel'),
                             Part('cap', pcap, Machined('steel'), finish='steel'),
                             Part('cord', cord, Bought('x'), finish='cord'),
                             Part('canopy', canopy, Machined('steel'), finish='steel')], pled
    pend = [Part('shade', pshade, Machined('cast-acrylic'), finish='body' if key != 'f3' else 'shade'),
            Part('edge', pedge, Bought('x'), finish='edge'),
            Part('diffuser', pdiff, Sheet('cast-acrylic', 4 if key != 'f3' else 20), finish='shade' if key != 'f3' else 'body'),
            Part('cap', pcap, Machined(metal), finish=metal if key != 'f3' else 'brass'),
            Part('cord', cord, Bought('x'), finish='cord'),
            Part('canopy', canopy, Machined(metal), finish=metal if key != 'f3' else 'brass')]
    return table, tled, pend, pled


FAMILIES = {'f1': 'F1 Block', 'f2': 'F2 Column', 'f3': 'F3 Moon'}
EXTRA = {'f1b': 'F1b Block, lit low'}     # round 32b: built and rendered on its own (f1b.py), off the sheet
VIEWS = [('bar', 'smoked'), ('bar', 'ember'), ('seamless', 'frosted'), ('seamless', 'haze')]
PEND_Z = 1.30          # the pendant's lowest point above the floor in the shots
TABLE_Z = 0.76         # the table's top


def hidden_point(pos, watts, colour=2700):
    return {'type': 'point', 'position': [round(v, 4) for v in pos], 'power_w': watts, 'radius_m': 0.02, 'color': colour,
            'camera': False, 'transmission': False, 'specular': 0.0}


def shot(fam, where, colour, tled, pled):
    bar = where == 'bar'
    tx, ty = -0.12, 0.0
    px, py = 0.26, 0.18
    tgt = [0.06, 0.05, 1.08]
    s = {'title': f'{FAMILIES[fam]} in {colour}, {where}', 'size': [900, 1000],
         'products': [{'def': f'spinoffs/barkhorn/companions/out-bar/{fam}-table.json', 'flavour': colour,
                       'instances': [{'position': [tx, ty, TABLE_Z], 'rotate_z': 12}]},
                      {'def': f'spinoffs/barkhorn/companions/out-bar/{fam}-pendant.json', 'flavour': colour,
                       'instances': [{'position': [px, py, PEND_Z], 'rotate_z': 0}]}],
         'camera': {'position': [-0.40, -1.20, 1.10], 'target': tgt, 'lens_mm': 45, 'level': True, 'fstop': 4.0,
                    'focus': [tx, ty, TABLE_Z + 0.15]},
         'render': {'samples': 64, 'adaptive': 0.03, 'denoise': True, 'clamp': 8, 'bounces': 12, 'view': 'Khronos PBR Neutral',
                    'exposure': 0.6 if bar else 0.0, 'white_balance_k': 3000 if bar else 5200}}
    glow = 3.0 if bar else 1.2
    s['materials'] = {'shade': {'glow': glow}, 'edge': {'strength': 3.5 if bar else 1.5}}
    table_top = {'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'brown_planks_09', 'res': '2k', 'color': '#6E4A2E',
                 'size': [0.9, 0.7, 0.04], 'position': [-0.05, 0.05, TABLE_Z - 0.04]}
    lights = {'tlamp': hidden_point((tx + tled[0] / 1000, ty + tled[1] / 1000, TABLE_Z + tled[2] / 1000), 4.0 if bar else 2.0),
              'pend': hidden_point((px + pled[0] / 1000, py + pled[1] / 1000, PEND_Z + pled[2] / 1000), 14.0 if bar else 6.0)}
    if bar:
        s['set'] = {'kind': 'sweep', 'color': '#2B2724', 'width': 8.0, 'front': 5.0, 'depth': 1.5, 'radius': 0.6, 'height': 4.0,
                    'props': [{'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'concrete_wall_008', 'res': '2k',
                               'color': '#8C857C', 'size': [4.0, 0.05, 3.0], 'position': [0.0, 0.75, 0.0]}, table_top]}
        s['sky'] = {'kind': 'gradient', 'zenith': '#1A1C22', 'horizon': '#24221F', 'ground': '#141210', 'strength': 0.25}
        lights['fill'] = {'type': 'area', 'size_m': [1.5, 1.2], 'orbit': {'azimuth_deg': -40, 'elevation_deg': 30, 'distance_m': 3.0},
                          'target': tgt, 'irradiance': 0.14, 'color': 2700}
    else:
        s['set'] = {'kind': 'sweep', 'color': '#D9D6D0', 'width': 8.0, 'front': 5.0, 'depth': 1.5, 'radius': 1.2, 'height': 4.0,
                    'props': [{'kind': 'kit', 'shape': 'box', 'material': 'felt', 'color': '#C9C4BC', 'size': [0.6, 0.45, TABLE_Z],
                               'position': [-0.12, 0.05, 0.0]}]}
        s['sky'] = {'kind': 'gradient', 'zenith': '#C4C2BE', 'horizon': '#CFCDC8', 'ground': '#5A5650', 'strength': 0.7}
        lights['key'] = {'type': 'area', 'size_m': [2.0, 1.6], 'orbit': {'azimuth_deg': -35, 'elevation_deg': 42, 'distance_m': 3.0},
                         'target': tgt, 'irradiance': 1.8, 'color': '#FFF3E1'}
        lights['fill'] = {'type': 'area', 'size_m': [2.5, 2.0], 'orbit': {'azimuth_deg': 35, 'elevation_deg': 18, 'distance_m': 3.0},
                          'target': tgt, 'irradiance': 0.7, 'color': '#FFF7EA'}
    s['lights'] = lights
    return s


def build():
    K = _kit()
    import render as fk_render
    os.makedirs(OUT, exist_ok=True); os.makedirs(SHOTS, exist_ok=True)
    meta = {}
    for fam, title in FAMILIES.items():
        table, tled, pend, pled = family(fam)
        for kind, parts in (('table', table), ('pendant', pend)):
            name = f'{fam}-{kind}'
            prod = K.Product(name, f'{title} {kind}', 'bar lamp blockout', params={}, parts=lambda P, parts=parts: parts,
                             materials=MATERIALS, variants=VARIANTS)
            fk_render.write(prod, parts, os.path.join(OUT, name), engine_file=os.path.join(OUT, f'{name}.json'), proof=False)
        meta[fam] = {'table_light_mm': tled, 'pendant_light_mm': pled}
        for where, colour in VIEWS:
            json.dump(shot(fam, where, colour, tled, pled), open(os.path.join(SHOTS, f'{fam}-{where}-{colour}.json'), 'w'), indent=1)
        print(fam, title, flush=True)
    json.dump(meta, open(os.path.join(OUT, 'lights.json'), 'w'), indent=1)


def render_all():
    py = os.environ.get('PY', 'python3')
    os.makedirs(RENDERS, exist_ok=True)
    only = [a for a in sys.argv[2:] if a in FAMILIES] or list(FAMILIES)
    for fam in only:
        for where, colour in VIEWS:
            name = f'{fam}-{where}-{colour}'
            subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, name + '.json'),
                            '--out', os.path.join(RENDERS, name + '.png'), '--scale', '0.6'], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(name, flush=True)
    labels = ' '.join(f"-label '{FAMILIES[f]}: {w}, {c}' {os.path.join(RENDERS, f'{f}-{w}-{c}.png')}" for f in FAMILIES for w, c in VIEWS)
    sheet = os.path.join(RENDERS, 'sheet.png')
    subprocess.run(f"montage {labels} -tile 4x{len(FAMILIES)} -geometry 450x500+4+4 -pointsize 16 -background '#F2F0EC' -depth 8 {sheet}",
                   shell=True, check=True)
    print(sheet)


if __name__ == '__main__':
    render_all() if '--render' in sys.argv else build()
