"""The Hemisphere alone in a black world, to see whether the COB lights the opal (2026-11-09 23:40; lamp-alone/README.txt).

    python3.11 -c "import sys; sys.argv=[\"x\", \"liner-off\"]; exec(open(\"spinoffs/barkhorn/night-pictures/lamp_alone.py\").read())"

The last argument is liner-on or liner-off; with black-reflector also in argv, the reflector is matte black.
Writes /home/user/night-work/lamp-alone-MODE.exr and .png.
"""
import sys, os, math
sys.path.insert(0, '/home/user/earf/spinoffs/barkhorn/night-pictures')
import bpy, numpy as np
import night_room as NR
mode = sys.argv[-1]          # 'liner-off' or 'liner-on'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
Wd = bpy.data.worlds.new('w'); sc.world = Wd; Wd.use_nodes = True
Wd.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
got = NR._append_lamp(bpy, '/home/user/night-work/lamps-v5/hemi-fog-night.blend', (0.0, 0.0, 0.0), honest_cob=0.011)
if mode == 'liner-off':
    for m in bpy.data.materials:
        if m.node_tree:
            for nd in m.node_tree.nodes:
                if nd.type == 'EMISSION':
                    for l in list(nd.inputs['Strength'].links): m.node_tree.links.remove(l)
                    nd.inputs['Strength'].default_value = 0.0
if 'black-reflector' in sys.argv:
    bm = bpy.data.materials.new('black'); bm.use_nodes = True
    bm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0, 0, 0, 1)
    bm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1.0
    bm.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.0
    for n in got:
        if n.startswith('reflector'):
            o = bpy.data.objects[n]
            for sl in o.material_slots: sl.material = bm
    mode = mode + '-black-reflector'
bpy.context.view_layer.update()
opal = bpy.data.objects[[n for n in got if n == 'opal'][0]]
zs = [(opal.matrix_world @ v.co).z for v in opal.data.vertices]; z0, z1 = min(zs), max(zs)
print('opal z', round(z0, 4), round(z1, 4), 'cob z', round(bpy.data.objects['cob'].matrix_world.translation.z, 4), flush=True)
cd = bpy.data.cameras.new('c'); cd.lens = 85; co = bpy.data.objects.new('c', cd); sc.collection.objects.link(co)
zc = (z0 + z1) / 2; co.location = (0, -1.2, zc + 0.25); 
from mathutils import Vector
co.rotation_euler = (Vector((0, 0, zc)) - co.location).to_track_quat('-Z', 'Y').to_euler(); sc.camera = co
sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = 256; cy.use_denoising = False
cy.caustics_reflective = True; cy.caustics_refractive = True; cy.sample_clamp_indirect = 0.0
cy.max_bounces = 32; cy.transmission_bounces = 32; cy.glossy_bounces = 16
sc.render.resolution_x = 400; sc.render.resolution_y = 300
sc.view_settings.view_transform = 'Standard'; sc.render.image_settings.file_format = 'OPEN_EXR'
out = f'/home/user/night-work/lamp-alone-{mode}.exr'; sc.render.filepath = out
bpy.ops.render.render(write_still=True)
im = bpy.data.images.load(out); a = np.array(im.pixels[:], dtype=np.float32).reshape(300, 400, 4)[::-1]
y = a[..., :3] @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
m = y > 1e-5
print(f'RESULT {mode}: lit px {m.sum()}, the dome region (rows 120-200, cols 120-280) median {np.median(y[120:200,120:280]):.4f} p90 {np.percentile(y[120:200,120:280],90):.4f} max {y.max():.3f}', flush=True)
from PIL import Image
v = np.clip((y / max(np.percentile(y, 99), 1e-6)) ** (1/2.2), 0, 1)
Image.fromarray((v * 255).astype(np.uint8)).save(out.replace('.exr', '.png'))
