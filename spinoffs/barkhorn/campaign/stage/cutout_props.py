"""The stage's cutout props as a set prop (kit 'ext'): flat plywood boards cut to each tint's icon outline
(cutouts.json, make_cutouts.py), the icon painted on the front, the plywood's raw edge and back showing, each on a
little triangular brace behind. Plainly hand-made: a school play's flats.

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/campaign/stage/cutout_props.py", "fn": "place",
     "cutouts": [{"key": "fog", "x": .., "y": .., "z": .., "height": 0.5, "yaw": 0}, ...]}

`key` is a cutouts.json entry (a tint, or 'poison-sign'); `height` the board's icon box in metres (the board itself is
the outline inside that box); `stake` (metres) puts the board on a square stake that high instead of a brace; `thick`
the board's thickness (default 15 mm).
"""
import json, math, os
import bmesh
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))


def _paint(bpy, img_path, flip, name):
    """The icon painted on the board's face: the icon's colours where it is opaque, a cream ground coat elsewhere."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(img_path, check_existing=True)
    tex.interpolation = 'Cubic'; tex.extension = 'CLIP'
    uv = nt.nodes.new('ShaderNodeUVMap')
    if flip:
        mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, -1, 1); mp.inputs['Location'].default_value = (0, 1, 0)
        nt.links.new(uv.outputs['UV'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], tex.inputs['Vector'])
    else:
        nt.links.new(uv.outputs['UV'], tex.inputs['Vector'])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = (0.80, 0.74, 0.62, 1.0)                 # the ground coat, a warm cream
    nt.links.new(tex.outputs['Alpha'], mix.inputs['Factor']); nt.links.new(tex.outputs['Color'], mix.inputs['B'])
    nt.links.new(mix.outputs['Result'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = 0.62                              # flat emulsion
    return m


def _board(bm, outline, H, t):
    """The outline (0-1, v up) as a face in x-z, H across, front at y = 0 facing -y, extruded t back (+y)."""
    vs = [bm.verts.new(((u - 0.5) * H, 0.0, v * H)) for u, v in outline]
    f = bm.faces.new(vs)
    if f.normal.y > 0:
        f.normal_flip()
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    moved = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=Vector((0, t, 0)), verts=moved)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return f


def place(bpy, name, p, kit):
    import assets
    data = json.load(open(os.path.join(HERE, 'cutouts.json')))
    ply = assets.pbr(bpy, 'plywood', '2k', name='cutout-plywood')
    objs = []
    for k, c in enumerate(p['cutouts']):
        d = data[c['key']]
        H, t = c.get('height', 0.5), c.get('thick', 0.015)
        bm = bmesh.new()
        vmin = min(v for _, v in d['outline'])                  # the board stands on its lowest point
        _board(bm, [[u, v - vmin] for u, v in d['outline']], H, t)
        uvl = bm.loops.layers.uv.new('UVMap')
        for f in bm.faces:
            f.material_index = 0 if (f.normal.y < -0.9 and abs(max(v.co.y for v in f.verts)) < 1e-6) else 1
            for lp in f.loops:
                lp[uvl].uv = ((lp.vert.co.x / H) + 0.5, lp.vert.co.z / H + vmin)
        z0 = c.get('stake', 0.0)
        # the support: a little triangular brace behind (a flat's jack), or a square stake for a sign
        if z0:
            g = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=Vector((0.022, 0.022, z0 + 0.4 * H)), verts=g['verts'])
            bmesh.ops.translate(bm, vec=Vector((0, t + 0.012, (z0 + 0.4 * H) / 2 - z0)), verts=g['verts'])
        else:
            bh = 0.62 * H; bd = 0.32 * H
            tri = [(0.0, t, 0.0), (0.0, t + bd, 0.0), (0.0, t, bh)]
            vs = [bm.verts.new((x - 0.009, y, z)) for x, y, z in tri]
            f = bm.faces.new(vs)
            r = bmesh.ops.extrude_face_region(bm, geom=[f])
            mv = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
            bmesh.ops.translate(bm, vec=Vector((0.018, 0, 0)), verts=mv)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        # every face added after the board's own (the support) is plywood
        nb = len(d['outline']) + 2
        for i, f in enumerate(bm.faces):
            if i >= nb:
                f.material_index = 1
        me = bpy.data.meshes.new(f'{name}-{c["key"]}-{k}'); bm.to_mesh(me); bm.free()
        me.materials.append(_paint(bpy, os.path.join(HERE, d['image']), d['flip'], f'paint-{c["key"]}'))
        me.materials.append(ply)
        ob = bpy.data.objects.new(f'{name}-{c["key"]}-{k}', me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (c['x'], c['y'], c.get('z', 0.0) + z0)
        ob.rotation_euler = (0.0, 0.0, math.radians(c.get('yaw', 0.0)))
        objs.append(ob)
    return objs
