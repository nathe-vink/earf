"""The skyline test (the coordinator, 2026-11-12, before the Fog finals): for every tuft whose root the camera sees, a
ray from the camera aimed 3 cm below the root must hit ground, not fog or sky. Grass blades and the speaker on the way
are passed through, and so are volume-only boxes (fog, haze: a ray goes into them, not off them); the first other surface must be one of the ground meshes (the big surface meshes, as in
scattercheck.py). Also: the ray through the image a few pixels under the root's projection, the same rule.

usage: python3.11 rootray.py SCENE.blend LABEL W H [lens shift_x shift_y]   (camera overrides; W H the frame)
prints ROOTRAY LABEL: n tested, k fail, and one line per failure (name, world xyz, pixel, what the ray hit).
"""
import sys

import bpy
import bpy_extras.object_utils as ou
from mathutils import Vector

bpy.ops.wm.open_mainfile(filepath=sys.argv[1])
label, W, H = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
sc = bpy.context.scene; cam = sc.camera
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
if len(sys.argv) > 7:
    cam.data.lens, cam.data.shift_x, cam.data.shift_y = map(float, sys.argv[5:8])
bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
cp = cam.matrix_world.translation


def is_ground(o):
    if o.type != 'MESH' or o.name.startswith('grass_') or len(o.data.polygons) < 10000:
        return False
    if any(m.type == 'PARTICLE_SYSTEM' for m in o.modifiers):
        return False
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return max(v.x for v in bb) - min(v.x for v in bb) >= 5.0


def top(o):
    while o.parent is not None:
        o = o.parent
    return o


def volume_only(o):
    """a fog or haze box: its material has a volume and no surface, so a camera ray goes in, not off it"""
    ms = [s.material for s in o.material_slots if s.material and s.material.node_tree]
    outs = [n for m in ms for n in m.node_tree.nodes if n.type == 'OUTPUT_MATERIAL']
    return bool(outs) and all(not n.inputs['Surface'].is_linked and n.inputs['Volume'].is_linked for n in outs)


VOL = {}


def passthrough(o):
    t = top(o).name
    if t.startswith(('grass_', 'Tropos', 'foot')) or o.name.startswith('grass_'):
        return True
    if o.name not in VOL:
        VOL[o.name] = volume_only(o)
    return VOL[o.name]


def first(org, d, L):
    """the first surface that is not grass or the speaker, along d, within L + 0.5 m"""
    o0 = org
    for _ in range(40):
        h, loc, n, i, ob, m = sc.ray_cast(dg, org, d, distance=L + 0.5 - (org - o0).length)
        if not h:
            return 'SKY', None
        if ob.instance_type == 'NONE' and passthrough(ob) or ob.name.startswith('grass_'):
            org = loc + d * 0.002; continue
        return ob.name, (loc - o0).length
    return 'grass x40', None


from mathutils.bvhtree import BVHTree
G = []
for o in sc.objects:
    if not o.hide_render and is_ground(o):
        e = o.evaluated_get(dg); m = e.to_mesh(); mw = o.matrix_world
        G.append(BVHTree.FromPolygons([mw @ v.co for v in m.vertices], [q.vertices[:] for q in m.polygons])); e.to_mesh_clear()


def down(x, y):
    zs = [h[0].z for h in (g.ray_cast(Vector((x, y, 100.0)), Vector((0, 0, -1))) for g in G) if h[0] is not None]
    return max(zs) if zs else None


tufts = [o for o in sc.objects if o.parent is None and not o.hide_render and o.name.startswith('grass_')]
fr = [cam.matrix_world @ v for v in cam.data.view_frame(scene=sc)]                    # tr, br, bl, tl
tested = 0; fails = []
for o in tufts:
    zg = down(o.location.x, o.location.y)
    if zg is None:
        fails.append(f'  {o.name}: no ground under it'); continue
    r = Vector((o.location.x, o.location.y, zg + 0.005))         # the root where it meets the ground (tufts are bedded 1 cm)
    c = ou.world_to_camera_view(sc, cam, r)
    if not (0 <= c.x <= 1 and 0 <= c.y <= 1 and c.z > 0):
        continue
    d = r - cp; L = d.length
    nm, dist = first(cp, d.normalized(), L)
    if nm != 'SKY' and dist is not None and dist < L - 0.03:
        continue                                                      # the root is hidden: not a seen root
    tested += 1
    px, py = c.x * W, (1 - c.y) * H
    why = []
    t = Vector((r.x, r.y, zg - 0.03)); d = (t - cp); L = d.length
    nm, dist = first(cp, d.normalized(), L)
    if nm == 'SKY' or not is_ground(bpy.data.objects[nm]):
        why.append(f'3cm-below hit {nm}')
    u, v = c.x, 1 - c.y + 4.0 / H                                     # 4 px under the root in the image
    p = fr[3].lerp(fr[0], u).lerp(fr[2].lerp(fr[1], u), v); d = (p - cp).normalized()
    nm2, _ = first(cp, d, 5000.0)
    if nm2 == 'SKY' or not is_ground(bpy.data.objects[nm2]):
        why.append(f'4px-below hit {nm2}')
    if why:
        fails.append(f'  {o.name} at ({r.x:.2f}, {r.y:.2f}, {r.z:.3f}) px ({px:.0f}, {py:.0f}): ' + '; '.join(why))
print(f'ROOTRAY {label}: {len(tufts)} tufts, {tested} with a seen root, {len(fails)} fail')
for f in fails:
    print(f)
