"""Round 31c's companions, v2: the owner's notes of 2026-10-18 (evening), through the coordinator:

    "I'm not loving the record player and lamp. I want a squared record player similar to a debut or orbit but with a
    clear body and matching cover." "The brian eno one and the audio technica hotaru are acrylic I think and look
    really cool when backlit, but are way too expensive." "The lamp, I liked the squared on you had. Or cylindrical
    could be cool. I like spherical too. I also am a fan of shag lamps."

Quick blockouts for the owner to pick from, each by day in three colours and lit at dusk, on one comparison sheet:

- R1 Slab: one 25 mm slab in the Orbit's way, the motor outboard in its own pod, edge-lit (an LED strip in a groove
  under the back edge; the polished edges glow), a hinged cover in the same tint.
- R2 Sandwich: a water-clear 19 mm core between 3 mm tinted skins, so the light guide stays clear and only the skins
  carry the colour (T1 went muddy at 60 mm of tint); the motor under the plinth, the Debut's way; the core's edges glow.
- R3 Float: the slab raised 30 mm on four clear posts over a 10 mm lit base that glows round its edge, the platter
  above a ring of light (the Hotaru's idea, without its magnets).
- L1 Lantern (the owner liked it), L4 Cylinder, L5 Sphere, L6 Shag: a fountain of 3 mm acrylic rods from a lit core,
  their tips glowing (the seventies fibre-optic lamp, in EARF's acrylic).

    .venv-fab/bin/python spinoffs/barkhorn/companions/concepts2.py      # the models and their shots
    PY=python3.11 spinoffs/barkhorn/companions/concepts2.py --render    # render them all small and make the sheet
"""
import json, math, os, random, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import common as C                                                 # noqa: E402

OUT = os.path.join(HERE, 'out-concepts2')
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'companions2')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'companions2', 'concepts')
DAY = ['ember', 'ice', 'haze']                 # three colours by day
DUSK = 'haze'                                  # and one lit at dusk


def _kit():
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
    import kit
    return kit


def rrect_slab(K, w, d, z0, z1, r, cx, cy):
    return K.prism(K.rounded_rect(w, d, r, cx=cx, cy=cy), 'z', z0, z1)


def edge_ring(K, w, d, z0, z1, r, cx, cy, t=0.6):
    """The polished edges of a slab lit through it: a thin skin round its outline, glowing."""
    return rrect_slab(K, w + 2 * t, d + 2 * t, z0, z1, r + t, cx, cy) - rrect_slab(K, w + 0.02, d + 0.02, z0 - 1, z1 + 1, r, cx, cy)


def arm(K, px, py, z):
    """A stock arm (Pro-Ject's or Rega's), resting: a pillar, the tube to the front, a headshell, a counterweight."""
    from build123d import Pos, Rot
    h = z + 40
    L = 230
    a = -95.0
    tube = Pos(px, py, h) * Rot(0, 0, a) * Pos(L / 2, 0, 0) * Rot(0, 90, 0) * K.cyl('z', (0, 0), 8, -L / 2, L / 2)
    cw = Pos(px, py, h) * Rot(0, 0, a) * Rot(0, 90, 0) * K.cyl('z', (0, 0), 30, -60, -35)
    base = K.union(K.cyl('z', (px, py), 40, z, z + 8), K.cyl('z', (px, py), 22, z + 8, h - 6), K.box(px - 12, py - 10, h - 8, px + 12, py + 10, h + 8))
    ex, ey = px + L * math.cos(math.radians(a)), py + L * math.sin(math.radians(a))
    head = K.box(ex - 10, ey - 14, h - 20, ex + 10, ey + 14, h + 3)
    return K.union(base, tube, cw, head)


