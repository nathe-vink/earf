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


def lamps_pin(p):
    """The lamps lane's commit the shot asks for (`lamps_commit`, a sha or its prefix), checked against LAMPS_ROOT's HEAD
    (the audit, 21 Nov: LAMPS_ROOT was neither pinned nor recorded). Returns (root, sha); exits on a mismatch."""
    import subprocess
    root = os.environ.get('LAMPS_ROOT') or p.get('lamps_root')
    sha = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True).stdout.strip() if root else ''
    want = p.get('lamps_commit')
    if want and not sha.startswith(want):
        raise SystemExit(f'cores_off: LAMPS_ROOT {root} is at {sha[:10]}, the shot asks for {want}')
    env = {k: os.environ[k] for k in ('BASE_CONTACT', 'BASE_FIX', 'BASE_LIFT', 'REV_SEG', 'CORE_LOAD') if k in os.environ}
    print('LAMPS PIN:', root, sha, 'asked', want or '(none)', 'env', env)
    return root, sha


def cores_off(bpy, name, p, kit):
    root, sha = lamps_pin(p)
    bpy.context.scene['lamps_commit'] = sha                  # kept in the scene, and in the report by the room's script
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


def water_glass(bpy, name, p, kit):
    """A turned glass of water as light meets it (the coordinator's audit, 21 Nov: the water a hair inside the wall left an
    air film that reflected totally inside the wall, the silvery funnel; and the water was glass at 1.5). Three surfaces
    of revolution, each one interface with the ratio of its two sides:
      glass | air    the outside, the base, the rim and the inside wall above the water        IOR 1.5
      glass | water  the inside wall below the water line and the inside floor (no air between) IOR 1.5 / 1.33
      water | air    the water's top, with a meniscus climbing `meniscus` m up the wall       IOR 1.33
    `profile` is the glass's outer (r, z) profile (listening_bar's ROCKS form), `wall` its thickness, `base` the floor's,
    `fill` the water's height at the middle; `position` the foot's centre. Each surface's normal points from the denser
    side to the other, so Cycles takes its IOR as the ratio inside / outside."""
    import bmesh, math
    from mathutils import Vector
    prof = [tuple(q) for q in p['profile'] if not (q[0] == 0 and q[1] > 0)]
    t, base, fill = float(p.get('wall', 0.0035)), float(p.get('base', 0.016)), float(p['fill'])
    men = float(p.get('meniscus', 0.0015)); seg = int(p.get('segments', 128))
    top = prof[-1][1]
    def r_out(z):
        for (r0, z0), (r1, z1) in zip(prof, prof[1:]):
            if z0 <= z <= z1 and z1 > z0:
                return r0 + (r1 - r0) * (z - z0) / (z1 - z0)
        return prof[-1][0]
    r_in = lambda z: r_out(z) - t
    zw = fill + men                                         # where the water meets the wall
    # profiles, walked bottom-up / outward
    outer = [(0.0, 0.0)] + [q for q in prof if q[0] > 0] + [(r_in(top), top)]
    inner_dry = [(r_in(z), z) for z in (top, zw)]                       # down the inside wall to the water line
    wet = [(r_in(zw), zw)] + [(r_in(z), z) for z in sorted({z for _, z in prof if base < z < zw}, reverse=True)] + \
          [(r_in(base), base), (0.0, base)]
    rw = r_in(zw); n_m = 8
    # the water's top: flat to 4 meniscus-heights from the wall, then a quarter-cosine up to the wall
    surf = [(0.0, fill)] + [((rw - 4 * men) + 4 * men * k / n_m, fill + men * (1 - math.cos(0.5 * math.pi * k / n_m)))
                            for k in range(n_m + 1)]
    def mat(nm, ior, col):
        m = bpy.data.materials.new(nm); m.use_nodes = True
        b = m.node_tree.nodes['Principled BSDF']
        b.inputs['Base Color'].default_value = (*col, 1.0); b.inputs['Roughness'].default_value = 0.0
        b.inputs['Transmission Weight'].default_value = 1.0; b.inputs['IOR'].default_value = ior
        return m
    # (the bar test B1, 21 Nov: any liquid: `ior` (default water's 1.33), `color` its tint at its two interfaces, as the
    # kit's resin carried it; left out, the water glass as before)
    ior = float(p.get('ior', 1.33))
    def lin(h):
        h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)
    tint = lin(p['color']) if p.get('color') else None
    g_air = mat(f'{name}-glass-air', 1.5, (0.97, 0.97, 0.96))
    g_wat = mat(f'{name}-glass-water', 1.5 / ior, tint or (1.0, 1.0, 1.0))
    w_air = mat(f'{name}-water-air', ior, tint or (0.96, 0.985, 0.985))
    def revolve(nm, pr, m, out_dir):
        bm = bmesh.new()
        rings = []
        for r, z in pr:
            if r < 1e-6:
                rings.append([bm.verts.new((0.0, 0.0, z))])
            else:
                rings.append([bm.verts.new((r * math.cos(2 * math.pi * k / seg), r * math.sin(2 * math.pi * k / seg), z)) for k in range(seg)])
        for a, b_ in zip(rings, rings[1:]):
            for k in range(seg):
                k1 = (k + 1) % seg
                if len(a) == 1:
                    bm.faces.new((a[0], b_[k], b_[k1]))
                elif len(b_) == 1:
                    bm.faces.new((a[k], b_[0], a[k1]))
                else:
                    bm.faces.new((a[k], b_[k], b_[k1], a[k1]))
        bm.normal_update()
        f0 = max(bm.faces, key=lambda f: f.calc_area())                 # orient the strip by one face's test
        c = f0.calc_center_median()
        if f0.normal.dot(out_dir(c)) < 0:
            for f in bm.faces:
                f.normal_flip()
        me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
        for poly in me.polygons:
            poly.use_smooth = True
        me.materials.append(m)
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
        ob.location = Vector(p['position'])
        return ob
    radial = lambda c: Vector((c.x, c.y, 0.0)).normalized()
    objs = [revolve(f'{name}-glass-outer', outer, g_air, lambda c: radial(c) if c.z > 0.002 else Vector((0, 0, -1))),
            revolve(f'{name}-glass-inner-dry', inner_dry, g_air, lambda c: -radial(c)),           # into the empty glass
            revolve(f'{name}-glass-wet', wet, g_wat, lambda c: -radial(c) if c.z > base + 1e-4 else Vector((0, 0, 1))),
            revolve(f'{name}-water-top', surf, w_air, lambda c: Vector((0, 0, 1)))]
    if p.get('top') is False:                               # (a diagnostic: the water's top surface left out)
        bpy.data.objects.remove(objs.pop(), do_unlink=True)
    # ice (B1): each cube {size, position (world), rotate (deg XYZ), ease} split at the liquid's top: above it ice | air
    # at `ice_ior` (1.31), below it ice | liquid at 1.31 / ior; the liquid's top cut away inside each cube, so no ray
    # meets a liquid surface inside the ice (no overlapping volumes)
    cubes = []
    for j, c in enumerate(p.get('ice') or []):
        from mathutils import Matrix, Euler
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector(c['size']), verts=bm.verts)
        if c.get('ease'):
            bmesh.ops.bevel(bm, geom=list(bm.edges), offset=float(c['ease']), segments=3, affect='EDGES', profile=0.5)
        R = Euler([math.radians(a) for a in c.get('rotate', [0, 0, 0])], 'XYZ').to_matrix().to_4x4()
        bm.transform(Matrix.Translation(Vector(c['position']) - Vector(p['position'])) @ R)
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, fill), plane_no=(0, 0, 1))
        bm.normal_update()
        ia = mat(f'{name}-ice{j}-air', float(p.get('ice_ior', 1.31)), (0.97, 0.985, 0.99))
        il = mat(f'{name}-ice{j}-liquid', float(p.get('ice_ior', 1.31)) / ior, (1.0, 1.0, 1.0))
        for m_ in (ia, il):
            m_.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = float(p.get('ice_roughness', 0.12))
        for f in bm.faces:
            f.material_index = 0 if f.calc_center_median().z > fill else 1
        me = bpy.data.meshes.new(f'{name}-ice{j}'); bm.to_mesh(me); bm.free()
        me.materials.append(ia); me.materials.append(il)
        ob = bpy.data.objects.new(f'{name}-ice{j}', me); bpy.context.scene.collection.objects.link(ob)
        ob.location = Vector(p['position'])
        cubes.append(ob)
    if cubes and p.get('top') is not False:
        topo = objs[-1]
        for ob in cubes:
            md = topo.modifiers.new('ice-cut', 'BOOLEAN'); md.operation = 'DIFFERENCE'; md.solver = 'EXACT'
            md.use_hole_tolerant = True; md.object = ob
        dg = bpy.context.evaluated_depsgraph_get()
        me = bpy.data.meshes.new_from_object(topo.evaluated_get(dg))
        topo.modifiers.clear(); old = topo.data; topo.data = me; bpy.data.meshes.remove(old)
        print('WATER GLASS ice: top faces', len(me.polygons), 'area', round(sum(q.area for q in me.polygons) * 1e4, 2), 'cm2')
    objs += cubes
    print('WATER GLASS:', [o.name for o in objs], 'ior', ior, 'fill', fill, 'meniscus', men, 'wet to', round(zw, 4))
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


