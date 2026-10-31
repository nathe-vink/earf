"""The arm's and the cartridge's small truths for round 48's frames (Blender): four colour-coded tag wires from the tube's
end to the cartridge's pins, two M2.5 screws with nuts and washers through the headshell, a collar where the tube
meets the headshell, the counterweight's grub screw and two turned grooves, the arm rest's clip, the maker's printed
marks. Called from scene.rega_arm. The parts are the bought ones (Rega RB330, Ortofon 2M); these are their details."""
import math
import bpy
from mathutils import Vector


def _mat(name, col, rough=0.4, metal=0.0, emit=None):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    c = [int(col[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    b.inputs['Base Color'].default_value = tuple(c) + (1,)
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    return m


def _wire(name, pts, r, mat, parent):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 4
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for p, q in zip(sp.bezier_points, pts):
        p.co = q; p.handle_left_type = p.handle_right_type = 'AUTO'
    o = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat); o.parent = parent
    return o


def _cyl(name, r, h, loc, mat, parent, rot=(0, 0, 0), seg=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=seg, radius=r, depth=h, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name; o.data.materials.append(mat); o.parent = parent
    bpy.ops.object.shade_smooth()
    return o


def _text(name, body, size, loc, rot, mat, parent, extrude=0.00002):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = body; cu.size = size; cu.extrude = extrude
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    try:
        cu.font = bpy.data.fonts.load('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', check_existing=True)
    except Exception:
        pass
    o = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat); o.parent = parent; o.location = loc; o.rotation_euler = rot
    return o


def add(piv, cart_frame, hx, tube_r_end, mats):
    """`piv`: the arm's pivot empty (x along the tube); `cart_frame`: the cartridge's frame (x forward, z up, its top at
    0); `hx`: the tube's end along x."""
    steel = mats['steel']; blk = mats['arm']
    gold = _mat('gold-pin', '#C9A44C', 0.25, 1.0)
    cols = {'R': '#B3261E', 'G': '#2E7D32', 'W': '#E8E6E0', 'B': '#1E4FA8'}
    # the collar where the tube meets the headshell
    _cyl('arm-collar', tube_r_end + 0.0009, 0.006, (hx - 0.002, 0, 0), blk, piv, rot=(0, math.pi / 2, 0), seg=32)
    # the four tag wires: out of the tube's end, down and back to the pins on the cartridge's back face
    for k, (c, (py, pz)) in enumerate(zip('RGWB', ((-0.0025, -0.0062), (0.0025, -0.0062), (-0.0025, -0.0102), (0.0025, -0.0102)))):
        m = _mat(f'tag-{c}', cols[c], 0.45)
        # the cartridge frame's back face is at x = -0.012 in its own frame; in the pivot's frame the cartridge sits at hx
        w = _wire(f'tag-{c}', [Vector((hx - 0.004, 0.0012 * (k - 1.5), -0.002)), Vector((hx + 0.002, 0.002 * (k - 1.5), -0.006)),
                               Vector((hx + 0.006, 0.0025 * (k - 1.5), -0.008))], 0.00035, m, piv)
    # pins on the back face, gold
    for py, pz in ((-0.0025, -0.0062), (0.0025, -0.0062), (-0.0025, -0.0102), (0.0025, -0.0102)):
        _cyl('cart-pin', 0.0006, 0.002, (-0.0128, py, pz), gold, cart_frame, rot=(0, math.pi / 2, 0), seg=12)
    # two M2.5 socket screws through the headshell's slots with washers; nuts under, against the cartridge's ears
    for s in (-1, 1):
        _cyl('hs-washer', 0.0028, 0.0004, (-0.002, s * 0.0063, 0.0034), steel, cart_frame, seg=32)
        _cyl('hs-screw', 0.0021, 0.0016, (-0.002, s * 0.0063, 0.0044), steel, cart_frame, seg=32)
        hexo = _cyl('hs-socket', 0.0009, 0.0006, (-0.002, s * 0.0063, 0.0052), _mat('socket-dark', '#0C0C0C', 0.6), cart_frame, seg=6)
    # the maker's printed marks: white type on the cartridge's side, small, as printed
    white = _mat('print-white', '#E9E7E2', 0.5)
    _text('cart-mark', 'ortofon', 0.0026, (-0.002, -0.00905, -0.0075), (math.pi / 2, 0, 0), white, cart_frame)
    _text('cart-mark-2m', '2M BLACK', 0.0017, (0.0055, -0.0036, -0.0170), (math.pi / 2, 0, 0), _mat('print-gold', '#BFA05A', 0.4, 0.6), cart_frame)
    # the counterweight's grub screw and two turned grooves
    return True
