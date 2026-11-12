"""Every scattered tuft in a saved scene checked against the ground (the coordinator, 2026-11-11: Fog's tufts floated):
none floating (base more than 2 cm above the ground under it), none buried past 5 cm, none within 18 cm of a fall of
4 cm or more (a brow, the patch's edge), none whose blades' footprint (0.75 of its half-width) reaches over a fall of
more than 4 cm or 15 % of that radius (2026-11-12: Fog's lip row hung its blades over the fog), none with its base in frame but hidden behind the ground, none with no ground
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
    if any(m.type == 'PARTICLE_SYSTEM' for m in o.modifiers):
        continue                                                      # a hair emitter is grass, not the ground
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
bad = {'no ground': 0, 'floating': 0, 'buried': 0, 'over an edge': 0, 'overhang': 0, 'base hidden': 0}; inframe = 0


def footprint(o):
    pts = [q.matrix_world @ Vector(c) for q in [o, *o.children_recursive] if q.type == 'MESH' for c in q.bound_box]
    return 0.75 * 0.5 * max(max(p.x for p in pts) - min(p.x for p in pts), max(p.y for p in pts) - min(p.y for p in pts)) if pts else 0.0


RING = ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7))
for o in tufts:
    x, y = o.location.x, o.location.y; z = down(x, y)
    if z is None:
        bad['no ground'] += 1; continue
    gap = o.location.z - z
    bad['floating'] += gap > 0.02; bad['buried'] += gap < -0.05
    if any(r is None or r < z - 0.04 for r in (down(x + dx * 0.18, y + dy * 0.18) for dx, dy in
           ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)))):
        bad['over an edge'] += 1
    else:
        r_ = footprint(o)                                             # the blades over a brow (Fog's lip, 2026-11-12)
        if r_ > 0.18 and any(r is None or r < z - max(0.04, 0.15 * r_) for r in (down(x + dx * r_, y + dy * r_) for dx, dy in RING)):
            bad['overhang'] += 1
    b = Vector((x, y, z)); c = ou.world_to_camera_view(sc, cam, b)
    if 0 <= c.x <= 1 and 0 <= c.y <= 1 and c.z > 0:
        inframe += 1
        d = b - cp; L = d.length; d.normalize()
        if any(h[0] is not None and h[3] < L - 0.03 for h in (g.ray_cast(cp, d, L) for g in G)):
            bad['base hidden'] += 1
# hair grass (Haze): the emitter's vertices against the ground under them, and the share whose root is in frame
# but hidden behind the ground
hair = []
for o in sc.objects:
    if o.type == 'MESH' and not o.hide_render and any(m.type == 'PARTICLE_SYSTEM' for m in o.modifiers):
        mw = o.matrix_world; vs = [mw @ v.co for v in o.data.vertices][::max(1, len(o.data.vertices) // 4000)]
        fl = hid = fr = 0
        for v in vs:
            z = down(v.x, v.y)
            if z is None or v.z - z > 0.02:
                fl += 1; continue
            v = Vector((v.x, v.y, z + 0.02))                          # the root's ground, 2 cm up (grazing rays)
            c = ou.world_to_camera_view(sc, cam, v)
            if 0 <= c.x <= 1 and 0 <= c.y <= 1 and c.z > 0:
                fr += 1; d = v - cp; L = d.length; d.normalize()
                hid += any(h[0] is not None and h[3] < L - 0.05 for h in (g.ray_cast(cp, d, L) for g in G))
        hair.append(f'{o.name}: {len(vs)} roots sampled, {fl} off the ground, {fr} in frame of which {hid} hidden')
        bad['hair off ground'] = bad.get('hair off ground', 0) + fl
        bad['hair root hidden'] = bad.get('hair root hidden', 0) + hid
# small props (stones, plants, mushrooms, litter): a kit piece's parts grouped (prop53-kit-leaves, -berries ... are
# one plant); floating if its lowest point is more than 2 cm above the HIGHEST ground under its footprint (a rock on a
# slope or a brow touches where the ground is highest)
import re
groups = {}
for o in sc.objects:
    if o.parent is not None or o.hide_render or o.name.startswith('grass_') or o.type not in ('MESH', 'EMPTY'):
        continue
    if o.name.startswith(('Tropos', 'foot', 'black-flag', 'reflector', 'camera')):
        continue
    obs = [q for q in [o, *o.children_recursive] if q.type == 'MESH' and not q.hide_render]
    if obs:
        groups.setdefault(re.sub(r'^(prop\d+-kit)-.*$', r'\1', o.name), []).extend(obs)
props = []
for k, obs in groups.items():
    pts = [q.matrix_world @ Vector(c) for q in obs for c in q.bound_box]
    x0, x1 = min(p.x for p in pts), max(p.x for p in pts); y0, y1 = min(p.y for p in pts), max(p.y for p in pts)
    if x1 - x0 > 3.0 or y1 - y0 > 3.0:
        continue
    zs = [down(x0 + (x1 - x0) * i / 4, y0 + (y1 - y0) * j / 4) for i in range(5) for j in range(5)]
    zs = [z for z in zs if z is not None]
    if not zs:
        continue
    gap = min(p.z for p in pts) - max(zs)
    if gap > 0.02 and abs(max(zs)) < 50:
        props.append(f'{k} {gap:+.3f} m at {(Vector(((x0 + x1) / 2, (y0 + y1) / 2, max(zs))) - cp).length:.0f} m')
bad['props floating'] = len(props)
n = sum(bad.values())
print(f'SCATTER {label}: {len(tufts)} tufts ({inframe} based in frame) on {len(G)} ground mesh(es): '
      + ('CLEAN' if n == 0 else ', '.join(f'{k} {v}' for k, v in bad.items() if v)))
for h in hair:
    print('  hair', h)
if props:
    print('  floating props', props[:20])
