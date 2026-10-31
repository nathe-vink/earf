"""Planet EARF, round 42: the axonometric. The plan (plan42.py) built as a cutaway model in Blender, the walls cut at
8 ft 6 in, the furniture and the products as simple solids in their colours, lit by a soft sky; Cycles, orthographic.

    python3 spinoffs/barkhorn/planet/r42/axo42.py OUT.png [--scale 0.5] [--samples 64]

One model, every number from the plan: it is the drawing set's A-301 and the house book's overview.
"""
import math, os, sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan42 as P                                                   # noqa: E402

W, L = P.W, P.L
CUT = 2.60                       # the walls cut here, so the rooms read from above
MATS = {}


def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c) + (1.0,)


def mat(name, col, rough=0.7, metal=0.0, emit=None, strength=0.0, trans=0.0, alpha=1.0):
    if name in MATS:
        return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = lin(col); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if trans:
        b.inputs['Transmission Weight'].default_value = trans
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha
    if emit:
        b.inputs['Emission Color'].default_value = lin(emit); b.inputs['Emission Strength'].default_value = strength
    MATS[name] = m
    return m


def box(x0, y0, z0, x1, y1, z1, m, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.object
    o.scale = (abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        mod = o.modifiers.new('b', 'BEVEL'); mod.width = bevel; mod.segments = 3
    o.data.materials.append(m)
    return o


def cyl(x, y, z0, z1, r, m, verts=40):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=z1 - z0, location=(x, y, (z0 + z1) / 2))
    o = bpy.context.object; o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    return o


def sphere(x, y, z, r, m, half=False):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=r, location=(x, y, z))
    o = bpy.context.object; o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    if half:                                                    # keep the top half: a shade
        import bmesh
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -1e-4], context='VERTS')
        bm.to_mesh(o.data); bm.free()
        o.modifiers.new('s', 'SOLIDIFY').thickness = 0.01
    return o


def rot(o, deg):
    o.rotation_euler[2] = math.radians(deg)


