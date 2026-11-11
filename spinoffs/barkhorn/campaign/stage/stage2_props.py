"""THE STAGE, second version: its set pieces as kit 'ext' props.

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/campaign/stage/stage2_props.py", "fn": "scenic",
     "pieces": [{"tint": "ember", "x": .., "y": .., "z": .., "height": 1.2, "yaw": 0, "flip": false}, ...]}
        each piece its layers from scenic.json, 18 mm thick, matte, the layers 60 mm apart in depth (back first);
    {"kind": "kit", "shape": "ext", "path": ..., "fn": "backdrop", "x0", "x1", "y", "z0", "z1", "stops": [[v, hex], ...]}
        a painted cloth: a soft vertical gradient (v 0 at the foot, 1 at the top), matte;
    {"kind": "kit", "shape": "ext", "path": ..., "fn": "pendants", "top_z": .., ...lamps_final's own keys...}
        the lamps by lamps_final.place (the lane's own builder, unchanged), each Hemisphere's cord then run up to
        `top_z` (out of frame): the brief's "cords as long as that takes". Nothing else about the lamps is touched.
"""
import json, math, os, sys
import bmesh
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))


def _hex(h):
    c = [int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    return [((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c]


def _matte(bpy, name, hx, rough=0.85):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value = (*_hex(hx), 1.0); b.inputs['Roughness'].default_value = rough
    return m


def scenic(bpy, name, p, kit):
    data = json.load(open(os.path.join(HERE, 'scenic.json')))
    objs = []
    for k, c in enumerate(p['pieces']):
        H, t, gap = c.get('height', 1.0), c.get('thick', 0.018), c.get('gap', 0.06)
        layers = data[c['tint']]
        nd = max(l['depth'] for l in layers)
        bm = bmesh.new(); mats = []
        for l in layers:
            uv = l['outline']
            if c.get('flip'):
                uv = [[1 - u, v] for u, v in uv][::-1]
            y0 = (nd - l['depth']) * gap                          # the back layer furthest back
            vs = [bm.verts.new(((u - 0.5) * H, y0, v * H)) for u, v in uv]
            try:
                f = bm.faces.new(vs)
            except ValueError:
                continue
            if f.normal.y > 0:
                f.normal_flip()
            r = bmesh.ops.extrude_face_region(bm, geom=[f])
            mv = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
            bmesh.ops.translate(bm, vec=Vector((0, t, 0)), verts=mv)
            if l['color'] not in mats:
                mats.append(l['color'])
        # every face of a layer carries its layer's colour: assign by the face's depth band
        for fc in bm.faces:
            yc = sum(v.co.y for v in fc.verts) / len(fc.verts)
            band = min(nd, max(0, round((yc - t / 2) / gap)))
            want = [l['color'] for l in layers if (nd - l['depth']) == band]
            if want:
                fc.material_index = mats.index(want[0])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        me = bpy.data.meshes.new(f'{name}-{c["tint"]}-{k}'); bm.to_mesh(me); bm.free()
        for hx in mats:
            me.materials.append(_matte(bpy, f'scenic-{hx}', hx))
        ob = bpy.data.objects.new(f'{name}-{c["tint"]}-{k}', me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (c['x'], c['y'], c.get('z', 0.0)); ob.rotation_euler = (0.0, 0.0, math.radians(c.get('yaw', 0.0)))
        objs.append(ob)
    return objs


def backdrop(bpy, name, p, kit):
    """A painted cloth with a soft vertical gradient: a plane, its colour from a colour ramp on its height."""
    x0, x1, y, z0, z1 = p['x0'], p['x1'], p['y'], p['z0'], p['z1']
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in ((x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1))]
    bm.faces.new(vs)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'); b.inputs['Roughness'].default_value = 0.95
    tc = nt.nodes.new('ShaderNodeTexCoord'); sx = nt.nodes.new('ShaderNodeSeparateXYZ')
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = z0; mr.inputs['From Max'].default_value = z1
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp; cr.interpolation = 'EASE'
    stops = p['stops']
    while len(cr.elements) < len(stops):
        cr.elements.new(0.5)
    for e, (v, hx) in zip(cr.elements, stops):
        e.position = v; e.color = (*_hex(hx), 1.0)
    nt.links.new(tc.outputs['Object'], sx.inputs[0]); nt.links.new(sx.outputs['Z'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return [ob]


def lamps(bpy, name, p, kit):
    """The lamps by lamps_final.place (unchanged), the Hemispheres then scaled by `hemi_scale` about each one's rim
    centre (the shade, its ring of LEDs and their emitting faces together; the lumens unchanged: a bigger shade, the
    same light), their cords then run up to `top_z`. The Hemisphere's size is the owner's open question (2026-11-11:
    "double the diameter of the core? Maybe 1.5?"): one factor, so a scene re-renders at 1.0, 1.5 or 2.0."""
    sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'afterhours'))
    import lamps_final
    k = float(p.get('hemi_scale', 1.0))
    before = set(bpy.context.scene.objects)
    objs = lamps_final.place(bpy, name + '-hemi', {**p, 'cores': []}, kit) if p.get('hemispheres') else []
    hemi_new = [o for o in bpy.context.scene.objects if o not in before]
    rims = [Vector((h['x'], h['y'], h['rim_z'])) for h in p.get('hemispheres', [])]
    if k != 1.0 and rims:
        bpy.context.view_layer.update()
        for o in hemi_new:
            if o.parent is not None and o.parent in hemi_new:
                continue
            c = min(rims, key=lambda r: (Vector((o.matrix_world.translation.x, o.matrix_world.translation.y, 0)) - Vector((r.x, r.y, 0))).length)
            o.location = c + (o.location - c) * k
            o.scale = o.scale * k
        bpy.context.view_layer.update()
    top = p.get('top_z')
    if top is not None:
        for o in hemi_new:
            if o.type == 'MESH' and o.name.split('.')[0] == 'cord':
                o.data = o.data.copy()
                mw = o.matrix_world; inv = mw.inverted()
                zl = (inv @ Vector((mw.translation.x, mw.translation.y, top))).z
                hi = max(v.co.z for v in o.data.vertices)
                for v in o.data.vertices:
                    if v.co.z > hi - 0.002:
                        v.co.z = zl
    if p.get('cores'):
        before = set(bpy.context.scene.objects)
        objs += lamps_final.place(bpy, name + '-core', {**p, 'hemispheres': []}, kit)
        cb = p.get('core_base')
        if cb:   # (the owner, 2026-11-11 16:25: Core's base satin black, not shiny plastic: until the lamps lane ships it,
                 # the base and the dock overridden to a satin black here)
            m = _matte(bpy, 'core-base-satin', cb.get('color', '#0B0B0C'), cb.get('roughness', 0.45))
            n = 0
            for o in [o for o in bpy.context.scene.objects if o not in before]:
                if o.type == 'MESH' and o.name.split('.')[0] in ('dock', 'base'):
                    for sl in o.material_slots:
                        sl.material = m
                    n += 1
            print('CORE base satin:', n, 'parts')
    print('LAMPS hemi_scale', k, 'cords to', top)
    return objs


def pendants(bpy, name, p, kit):
    sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'afterhours'))
    import lamps_final
    before = set(bpy.context.scene.objects)
    objs = lamps_final.place(bpy, name, p, kit)
    top = p['top_z']
    n = 0
    for o in [o for o in bpy.context.scene.objects if o not in before]:
        if o.type == 'MESH' and o.name.split('.')[0] == 'cord':
            o.data = o.data.copy()                                  # its own mesh, so each cord runs to its own length
            mw = o.matrix_world; inv = mw.inverted()
            zl = (inv @ Vector((mw.translation.x, mw.translation.y, top))).z
            hi = max(v.co.z for v in o.data.vertices)
            for v in o.data.vertices:
                if v.co.z > hi - 0.002:
                    v.co.z = zl
            n += 1
    print('PENDANTS cords run up to', top, ':', n)
    return objs
