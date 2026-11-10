"""A Fresnel test (2026-11-10): a 10 mm plate of Ember's cabinet acrylic at INC deg to the camera, mirroring a white
emitter of radiance 1.0 (linear), black world. Run with the bpy Python: python3.11 fresnel_plate.py INC resin|glass VIEW."""
import sys, math
sys.path.insert(0, 'studio/engine')
import bpy, bmesh
from mathutils import Vector
import materials as M
inc = float(sys.argv[1]); mode = sys.argv[2]; VT = sys.argv[3]            # mode: 'resin' (the cabinet's) or 'glass' (a bare Principled, IOR 1.49)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 512; sc.cycles.device = 'CPU'
sc.cycles.use_denoising = False; sc.render.resolution_x = sc.render.resolution_y = 64
w = bpy.data.worlds.new('w'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0; sc.world = w
sc.view_settings.view_transform = VT; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0
sc.cycles.max_bounces = 32; sc.cycles.transmission_bounces = 32; sc.cycles.glossy_bounces = 16; sc.cycles.volume_bounces = 8
# camera at origin looking +y; the plate 1 m away, its normal turned inc deg from -y about z
cd = bpy.data.cameras.new('c'); cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam); sc.camera = cam
cd.lens = 200; cam.location = (0, 0, 0); cam.rotation_euler = (math.radians(90), 0, 0)
a = math.radians(inc); n = Vector((math.sin(a), -math.cos(a), 0)); P = Vector((0, 1, 0))
bpy.ops.mesh.primitive_cube_add(size=1, location=P); pl = bpy.context.object
pl.scale = (0.3, 0.01, 0.3); pl.rotation_euler = (0, 0, a); bpy.ops.object.transform_apply(scale=True)
if mode == 'resin':
    m = M.make(bpy, 'bark', 'clear_resin', {'deep': '#CF0913', 'radius': 0.025, 'roughness': 0.05, 'ior': 1.49})
else:
    m = bpy.data.materials.new('g'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (1, 1, 1, 1); b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['Roughness'].default_value = 0.05; b.inputs['IOR'].default_value = 1.49
pl.data.materials.append(m)
d = (P - cam.location).normalized(); r = d - 2 * d.dot(n) * n
E = P + r * 2.0
bpy.ops.mesh.primitive_plane_add(size=6, location=E); em = bpy.context.object
em.rotation_euler = (-r).to_track_quat('Z', 'Y').to_euler()
me = bpy.data.materials.new('e'); me.use_nodes = True; nt = me.node_tree; nt.nodes.clear()
e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Strength'].default_value = 1.0; o = nt.nodes.new('ShaderNodeOutputMaterial')
nt.links.new(e.outputs[0], o.inputs[0]); em.data.materials.append(me)
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_depth = '16'; out = f'/tmp/{mode}-{int(inc)}-{VT[:3]}.png'
sc.render.filepath = out; bpy.ops.render.render(write_still=True)
im = bpy.data.images.load(out); px = list(im.pixels); W = im.size[0]
import statistics
vals = [[px[(y * W + x) * 4 + c] for y in range(24, 40) for x in range(24, 40)] for c in range(3)]
print('RESULT', mode, inc, 'linear RGB', [round(statistics.median(v), 4) for v in vals])
print('RESULT_DISPLAY', mode, inc, VT, 'display 0-255', [round(statistics.median(v) * 255, 1) for v in vals])
