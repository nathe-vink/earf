"""How many times does glass_shadows' tint reach a shadow ray through one wall? A 20 mm slab like a habitat wall (glass
surface + volume absorption, the shadow-ray mix as habitat.py builds it) over a white floor under an overhead sun;
the floor under it against the open floor gives the effective transmission; compare with tr, tr^2, tr^3."""
import math, sys
import bpy, bmesh

COL, DENS, MM = (1.0, 0.9023, 0.0), 75.9, 0.020          # Acid's old cabinet (any tint will do)
FRES = float(sys.argv[1]) if len(sys.argv) > 1 else 0.92
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 64; sc.cycles.use_denoising = False
sc.render.resolution_x = sc.render.resolution_y = 200; sc.view_settings.view_transform = 'Standard'
sc.cycles.max_bounces = 0; sc.cycles.transparent_max_bounces = 16   # direct light only
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
NOVOL = len(sys.argv) > 2 and sys.argv[2] == 'novol'
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[1].default_value = 0.0

def mesh_box(name, sx, sy, sz, z):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co.x *= sx; v.co.y *= sy; v.co.z = v.co.z * sz + z
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); return o

floor = mesh_box('floor', 4, 4, 0.01, -0.005)
fm = bpy.data.materials.new('floor'); fm.use_nodes = True
fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1); floor.data.materials.append(fm)
slab = mesh_box('slab', 1.0, 2.0, MM, 0.5)               # covers the left half of the floor under the camera
slab.location.x = -0.5
m = bpy.data.materials.new('bark'); m.use_nodes = True; nt = m.node_tree
bs = nt.nodes['Principled BSDF']; bs.inputs['Transmission Weight'].default_value = 1.0; bs.inputs['IOR'].default_value = 1.49
bs.inputs['Roughness'].default_value = 0.05
out = nt.nodes['Material Output']
va = nt.nodes.new('ShaderNodeVolumeAbsorption'); va.inputs['Color'].default_value = (*COL, 1); va.inputs['Density'].default_value = DENS
if not NOVOL: nt.links.new(va.outputs[0], out.inputs['Volume'])
tr = [FRES * math.exp(-(1 - COL[i]) * DENS * MM) for i in range(3)]
FACE = [math.sqrt(FRES)] * 3 if 'perface' in sys.argv else tr
lp = nt.nodes.new('ShaderNodeLightPath'); tp = nt.nodes.new('ShaderNodeBsdfTransparent'); tp.inputs['Color'].default_value = (*FACE, 1)
mx = nt.nodes.new('ShaderNodeMixShader')
nt.links.new(lp.outputs['Is Shadow Ray'], mx.inputs[0]); nt.links.new(bs.outputs[0], mx.inputs[1]); nt.links.new(tp.outputs[0], mx.inputs[2])
nt.links.new(mx.outputs[0], out.inputs['Surface'])
slab.data.materials.append(m)
slab.visible_camera = False                               # the camera sees only the floor, lit through the slab or not

sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sun.data.energy = 3.0; sun.data.angle = 0.0
sc.collection.objects.link(sun)
cd = bpy.data.cameras.new('c'); cd.type = 'ORTHO'; cd.ortho_scale = 2.0
cam = bpy.data.objects.new('c', cd); cam.location = (0, 0, 3); sc.collection.objects.link(cam); sc.camera = cam
sc.render.filepath = '/tmp/claude-0/-home-user-earf/57ed16bf-b821-5fb9-96e8-d26782970682/scratchpad/trace/slab.exr'
sc.render.image_settings.file_format = 'OPEN_EXR'; sc.render.image_settings.color_depth = '32'
bpy.ops.render.render(write_still=True)
img = bpy.data.images.load(sc.render.filepath); px = list(img.pixels); W = H = 200
def mean(x0, x1):
    s = [0.0, 0.0, 0.0]; n = 0
    for y in range(60, 140):
        for x in range(x0, x1):
            i = (y * W + x) * 4; s = [s[k] + px[i + k] for k in range(3)]; n += 1
    return [v / n for v in s]
under, openf = mean(20, 80), mean(120, 180)
eff = [u / o if o else 0 for u, o in zip(under, openf)]
print('volume', 'off' if NOVOL else 'on', '| face colour', [round(x, 3) for x in FACE], '| per-wall factor', FRES, '| tr (once)', [round(x, 3) for x in tr])
print('effective transmission under the slab', [round(x, 3) for x in eff])
print('tr^2', [round(x * x, 3) for x in tr], '| tr^3', [round(x ** 3, 3) for x in tr],
      '| tr^2 x volume', [round(t * t * math.exp(-(1 - COL[i]) * DENS * MM), 3) for i, t in enumerate(tr)])
