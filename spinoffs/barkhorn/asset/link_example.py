# Link four Tropos tints from tropos.blend into an empty scene and render them (a check that the asset links; run:
#   python3.11 spinoffs/barkhorn/asset/link_example.py -- OUT.png)
import bpy, math, sys
import os
lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tropos.blend')
out = sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
names = ['Tropos Ember', 'Tropos Smoke', 'Tropos Poison', 'Tropos Ice']
with bpy.data.libraries.load(lib, link=True, assets_only=True) as (src, dst):
    print('collections in the library:', src.collections)
    dst.collections = list(names)
sc = bpy.context.scene
for i, n in enumerate(names):
    e = bpy.data.objects.new(n, None); e.instance_type = 'COLLECTION'; e.instance_collection = bpy.data.collections[n]
    e.location = (-1.65 + 1.1 * i, 0, 0); e.rotation_euler = (0, 0, math.radians(-20)); sc.collection.objects.link(e)
bpy.ops.mesh.primitive_plane_add(size=30); 
sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sun.data.energy = 4; sun.rotation_euler = (math.radians(50), 0, math.radians(-40)); sc.collection.objects.link(sun)
w = bpy.data.worlds.new('w'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs[1].default_value = 0.6; sc.world = w
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); cam.location = (0, -7.5, 1.6); cam.rotation_euler = (math.radians(84), 0, 0); cam.data.lens = 45
sc.collection.objects.link(cam); sc.camera = cam
sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.cycles.device = 'CPU'
sc.render.resolution_x, sc.render.resolution_y = 900, 450
sc.render.filepath = out; bpy.ops.render.render(write_still=True)
print('rendered', out)
