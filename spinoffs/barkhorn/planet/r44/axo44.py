"""Planet EARF, round 44: the axonometric (drawing A-401). The render model itself (kit44.house), cut: the shell's walls
and the bar's partitions at 2.6 m, the ceiling lifted off; the lantern left whole, a closed oak box with its lit band (it
is the building's one object; its inside is drawn in the sections and rendered). Orthographic, a soft sky and a low sun; Cycles.

    python3 spinoffs/barkhorn/planet/r44/axo44.py OUT.png [--scale 0.5] [--samples 64]

It writes OUT.anchors.json (each label's point in the image) for the A-401 sheet.
"""
import json, math, os, sys

import bpy
import bmesh
import mathutils

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
import plan44 as P                                                   # noqa: E402
import kit44                                                         # noqa: E402

CUT = 2.60
KEEP = ('h44-lant-', 'h44-fins', 'h44-band-', 'h44-porch', 'h44-push')
DROP = ('h44-ceiling', 'h44-slots')


def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1.0]


def cut(ob, z):
    me = ob.data
    bm = bmesh.new(); bm.from_mesh(me)
    mw = ob.matrix_world.inverted()
    co = mw @ mathutils.Vector((0, 0, z)); no = (mw.to_3x3() @ mathutils.Vector((0, 0, 1))).normalized()
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    r = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=no, clear_outer=True)
    edges = [e for e in r['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
    if edges:
        bmesh.ops.holes_fill(bm, edges=edges)
    bm.to_mesh(me); bm.free()


def speakers():
    """The Tropos pair as plain solids in Ember (the product models load only through the shot engine)."""
    m = bpy.data.materials.new('axo-ember'); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = lin('#9E2A1C'); b.inputs['Roughness'].default_value = 0.3
    for (x, y) in P.STACKS:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, P.TROPOS['plinth'] + P.TROPOS['h'] / 2))
        o = bpy.context.active_object; o.scale = (P.TROPOS['d'], P.TROPOS['w'], P.TROPOS['h'])
        o.data.materials.append(m)


def scene(out, scale, samples):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.render.resolution_x = int(3000 * scale); sc.render.resolution_y = int(2000 * scale)
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Base Contrast'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = lin('#f4f1ec'); bg.inputs['Strength'].default_value = 0.8
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 2.4; sun.angle = math.radians(14)
    so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(40), math.radians(6), math.radians(-30))
    gm = bpy.data.materials.new('ground'); gm.use_nodes = True
    gm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = lin('#efebe4')
    bpy.ops.mesh.primitive_plane_add(size=120, location=(P.L / 2, P.W / 2, -0.12))
    bpy.context.active_object.data.materials.append(gm)
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = 22.0
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    cx, cy, cz = P.L / 2 + 0.2, P.W / 2 + 0.2, 0.8
    az, el, dist = math.radians(-128), math.radians(42), 60.0
    co.location = (cx + dist * math.cos(el) * math.cos(az), cy + dist * math.cos(el) * math.sin(az), cz + dist * math.sin(el))
    d = (cx - co.location.x, cy - co.location.y, cz - co.location.z)
    co.rotation_euler = mathutils.Vector(d).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = out
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()
    I = P.INNER; yc = (I['y0'] + I['y1']) / 2
    pts = {'Sound-lock entry': (2.0, 0.9, 2.5), 'Shop wall': (3.2, P.W - 0.2, 2.6), 'Window': (0.8, 5.0, 0.6),
           'Shop table': (4.4, 3.75, 1.0), 'Bar, quartzite top, terrazzo die': (10.0, P.COUNTER['y0'], 1.1),
           'Back bar; ice and glasswasher in the alcove': (6.5, P.W - 0.3, 2.3), 'Banquette': (9.0, P.BANQ['y0'], 1.1),
           'Accessible route, 64 in clear': (11.0, 0.8, 0.05), 'Porch (sound lock)': (P.LOCK['x0'] + 0.8, P.LOCK['y0'], 2.7),
           'The lantern: lit acrylic band': (P.LANT['x0'], P.W / 2, 3.9), 'Slotted oak baffle': (P.LANT['x0'], P.W / 2 + 1.5, 1.6),
           'The listening room inside, on a floated floor': (P.LANT['x1'] - 2.0, P.W / 2, 3.9),
           'Three all-gender rooms': (P.LOBBY['x1'] + 1.0, 4.6, 2.6), 'Rear exit': (P.L, 0.7, 1.0)}
    anchors = {}
    for k, v in pts.items():
        c = world_to_camera_view(sc, co, mathutils.Vector(v))
        anchors[k] = [round(c.x, 4), round(1 - c.y, 4)]
    json.dump(anchors, open(os.path.splitext(out)[0] + '.anchors.json', 'w'), indent=1)
    bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    out = os.path.abspath(a[0])
    scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
    samples = int(a[a.index('--samples') + 1]) if '--samples' in a else 64
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = kit44.house(bpy, 'h44', {'street': False, 'interior': False, 'mother': False}, None)
    for ob in list(bpy.data.objects):
        if ob.type != 'MESH':
            continue
        if ob.name.startswith(DROP):
            bpy.data.objects.remove(ob, do_unlink=True); continue
        if ob.name.startswith(KEEP):
            continue
        cut(ob, CUT)
    scene(out, scale, samples)
