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


def shot_plaza(sc):
    sc.view_settings.exposure = 0.0
    w = sc.world.node_tree; bg = w.nodes['Background']
    sky = w.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'MULTIPLE_SCATTERING'
    try:
        sky.sun_elevation = math.radians(-2.5); sky.sun_rotation = math.radians(200); sky.altitude = 0
    except Exception:
        pass
    w.links.new(sky.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.6
    # the plaza: stone pavers, wet enough to hold a reflection
    m = bpy.data.materials.new('pavers'); m.use_nodes = True; nt = m.node_tree; p = nt.nodes['Principled BSDF']
    br = P.node(nt, 'ShaderNodeTexBrick', (-500, 0), Scale=0.6, **{'Mortar Size': 0.012})
    br.inputs['Color1'].default_value = P.lin('#6B6863'); br.inputs['Color2'].default_value = P.lin('#5A5853')
    br.inputs['Mortar'].default_value = P.lin('#2C2B29')
    nt.links.new(br.outputs['Color'], p.inputs['Base Color'])
    p.inputs['Roughness'].default_value = 0.32
    bpy.ops.mesh.primitive_plane_add(size=200); bpy.context.object.data.materials.append(m)
    # buildings round it, dark with lit windows
    win = bpy.data.materials.new('facade'); win.use_nodes = True; nt = win.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = P.lin('#1A1A1E'); p.inputs['Roughness'].default_value = 0.8
    bk = P.node(nt, 'ShaderNodeTexBrick', (-600, -200), Scale=0.45, Bias=-0.55, **{'Mortar Size': 0.18, 'Brick Width': 1.1, 'Row Height': 0.5})
    bk.inputs['Color1'].default_value = P.lin('#FFD7A0'); bk.inputs['Color2'].default_value = (0, 0, 0, 1)
    bk.inputs['Mortar'].default_value = (0, 0, 0, 1)
    tc = P.node(nt, 'ShaderNodeTexCoord', (-900, -200)); nt.links.new(tc.outputs['Object'], bk.inputs['Vector'])
    nz = P.node(nt, 'ShaderNodeTexWhiteNoise', (-900, -400))
    nt.links.new(bk.outputs['Color'], p.inputs['Emission Color'])
    p.inputs['Emission Strength'].default_value = 2.5
    dark = P.mat_basic('skyline', '#0E0E12', rough=0.9)
    import random
    random.seed(4)
    x = -160.0
    while x < 160:                      # a far skyline, in silhouette
        w_ = random.uniform(8, 22); h = random.uniform(3, 13)
        P.box('bld', x, 180, 0, x + w_, 190, h, dark); x += w_ + random.uniform(0, 4)
    # the plinth and the globe, 4 m across, lifted 0.6 m
    plinth = P.mat_basic('plinth', '#151417', rough=0.25)
    P.cylinder('plinth', 1.6, 0.6, (0, 0, 0), plinth, verts=128)
    globe(4.0 / 0.3, 0.6 - 0.0181 * 4.0 / 0.3)
    # a low warm uplight from the plinth's rim, and the street's own spill
    P.area('up', (0, -2.2, 0.62), (0, 0, 3.0), 1.2, 900, '#FFE2C0')
    P.area('spill', (-14, -12, 7), (0, 0, 1), 6.0, 2500, '#FFC890')
    P.camera((4.2, -16.5, 1.6), (0.0, 0.0, 3.6), lens=30)


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
    sc.render.filepath = args.out or os.path.join(P.OUT, f'idea-{args.shot}.png')
    bpy.ops.render.render(write_still=True)
    print('wrote', sc.render.filepath)


if __name__ == '__main__':
    main()
