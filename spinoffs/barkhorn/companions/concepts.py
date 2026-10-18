"""Round 31's companions, the concepts: three directions for the record player and three for the lamp, as quick
blockouts in the Clouds' acrylic, rendered small on the look book's sweep (README.md says what each is and which was
picked). Not fabrication: the picked two are built properly in turntable.py and lamp.py.

    .venv-fab/bin/python spinoffs/barkhorn/companions/concepts.py          # the six models and their shots
    python3.11 studio/engine/render.py studio/shots/barkhorn/companions/concept-t1.json --out ...   (shots.py renders all)
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
sys.path.insert(0, HERE)
from kit import *                                                  # noqa: E402,F403
import render as fk_render                                         # noqa: E402
import common as C                                                 # noqa: E402

OUT = os.path.join(HERE, 'out-concepts')
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'companions')
A = Sheet('cast-acrylic', 20)


def disc(cx, cy, d, z0, z1):
    return cyl('z', (cx, cy), d, z0, z1)


def arm(px, py, z, sx, sy):
    """A tonearm stand-in: a pillar at the pivot and a tube to the stylus at (sx, sy)."""
    L = math.hypot(sx - px, sy - py); a = math.degrees(math.atan2(sy - py, sx - px))
    from build123d import Pos, Rot
    tube = Pos(px, py, z + 28) * Rot(0, 0, a) * Pos(L / 2, 0, 0) * Rot(0, 90, 0) * cyl('z', (0, 0), 9, -L / 2, L / 2)
    return union(disc(px, py, 34, z, z + 32), tube, disc(px, py, 26, z + 24, z + 52).moved(Pos(-18 * math.cos(math.radians(a)), -18 * math.sin(math.radians(a)), 0)))


def t_slab():
    """T1, the Slab: three 20 mm sheets cemented into a 460 x 360 plinth, R40 corners, the platter 25 mm on it: the
    way most acrylic turntables are made."""
    pl = [prism(rounded_rect(460, 360, 40, cx=230, cy=180), 'z', 30 + 20 * i, 50 + 20 * i) for i in range(3)]
    px, py = 190, 190
    return [*(Part(f'plinth-{i}', s, A, finish='acrylic') for i, s in enumerate(pl)),
            Part('platter', disc(px, py, 300, 92, 117), Sheet('cast-acrylic', 25), finish='acrylic'),
            Part('spindle', disc(px, py, 10, 117, 135), Machined('stainless'), finish='steel'),
            Part('arm', arm(px + 190, py + 115, 90, px + 40, py - 60), Bought('x'), finish='arm'),
            Part('motor', disc(55, 320, 30, 90, 112), Bought('x'), finish='aluminium'),
            Part('feet', union(*(disc(x, y, 40, 0, 30) for x, y in ((50, 50), (410, 50), (50, 310), (410, 310)))), Bought('x'), finish='rubber')]


def t_cumulus():
    """T2, Cumulus: the plinth drawn as the icons are, of circles, one for each thing it holds (the platter's, the
    arm's, the motor's), two 20 mm sheets; the motor stands apart in its own circle, through a hole, on its own feet."""
    px, py = 200, 200
    ax, ay = px + 190, py + 115
    mx, my = px - 150, py + 135
    def layer(z0, z1, hole):
        s = union(disc(px, py, 340, z0, z1), disc(ax, ay, 150, z0, z1), disc(mx, my, 124, z0, z1))
        return s - disc(mx, my, 92, z0 - 1, z1 + 1) if hole else s
    return [Part('plinth-0', layer(30, 50, True), A, finish='acrylic'), Part('plinth-1', layer(50, 70, True), A, finish='acrylic'),
            Part('platter', disc(px, py, 300, 82, 107), Sheet('cast-acrylic', 25), finish='acrylic'),
            Part('spindle', disc(px, py, 10, 107, 125), Machined('stainless'), finish='steel'),
            Part('bearing', disc(px, py, 40, 5, 70), Machined('brass'), finish='brass'),
            Part('arm', arm(ax, ay, 70, px + 40, py - 60), Bought('x'), finish='arm'),
            Part('pod', disc(mx, my, 86, 12, 92), A, finish='acrylic'),
            Part('pulley', disc(mx, my, 40, 92, 104), Machined('aluminium'), finish='aluminium'),
            Part('feet', union(*(disc(x, y, 40, 0, 30) for x, y in ((px - 90, py - 110), (px + 110, py - 110), (ax + 20, ay + 20)))), Bought('x'), finish='rubber')]


def t_mast():
    """T3, the Mast: a skeleton. A round 20 mm foot, the bearing up a column of stacked discs, the platter floating on
    it; the arm and the motor each on a pillar of their own."""
    px, py = 190, 190
    ax, ay = px + 190, py + 115
    mx, my = px - 160, py + 120
    col = union(*(disc(px, py, 90 - 6 * i, 20 + 20 * i, 40 + 20 * i) for i in range(4)))
    return [Part('foot', disc(px, py, 260, 0, 20), A, finish='acrylic'),
            Part('column', col, A, finish='acrylic'),
            Part('platter', disc(px, py, 300, 112, 137), Sheet('cast-acrylic', 25), finish='acrylic'),
            Part('spindle', disc(px, py, 10, 137, 155), Machined('stainless'), finish='steel'),
            Part('arm-pillar', union(disc(ax, ay, 120, 0, 20), disc(ax, ay, 60, 20, 105)), A, finish='acrylic'),
            Part('arm', arm(ax, ay, 105, px + 40, py - 60), Bought('x'), finish='arm'),
            Part('motor-pillar', union(disc(mx, my, 90, 0, 20), disc(mx, my, 50, 20, 112)), A, finish='acrylic'),
            Part('pulley', disc(mx, my, 40, 112, 124), Machined('aluminium'), finish='aluminium')]


def l_lantern():
    """L1, the Lantern: the cabinet in small, five 20 mm panels cemented as the Clouds' are, 180 x 180 x 320, an opal
    tube inside round the LED, and a slot of the horn's mouth through the front."""
    W, H, T = 180, 320, 20
    sides = [box(0, 0, 30, T, W, H), box(W - T, 0, 30, W, W, H), box(T, 0, 30, W - T, T, H), box(T, W - T, 30, W - T, W, H),
             box(0, 0, H, W, W, H + T)]
    return [*(Part(f'panel-{i}', s, A, finish='acrylic') for i, s in enumerate(sides)),
            Part('base', box(0, 0, 0, W, W, 30), A, finish='acrylic-satin'),
            Part('diffuser', disc(W / 2, W / 2, 90, 30, H - 10) - disc(W / 2, W / 2, 84, 29, H - 9), Machined('cast-acrylic'), finish='opal'),
            Part('led', disc(W / 2, W / 2, 80, 30, H - 12), Bought('x'), finish='led')]