def build():
    M = dict(
        floor=mat('floor', '#b9b2a7', 0.55), wall=mat('wall', '#e9e5de', 0.85), cut=mat('cut', '#3a3835', 0.9),
        part=mat('part', '#d8d2c8', 0.85), glass=mat('glass', '#cfe0e6', 0.05, trans=0.9),
        oak=mat('oak', '#9c7a52', 0.5), zinc=mat('zinc', '#a9a8a3', 0.35, 0.8), dark=mat('dark', '#2a2826', 0.6),
        leather=mat('leather', '#5a2c20', 0.5), mohair=mat('mohair', '#4a3a2e', 0.9), walnut=mat('walnut', '#4e3a2a', 0.45),
        chair=mat('chair', '#8a7058', 0.7), velvet=mat('velvet', '#7b3b2c', 0.9), tropos=mat('tropos', '#3d3c42', 0.15),
        plinth=mat('plinth', '#1f1e1c', 0.6), endgrain=mat('endgrain', '#8f6f4c', 0.8), records=mat('records', '#c8b490', 0.9),
        sleeves=mat('sleeves', '#6b5544', 0.8), shelf=mat('shelf', '#efe9df', 0.8), felt=mat('felt', '#3a3532', 0.95),
        white=mat('white', '#f3f1ec', 0.3), rug=mat('rug', '#6e5a48', 0.95), absorber=mat('absorber', '#5d5650', 0.95),
        hemi=mat('hemi', '#2b2a28', 0.3, emit='#ffb15a', strength=0.0), glow=mat('glow', '#ffcf8a', 0.5, emit='#ffb15a', strength=6.0),
        mother=mat('mother', '#e8e2ee', 0.2, trans=0.4), cord=mat('cord', '#1a1a1a', 0.5))
    tints = ['#c8452f', '#d27a3a', '#d9b43c', '#5d8a4a', '#6fa8c8', '#8b6fb0', '#e9e7e2', '#4a4a50']
    T = P.WALL
    # floor and slab
    box(-0.4, -T, -0.25, L + T, W + T, 0.0, M['floor'])
    # walls, cut at CUT: the cut tops dark
    LOW = 1.00                                                      # the near walls cut low, so the rooms read
    for (x0, y0, x1, y1) in [(-0.3, -T, L + T, 0)]:
        box(x0, y0, 0, x1, y1, LOW, M['wall']); box(x0, y0, LOW, x1, y1, LOW + 0.01, M['cut'])
    for (x0, y0, x1, y1) in [(0, W, L + T, W + T), (L, 0, L + T, P.REAR_EXIT_Y),
                             (L, P.REAR_EXIT_Y + P.DOOR_W, L + T, W), (-0.3, P.GLASS[1], 0, P.VEST['y0'] - 0.12),
                             (-0.3, P.VEST['y1'] + 0.12, 0, W + T)]:
        box(x0, y0, 0, x1, y1, CUT, M['wall']); box(x0, y0, CUT, x1, y1, CUT + 0.01, M['cut'])
    box(-0.10, 0, 0, 0, P.GLASS[1], 0.45, M['dark'])
    box(-0.08, 0, 0.45, -0.02, P.GLASS[1], LOW, M['glass'])
    V = P.VEST
    for (x0, y0, x1, y1) in [(0, V['y0'] - 0.12, V['x1'] + 0.12, V['y0']), (0, V['y1'], V['x1'] + 0.12, V['y1'] + 0.12),
                             (V['x1'], V['y0'], V['x1'] + 0.12, P.INNER_DOOR_Y), (V['x1'], P.INNER_DOOR_Y + P.DOOR_W, V['x1'] + 0.12, V['y1'])]:
        box(x0, y0, 0, x1, y1, 2.75, M['part']); box(x0, y0, 2.75, x1, y1, 2.76, M['cut'])
    # partitions
    Pt, Lb = P.PARTITION, P.LOBBY
    parts = [(Pt['x0'], Pt['y0'], Pt['x1'], P.LISTEN_DOOR1_Y), (Pt['x0'], P.LISTEN_DOOR1_Y + P.DOOR_W, Pt['x1'], W),
             (Pt['x0'], P.CORRIDOR['y1'], L, P.LISTEN['y0']), (Lb['x1'], Lb['y0'], Lb['x1'] + 0.12, P.LISTEN_DOOR2_Y),
             (Lb['x1'], P.LISTEN_DOOR2_Y + P.DOOR_W, Lb['x1'] + 0.12, Lb['y1'] + 0.12), (Lb['x0'], Lb['y1'], Lb['x1'], Lb['y1'] + 0.12),
             (P.BOH['x0'] - 0.12, 0, P.BOH['x0'], P.CORRIDOR['y0'])]
    for i, (x0, x1, name) in enumerate(P.ROOMS):
        d0 = x0 + (0.25 if i else 0.20)
        parts += [(x0 if i == 0 else x0 + 0.06, P.BOH['y1'], d0, P.CORRIDOR['y0']),
                  (d0 + P.DOOR_W, P.BOH['y1'], x1 - 0.06 if x1 < L else L, P.CORRIDOR['y0'])]
        if i:
            parts.append((x0 - 0.06, 0, x0 + 0.06, P.BOH['y1']))
    for k, (x0, y0, x1, y1) in enumerate(parts):
        h = CUT - 0.15 if k < 7 else 1.30                           # back of house cut low, so the WCs read
        box(x0, y0, 0, x1, y1, h, M['part']); box(x0, y0, h, x1, y1, h + 0.01, M['cut'])
    # the listening room's floor (a darker carpet) and the lounge rug
    box(P.LISTEN['x0'], P.LISTEN['y0'], 0, L, W, 0.012, M['rug'])
    # shop wall: shelves and the pieces
    SW = P.SHOP_WALL
    box(SW['x0'], 0, 0, SW['x1'], SW['d'], 0.85, M['dark'])
    for z in (1.25, 1.65, 2.05):
        box(SW['x0'], 0, z, SW['x1'], SW['d'] - 0.05, z + 0.03, M['shelf'])
    for i, c in enumerate(tints):                                     # Cores on the shelf
        x = 4.15 + i * 0.17
        cyl(x, 0.25, 1.28, 1.30, 0.06, M['dark'])
        sphere(x, 0.25, 1.36, 0.065, mat(f'core{i}', c, 0.15, emit=c, strength=1.5))
    for i, c in enumerate(tints):                                     # Hemisphere shades on pegs
        sphere(2.62 + (i % 4) * 0.34, 0.20, 1.72 + (i // 4) * 0.40, 0.14, mat(f'shade{i}', c, 0.2), half=True)
    for x, y, what in P.SHOP_PLINTHS:
        if what == 'Tropos':
            box(x - 0.40, y - 0.33, 0, x + 0.40, y + 0.33, 0.20, M['plinth'])
            box(x - 0.28, y - 0.21, 0.20, x + 0.28, y + 0.21, 0.20 + P.TROPOS['h'], M['tropos'], bevel=0.04)
        else:
            box(x - 0.40, y - 0.30, 0, x + 0.40, y + 0.30, 0.70, M['plinth'])
            box(x - 0.24, y - 0.18, 0.70, x + 0.24, y + 0.18, 0.76, M['white'])
            cyl(x, y, 0.76, 0.785, 0.16, M['dark'])
    T_ = P.SHOP_TABLE
    box(T_['x0'], T_['y0'], 0, T_['x1'], T_['y1'], T_['h'], M['walnut'], bevel=0.01)
    for i, c in enumerate(tints):
        sphere(T_['x0'] + 0.3 + i * 0.13, T_['y1'] - 0.2, T_['h'] + 0.05, 0.05, mat(f'core{i}', c))
    for x, y in P.LOUNGE:
        cyl(x, y, 0, 0.42, 0.33, M['walnut'])
        for s in (-1, 1):
            cy = y + s * P.LOUNGE_CHAIR['gap']
            box(x - 0.38, cy - 0.36, 0, x + 0.38, cy + 0.36, 0.40, M['chair'], bevel=0.05)
            box(x - 0.38, cy + s * 0.22, 0.40, x + 0.38, cy + s * 0.36, 0.75, M['chair'], bevel=0.04)
    H = P.HOST
    box(H['x0'], H['y0'], 0, H['x1'], H['y1'], 1.07, M['walnut'])
    # the bar
    B, C = P.BACKBAR, P.COUNTER
    box(B['x0'], B['y0'], 0, B['x1'], B['y1'], B['h'], M['dark'])
    for z in (1.35, 1.75, 2.15):
        box(B['x0'], B['y0'] + 0.25, z, B['x1'], W, z + 0.025, M['glow'])
        for i in range(int((B['x1'] - B['x0']) / 0.12)):
            if (i * 7) % 11 < 8:
                cyl(B['x0'] + 0.08 + i * 0.12, W - 0.15, z + 0.025, z + 0.30, 0.035, mat(f'bottle{i % 3}', ['#6b4a2a', '#3f5a44', '#9a7a52'][i % 3], 0.1, trans=0.3))
    box(C['x0'], C['y0'], 0, C['x1'], C['y_work'], C['top_z'] - 0.05, M['oak'], bevel=0.08)
    box(C['x0'] - 0.04, C['edge'], C['top_z'] - 0.05, C['x1'] + 0.04, C['y_work'] + 0.03, C['top_z'], M['zinc'], bevel=0.03)
    box(P.LOW_END['x0'] - 0.04, C['edge'], P.LOW_END['top_z'] - 0.04, P.LOW_END['x1'], C['y0'] + 0.02, P.LOW_END['top_z'], M['zinc'])
    for x in P.STOOLS:
        cyl(x, P.STOOL_Y, 0, 0.72, 0.03, M['dark'])
        cyl(x, P.STOOL_Y, 0.70, 0.78, 0.21, M['leather'])
        box(x - 0.18, P.STOOL_Y - 0.22, 0.78, x + 0.18, P.STOOL_Y - 0.16, 0.98, M['leather'])
    for x in P.LOW_SEATS:
        chair(M, x, P.STOOL_Y + 0.05, 90)
    Bo = P.BOOTH
    box(Bo['desk'][0], Bo['y0'] + 0.08, 0, Bo['desk'][1], C['y_work'], Bo['h'], M['dark'])
    box(Bo['x0'], Bo['y0'], 0, Bo['x1'], Bo['y0'] + 0.08, 1.0, M['dark'])
    box(Bo['x0'], Bo['y0'], 1.0, Bo['x1'], Bo['y0'] + 0.02, 1.6, M['glass'])
    for dy in (0.45, 1.05):
        cyl(Bo['desk'][0] + 0.30, Bo['y0'] + dy, Bo['h'], Bo['h'] + 0.02, 0.16, M['records'])
    R = P.RECORD_WALL
    box(R['x0'], R['y0'], 0, R['x1'], R['y1'], CUT - 0.15, M['records'])
    n = int((CUT - 0.15) / R['cell'])
    for k in range(1, n + 1):
        box(R['x0'] - 0.005, R['y0'], k * R['cell'] - 0.02, R['x1'] - 0.03, R['y1'], k * R['cell'], M['shelf'])
        box(R['x0'] - 0.003, R['y0'] + 0.02, (k - 1) * R['cell'] + 0.02, R['x0'] + 0.02, R['y1'] - 0.02, k * R['cell'] - 0.04, M['sleeves'])
    # banquette, tables, chairs; communal; Mother EARF
    Q = P.BANQ
    box(Q['x0'], 0, 0, Q['x1'], Q['y1'], Q['seat'], M['mohair'], bevel=0.04)
    box(Q['x0'], 0, Q['seat'], Q['x1'], 0.22, Q['back'], M['mohair'], bevel=0.04)
    for x in P.BANQ_TABLES:
        BT = P.BANQ_TABLE
        box(x - BT['w'] / 2, BT['y0'], BT['h'] - 0.04, x + BT['w'] / 2, BT['y0'] + BT['d'], BT['h'], M['walnut'])
        cyl(x, BT['y0'] + BT['d'] / 2, 0, BT['h'] - 0.04, 0.03, M['dark'])
        chair(M, x, P.BANQ_CHAIR_Y, -90)
    Cm = P.COMMUNAL
    box(Cm['x0'], Cm['y0'], Cm['h'] - 0.05, Cm['x1'], Cm['y1'], Cm['h'], M['walnut'], bevel=0.02)
    for xx in (Cm['x0'] + 0.4, Cm['x1'] - 0.4):
        box(xx - 0.04, Cm['y0'] + 0.2, 0, xx + 0.04, Cm['y1'] - 0.2, Cm['h'] - 0.05, M['dark'])
    for x in P.COMMUNAL_CHAIRS:
        chair(M, x, P.COMMUNAL_CHAIR_Y[0], 90); chair(M, x, P.COMMUNAL_CHAIR_Y[1], -90)
    Mo = P.MOTHER
    mother_globe(Mo['x'], Mo['y'], Mo['z'], Mo['d'] / 2, tints)
    cyl(Mo['x'], Mo['y'], Mo['z'] + Mo['d'] / 2, 3.4, 0.004, M['cord'], 8)
    # Hemispheres over the counter and in the shop
    for x, y in [(x, P.HEMI_COUNTER_Y) for x in P.HEMI_COUNTER] + P.HEMI_SHOP + P.HEMI_LOUNGE:
        z = C['top_z'] + 0.66 if y > 8 else (1.70 if y < 2 else 1.45)
        sphere(x, y, z, 0.21, M['hemi'], half=True)
        sphere(x, y, z + 0.01, 0.10, M['glow'], half=True)
        cyl(x, y, z + 0.21, 3.4, 0.004, M['cord'], 8)
    for x, y in P.CORE_ON:
        z = 0.74 if y < 6 or x > 16 else 0.74
        if x > 16:
            z = 0.46
        elif x < 3:
            z = 0.42
        cyl(x, y, z, z + 0.03, 0.06, M['dark'])
        sphere(x, y, z + 0.09, 0.07, mat('coreglow', '#ffcf8a', 0.2, emit='#ffb15a', strength=3.0))
    # the listening room: plinths and Tropos toed in, the altar, the tubs, side tables, absorbers
    for x, y in P.STACKS:
        box(x - 0.43, y - 0.36, 0, x + 0.43, y + 0.36, P.TROPOS['plinth'], M['plinth'])
        o = box(-0.21, -0.28, 0, 0.21, 0.28, P.TROPOS['h'], M['tropos'], bevel=0.05)
        o.location = (x, y, P.TROPOS['plinth'])
        rot(o, math.degrees(math.atan2(P.SWEET[1] - y, P.SWEET[0] - x)))
        a = math.atan2(P.SWEET[1] - y, P.SWEET[0] - x)
        hz = P.TROPOS['plinth'] + P.TROPOS['h'] - 0.32
        bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.18, radius2=0.04, depth=0.22,
                                        location=(x + 0.25 * math.cos(a), y + 0.25 * math.sin(a), hz),
                                        rotation=(0, math.radians(-90), a))
        bpy.context.object.data.materials.append(M['dark'])
    A = P.ALTAR
    box(A['x0'], A['y0'], 0, A['x1'], A['y1'], min(A['z1'], CUT - 0.15), M['endgrain'])
    for x, y in P.TUBS:
        face = math.degrees(math.atan2(P.SWEET[1] - y, (L - 1.0) - x))
        cyl(x, y, 0, 0.38, P.TUB_R, M['velvet'])
        tb = cyl(x, y, 0.38, 0.66, P.TUB_R, M['velvet'])
        # cut the front open: a box removed by boolean
        cutter = box(-0.05, -0.36, -0.1, 0.6, 0.36, 0.5, M['velvet'])
        cutter.location = (x, y, 0.42); rot(cutter, face)
        mod = tb.modifiers.new('open', 'BOOLEAN'); mod.object = cutter; mod.operation = 'DIFFERENCE'
        bpy.context.view_layer.objects.active = tb; bpy.ops.object.modifier_apply(modifier='open')
        bpy.data.objects.remove(cutter)
        inner = cyl(x, y, 0.38, 0.67, P.TUB_R - 0.08, M['velvet'])
        mod = tb.modifiers.new('hollow', 'BOOLEAN'); mod.object = inner; mod.operation = 'DIFFERENCE'
        bpy.context.view_layer.objects.active = tb; bpy.ops.object.modifier_apply(modifier='hollow')
        bpy.data.objects.remove(inner)
    for x, y in P.SIDE_TABLES:
        cyl(x, y, 0, 0.46, 0.22, M['walnut'])
    for x0, x1 in P.PANELS_L:
        box(x0, W - 0.10, 0.5, x1, W, 2.2, M['absorber'])
        box(x0 + 1.2, P.LISTEN['y0'], 0.5, x1, P.LISTEN['y0'] + 0.10, 2.2, M['absorber'])
    # back of house: WCs and lavatories, the stock room's shelves
    for x0, x1, name in P.ROOMS[:3]:
        box(x0 + 0.24, 0.02, 0, x0 + 0.60, 0.20, 0.80, M['white'])
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.2, depth=0.42, location=(x0 + 0.42, 0.42, 0.21))
        o = bpy.context.object; o.scale[1] = 1.4; o.data.materials.append(M['white'])
        box(x1 - 0.62, 0.0, 0.80, x1 - 0.12, 0.45, 0.86, M['white'])
    x0, x1, _ = P.ROOMS[3]
    box(x0 + 0.10, 0.0, 0, x1 - 0.05, 0.45, 2.0, M['shelf'])
    box(x0 + 0.10, 1.90, 0.72, x0 + 1.30, 2.50, 0.75, M['walnut'])


