"""The big ideas, path-traced (brand lane, r47): Mother EARF at plaza scale, and the Tint Library trade kit.

    python3.11 ideas_render.py --shot plaza|library [--samples 128] [--scale 1] [--out ...]

plaza    Mother EARF as public art: the colour globe (out-globe-colour's GLB, the six discs in their tints) scaled to
         4 m across on a low black plinth, in a stone plaza at dusk, its rims lit. A proposal's picture, not a site.
library  The Tint Library: eight 100 x 100 x 20 mm cast tiles standing in a birch tray in the spectrum's order, the
         lid beside, the coin of each tint in front. For architects and interior designers.
"""
import argparse, math, os, sys
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack_render as P                                   # noqa: E402

GLB = os.path.join(HERE, '..', 'out-globe-colour', 'render', 'earf-globe-colour.glb')
DISC = {'m90': 'poison', 'm30': 'haze', 'm150': 'dust', 'equator': 'ice', 'north': 'ember', 'south': 'acid'}
GLOW = {'ember': '#FF3A22', 'dust': '#FF7A1E', 'acid': '#FFC21A', 'poison': '#43C02A', 'ice': '#2C9BFF', 'haze': '#8A4BFF'}


def emitter(name, color, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = P.lin(color)
    p.inputs['Emission Color'].default_value = P.lin(color)
    p.inputs['Emission Strength'].default_value = strength
    return m


def globe(scale, z0):
    bpy.ops.import_scene.gltf(filepath=GLB)
    objs = [o for o in bpy.context.selected_objects]
    root = bpy.data.objects.new('globe', None); bpy.context.collection.objects.link(root)
    for o in objs:
        if o.parent is None:
            o.parent = root
    for o in list(objs):
        n = o.name.split('.')[0]
        if n.startswith('chip') or n in ('uv', 'base'):
            bpy.data.objects.remove(o, do_unlink=True); continue
        if o.type != 'MESH':
            continue
        kind, key = n.split('-', 1)
        t = DISC.get(key)
        if not t:
            continue
        o.data.materials.clear()
        if kind == 'rim':
            o.data.materials.append(emitter('rim-' + key, GLOW[t], 6.0))
        elif kind == 'face':
            o.hide_render = True
        else:
            m = P.mat_acrylic('disc-' + key, P.TINTS[t], frosted=0.0)
            pb = m.node_tree.nodes['Principled BSDF']   # edge-lit: the light caught in the sheet glows faintly across it
            pb.inputs['Emission Color'].default_value = P.lin(GLOW[t]); pb.inputs['Emission Strength'].default_value = 0.35
            o.data.materials.append(m)
    root.scale = (scale, scale, scale)
    root.location = (0, 0, z0)
    return root


def figure(x, y, h, mat, rot=0.0):
    """A person for scale, in silhouette at dusk: legs, a coat and a head, h tall."""
    parts = []
    for dx in (-0.09, 0.09):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=h * 0.47, location=(x + dx, y, h * 0.235)); parts.append(bpy.context.object)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=h * 0.38, location=(x, y, h * 0.47 + h * 0.19)); parts.append(bpy.context.object)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=h * 0.065, location=(x, y, h * 0.93)); parts.append(bpy.context.object)
    for o in parts:
        o.data.materials.append(mat); o.rotation_euler.z = rot
        bpy.context.view_layer.objects.active = o; bpy.ops.object.shade_smooth()


def tree(x, y, mat_trunk, mat_crown, h=7.0):
    P.cylinder('trunk', 0.14, h * 0.55, (x, y, 0), mat_trunk, verts=16)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=h * 0.28, location=(x, y, h * 0.7))
    c = bpy.context.object; c.scale = (1.0, 1.0, 1.15); c.data.materials.append(mat_crown)
    tex = bpy.data.textures.new('leaf', 'CLOUDS'); tex.noise_scale = 0.6
    d = c.modifiers.new('d', 'DISPLACE'); d.texture = tex; d.strength = 0.6


def lamp_post(x, y, mat, glow):
    P.cylinder('post', 0.06, 4.2, (x, y, 0), mat, verts=16)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(x, y, 4.35)); bpy.context.object.data.materials.append(glow)


