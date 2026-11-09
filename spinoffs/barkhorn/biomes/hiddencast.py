"""What is hidden from the camera but stands in the frame, in a saved scene (the scene as rendered: final framing).

usage: python3.11 hiddencast.py scene.blend [label]

Lists every light, and every mesh whose camera visibility is off or which emits light, with its share of the frame:
a grid of camera rays (120 x 150) through the render frame; a mesh counts where it is the first surface a ray meets
(the scene's own ray cast, which sees meshes whatever their camera visibility), a lamp where its shape (an area
lamp's rectangle or disk, a point or spot lamp's sphere) is crossed before the first surface. A sun has no place.
The rule (the coordinator, 2026-11-09): nothing hidden from the camera in frame, except a practical's bulb in its fitting.
"""
import math
import sys

import bpy
from mathutils import Vector

bpy.ops.wm.open_mainfile(filepath=sys.argv[1])
label = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
sc = bpy.context.scene
cam = sc.camera
dg = bpy.context.evaluated_depsgraph_get()
NX, NY = 120, 150
tr, br, bl, tl = [cam.matrix_world @ v for v in cam.data.view_frame(scene=sc)]
C = cam.matrix_world.translation.copy()


def emits(o):
    for s in getattr(o, 'material_slots', []):
        m = s.material
        if not (m and m.node_tree):
            continue
        for n in m.node_tree.nodes:
            if n.type == 'EMISSION' and n.inputs['Strength'].default_value > 0 and any(l for l in n.outputs[0].links):
                return True
            if n.type == 'BSDF_PRINCIPLED' and n.inputs['Emission Strength'].default_value > 0 \
                    and max(n.inputs['Emission Color'].default_value[:3]) > 0:
                return True
    return False


meshes = {o.name: o for o in sc.objects if o.type == 'MESH' and not o.hide_render
          and (not o.visible_camera or emits(o))}
lights = [o for o in sc.objects if o.type == 'LIGHT' and not o.hide_render]
mesh_hits = {k: 0 for k in meshes}
light_hits = {o.name: 0 for o in lights}


def light_hit(o, C, ray, dmax):
    L = o.data
    if L.type == 'SUN':
        return False
    p = o.matrix_world.translation
    if L.type in ('POINT', 'SPOT'):
        r = max(L.shadow_soft_size, 1e-3)
        oc = C - p; b = oc.dot(ray); c = oc.dot(oc) - r * r; disc = b * b - c
        if disc < 0:
            return False
        t = -b - math.sqrt(disc)
        return 0 < t < dmax
    R = o.matrix_world.to_3x3().normalized()
    n = R @ Vector((0, 0, 1)); ux = R @ Vector((1, 0, 0)); uy = R @ Vector((0, 1, 0))
    den = ray.dot(n)
    if abs(den) < 1e-9:
        return False
    t = (p - C).dot(n) / den
    if not (0 < t < dmax):
        return False
    x = C + ray * t - p
    sx = L.size * o.matrix_world.to_scale().x
    sy = (L.size_y if L.shape in ('RECTANGLE', 'ELLIPSE') else L.size) * o.matrix_world.to_scale().y
    if L.shape in ('DISK', 'ELLIPSE'):
        return (x.dot(ux) / (sx / 2)) ** 2 + (x.dot(uy) / (sy / 2)) ** 2 <= 1
    return abs(x.dot(ux)) <= sx / 2 and abs(x.dot(uy)) <= sy / 2


for i in range(NX):
    for j in range(NY):
        u, v = (i + 0.5) / NX, (j + 0.5) / NY
        ray = ((tl + (tr - tl) * u + (bl - tl) * v) - C).normalized()
        ok, loc, nrm, idx, ob, _m = sc.ray_cast(dg, C, ray)
        dmax = (loc - C).length if ok else 1e9
        if ok and ob.name in mesh_hits:
            mesh_hits[ob.name] += 1
        for o in lights:
            if light_hit(o, C, ray, dmax):
                light_hits[o.name] += 1

N = NX * NY
print(f'== {label}: camera {cam.name}, frame {sc.render.resolution_x} x {sc.render.resolution_y}')
for o in lights:
    L = o.data
    vis = getattr(o, 'visible_camera', True)
    print(f'  light {o.name:24s} {L.type:5s} camera={vis!s:5s} energy {L.energy:8.2f}  in frame {100 * light_hits[o.name] / N:5.1f}%')
for k, o in meshes.items():
    print(f'  mesh  {k:24s} camera={o.visible_camera!s:5s} emits={emits(o)!s:5s}  in frame {100 * mesh_hits[k] / N:5.1f}%')
bad = [o.name for o in lights if light_hits[o.name] and not getattr(o, 'visible_camera', True)] + \
      [k for k, o in meshes.items() if mesh_hits[k] and not o.visible_camera]
print('  RESULT:', 'PASS (nothing hidden from the camera in frame)' if not bad else f'FAIL: {bad}')