def turntable(kind):
    K = _kit()
    Part, Sheet, Bought, Machined = K.Part, K.Sheet, K.Bought, K.Machined
    W, D, T, R = 430.0, 340.0, 25.0, 10.0
    cx, cy = W / 2, D / 2
    sx, sy = 175.0, 170.0                         # the spindle
    lift = 30.0 if kind == 'r3' else 0.0
    feet_h = 12.0
    z0 = feet_h + lift + (10.0 if kind == 'r3' else 0.0)
    z1 = z0 + T
    parts = []
    if kind == 'r2':
        parts += [Part('skin-lower', rrect_slab(K, W, D, z0, z0 + 3, R, cx, cy), Sheet('cast-acrylic', 6), finish='acrylic-dense'),
                  Part('core', rrect_slab(K, W, D, z0 + 3, z1 - 3, R, cx, cy), Sheet('cast-acrylic', 20), finish='clear'),
                  Part('skin-upper', rrect_slab(K, W, D, z1 - 3, z1, R, cx, cy), Sheet('cast-acrylic', 6), finish='acrylic-dense'),
                  Part('edge', edge_ring(K, W, D, z0 + 3, z1 - 3, R, cx, cy), Bought('x'), finish='glow')]
    else:
        parts += [Part('plinth', rrect_slab(K, W, D, z0, z1, R, cx, cy), Sheet('cast-acrylic', 25), finish='acrylic'),
                  Part('edge', edge_ring(K, W, D, z0, z1, R, cx, cy), Bought('x'), finish='glow')]
    if kind == 'r3':
        bz0, bz1 = feet_h, feet_h + 10
        parts += [Part('base', rrect_slab(K, W + 20, D + 20, bz0, bz1, R + 10, cx, cy), Sheet('cast-acrylic', 10), finish='acrylic'),
                  Part('base-edge', edge_ring(K, W + 20, D + 20, bz0, bz1, R + 10, cx, cy), Bought('x'), finish='glow'),
                  Part('posts', K.union(*(K.cyl('z', (x, y), 20, bz1, z0) for x, y in ((40, 40), (W - 40, 40), (40, D - 40), (W - 40, D - 40)))),
                       Machined('cast-acrylic'), finish='clear')]
    parts += [Part('platter', K.cyl('z', (sx, sy), 300, z1 + 4, z1 + 24), Sheet('cast-acrylic', 20), finish='acrylic'),
              Part('label', K.cyl('z', (sx, sy), 100, z1 + 24, z1 + 24.4), Bought('x'), finish='accent'),
              Part('spindle', K.cyl('z', (sx, sy), 7.2, z1 + 24, z1 + 40), Machined('stainless'), finish='steel'),
              Part('arm', arm(K, W - 70, D - 75, z1), Bought('x'), finish='arm'),
              Part('feet', K.union(*(K.cyl('z', (x, y), 40, 0, feet_h) for x, y in ((40, 40), (W - 40, 40), (40, D - 40), (W - 40, D - 40)))),
                   Bought('x'), finish='rubber')]
    if kind == 'r1':                              # the Orbit's outboard motor, in its own acrylic pod at the back left
        parts += [Part('pod', K.cyl('z', (-38, D - 60), 60, 0, z1 + 14), Machined('cast-acrylic'), finish='acrylic'),
                  Part('pulley', K.cyl('z', (-38, D - 60), 22, z1 + 14, z1 + 24), Machined('aluminium'), finish='aluminium')]
    else:                                         # the Debut's motor under the plinth, its pulley through a hole
        parts += [Part('pulley', K.cyl('z', (40, D - 60), 22, z1, z1 + 14), Machined('aluminium'), finish='aluminium')]
    # the cover: 4 mm sheet in the same tint, hinged at the back, closed
    ch = 95.0
    ctop = z1 + ch
    shell = rrect_slab(K, W, D, z1 + 2, ctop, R, cx, cy) - rrect_slab(K, W - 8, D - 8, z1 + 1, ctop - 4, max(R - 4, 1), cx, cy)
    parts += [Part('cover', shell, Sheet('cast-acrylic', 4), finish='acrylic')]
    return parts