def shot_plaza(sc):
    # critic round 1 (4.0): pavers that read, a lit skyline lifted by distance, people, trees and lamps for scale,
    # the uplight hidden, a deeper sky, a honed stone plinth, a lower, closer camera with the globe on the right third
    sc.view_settings.exposure = 0.0
    w = sc.world.node_tree; bg = w.nodes['Background']
    sky = w.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'MULTIPLE_SCATTERING'
    try:
        sky.sun_elevation = math.radians(-3.0); sky.sun_rotation = math.radians(240); sky.altitude = 0
    except Exception:
        pass
    w.links.new(sky.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.5
    # the plaza: granite pavers 600 x 300 with dark joints, a post-rain sheen in patches
    m = bpy.data.materials.new('pavers'); m.use_nodes = True; nt = m.node_tree; p = nt.nodes['Principled BSDF']
    tc = P.node(nt, 'ShaderNodeTexCoord', (-900, 0))
    br = P.node(nt, 'ShaderNodeTexBrick', (-500, 0), Scale=1.0, **{'Mortar Size': 0.012, 'Brick Width': 0.6, 'Row Height': 0.3})
    nt.links.new(tc.outputs['Object'], br.inputs['Vector'])
    br.inputs['Color1'].default_value = P.lin('#7A7670'); br.inputs['Color2'].default_value = P.lin('#5E5B56')
    br.inputs['Mortar'].default_value = P.lin('#1E1D1C')
    nt.links.new(br.outputs['Color'], p.inputs['Base Color'])
    wet = P.node(nt, 'ShaderNodeTexNoise', (-500, -300), Scale=0.15, Detail=3.0)
    rr = P.node(nt, 'ShaderNodeMapRange', (-250, -300)); rr.inputs['To Min'].default_value = 0.18; rr.inputs['To Max'].default_value = 0.55
    nt.links.new(wet.outputs['Fac'], rr.inputs['Value']); nt.links.new(rr.outputs['Result'], p.inputs['Roughness'])
    bm = P.node(nt, 'ShaderNodeBump', (-250, -500), Strength=0.3, Distance=0.004)
    nt.links.new(br.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], p.inputs['Normal'])
    bpy.ops.mesh.primitive_plane_add(size=400); bpy.context.object.data.materials.append(m)
    # the skyline: blue-grey facades lifted by distance, lit windows on the faces toward us
    import random
    random.seed(4)
    for row, (y0, tone, lit) in enumerate([(220, '#2A2E3C', 0.16), (420, '#3A4054', 0.10)]):
        x = -260.0
        while x < 260:
            w_ = random.uniform(14, 34); h = random.uniform(10, 40) * (1.4 if row else 1.0)
            fac = bpy.data.materials.new('fac'); fac.use_nodes = True; nt = fac.node_tree; p = nt.nodes['Principled BSDF']
            p.inputs['Base Color'].default_value = P.lin(tone); p.inputs['Roughness'].default_value = 0.9
            tc = P.node(nt, 'ShaderNodeTexCoord', (-900, 0)); sep = P.node(nt, 'ShaderNodeSeparateXYZ', (-700, 0))
            nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
            comb = P.node(nt, 'ShaderNodeCombineXYZ', (-500, 0))
            nt.links.new(sep.outputs['X'], comb.inputs['X']); nt.links.new(sep.outputs['Z'], comb.inputs['Y'])
            bk = P.node(nt, 'ShaderNodeTexBrick', (-300, 0), Scale=0.5, Bias=-0.75, **{'Mortar Size': 0.35, 'Brick Width': 0.9, 'Row Height': 0.55})
            nt.links.new(comb.outputs['Vector'], bk.inputs['Vector'])
            bk.inputs['Color1'].default_value = P.lin('#FFD49A'); bk.inputs['Color2'].default_value = (0.0, 0.0, 0.0, 1)
            bk.inputs['Mortar'].default_value = (0, 0, 0, 1)
            add = P.node(nt, 'ShaderNodeMix', (-100, -100)); add.data_type = 'RGBA'; add.blend_type = 'ADD'
            add.inputs['Factor'].default_value = 1.0
            add.inputs['A'].default_value = tuple(c * 0.12 for c in P.lin(tone)[:3]) + (1.0,)   # the air between us and it
            nt.links.new(bk.outputs['Color'], add.inputs['B'])
            nt.links.new(add.outputs['Result'], p.inputs['Emission Color']); p.inputs['Emission Strength'].default_value = 3.0
            P.box('bld', x, y0, 0, x + w_, y0 + 20, h, fac); x += w_ + random.uniform(1, 8)
    # dressing: trees and lamps receding left and right, a few people
    trunk = P.mat_basic('trunk', '#1A1714', rough=0.9); crown = P.mat_basic('crown', '#141A14', rough=0.9)
    post = P.mat_basic('post', '#111114', rough=0.5, metal=1.0); glow = P.mat_basic('glow', '#FFE6C0', rough=0.5)
    glow.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value = P.lin('#FFD9A8')
    glow.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 30.0
    for k in range(6):
        tree(-16 - k * 0.6, 8 + k * 10, trunk, crown, h=6.0); tree(15 + k * 0.6, 10 + k * 10, trunk, crown, h=6.0)
        lamp_post(-11, 0 + k * 9, post, glow); lamp_post(10.5, 2 + k * 9, post, glow)
    coat = P.mat_basic('coat', '#16151A', rough=0.8)
    for x, y, h in [(-3.4, -2.4, 1.78), (-2.9, -2.6, 1.66), (5.2, 3.5, 1.74), (-7.5, 6.0, 1.70)]:
        figure(x, y, h, coat, rot=0.3)
    # the plinth, honed black granite, and the globe, 4 m across
    plinth = P.mat_basic('plinth', '#151417', rough=0.45)
    P.cylinder('plinth', 1.6, 0.6, (0, 0, 0), plinth, verts=128, bevel=0.015)
    globe(4.0 / 0.3, 0.6 - 0.0181 * 4.0 / 0.3)
    up = P.area('up', (0, 0, 0.61), (0, 0, 3.0), 1.0, 600, '#FFE2C0')
    up.visible_camera = False; up.visible_glossy = False
    P.area('spill', (-14, -12, 7), (0, 0, 1), 6.0, 1800, '#FFC890')
    P.camera((5.5, -11.0, 1.2), (-1.6, 0.0, 3.0), lens=35, fstop=5.6)


