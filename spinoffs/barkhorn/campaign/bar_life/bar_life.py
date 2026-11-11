"""The bar's printed things as boards with their faces printed (kit 'ext'): record sleeves, a newspaper, a book of
matches, a tent card. Each is a thin box, its print on the face toward -y (before turning), the rest its ground.

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/campaign/bar_life/bar_life.py", "fn": "boards",
     "boards": [{"image": "tex/cover-03.png", "w": 0.315, "h": 0.315, "t": 0.003, "x": .., "y": .., "z": ..,
                 "rot": [rx, ry, rz], "ground": "#1C1B1A", "rough": 0.6}, ...]}

`rot` in degrees, about the board's bottom-front-centre; a board lies flat with rot [-90, 0, rz] (its print up).
"""
import math, os
import bmesh
from mathutils import Euler, Vector

HERE = os.path.dirname(os.path.abspath(__file__))


def _hex(h):
    c = [int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    return [((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c]


def _print(bpy, img, ground, rough):
    key = f'print-{os.path.basename(img)}-{ground}-{rough}'
    m = bpy.data.materials.get(key)
    if m:
        return m
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'); b.inputs['Roughness'].default_value = rough
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(os.path.join(HERE, img), check_existing=True)
    tex.extension = 'EXTEND'
    nt.links.new(nt.nodes.new('ShaderNodeUVMap').outputs['UV'], tex.inputs['Vector'])
    nt.links.new(tex.outputs['Color'], b.inputs['Base Color'])
    return m


def _plain(bpy, hx, rough):
    key = f'ground-{hx}-{rough}'
    m = bpy.data.materials.get(key)
    if m:
        return m
    m = bpy.data.materials.new(key); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value = (*_hex(hx), 1.0); b.inputs['Roughness'].default_value = rough
    return m


def boards(bpy, name, p, kit):
    objs = []
    for k, c in enumerate(p['boards']):
        w, h, t = c['w'], c['h'], c.get('t', 0.003)
        bm = bmesh.new()
        g = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((w, t, h)), verts=g['verts'])
        bmesh.ops.translate(bm, vec=Vector((0, t / 2, h / 2)), verts=g['verts'])
        if c.get('ease', 0.0005) > 0:
            bmesh.ops.bevel(bm, geom=bm.edges[:], offset=min(c.get('ease', 0.0005), t * 0.45), segments=1, affect='EDGES')
        uv = bm.loops.layers.uv.new('UVMap')
        for f in bm.faces:
            front = f.normal.y < -0.9
            f.material_index = 0 if front else 1
            for lp in f.loops:
                lp[uv].uv = (lp.vert.co.x / w + 0.5, lp.vert.co.z / h)
        me = bpy.data.meshes.new(f'{name}-{k}'); bm.to_mesh(me); bm.free()
        me.materials.append(_print(bpy, c['image'], c.get('ground', '#1C1B1A'), c.get('rough', 0.6)))
        me.materials.append(_plain(bpy, c.get('ground', '#1C1B1A'), c.get('rough', 0.6)))
        ob = bpy.data.objects.new(f'{name}-{k}', me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (c['x'], c['y'], c['z'])
        ob.rotation_euler = Euler([math.radians(a) for a in c.get('rot', [0, 0, 0])], 'XYZ')
        objs.append(ob)
    return objs