def lamp(kind):
    K = _kit()
    Part, Sheet, Bought, Machined = K.Part, K.Sheet, K.Bought, K.Machined
    c = (150.0, 150.0)
    if kind == 'l1':                              # the Lantern: five 20 mm panels round an opal tube
        W, H, T = 180.0, 320.0, 20.0
        x0, y0 = c[0] - W / 2, c[1] - W / 2
        sides = [K.box(x0, y0, 20, x0 + T, y0 + W, H), K.box(x0 + W - T, y0, 20, x0 + W, y0 + W, H),
                 K.box(x0 + T, y0, 20, x0 + W - T, y0 + T, H), K.box(x0 + T, y0 + W - T, 20, x0 + W - T, y0 + W, H),
                 K.box(x0, y0, H, x0 + W, y0 + W, H + T)]
        return [Part(f'panel-{i}', s, Sheet('cast-acrylic', 20), finish='acrylic') for i, s in enumerate(sides)] + [
            Part('base', K.box(x0, y0, 0, x0 + W, y0 + W, 20), Sheet('cast-acrylic', 20), finish='acrylic-satin'),
            Part('core', K.cyl('z', c, 70, 20, H - 10), Bought('x'), finish='glow')]
    if kind == 'l4':                              # the Cylinder: a cast tube 200 x 5 on a disc, an opal core
        return [Part('tube', K.cyl('z', c, 200, 20, 340) - K.cyl('z', c, 190, 19, 341), Machined('cast-acrylic'), finish='acrylic-dense'),
                Part('cap', K.cyl('z', c, 204, 340, 352), Sheet('cast-acrylic', 12), finish='acrylic'),
                Part('foot', K.cyl('z', c, 220, 0, 20), Sheet('cast-acrylic', 20), finish='acrylic'),
                Part('core', K.cyl('z', c, 60, 20, 300), Bought('x'), finish='glow')]
    if kind == 'l5':                              # the Sphere: a blown acrylic globe 300 on a turned neck and a foot
        from build123d import Sphere, Pos
        g = Pos(c[0], c[1], 210) * Sphere(150) - Pos(c[0], c[1], 210) * Sphere(146)
        g = g - K.cyl('z', c, 80, 50, 80)
        return [Part('globe', g, Machined('cast-acrylic-formed', 'formed'), finish='acrylic-dense'),
                Part('neck', K.cyl('z', c, 84, 20, 70) - K.cyl('z', c, 76, 19, 71), Machined('cast-acrylic'), finish='acrylic'),
                Part('foot', K.cyl('z', c, 170, 0, 20), Sheet('cast-acrylic', 20), finish='acrylic'),
                Part('core', Pos(c[0], c[1], 200) * Sphere(45), Bought('x'), finish='glow')]
    # L6 Shag: 3 mm rods fanned out of a lit core in a turned foot, their polished tips glowing
    from build123d import Pos, Rot, Sphere, Compound
    rnd = random.Random(31)
    rods, tips = [], []
    for i in range(260):
        tilt = math.degrees(math.acos(1 - rnd.random() * (1 - math.cos(math.radians(62)))))
        az = rnd.uniform(0, 360)
        L = rnd.uniform(240, 330)
        base = (c[0] + rnd.uniform(-14, 14), c[1] + rnd.uniform(-14, 14), 96)
        tr = Pos(*base) * Rot(0, 0, az) * Rot(0, tilt, 0)
        rods.append(tr * K.cyl('z', (0, 0), 3, 0, L))
        tips.append(tr * Pos(0, 0, L) * Sphere(2.4))
    return [Part('foot', K.cyl('z', c, 180, 0, 70), Machined('cast-acrylic'), finish='acrylic'),
            Part('crown', K.cyl('z', c, 70, 70, 100), Machined('cast-acrylic'), finish='acrylic'),
            Part('core', K.cyl('z', c, 50, 40, 98), Bought('x'), finish='glow'),
            Part('rods', Compound(children=rods), Machined('cast-acrylic'), finish='acrylic-dense'),
            Part('tips', Compound(children=tips), Bought('x'), finish='glow')]


CONCEPTS = {'r1': ('R1 Slab', 'turntable'), 'r2': ('R2 Sandwich', 'turntable'), 'r3': ('R3 Float', 'turntable'),
            'l1': ('L1 Lantern', 'lamp'), 'l4': ('L4 Cylinder', 'lamp'), 'l5': ('L5 Sphere', 'lamp'), 'l6': ('L6 Shag', 'lamp')}
MATERIALS = dict(C.MATERIALS, clear={'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#F4F6F5', 'radius': 0.05, 'roughness': 0.04})


