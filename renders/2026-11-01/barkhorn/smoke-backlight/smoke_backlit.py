# Smoke backlit: the asset as biomes links it, before a bright warm backdrop (argv: tint variant out.png)
import bpy, math, sys
tint, var, out = sys.argv[-3], sys.argv[-2], sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
lib = '/home/user/earf/spinoffs/barkhorn/asset/tropos.blend'
with bpy.data.libraries.load(lib, link=False, assets_only=True) as (s, d):
    d.collections = [f'Tropos {tint}']
col = bpy.data.collections[f'Tropos {tint}']
for ch in list(col.children): col.children.unlink(ch)
sc = bpy.context.scene; sc.collection.children.link(col)
for o in col.objects:
    o.rotation_euler = (0, 0, math.radians(-25))
if var in ('black', 'both'):
    blk = bpy.data.materials.new('voile-black'); blk.use_nodes = True
    pb = blk.node_tree.nodes['Principled BSDF']; pb.inputs['Base Color'].default_value = (0.01, 0.01, 0.011, 1); pb.inputs['Roughness'].default_value = 0.85
    for o in col.objects:
        if 'lining' in o.name:
            for sl in o.material_slots: sl.link = 'OBJECT'; sl.material = blk
if var in ('deep', 'both'):
    k = float(__import__('os').environ.get('SMOKE_K', '1.86'))
    done = set()
    for o in col.objects:
        for sl in o.material_slots:
            m = sl.material
            if m and m.name not in done and m.node_tree and m.name.startswith('bark'):
                for n in m.node_tree.nodes:
                    if n.type == 'VOLUME_ABSORPTION':
                        n.inputs['Density'].default_value *= k
                done.add(m.name)
    print('deepened', sorted(done))
# the backdrop: a bright warm emitter behind, as a fire or a low sun; a dim cool front
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 2.2, 1.2), rotation=(math.radians(90), 0, 0))
bd = bpy.context.object; m = bpy.data.materials.new('fire'); m.use_nodes = True
e = m.node_tree.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (1.0, 0.55, 0.22, 1); e.inputs['Strength'].default_value = 1.2
m.node_tree.links.new(e.outputs[0], m.node_tree.nodes['Material Output'].inputs['Surface']); bd.data.materials.append(m)
bpy.ops.mesh.primitive_plane_add(size=20)
fire = bpy.data.objects.new('fire', bpy.data.lights.new('fire', 'AREA')); fire.data.energy = 2500; fire.data.size = 1.0
fire.data.color = (1.0, 0.5, 0.2); fire.location = (-0.5, 0.9, 0.6); fire.rotation_euler = (math.radians(-80), 0, math.radians(-20))
sc.collection.objects.link(fire)
w = bpy.data.worlds.new('w'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.35, 0.4, 0.5, 1)
w.node_tree.nodes['Background'].inputs[1].default_value = 0.15; sc.world = w
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); cam.data.lens = 50
cam.location = (0.0, -3.3, 0.85); cam.rotation_euler = (math.radians(89), 0, 0); sc.collection.objects.link(cam); sc.camera = cam
r = sc.render; r.engine = 'CYCLES'; sc.cycles.samples = 48; sc.cycles.device = 'CPU'; sc.cycles.max_bounces = 24
sc.cycles.transmission_bounces = 24; sc.cycles.volume_bounces = 4; sc.cycles.use_denoising = True
r.resolution_x, r.resolution_y = 450, 600
sc.view_settings.view_transform = 'Khronos PBR Neutral'
r.filepath = out; bpy.ops.render.render(write_still=True); print('wrote', out)