def shadow_ray_report(bpy, name, p, kit):
    """A diagnostic (B1, 21 Nov): every material with a Light Path 'Is Shadow Ray' output still linked, and where it goes.
    Place it after no_glass_shadows to list what the cut left. Changes nothing."""
    found = []
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        for n in m.node_tree.nodes:
            if n.type == 'LIGHT_PATH' and n.outputs['Is Shadow Ray'].links:
                found.append((m.name, [f'{l.to_node.type}.{l.to_socket.name}' for l in n.outputs['Is Shadow Ray'].links]))
    print('SHADOW RAY LINKS LEFT:', len(found), found[:60])
    return []


def softbox(bpy, name, p, kit):
    """A real softbox (B1, 21 Nov): a diffuser face `size` [w, h] m glowing at `strength` (scene-linear radiance, the
    engine panel's unit) and `color`, in a black box `depth` m deep behind it, at `position`, facing `target`. Every ray
    visibility is left on (a mesh's defaults: camera, diffuse, glossy, transmission, shadow), so it is seen, lights and
    casts shadows as one. (A Cycles AREA lamp of the same lighting reads about a tenth as bright seen head-on, so seen
    through a clear horn it does not stand for a lit diffuser.)"""
    import bmesh
    from mathutils import Vector
    w, h = p['size']; dpt = float(p.get('depth', 0.25))
    def hexlin(s):
        s = s.lstrip('#'); c = [int(s[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)
    em = bpy.data.materials.new(f'{name}-diffuser'); em.use_nodes = True; nt = em.node_tree
    b = nt.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1); b.inputs['Roughness'].default_value = 0.9
    b.inputs['Emission Color'].default_value = (*hexlin(p.get('color', '#FFFFFF')), 1); b.inputs['Emission Strength'].default_value = float(p['strength'])
    bk = bpy.data.materials.new(f'{name}-body'); bk.use_nodes = True
    bb = bk.node_tree.nodes['Principled BSDF']; bb.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1); bb.inputs['Roughness'].default_value = 0.8
    bm = bmesh.new()
    # the face at local z 0 facing -z (aim() turns -z to the target), the body behind it to +z
    v = [bm.verts.new(c) for c in ((-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0),
                                   (-w / 2, -h / 2, dpt), (w / 2, -h / 2, dpt), (w / 2, h / 2, dpt), (-w / 2, h / 2, dpt))]
    faces = [((0, 3, 2, 1), 0), ((4, 5, 6, 7), 1), ((0, 1, 5, 4), 1), ((1, 2, 6, 5), 1), ((2, 3, 7, 6), 1), ((3, 0, 4, 7), 1)]
    for idx, mi in faces:
        f = bm.faces.new([v[i] for i in idx]); f.material_index = mi
    bm.normal_update()
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(em); me.materials.append(bk)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p['position'])
    ob.rotation_euler = (Vector(p['target']) - ob.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()
    zs = [(ob.matrix_world @ vv.co).z for vv in me.vertices]
    print('SOFTBOX', name, 'face', w, 'x', h, 'strength', p['strength'], 'z', round(min(zs), 3), 'to', round(max(zs), 3))
    return [ob]
