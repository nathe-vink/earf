"""python3.11 studio/engine/check_alpha.py  ->  ok: grass_bermuda_01's cards cut out. Its Poly Haven glTF has no alpha;
assets._alpha_maps wires the published Alpha map (without it the cards render whole, their glossy surround as white flecks)."""
import os, sys
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import assets
bpy.ops.wm.read_factory_settings(use_empty=True); assets.place(bpy, 'grass_bermuda_01', '1k')
assert all(n.inputs['Alpha'].is_linked for m in bpy.data.materials if m.name.startswith('grass_bermuda_01') and m.node_tree for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), 'grass_bermuda_01: alpha not wired'
print('ok: grass_bermuda_01 cards cut out')
