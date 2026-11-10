import sys, os, math
sys.path.insert(0, '/home/user/earf/spinoffs/barkhorn/companions'); sys.path.insert(0, '/home/user/earf/spinoffs/barkhorn/companions/launch')
os.environ['AUDIT'] = '1'; os.environ['COB_LM'] = '0'; os.environ['LINER_LM'] = os.environ.get('LM', '145')
import lamp_site as L
L.build('dome-blue', 1, 0.2)
import bpy, bmesh
sc = bpy.context.scene
for o in list(sc.objects):                                  # the dome alone: the set, the studio, the camera out
    if o.name in ('sweep', 'key', 'fill', 'kicker') or o.type in ('LIGHT',):
        bpy.data.objects.remove(o, do_unlink=True)
if sc.world:
    sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
def sensor():
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=5, radius=1.0)
    for f in bm.faces: f.smooth = False
    bmesh.ops.reverse_faces(bm, faces=bm.faces)          # facing in, toward the lamp
    me = bpy.data.meshes.new('sensor'); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('sensor', me); sc.collection.objects.link(ob); ob.location = (0, 0, 0.55)
    m = bpy.data.materials.new('black'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1); b.inputs['Specular IOR Level'].default_value = 0.0; b.inputs['Roughness'].default_value = 1.0
    me.materials.append(m); ca = me.color_attributes.new('E', 'FLOAT_COLOR', 'POINT')
    me.color_attributes.active_color = ca; me.color_attributes.render_color_index = 0
    return ob
def bake(ob):
    for o in sc.objects: o.select_set(False)
    ob.select_set(True); bpy.context.view_layer.objects.active = ob
    sc.render.engine = 'CYCLES'; sc.cycles.samples = int(os.environ.get('SPP', '256'))
    bk = sc.render.bake; bk.target = 'VERTEX_COLORS'; bk.use_pass_direct = True; bk.use_pass_indirect = True; bk.use_pass_color = False
    bpy.ops.object.bake(type='DIFFUSE')
    me = ob.data; col = me.color_attributes['E']; tot = 0.0
    print('ISPHERE dbg max vertex', max(max(c.color[:3]) for c in col.data), 'n', len(col.data), 'lights', [o.name for o in sc.objects if o.type == 'LIGHT'], 'meshes', len([o for o in sc.objects if o.type == 'MESH']))
    import mathutils
    vval = [0.2126 * c.color[0] + 0.7152 * c.color[1] + 0.0722 * c.color[2] for c in col.data]
    for p in me.polygons:
        tot += p.area * sum(vval[i] for i in p.vertices) / len(p.vertices)
    return tot
s = sensor()
liner = bake(s)
# calibration: the same bake with the dome gone and a 1 W point light at the dome's place
for o in list(sc.objects):
    if o.name != 'sensor': bpy.data.objects.remove(o, do_unlink=True)
ld = bpy.data.lights.new('cal', 'POINT'); ld.energy = 1.0; ld.shadow_soft_size = 0.01; ld.color = (1, 1, 1)
lo = bpy.data.objects.new('cal', ld); sc.collection.objects.link(lo); lo.location = (0, 0, 0.55)
cal = bake(s)
WLM = 3.2 / 490.0
print('ISPHERE baked integral liner', liner, 'cal (1 W)', cal, '=> liner W', liner / cal if cal else None, 'lm', liner / cal / WLM if cal else None)