def shot_library(sc):
    P.floor_and_wall('#E4DFD7')
    tray = P.mat_birch('tray')
    order = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
    pitch, tw, th, td = 0.034, 0.020, 0.100, 0.100
    L = pitch * 8 + 0.03
    P.box('tray-base', -L / 2, -0.07, 0, L / 2, 0.07, 0.012, tray)
    P.box('tray-slots', -L / 2, -0.07, 0.012, L / 2, 0.07, 0.03, tray)
    P.box('tray-front', -L / 2, -0.07 - 0.012, 0, L / 2, -0.07, 0.04, tray)
    for i, t in enumerate(order):
        x = -L / 2 + 0.015 + pitch * i + (pitch - tw) / 2
        tile = P.box('tile-' + t, x, -td / 2, 0.022, x + tw, td / 2, 0.022 + th, P.mat_acrylic('tile-' + t, P.TINTS[t]), bevel=0.0015)
    # the lid, standing behind, the wordmark printed on it
    art = os.path.join(HERE, 'out', 'decal-library-lid.png')
    lid = P.mat_birch('lid', decal=art if os.path.exists(art) else None)
    lb = P.box('lid', -L / 2 - 0.004, 0.16, 0.0, L / 2 + 0.004, 0.172, 0.15, lid, uv_face='-y')
    lb.rotation_euler = (math.radians(-8), 0, 0)
    P.area('back', (0.15, 1.2, 0.5), (0, 0, 0.07), 0.8, 60, '#FFFFFF')
    P.area('key', (-0.9, -0.9, 0.9), (0, 0, 0.05), 0.7, 70)
    P.area('fill', (1.0, -0.6, 0.4), (0, 0, 0.05), 0.8, 18, '#EEF2FA')
    P.camera((0.28, -0.78, 0.36), (0.0, -0.02, 0.055), lens=60, fstop=4)
    sc.cycles.caustics_refractive = True


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--shot', default='plaza'); a.add_argument('--samples', type=int, default=128)
    a.add_argument('--scale', type=float, default=1.0); a.add_argument('--out')
    args = a.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    sc = P.reset()
    {'plaza': shot_plaza, 'library': shot_library}[args.shot](sc)
    sc.render.resolution_x, sc.render.resolution_y = int(1800 * args.scale), int(1200 * args.scale)
    sc.cycles.samples = args.samples
    sc.render.filepath = args.out or os.path.join(P.OUT, f'idea-{args.shot}-render.png' if args.shot == 'plaza' else f'idea-{args.shot}.png')
    bpy.ops.render.render(write_still=True)
    print('wrote', sc.render.filepath)


if __name__ == '__main__':
    main()
