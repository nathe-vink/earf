"""Every light in a saved scene: lamps (type, size, energy, colour, rays they're seen by, render-hidden or not), the world
(its image and strength), and every mesh whose material emits (an emission shader with strength > 0 linked to an output,
or a Principled with emission). The habitat rule (the coordinator, 2026-11-09 23:42): the sun and the sky only.

usage: python3.11 lightlist.py SCENE.blend [label]
"""
import sys

import bpy

bpy.ops.wm.open_mainfile(filepath=sys.argv[1])
label = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
sc = bpy.context.scene
print(f'== {label}')
w = sc.world
if w and w.node_tree:
    imgs = [n.image.name for n in w.node_tree.nodes if n.type == 'TEX_ENVIRONMENT' and n.image]
    bg = [round(n.inputs['Strength'].default_value, 3) for n in w.node_tree.nodes if n.type == 'BACKGROUND']
    print(f'  world {w.name}: sky image {imgs}, background strength {bg}')
n_lamps = 0
for o in sc.objects:
    if o.type != 'LIGHT':
        continue
    L = o.data; n_lamps += 1
    size = '' if L.type in ('SUN', 'POINT', 'SPOT') else f' {L.size:.2f} x {getattr(L, "size_y", L.size):.2f} m'
    vis = ','.join(a.replace('visible_', '') for a in ('visible_camera', 'visible_diffuse', 'visible_glossy', 'visible_transmission')
                   if getattr(o, a, True))
    print(f'  lamp {o.name}: {L.type}{size}, energy {L.energy:.2f}, colour {tuple(round(c, 3) for c in L.color)}, '
          f'render {"OFF" if o.hide_render else "on"}, seen by {vis}')
em = []
for o in sc.objects:
    if o.type != 'MESH' or o.hide_render:
        continue
    for s in o.material_slots:
        m = s.material
        if not (m and m.node_tree):
            continue
        for n in m.node_tree.nodes:
            if n.type == 'EMISSION' and n.inputs['Strength'].default_value > 0 and n.outputs[0].is_linked \
                    and max(n.inputs['Color'].default_value[:3]) > 0:
                em.append((o.name, m.name)); break
            if n.type == 'BSDF_PRINCIPLED' and n.inputs['Emission Strength'].default_value > 0 \
                    and max(n.inputs['Emission Color'].default_value[:3]) > 0:
                em.append((o.name, m.name)); break
print(f'  lamps: {n_lamps}; emitting meshes (outside the speaker): {em if em else "none"}')
