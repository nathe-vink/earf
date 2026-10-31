"""Planet EARF, round 42: the pop-up's axonometric, from popup42.py, with axo42's materials and solids.

    python3.11 spinoffs/barkhorn/planet/r42/popaxo42.py OUT.png [--scale 0.5] [--samples 64]
"""
import math, os, sys

import bpy
import mathutils

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import popup42 as Q                                                 # noqa: E402
import axo42 as A                                                   # noqa: E402

TINTS = ['#c8452f', '#d27a3a', '#d9b43c', '#5d8a4a', '#6fa8c8', '#8b6fb0', '#e9e7e2', '#4a4a50']


def build():
    m = A.mat
    M = dict(floor=m('pfloor', '#b9b2a7', 0.55), wall=m('pwall', '#e9e5de', 0.85), cut=m('pcut', '#3a3835', 0.9),
             glass=m('pglass', '#cfe0e6', 0.05, trans=0.9), oak=m('poak', '#9c7a52', 0.5), dark=m('pdark', '#2a2826', 0.6),
             shelf=m('pshelf', '#efe9df', 0.8), walnut=m('pwalnut', '#4e3a2a', 0.45), felt=m('pfelt', '#5b2a22', 0.95),
             tropos=m('ptropos', '#3d3c42', 0.15), plinth=m('pplinth', '#1f1e1c', 0.6), chair=m('pchair', '#8a7058', 0.7),
             white=m('pwhite', '#f3f1ec', 0.3), hemi=m('phemi', '#2b2a28', 0.3), glow=m('pglow', '#ffcf8a', 0.5, emit='#ffb15a', strength=6.0),
             cord=m('pcord', '#1a1a1a', 0.5), rug=m('prug', '#6e5a48', 0.95))
    W, L, T, CUT, LOW = Q.W, Q.L, 0.25, 2.6, 1.0
    A.box(-0.3, -T, -0.2, L + T, W + T, 0.0, M['floor'])
    A.box(-0.3, -T, 0, L + T, 0, LOW, M['wall']); A.box(-0.3, -T, LOW, L + T, 0, LOW + 0.01, M['cut'])
    for (x0, y0, x1, y1) in [(0, W, L + T, W + T), (L, 0, L + T, Q.REAR_DOOR_Y), (L, Q.REAR_DOOR_Y + 0.915, L + T, W),
                             (-0.25, Q.GLASS[1], 0, Q.DOOR['y0']), (-0.25, Q.DOOR['y0'] + 0.915, 0, W + T)]:
        A.box(x0, y0, 0, x1, y1, CUT, M['wall']); A.box(x0, y0, CUT, x1, y1, CUT + 0.01, M['cut'])
    A.box(-0.08, 0, 0, -0.02, Q.GLASS[1], LOW, M['glass'])
    # back of house partitions (low)
    for (x0, y0, x1, y1) in [(Q.LISTEN['x1'], 0, Q.LISTEN['x1'] + 0.12, 3.2), (Q.LISTEN['x1'], 4.12, Q.LISTEN['x1'] + 0.12, W),
                             (Q.WC['x0'], Q.WC['y1'], L, Q.WC['y1'] + 0.12), (Q.STORE['x0'], Q.STORE['y1'], L, Q.STORE['y1'] + 0.12)]:
        A.box(x0, y0, 0, x1, y1, 1.4, M['wall']); A.box(x0, y0, 1.4, x1, y1, 1.41, M['cut'])
    # the felt drapes: a pleated wall to 2.4 m, the opening left
    x = Q.LISTEN['x0']
    for ya, yb in ((Q.DRAPE_OPEN[1], W),):
        n = int((yb - ya) / 0.12)
        for k in range(n):
            A.box(x - 0.04 + 0.05 * (k % 2), ya + k * 0.12, 0, x + 0.04 + 0.05 * (k % 2), ya + (k + 1) * 0.12, 2.4, M['felt'])
    for ya, yb in ((0.0, Q.DRAPE_OPEN[0]),):
        n = int((yb - ya) / 0.12)
        for k in range(n):
            A.box(x - 0.04 + 0.05 * (k % 2), ya + k * 0.12, 0, x + 0.04 + 0.05 * (k % 2), ya + (k + 1) * 0.12, 2.4, M['felt'])
    A.box(Q.LISTEN['x0'] + 0.1, 0, 0, Q.LISTEN['x1'], W, 0.012, M['rug'])
    # shop walls
    for Wl, y0, y1 in ((Q.WALL_R, 0, Q.WALL_R['d']), (Q.WALL_L, W - Q.WALL_L['d'], W)):
        A.box(Wl['x0'], y0, 0, Wl['x1'], y1, 0.85, M['dark'])
        for z in (1.25, 1.65, 2.05):
            A.box(Wl['x0'], y0, z, Wl['x1'], y1, z + 0.03, M['shelf'])
    for i, c in enumerate(TINTS):
        A.cyl(1.2 + i * 0.3, 0.25, 1.28, 1.30, 0.06, M['dark'])
        A.sphere(1.2 + i * 0.3, 0.25, 1.36, 0.065, m(f'pcore{i}', c, 0.15, emit=c, strength=1.5))
        A.sphere(1.8 + (i % 4) * 0.4, W - 0.22, 1.72 + (i // 4) * 0.40, 0.14, m(f'pshade{i}', c, 0.2), half=True)
    A.box(4.6, 0.05, 0.88, 5.1, 0.42, 0.95, M['white']); A.cyl(4.85, 0.24, 0.95, 0.97, 0.15, M['dark'])     # Mantle
    P_ = Q.WINDOW_PLINTH
    A.box(P_['x'] - P_['d'] / 2, P_['y'] - P_['w'] / 2, 0, P_['x'] + P_['d'] / 2, P_['y'] + P_['w'] / 2, P_['h'], M['plinth'])
    for dy in (-0.45, 0.45):
        A.box(P_['x'] - 0.21, P_['y'] + dy - 0.28, P_['h'], P_['x'] + 0.21, P_['y'] + dy + 0.28, P_['h'] + Q.TROPOS['h'], M['tropos'], bevel=0.04)
    T_ = Q.TABLE
    A.box(T_['x0'], T_['y0'], 0, T_['x1'], T_['y1'], 0.9, M['walnut'], bevel=0.01)
    for i, c in enumerate(TINTS):
        A.sphere(T_['x0'] + 0.3 + i * 0.12, T_['y1'] - 0.2, 0.95, 0.05, m(f'pcore{i}', c))
    for x_, y_ in Q.HEMI:
        A.sphere(x_, y_, 1.9, 0.21, M['hemi'], half=True); A.sphere(x_, y_, 1.91, 0.10, M['glow'], half=True)
        A.cyl(x_, y_, 2.11, Q.CEIL, 0.004, M['cord'], 8)
    B = Q.BAR
    A.box(B['x0'], B['y0'], 0, B['x1'], B['y1'], 1.07, M['oak'], bevel=0.02)
    A.box(B['x0'] + 0.2, W - 0.05 - B['back'], 0, B['x1'] - 0.2, W - 0.05, 0.9, M['dark'])
    for x_, y_ in Q.STAND:
        A.cyl(x_, y_, 0, 1.05, 0.04, M['dark']); A.cyl(x_, y_, 1.02, 1.06, 0.30, M['walnut'])
    sweet = (Q.STACKS[0][0] - 4.12 * math.sqrt(3) / 2, W / 2)
    for x_, y_ in Q.STACKS:
        A.box(x_ - 0.43, y_ - 0.36, 0, x_ + 0.43, y_ + 0.36, 0.40, M['plinth'])
        o = A.box(-0.21, -0.28, 0, 0.21, 0.28, Q.TROPOS['h'], M['tropos'], bevel=0.05)
        o.location = (x_, y_, 0.40); A.rot(o, math.degrees(math.atan2(sweet[1] - y_, sweet[0] - x_)))
    for x_, y_ in Q.SEATS:
        A.chair({'chair': M['chair'], 'walnut': M['walnut'], 'dark': M['dark']}, x_, y_, 0)
    D = Q.DECKS
    A.box(D['x0'], D['y0'], 0, D['x1'], D['y1'], 0.9, M['dark'])
    A.box(Q.WC['x1'] - 0.62, 0.02, 0, Q.WC['x1'] - 0.22, 0.2, 0.8, M['white'])


def scene(out, scale, samples):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.render.resolution_x = int(3000 * scale); sc.render.resolution_y = int(2000 * scale)
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Base Contrast'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = A.lin('#f4f1ec'); bg.inputs['Strength'].default_value = 0.9
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 2.6; sun.angle = math.radians(12)
    so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(38), math.radians(8), math.radians(-35))
    A.box(-30, -30, -0.22, 60, 50, -0.21, A.mat('ground', '#f4f1ec', 0.9))
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = 16.8
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    cx, cy, cz = Q.L / 2 + 0.9, Q.W / 2 + 0.3, 0.6
    az, el, dist = math.radians(-124), math.radians(44), 50.0
    co.location = (cx + dist * math.cos(el) * math.cos(az), cy + dist * math.cos(el) * math.sin(az), cz + dist * math.sin(el))
    d = (cx - co.location.x, cy - co.location.y, cz - co.location.z)
    co.rotation_euler = mathutils.Vector(d).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    out = a[0]
    scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
    samples = int(a[a.index('--samples') + 1]) if '--samples' in a else 96
    bpy.ops.wm.read_factory_settings(use_empty=True)
    build()
    scene(os.path.abspath(out), scale, samples)
