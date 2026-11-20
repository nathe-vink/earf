"""Set pieces the living room builds itself (kit 'ext'), called as fn(bpy, name, p, kit).

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/campaign/living/living_ext.py", "fn": "cores_off", ...}

cores_off: the Cores placed by the lamps lane's code (stage2_props.lamps, the same keys), then switched off: every
lamp the lane's code added for them is removed and every glowing face among their materials set to no light. The ball,
its opal inside, the base: as built, unlit. Prints what it removed, so the emitter list can say so.
"""
import importlib.util, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))


def _stage2():
    path = os.path.join(ROOT, 'spinoffs', 'barkhorn', 'campaign', 'stage', 'stage2_props.py')
    spec = importlib.util.spec_from_file_location('stage2_props_living', path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def cores_off(bpy, name, p, kit):
    before = set(bpy.context.scene.objects)
    objs = _stage2().lamps(bpy, name, p, kit)
    new = [o for o in bpy.context.scene.objects if o not in before]
    lamps = [o for o in new if o.type == 'LIGHT']
    meshes = [o for o in new if o.type == 'MESH']
    n_lamps = len(lamps)
    for o in lamps:
        bpy.data.objects.remove(o, do_unlink=True)
    dark = 0
    seen = set()
    for o in meshes:
        for sl in o.material_slots:
            m = sl.material
            if not m or m.name in seen or not m.use_nodes:
                continue
            seen.add(m.name)
            for n in m.node_tree.nodes:
                if n.type == 'EMISSION' and n.inputs['Strength'].default_value > 0:
                    n.inputs['Strength'].default_value = 0.0; dark += 1
                elif n.type == 'BSDF_PRINCIPLED' and n.inputs['Emission Strength'].default_value > 0:
                    n.inputs['Emission Strength'].default_value = 0.0; dark += 1
    print('CORES OFF:', n_lamps, 'lamps removed,', dark, 'glowing faces set dark')
    return objs                                  # (lamps_final.place returns no lamps: nothing removed is in it)


def no_portal(bpy, name, p, kit):
    """Take out the sky portal of each window named in `windows` (e.g. ["wall-back"]): a portal only steers the sky's
    light through an opening and adds none, but it is a lamp object, and a window in frame must hold no lamp."""
    gone = []
    for w in p.get('windows', []):
        o = bpy.data.objects.get(f'{w}-portal')
        if o is not None:
            bpy.data.objects.remove(o, do_unlink=True); gone.append(w)
    print('NO PORTAL in', gone)
    return []


def no_glass_shadows(bpy, name, p, kit):
    """One light model for the frame (the coordinator, 20 Nov 19:45): with refractive caustics on, the acrylics' glass-
    shadow shortcut (a Light Path 'Is Shadow Ray' switching the surface to a transparent BSDF, so direct light crosses the
    face unbent) would count the light through the acrylic twice: once on that straight shadow ray, once on the refracted
    caustic path. Every material that carries the shortcut (the Tropos acrylic, the Mantle asset's, the Core's) has its
    switch cut and set to the surface's own BSDF, so light crosses the acrylic only by refracting. Placed last in the set,
    when the products and the lamps are built. Prints what it changed."""
    cut = []
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        nt = m.node_tree
        for n in list(nt.nodes):
            if n.type != 'LIGHT_PATH':
                continue
            for lk in list(n.outputs['Is Shadow Ray'].links):
                mx = lk.to_node
                if mx.type != 'MIX_SHADER' or lk.to_socket != mx.inputs['Fac']:
                    continue
                transparent_on_b = any(l2.from_node.type == 'BSDF_TRANSPARENT' for l2 in mx.inputs[2].links)
                transparent_on_a = any(l2.from_node.type == 'BSDF_TRANSPARENT' for l2 in mx.inputs[1].links)
                if not (transparent_on_a or transparent_on_b):
                    continue
                nt.links.remove(lk)
                mx.inputs['Fac'].default_value = 0.0 if transparent_on_b else 1.0     # keep the other input, the surface
                cut.append(m.name)
    print('NO GLASS SHADOWS:', len(cut), 'materials:', sorted(set(cut))[:40])
    return []