def shot(key, colour, dusk):
    tt = CONCEPTS[key][1] == 'turntable'
    H = 0.16 if tt else 0.4
    tgt = [0.0, 0.0, round(H * 0.5, 3)]
    el, az, dist = (26, -28, 1.15) if tt else (10, -24, 1.55)
    cam = [round(dist * math.cos(math.radians(el)) * math.sin(math.radians(az)), 3),
           round(-dist * math.cos(math.radians(el)) * math.cos(math.radians(az)), 3), round(tgt[2] + dist * math.sin(math.radians(el)), 3)]
    k = 0.08 if dusk else 1.0
    s = {'title': f'{CONCEPTS[key][0]} in {C.NAMES[colour]}' + (', lit at dusk' if dusk else ''), 'size': [900, 720],
         'product': {'def': f'spinoffs/barkhorn/companions/out-concepts2/{key}.json', 'flavour': colour,
                     'instances': [{'position': [0, 0, 0], 'rotate_z': 0}]},
         'set': {'kind': 'sweep', 'color': '#3A3D4A' if dusk else C.SWEEP[colour], 'width': 6.0, 'front': 5.0, 'depth': 1.5,
                 'radius': 1.2, 'height': 4.0},
         'camera': {'position': cam, 'target': tgt, 'lens_mm': 55 if tt else 60, 'level': True},
         'lights': {'key': {'type': 'area', 'size_m': [2.0, 1.6], 'orbit': {'azimuth_deg': -35, 'elevation_deg': 42, 'distance_m': 3.0},
                            'target': tgt, 'irradiance': round(2.2 * k, 3), 'color': '#C9D6F0' if dusk else '#FFF3E1'},
                    'fill': {'type': 'area', 'size_m': [2.5, 2.0], 'orbit': {'azimuth_deg': 35, 'elevation_deg': 18, 'distance_m': 3.0},
                             'target': tgt, 'irradiance': round(0.9 * k, 3), 'color': '#FFF7EA'}},
         'sky': {'kind': 'gradient', 'zenith': '#C4C2BE', 'horizon': '#CFCDC8', 'ground': '#5A5650', 'strength': round(0.7 * k, 3)},
         # lit, the glow parts emit; by day they are the clear acrylic they are (an unlit emitter renders black)
         'materials': {'glow': {'strength': 8.0} if dusk else {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#F4F6F5',
                                                                'radius': 0.05, 'roughness': 0.04}},
         'render': {'samples': 48, 'adaptive': 0.03, 'denoise': True, 'clamp': 8, 'bounces': 12, 'view': 'Khronos PBR Neutral',
                    'exposure': 0.0, 'white_balance_k': 5600}}
    return s


def build():
    K = _kit()
    import render as fk_render
    os.makedirs(OUT, exist_ok=True); os.makedirs(SHOTS, exist_ok=True)
    for key, (title, kind) in CONCEPTS.items():
        parts = turntable(key) if kind == 'turntable' else lamp(key)
        prod = K.Product(key, title, 'concept blockout', params={}, parts=lambda P, parts=parts: parts, materials=MATERIALS,
                         variants=C.VARIANTS)
        fk_render.write(prod, parts, os.path.join(OUT, key), engine_file=os.path.join(OUT, f'{key}.json'), proof=False)
        for col in DAY:
            json.dump(shot(key, col, False), open(os.path.join(SHOTS, f'concept-{key}-{col}.json'), 'w'), indent=1)
        json.dump(shot(key, DUSK, True), open(os.path.join(SHOTS, f'concept-{key}-dusk.json'), 'w'), indent=1)
        print(key, title, flush=True)


def render_all():
    py = os.environ.get('PY', 'python3')
    os.makedirs(RENDERS, exist_ok=True)
    for key in CONCEPTS:
        for v in DAY + ['dusk']:
            name = f'concept-{key}-{v}'
            subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, name + '.json'),
                            '--out', os.path.join(RENDERS, name + '.png'), '--scale', '0.5'], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(name, flush=True)
    # the sheet: a row a concept, its three colours by day and lit at dusk, labelled
    rows = [' '.join(os.path.join(RENDERS, f'concept-{k}-{v}.png') for v in DAY + ['dusk']) for k in CONCEPTS]
    labels = ' '.join(f"-label '{CONCEPTS[k][0]}, {C.NAMES[v] if v != 'dusk' else 'lit at dusk'}' {os.path.join(RENDERS, f'concept-{k}-{v}.png')}"
                      for k in CONCEPTS for v in DAY + ['dusk'])
    sheet = os.path.join(RENDERS, 'sheet.png')
    subprocess.run(f"montage {labels} -tile 4x{len(CONCEPTS)} -geometry 450x360+4+4 -pointsize 16 -background '#F2F0EC' -depth 8 {sheet}",
                   shell=True, check=True)
    print(sheet)


if __name__ == '__main__':
    render_all() if '--render' in sys.argv else build()