def chair(M, x, y, facing):
    o = box(-0.23, -0.23, 0.43, 0.23, 0.23, 0.47, M['chair'], bevel=0.02); o.location.x += x; o.location.y += y
    rot(o, facing)
    a = math.radians(facing)
    bx, by = x - 0.21 * math.cos(a), y - 0.21 * math.sin(a)
    b = box(-0.03, -0.22, 0.47, 0.03, 0.22, 0.85, M['walnut']); b.location.x += bx; b.location.y += by
    rot(b, facing)
    for dx, dy in ((-0.19, -0.19), (0.19, -0.19), (-0.19, 0.19), (0.19, 0.19)):
        cyl(x + dx * math.cos(a) - dy * math.sin(a), y + dx * math.sin(a) + dy * math.cos(a), 0, 0.43, 0.015, M['dark'], 8)


def mother_globe(x, y, z, r, tints):
    """Mother EARF as the mark: six discs slotted together, each its own tint, thin."""
    for i in range(6):
        if i < 3:
            rotn = (0, math.radians(90), math.radians(i * 60))
        else:
            rotn = (0, 0, 0)
        if i >= 3:
            zz = z + (i - 4) * r * 0.62
            rr = math.sqrt(max(r * r - (zz - z) ** 2, 0.01))
            bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=rr, depth=0.02, location=(x, y, zz))
        else:
            bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r, depth=0.02, location=(x, y, z), rotation=rotn)
        o = bpy.context.object
        c = tints[i]
        o.data.materials.append(mat(f'mother{i}', c, 0.15, trans=0.5, emit=c, strength=0.4))