def l_edge():
    """L2, Edge: one 20 mm sheet cut to the horn's section (its flare either side, the rim rolled), standing in a
    cemented foot that hides an LED strip under its bottom edge; the polished edges carry the light."""
    fl = C.flare(30, 150, 360, n=24, m=2.2)
    out = [(170 + r, h + 60) for r, h in fl]
    pts = out + [(170 - r, h + 60) for r, h in reversed(fl)]
    sheet = prism(pts, 'y', 50, 70)
    return [Part('sheet', sheet, A, finish='acrylic'),
            Part('foot', box(60, 20, 0, 280, 100, 60) - box(138, 49, 20, 202, 71, 61), A, finish='acrylic-satin'),
            Part('led', box(140, 50, 50, 200, 70, 60), Bought('x'), finish='led')]


def l_bell():
    """L3, Bell: the horn turned up to the ceiling. Its flare formed from 5 mm tinted sheet, on a stem of acrylic tube,
    a foot of two 20 mm discs; the LED sits at the throat, where the speaker's compression driver sits."""
    cx = cy = 190
    pts, sm = C.shell_profile(C.flare(36, 185, 170), 5)
    shade = revolve_profile([(r, h + 330) for r, h in pts], axis='z', centre=(cx, cy, 0), smooth=sm)
    return [Part('foot', union(disc(cx, cy, 220, 0, 20), disc(cx, cy, 200, 20, 40)), A, finish='acrylic'),
            Part('stem', disc(cx, cy, 30, 40, 300) - disc(cx, cy, 22, 39, 301), Machined('cast-acrylic'), finish='acrylic'),
            Part('pod', disc(cx, cy, 82, 300, 336), A, finish='acrylic'),
            Part('shade', shade, Machined('cast-acrylic-formed', 'formed'), finish='acrylic'),
            Part('led', disc(cx, cy, 60, 336, 338), Bought('x'), finish='led')]


