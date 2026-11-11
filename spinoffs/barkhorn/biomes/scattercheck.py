"""Every scattered tuft in a saved scene checked against the ground (the coordinator, 2026-11-11: Fog's tufts floated):
none floating (base more than 2 cm above the ground under it), none buried past 5 cm, none within 18 cm of a fall of
4 cm or more (a brow, the patch's edge), none with its base in frame but hidden behind the ground, none with no ground
under it. The ground is every big surface mesh (at least 10k faces and 5 m across), as land_scatter in habitat.py.

usage: python3.11 scattercheck.py SCENE.blend [label]   (prints one line; CLEAN or the counts)
"""
import sys

import bpy
import bpy_extras.object_utils as ou
from mathutils import Vector
from mathutils.bvhtree import BVHTree

bpy.ops.wm.open_mainfile(filepath=sys.argv[1])
label = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get()
tufts = [o for o in sc.objects if o.parent is None and not o.hide_render and o.name.startswith('grass_')]
G = []
for o in sc.objects:
    if o.type != 'MESH' or o.parent is not None or o.hide_render or o.name.startswith('grass_') or len(o.data.polygons) < 10000:
        continue
    ms = [s.material for s in o.material_slots if s.material and s.material.node_tree]
    if not any(n.type == 'OUTPUT_MATERIAL' and n.inputs['Surface'].is_linked for m in ms for n in m.node_tree.nodes):
        continue
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    if max(v.x for v in bb) - min(v.x for v in bb) < 5.0:
        continue
    e = o.evaluated_get(dg); m = e.to_mesh(); mw = o.matrix_world
    G.append(BVHTree.FromPolygons([mw @ v.co for v in m.vertices], [q.vertices[:] for q in m.polygons])); e.to_mesh_clear()


def down(x, y):
    zs = [h[0].z for h in (g.ray_cast(Vector((x, y, 100.0)), Vector((0, 0, -1))) for g in G) if h[0] is not None]
    return max(zs) if zs else None


cam = sc.camera; cp = cam.matrix_world.translation
bad = {'no ground': 0, 'floating': 0, 'buried': 0, 'over an edge': 0, 'base hidden': 0}; inframe = 0
for o in tufts:
    x, y = o.location.x, o.location.y; z = down(x, y)
    if z is None:
        bad['no ground'] += 1; continue
    gap = o.location.z - z
    bad['floating'] += gap > 0.02; bad['buried'] += gap < -0.05
    if any(r is None or r < z - 0.04 for r in (down(x + dx * 0.18, y + dy * 0.18) for dx, dy in
           ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)))):
        bad['over an edge'] += 1
    b = Vector((x, y, z)); c = ou.world_to_camera_view(sc, cam, b)
    if 0 <= c.x <= 1 and 0 <= c.y <= 1 and c.z > 0:
        inframe += 1
        d = b - cp; L = d.length; d.normalize()
        if any(h[0] is not None and h[3] < L - 0.03 for h in (g.ray_cast(cp, d, L) for g in G)):
            bad['base hidden'] += 1
n = sum(bad.values())
print(f'SCATTER {label}: {len(tufts)} tufts ({inframe} based in frame) on {len(G)} ground mesh(es): '
      + ('CLEAN' if n == 0 else ', '.join(f'{k} {v}' for k, v in bad.items() if v)))
