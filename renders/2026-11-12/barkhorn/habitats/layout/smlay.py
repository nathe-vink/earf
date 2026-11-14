# Smoke layout proof (coordinator 04:21): clay shapes only, no volumes. Level camera as render.py
# (36 mm horizontal sensor, tilt -> shift_y). Prints where the key points land as shares of the frame.
import bpy, json, math, sys
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
L = json.load(open(sys.argv[sys.argv.index('--')+1])); out = sys.argv[sys.argv.index('--')+2]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; W, H = L.get('res', [320, 400])
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.engine = 'CYCLES'; sc.cycles.samples = 4; sc.cycles.device = 'CPU'; sc.cycles.use_denoising = False
sc.view_settings.view_transform = 'Standard'
mat = bpy.data.materials.new('clay'); mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()
oi = nt.nodes.new('ShaderNodeObjectInfo'); em = nt.nodes.new('ShaderNodeEmission'); ou = nt.nodes.new('ShaderNodeOutputMaterial')
nt.links.new(oi.outputs['Color'], em.inputs['Color']); nt.links.new(em.outputs[0], ou.inputs['Surface'])
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.55, 0.62, 0.78, 1)
def obj(name, fn, col, **kw):
    bpy.ops.object.select_all(action='DESELECT'); fn(**kw); o = bpy.context.active_object; o.name = name
    o.color = (*col, 1); o.data.materials.append(mat); return o
def tube(name, pts, radii, col):
    # a chain of cylinders between successive points
    for i in range(len(pts)-1):
        a, b = Vector(pts[i]), Vector(pts[i+1]); d = b - a; r = (radii[i] + radii[i+1]) / 2
        o = obj(name, bpy.ops.mesh.primitive_cylinder_add, col, vertices=12, radius=r, depth=d.length, location=(a+b)/2)
        o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
# ground: a plain to y 3000, then a low far band
g = obj('plain', bpy.ops.mesh.primitive_plane_add, (0.42, 0.36, 0.26), size=1); g.scale = (6000, 6000, 1); g.location = (0, 2900, 0)
obj('far', bpy.ops.mesh.primitive_cube_add, (0.40, 0.42, 0.48), location=(0, 5800, 0)).scale = (8000, 5, L['far_h'])
# burnt ground toward the camera
b = obj('burnt', bpy.ops.mesh.primitive_plane_add, (0.20, 0.17, 0.12), size=1); b.scale = (9, 6, 1); b.location = (0, -3.5, 0.003)
# crater: scorched disc, raised rim of thrown earth (torus), glowing pit, flames, thrown blocks
cx, cy = L['crater']; R = L['crater_r']
s = obj('scorch', bpy.ops.mesh.primitive_cylinder_add, (0.10, 0.09, 0.08), radius=L['scorch_r'], depth=0.01, location=(cx, cy, 0.005))
rim = obj('rim', bpy.ops.mesh.primitive_torus_add, (0.33, 0.25, 0.18), major_radius=R, minor_radius=L['rim_w'], location=(cx, cy, 0)); rim.scale = (1, 1, L['rim_h'] / L['rim_w'])
obj('pit', bpy.ops.mesh.primitive_cylinder_add, (1.0, 0.45, 0.08), radius=R*0.8, depth=0.02, location=(cx, cy, 0.05))
for k, (fx, fh) in enumerate(L['flames']):
    obj('flame', bpy.ops.mesh.primitive_cone_add, (1.0, 0.62, 0.15), radius1=0.18, radius2=0.0, depth=fh, location=(cx + fx, cy - R*0.3, L['rim_h']*0.5 + fh/2))
import random; rnd = random.Random(3)
for k in range(L['blocks']):
    a = rnd.uniform(0, 2*math.pi); d = rnd.uniform(R + 0.5, L['scorch_r'] * 1.4); z = rnd.uniform(0.08, 0.3)
    o = obj('block', bpy.ops.mesh.primitive_cube_add, (0.28, 0.22, 0.17), location=(cx + d*math.cos(a), cy + d*math.sin(a), z*0.5)); o.scale = (z, z*0.8, z*0.5); o.rotation_euler = (rnd.random(), rnd.random(), rnd.random())
for (fx, fy) in L['small_fires']:
    obj('fire', bpy.ops.mesh.primitive_cone_add, (1.0, 0.55, 0.12), radius1=0.06, radius2=0, depth=0.18, location=(fx, fy, 0.09))
# column: dense black smoke from the crater, leaning with the wind (a chain of growing spheres)
c0 = Vector((cx + L.get('column_dx', 0), cy, L['rim_h'])); lean = Vector(L['column_lean']).normalized()
for k in range(28):
    t = k / 27; p = c0 + lean * (t * L['column_len']); r = L['column_r'][0] + (L['column_r'][1] - L['column_r'][0]) * t ** 0.8
    obj('column', bpy.ops.mesh.primitive_uv_sphere_add, (0.06, 0.055, 0.05), radius=r, location=p, segments=16, ring_count=8)
