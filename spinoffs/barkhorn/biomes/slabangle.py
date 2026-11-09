"""The shadow ray through one wall at an angle: a 20 mm slab of tinted acrylic (glass surface + volume absorption, the
shadow-ray mix as habitat.py builds it, the faces flat sqrt(0.92) or Schlick by incidence) tilted THETA degrees under
an overhead sun, over a white floor. The floor under the slab with it against without it gives the effective
transmission; compared with (1 - F(theta))^2 x exp(-a d / cos theta), F the unpolarized Fresnel (exact and Schlick).

usage: python3.11 slabangle.py THETA flat|schlick
"""
import math
import os
import sys

import bpy
import bmesh

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from habitat import schlick_face  # noqa: E402

COL, DENS, MM, N = (1.0, 0.9023, 0.0), 75.9, 0.020, 1.49
TH = float(sys.argv[1]); MODE = sys.argv[2]
OUT = os.environ.get('SLAB_OUT', '/tmp/slabangle.exr')


def fresnel(c, n=N):
    """Unpolarized dielectric reflectance, air to n, cos of incidence c."""
    s = math.sqrt(max(0.0, 1 - (1 - c * c) / (n * n)))
    rs = ((c - n * s) / (c + n * s)) ** 2; rp = ((n * c - s) / (n * c + s)) ** 2
    return 0.5 * (rs + rp)


def schlick(c, n=N):
    r0 = ((n - 1) / (n + 1)) ** 2
    return r0 + (1 - r0) * (1 - c) ** 5


def render(with_slab):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 64; sc.cycles.use_denoising = False
    sc.render.resolution_x = sc.render.resolution_y = 200; sc.view_settings.view_transform = 'Standard'
    sc.cycles.max_bounces = 0; sc.cycles.transparent_max_bounces = 16
    sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[1].default_value = 0.0

    def box(name, sx, sy, sz, z):
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co.x *= sx; v.co.y *= sy; v.co.z *= sz
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.location.z = z; return o
    fl = box('floor', 6, 6, 0.01, -0.005)
    fm = bpy.data.materials.new('floor'); fm.use_nodes = True
    fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1); fl.data.materials.append(fm)
    if with_slab:
        sl = box('slab', 3.0, 2.0, MM, 0.8); sl.rotation_euler.y = math.radians(TH)
        m = bpy.data.materials.new('bark'); m.use_nodes = True; nt = m.node_tree
        bs = nt.nodes['Principled BSDF']; bs.inputs['Transmission Weight'].default_value = 1.0; bs.inputs['IOR'].default_value = N
        bs.inputs['Roughness'].default_value = 0.05
        out = nt.nodes['Material Output']
        va = nt.nodes.new('ShaderNodeVolumeAbsorption'); va.inputs['Color'].default_value = (*COL, 1); va.inputs['Density'].default_value = DENS
        nt.links.new(va.outputs[0], out.inputs['Volume'])
        lp = nt.nodes.new('ShaderNodeLightPath'); tp = nt.nodes.new('ShaderNodeBsdfTransparent')
        tp.inputs['Color'].default_value = (*[math.sqrt(0.92)] * 3, 1)
        if MODE == 'schlick':
            schlick_face(nt, tp, N)
        mx = nt.nodes.new('ShaderNodeMixShader')
        nt.links.new(lp.outputs['Is Shadow Ray'], mx.inputs[0]); nt.links.new(bs.outputs[0], mx.inputs[1]); nt.links.new(tp.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], out.inputs['Surface'])
        sl.data.materials.append(m); sl.visible_camera = False
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sun.data.energy = 3.0; sun.data.angle = 0.0
    sc.collection.objects.link(sun)
    cd = bpy.data.cameras.new('c'); cd.type = 'ORTHO'; cd.ortho_scale = 2.0
    cam = bpy.data.objects.new('c', cd); cam.location = (0, 0, 3); sc.collection.objects.link(cam); sc.camera = cam
    sc.render.filepath = OUT; sc.render.image_settings.file_format = 'OPEN_EXR'; sc.render.image_settings.color_depth = '32'
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(OUT); px = list(img.pixels); W = 200
    s = [0.0, 0.0, 0.0]; n = 0
    for y in range(70, 130):
        for x in range(85, 115):       # the slab's footprint centre (at 75 deg it is 0.78 m wide, +-39 px)
            i = (y * W + x) * 4; s = [s[k] + px[i + k] for k in range(3)]; n += 1
    return [v / n for v in s]


under, openf = render(True), render(False)
eff = [u / o for u, o in zip(under, openf)]
c = math.cos(math.radians(TH))
vol = [math.exp(-(1 - COL[i]) * DENS * MM / c) for i in range(3)]
print(f'theta {TH:4.0f} deg  faces {MODE:7s}  measured {[round(x, 4) for x in eff]}')
print(f'  exact (1-F)^2 x vol {[round((1 - fresnel(c)) ** 2 * v, 4) for v in vol]}  (1-F {1 - fresnel(c):.4f})')
print(f'  schlick (1-F)^2 x vol {[round((1 - schlick(c)) ** 2 * v, 4) for v in vol]}  | flat 0.92 x vol {[round(0.92 * v, 4) for v in vol]}')