def l_bell_down():
    """L3b, Bell turned over: the same horn hung mouth down from the top of its stem, the LED at the throat facing the
    table behind an opal disc, so the light pools below and the flare glows in its colour (the upturned bell read as a
    trophy)."""
    cx = cy = 200
    pts, sm = C.shell_profile(C.flare(36, 200, 190), 5)
    top = 470
    shade = revolve_profile([(r, top - h) for r, h in pts], axis='z', centre=(cx, cy, 0), smooth=sm)
    return [Part('foot', union(disc(cx, cy, 230, 0, 20), disc(cx, cy, 210, 20, 40)), A, finish='acrylic'),
            Part('stem', disc(cx, cy, 30, 40, top - 30) - disc(cx, cy, 22, 39, top - 29), Machined('cast-acrylic'), finish='acrylic'),
            Part('pod', disc(cx, cy, 82, top - 34, top + 6), A, finish='acrylic'),
            Part('shade', shade, Machined('cast-acrylic-formed', 'formed'), finish='acrylic'),
            Part('diffuser', disc(cx, cy, 70, top - 40, top - 36), Machined('cast-acrylic'), finish='opal'),
            Part('led', disc(cx, cy, 60, top - 36, top - 34), Bought('x'), finish='led')]


CONCEPTS = {'t1': ('The Slab', t_slab, 'ember'), 't2': ('Cumulus', t_cumulus, 'ember'), 't3': ('The Mast', t_mast, 'ember'),
            'l1': ('The Lantern', l_lantern, 'acid'), 'l2': ('Edge', l_edge, 'acid'), 'l3': ('Bell', l_bell, 'acid'),
            'l3b': ('Bell, turned over', l_bell_down, 'acid')}


def shot(key, colour, lamp):
    """The look book's sweep and light (lookbook21), the camera three-quarter from the front-left and above, framed on
    the blockout; the lamp's LED lit."""
    H = 0.45 if lamp else 0.16
    tgt = [0.0, 0.0, round(H * 0.5, 3)]
    el, az, dist = (12, -28, 1.45) if lamp else (28, -26, 1.05)
    cam = [round(dist * math.cos(math.radians(el)) * math.sin(math.radians(az)), 3),
           round(-dist * math.cos(math.radians(el)) * math.cos(math.radians(az)), 3), round(tgt[2] + dist * math.sin(math.radians(el)), 3)]
    s = {'title': f'companions concept {key}', 'size': [900, 720],
         'product': {'def': f'spinoffs/barkhorn/companions/out-concepts/{key}.json', 'flavour': colour,
                     'instances': [{'position': [0, 0, 0], 'rotate_z': 0}]},
         'set': {'kind': 'sweep', 'color': C.SWEEP[colour], 'width': 6.0, 'front': 5.0, 'depth': 1.5, 'radius': 1.2, 'height': 4.0},
         'camera': {'position': cam, 'target': tgt, 'lens_mm': 60 if lamp else 55, 'level': True},
         'lights': {'key': {'type': 'area', 'size_m': [2.0, 1.6], 'orbit': {'azimuth_deg': -35, 'elevation_deg': 42, 'distance_m': 3.0},
                            'target': tgt, 'irradiance': 2.2, 'color': '#FFF3E1'},
                    'fill': {'type': 'area', 'size_m': [2.5, 2.0], 'orbit': {'azimuth_deg': 35, 'elevation_deg': 18, 'distance_m': 3.0},
                             'target': tgt, 'irradiance': 0.9, 'color': '#FFF7EA'},
                    'rim': {'type': 'area', 'size_m': [3.0, 0.8], 'position': [0.4, 1.6, 1.2], 'target': tgt, 'irradiance': 1.4, 'color': '#FFF7EA'}},
         'sky': {'kind': 'gradient', 'zenith': '#C4C2BE', 'horizon': '#CFCDC8', 'ground': '#5A5650', 'strength': 0.7},
         'render': {'samples': 48, 'adaptive': 0.03, 'denoise': True, 'clamp': 8, 'bounces': 12, 'view': 'Khronos PBR Neutral',
                    'exposure': 0.0, 'white_balance_k': 5600, 'white_balance_tint': 3.0}}
    if lamp:
        s['materials'] = {'led': {'strength': 40.0}}
    return s


def main():
    os.makedirs(OUT, exist_ok=True); os.makedirs(SHOTS, exist_ok=True)
    only = sys.argv[1:] or list(CONCEPTS)
    for key in only:
        title, fn, colour = CONCEPTS[key]
        parts = fn()
        prod = Product(key, title, 'concept blockout', params={}, parts=lambda P: parts, materials=C.MATERIALS, variants=C.VARIANTS)
        fk_render.write(prod, parts, os.path.join(OUT, key), engine_file=os.path.join(OUT, f'{key}.json'), proof=False)
        json.dump(shot(key, colour, key.startswith('l')), open(os.path.join(SHOTS, f'concept-{key}.json'), 'w'), indent=1)
        print(key, title, 'ok', flush=True)


if __name__ == '__main__':
    main()
