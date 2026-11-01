# Diagnostic (2026-11-01): the four-pieces left speaker's view of the linked asset, matched camera (0, -4.5, 1.0), level, 30 mm.
#   python3.11 top_batt.py -- VARIANT OUT.png   (a as is, b top batt magenta, c hidden, d black sleeves, e the CAD's full batt, f e + d)
import bpy, math, sys
from pathlib import Path
from mathutils import Vector
ROOT = Path('/home/user/earf'); sys.path.insert(0, str(ROOT / 'studio' / 'engine'))
var, out = sys.argv[-2], sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(ROOT / 'spinoffs/barkhorn/asset/tropos.blend'), link=False, assets_only=True) as (src, dst):
    dst.collections = ['Tropos Poison']
col = bpy.data.collections['Tropos Poison']
for ch in list(col.children):
    col.children.unlink(ch)
sc = bpy.context.scene
root = bpy.data.objects.new('tropos', None); root.location = (-1.0, 0.53, 0); root.rotation_euler = (0, 0, math.radians(4))
sc.collection.objects.link(root)
sc.collection.children.link(col)
for o in col.objects:
    o.parent = root
top = bpy.data.objects['Tropos Poison lining-top-3-web']
if var == 'b':
    m = bpy.data.materials.new('magenta'); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (1, 0, 1, 1)
    b.inputs['Emission Color'].default_value = (1, 0, 1, 1); b.inputs['Emission Strength'].default_value = 0.5
    for s in top.material_slots: s.link = 'OBJECT'; s.material = m
if var == 'c':
    top.hide_render = True
if var in ('d', 'f'):     # black voile sleeves (f: and the full top batt)
    blk = bpy.data.materials.new('voile-black'); blk.use_nodes = True
    pb = blk.node_tree.nodes['Principled BSDF']; pb.inputs['Base Color'].default_value = (0.010, 0.010, 0.011, 1)
    pb.inputs['Roughness'].default_value = 0.85; pb.inputs['Sheen Weight'].default_value = 0.3
    for o in col.objects:
        if 'lining' in o.name:
            for s_ in o.material_slots:
                s_.link = 'OBJECT'; s_.material = blk
if var in ('e', 'f'):            # the CAD's full mesh, not the asset's collapsed one
    import product as Pr
    pdef = Pr.load_def('studio/products/barkhorn-cloud.json', ROOT)
    t = Pr.import_model(bpy, Path(ROOT, pdef['model']), pdef['origin_mm'], pdef.get('axes', 'gltf'))
    full = t['lining-top-3-web']
    print('full', len(full.data.polygons), 'asset', len(top.data.polygons), 'asset matrix', top.matrix_basis)
    top.data = full.data
    for k, s in enumerate(top.material_slots): s.link = 'OBJECT'
    for o in list(t.values()):
        bpy.data.objects.remove(o, do_unlink=True)
    mat = bpy.data.objects['Tropos Poison lining-top-3-web'].material_slots[0].material
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); cam.data.lens = 30; cam.data.sensor_width = 36
cam.location = (0, -4.5, 1.0); d = Vector((0, 0.3, 0.95)) - cam.location
yaw = math.atan2(d.x, d.y); cam.rotation_euler = (math.radians(90), 0, -yaw)        # level
sc.collection.objects.link(cam); sc.camera = cam
w = bpy.data.worlds.new('w'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.9, 0.85, 0.78, 1)
w.node_tree.nodes['Background'].inputs[1].default_value = 0.8; sc.world = w
sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sun.data.energy = 3
sun.rotation_euler = (math.radians(70), 0, math.radians(-60)); sc.collection.objects.link(sun)
bpy.ops.mesh.primitive_plane_add(size=20)
wall = bpy.data.objects.new('wall', bpy.data.meshes.new('wall')); 
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 1.2, 2), rotation=(math.radians(90), 0, 0))
r = sc.render; r.engine = 'CYCLES'; sc.cycles.samples = 64; sc.cycles.device = 'CPU'; sc.cycles.max_bounces = 24
sc.cycles.transmission_bounces = 24; sc.cycles.volume_bounces = 4
r.resolution_x, r.resolution_y = 1920, 1080
r.use_border = True; r.use_crop_to_border = True
x0, y0, x1, y1 = 523, 425, 751, 856
r.border_min_x, r.border_max_x = (x0 - 10) / 1920, (x1 + 10) / 1920
r.border_min_y, r.border_max_y = 1 - (y1 + 10) / 1080, 1 - (y0 - 10) / 1080
sc.view_settings.view_transform = 'Khronos PBR Neutral'
r.filepath = out; bpy.ops.render.render(write_still=True); print('wrote', out)