def scene(out, scale, samples):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.render.resolution_x = int(3000 * scale); sc.render.resolution_y = int(2000 * scale)
    sc.render.film_transparent = False
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Base Contrast'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = lin('#f4f1ec'); bg.inputs['Strength'].default_value = 0.9
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 2.6; sun.angle = math.radians(12)
    so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(38), math.radians(8), math.radians(-35))
    # a pale ground under the model
    box(-30, -30, -0.27, 60, 50, -0.26, mat('ground', '#f4f1ec', 0.9))
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = 23.5
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    cx, cy, cz = L / 2 + 0.6, W / 2 + 0.2, 0.6
    az, el, dist = math.radians(-124), math.radians(44), 60.0
    co.location = (cx + dist * math.cos(el) * math.cos(az), cy + dist * math.cos(el) * math.sin(az), cz + dist * math.sin(el))
    d = (cx - co.location.x, cy - co.location.y, cz - co.location.z)
    import mathutils
    co.rotation_euler = mathutils.Vector(d).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = out
    # where the labels go: each named point's position in the image (0..1 from the top left), for the A-301 sheet
    import json
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()
    pts = {'Shop wall': (4.0, 0.3, 1.6), 'Window lounge': (1.75, 5.45, 0.6), 'Vestibule': (2.1, 8.75, 2.7),
           'Counter': (11.0, 8.8, 1.1), 'Back bar': (11.0, W - 0.3, 2.3), 'Booth': (15.0, 8.6, 1.0),
           'Record wall': (15.8, 6.5, 2.4), 'Mother EARF': (P.MOTHER['x'], P.MOTHER['y'], 3.05),
           'Communal table': (11.4, 4.65, 0.8), 'Banquette': (12.0, 0.4, 1.1), 'Listening room': (20.5, 7.6, 0.7),
           'Tropos stacks': (23.3, 9.4, 1.7), 'Altar': (L - 0.2, 7.6, 2.4), 'WCs': (18.8, 1.5, 1.3),
           'Stock and office': (23.0, 1.5, 1.3), 'Rear exit': (L, 3.7, 1.0)}
    anchors = {}
    for k, v in pts.items():
        c = world_to_camera_view(sc, co, mathutils.Vector(v))
        anchors[k] = [round(c.x, 4), round(1 - c.y, 4)]
    json.dump(anchors, open(os.path.splitext(out)[0] + '.anchors.json', 'w'), indent=1)
    bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    out = a[0]
    scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
    samples = int(a[a.index('--samples') + 1]) if '--samples' in a else 96
    bpy.ops.wm.read_factory_settings(use_empty=True)
    build()
    scene(os.path.abspath(out), scale, samples)
