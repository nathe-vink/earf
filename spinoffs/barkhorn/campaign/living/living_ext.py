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


def plain_sleeves(bpy, name, p, kit):
    """Plain card sleeves (the coordinator, 20 Nov 22:03: unprinted kraft and dark matte, no graphic): the bar's leaning
    boards (bar_life.boards: the same card, the same lean and placing keys) with one plain card on every face. Each
    entry of `boards` takes w, h, t, x, y, z, rot, `card` (hex), rough, `ease` (the edges' round, m) and `grain`
    (a card's tooth, mm a grain; optional)."""
    path = os.path.join(ROOT, 'spinoffs', 'barkhorn', 'campaign', 'bar_life', 'bar_life.py')
    spec = importlib.util.spec_from_file_location('bar_life_living', path)
    bl = importlib.util.module_from_spec(spec); spec.loader.exec_module(bl)
    objs = []
    for k, c in enumerate(p['boards']):
        one = dict(c, image=None, ground=c['card'])
        bl._print = lambda bpy_, img, ground, rough: bl._plain(bpy_, ground, rough)      # no print: the card itself
        made = bl.boards(bpy, f'{name}-{k}', {'boards': [one]}, kit)
        if c.get('grain'):                                   # card's own tooth: a fine grain in the bump, on every face
            for ob in made:
                for m in ob.data.materials:
                    if m.get('grain'):
                        continue
                    m['grain'] = 1
                    nt = m.node_tree; b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
                    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
                    nz.inputs['Scale'].default_value = 1000.0 / float(c['grain']); nz.inputs['Detail'].default_value = 6.0
                    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.25
                    bump.inputs['Distance'].default_value = 0.0003
                    nt.links.new(tc.outputs['Object'], nz.inputs['Vector']); nt.links.new(nz.outputs['Fac'], bump.inputs['Height'])
                    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
        objs += made
    print('PLAIN SLEEVES:', len(objs))
    return objs


def soft_fabric(bpy, name, p, kit):
    """Upholstery that reads as cloth (the A critics, round 2: the sofa read as smooth rubber or clay, its outline
    faceted). For every mesh whose name starts with one of `prefixes`: a subdivision surface (`levels`, render and
    viewport), so the outline curves; on its materials, a sheen (the nap's soft rim light, `sheen` weight and
    `sheen_rough`, tinted grey by `sheen_tint`) and a fine nap in the bump (a noise grain, `weave_mm` a grain,
    `weave_depth` its strength), added over the scan's own normal map. Prints what it changed."""
    pref = tuple(p.get('prefixes', ['sofa_02']))
    lv = int(p.get('levels', 2))
    done_m, done_o = set(), []
    for o in list(bpy.data.objects):
        if o.type != 'MESH' or not o.name.startswith(pref):
            continue
        for poly in o.data.polygons:
            poly.use_smooth = True
        md = o.modifiers.new('soft', 'SUBSURF'); md.levels = lv; md.render_levels = lv; md.uv_smooth = 'PRESERVE_BOUNDARIES'
        done_o.append(o.name)
        for sl in o.material_slots:
            m = sl.material
            if not m or m.name in done_m or not m.use_nodes:
                continue
            done_m.add(m.name)
            nt = m.node_tree
            b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
            b.inputs['Sheen Weight'].default_value = float(p.get('sheen', 0.6))
            b.inputs['Sheen Roughness'].default_value = float(p.get('sheen_rough', 0.45))
            b.inputs['Sheen Tint'].default_value = (*([float(p.get('sheen_tint', 0.45))] * 3), 1.0)
            tc = nt.nodes.new('ShaderNodeTexCoord')
            nz = nt.nodes.new('ShaderNodeTexNoise')               # the nap: a fine, even grain with no direction
            nz.inputs['Scale'].default_value = 1000.0 / float(p.get('weave_mm', 1.2))
            nz.inputs['Detail'].default_value = 4.0; nz.inputs['Roughness'].default_value = 0.6
            nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
            mx = nz
            bump = nt.nodes.new('ShaderNodeBump')
            bump.inputs['Strength'].default_value = float(p.get('weave_depth', 0.35)); bump.inputs['Distance'].default_value = 0.0005
            nt.links.new(mx.outputs['Fac'], bump.inputs['Height'])
            nl = b.inputs['Normal'].links
            if nl:
                nt.links.new(nl[0].from_socket, bump.inputs['Normal'])
            nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    print('SOFT FABRIC:', done_o, sorted(done_m), 'levels', lv)
    return []