# trail: a thin pale tube from the crater out to a far start, kinked by the wind; radius grows with distance from the camera
cs = L['camera']; Cp = Vector(cs['position'])
E = Vector((cx + L.get('trail_dx', 0), cy, L['trail_end_z']))
Tg = Vector(cs['target']); fw = Vector(((Tg - Cp).x, (Tg - Cp).y, 0)).normalized(); rt = Vector((fw.y, -fw.x, 0)); ar = W / H
def ray(xs, ys, dep):   # the point on the camera ray through (x %, y % from the top) at this depth
    u = (xs / 100 - 0.5 + cs.get('shift_x', 0) / ar) * 36.0 / cs['lens_mm']; v = (0.5 - ys / 100 + cs.get('shift_y', 0)) * 36.0 / ar / cs['lens_mm']
    return Cp + dep * (fw + rt * u + Vector((0, 0, v)))
ctrl = [E] + [ray(*q) for q in L['trail_px_pts']]
print('LAY trail control points', [[round(c, 1) for c in q] for q in ctrl])
for it in range(L.get('smooth', 0)):   # Chaikin on the control polygon, endpoints kept: a soft bend
    q = [ctrl[0]]
    for a_, b_ in zip(ctrl[:-1], ctrl[1:]): q += [a_.lerp(b_, 0.25), a_.lerp(b_, 0.75)]
    ctrl = q + [ctrl[-1]]
pts = []
for i in range(len(ctrl) - 1):
    n = 30 if i == len(ctrl) - 2 else 3
    for k in range(n):
        t = (k / n) ** (2.0 if n == 30 else 1.0); pts.append(ctrl[i].lerp(ctrl[i+1], t))
pts.append(ctrl[-1])
radii = [L['trail_px'] * (p - Cp).length * 36.0 / cs['lens_mm'] / 2 for p in pts]
tube('trail', pts, radii, (0.95, 0.85, 0.6))
# speaker: cabinet and horn
rz = math.radians(L.get('rotate_z', 0))
cab = obj('cabinet', bpy.ops.mesh.primitive_cube_add, (0.9, 0.9, 0.95), location=(0, 0, 0.076 + 0.445)); cab.scale = (0.23, 0.19, 0.445); cab.rotation_euler = (0, 0, rz)
hn = obj('horn', bpy.ops.mesh.primitive_cube_add, (0.95, 0.95, 1.0), location=(0, 0, 1.105)); hn.scale = (0.25, 0.15, 0.19); hn.rotation_euler = (0, 0, rz)
obj('keepout', bpy.ops.mesh.primitive_plane_add, (0.30, 0.5, 0.95), size=1, location=(0, -0.19 - 0.3, 0.004)).scale = (0.9, 0.6, 1)
# camera
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 36.0; cd.lens = cs['lens_mm']; cd.clip_end = 12000
T = Vector(cs['target']); d = T - Cp; flat = Vector((d.x, d.y, 0))
cam.rotation_euler = flat.to_track_quat('-Z', 'Y').to_euler(); tilt = math.atan2(d.z, flat.length)
cd.shift_y = math.tan(tilt) * cd.lens / 36.0 * (W / H) + cs.get('shift_y', 0); cd.shift_x = cs.get('shift_x', 0); cam.location = Cp
bpy.context.view_layer.update()
def share(p):
    v = world_to_camera_view(sc, cam, Vector(p)); return (round(v.x * 100, 1), round((1 - v.y) * 100, 1))
print('LAY speaker base', share((0, -0.19, 0)), 'top', share((0, 0, 1.295)), 'horn L/R', share((-0.25, -0.15, 1.2)), share((0.25, -0.15, 1.2)))
print('LAY rim near', share((cx, cy - R - L['rim_w'], 0)), 'far top', share((cx, cy + R, L['rim_h'])), 'left', share((cx - R - L['rim_w'], cy, 0.1)), 'right', share((cx + R + L['rim_w'], cy, 0.1)))
print('LAY trail end', share(E), 'top-edge crossing', [share(p) for p in pts if 0 > share(p)[1] > -15][:1], 'at horn x', [share(p) for p in pts if abs(share(p)[0] - 55) < 3][:2])
print('LAY column top', share(c0 + lean * L['column_len']), 'horizon', share((0, 5800, 0)), 'trail width px', round(L['trail_px'] * W, 1))
print('LAY camera az', round(math.degrees(math.atan2(Cp.x - T.x, -(Cp.y - T.y))), 1), 'crater back of speaker', round(Vector((cx, cy)).length, 2), 'm')
sc.render.filepath = out; bpy.ops.render.render(write_still=True)
