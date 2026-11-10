"""The enclosing sensor (2026-11-10, generalising isphere_liner.py): the lm leaving a lamp of the site rig, its own
lights only (the set, the studio and the world gone). A 1 m inward icosphere, 50 % grey, baked DIFFUSE (light only)
to vertex colours, calibrated by the same bake round a 1 W point light at the same place. Env: FRAME (orb-blue,
dome-red, ...), BOUNCES (rig: the rig's own limits; or a number for every bounce kind), SPP; the rig's own switches
pass through (WINDOW, HEMI_LM, ...). Prints the total and, for a dome, the split above and below the rim plane."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['AUDIT'] = '1'
import lamp_site as L
fr = os.environ.get('FRAME', 'orb-blue')
L.build(fr, 1, 0.2)
import bpy, bmesh
sc = bpy.context.scene
for o in list(sc.objects):
    if o.name in ('sweep', 'key', 'fill', 'kicker'):
        bpy.data.objects.remove(o, do_unlink=True)
if sc.world:
    for n in sc.world.node_tree.nodes:
        if n.type == 'BACKGROUND':
            n.inputs['Strength'].default_value = 0.0
for pre in [x for x in os.environ.get('DROP', '').split(',') if x]:   # e.g. DROP=ball- (the outer ball off)
    for o in list(sc.objects):
        if o.name.startswith(pre):
            bpy.data.objects.remove(o, do_unlink=True)
b = os.environ.get('BOUNCES', 'rig')
if b != 'rig':
    n = int(b); c = sc.cycles
    c.max_bounces = c.diffuse_bounces = c.glossy_bounces = c.transmission_bounces = c.transparent_max_bounces = n
print('BOUNCES max', sc.cycles.max_bounces, 'diffuse', sc.cycles.diffuse_bounces, 'glossy', sc.cycles.glossy_bounces,
      'transmission', sc.cycles.transmission_bounces, 'caustics refr/refl', sc.cycles.caustics_refractive, sc.cycles.caustics_reflective)
zc = 0.5 if fr.startswith('dome') else 0.10            # the rim plane (dome) or about the ball's centre (orb)
def sensor():
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=5, radius=1.0)
    for f in bm.faces: f.smooth = False
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    me = bpy.data.meshes.new('sensor'); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('sensor', me); sc.collection.objects.link(ob); ob.location = (0, 0, zc)
    m = bpy.data.materials.new('grey'); m.use_nodes = True; bs = m.node_tree.nodes['Principled BSDF']
    bs.inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1); bs.inputs['Specular IOR Level'].default_value = 0.0; bs.inputs['Roughness'].default_value = 1.0
    me.materials.append(m); ca = me.color_attributes.new('E', 'FLOAT_COLOR', 'POINT')
    me.color_attributes.active_color = ca; me.color_attributes.render_color_index = 0
    return ob
def bake(ob):
    for o in sc.objects: o.select_set(False)
    ob.select_set(True); bpy.context.view_layer.objects.active = ob
    sc.cycles.samples = int(os.environ.get('SPP', '256'))
    bk = sc.render.bake; bk.target = 'VERTEX_COLORS'; bk.use_pass_direct = True; bk.use_pass_indirect = True; bk.use_pass_color = False
    bpy.ops.object.bake(type='DIFFUSE')
    me = ob.data; col = me.color_attributes['E']
    v = [0.2126 * c.color[0] + 0.7152 * c.color[1] + 0.0722 * c.color[2] for c in col.data]
    up = dn = 0.0
    for p in me.polygons:
        e = p.area * sum(v[i] for i in p.vertices) / len(p.vertices)
        if p.center.z >= 0: up += e
        else: dn += e
    return up, dn
s = sensor()
lu, ld_ = bake(s)
for o in list(sc.objects):
    if o.name != 'sensor': bpy.data.objects.remove(o, do_unlink=True)
li = bpy.data.lights.new('cal', 'POINT'); li.energy = 1.0; li.shadow_soft_size = 0.01
lo = bpy.data.objects.new('cal', li); sc.collection.objects.link(lo); lo.location = (0, 0, zc)
cu, cd = bake(s); cal = cu + cd
k = 1.0 / cal / L.WLM
print('ISPHERE', fr, 'total lm', round((lu + ld_) * k, 1), 'above', round(lu * k, 1), 'below', round(ld_ * k, 1))
